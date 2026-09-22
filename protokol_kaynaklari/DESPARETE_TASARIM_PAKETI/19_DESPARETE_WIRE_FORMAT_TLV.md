# DESPARETE — Wire Format ve TLV Uzantıları

**Sürüm:** 0.1 (onaylı wire profile ve Security Profile 1 eki)  
**Durum:** Kontrol mesajı semantiğini paketlenebilir ikili biçime dönüştürür; `26`daki zorunlu AUTHENTICATION alt-biçimiyle birlikte uygulanır. Uygulama taşıyıcısı ve IANA kaydı daha sonra tanımlanacaktır.  
**Tarih:** 2026-09-20

## 1. Kapsam ve taşıma varsayımı

Bu belge, DESPARETE paketinin ikili başlık biçimini tanımlar. Paket, uygun bir link veya ağ taşıyıcısı üzerinde taşınabilir; Ethernet, IPv6 next-header/protocol numarası, UDP portu veya başka bir kapsüllemenin seçimi bu sürümün kapsamı dışındadır.

Byte sırası ağ byte sırasıdır (big-endian). Bit numarası bir octet içinde en anlamlı bitten en az anlamlı bite doğrudur. Tüm rezerve alanlar gönderimde sıfır olmalı, alıcıda aksi profil belirtilmedikçe reddedilmelidir.

Bu format dört tasarım ilkesini uygular:

- Kimlikler ve sıra alanları açık, sonlu ve doğrulanabilir kodlanır.
- Maliyetler kayan nokta yerine ortak sabit noktalı tamsayı kuantalarıyla taşınır.
- Field state için `∞` yalnız withdrawal'a ayrılır.
- Uzantılar TLV ile eklenir; bilinmeyen kritik uzantı fail-closed davranış üretir.

## 2. Ortak taban başlık

Her DESPARETE paketi aşağıdaki 4-octet taban başlıkla başlar.

```text
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +---+---+---------------+---------------+---------------+
 |Ver|Type| Header Length |   Hop Limit   |  Base Flags   |
 +---+---+---------------+---------------+---------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik |
|---|---:|---|---|
| Ver | 4 | `1` bu tasarım sürümü; `0` ve desteklenmeyen değerler geçersiz | Protokol sürümü. |
| Type | 4 | §3 tablosundaki paket türleri | Core body biçimini seçer. |
| Header Length | 8 | Tüm header'ın octet uzunluğu; türün minimumundan küçük veya `4`ten küçük olamaz | Base, core body ve TLV/padding'i kapsar; DATA payload'ını kapsamaz. |
| Hop Limit | 8 | `1…255`; `0` geçersiz | Her çok-atlama iletimde bir azaltılır. Tek-atlama paketlerde `1` olmalıdır. |
| Base Flags | 8 | Bu sürümde `0`; başka değer geçersiz | Gelecekte uyumsuz olmayan taban özellikleri için ayrılmıştır. |

Hop Limit `1` olan paketi alan node onu yeniden iletmez. Hop Limit, data-loop güvenlik kanıtı değildir; yalnız kapsam/zarar sınırıdır.

## 3. Paket türleri

| Type | Ad | Core body | Payload |
|---:|---|---|---|
| 0 | DATA | §4 | Uygulama verisi; Header Length sonrasında gelir. |
| 1 | FIELD_UPDATE | §6 | Yok. |
| 2 | FIELD_SOLICIT | §7 | Yok. |
| 3 | DFSN_REQUEST | §8 | Yok. |
| 4 | PROBE | §9 | Yok. |
| 5 | PROBE_REPLY | §10 | Yok. |
| 6 | FAILURE_REPORT | §11 | Yok. |
| 7–15 | Reserved | — | Gönderilmez; alınırsa reddedilir. |

Kontrol paketlerinde `Header Length`, TLV/padding dahil paket boyutuna eşit olmalıdır. DATA paketinde Header Length'i izleyen octetler uygulama payload'ıdır.

## 4. DATA core body

DATA core body, taban başlıktan sonra gelir ve 32 octettir. Bu nedenle uzantısız DATA header uzunluğu 36 octettir.

```text
 +-------------------------------+--------------------------------+
 | Application Destination-ID (64)                                |
 +-------------------------------+--------------------------------+
 | Data Source-ID (64)                                           |
 +-------------------------------+--------------------------------+
 | Data Source-Instance-ID (64)                                  |
 +-------------------------------+--------------------------------+
 | Data Sequence (32)            | Traffic Class | DFlags | RB |R|
 +-------------------------------+--------------------------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik ve etkileşim |
|---|---:|---|---|
| Application Destination-ID | 64 | Opaque, `0` geçersiz | Uygulama hedefi; node yerel olarak bu hedef için güncel kabul edilen `K` alanını seçer. OIID/DFSN DATA kimliğinin parçası değildir. |
| Data Source-ID | 64 | Opaque, `0` geçersiz | Data-ID'nin kaynağı. |
| Data Source-Instance-ID | 64 | Opaque, `0` geçersiz; kaynak restartında değişir | Data-ID'nin restart ayracı. |
| Data Sequence | 32 | Unsigned serial; aynı source instance içinde duplicate-cache ömründe tekrar etmez | Data-ID = `(Source-ID, Source-Instance-ID, Data-Sequence)`. |
| Traffic Class | 8 | `0` normal/belirtilmemiş; `1…255` profile tanımlı | Uygulama/QoS sınıfı; çekirdek routing onu öncelik sırası olarak yorumlamaz. |
| DFlags | 8 | Bit 0 `Protection-Eligible`; bit 1–7 `0` | Bit 0, §17 koşulları sağlanırsa redundancy'ye izin verir. |
| RB (Replication Budget) | 8 | Wire aralığı `0…255`; ilk-sürüm ingress profili `0` veya `1` | Kullanılmamış **ek kopya** üretim hakkı. Primary forwarding tüketmez; ek kopya üretildiğinde ilgili çıkış kopyalarındaki RB bir azaltılır. İlk-sürüm `MaxReplicaFanout=2` ve `RB∈{0,1}` olduğundan en çok primary + bir secondary çıkar ve bu iki çıkışta RB `0` kalır. Security Profile 1'de core `RB`, imzalı `Source-RB`yi aşamaz. DFlags bit 0 sıfırsa ikisi de **0** olmalıdır. |
| R | 8 | `0` | Rezerve. |

Forwarder, DATA'nın immutable Data-ID'sini korur. Replication Budget yalnız geçerli redundant forwarding olayında azaltılabilir; artırılamaz. Security Profile 1, Data-ID, DFlags, Source-RB ve payload için source integrity; bu hop'taki RB/Hop Limit için hop integrity uygular. DATA, her atlamada yalnız forwarding için seçilen güncel local field context'i kullanır; eski OIID/DFSN bilgisi DATA paketinde taşınarak alan güvenliği atlanamaz.

## 5. Kontrol gönderen bloğu

Her kontrol core body, taban başlıktan hemen sonra 24-octet **Control Sender Block** ile başlar.

```text
 +-------------------------------+--------------------------------+
 | Sender-ID (64)                                                |
 +-------------------------------+--------------------------------+
 | Sender-Instance-ID (64)                                       |
 +-------------------------------+--------------------------------+
 | Message Sequence (32)        | Reserved (32)                 |
 +-------------------------------+--------------------------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik |
|---|---:|---|---|
| Sender-ID | 64 | Opaque, `0` geçersiz | Bu hop'taki gönderen node. DFSN_REQUEST forward edildiğinde isteğin ilk üreticisi olmayabilir. |
| Sender-Instance-ID | 64 | Opaque, `0` geçersiz; restartta değişir | Eski kontrol mesajlarını yeni node örneğinden ayırır. |
| Message Sequence | 32 | Unsigned serial; sender instance içinde duplicate-cache ömründe tekrar etmez | Message-ID'nin sıra bileşeni. |
| Reserved | 32 | `0` | Hizalama / gelecekte kullanım. |

Kontrol Message-ID = `(Sender-ID, Sender-Instance-ID, Message-Sequence)` üçlüsüdür. Message Sequence, DFSN veya Advertisement-Serial değildir.

## 6. FIELD_UPDATE core body

FIELD_UPDATE core body, Control Sender Block sonrası 32 octettir. Uzantısız toplam header uzunluğu 60 octettir.

```text
 +-------------------------------+--------------------------------+
 | Destination-ID (64)                                           |
 +-------------------------------+--------------------------------+
 | Originator-Instance-ID (64)                                   |
 +-------------------------------+--------------------------------+
 | DFSN (32)                      | Advertisement-Serial (32)   |
 +-------------------------------+--------------------------------+
 | Advertised Potential (32)      | Lifetime (16) | State |Flags|
 +-------------------------------+--------------------------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik / doğrulama |
|---|---:|---|---|
| Destination-ID | 64 | Opaque, `0` geçersiz | Field-Key `K`nin hedefi. |
| Originator-Instance-ID (OIID) | 64 | Opaque, `0` geçersiz | Aynı hedefin yeniden başlatılmış eski/yeni field örneklerini ayırır. |
| DFSN | 32 | RFC 1982 serial | Yalnız field originator artırır. Tanımsız yarım-aralık kıyası fail-closed'dur. |
| Advertisement-Serial (ADS) | 32 | Gönderen ve `K` başına RFC 1982 serial | Aynı DFSN içindeki sender potential/withdrawal sırasını belirler. |
| Advertised Potential | 32 | Unsigned fixed-point cost; `0…0xFFFFFFFE` sonlu, `0xFFFFFFFF` = `∞` | REACHABLE'da sonlu olmalıdır; WITHDRAWAL'da `∞` olmalıdır. `0` yalnız `Sender-ID = Destination-ID` olan origin update'te geçerlidir. |
| Lifetime | 16 | Unsigned, 100 ms kuantaları; REACHABLE'da `1…65535`, WITHDRAWAL'da `0` | İlanın gönderici tarafından önerilen en uzun ömrü. Alıcı bunu kendi yerel üst sınırıyla sınırlar. |
| State | 8 | `0` REACHABLE, `1` WITHDRAWAL; diğerleri geçersiz | İlanın route veya retraction olduğunu açıklar. |
| Flags | 8 | `0` | Gelecek field özellikleri için ayrılmıştır. |

ADS, sender instance başına `K` için artar; sender restartı yeni Sender-Instance-ID ile ADS alanını ayırır. Alıcı aynı sender instance/K/DFSN bağlamında yalnız tanımlı olarak daha yeni ADS'yi cache'ine yazabilir. Security Profile 1'de her FIELD_UPDATE, target'ın aynı `(Destination-ID,OIID,DFSN)` üçlüsü için ürettiği OriginSignature'ı taşımak zorundadır; relay'in HopSignature'ı yalnız kendi local ilanını bağlar.

## 7. FIELD_SOLICIT core body

FIELD_SOLICIT core body, Control Sender Block sonrası 24 octettir. Uzantısız toplam header uzunluğu 52 octettir. Hop Limit `1` olmalıdır.

```text
 +-------------------------------+--------------------------------+
 | Destination-ID (64)                                           |
 +-------------------------------+--------------------------------+
 | Known OIID (64)                                               |
 +-------------------------------+--------------------------------+
 | Known DFSN (32)                 | SFlags | Reserved (24)      |
 +-------------------------------+--------------------------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik |
|---|---:|---|---|
| Destination-ID | 64 | Opaque, `0` geçersiz | İstenen hedef alanı. |
| Known OIID | 64 | `SFlags.HAS_CONTEXT=0` ise `0`; aksi hâlde nonzero | Requester'ın son kabul ettiği originator instance. |
| Known DFSN | 32 | Context yoksa `0`; aksi hâlde RFC 1982 serial | Requester'ın son kabul ettiği field turu. |
| SFlags | 8 | Bit 0 `HAS_CONTEXT`; bit 1–7 `0` | Bilinen K bağlamının bulunup bulunmadığı. |
| Reserved | 24 | `0` | Rezerve. |

Message Sequence, solicit kimliği olarak kullanılır. Yanıt veren node ilgili FIELD_UPDATE'ta kendi güncel alanını gönderir; FIELD_SOLICIT yeniden yayılmaz.

## 8. DFSN_REQUEST core body

DFSN_REQUEST core body, Control Sender Block sonrası 44 octettir. Uzantısız toplam header uzunluğu 72 octettir.

```text
 +-------------------------------+--------------------------------+
 | Requester-ID (64)                                             |
 +-------------------------------+--------------------------------+
 | Requester-Instance-ID (64)                                    |
 +-------------------------------+--------------------------------+
 | Request Sequence (32)        | Reserved (32)                  |
 +-------------------------------+--------------------------------+
 | Destination-ID (64)                                           |
 +-------------------------------+--------------------------------+
 | Known OIID (64)                                               |
 +-------------------------------+--------------------------------+
 | Requested-Minimum-DFSN (32)  | Reason | RFlags | Reserved(16) |
 +-------------------------------+--------------------------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik |
|---|---:|---|---|
| Requester-ID / Instance-ID / Sequence | 64 / 64 / 32 | Nonzero ID/instance; sequence sender instance içinde unique | Request-ID; forward eden node değişse bile aynı kalır. |
| Destination-ID | 64 | Opaque, `0` geçersiz | Yeni field turunu üretebilecek hedef. |
| Known OIID | 64 | `RFlags.HAS_CONTEXT=0` ise `0` | İstemin bilinen instance bağlamı. |
| Requested-Minimum-DFSN | 32 | Context yoksa `0`; aksi hâlde RFC 1982 serial | Hedefin üretmesi istenen yeni DFSN alt sınırı. |
| Reason | 8 | `0` acquisition, `1` feasible-starvation, `2` freshness ambiguity; diğerleri geçersiz | Yalnız gözlemlenebilir local istek sınıfı; jamming hükmü değildir. |
| RFlags | 8 | Bit 0 `HAS_CONTEXT`; bit 1–7 `0` | OIID/DFSN bağlamının mevcutluğu. |
| Reserved | 16 | `0` | Rezerve. |

DFSN_REQUEST tek-atlama değildir; Hop Limit her forwardingde azaltılır. Request-ID duplicate anahtarıdır. Mesaj, active komşular arasında §18 sınırlarıyla yayılır; data successor veya eski route üzerinden taşındığı varsayılmaz.

## 9. PROBE core body

PROBE core body, Control Sender Block sonrası 12 octettir. Uzantısız toplam header uzunluğu 40 octettir. Hop Limit `1` olmalıdır.

```text
 +-------------------------------+--------------------------------+
 | Target-Neighbour-ID (64)                                      |
 +-------------------------------+--------------------------------+
 | Probe Flags (8) | Reserved (24)                               |
 +-------------------------------+--------------------------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik |
|---|---:|---|---|
| Target-Neighbour-ID | 64 | Opaque, `0` geçersiz | Bu node ile eşleşmiyorsa paket bırakılır. |
| Probe Flags | 8 | `0` | Rezerve. |
| Reserved | 24 | `0` | Rezerve. |

Probe-ID, Control Sender Block'taki sender identity ve Message Sequence'dir.

## 10. PROBE_REPLY core body

PROBE_REPLY core body, Control Sender Block sonrası 24 octettir. Uzantısız toplam header uzunluğu 52 octettir. Hop Limit `1` olmalıdır.

```text
 +-------------------------------+--------------------------------+
 | Original Requester-ID (64)                                   |
 +-------------------------------+--------------------------------+
 | Original Requester-Instance-ID (64)                          |
 +-------------------------------+--------------------------------+
 | Probe Message Sequence (32)   | Reserved (32)                 |
 +-------------------------------+--------------------------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik |
|---|---:|---|---|
| Original Requester-ID / Instance-ID | 64 / 64 | PROBE sender değerleriyle tam eşleşir | Yanıtın hangi node örneğine ait olduğunu bağlar. |
| Probe Message Sequence | 32 | PROBE'un Message Sequence'i | Eşleşen Probe-ID. |
| Reserved | 32 | `0` | Rezerve. |

Alıcı, PROBE_REPLY'i ancak kendi bekleyen probe kaydıyla tam eşleşirse forwarding-grade iki yönlü kanıt olarak kullanabilir.

## 11. FAILURE_REPORT core body

FAILURE_REPORT core body, Control Sender Block sonrası 56 octettir. Uzantısız toplam header uzunluğu 84 octettir. Bu mesaj çok-atlama ise kendi rapor hedefi alanında normal safe-successor forwarding kullanır.

```text
 +-------------------------------+--------------------------------+
 | Report-Destination-ID (64)                                    |
 +-------------------------------+--------------------------------+
 | Failed Data Source-ID (64)                                    |
 +-------------------------------+--------------------------------+
 | Failed Data Source-Instance-ID (64)                           |
 +-------------------------------+--------------------------------+
 | Failed Data Sequence (32)     | Reserved (32)                 |
 +-------------------------------+--------------------------------+
 | Failed Application Destination-ID (64)                        |
 +-------------------------------+--------------------------------+
 | Failed OIID (64)                                               |
 +-------------------------------+--------------------------------+
 | Failed DFSN (32)              | Reason | FFlags | Reserved(16)|
 +-------------------------------+--------------------------------+
```

| Alan | Bit | Encoding / geçerli değer | Semantik |
|---|---:|---|---|
| Report-Destination-ID | 64 | Opaque, `0` geçersiz | Raporun bağımsız olarak yönlendirileceği hedef. |
| Failed Data Source-ID / Instance-ID / Sequence | 64 / 64 / 32 | DATA Data-ID ile eşleşir | Yerel başarısızlık olayını iliştirir. |
| Failed Application Destination-ID | 64 | Opaque, `0` geçersiz | Başarısız data'nın uygulama hedefi. |
| Failed OIID / DFSN | 64 / 32 | Alan bilinmiyorsa sırasıyla `0`/`0`; aksi hâlde local failure bağlamı | Hata anındaki field context; rapor alanı değildir. |
| Reason | 8 | `0` buffer lifetime, `1` buffer quota, `2` field unreachable, `3` freshness invalid, `4` local link failure; diğerleri geçersiz | Yerel gözlem sınıfı; global partition/jamming hükmü değildir. |
| FFlags | 8 | `0` | Rezerve. |
| Reserved | 16 + 32 | `0` | Rezerve/hizalama. |

Rapor için geçerli bağımsız field yoksa FAILURE_REPORT üretilmez; yalnız yerel delivery-failure olayı üretilir.

## 12. Maliyet ve seri alan encoding kuralları

### 12.1 Potential / cost

Advertised Potential 32-bit unsigned fixed-point **cost quanta**dır. Kuantanın fiziksel birimi yoktur; her uyumlu node aynı `CostQuantum` profilini kullanmalıdır. v0.1 M0.1 ortak dönüşüm/tablesi `35`te tanımlıdır ve görev öncesi admission ile eşlenir; packet body yeni bir MetricProfile-ID taşımaz.

| Değer | Semantik |
|---|---|
| `0` | Yalnız hedef originator'ın REACHABLE potansiyeli. |
| `1…0xFFFFFFFE` | Sonlu, pozitif toplam yönlendirme maliyeti. |
| `0xFFFFFFFF` | `∞`; yalnız WITHDRAWAL ile birlikte. |

Yerel `C_hop`, `C_quality` ve `C_risk` hesapları aynı kuantaya nicemlenir; toplama taşması `∞`ye doyurulur ve node withdrawal/repair davranışını uygular. M0.1 için bu tamsayı dönüşümler ve `C_hop=16` `35`te normatiftir. Kayan nokta, NaN, negatif değer veya farklı CostQuantum'la hesaplanan potential geçersizdir.

### 12.2 Serial alanlar

DFSN ve ADS, 32-bit RFC 1982 serial alanlarıdır. İlgili sender/originator, aynı alıcının saklama penceresi içinde seri uzayın yarısından fazla ilerlemeyecek biçimde artış hızını sınırlandırmalıdır. Eşitlik dışındaki tanımsız yarım-aralık karşılaştırması fail-closed'dur.

Message Sequence, Data Sequence ve Request Sequence de 32-bit unsigned serialdir. Her source/sender instance, ilgili duplicate-cache ömründe aynı sequence değerini tekrar kullanmamalıdır. Security Profile 1'de authenticated control Message Sequence ayrıca aktif peer için R1 anti-replay high-water değeridir: eşit, eski veya half-space ambiguous değer kabul edilmez. DATA Sequence, source proof ve Data-ID duplicate cache'iyle birlikte çalışır; persistent exactly-once semantics sağlamaz.

## 13. TLV uzantı biçimi

Core body sonrasında, Header Length'e kadar sıfır veya daha fazla TLV bulunabilir. Her TLV şu biçimdedir:

```text
 +---------------+---------------+-------------------+
 | TLV Type (8)  | Length (8)    | Value (Length*8)  |
 +---------------+---------------+-------------------+
                 followed by 0–3 zero padding octets
```

| Alan | Bit | Semantik |
|---|---:|---|
| TLV Type | 8 | Bit 7 `Critical`; bit 0–6 TLV numarası. Bilinmeyen critical TLV tüm paketin reddini gerektirir; bilinmeyen non-critical TLV atlanır. |
| Length | 8 | Value'nin octet sayısı; padding'i kapsamaz. |
| Value | `0…2040` | Type'a özgü içerik. Toplam header 255 octeti aşamaz. |
| Padding | `0…24` | Sonraki TLV'nin 32-bit hizalanması için sıfır octetler; Header Length'e dahildir. |

Bu sürümde tanımlı uzantılar:

| Type | Critical | Ad | Value semantiği |
|---:|---|---|---|
| `0x00` | Hayır | PAD | Boş veya sıfır dolgu; alıcı atlar. |
| `0x01` | Hayır | CAPABILITY | Gönderenin isteğe bağlı profil/yetenek bitmap'i; forwarding güvenliğini değiştirmez. |
| `0x02` | Hayır | DIAGNOSTIC | Denetim için profile-bağımlı ölçüm/olay; risk veya jamming hükmü olarak işlenmez. |
| `0x81` | Evet | AUTHENTICATION | Security Profile 1 için zorunlu, tek ve son TLV'dir. HOP, FIELD_UPDATE için ORIGIN, DATA için SOURCE imza blokları `26`da tanımlıdır. |

Bir TLV, core body'deki Field-Key, DFSN, potential, hop-limit, routing state veya replication budget semantiğini değiştiremez. Security Profile 1'in Source-RB alt alanı core RB için imzalı üst sınırdır; core semantiğini değiştirmez. Başka türde değişiklik yeni protocol version veya explicit core-field değişikliği gerektirir.

## 14. Minimum header boyutları

| Packet Type | Base + core | Uzantısız Header Length | Security Profile 1 asgari Header Length |
|---|---:|---:|---|
| DATA | 4 + 32 | 36 octet | 194 octet (HOP + SOURCE) |
| FIELD_UPDATE | 4 + 24 + 32 | 60 octet | 210 octet (HOP + ORIGIN) |
| FIELD_SOLICIT | 4 + 24 + 24 | 52 octet | 130 octet (HOP) |
| DFSN_REQUEST | 4 + 24 + 44 | 72 octet | 150 octet (HOP) |
| PROBE | 4 + 24 + 12 | 40 octet | 118 octet (HOP) |
| PROBE_REPLY | 4 + 24 + 24 | 52 octet | 130 octet (HOP) |
| FAILURE_REPORT | 4 + 24 + 56 | 84 octet | 162 octet (HOP) |

Header Length veya packet uzunluğu bu değerlerle uyumsuzsa paket geçersizdir. Security Profile 1 etkinse sağdaki minimumlar geçerlidir; tüm değerler 255-octet Header Length üst sınırının içindedir. DATA'da uygulama payload uzunluğu sıfır olabilir; kontrol paketlerinde payload yasaktır.

## 15. Validation ve error handling özeti

Alıcı aşağıdaki durumda paketi field/neighbor state değiştirmeden bırakır:

- desteklenmeyen Version veya reserved Packet Type/flag;
- Header Length, core size, TLV length veya padding tutarsızlığı;
- `0` kimlik/instance, rezerve değerin sıfır olmaması;
- illegal potential/state/lifetime bileşimi;
- serial aritmetikte tanımsız kıyaslama;
- Hop Limit `0` veya tek-atlama mesajında `1` olmaması;
- bilinmeyen critical TLV;
- Security Profile 1'e aykırı, eksik/çift/son olmayan veya doğrulanamayan AUTHENTICATION; roster/Key-ID/Sender-ID uyuşmazlığı; gerekli Origin/Source proof yokluğu;
- duplicate/expired Request-ID veya control Message-ID.

Bir node hata sayacı tutabilir fakat malformed pakete hata paketi üreterek kontrol amplifikasyonu yapmaz.

## 16. Onaylanan wire ve güvenlik eki

Onaylanan v0.1 wire profili:

- 4-octet ortak base header;
- 64-bit opaque node/destination/OIID/instance kimlikleri;
- 32-bit RFC 1982 DFSN ve ADS;
- 32-bit sabit-noktalı, doygunluklu potential; `∞` withdrawal'a ayrılmış;
- mesaj türüne özgü sabit core body + 32-bit hizalı TLV alanı;
- Security Profile 1 için zorunlu AUTHENTICATION kritik uzantısı: hop integrity, FIELD_UPDATE target-origin proof ve DATA source integrity.

**Kazanç:** Alan güvenliği için gereken ID/serial ayrımları pakette açık kalır; floating-point farklılıkları engellenir; unknown critical uzantı sessiz yanlış yorumlanmaz.

**Bedel:** FIELD_UPDATE uzantısız 60 octet, DFSN_REQUEST 72 octet header taşır. Bu, güvenli freshness/duplicate/withdrawal davranışı için açık state maliyetidir; timer ve compression/aggregation optimizasyonu sonraki fazlarda değerlendirilir.

Bu wire profile ve Security Profile 1 eki, bütün uygulama ve güvenlik etkileşimlerini belirlediği için MAJOR olarak onaylanmıştır.
