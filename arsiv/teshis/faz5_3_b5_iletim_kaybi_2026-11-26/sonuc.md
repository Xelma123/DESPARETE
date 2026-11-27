# Faz 5-3 · B5 teşhisi — iletim kaybının yeri: karıştırılan alıcı, sıradaki aday ve kanıtın zamanı — sonuç

> 27 Kasım 2026 · ölçüt `beklenti.md` (öngörüler ve karar kuralı commit `cdb1a48`, dumandan önce; duman notu ve dumandan sonra eklenen betimleyici ölçü S6 commit `09ba063`).
> - **Koşu** (`zaman.txt`): 00:43–02:59, toplam 2 sa 16 dk (tahmin ~2–3 sa). Adımlar: ikiz 1 sa 0 dk · birincil 1 sa 16 dk.
> - **Kopya:** `kopya/` = `09ba063`, 166 dosya birebir (satır sonları normalleştirilerek; `kopya_ozet.txt`).
> - **Çıktılar:** ham çıktı `olcum_*.txt`, kayıt `kayit_*.json.gz`; karar kuralı `sonuc_hesap.py` → `sonuc_hesap.txt`; ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil; E4'ün düzeltmesi ve E7–E9 27 Kasım'da, ana seçenekten önce eklendi; E10 B5 kâğıdı için, karardan sonra).
>
> Paylar açık dönemde doğan paketlere oranladır (`PDR_açık`'ın birimi), sekiz tohumun ortalamasıdır. "Ağırlıklı" pay, sıradaki adaya gidilseydi geçme olasılığının kâhine göre üst sınırıdır.

## 0 · Geçerlilik ✓

- 16 koşunun hepsi kayıtta ve geçerli; kaydedicinin iç denetimleri 16 koşuda da geçti:
  - sayaçlar eşit;
  - her karar bir MAC sonucuyla eşleşti; her selamın kurulma kaydı var; çift düşüş yok;
  - kayıp, alan başına kayıp anatomisiyle aynı.
- Birebirlik: iki hücrede 8'er satır, yeni çekirdek ölçümünün `eğim0` satırlarıyla PDR, pencere PDR'si, üretilen, teslim, simülatör sayaçları ve protokol sayaçlarında aynı.
- Kaydedicinin iletim kaybı (0,2971) kayıp anatomisininkiyle aynı.

## 1 · K1 — kaybın yeri (karar)

| sınıf | anlamı | ham | ağırlıklı (anında) | ham (gerçekçi) | tohum başına ağırlıklı (1003 … 1010) |
|---|---|---|---|---|---|
| J1 | katmanın işi | 0,0489 | 0,0485 | 0,0447 | 0,094 · 0,013 · 0,049 · 0,026 · 0,029 · 0,011 · 0,075 · 0,091 |
| J2 | kanıt geç, k1 temiz | 0,0221 | 0,0220 | 0,0267 | 0,036 · 0,018 · 0,030 · 0,016 · 0,011 · 0,011 · 0,027 · 0,027 |
| J3 | k1 kirli | 0,0816 | 0,0360 | 0,0812 | 0,093 · 0,024 · 0,015 · 0,003 · 0,017 · 0,062 · 0,018 · 0,057 |
| J4 | tek aday | 0,0529 | — | 0,0529 | — |
| J5 | hedef karıştırılıyor | 0,0062 | — | 0,0062 | — |
| U1 | temiz alıcı, k1 temiz | 0,0428 | 0,0426 | 0,0428 | 0,023 · 0,067 · 0,055 · 0,076 · 0,028 · 0,023 · 0,023 · 0,044 |
| U2 | temiz alıcı, k1 yok ya da kirli | 0,0369 | 0,0105 | 0,0369 | 0,002 · 0,016 · 0,013 · 0,016 · 0,004 · 0,012 · 0,010 · 0,012 |
| komut | | 0,0055 | | | |
| toplam | | 0,2971 | | | |

**Elemeler** (ağırlıklı, anında biçim; eşik 0,02):
- **B:** J2 = 0,0220 → elenmez;
- **C:** J3 = 0,0360 → elenmez;
- **D:** J2 + J3 + U1 = 0,1005 → elenmez.

**Hüküm K1:** elenen aile yok; A, B, C ve D ana seçeneğin kararına girer.

**Hedefe yeter mi** (betimleyici): J1 + J2 + J3 (ağırlıklı) = 0,1065; gereken 0,048.

## 2 · K2 — zaman (betimleyici)

J1 + J2'de 2 046 kayıp:
- dönem başından gecikme ortancası 7,8 s (çeyrekler 4,2–11,2);
- alıcının alana girişinden 5,7 s (1,9–9,9);
- J1'de kanıtın başlangıcından 3,1 s (1,0–6,4).

Dönemin ilk 3 s'sinde olan pay %17,8.

## 3 · K3 — hızlı sapmanın tetiği

| aday | seçim: yakalama | seçim: temiz sapma | doğrulama: yakalama | doğrulama: temiz sapma | sapan temiz kararda k1'in bandı kötü (seçim) |
|---|---|---|---|---|---|
| DEN7x1 · W 1 s | %61,7 | %12,4 | %55,3 | %11,2 | %11,9 |
| DEN7x1 · W 3 s | %72,1 | %21,7 | %64,8 | %20,8 | %10,6 |
| VAZ1 · W 1 s | %57,3 | %8,6 | %52,1 | %7,5 | %12,9 |
| VAZ1 · W 3 s | %69,3 | %15,7 | %60,8 | %14,8 | %11,6 |
| DEN7x2 · W 1 s | %33,3 | %2,19 | %28,8 | %1,52 | %15,7 |
| DEN7x2 · W 3 s | %44,8 | %4,4 | %33,2 | %3,4 | %14,1 |

**Hüküm K3: tetik yok.** Seçim yarısında hiçbir adayın temiz sapması %2'nin altında değil; en yakını DEN7x2, W 1 s (%2,19).

## 4 · K4 — kopyanın bedeli (betimleyici)

| kural | ateşleme (birincil) | ateşleme (ikiz) | yayın eki: birincil · ikiz | kapsadığı kayıp (birincil, adet) |
|---|---|---|---|---|
| C1 | açık·E %57,2 · açık·G %27,2 · açık·U %3,8 · sessiz %3,0 · önce %1,6 | %1,60 | %21,7 · %5,8 | J1 1 409 · J3 1 668 · U1 208 · U2 91 |
| C2 | açık·E %3,0 · açık·G %4,3 · açık·U %0,2 · sessiz %0,4 · önce %0,02 | %0,01 | %3,8 · %0,04 | J3 452 · U1 1 · U2 12 |

## 5 · K5 — kurtarmanın kestirimi (betimleyici)

- Ağırlıklı hedef (K1'in D satırı): J2 0,0220 · J3 0,0360 · U1 0,0426; toplam 0,1005.
- Yayın eki:
  - birincil: 15 322 vazgeçme, %76'sının k1'i var, ek %11,0;
  - ikiz: 6 995 vazgeçme, %85'inin k1'i var, ek %4,9.

## 6 · K6 — uygulanabilirlik koşulunun ve ilanın ömrünün bedeli (betimleyici; dumandan sonra eklendi, öngörüsü yok)

Yalnız uygulanabilirlik yüzünden aday olmayan temiz bir komşu (yeni bir tur onu aday yapardı):

| sınıf | sınıfın payı | temiz engelli komşusu olan | ağırlıklı |
|---|---|---|---|
| J3 | 0,0816 | 0,0623 | 0,0622 |
| J4 | 0,0529 | 0,0455 | 0,0455 |
| U2 | 0,0369 | 0,0288 | 0,0288 |

Ardılın kanıtı, temiz kararlarda (bir karar birden çok sebep taşıyabilir):

| hücre · evre | karar | herhangi | ilan bayat | bildirim (gerçekçi · anında) | gönderici | veri yok |
|---|---|---|---|---|---|---|
| ikiz | 311 882 | %2,30 | %2,12 | %0,10 · %0,07 | %0,12 | %0,02 |
| birincil · önce | 142 693 | %2,16 | %2,00 | %0,06 · %0,06 | %0,11 | %0,02 |
| birincil · sessiz | 94 382 | %4,23 | %2,89 | %1,55 · %1,35 | %0,16 | %0,07 |
| birincil · açık·U | 63 737 | %5,49 | %4,13 | %0,53 · %0,91 | %0,61 | %0,36 |

## 7 · Öngörülerle karşılaştırma

| # | öngörü | sonuç | |
|---|---|---|---|
| 1 | K0 tutar; kayıp anatomiyle aynı | birebir, iç denetimler geçti | tuttu |
| 2 | anatominin alanıyla E 0,048 · G 0,168 · U 0,081 | 0,0479 · 0,1678 · 0,0814 (E1) | tuttu |
| 3 | J1–J5 0,19–0,216 · U1 + U2 0,081–0,11 | 0,2117 · 0,0797 | tuttu · hemen altında |
| 4 | J5 ≤ 0,01, en olası < 0,005 | 0,0062 | tuttu · en olası tutmadı |
| 5 | k1'in temiz payı %30–60 · J1 + J2 0,06–0,13 · J3 0,04–0,10 · J4 0,02–0,06 | %34 · 0,071 · 0,082 · 0,053 | tuttu |
| 6 | J1 0,02–0,07 · J2 (anında) 0,03–0,08 · gerçekçi fazlası 0,00–0,03 | 0,049 · 0,022 · 0,005 | tuttu · altında · tuttu |
| 7 | U1 0,04–0,07 · U2 0,015–0,04 | 0,043 · 0,037 | tuttu |
| 8 | ağırlıklı/ham: J2 > %90 · J3 %20–60 | %99,5 · %44 | tuttu |
| 9 | en olası B ve D elenmez; C belirsiz | üçü de elenmedi | tuttu |
| 10 | J1 + J2 + J3 (ağırlıklı) 0,06–0,20, en olası 0,048'i aşar | 0,1065 | tuttu |
| 11 | ilk 3 s'nin payı %20–40 · alana girişten ortanca 3–8 s | %17,8 · 5,7 s | altında · tuttu |
| 12 | DEN7x1 ve VAZ1 W 3 s'de sınırı aşar; en olası seçim DEN7x2 W 1 s, "tetik yok" ~%30 | aştılar; "tetik yok" | tuttu · tutmadı |
| 13 | C1 açık evrede %5–20 · C2 %1–6 · C1'in eki %1–8 · C2'ninki %0,3–2 · ikizde ikisi de < %1 | %9,0 · %1,0 · %21,7 · %3,8 · C1 %1,6, C2 %0,01 (E2, K4) | tuttu · hemen altında · üstünde · üstünde · C1 üstünde |
| 14 | kurtarmanın eki %2–6 | %11,0 | üstünde |
| 15 | karar 35 000–45 000 · kayıp 800–1 400 (koşu başına) | ortalama 38 985 · 39 534 ve 1 050; uçlar 33 410–47 617 ve 644–1 534 (E5) | ortalamada tuttu, uçlarda değil |

Tutmayanların gerekçesi:
- **Yayın ekini küçük görmüştüm** (13, 14). İki sebep var:
  - Kopya, eşin geçide kalan bütün yolunu taşır: bedeli `E_selam` + C(k1), ~3–5 gönderim.
  - Birincilde vazgeçme koşu başına ~1 900 (ikizde ~870); kurtarma her birinde bir gönderim ister.
- **J2'yi büyük görmüştüm** (6). Anında biçimde kanıt erken geliyor: J1'deki kayıp kanıttan ortanca 3,1 s sonra oluyor. Kanıtsız kalan kaybın büyüğü ise k1'i kirli (J3) ya da adaysız (J4) kayıplar.
- **Kaybın dönemin başına yığılacağını sanmıştım** (11). `eğim0` karıştırılan bağa dönem boyunca göndermeyi sürdürdüğü için kayıp döneme yayılıyor (ortanca 7,8 s).

## 8 · Kuraldan sonra görülenler (karar girdisi değil; `ek_hesap.txt`)

- **B sınırda:**
  - J2 0,0220; tohum başına 8 tohumun 4'ünde 0,02'yi geçiyor (E3).
  - Temiz sapma sınırını hiçbir tetik geçmiyor. En yakın aday DEN7x2, W 1 s: temiz sapması seçimde %2,19, doğrulamada %1,52; yakalaması %29–33. Bu adayla sapan temiz kararların %16'sında k1'in bandı ardılınkinden kötü.
- **C'nin kazancı bedeline göre küçük** (E2, E6):
  - C1, J1 dışındaki kaybın ağırlıklı 0,033'üne ulaşıyor. Ama birincilde koşu başına veri yayın süresine 81 s ekliyor (372 s'nin %22'si), ikizde 19 s.
  - C2 ucuz (14 s · 0,1 s) ama yalnız 0,004'e ulaşıyor.
  - Kalabalık kanalda toplam gönderim 100 s artınca alıcıların kilitlenmesi kabaca 2 puan düşüyordu (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5). Bu ilişkiyle C1'in eki bütün iletimlere ~1,6 puanlık bir kilitlenme kaybı olarak yansır (kaba kestirim).
- **D'nin kazancı büyük ama önemli bir kısmı genel** (E4, E6):
  - Vazgeçen kararlarda temiz k1'in p₇'si, penceredeki doğuma oranla ikizde 0,0525, birincilde (bütün evreler) 0,078. İkisi de üst sınırdır; onayı kaybolmuş ama alıcıya ulaşmış paketleri de içerir.
  - Düzeltme (27 Kasım): ilk hesap pencerenin dışındaki (0–50 s) kararları da sayıyordu, payda ise yalnız penceredeki doğumdu; 0,063 ve 0,089 vermişti. Sayılar pencere içindeki kararlarla yeniden hesaplandı (E4).
  - D karıştırmasız ağda da kazandırır, yani genel bir mekanizmadır (K-247). Fark-içinde-farka katkısı birincildeki fazlası kadardır, mekanizma kapısına girmez.
  - Yayın eki birincilde 41 s, ikizde 17 s.
- **J1 (katmanın kendi payı) 0,0485**, gereken 0,048 kadar bir üst sınır. Bu kayıplarda B2–B4'ün kanıtı ortanca 3,1 s önce gelmiş ve temiz bir olağan aday var. Yeni tasarımda bu paketler çoğunlukla temiz adaya giderdi; B3'ün 5 s'lik yeniden denemesi bir kısmını yine kaybettirirdi.
- **Uygulanabilirlik koşulunun bedeli büyük** (K6). J3, J4 ve U2'de yalnız FD yüzünden aday olmayan temiz bir komşu toplam 0,137 payda var (0,062 + 0,046 + 0,029).
  - B4 tur isteğini yalnız hiç aday kalmayınca gönderir (B4 kural 11). Ardıl son çaredeyken ya da sıradaki aday kirliyken göndermez.
  - Bu kayba B5'in aileleri ulaşamaz (J4) ya da kirli adayla ulaşır (J3); yeni bir tur temiz adayı açabilirdi. Bu, B4'ün sorusudur.
- **İlanın ömrü temiz kanalda da işliyor** (K6):
  - Ardılın ilanı ikizde kararların %2,1'inde bayat. Birincilin önce evresinde %2,0, sessiz evresinde %2,9, açık evrede alıcısı uzak olanlarda %4,1.
  - Yeni tasarımda bu kararlarda ardıl aday olmaktan çıkar (zorunlu geçiş).
  - Bu, `ILAN_OMUR_KAT`'ın (3,5 × a; `v2/bilesen/00-DIZIN.md`, "Aşama 4'te bakılır") girdisidir.

**Ana seçeneğin kararı için eklenen okumalar** (27 Kasım; kuraldan sonra, yalnız kayıtlardan; `ek_hesap.txt` E7–E9):
- **J1'in çoğu çekirdeğin kanıtıyla da görülüyor** (E7):
  - J1'in 0,0485'inin 0,0324'ünde karar anında çekirdeğin bir kanıtı da var: veri yok 0,0289, ilan bayat 0,0093 (ikisi örtüşebilir). Yalnız karıştırma katmanının kanıtıyla (bildirim, gönderici) görülen pay 0,0161.
  - Mekanizma kapısının kolunda (katman kapalı, genel mekanizmalar açık) çekirdeğin kanıtı kalır. Katmanın J1'deki kendi payı bu yüzden en çok 0,016'dır (üst sınır).
  - Genel bir kurtarma (D) bu kolda katmanın yakalayacağı kayıpları da kurtarır. Katmanın kapıdaki payını daha da küçültür.
- **K6'nın temiz engelli komşusu, ardılın durumuna göre** (E8; p₇ ile ağırlıklı):
  - "Ardılın kanıtı var, olağan aday yok" durumunda 0,0382 (J3 0,0116 · J4 0,0256 · U2 0,0010); bunun yalnız katman kanıtlı kısmı 0,0143. Bu durumda bir tur isteği tetiklenebilirdi: RFC 8966 §3.8.2.2'nin ikinci paragrafı, seçili olmayan bir komşudan seçili rotadan iyi ama uygulanamaz bir ilan gelince o komşuya tek alıcılı istek gönderilmesini ister (SHOULD). B4'te bu kural yok; Babel-a'da var (`protokoller/babel_bicim.py`, eşiği 512).
  - Açlıkta B4 kural 11'in zaten istediği pay 0,0072. Ardılın kanıtı varken olağan ama kirli bir adayın bulunduğu pay 0,0347. Ardılın kanıtı olmayan pay 0,0563.
- **İlanın bayatlığı temiz kanalda çoğunlukla yanlış alarm** (E9, pencere içi):
  - İkizde kararların %2,06'sında ardılın tek kanıtı ilanın bayatlığı. Bu kararlarda ardıla giden çerçevenin onayı %96,1 (kanıtsız kararlarda %97,9) ve ardılın bağı hep iyi bantta. Birincilin temiz kararlarında %90,2 ↔ %97,4.
  - Bu kararların %30,6'sında ardıldan başka aday yok. Yeni tasarımda ardıl bu kararlarda aday olmaktan çıkar; üçte birinde açlık ve tur isteği doğar.
  - Babel-a seçili rotanın süresi dolmadan ilan edene tek alıcılı istek gönderiyor (RFC 8966 §3.8.2.3, SHOULD; süresinin 7/8'inde). B4'te bu kural yok.
- **J4'ün çoğu girişimde** (E10; B5 kâğıdı için, karardan sonra eklendi): J4'ün 0,053'ünün 0,011'i kanal kilidindeki, 0,042'si girişimdeki alıcıda. J3'ün 0,016'sı kanal kilidinde, 0,066'sı girişimde.

## 9 · Bundan çıkan

- **Elenen aile yok.** A, B, C ve D ana seçeneğin kararına girer.
- **Ölçülen hedef ve bedel** (ağırlıklı üst sınır; yayın eki birincil · ikiz, koşu başına):

  | aile | hedef | bedel ve not |
  |---|---|---|
  | A · tek yol | — (temel) | karıştırmaya karşılık J1'den (0,0485) |
  | B · hızlı sapma | 0,022 (4/8 tohum ≥ 0,02) | tetik yok: en iyi aday temiz kararların %1,5–2,2'sini saptırır |
  | C1 · kopya | 0,033 (J1 dışında) | +81 s · +19 s |
  | C2 · kopya | 0,004 | +14 s · +0,1 s |
  | D · kurtarma | 0,100 (birincil); ikizde 0,0525 (genel) | +41 s · +17 s; simülatörün yetenek sözleşmesini (`13`) genişletir; mekanizma kapısının kolunda katmanın kayıplarını da kurtarır (E7) |

- **B4'e iki soru** (onaylı kâğıt):
  1. son çaredeki ardıl için tur isteği (K6: 0,137'lik üst sınır; ardılın kanıtı varken olağan aday yoksa 0,038, E8; RFC 8966 §3.8.2.2'nin ikinci paragrafı);
  2. ilanın ömrü (temiz kanalda kararların %2–4'ünde ardıl bayat, çoğu yanlış alarm, E9; RFC 8966 §3.8.2.3).
