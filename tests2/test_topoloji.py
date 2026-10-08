"""
ADIM 3 — `sim2/dunya/topoloji.py` kapanış ölçütleri.

Kapanış ölçütü (yol haritası):
    "1000×1000×120 · R=280'de ort. derece ve bağlı oran raporlanmış.
     Hareket boyunca bağlantılılık zaman serisi ölçülmüş."

🔴 BU DOSYANIN EN ÖNEMLİ TESTİ `test_mobilite_UZAY_DAGILIMINI_BOZMUYOR`.
Adım 3'ün ölçümü, Adım 2'de fark edilmemiş iki kusuru ortaya çıkardı:

  1. **Yansıma yalnız ANLIK yönü çeviriyordu.** Gauss-Markov düğümü duvarı
     gösteren ORTALAMA yönüne geri çekiyordu; düğümler duvara yapışıyordu.
     Kenardan ortanca uzaklık 170 m → **5 m**, ortalama derece 7,2 → **11,2**,
     tam bağlı zaman oranı **%11,1** (en kötü tohum %0,9).
  2. **Ortalama pitch +0,05 rad** her düğümü kalıcı tırmanışa sokuyordu
     (geniş bandda 350 s'de +299 m sürüklenme) ve dipol anten kararının
     dayandığı "düz uçuş" varsayımıyla çelişiyordu.

⚠️ İkisi BİRLİKTE ölçülüyordu: düzeltmeden önce t = 350 s'de ortalama irtifa
117,0 m (tavan 120 m) idi, ama o çöküşün sebebi tırmanış DEĞİL, tırmanan
düğümün tavanda kalmasıydı. Aynalama geldikten sonra +0,05 tek başına
irtifayı çökertmiyor. Bu yüzden iki kusurun testleri de AYRI:
`test_mobilite_UZAY_DAGILIMINI_BOZMUYOR` sınırı, `test_ortalama_pitch_
SIFIR_kalici_tirmanis_yok` sürüklenmeyi yakalar.

İkisi de "kod doğru görünüyor, testler geçiyor, ölçüm sessizce başka bir şey"
sınıfındaydı. Her ikisi de geri konularak testlerin KIRILDIĞI doğrulandı.
"""

from __future__ import annotations

import math
import pathlib
import statistics as ist
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import mesafe  # noqa: E402
from sim2.dunya.topoloji import Topoloji, topoloji_kur  # noqa: E402
from sim2.dunya.yerlesim import kutu_kur  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402


# 🔴 Alan buyuklugu KONFIGDEN okunur, elle yazilmaz. 5 Eylul 2026'da alan
# 1000 -> 1800 m olunca elle yazilmis "1000.0"lar sessizce anlamsizlasti:
# "kenardan uzaklik -250 m" gibi sayilar uretti. `03` B5, etiketi elle tasima.
EN = Konfig(kol="t").alan_en_m


def _top(senaryo: str = "statik-yok", tohum: int = 1, **ek) -> Topoloji:
    return topoloji_kur(Konfig(kol="t", senaryo=senaryo, tohum=tohum, **ek),
                        Akislar(tohum))


# ==========================================================================
# KUTU — irtifa bandı hem yerleşimin hem KUTUNUN sınırı
# ==========================================================================

def test_kutu_dikey_siniri_IRTIFA_BANDI():
    k = Konfig(kol="t")
    kutu = kutu_kur(k)
    assert (kutu.taban_m, kutu.yukseklik_m) == (k.irtifa_min_m, k.irtifa_maks_m)


def test_hareket_boyunca_IRTIFA_BANDINDA_kaliniyor():
    """🔴 "İrtifa 20–120 m" kararı yalnız başlangıçta uygulansaydı yarım
    uygulanmış olurdu: tabansız kutuda düğümler dakikalar içinde 0 m'ye,
    yani yere iniyordu."""
    k = Konfig(kol="t", senaryo="bagimsiz-yok")
    top = _top("bagimsiz-yok", 3)
    for a in top.zaman_serisi(0.0, 350.0, 5.0):
        for p in a.konumlar:
            assert k.irtifa_min_m - 1e-9 <= p.z <= k.irtifa_maks_m + 1e-9
            assert 0.0 <= p.x <= k.alan_en_m and 0.0 <= p.y <= k.alan_boy_m


# ==========================================================================
# ZAMANA BAĞLILIK — eski simülatörün en büyük kusuru
# ==========================================================================

def test_statik_kolda_konum_DEGISMIYOR():
    top = _top("statik-yok", 5)
    ilk = top.anlik(0.0)
    for t in (10.0, 100.0, 350.0):
        assert top.anlik(t).konumlar == ilk.konumlar
    assert top.hareketli is False


def test_mobil_kolda_konum_DEGISIYOR():
    top = _top("bagimsiz-yok", 5)
    assert top.hareketli is True
    assert top.anlik(0.0).konumlar != top.anlik(50.0).konumlar


def test_ayni_tohum_BIREBIR_ayni_topoloji():
    for tohum in (1, 7, 42):
        a = _top("bagimsiz-yok", tohum).anlik(123.5)
        b = _top("bagimsiz-yok", tohum).anlik(123.5)
        assert a.konumlar == b.konumlar and a.komsular == b.komsular


def test_statik_kolda_BAG_OLAYI_YOK():
    seri = _top("statik-yok", 9).zaman_serisi(0.0, 100.0, 1.0)
    assert Topoloji.bag_olaylari(seri) == {"acilan": 0, "kapanan": 0}


def test_mobil_kolda_BAG_OLAYI_VAR():
    seri = _top("bagimsiz-yok", 9).zaman_serisi(0.0, 100.0, 1.0)
    olay = Topoloji.bag_olaylari(seri)
    assert olay["acilan"] > 0 and olay["kapanan"] > 0


# ==========================================================================
# ANLIK — dondurulmuş, tutarlı
# ==========================================================================

def test_anlik_DONDURULMUS():
    import dataclasses
    a = _top().anlik(0.0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        a.t_s = 1.0  # type: ignore[misc]


def test_komsuluk_SIMETRIK():
    a = _top("bagimsiz-yok", 11).anlik(77.0)
    for i, ks in enumerate(a.komsular):
        for j in ks:
            assert i in a.komsular[j], f"{i}–{j} bağı tek yönlü"


def test_bilesenler_TUM_dugumleri_ortuyor_ve_ORTUSMUYOR():
    a = _top("bagimsiz-yok", 13).anlik(200.0)
    uyeler = [d for b in a.bilesenler for d in b]
    assert sorted(uyeler) == list(range(40))
    assert a.en_buyuk_bilesen == len(a.bilesenler[0])
    assert a.bagli_mi == (len(a.bilesenler) == 1)


def test_bilesenler_BUYUKTEN_KUCUGE():
    a = _top("bagimsiz-yok", 13).anlik(200.0)
    boylar = [len(b) for b in a.bilesenler]
    assert boylar == sorted(boylar, reverse=True)


def test_gecersiz_ornekleme_reddediliyor():
    top = _top()
    with pytest.raises(DegismezHatasi):
        top.zaman_serisi(0.0, 10.0, 0.0)
    with pytest.raises(DegismezHatasi):
        top.zaman_serisi(10.0, 0.0, 1.0)
    with pytest.raises(DegismezHatasi):
        Topoloji.baglantililik_ozeti(())


# ==========================================================================
# 🔒 KALİBRASYON KAPISI — çalışma noktası
# ==========================================================================

def test_KALIBRASYON_calisma_noktasi():
    """🔴 BU GRAFİK BİR TEŞHİSTİR — BAĞLANTILILIK MODELİ DEĞİL.

    `Topoloji`nin komşuluk grafiği `nominal_bag_m` (280 m) yarıçaplı sert
    bir disktir. 280 m, VERİCİ GÜCÜNÜN türetildiği çapadır; veri yolunda
    hiçbir yeri kapamaz. Gerçekte kimin duyacağını girişim menzili, alınıp
    alınmadığını SINR belirler (K-096).

    ⚠️ 5 Eylül 2026'da ölçüldü ve tek bir yarıçapın gerçek bağ kümesini
    TEMSİL EDEMEDİĞİ görüldü: derece eşitlense bile (r = 560 m'de 8,23 ↔
    8,25) kenarların yalnız yarısı örtüşüyor (Jaccard 0,53). Sebebi
    gölgeleme: σ = 3 dB, α = 2'de mesafede ±%41 demek. "Menzil" bir daire
    değil, kenarları 1,4 kat oynayan bulanık bir buluttur.

    🔒 O yüzden buradaki sayılar bir ÇALIŞMA NOKTASI kapısı değil, bir
    DEĞİŞİM DEDEKTÖRÜdür: geometri sessizce kayarsa bu test konuşur.
    Gerçek çalışma noktası — kullanılabilir bağ grafiğinde derece 8,67 ve
    statik kolda 30 tohumda kopukluk %0 — `kalibrasyon/calisma_noktasi.py`
    tarafından ölçülür ve kapı ORADADIR.

    ⚠️ Eski gerekçe (derece 7,271 · bağlı %78,2) `konfig.py`de GEÇERSİZ
    etiketiyle duruyor: o ölçüm 1000 m'lik alanda, aynı teşhis grafiğinde
    yapılmıştı.
    """
    dereceler, bagli = [], 0
    for tohum in range(1, 121):
        a = _top("statik-yok", tohum).anlik(0.0)
        dereceler.append(a.ortalama_derece)
        bagli += a.bagli_mi
    ort = ist.mean(dereceler)
    oran = bagli / 120

    # Teşhis grafiğinin analitik beklentisi: n·π·r²/L², kenar etkisi hariç.
    # Elle yazılmış bir sayı DEĞİL — konfigden türer, alan değişince izler.
    kfg = Konfig(kol="t")
    beklenen = ((kfg.dugum_sayisi - 1) * math.pi
                * kfg.nominal_bag_m ** 2
                / (kfg.alan_en_m * kfg.alan_boy_m))
    assert 0.60 * beklenen < ort < 1.05 * beklenen, (
        f"🔴 teşhis grafiğinin derecesi {ort:.3f}; kenar etkisiz analitik "
        f"beklenti {beklenen:.3f}. Sapma, yerleşimin düzgün olmadığını ya da "
        f"geometrinin kaydığını gösterir.")
    # 280 m'lik disk 1800 m'lik alanda bağlantılılık eşiğinin ÇOK altında;
    # bağlı çıkan tohum olmaması beklenen davranıştır ve bu, o grafiğin neden
    # bağlantılılık modeli olarak kullanılamayacağının doğrudan kanıtıdır.
    assert oran < 0.05, (
        f"🔴 teşhis grafiğinde bağlı tohum oranı {oran:.3f}. Beklenen ≈ 0: "
        f"derece {ort:.2f}, bağlantılılık eşiği ise ~2·ln(40) ≈ 7,4. "
        f"Bu oran yükselirse geometri ya da alan değişmiş demektir.")


def test_3B_gecisi_agi_SEYRELTIYOR():
    """Telafinin neden gerektiğini gösteren karşılaştırma — kapının gerekçesi."""
    def derece(irtifa_maks):
        return ist.mean(
            _top("statik-yok", t, irtifa_maks_m=irtifa_maks).anlik(0.0)
            .ortalama_derece for t in range(1, 61))
    # ⚠️ ORANSAL esik, mutlak degil. Eskiden "- 0.7" yaziyordu ve o sayi
    # 7,27'lik eski derece olcegine gore secilmisti; alan buyuyup derece
    # olcegi degisince test, iddiasi hala dogruyken kirildi. Iddia
    # "seyreltiyor mu", "0,7 kadar mi seyreltiyor" degil.
    assert derece(300.0) < derece(120.0) * 0.90, (
        "🔴 300 m irtifa bandı ağı SEYRELTMELİ; seyrelmiyorsa çalışma "
        "noktasının gerekçesi düşer")


# ==========================================================================
# 🔴 ADIM 3'ÜN ÖLÇÜMÜNÜN BULDUĞU İKİ KUSUR — geri gelirse burası konuşur
# ==========================================================================

def test_mobilite_UZAY_DAGILIMINI_BOZMUYOR():
    """🔴 Mobilite modeli düzgün dağılımı korumak ZORUNDA.

    Korumazsa ölçülen şey karıştırma değil, mobilite modelinin yapaylığı
    olur. Dört bağımsız büyüklük, düzgün dağılımın analitik beklentisiyle
    karşılaştırılır (10 tohum × 350 s, 5 s örnekleme):

        büyüklük                    ölçülen   düzgün dağılım
        kenardan ortalama uzaklık    166,6         166,7      (= L/6)
        zaman boyunca ort. derece      7,31          7,27      (t = 0)
        irtifa ortalaması             71,0          70,0
        irtifa std                    28,7          28,9

    Bu testin yakaladığı iki gerçek kusur:
      · duvara yapışma  → kenar 5 m · derece 11,2
      · tavana yapışma  → irtifa 117,0 m · std 2,4
    """
    kenarlar, dereceler, irtifalar = [], [], []
    for tohum in range(1, 11):
        top = _top("bagimsiz-yok", tohum)
        seri = top.zaman_serisi(0.0, 350.0, 5.0)
        dereceler.append(Topoloji.baglantililik_ozeti(seri)["ortalama_derece"])
        for a in seri:
            for p in a.konumlar:
                kenarlar.append(min(p.x, EN - p.x, p.y, EN - p.y))
                irtifalar.append(p.z)

    kenar_ort = ist.mean(kenarlar)
    derece_ort = ist.mean(dereceler)
    irtifa_ort = ist.mean(irtifalar)
    irtifa_std = ist.pstdev(irtifalar)

    # Düzgün dağılımın analitik beklentileri — elle yazılmış hedef DEĞİL.
    beklenen_kenar = EN / 6.0                           # L/6
    beklenen_irtifa = (20.0 + 120.0) / 2.0              # 70,0
    beklenen_irtifa_std = (120.0 - 20.0) / (12 ** 0.5)  # 28,87

    assert abs(kenar_ort - beklenen_kenar) < 25.0, (
        f"🔴 kenardan ortalama uzaklık {kenar_ort:.1f} m, düzgün dağılımda "
        f"{beklenen_kenar:.1f} m olmalı. Düğümler sınıra yapışıyor ya da "
        f"merkeze toplanıyor — mobilite modeli çalışma noktasını kaydırıyor.")
    # ⚠️ ORANSAL esik. Eskiden "6,6 < derece < 8,2" yaziliyordu; o aralik
    # 7,27'lik eski derece olcegine gore secilmisti ve alan degisince test,
    # iddiasi hala dogruyken kirildi. Iddia mutlak bir derece degil,
    # "hareketli kolun zaman ortalamasi STATIK referanstan sapmiyor".
    # Tolerans aynen korundu: 6,6/7,27 = 0,908 ve 8,2/7,27 = 1,128.
    statik_derece = ist.mean(
        _top("statik-yok", tohum).anlik(0.0).ortalama_derece
        for tohum in range(1, 11))
    assert 0.908 * statik_derece < derece_ort < 1.128 * statik_derece, (
        f"🔴 zaman boyunca ortalama derece {derece_ort:.2f}; statik referans "
        f"{statik_derece:.2f}. Sapma, düğümlerin bir bölgede yığıldığını "
        f"gösterir.")
    assert abs(irtifa_ort - beklenen_irtifa) < 10.0, (
        f"🔴 ortalama irtifa {irtifa_ort:.1f} m, band ortası "
        f"{beklenen_irtifa:.1f} m. İrtifa boyutu çöküyor.")
    assert irtifa_std > 0.7 * beklenen_irtifa_std, (
        f"🔴 irtifa std {irtifa_std:.1f}, düzgün dağılımda "
        f"{beklenen_irtifa_std:.1f}. Düğümler tek bir irtifada toplanıyor — "
        f"3B model tavana yapışmış bir 2B modele dönüşüyor.")


def test_ortalama_pitch_SIFIR_kalici_tirmanis_yok():
    """🔴 Ortalama pitch 0 olmazsa her düğüm kalıcı tırmanışa geçer.

    Kutu tavanı yoksa bile ölçülebilir olmalı: tavansız bir bandda 350 s
    sonunda ortalama irtifa artışı sıfıra yakın kalmalı.
    """
    k = Konfig(kol="t")
    assert k.gm_pitch_ort_rad == 0.0, (
        "🔴 ortalama pitch sıfırdan farklı — v·sin(pitch) kadar KALICI düşey "
        "hız demektir; ölçüldü, t = 350 s'de irtifa tavana yapışıyordu")
    # Geniş bir bandda tavan/taban etkisi olmadan sürüklenme ölçülür.
    top = _top("bagimsiz-yok", 4, irtifa_min_m=0.0, irtifa_maks_m=5000.0)
    bas = ist.mean(p.z for p in top.anlik(0.0).konumlar)
    son = ist.mean(p.z for p in top.anlik(350.0).konumlar)
    assert abs(son - bas) < 150.0, (
        f"🔴 350 s'de ortalama irtifa {bas:.0f} → {son:.0f} m sürükleniyor; "
        f"sistematik bir tırmanış/alçalma var")


def test_yansimada_ORTALAMA_yon_de_aynalaniyor():
    """🔴 Yalnız anlık yön aynalansaydı düğüm duvara yapışırdı.

    Doğrudan ölçüm: kutunun dış onda birlik kabuğunda geçirilen zaman payı,
    o kabuğun hacim payını çok aşmamalı.
    """
    kabuk_hacim_payi = 1.0 - 0.8 ** 2      # x ve y'de %10'ar kabuk → 0,36
    icerde = disarda = 0
    for tohum in range(1, 8):
        for a in _top("bagimsiz-yok", tohum).zaman_serisi(0.0, 350.0, 5.0):
            for p in a.konumlar:
                if min(p.x, EN - p.x, p.y, EN - p.y) < 0.1 * EN:
                    disarda += 1
                else:
                    icerde += 1
    pay = disarda / (icerde + disarda)
    assert pay < kabuk_hacim_payi * 1.35, (
        f"🔴 zamanın %{100*pay:.1f}'i dış kabukta geçiyor; düzgün dağılımda "
        f"%{100*kabuk_hacim_payi:.1f}. Düğümler duvara yapışıyor.")


# ==========================================================================
# 🔒 BAĞLANTILILIK ZAMAN SERİSİ — kapanış ölçütünün ikinci yarısı
# ==========================================================================

def test_statik_kol_IKI_UCLU_mobil_kol_FASILALI():
    """🔴 TEŞHİS GRAFİĞİNİN ZAMAN DAVRANIŞI — bağlantılılık kapısı DEĞİL.

    Bu test `Topoloji`nin 280 m'lik komşuluk grafiğini ölçer. O grafik verici
    gücünün çapasıdır; veri yolunda kullanılmaz (K-096). 1800 m'lik alanda
    derecesi ~2,6 ve bağlantılılık eşiğinin (~2·ln 40 ≈ 7,4) çok altında,
    dolayısıyla hiçbir kolda "tam bağlı" beklenmez.

    🔒 Burada test edilen tek şey, grafiğin ZAMAN DAVRANIŞIdır:
      · statik kolda konumlar değişmez → bağlantılılık ya 0 ya 1, ara yok
      · hareketli kolda konumlar değişir → ara değerler görünmeli

    ⚠️ GERÇEK bağlantılılık ölçümü `kalibrasyon/calisma_noktasi.py`dedir ve
    kullanılabilir bağ grafiğinde yapılır. Ölçülen (5 Eylül 2026):
        statik-yok   : 30 tohumun hiçbirinde ulaşılamaz çift YOK
        bagimsiz-yok : 10 tohumun 3'ü en az bir anda kopuyor;
                       en kötü anda çiftlerin %9,7'si ulaşılamaz
    U1'in yalnız statik kolda koşabilmesinin gerekçesi ORADAN gelir —
    buradan değil. Eski hâlinde bu test o gerekçeyi teşhis grafiğinden
    okuyordu ve alan değişince sessizce anlamsızlaştı.
    """
    statik, mobil = [], []
    for tohum in range(1, 16):
        statik.append(Topoloji.baglantililik_ozeti(
            _top("statik-yok", tohum).zaman_serisi(0.0, 200.0, 5.0)
        )["tam_bagli_zaman_orani"])
        mobil.append(Topoloji.baglantililik_ozeti(
            _top("bagimsiz-yok", tohum).zaman_serisi(0.0, 200.0, 5.0)
        )["tam_bagli_zaman_orani"])

    assert all(o in (0.0, 1.0) for o in statik), (
        "🔴 statik kolda ara değer çıktı — konumlar değişmediğine göre "
        "bağlantılılık de değişemez")
    # Hareketli kolda grafiğin ZAMANLA DEĞİŞTİĞİ gösterilmeli. Teşhis
    # grafiğinde tam bağlılık hiç görülmeyebilir (derece eşiğin altında),
    # o yüzden kanıt "tam bağlı" değil, BAĞ SAYISININ oynamasıdır.
    seri = _top("bagimsiz-yok", 1).zaman_serisi(0.0, 200.0, 5.0)
    dereceler = {round(a.ortalama_derece, 6) for a in seri}
    assert len(dereceler) > 1, (
        "🔴 hareketli kolda topoloji hiç değişmiyor — mobilite ya kapalı ya "
        "da konumlar donmuş")
    durgun = {round(a.ortalama_derece, 6)
              for a in _top("statik-yok", 1).zaman_serisi(0.0, 200.0, 5.0)}
    assert len(durgun) == 1, (
        "🔴 statik kolda topoloji değişiyor — konumlar sabit olmalıydı")


def test_bag_olayi_sayimi_ORNEKLEME_ADIMINA_kaba_duyarli():
    """Adımdan kısa süren kopma sayımda görünmez; sayım adım küçüldükçe artar.

    Ölçüldü: 2,0 s → 2570 · 1,0 s → 2601 · 0,5 s → 2619 kapanan (5 tohum).
    Artış %1,9 — yani sayım bu adım aralığında kaba duyarlı, ama SIFIR
    duyarlı değil. Rapora adım da yazılır.
    """
    top = _top("bagimsiz-yok", 2)
    kaba = Topoloji.bag_olaylari(top.zaman_serisi(0.0, 200.0, 2.0))["kapanan"]
    ince = Topoloji.bag_olaylari(top.zaman_serisi(0.0, 200.0, 0.5))["kapanan"]
    assert ince >= kaba, "ince örnekleme daha AZ olay göremez"
    assert ince < kaba * 1.5, (
        f"🔴 sayım örnekleme adımına aşırı duyarlı ({kaba} → {ince}); "
        f"bu adımlarda raporlanan olay sayısı anlamsız olurdu")


# ==========================================================================
# 🔒 GÖREV TABANLI KOL — üçüncü mobilite kolu
# ==========================================================================

def test_uc_kol_da_kuruluyor_ve_AYRI_davraniyor():
    for senaryo, hareketli in (("statik-yok", False), ("bagimsiz-yok", True),
                               ("gorev-yok", True)):
        top = _top(senaryo, 3)
        assert top.hareketli is hareketli
        assert (top.anlik(0.0).konumlar != top.anlik(120.0).konumlar) is hareketli


def test_gorev_kolu_SEKTOR_tutuyor():
    """🔒 Modelin görev yapısı: her müfreze harekât alanının bir bölümünü tutar.

    🔴 Serbest dolaşan merkezler ÖLÇÜMLE elendi: 8 müfreze 1000×1000'de
    bağımsız dolaşınca rastgele üst üste biniyor ve ortalama derece 10–17
    arasında geziniyordu (hedef 7,45). Sektör, "dış dünyaya göre hareket"in
    modeldeki karşılığıdır — müfrezenin nereye gideceğini rastgelelik değil
    görevi belirler.
    """
    top = _top("gorev-yok", 5)
    mob = top.mobilite
    grup_of = mob.grup_of
    kokenler = mob.sektor_kokeni
    # Her üye, koşu boyunca KENDİ sektörünün yakınında kalmalı: sektörden
    # uzaklığı grup yarıçapını çok aşmamalı.
    k = Konfig(kol="t")
    sutun = math.ceil(math.sqrt(k.gorev_grup_sayisi))
    satir = math.ceil(k.gorev_grup_sayisi / sutun)
    sek_en, sek_boy = k.alan_en_m / sutun, k.alan_boy_m / satir
    tasma = []
    for a in top.zaman_serisi(0.0, 350.0, 10.0):
        for i, p in enumerate(a.konumlar):
            ox, oy = kokenler[grup_of[i]]
            dx = max(ox - p.x, p.x - (ox + sek_en), 0.0)
            dy = max(oy - p.y, p.y - (oy + sek_boy), 0.0)
            tasma.append(math.hypot(dx, dy))
    ort = ist.mean(tasma)
    assert ort < k.gorev_grup_yaricapi_m, (
        f"🔴 üyeler sektörlerinden ortalama {ort:.0f} m taşıyor "
        f"(grup yarıçapı {k.gorev_grup_yaricapi_m:.0f} m). Sektör yapısı "
        f"çözülmüşse kol, bağımsız kolun gürültülü bir kopyasıdır.")


def test_gorev_kolu_KOORDINELI_bagimsiz_koldan_yavas():
    """🔴 Kolun VAR OLUŞ SEBEBİ: komşular arası bağıl hızı düşürmek.

    Ölçüldü — bağımsız 26,0 m/s ↔ görev 16,6 m/s (0,66×). Bu oran 1'e
    yaklaşırsa kol sessizce bağımsız kola dönmüş demektir ve üçüncü kolu
    koşmanın hiçbir anlamı kalmaz.
    """
    def bagil_hiz_ortancasi(senaryo):
        h = []
        for tohum in (1, 2, 3):
            top = _top(senaryo, tohum)
            for t in (50.0, 150.0, 250.0):
                a, b = top.anlik(t), top.anlik(t + 0.5)
                for i in range(40):
                    for j in range(i + 1, 40):
                        if mesafe(a.konumlar[i], a.konumlar[j]) > 280.0:
                            continue
                        vx = ((b.konumlar[i].x - a.konumlar[i].x)
                              - (b.konumlar[j].x - a.konumlar[j].x)) / 0.5
                        vy = ((b.konumlar[i].y - a.konumlar[i].y)
                              - (b.konumlar[j].y - a.konumlar[j].y)) / 0.5
                        vz = ((b.konumlar[i].z - a.konumlar[i].z)
                              - (b.konumlar[j].z - a.konumlar[j].z)) / 0.5
                        h.append(math.sqrt(vx * vx + vy * vy + vz * vz))
        return ist.median(h)

    bagimsiz = bagil_hiz_ortancasi("bagimsiz-yok")
    gorev = bagil_hiz_ortancasi("gorev-yok")
    assert gorev < 0.85 * bagimsiz, (
        f"🔴 görev kolu koordineli DEĞİL: bağıl hız {gorev:.1f} ↔ bağımsız "
        f"{bagimsiz:.1f} m/s. Kol bağımsız kola dönmüş.")


def test_gorev_kolu_STATIK_kolun_kopyasi_DEGIL():
    """🔒 Diğer yönden dejenerasyon: rijit bir formasyon, kayan bir başlangıç
    noktasıyla STATİK koldan ibaret olurdu. Bağ olayı sayısı bunu ölçer."""
    # ⚠️ ESKİ EŞİK 50 İDİ ve Mach-4 hızlarına göre yazılmıştı (K-101).
    # Hızlar 1/50 ölçeğe çekilince ağ 28 kat yavaş çalkalanıyor ve o eşik,
    # iddiası hâlâ doğruyken testi kırdı. Yeniden ÖLÇÜLDÜ (7 tohum, 200 s):
    #     statik-yok    :  0,0 kapanan   ← donmuş, tanım gereği
    #     gorev-yok     : 11,1 kapanan
    #     bagimsiz-yok  : 14,6 kapanan
    #
    # 🔒 İddia "görev kolu DONMUŞ DEĞİL"dir; eşik ölçülen 11,1'in yarısında.
    # ⚠️ "görev < bağımsız" BİLEREK test edilmiyor: `mobilite.py` bağıl hızı
    # ve rota ömrünü ÖLÇÜT DEĞİL SONUÇ olarak ilan ediyor. Sonucu kapıya
    # çevirmek cevabı seçmek olurdu.
    seri = _top("gorev-yok", 7).zaman_serisi(0.0, 200.0, 2.0)
    olay = Topoloji.bag_olaylari(seri)
    durgun = Topoloji.bag_olaylari(
        _top("statik-yok", 7).zaman_serisi(0.0, 200.0, 2.0))
    assert durgun["kapanan"] == 0, "🔴 statik kolda bağ olayı olmamalı"
    assert olay["kapanan"] >= 5, (
        f"🔴 görev kolunda yalnız {olay['kapanan']} bağ kopuyor — topoloji "
        f"neredeyse donmuş, kol statik kolun kopyası")


def test_gorev_kolu_KALIBRE_derece_bagimsiz_kolla_esit():
    """🔒 İlan edilmiş ölçütün kod karşılığı.

    Kolları karşılaştırılabilir yapan şey yerleşimin aynılığı DEĞİL —
    "formasyonda" ile "düzgün rastgele" farklı dağılımlardır — yoğunluğun
    eşitliğidir. Eşitlenmezse ölçülen fark koordinasyonun değil, ağın
    seyrekliğinin farkı olur.

    ⚠️ ASIL KALİBRASYON BURADA DEĞİL. Yarıçap, KULLANILABİLİR BAĞ grafiğinde
    seçilir (`kalibrasyon/calisma_noktasi.py`, bölüm 4) — çünkü eşitlenmesi
    gereken yoğunluk telsizlerin gördüğü yoğunluktur, 280 m'lik teşhis
    diskininki değil. Bu test teşhis grafiğinde koşar ve bir DEĞİŞİM
    DEDEKTÖRÜdür: kalibrasyon kayarsa burası konuşur.

    ⚠️ Tolerans ORANSAL. Eskiden "|fark| < 0,8" yazıyordu; o sayı 7,27'lik
    eski derece ölçeğine göre seçilmişti (%11) ve alan büyüyüp ölçek 2,5'e
    inince aynı 0,8 sessizce %32'lik bir tolerans hâline geldi — test
    kırılmadan gevşedi. Sıkılık aynen korundu: ±%11.
    """
    def zaman_ortalamasi(senaryo):
        return ist.mean(
            Topoloji.baglantililik_ozeti(
                _top(senaryo, t).zaman_serisi(0.0, 350.0, 5.0)
            )["ortalama_derece"] for t in range(1, 8))

    bagimsiz = zaman_ortalamasi("bagimsiz-yok")
    gorev = zaman_ortalamasi("gorev-yok")
    assert abs(gorev - bagimsiz) < 0.11 * bagimsiz, (
        f"🔴 derece eşitliği bozuldu: bağımsız {bagimsiz:.2f} ↔ görev "
        f"{gorev:.2f} (oran {gorev / bagimsiz:.3f}). Ölçülen fark "
        f"koordinasyonun değil yoğunluğun farkı olur.")


def test_gorev_kolu_belirlenimci_ve_KUTUDA():
    k = Konfig(kol="t")
    for tohum in (1, 9):
        a = _top("gorev-yok", tohum).anlik(211.5)
        b = _top("gorev-yok", tohum).anlik(211.5)
        assert a.konumlar == b.konumlar
    for a in _top("gorev-yok", 4).zaman_serisi(0.0, 350.0, 7.0):
        for p in a.konumlar:
            assert 0.0 <= p.x <= k.alan_en_m and 0.0 <= p.y <= k.alan_boy_m
            assert k.irtifa_min_m - 1e-9 <= p.z <= k.irtifa_maks_m + 1e-9


def test_bilinmeyen_mobilite_kolu_REDDEDILIYOR():
    from sim2.dunya.mobilite import mobilite_kur
    from sim2.dunya.geometri import Kutu, Nokta3
    with pytest.raises(ValueError):
        mobilite_kur(kol="ucan_hali", baslangic=[Nokta3(0, 0, 0)],
                     kutu=Kutu(100, 100, 100), akislar=Akislar(1),
                     kosu_bitis_s=1.0)
