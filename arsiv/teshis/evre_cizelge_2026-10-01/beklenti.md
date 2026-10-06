# Evre metrikleri v2 · kapılar G1ç · G2ç · G4ç — beklenti ve karar kuralları (ölçmeden önce)

> 30 Eylül 2026 gece · ajan · tanım `v2/08` §08 (K-209; öğrenci onayı K-207) · kod `sim2/olcum/evre.py` (`cizelge`), testler `tests2/test_evre.py` (`test_K209_*`, 32 geçti).
> Komutlar (U1 bittikten sonra, dondurulmuş kopyadan, sırayla, yanında ağır iş yok):
> `py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c` (~1,3 sa, 8 koşu) · `py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 2c` (~1,5 sa, 10 koşu)
> Tohumlar 1003 · 1004 (geliştirme; K-200 partisinin tohumları).

## Kurallar

- **G1ç · boş kol, hayalet çizelge** (formasyon · yere toplama · karıştırıcısız; çizelge `tehdit_acik_s`/`tehdit_sessiz_s` = 15 · 15; AODV · OLSR · AOMDV · DESPARETE × 2):
  - M4 yanlış tespit (ilk açık dönem) ≤ 1/8
  - M1 kol ortalaması 2 SE dışında ≤ 1/4 protokol
  - `D = PDR(sessiz) − PDR(TEMİZ)` iki tohumda da 2 SE dışında kalan protokol yok. Kalan protokolün birincil hücredeki M2'si "yorumlanamaz (ÖNCE referansı durağan değil)" diye yazılır; düzeltilmiş sayı üretilmez.
- **D'nin hata payı:** K-196'nın kuralı, gerçek pencere uzunluğuyla: `max(Agresti–Caffo, s_L · √(L/T_s + L/T))`.
  - `T_s` sessiz dönemlerin toplamı (80 s), `T` TEMİZ (100 s).
  - M1'in `√(1 + L/T)`'si tek bir `L` penceresi içindir (`L/L = 1`); D'nin penceresi `T_s`.
  - Yeni serbest sayı yok.
- **G2ç · kâhin, birincil hücre:**
  - M1 kol ortalamasında 2 SE dışında, yani karıştırıcı etkili
  - D 2 SE içinde: grafiği açık/sessiz geçişinde yenilenen kâhin sessizde anında temiz olmalı. Kalırsa evre bölümlemesinde hata aranır.
- **G4ç · her kol, birincil hücre:**
  - `p99 < açık süre` (`bulaniklik_orani_evre < 1`) → M1 ve M2 geçerli
  - `p99 ≥ 1 s` olan kolun 1 s profili "bulanık" etiketiyle çizilir
  - evre sızıntısı raporlanır

## Ölçmeden önce bilinen

K-200 partisinden (eski kod, `evre_mevcut_veri.py`): sessiz/önce oranı kâhin 0,985 (0,96–1,04) · OLSR 1,096 (en çok 1,26). OLSR'ın G1ç'de D'den kalma olasılığı var; kalırsa kural yukarıda.

## Sonuç (2 Ekim 02:26 – 06:31; `g1c.txt`, `g2c.txt`)

**G1ç: GEÇTİ.**
- M4 yanlış tespit 0/8.
- M1 2 SE dışında 1/4 (DESPARETE +0,056, 2 SE 0,051).
- D iki tohumda birden dışarıda kalan protokol yok. Tek tohumda dışarıda: AODV 1004 +0,037, 2 SE 0,032.
- OLSR'ın D'si −0,004 · −0,090 (2 SE 0,115 · 0,182): ÖNCE referansı bu hareketlilikte durağan.

**G4ç: GEÇTİ** (p99 < 15 s hepsinde). p99 ≥ 1 s olan kollar: kâhin, AODV, OLSR, AOMDV, DESPARETE (0,28–4,7 s). 1 s profili hepsinde "bulanık" etiketiyle.

**G2ç: KALDI.**
- Kâhinde M1 ort +0,214 (2 SE 0,036): karıştırıcı etkili ✅.
- Kâhinde D: 1003 −0,030 (2 SE 0,041, içeride) · 1004 −0,035 (2 SE 0,012, **dışarıda**). Sessiz 0,915 / önce 0,950.

**Kural gereği** "evre bölümlemesinde hata aranır".
- Bölümleme sentetik testlerle ve karıştırıcının `devrede_mi`siyle tutarlılık testiyle sınanıyor (`test_K209_*`).
- Teşhis `g2c_teshis.py` (tohum 1004, kâhin, birincil ve boş kol, çevrim başına ve katlanmış profil): sessizin başında geçici çukur mu (kuyruk birikimi), bütün sessizde düz kayma mı.

## Sonuç 2 — G2ç teşhisi (`g2c_teshis_birincil.txt`, `g2c_teshis_bos.txt`, kâhin, tohum 1004)

| | önce | açık | sessiz | M2 |
|---|---|---|---|---|
| boş kol (hayalet çizelge) | 0,950 | 0,902 | **0,900** | 0,947 |
| birincil hücre | 0,950 | 0,803 | **0,915** | 0,963 |

**Bölümleme hatası YOK.**
- Karıştırıcısız kolda da kâhinin PDR'si 150 s'den sonra ~0,90'a iniyor (hayalet ilk açık dönem 0,80, hayalet M1 0,150). Bu tohumda formasyonun topolojisi zamanla kötüleşiyor.
- Birincil hücrenin sessiz dönemleri boş kolun aynı dönemlerinden yüksek (0,915 > 0,900): kâhin karıştırıcı susunca toparlanıyor. D'nin −0,035'i zaman kaymasıdır.

**Kapının öncülü yanlış kurulmuştu:** "kâhinin ÖNCE düzeyi durağan". G1ç bunu yalnız protokoller için sınıyordu; protokollerde durağan çıktı. Kâhinde (PDR ~0,95, topolojiye en duyarlı) durağan değil.

**Öneri (öğrenci onayına):** G2ç'nin D maddesi kâhinin AYNI tohumdaki boş kol koşusuna göre eşleştirilir: `D_birincil − D_boş` 2 SE içinde. 1004'te +0,015. 1003 için boş kol koşusu gerekir (~50 dk).

**Yan bulgu:** tohum başına M1 bu tür topoloji olaylarıyla karışabilir (1004'te hayalet M1 0,150, birincil M1 0,072). `08` §06'nın "tohum başına şok derinliği tek başına okunmaz, kol düzeyinde SE'siyle" kuralı burada açıkça görünüyor.
