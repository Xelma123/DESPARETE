# Faz 4 kapanışı · regresyon `k198 → k203` — beklenen farklar (ölçmeden önce)

> 30 Eylül 2026 gece · ajan · U1 bittikten sonra, dondurulmuş kopyadan, yanında ağır iş yok.
> Komut: `py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k203` → `karsilastir k198 k203 --izin teshis.koken_kovalari --yeni u- --degisen <aşağıdaki üç vaka>`

## k198'den beri değişen

1. **Yorum temizliği** (`sim2/` + `protokoller/`): kod ağacı birebir (`yorum_denetci.py`, tek bilinçli fark `konfig.py`'deki bir hata MESAJI metni). Etkisi yalnız kod kimliği: `arac_hash` · `protokol_hash` · `kosu_kimligi` (KOD_KIMLIGI sınıfı, otomatik).
2. **Köken defteri yeniden yazıldı** (K-203): kova sayımları değişti → her satırda `teshis.koken_kovalari.*` → `--izin teshis.koken_kovalari`. Değişen kayıtlar: kova değişen 802.11b sabitleri (→ KAYNAK), dünya tanımları (→ DUNYA_TANIMI), eski dünyaya dayanan DUYARSIZ/ÖLÇÜLMÜŞ kayıtları (→ SINANMAMIŞ ya da TÜRETİLMİŞ), silinen dört alet sabiti, eklenen `REFERANS_VAKALARI`; yeni kova `DUNYA_TANIMI` alanı her satırda YENİ anahtar.
3. **Davranış değişikliği — B4** (`sim2/kosum/dugum.py::_guc_mesgul_bitisi_s`): gerçekçi karıştırıcıda (güç kipi) ED ile kilitli düğüm her zaman 10 ms sonra yeniden bakar (önce: sabit karıştırıcıda 1 s). Değişmesi BEKLENEN vakalar (güç kipi + gerçekçi karıştırıcı + sabit karıştırıcı):
   - `p-statik-aldatici-dogrudan_komsu-tasiyici_guc-karistirici_gercekci`
   - `r-referans-bagimsiz-surekli-dogrudan_komsu`
   - `r-referans-statik-surekli-aodv`
   ⚠️ Kilitlenen düğüm yoksa satır birebir kalabilir — bu da kabul (değişen DEĞİL diye raporlanır).
4. **Yeni vakalar:** 13 `u-` (referans dünya) → `--yeni u-`; ilk kez üretilir, tabanı `k203` olur.

## Değişmemesi gerekenler

- Eski dünyanın öteki bütün vakaları (`karistirici_gercekci` kapalı ya da geometrik kip) metriklerde, korunumda ve kurulum özetinde BİREBİR.
- `kurulum_hash` hiçbir vakada değişmez (`Konfig` alanı eklenmedi).
- Birincil hücre ve U1 bu değişikliklerden etkilenmez (hareketli karıştırıcı zaten 10 ms · U1 karıştırıcısız).

Kural: yukarıdakiler dışında her fark BULGU'dur; açıklanmadan taban değişmez.
