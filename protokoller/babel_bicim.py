"""
Babel — RFC 8966: tel biçimi, sabitler ve beyan tablosu — TEK KAYNAK.

Kaynaklar (`v2/02` G3): RFC 8966, Chroboczek & Schinazi, Ocak 2021,
Standards Track (`protokol_kaynaklari/rfc8966_babel.txt`). Hakem: babeld 1.14
(RFC'nin yazarının referans uygulaması, MIT;
`protokol_kaynaklari/uygulama_kaynaklari/babeld/`).

Gerçekleme ilkesi (K-242 ve Babel'in kaydı):
  · RFC'nin MUST ve SHOULD'u uygulanır. RFC açık bir değer ya da yordam
    veriyorsa (Ek A.1 zaman aşımı, Ek A.3 seçim kuralı, §3.5.3 süre dolumu,
    Ek B parametreleri) o alınır; babeld farklıysa tabloda yazılıdır.
  · RFC'nin seçeneğe bıraktığı ya da örnekle geçtiği yerde ("say, 6",
    "such as 3") ve MAY'lerde hakem babeld'dir: babeld varsayılan olarak ne
    yapıyorsa alınır, yapmıyorsa alınmaz. AODV'de ns-3 ve OLSRv2'de olsrd2
    için de aynı ilke geçerlidir.
Parametreler hiçbir senaryoya göre ayarlanmaz.

🔒 TEL BİÇİMİ — RFC 8966 §4 BAYT BAYT
=====================================
Bir Babel paketi (4 baytlık başlık + TLV'ler) `paket_kodla` ile kodlanır ve
simülatörün biçim sözleşmesinde tekrarlı 8 bitlik tek alanla taşınır
(`BABEL`); ödenen bayt gerçek tel boyutudur, alıcı aynı baytları
`paket_coz` ile çözer (OLSRv2'nin RFC 5444 yolu ile aynı yaklaşım).
Kullanılan TLV'ler: Hello (4) · IHU (5) · Update (8) · Route Request (9,
joker dâhil) · Seqno Request (10) · Acknowledgment (3, yalnız yanıt).

🔴 BEYAN TABLOSU — RFC'nin seçeneğe bıraktığı her yer
=====================================================
| konu | RFC | gerçekleme | dayanak |
|---|---|---|---|
| adres ailesi | §3.1: denetim trafiği için yalnız IPv6 RECOMMENDED | IPv4 (AE 1) | simülatörün tek ağ katmanı IPv4: bütün protokollerin kontrol çerçevesi IPv4/UDP ile faturalanır (`13` §03.1); IPv6 Babel'e paket başına 20 B ek getirirdi. Adres aileleri arasında davranış farkı yok |
| adres modeli | serbest | tek arayüz, tek adres; düğüm k → 10.0.0.0 + k + 1; her düğüm kendi /32 önekini duyurur | OLSRv2 ile aynı; her İHA'nın tek telsizi var |
| router-id | §3: keyfî, tekil | 4 sıfır bayt + düğümün IPv4 adresi; Update'te R bayrağıyla taşınır (§4.6.9), Router-Id TLV'si gerekmez | RFC'nin kendi notu: router-id'ler bu biçimde atanınca kodlama kısalır (§3, §4.6.9) |
| önek sıkıştırma | §4.6.9: isteğe bağlı | pakette ilk Update P bayraklı tam önek; sonrakiler ortak baştaki baytları atlar (aynı /24'te Omitted 3) | RFC'nin kodlaması |
| paket boyu | §4: UDP gövdesi | en çok 1472 B (802.11 MTU 1500 − IPv4 20 − UDP 8); aşan TLV dizisi birden çok pakete bölünür | babeld de arayüz MTU'suna göre böler |
| düğüm sıra numarasının başlangıcı | tanımsız | 0 | yeniden başlatma yok |
| tek-yayın Hello | Ek B: sonsuz (gönderilmez) | gönderilmez | Ek B |
| Hello geçmişi | Ek A.1 | 16 bitlik geçmiş, beklenen sıra; zaman aşımı 1,5 × ilan edilen aralık, sonrakiler aralık kadar; iki geçmiş de boşsa komşu silinir | Ek A.1 (babeld 1,7 ×; RFC'nin açık değeri alındı) |
| komşu kaydı ne zaman açılır | §3.4: uygulamaya bağlı | Hello TLV'si çözülünce | babeld her pakette açar, Hello'suz kaydı geçmişi boş olduğu için hemen siler: sonuç aynı |
| bağ maliyeti (rxcost) | Ek A.2.2: beta "son birkaç Hello'nun oranı (say, 6) ya da üstel ortalama ya da ikisinin birleşimi" | babeld'in ağırlıklı geçmişi: sreach = (b15 ≫ 2) + (b14 ≫ 1) + (geçmiş & 3FFF); rxcost = 8000h · 256 / (sreach + 1). Son 12 Hello'nun hiçbiri alınmadıysa ya da son Hello olayı 180 s önceyse ∞; 40 s'den eskiyse rxcost · (gecikme − 20 s) / 20 s | babeld `neighbour_rxcost` |
| bağ maliyeti (birleşim) | Ek A.2.2: cost = 256 / (alpha · beta) | (max(txcost, 256) · rxcost + 128) ≫ 8 | RFC'nin formülü; tamsayı yuvarlaması babeld `neighbour_cost` |
| IHU sıklığı | Ek B: ilan edilen aralık 3 × Hello; "kayıplı" bağda her Hello'yla, kayıpsızda üç Hello'da bir | sırası 3'e bölünen Hello'yla bütün komşulara; öteki Hello'larda son 4 Hello'dan biri kaçmış ya da txcost ≥ 384 olan komşuya | babeld `send_hello` · `send_marginal_ihu` |
| IHU tutma süresi | Ek B: 3,5 × IHU aralığı | 3,5 × | Ek B (babeld 10 × ya da Hello geçmişi boşalınca) |
| metrik | §3.5.2: yerel politika, toplamsal RECOMMENDED | M(c, m) = c + m, ∞'a (FFFF) kırpılır | §3.5.2 |
| rota seçimi | §3.6: histerezis SHOULD; Ek A.3 | Ek A.3'ün kuralı: seçili yoksa en küçük metrik; seçili R iken R'ye ancak m(R') < m(R) ve ms(R') < ms(R) ise geçilir; eşitlikte küçük komşu kimliği | Ek A.3 |
| düzgünleştirme | Ek A.3: zaman sabiti "Hello aralığı × küçük bir sayı, örneğin 3" | yarı ömür 4 s: geçen sürede eski metriğe doğru ms ← ms + (m − ms)(1 − 2^(−Δt/4)), fark 4'ten küçükse ms = m; yeni rotada ms = max(m, ∞/2); ∞ metrikte ms = ∞ | babeld `route_smoothed_metric` (her saniyeki rastgele yuvarlama alınmadı: belirlenimcilik) |
| rota süresi | §3.5.3 · Ek B: 3,5 × ilan edilen güncelleme aralığı; dolunca metrik ∞, ikinci dolumda silinir | RFC | babeld 6 × ve süresinin 7/8'ini geçen rotayı ~30 s'lik taramada siler; RFC'nin açık değeri ve yordamı alındı |
| uygulanamaz güncelleme, kayıt yokken | §3.5.3: MAY yok sayılır | yok sayılmaz, kayıt açılır (seçilemez) | babeld kaydı açar; açlıkta istek bu rotalar boyunca gider (§3.8.2.1) |
| seçili rotanın aynı router-id'li uygulanamaz güncellemesi | §3.5.3: MAY yok sayılır; yok sayılmazsa güncellenen kayıt hemen seçimden çıkar (MUST) | yok sayılır (rota seçili kalır, kayıt değişmez); ilan edene sıra isteği gider (§3.8.2.2) | babeld kaydı günceller ama seçimden çıkarmaz (`update_route`): RFC'nin iki dalının arası; babeld'in seçili tutma amacına RFC'yle uyumlu dal yok saymadır |
| seçili rotanın farklı router-id'li uygulanamaz güncellemesi | §3.5.3: MUST, hemen seçimden çıkar | RFC | §3.5.3 |
| tetiklenen güncelleme | §3.7.2: router-id değişince MUST (acil), geri çekmede SHOULD; metrik belirgin değişince MAY | babeld `send_triggered_update`: router-id değişimi ve geri çekme acil, 2 · 4 · 8 s sonra yinelenir; kötüleşme (eski < 1536, fark ≥ 512) acil; bekleyen isteği karşılayan rota acil; ∞'dan sonluya dönen rota acil değil; 1024'ten küçük iyileşme ve 384'ten küçük fark gönderilmez, öteki değişim acil değil. Hiç kurulu rotası olmayan önekte ilk rota acil (`consider_route`) | babeld; RFC: kopya sayısı ≤ 5 (MUST) |
| geri çekilen rota | §3.5.4: ∞ metrikli kayıt tutulur; §3.7: yakında geri çekilmiş önekler için geri çekme gönderilebilir | kayıt silinene dek periyodik dökümde geri çekme olarak duyurulur | babeld (kurulu ∞ rota dökümde) |
| joker geri çekme (AE 0 Update) | §4.6.9: komşunun bütün rotalarını geri çeker | gönderilmez; alınırsa işlenmez | ağdaki hiçbir düğüm göndermez (yeniden başlatma yok) |
| bölünmüş ufuk | §3.7.4: 802.11 ad hoc'ta SHOULD NOT | kullanılmaz | §3.7.4 |
| onay istekleri | §3.3: isteğe bağlı | gönderilmez; gelirse yanıtlanır | §3.3: her konuşmacı yanıtlayabilmeli (MUST) |
| açlıkta sıra isteği | §3.8.2.1: uygulanamaz rota varken MUST (hepsine SHOULD), yokken MAY; yineleme SHOULD | uygulanamaz rota varsa çoklu-yayın; yoksa seçili rota süre dolumuyla ya da farklı router-id'li uygulanamaz güncellemeyle kaybedildiyse ve eski metrik ≤ ∞/2 ise çoklu-yayın. Rota uygulanabilir olmazsa 2 · 4 · 8 s'lik bekleyişlerle (+2, +6, +14 s) en çok üç kez | MUST dalı RFC; MAY dalı babeld `route_lost`; yineleme Ek B (babeld +2, +4, +8 s) |
| sıra isteğinin hop count'u | §3.8.2.1: çaptan büyük herhangi bir değer, "64 is a suitable default" | 64 | RFC'nin önerdiği varsayılan (babeld 127; ağın çapı 10'dan küçük, fark yok) |
| uygulanamaz güncellemede sıra isteği | §3.8.2.2: seçili rota için SHOULD; seçili olmayan ama "tercih edilir" rota için SHOULD | seçili rota için gönderene tek-yayın; seçili olmayan rota için seçili rota yoksa ya da seçilinin metriği yeni metrik + 512'den küçük değilse gönderene tek-yayın; ikisinde de bekleyen eşdeğer istek yoksa (§3.2.7) | RFC; "tercih edilir"in eşiği babeld `send_unfeasible_request` (babeld seçili rota için yalnız rota eskiyse gönderir; RFC'nin SHOULD'u alındı) |
| süresi dolmadan rota isteği | §3.8.2.3: SHOULD, "shortly before" | seçili rotanın tutma süresinin 7/8'i dolunca ilan edene tek-yayın | babeld'in eşiği (`route_old`) |
| sıra isteğini iletme | §3.8.1.2: uygulanabilir rota varsa MUST, yoksa uygulanamaz rotaya SHOULD; istekçi dışındaki bir komşuya | seçili rotanın komşusu istekçi değilse o; değilse en küçük düzgünleştirilmiş metrikli rota; iletim acil tek-yayın | RFC; seçim sırası babeld `handle_request` · `find_best_route` |
| istek listesi | §3.8.1.2: "recently" | kayıttan 65 s sonra ya da karşılanınca silinir; aynı önek, router-id ve daha küçük olmayan sırayla kayıt varken gelen istek iletilmez | RFC; süre babeld `REQUEST_TIMEOUT` (babeld'in `request_redundant` karşılaştırması ters yönde; RFC'nin SHOULD'u alındı) |
| bekleyen istekler tablosu | §3.2.7: yerelde üretilen ve iletilen istekler, yanıt gelene dek; zamanlayıcı yinelemeyi ve ömrü yönetir | her üretilen istek tabloda; aynı önek ve router-id için daha küçük olmayan sıralı istek beklerken yenisi üretilmez. Uygulanamaz güncelleme isteği (§3.8.2.2) yinelenmez, istek zaman aşımında (2 s) düşer; açlık isteği Ek B'ye göre yinelenir, 65 s'de düşer | RFC §3.2.7 (babeld §3.8.2.2 isteğini tabloya yazmaz; RFC'nin tablosu alındı) |
| sıra isteğine yanıt | §3.8.1.2: güncelleme MUST; biçim serbest | acil çoklu-yayın | babeld `handle_request` |
| bekleyen isteğin yanıtı | §3.8.1.2: acil SHOULD | isteği karşılayan rota seçiliyken acil çoklu-yayın güncelleme | babeld (`unsatisfied_request`) |
| rota isteğine yanıt | §3.8.1.1: güncelleme ya da geri çekme MUST; biçim serbest | çoklu-yayın, acil değil | babeld |
| kötüleşmede rota isteği | §3.8.2: MAY (her an) | seçili rotanın metriği en az 288 kötüleşip bir güncelleme gönderilince (geri çekme dâhil) çoklu-yayın rota isteği | babeld `send_triggered_update` |
| joker rota isteği (AE 0) | §3.8.1.1: MAY gönder; alınırsa tam döküm SHOULD, hız sınırlı SHOULD | açılışta çoklu-yayın joker istek; alınınca o komşuya IHU ve son tam dökümden bu yana en az bir Hello aralığı geçtiyse tam döküm, acil değil. Açılıştaki joker geri çekme gönderilmez | babeld açılışı ve hız sınırı; joker geri çekme yeniden başlatmada eski rotaları siler, burada yeniden başlatma yok |
| titreşim | §3.1: SHOULD; acil TLV acil zaman aşımı içinde, öteki TLV'ler Hello aralığının yarısı içinde | periyodik Hello ve tam döküm: sonraki = aralık − J + U(0, J), J = aralık/4 (ilan edilen aralık aşılmaz); tampon ilk acil TLV'de U(0, 0,2 s), yoksa U(0, Hello/2) içinde boşalır | RFC 5148 §5'in MAXJITTER = aralık/4'ü (OLSRv2'de de); babeld ±%25 kullanır ve ilan edilen aralığı aşabilir, RFC'nin üst sınırı korundu; acil olmayan güncellemeyi babeld 3–5 s'de boşaltır, RFC'nin yarım Hello sınırı alındı |
| TLV birleştirme | §3.1: tamponlanıp rastgele gecikmeyle gönderilir (SHOULD), birleştirmeye izin verir | hedef başına tampon (çoklu-yayın ya da komşu): aynı önekin duyuruları tek Update'e iner ve gönderim anındaki hâliyle kurulur; Hello, periyodik döküm ve açılış bekleyen çoklu-yayın tamponunu da taşır; paket MTU'yu aşarsa bölünür | babeld'in arayüz ve komşu tamponları (`buffer_update` · `flushupdates` · `flushbuf`) |
| ara zaman aşımları | Ek B | zamanlayıcılar tek bir "en erken son tarih" uyandırmasıyla işlenir | sonuç aynı; düğüm başına bekleyen uyandırma sınırı (`13` §03.5) |
| bağ katmanı bildirimi | §3.4.3: rxcost bağ katmanı istatistikleriyle birleştirilebilir | kullanılmaz | babeld'in kablosuz varsayılanı yalnız Hello geçmişi |
| RTT bileşeni | eklenti (RFC 9616) | yok | RFC 8966'nın parçası değil; babeld'de varsayılan kapalı |
| tutma süresi (§3.5.4) | daha kısa önek varsa | ∞ metrikli kayıt süresi dolana dek tutulur; daha kısa önek yok | her önek /32 |
| veri tamponu | tanımsız | yok, rota yoksa paket düşer | proaktif; OLSRv2 ile aynı; babeld ∞ rotayı çekirdeğe "unreachable" kurar |
"""

from __future__ import annotations

import struct

from sim2.gozlem.kontrol import MesajBicimi

__all__ = [
    "BABEL", "BicimHatasi", "SONSUZ", "ADRES_TABANI", "PAKET_UST_SINIRI_B",
    "HELLO_ARALIGI_S", "IHU_ARALIGI_S", "GUNCELLEME_ARALIGI_S",
    "IHU_TUTMA_KATSAYISI", "ROTA_SURESI_KATSAYISI",
    "HELLO_ZAMAN_ASIMI_KATSAYISI", "ISTEK_ZAMAN_ASIMI_S", "ISTEK_TEKRAR",
    "ACIL_ZAMAN_ASIMI_S", "KAYNAK_GC_S", "SIRA_ISTEGI_HOP", "GECMIS_BIT",
    "YARI_OMUR_S", "TETIK_YENIDEN_S", "ROTA_ISTEGI_ORANI", "ISTEK_LISTE_S",
    "ETX_SONSUZ_MASKE", "ETX_CEZA_S", "ETX_SONSUZ_S",
    "IHU_KAYIPLI_MASKE", "IHU_TXCOST_ESIGI", "KOTULESME_TABANI",
    "KOTULESME_FARKI", "IYILESME_YOKSAY", "ONEMSIZ_FARK",
    "ROTA_ISTEGI_KOTULESME", "TERCIH_FARKI",
    "TLV_HELLO", "TLV_IHU", "TLV_UPDATE", "TLV_ROUTE_REQUEST",
    "TLV_SEQNO_REQUEST", "TLV_ACK_REQUEST", "TLV_ACK",
    "Hello", "Ihu", "Guncelleme", "RotaIstegi", "SiraIstegi",
    "adres", "dugum", "paket_kodla", "paket_coz", "sira_kucuk",
    "sira_artir",
]

# ==========================================================================
# Ek B · Protocol Parameters — RECOMMENDED varsayılanlar
# ==========================================================================
HELLO_ARALIGI_S: float = 4.0            # Multicast Hello interval
IHU_ARALIGI_S: float = 3 * HELLO_ARALIGI_S       # ilan edilen IHU aralığı
GUNCELLEME_ARALIGI_S: float = 4 * HELLO_ARALIGI_S  # Update interval
IHU_TUTMA_KATSAYISI: float = 3.5        # IHU Hold time = 3,5 × IHU aralığı
ROTA_SURESI_KATSAYISI: float = 3.5      # Route Expiry = 3,5 × Update aralığı
ISTEK_ZAMAN_ASIMI_S: float = 2.0        # Request timeout, her yinelemede × 2
ISTEK_TEKRAR: int = 3                   # "up to a maximum of three times"
ACIL_ZAMAN_ASIMI_S: float = 0.2         # Urgent timeout
KAYNAK_GC_S: float = 180.0              # Source GC time (3 dk)
# Ek A.1: zaman aşımı ilk kez 1,5 × ilan edilen aralık (titreşim payı).
HELLO_ZAMAN_ASIMI_KATSAYISI: float = 1.5
GECMIS_BIT: int = 16                    # Ek A.1: 16 bitlik Hello geçmişi
SIRA_ISTEGI_HOP: int = 64               # §3.8.2.1: "64 is a suitable default"

# ==========================================================================
# Hakem babeld 1.14 — RFC'nin seçeneğe ya da MAY'e bıraktığı yerler
# ==========================================================================
# Ek A.3 düzgünleştirmesi: `smoothing_half_life` varsayılanı (babeld.c).
YARI_OMUR_S: float = 4.0
# §3.7.2 yinelenen tetik: ilk gönderimden 2 · 4 · 8 s sonra (resend.c:
# RESEND_MAX 3, `resend_delay` = min(2 s, Hello/2), her seferde × 2, süre
# ilk gönderimden sayılır).
TETIK_YENIDEN_S: tuple[float, ...] = (2.0, 4.0, 8.0)
# §3.8.2.3: tutma süresinin 7/8'i dolunca (route.c `route_old`).
ROTA_ISTEGI_ORANI: float = 7 / 8
# §3.8.1.2 "recently forwarded": istek kaydının ömrü (resend.h
# `REQUEST_TIMEOUT` 65 000 ms).
ISTEK_LISTE_S: float = 65.0
# Ek A.2.2 rxcost (neighbour.c `neighbour_rxcost`): son 12 Hello'nun hiçbiri
# yoksa ∞; son Hello olayı 40 s'den eskiyse ceza, 180 s'den eskiyse ∞.
ETX_SONSUZ_MASKE: int = 0xFFF0
ETX_CEZA_S: float = 40.0
ETX_SONSUZ_S: float = 180.0
# Ek B IHU sıklığı (message.c `send_marginal_ihu`): son 4 Hello'dan biri
# kaçmışsa ya da txcost ≥ 384 ise her Hello'da.
IHU_KAYIPLI_MASKE: int = 0xF000
IHU_TXCOST_ESIGI: int = 384
# §3.7.2 metrik değişiminde tetik (route.c `send_triggered_update`).
KOTULESME_TABANI: int = 6 * 256         # eski metrik bunun altındaysa
KOTULESME_FARKI: int = 512              # ... ve kötüleşme ≥ 512: acil
IYILESME_YOKSAY: int = 1024             # bundan küçük iyileşme gönderilmez
ONEMSIZ_FARK: int = 384                 # bundan küçük fark gönderilmez
ROTA_ISTEGI_KOTULESME: int = 288        # ≥ 288 kötüleşmede rota isteği
# §3.8.2.2 "preferable" (route.c `send_unfeasible_request`): seçili rotanın
# metriği yeni metrik + 512'den küçük değilse.
TERCIH_FARKI: int = 512

SONSUZ: int = 0xFFFF
ADRES_TABANI: int = 0x0A000000          # 10.0.0.0 — OLSRv2 ile aynı model
# 802.11 MTU 1500 − IPv4 başlığı 20 − UDP başlığı 8 (paketin tamamı).
PAKET_UST_SINIRI_B: int = 1472

# TLV tipleri (§4.6)
TLV_PAD1, TLV_PADN, TLV_ACK_REQUEST, TLV_ACK = 0, 1, 2, 3
TLV_HELLO, TLV_IHU, TLV_ROUTER_ID, TLV_NEXT_HOP = 4, 5, 6, 7
TLV_UPDATE, TLV_ROUTE_REQUEST, TLV_SEQNO_REQUEST = 8, 9, 10
_SIHIRLI, _SURUM = 42, 2                # §4.2 Magic · Version
_AE_JOKER, _AE_IPV4 = 0, 1
_BAYRAK_P, _BAYRAK_R = 0x80, 0x40       # Update bayrakları (§4.6.9)
_BAYRAK_U = 0x8000                      # Hello Unicast bayrağı (§4.6.5)

# Simülatörün biçim sözleşmesi: gerçek paket baytları tekrarlı 8 bitlik tek
# alanda (OLSRv2'nin `rfc5444` alanı gibi).
BABEL = MesajBicimi("BABEL", (), tekrarli=(("babel", 8),))


class BicimHatasi(ValueError):
    """RFC 8966 §4 — bozuk ya da tanınmayan paket."""


# ==========================================================================
# Adresler ve sıra numaraları
# ==========================================================================
def adres(k: int) -> int:
    return ADRES_TABANI + k + 1


def dugum(a: int) -> int:
    return a - ADRES_TABANI - 1


def sira_artir(s: int, n: int = 1) -> int:
    """§3.2.1: s + n (mod 2^16)."""
    return (s + n) & 0xFFFF


def sira_kucuk(s: int, t: int) -> bool:
    """§3.2.1: s < t (mod 2^16) ⇔ 0 < (t − s) mod 2^16 < 32768."""
    return 0 < ((t - s) & 0xFFFF) < 0x8000


# ==========================================================================
# TLV'ler — çözülmüş biçim
# ==========================================================================
class Hello(tuple):
    """(sira, aralik_cs) — çoklu-yayın Hello (U bayrağı 0)."""
    __slots__ = ()

    def __new__(cls, sira: int, aralik_cs: int):
        return super().__new__(cls, (sira, aralik_cs))

    sira = property(lambda s: s[0])
    aralik_cs = property(lambda s: s[1])


class Ihu(tuple):
    """(rxcost, aralik_cs, adres)."""
    __slots__ = ()

    def __new__(cls, rxcost: int, aralik_cs: int, adres_: int):
        return super().__new__(cls, (rxcost, aralik_cs, adres_))

    rxcost = property(lambda s: s[0])
    aralik_cs = property(lambda s: s[1])
    adres = property(lambda s: s[2])


class Guncelleme(tuple):
    """(onek, plen, aralik_cs, sira, metrik, router_id). Geri çekmede
    router_id ve sira kullanılmaz."""
    __slots__ = ()

    def __new__(cls, onek: int, plen: int, aralik_cs: int, sira: int,
                metrik: int, router_id: int):
        return super().__new__(cls, (onek, plen, aralik_cs, sira, metrik,
                                     router_id))

    onek = property(lambda s: s[0])
    plen = property(lambda s: s[1])
    aralik_cs = property(lambda s: s[2])
    sira = property(lambda s: s[3])
    metrik = property(lambda s: s[4])
    router_id = property(lambda s: s[5])


class RotaIstegi(tuple):
    """(onek, plen). plen 0 joker istektir (AE 0, §4.6.10)."""
    __slots__ = ()

    def __new__(cls, onek: int, plen: int):
        return super().__new__(cls, (onek, plen))

    onek = property(lambda s: s[0])
    plen = property(lambda s: s[1])
    joker = property(lambda s: s[1] == 0)


class SiraIstegi(tuple):
    """(onek, plen, sira, hop, router_id)."""
    __slots__ = ()

    def __new__(cls, onek: int, plen: int, sira: int, hop: int,
                router_id: int):
        return super().__new__(cls, (onek, plen, sira, hop, router_id))

    onek = property(lambda s: s[0])
    plen = property(lambda s: s[1])
    sira = property(lambda s: s[2])
    hop = property(lambda s: s[3])
    router_id = property(lambda s: s[4])


# ==========================================================================
# Kodlama — §4.2 paket, §4.6 TLV'ler
# ==========================================================================
def _tlv(tip: int, govde: bytes) -> bytes:
    if len(govde) > 255:
        raise BicimHatasi("TLV gövdesi 255 baytı aşıyor")
    return bytes((tip, len(govde))) + govde


def _onek_baytlari(onek: int, plen: int) -> bytes:
    """§4.1.5: önek, anlamlı bitleri tutacak en az baytta."""
    return onek.to_bytes(4, "big")[:(plen + 7) // 8]


def paket_kodla(tlvler) -> bytes:
    """TLV listesinden tam Babel paketi. Update'ler §4.5'in sıkıştırmasıyla:
    ilk Update P bayraklı tam önek taşır, sonrakiler o önekle ortak baştaki
    baytları atlar; R bayrağı router-id'yi önekten türetir (router-id =
    4 sıfır bayt + IPv4)."""
    govde = bytearray()
    varsayilan: bytes | None = None             # §4.5 parser state (AE 1)
    for t in tlvler:
        if isinstance(t, Hello):
            govde += _tlv(TLV_HELLO, struct.pack(">HHH", 0, t.sira,
                                                 t.aralik_cs))
        elif isinstance(t, Ihu):
            govde += _tlv(TLV_IHU, struct.pack(">BBHH", _AE_IPV4, 0,
                                               t.rxcost, t.aralik_cs)
                          + t.adres.to_bytes(4, "big"))
        elif isinstance(t, Guncelleme):
            tam = _onek_baytlari(t.onek, t.plen)
            atla = 0
            if varsayilan is not None:
                while (atla < min(len(tam), len(varsayilan)) - 1
                       and tam[atla] == varsayilan[atla]):
                    atla += 1
            bayrak = 0
            if t.metrik != SONSUZ:
                # R: router-id = 4 sıfır + adres; yalnız önek /32 ve
                # router-id bu biçimdeyse.
                if t.plen != 32 or t.router_id != t.onek:
                    raise BicimHatasi("router-id önekten türetilemiyor")
                bayrak |= _BAYRAK_R
            if atla == 0:
                bayrak |= _BAYRAK_P
                varsayilan = tam
            govde += _tlv(TLV_UPDATE, struct.pack(
                ">BBBBHHH", _AE_IPV4, bayrak, t.plen, atla, t.aralik_cs,
                t.sira, t.metrik) + tam[atla:])
        elif isinstance(t, RotaIstegi):
            if t.joker:
                govde += _tlv(TLV_ROUTE_REQUEST, struct.pack(">BB",
                                                             _AE_JOKER, 0))
            else:
                govde += _tlv(TLV_ROUTE_REQUEST,
                              struct.pack(">BB", _AE_IPV4, t.plen)
                              + _onek_baytlari(t.onek, t.plen))
        elif isinstance(t, SiraIstegi):
            if not 0 < t.hop < 256:
                raise BicimHatasi("Hop Count 1–255 olmalı")
            govde += _tlv(TLV_SEQNO_REQUEST, struct.pack(
                ">BBHBBQ", _AE_IPV4, t.plen, t.sira, t.hop, 0, t.router_id)
                + _onek_baytlari(t.onek, t.plen))
        elif isinstance(t, tuple) and t and t[0] == "ack":
            govde += _tlv(TLV_ACK, struct.pack(">H", t[1]))
        else:
            raise BicimHatasi(f"bilinmeyen TLV: {t!r}")
    if len(govde) > 0xFFFF:
        raise BicimHatasi("paket gövdesi 65 535 baytı aşıyor")
    return struct.pack(">BBH", _SIHIRLI, _SURUM, len(govde)) + bytes(govde)


def paket_coz(b: bytes) -> list:
    """§4.2 · §4.5 · §4.6. Tanınmayan TLV sessizce atlanır (§4.3); Ack
    isteği `("ack_istek", opak, aralik_cs)` olarak döner."""
    if len(b) < 4 or b[0] != _SIHIRLI or b[1] != _SURUM:
        raise BicimHatasi("başlık geçersiz (Magic 42 · Version 2)")
    uzunluk = struct.unpack(">H", b[2:4])[0]
    if 4 + uzunluk > len(b):
        raise BicimHatasi("gövde uzunluğu paketi aşıyor")
    govde = b[4:4 + uzunluk]
    cikti: list = []
    varsayilan: bytes | None = None
    router_id: int | None = None
    i = 0
    while i < len(govde):
        tip = govde[i]
        if tip == TLV_PAD1:
            i += 1
            continue
        if i + 2 > len(govde):
            raise BicimHatasi("TLV başlığı kesik")
        n = govde[i + 1]
        v = govde[i + 2:i + 2 + n]
        if len(v) < n:
            raise BicimHatasi("TLV gövdesi kesik")
        i += 2 + n
        if tip == TLV_HELLO and n >= 6:
            bayrak, sira, aralik = struct.unpack(">HHH", v[:6])
            if not bayrak & _BAYRAK_U:          # yalnız çoklu-yayın Hello
                cikti.append(Hello(sira, aralik))
        elif tip == TLV_IHU and n >= 6:
            ae, _r, rx, aralik = struct.unpack(">BBHH", v[:6])
            if ae == _AE_IPV4 and n >= 10:
                cikti.append(Ihu(rx, aralik,
                                 int.from_bytes(v[6:10], "big")))
        elif tip == TLV_UPDATE and n >= 10:
            ae, bayrak, plen, atla, aralik, sira, metrik = struct.unpack(
                ">BBBBHHH", v[:10])
            if ae != _AE_IPV4 or plen > 32:
                continue
            boy = (plen + 7) // 8
            if atla > boy or (atla and varsayilan is None):
                continue                         # §4.6.9 MUST ignore
            tam = (varsayilan[:atla] if atla else b"") + v[10:10 + boy - atla]
            if len(tam) < boy:
                raise BicimHatasi("Update öneki kesik")
            if bayrak & _BAYRAK_P:
                varsayilan = tam
            onek = int.from_bytes(tam.ljust(4, b"\0"), "big")
            if bayrak & _BAYRAK_R:
                router_id = int.from_bytes(tam.rjust(8, b"\0")[-8:], "big")
            if metrik == SONSUZ:                 # geri çekmede router-id yok
                cikti.append(Guncelleme(onek, plen, aralik, sira, metrik, 0))
                continue
            if router_id is None:
                continue                         # router-id yok → yok say
            cikti.append(Guncelleme(onek, plen, aralik, sira, metrik,
                                    router_id))
        elif tip == TLV_ROUTER_ID and n >= 10:
            router_id = struct.unpack(">Q", v[2:10])[0]
        elif tip == TLV_ROUTE_REQUEST and n >= 2:
            ae, plen = v[0], v[1]
            if ae == _AE_JOKER and plen == 0:
                cikti.append(RotaIstegi(0, 0))
            elif ae == _AE_IPV4 and 0 < plen <= 32:
                tam = v[2:2 + (plen + 7) // 8]
                cikti.append(RotaIstegi(
                    int.from_bytes(tam.ljust(4, b"\0"), "big"), plen))
        elif tip == TLV_SEQNO_REQUEST and n >= 14:
            ae, plen, sira, hop, _r, rid = struct.unpack(">BBHBBQ", v[:14])
            if ae == _AE_IPV4 and plen <= 32 and hop > 0:
                tam = v[14:14 + (plen + 7) // 8]
                cikti.append(SiraIstegi(
                    int.from_bytes(tam.ljust(4, b"\0"), "big"), plen, sira,
                    hop, rid))
        elif tip == TLV_ACK_REQUEST and n >= 6:
            _r, opak, aralik = struct.unpack(">HHH", v[:6])
            cikti.append(("ack_istek", opak, aralik))
        # Ack, Pad, Next Hop ve bilinmeyen tipler: bu gerçeklemede etkisiz.
    return cikti
