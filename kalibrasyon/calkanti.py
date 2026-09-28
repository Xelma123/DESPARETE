"""
ÇALKANTI SAYISI Θ — mobilite m/s ile değil, PROTOKOLÜN ZAMANIYLA tanımlanır.

Üretici:
    PYTHONIOENCODING=utf-8 python kalibrasyon/calkanti.py

🔴 NEDEN BU ÖLÇÜM VAR
=====================
Mobilite bugüne kadar `gm_hiz_min/maks_ms` ile tanımlıydı ve o sayıların
hiçbir gerekçesi yoktu. Ölçüldü: bağıl hız **26,4 m/s**, rota ömrü **2,6 s**.

OLSR'ın `TOP_HOLD_TIME`ı **15 s**tir (RFC 3626). Yani topoloji bilgisi
**kullanılmadan bayatlıyor**: OLSR bir rotayı öğrenip kullanamadan o rota
çoktan yok olmuş oluyor. Bu, OLSR'ın tasarımının değil **bizim kurulumumuzun**
sonucudur — yani kurulum yüzünden zayıflatılmış bir taban çizgisi, straw-man.

🔒 ÇALKANTI SAYISI
==================
    Θ = ortalama rota ömrü / en yavaş taban çizgisinin topoloji zamanı
      = τ_rota / 15 s

    Θ = ∞    durgun — topoloji değişmez, referans nokta
    Θ ≈ 10   protokol bilgisi çoğu zaman TAZE — gerçekçi seyir
    Θ ≈ 3    bilgi zamanın üçte birinde bayat — zorlayıcı ama ADİL
    Θ < 1    🔴 protokoller çalışamaz; karşılaştırma değil, kurulum hatası

**Hızlar Θ'dan TÜRETİLİR.** Ölçüt doğrulanmamış bir menzil ya da hız
sayısına değil, **RFC'nin kendi tablosuna** dayanır — ve taban çizgilerinin
zayıflatılmadığını garanti eden tek şey onların kendi zaman sabitleridir.

⚠️ ÇAPRAZ KONTROL — ölçek
=========================
Seçilen Θ'ya karşılık gelen hızlar, `olcek` uygulanınca doğrulanmış İHA hız
aralığına (30–400 km/h, kaynak A5a) düşmelidir. Düşmezse ya Θ ya ölçek
yanlıştır ve ikisi de kayda geçer.

🔴 BU BETİK ARTIK KARAR ÜRETMİYOR — 9 Eylül 2026
================================================
Başlığı şunu taahhüt ediyordu: *"TARAMA sert diskle yapılır; SEÇİLEN nokta
sonra kanal tabanlı grafikle DOĞRULANIR."* **O doğrulama depoda YOKTU.**
Yazıldı (`kalibrasyon/bag_kumesi.py` §F–§H) ve iki şey ortaya çıktı:

  1. 🔒 Disk yaklaşımı SIRALAMA için tutuyor: sönümlemesiz kanal grafiği
     Θ = 5,21, disk 5,93 — %14 fark.
  2. 🔴 Ama DEĞER için tutmuyor: disk gölgelemeyi hiç görmediği için rota
     ömrünü **iki kat uzun** gösteriyor (89 s ↔ 43 s). Fiziksel olarak doğru
     tanım YAVAŞ SINR'dir — `kopma_fiziksel` için zaten ilan edilmiş olan.

⚠️ VE İKİ KESTİRİCİ YANLILIĞI VARDI, ikisi de Θ'yı DÜŞÜK gösteriyor:
soldan kesme (t = 0'da var olan rotanın yaşı bilinmiyor) ve sağdan sansür
(koşu bitince yaşayan rota "ölmüş" sayılıyor — burada, `rota_omurleri`nin
sonundaki *"kırpılmış (sansürlü)"* satırı). Düzeltilmiş türetme
`bag_kumesi.py §H`de: ilk ömür atılır, sansür Kaplan–Meier ile giderilir.

🔒 HIZLAR ORADAN GELİR. Bu betik bir HIZLI TARAMA aleti olarak kalıyor —
sıralama doğru, mutlak değer iyimser. Ürettiği Θ değerleri bir TEŞHİSTİR.

    disk (bu betik)          çekirdek kol Θ = 5,93  ← iyimser
    yavaş SINR + Kaplan-Meier             Θ = 3,25  ← KARAR bundan
    kapı                                  Θ ≥ 3

⚠️ MARJ DAR: %8. Çalışma noktasını değiştiren her şey (alan, güç, gölgeleme
σ'sı) bu marjı yeniden sınamayı gerektirir.
"""

from __future__ import annotations

import random
import statistics as ist
import sys
from collections import deque
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import mesafe  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)

# 🔒 OLSR RFC 3626 varsayılanı. Θ'nın paydası budur ve ELLE SEÇİLMEDİ:
# en yavaş taban çizgisinin kendi zaman sabitidir.
OLSR_TOP_HOLD_S: float = 15.0

# Etkin bağ yarıçapı — `kalibrasyon/calisma_noktasi.py`de ölçülen kanal
# tabanlı dereceyi veren eşdeğer disk. Tarama için yeterli yaklaşım.
ETKIN_YARICAP_M: float = 400.0

ADIM_S: float = 1.0          # rota ömrü örnekleme adımı
BITIS_S: float = 350.0
CIFT_SAYISI: int = 40        # tohum başına izlenen kaynak-hedef çifti
TOHUMLAR = range(1000, 1006)


def _komsuluk(konumlar, yaricap_m):
    n = len(konumlar)
    kom = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if mesafe(konumlar[i], konumlar[j]) <= yaricap_m:
                kom[i].add(j)
                kom[j].add(i)
    return kom


def _yol(kom, kaynak, hedef):
    onceki = {kaynak: None}
    kuyruk = deque([kaynak])
    while kuyruk:
        u = kuyruk.popleft()
        if u == hedef:
            break
        for v in sorted(kom[u]):
            if v not in onceki:
                onceki[v] = u
                kuyruk.append(v)
    if hedef not in onceki:
        return None
    yol = [hedef]
    while yol[-1] != kaynak:
        yol.append(onceki[yol[-1]])
    return tuple(reversed(yol))


def olc(hiz_min: float, hiz_maks: float, senaryo: str = "bagimsiz-yok",
        yaricap_m: float = ETKIN_YARICAP_M, **ek) -> dict[str, float]:
    """Bir hız ayarında bağıl hız, bağ ömrü ve ROTA ÖMRÜ."""
    bagil, rota_omurleri, atlamalar = [], [], []
    for tohum in TOHUMLAR:
        kfg = DS.konfig(kol="calkanti", senaryo=senaryo, tohum=tohum,
                     gm_hiz_min_ms=hiz_min, gm_hiz_maks_ms=hiz_maks,
                     gm_hiz_sigma_ms=max(hiz_maks / 10.0, 1e-4),
                     gorev_jitter_hiz_ms=max(hiz_maks / 15.0, 1e-4), **ek)
        top = topoloji_kur(kfg, Akislar(tohum))
        n = kfg.dugum_sayisi
        adet = int(BITIS_S / ADIM_S)
        konum = [[top.konum(i, k * ADIM_S) for i in range(n)]
                 for k in range(adet)]
        kom = [_komsuluk(konum[k], yaricap_m) for k in range(adet)]

        # --- bağıl hız (komşu çiftler) --------------------------------
        for k in range(0, adet - 1, 10):
            for i in range(n):
                for j in kom[k][i]:
                    if j <= i:
                        continue
                    d = [((konum[k + 1][i].x - konum[k][i].x)
                          - (konum[k + 1][j].x - konum[k][j].x)) / ADIM_S,
                         ((konum[k + 1][i].y - konum[k][i].y)
                          - (konum[k + 1][j].y - konum[k][j].y)) / ADIM_S,
                         ((konum[k + 1][i].z - konum[k][i].z)
                          - (konum[k + 1][j].z - konum[k][j].z)) / ADIM_S]
                    bagil.append(sum(x * x for x in d) ** 0.5)

        # --- rota ömrü ------------------------------------------------
        rnd = random.Random(tohum)
        for _ in range(CIFT_SAYISI):
            kaynak, hedef = rnd.sample(range(n), 2)
            yol, sure = None, 0.0
            for k in range(adet):
                if yol is None:
                    yol = _yol(kom[k], kaynak, hedef)
                    if yol is not None:
                        atlamalar.append(len(yol) - 1)
                        sure = 0.0
                    continue
                if all(yol[z] in kom[k][yol[z - 1]]
                       for z in range(1, len(yol))):
                    sure += ADIM_S
                else:
                    rota_omurleri.append(sure)
                    yol = None
            if yol is not None and sure > 0.0:
                rota_omurleri.append(sure)   # ⚠️ kırpılmış (sansürlü)
    tau = ist.mean(rota_omurleri) if rota_omurleri else float("nan")
    return {"bagil_hiz_ms": ist.mean(bagil) if bagil else 0.0,
            "rota_omru_s": tau,
            "theta": tau / OLSR_TOP_HOLD_S,
            "atlama": ist.mean(atlamalar) if atlamalar else float("nan")}


def _bolum(baslik: str) -> None:
    print()
    print("=" * 78)
    print(baslik)
    print("=" * 78)


def tarama() -> None:
    _bolum("1 - HIZ TARAMASI  (Θ = rota omru / OLSR TOP_HOLD_TIME)")
    kfg = DS.konfig(kol="calkanti")
    print(f"  alan {kfg.alan_en_m:.0f} m · etkin yaricap {ETKIN_YARICAP_M:.0f} m"
          f" · {len(list(TOHUMLAR))} tohum · {BITIS_S:.0f} s")
    print(f"  OLSR TOP_HOLD_TIME = {OLSR_TOP_HOLD_S:.0f} s  (RFC 3626)\n")
    print(f"  {'hiz m/s':>14} {'bagil':>8} {'rota_omru':>10} {'Θ':>8} "
          f"{'atlama':>8} {'rejim':>12}")
    adaylar = ((10.0, 30.0), (2.0, 6.0), (1.0, 3.0), (0.5, 1.5),
               (0.25, 0.75), (0.12, 0.36), (0.06, 0.18))
    for hmin, hmaks in adaylar:
        s = olc(hmin, hmaks)
        theta = s["theta"]
        rejim = ("🔴 YASAK" if theta < 1.0
                 else "zorlayici" if theta < 6.0
                 else "gercekci" if theta < 20.0 else "neredeyse durgun")
        print(f"  {f'{hmin}-{hmaks}':>14} {s['bagil_hiz_ms']:>8.2f} "
              f"{s['rota_omru_s']:>10.1f} {theta:>8.2f} {s['atlama']:>8.2f} "
              f"{rejim:>12}")
    print("\n  🔴 Bugunku ayar (10-30 m/s) YASAK bolgede: OLSR'in topoloji")
    print("     bilgisi kullanilmadan bayatliyor ve taban cizgisi kurulum")
    print("     yuzunden zayiflatilmis oluyor.")


def olcek_kontrolu() -> None:
    """⚠️ Seçilen hızlar, ölçek uygulanınca gerçek İHA hızına düşüyor mu?"""
    _bolum("2 - OLCEK CAPRAZ KONTROLU  (dogrulanmis IHA hizi 30-400 km/h)")
    print(f"  {'sim m/s':>12} {'x50 → km/h':>14} {'x30 → km/h':>14} "
          f"{'A5a araliginda mi':>20}")
    for h in (0.06, 0.12, 0.25, 0.5, 1.0, 2.0, 6.0, 30.0):
        k50 = h * 50.0 * 3.6
        k30 = h * 30.0 * 3.6
        icinde = "evet" if 30.0 <= k50 <= 400.0 else "🔴 HAYIR"
        print(f"  {h:>12.2f} {k50:>14.0f} {k30:>14.0f} {icinde:>20}")
    print("\n  🔒 Olcek bir RAPORLAMA parametresidir; fizigi degistirmez.")
    print("     Ama secilen hiz, makul bir olcekte gercek IHA hizina")
    print("     denk DUSMELIDIR — dusmuyorsa ya Θ ya olcek yanlistir.")


if __name__ == "__main__":
    BOLUMLER = {"1": tarama, "2": olcek_kontrolu}
    secim = sys.argv[1:] or list(BOLUMLER)
    for s in secim:
        BOLUMLER[s]()
