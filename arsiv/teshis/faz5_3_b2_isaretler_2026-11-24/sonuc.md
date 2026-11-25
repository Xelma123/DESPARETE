# Faz 5-3 · B2 teşhisi — karıştırma işaretleri, bizim çekirdeğimizin trafiğinde — sonuç

> 25 Kasım 2026 · ölçüt `beklenti.md` (öngörüler ve karar kuralı commit `7add3e8`, koşudan ve dumandan önce; duman notu commit `e6b0bb6`).
> - **Koşu** (`zaman.txt`): 25 Kasım 00:21–05:19, toplam 4 sa 58 dk (tahmin 4,5–6,5 sa). Adımlar: ikiz 52 dk · birincil 72 dk · dayanıklılık 68 dk · cephe 107 dk.
> - **Kopya:** `kopya/` = `e6b0bb6`, 166 dosya birebir (`kopya_ozet.txt`).
> - **Çıktılar:** ham çıktı `olcum_*.txt`, kayıt `kayit_*.json`; karar kuralı `sonuc_hesap.py` → `sonuc_hesap.txt`.
> - **Ek sayılar:** `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil).

## 0 · Geçerlilik ✓

- 32 koşunun hepsi kayıtta ve geçerli; kaydedicinin iç denetimleri 32 koşuda da geçti.
- İkiz ve birincil satırları, döngü kuralları ölçümünün `geri_sinir` satırlarıyla 8/8 tohumda bütün alanlarda birebir. Kaydedici, kanal meşgul sayacını açmak dâhil, davranışı değiştirmedi.

## 1 · Betimleyici (bütün tohumlar)

| hücre | sınıf | düğüm-saniye | m | c (çerçeve/s) | s |
|---|---|---|---|---|---|
| ikiz | ikiz | 86 400 | 0,258 | 71,4 | 0,463 |
| birincil | önce · sessiz · uzak | 32 000 · 25 600 · 23 247 | 0,254 · 0,285 · 0,257 | 69,8 · 81,4 · 60,9 | 0,461 · 0,464 · 0,545 |
| birincil | G · E | 4 929 · 624 | 0,187 · 0,847 | 38,3 · 6,2 | 0,734 · 0,864 |
| dayanıklılık | G · E | 4 948 · 529 | 0,192 · 0,835 | 37,1 · 6,3 | 0,722 · 0,831 |
| cephe | G · E | 6 120 · 1 017 | 0,133 · 0,922 | 26,6 · 0,8 | 0,563 · 0,795 |

## 2 · K1 — kanal kilidi, kendi durumum (karar)

Seçim yarısında (θ · ikizde yanlış alarm · önce · E alanında erken yakalama · dönem içinde · gecikme ortancası):

| θ | ikiz | önce | erken | dönem içinde | gecikme |
|---|---|---|---|---|---|
| 0,50 | %0,354 | %0,206 | 0,463 | 0,951 | 4,0 s |
| **0,55** | **%0,037** | %0,025 | 0,463 | 0,927 | 3,5 s |
| 0,60 | %0,000 | %0,000 | 0,366 | 0,854 | 4,0 s |
| 0,62 | %0,000 | %0,000 | 0,341 | 0,780 | 4,0 s |
| 0,80 | %0,000 | %0,000 | 0,317 | 0,634 | 3,5 s |

- **Seçilen θ:** 0,55, ikizde yanlış alarmı ≤ %0,05 olan en küçük değer.
- **Doğrulama:** ikizde yanlış alarm %0,007; E alanında erken yakalama 0,463 (n 54); gecikme ortancası 3,5 s.

**Hüküm K1: kanal kilidi kuralı tutmaz** (erken yakalama 0,80'in altında). Sebebi kuraldan sonra ölçüldü (§8.1): değerlendirme biriminin tanımından geliyor.

## 3 · K2 — girişim, kendi durumum (karar)

- **Aday:** 288 kuralın 61'i seçim yarısında yanlış alarm sınırlarını geçti (ikizde ve önce evresinde ≤ %0,1, açık dönemde uzak alanda ≤ %1).
- **Seçilen:** **G(α 0,4 · β 0,6 · giriş 2 · çıkış 1)**. Anlamı: çözülen çerçeve kendi ortalamasının %40'ının altına düşer **ve** selam kaybı ≥ 0,6 olur, bu iki saniye üst üste sürerse "karıştırılıyorum"; bir saniye işaretsiz geçerse çıkış.
- **Seçim yarısında en iyi üç** (erken yakalama):
  - seçilen kural: 0,359;
  - G(0,4 · 0,5 · 3 · 1): 0,313;
  - G(0,5 · 0,7 · 2 · 1): 0,310.

| | yarı | ikiz | önce | sessiz | uzak | erken | dönem içinde | gecikme | kapsama | çıkış |
|---|---|---|---|---|---|---|---|---|---|---|
| seçilen · birincil | doğrulama | %0,002 | %0,006 | %0,094 | %0,498 | **0,344** (n 183) | 0,530 | 3,0 s | 0,321 | 1,0 s |
| seçilen · dayanıklılık | doğrulama | %0,002 | %0,006 | %0,017 | %1,508 | **0,347** (n 297) | 0,545 | 3,0 s | 0,342 | 1,0 s |
| önceki KK-03 · birincil | doğrulama | %0,030 | %0,062 | %2,172 | %3,244 | 0,410 | 0,661 | 3,0 s | 0,453 | 3,0 s |
| önceki KK-03 · dayanıklılık | doğrulama | %0,030 | %0,062 | %2,597 | %6,932 | 0,434 | 0,694 | 3,0 s | 0,499 | 3,0 s |

**Hüküm K2: girişim kuralı var.** Doğrulamada:
- ikizde yanlış alarm %0,002 (sınır %0,2);
- uzak alanda yanlış alarm, iki hücre birlikte, %2'nin altında;
- erken yakalama birincilde 0,344, dayanıklılıkta 0,347 (sınır 0,25).

Önceki KK-03 kuralı daha çok yakalıyor, ama açık dönemde uzak alandaki düğümlerin %3–7'sinde yanlış alarm veriyor; uzak alan sınırı onu eledi.

## 4 · K3 · K4 — göndericinin bağ kanıtı (karar)

Seçim yarısında, veri taşıyan bağlarda (ikizde ve önce evresinde yanlış alarm 1000 çerçevede · erken yakalama E · G):

| kural | ikiz ‰ | önce ‰ | erken E (n 44) | erken G (n 548) |
|---|---|---|---|---|
| VAZ1 | 13,60 | 14,32 | 0,409 | 0,370 |
| VAZ3 | 0,30 | 0,27 | 0,205 | 0,141 |
| DEN4x1 | 92,42 | 95,79 | 0,545 | 0,467 |
| DEN6x2 | 4,05 | 4,29 | 0,250 | 0,286 |
| DEN6x3 | 0,93 | 1,03 | 0,227 | 0,192 |
| DEN7x3 | 0,51 | 0,51 | 0,205 | 0,159 |
| BIR6_15x2 | 0,68 | 0,79 | 0,068 | 0,084 |
| SES3 | 21,43 | 21,32 | 0,000 | 0,069 |

Yanlış alarm sınırını (≤ binde 1, ikiz ve önce) geçen yalnız üç kural var: VAZ3, DEN7x3, BIR6_15x2.

- **K3 · E alanındaki alıcı:** seçilen VAZ3, art arda 3 vazgeçme.
  - Doğrulama: ikizde binde 0,17; erken yakalama birincilde 0,348, dayanıklılıkta 0,268.
  - Yaprak benzeri bağlarda 0,277, röle bağlarında 0,353.
  - **Hüküm: göndericide tanınmaz** (sınır 0,50).
- **K4 · G alanındaki alıcı:** seçilen DEN7x3, art arda 3 çerçeve, her biri 7 deneme.
  - Doğrulama: ikizde binde 0,40; erken yakalama birincilde 0,184, dayanıklılıkta 0,213.
  - **Hüküm: göndericide tanınmaz** (sınır 0,30).

## 5 · K5 · K6 · K7

- **K5 · kalabalık:** seçilen kuralın ikizdeki yanlış alarmı 86 400 düğüm-saniyenin 2'si, ikisi de en az yüklü üçte birde. **Hüküm: yük koruması gerekmez.**
- **K6 · bitin ulaşması:** G alanındaki düğümün açık dönemdeki selamlarından tanıdık komşulara ulaşan pay:

  | hücre | uzak alıcı | G alıcı | E alıcı |
  |---|---|---|---|
  | birincil | 0,346 | 0,268 | 0,166 |
  | dayanıklılık | 0,345 | 0,251 | 0,093 |
  | cephe | 0,420 | 0,283 | 0,000 |
- **K7 · genelleme** (cephe hattı ↔ birincil, bütün tohumlar):
  - **Kanal kilidi kuralı:** cephede önce evresinde yanlış alarm %0,013; erken yakalama 1,000 (n 4) ↔ birincilde 0,465. Düşmüyor.
  - **Girişim kuralı:** cephede önce evresinde %0,003; erken yakalama 0,133 (n 45) ↔ birincilde 0,341. **Genellemede düşüyor.**
  - **Bağ, E alanı (VAZ3):** cephede 0,600 (n 5) ↔ birincilde 0,256. Düşmüyor.
  - **Bağ, G alanı (DEN7x3):** cephede 0,046 ↔ birincilde 0,171. **Genellemede düşüyor.**

## 6 · Hükümlerin tasarıma etkisi (beklentide önceden yazıldığı gibi)

- **K2 "var":** A, seçilen kuralla; B2'nin kâğıdı bu kuralla yazılır.
- **K1 "tutmaz":** kural kanal kilidi için başka işaret aranmasını söylüyor. §8.1 bu hükmün değerlendirme biriminden geldiğini gösteriyor; iki okuma arasındaki karar B2'nin kâğıdında verilir.
- **K3, K4 "tanınmaz":** göndericinin kanıtı yalnız geç gelen işaretlerle kalır, bitin önemi artar.
- **K5 "gerekmez":** girişim kuralına yük koşulu eklenmez.
- **K7 "düşüyor"** (girişim ve G alanındaki bağ): eşikler cephe hattıyla birlikte yeniden düşünülür ya da B2'nin kâğıdında kapsam sınırı olarak yazılır. §8.6 cephe hattında G alanının titrediğini gösteriyor.

## 7 · Öngörülerle karşılaştırma

| # | öngörü | sonuç | |
|---|---|---|---|
| 1 | K0 birebir, iç denetimler geçer | birebir, geçti | tuttu |
| 2 | θ 0,50–0,62 · doğrulamada ikizde ≤ %0,05 · E'de erken 0,85–1,00 · gecikme 1,0–1,5 s · K1 "tutar" | 0,55 · %0,007 · 0,463 · 3,5 s · "tutmaz" | tuttu · tuttu · tutmadı · tutmadı · tutmadı |
| 3 | ikizde s 0,30–0,50 | 0,463 | tuttu |
| 4 | önceki KK-03 kuralı ikizde %0,1–%1 | %0,030 | tutmadı (daha düşük) |
| 5 | sınırları geçen ≥ 20 kural | 61 | tuttu |
| 6 | seçilenin girişi 2 ya da 3 s | 2 | tuttu |
| 7 | doğrulamada erken birincilde 0,25–0,55 · dayanıklılıkta 0,20–0,50 · dönem içinde 0,50–0,85 · gecikme 2–4 s · çıkış 2–5 s · kapsama 0,30–0,65 | 0,344 · 0,347 · 0,53–0,55 · 3,0 s · 1,0 s · 0,32–0,34 | tuttu (çıkış dışında; seçilen kuralın çıkışı 1 s) |
| 8 | K2 en olası "var" | var | tuttu |
| 9 | ikizde DEN6x1 binde 20–60 · DEN6x2 1–5 · DEN6x3 0,1–1 | 35,0 · 4,05 · 0,93 | tuttu |
| 10 | VAZ3 ikizde < binde 0,5, erken 0,10–0,35 · SES3 erken ≤ 0,15 | 0,30 · 0,21–0,35 · 0,000 | tuttu |
| 11 | seçilen DEN6x3, DEN7x2 ya da BIR6_15x2 türü · erken 0,40–0,75 · rölede yapraktan yüksek | VAZ3 · 0,27–0,35 · 0,353 ↔ 0,277 | tutmadı · tutmadı · tuttu |
| 12 | K3 belirsiz | tanınmaz | (yön verilmemişti) |
| 13 | K4: erken 0,10–0,35, en olası "tanınmaz" | 0,18–0,21, tanınmaz | tuttu |
| 14 | yanlış alarmların yarısından çoğu en yüklü üçte birde · K5 "gerekmez" | 2 yanlış alarm saniyesi, ikisi de en az yüklü üçte birde · gerekmez | tutmadı · tuttu |
| 15 | bitin uzak komşulara ulaşan payı 0,50–0,85 · G'ye 0,10–0,40 · E'ye ≤ 0,10 | 0,35–0,42 · 0,25–0,28 · 0,17 · 0,09 · 0 | tutmadı · tuttu · birincilde tutmadı |
| 16 | kanal kilidi cephede tutar · girişim kuralı cephede birincilinkinin 0,5–1,0 katı · sürekli yayında çıkılmayan pay yüksek | 1,000 (n 4) · 0,39 katı · girişim kuralında çıkılmayan 0 | tuttu · tutmadı · tutmadı |

**Tutanlar:** girişim kuralının düzeyleri, bağ kurallarının yanlış alarmları ve gecikmeleri öngörüldüğü gibi çıktı.

**Tutmayanlar:**
- kanal kilidinin yakalama gecikmesi (sebebi §8.1);
- bitin uzak komşulara ulaşması (daha düşük);
- girişim kuralının cephe hattında düşmesi.

## 8 · Kuraldan sonra görülenler (karar girdisi değil; `ek_hesap.txt`)

**8.1 · Kanal kilidinin geç yakalanması, alanın dönem içinde değişmesinden.**
- **Mekanizma:** yer–hava kanalında görüş hattı, karıştırıcının yakınındaki "engel noktası"nın düştüğü bina hücresinden (~11,5 m) belirleniyor (`sim2/kanal/yer_hava.py`; DD-01, K-242). İHA alçalıp yükselince engel noktası kayıyor; hücre değişince ek kayıp 21 dB ile 0,1 dB arasında atlıyor.
- **Örnek** (birincil, tohum 1003, düğüm 32, 180–195 s dönemi): karıştırıcı 180,0 s'den beri yerinde; İHA saniyede ~4 m alçalıyor. Engel noktası 183,2 s'de yeni hücreye geçiyor ve görüş hattı açılıyor. Düğümdeki karıştırıcı gücü −88,7'den −67,7 dBm'e çıkıyor; düğüm girişimden kanal kilidine geçiyor, kanal meşgul payı 0,33'ten 0,94'e.
- **Ne kadar yaygın** (E6): birincilde ve dayanıklılıkta, dönemin ortasında E alanında olan düğümler dönemin ortanca %60'ında E alanında; yalnız %21'i bütün dönem boyunca. Açık dönemde ardışık iki saniye arasında bir düğümün alanının değişmesi %3,3–3,4; cephe hattında %7,8.
- **Alana girişten gecikme** (E7): kanal kilidi kuralı, düğüm E alanına ilk girdiği saniyeden itibaren sayınca:
  - birincilde %95'ini, dayanıklılıkta %90'ını 3 s içinde yakalıyor, gecikme ortancası 1,0 s;
  - cephe hattında 4/4.

  Kural, teşhis (d)'deki gibi düğümü kanal kilidine girdiği saniyede tanıyor.
- **Ölçü neden ayrıştı:** K1'in birimi (alan dönemin ortasında, gecikme dönem başından) bu modelde düğümün kanal kilidine girmesini bekleme süresini de gecikmeye katıyor.
- **Tavan** (E8; 25 Kasım, kanal kilidi kararından sonra eklendi): K1'in birimiyle bir kuralın ulaşabileceği en yüksek erken yakalama, alana ilk girişi dönem başından 3 s içinde karara izin veren birimlerin payıdır. Doğrulamada (birincil ve dayanıklılık birlikte) tavan 0,463 (25/54), kanal kilidi kuralı 0,463 (25/54); seçimde 0,439 ve 0,463 (kural bir birimi geçiş saniyesinde, alan etiketinden önce yakaladı). K1'in 0,80 sınırına bu birimle hiçbir kanal kilidi kuralı ulaşamazdı.
- **Aynı etki öteki birimlerde:** K2–K4 de dönem başından ölçüldü. G alanında küçük, çünkü birimlerin %74–79'u bütün dönem G alanında. Girişim kuralının girişten itibaren 3 s içinde yakalaması 0,375–0,392 (dönem başından 0,341–0,359). Bağ birimlerinde alıcının kimliği kayda girmediği için girişe göre yeniden hesaplanamadı.

**8.2 · Kendi durumumun birleşimi** (E2), kanal kilidi VEYA girişim kuralı:
- **E alanında:** erken yakalama 0,56–0,61; yalnız kanal kilidi 0,46, yalnız girişim 0,40–0,49.
- **G alanında:** 0,36–0,39; yalnız girişim 0,34–0,36.
- Girişim kuralı E alanındaki düğümleri de yakalıyor (orada da çözülen çerçeve düşüyor, selamlar gelmiyor).

**8.3 · Girişim kuralının işaretleri** (E3):
- **Birincil ve dayanıklılık, G alanı, dönemin ilk saniyesi:** s 0,57–0,59; çözülen çerçeve dönemden önceki düzeyinin 0,44–0,52'si.
- **Sonra:** s 3 s'de 0,78–0,80'e çıkıyor. Çözülen çerçeve hemen düşüyor; gecikmenin büyüğü selam kaybından geliyor (selam kaybı birkaç selamlık pencerede birikiyor).

**8.4 · Önceki KK-03 kuralı:** ikizde yanlış alarmı %0,030, seçilenin 15 katı. Açık dönemde uzak alanda %3,2–6,9, sessiz dönemde %1,8–2,6. Seçilen kural uzak alanda %0,5–1,5, sessiz dönemde %0,02–0,23.

**8.5 · Göndericinin birleşik kuralı** (E4), VAZ3 veya DEN7x3:
- ikizde yanlış alarm ≤ binde 0,69;
- erken yakalama E alanında 0,26, G alanında 0,17–0,20.

Tek başına kurallardan belirgin iyi değil.

**8.6 · Cephe hattında G alanı titriyor** (E6): dönemin ortasında G alanında olan düğümler dönemin yalnız ortanca %17'sinde G alanında. İşaretler de zayıf: s 0,48–0,63, çözülen çerçeve önceki düzeyinin 0,60–0,87'si. Girişim kuralının cephe hattındaki düşüşü (K7) bununla birlikte okunur: üç sabit yer karıştırıcısının çevresinde birçok düğüm alan sınırında ve görüş hattıyla girişim ile uzak arasında gidip geliyor.

**8.7 · Bitin ulaşması** (E5): bir selamın uzak bir komşuya ulaşma payı 0,35 (cephede 0,42). Selamlar bağımsız sayılırsa bir uzak komşuya 3 selamdan en az birinin ulaşma olasılığı ~0,72, 5 selamdan ~0,88. Bu bir kestirimdir; selam başına zamanlama kayda girmediği için ölçülmedi.

## 9 · Bundan çıkan (B2'nin kâğıdına girdi)

- **Girişim kuralı var:** G(α 0,4 · β 0,6 · giriş 2 s · çıkış 1 s).
  - Yanlış alarmı ikizde %0,002, açık dönemde uzak alanda %0,5–1,5.
  - Karıştırılan düğümlerin üçte birini 3 s içinde, yarısından fazlasını dönem içinde yakalıyor.
  - Bit için kullanılabilir.
- **Kanal kilidi:** K1'in hükmü "tutmaz". Kuraldan sonra görülen, kuralın (m ≥ 0,55) düğümü kanal kilidine girdiği saniyede tanıdığı (§8.1). Hangisine dayanılacağı B2'nin kâğıdında karara bağlanır. → 25 Kasım kararım: kural alındı; dayanağı §8.1 (E7, E8) ve teşhis (d), sonuçtan sonra diye `v2/06` §10'a yazıldı (`v2/18` §2.2, `v2/bilesen/B2-KARISTIRMA-KANITI.md` §15).
- **Göndericinin kanıtı yavaş:** hiçbir bağ kuralı 3 s içinde E alanının yarısını, G alanının üçte birini yakalamıyor. En iyileri art arda vazgeçme ve tam deneme dizileri; yanlış alarmları düşük ama geç. Karıştırılan bağın hızlı kanıtı alıcının bitidir.
- **Karıştırmanın düğümdeki etkisi aynı açık dönem içinde açılıp kapanabiliyor** (yer–hava görüş hattı). B2'nin girişi ve çıkışı hızlı olmalı; seçilen kuralın 1 s'lik çıkışı buna uygun.
- **Bitin selam başına ulaşma payı düşük** (0,35). Bitin değişince hemen bir selamla gitmesi ve birkaç selam boyunca tekrarlanması B6'dan beklenir.
- **Yük koruması gerekmiyor** (seçilen kural için).
- **Genelleme:** girişim kuralı ve G alanındaki bağ kuralı cephe hattında düşüyor; orada G alanı titriyor (§8.6). Kapsam sınırı olarak yazılır.
