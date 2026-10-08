"""
ÇALIŞMA NOKTASI — "menzil" tek bir sayı değil, ve alan bunun sonucudur.

Üretici:
    PYTHONIOENCODING=utf-8 python kalibrasyon/calisma_noktasi.py

🔴 NEDEN BU ÖLÇÜM VAR
=====================
`nominal_bag_m` veri yolunda **hiçbir yeri kapamıyor**: kimin duyacağını
girişim menzili, alınıp alınmadığını SINR belirliyor. O sayı yalnızca verici
gücünün türetildiği bir ÇAPA ve kalibrasyon betiklerinin topoloji anlık
görüntüsüdür. β yükseltildiğinde çapa ile fiilen kullanılabilen yarıçap
AYRIŞTI ve Adım 3, kimsenin kullanmadığı bir grafiği kalibre etmiş oldu
(K-096).

Bu dosya dört yarıçapı ayrı ayrı ölçer ve alan büyüklüğünü **ilan edilmiş
bir ölçütle** seçer.

🔒 FAZ 4 (K-183) — `--dunya referans_2026`: ölçüt AYNEN korunur; değişen
dünya (1:1, `kanal/dunya.py`), alan ızgarası (km), uzak kesme (referansta
yok) ve bağ çerçevesi — hız uyarlaması açıksa bağ ARF'nin
TABANINDA (1 Mb/s) ölçülür, çünkü zayıf bağ gerçekte oraya iner (K-181).
Argümansız koşu eski dünyada birebir eskisidir.

🔴 İLK İLAN EDİLEN ÖLÇÜT INFEASIBLE ÇIKTI — ve nedeni öğreticidir
=================================================================
5 Eylül 2026'da, tarama koşulmadan önce şu ölçüt ilan edilmişti:

    Alan, aşağıdaki üçünü BİRDEN sağlayan en küçük değerdir:
      1. kaynak-hedef çiftlerinin ≥ %45'i 3 veya daha çok atlama
      2. kopukluk %0 (her çift ulaşılabilir)
      3. ortalama derece ≥ 7

**Bu ölçüt sağlanamaz, ve bu taramaya bakmadan da görülebilirdi.** İçinde
hem bir fazlalık hem bir çelişki var:

  · (2) ile (3) AYNI şeydir. Rastgele geometrik bir grafikte bağlantılılık,
    ortalama dereceyi eşiğin üstünde tutmaktan başka bir şey değildir.
  · (1) ile (2) BİRBİRİNİ DIŞLAR. Derece ≈ n·π/(L/r)² ve atlama derinliği
    ≈ L/r olduğu için, n = 40 sabitken derece × derinlik² sabittir. Derecenin
    7 olması L/r ≈ 4 demek, o da ortalama ~2,5 atlama demek — çiftlerin
    %45'ini 3+ atlamaya çıkarmaya yetmez. Ölçülen sınır: derece 7'de derin
    çift payı en çok ~%44,5.
  · (3)'ün "7"si, K-096'nın GEÇERSİZ ilan ettiği Adım 3 kalibrasyonundan
    (derece 7,45) miras kalmıştı. Yani otoritesini çürütülmüş bir sayıdan
    alıyordu.
  · (2)'nin "%0"ı ise HAREKETLİ kola hiç uygulanamaz: `senaryolar.py` mobil
    kolda fasılalı bölünmeyi zaten belgeliyor ve *"mobil kolda PDR ≈ 1 tanım
    gereği imkânsızdır"* diyor. Ölçüldü: 1700 m'de bile 10 tohumun 3'ü en az
    bir anda kopuyor. Bağlantılılık koşulu STATİK kola aittir — U1 orada
    koşar.

🔒 YENİDEN FORMÜLASYON — eşik gevşetilmedi, INFEASIBLE KISIT AMACA TAŞINDI
==========================================================================
    Sert kısıt : statik kolda 30 tohumun HİÇBİRİNDE ulaşılamaz çift yok.
    Amaç       : bu kısıt altında atlama derinliğini EN BÜYÜK yapmak.
    Sonuç      : ölçütün SIFIR serbest parametresi var; alanı veri seçer.

Bu bir eşik gevşetmesi değildir: sağlanamayan bir kısıt kısıt olmaktan çıkıp
amaç olur, sağlanabilen kısıt aynen kalır. Seçilen sayı hâlâ elle konmuş
değildir — kopukluğun sıfır kaldığı en büyük alandır.

Neden derinlik amaç: proje çok atlamalı mesh yönlendirme hakkında. Çiftlerin
çoğu bir ya da iki atlamadaysa yönlendirmenin ifade edebileceği fark yoktur
ve tarama *"protokoller arasında fark yok"* der — oysa ölçülemeyen şey farkın
yokluğu değil, başlığın yokluğudur.

Neden bağlantılılık sert kısıt: kopuk bir çift, PDR'ye yönlendirmeyle hiç
ilgisi olmayan bir tavan koyar. Statik kol referans noktasıdır; orada
bölünme varsa karşılaştırmanın tabanı yoktur.

⚠️ "KULLANILABİLİR BAĞ" TANIMI
==============================
Bir bağ, yeniden denemeler dâhil **atlama başarısı ≥ 0,90** ise sayılır.
Başarı, gölgeleme ve sönümleme dâhil hesaplanır ve sönümleme üzerinden
ortalanır — tek bir anlık örnek, kanalın o andaki derinliğini bağın kalıcı
özelliği sanardı. Girişim dâhil DEĞİLDİR: burada ölçülen şey topolojinin
taşıyabileceği bağ kümesidir, yükün altındaki hâli değil.
"""

from __future__ import annotations

import math
import statistics as ist
import sys
from collections import Counter, deque
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import mesafe  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.yapilandirma.konfig import HIZLAR_BPS, Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402

BASARI_ESIGI = 0.90      # bir bağ "kullanılabilir" sayılır mı
SONUMLEME_ORNEGI = 6     # sönümleme üzerinden ortalama için zaman örneği
UZAK_KESME_M = 1200.0    # bunun ötesinde PER zaten 1; hesap israfı
# 🔴 VARSAYILAN 6 İDİ ve ÖLÇÜTÜN KENDİSİYLE ÇELİŞİYORDU — 9 Eylül 2026.
# `OLCUT` aşağıda *"statik kolda kopukluk %0 (**30 tohum**)"* diyor; betiğin
# varsayılanı ise 6 tohumdu ve köken defterinin gösterdiği üretici komut
# argümansız `python kalibrasyon/calisma_noktasi.py`. Yani **belgelenen
# komut, belgelenen sayıyı üretmiyordu**:
#
#     6 tohum  → hiçbir alanda kopukluk görünmüyor → seçilen alan 2000 m
#     30 tohum → 2000 m'de kopukluk %0,3 açılıyor  → seçilen alan **1800 m**
#
# Sebep istatistikseldir, kod değil: kopukluk NADİR bir olaydır ve 6 tohum
# onu göremez. Bir ölçüt "30 tohum" diyorsa varsayılan da 30 olmalıdır;
# aksi hâlde ölçütü okuyan ile betiği koşturan farklı sayılar görür.
#
# 🔒 30 TOHUMLA YENİDEN ÜRETİLDİ ve kayıt AYAKTA (9 Eylül 2026):
#     1800 m → kopukluk %0,0 · derece **8,67** · derin çift payı %31,0
#     2000 m → kopukluk %0,3 → kalır
#   `konfig.py`de yazan derece de tam olarak 8,67. Yani sayı doğruymuş;
#   yeniden üretilebilirliği kırılmıştı.
# ⚠️ Bedeli: tam ızgara 30 tohumla BANT 10–15 dk (6 tohumla ~3 dk).
TOHUMLAR = range(1000, 1030)   # --tohum N ile degistirilebilir
ALANLAR = (1000.0, 1200.0, 1400.0, 1600.0, 1800.0, 2000.0)
# Faz 4 (K-183): referans dünyanın ızgarası. `v2/14` §3'ün ~6–8 km'si 10 dB
# paylı nominal bağa (2 Mb/s, 1,65 km) dayanıyordu; simülatörün kanalında
# bağ 1 Mb/s'te ~7 km'ye uzanır (K-181: 7 km'de tek atlama PDR 0,99). Izgara
# bu yüzden 30 km'ye kadar — seçilen nokta ızgaranın içinde kalmalı.
ALANLAR_REFERANS = (5000.0, 7000.0, 10000.0, 13000.0, 16000.0, 20000.0,
                    25000.0, 30000.0)
# Görev kolu yarıçap ızgarası; referansta alan oranıyla (~×3,9) ölçeklenir.
YARICAPLAR = (250.0, 350.0, 450.0, 550.0, 650.0, 750.0)
# K-187: alan 35 km (K-185) → alan oranıyla ~12,6 km; ızgara onu kuşatır.
YARICAPLAR_REFERANS = (6000.0, 8000.0, 10000.0, 12000.0, 14000.0, 16000.0)
# Komut satirindan alan listesi verilebilir (ince izgara icin):
#   python kalibrasyon/calisma_noktasi.py 1850 1900 1950
OLCUT = ("sert kisit: statik kolda kopukluk %0 (30 tohum) · "
         "amac: atlama derinligini en buyuk yapmak")


# ==========================================================================
# 🔴 BU BETİK 5 EYLÜL'DEN 9 EYLÜL'E KADAR KOŞMUYORDU — ve kayıtlar onu
# `alan_en_m` · `alan_boy_m` · `gorev_grup_yaricapi_m` kayıtlarının ÜRETİCİSİ
# gösteriyordu (üçü de `OLCULMUS`).
# ==========================================================================
# `Konfig` şunu istiyor: `2 × gorev_grup_yaricapi_m < min(alan_en, alan_boy)`.
# K-097 yarıçapı 250 → **650 m** yaptı; taramanın ilk ızgara noktası ise
# **1000 m**. 2 × 650 = 1300 > 1000 → `alan_taramasi()` İLK çağrısında
# `DegismezHatasi` ile patlıyordu. Yani bölüm 2 ve 3 dört gündür hiç
# koşmadı ve yukarıdaki üç sayı **yeniden üretilemiyordu**.
#
# 🔒 AYNI SINIF, İKİNCİ ÖRNEK. K-110 `adim3_kapanis.py`de tam bunu bulmuştu
# *(üretici var, yazılı, ve koşmuyor)* ve orada onardı; bu dosyaya
# bakılmadı. D11 betiğin **içe aktarılabildiğini** sınıyor (bu betik içe
# aktarılabiliyor, hata koşarken çıkıyor), D15 ise **terk edilmiş**
# üreticileri arıyor (bu terk edilmiş değil, KIRIK).
#
# 🔒 DÜZELTMENİN ÖLÇÜMÜ DEĞİŞTİRMEDİĞİ İKİ AYRI YOLDAN GÖSTERİLDİ:
#   · YAPISAL — taranan kollar `statik` ve `bagimsiz`. `mobilite_kur`
#     müfreze yarıçapını YALNIZ `gorev` kolunda okur; öbür ikisinde
#     parametreye hiç dokunmaz ve `gorev_*` RNG akışlarından çekim yapmaz.
#   · ÖLÇÜLDÜ — 6 tohum × 2 kol × 2 zamanda düğüm konumlarının parmak izi
#     yarıçap 650 ↔ 400 m'de **BİREBİR AYNI**.
#
# ⚠️ Bölüm 4 (görev kolu kalibrasyonu) bu yardımcıyı KULLANMAZ: orada
# yarıçap taranan büyüklüğün ta kendisidir ve alan varsayılan (1800 m).
def _tarama_yaricapi_m(alan_m: float) -> float:
    """Taranan alanda `Konfig` değişmezini sağlayan müfreze yarıçapı.

    Varsayılanı korur, yalnız değişmezi çiğneyen küçük alanlarda kelepçeler.
    0,45 katsayısı bir ayar düğmesi değil, `2r < alan` değişmezinin altında
    kalan en yakın yuvarlak paydır ve bu kollarda **etkisizdir**.
    """
    varsayilan = (DS.konfig(kol="kalib").gorev_grup_yaricapi_m
                  if DS.referans_mi() else
                  Konfig.__dataclass_fields__["gorev_grup_yaricapi_m"].default)
    return min(varsayilan, 0.45 * alan_m)


def _uzak_kesme_m(kfg) -> float:
    """Eski dünyada 1200 m (PER zaten 1); referansta KESME YOK (K-183) —
    1 Mb/s bağı girişim menzilinin (5,97 km) ötesine, ~7,4 km'ye uzanır;
    40 düğümde bütün çiftleri hesaplamak ucuz, elle km yazılmaz."""
    return math.inf if DS.referans_mi() else UZAK_KESME_M


def _veri_cercevesi(kfg):
    """Bağın ölçüldüğü veri çerçevesi — hız uyarlaması açıksa ARF'nin
    tabanında (K-183); kapalıysa bugünkü çerçeve (birebir)."""
    return cerceve_kur(kfg, "veri", hiz_bps=(
        min(HIZLAR_BPS) if kfg.hiz_uyarlamasi else None))


def _atlama_basarisi(kanal, kfg, veri, onay, i, j, t0) -> float:
    toplam = 0.0
    for n in range(SONUMLEME_ORNEGI):
        t = t0 + n * 0.005
        toplam += ((1.0 - kanal.alim_per(i, j, veri, t))
                   * (1.0 - kanal.alim_per(j, i, onay, t + veri.sure_s)))
    tek = toplam / SONUMLEME_ORNEGI
    return 1.0 - (1.0 - tek) ** (kfg.yeniden_deneme_siniri + 1)


def _yaricap(kanal, kfg, cerceve, hedef: float) -> float:
    """Alım hatasının `hedef`e eşit olduğu mesafe — ikili arama."""
    def hata(d: float) -> float:
        # K-183: alıcı anten kazancı (referansta dipol 2,15 dBi; eskide 0)
        kayip = kanal.yayilim.yol_kaybi_db(d) - kfg.alici_anten_kazanci_dbi
        pr = kanal.yayilim.verici_gucu_w / (10.0 ** (kayip / 10.0))
        s = pr / kanal.yayilim.gurultu_w
        onb = kanal.onbelge_per(cerceve, ((float(cerceve.onbelge_bit), s),))
        return 1.0 - (1.0 - onb) * (1.0 - kanal.kahin_per(cerceve, s))
    alt, ust = 1.0, 20000.0
    for _ in range(90):
        orta = 0.5 * (alt + ust)
        if hata(orta) < hedef:
            alt = orta
        else:
            ust = orta
    return 0.5 * (alt + ust)


def yaricaplar() -> None:
    print("=" * 78)
    print("1 - DORT YARICAP  (saf yol kaybi, golgelemesiz)")
    print("=" * 78)
    kfg = DS.konfig(kol="kalib")
    kanal = Kanal(kfg, topoloji_kur(kfg, Akislar(kfg.tohum)))
    veri = _veri_cercevesi(kfg)
    beacon = cerceve_kur(kfg, "beacon")
    print(f"  capa (SINR = esik = {kfg.sinr_esigi_db:.0f} dB)   : "
          f"{kfg.nominal_bag_m:7.1f} m")
    for hedef in (0.10, 0.50):
        print(f"  veri   alim hatasi {hedef:.2f}          : "
              f"{_yaricap(kanal, kfg, veri, hedef):7.1f} m")
    for hedef in (0.10, 0.50):
        print(f"  beacon alim hatasi {hedef:.2f}          : "
              f"{_yaricap(kanal, kfg, beacon, hedef):7.1f} m")
    print(f"  girisim / duyma menzili        : {kfg.girisim_menzili_m:7.1f} m")
    print(f"\n  yol kaybi usteli = {kfg.yol_kaybi_usteli}")
    print("  🔴 Komsu tablosu beacon yaricapina kadar uzanir; veri o kadar")
    print("     gitmez. Aradaki halka 'hayalet bag'dir (K-094, K-096).")


def _graf(kanal, kfg, veri, onay, konumlar, t0):
    n = len(konumlar)
    kom: list[list[int]] = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if mesafe(konumlar[i], konumlar[j]) > _uzak_kesme_m(kfg):
                continue
            if _atlama_basarisi(kanal, kfg, veri, onay, i, j, t0) >= BASARI_ESIGI:
                kom[i].append(j)
                kom[j].append(i)
    return kom


def alan_taramasi() -> None:
    print("\n" + "=" * 78)
    print("2 - ALAN TARAMASI  (kullanilabilir bag grafigi)")
    print("=" * 78)
    print(f"  olcut (ONCEDEN ILAN EDILDI): {OLCUT}")
    print(f"  kullanilabilir bag: atlama basarisi >= {BASARI_ESIGI:.2f}, "
          f"{SONUMLEME_ORNEGI} sonumleme ornegi uzerinden\n")
    print(f"  {'alan':>6} {'derece':>7} {'1 atl':>7} {'2 atl':>7} {'3 atl':>7} "
          f"{'4+ atl':>7} {'kopuk':>7} {'>=3atl':>7} {'duyan':>6} {'olcut':>7}")
    secilen = None
    for en in ALANLAR:
        dagilim: Counter = Counter()
        kopuk = toplam = 0
        dereceler, duyanlar = [], []
        for tohum in TOHUMLAR:
            kfg = DS.konfig(kol="kalib", tohum=tohum, alan_en_m=en,
                         alan_boy_m=en,
                         gorev_grup_yaricapi_m=_tarama_yaricapi_m(en))
            top = topoloji_kur(kfg, Akislar(tohum))
            kanal = Kanal(kfg, top)
            veri = _veri_cercevesi(kfg)
            onay = cerceve_kur(kfg, "onay")
            n = kfg.dugum_sayisi
            konumlar = [top.konum(i, 100.0) for i in range(n)]
            kom = _graf(kanal, kfg, veri, onay, konumlar, 100.0)
            dereceler.append(sum(len(k) for k in kom) / n)
            duyanlar.append(ist.mean(
                sum(1 for j in range(n)
                    if j != i and mesafe(konumlar[i], konumlar[j])
                    <= kfg.girisim_menzili_m) for i in range(n)))
            for kaynak in range(n):
                uzak = {kaynak: 0}
                kuyruk = deque([kaynak])
                while kuyruk:
                    u = kuyruk.popleft()
                    for v in kom[u]:
                        if v not in uzak:
                            uzak[v] = uzak[u] + 1
                            kuyruk.append(v)
                for hedef in range(n):
                    if hedef == kaynak:
                        continue
                    toplam += 1
                    if hedef in uzak:
                        dagilim[uzak[hedef]] += 1
                    else:
                        kopuk += 1
        pay = lambda k: 100.0 * dagilim[k] / toplam
        derin = 100.0 * sum(v for k, v in dagilim.items() if k >= 3) / toplam
        kopuk_pay = 100.0 * kopuk / toplam
        derece = ist.mean(dereceler)
        # 🔒 Sert kisit: kopukluk tam sifir. Amac: derinligi buyutmek.
        # O yuzden GECEN alanlarin EN BUYUGU secilir, en kucugu degil.
        gecti = kopuk_pay == 0.0
        if gecti:
            secilen = (en, derin, derece)
        print(f"  {en:>6.0f} {derece:>7.2f} {pay(1):>6.1f}% {pay(2):>6.1f}% "
              f"{pay(3):>6.1f}% "
              f"{100.0 * sum(v for k, v in dagilim.items() if k >= 4) / toplam:>6.1f}% "
              f"{kopuk_pay:>6.1f}% {derin:>6.1f}% {ist.mean(duyanlar):>6.1f} "
              f"{'GECER' if gecti else 'kalir':>7}")
    print()
    if secilen is None:
        print("  🔴 HICBIR ALAN SERT KISITI SAGLAMADI (kopukluk %0).")
        print("     Kisit gevsetilmez; tarama araligi KUCUK alanlara genisletilir.")
    else:
        en, derin, derece = secilen
        print(f"  🟢 SECILEN ALAN: {en:.0f} m — kopuklugun sifir kaldigi EN BUYUK.")
        print(f"     derin cift payi {derin:.1f}%  ·  ortalama derece {derece:.2f}")
        print("     ⚠️ Bu sayi ELLE KONMADI: sert kisit ile amacin kesistigi")
        print("        noktadir. Tarama araligindaki en buyuk gecen alan.")




def zaman_ve_kol() -> None:
    """🔴 Anlık görüntü yetmez: bağlantılılık ZAMANLA ve KOLA göre değişir.

    Alan taraması tek bir anda (t = 100 s) ve tek bir kolda ölçer. Ölçüt
    *"ağ kopmasın"* diyorsa, onu koşu boyunca ve hareketli kolda da ölçmek
    zorunludur — yoksa ölçüm, iddia ettiği şeyi test etmiyordur.

    ⚠️ `kopuk_tohum` sütunu ortalamadan daha bağlayıcıdır: koşunun HERHANGİ
    bir anında kopan bir tohum, ortalamanın içinde görünmez.

    🔴 BURADAKİ ESKİ CÜMLE 9 EYLÜL 2026'DA KALDIRILDI. Şöyle diyordu:
    *"kopan bir tohum U1 sanity kolundan dışlanmak zorundadır
    (`senaryolar.py`, 'bağlı' bir tohum süzgecidir)."* K-110 o beyanı
    **çürüttü**: süzgeç beş dosyada *"ZORUNLU"* yazılıydı, kodda hiç
    uygulanmamıştı ve veri taşıyan kanal grafiğinde **gerekli de değil**
    (statik kol 270/270 anda tek parça). Beyanlar `sim2/` tarafında
    kaldırıldı; bu dosya atlanmıştı ve işaret ettiği `senaryolar.py`
    artık tam tersini söylüyor.
    """
    print()
    print("=" * 78)
    print("3 - ZAMAN ve MOBILITE KOLU BOYUNCA KOPUKLUK")
    print("=" * 78)
    zamanlar = (50.0, 175.0, 320.0)
    kollar = ("statik-yok", "bagimsiz-yok")
    tohumlar = list(range(1000, 1010))
    print(f"  {len(tohumlar)} tohum · t = {zamanlar} · kol basina")
    print()
    print(f"  {'alan':>6} {'kol':<14} {'derece':>7} {'kopuk_ort':>10} "
          f"{'kopuk_maks':>11} {'>=3atl':>7} {'kopuk_tohum':>12}")
    for en in ALANLAR:
        for senaryo in kollar:
            dereceler, kopuklar = [], []
            derin_pay = derin_toplam = 0
            kotu_tohum = set()
            for tohum in tohumlar:
                kfg = DS.konfig(kol="kalib", senaryo=senaryo, tohum=tohum,
                             alan_en_m=en, alan_boy_m=en,
                             gorev_grup_yaricapi_m=_tarama_yaricapi_m(en))
                top = topoloji_kur(kfg, Akislar(tohum))
                kanal = Kanal(kfg, top)
                veri = _veri_cercevesi(kfg)
                onay = cerceve_kur(kfg, "onay")
                n = kfg.dugum_sayisi
                for t in zamanlar:
                    konumlar = [top.konum(i, t) for i in range(n)]
                    kom = _graf(kanal, kfg, veri, onay, konumlar, t)
                    dereceler.append(sum(len(k) for k in kom) / n)
                    kopuk = toplam = 0
                    for kaynak in range(n):
                        uzak = {kaynak: 0}
                        kuyruk = deque([kaynak])
                        while kuyruk:
                            u = kuyruk.popleft()
                            for v in kom[u]:
                                if v not in uzak:
                                    uzak[v] = uzak[u] + 1
                                    kuyruk.append(v)
                        for hedef in range(n):
                            if hedef == kaynak:
                                continue
                            toplam += 1
                            derin_toplam += 1
                            if hedef in uzak:
                                if uzak[hedef] >= 3:
                                    derin_pay += 1
                            else:
                                kopuk += 1
                    oran = 100.0 * kopuk / toplam
                    kopuklar.append(oran)
                    if oran > 0.0:
                        kotu_tohum.add(tohum)
            print(f"  {en:>6.0f} {senaryo:<14} {ist.mean(dereceler):>7.2f} "
                  f"{ist.mean(kopuklar):>9.2f}% {max(kopuklar):>10.2f}% "
                  f"{100.0 * derin_pay / derin_toplam:>6.1f}% "
                  f"{len(kotu_tohum):>7}/{len(tohumlar)}")
    print()
    print("  🔴 'kopuk_tohum' = en az bir anda kopmus tohum sayisi. Anlik")
    print("     ortalama kucuk gorunse de, kosunun herhangi bir aninda kopan")
    print("     bir tohum U1 kolundan dislanmak zorundadir.")


def gorev_kolu_kalibrasyonu() -> None:
    """🔴 Görev kolu bağımsız kolla AYNI YOĞUNLUKTA olmak zorunda.

    Değilse ölçülen fark koordinasyonun değil **seyrekliğin** farkı olur —
    3B'ye geçerken yaşanan tuzağın aynısı.

    ⚠️ EŞİTLEME KULLANILABİLİR BAĞ GRAFİĞİNDE YAPILIR, teşhis grafiğinde
    değil. Eski kalibrasyon 280 m'lik diskte yapılmıştı; o disk veri yolunda
    kullanılmıyor (K-096). Kümelenmiş bir yerleşimde iki yarıçap AYNI ORANDA
    ölçeklenmez: müfreze içi bağlar küçük yarıçapta zaten doygundur, büyük
    yarıçapta ise müfrezeler arası bağlar açılır. Yani 280 m'de eşitlemek,
    530 m'de eşitlediğini garanti etmez.

    Ölçüt: |görev derecesi − bağımsız derecesi| en küçük olan yarıçap.
    """
    print()
    print("=" * 78)
    print("4 - GOREV KOLU KALIBRASYONU  (kullanilabilir bag grafiginde)")
    print("=" * 78)
    tohumlar = list(range(1000, 1008))
    zamanlar = (50.0, 175.0, 320.0)

    def derece(senaryo: str, **ek) -> float:
        toplam = []
        for tohum in tohumlar:
            kfg = DS.konfig(kol="kalib", senaryo=senaryo, tohum=tohum, **ek)
            top = topoloji_kur(kfg, Akislar(tohum))
            kanal = Kanal(kfg, top)
            veri = _veri_cercevesi(kfg)
            onay = cerceve_kur(kfg, "onay")
            n = kfg.dugum_sayisi
            for t in zamanlar:
                kon = [top.konum(i, t) for i in range(n)]
                kom = _graf(kanal, kfg, veri, onay, kon, t)
                toplam.append(sum(len(k) for k in kom) / n)
        return ist.mean(toplam)

    taban = derece("bagimsiz-yok")
    print(f"  bagimsiz-yok referans derecesi : {taban:.3f}")
    print(f"  {len(tohumlar)} tohum × {len(zamanlar)} zaman noktasi\n")
    print(f"  {'yaricap_m':>10} {'gorev_derece':>13} {'fark':>8} {'oran':>7}")
    en_iyi = None
    for r in (YARICAPLAR_REFERANS if DS.referans_mi() else YARICAPLAR):
        d = derece("gorev-yok", gorev_grup_yaricapi_m=r)
        fark = abs(d - taban)
        if en_iyi is None or fark < en_iyi[2]:
            en_iyi = (r, d, fark)
        print(f"  {r:>10.0f} {d:>13.3f} {fark:>8.3f} {d / taban:>7.3f}")
    r, d, fark = en_iyi
    print(f"\n  🟢 SECILEN YARICAP: {r:.0f} m  "
          f"(derece {d:.3f} ↔ {taban:.3f}, fark {fark:.3f})")
    print("     ⚠️ Bu sayi elle secilmedi: farki en kucuk yapan izgara noktasi.")
    print("     Izgara adimi 100 m; daha ince arama ancak fark tohum")
    print("     gurultusunun altina inerse anlamli olur.")


if __name__ == "__main__":
    DS.secimi_oku()                         # Faz 4 (K-183): --dunya
    print(f"  DUNYA: {DS.secili()}")
    if DS.referans_mi():
        ALANLAR = ALANLAR_REFERANS
    argv = sys.argv[1:]
    if "--tohum" in argv:
        i = argv.index("--tohum")
        TOHUMLAR = range(1000, 1000 + int(argv[i + 1]))
        argv = argv[:i] + argv[i + 2:]
    # 🔒 BOLUM SECIMI — 15 Eylul 2026. Dosya dort bolumu de her seferinde
    # kosturuyordu ve olculdu: 3 tohumla bile 15 dakikanin ustunde. Oysa
    # bolumler AYRI ISLERE ait: C2 alan capasini `yaricaplar` +
    # `alan_taramasi`dan okur, `gorev_kolu_kalibrasyonu` ise C5'in isidir
    # (`12` §3: ~140 tohum, 1-3 saat, ogrenci karari). Hepsini birlikte
    # kosturmak, C2'yi C5'in faturasiyla odetiyordu.
    BOLUMLER = {"yaricaplar": yaricaplar, "alan_taramasi": alan_taramasi,
                "zaman_ve_kol": zaman_ve_kol,
                "gorev_kolu": gorev_kolu_kalibrasyonu}
    secim = list(BOLUMLER)
    if "--bolum" in argv:
        i = argv.index("--bolum")
        secim = [a for a in argv[i + 1].split(",") if a]
        argv = argv[:i] + argv[i + 2:]
        bilinmeyen = [a for a in secim if a not in BOLUMLER]
        if bilinmeyen:
            raise SystemExit(f"bilinmeyen bolum: {bilinmeyen} — "
                             f"secenekler: {list(BOLUMLER)}")
    if argv:
        ALANLAR = tuple(float(a) for a in argv)
    for _ad in secim:
        BOLUMLER[_ad]()
