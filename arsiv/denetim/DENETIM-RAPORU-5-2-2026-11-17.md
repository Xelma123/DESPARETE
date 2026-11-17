# Faz 5-2 · bağımsız içerik denetimi — rapor

> 17 Kasım 2026 · konu: `v2/17-TASARIM-KARARLARI.md` (kimlik, üç ilke, T-1…T-20), teşhis ölçümleri (a)–(d), Faz 5-2 aletleri, durum ve karar belgelerinin tutarlılığı · soru: 5-2 kapatılıp 5-3'e geçilebilir mi, geçilmeden önce ne yapılmalı.

## 0 · Başlık bilgisi

| | |
|---|---|
| denetlenen hâl | `main` @ `98b3875793cb5c0fc291959f13b6a5dd1b88bb9d` |
| başlangıç | `git rev-parse HEAD` → `98b3875…`; `git status --short` → boş |
| son | `git rev-parse HEAD` → `98b3875…`; `git status --short` → yalnız bu rapor (`?? arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md`) |
| yöntem | yalnız okuma. Git yalnız `log`, `show`, `diff`. Kayıtları okuyan dört kısa betik depo dışında (oturumun geçici klasöründe) koşuldu: (d)'nin ayırma güçlerinin bağımsız yeniden hesabı ve aynı alanla denetimi, (d)'nin teşhis (c)'yle birebirliği, T-20'nin geri iz oranları. Simülasyon, tam test takımı ve tohum kullanımı yok. PDF'ler `pdftotext` ile depo dışına çıkarılıp okundu |

**Okunanlar.**
- Belgeler: `v2/17` (tamamı) · `v2/16` (tamamı) · `v2/05` (tamamı) · `v2/12` (tamamı) · `v2/04` §6–§10 · `v2/README.md` · `v2/13` §02–§03 · `v2/06` (ilgili satırlar: §0.4, §5, §174) · `v2/02` G3 satırı · `protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md` (tamamı).
- Teşhisler: dört klasörün `beklenti.md` · `sonuc.md` (tamamı); (d)'nin `sonuc_hesap.py` · `sonuc_hesap.txt` · `ek_hesap.txt` (tamamı); (a)–(c)'nin `sonuc_hesap.txt` karar satırları; `zaman.txt`'ler; (c) ve (d)'nin `kayit_*.json`'ları betikle.
- Kod: `kalibrasyon/karistirma_isaretleri.py` (tamamı) · `kalibrasyon/kayip_anatomisi.py`'nin 5-2 farkı (`git diff bec9df3 98b3875`) · `tests2/test_karistirma_isaretleri.py` · `tests2/test_kayip_anatomisi.py`'nin 5-2 farkı · `sim2/kosum/dugum.py` `mesgul_guncelle` · `sim2/kosum/kontrol.py` `cerceve_duyuldu` · `sim2/kanal/karistirici.py` `gecis_anlari` ve sınıflar · `sim2/kanal/girisim.py` `parca_sinirlari` · `protokoller/babel.py` `_hello_kur`, `_hello_al` · `protokoller/babel_bicim.py` zamanlayıcılar · `protokoller/desparete.py` geri iz · `kalibrasyon/kahin.py` `_tek_deneme_basarisi` · `sim2/yapilandirma/konfig.py` `yol_kaybi_usteli`.
- Kaynaklar (asıl dosyada açılıp bakıldı): RFC 8966 §3.5.1, §3.5.3, §3.7.2, §3.7.3, §3.8.1.2, §3.8.2.1–§3.8.2.2, §4.2, §4.6.5 · RFC 6719 §3.2.2 ve önerilen değerler · RFC 6206 (bastırma) · Puñal 2014 [23] (§II ölçüler, Şekil 2–3, eşik bölümü, işbirliği ve Şekil 8) · De Couto 2003 [36] · Ramachandran 2007 [54] · Jonglez 2014 [55] · Cerar 2021 [57] · Tague 2011 [53] · Yang 2025 [59].

---

## 1 · Bulgular (ağırlığa göre)

### E-1 · engelleyici — "Açıklanamayan kanal meşguliyeti" bugünkü gözlem sözleşmesinde protokole görünmüyor

- **Yer:** `v2/17-TASARIM-KARARLARI.md:13` (kimlik: "Kanal dolu ama duyduğu çerçeveler bunu açıklamıyorsa…") · `:91` (T-5 işareti) · `:98` (≥ 0,58 eşiği) · `kalibrasyon/karistirma_isaretleri.py:30-32` · `v2/05-GOZLEM-PENCERESI.md:49-55`, `:108-115`.
- **Ne yanlış:** İşaret, CCA meşgul süresinden o saniyede çözülen çerçevelerin **hava süresinin** çıkarılmasıyla hesaplanıyor (`karistirma_isaretleri.py:262`, `:428-429`). Protokolün çözülen çerçeve hakkında aldığı bilgi `cerceve_duyuldu` kancasıyla gelir: gönderen, tür, adreslendiği düğüm, veri çerçevesinde paket başlığı ve RSSI (`v2/05:49-53`; `sim2/kosum/kontrol.py:237-238`). Çerçevenin süresi ya da hızı yoktur. Kaydedicinin kendi başlığı bunu söylüyor: hava süresi "gözlem penceresinde bugün yok — protokol kullanacaksa `05` §7 yolu ya da boyuttan tahmin (`beklenti.md` §0)" (`:30-32`). Atıf verilen `beklenti.md` §0 yok (beklentinin bölümleri: Sorular · Düzen · Tanımlar · Karar kuralı · Öngörüler · Duman koşusundan sonra). Bu çekince ne beklentiye, ne sonuca, ne `v2/17`ye ne de `v2/05`e girmiş. `v2/17` işareti kimliğin ve T-5'in merkezine koyuyor.
- **Kanıt:** `v2/05:49-55` alan listesi; `kontrol.py:237` çağrısı `(gozlem, gonderen, tip, hedef, rssi, gorunum)`; (d) `sonuc.md` §1 eşik tablosu.
- **Neden engelleyici:** `v2/05` bir sözleşmedir ve gerekçesiz genişletilmez (`:3`, `:108-115`); karşılaştırmanın geçerliliği buna dayanır (`:7`). 5-3'te kod T-5 üstüne kurulacak; işaretin nereden geleceği kod yazılmadan belli olmalı.
- **Öneri (biri seçilir ve `v2/17` T-5 ile kimliğe yazılır):**
  1. `v2/05` §7 yolu: alan gerekçesiyle `05`e, kararı `04`e girer, önceki sonuçların geçerliliği yazılır (gerçek telsiz PLCP başlığından süreyi bilir; gerekçe hazır).
  2. Sözleşme içinde tahmin: süre tür ve boyuttan, hız en düşük hız varsayılarak (denemelerin %94–96'sı 1 Mb/s'de, (b) `sonuc.md` §2); tahminin hatası 5-3'te ölçülür. Bunun için `cerceve_duyuldu`nun her çözülen çerçevede (onaylar dâhil) çağrıldığı ve boyutun görünür olduğu ayrıca doğrulanmalı.
  3. ED bölgesinde gözlenebilir `mesgul` kullanılır: (d)'de G 0,978 · 0,976, %80 yakalamada (≥ 0,62) ikizde yanlış alarm %0,035 (`sonuc.md` §1).
  Kaydedicinin `§0` atfı düzeltilir.

### E-2 · engelleyici — T-13'ün "uygulanamaz güncellemede rota bırakılmaz" kuralı döngüsüzlük için gereken koşulu taşımıyor

- **Yer:** `v2/17:179`, `:183`; ayrıca `:173` (FD tanımı).
- **Ne eksik:** RFC 8966'da seçili rotaya gelen uygulanamaz güncelleme için iki yol vardır: güncelleme **yok sayılır** (rota eski kabul edilen değeriyle kalır) ya da güncelleme uygulanır ve rota **hemen bırakılır** (§3.5.3, `rfc8966_babel.txt:1054-1065`; §3.8.2.2, `:1430-1441`). Sıra isteği bunun yanında gönderilir. `v2/17:179` yalnız "bırakılmaz; yeni tur istenir" diyor; güncellemenin yok sayıldığı yazılmamış. Kural "rotayı tut ve yeni maliyeti uygula" diye gerçeklenirse uygulanamaz bir rota seçili kalır; T-12'nin "döngü hiç oluşmaz" iddiası (`:174`) bu duruma dayanmaz. Araştırma notları doğru yazmış ("aynı kaynaktan gelen güncelleme yok sayılıyor", `NOTLAR.md:139`); karar metnine geçmemiş.
- **İlgili kesinlik:** `:173` FD'yi "benim bu turdaki en iyi maliyetim" diye tanımlıyor. RFC 8966'da FD, düğümün o kaynak için **gönderdiği** sonlu ilanların en küçüğüdür (§3.5.1, `:974-979`; bakımı §3.7.3, `:1249-1265`). T-16/T-17 ilanın zamanını değiştirdiği için (selamla ve yalnız önemli değişimde), hesaplanan ile ilan edilen maliyet arasında fark olacak; hangisinin FD'yi belirlediği yazılı olmalı.
- **Atıf:** `:183` yalnız §3.8.1.2'yi (isteğin yanıtı ve iletimi) gösteriyor; açlıkta istek §3.8.2.1, uygulanamaz güncelleme §3.5.3 ve §3.8.2.2'dir.
- **Öneri:** T-13'e "uygulanamaz güncelleme yok sayılır, seçili rotanın son kabul edilen maliyeti korunur; güncelleme uygulanırsa rota hemen bırakılır" cümlesi; T-12'ye "FD = bu turda ilan ettiğim en küçük maliyet"; ödünç satırına §3.5.1, §3.5.3, §3.8.2.1–§3.8.2.2.

### Ö-1 · önemli — Kimlik paragrafı karıştırma kanıtını teşhis (d)'nin gösterdiğinden kesin anlatıyor

- **Yer:** `v2/17:13`, `:15` ("son hâlini aldı").
- **Ne yanlış:**
  - "çözdüğü çerçeveler ve komşu selamları birlikte azalıyorsa karıştırılıyordur": birleşik kuralın başarısı ölçülmedi; (d) bunu açıkça yazıyor ("bu kayıt yalnız işaret başına dağılımları tuttuğu için birleşik kuralın başarısı buradan hesaplanamıyor", `sonuc.md:147`). Ayrıca çözülen çerçeve düşüşü karıştırmaya özgü değil (açık evrede uzak alanda 76 · 68 ↔ 99 çerçeve/s; G 0,652 · 0,710; `sonuc.md:148`, `ek_hesap.txt` C). Selam, çözülen çerçevenin alt kümesidir; iki işaret aynı olaydan beslenir, "birlikte azalma" ikinci bağımsız kanıt sayılamaz (ölçülmeden).
  - "tek bir kayıp ya da tek bir işaret karar için yetmez": ED bölgesinde tek işaret tek saniyede yetiyor (açıklanamayan meşguliyet ≥ 0,58, ikizde yanlış alarm 0; `sonuc.md:134-137`). Cümle girişim bölgesi için doğru, genel olarak değil.
  - "Kanal dolu ama duyduğu çerçeveler bunu açıklamıyorsa": E-1.
- **Öneri:** Kimlik cümlesi (d)'nin söylediğiyle sınırlanır: ED bölgesinde düğümün kendi kanal ölçümü; girişim bölgesinde birkaç işaret ve birkaç saniye birlikte, kuralın biçimi ve başarısı 5-3'te ölçülür.

### Ö-2 · önemli — Komşu başına işaretler ölçülmedi; T-6'nın "sessizleşen komşu" kanıtı ölçümle desteklenmiş gibi yazılmış

- **Yer:** `v2/17:92`, `:107`, `:110`; `kalibrasyon/karistirma_isaretleri.py:392-441`, `:432-433`.
- **Ne yanlış:**
  - (d)'nin `selam_kaybi`'ı **alıcının** düğüm-saniyesinde, bütün tanıdık komşulardan beklenen selamların kaçan payıdır ve alıcının alanıyla etiketlenir (`:392-441`). T-6'nın mekanizması başka bir büyüklüktür: bir komşunun, ED'deki **belirli bir göndericinin** sessizliğini tanıması (komşu başına, göndericinin alanına göre). `v2/17:110`'daki "komşularının 'sessizleşen komşu' kanıtı (selam kaybı) bu yüzden gerekli" ifadesi ikisini aynı sayıyor. Komşu başına sessizliğin ayırma gücü ve yanlış alarmı ölçülmedi; temizde selam kaybının 0,44 olması (`sonuc.md:151`) bu işaretin yanlış alarmının yüksek olabileceğini gösteriyor.
  - T-5 "komşulardan iki alım arasındaki en uzun süre"yi işaret sayıyor (`:92`; Puñal'in en uzun boşta kalma süresi, komşu başına). (d)'nin `sessizlik`i düğüm düzeyinde, herhangi bir komşudan son çözümden beri geçen süredir (`:432-433`). Girişimdeki "dışarıda" hükmü (`v2/17:99`) bu düğüm düzeyi ölçü içindir; Puñal'in komşu başına ölçüsüne aktarılamaz.
- **Öneri:** T-5 ve T-6 notlarında iki ölçü ayrılır; komşu başına sessizlik ve komşu başına en uzun boşluk 5-3'ün ölçüm listesine girer (yanlış alarm temizdeki %44 taban kayıpla birlikte okunur).

### Ö-3 · önemli — "Bağ kalitesi 32 s'de değişmiyor" sonucu doymuş bir ölçüye dayanıyor; T-1'e aktarılan yargı ölçüyü aşıyor

- **Yer:** `v2/17:55`; `v2/12-YOL-HARITASI.md:57`; `kalibrasyon/karistirma_isaretleri.py:551-553`; (d) `sonuc.md:83`, `:152`.
- **Ne yanlış:** S3 kâhinin **7 denemelik atlama başarısını**, `1 − (1 − p)^7`, ölçüyor (`:551-553`). "İyi" bant (≥ 0,90) tek deneme başarısı p ≥ 0,28'e karşılık gelir; bağ kalitesi büyük ölçüde değişse de bant çoğu zaman değişmez. Ölçülen bağlar en çok kullanılan 80 bağdır (seçilim gereği kararlı olanlar), hareket formasyondur ve ağın öteki iletimleri dışarıdadır (`kalibrasyon/kahin.py:234-238`). Her τ'da ortalama |Δp| 0,001 çıkması bu doymayla uyumlu. T-1'in selamı ise yeniden denemesiz, tek deneme bir yayının teslimini ölçer ve yedekler dâhil bütün komşulara bakar. `v2/17:55`'in "Selam aralığının üst sınırını hareket değil, karıştırmaya tepki hızı (T-10) ve açlık (T-13) belirler" yargısı bu ölçümden çıkmaz.
- **Öneri:** Cümle ölçünün kendisine indirilir ("en çok kullanılan bağların 7 denemelik atlama başarısı formasyonda 32 s içinde değişmiyor; tek deneme başarısı ve yedek bağlar ölçülmedi"); `v2/12:57` aynı. 5-3'te tek deneme başarısıyla ve bütün komşu bağlarıyla yeniden bakılır.

### Ö-4 · önemli — Teşhis (d)'nin kapsamı tek protokol ve tek karıştırıcı sınıfı; T-5'in hükümleri koşulsuz yazılmış

- **Yer:** `v2/17:94`, `:97-102`; (d) `beklenti.md:25`; `kalibrasyon/karistirma_isaretleri.py:77-78`.
- **Ne yanlış:**
  - Kol yalnız Babel-a (`beklenti.md:25`). `selam_kaybi` Babel'in 4 s'lik Hello'suna ve "son 16 s'de duyulmuş" tanımına bağlı (`:77-78`); `cozulen` ve `sessizlik` düzeyleri trafiğe bağlı. Yeni sürümün selamı uyarlanır aralıklı ve kontrol trafiği daha az olacak (T-1, T-16). "Dışarıda (kanıta girmez)" (`v2/17:99`) ve "güçlü" hükümleri bu trafiğe koşullu; `v2/17` bunu söylemiyor.
  - Sınıf yalnız sürekli (araç, derin sızma). `v2/17:94` "kanıt tek bir karıştırıcı türüne bağlanmaz" diyor; ama ED bölgesinin güçlü işaretleri (`mesgul`, açıklanamayan meşguliyet) CSMA'ya görünen karıştırıcıya bağlı. Simülatörde darbeli, reaktif, aldatıcı, taramalı sınıflar var (`sim2/kanal/karistirici.py:398-570`), `v2/06` H1.3 bunları kullanıyor ve `v2/12:92` her mekanizmanın A/B'sine bir yer karıştırıcılı aile koyuyor. Bunlarda işaretler ölçülmedi; 5-3 listesinde (`v2/17:125`) de yok.
- **Öneri:** T-5'in (d) notuna "Babel trafiğinde, sürekli sınıfta" koşulu; 5-3 listesine yeni sürümle yeniden ölçüm ve en az bir başka sınıf ya da yer karıştırıcılı aile.

### Ö-5 · önemli — Uyarlanır selam aralığı ile sayım ve sessizlik tespiti arasındaki bağ yazılmamış

- **Yer:** `v2/17:51` (T-1), `:58` (T-2), `:107` (T-6), `:148` (T-10), `:212-214` (T-16).
- **Ne eksik:** Aralık değişince alıcı, belli bir sürede kaç selam beklediğini (T-2'nin oranı) ve bir komşunun sustuğunu (T-6) ancak göndericinin o anki aralığını bilirse hesaplayabilir; sıra numarasındaki boşluk kaybı ancak sonraki selam gelince gösterir, hiç gelmeyen selamı göstermez. Babel bunu Hello'ya aralık alanı koyarak çözer (RFC 8966 §4.6.5, `rfc8966_babel.txt:1806`, `:1827`). `v2/17` selamın aralığını taşıyıp taşımadığını yazmıyor; 5-3 listesi yalnız "selamın biçimi ve boyutu" diyor (`:76`, `:231`).
- **Gerilim:** sessizliğe dayalı tespitin süresi "kaçan selam sayısı × aralık"tır. T-16'nın yük örneği 4 s'lik selamla (`:214`); bu aralıkla üç kaçan selam 12 s eder, dayanıklılık hücresinin 10 s'lik açık döneminden uzun. Hızlı tespit ile düşük kontrol yükü aynı üst sınırda çatışıyor; `v2/17:55` bunu kısmen görüyor, nicel seçim yazılı değil.
- **Öneri:** T-1/T-16'ya "selam o anki aralığını taşır" (Babel'deki gibi); 5-3 listesine "üst sınır ile sessizlik tespitinin süresi birlikte seçilir; kontrol payı T-19 ile birlikte okunur".

### Ö-6 · önemli — Bağın durum makinesi tanımsız (T-3 ↔ T-7 ↔ T-9 ↔ İlke 1)

- **Yer:** `v2/17:25`, `:66-69`, `:113-115`, `:141`.
- **Ne eksik:** T-9'a göre kanıt birikince bağ "karıştırılıyor" (T-7), kalitesi üst sınırı aşınca "kullanılmaz" (T-3) olur; ikisi aynı anda olabilir. Yazılı olmayanlar:
  - "karıştırılıyor" iken toplanan selam ve MAC örnekleri ETX penceresine girer mi;
  - girerse bağ T-3'ün sınırını da aşar; T-3'e göre dönüş, ölçülen kalitenin ikinci eşiği geçmesini bekler, T-7'ye göre ise kanıt kalkınca hatırlanan değerle hemen dönülür; hangisi önce gelir;
  - girmezse İlke 1'in mekanizması ("payı küçük uzun bağların teslimi önce düşer, maliyetleri artar ve rotalar kendiliğinden kısa bağlara kayar", `:25`) yalnız sezilmeyen karıştırmada işler.
- **Öneri:** Kod yazılmadan önce üç durum (olağan · kötü · karıştırılıyor), geçişleri ve pencerenin her durumda nasıl tutulduğu `v2/17`ye ya da açıkça 5-3'ün ilk kural kâğıdına yazılır.

### Ö-7 · önemli — T-18'in süre sınırı atlama başına mı uçtan uca mı belli değil; `PDR_açık`ın geç teslimi saymasına karşı koruma tamamlanmamış

- **Yer:** `v2/17:223`, `:225`, `:241`; `v2/05:31-33`; `v2/04-KARARLAR.md:116-117`, `:157`; teşhis (c) `beklenti.md:67`.
- **Ne eksik:**
  - "süre 5 s'lik gecikme tavanını aşmaz" (`:223`) bir rölenin tutma süresi için yazılmış görünüyor. Paketin yaşı protokole görünmez (`dogum_s` yok, saatler eşzamanlı değil; `v2/05:31-33`). Birkaç röle sırayla tutarsa uçtan uca gecikme 5 s'yi aşabilir; `PDR_açık` geç teslimi yine sayar. Gerekçedeki ölçü oyunu kaygısı (`:225`) 15 s'lik saklama için kapanmış, birden çok atlamada tutma için kapanmamış.
  - Gecikme tavanlı `PDR_açık`ın 5-3'te izlenmesi yalnız tavanın bedeli ≥ 0,02 olunca öngörülmüş (teşhis (c) `beklenti.md:67`); bekletme davranışı değişecekken her A/B'de raporlanması yazılı değil (T-19 yalnız kontrol payını zorunlu kılıyor).
  - T-20'de izsiz komut aynı tampona giriyor (`:241`); telemetriyle paylaşım ve öncelik yazılmamış. Tampon "dolunca en eski düşer" olduğu için komut telemetriyle yarışır. Birincil metrikte komutların yeri (KR-2) hâlâ açık (`v2/04:157`).
- **Öneri:** T-18'e sınırın türü (atlama başına sınır ve en çok kaç kez tutulabileceği, ya da başlıkta bedeli ödenen birikmiş bekleme alanı); T-19'un yanına "gecikme tavanlı `PDR_açık` (5 s) ve p99 her A/B'de raporlanır"; komut–telemetri paylaşımı 5-3 listesine.

### Ö-8 · önemli — `v2/12` §2 ile `v2/04` §6, `v2/17`'nin kararlarıyla çelişen mekanizma listelerini hâlâ taşıyor

- **Yer:** `v2/12-YOL-HARITASI.md:79-94`, `:123`; `v2/04-KARARLAR.md:110`.
- **Ne yanlış:** Faz 5 tablosu (K-228'in adayları) 5-2'nin kararlarından sonra işaretlenmeden duruyor ve kararlarla çelişiyor:
  - 5.6 "periyodik DFSN" (`v2/12:89`) ↔ T-13 "Tur düzenli aralıklarla artırılmaz" (`v2/17:180`);
  - 5.4 "PROTECT = seçici çok yol + çoğaltma" (`:87`) ↔ T-14 "Trafik komşulara bölünmez", çoğaltma çekirdekte yok (`v2/17:187-188`);
  - 5.3 "CAUTION/PROTECT postür" (`:86`) ↔ T-7'nin bağ başına "karıştırılıyor" durumu;
  - 5.2 öngörülü kaçınma `v2/17`de yok.
  Kaba plan (`v2/12:123`) "5.1 · 5.3 · 5.4" diye hesaplıyor. `v2/04:110` aynı eksikler listesini ("kanıta dayalı postür · PROTECT'in çok yolu ve çoğaltması") Faz 5'in konusu diye yazıyor. `v2/04` "bugün geçerli kararlar"ın, `v2/12` durumun tek yeri olduğu için çelişki bağlayıcı belgelerde.
- **Öneri:** Tablo "5-2 kararlarıyla aşıldı; güncel tasarım `17`" diye işaretlenir ya da T-n eşlemesiyle yeniden yazılır; kaba plan 5-3'ün gerçek A/B listesine göre; `v2/04:110` `17`ye atıfla değiştirilir.

### Ö-9 · önemli — Takvim bayat: mühür ~20 Kasım

- **Yer:** `v2/12:15`, `:96`; `v2/04:136`.
- **Ne yanlış:** Bugün 17 Kasım; 5-3 başlamadı. Planın kendi kaba hesabı Faz 5 için ~350 koşu ~80 sa, Faz 6 ~45 sa, Faz 7 ~190 sa (`v2/12:123-125`), proje hedefi 19 Aralık (`:15`). Mühür tarihi plan sırasıyla (5-3 → Faz 6) çelişiyor.
- **Öneri:** 5-3 açılmadan takvim yeniden yazılır: 5-3'ün A/B sayısı ve hesap saati, Faz 6'nın başlangıcı, mühür, Faz 7'nin başlangıcı, düşme sırası (`v2/12:135`).

### Ö-10 · önemli — "5-3'e kalanlar" listeleri eksik

- **Yer:** `v2/17:76`, `:125`, `:157`, `:197`, `:231`, `:245`.
- **Ne eksik** (yukarıdakilerin dışında kalanlar):
  - T-17'nin ara ilanı bir selam mı (sıra numarası alır, aralığın zamanlayıcısını sıfırlar mı), ayrı bir ileti mi (`:218`);
  - T-20'nin izi "karıştırılıyor" (T-7) ya da "kötü" (T-3) işaretli komşuyu gösteriyorsa iz bayat mı sayılır; v0.4.1 izi yalnız MAC vazgeçmesinde siliyor (`protokoller/desparete.py:459-463`);
  - `rssi_olcum_sigma_db` ve `gps_dikey_sigma_m` SINANMAMIŞ kayıtları (`v2/04:144`): RSSI artık okunuyor (T-5), kendi konumun okunup okunmayacağı ise yazılmamış (T-15 yalnız selama konum eklenmeyeceğini söylüyor);
  - mekanizmaların ablasyon bayraklarına eşlenmesi ve Aile 3'ün mekanizma kapısına hangilerinin gireceği; `v2/06:46` eski adlarla ("5.1 karıştırma kanıtı · 5.3 postür · 5.4 PROTECT") duruyor.
- **Öneri:** E-1, Ö-2…Ö-7 ve bu maddeler bölüm sonlarındaki listelere ya da `v2/17` sonunda tek bir "5-3'ün açılış listesi"ne yazılır.

### K-1 · küçük — T-3'ün ödünç satırı, bağın kullanılabilirliğindeki iki eşiği rota seçimi histerezisine bağlıyor

- **Yer:** `v2/17:71` (aynı bölüm `:70` iki konunun ayrı olduğunu söylüyor).
- **Kanıt:** MRHOF'ta bağ için tek bir sınır var (sınırı aşan bağ dışarıda kalır); histerezis ebeveyn değiştirmede, yol maliyeti farkı eşiği altında kalınca mevcut ebeveynle sürmektir (RFC 6719 §3.2.2, `rfc6719_mrhof.txt:302-320`). Jonglez 2014'teki Babel histerezisi de rota değiştirme içindir.
- **Öneri:** "Üst sınır MRHOF [64]; iki eşikli kullanılabilirlik benim uyarlamam (histerezis fikri MRHOF'ta ebeveyn seçiminde [64], Babel'de rota seçiminde [55])".

### K-2 · küçük — T-5'te Puñal 2014 yanlış aktarılmış

- **Yer:** `v2/17:94`.
- **Kanıt:** Puñal'de iki karıştırıcı türünü de güçlü gösteren ölçüler teslim oranı ve en uzun boşta kalma süresidir (Şekil 2'nin açıklaması); sinyal yardımcı ölçüdür ve karıştırmadan doğrudan etkilenmez (§II, sinyal ölçüleri); Xu'nun teslim–sinyal tutarlılık denetimi örneklerin örtüşmesi yüzünden elle eşikle ayrılamıyor (Şekil 3). "Tutarlılık işaretleri iki türü de görür" kaynağın dediği değil; (d)'de de tutarlılık zayıf çıktı.
- **Öneri:** "teslim oranı ve en uzun boşta kalma süresi iki türü de görür [23]".

### K-3 · küçük — Kaynakçada karşılığı olmayan ödünçler

- **Yer:** `v2/17:13` ve `:175` ("DSDV ailesi"); `:226` ("dolunca baştan düşürme bilinen bir kuyruk politikasıdır").
- **Kanıt:** `v2/16`da DSDV künyesi yok; `NOTLAR.md:134` DSDV'yi yalnız De Couto 2003 §4 üzerinden biliyor (↪). Baştan düşürme için kaynak gösterilmemiş.
- **Öneri:** DSDV ya kaynakçaya ↪ işaretiyle girer ("De Couto 2003'te aktarıldığı gibi") ya da cümleden çıkar; baştan düşürme için kaynak ya da "seçimim".

### K-4 · küçük — `v2/16`da [4]'ün durumu bayat; T-13'ün bölüm atfı eksik

- **Yer:** `v2/16-KAYNAKCA.md:29` "✓ (§1–2)"; `v2/02-DOGRULANMIS-KAYNAKLAR.md:93` "§1–§4 ve Ek A–B okundu"; `v2/17` §3.5, §3.7.2, §3.8.1.2, §4.2'ye atıf veriyor. `v2/16:3` "Güncel: 21 Ekim".
- **Öneri:** [4]'ün durumu `02` G3 ile hizalanır; T-13 atfı E-2'deki gibi.

### K-5 · küçük — T-12'nin gerekçesindeki ölçüm, kararın dayandığı özelliği göstermiyor

- **Yer:** `v2/17:174`.
- **Kanıt:** "döngü hiç oluşmaz; … Babel'in açık dönemdeki rota yokluğu kaybı 0,000" (`:174`). Babel'in R'sinin 0 olması rotayı bırakmamasından gelir; kaybı iletime gider (teşhis (c) `sonuc.md` §5: Babel ΔR 0 · Δİ +0,265). Aynı aileden v0.4.1'in R'si 0,237. Döngüsüzlüğün ölçülmüş göstergesi T (TTL) grubudur ve bütün kollarda ≈ 0'dır (en çok 0,013, `sonuc.md:69`). `v2/17:166` bunu doğru söylüyor ("fark açlığın çözülüşünde").
- **Öneri:** Gerekçe "T grubu bütün kollarda ≈ 0" ile değiştirilir; R'nin 0'ı T-13'ün gerekçesine taşınır.

### K-6 · küçük — "ED'de ortalama 1'den az, girişimde ~7 düğüm" yalnız birincil hücre için doğru

- **Yer:** `v2/17:110`; (d) `sonuc.md:11`, `:162`.
- **Kanıt:** Açık dilim sayısı birincilde 90, dayanıklılıkta 60 (kayıtlarda koşu başına 6 açık dönem; sınıf toplamları 28 800 ve 19 200 düğüm-saniye). Birincil: 624 / (8 × 90) = 0,87 · 4 929 / 720 = 6,8. Dayanıklılık: 529 / (8 × 60) = 1,10 · 4 948 / 480 = 10,3.
- **Öneri:** İki hücre ayrı yazılır.

### K-7 · küçük — T-10'daki tespit süreleri yalnız ulaşılan bağların ortancası

- **Yer:** `v2/17:150`; (d) `sonuc_hesap.py:312-319`.
- **Kanıt:** Ortanca `ulasan` (ulaşılan) üzerinden alınıyor; ulaşılan pay %18. Dayanıklılık hücresinde açık dönem 10 s olduğu için uzun süreler kesiliyor; 2,8 s ↔ 5,6 s farkının bir kısmı bu kesilmeden.
- **Öneri:** "ulaşılan %18'in ortancası" diye yazılır.

### K-8 · küçük — §3'teki evre farkları teşhis (c)'nin çekincesi olmadan veriliyor

- **Yer:** `v2/17:134`.
- **Kanıt:** "Kâhin bile açık dönemde 0,14 kaybediyor; Babel 0,27, v0.4.1 0,21". Karıştırmaya özgü kayıpta v0.4.1 ↔ Babel farkı ön-kayıtlı kuralla 8 tohumda ayırt edilemedi (+0,042, 5/8) ve "tasarımda dayanak yapılmaz" diye kayda geçti (teşhis (c) `sonuc.md:108`).
- **Öneri:** Satıra "(fark 8 tohumda ayırt edilemedi, teşhis (c) S3)".

### K-9 · küçük — Kaydedicinin "davranış aynı" kanıtının meşgul süre kısmı kendi kendini doğruluyor; testler yalnız saf yardımcıları kapsıyor

- **Yer:** `kalibrasyon/karistirma_isaretleri.py:42-51`, `:224-245`, `:321-325`; `tests2/test_karistirma_isaretleri.py`.
- **Kanıt:** İç eşitlik, dilimlere yazılan meşgul süreyi düğümün `_mesgul_toplam_s`'iyle karşılaştırıyor; ikisi de aynı sarmalayıcıda, aynı satırlarda artıyor (`:244-245`). Bu yalnız dilimlere bölmenin toplamı koruduğunu gösterir; sarmalayıcının `Dugum.mesgul_guncelle`'nin aynısı olduğunu göstermez. Teşhis (c)'deki Babel koşularında meşgul integrali hiç hesaplanmadığı için birebirlik de bunu sınamaz. Kod okumasıyla iki yöntem bugün aynı (`sim2/kosum/dugum.py:218-243` ↔ `:224-245`); simülatör değişirse kopya sessizce ayrışır. Testler `dagit`, `kutu`, `vazgecme_dizileri`, `nci_vazgecme`'yi kapsıyor; evre örneklemesi, ikiye bölme, selam kaybı ve bağ birimlerinin gruplanması sınanmıyor. `beklenti.md` §0 atfı kırık (E-1).
- **Öneri:** Sarmalayıcı aslını çağırıp farkı dilimlere yazacak biçimde ya da iki yöntemin aynı girdide aynı toplamı verdiğini gösteren bir testle; `evre`/`gecis_ani` ve `selam_kaybi` için küçük sentetik testler. 5-3'te kaydedici yeni sürümle yeniden kullanılacaksa önem kazanır.

### K-10 · küçük — Durum belgelerinde bayat satırlar

- **Yer:** `v2/12:3` "Güncel: 16 Kasım" (içerik 17 Kasım'ı anlatıyor) · `v2/12:13` "1095 passed (17 Ekim)" (5-2'de altı test eklendi; ana oturumun koşusundan sonra güncellenecek) · `v2/17:93` "teşhis (d)'de ölçülür" (gelecek zaman; sonuç aşağıda eklenmiş).
- **Öneri:** Kapanış güncellemesinde birlikte düzeltilir.

---

## 2 · Sorunlar (bulgu değil, bilinmesi gerekenler)

1. **`gecis_anlari` sürekli sınıfta boş.** Tanımlı üyenin açık/sessiz çizelgesi `gecis_anlari`'na yansımıyor (`sim2/kanal/karistirici.py:382-383`). Simülatörün meşgul integrali çizelge geçişinde bölünmüyor, parçanın durumu ortasında okunuyor (`sim2/kosum/dugum.py:233-243`). PHY tarafında açılma anı için beyan var (en çok bir parça, ~190 µs; `karistirici.py:200-203`); meşgul integrali için beyan yalnız (d)'nin beklentisindeki duman notunda (`beklenti.md:99`), etkisi ölçülmedi. Simülatör fiziği bu denetimin kapsamı dışında; ama `mesgul_sure_s` protokolün okuyacağı alan olduğu için beyanın `v2/05` ya da `v2/07`ye taşınması yararlı olur.
2. **Alanlar karıştırma öncesinde nötr değil.** Kayıtlardan aynı alanla denetim: ED ve girişim alanındaki düğümler karıştırıcı açılmadan önce de temizden ayrışıyor (AUC 0,57–0,69; ör. girişimde `mesgul` 0,669, `cozulen` 0,652). Karıştırılanı aynı alanın öncesiyle karşılaştırınca işaretlerin çoğu daha güçlü (girişimde `cozulen` G 0,917 · 0,925; ED'de `aciklanamayan` 0,996 · 0,994). (d)'nin hükümleri bu karışıklıkla zayıflamıyor; 5-3'teki "düşüş düğümün kendi yakın geçmişine göre okunsun mu" seçeneğini (`v2/17:125`) destekliyor.
3. **Çizelgeli karıştırmada tur istekleri dolaylı olarak düzenlileşebilir.** Yedeğe geçiş maliyeti yükseltir (T-14) → ara ilan (T-17) → aşağı akıştaki düğüm için uygulanamaz güncelleme → tur isteği (T-13). 15 s'lik çizelgede bu her dönemde yinelenebilir; T-13'ün "tur düzenli artırılmaz" gerekçesinin tersine işleyebilir. 5-3'te tur artışı sayacı izlenmeli.
4. **Puñal'in işbirliği bulgusu tek atlamalı ve iç mekân düzeneğinde, bütün komşuların aynı etkilendiği varsayımıyla naif ortalamadır;** kazanç hareketli ortalamayla birlikte %11'e kadar. T-6'nın aktarımı o düzenek için doğru; alanlı çok atlamalı dünyamıza taşınması ayrıca ölçülmeli.
5. **T-8 (kurala dayalı kanıt), Puñal'in vardığı sonuçla (802.11'de elle eşik zor) ters yönde bir seçim;** bedeli `v2/17:123`'te yazılı. Savunulabilir tasarım seçimi; bulgu değildir.
6. **`v2/06:46`** mekanizma kapısını eski adlarla anıyor. Ön-kayıt bu denetimin kapsamı dışında; mühürden önce `v2/17` ile hizalanmalı (Ö-10).
7. **T-5 bölümü ekleme biçiminde büyüdü:** ilk madde listesi (`v2/17:89-92`) (d)'den önceki hâl, sonuç altta. 5-3'ün kodlaması için tek bir "geçerli işaret listesi" yararlı olur.
8. **KR-2 açık** (`v2/04:157`): komutların birincil metrikteki yeri, T-18/T-20'nin etkisinin nasıl ölçüleceğini belirler.

---

## 3 · Temiz çıkanlar

- **Ölçüm disiplini (D-05):** dört teşhiste beklenti, karar kuralının hesabı ve koşu betiği aynı commit'te ve koşudan önce; sonradan hiçbirine dokunulmamış (`git log`: `6d6d67e` 14.11 16:31:10 → koşu 16:31:48; `3d4dc34` 15.11 01:03:41 → 01:04:53; `ef6d5cb` 15.11 12:52:44 → 12:53:43; `8750574` 16.11 19:24:20 → 19:25:07). Duman koşusundan sonraki değişiklikler (b'de ölçünün π'ye çevrilmesi, d'de evrenin örneklenmesi) ölçümden önce ve beklentinin içinde yazılmış.
- **Karar kuralının uygulanması:** (d)'nin `sonuc_hesap.py`'si beklentideki eşikleri birebir kullanıyor (G 0,80/0,70 · 6/8 · %80 yakalama · r_n ≤ 0,001 · 3 s · %50 · S3 %10). AUC'nin histogramdan hesabı doğru (P(X > Y) + ½P(=)); eşik ve yanlış alarm seçimi iki yönde de doğru. Kayıtlardan bağımsız yeniden hesapta 12 ayırma gücünün hepsi üç basamakta tuttu.
- **Birebirlik:** (d)'nin 24 koşusu teşhis (c)'nin Babel satırıyla `gecerli`, `pdr`, `pdr_pencere`, `uretilen`, `teslim` ve 131 sayacın hepsinde aynı (24/24, betikle doğrulandı).
- **Sayılar:** `v2/17`deki teşhis sayıları ilgili `sonuc.md` ve `sonuc_hesap.txt` ile tutuyor (örnekler: G +0,1518, İ %65 · R %35; π 0,44; kontrol kanal süresi oranı 185,0 / 68,7 = 2,69; Babel − OLSRv2 +0,122 · +0,168 · +0,141; S3 +0,042, 5/8; komşu silinmesi 15 171 ↔ 315; işlenmeyen duyuru 138 239 / 217 371 = %64; ardıl değişimi 10 804 / 40 / 350 s → 1,3 s). T-20'nin oranları kayıtlardan yeniden hesaplandı: 6 096 / 6 368 = %95,7 · 5 804 / 6 245 = %92,9 · 5 837 / 6 264 = %93,2.
- **Öngörü işaretlemeleri dürüst:** (a) 1 tutmadı, 1 sınanamadı; (b) 9 tutmadı; (c) 46'nın 8'i; (d) 24'ün 10'u. Tutmayanların gerekçeleri yazılı.
- **Etiketleme:** evre, dilimin başı, ortası ve sonu örneklenerek bulunuyor; açık dönemin uçları ikiye bölmeyle açılma ve kapanma yönünde doğru bulunuyor; kayıtlarda her koşuda 6 açık dönem ve sınıf toplamları açık süreyle tutarlı. Selam kaybında sıra numarası doğru eşleniyor (`_hello_kur` önce artırıyor, `protokoller/babel.py:753`); "tanımsız" payı bütün sınıflarda 0. RSSI formülü `cerceve_duyuldu`nunkiyle aynı (`kontrol.py:232-235` ↔ `karistirma_isaretleri.py:267-271`).
- **`kayip_anatomisi` ekleri:** ikincil sayım, çizelgeli kolda aletin evre sayımıyla eşitlik denetiminden geçiyor ve testli; veri denemesi sayısı `mac_deneme`ye, hedefte başarılı alım `veri_alim_hedefte`ye eşitleniyor; önceki kayıtlarla birebirlikler (12/12, 24/24, 10/10) davranışın değişmediğini gösteriyor.
- **Kaynaklar:** RFC 8966 §3.5.1, §3.7.2, §3.8.1.2, §4.2; RFC 6719'un 512 = 4 ETX ve 192 = 1,5 ETX değerleri; RFC 6206'nın bastırması; De Couto'nun küçük yoklama ve doğruluk–tepki değiş tokuşu; Ramachandran'ın %10 eşiği ve 4–4,5 katlık kalıcılık artışı; Jonglez'in gecikme ölçüsündeki geri besleme ve histerezis; Tague'nin ortalama ve varyans izlemesi ile ortak bağların kovaryansı; Yang'ın "bypass" stratejisi doğru aktarılmış (istisnalar K-1, K-2). α = 2 (`sim2/yapilandirma/konfig.py:169`), Babel zamanlayıcıları (`protokoller/babel_bicim.py:105-107`) ve `13` §02.1 · §02.5 · §03.1 atıfları tutuyor.

## 4 · Doğrulanamayanlar

- S3'ün tek deneme başarısıyla sonucu, komşu başına sessizlik işaretinin ayırma gücü ve birleşik kuralın başarısı: yeni koşu gerektirir.
- Sürekli sınıfta `gecis_anlari` boşluğunun meşgul integraline etkisinin büyüklüğü: ölçülmedi.
- Cerar 2021 [57]'nin "RSSI tek başına kaliteyi vermez" yargısı: ilgili bölümde donanım ve yazılım ölçüleri ayrımı ve tek ölçünün bilgi kaybettirebileceği ifadesi bulundu, yargıyı açıkça kuran cümle bulunamadı. Aynı yargıyı Puñal [23] açıkça veriyor; T-2'nin atfına [23] eklenebilir.
- Xu vd. 2005: açılmadı; `v2/17`deki "Puñal 2014'te aktarıldığı gibi" dili `v2/16` kuralıyla tutarlı.
- `kopya/` klasörlerinin dosya özetleri yeniden hesaplanmadı; `kopya_ozet.txt`'lere dayanıldı.
- Tam test takımı koşulmadı (ana oturumda koşuluyor).

## 5 · Hüküm

**5-2 bu hâliyle kapatılmamalı; aşağıdaki işler yapılınca kapatılabilir.** İşlerin hepsi belge ve karar düzeyindedir; simülasyon gerektirmez. Ölçüm gerektiren maddeler (Ö-2, Ö-3, Ö-4) 5-3'ün açık listesine yazılarak kapanır.

1. **E-1:** açıklanamayan kanal meşguliyetinin kaynağına karar (`v2/05` §7 yolu, sözleşme içinde tahmin ya da `mesgul`); `v2/17` kimlik ve T-5'e yazılması; kaydedicinin kırık atfı.
2. **E-2:** T-13'e uygulanamaz güncellemenin yok sayılması ya da rotanın bırakılması kuralı; T-12'de FD'nin ilan edilen değerle tanımı; RFC 8966 bölüm atıfları.
3. **Ö-1:** kimlik paragrafının (d)'nin gösterdiğiyle hizalanması.
4. **Ö-5, Ö-6, Ö-7:** selamın aralığını taşıması; bağın durum makinesi; tamponun sınırının türü, gecikme tavanlı `PDR_açık`ın her A/B'de raporlanması, komut–telemetri paylaşımı. Kararla ya da 5-3'ün ilk kural kâğıdına açık madde olarak.
5. **Ö-2, Ö-3, Ö-4:** (d)'nin koşulluluğu (tek protokol, tek sınıf, düğüm düzeyi ölçüler, doymuş S3) `v2/17` ve `v2/12:57`de; ilgili ölçümler 5-3 listesine.
6. **Ö-8, Ö-9:** `v2/12` §2 tablosu ve §3 kaba planı, `v2/04:110`; takvimin yeniden yazılması.
7. **Ö-10:** 5-3'ün açılış listesinin tamamlanması (ara ilan, iz ↔ T-7, RSSI ve konum kayıtları, ablasyon bayrakları ve mekanizma kapısı).
8. **K-1…K-10:** toplu düzeltme.

Kararların kendisi (ETX, FD + tur, hazır yedek, kurala dayalı kanıt, ayrı "karıştırılıyor" durumu, seyrek selam, kısa tampon, geri iz) kaynakla ve ölçümle savunulabilir durumda; bulgular kararların doğruluğunu değil, metnin kanıtla ve kendi içinde tutarlılığını ilgilendiriyor.
