# TAM BAĞIMSIZ DENETİM — sıfır bağlamlı ajana ilk mesaj

> Yürütücü için: `---` çizgisinden sonraki metnin TAMAMINI bu depo klasöründe açılan yeni bir ajan oturumuna ilk mesaj olarak yapıştır. O oturumda `termo-nuclear-code-quality-review` skill'i yüklü olmalı; bu makinede (`~/.claude/skills`, kurulu eklentiler) ve eklenti kataloğunda bu adla bir skill bulunamadı. Denetçi skill'i bulamazsa başlamadan durup sorar. Denetlenen hâl: `main` @ `ab2ca90` (çalışma ağacı temiz); denetimden önce yeni bir değişiklik varsa commit et. Hazırlayan: 13 Ekim 2026'da projeyi devralan ajan.

---

Sen bu projenin **bağımsız denetçisisin**. Depoyu sen yazmadın. Görevin bir şeyin doğru olduğunu onaylamak değil; yanlış, eksik, bayat, güvenilmez ya da gereksiz olanı bulmak ve sonunda üç soruya gerekçeli, net bir hüküm vermek:

1. Simülatör ve ölçüm aletleri, sonuçların üstüne kurulabileceği kadar güvenilir mi?
2. DESPARETE ile rakipler arasındaki karşılaştırma adil ve bilimsel olarak savunulabilir mi?
3. Proje bugünkü hâliyle TÜBİTAK 2204-A için yeterli ve güvenilir mi; değilse 19 Aralık 2026'ya kadar neyin yapılması gerekir?

Denetim yüzeysel olmayacak ve yalnız yazılım yönünden yapılmayacak: fizik, ölçüm, istatistik, ön-kayıt, rakiplerin sadakati, belgeler ve proje düzeyi de kapsamda. **Hiçbir şeyi düzeltmeyeceksin;** raporundaki bulguları başka bir ajan yürütücüyle birlikte ele alacak. Rapor, sıfır bağlamla gelen birinin tek tek uygulayabileceği kadar somut olmalı.

## 0 · Proje

- **Ne:** bir lise öğrencisinin TÜBİTAK 2204-A projesi (Yazılım / Havacılık ve Uzay). Son teslim **19 Aralık 2026**, ön-kayıt mührü ~20 Kasım.
- **Amaç:** projenin ürünü bu çalışmada önerilen yönlendirme protokolü **DESPARETE**'dir. Konu: karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme; telemetri İHA'lardan yer istasyonuna (geçit), komutlar ters yönde.
- **Simülatörün gerekçesi:** proje kendi kesikli olay simülatörünü (`sim2/`, Python, 802.11b, 1:1 "referans dünya" `referans_2026`) yazdı. Amaç, DESPARETE'yi gerçek fiziğe ve saha koşullarına yakın bir ortamda ölçüp taktik İHA senaryolarında rakiplere göre nasıl davrandığını göstermek. ns-3 ve OMNeT++ genel amaçlı olduğu, bu alan için yeterli ayrıntıyı vermediği gerekçesiyle kullanılmadı. Bu gerekçeyi de denetle (Alan B).
- **Senaryo sabitleri kesin kısıt değildir:** 40 İHA, 33 km alan, 20 dBm EIRP gibi değerler bugünkü çalışma noktasıdır. Daha gerçekçi ya da hesapça uygulanabilir bir seçim görürsen gerekçe ve bedeliyle öner.
- **Rakipler:**
  - `AODV-j` (RFC 3561) ve `OLSRv2-b` (RFC 7181 + 6130 + 5444 + 7779) donmuş taban protokollerdir.
  - JarmRout (Pu 2018) kodlandı ve dondu, ama yürütücünün 13 Ekim kararıyla rakiplikten çıktı; bu karar henüz karar günlüğüne yazılmadı. Üçüncü rakip aranıyor: en iyisi olmak zorunda değil, ama tanımı tam, bilimsel olarak güvenilir ve straw-man eleştirisine açık olmamalı.
- **DESPARETE v0.4.1** bir taslaktır. Faz 5'te geliştirilecek, gerekirse baştan yazılacak. Onu "zayıf" diye değil, Faz 5'te adil biçimde geliştirilip ölçülebilir mi, bugünkü kodu yanıltıcı teşhise yol açıyor mu diye denetle.
- **Durum:** Faz 0–4 ve Faz 4b'nin 1–4. adımları kapandı (yeni rakipler, U1, evre kapıları, belge ve kod temizliği). Sırada bu denetim, üçüncü rakip kararı, ardından Faz 5 (DESPARETE'nin karıştırma mekanizmaları), Faz 6 (ön-kayıt ve mühür), Faz 7 (ana deney ve yazım).
- **Ölçek** (git'teki `.py`): `sim2/` 63 dosya · 14,2 bin satır · `protokoller/` 21 · 7,4 bin · `kalibrasyon/` 28 · 13,2 bin · `analiz/` 4 · 0,6 bin · `tests2/` 31 · 16 bin (1059 test). `v2/` 14 belge, karar günlüğü K-001…K-241, `arsiv/` geçmiş.

## 1 · Kurallar

1. **Depoya dokunma.** Tek istisna raporun: `arsiv/denetim/DENETIM-RAPORU-2026-10-<gün>.md`. Kod, belge, test, köken defteri, karar günlüğü, bellek dosyaları — hiçbirini değiştirme. Başlangıçta ve sonda `git rev-parse HEAD`, `git status --short` ve depo dosyalarının SHA-256 manifestini al (`.git` hariç); ikisinin farkını rapora koy.
2. **Git** yalnız okuma: `log`, `show`, `diff`, `blame`. Commit, dal ve push yok.
3. **Dil:** yürütücüyle Türkçe; rapor da Türkçe. Belgelerin üslubuyla yaz: bilgi düzeyinde, nesnel, emoji ve süs yok; "öğrenci" yerine "yürütücü".
4. **Ortam (Windows):**
   - Python'u `py -3.11` ile çağır; `python` başka bir 3.12'yi açar, onda numpy/scipy/pytest yok.
   - Her çağrıda `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`.
   - Paket kurma. Kaynak doğrulamak için web sayfası okuyabilirsin; dosya indirmeden önce yürütücüden izin al (dosya adı, kaynak, boyut).
   - Satır sonları karışıktır (CRLF/LF).
5. **Ana deney tohumları 2000–2039 hiçbir koşuda kullanılmaz.** Geliştirme tohumları 1000–1039 ve 1100–1119.
6. **Hesap:**
   - Makine 12 mantıksal çekirdek, havuz 8 işçi; iki ağır işi aynı anda koşma.
   - İzinsiz koşabileceklerin:
     - tam test takımı (`py -3.11 -m pytest tests2 -q`, ~15 dk);
     - `kalibrasyon/mimari_denetimi.py`;
     - `arsiv/dogrulama/kayit_indeksi.py --kontrol`;
     - `kalibrasyon/uretici_duman.py --kapi`;
     - `kalibrasyon/regresyon_satirlari.py karsilastir k236 k236`;
     - kendi kısa deneylerin (her biri ≤ 30 dk, toplam ≤ ~4 sa).
   - 30 dakikayı aşan bir koşudan önce (ör. `regresyon_satirlari.py uret` ~70 dk; U1 ve kayıp anatomisi saatler) yürütücüye süresini söyleyip izin al.
   - Her koşuyu dondurulmuş kopyadan yap ve kopyayı depo dışına koy: `py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py <geçici_dizin>`. Kopyanın commit'le birebir olduğunu dosya özetleriyle göster.
7. **Kendi betiklerin** depo dışında dursun. Rapora komutunu ve çıktısını yaz ki yeniden üretilebilsin. Bir şüpheyi ölçerek sınayacaksan ölçütünü koşudan önce raporuna yaz.
8. **Alt ajan:** okuma ve inceleme için paralel alt ajan kullanabilirsin (skill gerektiriyorsa da). Ama bir alt ajanın her bulgusunu rapora koymadan önce kendin doğrula. Hesap koşuları sırayla yapılır.
9. **Skill — zorunlu:**
   - Denetimin başında `termo-nuclear-code-quality-review` skill'ini Skill aracıyla çağır. Kod incelemesini onun yöntemiyle, bütün kod tabanında yürüt: `sim2/` · `protokoller/` · `kalibrasyon/` · `analiz/` · `tests2/` · `arsiv/dogrulama/` ve canlı belgelerin atıf verdiği `arsiv/teshis/` betikleri.
   - Skill'in kendi önem ölçeği ve bulgu biçimi varsa koru, ama her bulguyu bu raporun tablosuna da `DD-xx` numarasıyla geçir.
   - Skill bu oturumda yoksa **denetime başlamadan dur**, yürütücüye söyle ve nasıl devam edileceğini sor. Skill kullanılmış gibi yazma.
   - Skill yalnız yazılım yönünü kapsar; Alan B–I'yı ayrıca bu istemle denetle.
10. **`DEVIR-PROMPT.md`** (kökte, git dışı) çalışan ajana yazılmış bir devir belgesidir. Kurallarını ve tuzaklarını bağlam olarak oku, ama §0'daki "ilk oturumun görevi" senin görevin değil.

## 2 · Okuma sırası

Önce oku, sonra sına:
1. `DEVIR-PROMPT.md` — kurallar, tuzaklar, doğrulama komutları (§5–§6).
2. `v2/01` (problem, kapsam, başarı ölçütü) · `v2/04-KARARLAR.md` (bugün geçerli kararlar, açık kararlar §10) · `v2/12` (durum, plan, hesap bütçesi, riskler).
3. **Simülatör:** `v2/07` · `v2/14` (referans dünyanın sayıları ve kaynakları) · `v2/05` (gözlem sözleşmesi) · `v2/13` (kontrol düzlemi).
4. **Yöntem:** `v2/06` (ön-kayıt taslağı) · `v2/08` (evre metrikleri) · `v2/03` · `v2/02` (doğrulanmış kaynaklar) · `v2/09` (Li replikasyonu).
5. **Kod:** `sim2/` · `protokoller/` · `kalibrasyon/` · `analiz/` · `tests2/`. Kaynak metinler: `protokol_kaynaklari/` (RFC'ler, makaleler, veri sayfaları).
6. **Önceki denetimler:** `arsiv/denetim/DENETIM-RAPORU-2026-09-25.md` ve `DENETIM-RAPORU-2026-10-08.md`. Bulgularının (D-01…D-24 ve öncekiler) bugünkü durumunu sen belirleyeceksin.
7. **Tarihçe yalnız gerektiğinde:** `v2/kayit/KARAR-GUNLUGU.md` (başında indeks) · `arsiv/teshis/<tarih_konu>/` (her ölçümün `beklenti.md`si ölçmeden önce yazılmış ölçüttür, `sonuc.md`si sonuç).

Yerel çıktılar `ciktilar2/`de (git dışı): regresyon tabanı `ciktilar2/regresyon/k236.jsonl` (85 vaka).

## 3 · Bilinen bağlam — yeniden "keşif" diye yazma, ama doğru olup olmadığını sorgula

- **İki dünya:** `Konfig()` varsayılanı eski 1:50 dünyadır, eski regresyon vakaları için korunur. Deneyler `referans_2026`da koşar. 25 Eylül öncesi sayılar eski dünyanındır.
- **Birincil hücre:** `formasyon · yere_toplama · derin_sizma · sürekli`, 10 W ortalama. Karıştırıcı 15 s açık · 15 s sessiz, açıkken 20 W. Birincil metrik `PDR_açık`: karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı. Karıştırmaya özgü kazanç fark-içinde-fark ve mekanizma kapısıyla kurulur (`v2/06` §0.4.5).
- **Kâhinler** (`kalibrasyon/kahin.py`) protokol değil ölçüm aletidir: ETX kâhini U1'in paydası, çözünürlük R'nin ve evre kapılarının aleti.
- **Köken defteri** (`sim2/yapilandirma/kokenler.py`): her parametre sekiz kovadan birinde; bugün SINANMAMIŞ 5 (pencere üçlüsü, `rssi_olcum_sigma_db`, `gps_dikey_sigma_m`).
- **Faz 6'ya bilerek bırakılanlar:** pencere üçlüsü · δ ve güç referans dünyada · R'nin ana deney penceresinde yeniden ölçümü · U2–U4 yeni rakiplerle · KR-2 (birincil metrikte komutlar).
- **Derin denetime bırakılan iki not:** G1-P yeni rakip kümesiyle koşulmadı · bütün kontrol mesajları UDP/IP ile faturalanıyor (gerçek DSR UDP kullanmaz).
- **Önceki ajanların sicili:** bu projede ajanlar tekrar tekrar fazla iddia etti, bayat bilgiyle devam etti, kendi kapattığı işi kendi doğruladı. Belgedeki ya da karar günlüğündeki bir "doğrulandı"ya, üretici komutunu ve sonucunu görmeden güvenme.

## 4 · Denetim alanları

Her alanda iki soru: **(i) doğru mu** (kod, ölçüm ve kaynakla sına), **(ii) gerekli, güncel ve savunulabilir mi.** Belgeye değil koda, ölçüme ve birincil kaynağa inan.

**A · Yazılım (skill'le).**
- Doğruluk kusurları ve sessiz hatalar: yanlış birim, kayan nokta eşitliği, sınır durumları, olay sırası.
- Belirlenimcilik; rastgele akışların bağımsızlığı ve protokolden bağımsızlığı (eşleştirmenin yapısal olması).
- Korunum ve kapalı düşme sebepleri; gizli küresel durum; hata yutma.
- Kopya mantık (aynı kuralın iki yerde yazılması); ölü kod ve eski dünyaya ait ölü alet.
- Mimari sınırlar: `protokoller/` yalnız `sim2/gozlem/`i görebilir — kaçamak yollar dâhil.
- Testlerin kalitesi: hiçbir şey sınamayan, totolojik ya da koşulu hiç tetiklenmeyen test; kritik değişmezlerin testleri.
- Performans: koşu başına 1–9 sa. Davranışı birebir koruyarak hızlandırılabilecek sıcak noktalar varsa raporla, değiştirme.

**B · Fizik, kanal ve "gerçek saha koşullarına yakınlık" iddiası.** Formülleri kaynaklardan bağımsız olarak yeniden türet. 8 Ekim denetimi kanal fiziğini yeniden türetmediğini kendisi yazıyor (§2.3).
- **PHY:**
  - gürültü tabanı (kTB + NF);
  - DBPSK/DQPSK'nin işlem kazançlı PER'i ve CCK (Pursley–Royster);
  - `v2/14`teki duyarlılık ve menzil tabloları;
  - EIRP ve anten kazancının hesaba girişi;
  - ED-CCA eşiklerinin verici gücüne bağlanışı.
- **Kanal:**
  - serbest uzay;
  - log-normal gölgelemenin korelasyonu (2,5 km hücre);
  - Rician K ve Doppler, blok üretecinin momentleri;
  - Al-Hourani yer–hava modeli: parametreleri ve 33 km'lik alanda, 3 m'lik yer karıştırıcısıyla küçük yükselme açılarında davranışı;
  - yayılım gecikmesi.
- **MAC:**
  - slot, SIFS, DIFS, CW, en çok 7 iletim denemesi;
  - ~9 km'lik bağlarda yayılım gecikmesiyle ACK zaman aşımı ve slot;
  - ARF'nin ns-3'le uyumu;
  - yakalama;
  - karıştırıcının ED-CCA ile vericiyi susturması.
- **Karıştırıcılar:** beş sınıf, beş aile, ailelerde ortalama gücün eşitlenmesi, çizelge ve hareket.
- **Mobilite ve trafik:** dört hareket kolu; MAVLink ölçeğinde telemetri hızı.
- **Simülatörün varlık gerekçesi:** bu soru için `sim2` hangi noktalarda ns-3/OMNeT++'tan daha ayrıntılı ya da gerçekçi, hangilerinde daha zayıf? Zayıf olduğu yerler rakipler arasındaki karşılaştırmayı bir yöne çekebilir mi?
- Bir sadeleştirme savunulabilir bir modelleme seçimiyse onu "bulgu" değil "savunulabilir seçim — jüri sorusu" olarak yaz (§5).

**C · Senaryo ve çalışma noktası.**
- N 40, 33 km, EIRP 20 dBm: K-230'un "serbest uzayda güç yalnız mesafeyi ölçekler" gerekçesi yer–hava kaybının açıya, yayılım gecikmesinin ve topoloji değişim hızının mutlak mesafeye bağlı olduğu düşünülünce tutuyor mu?
- Birincil hücrenin tehdidi (derin sızma, 15/15 s, 10 W) ve kısmi karıştırma rejimi gerçekçi mi? Formasyonda bağ hareketle kopmuyor; bu hücre yönlendirmeye anlamlı bir iş bırakıyor mu?
- Herhangi bir seçim DESPARETE'yi ya da bir rakibi kayırıyor mu?
- Senaryo sabitleri kesin kısıt değil (§0). Daha gerçekçi ya da hesapça uygulanabilir bir çalışma noktası görürsen gerekçe ve bedeliyle öner.

**D · Ölçüm, istatistik ve ön-kayıt.**
- **Metrik:** `PDR_açık`ın iki gerçeklemesi (`sim2/olcum/evre.py` · `analiz/satir.py`) tutarlı mı?
  - Doğum kohortu; pencere (50 / 320 / 350 s; trafik 320 s'de durur — son doğumlar boşalan ağda teslim edilir).
  - Kopya defteri altında paket düzeyi PDR.
- **Evre metrikleri ve kapıları:** kayıtlı muafiyet mekanizması bir kusuru örtebilir mi?
- **Kâhinler ve çözünürlük:** kâhinin yakınsaması; R = 0,0126'nın 50 s'lik kesitte ölçülmüş olması.
- **İstatistik planı:** δ formülü, güç planı (ön tahmin eski dünyanın), Wilcoxon, Holm, NaN tuzağı, fark-içinde-fark (`analiz/hucre.py`, `analiz/istatistik.py`).
- **Mekanizma kapısı:** kapıya girecek mekanizmaların adları Faz 5'te kesinleşiyor — sonucu görerek seçme riski var mı?
- **Ön-kaydın kanıtı:**
  - Son ölçümlerde (K-228…K-239) `beklenti.md` sonuçtan önce ayrı commit'le mi girdi? `git log`la göster.
  - Sonuçtan sonra değişen ölçütlerin hepsi `v2/06` §10'da mı?
  - 2000–2039 tohumlarının hiçbir çıktıda kullanılmadığını tara.
  - KR-3 kararı (`v2/04` §10) "DESPARETE yeni rakiplere karşı koşulmadan önce" verilecekti. Bu şart hâlâ geçerli mi?
- **U1 kabul kapısı:** eşik ölçüm görüldükten sonra seçildi (beyanlı). "Açıklanmış düşük hücre" kuralları bir yazılım kusurunu örtebilir mi?

**E · Karşılaştırmanın adaleti ve rakipler.**
- **Gözlem sözleşmesinin sızdırmazlığı:** test ve elle, protokolün kâhin, topoloji ya da karıştırıcı bilgisine ulaşabileceği bir yol var mı?
- **Gizli asimetriler:** HELLO aralıkları, kapsülleme (kontrol mesajı + 64 B), veri başlığı faturası, ortak bekleme tamponu (64 paket · 30 s), koşum beacon'ının kapatılması, kopya ve kaynak rotası faturası.
- **AODV-j ve OLSRv2-b'nin sadakati:** RFC metinleriyle kural kural örnek denetim; karıştırma altında en çok önemli olan kurallara öncelik ver (bağ kopması tespiti, RERR, yerel onarım, HELLO kaybı, bağ tutma süreleri, DAT metriği, MPR).
  - OLSRv2'nin sadakat denetimini onu yazan oturum yaptı; bağımsız gözle bak.
  - Rakipler gereğinden zayıf (straw-man) ya da senaryoya göre ayarlanmış olabilir mi?
- **JarmRout:** rakiplikten çıktı. Derinlemesine denetleme; yalnız çıkışının arkada sarkan bağımlılık bırakıp bırakmadığına bak (testler, regresyon matrisi, evre kapısındaki kayıtlı muafiyet, belgeler, `v2/06`'nın H2.c'si ve δ formülü).
- **Üçüncü rakip için:** kısa bir değerlendirme yapabilirsin. Hangi ölçütler, hangi aday sınıfları (literatürde karıştırmaya dayanıklı, tanımı tam bir protokol; yoksa DESPARETE'ye yakın, tanımı tam bir protokol — örneğin Babel, RFC 8966; kaynağı `protokol_kaynaklari/`de). Aday araştırması bu denetimin ana işi değil.

**F · DESPARETE ve Faz 5'e hazırlık.**
- `protokoller/desparete*.py`: kâhin erişimi yok mu; döngüsüzlük değişmezleri (FD, DFSN) her olayda korunuyor mu; sayaçlar doğru şeyi mi sayıyor?
- Faz 5.0'ın teşhisi (`arsiv/teshis/faz5_0_2026-10-10/sonuc.md`) bu sayaçlara ve `kalibrasyon/kayip_anatomisi.py`ye dayanıyor. Alet ya da sayaçta bir kusur bu teşhisi yanıltmış olabilir mi? 4 tohumla verilen sonuç ne kadar sağlam?
- Ablasyon bayrakları ve seçenekler (`desparete_bayrak.py`) Faz 5'in A/B ölçümlerini adil biçimde taşır mı?
- Tasarımı nihai sayıp eleştirme; taslak olduğu biliniyor.

**G · Doğrulama altyapısı ve yeniden üretilebilirlik.**
- Tam test takımını koş ve sonucunu yaz.
- **Regresyon** (`regresyon_satirlari.py`, taban k236): neyi bağlıyor, neyi bağlamıyor (referans dünyada tam pencere, evre metrikleri)?
- Mimari denetimi; donma testi (`tests2/test_donma.py`); kimlik özetleri (`arac_hash`, `protokol_hash`, `kurulum_hash`); dondurulmuş kopya akışı.
- **Temiz klondan yeniden üretim:** `ciktilar2/` git dışında. Bir jüri üyesi ya da hakem depodan bir sonucu yeniden üretebilir mi?

**H · Belgeler.**
- `v2/*.md`, `README.md`, `DEVIR-PROMPT.md`, kod yorumları: kod ve ölçümle çelişen sayı, sürüm, sayım; aynı bilginin iki yerde tutulması; bayat anlatı.
- Belgeler bir TÜBİTAK raporuna kaynak olabilecek düzende mi? `README`'deki yapay zekâ kullanımı beyanı yeterli ve dürüst mü?
- Hangi belge ya da bölüm sadeleşmeli, birleşmeli, arşive gitmeli — somut liste.

**I · Proje düzeyi: TÜBİTAK 2204-A uygunluğu ve güvenilirlik.**
- **Değerlendirme ölçütleri:** TÜBİTAK 2204-A'nın resmî çağrı ya da değerlendirme belgesine erişebilirsen ölçütlerini kaynak göstererek kullan; erişemezsen bunu açıkça yaz.
- **Kapsam ve anlaşılırlık:** proje bir lise projesi için uygun mu? Yöntemin karmaşıklığı jüri önünde anlatılabilir ve savunulabilir mi (`v2/01` §6: "jüri önünde savunulamayacak hiçbir yöntem kullanılmaz")?
- **Özgünlük ve emek beyanı:** özgünlük iddiası ve yapay zekâ ile yazılmış büyük bir kod tabanının yürütücünün emeği olarak sunulması — risk ve öneri.
- **Takvim ve hesap bütçesi:** `v2/12` §3–§4; tek makine, mühür ~20 Kasım, teslim 19 Aralık. Gerçekçi mi? Düşme sırası yeterli mi?
- **En kısa güvenilir yol:** bugünkü hâlden güvenilir bir teslime giden en kısa yol ne? Hangi iş vazgeçilmez, hangisi bırakılabilir?

## 5 · Nasıl denetle

- **Her bulguyu kanıtla:** dosya:satır, komut ve çıktısı, ya da belge veya kaynak alıntısı. Kanıtı olmayan sezgiyi "olası" diye işaretle.
- **Önem:**
  - KRİTİK — bir sonucu, kabul kapısını ya da ön-kaydı geçersiz kılar;
  - ÖNEMLİ — yanlış ama sonucu değiştirmeyebilir; Faz 5'ten önce düzelmeli;
  - KÜÇÜK — bayatlık, tutarsızlık, temizlik;
  - ÖNERİ.
- **Bulgu ile savunulabilir seçimi ayır.** Bilimsel güvenilirliği bozan kusur bulgudur ve düzeltilmelidir. Gerekçesi yazılı, savunulabilir bir modelleme seçimi bulgu değildir; onu ayrı bölümde, jürinin sorabileceği soru ve kısa cevabıyla yaz. Kalibre edilmiş dünyayı yeniden açmayı ancak sonuçları geçersiz kılan bir kusur varsa öner.
- **Kendi yanlışını ara:** tuhaf bir sayı ya da kalan bir kapı gördüğünde önce aleti ve kendi okumanı sına.
- **Ölçülebilir olanı ölç;** önce ölçütü yaz, kısa pencereli ve az tohumlu tut. Tek tohumlu 30 s'lik bir koşunun PDR'si ±0,15 oynar; tek koşu karar vermez.
- **Sağlam bulduklarını da yaz:** neye bakıp neyi doğru bulduğunu. Bakamadıklarını ve nedenini ayrıca yaz.

## 6 · Rapor biçimi — `arsiv/denetim/DENETIM-RAPORU-2026-10-<gün>.md`

1. **Özet hüküm** (bir sayfa):
   - Baştaki üç soruya ayrı ayrı net cevap ve güven derecesi.
   - Faz 5'e geçmeden önce mutlaka ele alınması gereken en önemli 5–10 şey.
2. **Yöntem:**
   - Skill'in nasıl kullanıldığı (adı, çağrılışı, kapsadığı dosyalar).
   - Okunanlar · koşulanlar (komut, süre, sonuç) · bakılamayanlar ve nedeni.
   - Başlangıç ve bitiş `git rev-parse HEAD`, `git status --short`, manifest farkı.
3. **Bulgu tablosu:** `| no | alan (A–I) | önem | tek cümle | kanıt türü |`. Numaralar `DD-01, DD-02…`; önceki denetimin `D-xx`leri ve karar günlüğünün `K-xxx`leriyle karışmasın.
4. **Bulgular ayrıntılı** — her biri için:
   - ne;
   - kanıt;
   - başarısızlık senaryosu (hangi girdi ya da durum → hangi yanlış sonuç);
   - sonuca etkisi (hangi sayı ya da hüküm değişebilir);
   - önerilen düzeltme (hangi dosya, ne değişmeli, sonrasında hangi doğrulama);
   - tahmini emek;
   - güven (doğrulandı / olası).
5. **Savunulabilir seçimler ve jüri soruları** (bulgu değil).
6. **Önceki denetimlerin bulguları:** her biri kapandı mı, kanıtıyla.
7. **Belge temizlik listesi:** belge ya da bölüm başına güncelle · sadeleştir · birleştir · arşive taşı, gerekçesiyle.
8. **Sağlam bulunanlar.**
9. **Önerilen sıra:**
   - Faz 5'ten önce yapılması gerekenler;
   - Faz 6'ya kalabilecekler;
   - yürütücü kararı isteyenler (kapsam, iddia, ön-kayıt metriği, büyük tasarım değişikliği).

## 7 · Önceki ajanın notları — bağımsız doğrula ya da çürüt

Projeyi 13 Ekim'de devralan ajanın okumada gördükleri. Doğru varsayma; rapora yalnız kendi kanıtınla gir.
- **G1ç ve G2ç kapı koşuları:** `arsiv/teshis/faz4b_kapanis2_2026-10-12/G1c.txt` · `G2c.txt` (K-239, tohum 1003 · 1004) DESPARETE'yi OLSRv2 ve JarmRout'la aynı hücrelerde koşturmuş. Bu, `v2/06` §10'daki "DESPARETE yeni rakiplere karşı hiç koşulmadı" ve `v2/04` §10'daki KR-3 şartıyla çelişiyor olabilir.
- **Aynı çıktılarda:** DESPARETE v0.4.1'in `PDR_açık`ı OLSRv2'ninkiyle başa baş, karıştırıcısız ikizde ise OLSRv2 daha yüksek görünüyor. İki tohum; karar için yetersiz.
- **`hedefli_canlilik` (V2+):** `desparete_bayrak.py`'de var ve kapalı. Kapatılma kararı (K-165) eski dünyada, 3 tohum × 40 s'lik, kaydın kendi deyişiyle ±0,03 gürültülü ölçüme dayanıyor.
- **Bayat docstring'ler:**
  - `sim2/kanal/tehdit.py` başlığı karıştırıcı hızlarını "SINANMAMIŞ" diyor; köken defterinde araç hızı DÜNYA TANIMI, hava hızı KOL TANIMI.
  - `sim2/kanal/dunya.py` başlığındaki "GEÇİCİ DEĞERLER (Faz 4'te kalibre edilir)" bayat görünüyor.

Bitirince yürütücüye sohbette kısa bir Türkçe özet ver: üç sorunun cevabı, en önemli bulgular ve raporun yolu. Rapor dışında hiçbir dosyayı değiştirmediğini başlangıç ve bitiş `git status` çıktılarıyla göster.
