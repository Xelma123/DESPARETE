# KK-02 · Selam ve ara ilan

> Kararlar: T-1 · T-16 · T-17 (`17`). Değerler ve genel kurallar `KK-00`. Kod `protokoller/desparete5_selam.py`. Güncel: 19 Kasım 2026 (`17` T-12, T-13, T-17: eğimde tur alanı yok; ara ilan olaylarına son çare seçimi ve döngü işareti girdi, tur isteğinin yanıtı çıktı). Önceki: 18 Kasım (`v2/arsiv/kural/KK-02-SELAM-2026-11-18.md`; kodlamayla Y-5 · Y-12, G-5).
>
> **Kod:** 19 Kasım'da bu kâğıda göre yazıldı. 18 Kasım'ın davranışı `egim` · `vazgecme_tetigi` · `duzgun_gecis` kapalı, `veri_kotu_tetigi` açık ve `DEGERLER_ESKI`yle birebir yeniden üretilir (küçük test dünyasında sekiz koşuda denetlendi: `arsiv/teshis/faz5_3_kod_2026-11-19/esdegerlik.txt`).

## Amaç ve sınıf

Komşuların varlığını ve iki yönlü bağ kalitesini ölçmek (KK-01), geçide uzaklığı ilan etmek (KK-04) ve karıştırılan alıcının durumunu bildirmek (KK-03) için tek bir ileti. **Genel**; uyarlanır aralık `uyarlanir_aralik`, alıcı biti `alici_bildirimi` (karıştırmaya karşı).

## İletinin alanları (`13` §02.1, `MesajBicimi`)

| alan | bit | anlamı |
|---|---|---|
| `sira` | 16 | 0'dan başlar, her selamda bir artar, modüler karşılaştırılır (KK-01'in sayımı) |
| `aralik` | 16 | bir sonraki planlı selama kadarki **üst sınır**, 0,01 s biriminde: bu selamdan sonra geçerli olacak aralığın (ikiye katlamadan sonraki `I`) titreşim dâhil 1,1 katı (RFC 8966 §4.6.5) |
| `tur` | 16 | **yalnız `egim` kapalıyken** (18 Kasım kuralları): seçili rotamın turu. Eğimde bu alan yoktur (T-13) |
| `maliyet` | 16 | geçide maliyetim, ETX × 64 tamsayı (yukarı yuvarlanır, sonlu en çok 0xFFFE); 0xFFFF = ∞ |
| `karistiriliyorum` | 1 | KK-03'ün kendi durumu; `alici_bildirimi` kapalıyken hep 0 |
| `komsular` (tekrarlı) | 8 + 8 | kayıtlı komşunun adresi · ondan aldığım selam oranı (`d_r` × 255, aşağı yuvarlanır); komşu listeye ancak en az `ORNEK_EN_AZ` örnekten sonra girer: tek örnekle 1,0 bildirilmez (Y-12) |

Boyut (`13` §02.1, `⌈bit / 8⌉`): eğimde sabit 49 bit → 7 bayt + komşu başına 2 bayt; 15 komşuyla 37 bayt, 64 baytlık çerçeve ek yüküyle 101 bayt, 1 Mb/s'de PLCP dâhil yaklaşık 1 ms. `egim` kapalıyken `tur`la sabit 65 bit → 9 bayt. `alici_bildirimi` ve `uyarlanir_aralik` kapalıyken alanlar bırakılır; boyut değişmez.

## Kurallar

1. **Gönderim:** her düğüm `I` aralıkla selam yayar; başlangıçta `I = I_MIN`. Titreşim `[0, 0,1·I]` zamanlayıcıya (`Uyandirma.jitter_s`) eklenir ve selam uyandırma anında, o anki bilgiyle kurulur: içerik titreşim boyunca bayatlamaz, kural 5 kurma anında denetlenir (18 Kasım, G-5). Uyandırmalar iptal edilemediği için her plan bir nesil numarası taşır; eski nesilden gelen uyandırma yok sayılır. Selam bastırılmaz (T-16).
2. **Aralığın uyarlanması** (`uyarlanir_aralik`; Trickle mantığı [62]): olaysız geçen her selamdan sonra `I ← min(2·I, I_MAX)`. Selamın `aralik` alanı bu yeni değerin üst sınırını taşır; böylece alıcının zaman aşımı (1,5 × `aralik`) olağan ikiye katlamada sahte kayıp saymaz. Bayrak kapalıyken `I` sabit `I_MAX`'tır.
3. **Ara ilan** (T-17; bayraktan bağımsız, çekirdek): bir **değişim olayında** `I ← I_MIN` ve selam hemen (titreşimle) gönderilir. `uyarlanir_aralik` kapalıyken ara ilan yine hemen gider ama `I` değişmez (`I_MAX`); yoksa katlama kapalı olduğu için `I` ilk olaydan sonra `I_MIN`'de kalırdı (18 Kasım, Y-5). İki selam arasında en az `SELAM_ARASI_EN_AZ` (= `I_MIN`) geçer; bu arada olan değişimler bir sonraki selamda birleşir. Değişim olayları:
   - geçide maliyetim son ilan ettiğimden `ILAN_ESIGI` kadar farklı ya da ∞ ↔ sonlu (KK-04 kural 7);
   - son çare seçimi: yokuş yukarı bir komşuya geçtim, maliyetim yükseldi (KK-04 kural 4);
   - döngü işareti: bayat bilgi ya da kesin döngü (KK-04 kural 8–9);
   - (yalnız `egim` kapalıyken) turum, bekleyen bir tur isteğini karşılayan bir değişimle değişti (arşivdeki KK-04 kural 9);
   - `karistiriliyorum` bitim değişti (`alici_bildirimi` açıkken; KK-03);
   - yeni bir komşu duyuldu (iki yönlü ölçüm çabuk kurulsun).
   Bir komşunun durumunun değişmesi tek başına olay değildir: rotamı değiştiriyorsa maliyet maddesine zaten girer. Böylece karıştırma sırasında, kanal zorlanırken selam seli oluşmaz. T-10'un "karıştırma başlayınca selamlar sıklaşır"ı böyle karşılanır: karıştırılan düğüm bitini değiştirince, rotası etkilenen komşular da maliyetlerini ilan edince aralıkları en küçüğe iner.
4. **Ara ilan ayrı bir ileti değildir:** sıra numarası alır, KK-01'in sayımına girer, aralığı sıfırlar.
5. **Gönderemezken selam kurulmaz:** kendi ED kaynaklı "karıştırılıyorum" durumumda (KK-03; kanal meşgul, gönderemem) yeni selam kurulmaz ve zamanlayıcı yeniden kurulmaz; bu sırada değişim olayları da selam planlamaz (planlasaydı her uyanma yeni bir boş uyanma doğururdu). Durum bitince ya da kaynak girişime geçince hemen bir selam gönderilir; o selam o anki bilgiyi taşır. Bitiş bir değişim olayı sayılır (kural 3): karıştırmanın bittiği komşulara çabuk duyulsun (T-10). Sebep: ileti içeriği kurulduğu anda donar; karıştırma boyunca biriken selamlar kanal açılınca bayat bilgiyle art arda giderdi. `karistirma_durumu` kapalıyken bu kural da yoktur.
6. **Alınca:** KK-01'e (sıra, aralık, benim için bildirilen oran; göndereni listesinde beni bildirmiyorsa oran bilinmiyordur, `d_f` değişmez: KK-01 "Gördüğü", Y-12), KK-03'e (bit, selam geldi olayı), KK-04'e (maliyet; `egim` kapalıyken tur da) dağıtılır.
7. `maliyet` ilan edildiği anda KK-04'ün `C_ilan`'ı olur (yokuş aşağı koşulunun dayanağı, KK-04 kural 3); ilan edilen nicemlenmiş değerdir. `egim` kapalıyken FD de bu değerle güncellenir (arşivdeki KK-04).

## Örnek

Sakin bir ağda düğüm 0,5 → 1 → 2 s'ye çıkar ve 2 s'de kalır; her selam bir sonrakinin en geç ne zaman geleceğini söyler (1,1 → 2,2 → 2,2 s). Karıştırılan bir düğüm bitini 1 yapınca hemen bir selam gönderir; karıştırma bitip bit 0'a dönünce yine hemen gönderir. Ardılı karıştırılan komşusu yedeğe geçer; maliyeti %15'ten çok değiştiyse o da hemen ilan eder. Bir düğümün duyduğu selamlar kanalın kabaca %1'ini kaplar (15 komşu × 0,5/s × 1 ms).

## Sınanması

- `uyarlanir_aralik` açık ↔ kapalı (sabit 2 s): kontrol payı (T-19); ikizde pencere PDR'si; sessiz dönemin başında toparlanma süresi.
- `I_MAX` 2 ↔ 4 s: kontrol payı ↔ karıştırmanın fark edilme süresi.

## Kaynak

Selam, aralık alanı (üst sınır olarak) ve ters yön bildirimi Babel [4] (RFC 8966 §3.4, §4.6.5) ve ETX [36]; aralığın iki katına çıkıp değişimde en küçüğe inmesi Trickle [62] (RFC 6206 §4.2; bastırması alınmadı); ilanın selamla birleşmesi ve "önemli değişim" kuralı Babel [4] (§3.7.2).
