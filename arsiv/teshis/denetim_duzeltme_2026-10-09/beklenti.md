# Denetim düzeltmeleri (K-223) — ölçümler ve ölçütleri (ölçmeden önce)

> 9 Ekim 2026 · ajan · kod K-223 (`AODV-j` · `OLSR-d` · `AOMDV-f` · referans dünyada en çok 7 iletim denemesi). Bu dosya koşudan ÖNCE ayrı bir commit'le girer (denetim D-05, öğrenci (a)); sonuçlar `sonuc.md`ye yazılır, bu dosyaya dokunulmaz.
> Her iş dondurulmuş kopyadan, sırayla, yanında ağır iş yok (8 işçi). Ana deney tohumları (2000–2039) hiçbir işte yok.

## 0 · Sıra ve süre

**Kuyruk A** (`kuyruk_a.sh`, `kopya_a`; ~2,5 sa): A1 regresyon (~55 dk) → A2 R (~70 dk) → A3 OLSR anatomisi (~25 dk).
Ardından ajan: `sonuc.md` (A) · R değiştiyse `duyarlilik.py::R_ESLESTIRILMIS` (aracın bayatlık kapısı, sapma > 0,0005) · öğrencinin commit'i · `kopya_b`.
**Kuyruk B** (`kuyruk_b.sh`, `kopya_b`; ~17 sa, koşullu adımlarla ~21 sa): B1 D-07 duyarlılığı (~45 dk; sınırdaysa +3 sa) → B2 U1 iki desen (~10,5 sa) → B3 evre kapıları 1c · 2c · 3c (~5,5 sa).
Kuyruk B'nin kopyası R'den sonra dondurulur: B1'in hükmü ve B2'nin kâhin aşımı kuralı R'yi okur.

## A1 · Regresyon k220 → k223

Ölçüt ayrı dosyada: `arsiv/teshis/regresyon_k223/beklenti.md` (+ `denetle.py`). **Geçerse yeni regresyon tabanı k223.**

## A2 · Çözünürlük R (7 denemeyle)

`py -3.11 -u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40`. Ön koşul aynı: kâhinin hücre ortalaması PDR'si 0,1–0,95 arasında. Yön önceden bilinmiyor, yazılmaz; büyüklük olarak 0,0142'ye yakın beklenir (yalnız deneme sayısı değişti).
- Sapma > 0,0005 → sabit güncellenir (köken ÖLÇÜLMÜŞ, K-224).
- **R küçülürse:** köken defterinde |Δ|'sı yazılı DUYARSIZ kayıtları yeni R'yle karşılaştırılır; |Δ| ≥ yeni R olan kayıt SINANMAMIŞ'a döner ve Faz 6'nın tam pencere taramasına (D-03) girer. **R büyürse** eski hükümler olduğu gibi kalır (eski, daha sıkı eşikle verildiler).

## A3 · OLSR — K-193'ün "kötü bağ seçimi değil" hükmü tek deneme bandıyla (D-02)

`py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol statik --protokoller olsr --tohumlar 1000,1001,1002 --isci 3 --kayit <dizin>/anatomi_statik.json` — K-193'ün hücreleri (statik-yok · yere toplama · tam pencere), kod `OLSR-d` ve 7 deneme.

Hüküm kuralı (üç tohumun toplamında, karar bağları):
1. **Yeniden denemeli bant** (`p_atlama` = 1 − (1 − p)^7): karar bağlarının ≥ %90'ı "iyi" (≥ 0,90) → *veri için* kötü bağ seçimi değil (veri unicast'tir, yeniden denenir). Sağlanmazsa K-193'ün hükmü düşer ve OLSR'ın bağ seçimi kusur adayı olarak teşhis edilir.
2. **Tek deneme bandı** (`p` — HELLO ve TC'nin gördüğü):
   - karar bağlarının ≥ %90'ı p ≥ 0,90 → hüküm **güçlü biçimiyle** ayakta: OLSR'ın yayın düzlemi de bu bağlarda kayıpsıza yakın; komşu çalkantısı bağ kalitesinden gelmiyor.
   - > %10'u p < 0,90 → K-193'ün dili daraltılır: *"veri bağları iyi; kontrol düzlemi bu bağların X'inde kayıplı"* — komşu çalkantısının **mekanizma adayı** olarak kayda geçer. Kusur değildir: RFC 3626'nın yayınları onaysızdır ve 802.11 yayını yeniden denemez.
3. Düşüş imzası: en büyük düşüş sebebi `rota_gecersiz` kalırsa K-196 atfının mekanizması (geçide rotanın aralıklı boşalması) `OLSR-d`de de geçerli; kalmazsa B2'de OLSR'ın düşük hücrelerinin açıklaması yeniden yazılır (B2 kuralı 4).
4. Kimlik: üç PDR, B2'de U1'in OLSR statik-yok yere toplama hücreleriyle 4 basamak aynı olmalı (aynı konfig).

## B1 · D-07 — `gm_alfa` · `gm_hiz_sigma_ms` (birincil hücre)

`py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil gm_alfa gm_hiz_sigma_ms` (5 tohum, ×0,5 · ×2). Aracın kuralı aynen, A2'nin R'siyle: DUYARSIZ ⇔ |Δ| < R **ve** kendi bandının içinde (üç çıktı, iki çarpan).
- **Sınırda** (önceden): DUYARLI ama en büyük |Δ| ≤ 1,3R ve band ≤ 1,8× · ya da duyarsız ama en büyük |Δ| ≥ 0,7R → aynı komut `--tohum 20` ile; 20 tohumluk sonuç 5 tohumluğun YERİNE geçer (K-215'in kuralı).
- DUYARSIZ → köken DUYARSIZ, sayılarıyla (SINANMAMIŞ 5 → 3). DUYARLI → öğrenciye: kaynak · DÜNYA TANIMI · eksen · kapsam; karar verilene kadar SINANMAMIŞ.
- ÖLÇÜLEMEDİ (parmak izi birebir) çıkarsa BULGU: formasyon kolu ikisini de okuyor (`mobilite.py`) — denetim D-07'nin kod okuması yanlış ya da alet hücreyi kurmuyor; teşhis edilir.

## B2 · U1 yeniden — iki desen, üç taban protokol + kâhin

`py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aodv,olsr,aomdv`, sonra `--desen esler_arasi`. Koşum hükmü kendisi basar; kayıt listeleri güncellenince altı kaydın her biri `aodv_uygunluk.py --dunya referans_2026 hukum <kayıt>` ile yeniden değerlendirilir. Eşikler değişmez (statik 0,90 · hareketli 0,60); kâhin aşımı kuralı A2'nin R'siyle.

Beklenen:
- Deneme sayısı protokolü ve kâhini birlikte etkiler; oranların yönü önceden bilinmiyor, değişim küçük beklenir. `OLSR-d`: K-193 §8.2.1 farkını statik-yok'ta +0,009 · −0,021 · +0,046 ölçmüştü → OLSR'ın düşük hücreleri eşiğin altında kalır (düzeltme onları kurtarmaz).

Kurallar (K-215 ön-kaydıyla aynı):
1. **U1-U** (keşif · çok atlamalı teslim · korunum · kâhin aşılmıyor) üç protokolde iki desende ✅ olmalı. Kâhin aşımı R'den büyükse K-192 (b) zarf prosedürü (koşullu adım: `arsiv/teshis/aodv_sadakat_2026-09-30/aomdv_zarf_hucre.py <desen> <kol> <tohum> <protokol PDR> <ETX PDR>`, `ZARF_KOK=kopya_b`): zarfın içindeyse kayıt (`KAHIN_ASIMI_ACIKLANMIS`), zarfı da aşıyorsa yazılım hatası aranır. Artık aşmayan eski kayıt ölüdür, silinir.
2. **Ölü kayıt:** açıklanmış listelerde olup artık eşiği geçen hücre silinir (alet yakalar).
3. **`AODV-j` · `AOMDV-f`nin yeni düşük hücreleri** → K-207 (kodları değişmedi; kaynağına sadık protokolün kendi sınırı) — BULGU.
4. **`OLSR-d`nin düşük hücreleri:** K-196 atfı ancak aynı anatomiyle. Statik kol A3'le yenilenir (A3 kuralı 3). A3'te ya da önceki listede olmayan yeni bir hücrede `kayip_anatomisi.py --sinif yok --protokoller olsr --kol <kol> --tohumlar <t>` (koşullu adım): en büyük düşüş `rota_gecersiz` **ve** karar bağlarının ≥ %90'ı yeniden denemeli bantta iyi; tek deneme bandı ayrıca yazılır. Sağlanmazsa mekanizma aranır, OLSR donmaz.
5. Kalan bütün kayıtların metni yeni sürüm etiketiyle (`OLSR-d`, 7 deneme, U1 tarihi) yeniden yazılır.
6. **Eşler arası** keşifseldir: oradaki OLSR düşük hücreleri açıklanmamış BULGU kalır, donmayı durdurmaz (K-218 gibi).

**Yeniden donma (K-224):** A1 geçti · U1-U iki desende ✅ · U1-B yere toplamada ✅ (bütün düşük hücreler 3–4'e göre açıklanmış) → `AODV-j` · `OLSR-d` · `AOMDV-f` DONAR, `tests2/test_donma.py` o hâle bağlı kalır. U1-U kalırsa donma yok: kusur aranır, öğrenciye bildirilir.

## B3 · Evre kapıları (7 denemeyle, `OLSR-d`yle)

`DESPARETE_DUNYA=referans_2026 py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c`, `2c`, `3c`. Ölçütler değişmez (`v2/08` §08; G2ç'nin D maddesi bugünkü kodundaki hâliyle, K-217) — G1ç · G2ç · G3ç · G4ç geçmeli. Beklenen: dördü de geçer (deneme sayısı metriğin tanımına dokunmuyor). Kalan kapı Faz 5'ten önce teşhis edilir.

## Kapanış

Tam test takımı · mimari denetimi · lint (değişiklik öncesiyle aynı) · kayıtlar (`aodv_uygunluk.py` listeleri, köken defteri) · belgeler (`04` §5 · `06` §9 · `12` · DEVIR) · K-224. Ardından Faz 5.0.
