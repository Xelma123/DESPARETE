"""
Karıştırma altında İHA mesh ağı ölçüm ortamı.

Bu paket bir ARAÇTIR. Sonuçlarının güvenilirliği, aracın kendisinin
doğrulanmış olmasına bağlıdır (03-YONTEM-KURALLARI.md, Bölüm D).

Katmanlar — 07-SIMULATOR-ARAYUZ.md
    Kat 0  trafik      traffic.py            ✅
    Kat 1  zaman       events.py             ✅
    Kat 2  radyo       radio.py              ✅
    Kat 3  MAC         mac.py                ✅
    Kat 5  gözlem      (henüz yazılmadı)
    Kat 4  yönlendirme (henüz yazılmadı)

Altyapı
    config.py    konfigürasyon — her kol bir bayrak    ✅
    rng.py       ayrık akışlar + sayaç tabanlı kanal   ✅
    ledger.py    korunum defteri                       ✅
    results.py   sonuç yazıcı + kaynak hash            ✅
    topology.py  konumlar · menzil · bağlı bileşen     ✅
    packet.py    paket + TTL                           ✅
    queues.py    sonlu kuyruk · kuyruk sonu atma       ✅

Koşucu
    kosucu.py    tüm katmanları birleştiren gerçek koşucu

⚠️ `skeleton.py` (kusursuz kanallı geçici koşucu) 18 Ağustos 2026'da SİLİNDİ.
Yanında bırakılsaydı bir gün yanlışlıkla çağrılır ve kusursuz kanaldan çıkan
bir sayı deney sonucu sanılırdı (Ç6.4).
"""

from .config import (
    DIRSEK_TARAMASI_DBM, Konfig, SENARYO_TANIMLARI, SENARYOLAR,
    TRAFIK_SEVIYELERI,
)
from .radio import Karistirici, Radyo, dbm_to_w, w_to_dbm
from .events import OlayKuyrugu, GecmisZamanHatasi
from .ledger import KorunumDefteri, KorunumHatasi, DUSME_SEBEPLERI
from .packet import Paket
from .queues import Kuyruk
from .rng import Akislar, kanal_cekimi, AKIS_ADLARI
from .results import SonucYazici, kaynak_hash, satirlari_oku
from .kosucu import Kosu
from .topology import Topoloji
from .traffic import Akis, TrafikUreteci

__all__ = [
    "Konfig", "SENARYOLAR", "TRAFIK_SEVIYELERI", "SENARYO_TANIMLARI",
    "DIRSEK_TARAMASI_DBM",
    "Radyo", "Karistirici", "dbm_to_w", "w_to_dbm",
    "OlayKuyrugu", "GecmisZamanHatasi",
    "KorunumDefteri", "KorunumHatasi", "DUSME_SEBEPLERI",
    "Paket", "Kuyruk",
    "Akislar", "kanal_cekimi", "AKIS_ADLARI",
    "SonucYazici", "kaynak_hash", "satirlari_oku",
    "Topoloji", "TrafikUreteci", "Akis",
    "Kosu",
]
