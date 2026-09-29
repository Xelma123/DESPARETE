"""
Sonuç yazıcı ve kaynak hash testleri.

"Yanlış sayı, çalışmayan koddan daha tehlikelidir çünkü sessizdir."
(03-YONTEM-KURALLARI.md, Bölüm B5)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.config import Konfig  # noqa: E402
from sim.ledger import KorunumDefteri  # noqa: E402
from sim.results import SonucYazici, kaynak_hash, satirlari_oku  # noqa: E402


def test_kaynak_hash_kararlı():
    assert kaynak_hash() == kaynak_hash()


def test_kaynak_hash_icerik_degisince_degisiyor(tmp_path):
    (tmp_path / "a.py").write_text("x = 1", encoding="utf-8")
    once = kaynak_hash(tmp_path)
    (tmp_path / "a.py").write_text("x = 2", encoding="utf-8")
    assert kaynak_hash(tmp_path) != once


def test_kaynak_hash_dosya_adi_degisince_degisiyor(tmp_path):
    """Yeniden adlandırma da kod değişikliğidir."""
    (tmp_path / "a.py").write_text("x = 1", encoding="utf-8")
    once = kaynak_hash(tmp_path)
    (tmp_path / "a.py").rename(tmp_path / "b.py")
    assert kaynak_hash(tmp_path) != once


def test_satir_tam_konfigurasyonu_tasiyor(tmp_path):
    """Bayrağı olmayan bir satır yeniden üretilemez."""
    kon = Konfig(kol="etx_takvimli", senaryo="S2", trafik="orta", tohum=1000)
    d = KorunumDefteri()
    d.uret(10)
    d.kuyruktan_al(10)
    d.teslim_et(10)

    yol = tmp_path / "sonuc.jsonl"
    with SonucYazici(yol, kaynak_hash_degeri="test") as y:
        y.yaz(kon.sozluk(), d.kontrol(), {"teslim_orani": 1.0})

    (satir,) = list(satirlari_oku(yol))
    assert satir["konfig"]["kol"] == "etx_takvimli"
    assert satir["konfig"]["tohum"] == 1000
    assert satir["konfig"]["kuyruk_kapasitesi"] == kon.kuyruk_kapasitesi
    assert satir["korunum"]["korunum_tamam"] is True
    assert satir["kaynak_hash"] == "test"

    # Konfigürasyonun HER alanı satırda olmalı — biri eksikse o koşu
    # yeniden üretilemez.
    assert set(satir["konfig"]) == set(kon.sozluk())


def test_bozuk_korunum_satiri_yine_de_yaziliyor(tmp_path):
    """Bozuk koşu SİLİNMEZ, işaretlenir.

    Silmek, kaç koşunun bozuk olduğunu da silmek demektir.
    """
    kon = Konfig(kol="x")
    d = KorunumDefteri()
    d.uret(5)
    d.teslim += 3                      # kasıtlı bozma

    yol = tmp_path / "s.jsonl"
    with SonucYazici(yol, kaynak_hash_degeri="t") as y:
        y.yaz(kon.sozluk(), d.kontrol(), {})

    (satir,) = list(satirlari_oku(yol))
    assert satir["korunum"]["korunum_tamam"] is False


def test_her_satir_aninda_diske_yaziliyor(tmp_path):
    """Matris yarıda kesilirse tamamlanan koşular kaybolmamalı."""
    yol = tmp_path / "s.jsonl"
    y = SonucYazici(yol, kaynak_hash_degeri="t")
    kon = Konfig(kol="x")
    for i in range(3):
        y.yaz(kon.sozluk(), {"korunum_tamam": True}, {"i": i})
        # kapat() ÇAĞRILMADAN dosya okunabiliyor olmalı
        assert len(yol.read_text(encoding="utf-8").strip().splitlines()) == i + 1
    y.kapat()


def test_bozuk_satir_sessizce_atlanmiyor(tmp_path):
    yol = tmp_path / "s.jsonl"
    yol.write_text('{"a": 1}\n{"bozuk"\n', encoding="utf-8")
    with pytest.raises(ValueError, match="bozuk JSON"):
        list(satirlari_oku(yol))


# --------------------------------------------------------------------------
# Konfigürasyon
# --------------------------------------------------------------------------

def test_konfig_dondurulmus():
    """Koşu ortasında değişen bir parametre, sonuç satırını yalancı yapar."""
    kon = Konfig(kol="x")
    with pytest.raises(Exception):
        kon.tohum = 5          # type: ignore[misc]


def test_gecersiz_sinr_esigi_reddediliyor():
    """Eşik ≤ 0 dB olursa girişim menzili iletim menzilinden geniş olmaz
    ve gizli terminal doğmaz — Li replikasyonu imkânsızlaşır."""
    with pytest.raises(ValueError, match="SINR eşiği"):
        Konfig(kol="x", sinr_esigi_db=0.0)
    with pytest.raises(ValueError, match="yol kaybı üsteli"):
        Konfig(kol="x", yol_kaybi_usteli=0.0)


def test_girisim_orani_turetilmis_alan_degil():
    """Girişim oranı ve menzili ayrı ALAN olmamalı — türetilmeli.

    Ayrı olsalardı radyo modeliyle sessizce çelişebilirlerdi: iki ayrı
    'doğru' kaynağı olurdu ve biri güncellenirken diğeri unutulurdu.
    """
    kon = Konfig(kol="x", iletim_menzili_m=280.0)
    assert kon.girisim_orani == pytest.approx(10.0 ** (1.0 / 3.0))
    assert kon.girisim_menzili_m == pytest.approx(280.0 * kon.girisim_orani)

    sozluk = kon.sozluk()
    for turetilmis in ("girisim_orani", "girisim_menzili_m",
                       "karistirici_guc_dbm", "karistirici_darbeli"):
        assert turetilmis not in sozluk, (
            f"{turetilmis} türetilmiş olmalı, konfigürasyon alanı değil"
        )

    with pytest.raises(TypeError):
        Konfig(kol="x", girisim_orani=2.2)  # type: ignore[call-arg]


def test_girisim_orani_esikle_birlikte_degisiyor():
    """β veya α değişince oran DA değişmeli.

    Elle yazılmış 2,2 değeri bu durumda sessizce yanlış kalırdı.
    """
    a = Konfig(kol="x", sinr_esigi_db=10.0, yol_kaybi_usteli=3.0)
    b = Konfig(kol="x", sinr_esigi_db=15.0, yol_kaybi_usteli=3.0)
    c = Konfig(kol="x", sinr_esigi_db=10.0, yol_kaybi_usteli=2.0)
    assert b.girisim_orani > a.girisim_orani
    assert c.girisim_orani > a.girisim_orani


def test_zaman_sinirlari_tutarli_olmali():
    with pytest.raises(ValueError, match="zaman sınırları"):
        Konfig(kol="x", isinma_s=100.0, olcum_bitis_s=50.0)


def test_sonsuz_kuyruk_yasak():
    with pytest.raises(ValueError, match="kuyruk kapasitesi"):
        Konfig(kol="x", kuyruk_kapasitesi=0)


def test_olcum_penceresi_kosu_bitisinden_kisa():
    """Boşaltma penceresi gerçekten var olmalı."""
    kon = Konfig(kol="x")
    bas, bit = kon.olcum_penceresi
    assert bas == kon.isinma_s
    assert bit == kon.olcum_bitis_s
    assert kon.kosu_bitis_s > bit, "boşaltma penceresi yok"
    assert kon.kosu_bitis_s - bit == pytest.approx(30.0)
