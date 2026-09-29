"""
ÖLÇÜM PENCERESİ KAPSAMI — `08` madde 31'in üreticisi.

🔴 NEDEN BU DOSYA VAR — F-4 (`10` §8)
=====================================
`08` madde 31 şunu iddia ediyor:

    "Ölçüldü (5 kol × 8 yapılandırma = 40 tam koşu): kontrol baytının
     **%17,63-22,84'ü** ölçüm penceresi DIŞINDA üretiliyor ve çarpıklık
     KOLA GÖRE değişiyor (`gurultuden_kacan`/`dongu_yapan` 1,004-1,047 ·
     `hedefe_en_yakin`/`en_kisa_yol` 1,054-1,079) — yani eşleştirilmiş bir
     kol karşılaştırması YANLIDIR."

ve üreticisi olarak `python scratchpad/b105_pencere.py` yazıyor.
🔴 **`scratchpad/` dizini depoda YOK** — sayı üretilemiyor (F-4).

⚠️ MATRİS YENİDEN İLAN EDİLDİ
==============================
Kayıp üreticinin "8 yapılandırma"sının ne olduğu **hiçbir belgede yazılı
değil**. Uydurmak `03` kural 1'in daha ağır ihlali olurdu (K-053: eski bir
kayda üretici komut UYDURMAK yasak). Bu yüzden matris burada AÇIKÇA
yeniden ilan ediliyor:

    5 kol × 2 senaryo (S0 · S2) × 3 trafik × **30 tohum** = 900 tam koşu

Çıkan sayı eskisinden farklıysa **`08` güncellenir** ve fark `04`e yazılır
(Y14). Amaç eski sayıyı tutturmak değil, ÜRETİLEBİLİR bir sayı koymak.

🔴 NEDEN BU BÜYÜKLÜK ÖNEMLİ
============================
`03` Bölüm C sözleşme 4: *"tüm sayaçlar aynı pencereden"*. Kümülatif bir
sayacın tüm koşu hâli ısınmayı da içerir; ısınma **asimetriktir** ve
protokoller farklı hızda yakınsar. Pencere dışı payın KOLA GÖRE değişmesi,
tüm koşu hâliyle yapılan eşleştirilmiş bir karşılaştırmayı YANLI yapar.

Kullanım:
    python dogrulama/pencere_kapsami.py --tahmin
    python dogrulama/pencere_kapsami.py
"""

from __future__ import annotations

import statistics as ist
import sys
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import AKTARICILAR                     # noqa: E402
# 🔴 B-168: DV `AKTARICILAR`da YOK; `gecerlilik.py` ile AYNI kaynaktan.
from dogrulama.kontrol_payi import mesafe_vektoru                  # noqa: E402
from dogrulama.olcum import kayit, olc, yaz_sonuc                  # noqa: E402
from sim.config import Konfig                                      # noqa: E402

CEKIRDEK = min(10, cpu_count())
# 🔴 B-123 (yedinci denetim) — TEK TOHUMDAN 30 TOHUMA.
# Önceki hâli `TOHUM = 1` idi ve `08` md 31 o tek tohumdan yazılmıştı.
# `03` kural 2: *"tek/az tohumlu sonuç raporlama; ≥30 tohum"*. Aynı
# oturum md 25'i 3 tohumdan 30'a taşırken bu maddeye 1 tohumluk bir
# band yazmıştı — kural bir nesneye uygulanıp yanındakine
# uygulanmamıştı. Denetim ölçtü: 5 tohumda band iki uçtan da
# genişliyor (%16,62–23,03), yani tek tohum bandı DAR gösteriyor.
TOHUMLAR = range(1, 31)         # ayarlama kümesi (K-025)
# 🔴 B-168 (SEKIZINCI DENETIM) — BAGLAYICI KOL BU ARACTA YOKTU.
#
# Depoda UC ayri kol kaydi vardi ve ikisi DV'yi gormuyordu:
#     AKTARICILAR             5 kol, DV YOK
#     gecerlilik.KOLLAR       3 kol, DV VAR   <- `06` kosul 3
#     pencere_kapsami.KOLLAR  5 kol, DV YOK   <- `08` md 31
#
# B-135 DV'yi *"kosul 3'un BAGLAYICI cifti"* ilan etti ve `gecerlilik.py`ye
# ekledi; `08` md 31'in pencere carpikligi bandini uretent BU dosya
# guncellenmedi. Sonucu: **baglayici ilan edilen kolun pencere kapsami
# hic olculmemisti** — ve `08` md 31 tam olarak *"Aile 1'in her
# karsilastirmasi `*_pencere` alanlarini kullanmak ZORUNDA"* diyor.
# Orintunun ("bir kurali bir nesneye uygulayip komsusuna uygulamamak")
# bir ornegi daha: B-135 bir sozluge uygulandi, komsusuna uygulanmadi.
#
# 🔒 `AKTARICILAR` DOKUNULMADI (K-088'in gerekcesi gecerli: kapinin Ç1 uc
# durum matrisi o sozlugu ada gore kullaniyor). Bu dosya `gecerlilik.py`
# ile AYNI deseni izler: kendi kayit sozlugu.
KOLLAR: dict[str, object] = {**AKTARICILAR, "DV": mesafe_vektoru}   # 6 kol
SENARYOLAR = ("S0", "S2")
TRAFIKLER = ("seyrek", "orta", "yogun")

# Pencere ikizi olan ve BU ölçümün ilgilendiği sayaçlar. Kontrol baytı
# birincil; ötekiler çarpıklığın yalnızca kontrol düzlemine mi özgü
# olduğunu gösteriyor (Y8: tek büyüklük ölçen bir tarama, o büyüklüğün
# özel olup olmadığını söyleyemez).
SAYACLAR = ("kontrol_bayt", "veri_bayt", "kontrol_airtime_s",
            "beacon_gonderilen", "mac_deneme")


def _isler() -> list[tuple]:
    return [({"kol_adi": kol, "senaryo_etiket": sen, "trafik_etiket": tr},
             dict(senaryo=sen, trafik=tr, tohum=t), kol)
            for kol in KOLLAR for sen in SENARYOLAR for tr in TRAFIKLER
            for t in TOHUMLAR]


def _kosu(arg) -> tuple[dict, dict]:
    """İŞÇİ — yazıcısız ölçer, TAM sonucu döndürür (D-13)."""
    etiketler, kwargs, kol = arg
    return etiketler, olc(Konfig(kol="pencere_kapsami", **kwargs),
                          KOLLAR[kol], aktarici=kol)


def dis_pay(sonuc: dict, sayac: str) -> float | None:
    """Sayacın ölçüm penceresi DIŞINDA üretilen payı, yüzde."""
    tum = sonuc.get(sayac)
    pen = sonuc.get(f"{sayac}_pencere")
    if not tum or pen is None:
        return None
    return 100.0 * (tum - pen) / tum


def carpiklik(sonuc: dict, sayac: str) -> float | None:
    """Tüm koşu / pencere oranı — `08` md 31'in "çarpıklık" büyüklüğü."""
    tum = sonuc.get(sayac)
    pen = sonuc.get(f"{sayac}_pencere")
    if not tum or not pen:
        return None
    return tum / pen


def _kalibrasyon_ornekleri(isler: list[tuple]) -> list[tuple]:
    """Kalibrasyon icin UC EKSENI DE ornekleyen is listesi (B-154 ikizi).

    🔒 AYRI FONKSIYON (`03` B5): `main()` icinde kalsaydi capa testi onu
    goremezdi — dosyanin kendi kapsam tablosu *"main() cagrilmiyor"*
    diyor.
    """
    return [next(i for i in isler
                 if i[0]["kol_adi"] == kol
                 and i[0]["senaryo_etiket"] == sen
                 and i[0]["trafik_etiket"] == tr)
            for kol in KOLLAR for sen in SENARYOLAR for tr in TRAFIKLER]


def main(argv: list[str]) -> int:
    isler = _isler()
    print("ÖLÇÜM PENCERESİ KAPSAMI — `08` madde 31")
    print(f"{len(KOLLAR)} kol × {len(SENARYOLAR)} senaryo × "
          f"{len(TRAFIKLER)} trafik × {len(TOHUMLAR)} tohum = "
          f"{len(isler)} tam koşu | tohum "
          f"{TOHUMLAR.start}-{TOHUMLAR.stop - 1}")

    # 🔴 KALİBRASYON İŞ LİSTESİNİN İLKİNDE YAPILMAZ — ölçüldü, tutmadı.
    # `_isler()` sıralı üretiyor ve ilk iş DAİMA en ucuz hücre
    # (`seyrek` trafik). Tek o işten kurulan tahmin 900 koşu için
    # "1,8-3,8 dk" dedi; gerçek koşu 10 dk'da BİTMEDİ. Bu, deponun
    # "süre tahmini beş kez tutmadı" örüntüsünün altıncısıdır.
    # 🔒 Tahmin artık ÜÇ TRAFİK SEVİYESİNDEN birer işle kurulur ve
    # ortalama DEĞİL, hücre başına ortalama × iş sayısı kullanılır.
    # KOL x TRAFIK: maliyet ikisine birden bağlı. Yalnız trafik
    # örneklemek de yetmedi — `en_kisa_yol` (kâhin, kısa yollar) ile
    # `dongu_yapan`/`gurultuden_kacan` arasında koşu maliyeti farkı var.
    # 🔴 B-154'UN IKIZI (sekizinci denetim, B0.9'da olculdu):
    # `_isler()` SIRALI uretiyor ve `next(...)` daima ILK eslesen isi
    # aliyor -> senaryo DAIMA S0. Yani kalibrasyon KOL x TRAFIK'i
    # ornekliyordu ama SENARYO eksenini orneklemiyordu. `gecerlilik.py`de
    # ayni kusur olculdu ve ortalama kosu uzunlugunu %9,1 IYIMSER
    # gosteriyordu. Burada senaryo kosu SURESINI degistirmiyor ama
    # MALIYETI degistiriyor (S2'de daha cok yeniden deneme).
    # 🔒 Uc eksen de orneklenir.
    ornekler = _kalibrasyon_ornekleri(isler)
    t0 = time.perf_counter()
    for o in ornekler:
        _kosu(o)
    tek = (time.perf_counter() - t0) / len(ornekler)
    alt = len(isler) * tek / CEKIRDEK / 60.0
    print(f"kalibrasyon: {len(ornekler)} hücre ortalaması {tek:.2f} sn/koşu")
    print(f"TAHMIN BANDI: {alt:.1f} - {alt * 2.10:.1f} dk (K-075)")
    if "--tahmin" in argv:
        print("(--tahmin: yalnızca tahmin istendi, koşulmadı)")
        return 0

    veri: dict = {}
    with kayit("pencere_kapsami") as yazici:
        with Pool(min(CEKIRDEK, len(isler))) as p:
            for et, sonuc in p.imap(_kosu, isler, chunksize=1):
                yaz_sonuc(sonuc, yazici=yazici, **et)
                veri[(et["kol_adi"], et["senaryo_etiket"],
                      et["trafik_etiket"], sonuc["konfig"]["tohum"])] = sonuc
        yazilan = yazici.yazilan
    assert yazilan == len(isler), (
        f"yazılan satır ({yazilan}) iş sayısına ({len(isler)}) eşit değil "
        f"— D-13 sınıfı bir kaçak var")
    print(f"yazılan satır: {yazilan} | korunum: "
          f"{sum(s['korunum']['korunum_tamam'] for s in veri.values())}"
          f"/{len(veri)}")

    print()
    print("=" * 88)
    print("PENCERE DIŞI PAY — sayaç bazında (tüm hücreler)")
    print("=" * 88)
    print(f"{'sayaç':<20}{'en küçük %':>13}{'en büyük %':>13}"
          f"{'ortanca %':>12}{'hücre':>8}")
    for sayac in SAYACLAR:
        paylar = [d for s in veri.values()
                  if (d := dis_pay(s, sayac)) is not None]
        if paylar:
            print(f"{sayac:<20}{min(paylar):>13.2f}{max(paylar):>13.2f}"
                  f"{ist.median(paylar):>12.2f}{len(paylar):>8}")

    print()
    print("=" * 88)
    print("🔴 ÇARPIKLIK KOLA GÖRE DEĞİŞİYOR MU  (kontrol_bayt, tüm koşu / pencere)")
    print("Değişiyorsa, tüm koşu hâliyle yapılan eşleştirilmiş bir kol")
    print("karşılaştırması YANLIDIR — `08` md 31'in bağlayıcı cümlesi.")
    print("=" * 88)
    print(f"{'kol':<20}{'en küçük':>12}{'en büyük':>12}{'pencere dışı %':>17}")
    kol_araliklari = {}
    for kol in KOLLAR:
        c = [d for (k, _s, _t, _n), s in veri.items() if k == kol
             and (d := carpiklik(s, "kontrol_bayt")) is not None]
        pay = [d for (k, _s, _t, _n), s in veri.items() if k == kol
               and (d := dis_pay(s, "kontrol_bayt")) is not None]
        if c:
            kol_araliklari[kol] = (min(c), max(c))
            print(f"{kol:<20}{min(c):>12.4f}{max(c):>12.4f}"
                  f"{f'{min(pay):.2f} - {max(pay):.2f}':>17}")

    if len(kol_araliklari) > 1:
        alt_uc = min(a for a, _b in kol_araliklari.values())
        ust_uc = max(b for _a, b in kol_araliklari.values())
        print()
        print(f"  🔴 KOLLAR ARASI ÇARPIKLIK AÇIKLIĞI: "
              f"{alt_uc:.4f} - {ust_uc:.4f}")
        ayrik = [k for k, (a, b) in kol_araliklari.items()
                 if a > max(x[1] for kk, x in kol_araliklari.items() if kk != k)]
        print(f"  Aralıkları HİÇ ÖRTÜŞMEYEN kol: {ayrik if ayrik else 'yok'}")
    # ----------------------------------------------------------------
    # 🔴 Y7 — ARAÇ NE ÖLÇTÜĞÜNÜ KENDİSİ DOĞRULAR (analitik çapa)
    #
    # ⚠️ BU BLOK B-120 İLE DÜZELTİLDİ (yedinci bağımsız denetim).
    #
    # Önceki hâli iki `assert` taşıyordu ve ikincisi YANLIŞTI: bütün
    # kolların çarpıklığını `[olcum_bitis/pencere, kosu_bitis/pencere]`
    # bandına hapsediyor ve bandı "ANALİTİK" diye adlandırıyordu.
    #
    # 🔴 O band analitik DEĞİLDİR — üç varsayıma dayanır ve üçü de kırılır:
    #   (i)   sayaç zamanda DÜZGÜN üretilir
    #   (ii)  üretim [0, kosu_bitis] aralığındadır
    #   (iii) pencere [isinma_s, olcum_bitis]'tir
    #
    # Denetim üç yoldan kırdı (hepsi ölçüldü):
    #   1. Aracın KENDİ çıktısında `beacon_gonderilen` 1,2942-1,3398
    #      (üstten) · `veri_bayt` ve `mac_deneme` 1,1786-1,2573 (alttan)
    #   2. `hedefe_en_yakin`/S2/orta/**tohum 4** -> 1,299260 > 1,296296
    #      => eski `assert` bu tohumda aracı ÇÖKERTİYORDU
    #   3. `isinma_s` = 5/15/25'te çarpıklık 1,0144/1,0446/1,0766 çıkıyor
    #
    # 🔒 KORUNAN kısım DOĞRUDUR ve kalıyor: `olu` kolu hiç veri
    # göndermez, YALNIZCA beacon üretir; beacon [0, kosu_bitis]'te
    # düzgündür, dolayısıyla oranı üst çapaya BİREBİR oturmak zorundadır.
    # Oturmuyorsa ölçülen şey çarpıklık değildir. O `assert` KALIR.
    #
    # 🔴 Diğer kollar için band bir BEKLENTİ, bir sınır değildir —
    # raporlanır, dayatılmaz (`03` kural 13: fiziksel sezgiyle çelişen
    # bir sonucu KURULUMU denetlemeden açıklamaya çalışma).
    # ----------------------------------------------------------------
    ornek = next(iter(veri.values()))
    bas_s, bit_s = ornek["olcum_penceresi_s"]
    pencere_uz = bit_s - bas_s
    kon = ornek["konfig"]
    ust_capa = kon["kosu_bitis_s"] / pencere_uz          # yalnız beacon
    alt_capa = kon["olcum_bitis_s"] / pencere_uz         # yalnız onay
    print()
    print("=" * 88)
    print("🔴 Y7 — ANALİTİK ÇAPA (araç ölçtüğünü iddia ettiği şeyi ölçüyor mu)")
    print("=" * 88)
    print(f"  düzgün beacon beklentisi (üst çapa): {ust_capa:.4f}")
    print(f"  düzgün onay   beklentisi (alt çapa): {alt_capa:.4f}")

    # 🔒 TEK ZORLAYICI DEĞİŞMEZ — ve gerçekten analitik olan tek şey.
    olu_hucreler = [d for (k, _s, _t, _n), s in veri.items() if k == "olu"
                    and (d := carpiklik(s, "kontrol_bayt")) is not None]
    if olu_hucreler:
        sapma = max(abs(c - ust_capa) for c in olu_hucreler)
        print(f"  `olu` kolu (yalnız beacon, hiç veri yok): "
              f"{len(olu_hucreler)} hücre · en büyük sapma {sapma:.6f}  "
              f"{'✅ BİREBİR' if sapma < 1e-3 else '🔴 TUTMUYOR'}")
        assert sapma < 1e-3, (
            f"`olu` kolunun çarpıklığı düzgün beacon beklentisine "
            f"({ust_capa:.4f}) oturmuyor (en büyük sapma {sapma:.6f}) — "
            f"ölçülen şey çarpıklık DEĞİL (Y7)")

    # 🔴 ZORLAMA YOK — GÖZLEM. Bandın dışına çıkan kol bir HATA değil,
    # o sayacın zamanda düzgün üretilmediğinin kanıtıdır ve raporlanır.
    disarda = {k: v for k, v in kol_araliklari.items()
               if v[0] < alt_capa - 1e-9 or v[1] > ust_capa + 1e-9}
    print(f"  beklenti bandının [{alt_capa:.4f}, {ust_capa:.4f}] DIŞINDA "
          f"kalan kol: {disarda if disarda else 'yok'}")
    if disarda:
        print("    ⚠️ Bu bir HATA DEĞİLDİR: band yalnızca DÜZGÜN üretilen")
        print("       bir sayaç için geçerlidir. Dışarı çıkan kol, kontrol")
        print("       baytını zamanda düzgün üretmiyor demektir (B-120).")

    print()
    print("🔒 Y14: `sim/` altında bir maliyet değişikliği olduğunda BU KOMUT")
    print("   YENİDEN KOŞULUR ve `08` madde 31 güncellenir.")
    return 0


if __name__ == "__main__":       # Windows `spawn` — devir teslim §6.2
    raise SystemExit(main(sys.argv[1:]))
