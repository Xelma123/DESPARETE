# Regresyon k220 → k223 — beklenen farklar (ölçmeden önce)

> 9 Ekim 2026 · ajan · K-222 (köken kovaları, analiz) ve K-223 (`OLSR-d` · referans dünyada `yeniden_deneme_siniri` 7 → 6 · kapsam metni · yeni evre vakası). Ölçüm dondurulmuş kopyadan (`arsiv/teshis/denetim_duzeltme_2026-10-09/kopya_a`).
> `py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k223` → `karsilastir k220 k223 --izin kapsam.rota_tamponu.kaynak,teshis.koken_kovalari --degisen r-referans-,u-,k-statik-surekli-olsr --yeni u-birincil-evre-` → `py -3.11 arsiv/teshis/regresyon_k223/denetle.py`

## k220'den beri satırı etkileyen değişiklikler (tam liste)

`git diff c187a28 -- sim2 protokoller` ve regresyon aleti:
1. `sim2/kanal/dunya.py` — referans dünyada `yeniden_deneme_siniri` 7 → 6 (yalnız referans satırları; eski dünya 4, değişmedi). MAC kodu değişmedi.
2. `protokoller/olsr.py` — §8.2.1 (`OLSR-d`); yalnız OLSR satırları.
3. `sim2/yapilandirma/kapsam.py` — `rota_tamponu.kaynak` metni (bütün satırlar).
4. `sim2/yapilandirma/kokenler.py` — kovalar: `gm_alfa` · `gm_hiz_sigma_ms` TÜRETİLMİŞ → SINANMAMIŞ, `gorev_jitter_hiz_ms` TÜRETİLMİŞ → KOL_TANIMI (K-222), `komut_akis_sayisi` TÜRETİLMİŞ → DÜNYA_TANIMI (K-223); öteki değişiklikler yalnız metin.
5. Yorum/metin: `dunya.py` · `desparete_bayrak.py` · `olsr_bicim.py` (beyan tablosu) · `kalibrasyon/kahin.py` — davranış yok.
6. Regresyon aleti: yeni vaka `u-birincil-evre-en_guvenilir_kahin`; `_kos`ta pencere birleştirme sırası (`{**pencere, **ek}`) — mevcut vakaların `ek`inde pencere anahtarı yok, sonuç aynı.

## Değişen (izinli ya da ilan edilmiş)

- **Bütün vakalar:** kod kimliği (`arac_hash` · `kosu_kimligi` · `protokol_hash`, otomatik) · `kapsam.rota_tamponu.kaynak` · `teshis.koken_kovalari` (yukarıdaki dört kayıt).
- **İlan edilmiş değişen vakalar (`--degisen`):**
  - 16 referans vakası (`r-referans-*` 3 · `u-*` 13): MAC her unicast'i etkiler; `u-birincil-olsr` ve `u-bagimsiz-surekli-olsr-dugum_kaybi` ayrıca §8.2.1. Hepsi **GEÇERLİ** olmalı. Farkın kaynağı tek: `denetle.py` iki dosyada bu vakaların `konfig` bölümünü karşılaştırır — tek fark `yeniden_deneme_siniri` 7 → 6 olmalı (ve `kimlik.kurulum_hash`).
  - `k-statik-surekli-olsr` (eski dünya, OLSR): §8.2.1 — değişebilir ya da birebir kalabilir; GEÇERLİ olmalı.
- **Büyüklük (yön değil):** referans satırlarında PDR farkı küçük beklenir (8 → 7 deneme: tek deneme başarısı 0,3 olan bağda atlama teslimi 0,942 → 0,918). Herhangi bir referans satırında |ΔPDR (pencere)| > 0,10 ise sebebi U1'den önce teşhis edilir.

## Yeni vaka (`--yeni u-birincil-evre-`)

`u-birincil-evre-en_guvenilir_kahin` (formasyon-sürekli · derin sızma · yere toplama · 1003 · ısınma 10 s · karıştırıcı 40 s · ölçüm 100 s · koşu 110 s). `denetle.py` sınar:
- GEÇERLİ; `metrikler.evre_cizelge_s == [15.0, 15.0]`;
- ölçüm penceresi 10–100 s, açılma 40 s; `pdr_temiz` · `pdr_acik` · `pdr_sessiz` · `sok_derinligi` dolu (None değil) ve `pdr_acik_n + pdr_sessiz_n` 40–100 s'de doğan paket sayısına eşit;
- `analiz/satir.py::ham_denetimi` her alanı tutuyor (`pdr_acik` · `pdr_sessiz` ham listeden ikinci gerçeklemeyle BİREBİR, K-222).

## Değişmemesi gerekenler

Eski dünyanın **63 vakası** (64'ten `k-statik-surekli-olsr` çıkınca): metrikler, korunum, ham, konfig ve öteki teşhis alanları BİREBİR. İzinli alanlar dışında her fark BULGU'dur.
