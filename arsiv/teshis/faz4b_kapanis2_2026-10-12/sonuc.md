# Faz 4b kapanış ölçümleri, ikinci kuyruk — sonuç

> 13 Ekim 2026 · ölçüt `beklenti.md` (commit `d3fd674`, koşudan önce) · `kopya/` = `d3fd674` (147 dosya birebir, `kopya_ozet.txt`; kuyruktan sonra kopya ve ana ağaç yeniden doğrulandı) · kuyruk 12 Ekim 19:20:49 – 13 Ekim 11:01:06 (15 sa 40 dk) · çıktılar `kopya_payi.txt` · `anatomi_*` · `G1c.txt` · `G2c.txt` · `zaman.txt`

| ölçüt | sonuç |
|---|---|
| A · kopya kuralı | ✓ sağlandı |
| B · dört temsilci anatomi | ✓ dördü de geçti |
| C · G1ç | ✗ kaldı, yalnız JarmRout yüzünden (D) → sebep ölçüldü, K-239'un kaydıyla ✓ |
| C · G2ç + G4ç | ✗ kaldı, yalnız JarmRout yüzünden (G4ç) → sebep ölçüldü, K-239'un kaydıyla ✓ |

## A · Kopya kuralı (K-238) — sağlandı

- **Önkoşul:** betiğin PDR'si 0,9954, U1 kaydıyla birebir ✓.
- **statik-yok 1001 (eşler arası):**
  - 12 799 paket üretildi, 12 740'ı teslim edildi; yalnız kopyayla teslim edilen 12.
  - Kopyasız PDR 0,9945. Oran 1,0129'dan 1,0120'ye iner; bu değer 1 + R = 1,0126'nın altında ✓.
  - Mimari denetimi yapısal ihlal bulmuyor (13 Ekim).
- **formasyon-yok 1000:** aşım 0,0083 < R; zarf adımı gerekmez, kayıt ölçümü yazar.
- **Öngörü tutmadı.** Yalnız kopyayla teslimin binde 13'ü aşması bekleniyordu; ölçülen binde 0,9. Kopya aşımın yalnız 0,0009'unu açıklıyor; kalan 0,0120 R'nin, yani ölçümün çözünürlüğünün içinde.
- **Kayıt:** iki hücre `KAHIN_ASIMI_ACIKLANMIS`a girdi. Hüküm her kayıtlı aşımı "ZARF İÇİNDE (K-192 b)" diye basıyordu; bu etiket kopya kuralına ve R altı aşıma uymadığı için "AÇIKLANMIŞ (K-192 b · K-238)" oldu (`tests2/test_aodv.py` buna göre).

## B · Düşük hücreler — dört anatomi de geçti

Anatomiler yere toplama deseninde, her kolun oranı en düşük hücresinde koşuldu. Dört hücrenin PDR'si U1 kaydıyla birebir.

| hücre | PDR | 1 korunum · çelişki · atfsız | 2 döngü/TTL | 3 `rotasiz_paket` | 4 RREQ yeniden yayını / üretim | RERR | en büyük düşüş (üretilene) |
|---|---|---|---|---|---|---|---|
| statik 1002 | 0,5139 | ✓ · 0 · 0 | 0 | 0 | 74,6 | 5 850 | iletim başarısızlığı %49,7 |
| bağımsız 1000 | 0,2494 | ✓ · 0 · 0 | 0 | 0 | 59,4 | 7 697 | iletim başarısızlığı %60,6 |
| görev 1000 | 0,2754 | ✓ · 0 · 0 | 0 | 0 | 54,3 | 7 098 | iletim başarısızlığı %60,2 |
| formasyon 1000 | 0,3578 | ✓ · 0 · 0 | 0 | 0 | 58,8 | 6 598 | iletim başarısızlığı %52,4 |

Ölçütün dışında kalan iki gözlem:
- İkinci büyük düşüş tampon taşması: statikte %2,3, hareketli kollarda %11,8–14,2.
- Hareketli kollarda 95–117 keşif yanıtsız kaldı (`kesif_basarisiz`), statikte hiç kalmadı.

Öngörüler:
- En büyük düşüş iletim başarısızlığı olur — tuttu.
- RREQ başına yeniden yayın 60–80 olur — ölçülen 54–75; hareketli kollar aralığın biraz altında.

**Kayıt.** Yere toplamanın 11 ve eşler arasının 5 düşük hücresi `ACIKLANMIS_DUSUK_REFERANS`a girdi. Her hücrenin metni U1 kaydındaki çöküş izini yazar:
- düşük hücreler: rota tamponu girişi 30 511–133 001, tepe doluluğu 32–64;
- geçen hücreler: giriş 41–3 674, tepe 2–26.

**`hukum` (kayıtlı U1 ölçümleri, bugünkü kod):**

| protokol | desen | U1-U | U1-B | not |
|---|---|---|---|---|
| JarmRout | yere toplama | ✓ | ✓ | 11 açıklanmış düşük hücre |
| JarmRout | eşler arası | ✓ | ✓ | iki aşım kayıtlı; 5 açıklanmış düşük hücre |
| OLSRv2 | yere toplama | ✓ | ✓ | değişmeden |
| OLSRv2 | eşler arası | ✓ | ✓ | değişmeden |

## C · Çizelgeli evre kapıları — ikisi de yalnız JarmRout yüzünden kaldı

**G1ç** (formasyon-yok, hayalet çizelge):
- M4 yanlış tespit 0/8 ✓.
- M1'i 2 SE dışında kalan protokol 1/4 ✓ (sınırda). Kalan protokol JarmRout: kol ortalaması +0,046, 2 SE 0,033.
- D'si iki tohumda da 2 SE dışında kalan protokol: **JarmRout** ✗.
  - JarmRout: 1003'te −0,029 (2 SE 0,023), 1004'te +0,035 (2 SE 0,028). İşaretler zıt.
  - AODV, OLSRv2 ve DESPARETE'nin D'si iki tohumda da içeride.

**G2ç** (formasyon-sürekli, derin sızma):
- Kâhinin M1'i +0,168 (2 SE 0,025): etkili ✓.
- Kâhinin D'si boş kolunkine göre 2 SE içinde ✓. Fark 1003'te −0,008, 1004'te +0,003.

**G4ç** — `p99 < açık süre` (15 s) ve sızıntı, tohum 1003 · 1004:

| protokol | p99 (s) | sızıntı | |
|---|---|---|---|
| AODV | 1,46 · 1,50 | 0,011 · 0,014 | ✓ |
| OLSRv2 | 3,04 · 0,37 | 0,016 · 0,005 | ✓ |
| DESPARETE | 4,22 · 4,05 | 0,030 · 0,026 | ✓ |
| kâhin | 0,51 · 0,15 | 0,007 · 0,003 | ✓ |
| **JarmRout** | **28,05 · 29,73** | **0,183 · 0,225** | ✗ |

Öngörü ("JarmRout'un p99'u keşif bekleyişleri yüzünden yüksek olabilir") tuttu. Simülatörün ortak rota tamponunun ömrü 30 s'dir (RFC 4728 §9 `SendBufferTimeout`, bütün protokoller için aynı). JarmRout'un p99'u bu tavana dayanıyor.

## Sebep (teşhis)

Beklenti, JarmRout yüzünden kalan kapının sebebinin ölçülmesini ister. Teşhis `arsiv/teshis/faz4b_kapi_teshis_2026-10-13/teshis.md`dedir: G1ç hücresi, 1003 · 1004, 5 sa 20 dk. Satırlar G1ç kaydıyla 18 alanda birebir.

- **G4ç — gecikme kuyruğu rota beklemesi (öngörü tuttu):**
  - 15 s'yi aşan teslimlerin %98,7–100'ü rota tamponundan geçmiş; bekleyiş payının medyanı 0,96.
  - Yolun kendi p99'u 4,1–5,0 s.
  - Keşif selin altında uzar: p99 26–27 s, en uzunu 106–127 s. Bekleyen paket ortak tamponun 30 s'lik ömrüne kadar tutulur.
- **G1ç — PDR karıştırıcısız kolda durağan değil.** Öngörülen "sel çevrimleri" tutmadı. Ölçülen iki etki:
  - **1003 · eğilim:** PDR koşu boyunca düşer (−0,032 / 100 s); 15 s başına RREQ yeniden yayını 25,9 binden 30–32 bine çıkar.
  - **İki tohumda · pencere sonu boşalması:** trafik 320 s'de durunca sel söner. Son 5 s'de doğanların PDR'si 0,525 · 0,588 (öncesi 0,29–0,47).
  - Son sessiz dönem [315; 320) bütünüyle boşalma bölgesindedir. 1004'te D'yi 2 SE dışına taşıyan budur.
- **Öteki protokoller etkilenmez:** p99 0,2–4,2 s; boşalma yalnız son birkaç saniyenin doğumlarına dokunur.

## Karar (K-239, yürütücü: "protokol düzeyinde etiket")

- **Kayıt:** `evre_metrikleri_kapilari.py::EVRE_YORUMLANAMAZ`. Kayıtlı protokol, kayıtlı olduğu maddenin (G1ç'nin D'si, G4ç'nin p99'u) hükmü dışında kalır; satırı basılır ve etiketlenir. Öteki maddeler onu saymaya devam eder. Ölü kayıt kapıyı kırmızı yakar. JarmRout iki maddeyle, ölçülmüş sebebiyle kayıtlı.
- **Raporlama:** JarmRout'un M1 · M2 · M4'ü "yorumlanamaz"; `PDR_açık`ı "bulanık" etiketi ve sızıntısıyla raporlanır.
- **H2.c aynen kalır.** Bulanıklık ve boşalma JarmRout'un lehinedir: bu hücrede 290 s sonrası doğanlar çıkarılınca açık evre PDR'si 0,012–0,017 düşer. Karşılaştırma DESPARETE açısından tutucudur.
- **Kayıtlı çıktıların bugünkü hükümle yeniden değerlendirilmesi** (yeni `hukum` kipi; `hukum_evre.txt`):
  - ikinci kuyruğun G1ç ✓ · G2ç + G4ç ✓;
  - K-224'ün çıktıları (`denetim_duzeltme_2026-10-09/B3_*`) değişmeden ✓.
- **Testler:** `tests2/test_evre.py` (kayıtlı geçer · kayıtsız kalır · ölü kayıt kalır, iki kapıda).
- **Pencere notu:** trafiğin 320 s'de durması uzun bekleyişli protokolde son doğumları kayırır. Simülatör değişmez; bu ölçüm, pencere üçlüsünün Faz 6 duyarlılığına (SINANMAMIŞ, `04` §9; açık karar §10) not düşüldü.

## Donma — dört şart tuttu

| şart | |
|---|---|
| A sağlandı | ✓ |
| B'nin dört anatomisi geçti | ✓ |
| iki protokolde U1-U | ✓ (kopya kuralıyla; `hukum_U1.txt`) |
| G1ç ile G2ç + G4ç | ✓ (K-239'un kaydıyla) |

`JarmRout-b` ve `OLSRv2-b` dondu. `tests2/test_donma.py` beş dosyaya bağlandı: `jarmrout.py` · `jarmrout_bicim.py` · `olsrv2.py` · `olsrv2_bicim.py` · `olsrv2_rfc5444.py`. Değerler ölçülen kopyayla birebir.
