"""
İŞARET TESTİ — `06` Bölüm 9 koşul 1'in ilan edilmiş ölçütü.

🔴 BU DOSYANIN ASIL İŞİ BİR SAYIYI KORUMAK DEĞİL, BİR ÖLÇÜTÜ KORUMAK.
Y12: *"elle tutulan her kapı sabiti ucuz bir testle korunur."* Buradaki
"sabit" bir eşik değil, bir KARARDIR: hangi kolun koşul 1'i geçtiğini
söyleyen kural. Kural sessizce gevşerse (α büyür, test tek yönlü olur,
beraberlikler sayılmaya başlar) 8/30 bir gün "geçti" görünür — ve
`03` kural 3'ün yasakladığı şey tam olarak budur.
"""

from __future__ import annotations

import math

import pytest

from dogrulama.isaret_testi import (
    cift_yonlu_p, isaret_testi, medyan_guven_araligi,
)


# ==========================================================================
# İLAN EDİLEN ÖLÇÜT — ve onu üreten iki gerçek ölçüm
# ==========================================================================

def test_ilan_edilen_olcut_BILINEN_IKI_YARGIYI_birebir_uretiyor():
    """🔒 Ölçüt, `10` §7b.3'ün 🟢/🔴 yargılarını DEĞİŞTİRMEDEN üretmeli.

    Bu, ölçütün geriye dönük bir GEVŞETME olmadığının kanıtıdır
    (`03` kural 3). Ölçüt ilan edilirken iki kolun verisi zaten
    ölçülmüştü; o yüzden "yeni ölçüt eski yargıyı korudu mu" sorusu
    sorulmak ZORUNDAYDI.
    """
    # `en_kisa_yol` (kâhin): 30 tohumun 15'inde kısa koşu daha yüksek
    assert cift_yonlu_p(15, 30) == pytest.approx(1.0)
    # `gurultuden_kacan` (saf gözlem): yalnızca 8'inde
    p_gozlem = cift_yonlu_p(8, 30)
    assert p_gozlem == pytest.approx(0.016124, abs=1e-6)
    assert p_gozlem <= 0.05, "🔴 8/30 GEÇER hâle geldi — ölçüt gevşemiş"


def test_olcut_TEK_YONLU_degil_CIFT_YONLU():
    """🔴 `03` B2: tek yönlü bir test ters yöndeki bulguyu göremez.

    Simetri, ölçütün çift yönlü olduğunun davranışsal kanıtıdır: 8/30 ile
    22/30 aynı p'yi vermeli. Test tek yönlü olsaydı biri 0,008 diğeri
    0,992 verirdi ve *"ters yönde sistematik"* bir kol sessizce geçerdi.
    """
    assert cift_yonlu_p(8, 30) == pytest.approx(cift_yonlu_p(22, 30))
    assert cift_yonlu_p(0, 10) == pytest.approx(cift_yonlu_p(10, 10))


@pytest.mark.parametrize("k,n,beklenen", [
    (0, 10, 2 / 2 ** 10),
    (5, 10, 1.0),
    (1, 5, 12 / 32),
    (15, 30, 1.0),
])
def test_kesin_binom_ELDE_HESAPLANAN_degerlerle_ayni(k, n, beklenen):
    """Yaklaşım yok: p elde hesaplanabilen kesin bir kesirdir."""
    assert cift_yonlu_p(k, n) == pytest.approx(beklenen, rel=1e-12)


def test_kuyruk_toplami_KESIN():
    """P(X ≤ k) tam sayı aritmetiğinden gelir — normal yaklaşımı DEĞİL."""
    elde = sum(math.comb(30, i) for i in range(9)) / 2 ** 30
    assert cift_yonlu_p(8, 30) == pytest.approx(2 * elde, rel=1e-12)


# ==========================================================================
# BERABERLİKLER ve DEJENERE DURUM — `03` B2
# ==========================================================================

def test_beraberlikler_DISLANIYOR_ve_RAPORLANIYOR():
    """Sıfır fark bir gözlem KAYBIDIR; sessizce yutulamaz."""
    s = isaret_testi([0.0, 0.1, 0.2, -0.05])
    assert s["n_ham"] == 4 and s["n"] == 3 and s["berabere"] == 1
    assert s["p"] == pytest.approx(cift_yonlu_p(2, 3))


def test_TUM_farklar_sifirken_ETKI_YOK_denmiyor():
    """🔴 `03` B2: *"`nan` = ölçüm yok"*, *"etki yok"* değil.

    Bir sayı döndürmek en tehlikeli seçenekti: 1,0 p değeri *"fark yok"*
    diye okunurdu. Test TANIMSIZ olduğunu söylemek zorunda.
    """
    s = isaret_testi([0.0] * 5)
    assert s["p"] is None and s["gecti"] is None
    assert "TANIMSIZ" in s["not"]
    with pytest.raises(ValueError):
        cift_yonlu_p(0, 0)


# ==========================================================================
# DIŞLANAN ETKİ BÜYÜKLÜĞÜ — `03` B2'nin ikinci şartı
# ==========================================================================

def test_ga_SIRA_ISTATISTIGI_ve_testle_AYNI_varsayimda():
    """GA, işaret testinin eşleniği: aynı binomdan türer, t tablosu yok."""
    veri = [i / 100 for i in range(1, 31)]        # 0,01 … 0,30
    ga = medyan_guven_araligi(veri)
    assert ga is not None
    s = sorted(veri)
    # n=30 için en büyük k: 2·P(X ≤ k−1) ≤ 0,05  →  k = 10
    assert ga == (s[9], s[20])
    assert ga[0] < ist_medyan(veri) < ga[1]


def ist_medyan(v):
    import statistics
    return statistics.median(v)


def test_ga_kucuk_n_de_YOK_ve_bu_SESSIZ_degil():
    """🔴 Aralık kurulamıyorsa `None` döner — sonsuz aralık uydurulmaz."""
    assert medyan_guven_araligi([0.1, 0.2, 0.3]) is None
    s = isaret_testi([0.1, 0.2, 0.3])
    assert s["ga"] is None and s["p"] is not None


def test_ga_TOHUM_STD_katina_cevriliyor():
    """Bir fark ancak deneyin KENDİ gürültüsüne göre 'küçük'tür (`03` B2)."""
    farklar = [0.01 * i for i in range(1, 31)]
    s = isaret_testi(farklar, tohum_std=0.1569)   # `10` §7b.1'in ölçtüğü std
    assert s["ga_std_kati"] is not None
    alt, ust = s["ga_std_kati"]
    assert alt == pytest.approx(s["ga"][0] / 0.1569)
    assert ust == pytest.approx(s["ga"][1] / 0.1569)


# ==========================================================================
# 🔴 Y8 — ÖLÇÜT GERÇEKTEN AYIRT EDİYOR MU (boş küme tuzağı)
# ==========================================================================

def test_y8_olcut_AYIRT_EDIYOR_hem_gecen_hem_gecmeyen_uretiyor():
    """Her şeyi geçiren bir ölçüt, ölçüt değildir.

    30 tohumda sistematik bir kayma GEÇMEMELİ; simetrik gürültü GEÇMELİ.
    İkisi de gösterilmezse test *"0 == 0"* sınıfına düşer (Y7).
    """
    sistematik = isaret_testi([-0.01] * 22 + [0.01] * 8)
    simetrik = isaret_testi([-0.01] * 15 + [0.01] * 15)
    assert sistematik["gecti"] is False, "sistematik kayma geçti — ölçüt kör"
    assert simetrik["gecti"] is True, "simetrik gürültü düştü — ölçüt fazla sıkı"
