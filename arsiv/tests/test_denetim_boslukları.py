"""
🔴 BAĞIMSIZ DENETİM — MUTASYON BOŞLUKLARININ REGRESYONU (B-04).

Sıfır bağlamlı bir denetçi 10 bağımsız mutasyon yazdı ve **8'i 198 testlik
paketten SAĞ ÇIKTI.** Bu dosya o boşlukları kapatır.

⚖️ NEDEN OLDU — kendi mutasyon paketimin 7 mutasyonu 7/7 yakalanıyordu, ama
o 7 mutasyon **zaten test edilmiş yollardan seçilmişti.** Seçim yanlılığı.
Denetçinin örüntü tespiti: *"Radyo ve MAC fiziği iyi korunuyor. Gözlem
penceresi, ölçüm penceresi, kontrol düzlemi muhasebesi ve kapı eşikleri hiç
korunmuyor."*

Her test, kapattığı mutasyonun kodunu başlığında taşır.
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import en_kisa_yol  # noqa: E402
from sim.config import Konfig  # noqa: E402
from sim.gozlem import KomsuKaydi  # noqa: E402
from sim.kosucu import Kosu  # noqa: E402
from sim.ledger import KorunumDefteri  # noqa: E402
from sim.packet import Paket  # noqa: E402
from sim.queues import Kuyruk  # noqa: E402


# ==========================================================================
# D3 — komşu tazelik filtresi
# ==========================================================================

def test_d3_bayat_komsu_gozlemden_dusuyor():
    """🔴 D3 — komşu tazelik filtresi kaldırılınca hiçbir test kırılmıyordu.

    v1'in TÜM teşhisi *"karar anında kullanılan bilginin yaşı"* idi
    (3,95 s vs rakibin 1,00 s). Tazelik filtresi korumasız kalırsa Aile 2'nin
    hipotezi ölçülemez hâle gelir.
    """
    kon = Konfig(kol="t", senaryo="S0", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    k.olaylar.simdi = 1000.0
    omur = kon.komsu_omru_s

    k.komsu_tablosu[0] = {
        1: KomsuKaydi(1, 1000.0 - omur * 0.5, 5, 0.0, 0, (0.0, 0.0)),   # taze
        2: KomsuKaydi(2, 1000.0 - omur * 2.0, 5, 0.0, 0, (0.0, 0.0)),   # bayat
    }
    g = k._gozlem_uret(0, None)
    gorulen = {x.dugum for x in g.komsular}
    assert gorulen == {1}, (
        f"bayat komşu filtrelenmedi: {gorulen} (ömür {omur} s)"
    )


def test_d3b_komsu_yasi_gercekten_hesaplaniyor():
    """`yas_s` protokolün tazelik kararı verdiği tek araç — çalışmalı."""
    kayit = KomsuKaydi(1, 100.0, 3, 0.0, 0, None)
    assert kayit.yas_s(105.0) == pytest.approx(5.0)


# ==========================================================================
# D4 — ölçüm penceresi sınırı
# ==========================================================================

def test_d4_olcum_penceresi_isinmaya_tasmiyor():
    """🔴 D4 — pencere 10 s ısınmaya taşırılınca hiçbir test kırılmıyordu.

    `03` Bölüm C: *"Ölçüm penceresi — ısınma ayrı, ölçüm ayrı; tüm sayaçlar
    aynı pencereden. Sonradan eklenemez."* Isınma sızıntısı hiçbir yerde
    sınanmıyordu.
    """
    kon = Konfig(kol="t", senaryo="S0", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    s = k.kostur()

    bas, bit = kon.olcum_penceresi
    assert bas == kon.isinma_s and bit == kon.olcum_bitis_s

    # Bağımsız sayım — koşucunun kendi filtresini kullanmadan
    bagimsiz = sum(1 for p in k.trafik.uretilen_paketler
                   if bas <= p.dogum_s <= bit)
    assert s["pencerede_uretilen"] == bagimsiz

    # 🔴 Sınırın DIŞINDA doğan hiçbir paket sayılmamalı
    pencere_disi = [p for p in k.trafik.uretilen_paketler
                    if p.dogum_s < bas or p.dogum_s > bit]
    assert pencere_disi, "test anlamlı değil: pencere dışında hiç paket yok"
    assert s["pencerede_uretilen"] + len(pencere_disi) == \
        len(k.trafik.uretilen_paketler)

    # Isınmada üretilen paket sayısı, ısınma süresi × akış sayısıyla tutarlı
    isinmada = sum(1 for p in k.trafik.uretilen_paketler if p.dogum_s < bas)
    beklenen = kon.isinma_s * kon.aktif_cift / kon.cbr_araligi_s
    assert isinmada == pytest.approx(beklenen, rel=0.1), (isinmada, beklenen)


# ==========================================================================
# D5 — kontrol düzlemi muhasebesi
# ==========================================================================

def test_d5_beacon_baytlari_kontrol_yukune_yaziliyor():
    """🔴 D5 — beacon baytı sayılmayınca hiçbir test kırılmıyordu.

    `03` B3: *"Kontrol yükünü BAYT cinsinden say."* K-009: *"tüm kollar eşit
    kontrol düzlemi bütçesiyle koşar."* Sayaç bozulursa eşitlik iddiası
    dayanaksız kalır.
    """
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    s = k.kostur()
    beacon_bayt = s["beacon_gonderilen"] * k.kon.beacon_bayt
    onay_bayt = s["mac_onay"] * k.kon.onay_bayt
    assert s["kontrol_bayt"] == beacon_bayt + onay_bayt, (
        s["kontrol_bayt"], beacon_bayt, onay_bayt)
    assert beacon_bayt > 0 and onay_bayt > 0


def test_d5b_cift_faturalama_yok():
    """Veri baytı kontrol yüküne, kontrol baytı veri yüküne karışmamalı."""
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    s = k.kostur()
    assert s["veri_bayt"] == s["mac_gonderilen"] * k.kon.paket_bayt
    assert sum(k.mac.dugum_gonderilen_bayt) == s["veri_bayt"] + s["kontrol_bayt"]


# ==========================================================================
# D8 — kuyruk kapasitesi
# ==========================================================================

def test_d8_kuyruk_kapasitesi_tam_olarak_uyuluyor():
    """🔴 D8 — kapasite fiilen +1 yapılınca hiçbir test kırılmıyordu.

    "Taşma var mı yok mu" testleri vardı ama "tam olarak kaçta taşıyor"
    testi yoktu — yani kapasitenin DEĞERİ korumasızdı.
    """
    defter = KorunumDefteri()
    kuyruk = Kuyruk(0, kapasite=3, defter=defter)
    for i in range(3):
        assert kuyruk.ekle(Paket(i, 0, 1, 100), yeni_uretilen=True) is True
    assert len(kuyruk) == 3
    # 4'üncü DÜŞMELİ
    assert kuyruk.ekle(Paket(3, 0, 1, 100), yeni_uretilen=True) is False
    assert len(kuyruk) == 3
    assert kuyruk.tasma_sayisi == 1
    assert defter.kontrol()["korunum_tamam"] is True


# ==========================================================================
# D9 — yakınsama eşiği
# ==========================================================================

def _sahte_paketler(k: Kosu, dilim_oranlari: list[float]) -> None:
    """Verilen dilim teslim oranlarını üretecek sahte paket listesi kurar."""
    bas, bit = k.kon.olcum_penceresi
    dilimler, _ = k._yakinsama_dilimleri()
    paketler = []
    kimlik = 0
    for (a, b), oran in zip(dilimler, dilim_oranlari):
        for i in range(100):
            p = Paket(kimlik, 0, 1, 100, dogum_s=a + (b - a) * (i + 0.5) / 100)
            if i < int(oran * 100):
                p.teslim_s = p.dogum_s + 0.01
            paketler.append(p)
            kimlik += 1
    k.trafik.uretilen_paketler = paketler


def test_d9_yakinsama_esigi_gercekten_ayirt_ediyor():
    """🔴 D9 — eşik 0,05 → 0,99 yapılınca hiçbir test kırılmıyordu.

    Hiçbir test `yakinsadi is False` iddia etmiyordu; kapı, kendi eşiği
    anlamsızlaştırıldığında sessiz kalıyordu.
    """
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)

    # Eşiğin ALTINDA fark → yakınsadı
    _sahte_paketler(k, [0.80, 0.81, 0.82])
    y = k.yakinsama_kontrolu()
    assert y["en_buyuk_fark"] == pytest.approx(0.02, abs=1e-9)
    assert y["yakinsadi"] is True

    # Eşiğin ÜSTÜNDE fark → YAKINSAMADI
    _sahte_paketler(k, [0.50, 0.70, 0.90])
    y = k.yakinsama_kontrolu()
    assert y["en_buyuk_fark"] == pytest.approx(0.40, abs=1e-9)
    assert y["yakinsadi"] is False, (
        "büyük dilim farkı 'yakınsadı' işaretlendi — eşik anlamsız"
    )


def test_d9b_pdr_sifirda_dejenere_isaretleniyor():
    """🔴 B-11 — hiçbir şey teslim edilmediğinde kapı EN İYİ skoru veriyordu."""
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    _sahte_paketler(k, [0.0, 0.0, 0.0])
    y = k.yakinsama_kontrolu()
    assert y["yakinsadi"] is None, y
    assert "dejenere" in y
    assert y["teslim_gozlem"] == 0


# ==========================================================================
# D10 — beacon içeriği
# ==========================================================================

def test_d10_beacon_gercek_konum_bildiriyor():
    """🔴 D10 — beacon herkese (0,0) bildirince hiçbir test kırılmıyordu.

    Beacon içeriği gözlem penceresinin tek bilgi kanalı; içeriği bozulursa
    coğrafi/kalite temelli her protokol sessizce körleşir.
    """
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    k.kostur()

    konumlar = set()
    for tablo in k.komsu_tablosu.values():
        for kayit in tablo.values():
            assert kayit.bildirdigi_konum is not None
            konumlar.add(kayit.bildirdigi_konum)
            # Bildirilen konum GERÇEK konum olmalı
            assert kayit.bildirdigi_konum == k.topo.konumlar[kayit.dugum]
    assert len(konumlar) > 5, f"yalnızca {len(konumlar)} farklı konum bildirildi"


def test_d10b_beacon_gurultu_ve_kuyruk_bildiriyor():
    """Beacon'ın diğer iki alanı da gerçek değer taşımalı."""
    k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol)
    k.kostur()
    gurultuler = {kayit.bildirdigi_gurultu_w
                  for tablo in k.komsu_tablosu.values()
                  for kayit in tablo.values()}
    assert len(gurultuler) > 5, "tüm komşular aynı gürültüyü bildiriyor"
    assert all(g > 0 for g in gurultuler), "gürültü sıfır bildirilmiş"


# ==========================================================================
# 🔴 B-06 — bildirilmiş ama kullanılmayan ablasyon bayrakları
# ==========================================================================

def _bayrak_metrigi_degistiriyor(ad: str, varsayilan: bool) -> bool:
    """Bayrağı ters çevirince EN AZ BİR tohumda sonuç değişiyor mu?

    Kısa koşu (5 s ısınma + 20 s ölçüm) yeterli: aranan şey etkinin
    BÜYÜKLÜĞÜ değil, VARLIĞI.

    ⚠️ Tohum aralığı ölçümle seçildi, tahminle değil: bağlantı koşullaması
    30 ayarlama tohumunun 4'ünde (5 · 15 · 23 · 25) fiilen devreye giriyor,
    yani 1–8 aralığı tam olarak bir tanesini (5) kapsıyor.
    Üretici: `Topoloji.uret` iki bayrak değeriyle, tohum 1..30, konum
    demetleri karşılaştırılarak.
    """
    ortak = dict(isinma_s=5.0, olcum_bitis_s=25.0, kosu_bitis_s=30.0,
                 trafik="seyrek", senaryo="S2")
    for tohum in range(1, 9):
        a = Kosu(Konfig(kol="a", tohum=tohum, **{ad: varsayilan}, **ortak),
                 en_kisa_yol).kostur()
        b = Kosu(Konfig(kol="b", tohum=tohum, **{ad: not varsayilan}, **ortak),
                 en_kisa_yol).kostur()
        if any(a[k] != b[k] for k in
               ("teslim_orani", "pencerede_uretilen", "mac_deneme", "topoloji")):
            return True
    return False


def test_b06_bildirilen_her_bool_bayrak_ya_etkilidir_ya_hata_verir():
    """🔴 B-06 REGRESYONU — `03` B5: "bildirim ≠ kullanım".

    İki ablasyon bayrağı (`takvimli_tazeleme`, `bayat_bilgi_null`) hiçbir kod
    tarafından okunmuyordu — ama `Konfig.sozluk()` `asdict()` kullandığı için
    HER SONUÇ SATIRINA yazılıyorlardı. Biri `bayat_bilgi_null=True` ile
    koşsaydı hiçbir şey değişmezdi, ama satır "null model kolu" diye
    etiketlenmiş olurdu.

    Bu test GELECEKTEKİ bayrakları da kapsar: `Konfig`e eklenen her `bool`
    alan ya ölçülebilir bir etki üretmek ya da `UYGULANMAMIS_BAYRAKLAR`da
    açıkça beyan edilmek zorundadır. Üçüncü bir seçenek yoktur.
    """
    from dataclasses import fields

    bayraklar = [(f.name, f.default) for f in fields(Konfig) if f.type == "bool"]
    # Y7 — tarama gerçekten bir şey topladı mı? Boş küme her koşulu sağlar.
    assert len(bayraklar) >= 3, f"bool alan taraması boş/eksik: {bayraklar}"

    for ad, varsayilan in bayraklar:
        if ad in Konfig.UYGULANMAMIS_BAYRAKLAR:
            with pytest.raises(NotImplementedError):
                Konfig(kol="t", **{ad: True})
            continue
        assert _bayrak_metrigi_degistiriyor(ad, varsayilan), (
            f"{ad!r} bayrağı ters çevrildiğinde 8 tohumun hiçbirinde metrik "
            f"değişmedi. Ya etkisizdir (o zaman UYGULANMAMIS_BAYRAKLAR'a "
            f"girmeli), ya da etkisi ölçülemiyordur — ikisi de sonuç "
            f"satırındaki etiketi yalancı yapar."
        )


# ==========================================================================
# 🔴 B-22 — kırılamayan iddia: pytest.approx'un mutlak tabanı
# ==========================================================================

def test_b22_kucuk_buyukluklerde_rel_tek_basina_baglayici_degil():
    """🔴 B-22 REGRESYONU — bu tuzak beş ayrı iddiayı sessizleştirmişti.

    `pytest.approx(beklenen, rel=r)` toleransı `max(r*|beklenen|, 1e-12)`
    olarak hesaplar. Karıştırıcı ve gürültü güçleri ~1e-14 W mertebesinde
    olduğu için MUTLAK TABAN her zaman baskındı: Ç3.1 (girişim toplamsal),
    Ç3.2 (parça parça hesap), Ç3.3 (darbeli ortalama güç) ve iki radyo
    testi, karşılaştırdıkları büyüklük NE OLURSA OLSUN geçiyordu.

    Ölçülen (aile0 denetim tekrarı, 19 Ağustos 2026): girişimi toplamsal
    olmaktan çıkaran bir mutasyon `abs=0.0` OLMADAN geçiyor, `abs=0.0` İLE
    kırılıyor.

    `03` B3: "metrik gerçekten onu mu ölçüyor?" — bir iddia, tanım gereği
    hiçbir zaman kırılamıyorsa hiçbir şey ölçmüyordur.
    """
    kucuk = 5e-15                      # tipik karıştırıcı gücü (W)

    # TUZAK: iki kat fark — %100 hata — ve yine de "yaklaşık eşit"
    assert 2 * kucuk == pytest.approx(kucuk, rel=0.02)

    # DOĞRUSU: mutlak taban kapatılınca `rel` fiilen bağlayıcı olur
    assert 2 * kucuk != pytest.approx(kucuk, rel=0.02, abs=0.0)
    assert kucuk * 1.001 == pytest.approx(kucuk, rel=0.02, abs=0.0)


# ==========================================================================
# 🔴 KÖR TARAMANIN SAĞ KALANLARI — ölçümle ayıklandı (K-037 eki)
#
# `dogrulama/kor_mutasyon.py` temiz tabanla koşunca 12 mutant sağ kaldı.
# `dogrulama/sag_kalan_ayikla.py` her birini 44 koşuluk bir matriste ölçtü:
# **4'ü davranışı gerçekten değiştiriyordu** ve hiçbir test bunu görmüyordu.
#
# ⚠️ Aşağıdaki testler sayaçların İŞARETİNİ değil DEĞİŞMEZİNİ sınar. Yalnızca
# "> 0" yazmak mutasyonu yakalardı ama sözleşmeyi korumazdı — sayaç yanlış
# şeyi sayarsa yine geçerdi.
# ==========================================================================

def test_s08_atlama_sayisi_ziyaret_listesiyle_tutarli():
    """🔴 S08 — `atlama_sayisi` işareti bozulunca hiçbir test kırılmıyordu.

    `ortalama_atlama` RAPORA GİREN üç metrikten biri (`06` Bölüm 4) ve
    tamamen bu sayaca dayanıyor.

    DEĞİŞMEZ: `atla()` hem sayacı artırır hem `_ziyaret`e ekler — ikisi
    aynı olayın iki kaydıdır ve ASLA ayrışamaz. Sayacı bozan bir mutasyon
    ikisini ayırır.
    """
    kon = Konfig(kol="t", senaryo="S2", trafik="orta", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    s = k.kostur()

    paketler = k.trafik.uretilen_paketler
    assert paketler, "hiç paket üretilmedi — test bir şey ölçmüyor (Y7)"

    atlayan = [p for p in paketler if p.atlama_sayisi]
    assert atlayan, "hiçbir paket atlamadı — bozulan yol tetiklenmedi (Y8)"
    for p in paketler:
        assert p.atlama_sayisi == len(p._ziyaret), (
            f"paket {p.kimlik}: sayaç {p.atlama_sayisi}, "
            f"ziyaret {len(p._ziyaret)} — tek olayın iki kaydı ayrışmış"
        )

    # Teslim edilen bir paket en az bir atlama yapmıştır.
    assert s["ortalama_atlama"] is not None and s["ortalama_atlama"] >= 1.0, (
        f"ortalama_atlama = {s['ortalama_atlama']}"
    )


def test_s05_toplam_deneme_iletim_sayisindan_az_olamaz():
    """🔴 S05 — `toplam_deneme` işareti bozulunca hiçbir test kırılmıyordu.

    DEĞİŞMEZ: her veri iletimi bir geri çekilmenin ardından başlar, ve her
    geri çekilme başlangıcı bir denemedir. Yeniden denemeler de sayıldığı
    için deneme sayısı iletim sayısından AZ OLAMAZ.
    """
    kon = Konfig(kol="t", senaryo="S2", trafik="orta", tohum=1)
    s = Kosu(kon, en_kisa_yol).kostur()

    assert s["mac_gonderilen"] > 0, "hiç veri gönderilmedi (Y8)"
    assert s["mac_deneme"] >= s["mac_gonderilen"], (
        f"deneme {s['mac_deneme']} < iletim {s['mac_gonderilen']} — "
        f"her iletim bir geri çekilmeden çıkar, bu imkânsız"
    )


def test_s07_kopya_alim_negatif_olamaz_ve_gerceklesiyor():
    """🔴 S07 — `kopya_alim` işareti bozulunca hiçbir test kırılmıyordu.

    Kopya alım, ONAY KAYBININ doğrudan kanıtıdır: alıcı paketi almış ama
    gönderen onayı duymamış ve yeniden göndermiştir. K-027'nin bulduğu
    hata tam olarak bu sayaçla görünür hâle gelmişti.
    """
    kon = Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1)
    s = Kosu(kon, en_kisa_yol).kostur()

    assert s["mac_kopya_alim"] >= 0, "sayaç negatife düştü"
    assert s["mac_kopya_alim"] > 0, (
        "S2/yoğun'da hiç kopya alım yok — bozulan yol tetiklenmedi (Y8); "
        "test bir şey ölçmüyor"
    )
    # Kopya, gönderilenden fazla olamaz.
    assert s["mac_kopya_alim"] <= s["mac_gonderilen"]


def test_s04_ttl_sifira_dusunce_paket_olur():
    """🔴 S04 — TTL sınırı `<= 0` yerine `< 0` yapılınca hiçbir test kırılmadı.

    ⚠️ BU BULGU İKİ AŞAMADA ÇIKTI. Ana matriste (36 koşu) mutasyon
    "eşdeğer" görünüyordu — çünkü `ttl_olumu` orada **0**'dır; TTL yolu hiç
    tetiklenmiyor. Uç durumlar (`ttl_baslangic=2`, döngü yapan aktarıcı)
    eklenince karar **DEĞİŞTİ**'ye döndü.

    Y8'in tam karşılığı: bozulan yolun tetiklendiği gösterilmeden verilen
    "eşdeğer" kararı, kararsızlıktan başka bir şey değildir.

    DEĞİŞMEZ: TTL bir atlamada sıfıra düşen bir paket, hedefe varmadıysa
    ÖLÜR. `< 0` yapmak ona bir atlama daha hediye eder.
    """
    kon = Konfig(kol="t", senaryo="S2", tohum=1, ttl_baslangic=1)
    k = Kosu(kon, en_kisa_yol)
    defter_once = k.defter.dusen["ttl"]

    # ttl=1 olan bir paket, hedefi OLMAYAN bir düğüme varınca:
    # atla() ttl'i 0 yapar -> `ttl <= 0` ile ölmeli.
    paket = Paket(kimlik=9001, kaynak=0, hedef=39, bayt=kon.paket_bayt, ttl=1)
    k.defter.uret()
    k.defter.kuyruktan_al()          # kuyrukta -> uçuşta
    k._alim_gerceklesti(paket, gonderen=0, alan=5)

    assert paket.ttl == 0, paket.ttl
    assert k.ttl_olumu == 1, (
        f"TTL sıfıra düştü ama paket ölmedi (ttl_olumu={k.ttl_olumu}) — "
        f"sınır `<= 0` olmalı, `< 0` bir atlama fazla verir"
    )
    assert k.defter.dusen["ttl"] == defter_once + 1
