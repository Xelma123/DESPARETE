"""
OLSRv2 mesaj biçimleri, sabitleri ve beyan tablosu — TEK KAYNAK.

Kaynaklar (`v2/02` R5): RFC 7181 (OLSRv2) · RFC 6130 (NHDP) · RFC 5444 (tel
biçimi) · RFC 5497 (zaman TLV'leri) · RFC 5148 (titreşim) · RFC 7779 (DAT
metriği) · güncelleyenler RFC 7183 · 7187 · 7188 · 7466. Hakem olsrd2 (OONF,
`protokol_kaynaklari/uygulama_kaynaklari/olsrd2/`, commit `477e716`).
Gerçekleme ilkesi (K-229): RFC'nin MUST ve SHOULD'u uygulanır, MAY beyan
edilir; olsrd2 yalnız RFC'nin seçeneğe bıraktığı yerde hakemdir, RFC dışı
eklemeleri alınmaz. Tasarım notu `arsiv/teshis/olsrv2_2026-10-11/tasarim.md`.

🔒 TEL BİÇİMİ — RFC 5444 BAYT BAYT
==================================
Paket `olsrv2_rfc5444.py` ile RFC 5444'e göre kodlanır ve tekrarlı 8 bitlik
tek alanda taşınır (`HELLO` · `TC`); boyut gerçek tel boyutudur. Paket
başlığı 3 bayt (paket sıra numarası, DAT için). HELLO başlığı 8 bayt (kaynak
adresi), TC başlığı 12 bayt (kaynak · hop limit · hop count · sıra).

🔴 BEYAN TABLOSU — RFC'nin seçeneğe bıraktığı her yer
=====================================================
| konu | RFC | gerçekleme | dayanak |
|---|---|---|---|
| adres modeli | serbest | tek arayüz, tek adres; kaynak adresi = arayüz adresi (RFC 7181 §7 izinli); düğüm k → 10.0.0.0 + k + 1 | simülatörde her İHA'nın tek telsizi var |
| bağ kalitesi (NHDP §14) | MAY | yok; HYST_ACCEPT 1 · HYST_REJECT 0 · INITIAL_QUALITY 1 · INITIAL_PENDING false (NHDP §15.4) | metrik DAT'ta; olsrd2 varsayılanı histerezissiz |
| bağ metriği | dış süreç (RFC 7181 §8.1) | DAT (RFC 7779) | `v2/02` R5 |
| DAT gelen hız L_DAT_rx_bitrate | dış süreç; sabit yapılandırma açıkça izinli (RFC 7779 §8) | sabit 1 Mbit/s (802.11b temel hızı) | gözlemde komşu başına alınan hız yok; tek değer Dijkstra'nın sonucunu değiştirmez; olsrd2'nin `ffdat_airtime=false` kipi aynı (ETX'e iner) |
| DAT kayıp histerezisi, hız süzgeci | bilgilendirici (RFC 7779 Ek C · D) | yok | normatif değil |
| yayın ↔ tek-yayın alım olasılığı | RFC 7779 §3 uyarısı | 802.11b yayını temel hızda: kayıp tahmini tek-yayın için iyimser | simülatörün MAC'i değişmez |
| simetrik olmayan göndericinin TC'si (§14.2 adım 1) | İSTEĞE BAĞLI | işlenir | olsrd2 işler |
| ilan edilen komşular (§17.3 madde 5) | MAY | yalnız yönlendirme MPR seçicileri | olsrd2; SHOULD "gereksiz değişimden kaçın" |
| bayrak MPR'lerinde metrik (§18.4) | A ya da B | A: giden bağ metriği | olsrd2 |
| MPR algoritması (§18 · Ek B) | Ek B örnek | Ek B harfiyen: WILL_ALWAYS → tek kapsayan → W, R, D, küçük adres; adım 4 yok (İSTEĞE BAĞLI) | §18.1: istek SHOULD dikkate alınır (olsrd2 istek adımını atlıyor) |
| yönlendirme MPR'lerinde d2(x, y) (§18.5) | metin "N2_out_metric" | N2_in_metric | RFC'nin kendi içinde çelişki: aynı paragrafın izin koşulu N2_in_metric'e, §4.6 "routing MPRs use incoming neighbor metrics" der; olsrd2 gelen metriği kullanır |
| RFC 7187 yönlendirme MPR iyileştirmesi | MAY | yok | olsrd2'de yok |
| 2-atlama rota kenarları (§19.1 · Ek C.7) | İSTEĞE BAĞLI | var; yalnız başka yolu olmayan ve omurga düğümü (komşu ya da TC kaynağı) olmayan hedefe; metrik N2_out_metric | olsrd2 kullanır; Ek C.7'nin metninde "N_out_metric" yazıyor, §19.1'in normatif kenar metriği N2_out_metric (olsrd2 de) |
| eşit metrikte atlama (§19.2) | SHOULD | az atlamalı; eşitse komşu tercihi (Ek C.1: N_will_routing, MPR seçicisi), sonra küçük adres | RFC |
| değişime yanıt HELLO/TC (NHDP §13 · §15.2 · §16.2) | MAY | yok, yalnız periyodik | olsrd2 periyodik |
| periyodik üretim titreşimi | SHOULD (RFC 5148 §5.1) | aralık U(0, HP_MAXJITTER) · U(0, TP_MAXJITTER) kısalır | RFC 5148 |
| iletme titreşimi | SHOULD (RFC 5148 §5.3) | U(0, F_MAXJITTER) gecikme | RFC 5148 · RFC 7181 §13.2 |
| mesajların pakette birleştirilmesi (§13.2) | SHOULD (aynı anda gönderilenler) | her pakette tek mesaj | bağımsız titreşimli zamanlayıcılarda iki mesaj aynı anda çıkmaz |
| HELLO'da INTERVAL_TIME | SHOULD (periyodik) | var | NHDP §10.1 |
| TC'de INTERVAL_TIME | MAY | var | olsrd2 |
| TC'de hop count | MAY (tek değerli zaman TLV'sinde) | var | olsrd2 koyar ve ister |
| TC'de gelen komşu metriği | yok | konmaz (yalnız giden, MUST) | olsrd2 ekliyor, RFC istemiyor |
| bütünlük koruması (RFC 7183) | gerçeklemede MUST, kurulumda SHOULD | kullanılmaz | tehdit modelinde mesaj sahteciliği yok (içeriden saldırılar kapsam dışı, K-230); öteki rakipler de imzasız; olsrd2'de ayrı eklenti, varsayılan kapalı |
| RFC 7466 (kayıp 2-atlama demetleri) | bağ kalitesiyle seçenek | uygulanmaz | bağ kalitesi kullanılmıyor |
| bağ katmanı bildirimi | tanımsız | kullanılmaz | OLSR v1'de de kapalı (K-196) |
| veri tamponu | tanımsız | yok, rota yoksa paket düşer | proaktif; OLSR v1 ile aynı |
"""

from __future__ import annotations

from sim2.gozlem.kontrol import MesajBicimi

__all__ = [
    "HELLO", "TC",
    "HELLO_INTERVAL_S", "HELLO_MIN_INTERVAL_S", "REFRESH_INTERVAL_S",
    "H_HOLD_TIME_S", "L_HOLD_TIME_S", "N_HOLD_TIME_S", "I_HOLD_TIME_S",
    "HP_MAXJITTER_S", "HT_MAXJITTER_S",
    "TC_INTERVAL_S", "TC_MIN_INTERVAL_S", "T_HOLD_TIME_S", "A_HOLD_TIME_S",
    "RX_HOLD_TIME_S", "P_HOLD_TIME_S", "F_HOLD_TIME_S", "O_HOLD_TIME_S",
    "TP_MAXJITTER_S", "TT_MAXJITTER_S", "F_MAXJITTER_S", "TC_HOP_LIMIT",
    "WILL_NEVER", "WILL_DEFAULT", "WILL_ALWAYS", "WILL_FLOODING",
    "WILL_ROUTING", "MINIMUM_METRIC", "MAXIMUM_METRIC",
    "DAT_MAXIMUM_LOSS", "DAT_MINIMUM_BITRATE", "DAT_MEMORY_LENGTH",
    "DAT_REFRESH_INTERVAL_S", "DAT_HELLO_TIMEOUT_FACTOR",
    "DAT_SEQNO_RESTART_DETECTION", "DAT_RX_BITRATE_BPS",
    "MSG_HELLO", "MSG_TC", "MTLV_INTERVAL_TIME", "MTLV_VALIDITY_TIME",
    "MTLV_MPR_WILLING", "MTLV_CONT_SEQ_NUM", "CONT_COMPLETE",
    "ATLV_LOCAL_IF", "ATLV_LINK_STATUS", "ATLV_OTHER_NEIGHB",
    "ATLV_LINK_METRIC", "ATLV_MPR", "ATLV_NBR_ADDR_TYPE",
    "THIS_IF", "LOST", "SYMMETRIC", "HEARD", "MPR_FLOODING", "MPR_ROUTING",
    "ROUTABLE_ORIG", "ORIGINATOR", "ROUTABLE", "METRIK_GELEN_BAG",
    "METRIK_GIDEN_BAG", "METRIK_GELEN_KOMSU", "METRIK_GIDEN_KOMSU",
    "ADRES_TABANI",
]

# ---------------------------------------------------------------- biçimler
# Tekrarlı tek alan: RFC 5444 paketinin baytları (`olsrv2_rfc5444.py`).
HELLO = MesajBicimi("HELLO", (), tekrarli=(("rfc5444", 8),))
TC = MesajBicimi("TC", (), tekrarli=(("rfc5444", 8),))

# ---------------------------------------------------------------- RFC 6130 §15
HELLO_INTERVAL_S: float = 2.0
HELLO_MIN_INTERVAL_S: float = HELLO_INTERVAL_S / 4
REFRESH_INTERVAL_S: float = HELLO_INTERVAL_S
H_HOLD_TIME_S: float = 3 * REFRESH_INTERVAL_S
L_HOLD_TIME_S: float = H_HOLD_TIME_S
N_HOLD_TIME_S: float = L_HOLD_TIME_S
I_HOLD_TIME_S: float = N_HOLD_TIME_S
HP_MAXJITTER_S: float = HELLO_INTERVAL_S / 4
HT_MAXJITTER_S: float = HP_MAXJITTER_S

# ---------------------------------------------------------------- RFC 7181 §20
O_HOLD_TIME_S: float = 30.0
TC_INTERVAL_S: float = 5.0
TC_MIN_INTERVAL_S: float = TC_INTERVAL_S / 4
T_HOLD_TIME_S: float = 3 * TC_INTERVAL_S
A_HOLD_TIME_S: float = T_HOLD_TIME_S
RX_HOLD_TIME_S: float = 30.0
P_HOLD_TIME_S: float = 30.0
F_HOLD_TIME_S: float = 30.0
TP_MAXJITTER_S: float = HP_MAXJITTER_S
TT_MAXJITTER_S: float = HT_MAXJITTER_S
F_MAXJITTER_S: float = TT_MAXJITTER_S
TC_HOP_LIMIT: int = 255

# ---------------------------------------------------------------- RFC 7181 §5.6
WILL_NEVER: int = 0
WILL_DEFAULT: int = 7
WILL_ALWAYS: int = 15
WILL_FLOODING: int = WILL_DEFAULT       # §20.7
WILL_ROUTING: int = WILL_DEFAULT
MINIMUM_METRIC: int = 1
MAXIMUM_METRIC: int = 16776960

# ---------------------------------------------------------------- RFC 7779
DAT_MAXIMUM_LOSS: int = 8               # §6
DAT_MINIMUM_BITRATE: int = 1000
DAT_MEMORY_LENGTH: int = 64             # §7.1
DAT_REFRESH_INTERVAL_S: float = 1.0
DAT_HELLO_TIMEOUT_FACTOR: float = 1.2
DAT_SEQNO_RESTART_DETECTION: int = 256
# 🔴 Beyan tablosu: §8'in "static configuration" seçeneği — 802.11b temel
# hızı (simülatörde yayınların ve onayların hızı).
DAT_RX_BITRATE_BPS: int = 1_000_000

# ---------------------------------------------------------------- IANA
MSG_HELLO, MSG_TC = 0, 1                         # RFC 6130 §18.2 · 7181 §24.1
MTLV_INTERVAL_TIME, MTLV_VALIDITY_TIME = 0, 1    # RFC 5497 §7
MTLV_MPR_WILLING, MTLV_CONT_SEQ_NUM = 7, 8       # RFC 7181 §24.4
CONT_COMPLETE = 0
ATLV_LOCAL_IF, ATLV_LINK_STATUS, ATLV_OTHER_NEIGHB = 2, 3, 4   # RFC 6130
ATLV_LINK_METRIC, ATLV_MPR, ATLV_NBR_ADDR_TYPE = 7, 8, 9       # RFC 7181
THIS_IF = 0
LOST, SYMMETRIC, HEARD = 0, 1, 2
MPR_FLOODING, MPR_ROUTING = 1, 2                 # bit alanı (RFC 7188)
ORIGINATOR, ROUTABLE, ROUTABLE_ORIG = 1, 2, 3
# LINK_METRIC değerinin 0–3. bitleri (16 bitlik değerin en anlamlı dördü).
METRIK_GELEN_BAG = 0x8000
METRIK_GIDEN_BAG = 0x4000
METRIK_GELEN_KOMSU = 0x2000
METRIK_GIDEN_KOMSU = 0x1000

# Adres modeli (beyan tablosu): düğüm k → 10.0.0.0 + k + 1.
ADRES_TABANI: int = 0x0A000000
