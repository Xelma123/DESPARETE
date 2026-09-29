# 4.1a · Çalışma noktası (alan) — sonuç

> 26 Eylül 2026 · ajan · beklenti: `a_calisma_noktasi_beklenti.md` (ölçmeden önce)
> Üretici (dondurulmuş kopyadan, `sim2` k182 ile aynı):
> - `python kalibrasyon/calisma_noktasi.py --dunya referans_2026 --bolum yaricaplar,alan_taramasi` → `a_calisma_noktasi.txt`
> - aynı komut + `35000 40000 …` → `a_calisma_noktasi_genis.txt`
> - aynı komut + `36000 37000 38000 39000` → `a_calisma_noktasi_ince.txt`
> - `--bolum zaman_ve_kol 7000 25000 30000 35000 40000` → `a_zaman_ve_kol.txt`

## Ölçülen

| alan | derece | 1 atlama | 2 atlama | ≥ 3 atlama | kopuk (30 tohum) | ölçüt |
|---|---|---|---|---|---|---|
| 5 km | 38,65 | %99,1 | %0,9 | %0,0 | %0 | geçer |
| **7 km (bugünkü referans)** | **37,43** | **%96,0** | %4,0 | **%0,0** | %0 | geçer |
| 10 km | 33,79 | %86,6 | %13,4 | %0,0 | %0 | geçer |
| 16 km | 24,54 | %62,9 | %37,1 | %0,0 | %0 | geçer |
| 20 km | 19,30 | %49,5 | %50,2 | %0,3 | %0 | geçer |
| 25 km | 14,50 | %37,2 | %57,9 | %4,9 | %0 | geçer |
| 30 km | 11,26 | %28,9 | %53,6 | %17,5 | %0 | geçer |
| **35 km** | **8,82** | %22,6 | %45,5 | **%31,9** | **%0** | **geçer** |
| 36 km | 8,37 | %21,5 | %42,6 | %35,8 | %0,2 | kalır |
| 37 km | 8,00 | %20,5 | %40,8 | %38,2 | %0,5 | kalır |
| 38 km | 7,72 | %19,8 | %39,4 | %40,3 | %0,5 | kalır |
| 39 km | 7,46 | %19,1 | %37,7 | %42,8 | %0,3 | kalır |
| 40 km | 7,01 | %18,0 | %35,0 | %46,2 | **%0,8** | **kalır** |

**Seçilen: 35 km** — 1 km'lik ince ızgarada kısıtı sağlayan en büyük alan; 36–40 km'nin beşi de kalır (eski dünyanın ızgara adımı %11, buradaki %3).

Karşılaştırma: eski dünyanın seçtiği nokta (1800 m) derece **8,67**, derin çift **%31,0**. Ölçüt ölçekten bağımsızdır; referans dünyada aynı topolojiyi 35 km'de buluyor.

**Yarıçaplar** (gölgelemesiz, sönümsüz): 1 Mb/s veride PER %10 → 8,9 km, PER %50 → 9,9 km; beacon PER %10 → 10,1 km.

**Zaman ve hareketli kol** (`a_zaman_ve_kol.txt`; 10 tohum × t = 50 · 175 · 320 s):

| alan | kol | derece | kopuk ort. | kopuk en çok | kopan tohum |
|---|---|---|---|---|---|
| 35 km | statik | 8,42 | %0 | %0 | 0/10 |
| 35 km | bağımsız | 7,66 | %0,83 | %5,0 | **4/10** |
| 40 km | statik | 6,78 | %0,99 | %9,9 | 1/10 |
| 40 km | bağımsız | 6,05 | %1,16 | %9,9 | 3/10 |

- 35 km'de bağımsız kolun fasılalı bölünmesi eski dünyayla aynı mertebede. Orada 1700 m'de bile 10 tohumun 3'ü kopuyordu (`calisma_noktasi` başlığı).
- Bu yüzden bölünme payı her satırda beyan edilir (K-132). Tablo Faz 4.1d'de referans dünya için yeniden ölçülür.

## Beklentiyle karşılaştırma

| madde | beklenti | ölçülen | |
|---|---|---|---|
| 1 Mb/s PER %10 yarıçapı | ≈ 7,4 km | **8,9 km** | ✗ — DBPSK aynı Eb/N0'da DQPSK'dan ~1,6 dB iyi; yalnız 3 dB'lik hız farkını saymıştım |
| 7 km'de derece | 25–35 | **37,4** | ✗ (üstünde) — aynı nedenle daha da yoğun |
| 7 km'de ≥ 3 atlama | ≈ %0 | %0,0 | ✓ |
| seçilen alan | 20–25 km | **35 km** | ✗ — L/r ≈ 3,4 oranı tuttu (35/3,4 ≈ 10 km etkin bağ); yanılan, etkin bağ uzunluğuydu |
| seçilen noktada derece · derin çift | 8–10 · %25–35 | 8,82 · %31,9 | ✓ |

## Yorum

- `v2/14` §3'ün "~6–8 km, derece ~8, geçide ≥ 3 atlama" resmi, 10 dB paylı nominal bağa (2 Mb/s'te 1,65 km) dayanıyordu.
- Simülatörün kanalında ise bağ 1 Mb/s'te ~9–10 km'dir: 20 dBm EIRP, serbest uzay (α = 2), σ 3 dB gölgeleme, K = 10 dB sönümleme, 7 yeniden deneme.
- 7 km'lik sürü bu yüzden neredeyse tam örgüdür. Bu, K-181'deki karıştırmasız tek atlama PDR'si 0,986 ile tutarlı.
- Onaylı ölçüt aynı topolojiyi (derece ~8,7, derin çift ~%31) **35 km**'de kuruyor.
- Plan (risk maddesi): "yeni dünya yönlendirmeye iş bırakmazsa alan ve N kaynaklı sürü geometrisi içinde ayarlanır; öğrenciye sorulur" → **karar öğrencide.**
