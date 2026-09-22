# DESPARETE — Güvenlik Profili v0.1

**Sürüm:** 0.1 (onaylı güvenlik semantiği; performans profili değildir)  
**Durum:** Public-key roster, target-origin authorization, hop bütünlüğü, R1 control anti-replay ve DATA source integrity için ilk-sürüm profili.  
**Tarih:** 2026-09-21

## 1. Kapsam ve güvenlik sınırı

Bu profil, açık radyo ortamında dış saldırgan paket enjeksiyonuna karşı ve en az bir katılımcı node'un kötü niyetli olabileceği varsayımıyla tasarlanmıştır. Yalnız group secret kullanan bir profil seçilmemiştir. Her participating node için görev öncesinde güvenilir biçimde yüklenmiş bir public-key roster bulunur.

Profil şunları sağlar:

- her kabul edilen DESPARETE paketi için mevcut hop sender bütünlüğü ve kimliği;
- her `(Destination-ID,OIID,DFSN)` bağlamı için target-only origin authorization;
- aktif bir authenticated peer ile aynı çalışma oturumu içindeki eski control paketlerinin R1 anti-replay reddi;
- DATA'nın kaynak kimliği ve immutable içeriği için source integrity.

Profil şunları sağlamaz:

- RF jamming, paketi seçici drop/delay, fiziksel konum sahteciliği veya radyo erişilebilirliği;
- doğrulanmış kötü niyetli node'un kendi potentiali, quality/hazard ölçümü veya request nedeninde yalan söylemesi;
- DATA için exactly-once teslim veya `T_data_duplicate` ötesinde kalıcı anti-replay;
- payload gizliliği, trafik analizi gizliliği, anahtar dağıtımının uçuş sırasında yenilenmesi veya compromised private key'in geri alınması.

Gizlilik gerekiyorsa, uygulama payload'u ayrı bir application-layer AEAD profiliyle korunur. Bu profile ait AUTHENTICATION TLV yalnız bütünlük/menşei sağlar; şifreleme sağlamaz. [RFC 5116](https://www.rfc-editor.org/rfc/rfc5116.html)

## 2. Güvenilir tedarik ve kimlik bağları

Her node, görev başlangıcından önce aşağıdaki salt-okunur rosterı yükler:

```text
TrustRoster[Node-ID] = {
    active Key-ID values,
    Ed25519 public key for each active Key-ID
}
```

`Node-ID` ve `Key-ID` 64-bit opak, sıfır olmayan değerlerdir. Bir `Key-ID`, rosterda tam olarak bir `Node-ID` için aktif olmalıdır. Görev sırasında roster değiştirme, sertifika zinciri indirme veya kontrol paketiyle key rollover yoktur. Bu sınır, key yönetimini routing control düzleminden ayırır.

Security Profile `1`, Ed25519'i kullanır. Ed25519 32-octet public key ve 64-octet signature kullanır. [RFC 8032](https://www.rfc-editor.org/rfc/rfc8032.html) İmza uygulaması kendi kripto üretimi değil, uygun şekilde doğrulanmış bir kripto kütüphanesi olmalıdır.

Tek-sink operasyon profilinde `Destination-ID`, target'ın `Node-ID` değeridir. Origin proof'taki Key-ID bu target'ın roster kaydıyla eşleşmelidir. Çok-hedef genişlemesi, her Destination-ID için eşdeğer target-key bağını açıkça tanımlamadan bu profili yeniden kullanamaz.

## 3. AUTHENTICATION TLV, Profile 1

Security Profile 1'de her DATA ve control paketi, son TLV olarak tam bir kritik `AUTHENTICATION` (`0x81`) TLV taşımalıdır. AUTHENTICATION TLV'si olmayan, birden fazla AUTHENTICATION TLV taşıyan, son TLV olmayan veya aşağıdaki biçime uymayan paket bırakılır.

```text
 +----------------+----------------+----------------+----------------+
 | SecProfile (8) | AuthFlags (8)  | Reserved (16)                    |
 +-------------------------------+------------------------------------+
 | Hop-Key-ID (64)                                                    |
 +--------------------------------------------------------------------+
 | Hop-Signature (512)                                                |
 +--------------------------------------------------------------------+
 | [Origin-Key-ID (64) | Origin-Signature (512)]     if ORIGIN = 1   |
 +--------------------------------------------------------------------+
 | [Source-Key-ID (64) | Source-RB (8) | Reserved (56) |             |
 |  Source-Signature (512)]                            if SOURCE = 1 |
 +--------------------------------------------------------------------+
```

| Alan | Değer / kural |
|---|---|
| `SecProfile` | Tam `1` olmalıdır. Başka değer bu v0.1 profilde geçersizdir. |
| `AuthFlags.HOP` | Bit 0, her pakette `1` olmalıdır. |
| `AuthFlags.ORIGIN` | Bit 1, yalnız FIELD_UPDATE'ta `1` olmalıdır. |
| `AuthFlags.SOURCE` | Bit 2, yalnız DATA'da `1` olmalıdır. |
| Diğer `AuthFlags` ve tüm Reserved | Sıfır olmalıdır. |
| `Hop-Key-ID` | Control Sender Block'taki Sender-ID'nin roster key'i olmalıdır. DATA'da gönderimi yapan mevcut hop'un key'idir; DATA core body source key'i değildir. |
| `Origin-Key-ID` | FIELD_UPDATE Destination-ID'nin, yani target'ın aktif roster key'i olmalıdır. |
| `Source-Key-ID` | DATA `Data Source-ID`nin aktif roster key'i olmalıdır. |
| `Source-RB` | Source tarafından imzalanan başlangıç replication budget'tır; paket core body `RB ≤ Source-RB` olmalıdır. |

AUTHENTICATION Value uzunluğu yalnız HOP için `76`, HOP+ORIGIN için `148`, HOP+SOURCE için `156` octettir. TLV'nin 2-octet type/length alanı dahil edildiğinde, profile ait minimum header uzunlukları §7'de verilir.

Roster, `Hop-Key-ID → Node-ID` için tersine de tekil eşleme sağlar. Control pakette bu Node-ID, Control Sender Block'taki Sender-ID ile eşleşmelidir. DATA core body current-hop Sender-ID taşımaz; alıcı, AUTH içindeki Hop-Key-ID'nin roster sahibini authenticated ingress identity olarak kullanır. Link taşıyıcısı bir komşu kimliği veriyorsa bu kimlik de roster sahibine bağlanmalıdır; uyuşmazlık paket reddidir.

## 4. Canonical imza girdileri

Bu bölümün byte dizileri canonicaldır: sabit domain string octetleri ASCII'dir; sayısal alanlar wire'daki big-endian encoding ile yazılır; imza alanları kendileri asla girdiye dahil edilmez.

### 4.1 HopSignature

`HopSignature`, paketin iletilmek üzereki gerçek byte dizisini bağlar:

```text
HOP_INPUT = all packet bytes before AUTHENTICATION TLV
            || DATA payload, if packet Type = DATA
```

Taban `Header Length` değeri, Hop Limit, Control Sender Block, tüm core alanlar ve AUTHENTICATION'dan önceki TLV'ler bu girdinin içindedir. Bu nedenle forwarder DFSN_REQUEST'ta Hop Limit'i azalttığında veya DATA'da RB'yi azalttığında, önce kendi current-hop bilgisiyle yeni HopSignature üretmelidir. HOP_INPUT, AUTHENTICATION TLV'nin type, length, value veya padding'ini içermez.

Alıcı, önce `Hop-Key-ID`yi Sender-ID ile rosterda bağlar, sonra `Ed25519.Verify(Hop-Public-Key, HOP_INPUT, Hop-Signature)` çalıştırır. Sonuç başarısızsa paket sessizce bırakılır.

### 4.2 OriginSignature

Her FIELD_UPDATE, ileten node target olmasa da aşağıdaki target-origin proof'u taşır:

```text
ORIGIN_INPUT = "DESPARETE/ORIGIN/v1"
             || Destination-ID
             || Originator-Instance-ID
             || DFSN
```

Target, yeni OIID veya DFSN üretirken `OriginSignature` üretir. Ara node aynı `(Destination-ID,OIID,DFSN)` alanında kendi potential/ADS/Lifetime/withdrawal ilanını yaparken bu proof'u değiştirmeden taşır; yalnız kendi HopSignature'ını yeniler.

Alıcı, Destination-ID için rosterdaki target public key ile proof'u doğrulamadan yeni OIID/DFSN bağlamını kabul etmez. Origin proof, relay potentialini, ADS'yi veya Lifetime'ı yetkilendirmez; bunlar hop sender'ın imzalı fakat yine de yerel/olası kötü niyetli ilanlarıdır.

### 4.3 SourceSignature

Her DATA aşağıdaki immutable kaynak bağını taşır:

```text
SOURCE_INPUT = "DESPARETE/DATA/v1"
             || Application-Destination-ID
             || Data-Source-ID
             || Data-Source-Instance-ID
             || Data-Sequence
             || Traffic-Class
             || DFlags
             || Source-RB
             || Payload-Length
             || DATA payload
```

Source node, DATA'yı ilk gönderirken core `RB = Source-RB` yapar ve bu girdiyi imzalar. Forwarder yalnız `RB`yi azaltabilir; artırma, Source-RB değerini veya source proof'u değiştiremez. Alıcı, Source-Key-ID'nin Data Source-ID roster kaydıyla eşleştiğini ve SourceSignature'ın geçerli olduğunu doğrular. Hop Limit, mevcut core `RB` ve HopSignature source proof'a dahil değildir; bunlar hop-bağımlı alanlardır.

## 5. Paket türüne göre zorunluluk

| Paket türü | Zorunlu auth blokları | İlave doğrulama |
|---|---|---|
| DATA | HOP + SOURCE | `RB ≤ Source-RB`; DFlags bit 0 sıfırsa hem RB hem Source-RB sıfır. |
| FIELD_UPDATE | HOP + ORIGIN | Origin Key-ID targeta bağlanır; proof `(Destination-ID,OIID,DFSN)` ile eşleşir. |
| FIELD_SOLICIT | HOP | Sender rosterda olmalıdır. |
| DFSN_REQUEST | HOP | Forwarder değiştiğinde HopSignature yenilenir; requester end-to-end proof değildir. |
| PROBE | HOP | Target-Neighbour-ID, alıcı node ile eşleşir. |
| PROBE_REPLY | HOP | Taze, bekleyen Probe-ID ile tam eşleşir. |
| FAILURE_REPORT | HOP | Rapor, yalnız mevcut hop sender'ın doğrulanmış beyanıdır. |

## 6. R1 authenticated control anti-replay

Her node, aktif veya retention süresindeki authenticated komşu **örneği** için aşağıdaki state'i tutar:

```text
AR_i[(Sender-ID, Sender-Instance-ID)] = LastAcceptedControlSequence
```

Sadece Node-ID'si bilinen direct-peer candidate, Sender-Instance-ID'si imzalı bir control pakette ilk kez görülene kadar `AR_i` kaydı taşımaz. `HopSignature` geçerli ve packet sender ilişkisi rosterla doğrulandıktan sonra control paketin Message Sequence değeri bu state ile RFC 1982 serial aritmetiği kullanılarak karşılaştırılır:

- state tanımsızsa, paket yalnız aktif peer bağlamı, bu node'a hedeflenmiş authenticated ilk PROBE veya taze eşleşen PROBE_REPLY işlemi için ilk değer olabilir; bu ilk kabulde Message Sequence kaydı atomik kurulur, fakat peer ACTIVE yapılmaz;
- `NEWER` ise state yeni değer olur;
- `EQUAL`, `OLDER` veya `AMBIGUOUS` ise paket replay/stale kabul edilir ve hiçbir state değiştirmeden bırakılır.

Bu ilk-sürüm R1 profili reordering penceresi açmaz. Geç sıralı meşru control paketi yeniden denenebilir veya sonraki FIELD_UPDATE ile telafi edilir; safety ve anti-replay için eski paketi kabul etmekten daha önceliklidir. `AR_i` kaydı, authenticated Sender-Instance'ın ilk kabul edilen control paketiyle kurulur, komşu retention yaşamı boyunca tutulur ve komşu EXPIRED olduğunda silinir. Yeni sender instance, yalnız authenticated ve taze nonce-bağlı PROBE/PROBE_REPLY yoluyla forwarding-grade ACTIVE olabilir.

R1, receiver restartından sonra tüm eski control trafiğine karşı kalıcı koruma değildir. Ancak replay edilen paketin tek başına ACTIVE komşu yaratmasını engeller ve aktif peer için high-water geri sarılmasını yasaklar. Reboot-sonrası global replay reddi gerekiyorsa R2 gerekir; R2 target-monotonic generation ve non-volatile anti-replay state ekleyeceği için bu profilin dışındadır.

DATA'nın Data-ID duplicate cache'i, `T_data_duplicate` penceresinde tekrar forward/delivery'yi bastırır. Bunun ötesinde bu protokol exactly-once veya persistent data anti-replay iddia etmez; uygulama gerekiyorsa kendi delivery semantics'ini sağlar.

## 7. Wire sınırları

Profile 1'in AUTHENTICATION ekinden sonraki asgari header boyutları aşağıdaki gibidir:

| Paket türü | Base + core | AUTH TLV | Profile-1 asgari header |
|---|---:|---:|---:|
| DATA (HOP+SOURCE) | 36 | 158 | 194 octet |
| FIELD_UPDATE (HOP+ORIGIN) | 60 | 150 | 210 octet |
| FIELD_SOLICIT (HOP) | 52 | 78 | 130 octet |
| DFSN_REQUEST (HOP) | 72 | 78 | 150 octet |
| PROBE (HOP) | 40 | 78 | 118 octet |
| PROBE_REPLY (HOP) | 52 | 78 | 130 octet |
| FAILURE_REPORT (HOP) | 84 | 78 | 162 octet |

Hepsi 255-octet Header Length üst sınırının içindedir. Bu yalnız wire sığma kontrolüdür; RF MTU, airtime, CPU, batarya veya mission throughput açısından yeterlilik kanıtı değildir.

## 8. Kabul sırası, hata ve kaynak davranışı

Alıcı şu sırayı izler:

1. Ucuz biçim sınırlarını doğrular: version/type, Header Length, core minimumu, TLV/padding, reserved alanlar, AUTH TLV sayısı/konumu/uzunluğu, Hop Limit ve packet-type bağları.
2. Roster lookup ve Key-ID ↔ Node-ID bağını doğrular; bilinmeyen/revoked olmayan fakat rosterda bulunmayan key kabul edilmez.
3. HopSignature'ı doğrular. Başarısızsa paket bırakılır; neighbor/field/AR state'i değişmez.
4. Control için R1 Message Sequence kapısını, DATA için SourceSignature ve Source-RB kapısını çalıştırır.
5. FIELD_UPDATE için OriginSignature'ı doğrular; sonra mevcut OIID/DFSN/ADS/freshness ve ACTIVE candidate kuralları uygulanır.
6. Yalnız bütün kapılar geçtikten sonra PROBE/REPLY kanıtı, field, request, buffer veya forwarding state'i değiştirilir.

İmza doğrulaması pahalı olduğundan, node biçim sınırlarından önce kripto çalıştırmaz ve başarısız pakete hata yanıtı üretmez. Pre-auth verification rate limit ve kuyruk bütçesi platform profiline bağlıdır; ölçülmemiş sayısal değer bu tasarımda atanmaz. Bütçe taşarsa node yeni paketi bırakır; safe-successor veya security kapısını gevşetmez.

Geçersiz imzalı bir paket, mevcut bir komşunun ACTIVE durumunu tek başına SUSPECT/EXPIRED yapmaz. Aksi kural, herhangi bir saldırganın rastgele geçersiz paketle komşu düşürebilmesine yol açar. Yalnız geçerli authenticated link failure kanıtı veya mevcut neighbor yaşam döngüsü timerları field adayını kaldırabilir.

## 9. Güvenlik–doğruluk ilişkisi

Bu profil, `24`teki SA-01 varsayımını dış radyo saldırganının sahte packet üretmesine karşı güçlendirir: accepted FIELD_UPDATE'ın hop sender'ı rosterda doğrulanır ve yeni OIID/DFSN bağlamı target proof taşır. Bu, accepted relay'in kendi potentialini dürüst hesapladığını kanıtlamaz; loop-freedom teoremi tüm participating node'ların handler kurallarını uyguladığı varsayımına yine bağlıdır.

Bir compromised target private key, roster compromise veya valid node'un doğrudan routing davranışını değiştirmesi bu profile dışında kalan ciddi olaylardır. Bunlar gözlem/incident response konusu olabilir; otomatik reputation veya misbehavior routing bu ilk sürüme eklenmemiştir.

## 10. Doğrulama yükümlülükleri

| Yükümlülük | Beklenen negatif senaryo |
|---|---|
| AUTH biçimi | Eksik/çift/son olmayan AUTH TLV, yanlış length/flag/reserved reddedilir. |
| Hop identity | Sender-ID ile eşleşmeyen veya rosterda olmayan Key-ID, geçersiz imza reddedilir. |
| Origin authorization | Relay tarafından uydurulan OIID/DFSN veya başka target key'iyle proof reddedilir. |
| DATA integrity | Payload/Data-ID/DFlags/Source-RB değiştirilince source proof reddedilir; current RB, Source-RB'yi aşamaz. |
| Hop mutation | Forwarder Hop Limit/RB değiştirdiğinde eski HopSignature reddedilir; doğru yeniden imza kabul edilir. |
| R1 replay | ACTIVE peer'dan EQUAL/OLDER/AMBIGUOUS Message Sequence state'i değiştirmez. |
| Probe replay | Eski imzalı PROBE_REPLY, taze local Probe-ID ile eşleşmez ve ACTIVE kanıtı olmaz. |
| DoS davranışı | Malformed veya bad-signature paket hata paketi üretmez; verification budget aşımı forwarding safety'yi değiştirmez. |

Bu testler kriptografik kütüphane doğrulamasının veya saha performans ölçümünün yerine geçmez.
