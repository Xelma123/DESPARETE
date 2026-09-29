

# K-184 · 🟢 `analiz/` KATMANI — ön-kaydın analiz planı kodda (Faz 6'nın parçası, erken)
> 26 Eylül · uzun koşular sürerken koşunun kullanmadığı iş (öğrenci: "boş durma") · ajan

**Ne:** `analiz/istatistik.py` ve `analiz/satir.py`; simülatörden hiçbir şey içe aktarmaz (test tarar).
- **Wilcoxon** (çift yönlü, eşleştirilmiş):
  - Yöntem `auto`ya bırakılmaz: sıfır olmayan fark ≤ 50 ve bağ yoksa kesin, değilse normal yaklaşım; seçilen yöntem sonuca yazılır.
  - **NaN tuzağı** (`v2/06` §7) kodda kapalı: bütün farklar sıfırsa test çağrılmaz, `p = 1`. Holm'a sonlu olmayan bir p girerse hata verir.
- **Holm, δ, hüküm:** δ = 2·SD_ref/√n (§0.4.2); hüküm tablosu üstün · aşağı · ayırt edilemedi.
- **Güç eğrisi ve MDE₈₀** (§0.4.3): merkezlenmemiş gürültü reddedilir.
- **GA:** eşleştirilmiş ortalama farkın yüzdelik bootstrap'ı. Yöntem §7'de yazmıyordu; burada seçildi ve beyan edildi.
- **Eşleştirme bir iddia olarak denetlenir:**
  - `arac_hash` ve `kurulum_hash` bütün satırlarda aynı olmalı;
  - her tohumda senaryo, tehdit, desen ve `evren_hash` aynı olmalı;
  - geçersiz satır sayılarak dışlanır; `None` metrik sessizce atlanmaz, hata verir.
- **Ham ikinci gerçekleme:** pencere PDR'si, gecikme p50/p95/p99 ve görev teslim oranı `ham`dan yeniden üretilir.

**Ölçüm:**
- `tests2/test_analiz.py` **16/16**.
- İkinci gerçekleme, düğüm kayıplı gerçek bir koşunun satırında simülatörün sayılarını **tam eşitlikle** yeniden üretti.
- Bozulmuş ham listeyi yakaladı.

**Açık (Faz 6):** hücre koşucusu (JSONL kümesinden H2.a–c tablosu), güç yönteminin taban protokol gürültüsüyle koşumu.

# K-185 · 🟢 REFERANS DÜNYANIN ALANI 35 km — öğrenci: "ölçütü boşver, en mantıklı ve gerçekçi olana önem ver"
> 26 Eylül · Faz 4.1a · karar ajanın (öğrenci devretti) · ölçüm `arsiv/teshis/faz4_2026-09-26/a_calisma_noktasi_sonuc.md` · beklenti `a_calisma_noktasi_beklenti.md` (ölçmeden önce)

**Bulgu:**
- Referans telsizle bağ 1 Mb/s'te ~9–10 km uzanıyor: 20 dBm EIRP, dipol, serbest uzay, σ 3 dB, K 10 dB, 7 yeniden deneme, ARF tabanı.
- 7 km'lik sürüde derece 37,4/39, çiftlerin %96'sı tek atlama, ≥ 3 atlama %0. Yönlendirmeye iş kalmıyor. K-181'deki karıştırmasız tek atlama PDR'si 0,986 bununla tutarlı.
- `v2/14` §3'ün ~6–8 km'si 10 dB paylı nominal bağa (1,65 km) dayanıyordu.
- Tarama (30 tohum): 30 km geçer; **35 km geçer** (derece 8,82, derin çift %31,9); 36–40 km kopar (%0,2–0,8).
- Eski dünyanın noktası 8,67 · %31,0 idi; ölçüt aynı topolojiyi 1:1 ölçekte buluyor.

**Karar ve gerekçe (ajan):**
1. **Fizik doğru.** 50–300 m irtifada hava–hava yayılımı serbest uzaydır; iki ışın kırılma mesafesi ~325 km (`v2/14` §2). Menzili kaynaksız bir kayıpla kısaltmak fiziği bozardı.
2. **Geometri platformun zarfı içinde:** NATO Sınıf I görev yarıçapı ≤ 50 km (G9).
3. **Karıştırma gerçekçi rejime oturur.** 1–50 W'lık karıştırıcı 35 km'lik ağın bir bölgesini etkiler. 7 km'de sürünün tamamını karartırdı; `v2/14` §4'ün sınır cümlesi tam da bunu söylüyor.
4. **B (7 km):** yönlendirme farkı ölçülemez. **C (menzili kısaltmak):** kaynağı yok. İkisi de reddedildi.

**⚠️ Beyan (yön):** gövde gölgelemesi ve anten yönelimi (yatış) modellenmiyor. Bağ bir üst sınırdır, gerçek sürüde aynı derinlik daha küçük alanda oluşur. Açık ölçüm raporları (ör. NASA hava–yer kanal ölçümleri) indirilirse bu kayıp modele girer ve alan yeniden ölçülür (her indirme izinle).

**Hareketli kol:** 35 km'de bağımsız kolda 10 tohumun 4'ü en az bir anda kopuyor (ortalama %0,83). Eski dünyadaki mertebe (1700 m'de 3/10); bölünme payı satırda beyan edilir (K-132), tablo 4.1d'de yeniden ölçülür.

**Uygulandı:**
- `REFERANS_ALAN_M = 35000`; köken ÖLÇÜLMÜŞ → SINANMAMIŞ 48 → **47**.
- `v2/14` §3 ve §10(i), `v2/06` §0.4.4 ve §9.
- Görev yarıçapı alan oranıyla 12,6 km (geçici; 4.1d'de derece eşitliğiyle).

**Beklentiyle:** seçilen alan 20–25 km ✗ (35 km). L/r ≈ 3,4 tuttu; yanılan, etkin bağ uzunluğuydu (~10 km, tahminim 7–7,5). 1 Mb/s PER %10 yarıçapı 7,4 km ✗ (8,9 km): DBPSK aynı Eb/N0'da DQPSK'dan ~1,6 dB iyi, bunu saymamıştım.
