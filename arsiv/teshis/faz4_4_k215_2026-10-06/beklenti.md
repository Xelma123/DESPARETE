# Faz 4.4 · K-215 sonrası ölçümler — ölçütler (ölçmeden önce)

> 6 Ekim 2026 · ajan · kod K-215 (`AODV-j` · `AOMDV-f` · kâhin 48 örnek · TTL 64 · beacon 84 B · Rician K eksen). Hepsi dondurulmuş kopyadan, sırayla, yanında ağır iş yok. Sıra `v2/12` §1.1/3.

## 1 · Regresyon k215

Beklenti ayrı dosyada: `arsiv/teshis/regresyon_k215/beklenti.md`.

## 2 · Çözünürlük R (yakınsamış kâhinle)

`py -3.11 -u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40`. Ön koşul aynı: kâhinin hücre ortalaması PDR'si 0,1 ile 0,95 arasında. Sonuç `duyarlilik.py::R_ESLESTIRILMIS`e (köken ÖLÇÜLMÜŞ). Beklenen yön: kâhin daha iyi tahmin ettiği için ETX kâhininin tohumlar arası yayılımı azalabilir; R'nin yönü önceden bilinmiyor, yazılmaz.

## 3 · Sınırdaki 6 parametre, 20 tohum

`py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil --tohum 20 <adlar>` — üç parti: (`golgeleme_hucre_m`, `gm_adim_s`) · (`kanal_dilimi_s`, `yakalama_esigi_db`) · (`cbr_titresim_s`, `sim2/dunya/mobilite.py::ISTASYON_TUTMA_S`). Aracın kuralı aynen: DUYARSIZ ⇔ |Δ| < R **ve** kendi bandının içinde (üç çıktı, iki çarpan). Bu ölçüm 5 tohumluğun YERİNE geçer (aracın "sınırdaki kayıt `--tohum N` ile yeniden ölçülür" kuralı). DUYARLI kalan → öğrenciye: kaynak / eksen / kapsam.

## 4 · Protokol kontrolleri

`protokol_kontrol.py` (ölçüt betiğin başında): OLSR'da `kuyruk_kapasitesi` ve `saat_sapma_ppm` TTL 64'le; AODV ve AOMDV'de `saat_ofset_araligi_s` `AODV-j`yle — beş tohumda iz BİREBİR bekleniyor.

## 5 · U1 yeniden — iki desen, üç taban protokol + kâhin

`py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen <yere_toplama|esler_arasi> --protokol aodv,olsr,aomdv`, ardından `hukum`. Eşikler değişmez (statik 0,90 · hareketli 0,60).
- Beklenen: kâhin hareketli kollarda iyileştiği için (6 → 48 örnek, kısa pencerede +0,04…+0,07) hareketli kollarda oranlar DÜŞER; statik kol değişmez (tek örnek) — yalnız AODV-j ve beacon farkı.
- U1-U: kâhin aşımı kalırsa K-192 (b) zarf prosedürü; eski zarf kayıtlarından artık aşmayanlar ölü kayıttır, silinir.
- U1-B: yeni düşük hücreler beklenir. `AODV-j` ve `AOMDV-f` için K-207 (kaynağına sadık protokolün kendi sınırı — bulgu); OLSR için K-196 atfı ancak mekanizma aynıysa (aynı anatomi), değilse aranır. Açıklanmış listelerin ölü kayıtları silinir.

## 6 · Evre kapıları

`evre_metrikleri_kapilari.py 1c` ve `2c` (protokoller ve kâhin değişti). Ölçütler `v2/08` §08; G2ç'nin D maddesi K-215'le boş kola eşleştirilmiş hâliyle.

## 7 · U1'in iki prosedür adımı (kuyruk B'den sonra, ölçmeden önce — 8 Ekim 00:50)

- **K-192 (b) zarfı** — eşler arası `statik-yok` 1001: AODV-j 0,9906 · AOMDV-f 0,9923 · ETX kâhini 0,9898 (aşım 0,0008 · 0,0025; kâhinin beacon'ı 84 B'a ağırlaştı). `aomdv_zarf_hucre.py esler_arasi statik-yok 1001 0.9923 0.9898` (üç kâhin). Kural aynen: protokol ≤ zarf → "ETX kâhini bu hücrede üst sınır değil", kayıt; zarfı aşan → yazılım hatası aranır. AOMDV'nin eşler arası üç eski zarf kaydı artık aşmıyor (ölü) → silinir.
- **OLSR anatomisi** — yere toplamada yeni açıklanmamış üç hücre (`bagimsiz-yok` 1001 · 1002, `gorev-yok` 1001) + karşılaştırma için açıklanmış `bagimsiz-yok` 1000: `kayip_anatomisi.py --dunya referans_2026 --sinif yok --protokoller olsr --kol <kol> --tohumlar …` (tam pencere). K-196 atfı ancak AYNI anatomiyse: her yeni hücrede (i) en büyük düşme sebebi `rota_gecersiz` (geçide rotanın boşalması) ve (ii) karar bağlarının ≥ %90'ı kâhine göre iyi (kötü bağ seçimi değil). Sağlanmazsa mekanizma aranır.
- Toplam yük: zarf 3 süreç (~10 dk), sonra iki anatomi çağrısı birlikte 3 + 1 süreç (8'in altında, ~1,5 sa).
