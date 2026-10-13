# G1ç ve G4ç'nin JarmRout yüzünden kalması — teşhis (13 Ekim 2026)

> Tetik: Faz 4b ikinci kapanış kuyruğunda (`arsiv/teshis/faz4b_kapanis2_2026-10-12/`) çizelgeli evre kapıları yalnız JarmRout yüzünden kaldı. G1ç'de D'si iki tohumda 2 SE dışında (−0,029 · +0,035). G4ç'de p99 28–30 s, açık süre 15 s. Beklenti (C): "JarmRout yüzünden kalırsa sebep ölçülür ve yürütücüye bildirilir."
>
> Koşu teşhistir, karar kuralı yoktur. Simülatörün ve protokolün kodu değişmez. `kapi_teshis.py`, `evre_metrikleri_kapilari._ciz_is`in kendisini G1ç hücresinde (formasyon-yok · yere toplama · hayalet çizelge) 1003 ve 1004 tohumlarıyla koşturur; sarmalar yalnız sayar. Kopya `faz4b_kapanis2_2026-10-12/kopya` = d3fd674 (147 dosya; ana ağaçla birlikte 13 Ekim'de yeniden doğrulandı).

## Öngörü (koşudan önce)

1. **Birebirlik:** satırın alanları (`pdr_temiz` · `pdr_acik` · `pdr_sessiz` · `d` · `p99_s`) `G1c.txt`deki KAYIT'la birebir.
2. **G4ç — gecikme kuyruğu rota beklemesidir:**
   - gecikmesi ≥ 15 s olan teslimlerin ≥ %90'ı rota tamponundan geçmiş;
   - bu paketlerde bekleyiş payının medyanı ≥ 0,9;
   - yolun kendi p99'u < 5 s (aynı hücrede öteki protokollerin p99 aralığı);
   - keşif süresinin p99'u ≥ 15 s.
3. **G1ç — PDR durağan değil, sel çevrimleri yüzünden:**
   - 15 s pencere PDR'sinin SD'si binom SD'sinin ≥ 2 katı;
   - 60–90 s bloklarda ölçek oranı > 1,5 (bağımsız bloklar varsayımının üstünde);
   - 15 s PDR ile aynı penceredeki RREQ yeniden yayınının ilintisi ≤ −0,5.

## Sonuç (13 Ekim 2026, 11:57–17:17; `kapi_teshis.txt` · `kapi_teshis.json` · ham veri `kapi_teshis.json.ham_*.json`)

**1 · Birebirlik ✓.** İki tohumun satırı `G1c.txt`deki KAYIT'la 18 alanın 18'inde birebir.

**2 · G4ç — öngörü tuttu: gecikme kuyruğu rota beklemesi.**

| tohum | p99 | ≥ 15 s teslim | rota tamponundan | bekleyiş payı (medyan) | yolun p99'u | keşif süresi p99 · en çok |
|---|---|---|---|---|---|---|
| 1003 | 25,35 s | 222 | 222 (%100) | 0,956 | 4,13 s | 25,9 s · 106 s |
| 1004 | 30,18 s | 398 | 393 (%98,7) | 0,960 | 4,96 s | 27,1 s · 127 s |

Uzun gecikme yolda değil, rota tamponunda oluşuyor. Keşifler selin altında uzuyor: keşiflerin %3–4'ü 15 s'yi aşıyor (2 641'in 100'ü · 2 595'in 84'ü). Bekleyen paket ortak tamponun 30 s'lik ömrüne kadar tutuluyor. Teslimlerin yarıdan çoğu bir kez tampondan geçiyor (3 903 teslimin 1 738'i · 4 339'un 2 630'u).

**3 · G1ç — öngörü tutmadı; mekanizma sel çevrimi değil, eğilim ve pencere sonu boşalması.**

| ölçü | 1003 | 1004 | öngörü |
|---|---|---|---|
| 15 s SD / binom SD | 0,0292 / 0,0196 = 1,5 | 0,0345 / 0,0200 = 1,7 | ≥ 2 ✗ |
| blok ölçek oranı 60 · 90 s | 1,29 · 1,40 | 0,58 · 0,67 | > 1,5 ✗ |
| ilinti (15 s PDR, RREQ yeniden yayını) | −0,48 | +0,16 | ≤ −0,5 ✗ |

Ham veriden, evre çevrimlerine göre:

| | 1003 | 1004 |
|---|---|---|
| TEMİZ | 0,381 | 0,389 |
| açık çevrimler | 0,332 · 0,360 · 0,322 · 0,323 · 0,341 · **0,409** | 0,347 · 0,364 · 0,358 · 0,418 · 0,408 · **0,481** |
| sessiz çevrimler | 0,373 · 0,308 · 0,347 · 0,337 · 0,340 · **0,525** | 0,463 · 0,403 · 0,406 · 0,385 · 0,409 · **0,588** |
| D tam (2 SE) | −0,0285 (0,0228) | +0,0349 (0,0275) |
| D, 290 s sonrası doğanlar hariç | −0,0439 | +0,0245 |
| eğilim [50; 290) | −0,032 / 100 s | +0,003 / 100 s |

- **Pencere sonu boşalması (iki tohumda).**
  - Trafik üretimi 320 s'de durur, koşu 350 s'de biter (`Konfig`). Yük kalkınca sel söner: RREQ yeniden yayını 5 s kovasında ~9–11 binden 330 s'de 88–151'e iner.
  - Son 15 s'de doğan paketler rotayı söndürülmüş ağda bulur. Son 5 s kovasında doğanların PDR'si 0,525 · 0,588, öncesinde 0,29–0,47.
  - Son sessiz dönem [315; 320) bütünüyle bu bölgededir. 1004'te D'yi 2 SE dışına taşıyan budur; bölge çıkarılınca D +0,0245, tam pencerenin 2 SE'sinin (0,0275) içinde.
- **Eğilim (1003).** PDR koşu boyunca düşer; 15 s başına RREQ yeniden yayını 25,9 binden 30–32 bine çıkar. TEMİZ, sonraki dönemlerin referansı olarak durağan değildir. Boşalma bölgesi çıkarılınca D büyür (−0,044).
- **Öteki protokoller etkilenmiyor.** AODV, OLSRv2 ve DESPARETE'de p99 0,2–4,2 s; boşalmadan yalnız son birkaç saniyenin doğumları etkilenir ve D'leri içeride kalır.

**Hüküm.** İki kapının kalma sebebi ölçüldü ve protokolün kendi davranışıdır: uzun rota beklemesi ve yüke duyarlı sel. Yazılım hatası izi yok: satırlar birebir; aynı protokolün anatomilerinde korunum ve mutabakat tamam (`faz4b_kapanis2_2026-10-12/sonuc.md` B). Pencere sonu boşalması, `PDR_açık`ı yalnız JarmRout'ta ve onun lehine şişirir: bu hücrede 290 s sonrası doğanlar çıkarılınca açık evre PDR'si 1003'te 0,012, 1004'te 0,017 düşüyor. Dolayısıyla DESPARETE ↔ JarmRout karşılaştırması (H2.c) açısından tutucudur. Pencere üçlüsünün (ısınma · ölçüm · boşalma) duyarlılığı zaten Faz 6'nın SINANMAMIŞ borcudur (`04` §9; açık karar §10); bu ölçüm §10'a not düşüldü.
