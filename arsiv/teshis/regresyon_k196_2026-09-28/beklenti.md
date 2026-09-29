# Regresyon k186 → k196 · BEKLENTİ (koşudan önce)

Ajan, 28 Eylül 2026. Taban `ciktilar2/regresyon/k186.jsonl` (27 Eylül). Yeni: `k196`, dondurulmuş kopyadan, 8 işçi.

## k186'dan bu yana değişen kod
| değişiklik | kayıt | etkilemesi beklenen |
|---|---|---|
| sönümleme FIR ağırlık önbelleği | K-195 yan iş | HİÇBİR satır (bit-özdeş olmalı) |
| kâhin grafiği karıştırıcı çizelgesiyle yenilenir | K-195 | kâhin vakaları, açılma/çizelge geçişi dilim içine düşüyorsa |
| AODV §6.8 kara liste (AOMDV miras) | K-194 | AODV/AOMDV vakaları, RREP bağ katmanında başarısız olduysa |
| OLSR §13 varsayılan kapalı | K-196 | OLSR vakası (MAC vazgeçmesi olduysa) |
| evre SE kümelenmeye dayanıklı · M4 negatif binom | K-196 | yalnız evre metrikli 4 tam vaka (`f-`) |
| köken defteri +3 TÜRETİLMİŞ | K-193, K-195, K-196 | her satırda `teshis.koken_kovalari` TURETILMIS 62 → 65, öteki kovalar aynı |

## Beklenen farklar (önceden ilan)
- **Davranışı değişebilen vakalar** (`--degisen`, geçerli olmak zorunda): `k-statik-surekli-aodv` · `k-statik-surekli-aomdv` · `k-statik-surekli-olsr` · `r-referans-statik-surekli-aodv` · `t-statik-surekli-aodv-dugum_kaybi` · kâhin vakaları `c-` · `f-statik-surekli-en_guvenilir_kahin-tam` · `g-statik-surekli-en_guvenilir_kahin-yere_toplama` · `h-formasyon-surekli-en_guvenilir_kahin` · `i-statik-surekli-en_guvenilir_kahin-hava_eslik`.
- **İzinli alanlar** (`--izin`): `teshis.koken_kovalari` · `metrikler.sok_derinligi_se` · `metrikler.toparlanma_suresi_s` · `metrikler.tespit_gecikmesi_s`.
- **Yönü de önceden:** `sok_derinligi_se` yalnız BÜYÜYEBİLİR (max(AC, küme) ≥ AC); `toparlanma_suresi_s` yalnız KISALABİLİR ya da `None`dan sayıya dönebilir (band yalnız genişler); `tespit_gecikmesi_s` koşum aletlerinde `None` kalır (beyan etmiyorlar).
- **Birebir kalması gerekenler:** geri kalan her şey — bütün `dogrudan_komsu`, `en_yakin_kimlik`, sınav protokolü vakaları ve `k-statik-surekli-desparete-yere_toplama` (DESPARETE AODV'den türemez). Burada tek bir fark, sönümleme önbelleğinin bit-özdeş OLMADIĞI demektir → bulgu.

## Tahmin
Kâhin vakalarının bir kısmı değişir (açılma dilim sınırına denk gelmiyorsa); OLSR vakası değişir; AODV/AOMDV vakalarında RREP başarısızlığı nadirse fark küçük ya da yok. Süre: k186 üretimi ~35–40 dk (8 işçi).

Üretici:
```
PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u kalibrasyon/regresyon_satirlari.py uret k196
PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u kalibrasyon/regresyon_satirlari.py karsilastir k186 k196 --izin teshis.koken_kovalari,metrikler.sok_derinligi_se,metrikler.toparlanma_suresi_s,metrikler.tespit_gecikmesi_s --degisen k-statik-surekli-aodv,k-statik-surekli-aomdv,k-statik-surekli-olsr,r-referans-statik-surekli-aodv,t-statik-surekli-aodv-dugum_kaybi,c-,f-statik-surekli-en_guvenilir_kahin-tam,g-statik-surekli-en_guvenilir_kahin-yere_toplama,h-formasyon-surekli-en_guvenilir_kahin,i-statik-surekli-en_guvenilir_kahin-hava_eslik
```
