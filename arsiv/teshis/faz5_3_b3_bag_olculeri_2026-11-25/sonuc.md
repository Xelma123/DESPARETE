# Faz 5-3 · B3 teşhisi — bağın iki ölçüsü aynı bağda, bizim çekirdeğimizin trafiğinde — sonuç

> 26 Kasım 2026 · ölçüt `beklenti.md` (öngörüler ve karar kuralı commit `08b180e`, koşudan ve dumandan önce; duman notu commit `ce77bbb`).
> - **Koşu** (`zaman.txt`): 25 Kasım 23:18 – 26 Kasım 02:28, toplam 3 sa 10 dk (tahmin 2–3 sa). Adımlar: ikiz 1 sa 50 dk · birincil 1 sa 19 dk.
> - **Kopya:** `kopya/` = `ce77bbb`, 166 dosya birebir (`kopya_ozet.txt`).
> - **Çıktılar:** ham çıktı `olcum_*.txt`, kayıt `kayit_*.json.gz`; karar kuralı `sonuc_hesap.py` → `sonuc_hesap.txt`.
> - **Ek sayılar:** `ek_hesap.py` → `ek_hesap.txt` (koşudan ve karar hesabından sonra yazıldı, karar girdisi değil).

## 0 · Geçerlilik ✓

- 16 koşunun hepsi kayıtta ve geçerli; kaydedicinin iç denetimleri 16 koşuda da geçti.
- Satırlar B2 teşhisinin satırlarıyla iki hücrede 8/8 tohumda bütün alanlarda birebir. Kaydedici davranışı değiştirmedi.
- Örnek sayısı: veri örneği ikizde 89 669, birincilde 88 784 (koşu başına 10 943–11 426); ızgara örneği 260 782 · 252 908 (koşu başına 28 781–35 835).
- İkiz adımı tahminin üstünde sürdü: koşu başına 87–110 dk; B2 teşhisinde aynı hücrenin adımı 52 dk. Simülasyon belirlenimli olduğu için sayıları etkilemez; sebebi ölçülmedi.

## 1 · S1 — ayrışma (betimleyici)

Kullanılan bağ, temiz sınıf, en az 8 önceki kayıt, `E_selam` sonlu:

| hücre | örnek | log2(`E_veri` / `E_selam`) ortancası | çeyrekler | `E_veri` > `E_selam` payı |
|---|---|---|---|---|
| ikiz | 75 288 | +0,168 | −0,101 … +0,453 | 0,660 |
| birincil | 48 674 | +0,159 | −0,117 … +0,455 | 0,649 |

Veri, kullanılan bağı selamdan ortanca ~%12 pahalı gösteriyor; örneklerin üçte ikisinde veri daha pahalı.

## 2 · K1 — selamın dönüşümü (karar)

- Genel katsayı (seçim yarısı): log2 k = +0,171 (k = 1,125).
- OMH, bit (seçim · doğrulama): D0 0,314 · 0,308 · D1 0,298 · 0,289 · D2 0,349 · 0,353.
- **Seçilen D0:** D1'in kazancı seçimde 0,016 bit, 0,10 sınırının altında. Düğümün kendi katsayısı (D2) en kötüsü.
- **Aktarılabilirlik:** ızgarada log2(`E_selam` · p) ortancası kullanılan bağlarda 0,636 (n 67 085), kullanılmayanlarda 1,032 (n 307 403); fark 0,396 bit → aktarılabilir.

**Hüküm K1: dönüşüm yok.** Ês* = `E_selam`.

## 3 · K2 — verinin üstünlüğü (karar)

En az 8 önceki kaydı olan örneklerde OMH, bit:

| yarı | hücre | örnek | `E_veri` | `E_selam` |
|---|---|---|---|---|
| seçim | ikisi | 59 464 | 0,241 | 0,308 |
| | ikiz · birincil | 36 168 · 23 296 | 0,231 · 0,256 | 0,308 · 0,308 |
| doğrulama | ikisi | 58 637 | **0,231** | **0,305** |
| | ikiz · birincil | 35 511 · 23 126 | 0,222 · 0,252 | 0,298 · 0,315 |

**Hüküm K2: veri üstün değil.** Doğrulamada fark 0,074 bit, sınır 0,10.
- Veri ölçüsü kullanılan bağın sonraki veri bedelini daha iyi kestiriyor: ortanca hata ~%17 ↔ ~%24.
- Ama fark, önceden yazdığım pratik eşiğin altında.

## 4 · K3 — yeterli kayıt ve tazelik (karar)

En az n önceki kaydı olan örneklerde OMH, bit (`E_veri` son n kayıtla · `E_selam`, aynı örnekler):

| n | seçim: örnek · `E_veri` · `E_selam` | doğrulama: örnek · `E_veri` · `E_selam` |
|---|---|---|
| 1 | 67 705 · 0,644 · 0,313 | 67 659 · 0,644 · 0,308 |
| 2 | 66 624 · 0,476 · 0,313 | 66 387 · 0,476 · 0,306 |
| 3 | 65 505 · 0,415 · 0,311 | 65 099 · 0,415 · 0,306 |
| 4 | 64 394 · 0,363 · 0,310 | 63 855 · 0,369 · 0,306 |
| 6 | 62 209 · 0,316 · 0,308 | 61 367 · 0,322 · 0,306 |
| 8 | 59 464 · 0,285 · 0,308 | 58 637 · 0,285 · 0,305 |
| 12 | 55 172 · **0,252** · 0,308 | 54 271 · **0,248** · 0,300 |
| 16 | 51 263 · 0,233 · 0,306 | 50 032 · 0,222 · 0,299 |

- **`VERI_EN_AZ` = 12** (seçim yarısında 0,05 bitlik farkı ilk sağlayan n); doğrulandı (0,248 ≤ 0,300).
- 6 kayıtla veri selamdan iyi değil; 1–4 kayıtla belirgin kötü.
- **Tazelik:** en yeni önceki kaydın yaşına göre bütün dilimlerde veri selamdan iyi; `VERI_TAZE_S` = 30 s.

  | yaş dilimi (s) | seçim: örnek · `E_veri` · `E_selam` | doğrulama: örnek · `E_veri` · `E_selam` |
  |---|---|---|
  | < 2 | 53 411 · 0,234 · 0,306 | 52 780 · 0,229 · 0,300 |
  | 2–5 | 952 · 0,295 · 0,380 | 663 · 0,263 · 0,303 |
  | 5–10 | 395 · 0,322 · 0,417 | 406 · 0,305 · 0,385 |
  | 10–20 | 341 · 0,316 · 0,336 | 345 · 0,316 · 0,392 |
  | 20–30 | 73 · 0,284 · 0,343 | 77 · 0,310 · 0,493 |

## 5 · K4 — yükle oynama (karar)

- İkizde 55 093 çift; 10 s'de iki katına değişen 279 (%0,5). **Hüküm: oynama küçük.**
- Sıra korelasyonu: log2 `E_veri` ile göndericinin yükü 0,031, alıcının yükü 0,299 (n 75 288).

## 6 · K5 — selamı geçen, veriyi taşımayan bağ (betimleyici)

| hücre | örnek payı | bağ payı | süre ortancası | kâhine göre iyi |
|---|---|---|---|---|
| ikiz | 0,0106 (n 75 288) | 0,129 (127/988) | 2,0 s | 1,000 |
| birincil | 0,0127 (n 48 674) | 0,137 (164/1 201) | 2,0 s | 1,000 |

Seyrek ve kısa: bağların yedide biri bu durumu en az bir kez gösteriyor, ortanca 2 s sürüyor; hepsi kâhine göre iyi bantta.

## 7 · K6 — karıştırma altında (betimleyici, birincil)

| alan | bağ-dönem | dönem içinde örneği olan | `E_veri` iki katına: 3 s içinde · dönem içinde | `E_selam` iki katına: 3 s içinde · dönem içinde |
|---|---|---|---|---|
| G | 590 | 0,810 | 0,192 · 0,427 | 0,000 · 0,007 |
| E | 60 | 0,650 | 0,083 · 0,400 | 0,000 · 0,017 |

Selam karıştırmaya neredeyse hiç tepki vermiyor. Veri, bağ-dönemlerin ~%40'ında dönem içinde iki katına çıkıyor; 3 s içinde %8–19.

## 8 · Hükümlerin tasarıma etkisi (beklentide önceden yazıldığı gibi)

- **K2 "değil":** seçenek 2'nin dayanağı tutmaz; çekirdeğin kararı `18` §2.3'te yeniden konuşulur, kâğıt yazılmaz.
- **K1 "dönüşüm yok":** selam kullanılırsa çevrilmeden kullanılır.
- **K3:** veri ölçüsü kullanılırsa `VERI_EN_AZ` 12, `VERI_TAZE_S` 30 s.
- **K4 "küçük":** düzgünleştirme gerekmez.
- **K5, K6:** betimleyici.

## 9 · Öngörülerle karşılaştırma

| # | öngörü | sonuç | |
|---|---|---|---|
| 1 | K0 birebir, iç denetimler geçer | birebir, geçti | tuttu |
| 2 | ortanca −0,3 … +1,0, en olası artı; çeyrekler arası ≥ 0,8 bit | +0,168 · +0,159; artı; 0,55–0,57 bit | tuttu · tuttu · tutmadı (daha dar) |
| 3 | veri üstün; OMH `E_veri` 0,3–0,7, Ês* 0,6–1,4 bit | üstün değil; 0,231; 0,305 | tutmadı · tutmadı (daha küçük) · tutmadı (çok daha küçük) |
| 4 | seçimde en olası D1; aktarılabilirlik farkı +0,5 … +1,5, en olası "aktarılamaz"; hüküm en olası "kullanılan bağlarda iyi, aktarılamaz" ya da "dönüşüm yok" | D0; +0,396, aktarılabilir; dönüşüm yok | tutmadı · tutmadı · tutmadı · tuttu (ikinci olası) |
| 5 | `VERI_EN_AZ` 2–4, doğrulanır; `VERI_TAZE_S` 10–30 s, en olası 30 | 12, doğrulandı; 30 | tutmadı · tuttu · tuttu |
| 6 | çiftlerin %2–10'u, en olası "küçük"; korelasyonlar 0,0–0,3 | %0,5, küçük; 0,031 · 0,299 | tutmadı (daha az) · tuttu · tuttu |
| 7 | örneklerin %0,5–5'i; bağların %3–20'si; süre 3–15 s; iyi ≥ 0,8 | %1,1–1,3; %12,9–13,7; 2,0 s; 1,000 | tuttu · tuttu · tutmadı (daha kısa) · tuttu |
| 8 | G: `E_veri` 3 s'de %25–60, `E_selam` ≤ %15; E: `E_veri` %25–60, `E_selam` ≤ %25 | G 0,192 · 0,000; E 0,083 · 0,000 | tutmadı · tuttu · tutmadı · tuttu |
| 9 | veri örneği 6 000–15 000, ızgara 15 000–35 000 | 10 943–11 426; 28 781–35 835 | tuttu · iki koşu sınırın hemen üstünde |

**Tutanlar:** ayrışmanın yönü, tazelik, yükle oynamanın küçüklüğü, selamı geçen ama veriyi taşımayan bağın seyrekliği.

**Tutmayanlar:**
- İki ölçünün hatasını çok büyük tahmin etmişim. Selam, kullanılan bağın sonraki bedelini öngördüğümden çok daha iyi kestiriyor; bu yüzden verinin üstünlüğü eşiğin altında kaldı.
- Verinin selamı geçmesi için gereken kayıt sayısı (12) beklediğimden büyük çıktı.
- Selamın kâhine göre kötümserliği kullanılan ve kullanılmayan bağlarda beklediğimden az ayrışıyor.
- Karıştırmada veri ölçüsünün 3 s içindeki tepkisi beklediğimden yavaş.

## 10 · Kuraldan sonra görülenler (karar girdisi değil; `ek_hesap.txt`)

**10.1 · Selam ölçüsünün dilimlerinde** (E1; kullanılan bağ, temiz sınıf, en az 8 önceki kayıt, iki yarı birlikte):

| `E_selam` | örnek | OMH `E_veri` | OMH `E_selam` | log2(F / `E_selam`) ortancası |
|---|---|---|---|---|
| 1,0–1,5 | 44 853 | 0,202 | 0,285 | +0,259 |
| 1,5–2,0 | 44 113 | 0,248 | 0,297 | +0,134 |
| 2,0–3,0 | 25 933 | 0,285 | 0,356 | +0,004 |
| 3,0–4,0 | 3 117 | 0,341 | 0,473 | −0,237 |
| ≥ 4,0 | 85 | 0,413 | 0,753 | −0,468 |

- Veri her dilimde selamdan iyi; fark kenar bağlarda büyüyor.
- Selam ölçeği sıkıştırıyor: iyi bağın bedelini ~%20 ucuz, kenar bağınkini ~%15–28 pahalı gösteriyor.

**10.2 · Önceki tasarımın selam eşiği** (E2; `E_selam` > 4 → KÖTÜ):
- Kullanılan bağ örneklerinin yalnız %0,07'si (81/118 101) eşiğin üstünde: çekirdek böyle bağları zaten ardıl seçmiyor. Onlarda F'nin ortancası 4,2; %32'sinde F ≤ 3.
- Izgarada eşiğin üstündeki bağ-dilimlerde kâhine göre iyi olanların payı: kullanılan bağlarda %99,4 (4 128), kullanılmayanlarda %44,8 (167 805).
- Eşik, iyi bağların büyük bölümünü dışarıda bırakırdı. Önceki tasarımdaki zararın kaynağı ölçünün kendisi değil, eşikti.

**10.3 · Ardıl ile yedek aynı terazide** (E3): kullanılan bağın maliyeti `E_veri`'den alınırsa, aynı düğümün kullanılmayan bağlarıyla sırası çiftlerin %9,65'inde (45 594/472 579) değişiyor. İki kaynağı karıştırmanın etkisi budur.

## 11 · Bundan çıkan

- **Veri biraz daha iyi, ama yeterince değil:** kullanılan bağın bedelini selamdan daha iyi kestiriyor (ortanca hata ~%17 ↔ ~%24). Fark önceden yazdığım pratik eşiğin altında; 12 kayıttan azıyla veri selamdan iyi değil.
- **Selam sanıldığından iyi.** Önceki tasarımdaki zarar ölçüden değil, eşikle düşürmeden geliyordu (§10.2).
- **Veri yükle oynamıyor;** selamı geçen ama veriyi taşımayan bağ seyrek ve kısa.
- **Karıştırmaya çekirdekte yalnız veri tepki veriyor, o da yavaş.** Hızlı yol B2'nin kanıtı.
- **K2'nin hükmüyle seçenek 2'nin dayanağı tutmadı;** çekirdeğin seçeneği yeniden konuşulur (`18` §2.3).
