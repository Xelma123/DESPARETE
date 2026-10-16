# AODV-k'nin U1 düşük hücreleri — kayıp anatomisi · beklenti (ölçmeden önce)

> 16 Ekim 2026 · tetik: AODV A/B sonucu (a) (`arsiv/teshis/aodv_k_ab_2026-10-15/sonuc.md` §5). Beklentisinin kuralı: *"düşük hücreler anatomiyle protokolün sınırı olarak açıklanır (K-207)"*. Betik `anatomi.sh`, donmuş kopyadan (`arsiv/teshis/rakipler_k244_2026-10-14/kopya`, `1163f81`; `aodv.py` · `aodv_bicim.py` · `kayip_anatomisi.py` ana dalla birebir).

## Hücreler (U1, yere toplama, referans dünya, karıştırıcısız, tam pencere)

| kol | tohum | AODV-k PDR | ETX kâhini | oran | eşik |
|---|---|---|---|---|---|
| statik | 1000 | 0,8441 | 0,9905 | 0,852 | 0,90 |
| statik | 1001 | 0,8445 | 0,9868 | 0,856 | 0,90 |
| statik | 1002 | 0,8079 | 0,9945 | 0,812 | 0,90 |
| bağımsız | 1000 | 0,3900 | 0,8204 | 0,475 | 0,60 |
| bağımsız | 1002 | 0,4802 | 0,8334 | 0,576 | 0,60 |
| görev | 1000 | 0,4451 | 0,9078 | 0,490 | 0,60 |
| görev | 1001 | 0,5172 | 0,8679 | 0,596 | 0,60 |

## Düzen

Kayıp anatomisi aleti üç kez, paralel çalışır (toplam 7 işçi, tek ağır iş):

- `--kol statik --tohumlar 1000,1001,1002 --isci 3`
- `--kol bagimsiz --tohumlar 1000,1002 --isci 2`
- `--kol gorev --tohumlar 1000,1001 --isci 2`

Hepsi `--dunya referans_2026 --sinif yok --protokoller aodv` ile koşar. Kâhin koşulmaz; değerleri U1 kaydından alınır. Süre tahmini ~1–1,5 sa.

## Ölçüt

1. **Kimlik:** yedi PDR U1 kaydıyla 4 basamak aynı olmalı ve korunum geçerli olmalı. Tutmazsa düzen hatalıdır, anatomi yorumlanmaz.
2. **Kusur izi:** TTL düşüşü (döngü) her hücrede üretilenin %1'inden az olmalı.
   - RFC'nin kendi kurallarından doğan geçici döngü mekanizmadır (K-205, K-207 madde 2). Bu eşik onun ölçeğidir; `AODV-g`de statik TTL düşüşü 4 ve 21 paketti.
   - Bir hücrede eşik aşılırsa o hücrenin döngü izi alınır (K-205'in yolu) ve AODV-k donmaz.
3. **Mekanizma (betimleyici):** her hücrede en büyük düşüş sebebi ve payı, karar bağlarının kâhin bandı (yeniden denemeli ve tek deneme) ve başarısız bağların bandı yazılır. Bu bilgi kayıt metnine girer. Sıralama iddiası yapılmaz, çünkü AODV'nin metriği atlama sayısıdır ve bağ kalitesini görmez.

## Sağlanırsa

Kimlik tutar ve kusur izi yoksa:

- Yedi hücre `ACIKLANMIS_DUSUK_REFERANS["aodv"]`a girer. Gerekçesi K-207 atfı, sadakat denetimi (42 kural, K-244), A/B sonucu ve bu anatomidir.
- `KAYITLI_ORAN["aodv"]` AODV-k'nin oranlarına güncellenir.
- AODV-j'nin üç yere toplama kaydı yerini AODV-k'ninkilere bırakır.
- Yere toplama kaydı `hukum` ile yeniden yargılanır; eşler arası kayıt U1 eşler arası bitince yargılanır.

## Öngörü (ölçüt değil)

- Statikte en büyük düşüş `iletim_basarisiz` ya da `rota_gecersiz` olmalı.
  - A/B'de titreşimin veri iletim başarısızlığını artırdığı görüldü.
  - Karşılıksız RREP ile kara liste ve RERR artıyor.
- Hareketli kollarda en büyük düşüş `rota_gecersiz` olmalı (K-224'teki OLSR ve AODV-j ile aynı yön).
