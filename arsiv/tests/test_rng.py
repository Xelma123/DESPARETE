"""
Rastgelelik akışları testleri.

Buradaki testlerin çoğu "bariz" görünür. Bariz olmayan şu: bu dosyadaki bir
hatanın belirtisi YOKTUR. Kod çalışır, testler geçer, sonuçlar makul görünür
ve eşleştirilmiş istatistik sessizce yanlış olur.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.rng import AKIS_ADLARI, Akislar, kanal_cekimi  # noqa: E402


# --------------------------------------------------------------------------
# Akışlar
# --------------------------------------------------------------------------

def test_akislar_ayni_tohum_ayni_dizi():
    a = Akislar(1000)
    b = Akislar(1000)
    for ad in AKIS_ADLARI:
        assert [a[ad].random() for _ in range(20)] == [b[ad].random() for _ in range(20)]


def test_akislar_farkli_tohum_farkli_dizi():
    a = Akislar(1000)
    b = Akislar(1001)
    assert [a["yerlesim"].random() for _ in range(20)] != \
           [b["yerlesim"].random() for _ in range(20)]


def test_akislar_birbirinden_bagimsiz():
    """ASIL TEST: bir akıştan çekmek diğerini KAYDIRMAMALI.

    Bu tutmasaydı, keşif yapan bir protokol yerleşimi de kaydırırdı ve
    protokoller farklı topolojiler görürdü.
    """
    a = Akislar(1000)
    beklenen = [a["yerlesim"].random() for _ in range(10)]

    b = Akislar(1000)
    for _ in range(5000):                     # başka akışı bolca tüket
        b["protokol_kesif"].random()
    gozlenen = [b["yerlesim"].random() for _ in range(10)]

    assert beklenen == gozlenen


def test_bilinmeyen_akis_hata_verir():
    a = Akislar(1)
    with pytest.raises(KeyError):
        a["kayit_disi_akis"]


# --------------------------------------------------------------------------
# Kanal — sayaç tabanlı, durumsuz
# --------------------------------------------------------------------------

def test_kanal_cekimi_araligi():
    for i in range(500):
        d = kanal_cekimi(1000, i % 30, (i * 7) % 30, i * 0.013, 1e-4)
        assert 0.0 <= d < 1.0


def test_kanal_cekimi_belirlenimci():
    assert kanal_cekimi(1000, 3, 7, 12.3456, 1e-4) == kanal_cekimi(1000, 3, 7, 12.3456, 1e-4)


def test_kanal_cekimi_dilim_yutuyor():
    """Aynı dilime düşen iki an aynı çekimi vermeli.

    Sebep: iki protokol aynı iletimi mikrosaniyelerle farklı anlarda
    başlatabilir. Dilim o farkı yutmazsa mekanizmanın amacı boşa gider.
    """
    assert (kanal_cekimi(1000, 3, 7, 12.345001, 1e-4)
            == kanal_cekimi(1000, 3, 7, 12.345099, 1e-4))


def test_kanal_cekimi_farkli_dilim_farkli_deger():
    """Ardışık dilimler bağımsız olmalı; yoksa yeniden deneme işlevsizleşir."""
    assert kanal_cekimi(1000, 3, 7, 12.3400, 1e-4) != kanal_cekimi(1000, 3, 7, 12.3460, 1e-4)


def test_kanal_cekimi_yon_duyarli():
    """x→y ile y→x aynı çekim OLMAMALI: farklı alıcı, farklı girişim ortamı."""
    assert kanal_cekimi(1000, 3, 7, 5.0, 1e-4) != kanal_cekimi(1000, 7, 3, 5.0, 1e-4)


def test_kanal_cekimi_tohuma_duyarli():
    assert kanal_cekimi(1000, 3, 7, 5.0, 1e-4) != kanal_cekimi(1001, 3, 7, 5.0, 1e-4)


def test_kanal_cekimi_parca_ayirici_calisiyor():
    """(1, 23) ile (12, 3) gibi bitişik yazımlar çakışmamalı."""
    assert kanal_cekimi(1000, 1, 23, 5.0, 1e-4) != kanal_cekimi(1000, 12, 3, 5.0, 1e-4)


# --------------------------------------------------------------------------
# ⭐ ASIL REGRESYON TESTİ
# --------------------------------------------------------------------------

class _OyuncakYonlendirici:
    """Sahte protokol: sadece kaç iletim denemesi yaptığıyla ayrışır.

    Gerçek protokoller henüz yok. Bu ikili, kanal mekanizmasını ONLAR
    yazılmadan sınamak için var — sorun ortaya çıktığında değil, çıkmadan
    önce yakalansın diye.
    """

    def __init__(self, tohum: int, deneme_katsayisi: int):
        self.tohum = tohum
        self.katsayi = deneme_katsayisi
        self.kayit: dict[tuple[int, int, int], float] = {}

    def kostur(self, adim: int = 200) -> None:
        t = 0.0
        for i in range(adim):
            gonderen, alan = i % 5, (i % 5) + 1
            # Aynı (gönderen, alan, dilim) üçlüsüne düşecek şekilde ilerle
            dilim = i
            zaman = dilim * 1e-4 + 5e-5
            for _ in range(self.katsayi):          # farklı sayıda deneme
                d = kanal_cekimi(self.tohum, gonderen, alan, zaman, 1e-4)
                self.kayit[(gonderen, alan, dilim)] = d
            t = zaman


def test_iki_protokol_ayni_kanali_goruyor():
    """🔴 Bu test kırılırsa eşleştirilmiş istatistik geçersizdir.

    İki 'protokol' farklı sayıda iletim denemesi yapıyor. Sıralı bir RNG
    akışında bu, akışı kaydırır ve ikisi farklı kanal gerçeklemesi görürdü.
    Sayaç tabanlı çekimde görmemeli.
    """
    a = _OyuncakYonlendirici(tohum=1000, deneme_katsayisi=1)
    b = _OyuncakYonlendirici(tohum=1000, deneme_katsayisi=7)
    a.kostur()
    b.kostur()

    ortak = set(a.kayit) & set(b.kayit)
    assert len(ortak) > 100, "test anlamlı olacak kadar ortak üçlü üretmedi"
    for anahtar in ortak:
        assert a.kayit[anahtar] == b.kayit[anahtar], (
            f"aynı (gönderen, alan, dilim) farklı çekim verdi: {anahtar}"
        )


# --------------------------------------------------------------------------
# Süreçler arası belirlenimcilik
# --------------------------------------------------------------------------

def test_hash_pythonhashseed_den_bagimsiz():
    """Python'un yerleşik hash()'i çalışmalar arasında tuzlanır.

    Eğer bir yerde yanlışlıkla hash() kullanılırsa bu test yakalar: farklı
    PYTHONHASHSEED ile aynı sayı çıkmalı. Yakalamazsa, aynı tohum farklı
    günlerde farklı sonuç verir ve kimse sebebini bulamaz.
    """
    kod = (
        "import sys; sys.path.insert(0, r'%s');"
        "from sim.rng import kanal_cekimi, Akislar;"
        "print(repr(kanal_cekimi(1000, 3, 7, 12.3456, 1e-4)));"
        "print(repr(Akislar(1000)['yerlesim'].random()))"
        % str(Path(__file__).resolve().parent.parent)
    )
    ciktilar = []
    for tohum_env in ("0", "1", "12345"):
        p = subprocess.run(
            [sys.executable, "-c", kod],
            capture_output=True, text=True,
            env={**__import__("os").environ, "PYTHONHASHSEED": tohum_env},
        )
        assert p.returncode == 0, p.stderr
        ciktilar.append(p.stdout)
    assert len(set(ciktilar)) == 1, f"PYTHONHASHSEED sonucu değiştirdi: {ciktilar}"


# --------------------------------------------------------------------------
# Kanal dilimi — MARJ kararı (K-024)
#
# ⚠️ DÜZELTME 18 Ağustos 2026: burada önce "yeniden denemeler aynı çekimi
# alıyor" diye bir HATA iddia edilmişti. Ölçüldü ve İDDİA YANLIŞ ÇIKTI.
#
# Hata analizinde yeniden deneme aralığı, başarısız çerçevenin BİTİMİNDEN
# hesaplanmıştı (384–1004 µs). Oysa kanal çekimi çerçevenin BAŞLANGICINA
# anahtarlanıyor ve ardışık başlangıçlar arasında tam bir çerçeve süresi var.
# Gerçek kod yolunda ölçülen ara: 9528–18068 µs. 1 ms dilimde bile çakışma
# hiç olmuyordu.
#
# Dilim yine de 100 µs'de bırakıldı — hata düzeltmesi olarak değil MARJ
# kararı olarak: güvenlik payı çerçeve süresine bağlı ve küçük çerçevelerde
# daralıyor (32 baytlık bir çerçeve 1 Mbit/s'te 448 µs; yeniden deneme arası
# ~832 µs < 1 ms). 100 µs bu bağımlılığı ortadan kaldırıyor.
# --------------------------------------------------------------------------

def test_ardisik_denemeler_gercek_mac_te_ayri_cekim_aliyor():
    """Yeniden denemeler bağımsız çekim almalı — GERÇEK MAC yolunda ölçülür.

    Bu testin ilk yazımı varsayımsal bir zamanlama üzerinden kuruluydu ve
    hiç oluşmayan bir durumu sınıyordu. Şimdi gerçek MAC koşturuluyor.
    """
    import sys
    from pathlib import Path as _P
    sys.path.insert(0, str(_P(__file__).resolve().parent.parent))
    from sim.config import Konfig
    from sim.events import OlayKuyrugu
    from sim.mac import KanalErisimi
    from sim.packet import Paket
    from sim.radio import Radyo
    from sim.topology import Topoloji

    kon = Konfig(kol="t", dugum_sayisi=2, senaryo="S0", yeniden_deneme_siniri=6)
    topo = Topoloji(konumlar=((0.0, 0.0), (5000.0, 0.0)),   # PER = 1
                    iletim_menzili_m=kon.iletim_menzili_m,
                    girisim_menzili_m=kon.girisim_menzili_m)
    ol = OlayKuyrugu()
    mac = KanalErisimi(kon, topo, Radyo.kur(kon), ol, None, Akislar(1))

    baslangiclar: list[float] = []
    asil = mac._ilet
    def izle(d):
        asil(d)
        baslangiclar.append(mac.aktif[-1].baslangic_s)
    mac._ilet = izle
    mac.iletim_basarisiz = lambda p, g, h: None
    mac.gonder(0, Paket(kimlik=0, kaynak=0, hedef=1, bayt=1024, ttl=32), 1)
    ol.kostur(2.0)

    assert len(baslangiclar) >= 5, "yeterince yeniden deneme oluşmadı"
    cekimler = [kanal_cekimi(kon.tohum, 0, 1, t, kon.kanal_dilimi_s)
                for t in baslangiclar]
    assert len(set(cekimler)) == len(cekimler), (
        f"{len(cekimler)} denemeden {len(set(cekimler))}'i ayrı çekim aldı — "
        f"yeniden denemeler bağımsız değil"
    )


def test_dilim_en_kucuk_cerceveyle_bile_guvenli():
    """MARJ değişmezi: dilim, EN KÜÇÜK çerçevenin yeniden deneme arasından küçük.

    Ara = çerçeve süresi + SIFS + onay + slot + DIFS.
    En küçük çerçeve onay çerçevesidir (14 bayt). Bu değişmez, ileride
    paket boyutu veya zamanlama değişirse uyarır.
    """
    from sim.config import Konfig
    kon = Konfig(kol="t")
    en_kucuk_ara = (kon.onay_suresi_s + kon.sifs_s + kon.onay_suresi_s
                    + kon.slot_s + kon.difs_s)
    assert kon.kanal_dilimi_s < en_kucuk_ara / 3, (
        f"kanal dilimi {kon.kanal_dilimi_s*1e6:.0f} µs, en küçük yeniden "
        f"deneme arası {en_kucuk_ara*1e6:.0f} µs — marj yetersiz"
    )


def test_dilim_hala_protokol_zaman_farkini_yutuyor():
    """Dilimin varlık sebebi: protokoller arası mikrosaniyelik farkı yutmak."""
    from sim.config import Konfig
    dilim = Konfig(kol="t").kanal_dilimi_s
    taban = 12.3450
    for fark_us in (1, 10, 50, 99):
        assert (kanal_cekimi(1000, 3, 7, taban, dilim)
                == kanal_cekimi(1000, 3, 7, taban + fark_us * 1e-6, dilim)), (
            f"{fark_us} µs zaman farkı çekimi değiştirdi — dilim çok ince"
        )


# ==========================================================================
# 🔴 B-10 — her akış ya KULLANILIYOR ya BEYAN EDİLMİŞ
# ==========================================================================

def test_b10_beacon_fazi_kendi_akisindan_geliyor():
    """🔴 B-10 REGRESYONU.

    Beacon fazı `trafik_zamani` akışından çekiliyordu — o akışın tanımı
    "CBR titreşimi"dir. `AKIS_ADLARI` listesi *"kapalıdır"* diyor ve
    `03` Bölüm C *"her rastgelelik kaynağı kendi akışını kullanır"* diyor.

    DEĞİŞMEZ: aynı tohumda, YALNIZCA beacon akışını ilerleten bir değişiklik
    CBR titreşim dizisini ETKİLEYEMEZ. İki akış bağımsızdır.
    """
    from sim.rng import AKIS_ADLARI, Akislar

    assert "beacon_faz" in AKIS_ADLARI

    # Beacon akışından N çekim yapmak, trafik akışının dizisini kaydırmamalı
    a1 = Akislar(4242)
    trafik_once = [a1["trafik_zamani"].random() for _ in range(5)]

    a2 = Akislar(4242)
    for _ in range(40):                      # 40 düğümlük beacon fazı kadar
        a2["beacon_faz"].uniform(0.0, 1.0)
    trafik_sonra = [a2["trafik_zamani"].random() for _ in range(5)]

    assert trafik_once == trafik_sonra, (
        "beacon akışı ilerleyince CBR titreşimi kaydı — akışlar bağımsız değil"
    )


def test_b10_her_akis_ya_kullaniliyor_ya_beyan_edilmis():
    """🔴 `03` B5: "bildirim ≠ kullanım" — akış listesi için.

    `AKIS_ADLARI` "kapalı" bir listedir. Kapalı olmak, listede olmayanın
    kullanılamaması kadar, listede olanın da GERÇEKTEN kullanılması demektir;
    aksi hâlde liste bir niyet beyanına dönüşür.

    Her akış ya bir koşuda fiilen çekim alır, ya `HENUZ_KULLANILMAYAN`da
    açıkça beyan edilir. Üçüncü seçenek yoktur.
    """
    from sim.config import Konfig
    from sim.kosucu import Kosu
    from sim.rng import AKIS_ADLARI, HENUZ_KULLANILMAYAN, Akislar
    from dogrulama.aktaricilar import en_kisa_yol

    kullanilan: set[str] = set()
    asil = Akislar.__getitem__

    def izleyen(self, ad):                    # noqa: ANN001
        kullanilan.add(ad)
        return asil(self, ad)

    Akislar.__getitem__ = izleyen             # type: ignore[assignment]
    try:
        Kosu(Konfig(kol="t", senaryo="S4", trafik="orta", tohum=1,
                    isinma_s=5.0, olcum_bitis_s=25.0, kosu_bitis_s=30.0),
             en_kisa_yol).kostur()
    finally:
        Akislar.__getitem__ = asil            # type: ignore[assignment]

    # Y7 — tarama gerçekten bir şey topladı mı?
    assert len(kullanilan) >= 4, f"izleme çalışmadı: {kullanilan}"

    for ad in AKIS_ADLARI:
        if ad in HENUZ_KULLANILMAYAN:
            assert ad not in kullanilan, (
                f"{ad!r} HENUZ_KULLANILMAYAN'da ama fiilen kullanılıyor — "
                f"liste güncellenmeli"
            )
            continue
        assert ad in kullanilan, (
            f"{ad!r} akışı bildirilmiş ama bir koşuda HİÇ çekim almıyor. "
            f"Ya kullanılmalı, ya HENUZ_KULLANILMAYAN'a yazılmalı."
        )


# ==========================================================================
# 🔴 B-117 / M25 (ALTINCI DENETİM) — DİLİMİN KABALAŞMASI KORUMASIZDI
#
# Mutasyon: `int(zaman_s // dilim_s)` -> `int(zaman_s // (dilim_s * 10))`.
# `Konfig.kanal_dilimi_s` DEĞİŞMİYOR; değişen, `kanal_cekimi`in İÇİNDEKİ
# bölen. Ölçüldü (27 Ağu, 4 yapılandırma × 65 sayısal alan): 44–48 alan
# değişiyor.
#
# 🔴 VE İKİ KORUMA DA SUSUYOR — ölçüldü, `test_rng.py` +
# `test_kapi_aile0.py` mutantla **43 passed**:
#
#   · Ç6.2'nin marj değişmezi `Konfig.kanal_dilimi_s`ten ANALİTİK hesap
#     yapar; `kanal_cekimi`in içindeki bölene BAKMAZ. Konfig değeri
#     değişmediği için değişmez susar.
#   · `test_dilim_hala_protokol_zaman_farkini_yutuyor` *"1–99 µs fark AYNI
#     çekimi vermeli"* der. Kabalaşma bunu DAHA DA doğru yapar -> geçer.
#
# İkincisi TEK YÖNLÜ bir iddiadır ve bu test onun EKSİK YARISIDIR:
# **dilim sınırını GEÇEN zamanlar FARKLI çekim almak zorunda.**
# `rng.py`nin kendi gerekçesi: *"fazla KABA olursa aynı çiftin ardışık
# denemeleri aynı dilime düşer, AYNI çekimi alır ve yeniden deneme
# mekanizması sessizce işlevsizleşir."* Gerekçe yazılıydı, ölçütü yoktu.
# ==========================================================================

def test_b117_m25_dilim_SINIRINI_GECEN_zamanlar_FARKLI_cekim_aliyor():
    """🔴 `test_dilim_hala_protokol_zaman_farkini_yutuyor`un EKSİK YARISI.

    O test *"yakın zamanlar AYNI çekim"* diyor. Tek başına, dilimi 10 kat
    kabalaştıran bir mutasyondan SAĞ ÇIKAR — kabalaşma yakınlığı artırır.
    Ayırt eden iddia bunun tersi: **bir dilimden fazla ayrık zamanlar
    FARKLI çekim almalı.**

    ⚠️ İLK YAZIMI KIRILDI ve sebebi TESTİN VARSAYIMIYDI (Y5): `12.0` saniyeyi
    "dilim sınırına hizalı" saymıştım, oysa kayan noktada
    `12.0 // 1e-4 == 119999` ve `12.00006 // 1e-4 == 120000` — sınır
    beklediğim yerde değil. Zamanlar artık DİLİM İNDEKSİNDEN türetiliyor
    (`(k + 0.5) * dilim`), yani sınır belirsizliği yapısal olarak yok.
    """
    from sim.config import Konfig

    dilim = Konfig(kol="t").kanal_dilimi_s
    assert dilim > 0
    k0 = 120_000
    orta = (k0 + 0.5) * dilim
    assert int(orta // dilim) == k0, "dilim ortası kurulumu bozuk (Y7)"

    ayni = kanal_cekimi(1000, 3, 7, orta, dilim)

    # 🔴 Y8 — AYNI dilim içinde çekim GERÇEKTEN sabit mi (ölçüt canlı mı)
    for kesir in (0.25, 0.75):
        assert kanal_cekimi(1000, 3, 7, (k0 + kesir) * dilim, dilim) == ayni, (
            "aynı dilim içinde çekim değişti — ölçüt bozuk, aşağıdaki "
            "'farklı olmalı' iddiası anlamsız olurdu (Y7)")

    # 🔴 ASIL ÖLÇÜT — sınırı geçen her adım FARKLI çekim vermeli
    farkli = sum(
        1 for k in (1, 2, 3, 5, 9)
        if kanal_cekimi(1000, 3, 7, (k0 + k + 0.5) * dilim, dilim) != ayni)
    assert farkli == 5, (
        f"🔴 dilim sınırını geçen 5 zamandan yalnızca {farkli}'i FARKLI "
        f"çekim aldı. Dilim KABALAŞMIŞ olabilir: `kanal_cekimi`in içindeki "
        f"bölen `Konfig.kanal_dilimi_s`ten ayrışırsa ardışık denemeler aynı "
        f"çekimi paylaşır ve yeniden deneme sessizce işlevsizleşir "
        f"(B-117/M25 · `rng.py`nin kendi gerekçesi).")


def test_b117_m25_dilim_INCELMEYI_de_yakaliyor():
    """🔴 Üstteki ölçüt KABALAŞMAYI yakalar; bu ölçüt İNCELMEYİ.

    İkisi birlikte bölenin DEĞERİNİ pinler, yalnızca yönünü değil (Y11:
    koruma tek yönlü kalırsa kapsamının yarısı boştur).
    """
    from sim.config import Konfig

    dilim = Konfig(kol="t").kanal_dilimi_s
    k0 = 120_000
    a = kanal_cekimi(1000, 3, 7, (k0 + 0.10) * dilim, dilim)
    b = kanal_cekimi(1000, 3, 7, (k0 + 0.90) * dilim, dilim)
    assert a == b, (
        "🔴 aynı dilimin iki ucu FARKLI çekim verdi — bölen "
        "`kanal_dilimi_s`ten İNCE. Protokoller arası mikrosaniyelik zaman "
        "farkı çekime sızar (`rng.py`nin ikinci gerekçesi).")
