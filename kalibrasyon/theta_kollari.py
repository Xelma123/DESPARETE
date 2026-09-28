"""
Θ KOLLARI — mobilite kolu başına rota ömrü ve Θ (Y7 · C4).

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/theta_kollari.py

Bağlam: `v2/07-SIMULATOR-TASARIMI.md` §03.3 · §18 Y7 · `v2/04` K-101, K-122.

🔒 İKİNCİ BİR KESTİRİCİ YAZILMADI
=================================
Ölçüm gövdesi `bag_kumesi.py::_is_theta_hiz`tir — K-101'in hızları ondan
türetildi. Burada yalnız SENARYO değişiyor; bağ tanımı (yavaş SINR ≥ eşik,
`kopma_fiziksel` ile AYNI), soldan kesme (her çiftin ilk ömrü atılır) ve
sağdan sansür düzeltmesi (Kaplan–Meier) aynen geçerli.

🔒 İKİ PAYDA, İKİ SORU
======================
    Θ_OLSR = τ / 15 s   OLSR `TOP_HOLD_TIME` — topoloji bilgisinin ömrü
    Θ_AODV = τ /  3 s   AODV `ACTIVE_ROUTE_TIMEOUT` — rotanın ömrü
`03` §03.3 ikisinin birden raporlanmasını istiyor: bir kol OLSR'ın zarfının
dışında kalırken AODV'ninkinin içinde olabilir ve bu bir BULGUDUR.

⚠️ Statik kolda hiçbir rota KOPMAZ: soldan kesme kuralı yüzünden ölçülebilir
ömür kalmaz ve Θ tanımsızdır. Bu bir eksiklik değil, kolun tanımıdır; tabloda
`None` ile ve gerekçesiyle durur.
"""

from __future__ import annotations

import statistics as ist
import sys
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from kalibrasyon.bag_kumesi import _is_theta_hiz, _km_ortalama  # noqa: E402
from kalibrasyon.calkanti import (ADIM_S, BITIS_S, CIFT_SAYISI,  # noqa: E402
                                  OLSR_TOP_HOLD_S, TOHUMLAR)
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from sim2.yapilandirma.senaryolar import MOBILITE_KOLLARI  # noqa: E402

# 🔒 RFC 3561 §10 · AODV `ACTIVE_ROUTE_TIMEOUT` = 3 000 ms. Birincil belge
# `02` §R1'de doğrulandı — `olcum/evre.py::IZGARA_ADIMI_S` ile aynı kaynak.
AODV_ACTIVE_ROUTE_S: float = 3.0


def kol_olcumu(isci: int = 6) -> dict[str, dict[str, float | None]]:
    """Her mobilite kolunda rota ömrü; Θ iki paydayla birlikte."""
    k0 = DS.konfig(kol="theta_kollari")
    tohumlar = list(TOHUMLAR)
    kollar = [f"{m}-yok" for m in MOBILITE_KOLLARI]
    print("Θ KOLLARI — mobilite kolu basina rota omru (Y7 · C4)")
    print(f"  bag tanimi: YAVAS SINR >= {k0.sinr_esigi_db:.0f} dB · "
          f"{len(tohumlar)} tohum · adim {ADIM_S:.1f} s · bitis {BITIS_S:.0f} s "
          f"· {CIFT_SAYISI} cift")
    print(f"  hizlar {k0.gm_hiz_min_ms}-{k0.gm_hiz_maks_ms} m/s (varsayilan) · "
          f"paydalar OLSR {OLSR_TOP_HOLD_S:.0f} s · AODV "
          f"{AODV_ACTIVE_ROUTE_S:.0f} s")
    print()

    gorevler = [(t, k0.gm_hiz_min_ms, k0.gm_hiz_maks_ms, ADIM_S, BITIS_S,
                 CIFT_SAYISI, kol) for kol in kollar for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_theta_hiz, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:200]}")
        return {}

    print(f"  {'kol':>11} {'atlama':>7} {'omur':>6} {'kopmayan':>9} "
          f"{'tau_ham':>8} {'tau_KM':>8} {'sansur':>7} {'Θ_OLSR':>8} "
          f"{'Θ_AODV':>8}")
    tablo: dict[str, dict[str, float | None]] = {}
    for ki, kol in enumerate(kollar):
        sureler, sansur, atlama = [], [], []
        cift = kopan = 0
        for si in range(len(tohumlar)):
            s, _h = ham[ki * len(tohumlar) + si]
            sureler += s["sure"]
            sansur += s["sansur"]
            atlama += s["atlama"]
            cift += s["cift"]
            kopan += s["kopan_cift"]
        kopmayan = 1.0 - kopan / cift
        mobilite = kol.split("-")[0]
        if not sureler:
            print(f"  {mobilite:>11} {ist.mean(atlama) if atlama else 0:>7.2f} "
                  f"{0:>6} {kopmayan:>8.1%}        —        —       —"
                  f"        —        —   (hic kopma yok)")
            # 🔴 `kopmayan` BU DALDA DA YAZILIR — 16 Eylül 2026.
            # Üç elemanlı demet basmaya geçerken (K-130) bu dal atlanmıştı ve
            # `KeyError: 'kopmayan'` veriyordu; hiç kopma olmayan kolda
            # (statik) ateşleniyordu. ⚠️ Aleti DEĞİŞTİRİP KOŞMAMIŞTIM; hatayı
            # üretici duman kapısı yakaladı — K-129'un dersi bu kez bana
            # uygulandı: koşulmayan kapı kapı değildir.
            tablo[mobilite] = {"tau_km_s": None, "theta_olsr": None,
                               "theta_aodv": None, "kopmayan": kopmayan}
            continue
        tau_km = _km_ortalama(sureler, sansur)
        t_olsr = tau_km / OLSR_TOP_HOLD_S
        t_aodv = tau_km / AODV_ACTIVE_ROUTE_S
        print(f"  {mobilite:>11} {ist.mean(atlama):>7.2f} {len(sureler):>6} "
              f"{kopmayan:>8.1%} {ist.mean(sureler):>8.1f} {tau_km:>8.1f} "
              f"{sum(sansur) / len(sansur):>6.1%} {t_olsr:>8.2f} "
              f"{t_aodv:>8.2f}")
        tablo[mobilite] = {"tau_km_s": tau_km, "theta_olsr": t_olsr,
                           "theta_aodv": t_aodv, "kopmayan": kopmayan}
    print()
    # 🔴 "KAPI" DEĞİL, "BEYAN EDİLEN EKSEN" — 16 Eylül 2026.
    # Θ ≥ 3 üç yerde (belge · bu çıktı · senaryo yorumları) "kapı" diye
    # anılıyordu ama HİÇBİR yerde uygulanmıyordu; ikisinin arası yanıltıcıdır.
    # Kodda uygulanmadı ve bu BİLİNÇLİ: çekirdek kol adayı `formasyon` bugün
    # 2,31 ile eşiğin altında ve kestiricinin AŞAĞI YANLI olduğu biliniyor
    # (çiftlerin %92,1'i hiç kopmuyor — aşağıdaki `kopmayan` sütunu). Bugün
    # kapıyı bağlamak, doğru işi kırmızıya boyayan bir kapı kurmak olurdu ve
    # insanları kapıyı görmezden gelmeye alıştıran şey tam olarak budur
    # (`v2/03` §2.1). Karar C4'ten (formasyon Θ'sının daha çok tohumla
    # yeniden ölçümü) sonra alınacak.
    print("  🔎 BEYAN EDILEN EKSEN: Θ_OLSR ≥ 3 (K-101). Altina dusen kol")
    print("     protokolu tasarim zarfinin DISINDA kosturur ve BULGU olarak")
    print("     raporlanir. KODDA UYGULANMIYOR — gerekce: C4 acik (`v2/12`).")
    print("  ⚠️ Θ YALNIZ GOZLENEN OMURLERDEN hesaplanir: her ciftin ILK omru")
    print("     atilir (yasi bilinmiyor) ve kosu sonunda yasayan rota")
    print("     sansurludur. 'kopmayan' sutunu yuksekse olcume yalniz esigin")
    print("     kiyisindaki cifler girmistir ve Θ ASAGI YANLIDIR.")
    print()
    # 🔒 ÜÇ ELEMANLI DEMET — 16 Eylül 2026. Burası İKİ eleman basıyordu ama
    # `senaryolar.MOBILITE_THETA` ÜÇ tutuyor (üçüncüsü `kopmayan`: Θ'nın kolu
    # ne kadar TEMSİL ettiğini söyler ve satırın kapsam bölümüne girer).
    # Eksik demet bir sonraki yeniden ölçümde ELLE tamamlanacaktı; elle
    # taşınan her etiket bir gün yanlış taşınır (`v2/03` §B5).
    print("  `senaryolar.MOBILITE_THETA` icin:")
    for mobilite, d in tablo.items():
        if d["tau_km_s"] is None:
            print(f'    "{mobilite}": (None, None, {d["kopmayan"]:.3f}),')
        else:
            print(f'    "{mobilite}": ({d["theta_olsr"]:.2f}, '
                  f'{d["theta_aodv"]:.2f}, {d["kopmayan"]:.3f}),')
    return tablo


if __name__ == "__main__":
    DS.secimi_oku()                         # Faz 4 (K-183): --dunya
    print(f"  DUNYA: {DS.secili()}")
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    kol_olcumu()
