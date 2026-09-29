# OLSR'ın referans dünyadaki U1-B düşüklüğü — teşhis · beklenti (ölçmeden ÖNCE)

> 28 Eylül 2026 · ajan · öğrenci onayı: plan (K-192) — statik, karıştırıcısız, 30 dk bandında
> Alet: `kalibrasyon/kayip_anatomisi.py` (K-193 genişletmesi: tohum başına, denenen bağ ve kâhin bandı, bölge alıcıda, OLSR §13 geri alma sayacı, K-146 K1 bayat rota denetimi, ısınma ayrımı, yalnız teşhis kolu `olsr_s13siz`)
> Komut: `python -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol statik --protokoller olsr,olsr_s13siz --tohumlar 1000,1001,1002 --isci 6 --kayit <bu klasör>/tam.json`
> Dondurulmuş kopyadan koşulur (ana depoda iş sürüyor).

## Soru

U1 (K-191): OLSR statik yere toplamada kâhine oran 0,602 · 0,797 · 0,526 (tüm koşu PDR 0,5912 · 0,7953 · 0,5186). Uygulama kusuru mu, mekanizma mı?

## Duman (kısa pencere 50 s, tohum 1000 — ÖLÇÜM DEĞİL, hipotezi yönlendirdi)

- OLSR: `rota_gecersiz` %38,5 · `hedef_yok` %22,0 (hepsi ısınmada) · `iletim_basarisiz` %5,4 · `ttl` %2,8. Karar bağlarının %100'ü kâhine göre iyi (p_atlama ≥ 0,90). Simetrik olmayan ardıla karar 0/5713.
- §13: 102 bildirimin 100'ü medyan 0,41 s'de geri alındı (86 pakette, 14 süpürmede).
- §13'süz teşhis kolu: `rota_gecersiz` %33,1 — §13 ana sebep DEĞİL.
- Ağ toplamı 50 s'de: komşu kaybı ~1 000, histerezisin saydığı OLSR paket kaybı ~30 000, simetrik olmayan komşudan gelip atılan TC ~3 800.
- AODV aynı duman: `iletim_basarisiz` %15,9 · `rota_gecersiz` %13,6; başarısız bağların %42'si kâhine göre kötü, medyan 16,7 km (geçide giden uzun bağlar).

## Hipotezler (K-146'nın çerçevesi)

| # | hipotez | tür | öngörü |
|---|---|---|---|
| H1 | gri bölge — zayıf bağ seçimi | mekanizma | karar bağlarında kötü/orta bant belirgin; kayıp çoğu `iletim_basarisiz` |
| H2 | rota tablosu boşluğu — komşu çalkantısı (histerezis + §8.5'in 2-atlama silmesi) geçide rotayı aralıklı yok ediyor, OLSR tamponlamıyor | mekanizma (RFC'ye sadık) ya da kusur | kayıp çoğu `rota_gecersiz`, pencerede; bayat rota ihlali 0 |
| H3 | döngü | kusur adayı | `ttl` belirgin |
| H4 | tıkanıklık | mekanizma | `kuyruk_tasmasi` belirgin |
| H5 | §13'ün ters etkisi | beyanlı RFC seçimi | §13'süz kolda PDR belirgin yüksek |

## Öngörü (sayılar)

1. **Kimlik:** OLSR tüm koşu PDR'si U1 kaydıyla 4 basamakta aynı: 0,5912 · 0,7953 · 0,5186. Tutmazsa önce bu açıklanır.
2. **Baskın sebep `rota_gecersiz`:** üç tohumda da düşüşlerin ≥ %50'si; `iletim_basarisiz` ≤ %25'i; `hedef_yok` yalnız ısınmada; `ttl` ≤ düşüşlerin %5'i; `kuyruk_tasmasi` 0. → H2 sürer, H1/H3/H4 düşer.
3. **Sıra:** düşüş payı 1002 > 1000 > 1001 (PDR'den).
4. **Bağlar:** karar bağlarının ≥ %95'i iyi bantta; başarısız bağların çoğu iyi bantta (girişim/çarpışma, AODV'nin tersine).
5. **§13:** bildirimlerin ≥ %90'ı geri alınıyor, medyan < 1 s.
6. **H5:** §13'süz kolun PDR'si OLSR'dan |Δ| ≤ 0,05 (tohum başına); §13 ana sebep değil.
7. **Çalkantı:** ağ toplamı komşu kaybı 4 000–10 000 (koşu başına); sırası düşüş sırasıyla aynı (1002 > 1000 > 1001).
8. **K1:** simetrik olmayan ardıla karar 0.

## Okuma kuralı

- 2 + 8 tutar ve döngü izi yoksa: OLSR'ın kaybı rota tablosunun geçide aralıklı olarak boşalmasıdır. Bir sonraki adım bunun RFC'ye sadık davranış mı (histerezis, §8.5 silmesi, §10'un 2-atlama kuralı, tamponsuzluk) yoksa kodumuzun bir sapması mı olduğunu ayırmaktır: rota boşalma anlarının komşu kaybıyla eşleşmesi ve RFC maddeleriyle satır satır karşılaştırma.
- 2 tutmazsa açıklama yeniden kurulur ve beyan edilir.

## Süre bandı

Statik OLSR U1'de önbelleksiz 1 849–2 462 s sürdü; önbellekle ~×0,6, sarmalayıcılarla biraz fazla. 6 iş paralel → **20–35 dk**.
