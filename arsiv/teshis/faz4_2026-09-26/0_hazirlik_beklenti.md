# 4.0 · Hazırlık — beklenti (ölçmeden önce)

> 26 Eylül 2026 · ajan · K-183 (kâhin · dünya seçimi · araçlar) + K-184 (`analiz/`)

## Değişenler

1. **Kâhin grafiği** (`kalibrasyon/kahin.py`). Üç değişiklik; üçü de anahtara bağlı:
   - güç kipinde ED susturması → grafik yönlü;
   - hız uyarlamasında bağ ARF tabanında (1 Mb/s);
   - kesme mesafesi simülatörün duyma kümesiyle aynı (`duyanlar_menzili_m`; işlem kazancı kapalıyken girişim menziline birebir eşit).
2. **`kalibrasyon/dunya_secimi.py`** (yeni), `calisma_noktasi` ve `karistirici_gucu`:
   - `--dunya referans_2026`;
   - karıştırıcı aracında tohumlar havuzda, yeni `mesafe` bölümü.
3. **`sim2/kosum/kurulum.py::duyma_turetimi`** — saf yeniden düzenleme. Li zinciri ve `iki_cift` A5/C1'in (iki çift ayrıca yere toplamanın) alanlarını almamıştı ve **kurulamıyordu**; artık bu türetimi kullanıyorlar.
4. **`analiz/`** (yeni): Wilcoxon (NaN tuzağı kapalı), Holm, δ, GA, hüküm, güç, eşleştirme kimlik denetimi, ham ikinci gerçeklemesi.

## Tam takım

- 891 + 24 = **915 passed**:
  - K-183: kâhin 2, dünya 1, araç dumanı 2, Bianchi referans 3;
  - `analiz` 16.

## Regresyon `k182 ↔ k183`

**67/67 birebir.** Tek fark `arac_hash`; kod kimliği otomatik izinli.
- Eski dünyanın kâhin vakaları (`c-`, `f-`, `g-`, `h-`, `i-`) değişmez: kesme mesafesi ×1,0, susturma yok, çerçeve aynı.
- `r-` vakaları kâhin kullanmıyor.
- Kurulum türetimi aynı kayan nokta işlemlerini aynı sırayla yapıyor.

## Aynı regresyonda: referans alanı 35 km (K-185)

Öğrenci "ölçütü boşver, en gerçekçi olana önem ver" dedi; ajan 35 km'yi seçti (`a_calisma_noktasi_sonuc.md`). Bu değişiklik yalnız `r-` vakalarını etkiler → `--degisen r-referans-`. `r-` dışı vakalar yine birebir kalır.

`r-` öngörüleri (7 km → 35 km):
- **`statik-yok` tek atlama** (k182: 0,986): PDR sert düşer, **0,15–0,45** arasına. Rastgele çiftlerin yalnız ~%23'ü doğrudan komşu; kalanı `hedef_yok`.
- **`bagimsiz-surekli` tek atlama:** aynı nedenle düşük.
- **`statik-surekli` AODV** (k182: 0,212, ED kilidi): PDR **artar, > 0,40**.
  - 1 W'lık merkez karıştırıcının ED yarıçapı ~2,5 km. 35 km'lik sürüde yalnız birkaç düğüm susar.
  - Çok atlamalı rotalar karıştırıcının dışından kurulur.
  - `kuyruk_tasmasi` (susan düğüm kuyruğu) 451'den belirgin biçimde azalır.
- Üçü de `gecerli=True`.

## Duman

Li zinciri ve iki çift kurulur ve 1 s koşar. Önceden ikisi de `TypeError` ile kurulamıyordu; bunu düzeltmeden önce bir kez koşup kanıtlayacağım.
