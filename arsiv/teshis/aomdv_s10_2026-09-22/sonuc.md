# AOMDV entegrasyonu — S10 kilidi (22 Eylül 2026, `v2/04` K-148)

Küçük test dünyası (`tests2/test_kosum.py::_konfig`), tohum 1000, 60 s.
Üreticiler bu klasörde: `python aomdv_duman.py` (AODV ↔ AOMDV yan yana) ·
`python aomdv_hata.py` (tampona giriş sebebi ve kaynağa gelen RREP'in sonucu).

⚠️ "S10 ÖNCESİ" sütunu BUGÜNKÜ kodla yeniden üretilemez — kusur düzeltildi.
Sayılar koşumun kendi çıktısından, o anda kaydedildi (K-143'ün önce/sonra
tablolarıyla aynı gelenek).

| `bagimsiz-yok` | AODV-e | AOMDV, S10 öncesi | AOMDV, S10 sonrası |
|---|---|---|---|
| PDR | 0,5098 | 0,3233 | **0,5698** |
| `tampon_asimi` | 0 | 79 | **0** |
| `tampon_giris` | 978 | 3 960 | 519 |
| kaynağa gelen RREP rotayı ne önce ne sonra kullanılır yaptı | 0 | **184** | 0 |
| yedek yola geçiş | — | 143 | 228 |

| `statik-yok` | AODV-e | AOMDV (S10 öncesi ve sonrası BİREBİR) |
|---|---|---|
| PDR | 0,8488 | 0,8644 |
| kontrol çerçevesi | 2 968 | 2 559 |
| RREQ üretilen | 209 | 111 |
| yedek yola geçiş | — | 61 |

**Kusur:** RFC 3561 §6.11 her geçersizleştirmede sıra numarasını YEREL
olarak bir artırır. Bir komşunun rotası kopup (S8 ile) yeniden kurulup
yeniden kopunca yerel sıra hedefin gerçek sırasını geçer. Şekil 3 harfiyen
uygulanınca `seq_i > seq_j` olur ve hedefin kendi cevabı reddedilir; keşif
"başarılı" sayılıp kapanır, paketler tampon tavanından düşer. AODV'miz
geçersiz rotaya gelen her ilanı kabul ettiği için aynı şişmeden
etkilenmiyordu. **Düzeltme (S10):** geçersiz girdide Şekil 3'ün (1) dalı
işler — RFC 3561 ve `AODV` ile aynı kural.
