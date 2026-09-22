# Yöntem: Ön-Kayıtlı Yanlışlanma Koşulu, Çoklu Tohum Tasarımı ve Eşleştirilmiş İstatistiksel Testler

## 1. Genel Yöntembilimsel Gerekçe

Ağ protokollerinin simülasyon tabanlı değerlendirmesi, deneysel bir süreçtir ve deneysel araştırmaların yöntembilimsel katılığına tabidir. İyi tasarlanmış bir simülasyon çalışması, üç yöntembilimsel ilkeyi birlikte uygulamalıdır: (i) hipotezleri ve başarı/ başarısızlık kriterlerini sonuçları görmeden önce kaydetmek (ön-kayıt), (ii) yeterli sayıda rastgele tohum (seed) kullanarak istatistiksel güç sağlamak ve (iii) karşılaştırılan protokolleri aynı rastgele koşullar altında eşleştirilmiş biçimde test ederek varyansı azaltmak. Bu üç ilke birbirini tamamlar: ön-kayıt, çalışmanın yanlışlanabilirliğini sağlar; çoklu tohum, sonuçların rastgeleliğe bağlı olmaktan çıkarılmasını güvence altına alır; eşleştirilmiş testler ise aynı tohum altında iki protokolün aynı mobilite ve trafik koşullarına maruz bırakılmasıyla istatistiksel güçü artırır (Goldsman, 2020; Munafò et al., 2017; Siepe et al., 2024).

---

## 2. Ön-Kayıtlı Yanlışlanma Koşulu

### 2.1. Tanım

Ön-kayıtlı yanlışlanma koşulu (pre-registered falsification condition), bir simülasyon çalışmasının hipotezlerini, değişkenlerini, metriklerini ve başarı/başarısızlık eşiklerini sonuçları gözlemeden önce resmi olarak kaydetmesi ve bu kaydın zaman damgalı bir platformda (örn. Open Science Framework, Zenodo, AsPredicted) yayınlanmasıdır (Siepe et al., 2024). Bu yaklaşım, Karl Popper'ın yanlışlanabilirlik ilkesini simülasyon araştırmalarına taşır: bir teori ancak belirli koşullar altında çürütülebilir (falsifiable) ise bilimsel olarak kabul edilir; bu koşulların sonuçlardan sonra değil, önceden tanımlanması gerekir (Herskovitz, 1991).

### 2.2. Yanlışlanma Koşulunun Biçimi

Bir FANET yönlendirme protokolü simülasyonunda, ön-kayıtlı yanlışlanma koşulu şu biçimde tanımlanabilir:

> **H1 (üstünlük hipotezi):** Önerilen protokol, baseline protokol (AODV veya OLSR) ile karşılaştırıldığında, karıştırma (jamming) altında ön-kayıtlı kriterleri karşılayacak biçimde PDR'de iyileşme, E2E gecikmede iyileşme VEYA yönlendirme yükünde azalma sağlar.
>
> **Yanlışlanma koşulu (falsification rule):** Eğer önerilen protokolün median PDR artışı \(\Delta_{\text{PDR}} \leq 0\) ise VEYA E2E gecikmede artış \(\Delta_{\text{E2E}} > \tau_{\text{E2E}}\) ise VEYA yönlendirme yükünde artış \(\Delta_{\text{OH}} > \tau_{\text{OH}}\) ise, \(H_1\) üstünlük hipotezi reddedilir/desteklenmez.
>
> Burada \(\tau_{\text{E2E}}\) ve \(\tau_{\text{OH}}\), ön-kayıt aşamasında tanımlanan eşiklerdir. Örneğin, \(\tau_{\text{E2E}} = 5\) ms ve \(\tau_{\text{OH}} = 20\%\) yalnızca örnek amaçlıdır; bu eşikler çalışmanın bağlamına göre önceden belirlenmelidir.

Bu koşulların sonuçlardan önce tanımlanması, "hindsight bias" (geriye dönük önyargı), "confirmation bias" (doğrulama önyargısı) ve "selective reporting" (seçici raporlama) gibi bilişsel yanılgıların etkisini azaltır (Siepe et al., 2024; Munafò et al., 2017).

### 2.3. Simülasyonlarda Ön-Kaydın Yöntembilimsel Önemi

Siepe vd. (2024), ADEMP-PreReg şablonunu geliştirerek simülasyon çalışmalarının planlanması, ön-kaydı ve raporlanması için standart bir çerçeve sunmuştur. Bu çerçeveye göre ön-kayıt şunları sağlar:

- **Araştırmacı serbestisini (researcher degrees of freedom) sınırlar:** Hangi simülasyon koşullarının dikkate alındığı ve neden, sonuçlardan önce belgelenir.
- **Değerlendirme kriterlerini sabitler:** Hangi performans farkının "anlamlı" sayılacağı önceden tanımlanır; post-hoc yorumlama engellenir.
- **Bilişsel yanılgılara karşı koruma:** Hindsight bias ve confirmation bias'a karşı bir tampon görevi görür.
- **Geçerli null sonuçların yayımlanabilirliğini kolaylaştırır:** Olumsuz sonuçların selective reporting nedeniyle bastırılmasını önler.

Munafò vd. (2017), "A Manifesto for Reproducible Science" başlıklı çalışmalarında, bilimsel araştırmaların güvenilirliğini artırmak için ön-kaydın benimsenmesi gerektiğini vurgulamıştır.

### 2.4. Ön-Kaydın Sınırları

Rubin (2024), ön-kaydın Popper'ın teori-merkezli yanlışlanabilirlik felsefesinde Mayo'nun hata-istatistiksel yaklaşımındaki kadar etkin olmadığını öne sürmektedir. Ancak bu eleştiri, ön-kaydın değerini tamamen reddetmez; sadece amaç odaklı ve bağlama duyarlı bir kullanım gerektirir. Simülasyon çalışmalarında ön-kayıt özellikle olgun (mature) yöntemlerin nötr biçimde karşılaştırıldığı geç faz (late-phase) çalışmalarda daha fazla yarar sağlar; erken faz araştırmalarında daha az kritiktir (Siepe et al., 2026).

---

## 3. \(\geq 30\) Rastgele Tohum Kullanımı ve Ortak Rastgelelik

### 3.1. Neden \(\geq 30\) Tohum?

Simülasyon çıktıları (PDR, gecikme, overhead) rastgele süreçler olduğundan, tek bir tohumdan elde edilen sonuçlar istatistiksel olarak anlamlı bir genelleme için yeterli değildir. Merkez Limit Teoremi (CLT), örneklem boyutu \(n \geq 30\) olduğunda örneklem ortalamasının dağılımının yaklaşık olarak normale yakınsadığını gösterir; bu, eşleştirilmiş parametrik testlerin (örn. eşleştirilmiş \(t\)-testi) pratik bir alt sınır sağlar. Ancak bu bir garanti değil, büyük-örneklem çıkarımı için makul bir alt sınırdır; sonuç dağılımı çarpık veya ağır kuyrukluysa ek tohum, Wilcoxon, permütasyon veya bootstrap güven aralığı gerekir (Goldsman, 2020; Siepe et al., 2024).

Simülasyon literatüründe, tekrarlama sayısı (\(n_{\text{sim}}\)) rastgele belirlenmemelidir; Monte Carlo standart hatası (MCSE) hedeflenen kesinliğe ulaşacak şekilde seçilmelidir (Siepe et al., 2024). Siepe vd. (2024), incelenen 100 simülasyon çalışmasının yalnızca %8'inin tekrarlama sayısını gerekçelendirdiğini ve %3'ünün gerekli sayıyı hesapladığını raporlamıştır; bu, çoğu çalışmada tohum/tekrarlama sayısının keyfi seçildiği anlamına gelir.

### 3.2. \(\geq 30\) Tohumun İstatistiksel Gerekçesi

Bir performans metriği \(M\) için, \(n\) farklı tohumdan elde edilen sonuçlar \(M_1, M_2, \ldots, M_n\) olsun. Örneklem ortalaması:

\[
\bar{M} = \frac{1}{n} \sum_{r=1}^{n} M_r
\]

Örneklem varyansı:

\[
S^2 = \frac{1}{n-1} \sum_{r=1}^{n} (M_r - \bar{M})^2
\]

Merkez Limit Teoremi altında, \(n \geq 30\) için \(\bar{M}\) yaklaşık olarak normal dağılır:

\[
\bar{M} \sim \mathcal{N}\left(\mu_M, \frac{S^2}{n}\right)
\]

Bu, güven aralıkları ve hipotez testleri için yaklaşık bir normalite temeli sağlar. Ancak nihai tekrarlama sayısı, Monte Carlo standart hatası (MCSE) veya hedeflenen istatistiksel güç temelinde gerekçelendirilmelidir; \(n \geq 30\) yalnızca pratik bir başlangıç noktasıdır. Daha küçük \(n\) değerlerinde veya çarpık dağılımlarda, normalite varsayımı geçerli olmayabilir ve parametrik olmayan testler (örn. Wilcoxon) tercih edilmelidir.

### 3.3. Ortak Rastgele Sayılar (Common Random Numbers — CRN)

Her tohum \(r\) için, her iki protokol (A: önerilen, B: baseline) aynı rastgele girdilere tabi tutulur:

- Aynı mobilite izi (Gauss-Markov konum dizisi)
- Aynı trafik paterni (CBR paket üretim zamanları)
- Aynı kanal gürültü realizasyonu
- Aynı karıştırıcı (jammer) aktivite paterni

Bu teknik, Common Random Numbers (CRN) olarak bilinir ve "matched streams" veya "matched pairs" olarak da adlandırılır (Goldsman, 2020). CRN, eşleştirilmiş \(t\)-testinin temelini oluşturur.

### 3.3.1. CRN Uygulama Notu

CRN'in etkili olması için, her iki protokolün aynı rastgele girdilere tabi tutulması gerekir. Bu, aşağıdaki yöntemlerle sağlanır:

- **Ön-üretilmiş izler (pre-generated traces):** Mobilite konum dizileri, trafik paket üretim zamanları, kanal gürültü realizasyonları ve karıştırıcı aktivite paternleri her iki protokol için önceden aynı tohumla üretilip bir dosyaya kaydedilir ve her iki protokol de aynı dosyadan okur.
- **Ayrık senkronize akışlar (separate synchronized substreams):** Her rastgelelik kaynağı (mobilite, trafik, kanal, jammer) için ayrı bir RNG akışı ayrılır. Bu akışlar her iki protokolde aynı sırayla ve aynı amaçla kullanılır.

> **Önemli:** Uyarlamalı (adaptive) protokollerde, farklı kontrol yolları farklı sayıda RNG çağrısı yapabilir ve akışları senkronizasyondan çıkarabilir (desynchronization). Bu nedenle, protokol içi RNG çağrılarına güvenmek yerine, dışsal girdilerin önceden üretilmesi ve dosyalardan okunması önerilir.

### 3.4. CRN ile Varyans Azaltımı

İki protokolün aynı tohum \(r\) altındaki sonuçları sırasıyla \(M_{A,r}\) ve \(M_{B,r}\) olsun. Eşleştirilmiş fark:

\[
\Delta_r = M_{A,r} - M_{B,r}, \quad r = 1, 2, \ldots, n
\]

Bu farkların varyansı:

\[
\operatorname{Var}(\Delta_r) = \operatorname{Var}(M_{A,r}) + \operatorname{Var}(M_{B,r}) - 2 \operatorname{Cov}(M_{A,r}, M_{B,r})
\]

Eğer iki protokol bağımsız (farklı tohumlarla) çalıştırılırsa, \(\operatorname{Cov}(M_{A,r}, M_{B,r}) = 0\) olur. CRN altında ise \(\operatorname{Cov}(M_{A,r}, M_{B,r}) > 0\) beklenir, çünkü her iki protokol de aynı rastgele koşullara maruz kalır ve benzer şekilde tepki verir. Bu pozitif kovaryans, farkların varyansını azaltır (Goldsman, 2020):

\[
\operatorname{Var}(\Delta_r) < \operatorname{Var}(M_{A,r}) + \operatorname{Var}(M_{B,r})
\]

Sonuç olarak, CRN ile eşleştirilmiş tasarım, aynı istatistiksel güçü daha az tekrarlama sayısıyla veya aynı sayıda tekrarlama ile daha dar güven aralıklarıyla elde eder.

---

## 4. Eşleştirilmiş Hipotez Testleri

### 4.1. Eşleştirilmiş \(t\)-Testi (Paired \(t\)-Test)

CRN tasarımı altında, her tohum \(r\) için iki protokolün sonuçları eşleştirilir ve farklar \(\Delta_r = M_{A,r} - M_{B,r}\) hesaplanır. Farkların ortalaması:

\[
\bar{\Delta} = \frac{1}{n} \sum_{r=1}^{n} \Delta_r
\]

Farkların standart sapması:

\[
S_{\Delta} = \sqrt{\frac{1}{n-1} \sum_{r=1}^{n} (\Delta_r - \bar{\Delta})^2}
\]

Eşleştirilmiş \(t\)-test istatistiği:

\[
t = \frac{\bar{\Delta} - \Delta_0}{S_{\Delta} / \sqrt{n}}, \quad \text{df} = n - 1
\]

burada \(\Delta_0\), sıfır hipotezi altındaki beklenen farktır (genellikle \(\Delta_0 = 0\)).

\(\%95\) güven aralığı:

\[
\bar{\Delta} \pm t_{\alpha/2, \, n-1} \cdot \frac{S_{\Delta}}{\sqrt{n}}
\]

Burada \(t_{\alpha/2, \, n-1}\), \(n-1\) serbestlik derecesine sahip Student \(t\)-dağılımının \(\alpha/2\) yüzdelik değeridir (Goldsman, 2020).

### 4.2. Varsayımlar

Eşleştirilmiş \(t\)-testinin geçerli olması için:

1. **Farkların normalitesi:** \(\Delta_r\) farklarının yaklaşık normal dağıldığı varsayılır. Bu, ham verilerin değil, farkların normalitesidir.
2. **Yeterli örneklem boyutu:** \(n \geq 30\) olduğunda, Merkez Limit Teoremi nedeniyle \(t\)-testi normalite sapmalarına karşı sağlamdır (robust).
3. **Bağımsızlık:** Farklı tohumlar (\(r \neq r'\)) arasında bağımsızlık varsayılır; aynı tohum içindeki iki protokol bağımlıdır (bu, eşleştirilmiş tasarımın tanımıdır).

### 4.3. Wilcoxon İşaretli Sıra Testi (Wilcoxon Signed-Rank Test)

Eğer farkların normalitesi sağlanmazsa (örneğin, çift modlu veya uzun kuyruklu dağılımlar, aykırı değerler, veya \(n < 30\) durumları), parametrik olmayan Wilcoxon işaretli sıra testi tercih edilir (Wilcoxon, 1945). Bu test:

- Farkların mutlak değerlerini sıralar
- İşaretleri (pozitif/negatif) dikkate alır
- Normalite varsayımı gerektirmez

Ancak Wilcoxon işaretli sıra testi de bazı varsayımlara sahiptir:

- **Bağımsızlık:** Eşleştirilmiş farkların birbirinden bağımsız olması gerekir (farklı tohumlar arasında bağımsızlık).
- **Simetri:** Farkların dağılımı medyan etrafında yaklaşık simetrik olmalıdır. Eğer simetri şüpheliyse veya çok sayıda sıfır fark/bağ (tie) varsa, işaret testi (sign test), permütasyon testi veya bootstrap güven aralığı daha sağlam alternatifler olarak kullanılmalıdır.

Wilcoxon test istatistiği \(W\), pozitif sıraların toplamı olarak tanımlanır ve sıfır hipotezi \(\text{medyan}(\Delta_r) = 0\) olarak test edilir (Wilcoxon, 1945).

### 4.4. Test Seçim Kararı

| Durum | Önerilen Test | Gerekçe |
|---|---|---|
| \(n \geq 30\) ve farklar yaklaşık normal | Eşleştirilmiş \(t\)-testi | Maksimum istatistiksel güç |
| \(n \geq 30\) ve hafif normalite sapması, aykırı değer yok | Eşleştirilmiş \(t\)-testi | CLT nedeniyle yaklaşık sağlam (robust) |
| \(n \geq 30\) ve belirgin çarpıklık, ağır kuyruk, aykırı değerler | Wilcoxon işaretli sıra testi | Parametrik olmayan alternatif |
| \(n < 30\) ve farklar yaklaşık normal | Eşleştirilmiş \(t\)-testi | Küçük örneklemde normalite varsayımı |
| \(n < 30\) ve farklar normal değil | Wilcoxon işaretli sıra testi | Parametrik olmayan alternatif |
| Çok sayıda sıfır fark veya bağ (tie) | Permütasyon testi veya bootstrap CI | Bağ problemini aşma |
| Simetri şüpheli | İşaret testi (sign test) veya permütasyon | Simetri varsayımı gerektirmeyen alternatif |

> **Analiz birimi:** İstatistiksel analiz birimi, tek tek paketler veya atlama (hop) bazlı gözlemler değil, her bir tohum/çalıştırmadan (seed/run) elde edilen toplu metrik değeridir. Her tohum bir gözlem birimidir.

### 4.5. Çoklu Karşılaştırma Düzeltmesi

Birden fazla protokol çiftini karşılaştırırken (örn. A vs. B, A vs. C, A vs. D), çoklu karşılaştırma problemi (ailevi hata oranı şişmesi) ortaya çıkar. Bu durumda Bonferroni düzeltmesi uygulanmalıdır:

\[
\alpha' = \frac{\alpha}{m}
\]

burada \(m\), karşılaştırma sayısıdır. Örneğin, 3 ikili karşılaştırma için \(\alpha' = 0.05 / 3 = 0.0167\).

---

## 5. Raporlama İlkeleri

### 5.1. Şeffaflık ve Tekrar Üretilebilirlik

Bir simülasyon çalışmasının yöntem bölümü, aşağıdaki bilgileri içermelidir:

1. **Tohum listesi:** Kullanılan tüm tohum değerleri (örn. 42, 123, 456, ..., 9999)
2. **CRN eşleştirme protokolü:** Her tohum için her iki protokolün aynı mobilite/trafik/kanal girdilerini paylaştığı açıkça belirtilmeli
3. **İstatistiksel test:** Hangi testin kullanıldığı, neden seçildiği ve varsayımların nasıl doğrulandığı
4. **Etki büyüklüğü:** Yalnızca \(p\)-değeri değil, etki büyüklüğü de raporlanmalıdır (örn. Cohen'in \(d\) değeri)
5. **Güven aralıkları:** Nokta tahminleri yanında %95 güven aralıkları verilmeli
6. **Hesaplama ortamı:** SimPy/NetworkX sürümü, Python sürümü, donanım konfigürasyonu

### 5.2. Ön-Kayıt Bağlantısı

Eğer çalışma ön-kaydedilmişse, yöntem bölümünde ön-kayıt bağlantısı (DOI veya URL) verilmeli ve herhangi bir sapma (amendment) şeffaf biçimde raporlanmalıdır (Siepe et al., 2024).

---

## Kaynaklar

Goldsman, D. (2020). *Comparing systems: Common random numbers and paired-t confidence intervals* [Ders notları]. School of Industrial and Systems Engineering, Georgia Institute of Technology. https://www2.isye.gatech.edu/~sman/courses/6644/Module10-ComparingSystems-201128.pdf

Herskovitz, P. J. (1991). A theoretical framework for simulation validation: Popper's falsificationism. *International Journal of Modelling and Simulation, 11*(2), 51–55. https://doi.org/10.1080/02286203.1991.11760122

Munafò, M. R., Nosek, B. A., Bishop, D. V. M., Button, K. S., Chambers, C. D., Percie du Sert, N., Simonsohn, U., Wagenmakers, E.-J., Ware, J. J., & Ioannidis, J. P. A. (2017). A manifesto for reproducible science. *Nature Human Behaviour, 1*(1), 0021. https://doi.org/10.1038/s41562-016-0021

Rubin, M. (2024). Preregistration does not improve the transparent evaluation of severity in Popper's philosophy of science or when deviations are allowed. *arXiv preprint*. https://arxiv.org/abs/2408.12347

Siepe, B. S., Bartoš, F., Morris, T. P., Boulesteix, A.-L., Heck, D. W., & Pawel, S. (2024). Simulation studies for methodological research in psychology: A standardized template for planning, preregistration, and reporting. *Psychological Methods, 29*(6), 1319–1339. https://doi.org/10.1037/met0000657

Siepe, B. S., Bartoš, F., Boulesteix, A.-L., Heck, D. W., Peikert, A., Sarafoglou, A., & Pawel, S. (2026). *Why, when, and how to (or not to) preregister a simulation study* [Preprint]. https://osf.io/preprints/psyarxiv/cxjrb

Wilcoxon, F. (1945). Individual comparisons by ranking methods. *Biometrics Bulletin, 1*(6), 80–83. https://doi.org/10.2307/3001968
