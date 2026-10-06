"""
UZAMSAL YENİDEN KULLANIM MESAFESİ — Li replikasyonunun açık sınavı.

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/yeniden_kullanim.py

Bağlam: `v2/09-LI-REPLIKASYONU.md` §SONUÇ · K-108.

🔴 NEDEN VAR
============
Li replikasyonunda H1 tutmadı (0,074 ↔ ilan edilen band [0,10; 0,20]) ve
sebep ölçülerek bulundu: **uzamsal yeniden kullanım mesafesi 8 atlama**,
Li'nin modelinde 4. Bu, kapalı formda türüyor:

    girişim menzili / iletim menzili = 10^(SINR_eşiği / (10·α))

α = 2,0'de bu **6,31** ve ölçülen oran birebir 6,31 çıktı. Ama türetme, α
değiştiğinde de tutmak zorunda — yoksa tesadüf olabilir.

🔒 BU BETİK O ÖNGÖRÜYÜ SINAR — ve sınanan şey ORANTIDIR, toplamsal bir
sabit değil.

🔴 İLK YAZDIĞIM ÖLÇÜT YANLIŞTI ve kayda geçer. *"Yeniden kullanım mesafesi
= oran + 1 atlama"* diye bir sezgi yazmıştım; o sezgi α = 2'de tuttuğu için
doğru sanılmıştı. Üç α'da ölçülünce toplamsal sabitin tutmadığı, **oranın**
tuttuğu görüldü:

    α      girişim/iletim   ÖLÇÜLEN   ölçülen/oran
    2,0            6,31        8,0         1,268
    3,0            3,41        4,0         1,171
    4,0            2,51        3,0         1,194
                                  ortalama **1,211** · saçılma **%8**

🔒 Yani `yeniden kullanım mesafesi ≈ 1,21 × (girişim/iletim oranı)` ve çarpan
2,5 katlık bir oran aralığında %8 saçılmayla sabit. Çarpanın kendisi
TÜRETİLMEDİ, ÖLÇÜLDÜ — ve neden 1'den büyük olduğu açık: PER eğrisi sert bir
basamak değil, eşiğin biraz altında da bir miktar teslim var.

⚠️ Sınav bu yüzden çarpanın DEĞERİNİ değil, **SABİTLİĞİNİ** sınar: mekanizma
doğruysa çarpan α'dan bağımsız olmalıdır. Bir sayı uydurup ona bakmak,
ölçütü sonuca göre seçmek olurdu.

⚠️ ZİNCİRLE DEĞİL, İKİ ÇİFTLE ÖLÇÜLÜR — ve bu bilinçli. Zincir kuyruk,
uçtan uca gecikme ve çok atlamalı etkileri de taşır; ölçülmek istenen şey
YALNIZ *"iki iletim ne kadar uzaktan itibaren aynı anda başarılı olabiliyor"*.
İki çift o soruyu saf hâlde sorar.

🔒 Verici gücü α'dan TÜRETİLİR (`yayilim.py`: hedef alınan güç
`iletim_menzili_m`de eşiğe eşitlenir), dolayısıyla bağ her α'da çalışır ve
karşılaştırma adildir. Ölçüldü: α = 2 · 3 · 4'te verici sırasıyla
+0,03 · +24,50 · +48,97 dBm.

⚠️ α = 3 ve 4 bu projede KULLANILMIYOR — `07` §04 hava-hava serbest uzay
için α = 2,0'ı gerekçelendiriyor ve ölçek kapısı α = 3'ü zaten elemişti
(35 kW verici). Buradaki tarama bir ÖNERİ değil, türetmenin SINAVIDIR.
"""

from __future__ import annotations

import statistics as ist
import sys
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from kalibrasyon.iki_cift import TOHUMLAR, kos  # noqa: E402

BAG_M = 280.0
AYRIMLAR = (560.0, 840.0, 1120.0, 1680.0, 2240.0, 3360.0, 4480.0)
ALFALAR = (2.0, 3.0, 4.0)
# Yeniden kullanım sayılması için gereken toplam verim oranı. İki çift tam
# paralel çalışıyorsa 2,0; tamamen serileştirilmişse 1,0. Orta nokta.
ESIK = 1.5

# 🔒 ÇARPANIN α'DAN BAĞIMSIZ SAYILMASI İÇİN İZİN VERİLEN SAÇILMA.
# Sınanan şey çarpanın DEĞERİ değil (o ölçülüyor), α ile DEĞİŞMEMESİ.
# Izgara 1 atlama çözünürlüklü olduğu için 3 atlamalık bir ölçümde tek
# adımlık belirsizlik zaten ±%33'tür; sınır ondan dar seçilemez.
SACILMA_SINIRI = 1.35


def _is(gorev):
    cift, tohum, ayrim, alfa = gorev
    try:
        return kos(cift, tohum, ayrim, BAG_M, alfa), None
    except Exception as hata:                                # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def main(isci: int = 8) -> None:
    print("=" * 84)
    print("UZAMSAL YENIDEN KULLANIM MESAFESI — turetmenin sinavi")
    print("=" * 84)
    print("  🔒 SINANAN: mesafe, girisim/iletim oraniyla ORANTILI mi?")
    print("     (carpanin DEGERI degil, alfa'dan BAGIMSIZLIGI sinaniyor)")
    for a in ALFALAR:
        oran = 10 ** (16.0 / (10.0 * a))
        print(f"     alfa={a:.1f} → girisim/iletim = 10^(16/{10 * a:.0f}) "
              f"= {oran:.2f}")
    print()

    gorevler = [(1, t, 20000.0, a) for a in ALFALAR for t in TOHUMLAR]
    gorevler += [(2, t, ay, a) for a in ALFALAR for ay in AYRIMLAR
                 for t in TOHUMLAR]
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)

    n = len(TOHUMLAR)
    tabanlar = {}
    for k, a in enumerate(ALFALAR):
        v = [x for x, e in ham[k * n:(k + 1) * n] if e is None]
        tabanlar[a] = ist.mean(v) if v else None
    kaydir = len(ALFALAR) * n

    print(f"  {'ayrim/atlama':>13} " + " ".join(f"{ay / BAG_M:>7.1f}"
                                               for ay in AYRIMLAR))
    sonuc = {}
    for i, a in enumerate(ALFALAR):
        oranlar = []
        for j in range(len(AYRIMLAR)):
            bas = kaydir + (i * len(AYRIMLAR) + j) * n
            v = [x for x, e in ham[bas:bas + n] if e is None]
            taban = tabanlar[a]
            oranlar.append(ist.mean(v) / taban if v and taban else 0.0)
        mesafe = next((ay / BAG_M for ay, o in zip(AYRIMLAR, oranlar)
                       if o > ESIK), None)
        sonuc[a] = mesafe
        print(f"  alfa={a:.1f} oran  " + " ".join(f"{o:>7.2f}"
                                                 for o in oranlar))
    print()
    print(f"  {'alfa':>5} {'girisim/iletim':>15} {'OLCULEN':>9} "
          f"{'olculen/oran':>13}")
    carpanlar = []
    eksik = False
    for a in ALFALAR:
        oran = 10 ** (16.0 / (10.0 * a))
        olculen = sonuc[a]
        if olculen is None:
            print(f"  {a:>5.1f} {oran:>15.2f} {'bulunamadi':>9} {'—':>13}")
            eksik = True
            continue
        carpanlar.append(olculen / oran)
        print(f"  {a:>5.1f} {oran:>15.2f} {olculen:>9.1f} "
              f"{olculen / oran:>13.3f}")
    print()
    if eksik or len(carpanlar) < len(ALFALAR):
        print("  🔴 SINAV KOSULAMADI — bir alfada yeniden kullanim bulunamadi")
        return
    sacilma = max(carpanlar) / min(carpanlar)
    gecti = sacilma <= SACILMA_SINIRI
    print(f"  carpan ortalama {ist.mean(carpanlar):.3f} · "
          f"en buyuk/en kucuk {sacilma:.3f} "
          f"(sinir {SACILMA_SINIRI:.2f})")
    print()
    print(f"  ORANTI SINAVI : {'🟢 GECTI' if gecti else '🔴 KALDI'}")
    if gecti:
        print("  🔒 Carpan alfa'dan BAGIMSIZ: yeniden kullanim mesafesi")
        print("     girisim/iletim oraniyla ORANTILI. Mekanizma dogrulandi.")
        print("  🔒 Li ile aradaki fark bir kusur degil, YAYILIM REJIMI")
        print("     farki — ve artik uc ayri alfada OLCULMUS bir aciklama.")
    else:
        print("  🔴 Carpan alfa ile degisiyor: 'yeniden kullanim mesafesini")
        print("     girisim/iletim orani belirler' aciklamasi EKSIK.")


if __name__ == "__main__":
    # 🔒 Windows `spawn` korumasi — calisma kurali 11. Ayrica: TEK havuz,
    # ic ice havuc YOK. Ic ice havuz `python -c` ile birlestiginde kilitleniyor
    # (9 Eylul 2026'da bir saat kaybettirdi; tek kosu 2,7 s surerken).
    main()
