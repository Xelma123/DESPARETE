# Regresyon k236 → k243 · kalıcı görüş hattı, AODV'nin yeni sürümü, kapı sertleştirmeleri (K-242) — sonuç

> 14 Ekim 2026 · ölçüt `beklenti.md` (commit `e5cd1b7`, koşudan önce) · `kopya/` = `e5cd1b7` (147 dosya birebir, `kopya_ozet.txt`; `arac_hash` 1b1ba98f…) · `uret` 18:55–20:48 (112,4 dk; en uzun vaka `u-birincil-jarmrout` 4578 s, k236'da 1979 s) · çıktılar `uret.txt` · `karsilastir.txt` · `mimari.txt` · `eski_gorus_hatti.txt`

## Ölçüte göre

- **İlan edilen 18 vaka değişti ve geçerli** (korunum ve mutabakat tamam) ✓
- **Öteki 67 vakadan 66'sı bulgusuz** (`BIREBIR`; farklar yalnız kod kimliği ve izinli üç alan: `kimlik.kurulum_hash` · `konfig.a2g_durum_dilimi_s` · `teshis.koken_kovalari.OLCULMUS` 17 → 19) ✓
- **1 vaka beklenti dışında değişti** ✗ — `p-statik-surekli-dogrudan_komsu-karistirici_gercekci-cephe_hatti` (aşağıda)
- **Mimari denetimi:** `Yapisal ihlal YOK`, çıkış kodu 0 ✓ (çıkış kodu ayrıca koşularak okundu: `zaman.txt`'deki `cikis` değeri `kosu.sh`'deki `$?`'in `$(date …)`'ten sonra açılması yüzünden `date`'in durumudur, komutun değil; aynı kalıp k236'nın betiğinde de var. Sonraki koşu betiklerinde çıkış kodu komuttan hemen sonra bir değişkene alınır.)

Ölçüt tam sağlanmadı: beklentinin kuralı gereği sebep arandı.

## Beklenti dışı vaka

`p-statik-surekli-dogrudan_komsu-karistirici_gercekci-cephe_hatti` K-176'nın A6 vakasıdır: `karistirici_gercekci` açık, cephe hattının karıştırıcıları yerde. `KaristiriciTabani` yer–hava kanalını `karistirici_gercekci` ve yer platformu (`sabit_yer`, `arac`) birlikteyse kurar (`sim2/kanal/karistirici.py`); referans dünya şartı yoktur. Beklenti, yer–hava değişikliğinin ulaştığı vakaları yalnız referans dünyadaki birincil hücre vakaları olarak saymış, bu yolu atlamıştır. Değişiklik ilan edilen DD-01'dir; ilan edilmemiş bir yol değildir.

Doğrulama (`eski_gorus_hatti.py`, çıktı `eski_gorus_hatti.txt`): vaka bugünkü kodla, yalnız yer–hava kanalı k236'daki zaman dilimli modele (`e5cd1b7~1`, dilim 1 s) döndürülerek koşuldu. k236 satırına göre farklı 8 alan kaldı: beş kod/koşu kimliği alanı ve izinli üç alan. Metrik ya da ham alanda fark yok; `pdr_pencere` 0,3439 (k236) = 0,3439 (eski modelle), k243'te 0,3147. Vakadaki değişimin tek sebebi kalıcı görüş hattıdır.

Aynı anahtarla koşan öteki dört A6 vakası (`p-statik-aldatici-…`, `p-statik-aldatici-…-tasiyici_guc-…`, `p-statik-reaktif-…`, `p-bagimsiz-surekli-…`) birebir kaldı: varsayılan `tekli_merkez` tanım üretmez (`sim2/kanal/tehdit.py`), karıştırıcısı eski tek merkez nesnesidir ve sürünün orta irtifasında durur; yer–hava kanalı kurulmaz. (`tehdit.py`'nin tablosu bu aileyi "sabit yer" diye anıyor; nesne ise orta irtifada. Belge düzeltmesi Faz 5 öncesi belge işlerine eklendi.)

## Değişen vakalar (`pdr_pencere`, tek tohum; regresyon vakası, karşılaştırma değil)

| vaka | k236 | k243 | fark | NRL bayt (pencere) |
|---|---|---|---|---|
| `k-statik-surekli-aodv` | 0,8975 | 0,9117 | +0,0142 | 0,150 → 0,133 |
| `k-statik-surekli-aomdv` | 0,9167 | 0,9342 | +0,0175 | 0,080 → 0,078 |
| `r-referans-statik-surekli-aodv` | 0,0000 | 0,0000 | 0 | — |
| `t-statik-surekli-aodv-dugum_kaybi` | 0,8463 | 0,8079 | −0,0384 | 0,191 → 0,273 |
| `u-birincil-aodv` | 0,4750 | 0,4457 | −0,0292 | 0,387 → 0,411 |
| `u-birincil-aomdv` | 0,4741 | 0,4508 | −0,0234 | 0,347 → 0,366 |
| `u-gorev-surekli-aomdv-esler_arasi` | 0,0993 | 0,0993 | 0 | 1,072 → 1,126 |
| `u-statik-aldatici-aodv` | 0,0000 | 0,0000 | 0 | 3,327 → 2,499 |
| `u-statik-reaktif-aodv` | 0,6195 | 0,6228 | +0,0033 | 0,291 → 0,281 |
| `u-statik-surekli-aodv-cephe_hatti` | 0,6819 | 0,7610 | +0,0791 | 0,329 → 0,272 |
| `u-statik-surekli_darbeli-aodv` | 0,4371 | 0,3189 | −0,1182 | 0,295 → 0,373 |
| `u-statik-taramali-aodv` | 0,4546 | 0,4163 | −0,0383 | 0,340 → 0,346 |
| `u-birincil-desparete` | 0,5760 | 0,6294 | +0,0534 | 0,458 → 0,454 |
| `u-birincil-en_guvenilir_kahin` | 0,7679 | 0,8230 | +0,0551 | 0,026 → 0,026 |
| `u-birincil-evre-en_guvenilir_kahin` | 0,8137 | 0,8231 | +0,0094 | 0,026 → 0,028 |
| `u-birincil-jarmrout` | 0,4215 | 0,4048 | −0,0167 | 1,258 → 1,397 |
| `u-birincil-olsr` | 0,4699 | 0,5083 | +0,0384 | 0,120 → 0,126 |
| `u-birincil-olsrv2` | 0,5543 | 0,4766 | −0,0776 | 0,094 → 0,074 |
| `p-statik-surekli-dogrudan_komsu-karistirici_gercekci-cephe_hatti` | 0,3439 | 0,3147 | −0,0292 | 0,033 → 0,033 |

Ön koşudaki üç vakanın değerleri tam koşuyla aynı (`u-statik-surekli-aodv-cephe_hatti` 0,7610 · `u-birincil-evre-en_guvenilir_kahin` 0,8231; OLSRv2 düğüm kaybı vakası birebir).

AODV vakalarında yön vakaya göre değişiyor (beklentinin öngörüsü: titreşim yukarı, başarısız keşfin tamponunun düşmesi aşağı). Birincil hücrede kâhinler, DESPARETE ve OLSR yukarı, OLSRv2 ve JarmRout aşağı gitti; tek tohumda ve kısa pencerede bu farklar protokol kıyası için kanıt değildir, evre kapıları ve G1-P yeni kodla yeniden koşulacak (K-242).

## Sonuç

Ölçütün tek sapması ilan edilen değişikliğin beklentide sayılmamış bir vakaya ulaşmasıdır; sebep doğrulandı. Yeni regresyon tabanı: **k243**. Bundan sonraki koşu beklentilerinde etkilenen vakalar, değişikliğin kod yolunu açan anahtarlara göre (burada `karistirici_gercekci` ve yer platformu) aranarak sayılır.
