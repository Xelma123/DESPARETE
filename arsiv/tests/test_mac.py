"""
MAC katmanı testleri.

Bu katman Li replikasyonunun taşıyıcısı. Buradaki sessiz bir hata,
replikasyonun tutmasına rağmen sonuçları bozabilir.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.config import Konfig  # noqa: E402
from sim.events import OlayKuyrugu  # noqa: E402
from sim.mac import Iletim, KanalErisimi  # noqa: E402
from sim.packet import Paket  # noqa: E402
from sim.radio import Karistirici, Radyo  # noqa: E402
from sim.rng import Akislar  # noqa: E402
from sim.topology import Topoloji  # noqa: E402


def duzenek(konumlar, tohum=1, **kw):
    kon = Konfig(kol="mac", senaryo=kw.pop("senaryo", "S0"), tohum=tohum,
                 dugum_sayisi=len(konumlar), **kw)
    topo = Topoloji(konumlar=tuple(konumlar),
                    iletim_menzili_m=kon.iletim_menzili_m,
                    girisim_menzili_m=kon.girisim_menzili_m)
    ak = Akislar(tohum)
    ol = OlayKuyrugu()
    kj = Karistirici.senaryodan(kon, ak)
    return kon, topo, ol, KanalErisimi(kon, topo, Radyo.kur(kon), ol, kj, ak)


def paket(bayt=1024, hedef=1):
    return Paket(kimlik=0, kaynak=0, hedef=hedef, bayt=bayt, ttl=32)


# ==========================================================================
# Çerçeve süreleri — AİLE 0 / K3 analitik kontrolü
# ==========================================================================

def test_cerceve_suresi_onbelge_arti_yuk():
    kon = Konfig(kol="t")
    assert kon.cerceve_suresi_s(1024) == pytest.approx(
        kon.onbelge_s + 1024 * 8 / kon.bit_hizi_bps)
    assert kon.onay_suresi_s == pytest.approx(
        kon.onbelge_s + 14 * 8 / kon.bit_hizi_bps)
    assert kon.difs_s == pytest.approx(kon.sifs_s + 2 * kon.slot_s)


def test_tek_atlama_verimi_analitik_hesapla_uyusuyor():
    """⭐ Elle hesap:  DIFS + ort.geri çekilme + önbelge+veri + SIFS + onay

    1500 B, 1 Mbit/s, CW=31 → ort. 15,5 slot:
        50 + 310 + 12192 + 10 + 304 = 12866 µs → 12000 bit / 12866 µs
        ≈ 933 kbps
    Bu test kırılırsa MAC zamanlaması bozulmuş demektir.
    """
    kon = Konfig(kol="t", paket_bayt=1500)
    beklenen_us = (
        kon.difs_s + (kon.cw_min / 2) * kon.slot_s
        + kon.cerceve_suresi_s(1500) + kon.sifs_s + kon.onay_suresi_s
    ) * 1e6
    assert beklenen_us == pytest.approx(12866.0, abs=5.0)
    verim = 1500 * 8 / (beklenen_us * 1e-6)
    assert verim == pytest.approx(933_000, rel=0.01)


# ==========================================================================
# Taşıyıcı dinleme
# ==========================================================================

def test_menzil_disindaki_dugum_kanali_bos_goruyor():
    """1000 m ayrık iki düğüm birbirini duymaz (girişim menzili 603 m)."""
    kon, topo, ol, mac = duzenek([(0, 0), (1000, 0)])
    mac.gonder(0, paket(hedef=1), 1)
    ol.kostur(0.001)
    assert mac.kanal_mesgul(1) is False


def test_girisim_menzilindeki_dugum_kanali_mesgul_goruyor():
    """560 m ayrık iki düğüm iletim menzilinde DEĞİL ama girişim menzilinde."""
    kon, topo, ol, mac = duzenek([(0, 0), (280, 0), (560, 0)])
    assert topo.iletim_menzilinde_mi(0, 2) is False
    assert topo.girisim_menzilinde_mi(0, 2) is True
    mac.gonder(0, paket(), 1)
    ol.kostur(0.002)
    assert mac.kanal_mesgul(2) is True


def test_tasiyici_dinleme_menzili_girisim_menziline_esit():
    """Ayrı bir eşik yok — üçüncü bir 'doğru' kaynağı doğmasın diye."""
    kon, topo, ol, mac = duzenek([(0, 0), (600, 0), (610, 0)])
    assert 0 in mac.cs_komsu[1]      # 600 m < 603 m
    assert 0 not in mac.cs_komsu[2]  # 610 m > 603 m


def test_karistirici_tasiyici_dinlemeyi_tetiklemiyor():
    """🔴 MODELLEME KARARI 2 — bu kırılırsa karar sessizce değişmiş demektir.

    Karıştırıcı yalnızca gürültüye girer. Girseydi düğümler kanalı sürekli
    meşgul sanar ve hiç konuşmazdı.
    """
    kon, topo, ol, mac = duzenek([(500, 500), (700, 500)], senaryo="S2")
    assert mac.karistirici is not None
    assert mac.kanal_mesgul(0) is False
    assert mac.kanal_mesgul(1) is False


# ==========================================================================
# Yarı çift yönlü ve gizli terminal
# ==========================================================================

def test_gonderirken_alamaz():
    """Yarı çift yönlü radyo: aynı anda gönderip alamaz.

    ⚠️ İlk yazımı YANLIŞTI: iki düğüme aynı anda gönderim istendiğinde
    taşıyıcı dinleme onları SIRAYA DİZİYOR, yani çakışma hiç olmuyordu ve
    ikisi de başarılı oluyordu. Bu, MAC'in doğru çalıştığının kanıtıydı —
    testin yanlış olduğunun değil kodun.

    Gerçekten eşzamanlı iletim için geri çekilme penceresi sıfırlanır:
    ikisi de aynı anda DIFS bitirip aynı anda gönderir.
    """
    kon, topo, ol, mac = duzenek([(0, 0), (200, 0)], cw_min=0,
                                 yeniden_deneme_siniri=0)
    tamam = []
    mac.alim_gerceklesti = lambda p, g, a: tamam.append((g, "ok"))
    mac.iletim_basarisiz = lambda p, g, h: tamam.append((g, "X"))
    mac.gonder(0, paket(hedef=1), 1)
    mac.gonder(1, paket(hedef=0), 0)
    ol.kostur(0.05)
    # Yeniden deneme kapali: ikisi de ilk denemede duser.
    assert [x[1] for x in tamam] == ["X", "X"], tamam
    assert mac.basarisiz_alim == 2


def test_eszamanli_olmayan_iletim_basarili():
    """Kontrol kolu: sıraya girdiklerinde ikisi de başarılı olmalı.

    Bu kol olmadan üstteki testin 'her şeyi bozduğu' ile
    'doğru şeyi bozduğu' ayırt edilemez.
    """
    kon, topo, ol, mac = duzenek([(0, 0), (200, 0)])
    tamam = []
    mac.alim_gerceklesti = lambda p, g, a: tamam.append((g, "ok"))
    mac.iletim_basarisiz = lambda p, g, h: tamam.append((g, "X"))
    mac.gonder(0, paket(hedef=1), 1)
    mac.gonder(1, paket(hedef=0), 0)
    ol.kostur(1.0)
    assert [x[1] for x in tamam] == ["ok", "ok"], tamam


def test_gizli_terminal_carpisma_uretiyor():
    """🔴 Li replikasyonunun temeli.

    Düzenek:  0 --280-- 1 --280-- 2 --280-- 3
    0 ile 3 arası 840 m > 603 m → birbirlerini DUYMAZLAR.
    Ama 3, 1'e 560 m uzakta → 1'in alımını BOZAR.
    Bu geometri yoksa 1/7 asla çıkmaz.
    """
    kon, topo, ol, mac = duzenek([(0, 0), (280, 0), (560, 0), (840, 0)])
    assert topo.girisim_menzilinde_mi(0, 3) is False   # duymuyorlar
    assert topo.girisim_menzilinde_mi(3, 1) is True    # ama bozuyor
    assert 3 not in mac.cs_komsu[0]
    assert 3 in mac.cs_komsu[1]


# ==========================================================================
# Geri çekilme ve yeniden deneme
# ==========================================================================

def test_yeniden_deneme_siniri_sonunda_dusuyor():
    """Alıcı menzil dışındaysa iletim tekrar tekrar başarısız olup düşmeli."""
    kon, topo, ol, mac = duzenek([(0, 0), (5000, 0)], yeniden_deneme_siniri=2)
    basarisiz = []
    mac.iletim_basarisiz = lambda p, g, h: basarisiz.append(g)
    mac.gonder(0, paket(hedef=1), 1)
    ol.kostur(5.0)
    assert basarisiz == [0]
    assert mac.mac[0].durum == "bos"
    assert mac.mac[0].paket is None


def test_cw_ikili_ustel_buyuyor():
    kon, topo, ol, mac = duzenek([(0, 0), (5000, 0)], yeniden_deneme_siniri=3)
    mac.iletim_basarisiz = lambda p, g, h: None
    mac.gonder(0, paket(hedef=1), 1)
    cw_gecmisi = []
    for _ in range(40):
        ol.kostur(ol.simdi + 0.05)
        cw_gecmisi.append(mac.mac[0].cw)
    assert max(cw_gecmisi) > kon.cw_min
    assert max(cw_gecmisi) <= kon.cw_max


def test_mesgulken_gonderim_hata_veriyor():
    """Sessizce yutulursa paket kaybolur ve korunum kırılır."""
    kon, topo, ol, mac = duzenek([(0, 0), (200, 0)])
    mac.gonder(0, paket(hedef=1), 1)
    with pytest.raises(RuntimeError, match="meşgulken"):
        mac.gonder(0, paket(hedef=1), 1)


# ==========================================================================
# Belirlenimcilik
# ==========================================================================

def test_ayni_tohum_ayni_sonuc():
    def kos():
        kon, topo, ol, mac = duzenek([(0, 0), (270, 0), (540, 0)], tohum=7)
        olay = []
        mac.alim_gerceklesti = lambda p, g, a: olay.append(("ok", g, a, ol.simdi))
        mac.iletim_basarisiz = lambda p, g, h: olay.append(("x", g, ol.simdi))
        mac.gonder(0, paket(hedef=2), 1)
        ol.kostur(0.5)
        return olay
    assert kos() == kos()


def test_karistirici_alimi_bozuyor():
    """S2'de karıştırıcının merkezindeki bir bağ, S0'dakinden kötü olmalı."""
    sonuc = {}
    for senaryo in ("S0", "S2"):
        basarili = 0
        for tohum in range(1, 21):
            kon, topo, ol, mac = duzenek([(500, 500), (500, 760)],
                                         tohum=tohum, senaryo=senaryo,
                                         yeniden_deneme_siniri=0)
            mac.alim_gerceklesti = lambda p, g, a: sonuc.__setitem__("ok", True)
            sonuc.pop("ok", None)
            mac.gonder(0, paket(hedef=1), 1)
            ol.kostur(0.5)
            basarili += sonuc.get("ok", False)
        sonuc[senaryo] = basarili
    assert sonuc["S2"] < sonuc["S0"], sonuc


def test_yari_cift_yonlu_sinr_den_bagimsiz_calisiyor():
    """🔴 M4 MUTASYON BOŞLUĞU — 19 Ağustos 2026'da eklendi.

    Mutasyon paketi, yarı çift yönlü kontrolü kaldırıldığında HİÇBİR testin
    kırılmadığını gösterdi. Sebep: mevcut test iki düğümü eşit uzaklığa
    koyuyordu ve orada SINR zaten paketi öldürüyordu — yani test yarı çift
    yönlülüğü değil ÇAKIŞMAYI ölçüyormuş.

    Bu test durumu yalıtır:
        A --250m-- B  ................. C (çok uzak)
        B, C'ye gönderirken A'dan alıyor.

    B'nin kendi iletimi B'deki girişime GİRMEZ (kod bunu bilerek dışlar),
    dolayısıyla SINR temizdir. Alım YİNE DE başarısız olmalı — çünkü telsiz
    yarı çift yönlüdür ve aynı anda hem gönderip hem alamaz.
    """
    kon, topo, ol, mac = duzenek([(0, 0), (250, 0), (250, 4000)])

    # SINR'in temiz olduğunu ÖNCE göster: B, C'ye göndermiyorken A'dan alım
    temiz = Iletim(0, 1, 0.0, kon.cerceve_suresi_s(1024), "veri", paket())
    mac.aktif = [temiz]
    per_temiz = mac.alim_per(temiz)
    assert per_temiz is not None and per_temiz < 0.5, (
        f"kurulum hatalı: girişimsiz PER {per_temiz} — test ayırt edici değil"
    )

    # Şimdi B aynı anda C'ye gönderiyor
    mac.gonderim_araligi[1] = (0.0, kon.cerceve_suresi_s(1024))
    b_iletimi = Iletim(1, 2, 0.0, kon.cerceve_suresi_s(1024), "veri", paket())
    mac.aktif = [temiz, b_iletimi]

    assert mac.alim_per(temiz) is None, (
        "B gönderirken A'dan alım başarılı sayıldı — yarı çift yönlü yok"
    )
    assert mac._alim_basarili_mi(temiz) is False


# ==========================================================================
# 🔴 CCA — aynı-slot çarpışması (M3 mutasyonunun BEKLENEN yakalayıcısı)
# ==========================================================================

def test_cca_ayni_slot_carpismasini_uretiyor(monkeypatch):
    """🔴 `cca_s`in TEK gerekçesini doğrudan sınar.

    `config.py` şunu yazıyor: *"SIFIR OLAMAZ: sıfır olsaydı bir düğüm
    başkasının iletimini başlama anında görürdü ve geri sayımı aynı slotta
    biten iki düğüm ASLA çarpışmazdı. Aynı-slot çarpışması 802.11'in temel
    çakışma kaynağıdır; onu silmek verimi sessizce şişirir."*

    🔴 BU GEREKÇENİN KOD KARŞILIĞI SINANMIYORDU. `mutasyon_paketi.py`nin M3
    mutasyonu (`cca_s = 0.0`) "yakalandı" sayılıyordu — ama onu kıran test
    yarı çift yönlü testiydi, yani BAŞKA bir sözleşme. B-21'in `beklenen_test`
    kontrolü bu boşluğu açığa çıkardı.

    KURULUM — çarpışma zorlanır, tesadüfe bırakılmaz:
      · 0 ve 1 birbirinin taşıyıcı dinleme menzilinde
      · geri çekilme çekimi sabitlenir → ikisi de AYNI anda biter
      · cca_s > 0 iken 1, 0'ın iletimini o anda göremez → ikisi de gönderir
      · cca_s = 0 iken 1 meşgul görür ve susar → çarpışma OLMAZ
    """
    kon, topo, ol, mac = duzenek([(0.0, 0.0), (50.0, 0.0), (150.0, 0.0)])

    # ⚠️ `cca_s > 0` ön koşulu BİLEREK assert edilmiyor: mutasyon testi o
    # satırda kırılsaydı, kırılan şey DAVRANIŞ değil ön koşul olurdu ve
    # çarpışma yolunun tetiklendiğini göstermezdi (Y8).

    # Aynı slotta bitsinler: geri çekilme çekimi sabit
    monkeypatch.setattr(mac._rnd, "randint", lambda a, b: 3)

    mac.gonder(0, paket(hedef=2), 2)
    mac.gonder(1, paket(hedef=2), 2)
    ol.kostur(0.001)                      # her iki geri sayım da bitmiş olur

    esZamanli = [il for il in mac.aktif if il.tur == "veri"]
    assert len(esZamanli) == 2, (
        f"aynı-slot çarpışması OLUŞMADI: {len(esZamanli)} eşzamanlı iletim. "
        f"cca_s={kon.cca_s} — sıfırlanmışsa 802.11'in temel çakışma kaynağı "
        f"yok olmuş ve verim sessizce şişmiş demektir."
    )
    # Y8 — bozulan yolun gerçekten çalıştığını göster: aralıklar ÖRTÜŞÜYOR
    a, b = esZamanli
    assert a.baslangic_s < b.bitis_s and b.baslangic_s < a.bitis_s


# ==========================================================================
# 🔴 B-23 — karıştırıcının ALDIĞI güç için MUTLAK analitik kontrol
# ==========================================================================

def test_b23_karistirici_alinan_gucu_kapali_formla_birebir():
    """🔴 B-23 — karıştırıcı gücünü 2'yle çarpınca 216 testin 216'sı geçiyordu.

    Ç3'ün analitik kontrolleri yol kaybını, gürültü tabanını, çerçeve
    sürelerini ve menzil sınırını kapalı formla doğruluyor — ama
    KARIŞTIRICININ ALICIDA YARATTIĞI GÜCÜ hiçbiri doğrulamıyordu. Oysa
    S1–S5 arasındaki bütün farkı üreten büyüklük odur.

    Mevcut testlerin hepsi GÖRELİ: "karıştırıcı etkili mi", "mesafeyle
    azalıyor mu", "S2 ile S4 ortalaması eşit mi". Hepsi, güç tekdüze bir
    çarpanla kayarsa sessiz kalır. (`03` B3: metrik gerçekten onu mu ölçüyor?)
    """
    kon = Konfig(kol="t", senaryo="S2")
    kj = Karistirici.senaryodan(kon, Akislar(1))
    jx, jy = kon.karistirici_merkez

    for d_m in (100.0, 300.0, 603.0):
        nokta = (jx + d_m, jy)
        olculen = kj.alinan_guc_w(nokta, 0.0)

        # Kapalı form: P_rx = P_tx / 10^(PL/10),  PL = 20log10(4πf/c) + 10α log10(d)
        import math as _m
        c = 299_792_458.0
        pl_1m = 20.0 * _m.log10(4.0 * _m.pi * kon.frekans_hz / c)
        pl_db = pl_1m + 10.0 * kon.yol_kaybi_usteli * _m.log10(d_m)
        p_tx_w = 10.0 ** (kon.karistirici_guc_dbm / 10.0) / 1000.0
        beklenen = p_tx_w / (10.0 ** (pl_db / 10.0))

        assert olculen == pytest.approx(beklenen, rel=1e-9, abs=0.0), (
            f"{d_m} m: ölçülen {olculen:.6e} W, kapalı form {beklenen:.6e} W"
        )


# ==========================================================================
# 🔴 B-51 — DARBELİ KARIŞTIRICININ PARÇA SINIRLARI
#
# Üçüncü bağımsız denetim: `_parca_sinirlari`'ndaki faz işaretini ters
# çeviren mutasyon (U11) **284/284 testten sağ çıktı** ve 8/48 koşuda
# davranışı değiştirdi (bütün S3/S4 darbeli koşular).
#
# Ç3.2 *(parça parça hesap = tek parça)* tam olarak SABİT girişimde koşuyor;
# darbe fazının DOĞRU YERDE kesildiğini sınayan hiçbir test yoktu.
# H1.3 (darbeli ↔ sabit, eşit ortalama güç) bu hesaba dayanıyor.
# ==========================================================================

def test_b51_parca_sinirlari_acik_mi_GECISLERIYLE_ayni():
    """Parça sınırları, karıştırıcının açılıp kapandığı anlar olmalı.

    BAĞIMSIZ HESAP: `acik_mi()` ayrı bir fonksiyondur ve fazı `+` işaretiyle
    kullanır; `_parca_sinirlari` `-` ile. İkisi tutarlıysa, **iki ardışık
    sınır arasında `acik_mi` SABİT kalır.** İşaret ters çevrilirse sınırlar
    yanlış yere düşer ve aralık İÇİNDE değişir.
    """
    kon, topo, ol, mac = duzenek([(0, 0), (250, 0)], senaryo="S4")
    kj = mac.karistirici
    assert kj is not None and kj.darbeli, "S4 darbeli değil — kurulum yanlış"

    bas = 1.0
    il = Iletim(0, 1, bas, bas + 3 * kj.periyot_s, "veri")
    mac.aktif = [il]
    sinirlar = mac._parca_sinirlari(il)

    # Y8 — darbe dalı fiilen sınır üretmeli, yoksa test bir şey ölçmüyor
    assert len(sinirlar) > 2, (
        f"yalnızca {len(sinirlar)} sınır — darbe dalı çalışmamış")

    for a, b in zip(sinirlar, sinirlar[1:]):
        degerler = {kj.acik_mi(a + (b - a) * kesir)
                    for kesir in (0.25, 0.5, 0.75)}
        assert len(degerler) == 1, (
            f"[{a:.6f}, {b:.6f}] aralığında karıştırıcı durumu DEĞİŞİYOR "
            f"({degerler}) — parça sınırı yanlış yerde. Faz işareti "
            f"`acik_mi` ile tutarsız olabilir.")

    # Ve sınırlar gerçekten GEÇİŞ noktası olmalı: iç sınırların iki yanı farklı
    eps = kj.periyot_s * 1e-6
    ic = [t for t in sinirlar if il.baslangic_s < t < il.bitis_s]
    assert ic, "iç sınır yok — kurulum darbe geçişi kapsamıyor"
    for t in ic:
        assert kj.acik_mi(t - eps) != kj.acik_mi(t + eps), (
            f"t={t:.6f} bir sınır ama karıştırıcı durumu değişmiyor")


# ==========================================================================
# 🔴 B-62 — KOPYA ALIMLARIN BAYTLARI
#
# U13 (kopya alım baytı sayılmıyor) **284/284 testten sağ çıktı**; matriste
# eşdeğer görünüyordu çünkü `alinan_bayt`ın tüketicisi yok.
# `test_b01_*` yalnızca GÖNDERİLEN tarafa değişmez kuruyordu.
# ==========================================================================

class _KayitliBayt(list):
    """Bayt kredilerini dışarıdan gözleyen liste — üretici ifadeyi tekrar etmez."""

    def __init__(self, n):
        super().__init__([0] * n)
        self.krediler: list[int] = []

    def __setitem__(self, i, deger):
        fark = deger - self[i]
        if fark:
            self.krediler.append(fark)
        super().__setitem__(i, deger)


def test_b62_kopya_alimlarin_baytlari_da_sayiliyor():
    """Kopya alınan bir paketin baytı da düğümün alınan sayacına girmeli.

    BAĞIMSIZ HESAP: her bayt kredisi dışarıdan gözleniyor ve BÜYÜKLÜĞÜNE
    göre sınıflanıyor *(veri 1024 · beacon 32 · onay 14 — üçü ayrık)*.
    Veri boyutlu kredi sayısı, **kabul edilen + kopya** alım sayısına eşit
    olmalı; kopyalar sayılmazsa sayı eksik kalır.
    """
    from sim.config import Konfig as _K
    from sim.kosucu import Kosu
    from dogrulama.aktaricilar import en_kisa_yol

    kon = _K(kol="t", senaryo="S2", trafik="yogun", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    k.mac.dugum_alinan_bayt = _KayitliBayt(kon.dugum_sayisi)

    kabul = {"n": 0}
    asil = k.mac.alim_gerceklesti

    def izle(paket, gonderen, alan):
        kabul["n"] += 1
        return asil(paket, gonderen, alan)

    k.mac.alim_gerceklesti = izle
    s = k.kostur()

    # Y8 — kopya yolu fiilen tetiklenmeli
    assert s["mac_kopya_alim"] > 0, "hiç kopya alım yok — test bir şey ölçmüyor"

    veri_kredi = sum(1 for f in k.mac.dugum_alinan_bayt.krediler
                     if f == kon.paket_bayt)
    assert veri_kredi == kabul["n"] + s["mac_kopya_alim"], (
        f"veri boyutlu kredi {veri_kredi}, beklenen "
        f"{kabul['n']} kabul + {s['mac_kopya_alim']} kopya = "
        f"{kabul['n'] + s['mac_kopya_alim']}. Kopya alımların baytı "
        f"sayılmıyor olabilir.")


# ==========================================================================
# 🔴 B-70 (K-056) — ALICI GERÇEK ÇERÇEVE BOYUTUNU KREDİLENİR
#
# 57 baytlık (32+25) bir beacon için alıcı **32 bayt** görüyordu; bir koşuda
# 1 668 050 bayt kredilenmiyordu. Veri ve onay yollarında böyle bir asimetri
# YOK — bu, B-47 kanalının getirdiği tutarsızlıktı.
# `alinan_bayt` bir GÖZLEM alanıdır: yük taşıyan bir kolun komşuları
# aldıklarını olduğundan AZ görürdü.
# ==========================================================================

def test_b70_alici_GERCEK_cerceve_boyutunu_kredileniyor():
    from sim.kosucu import Kosu

    kon = Konfig(kol="t", senaryo="S0", tohum=1)

    def fab(k):
        def s(g):
            return min(x.dugum for x in g.komsular) if g.komsular else None
        s.beacon_yuku = lambda d: {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        return s

    k = Kosu(kon, fab)
    krediler = []
    asil = k.mac._yayin_bitti

    def izle(dugum, il):
        n0 = k.mac.alinan_yayin
        a0 = sum(k.mac.dugum_alinan_bayt)
        asil(dugum, il)
        if k.mac.alinan_yayin > n0:
            krediler.append((sum(k.mac.dugum_alinan_bayt) - a0)
                            / (k.mac.alinan_yayin - n0))

    k.mac._yayin_bitti = izle
    s = k.kostur()

    # Y8 — yayın alım yolu fiilen tetiklenmeli
    assert len(krediler) > 100, f"yalnızca {len(krediler)} yayın alımı"

    yuk = s["yuk_bayt_toplam"] // s["beacon_gonderilen"]
    assert yuk > 0, "yük taşınmıyor — kurulum varsayımı tutmuyor"
    beklenen = kon.beacon_bayt + yuk
    assert all(abs(x - beklenen) < 1e-9 for x in krediler), (
        f"alıcı başına kredi {sorted(set(krediler))[:3]}, çerçeve "
        f"{kon.beacon_bayt} + {yuk} = {beklenen} bayt")


def test_b70_YUKSUZ_kolda_kredi_DEGISMIYOR():
    """Kontrol kolu: kancasız protokolde alıcı kredisi eskisi gibi."""
    from sim.kosucu import Kosu
    from dogrulama.aktaricilar import en_kisa_yol

    kon = Konfig(kol="t", senaryo="S0", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    krediler = []
    asil = k.mac._yayin_bitti

    def izle(dugum, il):
        n0 = k.mac.alinan_yayin
        a0 = sum(k.mac.dugum_alinan_bayt)
        asil(dugum, il)
        if k.mac.alinan_yayin > n0:
            krediler.append((sum(k.mac.dugum_alinan_bayt) - a0)
                            / (k.mac.alinan_yayin - n0))

    k.mac._yayin_bitti = izle
    k.kostur()
    assert krediler and all(abs(x - kon.beacon_bayt) < 1e-9 for x in krediler)


# ==========================================================================
# 🔴 B-72 (K-056) — TETİKLENEMEYEN DAL ARTIK BİR DEĞİŞMEZ
#
# `baska.gonderen == alici` dalı 246 378 çağrının 0'ında tetikleniyordu.
# Deponun kendi kuralı: *"Tetiklenemeyen bir kontrol, koruma sağlamadan
# koruma izlenimi verir."* Asıl risk, yarı çift yönlü kontrolü bir gün
# kalkarsa bu dalın SESSİZCE doğru cevabı verip hatayı MASKELEMESİydi.
# ==========================================================================

def test_b72_alici_kendi_iletimindeyken_DEGISMEZ_atesliyor():
    """🔴 Y11 — değişmezin gerçekten ateşlediği gösteriliyor.

    Yasak durum elle kuruluyor: alıcı, değerlendirilen anda kendi iletimini
    yapıyor. Gerçek koşuda bu imkânsız (bu yüzden dal tetiklenmiyordu), ama
    bir gün mümkün olursa **sessizce doğru cevap** vermek yerine düşmeli.
    """
    kon, topo, ol, mac = duzenek([(0, 0), (250, 0), (500, 0)], senaryo="S0")
    il = Iletim(0, 1, 1.0, 1.0 + kon.paket_suresi_s, "veri")
    # alıcı (1) aynı anda KENDİ iletimini yapıyor — yasak durum
    kendi = Iletim(1, 2, 1.0, 1.0 + kon.paket_suresi_s, "veri")
    mac.aktif = [il, kendi]
    with pytest.raises(AssertionError, match="yari cift yonlu"):
        mac._girisim_w(1, il, 1.0 + kon.paket_suresi_s / 2)


def test_b72_NORMAL_durumda_degismez_susuyor():
    """Kontrol kolu: meşru bir girişim hesabı hâlâ çalışıyor."""
    kon, topo, ol, mac = duzenek([(0, 0), (250, 0), (500, 0)], senaryo="S0")
    il = Iletim(0, 1, 1.0, 1.0 + kon.paket_suresi_s, "veri")
    baska = Iletim(2, 0, 1.0, 1.0 + kon.paket_suresi_s, "veri")
    mac.aktif = [il, baska]
    g = mac._girisim_w(1, il, 1.0 + kon.paket_suresi_s / 2)
    assert g > 0.0, "girişim hesaplanmıyor"


# ==========================================================================
# 🔴 B-117 / M14 (ALTINCI DENETİM) — MEŞGUL BİLDİRİMİNİN GECİKMESİ
#    KORUMASIZDI
#
# Mutasyon: `gecikmeyle_ekle(self.kon.cca_s, ...)` -> `gecikmeyle_ekle(0.0, ...)`
# Yani `cca_s` sabiti YERİNDE DURUYOR, yalnızca BİLDİRİM anında yapılıyor.
# Ölçüldü (27 Ağu, 4 yapılandırma × 65 sayısal alan): 43–48 alan değişiyor.
#
# 🔴 VE `test_cca_ayni_slot_carpismasini_uretiyor` SUSUYOR — ölçüldü,
# `test_mac.py` + `test_kapi_aile0.py` mutantla **48 passed**.
#
# Sebebi denetçinin yazdığı gibi: o test `cca_s` SABİTİNİ sıfırlamayı
# yakalıyor, **bildirim gecikmesi YOLUNU** değil. İkisi ayrı eksen ve
# ikincisinde hiçbir koruma yoktu.
#
# ⚠️ Bu test KASTEN yapısaldır: olay kuyruğundaki bildirimin ZAMANINI
# okur. Davranışsal bir kurulum (iki düğümü aynı slotta çarpıştırmak)
# zaten var ve M14'ü GÖREMİYOR — aynı deseni tekrarlamak boşluğu
# kapatmazdı (Y11: koruma, kapsamı DIŞINDAKİ vakayla sınanır).
# ==========================================================================

def test_b117_m14_mesgul_bildirimi_CCA_KADAR_erteleniyor():
    """🔴 Bildirim `cca_s` kadar ERTELENMELİ — anında değil.

    `config.py`nin gerekçesi: *"Anında bildirilseydi, geri sayımı aynı
    slotta biten iki düğümden ikincisi diğerini SIFIR gecikmeyle görür ve
    susardı -> aynı-slot çarpışması HİÇ OLMAZDI."*

    Gerekçe yazılıydı; kod karşılığını sınayan yoktu.
    """
    kon, topo, ol, mac = duzenek([(0.0, 0.0), (50.0, 0.0)])

    # 🔴 Y8 — ölçüt anlamlı mı: `cca_s` sıfır olsaydı bu test boş olurdu
    assert kon.cca_s > 0.0, "cca_s sıfır — bu testin ölçtüğü şey yok (Y7)"

    t0 = 0.25
    ol.kostur(t0)
    il = Iletim(0, 1, ol.simdi, ol.simdi + kon.paket_suresi_s, "veri")
    onceki = len(ol._yigin)
    mac._iletim_basla(il)

    yeni = [x for x in ol._yigin if x[2] == mac._mesgul_bildir]
    assert len(yeni) == 1, (
        f"`_iletim_basla` meşgul bildirimini planlamadı ({len(yeni)} olay) — "
        f"kuyrukta {len(ol._yigin) - onceki} yeni olay var")

    zaman = yeni[0][0]
    assert zaman == pytest.approx(ol.simdi + kon.cca_s, rel=1e-12, abs=0.0), (
        f"🔴 meşgul bildirimi t={zaman!r} anına planlandı; olması gereken "
        f"t={ol.simdi + kon.cca_s!r} (şimdi + cca_s). ANINDA bildirim, "
        f"aynı-slot çarpışmasını YOK EDER ve verimi sessizce şişirir "
        f"(B-117/M14).")

    # 🔴 Y11 — kapsam DIŞI vaka: gecikme sıfır DEĞİL, ve bu ayırt edilebilir
    assert zaman > ol.simdi, (
        "bildirim şimdiyle AYNI ana planlanmış — `cca_s` yok sayılmış")
