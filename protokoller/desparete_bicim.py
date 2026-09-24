"""
DESPARETE mesaj biçimleri — tel biçiminin alan düzeni. TEK KAYNAK.

Kaynak: `protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/19_DESPARETE_WIRE_FORMAT_TLV.md`
§2–§11 · §14. Kararlar: `v2/04` K-150 · K-152.

🔒 BOYUT ALANLARDAN TÜRER — PROTOKOL BİR BAYT YAZAMAZ
=====================================================
`MesajBicimi` alanları BİT genişliğiyle listeler ve boyutu kendisi hesaplar
(`13` §02.1). Aşağıdaki genişlikler `19`'un alan diyagramlarından birebir;
toplamlar `19` §14'ün bastığı en küçük başlık boylarına eşittir ve bu bir
TESTLE bağlıdır (`tests2/test_desparete.py`). Her kontrol biçimi 4 baytlık
taban başlıkla (§2) başlar; beş kontrol türü ardından 24 baytlık Kontrol
Gönderen Bloğunu (§5) taşır.

🔴 BİR ÇELİŞKİ — DFSN_REQUEST (K-152 §6)
========================================
`19` §8 ve §14 çekirdek gövdeyi **44** bayt (toplam 72) yazıyor; aynı
bölümün alan diyagramı ise İstek Sırası'ndan sonra **32 bitlik bir Reserved**
gösteriyor ve alanlarının toplamı **48** bayt (toplam 76). Burada DİYAGRAM
izlendi: (1) simülatörün sözleşmesi boyutu alanlardan türetir; (2) istek
kimliği bloğu (kimlik 64 · örnek 64 · sıra 32 · ayrılmış 32) Kontrol Gönderen
Bloğunun birebir aynısı ve o blok 24 bayttır; (3) aynı deseni taşıyan
PROBE_REPLY ve FAILURE_REPORT, ayrılmış 32 biti boyutlarına KATIYOR — 44,
toplamada o alanın unutulmasından çıkıyor. Fark 4 bayt; öğrencinin kararına
açık.

🔒 SİMÜLASYONA EŞLEME — beyan
=============================
  · Tel üstü kimlikler 64 bit ve **0 geçersiz**; simülatörün düğüm numaraları
    0'dan başlar → tel kimliği `düğüm + 1` (`tel_kimligi`).
  · Simülasyonda yeniden başlatma yok → her düğümün örnek kimliği ve her
    hedefin OIID'si sabit `1`.
  · Güvenlik Profili 1 (Ed25519 AUTHENTICATION TLV) ana karşılaştırmada
    KAPALI (K-150 §4); burada yalnız uzantısız biçimler var. Bayt bedeli ayrı
    kolda ölçülecek.
  · Taşıyıcı kapsüllemesi (`19` §1: kapsam dışı) simülatörün bütün
    protokollere AYNI uyguladığı kontrol kapsüllemesidir.
"""

from __future__ import annotations

from sim2.gozlem.kontrol import MesajBicimi

__all__ = [
    "SURUM", "TIP_DATA", "TIP_FIELD_UPDATE", "TIP_FIELD_SOLICIT",
    "TIP_DFSN_REQUEST", "TIP_PROBE", "TIP_PROBE_REPLY", "TIP_FAILURE_REPORT",
    "DATA", "FIELD_UPDATE", "FIELD_SOLICIT", "DFSN_REQUEST", "PROBE",
    "PROBE_REPLY", "FAILURE_REPORT", "KONTROL_BICIMLERI", "VERI_BASLIK_BAYT",
    "tel_kimligi", "DURUM_REACHABLE",
    "T_FRESH_S", "T_IDLE_PROBE_S", "T_PROBE_REPLY_S", "J_PROBE_S",
    "T_PROBE_START_S", "N_PROBE", "T_PROBE_ARA_S", "T_PROBE_SESSION_S",
    "T_RETENTION_S", "T_ADV_REFRESH_S", "J_ADV_S", "L_ADV_SENT_KUANTA",
    "DURUM_WITHDRAWAL", "L_ADV_MAX_S", "OMUR_KUANTA_S", "T_COALESCE_S",
    "T_URGENT_S", "T_ADV_CACHE_S", "T_WITHDRAW_CACHE_S", "T_REPAIR_MAX_S",
    "H_DATA", "G_ADV_REFRESH_S", "T_SOLICIT_REPLY_S", "T_SOLICIT_BACKOFF_S",
    "N_SOLICIT", "H_REQ", "T_REQ_SESSION_S", "T_REQ_RETRY_S", "N_REQ",
    "T_REQ_DUPLICATE_S", "BAYRAK_BAGLAM", "SEBEP_EDINIM", "SEBEP_ACLIK",
    "SEBEP_BELIRSIZLIK", "J_CONTROL_S", "YEREL_TAMPON", "Q_BUFFER_YUZDE",
    "Q_BUFFER_UST", "tampon_kotasi", "TAMPON_KOTASI", "T_CAUTION_EVIDENCE_S",
    "T_PROTECT_EVIDENCE_S", "T_RECOVERY_EVIDENCE_S", "T_PROTECT_MIN_S",
    "PROBE_YANIT_ISTE", "K_YEDEK_CANLI",
]

SURUM = 1                                  # §2 — `Ver = 1`

# §3 — paket türleri
TIP_DATA = 0
TIP_FIELD_UPDATE = 1
TIP_FIELD_SOLICIT = 2
TIP_DFSN_REQUEST = 3
TIP_PROBE = 4
TIP_PROBE_REPLY = 5
TIP_FAILURE_REPORT = 6

# §2 — Ver(4) · Type(4) · Header Length(8) · Hop Limit(8) · Base Flags(8)
_TABAN: tuple[tuple[str, int], ...] = (
    ("surum", 4), ("tip", 4), ("baslik_uzunlugu", 8), ("hop_siniri", 8),
    ("taban_bayraklari", 8))
# §5 — Sender-ID(64) · Sender-Instance-ID(64) · Message Sequence(32) ·
#      Reserved(32) = 24 bayt
_GONDEREN: tuple[tuple[str, int], ...] = (
    ("gonderen", 64), ("gonderen_ornek", 64), ("mesaj_sira", 32),
    ("gonderen_ayrilmis", 32))

# §4 — DATA çekirdeği 32 bayt → uzantısız başlık 36 bayt. Veri paketine
# eklenen yönlendirme başlığıdır; kontrol mesajı DEĞİLDİR, burada yalnız
# boyutunun alanlardan türemesi için bir `MesajBicimi` olarak durur.
DATA = MesajBicimi("DATA", _TABAN + (
    ("uygulama_hedefi", 64), ("veri_kaynagi", 64), ("veri_kaynagi_ornek", 64),
    ("veri_sira", 32), ("trafik_sinifi", 8), ("dbayraklar", 8),
    ("kopya_butcesi", 8), ("veri_ayrilmis", 8)))

# §6 — Destination-ID(64) · OIID(64) · DFSN(32) · ADS(32) · Potential(32) ·
#      Lifetime(16) · State(8) · Flags(8) = 32 bayt → toplam 60
FIELD_UPDATE = MesajBicimi("FIELD_UPDATE", _TABAN + _GONDEREN + (
    ("hedef", 64), ("oiid", 64), ("dfsn", 32), ("ads", 32),
    ("potansiyel", 32), ("omur", 16), ("durum", 8), ("alan_bayraklari", 8)))

# §7 — Destination-ID(64) · Known OIID(64) · Known DFSN(32) · SFlags(8) ·
#      Reserved(24) = 24 bayt → toplam 52
FIELD_SOLICIT = MesajBicimi("FIELD_SOLICIT", _TABAN + _GONDEREN + (
    ("hedef", 64), ("bilinen_oiid", 64), ("bilinen_dfsn", 32),
    ("sbayraklar", 8), ("solicit_ayrilmis", 24)))

# §8 — Requester-ID(64) · Requester-Instance-ID(64) · Request Sequence(32) ·
#      Reserved(32) · Destination-ID(64) · Known OIID(64) ·
#      Requested-Minimum-DFSN(32) · Reason(8) · RFlags(8) · Reserved(16)
#      = 48 bayt → toplam 76 (belgenin metni 44 / 72 — başlıktaki not)
DFSN_REQUEST = MesajBicimi("DFSN_REQUEST", _TABAN + _GONDEREN + (
    ("isteyen", 64), ("isteyen_ornek", 64), ("istek_sira", 32),
    ("istek_ayrilmis", 32), ("hedef", 64), ("bilinen_oiid", 64),
    ("istenen_en_az_dfsn", 32), ("sebep", 8), ("rbayraklar", 8),
    ("istek_ayrilmis2", 16)))

# §9 — Target-Neighbour-ID(64) · Probe Flags(8) · Reserved(24) = 12 bayt
#      → toplam 40
PROBE = MesajBicimi("PROBE", _TABAN + _GONDEREN + (
    ("hedef_komsu", 64), ("probe_bayraklar", 8), ("probe_ayrilmis", 24)))

# §10 — Original Requester-ID(64) · Original Requester-Instance-ID(64) ·
#       Probe Message Sequence(32) · Reserved(32) = 24 bayt → toplam 52
PROBE_REPLY = MesajBicimi("PROBE_REPLY", _TABAN + _GONDEREN + (
    ("asil_isteyen", 64), ("asil_isteyen_ornek", 64), ("probe_sira", 32),
    ("yanit_ayrilmis", 32)))

# §11 — Report-Destination-ID(64) · Failed Data Source-ID(64) · …-Instance-ID
#       (64) · Failed Data Sequence(32) · Reserved(32) · Failed Application
#       Destination-ID(64) · Failed OIID(64) · Failed DFSN(32) · Reason(8) ·
#       FFlags(8) · Reserved(16) = 56 bayt → toplam 84
FAILURE_REPORT = MesajBicimi("FAILURE_REPORT", _TABAN + _GONDEREN + (
    ("rapor_hedefi", 64), ("basarisiz_kaynak", 64),
    ("basarisiz_kaynak_ornek", 64), ("basarisiz_sira", 32),
    ("rapor_ayrilmis", 32), ("basarisiz_uygulama_hedefi", 64),
    ("basarisiz_oiid", 64), ("basarisiz_dfsn", 32), ("sebep", 8),
    ("fbayraklar", 8), ("rapor_ayrilmis2", 16)))

KONTROL_BICIMLERI: tuple[MesajBicimi, ...] = (
    FIELD_UPDATE, FIELD_SOLICIT, DFSN_REQUEST, PROBE, PROBE_REPLY,
    FAILURE_REPORT)

# FIELD_UPDATE.State (§6)
DURUM_REACHABLE = 0
DURUM_WITHDRAWAL = 1

# ==========================================================================
# `21` · Dengeli Zamanlama Profili v0.1 — öğrencinin onayladığı değerler,
# birebir. Hiçbiri bu projede seçilmedi. Zaman ilişkileri (TR-01 … TR-12,
# `20` §4) TESTLE bağlı.
# ==========================================================================
# §1 — profilin çalışma varsayımı: tek atlamalı kontrol titreşimi üst sınırı.
# Yayınlanan FIELD_SOLICIT ve iletilen DFSN_REQUEST bununla titreşir; aynı
# dalgayı duyan komşuların aynı anda yeniden yayınlayıp çarpışmaması için.
J_CONTROL_S = 0.1
# §2.1 — komşu doğrulama
T_FRESH_S = 3.0             # ACTIVE tutulma süresi (son iki yönlü kanıttan)
T_IDLE_PROBE_S = 2.0        # kanıtsız ACTIVE komşuya boşta PROBE
T_PROBE_REPLY_S = 0.5       # eşleşen yanıt bekleme
J_PROBE_S = 0.1             # PROBE zamanlama titreşimi üst sınırı
T_PROBE_START_S = 0.1       # oturum başlatma üst gecikmesi (= J_PROBE_S ile)
N_PROBE = 2                 # nitelik / hata oturumunda en çok deneme
T_PROBE_ARA_S = 0.2         # denemeler arası en az bekleme
T_PROBE_SESSION_S = 1.3     # 0,1 + 0,5 + 0,2 + 0,5
T_RETENTION_S = 5.0         # kayıt saklama üst süresi
# §2.2 — alan ilanı
T_ADV_REFRESH_S = 1.0       # FIELD_UPDATE tazeleme aralığı
J_ADV_S = 0.2               # tazeleme titreşimi üst sınırı
L_ADV_SENT_KUANTA = 30      # Lifetime = 3,0 s (100 ms kuanta)
L_ADV_MAX_S = 3.0           # alıcının kabul ettiği en uzun ilan ömrü
OMUR_KUANTA_S = 0.1         # Lifetime alanının birimi (`19` §6)
T_COALESCE_S = 0.2          # olağan tetik ilanı birleştirme / alan başına 5/s
T_URGENT_S = 0.1            # ardıl değişimi · potansiyel artışı · withdrawal
T_ADV_CACHE_S = 4.0         # süresi dolmuş sonlu ilanın sıra bilgisi
T_WITHDRAW_CACHE_S = 4.0    # withdrawal'ın sıra bilgisi
# §2.2 — ilan koruması
G_ADV_REFRESH_S = 1.5       # seçili ilan bitmeden FIELD_SOLICIT payı
# §2.3 — edinim ve onarım
T_SOLICIT_REPLY_S = 0.4     # bir FIELD_SOLICIT'e yanıt bekleme
T_SOLICIT_BACKOFF_S = 0.2   # iki solicit arası en az
N_SOLICIT = 2               # bir edinimde en çok solicit
H_REQ = 16                  # DFSN_REQUEST başlangıç Hop Limit
T_REQ_SESSION_S = 4.0       # istek oturumunun toplam ömrü
T_REQ_RETRY_S = 1.0         # yeni Request-ID'li ikinci dalgadan önce en az
N_REQ = 2                   # bir oturumda en çok istek dalgası
T_REQ_DUPLICATE_S = 4.0     # Request-ID tekrar önbelleği
T_REPAIR_MAX_S = 6.0        # REPAIRING'in üst sınırı
# `19` §7 · §8 — bayraklar ve istek nedenleri
BAYRAK_BAGLAM = 1           # SFlags / RFlags bit 0: HAS_CONTEXT
SEBEP_EDINIM = 0
SEBEP_ACLIK = 1             # FEASIBLE_STARVATION
SEBEP_BELIRSIZLIK = 2       # freshness ambiguity
# §2.4 — veri
H_DATA = 16                 # DATA başlangıç Hop Limit
# `Q_buffer[field, class 0]`: yerel onarım tamponunun en çok %10'u ve en çok
# 32 paket; küçüğü uygulanır. Yerel tampon = simülatörün bütün protokollere
# ortak rota tamponu kapasitesi (K-152 §3; test `Konfig`le bağlar) → 6.
YEREL_TAMPON = 64
Q_BUFFER_YUZDE = 10
Q_BUFFER_UST = 32


def tampon_kotasi(yerel: int = YEREL_TAMPON) -> int:
    """Alan başına kota — tam sayı aritmetiğiyle: kayan noktalı yüzde,
    tam sayıya denk gelen sınırda aşağı kırpılınca bir eksik verebilir."""
    return min(yerel * Q_BUFFER_YUZDE // 100, Q_BUFFER_UST)


TAMPON_KOTASI = tampon_kotasi()

# K-163 V1 — PROBE Flags bit 0: "yanıt iste" (ayrılmış bit; seçenek kapalıyken 0)
PROBE_YANIT_ISTE = 1
# K-165 V2+ — canlı tutulan yedek sayısı (ardıl dışında). Ajanın ADAY
# parametresi, tasarım paketinde karşılığı yok; ölçülmeden sabitlenmez.
K_YEDEK_CANLI = 2

# §2.5 — politika kanıtı ve bekleme (`22` §7; eşikler M0.1'de, `35` §5)
T_CAUTION_EVIDENCE_S = 1.5  # STEADY → CAUTION için kesintisiz kanıt
T_PROTECT_EVIDENCE_S = 2.5  # CAUTION → PROTECT için kesintisiz kanıt
T_RECOVERY_EVIDENCE_S = 4.0  # CAUTION → STEADY · PROTECT → CAUTION
T_PROTECT_MIN_S = 2.0       # PROTECT'te en az kalış (güvenlik kaybında yok)

# Y2 · K-151 — her veri paketine eklenen yönlendirme başlığı, ALANLARDAN.
VERI_BASLIK_BAYT: int = DATA.sabit_bit // 8


def tel_kimligi(dugum: int) -> int:
    """Simülatör düğüm numarası → tel üstü 64 bitlik kimlik (0 geçersiz)."""
    if not (isinstance(dugum, int) and 0 <= dugum < (1 << 64) - 1):
        raise ValueError(f"geçersiz düğüm numarası: {dugum!r}")
    return dugum + 1
