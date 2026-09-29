# Birincil hücre partisi · BEKLENTİ ve KARAR KURALLARI (ölçümden önce)

Ajan, 28 Eylül 2026. Öğrenci: *"her şey için onay veriyorum"* (pahalı koşular dâhil). `v2/12` Faz 4.3'ün kalanı + Faz 5.0.

## Düzen
Referans dünya, birincil hücre `formasyon · yere_toplama · derin_sizma · sürekli` (10 W), tam pencere (ısınma 50 · açılma 150 · ölçüm sonu 320 · koşu 350 s). Geliştirme tohumları. Alet `kalibrasyon/kayip_anatomisi.py` (açık/sessiz evre, K-197), dondurulmuş kopyadan, 8 işçi, yanında başka ağır iş yok. Sönümleme blok üreteciyle (K-198).

| kol | tohum | soru |
|---|---|---|
| `olsr` (OLSR-c) · `olsr_s13` (OLSR-b) | 1003–1006 | §13 karıştırma altında (K-196'nın açık maddesi) |
| `aodv` · `aodv@rota_tamponu_kapasitesi=256` · `aodv@rota_tamponu_omru_s=60` | 1003–1006 | rota tamponu duyarlılığı (İ-8c) |
| `aomdv` · `desparete` · `en_guvenilir_kahin` | 1003–1006 | kayıp anatomisi (Faz 5.0) |

8 kol × 4 tohum = **32 koşu = tam 4 dalga** (26 koşu da 4 dalga sürerdi; ek tohum bedava). İlk dalga §13 karşılaştırmasının 8 koşusu. Tahmini: tek süreçte ~66 dk/koşu (4 s'lik ölçümden, K-198); 8 işçide koşu başına ~2,5 kat → dalga başına ~3 sa → **~10–12 sa**.

## Karar kuralları (değiştirilmez)
Çözünürlük R = 0,023 (`cozunurluk.py`, eski dünya; referans dünyada yeniden ölçülmedi — beyan).
1. **§13:** tohum başına fark d = PDR(OLSR-c) − PDR(OLSR-b), ölçüm penceresi.
   - ort(d) < −R ve 4 tohumun ≥ 3'ünde d < 0 → **taban OLSR-b olur** (`s13=True` varsayılan; güçlü taban tutucu seçimdir).
   - ort(d) > +R ve ≥ 3'ünde d > 0 → OLSR-c kalır (kanıtlı).
   - aksi → OLSR-c kalır (RFC kuralı: MAY beyan edilir), fark "çözünürlük altında" diye beyan.
2. **Rota tamponu:** 64 / 30 s KAYNAK (ns-3 varsayılanı, K-198) — değer DEĞİŞMEZ. |Δ| ≤ R → duyarsız diye beyan; |Δ| > R → duyarlılık bulgusu (raporda eksen), tampon bütün protokollerde ortak olduğu için adillik bozulmaz.
3. **Anatomi:** karar yok; Faz 5 hedefleri (açık/sessiz evre PDR'si, bölge × sebep, kâhin − protokol farkı) buradan yazılır.

## Tahminler (sonuçtan önce)
- §13: eski dünyanın karıştırıcılı kısa vakası (−0,13) yönünde, ama referans dünyada karıştırmanın büyük kısmı ED kilidi (verici susar, MAC denemesi yok) → §13 tetiklenmesi azalır. Tahminim: |ort(d)| ≤ 0,05, yön belirsiz.
- Rota tamponu: 256 paket AODV'de |Δ| < R (tampon tepe doluluğu referans U1'de düşüktü); 60 s ömür etkisi küçük.
- Anatomi: sessiz evrede PDR temizin altında kalır (rota tazelenmesi 15 s'ye yetmez); en büyük kayıp sebebi `iletim_basarisiz` (girişim bölgesinde) ve `rota_gecersiz`; kâhin − protokol farkı ≥ 0,1.
