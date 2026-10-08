# Bağımsız Denetim Raporu — Faz 4 kapanışı, Faz 5'e geçiş kapısı

> **Tarih:** 8 Ekim 2026 (19:49–20:26) · **Denetçi:** yapay zekâ ajanı (Claude), `DENETIM-PROMPT.md` istemiyle, sıfır bağlamla
> **Denetlenen hâl:** `main` @ `f148b0fd4dba79b005da75917fc30f1bbe50c096` **+ işlenmemiş 27 değişik dosya** (K-220/K-221: `iletim_menzili_m → nominal_bag_m`, üç kova kararı, belgeler) **+ izlenmeyen `arsiv/teshis/regresyon_k220/`**. İstem "önce depoyu commit et" diyordu; commit yapılmamış. Bu rapor çalışma ağacının bugünkü hâlini denetler (k220 tabanını üreten kod budur — §2.2 E6).
> **Tek yazılan dosya bu rapordur.** Başlangıç ve bitişteki `git rev-parse HEAD` + `git status --short` ve 4 454 dosyanın SHA-256 manifesti §2.4'te.
> Önem: 🔴 KRİTİK · 🟠 ÖNEMLİ · 🟡 KÜÇÜK · ⚪ ÖNERİ. Bulgu numaraları `D-xx` (karar günlüğünün `K-xxx`leriyle karışmasın).

---

## 1 · Özet hüküm

**Altyapı sağlam, ölçüm kültürü güçlü; ama projenin ana iddiasını sınayacak test bugünkü hâliyle o iddiayı sınamıyor.**

Simülatör ve aletler bu denetimde tutarlı çıktı: tam test takımı **976/976** geçti; mimari denetimi ihlalsiz; regresyon tabanı `k220`'nin yedi vakası (dört protokol, kâhin, iki dünya) ayrı bir süreçte **bit bit aynı** yeniden üretildi; protokoller yalnız gözlem katmanını içe aktarıyor; istatistik kodu (Wilcoxon'un NaN tuzağı, Holm) doğru; OLSR'ın histerezis/MPR/§10 kuralları RFC metniyle örnek denetimde uyuşuyor. Karar günlüğü ve beklenti dosyaları sayesinde neredeyse her sayının üreticisi bulunabiliyor — bu bir lise projesi için olağanüstü.

Faz 5'e geçmeden önce düzelmesi ya da karara bağlanması gerekenler (öncelik sırasıyla):

1. 🔴 **D-01 — Birincil test (H2) karıştırmaya özgü kazancı ayırt etmiyor.** Birincil metrik "ölçüm penceresi PDR'si" ve 270 s'lik pencerenin yalnız **90 s'si (%33)** karıştırıcı açık. DESPARETE v0.4.1'in AODV'ye üstünlüğü **karıştırıcısız kollarda zaten var** (formasyon-yok +0,08…+0,13) ve birincil hücrede **karıştırıcı kapalıyken açıkken olduğundan büyük** (temiz +0,147 · sessiz +0,187 · **açık +0,101**); AODV ile DESPARETE açılmada aynı oranda (~%28) düşüyor. Bugünkü tasarım "DESPARETE üstün" hükmünü karıştırmayla hiç ilgisi olmayan bir sebepten (hedef-yönlü toplama ağacı) verebilir. Birincil kontrast ve Aile 3 kapısı Faz 5 başlamadan öğrenci kararıyla yeniden tanımlanmalı.
2. 🟠 **D-02 — OLSR hiç kural kural sadakat denetiminden geçmedi** (AODV geçti ve 11 sapma çıktı, K-208). OLSR en zayıf taban (yere toplamada 12 hücrenin 10'u eşik altı; karıştırıcısız **statik** ağda kâhinin %62–85'i; statikte TTL döngüsü), düşük hücreleri öğrenci istisnasıyla "açıklanmış" sayıldı ve bilinen bir okuma farkı (§8.2.1) beyan listesinde yok. H2.b'nin rakibi zayıf olabilir.
3. 🟠 **D-03 — R = 0,0142 ve 10 DUYARSIZ hükmünün tamamı 50 s'lik soğuk-başlangıç kesitinde ölçüldü** (ölçüm 30 s, karıştırıcı 5. saniyede); ana deneyin penceresi 270 s. "Birincil testin çözünürlüğü" etiketi yanlış; ana pencerenin gürültüsü daha küçükse bazı DUYARSIZ'lar R'yi aşabilir.
4. 🟠 **D-04 — `olculen_gurultu_w` anlık, hatasız, sürekli değerli** (karıştırıcı dâhil). RSSI'ye σ 2 dB ve tamsayı dBm verilmişken buna hiçbir ölçüm modeli yok. Faz 5.1 (C_jam) bu alanı kullanacak; kullanmadan önce gerçek bir sürücünün raporuna indirgenmeli.
5. 🟠 **D-05 — "Ölçüt ölçmeden önce yazıldı" iddiasının dış kanıtı yok.** Depoda 9 commit var; beklenti ve sonuç dosyaları çoğu kez aynı commit'te; beklenti dosyalarına sonuç ekleniyor; GitHub'a son push 24 Eylül (7 commit + işlenmemiş K-220/221 yalnız bu makinede). Mühürden önce süreç değişmeli.
6. 🟠 **D-06 — `06` §4.4 "bağlayıcı" metni uygulanan U1-B kuralıyla çelişiyor** (K-196, K-207 sonradan değiştirdi) ve sonuçtan sonra değişen beş ölçüt `06` §10 kayıt tablosunda yok.
7. 🟠 **D-07 — Köken defterinde "TÜRETİLMİŞ" serbest oranları saklıyor:** birincil hücrenin manevra gürültüsü `gm_hiz_sigma_ms` = "azami hızın %10'u" hiç taranmadı. SINANMAMIŞ 3 sayımı eksik.
8. 🟠 **D-08 / D-09 — Faz 5 planı tek çizelgeye (15/15 s) ve 8 tohuma ayar riskine açık; 5.2 birincil hücrede kazanç gösteremez** (formasyonda bağ hareketle kopmuyor); hesap bütçesi (`v2/12` §3) yalnız birincil hücrenin 200 koşusunu sayıyor.
9. 🟡 Bayat belgeler ve küçük kusurlar (D-10…D-22): MAC'te 8 deneme (kaynak 7) · regresyon referans dünyada evre metriklerini hiç sınamıyor · mimari D8/D9 eski dünyada · `protokol_hash` paket düzeyinde · 684 kod kopyası git'te · kırık üretici `li_beacon.py` · DEVIR/04/07/09/13/14/README'de bayat sayılar.

**Faz 5'e hazır mı?** *Koşullu hayır.* Simülatör ve aletler Faz 5'i taşır; ama Faz 5'in ne için geliştirileceğini belirleyen ölçüt (D-01) ve DESPARETE'nin kullanacağı gözlemin gerçekçiliği (D-04) karara bağlanmadan mekanizma geliştirmek, sonunda yanlış soruyu cevaplayan bir protokol üretme riski taşır. D-01 ve D-04 öğrenci kararı + küçük kod işi; D-05/D-06 belge ve süreç işi; D-02 bir sadakat denetimi (yaklaşık AODV'ninki kadar, K-208). Bunlar 2–4 günlük iş; sonra Faz 5.0 güvenle başlar.

---

## 2 · Yöntem

### 2.1 · Okunanlar

`DEVIR-PROMPT.md` · `DENETIM-PROMPT.md` · `README.md` · `v2/01, 03, 04, 05, 06, 07, 08, 09 (kısmen), 12, 13, 14, README` · `v2/kayit/KARAR-GUNLUGU.md` (K-191…K-221 tam, indeks) · çalışma ağacının `git diff`i (K-220) · `arsiv/teshis/` içinden `faz5_0_2026-09-30/beklenti.md`, `regresyon_k220/*`, `birincil_2026-09-28/ozet.txt`, `olsr_referans_2026-09-28/sonuc_1.md`, `faz4_5_2026-10-08/beklenti.md`, `faz4_4_birincil_2026-10-02/{taramalar.sh, sonumleme_yakinsama.txt}`, `faz4_4_k215_2026-10-06/{cozunurluk.txt, beklenti.md}` · önceki denetim raporunun özeti (`arsiv/denetim/DENETIM-RAPORU-2026-09-25.md`).

Kod: `sim2/cekirdek/kimlik.py` (tam) · `sim2/kosum/sonuc.py` (kimlik, yazıcı) · `sim2/kanal/dunya.py` (tam) · `sim2/mac/dcf.py` (deneme mantığı) · `sim2/kosum/dugum.py` (gözlem kuruluşu) · `sim2/kanal/girisim.py` · `sim2/kanal/karistirici.py::devrede_mi` · `sim2/dunya/mobilite.py` (formasyon) · `sim2/gozlem/pencere.py` (alanlar) · `sim2/yapilandirma/kokenler.py` (başlık, kovalar, DUYARSIZ/ÖLÇÜLMÜŞ/SINANMAMIŞ kayıtlarının hepsi) · `protokoller/olsr.py` (histerezis, MPR, §10, HELLO/TC işleme) · `olsr_bicim.py` (beyan tablosu) · `aodv_bicim.py` (TTL) · `desparete.py` (başlık, kimlik) · `desparete_bayrak.py` · `kalibrasyon/{kahin.py (başlık, sabitler), cozunurluk.py (tam), duyarlilik.py (başlık, karar ve koşucu), aodv_uygunluk.py (hüküm), regresyon_satirlari.py (matris, karşılaştırma), kayip_anatomisi.py (başlık, bant), mimari_denetimi.py (yapı), uretici_duman.py (başlık)}` · `analiz/istatistik.py` (tam) · `tests2/test_duyarlilik.py` · RFC 3626 §8.2.1, §14.3 ham metni · ns-3 `wifi-mac.cc`, `wifi-remote-station-manager.cc` (deneme sınırı).

### 2.2 · Koşulanlar (hepsi depo dışında ya da salt-okur)

Dondurulmuş kopya: `py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py <scratchpad>/kopya1` → `arac_hash 1f7e692994e0fd5734835999dd1de89e`. Ortam her çağrıda `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`. Tohum 2000–2039 hiçbir koşuda kullanılmadı.

| # | komut | süre | sonuç |
|---|---|---|---|
| E1 | (kopyada) `py -3.11 -m pytest tests2 -q -p no:cacheprovider` | 14 dk 39 s | **976 passed** |
| E2 | `py -3.11 kalibrasyon/mimari_denetimi.py` | 6 s | `Yapisal ihlal YOK` · 223 parametre: TÜRETİLMİŞ 71 · ÖLÇÜLMÜŞ 17 · KAYNAK 46 · DUYARSIZ 10 · TEDAVİ 39 · KOL TANIMI 15 · DÜNYA TANIMI 22 · **SINANMAMIŞ 3** · borç 0 · kapsam ilanı 12 |
| E3 | `py -3.11 arsiv/dogrulama/kayit_indeksi.py --kontrol` | <1 s | `✅ indeks güncel — 132 kayıt` |
| E4 | `py -3.11 kalibrasyon/uretici_duman.py --kapi` | 2 s | çıkış 0 |
| E5 | `py -3.11 kalibrasyon/regresyon_satirlari.py karsilastir k220 k220` | <1 s | 80/80 BİREBİR — ⚠️ dosyanın kendisiyle karşılaştırılması, yalnız aletin okuyabildiğini gösterir |
| E6 | (kopyada, kendi betiğim) k220'nin 7 vakasını `regresyon_satirlari._kos` ile yeniden koş, satırı JSON'dan geçirip k220 satırıyla alan alan karşılaştır | 2 dk (4 işçi) | **7/7 BİREBİR**, kod kimlikleri dâhil (aşağıda) |
| E7 | `ruff check sim2 protokoller kalibrasyon tests2 analiz --no-cache` (+ `--statistics`, `--select F821,B023,…`) | saniyeler | 973 satır; gerçek kusur sınıfları tek tek incelendi (D-24, §6) |
| E8 | U1 kayıtlarından oran tablosu (`ciktilar2/aodv_uygunluk/*_20261007_*.json`; kendi betiğim) | saniyeler | §4 D-02 tablosu |
| E9 | (kopyada) `py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --kol formasyon --aile derin_sizma --sinif surekli --protokoller aodv,desparete,en_guvenilir_kahin --tohumlar 1003 --kisa --isci 3 --kayit <scratchpad>/anatomi_kisa.json` — ölçüt önceden: çıkış 0 ve PDR'ler k220'nin `u-birincil-*` satırlarıyla birebir | 9 dk 22 s | çıkış 0 · PDR(pencere) kâhin **0,7922** · AODV **0,5167** · DESPARETE **0,6928** = k220 birebir → **Faz 5.0'ın aleti bugünkü kodla çalışıyor**. Evre bölümü "TANIMSIZ" (kısa pencere, D-13). Açık/sessiz (doğuma göre): AODV 0,438 / 0,595 · DESPARETE 0,582 / 0,803 (D-01) |

**E6 betiği** (`<scratchpad>/betik/regresyon_kesit.py`; ölçüt koşmadan önce betiğin başında: "her alan, `HER_KOSUDA_DEGISEN` dışında, kod kimliği dâhil BİREBİR"):

```
cd <scratchpad>/kopya1
py -3.11 -u ../betik/regresyon_kesit.py . <depo>/ciktilar2/regresyon/k220.jsonl \
   r-referans-statik-surekli-aodv u-bagimsiz-surekli-olsr-dugum_kaybi u-statik-aldatici-aodv \
   r-referans-statik-yok-dogrudan_komsu u-gorev-surekli-aomdv-esler_arasi u-statik-yok-desparete k-statik-surekli-olsr
k-statik-surekli-olsr                    86 s · alan 423 · fark 0
r-referans-statik-yok-dogrudan_komsu      9 s · alan 381 · fark 0
r-referans-statik-surekli-aodv           14 s · alan 425 · fark 0
u-statik-aldatici-aodv                   33 s · alan 446 · fark 0
u-bagimsiz-surekli-olsr-dugum_kaybi      10 s · alan 434 · fark 0
u-gorev-surekli-aomdv-esler_arasi        44 s · alan 425 · fark 0
u-statik-yok-desparete                  110 s · alan 458 · fark 0
SONUC: BIREBIR
```

(İlk denemede `ham.*` alanlarında 87 "fark" çıktı; sebep benim betiğimdi — bellekteki satır demet, diskteki liste. `SatirYazici`nın `_donustur`uyla JSON'dan geçirince hepsi birebir. Kendi aletimi böyle sınadım, bulgu değil.)

### 2.3 · Bakılamayanlar ve sebebi

- **Uzun koşular** (U1 yeniden, R'nin tam pencerede ölçümü, evre kapıları 1c/2c, birincil hücre tam pencere): her biri 30 dk'yı aşıyor; izin istenmedi. D-01 ve D-03'ün sayıları bu yüzden **mevcut kayıtlardan** (K-200 partisi, U1 JSON'ları, `cozunurluk.txt`) okundu; yeni ölçüm önerisi bulgularda.
- **AODV/AOMDV'nin RFC'ye kural kural yeniden denetimi:** K-208'in denetimi ve testleri okundu, yeniden yapılmadı. OLSR'da yalnız örnek kurallar (§8.2.1, §8.3.1, §9.5, §10, §14.3) RFC metniyle karşılaştırıldı.
- **DESPARETE'nin iç mantığı** (alan, edinim, Babel koşulu): yalnız yapı, kimlik ve bayraklar; algoritmanın doğruluğu denetlenmedi (Faz 5'te değişecek).
- **Kanal fiziği** (PER eğrileri, Rician blok üreteci, Al-Hourani): testleri geçtiği görüldü; formüller kaynaklarla yeniden türetilmedi.
- `v2/02`, `v2/16`, `protokol_kaynaklari/` kaynakların kendisi açılmadı (ns-3 ve RFC metinleri hariç).

### 2.4 · Başlangıç ve bitiş durumu (dokunulmadığının kanıtı)

Başlangıç (19:49, ilk komut):

```
$ git rev-parse HEAD
f148b0fd4dba79b005da75917fc30f1bbe50c096
$ git status --short
 M arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py
 M kalibrasyon/bag_kumesi.py
 M kalibrasyon/calisma_noktasi.py
 M kalibrasyon/iki_cift.py
 M kalibrasyon/kahin.py
 M kalibrasyon/li_replikasyonu.py
 M kalibrasyon/mimari_denetimi.py
 M kalibrasyon/onay_semantigi.py
 M kalibrasyon/pdr_tavani.py
 M kalibrasyon/yeniden_kullanim.py
 M sim2/dunya/topoloji.py
 M sim2/kanal/dunya.py
 M sim2/kanal/yayilim.py
 M sim2/kosum/kurulum.py
 M sim2/olcum/kayip_yeri.py
 M sim2/yapilandirma/kokenler.py
 M sim2/yapilandirma/konfig.py
 M tests2/test_kanal.py
 M tests2/test_kanal_yayilim.py
 M tests2/test_topoloji.py
 M tests2/test_yapilandirma.py
 M v2/04-KARARLAR.md
 M v2/06-ON-KAYIT.md
 M v2/07-SIMULATOR-TASARIMI.md
 M v2/09-LI-REPLIKASYONU.md
 M v2/12-YOL-HARITASI.md
 M v2/kayit/KARAR-GUNLUGU.md
?? arsiv/teshis/regresyon_k220/
```

Ara denetim (20:17): `find . -path ./.git -prune -o -newermt "2026-10-08 19:49:00" -print` → **boş** (depoda 19:49'dan sonra değişen dosya yok; önbellekler dâhil). SHA-256 manifesti (4 454 dosya, `.git` hariç) özeti `36d6a8f1c75206ae…`.

Bitiş (20:25, rapor depoya yazıldıktan hemen sonra):

```
$ git rev-parse HEAD
f148b0fd4dba79b005da75917fc30f1bbe50c096
$ git status --short
 M arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py
 M kalibrasyon/bag_kumesi.py
 M kalibrasyon/calisma_noktasi.py
 M kalibrasyon/iki_cift.py
 M kalibrasyon/kahin.py
 M kalibrasyon/li_replikasyonu.py
 M kalibrasyon/mimari_denetimi.py
 M kalibrasyon/onay_semantigi.py
 M kalibrasyon/pdr_tavani.py
 M kalibrasyon/yeniden_kullanim.py
 M sim2/dunya/topoloji.py
 M sim2/kanal/dunya.py
 M sim2/kanal/yayilim.py
 M sim2/kosum/kurulum.py
 M sim2/olcum/kayip_yeri.py
 M sim2/yapilandirma/kokenler.py
 M sim2/yapilandirma/konfig.py
 M tests2/test_kanal.py
 M tests2/test_kanal_yayilim.py
 M tests2/test_topoloji.py
 M tests2/test_yapilandirma.py
 M v2/04-KARARLAR.md
 M v2/06-ON-KAYIT.md
 M v2/07-SIMULATOR-TASARIMI.md
 M v2/09-LI-REPLIKASYONU.md
 M v2/12-YOL-HARITASI.md
 M v2/kayit/KARAR-GUNLUGU.md
?? arsiv/denetim/DENETIM-RAPORU-2026-10-08.md
?? arsiv/teshis/regresyon_k220/
$ find . -path ./.git -prune -o -newermt "2026-10-08 19:49:00" -print
./arsiv/denetim
./arsiv/denetim/DENETIM-RAPORU-2026-10-08.md
$ diff manifest_once.txt manifest_son.txt     # SHA-256, .git hariç bütün dosyalar
79a80
> 96ce69d5…  ./arsiv/denetim/DENETIM-RAPORU-2026-10-08.md
```

Başlangıçla tek fark bu rapor (izlenmeyen yeni dosya); öteki 4 454 dosyanın özeti birebir. Denetim boyunca bütün Python koşuları depo dışındaki dondurulmuş kopyadan ya da salt-okur araçlarla yapıldı; `ruff` `--no-cache` ile.

---

## 3 · Bulgu tablosu

| no | alan | önem | tek cümle | kanıt türü |
|---|---|---|---|---|
| D-01 | A · J | 🔴 | Birincil H2 testi karıştırmaya özgü kazancı ayırt etmiyor: pencerenin %33'ü karıştırıcı açık, v0.4.1'in üstünlüğü karıştırıcısız kollarda da var ve açık evrede en küçük | kayıtlardan sayı (K-200 `ozet.txt`, U1 JSON) + kod (çizelge) |
| D-02 | C | 🟠 | OLSR kural kural sadakat denetiminden geçmedi; en zayıf taban; §8.2.1 okuma farkı beyansız; "kötü bağ değil" hükmü yayın güvenilirliğini dışlamayan bir banda dayanıyor | kod + RFC metni + U1 kayıtları |
| D-03 | A · E | 🟠 | R ve bütün DUYARSIZ hükümleri 50 s'lik kısa pencerede ölçüldü; "birincil testin çözünürlüğü" değil | kod (`duyarlilik.py:184`, `cozunurluk.py:49`) + çıktı |
| D-04 | D · B | 🟠 | Protokole verilen gürültü ölçümü anlık, hatasız ve sürekli değerli; Faz 5.1 bunu kullanacak | kod (`dugum.py:169`) |
| D-05 | A · G | 🟠 | Ön-kaydın "önce yazıldı" kanıtı git'te yok (toplu commit'ler, beklentiye sonuç ekleme, 24 Eylül'den beri push yok, denetlenen hâl commit'lenmemiş) | git log + dosyalar |
| D-06 | A | 🟠 | `06` §4.4 (bağlayıcı) uygulanan U1-B kuralıyla çelişiyor; sonradan değişen beş ölçüt §10'da yok | belge alıntısı + karar günlüğü |
| D-07 | E | 🟠 | Köken defterinde TÜRETİLMİŞ kovası serbest oran taşıyor; birincil hücrenin manevra gürültüsü hiç taranmadı | kod (`kokenler.py:138`, `mobilite.py:598`, `duyarlilik.py:196`) |
| D-08 | D · A | 🟠 | Faz 5 tek çizelgede ve 8 tohumda geliştirilecek (çizelgeye ayar riski); 5.2 birincil hücrede kazanç gösteremez | plan + ölçülmüş Θ |
| D-09 | J | 🟠 | Hesap bütçesi yalnız birincil hücreyi sayıyor; Faz 5–7'nin gerçek koşu sayısı 3–4 katı; tek makine, yedek yok | plan + ölçülmüş süreler |
| D-10 | B | 🟡 | MAC bir çerçeveyi 8 kez deniyor; kaynak (ns-3, 802.11) "en çok 7 deneme" | kod + ns-3 kaynağı |
| D-11 | B | 🟡 | 33 km'lik dünyada bağlar ~9 km (≈30 µs) ama slot 20 µs; `14` §0'ın gerekçesi (≤ 7 µs) 7 km'lik alandan kalma | aritmetik + belge |
| D-12 | G | 🟡 | `protokol_hash` paket düzeyinde: DESPARETE değişince taban protokollerin kimliği de değişir; donmayı bağlayan bir test yok | kod + `regresyon_k220/karsilastir.txt` |
| D-13 | G | 🟡 | Regresyonun 16 referans vakasının hiçbirinde evre metrikleri hesaplanmıyor; tam pencere yok | k220 satırları |
| D-14 | E | 🟡 | Mimari denetiminin D8 ve D9 bölümleri eski 1:50 dünyada koşuyor | kod + E2 çıktısı |
| D-15 | E | 🟡 | Kâhinin 48 örnekte "yakınsadı" iddiası zayıf (bağımsız-yokta 24→48 hâlâ +0,010) | `sonumleme_yakinsama.txt` |
| D-16 | E | 🟡 | RSSI ve GPS hatalarının DUYARSIZ'ı "okuyan yok" diye verildi; Faz 5 okuyunca yeniden açılmasını zorlayan kapı yok | kod |
| D-17 | G | 🟡 | 684 kod kopyası dosyası (`kopya_2/`, `kopya_3/`, `kopya_b/`) git'te; `.gitignore` yalnız `kopya/` | `git ls-files` |
| D-18 | G · H | 🟡 | `li_beacon.py` (K-219'un "32 B'la 0,1270" üreticisi) K-220 yeniden adlandırmasıyla kırık | kod |
| D-19 | H | 🟡 | Canlı belgelerde bayat sayı ve durumlar (DEVIR, 04, 06, 07, 09, 13, 14, 05, README) | belge alıntıları (§5) |
| D-20 | H | 🟡 | Karar günlüğü indeksinde REVİZE işaretleri eksik (K-205, K-211, K-213) | indeks |
| D-21 | I · H | 🟡 | Kodda bayat iddialar (U1 aracının çıktısı "SINANMAMIS", `dunya.py`, `kahin.py`, `desparete_bayrak.py`) | kod |
| D-22 | D | 🟡 | Faz 5.0 beklentisi `v2/12` §1.1 ile uyuşmuyor ve D-01'den önce yazılmış | belge |
| D-23 | D | ⚪ | Faz 5.4 (çoğaltma) simülatör değişikliğinin PDR, korunum ve fatura tanımları önceden yazılsın | plan |
| D-24 | I | ⚪ | Ruff'ın 973 satırında gerçek kusur yok; `RUF100`/`I001` gürültüsü kapatılırsa gerçek uyarılar görünür olur | E7 |

---

## 4 · Bulgular ayrıntılı

### D-01 · 🔴 Birincil test karıştırmaya özgü kazancı ayırt etmiyor (A · J)

**Ne.** Ön-kayıt taslağının birincil testi H2.a/b/c: DESPARETE ↔ rakip, birincil hücrede, **birincil metrik PDR (ölçüm penceresi)** (`v2/06:42`), "üstün" = Holm sonrası p < 0,05 ve fark ≥ δ ve "mekanizma kapısı (kapı mühürde)" (`v2/06:34`). Projenin iddiası ise "DESPARETE karıştırmayı gerçekten çözen bir protokol" (`v2/01` §1, `README`). Bu test o iddiayı sınamıyor:

1. **Pencerenin üçte ikisi karıştırıcısız.** Ölçüm penceresi `[50; 320)`, `T_j = 150` (`v2/08:27`). `derin_sizma` `T_j`'den itibaren 15 s açık · 15 s sessiz (`sim2/kanal/karistirici.py:353–358`). Açık dönemler `[150,165) · [180,195) · [210,225) · [240,255) · [270,285) · [300,315)` = **90 s / 270 s = %33**. Birincil metriğin %67'si karıştırıcının hiç yayın yapmadığı zamandan gelir.
2. **v0.4.1'in üstünlüğü karıştırmadan bağımsız.** Karıştırıcısız kollarda (U1, yere toplama; DESPARETE 29 Eylül kaydı, AODV-j 7 Ekim kaydı):

   | kol | 1000 | 1001 | 1002 |
   |---|---|---|---|
   | formasyon-yok DESPARETE − AODV-j | +0,104 | +0,078 | +0,132 |
   | bağımsız-yok | +0,122 | +0,131 | +0,208 |
   | görev-yok | +0,127 | +0,167 | +0,172 |
   | statik-yok | +0,061 | +0,032 | +0,060 |

3. **Birincil hücrede kazanç karıştırıcı açıkken en küçük.** K-200 partisi (tam pencere, 1003–1006; `arsiv/teshis/birincil_2026-09-28/ozet.txt:1–9`), doğuma göre önce / açık / sessiz PDR:

   | | önce | açık | sessiz | önce→açık düşüş |
   |---|---|---|---|---|
   | AODV | 0,635 | 0,459 | 0,567 | −%27,7 |
   | AOMDV | 0,624 | 0,470 | 0,612 | −%24,7 |
   | DESPARETE | 0,782 | 0,560 | 0,754 | **−%28,4** |
   | kâhin | 0,862 | 0,729 | 0,848 | −%15,4 |
   | **DESPARETE − AODV** | **+0,147** | **+0,101** | **+0,187** | |

   DESPARETE karıştırıcı açıldığında AODV'den **daha çok** (mutlak 0,222 ↔ 0,176) kaybediyor; toplam pencere farkı (+0,144) büyük ölçüde temiz ve sessiz evrelerden geliyor. **Bugünkü kodla teyit** (E9, AODV-j, tek tohum 1003, kısa pencere): DESPARETE − AODV açıkta **+0,144**, sessizde **+0,208** — aynı yön.
4. **Mekanizma kapısı tanımsız** (`06` §0.4.2 "kapı mühürde"); bugünkü metinle "üstün" hükmü, bir ablasyon bayrağının herhangi bir pozitif katkısıyla verilebilir.

**Kanıt.** Yukarıdaki dosya:satırlar; U1 tablosu E8 betiğiyle `ciktilar2/aodv_uygunluk/desparete_referans_2026_yere_toplama_20260929_233427.json` ve `aodv_referans_2026_yere_toplama_20261007_120416.json`'dan. **Sınırlar:** K-200 partisi AODV-f ile (bugün AODV-j; U1'de hücre başına fark ≤ ~0,03) ve 4 geliştirme tohumuyla; DESPARETE'nin kodu o günden beri davranışça değişmedi (yalnız yorum; regresyon k204/k215'te DESPARETE vakaları birebir — K-211, K-216). Yön dört tohumun dördünde aynı değil ama ortalamalar ve karıştırıcısız kollar aynı hikâyeyi anlatıyor.

**Neden önemli.** Ana deney bugünkü tasarımla koşulursa H2.a büyük olasılıkla "üstün" çıkar (fark ~0,14 ≫ δ) ve rapor "DESPARETE karıştırmaya dayanıklı" diye okunur; jüri "karıştırıcıyı kapatınca da aynı fark var mı?" diye sorduğunda cevap "evet" olur. Bu, `01` §4'ün "bilimsel olarak dürüst ve savunulabilir" hedefini doğrudan tehdit eder. Ayrıca Faz 5'in mekanizmaları bu metrikle optimize edilirse temiz evreyi iyileştiren değişiklikler "karıştırma çözümü" gibi görünür.

**Önerilen düzeltme (öğrenci kararı — ön-kayıt metriği).** Faz 5.0'dan **önce**, sonucu bilmeden (yön DESPARETE aleyhine tutucu olduğu için p-avcılığı değildir; kayıt §10'a):
- (a) **Birincil metrik:** açık evrede doğan paketlerin PDR'si (`evre_cevrim_pdr`/kayıp anatomisinin `acik` dilimi zaten hesaplıyor) **ya da** (b) karıştırma kaybı `PDR(önce) − PDR(açık)` (M1'in tohum düzeyi hâli) **ya da** (c) aynı tohumlarda karıştırıcısız ikiz hücreyle fark-içinde-fark: `[P_D − P_R]_birincil − [P_D − P_R]_formasyon-yok`. Bence (a) birincil, (c) ikincil ve "karıştırmayı çözer" iddiasının tek savunması.
- **Aile 3 kapısı** (`06` §0.4.2, §5.3) şimdi yazılsın: "üstün" için karıştırmaya özgü mekanizmaların (5.1 C_jam · 5.3 postür · 5.4 PROTECT) bayrakla kapatıldığı kolun açık evre PDR'sinin anlamlı düştüğü gösterilmeli.
- Karıştırıcısız fark (`formasyon-yok`, aynı 40 tohum) ana deneye **ön-kayıtlı kontrol** olarak girsin (40 koşu × 2 protokol, bütçe D-09).
- İddia dili `01`, `README`, `06` §5.2'de: "karıştırma altında daha yüksek teslim" ile "karıştırmayı çözer" ayrımı.
- **Doğrulama:** değişiklikten sonra `analiz/hucre.py`ye yeni metrik + test; K-200 partisinin kayıtlarıyla (`kayit.jsonl`) yeni metrikte DESPARETE − AODV'yi yeniden hesaplayıp beklenti dosyasına "bugünkü fark" diye yazmak (Faz 5'in başlangıç çizgisi).

**Güven:** doğrulandı (sayılar kayıtlardan yeniden okundu; hesap E8).

---

### D-02 · 🟠 OLSR'ın sadakati denetlenmedi; en zayıf taban (C)

**Ne.** AODV, öğrencinin şartıyla (K-207: "kesinlikle gerçeğine birebir yapıldıysa") RFC 3561'e kural kural denetlendi ve **11 sapma** çıktı (K-208). OLSR için eşdeğer bir denetim yok (`arsiv/teshis/` içinde RFC 3626 kural tablosu yok; K-193 bir teşhis, denetim değil). Oysa:

- **U1 (7 Ekim, yere toplama, oran = protokol/kâhin):** OLSR 12 hücrenin 10'unda eşik altı; **karıştırıcısız statik** kolda 0,624 · 0,849 · 0,685 (eşik 0,90; aynı hücrelerde AOMDV 0,906 · 0,960 · 0,911). Eşler arasında 9 hücre düşük.
- Statikte bile döngü: TTL 32 → 64 OLSR'ı −0,079 düşürdü (K-214), statik 1002 0,799 → 0,685 (K-217); K-193'te düşüşlerin %10–14'ü TTL. Kayıpsız, hareketsiz bir ağda bağlantı-durumu protokolünde kalıcı döngü olağan değildir.
- Koşu başına ~9 500–11 500 komşu kaybı (K-193, statik-yok).
- **Beyan edilmemiş okuma farkı:** RFC 3626 §8.2.1 2-atlama kümesini *"L_SYM_time >= current time"* koşuluyla günceller (`protokol_kaynaklari/rfc3626_olsr.txt:2064–2070`); kod histerezisli `_simetrik_mi`yi kullanıyor (`protokoller/olsr.py:535–536`, `:290–296`). K-193 farkı ölçtü (+0,009 · −0,021 · +0,046) ve "okuma farkı beyan edilir" dedi; `olsr_bicim.py`nin beyan tablosunda (`:47–55`) yok. AODV'ye uygulanan kural ("gerekçesiz her sapma düzeltilir", K-207) OLSR'a uygulanmadı.
- **"Kötü bağ seçimi DEĞİL" hükmünün aleti yayını göremez:** bant `p_atlama = 1 − (1 − p)^(deneme + 1) ≥ 0,90` (`kalibrasyon/kayip_anatomisi.py:34–35, 137–138`), 8 denemeyle; yani tek deneme başarısı **≥ 0,25** olan bağ "iyi". OLSR'ın bağ algılaması ve TC taşması tek denemeli yayınlarla işler; %75 yayın kaybı olan bir bağ bu bantta "iyi"dir. K-193'ün "H1 düştü" okuması bu yüzden fazla.
- U1-B düşük hücreleri K-196'nın öğrenci istisnasıyla (sıralama koşulu sağlanmadan) açıklanmış sayıldı.

**Sağlam bulduğum kısım (§6):** histerezis (§14.3) RFC metniyle birebir; MPR buluşsalı (§8.3.1 adım 1–4), yönlendirme tablosu (§10, h = 2'den topoloji), TC işleme (§9.5 adım 2–4) ve varsayılan iletme (§3.4.1) örnek okumada RFC'ye uygun; kontrol defterinde kuyruk taşması 0 (k220'nin üç OLSR satırı) → PSN boşlukları yapay değil.

**Neden önemli.** H2.b (DESPARETE ↔ OLSR) ve Aile 1'in "ailenin bozunumu" hipotezi (H1.1) OLSR'ın gerçeğe sadık olmasına dayanır. "Statik, karıştırıcısız ağda OLSR kâhinin %62'si" tablosu jüride ilk sorulacak şeydir.

**Önerilen düzeltme.** Faz 5.0'dan önce `arsiv/teshis/olsr_sadakat_<tarih>/denetim.md`: RFC 3626 §3–§10, §14, §18 kural tablosu (K-208'in kalıbıyla; MUST/SHOULD/MAY, kodun satırı, ns-3 `olsr-routing-protocol.cc` hakemliği). Bulunan her gerekçesiz sapma ya düzeltilir (davranış değişir → yeni K, U1, regresyon; taban donmuştu, bu bilinçli bir "çözülme" kaydı ister) ya da `olsr_bicim.py` tablosuna gerekçesiyle girer — en az §8.2.1. Ayrıca kayıp anatomisine tek deneme başarısı bandı (yayın için) eklenip K-193'ün H1 hükmü yeniden okunmalı (statik-yok, 3 tohum, ~25 dk). Öğrenci kararı: sapma bulunursa OLSR'ın yeniden açılması.

**Güven:** denetim eksikliği ve §8.2.1 farkı doğrulandı; bir kusur olduğu **olası** (kanıtlanmadı).

---

### D-03 · 🟠 R ve DUYARSIZ hükümleri kısa pencerede (A · E)

**Ne.** `cozunurluk.py` ölçüm gövdesini `duyarlilik._is`ten alır (`kalibrasyon/cozunurluk.py:49`); o da `PENCERE = dict(karistirici_baslangic_s=5.0, isinma_s=10.0, olcum_bitis_s=40.0, kosu_bitis_s=50.0)` ile koşar (`kalibrasyon/duyarlilik.py:184–185, 309–310`). Yani **R = 0,0142**, 50 s'lik koşunun 30 s'lik penceresinde, karıştırıcının 5. saniyede (rotalar kurulmadan) açıldığı bir kesitte ölçüldü; araç yine de "KULLANILACAK ESIK R … (ESLESTIRILMIS — birincil testin cozunurlugu)" basıyor (`cozunurluk.py:124–125`). 10 DUYARSIZ hükmü de (kâhinle ve `protokol_tarama.py`/`protokol_kontrol.py` ile taban protokollerle) aynı `PENCERE`de verildi (`arsiv/teshis/faz4_4_birincil_2026-10-02/protokol_tarama.py:63`, `faz4_4_k215_2026-10-06/protokol_kontrol.py:55`). Ana deneyin penceresi 270 s (`v2/08:27`): tohum başına ~9 kat paket, ısınmış ağ.

`v2/03` §2'nin kendi kuralı: *"Kısa pencere zamanla biriken etkiyi göremez; profil kararları uzun pencerede verilir."* `saat_sapma_ppm`in gerekçesi 350 s'deki 7 ms'yi anar ama ölçüm 50 s'de (≤ 1 ms).

**Neden önemli.** Ana pencerede tohum başına gürültü küçükse gerçek çözünürlük 0,0142'den küçük olur; bugün |Δ| = 0,0118 (`yakalama_esigi_db`, 0,8R), 0,0068 (`gm_adim_s`), 0,0067 (kuyruk, OLSR) olan DUYARSIZ'lar ana deneyin görebileceği büyüklükte olabilir. Ters yönde de olabilir (topoloji varyansı baskınsa); ölçülmeden bilinmez.

**Önerilen düzeltme.** (1) `cozunurluk.py`nin basılı etiketi ve köken kaydı (`kokenler.py` `R_ESLESTIRILMIS`) "kısa pencere kesitinin çözünürlüğü" diye düzeltilsin. (2) Faz 6'nın δ gürültü ölçümü (3 taban × 20 tohum, tam pencere) yapılırken aynı koşulardan **tam pencere R'si** (kâhin çifti 20 tohum ek) hesaplansın; 10 DUYARSIZ'ın |Δ|'sı yeni R'ye karşı yeniden okunsun, aşanlar ya tam pencerede yeniden ölçülür ya kapsam ilanına gider. (3) `06` §8 koşul 1'in pencere taramasıyla birleştirilebilir. **Doğrulama:** mimari D12'ye "R'nin penceresi = ana deneyin penceresi" maddesi.

**Güven:** pencere doğrulandı; DUYARSIZ'ların değişeceği **olası**.

---

### D-04 · 🟠 Gürültü gözlemi idealleştirilmiş (D · B)

**Ne.** Her kancada protokole `olculen_gurultu_w = girisim.girisim_w(dugum, t, haric=-1) + gurultu_w` verilir (`sim2/kosum/dugum.py:169–170`): o andaki bütün iletimlerin ve karıştırıcının alıcıdaki **anlık, kesin, sürekli değerli** gücü (`sim2/kanal/girisim.py:138–158`). RSSI için σ 2 dB hata ve tamsayı dBm modellendi (`05` §3.3a), GPS'e hata verildi; bu alana hiçbir şey yok. `05` §3.1 "mutlak değeri serbest bir ölçek; sezim oranla ya da değişimle" diyor — bu bir kullanım kuralı, model değil. Bugün hiçbir protokol okumuyor (`grep olculen_gurultu_w protokoller/` boş).

**Neden önemli.** Faz 5.1 (C_jam) tam olarak bu alanı, `mesgul_sure_s` ve `phy_hata` ile kullanacak. Kesin anlık değer, karıştırıcının açık/kapalı geçişini mikrosaniyede ve mesafeyi neredeyse kesin verir — gerçek bir sürücü (gürültü tabanı raporu: tamsayı dBm, yüzlerce ms ortalama, kalibrasyon aralığı) bunu vermez. Jüri: *"Protokolünüz karıştırıcının gücünü her düğümde anlık ve hatasız ölçüyordu."*

**Önerilen düzeltme.** Faz 5.1'den önce, `05` §7'nin yoluyla: alanı bir ölçüm modelinden geçir (tazeleme aralığı, pencere ortalaması, tamsayı dBm, σ; köken defterine kova — kaynak yoksa SINANMAMIŞ ve Faz 6'da duyarlılık). Taban protokoller okumadığı için satırları birebir kalır (regresyon `--degisen` gerekmez; doğrulama: k220 karşılaştırması BİREBİR + yeni test "ölçülen gürültü yalnız tazeleme anlarında değişir").

**Güven:** doğrulandı (kod).

---

### D-05 · 🟠 Ön-kaydın "önce yazıldı" kanıtı zayıf (A · G)

**Ne.**
- Depoda **9 commit** var (`git log | wc -l`). Sıra yer yer kanıtlanabiliyor — `faz4_4_k215_2026-10-06/beklenti.md` `3457137`de (6 Ekim), sonuçlarının çoğu `f148b0f`te (8 Ekim); `faz5_0_2026-09-30/beklenti.md` henüz koşulmadan `b860e10`da — ama sistematik değil: `faz4_5_2026-10-08/beklenti.md` sonuçlarıyla birlikte `f148b0f`te; `evre_cizelge_2026-10-01/beklenti.md` ve 2 Ekim'de ölçülen `g1c.txt`/`g2c.txt` birlikte `3457137`de; `olsr_referans_2026-09-28/` ve `evre_g1p_2026-09-28/`nin beklenti ve sonuçları birlikte `b860e10`da.
- Beklenti dosyalarına sonradan sonuç ekleniyor: `faz4_5_2026-10-08/beklenti.md` "ölçütler (ölçmeden önce)" başlığıyla başlıyor, aynı dosyada "## Sonuç 1 (03:42)" var. Dosyanın değiştirilme zamanı bile ölçütün tarihini göstermez.
- `.gitignore:13–15` "commit zamanı ölçütün ölçümden önce yazıldığının kanıtıdır" diyor — uygulamada değil.
- `git status -sb`: `main...origin/main [ahead 7]`; `origin/main` = `c48fdc2` (24 Eylül). Faz 4'ün bütün kayıtları ve kod tek makinede.
- Denetlenen hâl (K-220/K-221) commit'lenmemiş; `arsiv/teshis/regresyon_k220/` izlenmiyor.

Beklenti dosyalarının içeriği güvenilir görünüyor (önceden yazılmış öngörülerin tutmadığı yerler dürüstçe "✗" diye işaretli, ör. K-191); sorun içerik değil, **kanıtlanabilirlik**.

**Neden önemli.** Mühür (~12 Kasım) projenin bilimsel değerinin temeli; jüri "hipotezler sonuçtan önce yazıldı" iddiasının kanıtını sorabilir. Ayrıca tek makine = veri kaybı riski (elektrik kesintisi K-211'de yaşandı).

**Önerilen düzeltme (öğrenci; git yalnız öğrencide).** (1) Bugünkü hâli hemen commit + push. (2) Bundan sonra her ölçümde: beklenti dosyası **ayrı bir commit**, koşudan önce; sonuçlar `sonuc.md`ye, beklentiye dokunulmaz; push. (3) Mühürde: `06` + analiz kodu + tohum listesi için etiketli commit (`git tag muhur-2026-11-12`) + push; mümkünse commit özetini danışmana e-postayla göndermek (üçüncü taraf zaman damgası). **Doğrulama:** `git log --format='%h %ad' -- <beklenti>` sonuç dosyasınınkinden önce.

**Güven:** doğrulandı.

---

### D-06 · 🟠 `06` §4.4 uygulanan kuralla çelişiyor; sonradan değişen ölçütler kayıtsız (A)

**Ne.** `06` başlığı §4.4'ü "bağlayıcı hüküm, değişmez" sayıyor (`v2/06:3`). §4.4/3 U1-B'yi şöyle tanımlıyor: *"eşik altı hücre, mekanizma hücreleri doğru sıralıyor ve kusur izleri (kuyruk/tampon düşüşü, **döngü**) dışlanıyorsa açıklanmış sayılır"* (`v2/06:101`). Uygulamada:
- OLSR'ın 10 hücresi **sıralama koşulu sağlanmadan** açıklandı (K-196 istisnası);
- AODV'nin hücreleri **döngü izine rağmen** açıklandı (K-207: "RFC kurallarından doğan döngü mekanizmadır").

Faz 4'te sonuç görüldükten sonra değişen ölçütler (hepsi karar günlüğünde dürüstçe beyanlı, ama `06` §10 "kayıt tablosunda" yok; son satır 26–28 Eylül, `v2/06:172`):
1. K-196 — OLSR için U1-B sıralama istisnası;
2. K-207 — U1-B "kusur izi"nin anlamı;
3. K-212 → K-215 — G2ç'nin D maddesi kâhinin boş kol koşusuna eşlendi (sonra özgün ölçütle de geçti, K-217);
4. K-219 — örnekleme denetimi C 0/270'te kaldı, "ED dışarıda" diye yeniden soruldu (270/270);
5. K-219 — G3 → G3ç.

**Neden önemli.** Her biri gerekçeli; ama örüntü ("kapı kalınca tanım değişir") ön-kayıt kültürünün en çok sorgulanacak yeri. Belge "bağlayıcı" dediği metni uygulamadığı sürece mühür metni de güvenilmez görünür.

**Önerilen düzeltme.** `06` §4.4/3'ü bugünkü kuralla yeniden yaz (K-196, K-207 atfıyla; OLSR istisnasını adıyla), §10'a beş satır ekle (tarih · ne · sonuçtan önce mi sonra mı · etkisi). Rapor yazımında bunlar "sınırlılıklar"a girsin. Doğrulama: `06` ↔ `04` §5 tutarlılığı.

**Güven:** doğrulandı.

---

### D-07 · 🟠 "TÜRETİLMİŞ" kovası serbest sayılar taşıyor (E)

**Ne.** `KOVALAR["TURETILMIS"]` = "başka parametrelerden hesaplanıyor; serbest değil" (`sim2/yapilandirma/kokenler.py:29`). Ama:
- `gm_hiz_sigma_ms`: *"azami hızın %10'u; hız zarfıyla orantılı"* (`kokenler.py:138–139`) — %10 serbest bir seçim. **Birincil hücrenin kod yolunda:** formasyon kolu manevra gürültüsünü bundan alır (`sim2/dunya/mobilite.py:598–604`, `topoloji.py:156`).
- `gorev_jitter_hiz_ms`: *"azami hızın ~%7'si"* (`kokenler.py:161–162`) — görev kolu (keşifsel).
- `gm_alfa`: τ_v ≈ 30 s seçimi; "Θ'yı değiştirmiyor (5,95 → 5,93)" ölçümü eski dünyanın.

Duyarlılık aracı yalnız SINANMAMIŞ ve KOL_TANIMI'nı tarar (`kalibrasyon/duyarlilik.py:196–198`), yani TÜRETİLMİŞ etiketli serbest bir sayı hiçbir zaman sınanmaz. Faz 4.4'ün taramalarında (`arsiv/teshis/faz4_4_birincil_2026-10-02/taramalar.sh`) bu üçü yok.

**Neden önemli.** "Mühürden önce SINANMAMIŞ = 0" kuralı köken defterinin dürüstlüğüne dayanır; bugünkü "SINANMAMIŞ 3" eksik sayım. Birincil hücrenin hareket dinamiği doğrudan bağ değişimini belirler (istasyon tutma zaten DUYARLI çıktı, K-217).

**Önerilen düzeltme.** `gm_hiz_sigma_ms` ve `gm_alfa` → SINANMAMIŞ (ya da öğrenci kararıyla DÜNYA TANIMI); `gorev_jitter_hiz_ms` → KOL_TANIMI + KAPSAM_İLANI. Birincil hücrede `duyarlilik.py --dunya referans_2026 birincil gm_hiz_sigma_ms gm_alfa --tohum 20` (~2 × 17 dk + taban 8 dk; D-03'ün pencere sorusuyla birlikte). TÜRETİLMİŞ kayıtlarının hepsinin (71) "serbest oran/seçim" sözcükleri için gözden geçirilmesi (benim taramam: `%`, `~`, `seçil` geçen 15 kayıt; çoğu gerçekten türetilmiş ya da sonucu değiştirmeyen önbellek sınırı). Doğrulama: mimari D12 sayımı.

**Güven:** doğrulandı (sınıflandırma); duyarlılığı **ölçülmedi**.

---

### D-08 · 🟠 Faz 5'in geliştirme düzeni ayar riskine açık; 5.2 birincil hücrede boşa (D · A)

**Ne.**
- Faz 5 her mekanizmayı "geliştirme tohumları 1003–1010 · birincil hücre + bir yer karıştırıcılı aile" ile değerlendirecek (`v2/12` §2). Birincil hücrenin karıştırıcısı **sabit 15 s / 15 s çizelgeli**; DESPARETE'nin zaman sabitleri (`T_repair_max` 6 s, postür histerezisi, epoch) bu çizelgeye karşı ayarlanırsa kazanç senaryoya özgü olur (`03` §1: "hiçbir kol — kendi protokolümüz dâhil — senaryoya göre ayarlanmaz"). Ana deneyin tohumları yeni (2000–2039) ama **çizelge aynı**; tohum ayrımı bu ayarı yakalamaz.
- 5.2 "öngörülü kaçınma — hareketle kopan bağı önceden bırakmak": birincil hücrenin kolu formasyon, ölçülen Θ "formasyon tanımsız (%99,6 kopmuyor, tek ömür)" (`kokenler.py` `MOBILITE_THETA_REFERANS`). Birincil testte gösterebileceği kazanç yok.
- Plan 7 alt faz × ablasyon × önceden yazılı beklenti, ~4 haftada (mühür 12 Kasım).

**Önerilen düzeltme.** (1) Faz 5'in değerlendirme setine **farklı çizelgeli bir dayanıklılık hücresi** (ör. 10 s açık / 20 s sessiz ya da rastgele süreli) ve sürekli bir yer ailesi (`cephe_hatti`) eklensin; ana deneyde bu hücre ön-kayıtlı ikincil test olsun. (2) Öncelik D-01'e göre: 5.1 → 5.3 → 5.4 (karıştırmaya özgü); 5.2 keşifsel kollara ya da "gelecek çalışma"ya; 5.5/5.6 yalnız kontrol yükü sorun çıkarırsa. (3) Her mekanizmanın beklentisi "açık evre PDR'si" ve "karıştırıcısız kolda zarar yok" iki ölçütüyle yazılsın. Öğrenci kararı (kapsam).

**Güven:** risk **olası**; 5.2'nin birincil hücredeki etkisizliği ölçülmüş Θ'dan çıkarım.

---

### D-09 · 🟠 Takvim ve hesap bütçesi eksik sayılmış (J)

**Ne.** `v2/12` §3: *"Ana deney (40 tohum × ~5 kol ≈ 200 koşu) ~40–45 sa"* — yalnız birincil hücre. Faz 7 ayrıca "Aile 1 hücreleri + Aile 3 kolları" (`v2/12` §2). Ölçülmüş verimle (K-200: 8 işçide 32 koşu 7,1 sa ≈ 4,5 koşu/sa; DESPARETE ve AODV koşu başına 105–140 dk):

| iş | koşu (kaba) | süre |
|---|---|---|
| Faz 5: 6 mekanizma × (açık/kapalı × 8 tohum × 2 hücre) × ~2 deneme + 5.0 + 5.7 (U1, U3) | ~450 | ~100 sa |
| Faz 6: δ gürültüsü 60 · pencere üçlüsü ~60 · tam pencere R (D-03) 40 · Rician keşifsel ~40 | ~200 | ~45 sa |
| Faz 7: birincil 200 · Aile 3 (4 kol × 40) 160 · Aile 1 (3 protokol × 4 hücre × 40) 480 · karıştırıcısız kontrol (D-01) 80 · dayanıklılık hücresi (D-08) 80 | ~1 000 | ~220 sa |

Faz 7'nin bilgisayar süresi tek başına ~9 gün kesintisiz; 12 Kasım–19 Aralık penceresinde yazım "Kasım başında başlar". Tek makine, son push 24 Eylül (D-05).

**Önerilen düzeltme.** `v2/12` §3'e bu tablo (gerçek sayılarla) ve bir **düşme sırası** (zaten §4'te var — ona Aile 1 hücre sayısının sınırı eklensin); Aile 1'in hücreleri mühürde 2–3 ile sınırlansın; 20 tohumla yetinilecek keşifsel kollar adlandırılsın; güç benzetimi (Faz 6) n'yi 40'ın üstüne çıkarırsa ne düşeceği önceden yazılsın. Öğrenci kararı.

**Güven:** tablo kaba tahmin (ölçülmüş birim sürelerle); sonucun yönü sağlam.

---

### D-10 · 🟡 MAC deneme sayısı bir fazla (B)

**Ne.** `Dcf.onay_gelmedi`: her denemede `_deneme += 1`, vazgeçme `_deneme > yeniden_deneme_siniri` iken (`sim2/mac/dcf.py:173, 198`) → sınır 7 ile **8 deneme** (1 + 7). Kâhin de aynı varsayımla `deneme = yeniden_deneme_siniri + 1` (`kalibrasyon/kahin.py:283`). Kaynak: ns-3 `FrameRetryLimit` = *"The maximum number of transmission attempts of a frame … corresponds to the dot11ShortRetryLimit"*, varsayılan 7 (`protokol_kaynaklari/uygulama_kaynaklari/ns-3/wifi-mac.cc:150–154`); düşürme `GetRetryCount() == GetFrameRetryLimit()` (`wifi-remote-station-manager.cc:1232`) → 7 deneme. Köken kaydı "KAYNAK, 7" (`kokenler.py:376–380`).

**Neden önemli.** Bütün protokollere eşit; mutlak teslimi ve bağ kopması algılama gecikmesini biraz büyütür (tek deneme başarısı 0,3 olan bağda 0,918 → 0,942). Eski dünyada 4 ↔ 7 "etkisiz" ölçülmüştü (K-189). Asıl sorun KAYNAK etiketinin yanlış uygulanması.

**Önerilen düzeltme.** Öğrenci kararı: (a) `>` → `>=` (davranış değişir → regresyon, U1 hücreleri biraz oynar; taban donmuşken en az bir U1 yeniden), ya da (b) köken kaydına "1 + 7 deneme (ns-3'ten bir fazla, beyan)" ve duyarlılık (sınır 6) — tek parametre, ~25 dk. Ben (b)'yi öneririm (Faz 5 öncesi riski düşük).

**Güven:** doğrulandı.

---

### D-11 · 🟡 Uzun bağlarda slot zamanlaması (B)

**Ne.** `v2/14:18`: *"1–2 km'lik bağda ≤ ~7 µs < 20 µs slot → standart zamanlama geçerli"*. 33 km'lik alanda derece 9,67 (K-188) → yoğunluk 40/1089 km² ile tipik komşu yarıçapı ~9 km (π r² · 0,0367 ≈ 9,7) → yayılım ~30 µs > slot. Simülatör yayılım gecikmesini modelliyor ve ACK zaman aşımına `2 × maks_gecikme` ekliyor (`sim2/kosum/kosu.py:177`, `kontrol.py:347`) ama slot 20 µs sabit; 802.11'in kapsama sınıfı ikisini birlikte ayarlar.

**Neden önemli.** Uzak düğümler birbirini geç duyar → çarpışma artar; yayın ağırlıklı protokoller (OLSR TC taşması) daha çok etkilenebilir. Gerçek uzun menzilli telsizler (Doodle Labs "mesafe" ayarı) slotu da büyütür.

**Önerilen düzeltme.** `14` §0 satırını 33 km'ye göre düzelt ve kapsam beyanına "slot 20 µs, kapsama sınıfı yok — ACK zaman aşımı genişletildi" ekle; istenirse slot = 20 + maks_gecikme kolu ile tek duyarlılık (Faz 6).

**Güven:** aritmetik doğrulandı; etkisi **ölçülmedi**.

---

### D-12 · 🟡 Kimlik özetleri donmayı kanıtlayamıyor (G)

**Ne.** `_protokol_parmak_izi`: sınıfın modülü bir paketteyse **paketin tamamı** özetlenir (`sim2/kosum/sonuc.py:106–133`). Dört protokol aynı `protokoller/` paketinde → DESPARETE'nin bir dosyası değişince AODV/OLSR/AOMDV satırlarının `protokol_hash`i de değişir; kâhinin kimliği `kalibrasyon/`un tamamına bağlı. Regresyon bu alanı otomatik "beklenen" sayıyor (`regresyon_satirlari.py:105–110`); k215 → k220'de "kimlik.protokol_hash 11 vakada farklı (beklenen)" (`arsiv/teshis/regresyon_k220/karsilastir.txt`) — on biri de kâhin satırı; kâhinin davranışı değişmediği hâlde `kalibrasyon/`daki yorum ve ad değişiklikleri (K-220) yüzünden. Aynı mekanizma Faz 5'te öbür yönde işleyecek: DESPARETE'nin bir dosyası değişince taban protokol satırlarının kimliği de değişir. Taban protokol dosyalarının özetini sabitleyen bir test yok.

**Neden önemli.** Faz 5'te `protokoller/` sürekli değişecek; "taban protokoller K-218'den beri dondu" iddiası satır kimliğinden kanıtlanamaz (davranış değişikliğini regresyon yine yakalar).

**Önerilen düzeltme.** `tests2/`ye bir test: `aodv.py · aodv_bicim.py · olsr.py · olsr_bicim.py · aomdv.py · aomdv_bicim.py · kosum_kosumu.py`nin `dosya_hash`i K-218'de kaydedilen değerlere eşit (değişirse test kırılır, yeni K kaydı ister). İsteğe bağlı: `protokol_hash`e sınıfın kendi modül kümesi.

**Güven:** doğrulandı.

---

### D-13 · 🟡 Regresyon referans dünyada evre metriklerini sınamıyor (G)

**Ne.** 80 vakanın 16'sı referans dünyada (3 `r-` + 13 `u-`), hepsi kısa pencerede `karistirici_baslangic_s=5, isinma_s=10` (`regresyon_satirlari.py:385–386`) → TEMİZ evre boş, evre metrikleri hesaplanmıyor (k220'de `u-birincil-*` satırlarının `sok_*`, `toparlanma_*`, `tespit_*` alanları yok; dört `f-` tam vaka eski dünyada). K-211 bunu not etmiş ("evre metrikleri v2'yi birim testleri ve kapılar sınar"). Birincil hücrenin çizelgeli evre yolu (M1/M2/M4, `evre_cevrim_pdr`, katlanmış profil) regresyonda hiç yok.

**Önerilen düzeltme.** Bir referans vakası `isinma_s=10, karistirici_baslangic_s=40, olcum_bitis_s=100, kosu_bitis_s=110` ile (kâhin, birincil hücre; ~10–15 dk) — evre alanları dolar, D-01'in yeni metriği de buradan sınanır. Doğrulama: yeni taban + `--yeni` önekiyle karşılaştırma.

**Güven:** doğrulandı.

---

### D-14 · 🟡 Mimari denetiminin iki bölümü eski dünyada (E)

**Ne.** D8 "sayısal sağlık" `Konfig(kol="denetim")` (`kalibrasyon/mimari_denetimi.py:266`), D9 "belirlenimcilik" `Konfig(kol="d", …)` (`:310–319`) — ikisi de `Konfig()` varsayılanı = eski 1:50 dünya. E2 çıktısında "OK cw_max erisilemez (en cok CW = 511 < 1023)" ve "OK karistirici gucu None (olculmedi)" eski dünyanın gerçekleri; referans dünyada (deneme 7) CW 1023'e ulaşır.

**Önerilen düzeltme.** D8/D9'u `referans_2026` ile de koştur (eski dünya maddeleri "eski dünya" etiketiyle kalabilir); "cw_max erişilemez" maddesini dünyaya göre yaz. Doğrulama: E2 çıktısında iki dünya ayrı.

**Güven:** doğrulandı.

---

### D-15 · 🟡 Kâhinin yakınsama iddiası zayıf (E)

**Ne.** `arsiv/teshis/faz4_4_birincil_2026-10-02/sonumleme_yakinsama.txt`: bağımsız-yok 6 → 12 → 24 → 48 örnekte PDR 0,7895 · 0,8203 · 0,8437 · 0,8540 — artışlar +0,031 · +0,023 · **+0,010** (bandın 0,94'ü, "PLATO" eşikte); birincilde 24 → 48 artışı (+0,0058) 12 → 24'ünkünden (+0,0033) büyük. 96 ölçülmedi; 5 tohum. Köken kaydı "6 örnekte kâhin yakınsamamıştı … 48 (yakınsama)" diyor (`kokenler.py:747–757`).

**Neden önemli.** Kâhin U1'in paydası ve R'nin aleti; yakınsamamışsa U1 oranları hâlâ biraz şişik (bağımsızda belki ~0,01). Eşiklere göre küçük; ama "yakınsadı" sözcüğü fazla.

**Önerilen düzeltme.** Kayıtta "48'de kalan artış ≤ ~0,01 (tahmini)" diye yaz; Faz 6'da 96 örnekle tek kesit (koşu süresi örnek sayısından bağımsız ölçülmüştü).

**Güven:** doğrulandı (sayılar kayıttan).

---

### D-16 · 🟡 Faz 5'in okuyacağı alanların DUYARSIZ'ı mekanik olarak bağlı değil (E · F)

**Ne.** `rssi_olcum_sigma_db`, `gps_dikey_sigma_m`, `gps_hiz_sigma_ms` DUYARSIZ — gerekçe "bugün hiçbir protokol okumuyor … Faz 5'te bir mekanizma okursa yeniden ölçülür" (`kokenler.py:328–350`). Üçünün de kaynağı yok. 5.1 RSSI'yi, 5.2 konum/hızı okuyacak. Hiçbir test ya da mimari maddesi "protokol bu alanı okumaya başladı → kova yeniden açılmalı" demiyor. (`05` §3.3a/3.3b ise hâlâ "SINANMAMIŞ" diyor — D-19.)

**Önerilen düzeltme.** Mimari denetimine madde: `protokoller/` içinde `rssi_dbm`, `kendi_konum`, `kendi_hiz`, `olculen_gurultu_w`, `mesgul_sure_s` okunuyorsa ilgili köken kaydı DUYARSIZ olamaz (SINANMAMIŞ'a döner). Faz 5.1'in ilk işi.

**Güven:** doğrulandı.

---

### D-17 · 🟡 Kod kopyaları git'te izleniyor (G)

**Ne.** `.gitignore:18` yalnız `kopya/`; `kopya_2/`, `kopya_3/`, `kopya_b/` eşleşmiyor. `git ls-files | grep -E "/kopya[^/]*/"` → **684 dosya** (`aodv_sadakat_2026-09-30/kopya_2` 136 · `faz4_4_birincil_2026-10-02/kopya_2` 137 · `kopya_3` 137 · `faz4_4_k215_2026-10-06/kopya_b` 137 · `faz4_5_2026-10-08/kopya_2` 137). K-204: "arşiv git'te izlenir (kopyalar … hariç)".

**Neden önemli.** Depo şişer; `grep` bayat kodu (ör. `iletim_menzili_m` yüzlerce kez) bulur — yeni ajanlar için bağlam zehri; kopyaların içindeki `test_*.py`ler yanlışlıkla toplanabilir.

**Önerilen düzeltme (öğrenci).** `.gitignore`'a `kopya*/`; `git rm -r --cached` ile beş dizin (dosyalar diskte kalır). Doğrulama: `git ls-files | grep -c /kopya` → 0.

**Güven:** doğrulandı.

---

### D-18 · 🟡 Kırık üretici: `li_beacon.py` (G · H)

**Ne.** `arsiv/teshis/faz4_5_2026-10-08/li_beacon.py:33` `DS.konfig(kol="li").iletim_menzili_m` — K-220 alanı `nominal_bag_m` yaptı; `b_li_ayristirma.py` iki adı da okuyacak biçimde yamandı, `li_beacon.py` unutuldu. K-219'un ve `DEVIR` §5'in "32 B'la 0,1270" sayısının üreticisi bugünkü kodla `AttributeError` verir.

**Önerilen düzeltme.** `b_li_ayristirma.py`deki satırı kopyala. Doğrulama: betiğin kısa kesiti (1 tohum).

**Güven:** doğrulandı (kod okuması; koşulmadı).

---

### D-19 · 🟡 Canlı belgelerde bayat sayılar (H) — liste §5'te.

### D-20 · 🟡 Karar indeksinde REVİZE eksik (H)

**Ne.** İndeks "132 kayıt · 2 revize" (`KARAR-GUNLUGU.md:156`). "🟢 geçerli" görünen ama yerine başkası geçenler: **K-211** "TABAN PROTOKOLLER DONDU — AODV-i · OLSR-c · AOMDV-e" (→ K-218, "K-211'in yerine") · **K-213** R = 0,0188 (→ K-216, 0,0142) · **K-205** "AODV-g RFC'ye sadık" (→ K-208 "iddia fazlaydı") · **K-191** OLSR U1 0,642 (→ K-196 "bayat"). Okuyan "K-211 geçerli: AODV-i dondu" sonucuna varır.

**Önerilen düzeltme.** `arsiv/dogrulama/kayit_indeksi.py::SUPERSEDE`e dört kayıt; indeks yeniden üretilir. Doğrulama: `--kontrol`.

**Güven:** doğrulandı.

### D-21 · 🟡 Kodda bayat iddialar (I · H)

| yer | iddia | gerçek |
|---|---|---|
| `kalibrasyon/aodv_uygunluk.py:676` (ve `:322–324` belge dizesi) | "ROTA TAMPONU (kapasite 64 · omur 30 s — ikisi de SINANMAMIS)" — U1 çıktısına basılıyor | ikisi KAYNAK (K-198), `kokenler.py:470–482` |
| `sim2/kanal/dunya.py:108–113` | gölgeleme hücresi "Değer SINANMAMIŞ kalır — duyarlılık ekseni" | DÜNYA TANIMI (K-220) |
| `kalibrasyon/kahin.py:143–145` | dilim "bugün ~0,8 s" | referansta 2,5 km / 66,7 m/s = 37,5 s → 10 s'ye kırpılır |
| `protokoller/desparete_bayrak.py:41–44` | "Koşu kimliği protokol parametrelerini İÇERMEZ" | K-171'den beri içerir (`desparete.py:831–838`) |
| `kalibrasyon/mimari_denetimi.py` D8 | "karistirici gucu None (olculmedi)" | eski dünyanın maddesi (D-14) |

Hepsi davranışa dokunmaz; tek commit'te düzeltilir (regresyon gerekmez, `arac_hash` değişir).

### D-22 · 🟡 Faz 5.0 beklentisi güncel değil (D)

**Ne.** `arsiv/teshis/faz5_0_2026-09-30/beklenti.md` yalnız `desparete,en_guvenilir_kahin`, tohum 1003–1006; soru K-200'ün sayılarıyla ("DESPARETE açık evrede 0,56, kâhin 0,73" — 6 örnekli kâhin). `v2/12` §1.1 "taban protokoller, kâhin ve DESPARETE" diyor. Karar kuralı DESPARETE'nin kendi onarım makinesine (kota, açlık) odaklı — Babel'in iç işi; D-01'in sorusu ("karıştırıcı açıkken farkı ne kapatır") yok. Kopya K-215 öncesi (12 bunu söylüyor).

**Önerilen düzeltme.** D-01 kararından sonra beklenti yeniden yazılsın: kollar AODV · AOMDV · OLSR · DESPARETE · kâhin; açık/sessiz/önce ayrımıyla; karar kuralına "açık evre kaybının bölgesi (ed/girişim/uzak) ve sebebi". Süre: 5 kol × 4 tohum ≈ 20 koşu ≈ 4,5 sa (8 işçi).

### D-23 · ⚪ Faz 5.4'ün simülatör değişikliği önceden tanımlansın (D)

PROTECT'in çoğaltması simülatöre "kopya kalemi" ister (`v2/12` §2). Önceden yazılmalı: PDR'de kopya (ilk teslim sayılır, kopyalar `tekrar_bastirilan`), korunum defterinde kopyanın akıbeti, kopyaların kontrol değil **veri** yüküne faturası, U1/kâhin karşılaştırmasında kopyanın etkisi. Anahtar arkasında, varsayılan kapalı (k220 birebir).

### D-24 · ⚪ Ruff çıktısı (I)

973 satırın 366'sı `RUF100` (kullanılmayan `noqa`), 113 `I001`, 192 `ISC004` (180'i `kokenler.py`nin uzun gerekçe dizeleri). "Gerçek kusur" sınıflarını tek tek baktım: `F821 grafik` (`sonumleme_onbellegi.py:115`) `del` kaynaklı yanlış alarm; 6 `B023` kapanışı döngü içinde hemen çağrılıyor; `regresyon_satirlari.py` ve `kapsam.py`'deki `ISC004`ler kasıtlı uzun kimlikler. **Gerçek kusur yok.** Öneri: bir `ruff.toml` ile `RUF100`, `I001`, `ISC004`'ü `kokenler.py` için kapat → kalan ~250 satır okunabilir olur, yeni gerçek uyarı görünür kalır.

---

## 5 · Belge temizlik listesi

| belge · yer | bugün yazan | doğrusu | iş |
|---|---|---|---|
| `DEVIR-PROMPT.md:72` (§5) | mimari "SINANMAMIŞ 12" | 3 (E2) | güncelle |
| `DEVIR-PROMPT.md` §5 | komutlar `python …` (aynı belge §4 `py -3.11` diyor) | `py -3.11` | güncelle |
| `v2/04:4` | "Güncel: 29 Eylül" | 8 Ekim | güncelle |
| `v2/04:60` (§7) | "R = 0,023 (eski dünya; referansta Faz 6'da)" | 0,0142 (K-216; kısa pencere — D-03); §9 ile çelişiyor | güncelle |
| `v2/04:64` (§8) | "geliştirme 1000–1010" | R 1000–1039, duyarlılık 1000–1019 kullandı; `06` §2 "2000–2039 dışı her tohum" | `06` ile birleştir |
| `v2/04:51` (§6) | K-200'ün sayıları, uyarısız | "K-215 öncesi kod" notu (12'deki gibi) + D-01 evre kırılımı | güncelle |
| `v2/06:3, 101` (§4.4) | "bağlayıcı, değişmez" + sıralama/döngü koşulu | K-196/K-207 uygulaması (D-06) | güncelle + §10 |
| `v2/06:94` (§4.3) | "Karıştırıcısız kâhin tavanı (eski dünya) 0,996–1,000 · 0,84–0,92" | referans: statik 0,99–1,00 · hareketli 0,84–0,98 (K-217) | güncelle |
| `v2/06:148` (§9) | "Taban protokoller donar … (koşuyor)" kutusu boş | K-218 ile tamam | işaretle |
| `v2/06` §4.4/4 | AODV sapma listesi (yerel onarım, RREP-ACK, karşılıksız RREP, +1 B) | `04` §5'in listesi daha tam (önceki atlama ömrü, RERR yayın, TTL yükte) | tek yerde tut (`aodv_bicim.py`), ikisi atıf |
| `v2/06` §10 | son satır 26–28 Eylül | D-06'nın beş satırı | ekle |
| `v2/07:13` | Li "H1 = 0,127" | 0,1188 (K-219, 84 B beacon) | güncelle |
| `v2/09:3, 119` | "0,127 TUTTU", tablo 0,1270 | 0,1188; 0,1270 32 B beacon'la | güncelle (ön-kayıt kısmına dokunmadan) |
| `v2/14:18` (§0) | "1–2 km'lik bağda ≤ 7 µs" | 33 km'de ~9 km (D-11) | güncelle |
| `v2/14:100` (§9) | "3 🟡 U1 … yeniden koşulacak" · Li 0,127 | ✅ K-218 · 0,1188 | güncelle |
| `v2/14` §2 Rician | "Faz 4'te … ölçülür" | EKSEN (K-215) | güncelle |
| `v2/13:45, 83` | `KONTROL_KAPSULLEME` "kökeni SINANMAMIŞ" · R6 açık | KAYNAK (G15/G16); `BEKLEYEN_UYANDIRMA_TAVANI` ÖLÇÜLMÜŞ | R6'yı kapat |
| `v2/05:38, 44` | RSSI σ "SINANMAMIŞ, kaynak aranıyor" · GPS "ikisi SINANMAMIŞ" | DUYARSIZ (okuyan yok, D-16) | güncelle |
| `v2/05` §3.1 | `olculen_gurultu_w` modelsiz | D-04'ün modeli | Faz 5.1'den önce |
| `v2/README.md:3` | "önceki hâllerin hepsi `arsiv/`de, git dışı" | `v2/arsiv` izleniyor (44 dosya) | güncelle |
| `README.md:20, 57` | "Durum — 28 Eylül … son kalibrasyonu sürüyor" · 7 kova | Faz 4 kapandı; 8 kova + kapsam ilanı | güncelle |
| `README.md` "Kurulum" | `python -m pytest` | `py -3.11` notu (Windows) | ekle |
| `v2/kayit/KARAR-GUNLUGU.md` indeks | K-191/205/211/213 "geçerli" | REVİZE (D-20) | üret |
| `.gitignore:13–15` | "commit zamanı … kanıtıdır" | D-05 süreci yerleşene kadar doğru değil | sadeleştir |
| `v2/04` · `v2/12` · `v2/06` §9 | SINANMAMIŞ/kapsam sayımı üç yerde | tek yer (`04` §9), ötekiler atıf | birleştir |
| `v2/06` §4.4/4 ↔ `aodv_bicim.py` ↔ `04` §5 | sapma listeleri üç yerde | kaynak `*_bicim.py` | birleştir |

**Arşive taşınabilir:** `kalibrasyon/onay_semantigi.py` ve `pdr_tavani.py` (K-219: eski dünyanın tarihçesi, referansta koşulmuyor; yalnız eski regresyon vakalarına mı bağlı, kontrol edilip `arsiv/kalibrasyon-…`ye) · `arsiv/teshis/faz5_0_2026-09-30/kopya/` (K-215 öncesi; D-22'den sonra yerine yenisi).

**Sadeleştirilmeli:** `kalibrasyon/` yorumları (~%32 yorum/docstring) toptan değil, "bugün", "ölçülmedi", "SINANMAMIŞ" geçen cümleler hedefli (D-21 türü).

---

## 6 · Sağlam bulunanlar

- **Test takımı:** 976/976 (E1); K-205…K-215'in davranış değişikliklerinin her biri adlandırılmış testle bağlı (`test_K208_H1…H11`, `test_K215_*`, `test_K209_*`, `test_K210_*`).
- **Belirlenimcilik ve taban:** k220'nin 7 vakası (eski + referans dünya; AODV · OLSR · AOMDV · DESPARETE · tek atlamalı sınav protokolü; düğüm kaybı, aldatıcı, eşler arası) ayrı süreçte bütün alanlarıyla birebir (E6) — çalışma ağacı = k220'yi üreten kod.
- **Kâhin sızıntısı:** `protokoller/` yalnız `sim2.gozlem`i ve kendisini içe aktarıyor (grep); gözlem yüzeyi izin listesiyle (`pencere.py:176–200`) ve P6 testiyle bağlı; DESPARETE'nin ablasyon bayrakları koşu kimliğinde (`desparete.py:831–838`).
- **İstatistik:** Wilcoxon'un tüm-sıfır NaN tuzağı test çağrılmadan kapanıyor; Holm adım adım, monoton; δ formülü `06` §0.4.2 ile aynı; güç eğrisi merkezlenmemiş gürültüyü reddediyor (`analiz/istatistik.py:81–198`).
- **OLSR örnek kuralları:** §14.3 histerezisi RFC metniyle birebir (PSN'nin titreşimden önce verilmesi parametresiz telafi edilmiş); §8.3.1 MPR adımları; §10'un h = 2'den başlayan topoloji yinelemesi; §9.5 sıra dışı TC'nin atılması; kontrol kuyruğunda taşma 0.
- **Duyarlılık aracı:** iki ayaklı kural (band **ve** R), "ÖLÇÜLEMEDİ"nin parmak iziyle ayrılması, olasılık eşiklerinin kayıp payından oynatılması ve R'nin bayatlık kapısı (K-216'da gerçekten ateşledi) iyi tasarlanmış.
- **Mimari denetimi** (6 s): katman yönü, çıplak `assert`, ölü kod, RNG akışları, köken defterinin eksiksizliği ve `DUYARSIZ` kayıtlarının ölçülen |Δ| taşıması.
- **Kayıt kültürü:** her beklentinin içinde tutmayan öngörüler işaretli; ajan hataları (çift başlatma, yanlış teşhis K-212, "RFC'ye sadık" fazla iddiası) karar günlüğünde açıkça düzeltilmiş.
- **Ruff:** gerçek kusur yok (D-24).
- **Gözlem sözleşmesinin geri kalanı:** komşu yalnız duyulan çerçeveden; saat senkronu yok; kendi GPS'i hatalı; `mesgul_sure_s` ve `phy_hata` gerçek sürücü sayaçlarına karşılık geliyor.

---

## 7 · Faz 5'e geçiş için öneri sırası

**Grup 0 — hemen (öğrenci, 10 dk):** bugünkü hâli commit + push (D-05). `.gitignore` `kopya*/` + `git rm --cached` (D-17).

**Grup 1 — öğrenci kararları (Faz 5'ten önce, ajan önerisiyle):**
1. **D-01:** birincil metrik/kontrast (önerim: açık evre PDR'si birincil; karıştırıcısız ikizle fark-içinde-fark ön-kayıtlı ikincil) · Aile 3 mekanizma kapısının tanımı · iddia dili.
2. **D-08/D-09:** Faz 5 kapsamı (5.1 → 5.3 → 5.4 öncelikli; 5.2 keşifsel) · dayanıklılık hücresi · Faz 7 bütçe tablosu ve düşme sırası.
3. **D-02:** OLSR sadakat denetimi yapılsın mı; sapma çıkarsa taban "çözülsün" mü.
4. **D-10:** deneme sayısı — düzelt mi beyan et mi.

**Grup 2 — ajan, kod ve belge (yarım–bir gün; davranış değiştirmeyenler):**
- D-04 gürültü ölçüm modeli (anahtar arkasında, taban satırları birebir) + D-16 mimari maddesi.
- D-06, D-19, D-20, D-21 belge/indeks/yorum düzeltmeleri (tek commit; `arac_hash` değişir, regresyon `karsilastir` yalnız kimlik farkı).
- D-12 donma testi · D-14 mimari D8/D9 referans dünyada · D-18 `li_beacon.py`.
- D-03 etiket düzeltmesi.
- Doğrulama: tam takım + mimari + `regresyon_satirlari.py uret k22x` (~45 dk, izinle) + `karsilastir k220 k22x --izin <kimlik ve köken alanları>`.

**Grup 3 — ölçüm (izinle, sırayla, dondurulmuş kopyadan):**
- D-02 OLSR denetimi (+ tek deneme bandıyla K-193'ün yeniden okunması, ~25 dk).
- D-07 `gm_hiz_sigma_ms` · `gm_alfa` duyarlılığı (~45 dk).
- D-13 evre yolunu sınayan referans regresyon vakası (taban yenilenirken).
- D-22 Faz 5.0 beklentisinin D-01'e göre yeniden yazılması → **Faz 5.0**.

**Faz 6'ya:** D-03 (tam pencere R ve DUYARSIZ'ların yeniden okunması, δ ölçümüyle aynı koşulardan) · D-11 (slot) · D-15 (kâhin 96 örnek) · D-23 (çoğaltma tanımları, 5.4'ten önce).

**Öğrenci kararı isteyenler:** D-01 · D-02 · D-05 (git) · D-08 · D-09 · D-10 · D-17 (git).
