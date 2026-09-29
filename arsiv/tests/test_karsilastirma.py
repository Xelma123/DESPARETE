"""
🔴 B-19 / B-20 — ortak alt küme şeması ve airtime muhasebesi.

B-19 denetimin *"Aile 1 için kritik"* dediği bulguydu: sonuç şeması paket
bazlı teslim bilgisi taşımadığı için `03` B3'ün istediği "ortak alt küme +
kesişim oranı" karşılaştırması YAPILAMIYORDU.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import AKTARICILAR, en_kisa_yol  # noqa: E402
from sim.config import Konfig  # noqa: E402
from sim.karsilastirma import (KarsilastirmaHatasi,  # noqa: E402
                               ortak_alt_kume, yuzdelik)
from sim.kosucu import Kosu  # noqa: E402


def _kos(senaryo="S2", kol="t", aktarici=en_kisa_yol, tohum=1, **kw):
    return Kosu(Konfig(kol=kol, senaryo=senaryo, trafik="orta", tohum=tohum,
                       **kw), aktarici).kostur()


# ==========================================================================
# B-19
# ==========================================================================

def test_b19_paket_evreni_protokolden_bagimsiz():
    """🔴 ORTAK ALT KÜMENİN DAYANDIĞI VARSAYIM — önce bu doğrulanır (Y8).

    `kimlik` ancak paket evreni protokolden bağımsızsa ortak anahtar
    olabilir. Trafik akışları (`trafik_ciftleri`, `trafik_zamani`) protokolün
    çektiği rastgele sayı adedinden etkilenmez — ama bu İDDİA, ölçülmeden
    şemanın temeli yapılamaz.
    """
    evrenler = {}
    for ad in ("en_kisa_yol", "hedefe_en_yakin", "gurultuden_kacan"):
        k = Kosu(Konfig(kol=ad, senaryo="S2", trafik="orta", tohum=1),
                 AKTARICILAR[ad])
        k.kostur()
        evrenler[ad] = [(p.kimlik, p.dogum_s, p.kaynak, p.hedef)
                        for p in k.trafik.uretilen_paketler]

    ilk = evrenler["en_kisa_yol"]
    assert len(ilk) > 1000, f"evren fazla küçük ({len(ilk)}) — test zayıf (Y7)"
    for ad, e in evrenler.items():
        assert e == ilk, f"{ad} farklı bir paket evreni gördü — kimlik ortak anahtar OLAMAZ"


def test_b19_ortak_alt_kume_secilim_yanliligini_ortaya_cikariyor():
    """🔴 B-19'un ta kendisi: ham okuma ile ortak alt küme AYRIŞIYOR.

    ⚠️ **BU TEST 1 EYLÜL SONRASI DÜZELTİLDİ (F-7, B0.5 denetimi).**
    Eski hâli `ham_fark_s > gecikme_farki_s > 0` diye BİR YASA iddia
    ediyordu ve **yalnızca tohum 1'de** doğruydu. Ölçüldü (30 tohum,
    `en_kisa_yol`, S0→S2, eşleştirilmiş):

        "ham > ortak > 0"  ....................  **5/30** tohumda tutuyor
        ham fark > 0       ....................  12/30  (işaret KARARSIZ)
        ortak fark > 0     ....................  **25/30**, p = 0,0003
        |ham| > |ortak|    ....................  18/30

    Yani ham okuma *"abartmıyor"* — **işareti bile tutmuyor**. Bir
    tohumdan çıkan ilişkiyi değişmez sanmak `03` kural 2'nin
    (*"tek/az tohumlu sonuç raporlama"*) test tarafındaki hâliydi.

    🔒 Bu test artık YALNIZCA yapısal olanı sınar; yönü ve büyüklüğü
    30 tohumla ölçen üretici: `python dogrulama/gecerlilik.py`
    """
    a = _kos("S0", kol="a")
    b = _kos("S2", kol="b")
    o = ortak_alt_kume(a, b)

    # Y8 — kurulum gerçekten asimetrik mi?
    assert o.teslim_a > 2 * o.teslim_b, (o.teslim_a, o.teslim_b)
    assert o.ortak_paket > 100, o.ortak_paket

    # 🔒 YAPISAL: ortak alt küme her iki kolun teslim kümesinden KÜÇÜKTÜR,
    # dolayısıyla ham ve ortak okumalar FARKLI paket kümeleri üzerindedir.
    # Yanlılığın VARLIĞI budur; yönü tohuma bağlıdır ve yukarıda ölçüldü.
    assert o.ortak_paket <= o.teslim_b < o.teslim_a
    assert o.ham_fark_s is not None and o.gecikme_farki_s is not None
    assert o.ham_fark_s != o.gecikme_farki_s, (
        "ham ve ortak okuma birebir aynı çıktı — ortak alt küme "
        "hesaplanmıyor olabilir")

    # Kesişim oranı DAİMA raporlanabilir olmalı
    assert 0.0 < o.kesisim_orani_birlesim <= 1.0
    assert "kesişim" in o.ozet()


def test_b19_farkli_paket_evreni_reddediliyor():
    """Y7 — araç ne karşılaştırdığını kendisi doğrular."""
    a = _kos(tohum=1)
    b = _kos(tohum=7)                       # farklı tohum → farklı evren
    with pytest.raises(KarsilastirmaHatasi):
        ortak_alt_kume(a, b)


def test_b19_sema_oncesi_satir_reddediliyor():
    """B-19 öncesi üretilmiş bir satır sessizce karşılaştırılamaz.

    `03` B5 "şemanın kaybolması": bayrağı olmayan satır yeniden
    üretilemez — ve karşılaştırılamaz.
    """
    a = _kos()
    eski = {k: v for k, v in a.items() if k != "teslim_kimlikleri"}
    with pytest.raises(KarsilastirmaHatasi):
        ortak_alt_kume(eski, a)


def test_b19_kol_kendisiyle_karsilastirilinca_fark_sifir():
    """Kontrol kolu: aynı sonuç kendisiyle karşılaştırılınca fark 0, kesişim 1."""
    a = _kos()
    o = ortak_alt_kume(a, a)
    assert o.gecikme_farki_s == pytest.approx(0.0, abs=1e-12)
    assert o.kesisim_orani_birlesim == 1.0


# ==========================================================================
# B-20
# ==========================================================================

def test_b20_airtime_cerceve_surelerinin_toplamina_esit():
    """DEĞİŞMEZ: airtime = çerçeve sayısı × çerçeve süresi.

    Sayaç bağımsız olarak yeniden hesaplanabiliyorsa, "airtime" gerçekten
    kanal zamanıdır; keyfi bir sayı değil.
    """
    kon = Konfig(kol="t", senaryo="S2", trafik="orta", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    s = k.kostur()

    beklenen_veri = k.mac.gonderilen_veri * kon.cerceve_suresi_s(kon.paket_bayt)
    beklenen_kontrol = (k.mac.gonderilen_onay * kon.onay_suresi_s
                        + k.mac.gonderilen_yayin
                        * kon.cerceve_suresi_s(kon.beacon_bayt))

    assert s["veri_airtime_s"] == pytest.approx(beklenen_veri, rel=1e-9, abs=0.0)
    assert s["kontrol_airtime_s"] == pytest.approx(beklenen_kontrol,
                                                   rel=1e-9, abs=0.0)


def test_b20_kontrol_payi_airtimede_bayttan_yuksek():
    """🔴 B-20: önbelge her çerçeveye sabit 192 µs ekler.

    Küçük çerçeveler (onay 14 B, beacon 32 B) bayt cinsinden ucuz görünür
    ama kanal zamanında pahalıdır. Ölçülen: bayt %2,84 · airtime %5,12.
    Bu testin kırılması, kontrol yükü metriğinin tek birime düştüğünü
    gösterir — K-009'un "eşit kontrol bütçesi" şartı o zaman doğrulanamaz.
    """
    s = _kos()
    bayt_payi = s["kontrol_bayt"] / (s["kontrol_bayt"] + s["veri_bayt"])
    airtime_payi = (s["kontrol_airtime_s"]
                    / (s["kontrol_airtime_s"] + s["veri_airtime_s"]))

    assert 0.0 < bayt_payi < airtime_payi < 1.0, (bayt_payi, airtime_payi)
    assert airtime_payi / bayt_payi > 1.5, (
        f"airtime/bayt oranı {airtime_payi/bayt_payi:.2f} — önbelge maliyeti "
        f"kaybolmuş olabilir"
    )


# ==========================================================================
# 🔴 B-26 — KORUMA GERÇEKTEN NE DOĞRULUYOR?
#
# İkinci bağımsız denetim, B-19'un korumasını kırdı: `dugum_sayisi` 40→41
# yapıldığında iki kolun HİÇBİR paketi ortak değilken koruma karşılaştırmayı
# kabul etti ve 31,6 ms'lik bir "gecikme farkı" üretti.
#
# Sebep iki katmanlıydı:
#   1. Koruma yalnızca `pencerede_uretilen` ve `pencere_kimlik_araligi`ye
#      bakıyordu — ikisi de YALNIZCA `trafik_zamani` akışından belirlenir,
#      yani tohum dışında hiçbir konfigürasyon farkı onları değiştiremez
#   2. Tek pozitif test de TOHUM farkını kullanıyordu — yani koruma
#      **yalnızca yakalayabildiği tek durumla** sınanmıştı
#
# Aşağıdaki testler korumayı denetçinin kırdığı vakalarla VE meşru tedavi
# farklarıyla iki yönlü sınar.
# ==========================================================================

KIRILMASI_GEREKEN = [
    ("dugum_sayisi", dict(dugum_sayisi=41)),        # denetçinin kırdığı vaka
    ("iletim_menzili_m", dict(iletim_menzili_m=300.0)),
    ("alan_m", dict(alan_m=1010.0)),
    ("tohum", dict(tohum=7)),
    ("kuyruk_kapasitesi", dict(kuyruk_kapasitesi=10)),
    ("ttl_baslangic", dict(ttl_baslangic=8)),
    ("paket_bayt", dict(paket_bayt=512)),
]

# Yalnızca TEDAVİ farkı — karşılaştırma MEŞRU
KABUL_EDILMESI_GEREKEN = [
    ("senaryo S0", dict(senaryo="S0"), en_kisa_yol),
    ("senaryo S4 (H1.3 çifti)", dict(senaryo="S4"), en_kisa_yol),
    ("güç override (H1.2 taraması)", dict(karistirici_guc_override_dbm=4.0),
     en_kisa_yol),
    ("farklı protokol", {}, AKTARICILAR["gurultuden_kacan"]),
]


@pytest.mark.parametrize("ad,kw", KIRILMASI_GEREKEN, ids=[a for a, _ in KIRILMASI_GEREKEN])
def test_b26_kurulum_farki_reddediliyor(ad, kw):
    """🔴 Kurulum farkı olan iki koşu karşılaştırılamaz.

    `dugum_sayisi` ve `tohum` paket evrenini değiştirir;
    `iletim_menzili_m`/`alan_m`/`kuyruk`/`ttl`/`paket_bayt` evreni AYNI
    bırakıp **ağı** değiştirir. İkinci sınıf, ilk korumanın tamamen
    kaçırdığı sınıftı — `kurulum_hash` onu yakalar.
    """
    a = _kos()
    b = _kos(**kw)
    with pytest.raises(KarsilastirmaHatasi):
        ortak_alt_kume(a, b)


@pytest.mark.parametrize("ad,kw,rl", KABUL_EDILMESI_GEREKEN,
                         ids=[a for a, _, _ in KABUL_EDILMESI_GEREKEN])
def test_b26_tedavi_farki_kabul_ediliyor(ad, kw, rl):
    """Koruma fazla sıkı da olmamalı — ön-kayıtlı karşılaştırmalar geçmeli.

    Y6/`03` B1: bir kontrol, bozması gereken kanalı korurken **bozmaması
    gereken kanalı da bozmamalıdır.** Bu testler olmasaydı, korumayı
    "her şeyi reddet" yaparak da geçirebilirdim.
    """
    a = _kos()
    o = ortak_alt_kume(a, _kos(aktarici=rl, **kw))
    assert o.ortak_paket > 100, o.ozet()


def test_b26_parmak_izi_protokolden_bagimsiz_kurulumdan_bagimli():
    """İki hash'in ayrımı: evren protokolden bağımsız, kurulum tedaviden."""
    temel = _kos()
    # Üç farklı aktarıcı → aynı evren VE aynı kurulum
    for ad in ("hedefe_en_yakin", "gurultuden_kacan"):
        s = _kos(aktarici=AKTARICILAR[ad])
        assert s["pencere_evren_hash"] == temel["pencere_evren_hash"], ad
        assert s["kurulum_hash"] == temel["kurulum_hash"], ad

    # Senaryo TEDAVİDİR → kurulum hash'i değişmemeli
    assert _kos(senaryo="S4")["kurulum_hash"] == temel["kurulum_hash"]

    # Ağ değişimi kurulumdur → hash değişmeli
    assert _kos(iletim_menzili_m=300.0)["kurulum_hash"] != temel["kurulum_hash"]


def test_b26_hash_pythonhashseed_den_bagimsiz():
    """Ç2 korunuyor: parmak izleri ayrı süreçlerde de aynı.

    `hash()` kullanılsaydı PYTHONHASHSEED ile değişir ve belirlenimcilik
    kapısını sessizce kırardı (`rng.py`nin aynı gerekçesi).
    """
    import os
    import subprocess

    betik = (
        "import sys; sys.path.insert(0, r'%s');"
        "from sim.config import Konfig;"
        "from sim.kosucu import Kosu;"
        "from dogrulama.aktaricilar import en_kisa_yol;"
        "s = Kosu(Konfig(kol='t', senaryo='S2', trafik='orta', tohum=1),"
        "         en_kisa_yol).kostur();"
        "print(s['pencere_evren_hash'], s['kurulum_hash'])"
        % str(Path(__file__).resolve().parent.parent)
    )
    ciktilar = set()
    for tohum in ("0", "1", "42"):
        p = subprocess.run([sys.executable, "-c", betik], capture_output=True,
                           text=True, env={**os.environ,
                                           "PYTHONHASHSEED": tohum,
                                           "PYTHONIOENCODING": "utf-8"})
        assert p.returncode == 0, p.stderr[-400:]
        ciktilar.add(p.stdout.strip())
    assert len(ciktilar) == 1, ciktilar


# ==========================================================================
# 🔴 B-46 — KOD SÜRÜMÜ EKSENİ
#
# B-26'nın dersi *"bir koruma yalnızca yakalayabildiği durumla sınanamaz"*
# idi ve düzeltmesi KONFİGÜRASYON eksenine yazıldı. Üçüncü bağımsız denetim
# KOD eksenini kırdı: birebir aynı konfigürasyon ve tohum, tek fark
# `mac._onay_zaman_asimi`'ndeki geri çekilme — iki parmak izi de AYNI çıktı
# ve koruma 7,76 ms'lik bir "gecikme farkı" üretti.
# ==========================================================================

def test_b46_sonuc_satiri_KOD_SURUMUNU_tasiyor():
    """`05` §E sonuç sözleşmesi *"Kod sürümü"*nü ZORUNLU alan sayıyor."""
    from sim.results import kaynak_hash

    s = _kos()
    assert "kaynak_hash" in s, "sonuç satırı kod sürümünü taşımıyor"
    assert s["kaynak_hash"] == kaynak_hash(), (
        "sonuçtaki kod sürümü, `results.kaynak_hash()` ile aynı değil")


def test_b46_FARKLI_KODDAN_gelen_iki_satir_reddediliyor():
    """🔴 Y11 — korumanın KAPSAMI DIŞINDA kalan eksen.

    İki satır: aynı paket evreni, aynı kurulum, aynı tohum — **farklı kod**.
    Konfigürasyon eksenindeki iki parmak izi bunu göremez; üçüncü kontrol
    görmek zorunda.
    """
    a = _kos()
    b = dict(a)
    b["kaynak_hash"] = "0" * 32          # başka bir simülatör sürümü

    # Kurulum varsayımı: diğer iki parmak izi AYNI kalıyor
    assert a["pencere_evren_hash"] == b["pencere_evren_hash"]
    assert a["kurulum_hash"] == b["kurulum_hash"]

    with pytest.raises(KarsilastirmaHatasi, match="KOD SÜRÜM"):
        ortak_alt_kume(a, b)


def test_b46_AYNI_koddan_gelen_iki_satir_kabul_ediliyor():
    """Kontrol kolu: koruma her şeyi reddetmiyor olmalı."""
    a = _kos()
    ok = ortak_alt_kume(a, dict(a))
    assert ok.ortak_paket > 0


# ==========================================================================
# 🔴 B-67 (K-056) — DÖRDÜNCÜ EKSEN: SATIRIN KENDİ İÇİ
#
# Üç eksen (paket evreni · kurulum · kod sürümü) KOLLAR ARASI tutarlılığı
# denetliyordu. Dördüncü denetim dört bozuk satır üretti ve **dördü de kabul
# edildi** — `dict(zip(...))` sessizce kırpar ve tekrarlı kimliği ezer.
# 14 testin 14'ü de üç eksendeydi; satır içi yapı sınayan tek test yoktu.
# ==========================================================================

# 🔴 Her vaka HANGİ değişmezin ateşlediğini de sınar.
# ⚠️ İlk yazımı yalnızca `pytest.raises(KarsilastirmaHatasi)` diyordu ve NaN
# vakası **yanlış değişmez** tarafından yakalanıyordu: `nan >= 0.0` zaten
# `False` olduğu için negatiflik kontrolü ateşliyordu. Ölçüldü — finite
# kontrolünü kaldıran mutasyon testten SAĞ ÇIKTI (M-A1). Y11: bir koruma,
# başka bir korumanın gölgesinde sınanamaz. `+inf` vakası bu yüzden eklendi:
# negatiflik kontrolünden GEÇER, yalnızca finite kontrolü yakalar.
@pytest.mark.parametrize("ad, bozan, beklenen", [
    # 🔴 BEKLENEN MESAJ DARALTILDI (B0.5 · M13). Eskiden "gecikme" idi ve
    # uzunluk kontrolü kaldırıldığında E5 (`ortalama_gecikme_s` tutarlılığı)
    # ateşleyip AYNI dizgiyi içeriyordu — mutant SAĞ ÇIKIYORDU. Y11: bir
    # koruma, başka bir korumanın gölgesinde sınanamaz.
    ("gecikme listesi yarıya kırpık",
     lambda s: s.update(teslim_gecikmeleri_s=s["teslim_gecikmeleri_s"][:len(s["teslim_gecikmeleri_s"]) // 2]),
     "kimlik ama"),
    ("tüm kimlikler aynı",
     lambda s: s.update(teslim_kimlikleri=[s["teslim_kimlikleri"][0]] * len(s["teslim_kimlikleri"])),
     "TEKRARLI"),
    ("tüm gecikmeler NaN",
     lambda s: s.update(teslim_gecikmeleri_s=[float("nan")] * len(s["teslim_gecikmeleri_s"])),
     "NaN"),
    ("tüm gecikmeler +sonsuz",
     lambda s: s.update(teslim_gecikmeleri_s=[float("inf")] * len(s["teslim_gecikmeleri_s"])),
     "NaN"),
    ("tüm gecikmeler negatif",
     lambda s: s.update(teslim_gecikmeleri_s=[-1.0] * len(s["teslim_gecikmeleri_s"])),
     "NEGATİF"),
])
def test_b67_SATIR_ICI_bozuk_yapi_reddediliyor(ad, bozan, beklenen):
    """Bozuk bir satır sessizce KABUL EDİLMEMELİ.

    Dördü de ölçüldü ve dördü de bir SAYI üretiyordu: 846,701 ms · 551,345 ms
    · `nan` · −1 023,977 ms. Araç, var olduğu tek büyüklüğü — kaç paket
    ortak — sessizce yanlış üretiyordu.
    """
    import copy

    a = _kos()
    b = copy.deepcopy(a)
    bozan(b)
    with pytest.raises(KarsilastirmaHatasi, match=beklenen):
        ortak_alt_kume(a, b)


def test_b67_MESRU_satir_hala_kabul_ediliyor():
    """Kontrol kolu: dört değişmez her şeyi reddetmiyor.

    🔴 Y11 — bir koruma yalnızca reddettiğiyle değil, KABUL ETTİĞİYLE de
    sınanır. Bugünkü gerçek çıktıda dördü de TUTUYOR.
    """
    a = _kos()
    ok = ortak_alt_kume(a, dict(a))
    assert ok.ortak_paket > 100, f"yalnızca {ok.ortak_paket} ortak paket"


# ==========================================================================
# 🔴 B0.3 / B0.4 — `06` BÖLÜM 9'UN KOŞUL 2 VE KOŞUL 3'Ü KODA BAĞLANIYOR
#
# koşul 2 (metriğin ne ölçtüğü doğrulanmış):
#   Ortalama tek başına kuyruğu göremez. Ölçüldü (30 tohum, eşleştirilmiş,
#   `en_kisa_yol` S0→S2, ORTAK alt küme): ortalama +5,40 ms (p = 0,0003),
#   p95 **+28,15 ms** (p = 0,0000). Kuyruk merkezin ~5 KATI kötüleşiyor.
#
# koşul 3 (kollar arasında gizli asimetri yok):
#   Kontrol payı ölçülmeden karşılaştırma yapılamaz. Ölçüldü (30 tohum,
#   PENCEREDEN): kollar arası oran **4,0–38,0 kat** (bayt) ·
#   **2,6–18,9 kat** (airtime). Fark bir haksızlık değil bir BULGUDUR —
#   ama raporlanmadan hiçbir karşılaştırma geçerli değildir.
#
# 🔒 Zorlama TİPLİ: eksik alan sessizce `None` üretmez, `KarsilastirmaHatasi`
# fırlatır (B-26/B-87/D-11 deseni).
# ==========================================================================

@pytest.mark.parametrize("eksik", [
    "kontrol_bayt_pencere", "veri_bayt_pencere",
    "kontrol_airtime_s_pencere", "veri_airtime_s_pencere",
])
def test_b04_kontrol_payi_alani_EKSIKSE_karsilastirma_REDDEDILIYOR(eksik):
    """🔴 `06` koşul 3 — kontrol payı olmadan karşılaştırma YAPILAMAZ."""
    a = _kos()
    b = dict(a)
    b.pop(eksik)
    with pytest.raises(KarsilastirmaHatasi, match=eksik):
        ortak_alt_kume(a, b)


def test_b04_dejenere_kontrol_payi_TANIMSIZ_ama_KARSILASTIRMA_YASIYOR():
    """🔴 B-134 — DAVRANIŞ DEĞİŞTİ (yedinci denetim + K-088 kararı).

    Eski hâli tüm karşılaştırmayı `KarsilastirmaHatasi` ile düşürüyordu.
    Denetim ölçtü: 801 ortak paket üzerinden hesaplanmış, tamamen geçerli
    bir gecikme farkı (+10,140 ms) **gecikmeyle hiç ilgisi olmayan** bir
    payda yüzünden üretilemiyordu — `03` B3'ün *"iki çakışmayan olgu tek
    metriğe sıkışırsa metriği İKİYE AYIR"* kuralına aykırı.

    🔒 Yeni sözleşme: kontrol payı `None` olur, karşılaştırma **yaşar**,
    ve `ozet()` bunu **bağırır**. D-11'in asıl derdi *"kendinden emin
    görünen bir SAYI"*ydı; `None` + açık etiket onu karşılıyor.
    """
    a = _kos()
    b = dict(a)
    b["veri_bayt_pencere"] = 0

    o = ortak_alt_kume(a, b)
    assert o.kontrol_payi_b is None, "dejenere pay bir SAYIYA dönüşmüş"
    assert o.kontrol_payi_a is not None, "sağlam taraf da kaybolmuş"

    # 🔴 Asıl kazanç: gecikme karşılaştırması HÂLÂ üretiliyor
    assert o.ortak_paket > 100
    assert o.gecikme_farki_s is not None and o.p95_farki_s is not None

    # 🔒 Ve TANIMSIZLIK sessiz geçmiyor
    assert "TANIMSIZ" in o.ozet(), (
        f"özet tanımsızlığı bağırmıyor: {o.ozet()}")


def test_b04_ozet_KONTROL_PAYINI_iki_birimde_tasiyor():
    """🔴 `08` §Ayrıca — tek birim K-009'un adalet şartını doğrulayamaz.

    Ölçüldü: aynı koşuda kontrol payı bayt cinsinden %2,84, airtime
    cinsinden %5,12 — **1,80 kat**. Sebep önbelge: her çerçeveye sabit
    192 µs ekleniyor, yani aynı baytı daha çok çerçeveye bölen protokol
    airtime'da daha pahalıdır.
    """
    o = ortak_alt_kume(_kos("S0", kol="a"), _kos("S2", kol="b"))
    for pay in (o.kontrol_payi_a, o.kontrol_payi_b):
        assert set(pay) == {"bayt", "airtime"}
        assert 0.0 < pay["bayt"] < 100.0
        assert pay["airtime"] > pay["bayt"], (
            f"airtime payı ({pay['airtime']:.2f}%) bayt payından "
            f"({pay['bayt']:.2f}%) büyük olmalı — önbelge amortismanı")
    assert "kontrol payı" in o.ozet()


def test_b03_yuzdelikler_ORTAK_alt_kumeden_hesaplaniyor():
    """🔴 Yüzdelikler HAM listeden değil, ORTAK alt kümeden gelmeli.

    Ham listeden gelseydi, `06` §8.1'in düzeltmeye çalıştığı seçilim
    yanlılığını yüzdelikler de taşırdı — ilaç hastalığı tekrarlardı.
    """
    a = _kos("S0", kol="a")
    b = _kos("S2", kol="b")
    o = ortak_alt_kume(a, b)

    assert set(o.yuzdelik_a) == {"p50", "p95", "p99"}
    assert o.yuzdelik_a["p50"] <= o.yuzdelik_a["p95"] <= o.yuzdelik_a["p99"]

    # ORTAK alt kümeden hesaplandığının kanıtı: bağımsız yeniden üretim
    ga = dict(zip(a["teslim_kimlikleri"], a["teslim_gecikmeleri_s"]))
    gb = dict(zip(b["teslim_kimlikleri"], b["teslim_gecikmeleri_s"]))
    ortak = sorted(set(ga) & set(gb))
    assert o.yuzdelik_a["p95"] == yuzdelik([ga[k] for k in ortak], 0.95)
    assert o.yuzdelik_b["p95"] == yuzdelik([gb[k] for k in ortak], 0.95)

    # 🔴 Y8 — ham okuma FARKLI bir sayı vermeli, yoksa test hiçbir şey ölçmez.
    #
    # ⚠️ AYRIM **A KOLUNDA** ARANIR, B'de değil (Y5: test kırıldı, önce
    # testin varsayımı denetlendi). Ölçüldü: S0 paketlerin %99,6'sını,
    # S2 %51,2'sini teslim ediyor — yani B'nin teslim ettiklerinin
    # neredeyse TAMAMI zaten ortak kümededir ve B'nin iki okuması
    # meşru biçimde AYNI çıkar. Daralan taraf A'dır.
    assert o.yuzdelik_a["p95"] != yuzdelik(a["teslim_gecikmeleri_s"], 0.95), (
        "A kolunun ortak alt küme p95'i ham p95'iyle aynı — ortak alt küme "
        "daraltmıyor olabilir")

    assert o.p95_farki_s is not None
    assert "p95" in o.ozet()


# ==========================================================================
# 🔴 B0.5 — A-14 DENETİMİNİN KAPATTIĞI TEST BOŞLUKLARI
#
# Modül altı bağımsız denetimde HİÇ açılmadı. Mutasyon kapsamı ölçüldü
# (16 hedefli mutasyon, `dogrulama/` dışı bir ölçüm betiğiyle):
#
#     tüm paket        : 10/16  (%62,5)
#     bu dosya tek başına : 8/16
#
# Sağ kalan ALTI mutant, altı TEST BOŞLUĞUDUR. Üçü "hiç sınanmamış"
# sınıfı (M2 · M3 · M7 · M15), ikisi 🔴 **Y11 sınıfı**: koruma BAŞKA BİR
# KORUMANIN GÖLGESİNDE kalıyordu (M12 · M13) — bir hata yine yakalanıyor
# ama YANLIŞ değişmez tarafından, yani asıl koruma silinse kimse görmez.
#
# ⚠️ Bu, `sim/karsilastirma.py`nin Aile 1'in HER gecikme karşılaştırmasını
# taşıyacağı düşünülünce en pahalı boşluk sınıfıydı.
# ==========================================================================

@pytest.fixture(scope="module")
def s0_sonuc():
    """Modül kapsamlı: tam koşu pahalı, tekrar koşmanın bilgi değeri yok."""
    return _kos("S0", kol="a")


def test_b05_gecikme_ve_p95_farkinin_YONU_dogru(s0_sonuc):
    """🔴 M2 · M3 — fark `b − a` mı, `a − b` mi? Hiçbir test söylemiyordu.

    İşaret ters çevrildiğinde *"kuyruk kötüleşti"* ile *"iyileşti"* yer
    değiştirir ve `06` §8.1b'nin bütün yargısı tersine döner — ama 36
    testin hiçbiri kırılmıyordu.

    Kurulum: B kolu A'nın **birebir aynısı**, yalnızca her gecikmeye sabit
    +10 ms eklenmiş. Ortak alt küme aynı paketleri taşır, dolayısıyla hem
    ortalama hem p95 farkı **tam olarak +10 ms** olmak zorunda.
    """
    import copy
    import statistics

    a = s0_sonuc
    b = copy.deepcopy(a)
    ek = 0.010
    b["teslim_gecikmeleri_s"] = [g + ek for g in a["teslim_gecikmeleri_s"]]
    b["ortalama_gecikme_s"] = statistics.fmean(b["teslim_gecikmeleri_s"])
    b["ortanca_gecikme_s"] = statistics.median(b["teslim_gecikmeleri_s"])

    o = ortak_alt_kume(a, b)
    assert o.ortak_paket == len(a["teslim_kimlikleri"]), "kurulum bozuk (Y8)"
    assert o.gecikme_farki_s == pytest.approx(ek, abs=1e-12), (
        f"ortalama farkının YÖNÜ ya da büyüklüğü yanlış: "
        f"{1000*o.gecikme_farki_s:+.3f} ms, +{1000*ek:.0f} bekleniyordu")
    assert o.p95_farki_s == pytest.approx(ek, abs=1e-12), (
        f"p95 farkının YÖNÜ ya da büyüklüğü yanlış: "
        f"{1000*o.p95_farki_s:+.3f} ms")
    assert o.ham_fark_s == pytest.approx(ek, abs=1e-12)


def test_b05_kontrol_payi_paydasi_TOPLAM_pay_degil(s0_sonuc):
    """🔴 M7 — payda `kb + vb` mi, yoksa `vb` mi?

    `kb / vb` mutasyonu sağ çıkmıştı çünkü tek testin iddiası
    `0 < pay < 100` idi ve küçük bir kontrol payında **ikisi de** o
    aralıkta kalıyor. Bir oran, tanımını sabitleyen bir SAYIYLA
    bağlanmalı — aralıkla değil (`03` B5: yargı veriden çıkmalı).
    """
    from sim.karsilastirma import kontrol_payi_yuzde

    s = dict(s0_sonuc)
    s["kontrol_bayt_pencere"] = 1000
    s["veri_bayt_pencere"] = 1000          # eşit → pay tam %50
    s["kontrol_airtime_s_pencere"] = 1.0
    s["veri_airtime_s_pencere"] = 3.0      # 1/(1+3) → tam %25

    p = kontrol_payi_yuzde(s)
    assert p["bayt"] == pytest.approx(50.0), (
        f"kontrol payı %{p['bayt']:.2f} — payda TOPLAM değil (kb+vb) "
        f"olmalı; `kb/vb` %100 verirdi")
    assert p["airtime"] == pytest.approx(25.0)


def test_b05_EVREN_hash_kontrolu_BAGIMSIZ_calisiyor(s0_sonuc):
    """🔴 M12 · Y11 — paket evreni kontrolü KURULUM kontrolünün gölgesinde.

    `test_b19_farkli_paket_evreni_reddediliyor` iki farklı TOHUM kullanıyor
    ve tohum `kurulum_hash`e de giriyor — yani evren kontrolü silinse bile
    kurulum kontrolü ateşliyor ve test geçiyordu. Ölçüldü: M12 sağ kaldı.

    Burada **yalnızca** `pencere_evren_hash` bozuluyor; başka hiçbir alan
    değişmiyor, dolayısıyla ateşleyebilecek tek koruma odur.
    """
    b = dict(s0_sonuc)
    b["pencere_evren_hash"] = "0" * len(s0_sonuc["pencere_evren_hash"])
    with pytest.raises(KarsilastirmaHatasi, match="EVRENLERİ"):
        ortak_alt_kume(s0_sonuc, b)


def test_b05_KARDINALITE_kontrolu_calisiyor(s0_sonuc):
    """🔴 M15 — B-85'in "teslim > üretilen olamaz" kontrolü hiç sınanmamış.

    Kontrol silindiğinde `ozet()` %100'ü aşan bir kesişim oranı basar —
    denetçinin gördüğü **%328,5** tam olarak buydu. Hiçbir test o satırı
    üretmiyordu.
    """
    # ⚠️ İKİ TARAF DA DEĞİŞTİRİLİR (Y5: test kırıldı, önce testin varsayımı
    # denetlendi). Yalnız B değiştirilirse KOLLAR ARASI kontrol
    # ("pencerede üretilen paket sayıları farklı") ÖNCE ateşliyor ve satır
    # İÇİ kardinalite kontrolü hiç sınanmamış oluyor — aranan boşluğun ta
    # kendisi. Eşit bırakınca ateşleyebilecek tek koruma kardinalitedir.
    az = len(s0_sonuc["teslim_kimlikleri"]) - 1
    a = dict(s0_sonuc)
    b = dict(s0_sonuc)
    a["pencerede_uretilen"] = az
    b["pencerede_uretilen"] = az
    with pytest.raises(KarsilastirmaHatasi, match="ÜRETİLDİ"):
        ortak_alt_kume(a, b)
