# DESPARETE — Kavramsal Model

**Sürüm:** 0.1 (onaylı kavramsal temel; normatif ayrıntı kaynağı değildir)  
**Durum:** Q/H/U/R kavramsal ayrımı DL-004/DL-006 ile onaylandı; M0.1 sayısal kuralları `35`, normatif davranış ilgili v0.1 belgelerindedir.  
**Tarih:** 2026-09-20

## 1. Amaç

Bu belge, DESPARETE'nin yerel bağ bilgilerini hangi anlam ayrımlarıyla işleyeceğini tanımlar. Sayısal formül, ağırlık, eşik, durum geçişi veya mesaj alanı seçmez. Amaç, aynı kelimenin hem ölçüm, hem tahmin, hem maliyet ve hem de politika anlamında kullanılmasını önlemektir.

Önerilen zincir şudur:

```text
Yerel gözlemler
      ↓
Bağ durum kestirimi
      ↓
Kalite ─── Hazard ─── Belirsizlik
      ↓                 ↓
      └──── link riski ─┘
                    ↓
              yerel politika
                    ↓
        aday uygunluğu / maliyet / kontrol yoğunluğu
```

Bu zincir, bir bağın **şu anki iletim durumunu**, **yakın gelecekte kötüleşme eğilimini** ve **bu sonuca ne kadar güvenilebileceğini** ayırır. Risk, bunların yerine geçen ham bir ölçüm değildir.

## 2. Varlıklar ve bilgi sahipliği

Bir düğüm `i`, yalnızca doğrudan komşusu `j` ile ilgili yerel bir bağ kaydı tutar: `L(i,j)`. Bu kayıt, `i → j` yönündeki iletim deneyimine dayanır.

- `L(i,j)` ve `L(j,i)` farklı olabilir. Bağ simetrisi varsayılmaz.
- Bir düğüm, başka bir düğümün ölçümünü kendi yerel ölçümüyle eşdeğer kabul etmez.
- Hedefe ilişkin alan/potansiyel bilgisi, bağ kaydından ayrı bir bilgi nesnesidir.
- Yerel risk, ağ-geneli “kriz gerçeği” değildir. Komşudan gelen bir bildirim varsa bu yalnız ek kanıt olabilir.

Bu ayrım FR-04, FR-07, FR-10 ve NFR-04'ü destekler; aynı zamanda doğrulanmamış risk veya jamming bilgisinin yayılmasını sınırlamayı amaçlar.

## 3. Gözlem katmanı

Gözlem, bir düğümün ölçtüğü ham ya da doğrudan türetilmiş olgudur. Gözlem tek başına yönlendirme kararı değildir.

| Gözlem ailesi | Örnek kanıt | Ne söyler? | Ne söylemez? |
|---|---|---|---|
| Teslim deneyi | MAC/bağ-katmanı başarı-başarısızlık, yeniden iletim, ACK | Son iletim girişimlerinin sonucu | Kayıbın kesin nedeni |
| Zaman davranışı | Gecikme, varyasyon, ardışık kayıp serileri | İletimin son zaman davranışı | Uçtan uca gecikmenin yalnız bu bağdan kaynaklandığı |
| Radyo/kanal gözlemi | Uygunsa RSSI, SINR/SJR, kanal meşguliyeti | Yerel alıcı/verici çevresindeki fiziksel koşul kanıtı | Tek başına teslim olasılığı veya jamming kimliği |
| Hareket/komşuluk | Son duyulma, göreli konum/hız varsa eğilim, komşu değişim oranı | Bağ ömrünü etkileyebilecek değişim kanıtı | Kesin gelecek yörünge veya kesin kopma zamanı |
| Bilgi bütünlüğü | Ölçüm yaşı, örnek hacmi, gözlemler arası uyumsuzluk | Kestirimin güven sınırı | Bağın iletişim kalitesi |

Bir uygulama, her gözlem ailesini desteklemek zorunda değildir. Kullanılan her gözlem için ölçüm katmanı, örnekleme penceresi, geçerlilik koşulu ve arıza modu daha sonraki bilgi modelinde tanımlanmalıdır.

## 4. Kavram sözlüğü

### 4.1 Kalite `Q(i,j)`

**Soru:** “`i`, `j`'ye şu anda veri iletmeye çalışırsa iletişim koşulu ne durumda?”

Kalite, yakın tarihli yerel teslim ve gerekirse kanal gözlemlerinden türetilen **mevcut koşul kestirimidir**. İyi kalite, bağın mutlaka uzun süre yaşayacağı anlamına gelmez; kötü kalite de nedeninin jamming olduğu anlamına gelmez.

Kalitenin zorunlu özellikleri:

- Yönlüdür ve yereldir.
- Ölçüm zamanı ve örnek tabanı ile ilişkilidir.
- Yaşlandıkça kendisi değil, ona duyulan güven değişir.
- Maliyet veya risk ile eş anlamlı değildir.

### 4.2 Hazard `H(i,j)`

**Soru:** “Mevcut kanıt, bu bağın karar ufku içinde uygunsuz hale gelme eğilimi olduğunu gösteriyor mu?”

Hazard, kalite düzeyinden ayrı olarak **kötüleşme eğilimi/tehlike göstergesidir**. Örneğin iki bağ aynı anlık kaliteyi gösterebilir; hızlı kötüleşen teslim davranışı veya ayrılan komşu nedeniyle birinin hazard'ı daha yüksek olabilir.

Hazard olasılık ya da kesin kopma tahmini değildir; kalibrasyon ve kanıt yokken öyle yorumlanmayacaktır. Hazard üretmek için en az bir zamansal eğilim veya bağın sürdürülebilirliğine ilişkin gözlem gerekir. Tek bir kayıp olayından hazard çıkarılmamalıdır.

### 4.3 Belirsizlik `U(i,j)`

**Soru:** “Kalite ve hazard hakkındaki bilgi ne kadar güncel ve desteklenmiş?”

Belirsizlik; ölçüm yaşı, yetersiz örnek, gözlem çelişkisi, ölçüm kaynağının kullanılamazlığı ve komşu durumunun güvenilirliği gibi nedenlerle artan **epistemik güven sınırıdır**. Belirsizlik, kötü bağlantı demek değildir. Yeni gözlemi olmayan, daha önce iyi görünen bir bağ düşük kalite değil yüksek belirsizlik taşır.

### 4.4 Jamming evidence `J(i,j)`

**Soru:** “Yerel gözlemlerde kasıtlı karıştırmayla uyumlu, fakat başka nedenlerle de açıklanabilir bir örüntü var mı?”

Jamming evidence, isteğe bağlı bir açıklama düzeyidir. `J` ikili “jammer var/yok” bayrağı değildir ve riskin zorunlu girdisi değildir. Aynı örüntü girişim, tıkanıklık, çarpışma, hareket veya kanal bozulmasından kaynaklanabilir. Bu nedenle `J`, varsa bozunma gözlemlerini yorumlamaya yardım eder; yönlendirme kararı bir jamming hükmüne bağlanmaz.

### 4.5 Link riski `R(i,j)`

**Soru:** “Bu bağ, seçildiği anda sürdürülebilir forwarding için ne kadar ihtiyat gerektiriyor?”

Link riski, hazard ve belirsizliğin karar odaklı bileşimidir; kaliteyi yeniden adlandırmaz. Kalite, bağın mevcut hizmet koşulunu; risk ise bağın karar ufkundaki güvenilir seçilebilirliğini ifade eder.

Önerilen niteliksel monotonluk ilkeleri:

- Hazard artarsa, diğer bilgiler aynı kalırken risk azalmaz.
- Belirsizlik artarsa, diğer bilgiler aynı kalırken risk azalmaz.
- Hazard hakkında güçlü ve güncel iyi kanıt varsa, yalnız yaş nedeniyle bağlantı “kötü kaliteli” ilan edilmez; belirsizlik etkisi ayrı işlenir.
- Jamming evidence artışı tek başına kesin saldırı sonucu üretmez; yalnız destekleyen gözlem olarak kaydedilir.

Bu ilkeler bir ağırlıklı toplam veya olasılık formülü değildir. Sayısal temsil seçilmeden önce ölçek, normalizasyon, örnekleme ve hata analizi gerekir.

### 4.6 Politika

**Soru:** “Node, mevcut yerel bağ görünümü karşısında ne kadar ihtiyatlı davranmalı?”

Politika, ölçüm değildir ve link maliyeti değildir. Yerel bağ adaylarının kalite, hazard, belirsizlik ve risk görünümünden; ayrıca hedef alanının geçerliliğinden türetilen eylem seçicisidir. Olası etkiler şunlardır:

- gözlem veya probe sıklığını değiştirmek;
- geçerli adaylar arasında ihtiyatlı tercih yapmak;
- güvenli alternatif varsa önceden geçişe hazırlanmak;
- sınırlı yedekliliği yalnız gerektiğinde etkinleştirmek;
- alan bilgisini yenilemeyi istemek.

Bu tarihsel NORMAL/CRISIS adları, DL-014 ile alan-geneli STEADY/CAUTION/PROTECT postürleriyle değiştirilmiştir. Politika değişimi, forwarding güvenlik koşulunu gevşetemez.

### 4.7 Maliyet ve potansiyel

Maliyet `C(i,j)` bağ seçiminin toplanabilir yönlendirme temsilidir; potansiyel `P_d(i)` ise belirli hedef `d` için tahmini toplam maliyettir. İkisi de gözlem, kalite, hazard, belirsizlik veya riskle özdeş değildir.

Sonraki maliyet fazı, şu kararı verecektir: kalite ve/veya risk maliyette tercih sinyali mi olur; yoksa bazı risk/belirsizlik seviyeleri aday uygunluğunu mu sınırlar? Bu belgede seçim yapılmamıştır.

## 5. Karar katmanları arasında yasak eşleştirmeler

| Yanlış eşleştirme | Neden hatalı? | Doğru yaklaşım |
|---|---|---|
| Paket kaybı = jamming | Aynı gözlem birçok nedenden doğabilir. | Kayıp, teslim/kalite kanıtıdır; jamming evidence ayrı ve ihtiyatlıdır. |
| Düşük kalite = yüksek hazard | Şu anda kötü olan bağ iyileşebilir; iyi bağ hızla bozulabilir. | Düzey ve eğilim ayrı değerlendirilir. |
| Bayat bilgi = kötü bağ | Gözlemin yaşı bağın fiziksel durumunu ölçmez. | Belirsizlik ve komşu geçerliliği artar. |
| Risk = maliyet | Risk karar ihtiyatı; maliyet toplamsal rota temsili olabilir. | Etkileşim, maliyet fazında ayrı gerekçelendirilir. |
| CRISIS = jamming | Politika, her türlü önemli yerel bozunmaya tepki olabilir. | Policy change için nedensel saldırı atfı gerekmez. |
| Daha düşük potansiyel = güvenli forwarding | Bayat/eşzamanlı alan bilgisi döngü yaratabilir. | Ayrı loop-freedom kabul koşulu gerekir. |

## 6. Bir örnek düşünce deneyi

`i` düğümünün hedef `d` için iki komşusu olsun: `a` ve `b`.

- Her iki bağın son teslim başarısı benzer ise `Q(i,a)` ve `Q(i,b)` benzer olabilir.
- `a` için son ardışık ölçümler bozuluyorsa veya komşu hızla uzaklaşıyorsa `H(i,a)` yükselir.
- `b` uzun süredir duyulmamış ama en son iyi görünmüşse `U(i,b)` yükselir; `b`'nin kalitesinin iyi kaldığı sonucu çıkarılmaz.
- `i`, bu görünümü politika katmanına aktarır. Politika, güvenli alan/forwarding koşullarını koruyarak daha çok gözlem, alternatif hazırlığı veya alan yenileme isteği seçebilir.

Bu örnek, hangi komşunun kesin seçileceğini, çoğaltma yapılacağını veya hangi eşiklerin kullanılacağını belirlemez.

## 7. Gereksinim izlenebilirliği

| Kavramsal öğe | Karşıladığı gereksinimler | Sonraki bağımlı çıktı |
|---|---|---|
| Yerel yönlü bağ kaydı | FR-01, FR-04, FR-07, FR-11 | Bilgi ve komşu modeli |
| Kalite | FR-04, FR-07 | Ölçüm/kalite modeli |
| Hazard | FR-02, FR-04 | Hazard modeli |
| Belirsizlik | FR-01, FR-07, FR-11 | Freshness ve komşu modeli |
| Link riski | FR-02, FR-04, FR-07, FR-12 | Risk ve politika modeli |
| Politika | FR-02, FR-08, FR-12, NFR-01 | Uyarlamalı politika modeli |
| Maliyet/potansiyel ayrımı | FR-09, FR-10, NFR-03 | Maliyet ve alan modeli |

## 8. Açık kararlar ve öneri

Bu belge iki mimari yönden önemli öneri getirir:

1. **Riski olasılık veya jamming etiketi değil, link-yerel ihtiyat değişkeni olarak ele almak.** Bu, zayıf/heterojen gözlemler altında dürüst davranır; bedeli, daha sonra karar kurallarının dikkatle tanımlanmasıdır.
2. **Kalite, hazard ve belirsizliği ayrı tutmak.** Bu, v0'daki `C_jam` tek terimini daha doğru bir gözlemsel modele dönüştürür; bedeli, en az üç semantik durumu tutarlı biçimde izlemektir.

Bu öneriler risk semantiğini ve dolayısıyla maliyet/politika mimarisini etkilediğinden, onaylanmadan tasarım kararı sayılmaz. Onay sonrası sıradaki faz, her kavramın tutulacağı yerel bilgi kaydını ve komşu yaşam döngüsünü belirlemektir.
