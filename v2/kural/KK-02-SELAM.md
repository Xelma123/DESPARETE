# KK-02 · Selam ve ara ilan

> Kararlar: T-1 · T-16 · T-17 (`17`). Değerler `KK-00`. Güncel: 17 Kasım 2026.

## Amaç ve sınıf

Komşuların varlığını ve iki yönlü bağ kalitesini ölçmek (KK-01), geçide uzaklığı ilan etmek (KK-04) ve karıştırılan alıcının durumunu bildirmek (KK-03) için tek bir ileti. **Genel**; uyarlanır aralık bayrağı `uyarlanir_aralik`, alıcı biti `alici_bildirimi`.

## İletinin alanları (`13` §02.1, `MesajBicimi`)

| alan | bit | anlamı |
|---|---|---|
| `sira` | 16 | her selamda bir artar (KK-01'in sayımı) |
| `aralik` | 16 | o anki aralık, 0,01 s biriminde (Ö-5) |
| `tur` | 16 | seçili rotamın turu: ardılımın ilan ettiği tur, geçitte kendi turu (KK-04 kural 6) |
| `maliyet` | 16 | geçide maliyetim, ETX × 64 tamsayı; 0xFFFF = ∞ |
| `karistiriliyorum` | 1 | KK-03'ün kendi durumu |
| `komsular` (tekrarlı) | 8 + 8 | komşu adresi · ondan aldığım selam oranı (`d_r` × 255) |

Boyut: sabit 9 bayt + komşu başına 2 bayt. 15 komşuyla 39 bayt; 64 baytlık çerçeve ek yüküyle 103 bayt, 1 Mb/s'de yaklaşık 1 ms.

## Kurallar

1. **Gönderim:** her düğüm `I` aralıkla selam yayar; titreşim `I`'nın %10'u (`KontrolIstegi.jitter_s`). Zamanlayıcı `Uyandirma` ile kurulur. Selam bastırılmaz (T-16).
2. **Aralığın uyarlanması** (Trickle mantığı [62]): olaysız geçen her selamdan sonra `I ← min(2·I, I_MAX)`. Bir **değişim olayında** `I ← I_MIN` ve selam hemen (titreşimle) gönderilir; bu, ara ilandır (T-17). İki selam arasında en az `SELAM_ARASI_EN_AZ` (= `I_MIN`) geçer; bu arada olan değişimler bir sonraki selamda birleşir.
3. **Değişim olayları** (T-17'nin listesi):
   - geçide maliyetim son ilan ettiğimden `ILAN_ESIGI` kadar farklı ya da ∞ ↔ sonlu;
   - ilan ettiğim tur değişti (KK-04);
   - `karistiriliyorum` bitim değişti (KK-03);
   - yeni bir komşu duyuldu (iki yönlü ölçüm çabuk kurulsun).
   Bir komşunun durumunun değişmesi tek başına olay değildir: rotamı değiştiriyorsa maliyet ya da tur maddesine zaten girer. Böylece karıştırma sırasında, kanal zorlanırken selam seli oluşmaz.
   T-10'un "karıştırma başlayınca selamlar sıklaşır"ı böyle karşılanır: karıştırılan düğüm bitini değiştirince, rotası etkilenen komşular da maliyetlerini ilan edince aralıkları en küçüğe iner.
4. **Ara ilan ayrı bir ileti değildir:** sıra numarası alır, KK-01'in sayımına girer ve aralığı sıfırlar.
4a. **Gönderemezken selam kurulmaz:** kendi ED işaretim varken (KK-03; kanal meşgul, gönderemem) yeni selam kurulmaz; işaret bitince hemen bir selam gönderilir. Sebep: ileti içeriği kurulduğu anda donar; karıştırma boyunca biriken selamlar kanal açılınca bayat bilgiyle (eski maliyet, eski bit) art arda giderdi.
5. **Alınca:** KK-01'e (sıra, aralık, benim için bildirilen oran), KK-03'e (bit, selam geldi olayı), KK-04'e (tur, maliyet) dağıtılır. Göndereni listesinde beni bildirmiyorsa `d_f = 0`.
6. `maliyet` ve `tur` ilan edildiği anda KK-04'ün FD'si güncellenir (T-12).

## Örnek

Sakin bir ağda düğüm 0,5 → 1 → 2 s'ye çıkar ve 2 s'de kalır. Karıştırılan bir düğüm "karıştırılıyorum" bitini 1 yapınca hemen bir selam gönderir; karıştırma bitip bit 0'a dönünce yine hemen gönderir, bu yüzden bitiş beklemeden duyulur. Ardılı karıştırılan komşusu yedeğe geçer; maliyeti %15'ten çok değiştiyse o da hemen ilan eder. 40 düğüm 2 s'de bir selam gönderirken bir düğümün duyduğu selamlar kanalın kabaca %1'ini kaplar (15 komşu × 0,5/s × 1 ms).

## Sınanması

- `uyarlanir_aralik` açık ↔ kapalı (sabit 2 s): kontrol payı (T-19), sessiz dönemin başında toparlanma süresi, ikizde fark yok.
- `I_MAX` 2 ↔ 4 s: kontrol payı ↔ karıştırmanın fark edilme süresi.

## Kaynak

Selam, aralık alanı ve ters yön bildirimi Babel [4] (RFC 8966 §3.4, §4.6.5) ve ETX [36]; aralığın iki katına çıkıp değişimde en küçüğe inmesi Trickle [62] (RFC 6206 §4.2; bastırması alınmadı); ilanın selamla birleşmesi ve "önemli değişim" kuralı Babel [4] (§3.7.2).
