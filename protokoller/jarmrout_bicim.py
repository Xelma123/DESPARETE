"""
JarmRout mesaj biçimleri, sabitleri ve beyan tablosu — TEK KAYNAK.

Kaynak: C. Pu, *"Jamming-Resilient Multipath Routing Protocol for Flying Ad
Hoc Networks"*, IEEE Access 6:68472–68486, 2018
(`protokol_kaynaklari/pu_2018_jarmrout_ieee_access.pdf`; `v2/02` R6).
Gerçekleme ilkesi (K-229 · K-231, yürütücü: "yüzde yüz sadık"):

  1. makalede yazan her kural HARFİYEN — DSR'den farklı olduğu yerde de;
  2. makalenin SUSTUĞU yerde DSR (RFC 4728; `v2/02` R7) — makale DSR
     üzerine kurulu (rota kaydı, ters rotayla RREP, kaynakta tam rota,
     RERR) ve karşılaştırma tabanı DSR;
  3. ikisinin de sustuğu yerde gerekçeli seçim — aşağıdaki tabloda
     "seçim" diye işaretli, duyarlılığı ölçülür.

Tasarım notu `arsiv/teshis/jarmrout_2026-10-11/tasarim.md`.

🔒 MESAJ BOYUTLARI KAYNAKTAN
============================
  RREQ  (makale Şekil 2): S_id 4 · D_id 4 · pkt_seq 2 · C_hop 1 · H_route 4n
        · P_coord 4n · L_qt 4 · T_ld 4  →  19 + 8n bayt
        P_coord düğüm başına 4 bayt: iki 16 bitlik koordinat (metre, yatay;
        makale 2B varsayar).
  RREP  (RFC 4728 §6.1 · §6.3 · §6.7): DSR seçenek başlığı 4 · Route Reply
        seçeneği 3 + 4n (n: rotanın adresleri, hedef dâhil) · RREP'i kaynağa
        taşıyan Source Route seçeneği 4 + 4m (m: dönüş yolunun ara düğümleri)
        · kaynağın adresi 4 (gerçekte IP başlığının hedef adresi — beyanlı +4
        bayt, AODV'deki TTL gibi tutucu yönde)  →  15 + 4n + 4m bayt
  RERR  (RFC 4728 §6.1 · §6.4 · §6.7): DSR seçenek başlığı 4 · Route Error
        seçeneği 16 (hata kaynağı · hata hedefi · ulaşılamaz düğüm) · Source
        Route seçeneği 4 + 4m  →  24 + 4m bayt
  VERİ başlığı (RFC 4728 §6.1 · §6.7): DSR seçenek başlığı 4 + Source Route
        seçeneği 4 → `VERI_BASLIK_BAYT` 8; ara düğüm başına `ROTA_ADRES_BAYT`
        4 (simülatörün kaynak rotası, K-232).
Boyutlar `tests2/test_jarmrout.py` ile bağlı.

🔴 BEYAN TABLOSU — makaleye göre her fark ve her dolgu
=====================================================
| konu | makale | gerçekleme | kaynak |
|---|---|---|---|
| trafik yükünün kanal terimi | son erişimdeki NAV, ms (RTS/CTS'in sanal taşıyıcı dinlemesi, Eş. 6; Tablo 2: T_busy ≈ 7 ms) | son güncellemeden bu yana CCA'nın meşgul kaldığı süre, ms (`mesgul_sure_s`, sürücünün "channel busy time"ı) | simülatörde RTS/CTS yok (`04` §1); NAV ortamın meşgul tutulduğu süredir, CCA meşgul süresi aynı büyüklüğün fiziksel ölçüsü — beyanlı sapma |
| bağ kopması | "sürekli teslim edemezse" (örtük/açık onay yok) | MAC'in vazgeçmesi (7 deneme, `iletim_basarisiz`) | makale + RFC 4728 §3.3 (bağ katmanı onayı) |
| RREQ önbelleği anahtarı | `pkt_seq` | `(S_id, pkt_seq)` | RFC 4728 §3.3.2 Route Request Table (başlatıcı + kimlik); farklı kaynaklar aynı sırayı taşıyabilir |
| RREQ yeniden denemesi | yok | RequestPeriod 0,5 s, iki katına, en çok 10 s, en çok 16 kez | RFC 4728 §3.3.2 · §9 |
| yayın titreşimi | yok | 0–10 ms tekdüze | RFC 4728 §9 BroadcastJitter |
| rota önbelleği ömrü | yok | 300 s (RERR'e kadar) | RFC 4728 §9 RouteCacheTimeout |
| keşif sürerken veri | yok (Şekil 4: "broadcast RREQ") | simülatörün ortak bekleme tamponu (64 paket · 30 s, herkes için aynı) | RFC 4728 §9 SendBufferTimeout 30 s; tampon ortak (`06` §8 koşul 3) |
| RSSI örnek sayısı N_rssi | Tablo 1'in örneği: komşudan en son dört paket (R_x … R_x+3) | 4 | makalenin örneği |
| eşitlik bozan beklenen RSSI | örnek −55 dBm | −55 dBm | makalenin örneği |
| `t_wait` | değer yok | SEÇİM — bkz. `T_WAIT_S` | makale ve DSR susuyor |
| Eş. 8'in kazancı γ ve düzeltme çarpanı ε | metinde değer yok | γ = 0,5 · ε = 0,02 | Tablo 2'nin örneğinden çözüldü: TL = (γ+ε)·T_busy + (1−γ+ε)·Q_buf, n_b ve n_c'den iki katsayı 0,52 → γ 0,5, ε 0,02; n_a ile sağlama 11,6282 |
| Eş. 6 · 7'nin süzgeç sabitleri | değer yok | SEÇİM 0,5 — bkz. `YUK_*_SUZGECI` | makale susuyor; Tablo 2 ortalamaları verir, süzgeç geçmişini vermez |
| Eş. 13'ün mekânsal terimi | γ·e^(1/Υ) | aynı; Υ metre (makalenin benzetiminde de metre, 1000 m alan) | Şekil 3'ün örneği (7,4638 · 6,8831 · 7,7095) ile birebir sınandı; Υ tanımsız (ara düğümsüz yol) → terim γ (seçim) |
| tek yol bulunursa | kısıt tartışması: tek yol kurulur | tek RREP, tek yol | makale §VI.A |
| konum | 2B (sabit irtifa varsayımı) | GPS/INS konumunun yatay izdüşümü, metre, 16 bit | makale §III.A |
| RREP · RERR biçimi | yok | DSR seçenekleri | RFC 4728 §6.3 · §6.4 |
"""

from __future__ import annotations

from sim2.gozlem.kontrol import MesajBicimi

__all__ = [
    "RREQ", "RREP", "RERR", "VERI_BASLIK_BAYT", "ROTA_ADRES_BAYT",
    "AGIRLIK_BAG", "AGIRLIK_YUK", "AGIRLIK_UZAKLIK", "N_RSSI",
    "BEKLENEN_RSSI_DBM", "REQUEST_PERIOD_S", "MAX_REQUEST_PERIOD_S",
    "MAX_REQUEST_REXMT", "BROADCAST_JITTER_S", "ROUTE_CACHE_TIMEOUT_S",
    "T_WAIT_S", "YUK_KANAL_SUZGECI", "YUK_KUYRUK_SUZGECI",
    "YUK_KANAL_AGIRLIGI", "YUK_DUZELTME", "KONUM_BIT",
]

# ---------------------------------------------------------------- biçimler
# Makale Şekil 2 — RREQ. Tekrarlı üç alan düğüm başına: H_route 32 bit +
# P_coord (x 16 + y 16) = 8 bayt.
RREQ = MesajBicimi("RREQ", (
    ("kaynak", 32),
    ("hedef", 32),
    ("pkt_seq", 16),
    ("c_hop", 8),
    ("l_qt", 32),               # yoldaki en kötü (en büyük) bağ kalitesi
    ("t_ld", 32),               # yoldaki en büyük trafik yükü
), tekrarli=(
    ("h_route", 32),
    ("x", 16),
    ("y", 16),
))

# RFC 4728 §6.1 (DSR seçenek başlığı) · §6.3 (Route Reply) · §6.7 (Source
# Route, RREP'i kaynağa taşır). `ip_hedef` IP başlığının hedef adresidir
# (kaynak düğüm); yükte taşınır, +4 bayt beyanlı (tutucu yön).
RREP = MesajBicimi("RREP", (
    ("dsr_baslik", 32),         # Next Header 8 · F 1 · Reserved 7 · Len 16
    ("rrep_secenek", 24),       # Option Type 8 · Opt Data Len 8 · L|Res 8
    ("kaynak_rota_secenek", 32),  # Type 8 · Len 8 · F L Res Salvage SegsLeft 16
    ("ip_hedef", 32),
), tekrarli=(
    ("yol", 32),                # Route Reply Address[1..n] (hedef dâhil)
    ("donus", 32),              # Source Route Address[1..m] (kaynağa dönüş)
))

# RFC 4728 §6.1 · §6.4 (Route Error) · §6.7 (Source Route, RERR'i kaynağa
# taşır).
RERR = MesajBicimi("RERR", (
    ("dsr_baslik", 32),
    ("rerr_secenek", 32),       # Type 8 · Len 8 · Error Type 8 · Res|Salvage 8
    ("hata_kaynagi", 32),       # bağı kopan düğüm
    ("hata_hedefi", 32),        # RERR'in gittiği kaynak düğüm
    ("ulasilamaz", 32),         # kopan bağın öteki ucu
    ("kaynak_rota_secenek", 32),
), tekrarli=(
    ("donus", 32),
))

VERI_BASLIK_BAYT: int = 4 + 4   # DSR seçenek başlığı + Source Route sabiti
ROTA_ADRES_BAYT: int = 4        # Source Route Address[i]
KONUM_BIT: int = 16             # P_coord'un bir koordinatı (metre)

# ---------------------------------------------------------------- makale
AGIRLIK_BAG: float = 0.2        # Eş. 13 α
AGIRLIK_YUK: float = 0.2        # Eş. 13 β
AGIRLIK_UZAKLIK: float = 0.6    # Eş. 13 γ
N_RSSI: int = 4                 # Tablo 1'in örneği: R_x … R_x+3
BEKLENEN_RSSI_DBM: float = -55.0  # §III.B'nin örneği (eşitlik bozma)

# ---------------------------------------------------------------- DSR §9
REQUEST_PERIOD_S: float = 0.5
MAX_REQUEST_PERIOD_S: float = 10.0
MAX_REQUEST_REXMT: int = 16
BROADCAST_JITTER_S: float = 0.010
ROUTE_CACHE_TIMEOUT_S: float = 300.0

# ---------------------------------------------------------------- SEÇİM
# 🔴 Makale ve DSR susuyor → GEÇİCİ SEÇİM, duyarlılığı ölçülür.
#   `t_wait`: RREQ'nun düğüm-ayrık seçenekleri hedefe yayın titreşimi
#   (≤ 10 ms/atlama) ve kanal erişimiyle birkaç on ms içinde ulaşır; 0,1 s
#   bunları toplar ve kaynağın ilk yeniden denemesinden (RequestPeriod
#   0,5 s) kısadır — RREP yeniden denemeden önce döner.
#   Eş. 6 · 7: makalede değer yok. Süzgeçler yarı yarıya (0,5: geçmiş ve
#   son ölçüm eşit ağırlıklı).
T_WAIT_S: float | None = 0.1
YUK_KANAL_SUZGECI: float | None = 0.5     # Eş. 6
YUK_KUYRUK_SUZGECI: float | None = 0.5    # Eş. 7

# ---------------------------------------------------------------- Tablo 2
# Eş. 8 — makalenin örneğinden çözüldü (beyan tablosu).
YUK_KANAL_AGIRLIGI: float | None = 0.5    # γ (süzgeç kazancı)
YUK_DUZELTME: float | None = 0.02         # ε (düzeltme çarpanı)
