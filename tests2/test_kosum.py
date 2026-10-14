"""
Adım 9 — `kosum/` testleri.

🔴 BURADA SINANAN ŞEY BİR SAYI DEĞİL, BİR DEFTERDİR
===================================================
Koşu döngüsü yanlışsa çıkan sayılar yine "makul" görünür: PDR bir orandır,
gecikme bir dağılımdır, ikisi de gözle yanlış görünmez. Yanlışlığı görünür
kılan tek şey korunum denklemi ile mutabakattır — ve ikisi de her koşuda
otomatik denetlenir. Bu dosya onları GERÇEK trafikte, beş senaryoda ve
otuz tohumda zorlar.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from protokoller.kosum_kosumu import DogrudanKomsu, EnYakinKimlik  # noqa: E402
from sim2.ag.paket import Paket  # noqa: E402
from sim2.kanal.girisim import Iletim  # noqa: E402
from sim2.kosum import gonderim  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import BOLUMLER, SatirYazici, sonuc_satiri  # noqa: E402
from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.gozlem.karar import Beyan, Karar  # noqa: E402
from sim2.gozlem.protokol import SonucBildirimliProtokol  # noqa: E402
from sim2.gozlem.kontrol import (KontrolIstegi,  # noqa: E402
                                 MesajBicimi, Uyandirma)

# Sınav protokollerinin uyandırma gecikmesi — bir MAC slotundan büyük olmak
# zorunda (`13` §03.5); değeri bir ölçüm değil, bir test sabiti.
GECIKME_S = 0.01
from sim2.kosum.teslim import onay_alindi, veri_alindi  # noqa: E402
from sim2.mac.alici import ALIM_SONUCLARI, sonuc_dogrula  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

PROTOKOLLER = {"dogrudan": DogrudanKomsu, "enyakin": EnYakinKimlik}


# 🔒 KÜÇÜK DÜNYA — testler için, DENEY İÇİN DEĞİL.
# 40 düğüm × tam alan ile bu dosya 914 saniye sürüyordu ve o kadar yavaş bir
# test paketi koşturulmaz olur. Deneyin çalışma noktası `Konfig`in
# VARSAYILANIDIR ve buradan etkilenmez.
#
# 🔴 BÜTÜN BOYUTLAR VARSAYILANDAN TÜRETİLİR, ELLE YAZILMAZ. Eskiden
# "alan_en_m=600.0" ve yorumda "14/600² ≈ 40/1000²" yazıyordu; alan
# 1000 → 1800 m olunca (K-097) o eşitlik sessizce bozuldu ve küçük dünya
# gerçek deneyden 3,2 kat yoğun hâle geldi. Ayrıca müfreze yarıçapı sabit
# kaldığı için "grup çapı alandan büyük" doğrulaması kırıldı — 24 test.
#   · alan  : yoğunluk (düğüm/alan) korunacak biçimde
#   · yarıçap: alanla orantılı
_VARSAYILAN = Konfig(kol="t")
_KUCUK_DUGUM = 14
_KUCUK_EN = _VARSAYILAN.alan_en_m * (_KUCUK_DUGUM
                                     / _VARSAYILAN.dugum_sayisi) ** 0.5
KUCUK = dict(dugum_sayisi=_KUCUK_DUGUM, akis_sayisi=4,
             alan_en_m=_KUCUK_EN, alan_boy_m=_KUCUK_EN,
             gorev_grup_sayisi=2,
             gorev_grup_yaricapi_m=(_VARSAYILAN.gorev_grup_yaricapi_m
                                    * _KUCUK_EN / _VARSAYILAN.alan_en_m))


def _konfig(senaryo="statik-yok", tohum=1000, bitis=6.0, kucuk=True, **ek):
    if not senaryo.endswith("-yok"):
        ek.setdefault("karistirici_guc_override_dbm", 0.0)
    if kucuk:
        for ad, deger in KUCUK.items():
            ek.setdefault(ad, deger)
    return Konfig(kol="test", senaryo=senaryo, tohum=tohum,
                  isinma_s=0.2 * bitis, olcum_bitis_s=0.8 * bitis,
                  kosu_bitis_s=bitis, **ek)


def _kos(senaryo="statik-yok", protokol="enyakin", tohum=1000, bitis=6.0,
         **ek):
    kur = kurulum_yap(_konfig(senaryo, tohum, bitis, **ek))
    p = PROTOKOLLER[protokol]
    kosu = Kosu(kur, lambda i: p())
    kosu.kostur()
    return kur, kosu


def _defter(kur, kosu):
    """🔒 `sonuc.py` ile AYNI tanım — el değiştirmiş paket uçuşta değildir."""
    from sim2.kosum.sonuc import korunum_bolumu
    rapor = korunum_bolumu(kur, kosu.dugumler)
    return rapor, rapor


# ==========================================================================
# KORUNUM ve MUTABAKAT — iki AYRI kapı
# ==========================================================================
@pytest.mark.parametrize("senaryo,protokol", [
    ("statik-yok", "dogrudan"),
    ("statik-yok", "enyakin"),
    ("bagimsiz-yok", "enyakin"),
    ("gorev-yok", "enyakin"),
    ("bagimsiz-surekli", "enyakin"),
    ("bagimsiz-reaktif", "enyakin"),
    ("gorev-aldatici", "enyakin"),
])
def test_korunum_ve_mutabakat_GERCEK_trafikte(senaryo, protokol):
    kur, kosu = _kos(senaryo, protokol, bitis=5.0)
    kontrol, mutabakat = _defter(kur, kosu)
    assert kontrol["korunum_tamam"], f"🔴 denklem kırıldı: {kontrol}"
    assert mutabakat["mutabakat_tamam"], f"🔴 mutabakat kırıldı: {mutabakat}"
    assert kontrol["uretilen"] > 0, "hiç paket üretilmemiş — test boş koşuyor"


def test_OTUZ_tohumda_defter_tutuyor():
    """🔒 Kapanış ölçütü: 30 tohum, tek bir ayrışma yok."""
    kirik = []
    for tohum in range(1000, 1030):
        kur, kosu = _kos("bagimsiz-yok", "enyakin", tohum=tohum, bitis=3.0)
        kontrol, mutabakat = _defter(kur, kosu)
        if not (kontrol["korunum_tamam"] and mutabakat["mutabakat_tamam"]):
            kirik.append((tohum, kontrol["fark"], mutabakat["ucus_farki"]))
    assert not kirik, f"🔴 defteri tutmayan tohumlar: {kirik}"


def test_TESLIM_ve_AKTARMA_gercekten_atesleniyor():
    """Boş bir koşu her şeyi doğrular. Dalların koştuğunu ayrıca sınarız."""
    kur, _ = _kos("statik-yok", "enyakin", bitis=8.0)
    s = kur.sayaclar.disa_ver()
    for ad in ("teslim_paket", "aktarilan_paket", "mac_deneme",
               "mac_gonderim_basarili", "beacon_gonderilen", "beacon_alinan",
               "alim_basarili"):
        assert s[ad] > 0, f"🔴 hiç ateşlenmeyen sayaç: {ad}"


# ==========================================================================
# ALIM SONUÇLARI — kapalı küme, toplamı denetlenir
# ==========================================================================
def test_ALIM_SONUCLARI_toplami_deneme_sayisina_esit():
    """🔴 Kusur 2'yi yakalayan denetimin ta kendisi.

    Bir alım denemesi tam olarak bir sonuç üretmek zorunda. Yarım çift
    yüzünden düşen bir KİLİT de sayılır — sayılmasaydı `cerceve_geldi` onu
    deneme sayar, `cerceve_bitti` kilit boşaldığı için hiçbir şey dönmez ve
    toplam sessizce eksik kalırdı.
    """
    kur, _ = _kos("statik-yok", "enyakin", bitis=6.0)
    s = kur.sayaclar.disa_ver()
    sayimlar = {ad: int(s[ad]) for ad in ALIM_SONUCLARI}
    toplam = sum(sayimlar.values())
    assert toplam > 0
    sonuc_dogrula(sayimlar, toplam)      # şema denetimi: bilinmeyen sebep yok


def test_YARIM_CIFT_dali_atesleniyor():
    """Adım 6a'da ölçülmüştü: hiç kimse göndermediği için %0,0 idi.

    ⚠️ KÜÇÜK DÜNYADA DEĞİL, varsayılan dünyada bakılır. β 16 dB olunca
    girişim menzili 1 767 m'ye çıktı; 600 m'lik test dünyasında herkes
    herkesi duyuyor, taşıyıcı dinleme neredeyse hiç eşzamanlı gönderim
    bırakmıyor ve yarım çiftlik dal ateşlenmiyor. Bu dalın varlığı bir
    MODEL özelliğidir, test dünyasının değil — o yüzden gerçek çalışma
    noktasında sınanır.
    """
    kur, _ = _kos("statik-yok", "enyakin", bitis=6.0, kucuk=False)
    assert kur.sayaclar.oku("alim_red_yari_cift") > 0


# ==========================================================================
# ÇEKİŞME — kanal meşgulken gönderilmez
# ==========================================================================
def test_MESGUL_kanalda_veri_gonderilmiyor():
    """🔒 Taşıyıcı dinleme fiilen işliyor mu.

    ⚠️ Onay ÇERÇEVESİ hariç: 802.11'de onay, SIFS sonrası taşıyıcı dinleme
    YAPMADAN gönderilir. Onayı da bu kurala soksaydık gerçek protokolden
    ayrılırdık ve onay çarpışmaları sistematik olarak eksik ölçülürdü.
    """
    kur = kurulum_yap(_konfig("statik-yok", bitis=5.0))
    kosu = Kosu(kur, lambda i: EnYakinKimlik())
    ihlal = []
    asil = gonderim.gonder

    anlar = []

    def izle(k, n, iletim, yuk):
        t = k.olaylar.simdi
        if yuk[0] == "veri":
            anlar.append(t)
        # 🔴 `ayni_an_haric=True` — AYNI ANDA başlayan iletim ihlal DEĞİL,
        # çarpışmanın ta kendisidir. Bayraksız bakılsaydı bu test, DCF'nin
        # birincil çarpışma mekanizmasını "hata" diye raporlardı.
        if yuk[0] != "onay" and k.dugumler[n].kanal_mesgul_mu(
                t, ayni_an_haric=True):
            ihlal.append((n, t, yuk[0]))
        asil(k, n, iletim, yuk)

    gonderim.gonder = izle
    try:
        kosu.kostur()
    finally:
        gonderim.gonder = asil
    assert not ihlal, f"🔴 meşgul kanalda gönderim: {ihlal[:5]}"
    assert anlar, "hiç veri gönderilmemiş — test boş koşuyor"


def test_AYNI_SLOTTA_biten_geri_cekilmeler_CARPISIR():
    """🔴 DCF'nin BİRİNCİL çarpışma mekanizması modelde var mı?

    Toplam bir sayıya bakmak yanıltıcı olurdu: aynı slotta bitme olasılığı
    kaç düğümün AYNI ANDA çekiştiğine bağlıdır ve o da yüke. Bu yüzden
    mekanizmanın kendisi sınanır — iki kural, ikisi de yükten bağımsız.
    """
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=3.0)
    d = kosu.dugumler[0]
    t = 1.0
    iletim = Iletim(1, kur.veri_cercevesi, t,
                    kur.kanal.yayilim.verici_gucu_w)
    kur.kanal.ortam.ekle(iletim)

    # 1) AYNI ANDA başlayan iletim, gönderim kararını ERTELETMEZ
    assert d.kanal_mesgul_mu(t, ayni_an_haric=False) is True
    assert d.kanal_mesgul_mu(t, ayni_an_haric=True) is False
    # 2) ama BİR SLOT SONRA hâlâ havadaysa ertelenir
    sonra = t + kur.zamanlar.slot_s
    assert d.kanal_mesgul_mu(sonra, ayni_an_haric=True) is True


def test_TAAHHUTLU_dugum_DONDURULMUYOR():
    """Geri çekilmesi bitmiş düğüm, aynı andaki bir iletimle dondurulamaz."""
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=3.0)
    d = kosu.dugumler[0]
    d.bekleme_baslat(1.0, 1.5)
    assert d.taahhutlu_mu(1.4) is False      # daha bitmedi → DONAR
    assert d.taahhutlu_mu(1.5) is True       # bitti → göndermeye taahhütlü
    assert d.taahhutlu_mu(1.6) is True


# ==========================================================================
# EL DEĞİŞTİRME — "veri alındı, onay kayboldu"
# ==========================================================================
def _tek_paket(kaynak=0, hedef=1, kimlik=7, ttl=8):
    return Paket(kimlik=kimlik, akis_kimligi=0, kaynak=kaynak, hedef=hedef,
                 dogum_s=0.0, boyut_bayt=512, ttl_kalan=ttl)


def test_ONAY_kaybolan_paket_DUSURULMUYOR():
    """🔴 Defterin çift saymasının tek yapısal panzehiri.

    Paket alıcıya geçmişse gönderen vazgeçse bile onu düşüremez: kaybolmadı,
    el değiştirdi. Düşürseydi aynı paket hem "düşen"e hem alıcının
    "kuyrukta"sına yazılır ve denklem GERÇEKTEN kırılırdı.
    """
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=2.0)
    d = kosu.dugumler[0]
    d.kuyruk.ekle(_tek_paket())
    kur.korunum.uret()
    kur.korunum.kuyruktan_al()
    d.ucusa_al(d.kuyruk.al(), 1)
    d.devret(d.ucus_no)                  # alıcı çözdü, onay kayboldu
    kur.korunum.ucustan_kuyruga()        # defterde el değişti
    onceki = dict(kur.korunum.dusen)
    gonderim.vazgec(kosu, d)
    assert kur.korunum.dusen == onceki, "🔴 el değiştirmiş paket düşürüldü"
    assert d.ucustaki is None


def test_EL_DEGISTIRMEYEN_paket_DUSURULUYOR():
    """Simetrik denetim: bayrak yoksa düşüş GERÇEKTEN yazılmalı."""
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=2.0)
    d = kosu.dugumler[0]
    d.kuyruk.ekle(_tek_paket())
    kur.korunum.uret()
    kur.korunum.kuyruktan_al()
    d.ucusa_al(d.kuyruk.al(), 1)
    onceki = kur.korunum.dusen["iletim_basarisiz"]
    gonderim.vazgec(kosu, d)
    assert kur.korunum.dusen["iletim_basarisiz"] == onceki + 1
    assert kur.korunum.denklem_tutuyor_mu()


def test_Y1_PSR_ALICI_tarafinda_onay_kaybi_BASARI_onaya_dayali_BASARISIZ():
    """🔒 Y1 kapısı (`v2/07` §18). Onayı kaybolan iletimde veri ALINMIŞTIR:
    öğrencinin PSR'si (alıcı tarafı, CRC) bunu başarı sayar, onaya dayalı
    oran başarısızlık. Yeniden denemenin çözülmesi de bir başarılı iletimdir;
    paket ise bir kez el değiştirir. Başkasına adresli çerçeve sayılmaz."""
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=2.0)
    s = kur.sayaclar
    d, alici, baska = kosu.dugumler[0], kosu.dugumler[1], kosu.dugumler[2]
    paket = _tek_paket(kaynak=0, hedef=5)     # alıcı ara düğüm: aktarılır
    d.kuyruk.ekle(paket)
    kur.korunum.uret()
    kur.korunum.kuyruktan_al()
    d.ucusa_al(d.kuyruk.al(), 1)
    once = {a: s.oku(a) for a in ("veri_alim_hedefte",
                                  "mac_gonderim_basarili", "aktarilan_paket")}
    bilgi = (paket, 1, d.ucus_no)

    veri_alindi(kosu, alici, 0, bilgi)        # alıcı çözdü, onay KAYBOLDU
    assert s.oku("veri_alim_hedefte") == once["veri_alim_hedefte"] + 1
    assert s.oku("mac_gonderim_basarili") == once["mac_gonderim_basarili"], \
        "onay gelmeden onaya dayalı başarı sayılmamalı"
    assert s.oku("aktarilan_paket") == once["aktarilan_paket"] + 1

    veri_alindi(kosu, alici, 0, bilgi)        # yeniden deneme de çözüldü
    assert s.oku("veri_alim_hedefte") == once["veri_alim_hedefte"] + 2
    assert s.oku("aktarilan_paket") == once["aktarilan_paket"] + 1, \
        "tekrar ikinci kez el değiştirmemeli"

    veri_alindi(kosu, baska, 0, bilgi)        # başkasına adresli
    assert s.oku("veri_alim_hedefte") == once["veri_alim_hedefte"] + 2


def test_Y1_PSR_gercek_trafikte_ONAYA_DAYALI_orandan_BUYUK():
    """Onay ancak alıcı çözdüyse gönderilir; bir onay zaman aşımı el
    değiştirmiş bir paketteyse, o el değiştirmeyi yapan iletimin onayı
    sayılmamıştır. Onay kaybı gözlenen koşuda PSR kesin olarak büyüktür."""
    kur, kosu = _kos("statik-surekli", "enyakin", bitis=5.0,
                     karistirici_baslangic_s=1.0)
    s = kur.sayaclar.disa_ver()
    assert s["mac_onaysiz_onay"] > 0, "boş geçmemeli — onay kaybı olmalı"
    assert s["veri_alim_hedefte"] >= s["mac_gonderim_basarili"]
    assert s["psr"] > s["mac_basari_orani"]


def test_Y2_SEYIRCININ_cozdugu_onay_gondereni_SERBEST_BIRAKMIYOR():
    """🔒 Y2 kapısı (`v2/07` §18). Onay yalnız göndericinin KENDİSİ çözdüğünde
    işlenir; seyircinin çözdüğü onay göndericiye ulaşmış sayılmaz (K-114
    §4.2). Olumlu yol — gönderenin kendi çözdüğü onay — bütün koşularda ve
    ölçüm aletinin Y2 kapısında (`onay_semantigi.py y2kapi`) sınanıyor."""
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=2.0)
    s = kur.sayaclar
    d, alici, seyirci = kosu.dugumler[0], kosu.dugumler[1], kosu.dugumler[2]
    paket = _tek_paket(kaynak=0, hedef=5)
    d.kuyruk.ekle(paket)
    kur.korunum.uret()
    kur.korunum.kuyruktan_al()
    d.ucusa_al(d.kuyruk.al(), 1)
    veri_alindi(kosu, alici, 0, (paket, 1, d.ucus_no))  # alıcı çözdü, onayladı
    d.onay_bekle(True)
    once = s.oku("mac_gonderim_basarili")
    onay_alindi(kosu, seyirci.kimlik, (0, d.ucus_no))   # onayı yalnız seyirci çözdü
    assert d.onay_bekleniyor, "🔴 seyircinin onayı göndereni serbest bıraktı"
    assert d.ucustaki is not None
    assert s.oku("mac_gonderim_basarili") == once


def test_ILETIM_SONUCU_kosu_sonunda_ASKIDA_deneme_ile_KAYIP_sonuc_AYRILIYOR():
    """🔴 Koşu sınırı — 11 Eylül 2026 (K-115). Bitişten sonraya düşen olaylar
    işlenmez; son anda başlayan bir veri denemesinin onay penceresi bitişi
    aşarsa deneme sayılmış ama sonucu yazılmamış olur ve kapı bunu
    `iletim_sonucu_askida` ile sayar. Sonucu GERÇEKTEN kaybolmuş bir deneme
    (onay beklenmiyorken sayılmış) ise hâlâ satırı geçersiz yapmalı."""
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=2.0)
    once, _ = _defter(kur, kosu)
    assert once["iletim_sonucu_tamam"]
    d = next(x for x in kosu.dugumler if not x.onay_bekleniyor)
    kur.sayaclar.artir("mac_deneme")          # bitişte başlamış deneme
    d.onay_bekle(True)                        # onay penceresi bitişten sonra
    askida, _ = _defter(kur, kosu)
    assert askida["iletim_sonucu_tamam"] and askida["gecerli"]
    assert askida["iletim_sonucu_askida"] == once["iletim_sonucu_askida"] + 1
    kur.sayaclar.artir("mac_deneme")          # sonucu kaybolmuş deneme
    kayip, _ = _defter(kur, kosu)
    assert not kayip["iletim_sonucu_tamam"] and not kayip["gecerli"]


def test_Y4_yere_toplama_KORUNUM_KAYIP_YERI_GECIT_SABIT_oteki_yorungeler_AYNI():
    """🔒 Y4 kapıları (`v2/07` §18). Yere toplamalı gerçek koşuda defter
    kapanır; kayıp yeri toplamı düşen paket sayısına eşittir; geçit sabit
    istasyonda durur; öteki düğümlerin konumu eşler arası kolla birebir
    aynıdır (çekimler kaymadı); satır desenin sınırlarını beyan eder."""
    from sim2.dunya.yerlesim import gecit_noktasi
    from sim2.yapilandirma.kapsam import kapsam_bolumu
    kur, kosu = _kos("bagimsiz-surekli", "enyakin", bitis=5.0,
                     karistirici_baslangic_s=1.0, trafik_deseni="yere_toplama")
    k, _ = _defter(kur, kosu)
    assert k["gecerli"], k
    assert kur.kayip_yeri is not None
    assert kur.kayip_yeri.toplam == k["dusen_toplam"] > 0
    assert sum(kur.kayip_yeri.rapor()["toplam"].values()) == k["dusen_toplam"]
    g = kur.konfig.gecit
    nokta = kur.topoloji.konum(g, 0.0)
    assert nokta == gecit_noktasi(kur.konfig)
    assert all(kur.topoloji.konum(g, t) == nokta for t in (0.5, 2.0, 4.9))
    esler = kurulum_yap(_konfig("bagimsiz-surekli", 1000, 5.0,
                                karistirici_baslangic_s=1.0))
    assert esler.kayip_yeri is None
    for i in (1, 5, kur.konfig.dugum_sayisi - 1):
        for t in (0.0, 2.5, 4.9):
            assert kur.topoloji.konum(i, t) == esler.topoloji.konum(i, t)
    assert "desen_sinirlari" in kapsam_bolumu(kur.konfig)
    assert "desen_sinirlari" not in kapsam_bolumu(esler.konfig)


def test_TEKRAR_ayni_ucus_numarasiyla_bastiriliyor():
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=2.0)
    alici = kosu.dugumler[2]
    assert not alici.tekrar_mi(0, 5)
    alici.gorduk(0, 5)
    assert alici.tekrar_mi(0, 5), "🔴 yeniden deneme bastırılmıyor"


def test_DONGUDEKI_yeniden_ziyaret_BASTIRILMIYOR():
    """🔴 Anahtar paket kimliği olsaydı bu paket sessizce yutulurdu.

    Bir yönlendirme döngüsünde aynı paket aynı komşuya İKİNCİ KEZ meşru
    olarak gelebilir. O gelişin uçuş numarası farklıdır ve bastırılmamalıdır;
    bastırılsaydı paket defterde asılı kalır ve mutabakat kırılırdı.
    """
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=2.0)
    alici = kosu.dugumler[2]
    alici.gorduk(0, 5)
    assert not alici.tekrar_mi(0, 6), "🔴 yeni atlama tekrar sanıldı"


def test_UCUS_numarasi_yeniden_denemede_SABIT_atlamada_ARTAR():
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=2.0)
    d = kosu.dugumler[0]
    d.ucusa_al(_tek_paket(), 1)
    ilk = d.ucus_no
    d.ucustan_indir()
    d.ucusa_al(_tek_paket(kimlik=8), 1)
    assert d.ucus_no == ilk + 1, "🔴 atlama başına numara artmıyor"


# ==========================================================================
# BELİRLENİMCİLİK
# ==========================================================================
def test_AYNI_tohum_AYNI_sonuc():
    a = _kos("bagimsiz-yok", "enyakin", tohum=1234, bitis=4.0)[0]
    b = _kos("bagimsiz-yok", "enyakin", tohum=1234, bitis=4.0)[0]
    assert a.sayaclar.disa_ver() == b.sayaclar.disa_ver()


def test_FARKLI_tohum_FARKLI_sonuc():
    a = _kos("bagimsiz-yok", "enyakin", tohum=1234, bitis=4.0)[0]
    b = _kos("bagimsiz-yok", "enyakin", tohum=4321, bitis=4.0)[0]
    assert a.sayaclar.oku("teslim_paket") != b.sayaclar.oku("teslim_paket") \
        or a.sayaclar.oku("mac_deneme") != b.sayaclar.oku("mac_deneme")


def test_PYTHONHASHSEED_sonucu_DEGISTIRMIYOR():
    """🔒 `hash()` kullanan bir yer kalsaydı burada patlardı."""
    kod = (
        "import sys; sys.path.insert(0, r'%s');"
        "from sim2.yapilandirma.konfig import Konfig;"
        "from sim2.kosum.kurulum import kurulum_yap;"
        "from sim2.kosum.kosu import Kosu;"
        "from protokoller.kosum_kosumu import EnYakinKimlik;"
        "k=Konfig(kol='t',senaryo='bagimsiz-yok',tohum=99,isinma_s=1.0,"
        "olcum_bitis_s=2.0,kosu_bitis_s=3.0);"
        "kur=kurulum_yap(k);Kosu(kur,lambda i:EnYakinKimlik()).kostur();"
        "print(sorted((a,v) for a,v in kur.sayaclar.disa_ver().items()))"
    ) % KOK
    ciktilar = []
    for tohum in ("0", "1", "12345"):
        p = subprocess.run([sys.executable, "-c", kod], capture_output=True,
                           text=True, env={**__import__("os").environ,
                                           "PYTHONHASHSEED": tohum,
                                           "PYTHONIOENCODING": "utf-8"})
        assert p.returncode == 0, p.stderr[-2000:]
        ciktilar.append(p.stdout)
    assert len(set(ciktilar)) == 1, "🔴 PYTHONHASHSEED sonucu değiştiriyor"


# ==========================================================================
# SONUÇ SATIRI
# ==========================================================================
def test_sonuc_satiri_BUTUN_bolumleri_tasiyor():
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=4.0)
    satir = sonuc_satiri(kur, kosu.dugumler, "dogrudan_komsu")
    assert tuple(satir) == BOLUMLER
    assert satir["korunum"]["gecerli"] is True
    assert satir["kimlik"]["kol"] == "test"
    assert satir["kimlik"]["protokol"] == "dogrudan_komsu"
    assert len(satir["kimlik"]["kosu_kimligi"]) == 24


def test_sonuc_satiri_JSON_a_cevrilebiliyor(tmp_path):
    kur, kosu = _kos("statik-yok", "dogrudan", bitis=4.0)
    satir = sonuc_satiri(kur, kosu.dugumler, "dogrudan_komsu")
    yol = tmp_path / "alt" / "sonuc.jsonl"
    with SatirYazici(yol) as y:
        y.yaz(satir)
        y.yaz(satir)
    satirlar = yol.read_text(encoding="utf-8").splitlines()
    assert len(satirlar) == 2
    geri = json.loads(satirlar[0])
    assert geri["metrikler"]["pdr"] == satir["metrikler"]["pdr"]


def test_YAZICI_bilinmeyen_tipi_SESSIZCE_gecmiyor(tmp_path):
    """🔴 Sessiz `str()` şemayı kaydırır — hata vermek zorunda."""
    yol = tmp_path / "x.jsonl"
    with SatirYazici(yol) as y:
        with pytest.raises(TypeError):
            y.yaz({"a": object()})


def test_AYNI_kurulum_AYNI_kosu_kimligi():
    a = _kos("statik-yok", "dogrudan", tohum=77, bitis=3.0)
    b = _kos("statik-yok", "dogrudan", tohum=77, bitis=3.0)
    x = sonuc_satiri(a[0], a[1].dugumler, "p")["kimlik"]
    y = sonuc_satiri(b[0], b[1].dugumler, "p")["kimlik"]
    assert x["kosu_kimligi"] == y["kosu_kimligi"]
    assert x["evren_hash"] == y["evren_hash"]
    assert x["calisma_kimligi"] == y["calisma_kimligi"]   # aynı süreç


def test_FARKLI_tohum_FARKLI_kosu_kimligi():
    a = _kos("statik-yok", "dogrudan", tohum=77, bitis=3.0)
    b = _kos("statik-yok", "dogrudan", tohum=78, bitis=3.0)
    x = sonuc_satiri(a[0], a[1].dugumler, "p")["kimlik"]
    y = sonuc_satiri(b[0], b[1].dugumler, "p")["kimlik"]
    assert x["kosu_kimligi"] != y["kosu_kimligi"]
    assert x["kurulum_hash"] == y["kurulum_hash"], \
        "🔴 tohum bir TEDAVİ alanıdır, kurulum özetine girmemeli"


# ==========================================================================
# YAPI ÖLÇÜTLERİ — kapanış şartları
# ==========================================================================
def _kod_satiri(yol: Path) -> int:
    s = yol.read_text(encoding="utf-8")
    agac = ast.parse(s)
    belge: set[int] = set()
    for n in ast.walk(agac):
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) \
                and isinstance(n.value.value, str):
            belge.update(range(n.lineno, n.end_lineno + 1))
    return sum(1 for i, x in enumerate(s.splitlines(), 1)
               if x.strip() and not x.strip().startswith("#") and i not in belge)


def test_kosu_py_YUZELLI_satiri_asmiyor():
    """🔒 Kapanış ölçütü. Büyük bir olay döngüsü hatayı SAKLAR."""
    n = _kod_satiri(KOK / "sim2" / "kosum" / "kosu.py")
    assert n <= 150, f"🔴 kosu.py {n} kod satırı — bölünmeli"


def test_sonuc_py_de_SOZLUK_LITERALI_YOK():
    """🔒 Kapanış ölçütü. Elle yazılan bir sözlük ikinci bir doğru kaynağıdır."""
    agac = ast.parse((KOK / "sim2" / "kosum" / "sonuc.py")
                     .read_text(encoding="utf-8"))
    literaller = [n for n in ast.walk(agac) if isinstance(n, ast.Dict)]
    assert not literaller, (
        f"🔴 sonuc.py'de {len(literaller)} sözlük literali var — "
        f"satır {[n.lineno for n in literaller]}")


# 🔒 İZİN LİSTESİ (denetim DD-05, K-242). Eski tarama yasak bir liste
# tutuyordu; `sys.modules`, `inspect`, `gc`, `builtins`, `exec`, depo
# kökündeki bir yardımcı modül üzerinden geçişli içe aktarma ve
# `object.__setattr__` kaçıyordu. Protokol yalnız şunları içe aktarabilir:
# kendi paketi (`protokoller`), gözlem katmanı (`sim2.gozlem`) ve aşağıdaki
# standart kütüphane modülleri. `random` bilerek yok: rastgelelik
# simülatörün eşleştirilmiş akışlarından gelir (`13` §03.7). Yeni bir modül
# gerekirse buraya gerekçesiyle eklenir.
_PROTOKOLE_IZINLI_STDLIB = frozenset((
    "__future__", "abc", "bisect", "collections", "dataclasses", "enum",
    "fractions", "functools", "heapq", "itertools", "math", "operator",
    "struct", "typing"))
_PROTOKOLE_IZINLI_PAKET = ("protokoller", "sim2.gozlem")
# Çalışma anında simülatörün içine uzanmanın yolları.
_PROTOKOLE_YASAK_AD = frozenset((
    "__import__", "exec", "eval", "compile", "globals", "locals", "vars",
    "breakpoint", "open", "input", "__builtins__"))
_PROTOKOLE_YASAK_OZNITELIK = frozenset((
    "__builtins__", "__globals__", "__dict__", "__class__", "__subclasses__",
    "__mro__", "__bases__", "__base__", "__code__", "__closure__",
    "__self__", "__func__", "__setattr__", "__delattr__",
    "__getattribute__", "__reduce__", "__reduce_ex__", "f_back", "f_locals",
    "f_globals", "f_code", "gi_frame", "cr_frame", "tb_frame",
    "tb_next"))


def _izinli_modul(ad: str) -> bool:
    if ad in _PROTOKOLE_IZINLI_STDLIB:
        return True
    return any(ad == p or ad.startswith(p + ".")
               for p in _PROTOKOLE_IZINLI_PAKET)


def _yasak_ice_aktarmalar(kaynak: str) -> list[str]:
    """Kaynakta izin listesi dışındaki her içe aktarma ve çalışma anında
    simülatörün içine uzanabilecek her ad ya da öznitelik.

    K-166 (denetim D-1): `from sim2 import kanal`, `import os, sim2.kanal`,
    `import sim2` ve dinamik içe aktarma yakalanır. DD-05 (K-242): izin
    listesi ve çalışma anı kaçamakları.
    """
    kotu: list[str] = []
    for n in ast.walk(ast.parse(kaynak)):
        if isinstance(n, ast.Import):
            kotu += [a.name for a in n.names if not _izinli_modul(a.name)]
        elif isinstance(n, ast.ImportFrom):
            if n.level > 1:
                kotu.append("." * n.level + (n.module or ""))
            elif n.level == 1:
                continue                     # `protokoller` içi göreli
            elif n.module == "sim2":         # `from sim2 import gozlem` meşru
                kotu += [f"sim2.{a.name}" for a in n.names
                         if not _izinli_modul(f"sim2.{a.name}")]
            elif not _izinli_modul(n.module or ""):
                kotu.append(n.module or "")
        elif isinstance(n, ast.Name) and n.id in _PROTOKOLE_YASAK_AD:
            kotu.append(n.id)
        elif isinstance(n, ast.Attribute) \
                and n.attr in _PROTOKOLE_YASAK_OZNITELIK:
            kotu.append(f".{n.attr}")
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) \
                and n.value in (_PROTOKOLE_YASAK_OZNITELIK
                                | _PROTOKOLE_YASAK_AD):
            kotu.append(repr(n.value))       # `getattr(x, "__globals__")`
    return sorted(set(kotu))


def test_ICE_AKTARMA_taramasi_KACAMAKLARI_yakalar():
    """🔴 Mekanizmanın kendisi sınanır (K-166)."""
    for kaynak in ("from sim2 import kanal", "import os, sim2.kanal",
                   "import sim2", "from kalibrasyon.kahin import X",
                   "import importlib", "m = __import__('sim2.kanal')",
                   "from sim2.kosum.kosu import Kosu",
                   # DD-05 (K-242): çalışma anı kaçamakları ve geçişli yol
                   "import sys\nk = sys.modules['sim2.kanal.kanal']",
                   "import inspect\nf = inspect.currentframe().f_back",
                   "import gc\no = gc.get_objects()",
                   "import builtins\nm = builtins.__import__('sim2')",
                   "exec('import sim2.kanal')",
                   "m = getattr(__builtins__, '__imp' + 'ort__')('sim2')",
                   "g = f.__globals__", "s = ().__class__.__base__",
                   "object.__setattr__(kayit, 'rssi', 0)",
                   "v = getattr(x, '__dict__')", "import random",
                   "from yardimci_kok import kanal_bilgisi",
                   "import ctypes", "from .. import kalibrasyon"):
        assert _yasak_ice_aktarmalar(kaynak), kaynak
    for kaynak in ("from sim2.gozlem.pencere import Gozlem",
                   "from sim2.gozlem import kontrol", "from sim2 import gozlem",
                   "from protokoller.aodv import AODV", "import math",
                   "from . import yardimci", "from collections import deque",
                   "v = getattr(self, ad)", "import heapq, struct"):
        assert not _yasak_ice_aktarmalar(kaynak), kaynak


def test_PROTOKOL_paketi_YALNIZ_gozlemi_goruyor():
    """🔴 Kâhin sızıntısının yapısal panzehiri — disiplin değil, GRAFİK."""
    ihlal = []
    for yol in (KOK / "protokoller").rglob("*.py"):
        kotu = _yasak_ice_aktarmalar(yol.read_text(encoding="utf-8"))
        ihlal += [(yol.name, ad) for ad in kotu]
    assert not ihlal, f"🔴 protokol katmanı sim2'nin içine uzanıyor: {ihlal}"


# ==========================================================================
# 🔴 BEACON YÜKÜ — bedeli SAYAÇTA DEĞİL, KANALDA ödenir (K-111 EK-2)
# ==========================================================================
class _YukluProtokol:
    """Beacon'a gerçekten bir şey koyan protokol.

    🔒 Depodaki üç gerçeklemenin üçü de boş yük döndürüyordu; bu yüzden
    bedelin fiilen ödenip ödenmediğini HİÇBİR test sınamıyordu ve kusur
    9 Eylül 2026'ya kadar görünmedi.
    """

    ad = "yuklu"
    __slots__ = ("_alan",)

    def __init__(self, alan: int = 20) -> None:
        self._alan = alan

    def sonraki_atlama(self, gozlem):
        from sim2.gozlem.karar import Karar
        if gozlem.paket is None or not gozlem.komsular:
            return Karar()
        hedef = gozlem.paket.hedef
        adaylar = [k.dugum for k in gozlem.komsular]
        if hedef in adaylar:
            return Karar(sonraki=hedef)
        return Karar(sonraki=min(adaylar, key=lambda n: (abs(n - hedef), n)))

    def beacon_yuku(self, gozlem) -> dict:
        return {f"r{i}": i for i in range(self._alan)}

    def beacon_alindi(self, gozlem, komsu, yuk) -> None:
        return None

    def teshis(self, dugum: int) -> dict:
        return {}


def test_BEACON_YUKU_cerceveyi_UZATIYOR():
    """🔴 Yük yalnız sayaçta ödeniyordu; çerçeve SABİT boyuttaydı.

    Ölçülmüştü: 250 baytlık bir yükte çerçeve 320 µs yerine 1 320 µs
    sürmeliydi (4,12 kat) ama 320 µs kalıyordu. Yani yükü şişiren bir
    protokol fizikte BEDAVA taze komşu bilgisi alıyordu.
    """
    from sim2.gozlem.yuk import yuk_bayt
    kur = kurulum_yap(_konfig())
    kosu = Kosu(kur, lambda i: _YukluProtokol())
    yuk = _YukluProtokol().beacon_yuku(0)
    ek = yuk_bayt(yuk)
    assert ek > 0, "test protokolü gerçekten yük taşımalı"

    bos = gonderim.beacon_cercevesi(kosu, 0)
    yuklu = gonderim.beacon_cercevesi(kosu, ek)
    assert bos is kur.beacon_cercevesi, "boş yük kurulumdaki çerçeveyi verir"
    assert yuklu.bayt == kur.konfig.beacon_bayt + ek
    assert yuklu.sure_s > bos.sure_s, "yük havada süre HARCAMAK zorunda"


def test_BEACON_YUKU_CIFT_FATURALANMIYOR():
    """🔒 Bedel TEK KAYNAKTAN okunur: çerçevenin boyutu.

    Düzeltmeden önce `Dugum` yükü, `Kosu` çerçeveyi ayrı ayrı sayıyordu;
    çerçeve yükü içerecek biçimde uzatılınca ikisi birden sayılsaydı yük
    **çift faturalanırdı**.
    """
    from sim2.gozlem.yuk import yuk_bayt
    ek = yuk_bayt(_YukluProtokol().beacon_yuku(0))
    kur, kosu = None, None
    kur = kurulum_yap(_konfig())
    kosu = Kosu(kur, lambda i: _YukluProtokol())
    kosu.kostur()
    s = kur.sayaclar.disa_ver()
    gonderilen = s["beacon_gonderilen"]
    assert gonderilen > 0, "kapı boş geçmemeli — beacon fiilen gönderilmiş olmalı"
    # Kontrol baytının beacon'dan gelen payı: tam olarak çerçeve boyutu kadar.
    beklenen_beacon_bayt = gonderilen * (kur.konfig.beacon_bayt + ek)
    assert s["kontrol_bayt"] >= beklenen_beacon_bayt
    # Onay çerçeveleri de `kontrol_bayt`a giriyor; fark onlardan gelmeli ve
    # yükün İKİ katı kadar bir fazlalık OLMAMALI.
    fazla = s["kontrol_bayt"] - beklenen_beacon_bayt
    assert fazla < gonderilen * ek, (
        f"yük çift faturalanıyor gibi: fazla={fazla}, "
        f"tek katı={gonderilen * ek}")


def test_BOS_YUKTE_sonuc_BIREBIR_AYNI():
    """🔒 Düzeltmenin bugün ölçülmüş hiçbir sayıyı değiştirmediğinin kanıtı.

    Depodaki üç protokolün üçü de `{}` döndürüyor → `yuk_bayt({}) = 0` →
    çerçeve kurulumdakiyle AYNI NESNE. Bu test onu bir iddia olmaktan
    çıkarır: boş yüklü bir koşumda beacon başına düşen kontrol baytı tam
    olarak `beacon_bayt`tır, ne eksik ne fazla.
    """
    kur, kosu = _kos(protokol="dogrudan")
    s = kur.sayaclar.disa_ver()
    gonderilen = s["beacon_gonderilen"]
    assert gonderilen > 0
    from sim2.gozlem.yuk import yuk_bayt
    assert yuk_bayt({}) == 0
    kalan = s["kontrol_bayt"] - gonderilen * kur.konfig.beacon_bayt
    assert kalan >= 0
    # Kalan yalnız ONAY çerçevelerinden gelebilir; onay boyutunun katı olmalı.
    assert kalan % kur.konfig.onay_bayt == 0, (
        f"boş yükte beacon başına fazladan bayt var: kalan={kalan}")

# ==========================================================================
# ROTA BEKLEME TAMPONU — K-131 (denetim B1)
#
# 🔴 NEDEN BU BÖLÜM VAR
# Protokolün paket başına verebileceği cevap 16 Eylül 2026'ya kadar İKİ
# ŞIKLIYDI: *"şu komşuya gönder"* ya da *"gönderme"*. İkincisi paketi ANINDA
# düşürüyordu. RFC 3561 §6.3 ise rota keşfi sırasında tamponlamayı ŞART koşar
# ve NS-2'nin AODV'si 64 paketlik bir kuyruk tutar. Tamponsuz bir AODV akış
# başlangıcında ve her rota kopmasından sonra keşif bitene kadar doğan her
# paketi kaybederdi; OLSR proaktif olduğu için bu kayba uğramazdı — yani
# eksik, karşılaştırdığımız iki aileden YALNIZ BİRİNE biniyordu.
# ==========================================================================
class _Bekleten:
    """Hedef doğrudan komşu değilse BEKLETİR — düşürmez.

    Kontrol kancası YOKTUR: yeniden sormayı tetikleyecek bir olay üretmez,
    yani paketleri yalnız SÜRE TAVANI kurtarır. Tavanın gerçekten
    ateşlendiğini görmek için istenen budur.
    """

    ad = "bekleten"
    __slots__ = ()

    def sonraki_atlama(self, gozlem):
        if gozlem.paket is None:
            return Karar()
        hedef = gozlem.paket.hedef
        for k in gozlem.komsular:
            if k.dugum == hedef:
                return Karar(sonraki=hedef)
        return Karar(beklet=True)

    def beacon_yuku(self, gozlem):
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk):
        return None

    def teshis(self, dugum):
        return {}


def _tampon_kos(bitis=5.0, senaryo="statik-yok", **ek):
    kur = kurulum_yap(_konfig(senaryo, 1000, bitis, **ek))
    kosu = Kosu(kur, lambda i: _Bekleten())
    kosu.kostur()
    return kur, kosu


def test_tampon_BOS_GECMIYOR_ve_defter_kapaniyor():
    """🔒 Kapanış ölçütü: mekanizma devredeyken kanıt sayısı > 0.

    Boş geçen bir kapı kapı değildir — `beklet` döndüren bir protokolde
    tamponun gerçekten dolduğu ÖLÇÜLMELİ, yoksa bu bölüm hiçbir şey sınamaz.
    """
    kur, kosu = _tampon_kos()
    s = kur.sayaclar.disa_ver()
    assert s["tampon_giris"] > 0, "tampon hiç kullanılmamış — test BOŞ koşuyor"
    assert s["en_yuksek_tampon"] > 0
    kontrol, mutabakat = _defter(kur, kosu)
    assert kontrol["korunum_tamam"], f"🔴 denklem kırıldı: {kontrol}"
    assert mutabakat["mutabakat_tamam"], f"🔴 mutabakat kırıldı: {mutabakat}"


def test_tampon_MUTABAKATTA_sayiliyor():
    """🔴 Tampon defterde ayrı bir havuz DEĞİL: paket hâlâ "kuyrukta"dır.

    Mutabakat, defterin `kuyrukta` sayacını FİİLEN kuyruklarda duran paketlere
    karşı denetler. Tampon oraya eklenmeseydi bekleyen her paket defterde
    görünür ama hiçbir kuyrukta olmazdı — ve mutabakat tam olarak bunu
    yakalamak için var (`cekirdek/korunum.py`: denklem tutar, model ayrışır).

    ⚠️ Bu test boş geçmesin diye koşu sonunda tamponda paket KALDIĞI ayrıca
    doğrulanıyor.
    """
    kur, kosu = _tampon_kos()
    bekleyen = sum(len(d.bekleyenler) for d in kosu.dugumler)
    assert bekleyen > 0, "koşu sonunda tamponda paket yok — test BOŞ koşuyor"
    kontrol, mutabakat = _defter(kur, kosu)
    assert mutabakat["mutabakat_tamam"]
    assert mutabakat["kuyrukta_defter"] == mutabakat["kuyrukta_gercek"]
    # 🔒 Tamponu saymayan bir mutabakat bu koşuda KIRILIRDI:
    kuyruklarda = sum(len(k) for k in kur.kuyruklar)
    assert mutabakat["kuyrukta_gercek"] == kuyruklarda + bekleyen


def test_tampon_SURE_tavani_ATESLENIYOR():
    """🔒 Süre tavanı ilan edilmiştir ve gerçekten uygulanır.

    Kontrol kancası olmayan bir protokolde tamponu boşaltacak tek şey budur.
    Ömür koşudan kısa seçilir; yoksa tavan hiç ateşlenmez ve test, uygulanmayan
    bir tavanı "uygulanıyor" sanır.
    """
    kur, kosu = _tampon_kos(bitis=20.0, rota_tamponu_omru_s=2.0)
    s = kur.sayaclar.disa_ver()
    assert s["tampon_dusen"] > 0, "süre tavanı hiç ateşlenmemiş"
    assert kur.korunum.dusen["tampon_asimi"] == s["tampon_dusen"]
    kontrol, mutabakat = _defter(kur, kosu)
    assert kontrol["korunum_tamam"] and mutabakat["mutabakat_tamam"]


def test_tampon_SAYI_tavaninda_EN_ESKI_duser():
    """🔴 Baştan atma — arayüz kuyruğunun kuralının TERSİ, ve bilinçli.

    Arayüz kuyruğu kuyruk sonu atma kullanır çünkü oradaki soru *"hangi paket
    gecikir"*dır. Burada soru *"hangi paket rotayı bekleyerek çoktan
    bayatladı"*dır ve en eski paket en bayat olandır; NS-2'nin `aodv_rqueue`si
    de onu atar.
    """
    kur, kosu = _tampon_kos(bitis=8.0, rota_tamponu_kapasitesi=2,
                            rota_tamponu_omru_s=1000.0)
    s = kur.sayaclar.disa_ver()
    assert s["tampon_dusen"] > 0, "kapasite tavanı hiç ateşlenmemiş"
    assert s["en_yuksek_tampon"] == 2, "tepe, kapasiteyi aşmamalı"
    for d in kosu.dugumler:
        assert len(d.bekleyenler) <= 2
    kontrol, mutabakat = _defter(kur, kosu)
    assert kontrol["korunum_tamam"] and mutabakat["mutabakat_tamam"]


def test_tampon_KUYRUGU_TIKAMIYOR():
    """🔴 Baş-hat tıkanması yok: bekleyen paket sıradakini engellemez.

    Paket kuyruk BAŞINDA bekletilseydi tek bir rotasız paket düğümün bütün
    kuyruğunu tıkardı — gerçek AODV'de olmayan ve yalnız reaktif aileyi vuran
    bir ceza. Ölçüt: aynı koşuda hem tamponlanan paket VAR hem de teslim VAR.
    """
    kur, kosu = _tampon_kos()
    s = kur.sayaclar.disa_ver()
    assert s["tampon_giris"] > 0
    assert s["teslim_paket"] > 0, (
        "tamponlanan paket varken hiç teslim olmamış — kuyruk tıkanmış "
        "olabilir")


def test_beklet_SIZMIYOR_tamponsuz_protokol_BIREBIR_ayni():
    """🔒 P7'nin kardeşi: `beklet` döndürmeyen protokolde satır DEĞİŞMEZ.

    Tampon mekanizması varsayılan KAPALIDIR — kapalılığı bir bayrakla değil,
    protokolün cevabıyla belirlenir. Kullanmayan protokolde üç sayacın üçü de
    sıfır kalır ve tampon hiç yaratılmaz.
    """
    kur, kosu = _kos("statik-yok", "enyakin", bitis=5.0)
    s = kur.sayaclar.disa_ver()
    assert s["tampon_giris"] == 0 and s["tampon_dusen"] == 0
    assert s["en_yuksek_tampon"] == 0
    assert all(not d.bekleyenler for d in kosu.dugumler)
    assert kur.korunum.dusen["tampon_asimi"] == 0


def test_beklet_ile_sonraki_BIRLIKTE_verilemez():
    """*"Hem gönder hem beklet"* bir niyet değildir; belirsizliği MAC kapatırdı."""
    with pytest.raises(DegismezHatasi):
        Karar(sonraki=3, beklet=True)
    Karar(beklet=True)          # tek başına geçerli
    Karar(sonraki=3)            # tek başına geçerli

# ==========================================================================
# YENİDEN SORMA — tamponun BOŞALDIĞI yol
#
# 🔴 BU BÖLÜM BİR BOŞLUKTAN SONRA YAZILDI (16 Eylül 2026). Tamponun ilk yedi
# kapısı `_Bekleten` ile koşuyordu ve o protokolün kontrol kancası YOK; yani
# `tamponu_kuyruga_dok` hiçbir testte ÇALIŞMIYORDU. Mekanizmanın en kritik
# yarısı — paketin tampondan ÇIKIP teslim edilmesi — sınanmamış kalmıştı.
# ==========================================================================
HELLO_T = MesajBicimi("T_HELLO", (("kaynak", 8),))


class _BekletSonraGonder:
    """Kontrol mesajı GELENE KADAR bekletir; geldikten sonra komşuya gönderir.

    🔒 Gerçek AODV'nin iskeleti: rota yokken tamponla, cevap gelince tamponu
    boşalt. Burada "cevap" herhangi bir kontrol mesajıdır — RREQ/RREP
    mantığını taklit etmek gerekmiyor, sınanan şey TAMPONUN BOŞALMASI.
    """

    ad = "beklet_sonra_gonder"
    # 🔒 "Rota" ACILMA_S'ten SONRA gelen ilk kontrol mesajıyla kurulur.
    # Bir eşik gerekiyor: eşiksiz kurulumda ilk kontrol mesajı daha komşu
    # tablosu dolmadan geliyor ve protokol hiç bekletmiyordu — testin boş
    # geçme kapısı bunu yakaladı ve haklıydı.
    ACILMA_S = 3.0
    __slots__ = ("kimlik", "acik")

    def __init__(self, kimlik: int) -> None:
        self.kimlik = kimlik
        self.acik = False

    def sonraki_atlama(self, gozlem):
        if gozlem.paket is None:
            return Karar()
        if not self.acik:
            # 🔒 Gerçek AODV'nin davranışı: rota YOKKEN paket düşmez, bekler.
            return Karar(beklet=True)
        hedef = gozlem.paket.hedef
        if any(k.dugum == hedef for k in gozlem.komsular):
            return Karar(sonraki=hedef)
        return Karar()                     # erişilemez: düşsün

    def beacon_yuku(self, gozlem):
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk):
        return None

    def teshis(self, dugum):
        return {}

    # --- kontrol düzlemi: hepsi ya da hiçbiri ---------------------------
    def zamanlayicilar(self):
        return {"t_hello": 0.5}

    def zamanlayici_doldu(self, gozlem, etiket):
        return (KontrolIstegi.kur(None, HELLO_T, {"kaynak": self.kimlik}),)

    def uyandi(self, gozlem, etiket):
        return ()

    def kontrol_alindi(self, gozlem, gonderen, bicim, yuk, yayin):
        if self.acik or float(gozlem.saat_s) < self.ACILMA_S:
            return ()
        self.acik = True                   # "rota bulundu"
        # 🔒 YENİDEN SORULMAYI PROTOKOL İSTER — 16 Eylül 2026 (K-135).
        # İlk kural her kontrol mesajından sonra soruyordu ve ölçüldü: gerçek
        # AODV'de 1 598 pakete karşı 146 678 tampon girişi, yani tampon
        # kontrol trafiği hızında dönen bir yoklama döngüsüne dönmüştü.
        # Kural daraltıldı; bekleyenlerini geri isteyen protokol bir
        # `Uyandirma` döndürür. ⚠️ Bu testin İDDİASI değişmedi (tampon
        # boşalmalı ve teslim olmalı) — değişen, sınav protokolünün yeni
        # sözleşmeye uyması.
        return (Uyandirma(GECIKME_S, "tampon"),)

    def iletim_basarisiz(self, gozlem, hedef, tur):
        return ()


def test_tampon_YENIDEN_SORULUP_teslim_ediliyor():
    """🔒 Kapanış ölçütü: paket tampona GİRİYOR ve oradan ÇIKIP teslim ediliyor.

    Üç şey birden ölçülür, üçü de boş geçmeye kapalı:
      1. tampona giren paket var                 (`tampon_giris > 0`)
      2. koşu sonunda tampon BOŞALMIŞ            (mekanizma tıkanmadı)
      3. teslim var                              (paket gerçekten gitti)

    ⚠️ (2) olmadan (1) ve (3) birlikte de geçerdi: tamponlanan paketler
    ölseydi ve yalnız sonradan doğanlar teslim edilseydi tablo aynı görünürdü.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    kosu = Kosu(kur, _BekletSonraGonder)
    kosu.kostur()
    s = kur.sayaclar.disa_ver()
    assert s["tampon_giris"] > 0, "tampon hiç kullanılmamış — test BOŞ koşuyor"
    assert s["teslim_paket"] > 0, "hiç teslim yok — tampon tıkanmış olabilir"
    assert s["tampon_dusen"] == 0, (
        "tavan ateşlenmiş: bu koşu yeniden sormayı değil tavanı ölçüyor")
    kalan = sum(len(d.bekleyenler) for d in kosu.dugumler)
    assert kalan == 0, f"tampon boşalmamış, {kalan} paket asılı kaldı"
    kontrol, mutabakat = _defter(kur, kosu)
    assert kontrol["korunum_tamam"] and mutabakat["mutabakat_tamam"]


def test_tampon_dokerken_kuyruk_DOLARSA_kalanlar_TAMPONDA_kalir():
    """🔴 BU KUSUR YAZARKEN BULUNDU ve düzeltildi (16 Eylül 2026).

    İlk yazımda dökme döngüsü kuyruk dolsa bile sürüyordu ve kalan HER paket
    `kuyruk_tasmasi` ile düşüyordu: GEÇİCİ bir doluluk tamponun tamamını yok
    ederdi — tamponun var olma sebebinin tam tersi. Bekleyen paketin süre
    tavanı zaten işliyor; onu bir kuyruk doluluğu yüzünden erken öldürmenin
    gerekçesi yok.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0, kuyruk_kapasitesi=3))
    d = Kosu(kur, lambda i: _Bekleten()).dugumler[0]
    yapay = [Paket(kimlik=900 + n, akis_kimligi=0, kaynak=0, hedef=1,
                   dogum_s=0.0, boyut_bayt=512, ttl_kalan=8)
             for n in range(5)]
    # Kuyruğu TAM doldur, kalanları tampona koy.
    for p in yapay[:3]:
        assert d.kuyruga_al(p, uretim=True)
    for p in yapay[3:]:
        kur.korunum.uret()
        d.bekleyenler.append(p)
    assert d.kuyruk.dolu_mu and len(d.bekleyenler) == 2

    tasindi = d.tamponu_kuyruga_dok()
    assert tasindi is False, "dolu kuyruğa hiçbir şey taşınamamalı"
    assert len(d.bekleyenler) == 2, "kalanlar TAMPONDA kalmalı, düşmemeli"
    assert kur.korunum.dusen["kuyruk_tasmasi"] == 0

    # Kuyrukta yer açılınca dökme çalışır.
    d.kuyruk.al()
    assert d.tamponu_kuyruga_dok() is True
    assert len(d.bekleyenler) == 1, "yer kadarı taşınmalı, fazlası değil"
    assert kur.korunum.dusen["kuyruk_tasmasi"] == 0

# ==========================================================================
# BEYAN KANALI — K-134 (kancalar da beyan döndürür · düşme sebebi beyana bakar)
#
# 🔴 İKİSİ DE ÖLÇÜLMÜŞ BİR EKSİKTEN SONRA YAZILDI. `Karar.beyan` protokolün
# *"rotam koptu"* diyebildiği TEK kanaldı ve yalnız VERİ GÖNDERME kararında
# açılıyordu; kuyruğu boş bir düğüm hiçbir şey bildiremiyordu. Ve düşme
# sebebi `rota_gecersiz` şemada ayrılmıştı ama ona giden dal YOKTU — ölçüldü:
# 320 beyan, 0 düşüş.
# ==========================================================================
class _Gecersizleyen:
    """Her veri kararında `rota_gecersiz` beyan eder ve göndermez."""

    ad = "gecersizleyen"
    __slots__ = ()

    def sonraki_atlama(self, gozlem):
        return Karar(sonraki=None, beyan=(Beyan("rota_gecersiz", komsu=1),))

    def beacon_yuku(self, gozlem):
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk):
        return None

    def teshis(self, dugum):
        return {}


def test_rota_gecersiz_DUSME_SEBEBI_olarak_kullaniliyor():
    """🔴 Şemada ayrılmış sebebe giden dal DÖŞENDİ (K-134).

    Ölçüldü (düzeltmeden önce): her kararda `rota_gecersiz` beyan eden bu
    protokolde sayaç 320 arttı ama `rota_gecersiz` sebebiyle düşüş **0**
    kaldı; 320 paketin hepsi `hedef_yok` yazdı. Sebep listesi bir ŞEMA
    taahhüdüdür ve protokoller yazılmadan ÖNCE ayrılmıştı.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    Kosu(kur, lambda i: _Gecersizleyen()).kostur()
    d = kur.korunum.dusen
    assert d["rota_gecersiz"] > 0, "sebep hâlâ ölü — dal döşenmemiş"
    assert d["hedef_yok"] == 0, "beyan varken `hedef_yok` yazılmamalı"
    assert kur.sayaclar.disa_ver()["kopma_rota_gecersiz"] == d["rota_gecersiz"]


def test_beyansiz_dusus_HALA_hedef_yok():
    """🔒 Kapı boş geçmesin: beyan YOKKEN eski sebep korunuyor.

    Yalnız birinci testle, `dus(...)` çağrısını sabit `rota_gecersiz` yapan
    bir gerçekleme de geçerdi.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    Kosu(kur, lambda i: DogrudanKomsu()).kostur()
    d = kur.korunum.dusen
    assert d["hedef_yok"] > 0, "test BOŞ koşuyor — hiç `hedef_yok` düşüşü yok"
    assert d["rota_gecersiz"] == 0
    assert d["politika"] == 0


# ==========================================================================
# POLİTİKA DÜŞMESİ — K-171 (`v2/15` A1)
#
# 🔴 DESPARETE v0.1 geçit dışı hedefe giden komutu BİLEREK taşımaz (K-160
# §10 C) ve bu düşüş `hedef_yok`a yazılıyordu: "rota bulunamadı" ile
# "tasarım gereği taşınmadı" aynı sayıda toplanıyordu.
# ==========================================================================
class _Politikaci:
    """Her veri kararında `politika` beyan eder ve göndermez."""

    ad = "politikaci"
    __slots__ = ()

    def sonraki_atlama(self, gozlem):
        return Karar(sonraki=None, beyan=(Beyan("politika"),))

    def beacon_yuku(self, gozlem):
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk):
        return None

    def teshis(self, dugum):
        return {}


def test_politika_DUSME_SEBEBI_ayri_ve_ROTA_olayi_DEGIL():
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    Kosu(kur, lambda i: _Politikaci()).kostur()
    d = kur.korunum.dusen
    s = kur.sayaclar.disa_ver()
    assert d["politika"] > 0, "test BOŞ koşuyor — hiç politika düşüşü yok"
    assert d["hedef_yok"] == 0 and d["rota_gecersiz"] == 0
    assert s["politika_dusen"] == d["politika"]
    # rota olayı değil: kopma sayaçlarına ve rota defterine GİRMEZ
    assert s["kopma_rota_gecersiz"] == 0 and s["kopma_algilanan"] == 0
    assert kur.rota_defteri.sayim("politika") == 0


def test_politika_beyani_YALNIZ_dusen_kararda():
    """🔒 Gönderilen ya da bekletilen pakette anlamsız; `rota_gecersiz`le
    birlikte düşme sebebi belirsiz; kancada elde paket yok."""
    from sim2.gozlem.kontrol import KontrolHatasi, niyetleri_dogrula
    Karar(sonraki=None, beyan=(Beyan("politika"),))
    with pytest.raises(DegismezHatasi):
        Karar(sonraki=3, beyan=(Beyan("politika"),))
    with pytest.raises(DegismezHatasi):
        Karar(beklet=True, beyan=(Beyan("politika"),))
    with pytest.raises(DegismezHatasi):
        Karar(beyan=(Beyan("politika"), Beyan("rota_gecersiz", komsu=1)))
    with pytest.raises(KontrolHatasi):
        niyetleri_dogrula((Beyan("politika"),), beyan_izinli=True)
    niyetleri_dogrula((Beyan("kopma", komsu=1),), beyan_izinli=True)


# ==========================================================================
# KOŞU KİMLİĞİ — K-171: farklı koşu → farklı kimlik
# ==========================================================================
class _Parametreli(DogrudanKomsu):
    """`kimlik_parametreleri()` bildiren sınav protokolü."""

    def __init__(self, esik):
        super().__init__()
        self._esik = esik

    def kimlik_parametreleri(self):
        return {"esik": self._esik}


def _kimlik(kur, kosu, ad="p"):
    return sonuc_satiri(kur, kosu.dugumler, ad)["kimlik"]


def test_FARKLI_tedavi_FARKLI_kosu_kimligi():
    """🔴 Eskiden tedavi alanlarından yalnız `kol` ve `tohum` kimliğe
    giriyordu: aynı kol ve tohumla farklı senaryo AYNI kimliği taşırdı."""
    a = _kos("statik-yok", "dogrudan", tohum=77, bitis=3.0)
    b = _kos("statik-surekli", "dogrudan", tohum=77, bitis=3.0)
    x, y = _kimlik(*a), _kimlik(*b)
    assert x["kol"] == y["kol"] and x["tohum"] == y["tohum"]
    assert x["tedavi_hash"] != y["tedavi_hash"]
    assert x["kosu_kimligi"] != y["kosu_kimligi"]


def test_FARKLI_protokol_FARKLI_kosu_kimligi():
    """🔴 Protokol kodu ve parametreleri hiçbir özete girmiyordu."""
    def kos(fabrika):
        kur = kurulum_yap(_konfig("statik-yok", 77, 3.0))
        kosu = Kosu(kur, fabrika)
        kosu.kostur()
        return kur, kosu
    dogrudan = _kimlik(*kos(lambda i: DogrudanKomsu()))
    enyakin = _kimlik(*kos(lambda i: EnYakinKimlik()))
    p1 = _kimlik(*kos(lambda i: _Parametreli(1)))
    p1_yine = _kimlik(*kos(lambda i: _Parametreli(1)))
    p2 = _kimlik(*kos(lambda i: _Parametreli(2)))
    # aynı konfig, aynı ad ("p") — yalnız protokol farklı
    assert dogrudan["kurulum_hash"] == enyakin["kurulum_hash"]
    assert dogrudan["tedavi_hash"] == enyakin["tedavi_hash"]
    assert dogrudan["protokol_hash"] != enyakin["protokol_hash"]
    assert dogrudan["kosu_kimligi"] != enyakin["kosu_kimligi"]
    assert p1["kosu_kimligi"] == p1_yine["kosu_kimligi"]
    assert p1["protokol_hash"] != p2["protokol_hash"]
    assert p1["kosu_kimligi"] != p2["kosu_kimligi"]
    assert p1["protokol_hash"] != dogrudan["protokol_hash"]


# ==========================================================================
# PDR YÖN AYRIMI — K-171: telemetri (geçide) · komut (geçitten)
# ==========================================================================
def test_yere_toplamada_PDR_telemetri_ve_komut_AYRI():
    kur, kosu = _kos("bagimsiz-yok", "enyakin", bitis=5.0,
                     trafik_deseni="yere_toplama")
    m = sonuc_satiri(kur, kosu.dugumler, "enyakin")["metrikler"]
    g = kur.konfig.gecit
    sinif = {a.kimlik: a.hedef == g for a in kur.trafik.akislar}
    for sonek, pencere in (("", False), ("_pencere", True)):
        dogan = kur.paket_defteri.dogumlar(pencere)
        teslim = kur.paket_defteri.kayitlar(pencere)
        for ad, telemetri_mi in (("telemetri", True), ("komut", False)):
            u = sum(1 for _, a, _ in dogan if sinif[a] is telemetri_mi)
            t = sum(1 for k in teslim if sinif[k.akis_kimligi] is telemetri_mi)
            assert u > 0, f"{ad}{sonek}: test BOŞ koşuyor"
            assert m[f"pdr_{ad}{sonek}"] == t / u
        # iki sınıf birlikte tek PDR'yi verir
        toplam_u = len(dogan)
        assert m[f"pdr{sonek}"] == len(teslim) / toplam_u


def test_esler_arasinda_PDR_sinif_alani_YOK():
    """🔒 Eşler arası desende satır birebir eskisi gibi."""
    kur, kosu = _kos("statik-yok", "enyakin", bitis=3.0)
    m = sonuc_satiri(kur, kosu.dugumler, "enyakin")["metrikler"]
    assert not any(k.startswith(("pdr_telemetri", "pdr_komut")) for k in m)


class _KancadanBildiren:
    """Kontrol kancalarından beyan döndürür — VERİ göndermeden.

    🔒 Kapının çekirdeği: bu protokol `sonraki_atlama`da HİÇ beyan etmez.
    Sayaç yine de artıyorsa beyan kanalı kancalardan açılmış demektir.
    """

    ad = "kancadan_bildiren"
    __slots__ = ("kimlik",)

    def __init__(self, kimlik: int) -> None:
        self.kimlik = kimlik

    def sonraki_atlama(self, gozlem):
        return Karar()                      # beyan YOK

    def beacon_yuku(self, gozlem):
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk):
        return None

    def teshis(self, dugum):
        return {}

    def zamanlayicilar(self):
        return {"bildir": 0.5}

    def zamanlayici_doldu(self, gozlem, etiket):
        return (Beyan("kopma", komsu=(self.kimlik + 1) % 4),)

    def uyandi(self, gozlem, etiket):
        return ()

    def kontrol_alindi(self, gozlem, gonderen, bicim, yuk, yayin):
        return ()

    def iletim_basarisiz(self, gozlem, hedef, tur):
        return ()


def test_KANCADAN_beyan_sayaca_giriyor():
    """🔴 Beyan artık ÖĞRENİLDİĞİ anda söylenebiliyor (K-134).

    Öncesinde tek kanal veri gönderme kararıydı ve kuyruğu boş bir düğüm
    hiçbir şey bildiremiyordu — `algilama_duyarliligi` proaktif aileyi
    sistematik olarak düşük gösterirdi (`06` §8 koşul 3'ün ihlali).
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    Kosu(kur, _KancadanBildiren).kostur()
    s = kur.sayaclar.disa_ver()
    assert s["kopma_algilanan"] > 0, (
        "kancadan gelen beyan sayaca girmemiş — kanal kapalı")
    assert kur.rota_defteri.kopma_algilanan == s["kopma_algilanan"], (
        "sayaç ile rota defteri ayrışmış — beyan işleme iki yerde olabilir")


def test_Karar_niyetlerinde_Beyan_REDDEDILIYOR():
    """🔒 İki yol açılmadı: `Karar`ın zaten bir `beyan` alanı var.

    Aynı şeyi iki yerden söyleyebilmek `03` §B5'in hatasıdır ve sayaç iki
    kez artabilirdi.
    """
    from sim2.gozlem.kontrol import KontrolHatasi
    with pytest.raises(KontrolHatasi):
        Karar(niyetler=(Beyan("kopma"),))
    Karar(beyan=(Beyan("kopma"),))          # doğru yol


# ==========================================================================
# Y1 · K-151 — her unicast sonucu, isteyen protokole bildirilir
# ==========================================================================
def _sonuc_sayan_aodv():
    from protokoller.aodv import AODV

    class SonucSayan(AODV):
        def __init__(self, kimlik):
            super().__init__(kimlik)
            self.sonuclar = []
            self.sira_ihlali = 0

        def iletim_sonucu(self, gozlem, hedef, basarili, tekrar, tur):
            self.sonuclar.append((hedef, basarili, tekrar, tur))

        def iletim_basarisiz(self, gozlem, hedef, tur):
            # 🔒 Sıra: bildirim, `iletim_basarisiz`den ÖNCE gelmiş olmalı.
            son = self.sonuclar[-1] if self.sonuclar else None
            if son is None or son[0] != hedef or son[1] or son[3] != tur:
                self.sira_ihlali += 1
            return super().iletim_basarisiz(gozlem, hedef, tur)
    return SonucSayan


def test_Y1_SONUC_BILDIRIMI_simulatorun_KENDI_SAYACLARIYLA_birebir():
    """🔴 Bildirimler MAC'in kendi sayımıyla eşleşmeli — boş geçemez.

    Veri başarısı = `mac_gonderim_basarili` · her vazgeçme = bir
    `iletim_basarisiz` bildirimi · kontrol başarısı = onaylanan unicast.
    Tekrar sayısı 0 ile yeniden deneme sınırı arasında; vazgeçmede sınırın
    kendisi. Hareketli dünyada tekrarlı başarı da görülmeli.
    """
    sinif = _sonuc_sayan_aodv()
    kfg = _konfig("bagimsiz-yok", 1000, 20.0)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, sinif)
    assert isinstance(kosu.dugumler[0].protokol, SonucBildirimliProtokol)
    kosu.kostur()
    m = sonuc_satiri(kur, kosu.dugumler, "y1")["metrikler"]
    tum = [s for d in kosu.dugumler for s in d.protokol.sonuclar]
    veri_basari = sum(1 for _h, b, _t, tur in tum if b and tur == "veri")
    kontrol_basari = sum(1 for _h, b, _t, tur in tum if b and tur == "kontrol")
    vazgecme = [t for _h, b, t, _tur in tum if not b]
    assert veri_basari and vazgecme and kontrol_basari, "sınav boş geçti"
    assert veri_basari == m["mac_gonderim_basarili"]
    assert kontrol_basari == m["kontrol_unicast_onaylanan"]
    assert len(vazgecme) == m["kontrol_basarisiz_bildirim"]
    assert len(tum) == m["sonuc_bildirimi"]
    sinir = kfg.yeniden_deneme_siniri
    assert all(t == sinir for t in vazgecme), "vazgeçmede tekrar = sınır"
    assert all(0 <= t <= sinir for _h, _b, t, _tur in tum)
    assert any(b and t > 0 for _h, b, t, _tur in tum), "tekrarlı başarı yok"
    assert sum(d.protokol.sira_ihlali for d in kosu.dugumler) == 0, (
        "bildirim `iletim_basarisiz`den sonra geldi")


def test_Y1_bildirimi_TASIMAYAN_protokol_hic_CAGRILMAZ():
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    kosu = Kosu(kur, lambda i: DogrudanKomsu())
    assert not isinstance(DogrudanKomsu(), SonucBildirimliProtokol)
    kosu.kostur()
    assert not any(d.sonuc_kancasi for d in kosu.dugumler)
    assert kur.sayaclar.disa_ver()["sonuc_bildirimi"] == 0


class _NiyetDonduren(DogrudanKomsu):
    def iletim_sonucu(self, gozlem, hedef, basarili, tekrar, tur):
        return (Beyan("kopma", komsu=hedef),)


def test_Y1_NIYET_DONDUREN_bildirim_REDDEDILIR():
    """🔒 Bildirim yalnız protokolün geçmişine girer; bir eyleme bağlanamaz."""
    from sim2.kosum.kontrol_durum import KontrolDuzlemiHatasi
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    with pytest.raises(KontrolDuzlemiHatasi):
        Kosu(kur, lambda i: _NiyetDonduren()).kostur()


# ==========================================================================
# Y2 · K-151 — protokolün veri başlığı çerçeveyi uzatır, EK YÜKE sayılır
# ==========================================================================
class _Baslikli(DogrudanKomsu):
    veri_baslik_bayt = 36


def test_Y2_VERI_BASLIGI_cerceveyi_uzatir_ve_YONLENDIRME_EK_YUKUNE_sayilir():
    from sim2.kanal.cerceve import cerceve_kur
    kfg = _konfig("statik-yok", 1000, 6.0)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: _Baslikli())
    assert kosu.veri_cercevesi.bayt == kfg.paket_bayt + 36
    kosu.kostur()
    m = kur.sayaclar.disa_ver()
    iletim = m["mac_deneme"]
    assert iletim > 0, "sınav boş geçti"
    assert m["veri_bayt"] == iletim * kfg.paket_bayt, "veri = yalnız yük"
    assert m["veri_baslik_bayt"] == iletim * 36
    fark = (cerceve_kur(kfg, "veri", bayt=kfg.paket_bayt + 36).sure_s
            - cerceve_kur(kfg, "veri").sure_s)
    assert m["veri_baslik_airtime_s"] == pytest.approx(iletim * fark)
    assert m["nrl_bayt"] == pytest.approx(
        (m["kontrol_bayt"] + m["veri_baslik_bayt"]) / m["veri_bayt"])
    assert m["nrl_airtime"] == pytest.approx(
        (m["kontrol_airtime_s"] + m["veri_baslik_airtime_s"])
        / m["veri_airtime_s"])


def test_Y2_BASLIKSIZ_protokolde_cerceve_AYNI_ve_sayac_SIFIR():
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    kosu = Kosu(kur, lambda i: DogrudanKomsu())
    assert kosu.veri_cercevesi is kur.veri_cercevesi
    kosu.kostur()
    m = kur.sayaclar.disa_ver()
    assert m["veri_baslik_bayt"] == 0 and m["veri_baslik_airtime_s"] == 0


class _NegatifBaslik(DogrudanKomsu):
    veri_baslik_bayt = -4


def test_Y2_NEGATIF_baslik_REDDEDILIR():
    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    with pytest.raises(DegismezHatasi):
        Kosu(kur, lambda i: _NegatifBaslik())


# --------------------------------------------------------------------------
# K-157 · PAKET KİMLİĞİ GÖZLEMDE — `(kaynak, kaynak_sira)`
# --------------------------------------------------------------------------
def test_K157_kaynak_sira_GOZLEME_ulasiyor_ROLEDE_ayni():
    """Gerçek koşuda: kaynakta (atlama 0) her kaynağın sırası artarak görünür
    (kuyruk FIFO) ve birden çok değer alır; rölede görülen her kimlik kaynakta
    önce görülmüştür. Alan hep 0 kalsaydı ya da rölede değişseydi kırılırdı."""
    gorulen: list[tuple[int, int, int, int]] = []

    class Kayitci(EnYakinKimlik):
        __slots__ = ()

        def sonraki_atlama(self, gozlem):
            p = gozlem.paket
            if p is not None:
                gorulen.append((gozlem.dugum, p.kaynak, p.kaynak_sira,
                                p.atlama_sayisi))
            return super().sonraki_atlama(gozlem)

    kur = kurulum_yap(_konfig("statik-yok", 1000, 6.0))
    Kosu(kur, lambda i: Kayitci()).kostur()
    kaynakta: dict[int, list[int]] = {}
    for dugum, kaynak, sira, atlama in gorulen:
        if atlama == 0:
            assert dugum == kaynak
            kaynakta.setdefault(kaynak, []).append(sira)
    assert kaynakta, "sınav boş geçti"
    for kaynak, siralar in kaynakta.items():
        assert siralar == sorted(siralar), f"{kaynak}: kaynakta sıra geriledi"
        assert len(set(siralar)) > 1, f"{kaynak}: tek sıra görüldü"
    roleler = [(k, s) for d, k, s, a in gorulen if a > 0]
    assert roleler, "sınav boş geçti: röle yok"
    assert all(s in kaynakta[k] for k, s in roleler)


# ==========================================================================
# `cerceve_duyuldu` — `v2/15` B1 · B2 (K-172)
# ==========================================================================
class _Duyan(EnYakinKimlik):
    """Çözülen her çerçeveyi kaydeder; davranışı `EnYakinKimlik`in aynısı."""

    def __init__(self, kayit):
        self._kayit = kayit

    def cerceve_duyuldu(self, gozlem, gonderen, tur, hedef, rssi_dbm, paket):
        self._kayit.append((gozlem.dugum, gonderen, tur, hedef, rssi_dbm,
                            None if paket is None else
                            (paket.kaynak, paket.kaynak_sira, paket.hedef)))


def _duyan_kos(senaryo="statik-yok", **ek):
    kayit: list = []
    kur = kurulum_yap(_konfig(senaryo, 1000, 4.0, **ek))
    kosu = Kosu(kur, lambda i: _Duyan(kayit))
    kosu.kostur()
    return kur, kosu, kayit


def test_B1_her_BASARILI_alimda_BIR_kez_ve_DAVRANIS_degismiyor():
    kur, kosu, kayit = _duyan_kos()
    s = kur.sayaclar.disa_ver()
    assert len(kayit) == s["duyma_bildirimi"] == s["alim_basarili"] > 0
    turler = {k[2] for k in kayit}
    assert {"veri", "onay", "beacon"} <= turler
    for dugum, gonderen, tur, hedef, rssi, paket in kayit:
        assert gonderen != dugum and isinstance(rssi, int)
        assert (paket is not None) == (tur == "veri")
        assert (hedef is None) == (tur == "beacon")
    # başkasına adresli veri çerçevesi de gelir (kulak misafiri)
    assert any(k[2] == "veri" and k[3] != k[0] for k in kayit)
    # 🔒 kanca hiçbir şeyi değiştirmez: kancasız ikizle birebir aynı satır
    ikiz_kur, ikiz = _kos("statik-yok", "enyakin", bitis=4.0)
    a = sonuc_satiri(kur, kosu.dugumler, "p")["metrikler"]
    b = sonuc_satiri(ikiz_kur, ikiz.dugumler, "p")["metrikler"]
    fark = {k for k in a if a[k] != b.get(k)} - {"duyma_bildirimi",
                                                  "duyma_bildirimi_pencere"}
    assert not fark, fark
    assert b["duyma_bildirimi"] == 0, "kancasız protokol bildirim almamalı"


def test_B1_BELIRLENIMCI_ve_KARISTIRICI_cercevesi_SIZMIYOR():
    _, _, a = _duyan_kos("statik-surekli")
    kur, _, b = _duyan_kos("statik-surekli")
    assert a == b and a
    assert all(0 <= k[1] < kur.konfig.dugum_sayisi for k in a)


def test_B2_RSSI_hatasi_SIFIR_ortalamali_ve_sigma_BEYANLI():
    """Aynı çerçeveler (davranış değişmiyor) σ 0 ve σ 2 dB ile: fark N(0, 2²)
    + yuvarlama. Hata alım kararına girmez — kayıtlar sıra sıra eşleşir."""
    _, _, sifir = _duyan_kos(rssi_olcum_sigma_db=0.0)
    _, _, iki = _duyan_kos(rssi_olcum_sigma_db=2.0)
    assert [k[:4] for k in sifir] == [k[:4] for k in iki]
    fark = [b[4] - a[4] for a, b in zip(sifir, iki)]
    n = len(fark)
    ort = sum(fark) / n
    sd = (sum((f - ort) ** 2 for f in fark) / (n - 1)) ** 0.5
    assert n > 500
    assert abs(ort) < 0.2 and 1.8 < sd < 2.3, (n, ort, sd)


def test_B1_NIYET_dondurmek_HATA():
    class Donduren(_Duyan):
        def cerceve_duyuldu(self, *a):
            return (Uyandirma(1.0, "x"),)
    from sim2.kosum.kontrol_durum import KontrolDuzlemiHatasi
    kur = kurulum_yap(_konfig("statik-yok", 1000, 2.0))
    with pytest.raises(KontrolDuzlemiHatasi):
        Kosu(kur, lambda i: Donduren([])).kostur()


def test_A2_duyma_menzili_ISLEM_KAZANCIYLA_genisler():
    """K-173: önbelge ×22 → menzil ×22^(1/α); kapalıyken birebir."""
    kapali = kurulum_yap(_konfig("statik-yok", 1000, 2.0))
    acik = kurulum_yap(_konfig("statik-yok", 1000, 2.0, islem_kazanci=True,
                               bant_genisligi_hz=22e6))
    assert kapali.duyanlar_menzili_m == kapali.konfig.girisim_menzili_m
    a = acik.konfig.yol_kaybi_usteli
    assert acik.duyanlar_menzili_m == pytest.approx(
        acik.konfig.girisim_menzili_m * 22.0 ** (1.0 / a), rel=1e-12)


# ==========================================================================
# A3 · GÜCE DAYALI TAŞIYICI DİNLEME + ED-CCA — `v2/15` A3 (K-174)
# ==========================================================================
def test_A3_kip_KAPALI_KUME_varsayilan_GEOMETRIK():
    assert Konfig(kol="t").tasiyici_dinleme == "geometrik"
    with pytest.raises(DegismezHatasi):
        Konfig(kol="t", tasiyici_dinleme="sezgi")


def _a3_kur(**ek):
    kur = kurulum_yap(_konfig("statik-yok", 1000, 2.0,
                              tasiyici_dinleme="guc", **ek))
    kosu = Kosu(kur, lambda i: DogrudanKomsu())
    a, b = min(((i, j) for i in range(kur.dugum_sayisi)
                for j in range(kur.dugum_sayisi) if i < j),
               key=lambda c: kur.topoloji.mesafe(c[0], c[1], 0.5))
    iletim = Iletim(a, kur.veri_cercevesi, 0.5,
                    kur.kanal.yayilim.verici_gucu_w)
    kur.kanal.ortam.ekle(iletim)
    return kur, kosu.dugumler[b], iletim


def test_A3_ONBELGE_sezme_KILIT_enerji_sezme_ESIK():
    """Üç dal: kilitliyse meşgul (ED eşiği ne olursa olsun) · kilitsiz ve
    enerji eşiğin altındaysa BOŞ (geometrik kip burada meşgul derdi) ·
    kilitsiz ama enerji eşiği aşıyorsa meşgul."""
    t = 0.5 + 1e-4
    kur, d, iletim = _a3_kur(ed_esigi_dbm=100.0)
    assert not d.kanal_mesgul_mu(t), "kilit yok, enerji eşik altı → boş"
    d.alici.cerceve_geldi(iletim, 0.5)
    assert d.alici.kilitli_iletim is iletim, "en yakın çift kilitlenmeli"
    assert d.kanal_mesgul_mu(t)
    assert d.mesgul_bitisi_s(t) == pytest.approx(iletim.bitis_s)
    _, d2, _ = _a3_kur(ed_esigi_dbm=-200.0)
    assert d2.kanal_mesgul_mu(t), "kilit yok ama enerji eşiğin üstünde"
    # `cca_s`: aynı anda başlayan iletim henüz sezilmez
    assert not d2.kanal_mesgul_mu(0.5, ayni_an_haric=True)


def test_A3_ED_surekli_karistirici_VERICIYI_SUSTURUR():
    """🔒 KAPI (`v2/15` A3). Sürekli karıştırıcının enerjisi her düğümde ED
    eşiğinin üstündeyken, açıldığı andan sonra HİÇBİR düğüm iletime
    başlamaz (veri, beacon); geometrik kipte gürültü karıştırıcısı taşıyıcı
    dinlemeye görünmez ve düğümler göndermeye devam eder."""
    ortak = dict(karistirici_baslangic_s=1.0, karistirici_guc_override_dbm=40.0)
    kur, _ = _kos("statik-surekli", "enyakin", bitis=5.0,
                  tasiyici_dinleme="guc", **ortak)
    s = kur.sayaclar.disa_ver()
    assert kur.konfig.olcum_penceresi[0] >= 1.0
    assert s["mac_deneme_pencere"] == 0 and s["beacon_gonderilen_pencere"] == 0
    assert s["mac_deneme"] > 0, "açılmadan önce gönderilmeli (test boş değil)"
    geo, _ = _kos("statik-surekli", "enyakin", bitis=5.0, **ortak)
    assert geo.sayaclar.disa_ver()["mac_deneme_pencere"] > 0


def test_A3_TEK_CARPISMA_ALANINDA_geometrikle_ESDEGER():
    """Bianchi'nin rejimi (herkes herkesi duyar): ED eşiği her iletimi
    sezecek kadar düşükken güç kipi geometrik kiple aynı MAC davranışını
    verir. Birebir değil — sezme `cca_s` sürer ve donma alım kararından
    sonra gelir — ama deneme, çarpışma ve teslim %5 içinde."""
    sonuc = []
    for ek in ({}, {"tasiyici_dinleme": "guc", "ed_esigi_dbm": -200.0}):
        kur, _ = _kos("statik-yok", "enyakin", bitis=6.0, **ek)
        s = kur.sayaclar.disa_ver()
        sonuc.append((s["mac_deneme"], s["alim_red_mesgul"], s["teslim_paket"]))
    for a, b in zip(*sonuc):
        assert a > 0 and abs(a - b) <= 0.05 * a, sonuc


def test_A3_HAREKETLI_karistirici_10_ms_SABIT_olan_gecis_ya_da_ufuk():
    """Karıştırıcı yüzünden donmuş düğüm: hareketliyse en geç
    `karistirici_denetim_araligi_s` sonra yeniden bakar; sabit sürekli
    karıştırıcıda geçiş yok → ufuk (beacon aralığı)."""
    ortak = dict(tasiyici_dinleme="guc", karistirici_baslangic_s=0.5,
                 karistirici_guc_override_dbm=40.0)
    t = 1.0
    for aile, bekle in (("hava_eslik", "denetim"), ("tekli_merkez", "ufuk")):
        kur = kurulum_yap(_konfig("statik-surekli", 1000, 3.0,
                                  tehdit_senaryosu=aile, **ortak))
        kosu = Kosu(kur, lambda i: DogrudanKomsu())
        d = kosu.dugumler[0]
        assert kur.kanal.karistirici.hareketli == (aile == "hava_eslik")
        assert d.karistirici_mesgul_mu(t) and d.kanal_mesgul_mu(t)
        k = kur.konfig
        hedef = (t + k.karistirici_denetim_araligi_s if bekle == "denetim"
                 else t + k.beacon_araligi_s)
        assert d.mesgul_bitisi_s(t) == pytest.approx(hedef)


def test_A3_HAREKETLI_karistiricili_TAM_KOSU_defter_KAPANIR():
    kur, kosu = _kos("statik-surekli", "enyakin", bitis=5.0,
                     tasiyici_dinleme="guc", tehdit_senaryosu="hava_eslik",
                     karistirici_baslangic_s=1.0)
    k, _ = _defter(kur, kosu)
    assert k["gecerli"], k
    assert kur.sayaclar.disa_ver()["mac_deneme"] > 0


# ==========================================================================
# A5 · YAYILIM GECİKMESİ — `v2/15` A5 (K-175)
# ==========================================================================
def _a5(**ek):
    kur = kurulum_yap(_konfig("statik-yok", 1000, 2.0, **ek))
    return kur, Kosu(kur, lambda i: DogrudanKomsu())


def test_A5_KAPALIYKEN_gecikme_TAM_SIFIR():
    kur, kosu = _a5()
    assert not kur.yayilim_gecikmeli and kur.maks_gecikme_s == 0.0
    assert kosu.dugumler[1].gecikme_s(0, 0.5) == 0.0


def test_A5_ACIKKEN_gecikme_d_bolu_c_ve_ONAY_PAYI():
    from sim2.kanal.yayilim import ISIK_HIZI
    kur, kosu = _a5(yayilim_gecikmesi=True)
    assert kosu.dugumler[1].gecikme_s(0, 0.5) == pytest.approx(
        kur.topoloji.mesafe(0, 1, 0.5) / ISIK_HIZI)
    assert kur.maks_gecikme_s == pytest.approx(
        kur.duyanlar_menzili_m / ISIK_HIZI)


def test_A5_tasiyici_dinleme_VARIS_PENCERESINDE():
    """Uzaktaki vericinin çerçevesi d/c sonra sezilir ve kaynakta bittikten
    d/c sonrasına kadar sezilmeye devam eder."""
    kur, kosu = _a5(yayilim_gecikmesi=True)
    n = kur.dugum_sayisi
    a, b = max(((i, j) for i in range(n) for j in range(n)
                if i != j and kosu.dugumler[j].duyar_mi(i, 0.5)),
               key=lambda c: kur.topoloji.mesafe(c[0], c[1], 0.5))
    d = kosu.dugumler[b]
    iletim = Iletim(a, kur.veri_cercevesi, 0.5,
                    kur.kanal.yayilim.verici_gucu_w)
    kur.kanal.ortam.ekle(iletim)
    g = d.gecikme_s(a, 0.5)
    assert g > 0.0
    assert not d.kanal_mesgul_mu(0.5 + 0.5 * g), "henüz ulaşmadı"
    assert d.kanal_mesgul_mu(0.5 + 1.5 * g)
    assert d.mesgul_bitisi_s(0.5 + 1.5 * g) == pytest.approx(
        iletim.bitis_s + g)
    assert d.kanal_mesgul_mu(iletim.bitis_s + 0.5 * g), "kaynakta bitti, burada sürüyor"


@pytest.mark.parametrize("ek", [{}, {"tasiyici_dinleme": "guc"}])
def test_A5_ACIK_TAM_KOSU_defter_KAPANIR(ek):
    kur, kosu = _kos("statik-surekli", "enyakin", bitis=5.0,
                     yayilim_gecikmesi=True, **ek)
    k, _ = _defter(kur, kosu)
    assert k["gecerli"], k
    assert kur.sayaclar.disa_ver()["teslim_paket"] > 0


# ==========================================================================
# A6 · KARIŞTIRICI GERÇEKÇİLİĞİ — `v2/15` A6 (K-176)
# ==========================================================================
def test_A6_al_hourani_BANLIYO_ve_P_LoS_ACIYLA_ARTAR():
    from sim2.kanal.yer_hava import (A2G_ORTAMLARI, gorus_hatti_olasiligi,
                                     s_egrisi)
    from sim2.yapilandirma.konfig import A2G_ORTAM_ADLARI
    assert tuple(A2G_ORTAMLARI) == A2G_ORTAM_ADLARI
    a, b = s_egrisi("banliyo")
    assert a == pytest.approx(4.88, abs=0.01)
    assert b == pytest.approx(0.429, abs=0.001)
    for ortam in A2G_ORTAMLARI:
        a, b = s_egrisi(ortam)
        p = [gorus_hatti_olasiligi(a, b, th) for th in (1, 10, 30, 60, 89)]
        assert p == sorted(p), f"{ortam}: P(LoS) yükseklik açısıyla artmalı"


def test_DD01_GORUS_HATTI_KALICI_ve_ORTALAMASI_MAKALENIN():
    """DD-01 (K-242): görüş hattı engel noktasının bina hücresine bağlı —
    hücreler üzerinden oran P(LoS, θ); küçük yer değiştirmede durum aynı;
    karıştırıcı taşınınca yeni binalar."""
    import math

    from sim2.dunya.geometri import Nokta3
    from sim2.kanal.yer_hava import (YerHavaKanali, bina_genisligi_m,
                                     gorus_hatti_olasiligi, s_egrisi)
    assert bina_genisligi_m("banliyo") == pytest.approx(11.547, abs=0.001)
    k = YerHavaKanali(1000, "banliyo")
    yer = Nokta3(16500.0, 16500.0, 3.0)
    a, b = s_egrisi("banliyo")
    # Engel noktası: ışın γ = 8 m'ye karıştırıcıdan (8 − 3)/tan θ uzakta iner.
    hava = Nokta3(16500.0 + 10_000.0, 16500.0, 3.0 + 10_000.0 * math.tan(
        math.radians(2.0)))
    x, _ = k.engel_noktasi(yer, hava)
    assert x - 16500.0 == pytest.approx(5.0 / math.tan(math.radians(2.0)))
    # Ortalama: karıştırıcının 3 000 ayrı konumunda (her biri yeni binalar)
    # aynı açıdaki oran P(LoS, θ). Tek konumda yönler az hücreye düşer.
    for teta in (1.0, 3.0, 10.0):
        yatay, n = 10_000.0, 3000
        z = 3.0 + yatay * math.tan(math.radians(teta))
        los = []
        for i in range(n):
            y0 = Nokta3(1000.0 + 97.0 * (i % 300), 1000.0 + 103.0 * (i // 300),
                        3.0)
            f = 2 * math.pi * ((i * 0.618) % 1.0)
            los.append(k.gorus_hatti_mi(y0, Nokta3(
                y0.x + yatay * math.cos(f), y0.y + yatay * math.sin(f), z)))
        p = gorus_hatti_olasiligi(a, b, teta)
        assert abs(sum(los) / n - p) < 4 * math.sqrt(p * (1 - p) / n)
    # Kalıcılık: 10 km'de 20 m yer değiştirme engel noktasını ~0,5 m kaydırır.
    ayni = 0
    for i in range(500):
        f = 2 * math.pi * i / 500
        h1 = Nokta3(yer.x + 10_000 * math.cos(f), yer.y + 10_000 * math.sin(f),
                    180.0)
        h2 = Nokta3(h1.x + 20.0, h1.y, 181.0)
        ayni += k.gorus_hatti_mi(yer, h1) == k.gorus_hatti_mi(yer, h2)
    assert ayni >= 480
    # Karıştırıcı 250 m taşınınca durumlar yeniden çekilir.
    tasindi = Nokta3(yer.x - 250.0, yer.y, 3.0)
    farkli = sum(
        k.gorus_hatti_mi(yer, h) != k.gorus_hatti_mi(tasindi, h)
        for h in (Nokta3(yer.x + 10_000 * math.cos(2 * math.pi * i / 2000),
                         yer.y + 10_000 * math.sin(2 * math.pi * i / 2000),
                         600.0) for i in range(2000)))
    assert farkli > 0


def test_A6_yer_karistiricisi_YERDE_ek_kayip_IKI_DEGERLI():
    def uyeler(k):
        return getattr(k, "uyeler", (k,))
    kur = kurulum_yap(_konfig("statik-surekli", 1000, 2.0,
                              tehdit_senaryosu="cephe_hatti",
                              karistirici_gercekci=True))
    k = kur.konfig
    assert all(u.konum.z == k.yer_karistirici_yukseklik_m
               for u in uyeler(kur.kanal.karistirici))
    u = uyeler(kur.kanal.karistirici)[0]
    ek = {u._a2g.ek_kayip_db(u.konum, kur.topoloji.konum(d, 1.0))
          for d in range(k.dugum_sayisi)}
    assert ek <= {0.1, 21.0} and ek
    kapali = kurulum_yap(_konfig("statik-surekli", 1000, 2.0,
                                 tehdit_senaryosu="cephe_hatti"))
    orta = 0.5 * (k.irtifa_min_m + k.irtifa_maks_m)
    assert all(u._a2g is None and u.konum.z == orta
               for u in uyeler(kapali.kanal.karistirici))


def test_A6_karistirici_bagi_SONUMLENIR_ortalama_KORUNUR():
    ortak = dict(karistirici_baslangic_s=0.5)
    acik = kurulum_yap(_konfig("bagimsiz-surekli", 1000, 2.0,
                               karistirici_gercekci=True, **ortak))
    kapali = kurulum_yap(_konfig("bagimsiz-surekli", 1000, 2.0, **ortak))
    oran = []
    for i in range(1300):
        t = 0.6 + 0.001 * i
        konum = kapali.topoloji.konum(0, t)
        oran.append(acik.kanal.karistirici.alinan_guc_w(0, konum, t)
                    / kapali.kanal.karistirici.alinan_guc_w(0, konum, t))
    ort = sum(oran) / len(oran)
    assert 0.85 < ort < 1.15, ort
    assert max(oran) / min(oran) > 2.0, "kazanç zamanla değişmeli"


def test_A6_reaktif_GUC_ESIGI_menzilsiz_duyma_YOK():
    sonuc = {}
    for esik in (200.0, -300.0):
        kur = kurulum_yap(_konfig("statik-reaktif", 1000, 2.0,
                                  karistirici_gercekci=True,
                                  reaktif_esik_dbm=esik,
                                  karistirici_baslangic_s=0.0))
        k = kur.kanal.karistirici
        acik = []
        for n in range(kur.dugum_sayisi):
            il = Iletim(n, kur.veri_cercevesi, 0.5 + 0.01 * n,
                        kur.kanal.yayilim.verici_gucu_w)
            kur.kanal.ortam.ekle(il)
            acik.append(k.acik_mi(il.baslangic_s + k._sezme + 1e-6))
        sonuc[esik] = acik
    assert not any(sonuc[200.0]), "eşiğin altındaki iletim sezilmemeli"
    assert sum(sonuc[-300.0]) >= 0.8 * len(sonuc[-300.0])


def test_A6_aldatici_SAHTE_CERCEVE_bos_aliciyi_KILITLER():
    ortak = dict(karistirici_baslangic_s=0.0, karistirici_guc_override_dbm=30.0)
    kur = kurulum_yap(_konfig("statik-aldatici", 1000, 2.0,
                              karistirici_gercekci=True, **ortak))
    d = Kosu(kur, lambda i: DogrudanKomsu()).dugumler[0]
    k = kur.kanal.karistirici
    t_ic = 5 * k._periyot + 0.5 * k._cerceve_s
    t_bosluk = 5 * k._periyot + k._cerceve_s + 0.5 * k._bosluk_s
    assert d.alici.sahte_kilitli_mi(t_ic)
    assert not d.alici.sahte_kilitli_mi(t_bosluk)
    d.alici._bos_bas_s = 5 * k._periyot + 0.1 * k._cerceve_s
    assert not d.alici.sahte_kilitli_mi(t_ic), "başı kaçırılan çerçeve kilitlemez"
    kur0 = kurulum_yap(_konfig("statik-aldatici", 1000, 2.0, **ortak))
    d0 = Kosu(kur0, lambda i: DogrudanKomsu()).dugumler[0]
    assert not d0.alici.sahte_kilitli_mi(t_ic), "kapalıyken kilit modeli yok"


@pytest.mark.parametrize("senaryo,ek", [
    ("statik-aldatici", {}),
    ("statik-aldatici", {"tasiyici_dinleme": "guc"}),
    ("statik-reaktif", {}),
    ("statik-surekli", {"tehdit_senaryosu": "cephe_hatti"}),
    ("bagimsiz-surekli", {}),
])
def test_A6_TAM_KOSU_defter_KAPANIR(senaryo, ek):
    kur, kosu = _kos(senaryo, "enyakin", bitis=4.0, karistirici_gercekci=True,
                     karistirici_baslangic_s=1.0, **ek)
    k, _ = _defter(kur, kosu)
    assert k["gecerli"], k


# ==========================================================================
# A4 · HIZ UYARLAMASI — `v2/15` A4 (K-177)
# ==========================================================================
_A4 = dict(islem_kazanci=True, bant_genisligi_hz=22e6, hiz_uyarlamasi=True)


def test_A4_ARF_ns3_ile_AYNI_DIZI():
    """G14 — ns-3 `ArfWifiManager`in birebir davranışı."""
    from sim2.mac.hiz import Arf
    a = Arf((1e6, 2e6, 5.5e6, 11e6), 10, 15)
    assert a.hiz(7) == 1e6, "en düşük hızdan başlar"
    for _ in range(10):
        a.basarili(7)
    assert a.hiz(7) == 2e6, "10 başarı → bir hız yukarı (kurtarma)"
    a.basarisiz(7)
    assert a.hiz(7) == 1e6, "kurtarmada ilk başarısızlık → aşağı"
    for _ in range(10):
        a.basarili(7)
    a.basarili(7)                      # kurtarma kapandı
    for _ in range(9):
        a.basarili(7)
    assert a.hiz(7) == 5.5e6
    a.basarili(7)                      # normal kip
    beklenen = (5.5e6, 2e6, 2e6, 1e6)  # 2. ve 4. başarısızlıkta aşağı
    for b in beklenen:
        a.basarisiz(7)
        assert a.hiz(7) == b
    s = Arf((1e6, 2e6), 10, 15)
    for i in range(15):                # B,A,B,…,B — 15. denemede sayaç dolar
        (s.basarili if i % 2 == 0 else s.basarisiz)(3)
    assert s.hiz(3) == 2e6, "sayaç eşiği (15) başarıda yukarı çıkarır"


def test_A4_TEK_BAG_SINR_ile_HIZ_SECIMI():
    """🔒 KAPI (`v2/15` A4): tek bağ, sabit SNR; ARF'ye her denemede
    Bernoulli(1 − PER) — ortalama hız SNR ile artar."""
    import random
    from sim2.cekirdek.rng import Akislar
    from sim2.dunya.topoloji import topoloji_kur
    from sim2.kanal.cerceve import cerceve_kur
    from sim2.kanal.kanal import Kanal
    from sim2.mac.hiz import Arf
    from sim2.yapilandirma.konfig import HIZLAR_BPS
    k = Konfig(kol="t", gurultu_figuru_db=7.0, **_A4)
    kanal = Kanal(k, topoloji_kur(k, Akislar(1)))
    cer = {h: cerceve_kur(k, "veri", hiz_bps=h) for h in HIZLAR_BPS}
    ortalama = []
    for snr_db in (-2.0, 2.0, 6.0, 10.0):
        s = 10 ** (snr_db / 10)
        a, r, toplam = Arf(HIZLAR_BPS, 10, 15), random.Random(1), 0.0
        for _ in range(3000):
            h = a.hiz(1)
            toplam += h
            (a.basarili if r.random() >= kanal.kahin_per(cer[h], s)
             else a.basarisiz)(1)
        ortalama.append(toplam / 3000)
    assert ortalama == sorted(ortalama), ortalama
    assert ortalama[0] < 1.5e6 and ortalama[-1] > 10e6, ortalama


def test_A4_TAM_KOSU_defter_KAPANIR_ve_HIZ_YUKSELIR():
    """Tam koşuda ARF beslenir ve hız başlangıçtan (1 Mb/s) yükselir; 11
    Mb/s'e ulaşmayı tek bağ kapısı sınar (kısa küçük dünyada komşu başına
    trafik seyrek)."""
    kur, kosu = _kos("statik-surekli", "enyakin", bitis=4.0, **_A4)
    k, _ = _defter(kur, kosu)
    assert k["gecerli"], k
    dagilim = {}
    for d in kosu.dugumler:
        for h, n in d.hiz_denetcisi.dagilim().items():
            dagilim[h] = dagilim.get(h, 0) + n
    assert sum(n for h, n in dagilim.items() if h > 1e6) > 0, dagilim
    kapali, kosu0 = _kos("statik-surekli", "enyakin", bitis=4.0)
    assert all(d.hiz_denetcisi is None for d in kosu0.dugumler)


# ==========================================================================
# A7 · REFERANS DÜNYA — `v2/15` A7 (K-178)
# ==========================================================================
def test_A7_referans_dunyada_KISA_KOSU_defter_KAPANIR():
    from sim2.kanal.dunya import referans_2026
    kfg = referans_2026(kol="t", senaryo="bagimsiz-surekli", tohum=1000,
                        isinma_s=1.0, olcum_bitis_s=4.0, kosu_bitis_s=5.0,
                        karistirici_baslangic_s=2.0)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: EnYakinKimlik())
    kosu.kostur()
    k, _ = _defter(kur, kosu)
    assert k["gecerli"], k
    assert kur.sayaclar.disa_ver()["teslim_paket"] > 0
    satir = sonuc_satiri(kur, kosu.dugumler, "p")
    assert satir["kapsam"]["dunya"] == "referans_2026"


# ==========================================================================
# B3 · GÖZLEM v2 — kendi GPS/INS'i ve telsiz sayaçları (`v2/15` B3, K-179)
# ==========================================================================
class _Dolulukcu(EnYakinKimlik):
    """Kanal doluluğunu ister; her kararın gözlemini kaydeder."""

    kanal_dolulugu_ister = True

    def __init__(self, kayit):
        self._kayit = kayit

    def sonraki_atlama(self, gozlem):
        self._kayit.append(gozlem)
        return super().sonraki_atlama(gozlem)


def test_B3_SAYACLAR_global_alimla_TUTARLI_ve_alanlar_DOLU():
    kayit: list = []
    kur = kurulum_yap(_konfig("statik-yok", 1000, 4.0))
    kosu = Kosu(kur, lambda i: _Dolulukcu(kayit))
    kosu.kostur()
    s = kur.sayaclar.disa_ver()
    assert sum(d._alinan_cerceve for d in kosu.dugumler) == s["alim_basarili"]
    assert sum(d._phy_hata for d in kosu.dugumler) == s["alim_red_per"]
    assert kayit, "sınav boş geçti"
    g = kayit[-1]
    assert g.kendi_konum is not None and g.kendi_hiz is not None
    assert 0.0 <= g.mesgul_sure_s <= kur.konfig.kosu_bitis_s
    assert g.alinan_cerceve > 0


def test_B3_DOLULUK_istemeyen_protokolde_OLCULMEDI():
    kur, kosu = _kos("statik-yok", "enyakin", bitis=2.0)
    g = kosu.dugumler[0].gozlem(1.0, None)
    assert g.mesgul_sure_s is None, "ölçülmedi ≠ 0"
    assert g.kendi_konum is not None


def test_B3_DOLULUK_surekli_karistiricida_TAM_MESGUL():
    """Güç kipinde 40 dBm'lik sürekli karıştırıcı 1 s'de açılır: her düğüm
    ED'den meşgul — 1–4 s arası süre TAMAMEN sayılır."""
    ortak = dict(karistirici_baslangic_s=1.0, karistirici_guc_override_dbm=40.0,
                 tasiyici_dinleme="guc")
    kur = kurulum_yap(_konfig("statik-surekli", 1000, 4.0, **ortak))
    kosu = Kosu(kur, lambda i: _Dolulukcu([]))
    kosu.kostur()
    for d in kosu.dugumler:
        d.mesgul_guncelle(4.0)
        assert 3.0 - 1e-6 <= d._mesgul_toplam_s <= 4.0, d._mesgul_toplam_s


def test_B3_GPS_hatasi_CEP_DIKEY_ve_DILIM_icinde_SABIT():
    import math
    kur = kurulum_yap(_konfig("statik-yok", 1000, 2.0))
    d = Kosu(kur, lambda i: DogrudanKomsu()).dugumler[0]
    yatay, dikey = [], []
    for s in range(400):
        t = s + 0.5
        (x, y, z), _ = d._gps(t)
        p = kur.topoloji.konum(0, t)
        yatay.append(math.hypot(x - p.x, y - p.y))
        dikey.append(z - p.z)
    yatay.sort()
    assert 1.2 < yatay[len(yatay) // 2] < 1.8, "CEP (ortanca yatay hata) 1,5 m"
    sd = (sum(v * v for v in dikey) / len(dikey)) ** 0.5
    assert 1.7 < sd < 2.3
    a = d._gps(10.1)[0][0] - kur.topoloji.konum(0, 10.1).x
    b = d._gps(10.9)[0][0] - kur.topoloji.konum(0, 10.9).x
    assert a == pytest.approx(b), "dilim (1 s) içinde hata sabit"


# ==========================================================================
# C · SENARYO EKSENLERİ — düğüm kaybı · enerji (`v2/15` C1 · C3, K-180)
# ==========================================================================
_KAYIP = dict(kayip_dugum_sayisi=4, kayip_bas_s=1.0, kayip_bitis_s=3.0)


def test_C1_OLU_dugum_SUSAR_gecit_OLMEZ_defter_KAPANIR():
    from sim2.kosum.kayip import olum_anlari
    kfg = _konfig("bagimsiz-surekli", 1000, 5.0, trafik_deseni="yere_toplama",
                  karistirici_baslangic_s=1.0, **_KAYIP)
    anlar = olum_anlari(kfg)
    assert sum(a is not None for a in anlar) == 4
    assert anlar[kfg.gecit] is None, "geçit düşmez"
    assert anlar == olum_anlari(kfg), "belirlenimci"
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: EnYakinKimlik())
    gonderilen_olumde: dict = {}
    from sim2.kosum import kayip

    asil = kayip.dugum_oldur

    def izle(kosu_, n):
        asil(kosu_, n)
        gonderilen_olumde[n] = kosu_.dugumler[n]._gonderilen_bayt
    kayip.dugum_oldur = izle              # `kostur` ölümleri zamanlarken okur
    try:
        kosu.kostur()
    finally:
        kayip.dugum_oldur = asil
    assert set(gonderilen_olumde) == {n for n, a in enumerate(anlar)
                                      if a is not None}
    for n, bayt in gonderilen_olumde.items():
        d = kosu.dugumler[n]
        assert d.olu and d._gonderilen_bayt == bayt, "ölümden sonra gönderdi"
    k, _ = _defter(kur, kosu)
    assert k["gecerli"], k


def test_C1_KAYIP_YOKKEN_kimse_OLMEZ():
    kur, kosu = _kos("statik-yok", "enyakin", bitis=2.0)
    assert all(a is None for a in kur.olum_anlari)
    assert not any(d.olu for d in kosu.dugumler)


def test_C3_ENERJI_sure_DEGISMEZI_ve_FORMUL():
    kfg = _konfig("bagimsiz-surekli", 1000, 5.0, karistirici_baslangic_s=1.0,
                  **_KAYIP)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: EnYakinKimlik())
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "p")
    assert satir["korunum"]["enerji_sure_tamam"]
    toplam = 0.0
    for d in kosu.dugumler:
        e, tx, rx, dinle = d.enerji(kfg.kosu_bitis_s)
        sure = kfg.kosu_bitis_s if d.olum_s is None else d.olum_s
        assert tx >= 0 and rx >= 0 and dinle >= -1e-9
        assert tx + rx + dinle == pytest.approx(sure)
        assert e == pytest.approx(kfg.enerji_gonderim_w * tx
                                  + kfg.enerji_alim_w * (sure - tx))
        toplam += e
    m = satir["metrikler"]
    assert m["enerji_toplam_j"] == pytest.approx(toplam)
    assert m["enerji_dugum_p50_j"] <= m["enerji_dugum_p95_j"] <= \
        m["enerji_dugum_maks_j"]


def test_C1_YAYIN_ORTASINDA_olum_cerceve_VARINCA_gerceklesir(monkeypatch):
    """🔴 K-180: ölüm kendi veri çerçevesinin ortasına düşerse ertelenir —
    ertelenmeseydi alıcı ölü göndericiden "devralır", değişmez patlardı.
    Gecikme kapalı ve açık (A5: varış çerçeve sonundan d/c sonra)."""
    from sim2.kosum import kayip
    from sim2.kosum.dugum import Dugum
    for ek in ({}, {"yayilim_gecikmesi": True}):
        kur = kurulum_yap(_konfig("statik-yok", 1000, 3.0, **ek))
        kosu = Kosu(kur, lambda i: EnYakinKimlik())
        asil = Dugum.gonderim_ekle
        kurban: dict = {}

        def izle(self, t_s, sure_s, kosu=kosu, kurban=kurban, asil=asil):
            asil(self, t_s, sure_s)
            if not kurban and t_s > 1.0 and self.ucustaki is not None \
                    and self.dcf.durum != "bos":
                kurban.update(n=self.kimlik, bitis=t_s + sure_s)
                kosu.olaylar.ekle(t_s + sure_s / 2, kayip.dugum_oldur, kosu,
                                  self.kimlik)
        monkeypatch.setattr(Dugum, "gonderim_ekle", izle)
        kosu.kostur()
        monkeypatch.undo()
        d = kosu.dugumler[kurban["n"]]
        assert d.olu
        assert d.olum_s >= kurban["bitis"] + kur.maks_gecikme_s - 1e-12
        assert d.olum_s <= kurban["bitis"] + kur.maks_gecikme_s + 1e-3
        k, _ = _defter(kur, kosu)
        assert k["gecerli"], k


def test_KRE_kayipli_kosuda_defterler_MUTABIK():
    """KR-E: korunumun ürettiği = PDR kohortu + ölü hedefe doğan; kayıpsız
    koşuda görev oranı PDR'ye birebir eşit."""
    kfg = _konfig("bagimsiz-surekli", 1000, 5.0, karistirici_baslangic_s=1.0,
                  **_KAYIP)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: EnYakinKimlik())
    kosu.kostur()
    pd = kur.paket_defteri
    ham = pd.ham_sozluk()
    assert kur.korunum.uretilen == pd.uretilen + len(ham["olu_hedefe_dogum_s"])
    m = sonuc_satiri(kur, kosu.dugumler, "p")["metrikler"]
    assert m["pdr"] == pytest.approx(pd.teslim / pd.uretilen)
    assert m["gorev_teslim_orani"] <= m["pdr"]
    kur0, kosu0 = _kos("statik-yok", "enyakin", bitis=2.0)
    m0 = sonuc_satiri(kur0, kosu0.dugumler, "p")["metrikler"]
    assert m0["gorev_teslim_orani"] == m0["pdr"]


# ==========================================================================
# FAZ 4.0 · KÂHİN REFERANS DÜNYAYI GÖRÜR · DÜNYA SEÇİMİ (K-183)
# ==========================================================================
_GUCLU = dict(karistirici_baslangic_s=0.5, karistirici_guc_override_dbm=40.0)


def test_K183_kahin_GUC_KIPINDE_susan_vericinin_CIKAN_bagi_YOK():
    """ED susturması: karıştırıcı enerjisi ED eşiğini aşan verici kanalı
    alamaz; kâhin grafiğinde çıkan bağı yoktur. Geometrik kipte susturma
    yoktur (eski dünya birebir)."""
    from kalibrasyon.kahin import KanalGrafigi
    t = 1.0
    kur = kurulum_yap(_konfig("statik-surekli", 1000, 3.0,
                              tasiyici_dinleme="guc", **_GUCLU))
    g = KanalGrafigi(kur)
    g._tazele(t)
    susan = [i for i in range(kur.dugum_sayisi) if g._susturulmus_mu(i, t)]
    assert susan, "10 W'lık merkez karıştırıcı en az bir düğümü susturmalı"
    for i in susan:
        assert g._komsu[i] == [] and not g._etx[i], i
    kur0 = kurulum_yap(_konfig("statik-surekli", 1000, 3.0, **_GUCLU))
    g0 = KanalGrafigi(kur0)
    g0._tazele(t)
    assert not any(g0._susturulmus_mu(i, t)
                   for i in range(kur0.dugum_sayisi))


def test_K195_kahin_KARISTIRICI_CIZELGESINDE_grafigi_YENILER():
    """🔴 K-195: kâhin grafiği yalnız hareket dilimiyle yenileniyordu; açık ·
    sessiz çizelgeli karıştırıcıda (`derin_sizma`, 15 s · 15 s) aynı dilim
    içindeki kapanma görünmüyordu. Artık üyelerin `devrede_mi` durumu
    değişince grafik yeniden kurulur; karıştırıcısız kolda imza boş."""
    from kalibrasyon.kahin import KanalGrafigi
    kur = kurulum_yap(_konfig("statik-surekli", 1000, 40.0,
                              tehdit_senaryosu="derin_sizma",
                              tasiyici_dinleme="guc", **_GUCLU))
    g = KanalGrafigi(kur)
    t_acik, t_sessiz = 15.4, 15.6          # açılma 0,5 s → kapanma 15,5 s
    assert int(t_acik / g.dilim_s) == int(t_sessiz / g.dilim_s), \
        "ön koşul: iki an aynı hareket diliminde"
    g._tazele(t_acik)
    once = [dict(e) for e in g._etx]
    assert g._imza == (True,)
    g._tazele(t_sessiz)
    assert g._imza == (False,), "kapanma grafiği yenilemedi"
    assert [dict(e) for e in g._etx] != once, \
        "karıştırıcı kapandı ama kâhin grafiği değişmedi"
    g0 = KanalGrafigi(kurulum_yap(_konfig("statik-yok", 1000, 3.0)))
    g0._tazele(1.0)
    assert g0._devrede_imzasi(1.0) == ()


def test_K183_kahin_HIZ_UYARLAMASINDA_bag_ARF_TABANINDA():
    from kalibrasyon.kahin import KanalGrafigi
    from sim2.kanal.cerceve import cerceve_kur
    kur = kurulum_yap(_konfig("statik-yok", 1000, 3.0, islem_kazanci=True,
                              bant_genisligi_hz=22e6, hiz_uyarlamasi=True))
    assert KanalGrafigi(kur)._veri.hiz_bps == 1e6
    kur0 = kurulum_yap(_konfig("statik-yok", 1000, 3.0))
    assert KanalGrafigi(kur0)._veri.hiz_bps == \
        cerceve_kur(kur0.konfig, "veri").hiz_bps


def test_K183_dunya_secimi_ARGUMANI_cikarir_ORTAMA_yazar(monkeypatch):
    from kalibrasyon import dunya_secimi as DS
    # 🔒 Önce `setenv`: `delenv` olmayan değişkende geri alma kaydı TUTMAZ;
    # `secimi_oku`nun doğrudan yazdığı değer sonraki testlere sızıyordu
    # (1 Ekim 2026, dosya sırası değişince U1 testleri kırıldı).
    monkeypatch.setenv(DS.ORTAM, "olcek_1_50")
    monkeypatch.delenv(DS.ORTAM)
    assert DS.secili() == "olcek_1_50"
    argv = ["arac", "--dunya", "referans_2026", "tarama"]
    assert DS.secimi_oku(argv) == "referans_2026"
    assert argv == ["arac", "tarama"]
    assert DS.konfig(kol="t").dunya == "referans_2026"
    assert DS.etiket("x") == "x_referans_2026"
    monkeypatch.setenv(DS.ORTAM, "olcek_1_50")
    assert DS.konfig(kol="t").dunya == "olcek_1_50"
    with pytest.raises(DegismezHatasi):
        DS.secimi_oku(["arac", "--dunya", "hayal"])


def test_K183_ELLE_KURULUM_kuran_araclar_KURULABILIR_ve_KOSAR():
    """🔴 K-183: Li zinciri ve iki çift `Kurulum`u elle kuruyor ve A5/C1
    alanları eklenince KURULAMAZ hâle gelmişti — kimse fark etmedi, çünkü
    son koşumları eskiydi. Bu duman testi onları her takımda kurdurur ve
    kısa koşturur; `Kurulum`a yeni zorunlu alan eklenirse burada kırılır."""
    from kalibrasyon.iki_cift import kos as iki_cift_kos
    from kalibrasyon.li_replikasyonu import _kos as li_kos
    li = li_kos(3, 250.0, 1000, 50.0, bitis_s=1.0)
    assert li["uretilen"] > 0 and li["pdr"] is not None
    assert iki_cift_kos(1, 1000, 1000.0, yuk_hz=50.0, bitis_s=1.0) >= 0.0


def test_K183_duyma_turetimi_KURULUMLA_AYNI():
    from sim2.kanal.cerceve import cerceve_kur
    from sim2.kosum.kurulum import duyma_turetimi
    for ek in ({}, {"islem_kazanci": True, "bant_genisligi_hz": 22e6,
                    "yayilim_gecikmesi": True}):
        kur = kurulum_yap(_konfig("statik-yok", 1000, 2.0, **ek))
        m, g = duyma_turetimi(kur.konfig, cerceve_kur(kur.konfig, "beacon"))
        assert (m, g) == (kur.duyanlar_menzili_m, kur.maks_gecikme_s)


def test_K185_dunya_secimi_ALAN_gecersiz_kilma(monkeypatch):
    """Faz 4.1 alan × güç taraması: `--alan` referans alanını ve görev
    yarıçapını (alan oranıyla) değiştirir; eski dünyada etkisizdir."""
    from kalibrasyon import dunya_secimi as DS
    # 🔒 Önce `setenv` (geri alma kaydı için; yukarıdaki testin notu).
    for ad in (DS.ORTAM, DS.ALAN_ORTAM):
        monkeypatch.setenv(ad, "x")
        monkeypatch.delenv(ad)
    argv = ["arac", "--dunya", "referans_2026", "--alan", "15000", "x"]
    DS.secimi_oku(argv)
    assert argv == ["arac", "x"]
    k = DS.konfig(kol="t")
    assert (k.alan_en_m, k.alan_boy_m) == (15000.0, 15000.0)
    assert k.gorev_grup_yaricapi_m == pytest.approx(15000.0 * 650.0 / 1800.0)
    assert DS.etiket("a") == "a_referans_2026_alan15000"
    monkeypatch.setenv(DS.ORTAM, "olcek_1_50")
    assert DS.konfig(kol="t").alan_en_m == Konfig(kol="t").alan_en_m


def test_K186_kahin_ozeti_GUCLU_bilesenler_yonlu_grafikte():
    """Yönlü grafikte (güç kipi) güçlü bileşenler: boyutlar toplamı N,
    susan düğüm tek başına; simetrik grafikte eski bileşenlerle aynı."""
    from kalibrasyon.kahin import KanalGrafigi
    kur = kurulum_yap(_konfig("statik-surekli", 1000, 3.0,
                              tasiyici_dinleme="guc", **_GUCLU))
    g = KanalGrafigi(kur)
    o = g.ozet(1.0)
    assert 0.0 < o["gb_ikinci"] <= o["gb_en_buyuk"] <= 1.0
    kur0 = kurulum_yap(_konfig("statik-yok", 1000, 3.0))
    o0 = KanalGrafigi(kur0).ozet(1.0)
    assert o0["gb_en_buyuk"] == o0["en_buyuk_bilesen"]


def test_K187_kalibrasyon_Konfigi_YALNIZ_dunya_seciminden_kurar():
    """🔴 K-187: `theta_kollari` `--dunya` alıyordu ama ölçüm gövdesi
    (`bag_kumesi._is_theta_hiz`) Konfig'i doğrudan kuruyordu — referans
    dünya istenince SESSİZCE eski dünyayı ölçecekti. Bütün araçlar
    `dunya_secimi.konfig` üzerinden kurar; muaflar gerekçeli."""
    muaf = {"dunya_secimi.py",        # seçimin kendisi
            "adim3_oncesi.py",        # tarihsel, dondurulmuş
            "mimari_denetimi.py",     # varsayılanları inceler
            "regresyon_satirlari.py"}  # dünya vaka önekinden, bilerek
    kok = Path(__file__).resolve().parent.parent / "kalibrasyon"
    ihlal = []
    for dosya in sorted(kok.glob("*.py")):
        if dosya.name in muaf:
            continue
        agac = ast.parse(dosya.read_text(encoding="utf-8"))
        for d in ast.walk(agac):
            if (isinstance(d, ast.Call) and isinstance(d.func, ast.Name)
                    and d.func.id == "Konfig"):
                ihlal.append(f"{dosya.name}:{d.lineno}")
    assert not ihlal, ihlal
