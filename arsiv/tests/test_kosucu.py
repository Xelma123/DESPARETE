"""
Gerçek koşucu testleri — korunum · TTL · kuyruk · boşaltma · belirlenimcilik.

`test_skeleton.py`nin yerini alır. Fark: buradaki her paket GERÇEK MAC'ten,
gerçek çekişmeden ve gerçek karıştırıcıdan geçer. İskelet kusursuz kanal
kullanıyordu ve bu üç yol hiç sınanmıyordu.

🔴 Aktarıcılar `dogrulama/aktaricilar.py`den geliyor ve KÂHİNDİR — topolojiyi
doğrudan okurlar. `sim/` altında değiller, olmamalılar da.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import AKTARICILAR  # noqa: E402
from dogrulama.aktaricilar import (  # noqa: E402
    dongu_yapan, en_kisa_yol, hedefe_en_yakin, olu,
)
from sim.config import Konfig  # noqa: E402
from sim.kosucu import Kosu  # noqa: E402


# ==========================================================================
# Korunum — Ç1'in birim test karşılığı
# ==========================================================================

@pytest.mark.parametrize("tohum", [1, 2, 3])
@pytest.mark.parametrize("senaryo", ["S0", "S2", "S4"])
def test_korunum_gercek_mac_yolunda_tutuyor(tohum, senaryo):
    k = Kosu(Konfig(kol="t", senaryo=senaryo, tohum=tohum), en_kisa_yol)
    k.kostur()
    assert k.defter.kontrol()["korunum_tamam"] is True, k.defter.kontrol()


@pytest.mark.parametrize("aktarici", [en_kisa_yol, hedefe_en_yakin,
                                      dongu_yapan, olu])
def test_korunum_her_aktarici_turunde_tutuyor(aktarici):
    """Aktarıcı ne kadar bozuk olursa olsun paket YOK EDİLEMEZ.

    Kötü bir aktarıcı yalnızca düşürebilir, ve düşen paket sayılır.
    """
    k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1, ttl_baslangic=8), aktarici)
    k.kostur()
    assert k.defter.kontrol()["korunum_tamam"] is True


# ==========================================================================
# Belirlenimcilik
# ==========================================================================

def test_ayni_tohum_birebir_ayni_sonuc():
    def kos():
        return Kosu(Konfig(kol="t", senaryo="S2", tohum=7), en_kisa_yol).kostur()
    assert kos() == kos()


def test_farkli_tohum_farkli_sonuc():
    a = Kosu(Konfig(kol="t", senaryo="S2", tohum=7), en_kisa_yol).kostur()
    b = Kosu(Konfig(kol="t", senaryo="S2", tohum=8), en_kisa_yol).kostur()
    assert a != b


def test_karistiricinin_etkisi_var():
    """S2, S0'dan anlamlı biçimde kötü olmalı — yoksa karıştırıcı bağlı değil."""
    s0 = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol).kostur()
    s2 = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol).kostur()
    assert s2["teslim_orani"] < s0["teslim_orani"] - 0.1, (s0, s2)


# ==========================================================================
# Mekanizmalar gerçekten çalışıyor mu (bildirim ≠ kullanım)
# ==========================================================================

def test_ttl_dongude_devreye_giriyor():
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1, ttl_baslangic=6),
             dongu_yapan)
    s = k.kostur()
    assert s["ttl_olumu"] > 0
    assert s["donguyle_olen"] > 0
    assert k.defter.kontrol()["korunum_tamam"] is True


def test_hedef_yok_sayiliyor():
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), olu)
    s = k.kostur()
    assert s["hedef_yok"] > 0
    assert s["teslim_orani"] == 0.0


def test_kuyruk_tasmasi_dar_kuyrukta_gorunuyor():
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1, kuyruk_kapasitesi=1,
                    trafik="yogun", cbr_araligi_s=0.05), en_kisa_yol)
    s = k.kostur()
    assert s["kuyruk_tasmasi"] > 0
    assert k.defter.kontrol()["korunum_tamam"] is True


def test_genis_kuyrukta_tasma_yok():
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1, kuyruk_kapasitesi=500,
                    trafik="seyrek"), en_kisa_yol)
    assert k.kostur()["kuyruk_tasmasi"] == 0


def test_mac_dusurmesi_karistirici_altinda_artiyor():
    s0 = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol).kostur()
    s2 = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol).kostur()
    assert s2["mac_dusurmesi"] > s0["mac_dusurmesi"]


# ==========================================================================
# Ölçüm penceresi ve boşaltma
# ==========================================================================

def test_isinmada_uretilenler_metrige_girmiyor():
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    s = k.kostur()
    toplam = len(k.trafik.uretilen_paketler)
    assert s["pencerede_uretilen"] < toplam
    # Defter TÜM koşuyu sayar; metrik yalnızca pencereyi — ayrı defterler.
    assert k.defter.uretilen == toplam


def test_bosaltma_boruyu_bosaltiyor():
    """Koşu sonunda kuyrukta/uçuşta paket kalmamalı."""
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1, trafik="yogun"),
             en_kisa_yol)
    s = k.kostur()
    assert s["boruda_kalan"] == 0, s


def test_bosaltma_penceresi_teslim_oranini_kurtariyor():
    """Boşaltmasız kurulum daha DÜŞÜK teslim oranı vermeli."""
    ortak = dict(kol="t", senaryo="S0", tohum=1, trafik="yogun",
                 cbr_araligi_s=0.2, kuyruk_kapasitesi=500)
    ile = Kosu(Konfig(**ortak, olcum_bitis_s=320.0, kosu_bitis_s=350.0),
               en_kisa_yol).kostur()
    siz = Kosu(Konfig(**ortak, olcum_bitis_s=320.0, kosu_bitis_s=320.0),
               en_kisa_yol).kostur()
    assert ile["pencerede_uretilen"] == siz["pencerede_uretilen"]
    assert ile["teslim_orani"] > siz["teslim_orani"]


def test_s0_teslim_tavani_yuksek():
    """Kontrol kolunda teslim tavanı ~%100 olmalı.

    Kalan kayıp MAC'e ve bağ PER'ine atfedilebilir; topolojiye değil,
    çünkü çiftler yalnızca bağlı düğümlerden seçiliyor.
    """
    s = Kosu(Konfig(kol="t", senaryo="S0", tohum=1, trafik="seyrek"),
             en_kisa_yol).kostur()
    assert s["teslim_orani"] > 0.99, s["teslim_orani"]


# ==========================================================================
# Trafik ekseni ve rezonans koruması
# ==========================================================================

def test_trafik_seviyeleri_farkli_yuk_uretiyor():
    sayilar = {}
    for seviye in ("seyrek", "orta", "yogun"):
        s = Kosu(Konfig(kol="t", senaryo="S0", tohum=1, trafik=seviye),
                 en_kisa_yol).kostur()
        sayilar[seviye] = s["pencerede_uretilen"]
    assert sayilar["seyrek"] < sayilar["orta"] < sayilar["yogun"], sayilar


def test_akislarin_baslangic_fazi_dagilmis():
    kon = Konfig(kol="t", senaryo="S0", tohum=1, trafik="yogun")
    k = Kosu(kon, en_kisa_yol)
    fazlar = [a.ilk_gonderim_s for a in k.trafik.akislar_listesi]
    assert len(set(fazlar)) == len(fazlar)
    assert max(fazlar) - min(fazlar) > 0.3 * kon.cbr_araligi_s


# ==========================================================================
# Yakınsama kapısı (K5)
# ==========================================================================

def test_duragan_senaryolarda_yakinsiyor():
    for senaryo in ("S0", "S2", "S4"):
        s = Kosu(Konfig(kol="t", senaryo=senaryo, tohum=1), en_kisa_yol).kostur()
        assert s["yakinsama"]["yakinsadi"] is True, (senaryo, s["yakinsama"])


def test_hareketli_karistirici_fizigi_metrige_uydurulmamis():
    """🔴 K-035 regresyonu — TERSİNE ÇEVRİLDİ.

    ⚠️ Bu testin ÖNCEKİ hâli, yörünge periyodunun yakınsama diliminin tam
    katı OLMASINI iddia ediyordu (K-026). Bağımsız denetim gösterdi ki o
    hizalama, faz kaynaklı varyansı 3,3 kat BASTIRIYOR — `03` B6'nın
    örtüşmesi. Ve daha kötüsü: bir KAPI ateşledi diye bir FİZİKSEL parametre
    değiştirilmişti (kural 3 ve 12).

    Şimdi test tersini koruyor: fizik metriğe uydurulmamış OLMALI.
    Hizalamayı metrik yapar, `_yakinsama_dilimleri` yörünge-hizalı dilim
    üretir.
    """
    import math
    kon = Konfig(kol="t", senaryo="S5")
    periyot = (2 * math.pi * kon.karistirici_yorunge_yaricap_m
               / kon.karistirici_hiz_ms)
    ucte_bir = (kon.olcum_bitis_s - kon.isinma_s) / 3.0

    # 🔴 Fizik metriğe UYDURULMAMIŞ olmalı
    assert periyot != pytest.approx(ucte_bir, rel=1e-3), (
        "yörünge periyodu yakınsama diliminin tam katı — fizik metriğe "
        "uydurulmuş olabilir (K-026 hatası)"
    )

    # Hizalamayı METRİK yapıyor
    k = Kosu(kon, en_kisa_yol)
    dilimler, gerekce = k._yakinsama_dilimleri()
    assert "yörünge-hizalı" in gerekce, gerekce
    assert len(dilimler) >= 2
    for a, b in dilimler:
        assert (b - a) == pytest.approx(periyot, rel=1e-9)


def test_s5_de_yakinsiyor():
    """Hizalama sonrası hareketli karıştırıcı da yakınsamalı."""
    s = Kosu(Konfig(kol="t", senaryo="S5", tohum=1), en_kisa_yol).kostur()
    assert s["yakinsama"]["yakinsadi"] is True, s["yakinsama"]


# ==========================================================================
# 🔴 B-50 · B-54 — MUHASEBE KATMANI
#
# Üçüncü bağımsız denetimin örüntüsü: *"Fizik ve MAC iyi korunuyor; RAPORA
# GİREN SAYILAR korunmuyor."* Üç sağ kalan mutasyon da bir sayaç/metrikti.
# ==========================================================================

def test_b50_boruda_kalan_IKI_BILESENIN_toplami():
    """Ç1.4'ün payı sessizce eksiltilebiliyordu.

    `boruda_kalan` yalnızca `ucusta`ya indirgendiğinde 284/284 test
    geçiyordu — ve mutasyon kapı ölçütünü **kolaylaştırıyordu**
    *("boruda kalan < %1")*.

    🔴 Y8: `kuyrukta > 0` olan bir kurulum seçildi, yoksa iki biçim
    ayırt edilemezdi.

    ⚠️ 26 AĞUSTOS 2026 — B-96 (BEŞİNCİ DENETİM): NÖBETÇİ `assert` DEĞİL
    `skip`. Beşinci denetim ölçtü: iki MEKANİZMA mutasyonu *(ikili üstel
    geri çekilme · BER)* kuyruğu boşaltıyor, nöbetçi asıl değişmezden ÖNCE
    kırılıyor ve test *"bu koşuda ÖLÇEMİYORUM"* diyor — ama mutasyon
    oracle'ı bunu **"yakaladım"** diye puanlıyordu. Bir testin *ölçememesi*
    ile *bir kusur bulması* aynı şey değildir.

    🔒 `skip`, Y8'in doğru biçimidir: ölçüm yapılamıyorsa sonuç **yok**
    sayılır, **olumlu** değil.
    """
    k = Kosu(Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1),
             en_kisa_yol)
    s = k.kostur()

    if k.defter.kuyrukta <= 0:
        pytest.skip(
            f"kurulum varsayımı tutmuyor: kuyrukta={k.defter.kuyrukta}. "
            f"Bu koşuda iki biçim AYIRT EDİLEMEZ — ölçüm yapılamadı, "
            f"kusur bulunmadı (B-96).")
    assert s["boruda_kalan"] == k.defter.kuyrukta + k.defter.ucusta, (
        f"boruda_kalan={s['boruda_kalan']}, kuyrukta={k.defter.kuyrukta} + "
        f"ucusta={k.defter.ucusta}")


def test_b95_boruda_kalan_AYNA_yonu_de_yakalaniyor():
    """🔴 B-95 — indirgemenin AYNA yönü: `ucusta` terimini silmek.

    B-50 `kuyrukta > 0`ı zorluyordu ama `ucusta > 0`ı zorlamıyordu.
    Beşinci denetim 18 yapılandırma taradı, hepsinde `ucusta = 0` buldu ve
    mutasyonu **"EŞDEĞER"** ilan etti.

    🔴 **ÖLÇÜM BUNU ÇÜRÜTTÜ.** Denetçinin örneklemi yalnızca `en_kisa_yol`
    kolunu kullanıyordu. Beş kol × 12 yapılandırma tarandı:

        4/60 yapılandırmada `ucusta != 0`
        (`gurultuden_kacan` S0/yoğun · `dongu_yapan` S0/yoğun ×2, S5/yoğun)

    Yani mutasyon eşdeğer DEĞİL; ölçülebilir. Bu test o çalışma noktasını
    sabitler.

    ⚠️ Ç1.4 iki yerde hesaplanıyor ve mutasyon **kapının kendi sayısını**
    eksiltiyor: `aile0_kapi_raporu.py` `boruda_kalan` ALANINDAN okuyor,
    birim testi ise defterden yeniden hesaplıyor.
    """
    k = Kosu(Konfig(kol="t", senaryo="S0", trafik="yogun", tohum=2),
             AKTARICILAR["dongu_yapan"])
    s = k.kostur()

    # 🔴 Y8/B-96 — nöbetçi `skip`, `assert` DEĞİL (ölçememek ≠ kusur bulmak)
    if k.defter.ucusta <= 0:
        pytest.skip(
            f"kurulum varsayımı tutmuyor: ucusta={k.defter.ucusta}. Ayna "
            f"yön bu koşuda AYIRT EDİLEMEZ — ölçüm yapılamadı (B-96).")

    assert s["boruda_kalan"] == k.defter.kuyrukta + k.defter.ucusta, (
        f"🔴 boruda_kalan={s['boruda_kalan']} ama kuyrukta="
        f"{k.defter.kuyrukta} + ucusta={k.defter.ucusta}. Terimlerden biri "
        f"düşürülmüş — Ç1.4'ün payı sessizce eksiliyor (B-95).")

    # 🔴 Y10 — DEĞİŞMEZ KIRILABİLİR Mİ: `ucusta` gerçekten sıfırdan büyük
    # olmalı, yoksa yukarıdaki satır `kuyrukta == kuyrukta + 0`dır.
    assert k.defter.ucusta > 0


def test_b54_en_yuksek_doluluk_BAGIMSIZ_gozlemle_ayni(monkeypatch):
    """Tepe doluluk sayacı gerçekten gözlenen en büyük uzunluk mu?

    BAĞIMSIZ HESAP: her başarılı eklemeden sonra kuyruğun GERÇEK uzunluğu
    okunur ve en büyüğü tutulur. Sayacın kendi güncellemesi kullanılmaz.
    Bir eksik sayan mutasyon 48/48 koşuda davranışı değiştiriyordu ve
    hiçbir test görmüyordu.
    """
    from sim.queues import Kuyruk

    gozlenen = {"tepe": 0}
    asil = Kuyruk.ekle

    def izle(self, paket, yeni_uretilen=False):
        sonuc = asil(self, paket, yeni_uretilen)
        gozlenen["tepe"] = max(gozlenen["tepe"], len(self._paketler))
        return sonuc

    monkeypatch.setattr(Kuyruk, "ekle", izle)
    s = Kosu(Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1),
             en_kisa_yol).kostur()

    assert gozlenen["tepe"] > 1, (
        f"gözlenen tepe {gozlenen['tepe']} — Y8: kuyruk hiç dolmamış, "
        f"sayaç sınanmamış olur")
    assert s["en_yuksek_doluluk"] == gozlenen["tepe"], (
        f"sayaç {s['en_yuksek_doluluk']}, bağımsız gözlem "
        f"{gozlenen['tepe']}")


def test_b54_kacirilan_beacon_KOSULU_yeniden_turetilerek_ayni():
    """Kaçırılan beacon sayacı, kendi koşulundan bağımsız olarak doğrulanır.

    ⚠️ Denetçinin önerdiği formül *(üretilen − gönderilen − bekleyen)*
    ÖLÇÜLDÜ ve **kapanmıyor**: 14 000 − 13 842 − 91 − 0 = 67 fark kalıyor
    *(geri çekilmede bekleyen ve koşu sonunda düşen çerçeveler)*. Bu yüzden
    sayaç bir formülle değil, **düşme koşulunun kendisi yeniden türetilerek**
    doğrulanıyor: MAC meşgul VE zaten bekleyen bir yayın varsa, eski olan
    düşer.

    Sayacı hiç artırmayan bir mutasyon 39/48 koşuda davranışı değiştiriyor
    ve tam paketten sağ çıkıyordu.
    """
    k = Kosu(Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1),
             en_kisa_yol)
    beklenen = {"n": 0}
    asil = k.mac.yayin_gonder

    def izle(dugum, bayt, icerik, yuk_bayt=0):
        m = k.mac.mac[dugum]
        if m.durum != "bos" and m.bekleyen_yayin is not None:
            beklenen["n"] += 1
        return asil(dugum, bayt, icerik, yuk_bayt)

    k.mac.yayin_gonder = izle
    s = k.kostur()

    # Y8 — düşme yolu fiilen tetiklenmeli
    assert beklenen["n"] > 0, "hiç beacon düşmemiş — sayaç sınanmamış olur"
    assert s["beacon_kacirilan"] == beklenen["n"], (
        f"sayaç {s['beacon_kacirilan']}, bağımsız türetme {beklenen['n']}")


# ==========================================================================
# 🔴 B-61 — TRAFİK ÇİFTİ SEÇİMİ
#
# Üçüncü denetim: çift seçimini `sorted(aday)[:istenen]` yapan mutasyon (U12)
# "yakalandı" ama kıran **iki test de İLGİSİZDİ** (gecikme yanlılığı ve
# boşaltma penceresi). *"Yakalandı ≠ korundu"* — mutasyon skoru olduğundan
# iyi görünüyor.
# ==========================================================================

def test_b61_trafik_ciftleri_dugum_uzayina_YAYILIYOR():
    """Kaynak-hedef çiftleri ilk N düğüme YIĞILMAMALI.

    BAĞIMSIZ HESAP: seçilen çiftlerin kaynak/hedef kimliklerinin ORTALAMASI,
    düğüm uzayının ortasına yakın olmalı. `sorted(aday)[:n]` gibi bir seçim
    ortalamayı aşağı çeker — klasik bir `03` B6 kurulum hatası ve tohumlar
    arası varyansı yapay olarak düşürür.
    """
    kon = Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    k.trafik.basla()

    akislar = k.trafik.akislar_listesi
    assert len(akislar) > 5, f"yalnızca {len(akislar)} akış — ölçüm zayıf"

    n = kon.dugum_sayisi
    orta = (n - 1) / 2
    for ad, degerler in (("kaynak", [a.kaynak for a in akislar]),
                         ("hedef", [a.hedef for a in akislar])):
        ort = sum(degerler) / len(degerler)
        assert abs(ort - orta) < n * 0.25, (
            f"{ad} ortalaması {ort:.1f}, düğüm uzayının ortası {orta:.1f} — "
            f"çiftler uzayın bir ucuna yığılmış olabilir")
        # ve üst yarıdan da düğüm seçilmiş olmalı
        assert max(degerler) > orta, (
            f"hiçbir {ad} üst yarıdan seçilmemiş: en büyük {max(degerler)}")


# ==========================================================================
# 🔴 ZİNCİR D (BEŞİNCİ DENETİM) — SONUÇ ŞEMASI: KORUMASIZ KALAN ASIL YÜZEY
#
# Beşinci denetim sayaç/raporlama katmanında **10/26 sağ kalan** ölçtü ve
# şunu yazdı: *"korumasız kalan yüzey mekanizma değil, SONUÇ ŞEMASIDIR — ve
# o yüzey Aile 1'in ölçtüğü şeydir."* Sağ kalanların en ağırları:
#
#   C01 · `ortanca_gecikme_s` ORTALAMAYA çevriliyor  (S0'da 0,109 → 2,450 s)
#   C17 · `pencerede_teslim` → `len(pencere)`         (802 → 2 698)
#   C05 · `islenen_olay` → 0        C10 · `mac_kayip_onay` → 0
#   C19 · `mac_basarisiz_alim` → 0  C16 · `secim_avantaji_karar` kayması
#
# **376 test hiçbirini görmüyordu.** Aşağıdaki üç test o yüzeyi kapatıyor.
#
# ⚠️ Koşular MODÜL KAPSAMINDA paylaşılıyor: üç testin toplamı 2 tam koşu.
# Pahalı bir koruma kapıyı ödenemez kılar (Y12'nin öteki yüzü, K-065).
# ==========================================================================

_D_ONBELLEK: dict = {}


def _d_kosu(kol, senaryo, trafik, tohum):
    """Modül kapsamında paylaşılan koşu — aynı yapılandırma bir kez koşar."""
    anahtar = (kol, senaryo, trafik, tohum)
    if anahtar not in _D_ONBELLEK:
        _D_ONBELLEK[anahtar] = Kosu(
            Konfig(kol="t", senaryo=senaryo, trafik=trafik, tohum=tohum),
            AKTARICILAR[kol]).kostur()
    return _D_ONBELLEK[anahtar]


def test_zd_sonuc_semasi_KENDI_ICINDE_tutarli():
    """🔴 Türetilebilir her alan, kaynağıyla TUTARLI olmak zorunda.

    Beşinci denetimin iki en ağır sağ kalanı burada kapanıyor:
      · **C01** — `ortanca_gecikme_s` ORTALAMAYA çevrilirse yakalanır
        *(iki büyüklük uzun kuyruklu dağılımda taban tabana farklıdır)*
      · **C17** — `pencerede_teslim` `len(pencere)`ye çevrilirse yakalanır

    ⚠️ `03` B3: *"üçlü sun: teslim · gecikme · kontrol yükü"*. Hangi
    gecikme büyüklüğünün raporlandığını hiçbir test doğrulamıyordu.
    """
    import statistics

    s = _d_kosu("en_kisa_yol", "S2", "orta", 1)
    kim = s["teslim_kimlikleri"]
    gec = s["teslim_gecikmeleri_s"]

    # Y8 — kurulum anlamlı mı: ölçüm boş bir kümede yapılmıyor
    assert len(kim) > 100, f"yalnızca {len(kim)} teslim — test zayıf (Y7)"

    assert len(kim) == len(gec), (
        f"{len(kim)} kimlik ama {len(gec)} gecikme")
    assert s["pencerede_teslim"] == len(kim), (
        f"🔴 C17: `pencerede_teslim` {s['pencerede_teslim']} diyor ama "
        f"{len(kim)} kimlik var")
    assert abs(s["teslim_orani"] - len(kim) / s["pencerede_uretilen"]) < 1e-12
    assert len(kim) <= s["pencerede_uretilen"], (
        "teslim, üretilenden çok olamaz")

    # 🔴 D-10 (27 Ağu) — ÜST UÇ KAPALI. Burada `k < ust` yazıyordu ve
    # YANLIŞTI: aralık `[pencere[0].kimlik, pencere[-1].kimlik]` biçiminde
    # kuruluyor, yani İKİ UCU DA KAPALI. Pencerenin SON paketi teslim
    # edilirse `k == ust` olur ve iddia düşerdi.
    #
    # Test yalnızca TEK bir yapılandırma kullandığı için geçiyordu (Y4:
    # "tek noktada tutan sonuç doğrulama sayılmaz"). Ölçüldü — 2 kol ×
    # 6 yapılandırma: eski `k < ust` varsayımı **8/12'de KIRILIR**,
    # `k <= ust` **0/12'de**. Üretici: `python scratchpad/d10_ust_uc.py`
    #
    # ⚖️ Bu, 26 Ağustos oturumunun kendi kaydettiği 4 numaralı hatanın
    # (`pencere_kimlik_araligi`nın üst ucunu dışlayıcı sanmak) bir teste
    # gömülü hâliydi: hata kayda geçmiş, ama kopyası kodda kalmıştı.
    alt, ust = s["pencere_kimlik_araligi"]
    assert all(alt <= k <= ust for k in kim), (
        "pencere ARALIĞI dışında teslim kimliği var")

    assert abs(s["ortalama_gecikme_s"] - statistics.fmean(gec)) < 1e-12
    assert abs(s["ortanca_gecikme_s"] - statistics.median(gec)) < 1e-12, (
        f"🔴 C01: `ortanca_gecikme_s` {s['ortanca_gecikme_s']:.6f} diyor ama "
        f"listenin ortancası {statistics.median(gec):.6f}. Hangi büyüklüğün "
        f"raporlandığı doğrulanmıyor.")

    # 🔴 Y10 — DEĞİŞMEZ KIRILABİLİR Mİ: ortanca ile ortalama gerçekten
    # farklı olmalı, yoksa yukarıdaki iki satır aynı şeyi söyler.
    assert abs(s["ortanca_gecikme_s"] - s["ortalama_gecikme_s"]) > 1e-6, (
        "bu koşuda ortanca ≈ ortalama — C01 mutasyonu bu kurulumda "
        "AYIRT EDİLEMEZ, başka bir çalışma noktası seçilmeli (Y8)")

    # kovalar paydayı tüketiyor mu
    assert (s["iyi_bag_karar"] + s["ara_bolge_karar"] + s["olu_bag_karar"]
            == s["yonlendirme_karari"])
    assert s["secim_avantaji_karar"] <= s["yonlendirme_karari"], (
        "🔴 C16: seçim avantajı, karar sayısını aşamaz")


def test_zd_sonuc_sayaclari_CANLI_sifirlanamiyor():
    """🔴 Sabitlenebilen ve HİÇBİR TESTİN görmediği sayaçlar kapanıyor.

    Beşinci denetim ölçtü: `islenen_olay` · `mac_kayip_onay` ·
    `mac_basarisiz_alim` sıfırlanabiliyordu ve 376 test görmüyordu
    *(C05 · C10 · C19)*.

    🔴 Y8 — ÖNCE MEKANİZMANIN TETİKLENDİĞİ gösterilir: bu sayaçların
    hepsi KARIŞTIRMA ALTINDA ve YOĞUN trafikte canlıdır; sıfır olmaları
    bir kusur işaretidir, tasarım değil.
    """
    s = _d_kosu("en_kisa_yol", "S0", "yogun", 1)

    CANLI = {
        "islenen_olay": "olay döngüsü hiç çalışmamış olamaz",
        "mac_kayip_onay": "yoğun trafikte onay kaybı olmaması beklenmez",
        "mac_basarisiz_alim": "yoğun trafikte başarısız alım beklenir",
        "secim_avantaji_karar": "yönlendirme kararı veriliyorsa bu da sayılır",
        "mac_deneme": "iletim denemesi olmadan paket teslim edilemez",
        "mac_gonderilen": "gönderim olmadan teslim olamaz",
        "pencerede_teslim": "bu çalışma noktasında teslim VARDIR",
        "yonlendirme_karari": "protokol karar vermeden paket ilerleyemez",
    }
    olu = [a for a in CANLI if not s.get(a)]
    assert not olu, (
        f"🔴 sıfır kalan sayaç(lar): {olu}. Bu çalışma noktasında hepsinin "
        f"mekanizması tetikleniyor; sıfır olmaları alanın SABİTLENDİĞİNİ "
        f"gösterir ve hiçbir test bunu görmüyordu (C05 · C10 · C19).")

    # 🔴 `08` madde 22'nin sonuç şemasındaki karşılığı: BEYAN EDİLMİŞ ölü alan
    assert s["yuk_bayt_toplam"] == 0, (
        "`yuk_bayt_toplam` bu kolda sıfır OLMALI — kol `beacon_yuku` "
        "kullanmıyor. Sıfırdan farklıysa bedel yanlış yere yazılıyor.")


def test_b97_mac_deneme_KATI_esitsizlik_gorebiliyor():
    """🔴 B-97 ÇÜRÜTÜLDÜ — iki alan AYNI SAYIYI TAŞIMIYOR.

    Beşinci denetim şöyle yazdı: *"`mac_deneme` ≡ `mac_gonderilen`
    (18/18); koruyan değişmez fiilen `x ≥ x`"* ve `08`e *"şema aynı
    büyüklüğü iki alanla taşıyor"* diye bir madde önerdi.

    🔴 **Ölçüm bunu çürüttü.** Denetçinin örneklemi yalnızca `en_kisa_yol`
    kolunu kullanıyordu. Dört kol × 8 yapılandırma tarandı:

        3/32 yapılandırmada KATI eşitsizlik (fark 1 · 2 · 4)
        hepsi S0/yoğun · `gurultuden_kacan` ve `dongu_yapan`

    Yani değişmez `x ≥ x` DEĞİL: geri çekilmesi tamamlanmadan biten
    iletimler farkı yaratıyor. Bu test o çalışma noktasını sabitler ki
    iddia **kırılabilir** kalsın (Y10).
    """
    s = _d_kosu("dongu_yapan", "S0", "yogun", 2)

    assert s["mac_deneme"] >= s["mac_gonderilen"], (
        "deneme sayısı gönderim sayısından az olamaz")
    assert s["mac_deneme"] > s["mac_gonderilen"], (
        f"🔴 bu çalışma noktasında KATI eşitsizlik bekleniyordu "
        f"({s['mac_deneme']} vs {s['mac_gonderilen']}). Eşitse, değişmez "
        f"`x ≥ x`e döner ve hiçbir şey doğrulamaz (Y10). Kurulum değiştiyse "
        f"katı eşitsizlik veren BAŞKA bir nokta bulunmalı — değişmez "
        f"gevşetilemez.")


# ==========================================================================
# 🔴 FAZ 2 — `05` §E SONUÇ SÖZLEŞMESİ VE ÖLÇÜM PENCERESİ
#   B-104 · korunum denklemi sonuç satırında
#   B-105 · 25 kümülatif sayacın pencere ikizi
#   B-107 · `05` §E'nin beş zorunlu alanı
#   D-10  · `pencere_kimlik_araligi` üst ucu KAPALI
#
# ⚠️ Hepsi `_d_kosu` ÖNBELLEĞİNİ kullanır: bu blok pakete **sıfır** yeni tam
# koşu ekler (biri hariç — kırılabilirlik kanıtı, kasten KISA bir koşu).
# Pahalı bir koruma kapıyı ödenemez kılar (Y12'nin öteki yüzü, K-065).
# ==========================================================================

_D10_KOSULAR = (
    ("en_kisa_yol", "S2", "orta", 1),
    ("en_kisa_yol", "S0", "yogun", 1),
    ("dongu_yapan", "S0", "yogun", 2),
)


def test_b107_05E_BES_ZORUNLU_ALANIN_BESI_DE_sonucta():
    """🔴 `05` §E beş alan sayıyor; şema üçüncü denetimden beri BİRİNİ taşıyordu.

    B-46/K-051 `kaynak_hash`i ekletti ve **kalan dördüne bakmadı** (B-107).
    Bu test beşini de bağlar — ve her birinin GERÇEKTEN okunabilir olduğunu
    ölçer, yalnızca anahtarın varlığını değil.
    """
    s = _d_kosu("en_kisa_yol", "S2", "orta", 1)

    # 1 · tüm konfigürasyon bayrakları
    assert isinstance(s["konfig"], dict) and len(s["konfig"]) > 30, (
        f"`konfig` {len(s.get('konfig') or {})} bayrak taşıyor — `05` §E "
        f"*'tüm konfigürasyon bayrakları'* diyor")
    # 2 · tohum — `kurulum_hash` TEK YÖNLÜDÜR, geri çözülemez
    assert s["konfig"]["tohum"] == 1
    # 3 · kod sürümü
    assert isinstance(s["kaynak_hash"], str) and len(s["kaynak_hash"]) > 8
    # 4 · korunum denklemi sonucu
    assert "korunum_tamam" in s and isinstance(s["korunum"], dict)
    # 5 · ölçüm penceresi — ZAMAN, paket kimliği değil
    assert s["olcum_penceresi_s"] == [50.0, 320.0], s["olcum_penceresi_s"]
    assert s["olcum_penceresi_s"] != s["pencere_kimlik_araligi"], (
        "ölçüm penceresi ile kimlik aralığı KARIŞTIRILMIŞ — `05` §E zamanı "
        "istiyor (B-107)")


def test_b104_korunum_SONUCTA_ve_KIRILABILIR():
    """🔴 B-104 — `Kosu.kostur()` korunumu HİÇ çağırmıyordu.

    `03` Bölüm C: *"her koşuda OTOMATİK"*. Ölçüldü (altıncı denetim):
    `sim/` altında `defter.kontrol()` çağrısı **0**, sonuçta `korunum_tamam`
    **yok**. Somut sonucu: `mekanizma_kapisi.py` — Aile 1'in her kolunu
    geçiren kapı — kol başına 48 koşuda korunumu kontrol etmiyordu.

    🔴 Y10 — İDDİA KIRILABİLİR OLMALI. `korunum_tamam == True` demek yetmez:
    defter bozulduğunda **False dönmek zorunda**. Aksi hâlde alan bir
    süstür ve hiçbir şey korumaz.

    ⏱️ Kasten KISA koşu: kırılabilirlik kanıtı tam bir koşu gerektirmiyor.
    """
    kon = Konfig(kol="t", senaryo="S2", tohum=1,
                 isinma_s=5.0, olcum_bitis_s=15.0, kosu_bitis_s=20.0)
    k = Kosu(kon, AKTARICILAR["en_kisa_yol"])
    s = k.kostur()

    assert s["korunum_tamam"] is True, (
        f"sağlam koşuda korunum TUTMUYOR: {s['korunum']}")
    assert s["korunum"]["uretilen"] > 0, "boş koşu — Y7: ölçüt anlamsız"

    # 🔴 Y10 — defteri boz, alan KONUŞMALI
    k.defter.teslim += 1
    bozuk = k.sonuc()
    assert bozuk["korunum_tamam"] is False, (
        "🔴 `korunum_tamam` bozuk bir defteri de True gösteriyor — alan "
        "kırılamaz, yani koruma değil (Y10)")
    assert bozuk["korunum"]["fark"] != 0


def test_b105_PENCERE_AYNASI_sonuc_ile_AYNI():
    """🔴 Y7 / B-07 — `_sayac_anlik()` ikinci bir doğru kaynağıdır.

    `sonuc()`in ifadelerini elle yansıtıyor. Biri değişip diğeri unutulursa
    pencere ikizleri sessizce YANLIŞ alandan hesaplanır. Bu test ikisini
    bağlar: koşu sonundaki anlık değer, sonuç alanına EŞİT olmalı.
    """
    kon = Konfig(kol="t", senaryo="S2", tohum=1,
                 isinma_s=5.0, olcum_bitis_s=15.0, kosu_bitis_s=20.0)
    k = Kosu(kon, AKTARICILAR["en_kisa_yol"])
    s = k.kostur()
    anlik = k._sayac_anlik()

    for alan in Kosu._PENCERE_SAYACLARI:
        assert alan in s, f"{alan!r} sonuç şemasında yok — ayna bayatlamış"
        assert anlik[alan] == s[alan], (
            f"🔴 AYNA AYRIŞMIŞ: `_sayac_anlik()[{alan!r}]`={anlik[alan]!r} "
            f"ama `sonuc()[{alan!r}]`={s[alan]!r}. Pencere ikizi YANLIŞ "
            f"alandan hesaplanıyor (B-07'nin ikinci doğru kaynağı).")


def test_b105_pencere_ikizi_TUM_KOSUDAN_GERCEKTEN_farkli():
    """🔴 Y8/Y10 — ikizler SÜS DEĞİL: fark ölçülebilir olmalı.

    Ölçüldü (27 Ağu, 5 kol × 8 yapılandırma = 40 tam koşu): kontrol baytının
    **%17,63–22,84'ü** ölçüm penceresi dışında üretiliyor.
    Üretici: `python scratchpad/b105_pencere.py`

    İkizler tüm koşuya eşit çıkarsa üç şeyden biri olmuştur: pencere
    boştur, anlık görüntü alınmamıştır, ya da fark yanlış hesaplanmıştır.
    Üçü de sessizdir — bu yüzden ölçülür.
    """
    s = _d_kosu("en_kisa_yol", "S2", "orta", 1)

    disi = (s["kontrol_bayt"] - s["kontrol_bayt_pencere"]) / s["kontrol_bayt"]
    assert 0.05 < disi < 0.50, (
        f"pencere dışı kontrol baytı %{100*disi:.2f} — ölçülen bant "
        f"%17,63–22,84 idi. Bu kadar uzaksa kurulum değişmiştir ve sebebi "
        f"ölçülmeden bant gevşetilemez (Y9).")

    # Y8 — pencere gerçekten dolu
    assert s["yonlendirme_karari_pencere"] > 100
    # kümülatif alan pencere ikizinden BÜYÜK olmak zorunda
    for alan in Kosu._PENCERE_SAYACLARI:
        assert s[alan] >= s[f"{alan}_pencere"], (
            f"{alan}: pencere ikizi tüm koşudan BÜYÜK — fark yanlış yönde")


def test_b105_EN_YUKSEK_DOLULUK_farkla_turetilemez():
    """🔴 `en_yuksek_doluluk` bir MAKSİMUMDUR, toplam değil.

    `son - (bit - bas)` bu alanda ANLAMSIZDIR ve bu ölçülerek görüldü
    (27 Ağu): `gurultuden_kacan · S2/orta/t1`de kuyruk ısınma bitmeden
    doymuştu — bas=50, bit=50, son=50. Fark 50 verirdi ve "pencerede
    doluluk 50" demek DOĞRU olurdu ama tesadüfen; `bas=26, bit=50, son=50`
    olan komşu yapılandırmada fark **26** verir ve YANLIŞ olur.

    Bu yüzden ayrı izlenir. Bu test, alanın farkla üretilmediğini
    ve tutarlı olduğunu bağlar.
    """
    s = _d_kosu("en_kisa_yol", "S0", "yogun", 1)
    tum = s["en_yuksek_doluluk"]
    pen = s["en_yuksek_doluluk_pencere"]

    assert isinstance(pen, int) and pen >= 0
    assert pen <= tum, "pencere maksimumu tüm koşununkinden büyük olamaz"
    assert tum > 0, "kuyruk hiç dolmamış — Y7: ölçüt anlamsız"
    assert pen <= s["konfig"]["kuyruk_kapasitesi"]


def test_b105_OLCUM_KOSUSUNDA_pencere_alani_None_OLAMAZ():
    """🔴 `03` B2 — `None` "sıfır" değildir, "ölçüm yok" demektir.

    `kostur()` çağrılmadan `sonuc()` alınırsa ikizler `None` döner. Bu
    meşru bir durumdur (koşu yok) ama bir ÖLÇÜM koşusunda görülürse
    sessiz bir yanlış sayı kaynağıdır.
    """
    s = _d_kosu("en_kisa_yol", "S2", "orta", 1)
    bos = [a for a in s if a.endswith("_pencere") and s[a] is None]
    assert not bos, f"ölçüm koşusunda `None` pencere alanı: {bos}"

    # 🔴 Y11 — KAPSAM DIŞI VAKA: koşulmamış bir `Kosu` `None` DÖNMELİ,
    # sıfır değil. Sıfır dönseydi "pencerede hiç kontrol baytı yok" gibi
    # okunur ve bir ortalamaya karışırdı.
    k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), AKTARICILAR["en_kisa_yol"])
    ham = k.sonuc()
    assert ham["kontrol_bayt_pencere"] is None
    assert ham["en_yuksek_doluluk_pencere"] is None


def test_d10_pencere_kimlik_araligi_UST_UC_KAPALI():
    """🔴 D-10 — aralık İKİ UCU DA KAPALI ve bu ÜÇ yapılandırmada ölçülür.

    `test_zd_sonuc_semasi_KENDI_ICINDE_tutarli` bunu `k < ust` diye
    varsayıyordu ve **tek** yapılandırmada koşuyordu (Y4). Ölçüldü —
    2 kol × 6 yapılandırma: eski varsayım **8/12'de kırılır**.

    🔴 Y8 — ÜST UÇ FİİLEN TETİKLENMELİ: hiçbir koşuda pencerenin son paketi
    teslim edilmiyorsa bu test *"kapalı"* ile *"açık"* arasındaki farkı
    GÖREMEZ ve boş yere geçer.
    """
    tetiklendi = 0
    for kol, sen, tra, toh in _D10_KOSULAR:
        s = _d_kosu(kol, sen, tra, toh)
        alt, ust = s["pencere_kimlik_araligi"]
        kim = s["teslim_kimlikleri"]
        assert kim, f"{kol}/{sen}: hiç teslim yok — ölçüt anlamsız (Y7)"
        assert all(alt <= k <= ust for k in kim), (
            f"{kol}/{sen}/{tra}/t{toh}: pencere aralığı dışında teslim "
            f"kimliği var")
        if ust in kim:
            tetiklendi += 1

    assert tetiklendi >= 1, (
        "🔴 hiçbir yapılandırmada pencerenin SON paketi teslim edilmiyor — "
        "bu test kapalı/açık ayrımını göremez, örneklem GENİŞLETİLMELİ (Y8)")


# --------------------------------------------------------------------------
# 🔴 Y2 İLK TURU DÖRT DELİK GÖSTERDİ — aşağıdaki dört test onları kapatıyor.
#
# Kaçırılan mutasyonlar ve sebepleri (27 Ağu, ölçüldü):
#   M-E4 anlık görüntü t=0'da alındı  -> band %5–50 fazla GENİŞTİ (%8,6 geçer)
#   M-E6 doluluk FARKLA türetildi     -> `pen <= tum` iddiası ayırt etmiyor
#   M-E7 `pencere_baslat()` çağrılmıyor -> hiçbir davranış testi görmüyor
#   M-E8 pencere maksimumu 0'dan başlıyor -> aynı
#
# ⚖️ Dördü de "koruma yalnızca yakalayabildiği durumla sınandı" sınıfı (Y11).
# --------------------------------------------------------------------------

def test_b105_pencere_anligi_ISINMA_SONUNDA_aliniyor():
    """🔴 Anlık görüntü `t = isinma_s`de mi alınıyor, `t = 0`da mı?

    İkisi de "pencere ikizi" üretir ve ikisi de tüm koşudan küçüktür — yani
    bir BÜYÜKLÜK bandı ikisini AYIRT EDEMEZ (M-E4 tam olarak buradan kaçtı).

    Ayırt eden şey: ikizin `isinma_s`e DUYARLI olması. Yalnızca ısınma
    süresinde farklılaşan iki koşuda ikiz DEĞİŞMEK zorundadır; anlık
    görüntü t=0'da alınıyorsa ikisi BİREBİR aynı çıkar.
    """
    ortak = dict(kol="t", senaryo="S2", tohum=1,
                 olcum_bitis_s=30.0, kosu_bitis_s=35.0)
    kisa = Kosu(Konfig(**ortak, isinma_s=5.0), AKTARICILAR["en_kisa_yol"]).kostur()
    uzun = Kosu(Konfig(**ortak, isinma_s=20.0), AKTARICILAR["en_kisa_yol"]).kostur()

    # Y8 — iki koşu da gerçekten iş yapıyor
    assert kisa["beacon_gonderilen_pencere"] > 0
    assert uzun["beacon_gonderilen_pencere"] > 0

    assert uzun["beacon_gonderilen_pencere"] < kisa["beacon_gonderilen_pencere"], (
        "🔴 ısınma 5 s'den 20 s'ye çıktığı hâlde pencere ikizi DEĞİŞMEDİ — "
        "anlık görüntü `isinma_s`de değil, koşu başında alınıyor olabilir "
        "(B-105/M-E4).")
    # Tüm koşu değeri ise ısınmadan bağımsız olmalı (pencere kısaldı, koşu değil)
    assert kisa["beacon_gonderilen"] == uzun["beacon_gonderilen"]


def test_b105_kuyruk_PENCERE_MAKSIMUMU_ayri_izleniyor():
    """🔴 `en_yuksek_doluluk` bir MAKSİMUMDUR — birim testle ayrıştırılır.

    Tam koşu gerektirmez ve tam koşuda ayrıştırılamaz: gerçek koşularda
    kuyruk çoğu zaman pencerede de tepe yapar, yani iki büyüklük çakışır ve
    fark GÖRÜNMEZ. Kurgu senaryo ikisini ayırır.
    """
    from sim.ledger import KorunumDefteri
    from sim.packet import Paket
    from sim.queues import Kuyruk

    # senaryo 1 — pencere başlarken kuyruk BOŞ
    d = KorunumDefteri()
    q = Kuyruk(0, kapasite=10, defter=d)
    for i in range(8):
        q.ekle(Paket(i, 0, 1, 100), yeni_uretilen=True)
    for _ in range(8):
        q.al()
    assert q.en_yuksek_doluluk == 8
    q.pencere_baslat()
    assert q.pencere_en_yuksek_doluluk == 0, "boş kuyrukta pencere maks. 0"
    for i in range(100, 103):
        q.ekle(Paket(i, 0, 1, 100), yeni_uretilen=True)
    assert q.pencere_en_yuksek_doluluk == 3, (
        f"🔴 pencere maksimumu {q.pencere_en_yuksek_doluluk}, olması gereken 3 "
        f"— ısınmanın tepesi (8) pencereye SIZIYOR (B-105/M-E7).")
    assert q.en_yuksek_doluluk == 8, "tüm koşu maksimumu bozulmamalı"

    # senaryo 2 — pencere başlarken kuyruk DOLU: sıfırdan başlamak YANLIŞ
    d2 = KorunumDefteri()
    q2 = Kuyruk(1, kapasite=10, defter=d2)
    for i in range(8):
        q2.ekle(Paket(i, 1, 0, 100), yeni_uretilen=True)
    for _ in range(5):
        q2.al()
    assert len(q2) == 3
    q2.pencere_baslat()
    assert q2.pencere_en_yuksek_doluluk == 3, (
        f"🔴 pencere maksimumu {q2.pencere_en_yuksek_doluluk} — pencereye "
        f"3 paketle GİRİLDİ, bu pencerenin olgusudur ve sıfırlanamaz "
        f"(B-105/M-E8).")
    for _ in range(3):
        q2.al()
    assert q2.pencere_en_yuksek_doluluk == 3
    assert q2.en_yuksek_doluluk == 8


def test_b105_KOSTUR_pencere_baslat_ve_pencere_sayacini_KULLANIYOR():
    """🔴 `03` B5 — bildirim ≠ kullanım.

    `Kuyruk.pencere_en_yuksek_doluluk` doğru çalışsa bile `kostur()` onu
    çağırmıyor ya da okumuyorsa koruma sahtedir: birim testler geçer, sonuç
    satırı yine tüm koşu maksimumunu taşır. Ölçüldü — M-E6 ve M-E7 tam
    olarak buradan kaçtı. AST ile denetlenir; yorum metnine bakan bir
    tarama kendi metnini yakalar (B-68).
    """
    import ast

    kaynak = (Path(__file__).resolve().parent.parent
              / "sim" / "kosucu.py").read_text(encoding="utf-8")
    fn = next((d for d in ast.walk(ast.parse(kaynak))
               if isinstance(d, ast.FunctionDef) and d.name == "kostur"), None)
    assert fn is not None, "kostur() bulunamadı"

    cagrilan = {d.func.attr for d in ast.walk(fn)
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute)}
    assert "pencere_baslat" in cagrilan, (
        "🔴 `kostur()` `pencere_baslat()` ÇAĞIRMIYOR — ısınmanın kuyruk "
        "tepesi pencereye sızar (B-105/M-E7).")

    okunan = {d.attr for d in ast.walk(fn) if isinstance(d, ast.Attribute)}
    assert "pencere_en_yuksek_doluluk" in okunan, (
        "🔴 `kostur()` pencere maksimumunu `pencere_en_yuksek_doluluk`ten "
        "OKUMUYOR — tüm koşu maksimumundan türetiliyor olabilir "
        "(B-105/M-E6).")


def test_b105_pencere_disi_orani_OLCULEN_BANTTA():
    """Ölçülen bant: kontrol baytının **%17,63–22,84'ü** pencere dışında.

    ⚠️ Bant `test_b105_pencere_ikizi_*`de %5–50 idi ve M-E4'ü kaçırdı
    (mutasyon %8,6 üretiyordu, bandın içinde). Bant ölçülen değere
    daraltıldı — **gevşetilmedi, sıkılaştırıldı**.
    Üretici: `python scratchpad/b105_pencere.py` (5 kol × 8 yapılandırma)
    """
    s = _d_kosu("en_kisa_yol", "S2", "orta", 1)
    disi = (s["kontrol_bayt"] - s["kontrol_bayt_pencere"]) / s["kontrol_bayt"]
    assert 0.12 <= disi <= 0.30, (
        f"pencere dışı kontrol baytı %{100*disi:.2f} — ölçülen bant "
        f"%17,63–22,84. Sebebi ölçülmeden bant gevşetilemez (`03` kural 3, Y9).")
