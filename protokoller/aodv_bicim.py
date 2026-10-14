"""
AODV mesaj biçimleri ve RFC 3561 sabitleri — TEK KAYNAK.

🔒 NEDEN AYRI DOSYA
===================
Biçimler ve sabitler RFC'nin **alıntısıdır**; protokolün mantığı değildir.
Ayrı durunca iki şey kazanılıyor: (1) uygunluk testleri (`U1–U4`) boyutları
protokolü hiç kurmadan sınayabiliyor, (2) bir sabitin nereden geldiği tek bir
yerde okunuyor ve `aodv.py` onu yeniden yazmıyor.

🔴 BOYUT RFC ALANLARINDAN TÜRER — PROTOKOL BİR BAYT YAZAMAZ
============================================================
`MesajBicimi` alanları BİT genişliğiyle listeler ve boyutu kendisi hesaplar
(`13` §02.1, sözleşme kararı 1). Aşağıdaki genişlikler RFC 3561 §5'in paket
tablolarından birebir alınmıştır ve toplamları RFC'nin bastığı bayt
sayılarına **birebir** oturur:

    RREQ  24 bayt   ·   RREP  20 bayt   ·   RERR  4 + 8 × hedef

⚠️ Bu üç eşitlik bir TESTLE bağlıdır (`tests2/test_aodv.py`). Bir alan
genişliği yanlış yazılırsa toplam tutmaz ve test konuşur — yani "RFC'ye sadık"
iddiası bir cümle değil, bir ölçüm.

🔴 AYRIŞMANIN KAYNAĞI: IPv4 BAŞLIĞI ZATEN ÖDENİYOR
==================================================
RFC'de RREQ'in TTL'i **IP başlığındadır** ve o başlık `KONTROL_KAPSULLEME`de
zaten 20 bayt olarak faturalanıyor (`13` §03.1). Ama simülatörün kontrol
düzleminde bir çerçeveye "IP TTL" koymanın yolu yok: yük, biçimle birebir
eşleşmek zorunda. Bu yüzden TTL **yükte taşınıyor** ve bir bayt fazladan
ödeniyor.

    ölçülen bedel : RREQ 24 → 25 bayt (çerçevede 88 → 89 bayt, %1,1)
    yönü          : AODV'yi olduğundan biraz PAHALI gösterir

🔒 Yön bilinçli seçildi: kaçağa değil, GÜVENLİ tarafa doğru — `gozlem/yuk.py`
alan adlarını faturalarken aynı kararı vermişti. `nrl_*` karşılaştırmasında
AODV'nin lehine bir sapma OLMADIĞI böylece garanti.

🔴 UYGULANMAYAN RFC ÖZELLİKLERİ — beyan edilir (`06` §4.4 madde 4)
==================================================================
| özellik | RFC | neden yok |
|---|---|---|
| yerel onarım | §6.12 | RFC'de OPSİYONEL; `LOCAL_ADD_TTL`, `MAX_REPAIR_TTL` ve `MIN_REPAIR_TTL` yeni parametreler getirir ve üçü de ölçülmemiş olurdu |
| RREP-ACK MESAJI (yalnız mesaj) | §5.4 | 🟢 **Kara liste UYGULANIYOR (§6.8, K-194)** — tetiği RREP'in bağ katmanı onayının gelmemesi: RFC *"Such failures can be detected via the absence of a link-layer or network-layer acknowledgment (e.g., RREP-ACK)"*. Bu gerçeklemede tek yönlü (unicast) giden TEK kontrol mesajı RREP'tir (RREQ ve RERR yayın), yani `iletim_basarisiz(tur="kontrol")` tam olarak "RREP iletimi başarısız" demektir; ayrı bir RREP-ACK mesajı ek bayt dışında bilgi getirmez. 🔴 Eski gerekçe ("bağ SİMETRİKTİR") referans dünyada geçersizdi: ortalama güç simetrik ama karıştırıcı gücü ve ED susturması ALICIDA/VERİCİDE ayrı etki eder — bağ fiziksel olarak tek yönlü olabilir (denetim O-1) |
| karşılıksız RREP (G bayrağı) | §6.6.3 | kaynağa geri yol zaten RREQ'in ters rotasından kuruluyor; G bayrağı ek bir eniyileme |
| çok arayüzlü düğüm · alt ağ öneki | §5.2 Prefix Sz | tek arayüz, düz adresleme |

🔒 K-242 (denetim DD-04) — ÜÇ SAPMA KAPANDI, `AODV-k`
====================================================
  · §6.2'nin ÖNCEKİ ATLAMA ömrü UYGULANDI. Eski beyanın gerekçesi
    ("gözlem yüzeyi sınırı: paket kimden alındığını taşımaz") geçersizdi:
    RFC'nin önceki atlaması *"along the reverse path back to the IP
    source"*, yani kaynağa giden girdinin sonraki atlamasıdır — rota
    tablosundan bilinir (ns-3 `RouteInput`: `toOrigin.GetNextHop()`).
    O komşunun canlılığı da tazelenir (ns-3 `m_nb.Update`; RFC §6.9 "any
    packets"), yalnız zaten komşuysa: ölü bir komşu veriyle diriltilmez.
  · Yayınlarda TİTREŞİM (RFC susuyor → ns-3): RREQ üretimi ve iletimi,
    HELLO ve RERR `U(0, YAYIN_TITRESIMI_S)` gecikmeyle (ns-3 her birinde
    `GetInteger(0, 10)` ms). Beyan: ns-3 tam sayı ms çeker, simülatör
    sürekli `U(0, 10 ms)`; HELLO zamanlayıcısının başlangıç fazı ns-3'te
    `U(0, 100 ms)`, burada simülatörün periyodik zamanlayıcı fazı
    `U(0, HELLO_INTERVAL)` (`13` §03.5) — daha dağınık, eşzamanlılık daha az.
  · MY_ROUTE_TIMEOUT = 2 · max(PATH_DISCOVERY_TIME, ACTIVE_ROUTE_TIMEOUT)
    = 11,2 s. RFC §10'un metni *"MUST be at least 2 * PATH_DISCOVERY_TIME"*
    der, aynı bölümün tablosu 2 · ACTIVE_ROUTE_TIMEOUT (6 s); çelişkide
    MUST ve ns-3 (aynı formül, altında `NS_ABORT`).
Üçü de AODV'yi zayıflatıyordu. `AOMDV-f` aynı çekirdeği miras alır; onun
kayıtlı regresyon satırları da değişir (Faz 4'ün kaydı, rakip değil).

⚠️ Bu sapmalar AODV'yi **zayıflatır mı?** RREP-ACK mesajının yokluğu hayır
(kara liste bağ katmanı onayıyla tetikleniyor, K-194), G bayrağı bir
eniyileme, önek tek arayüzde anlamsız.
Yerel onarım EVET zayıflatabilir ve bu açıkça yazılıyor: karıştırma altında
kopma sıktır ve yerel onarım tam orada iş görür. Ölçüm raporlanırken bu sapma
sonucun yanında anılır.

🔒 SADAKAT DENETİMİ (K-208, `arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md`)
===============================================================================
Kod RFC 3561'e kural kural karşılaştırıldı; ns-3 yalnız RFC'nin sustuğu ya
da çeliştiği yerde hakem. İki hakem kararı:
  · §6.1 ("sırayı RREQ'tekiyle büyüğüne çıkar") ile §6.6.1 ("yalnız bir
    fazlasıysa artır") çelişir → ns-3 gibi §6.6.1.
  · §6.9 HELLO *"only if … part of an active route"*: RFC'nin tanımında etkin
    rota = geçerli girdi → ns-3 gibi HELLO son aralıkta yayın yoksa gider.
ns-3'ün RFC'de olmayan üç eklemesi ALINMADI: rotası RREQ göndereninden geçen
ara düğümün RREQ'i düşürmesi · kaynağın keşifte her RREP'i kabulü · RREP'in
güncelleme olmasa da iletilmesi.
Başlangıç durumu (K-215, `AODV-j`): HELLO'nun "son yayın" anı ve §10
pencereleri −∞'dan başlar; yerel saatin 0 anına çapalı başlangıç sonucu saat
ofsetine bağlı kılıyordu (Faz 4.4 ölçümü; yamalıyken ofsete birebir).
"""

from __future__ import annotations

from sim2.gozlem.kontrol import MesajBicimi

__all__ = [
    "RREQ", "RREP", "RERR",
    "TIP_RREQ", "TIP_RREP", "TIP_RERR",
    "ACTIVE_ROUTE_TIMEOUT_S", "HELLO_INTERVAL_S", "ALLOWED_HELLO_LOSS",
    "NET_DIAMETER", "NODE_TRAVERSAL_TIME_S", "RREQ_RETRIES",
    "MY_ROUTE_TIMEOUT_S", "DELETE_PERIOD_K", "TTL_START", "TTL_INCREMENT",
    "TTL_THRESHOLD", "TIMEOUT_BUFFER", "RREQ_RATELIMIT", "RERR_RATELIMIT",
    "NET_TRAVERSAL_TIME_S", "PATH_DISCOVERY_TIME_S", "DELETE_PERIOD_S",
    "BLACKLIST_TIMEOUT_S", "halka_suresi_s", "SONSUZ_SIRA",
    "YAYIN_TITRESIMI_S",
]

# ==========================================================================
# RFC 3561 §10 · Configuration Parameters
#
# 🔒 BİRİNCİL BELGE AÇILDI (`02` §R1, 8 Eylül 2026; §5 ve §10 16 Eylül'de
# yeniden okundu). Aşağıdaki her satır RFC'nin BASTIĞI değerdir; hiçbiri bu
# projede seçilmedi, dolayısıyla hiçbiri bir kalibrasyon parametresi değildir.
# `06` §4.2: *"Rakipler RFC varsayılanındadır."*
# ==========================================================================
ACTIVE_ROUTE_TIMEOUT_S: float = 3.0        # 3,000 ms
HELLO_INTERVAL_S: float = 1.0              # 1,000 ms
ALLOWED_HELLO_LOSS: int = 2
NET_DIAMETER: int = 35
NODE_TRAVERSAL_TIME_S: float = 0.040       # 40 ms
RREQ_RETRIES: int = 2
DELETE_PERIOD_K: int = 5                   # "K = 5 recommended"
# Genişleyen halka araması (§6.4) — RFC §10'da tanımlı.
TTL_START: int = 1
TTL_INCREMENT: int = 2
TTL_THRESHOLD: int = 7
TIMEOUT_BUFFER: int = 2
# Hız sınırları (§10): saniyede en çok bu kadar RREQ/RERR yayını.
RREQ_RATELIMIT: int = 10
RERR_RATELIMIT: int = 10

# --- RFC'nin kendi TÜRETMELERİ — formülleri belgeden birebir ---------------
NET_TRAVERSAL_TIME_S: float = 2 * NODE_TRAVERSAL_TIME_S * NET_DIAMETER
PATH_DISCOVERY_TIME_S: float = 2 * NET_TRAVERSAL_TIME_S
# 🔒 K-242 (DD-04): §10 "MUST be at least 2 * PATH_DISCOVERY_TIME" → 11,2 s;
# tablo değeri (2 · ACTIVE_ROUTE_TIMEOUT = 6 s) MUST'ı çiğner. ns-3 aynı
# formül: `2 * std::max(m_pathDiscoveryTime, m_activeRouteTimeout)`.
MY_ROUTE_TIMEOUT_S: float = 2 * max(PATH_DISCOVERY_TIME_S,
                                    ACTIVE_ROUTE_TIMEOUT_S)
DELETE_PERIOD_S: float = DELETE_PERIOD_K * max(ACTIVE_ROUTE_TIMEOUT_S,
                                               HELLO_INTERVAL_S)
# §6.8 · §10 — kara liste süresi. Taban tanım `RREQ_RETRIES *
# NET_TRAVERSAL_TIME`; RFC §10: *"BLACKLIST_TIMEOUT should be suitably
# increased if an expanding ring search is used. In such cases, it should be
# {[(TTL_THRESHOLD - TTL_START)/TTL_INCREMENT] + 1 + RREQ_RETRIES} *
# NET_TRAVERSAL_TIME"* — bu gerçekleme halka araması kullanıyor (§6.4):
# (3 + 1 + 2) × 2,8 s = 16,8 s. Seçilmedi, RFC'nin formülü (K-194).
BLACKLIST_TIMEOUT_S: float = (
    ((TTL_THRESHOLD - TTL_START) // TTL_INCREMENT) + 1 + RREQ_RETRIES
) * NET_TRAVERSAL_TIME_S
# 🔒 K-242 (DD-04) · yayın titreşimi — RFC 3561 susar; ns-3 hakem: RREQ
# üretimi/iletimi, HELLO ve RERR `GetInteger(0, 10)` ms sonra gönderilir.
YAYIN_TITRESIMI_S: float = 0.010


def halka_suresi_s(ttl: int) -> float:
    """`RING_TRAVERSAL_TIME` — RFC §10'un formülü, birebir.

        2 * NODE_TRAVERSAL_TIME * (TTL_VALUE + TIMEOUT_BUFFER)
    """
    return 2 * NODE_TRAVERSAL_TIME_S * (ttl + TIMEOUT_BUFFER)


# 🔒 "Bilinmeyen sıra numarası" — RFC §6.1'de hedef sırası bilinmiyorsa RREQ'in
# U bayrağı kurulur. Bayrağı ayrı taşımak yerine 0 ayrılmış değer olarak
# kullanılıyor: RFC'de sıra numaraları 1'den başlar ve 0 hiçbir düğümün
# meşru sırası değildir. Bayrak alanı yine de biçimde duruyor ve BAYTI
# ödeniyor — yani bu bir bedel kaçağı değil, bir kodlama seçimi.
SONSUZ_SIRA: int = 0

# ==========================================================================
# RFC 3561 §5 · Message Formats
#
# 🔒 Genişlikler RFC'nin paket tablolarından. İlk 32 bitlik kelime her üçünde
# de tam oturur; toplamlar RFC'nin bastığı bayt sayılarına eşittir ve bu bir
# TESTLE bağlıdır.
# ==========================================================================

# §5.1 — Type(8) · J R G D U(5) · Reserved(11) · Hop Count(8)
#      · RREQ ID(32) · Dest IP(32) · Dest Seq(32) · Orig IP(32) · Orig Seq(32)
#      = 32 + 160 = 192 bit = 24 bayt ✓
# ⚠️ `ttl` RFC'de IP BAŞLIĞINDADIR; burada yükte taşınıyor ve +1 bayt ödeniyor
# (modül başlığı). Genişliği IPv4'ün TTL alanıyla aynı: 8 bit.
RREQ = MesajBicimi("RREQ", (
    ("tip", 8),
    ("bayraklar", 5),          # J · R · G · D · U
    ("ayrilmis", 11),
    ("atlama", 8),
    ("rreq_kimlik", 32),
    ("hedef", 32),
    ("hedef_sira", 32),
    ("kaynak", 32),
    ("kaynak_sira", 32),
    ("ttl", 8),                # ⚠️ RFC'de IP başlığında — beyanlı +1 bayt
))

# §5.2 — Type(8) · R A(2) · Reserved(9) · Prefix Sz(5) · Hop Count(8)
#      · Dest IP(32) · Dest Seq(32) · Orig IP(32) · Lifetime(32)
#      = 32 + 128 = 160 bit = 20 bayt ✓
# 🔒 HELLO AYRI BİR MESAJ DEĞİLDİR (§6.9): TTL = 1 olan, hedefi kendisi olan
# bir RREP'tir. Bu yüzden HELLO'nun bedeli de 20 bayttır ve ayrı bir biçim
# tanımlanmadı — tanımlansaydı aynı şey iki yerde yazılmış olurdu.
RREP = MesajBicimi("RREP", (
    ("tip", 8),
    ("bayraklar", 2),          # R · A
    ("ayrilmis", 9),
    ("onek_boyu", 5),
    ("atlama", 8),
    ("hedef", 32),
    ("hedef_sira", 32),
    ("kaynak", 32),
    ("omur_ms", 32),
))

# §5.3 — Type(8) · N(1) · Reserved(15) · DestCount(8)
#      + DestCount × (Unreachable Dest IP(32) + Unreachable Dest Seq(32))
#      = 32 bit + 64 bit/hedef = 4 + 8 × n bayt ✓
# 🔒 `tekrarli`: RERR'in ulaşılamaz hedef listesi tam olarak `13` §02.1'in
# *"değeri sayı demeti olan alan"* durumudur ve boyuta `eleman × bit` girer.
RERR = MesajBicimi("RERR", (
    ("tip", 8),
    ("bayraklar", 1),          # N
    ("ayrilmis", 15),
    ("hedef_sayisi", 8),
), tekrarli=(
    ("ulasilamaz", 32),
    ("ulasilamaz_sira", 32),
))

# RFC §5'in tip numaraları.
TIP_RREQ: int = 1
TIP_RREP: int = 2
TIP_RERR: int = 3
