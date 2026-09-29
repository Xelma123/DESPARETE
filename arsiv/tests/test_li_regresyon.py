"""
Ç4.1 — Li replikasyonu REGRESYON TESTİ.

🔴 NEDEN BETİK DEĞİL TEST
Bir kapı "geçti" diye ilan edildikten sonra, altındaki kod değişmeye devam
eder. Betik yalnızca elle koşulduğunda konuşur; test her seferinde konuşur.

Bu dosya olmasaydı MAC'teki bir değişiklik Li sonucunu sessizce kaydırırdı
ve kimse görmezdi. Bu tam olarak bir kez ramak kaldı: onay gerçek iletim
yapıldığında plato 1/5,98'den 1/8,86'ya fırladı — o sırada yalnızca elle
koşulan bir betik vardı.

BANT NASIL SEÇİLDİ
Ölçülen değerin etrafında ±%10. Gerekçe:
  - 5 tohumda güven aralığı genişliği %4–8 → ±%10 kararlı geçer
  - gerçek kaymalar çok daha büyük: onay hatası 8 atlamada %31 kaydırmıştı
Yani bant, gürültüyü tolere edip gerçek kaymayı yakalayacak genişlikte.

⚠️ Bant, sonuç görüldükten SONRA gevşetilemez. Kayma olursa sebebi bulunur;
bant büyütülmez.
"""

from __future__ import annotations

import statistics as ist
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.li_zincir import zincir_kosusu  # noqa: E402

TOHUMLAR = range(1, 6)
ARALIK = 0.85              # bağ kaybı ~0, Li'nin ns-2 modeli gibi
BANT = 0.10                # ±%10


def _oran(atlama: int, **ek) -> float:
    """Eşleştirilmiş oran: aynı tohumda uzun zincir / tek atlama."""
    tek = [zincir_kosusu(1, t, ARALIK, **ek)["verim_bps"] for t in TOHUMLAR]
    uzun = [zincir_kosusu(atlama, t, ARALIK, **ek)["verim_bps"] for t in TOHUMLAR]
    return ist.mean(u / v for u, v in zip(uzun, tek))


def test_tek_atlama_verimi_analitige_esit():
    """Tek atlama, çekişmesiz: DIFS + geri çekilme + veri + SIFS + onay."""
    from sim.config import Konfig
    kon = Konfig(kol="t", paket_bayt=1500)
    dongu = (kon.difs_s + (kon.cw_min / 2) * kon.slot_s
             + kon.cerceve_suresi_s(1500) + kon.sifs_s + kon.onay_suresi_s)
    beklenen = 1500 * 8 / dongu
    olculen = ist.mean(zincir_kosusu(1, t, ARALIK)["verim_bps"] for t in TOHUMLAR)
    assert olculen == pytest.approx(beklenen, rel=0.02), (olculen, beklenen)


def test_ideal_zincir_bolgesi_dorde_yakin():
    """4 atlamada oran ~1/4 olmalı — Li'nin 'ideal zincir' değeri.

    Ölçülen: 1/3,87. Bu, Li'nin 1/4'üne doğrudan karşılık gelir ve
    replikasyonun NİTEL olarak tuttuğunun en net göstergesidir.
    """
    oran = _oran(4)
    assert 1 / oran == pytest.approx(3.87, rel=BANT), 1 / oran


def test_uzun_zincir_platosu():
    """🔴 ASIL REGRESYON — raporda geçen sayı budur.

    8 atlamada ölçülen: 1/5,87  (20 atlamadaki plato: 1/6,29, 30 tohumla)
    Burada 8 atlama kullanılıyor çünkü test her koşuda çalışmalı; 20 atlama
    × 30 tohum doğrulama betiğinde (`dogrulama/li_duyarlilik.py`).
    """
    oran = _oran(8)
    assert 1 / oran == pytest.approx(5.87, rel=BANT), (
        f"Li platosu kaydı: 1/{1/oran:.2f} (beklenen 1/5,87 ± %{BANT*100:.0f}). "
        f"Bant gevşetilmez — sebep bulunur."
    )


def test_verim_atlama_sayisiyla_dusuyor():
    """Nitel davranış: verim monoton azalmalı ve plato yapmalı."""
    oranlar = [_oran(h) for h in (2, 4, 8)]
    assert oranlar[0] > oranlar[1] > oranlar[2], oranlar
    # 8'den 16'ya düşüş, 2'den 4'e düşüşten belirgin KÜÇÜK olmalı (plato)
    dusus_erken = oranlar[0] - oranlar[1]
    dusus_gec = oranlar[2] - _oran(16)
    assert dusus_gec < dusus_erken / 2, (dusus_erken, dusus_gec)


def test_bag_kaybi_platoyu_belirgin_kaydiriyor():
    """Kontrol kolu: aralık çarpanı en duyarlı eksen olmalı.

    Bu test olmadan, üstteki testlerin 'her şeyi sabit tutan bir hata'
    yüzünden mi geçtiği ayırt edilemez.
    """
    tek = [zincir_kosusu(1, t, 1.00)["verim_bps"] for t in TOHUMLAR]
    uzun = [zincir_kosusu(8, t, 1.00)["verim_bps"] for t in TOHUMLAR]
    kayipli = ist.mean(u / v for u, v in zip(uzun, tek))
    assert 1 / kayipli > 1 / _oran(8) * 1.5, (
        "bağ kaybı platoyu kaydırmıyor — kurulum şüpheli"
    )


def test_yeniden_deneme_siniri_platoyu_belirlemiyor():
    """K-028 bulgusu: ns-2'nin sınırı (7) ile bizimki (4) ayırt edilemez.

    Bu, Li açığının yeniden deneme sınırından GELMEDİĞİNİN regresyonudur.
    30 tohumluk ölçüm: 1/6,29 vs 1/6,24, GA'lar örtüşüyor.
    """
    dort = _oran(8, yeniden_deneme_siniri=4)
    yedi = _oran(8, yeniden_deneme_siniri=7)
    assert abs(dort - yedi) / dort < 0.05, (dort, yedi)
