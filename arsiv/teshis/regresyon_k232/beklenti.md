# Regresyon k231 → k232 · kaynak rotası (K-232) — beklenti (ölçmeden önce)

> 11 Ekim 2026 · tetik: DSR ailesinin kaynak rotası simülatöre eklendi (`sim2/ag/paket.py` · `gozlem/pencere.py` · `gozlem/karar.py` · `kosum/dugum.py` · `gonderim.py` · `kosu.py`; tanımı `v2/13` §07, `v2/05` §3.3). JarmRout'un (Pu 2018) DSR'ye dayanan iletimine sadakat için: paket başlığında ara düğümler, gözlem penceresinde `PaketGorunumu.rota` (29 → 30 alan), çerçeve adres başına bayt kadar uzar, bayt yönlendirme ek yüküne sayılır. Mekanizma yalnız protokol `Karar.rota` verip `rota_adres_bayt` bildirince devreye girer; regresyon matrisindeki hiçbir protokol bunu yapmaz.

## Komutlar (dondurulmuş kopyadan, `kosu.sh`)

    py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k232
    py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k231 k232

Süre ~45 dk (`uret`), karşılaştırma < 1 dk. Taban k231 (kopya defteri; K-231'in regresyonu k223 ile birebir çıkarsa).

## Ölçüt

- **81/81 vaka bulgusuz** (`BIREBIR`); farklar yalnız "her koşuda değişen" ve "kaynak koduna bağlı" sınıflarında. İzin gerekmez (köken defteri k231'den beri değişmedi).
- Biri tutmazsa kaynak rotası davranışı değiştirmiştir; sebebi bulunmadan devam edilmez.

## Kaynak rotası yolunun kendisi

Regresyon matrisi sınamaz; sınayan `tests2/test_kaynak_rotasi.py` (4 test: karar ve paket kuralları · rotanın başlıkta görünmesi ve her veri iletiminde başlık baytının adres başına 4 bayt olarak birebir sayılması · rotalı çerçevenin hızda uzaması · rotasız protokolde başlık sayacı olmaması) ve gözlem yüzeyi testi (P6: paket alanı 6 → 7). Ölçmeden önce koşuldu: kopya, gözlem ve kontrol düzlemi testleriyle birlikte 83 geçti.
