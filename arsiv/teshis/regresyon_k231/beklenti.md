# Regresyon k223 → k231 · uçtan uca kopya defteri (D-23 · K-231) — beklenti (ölçmeden önce)

> 11 Ekim 2026 · tetik: simülatöre kopya defteri eklendi (`sim2/ag/paket.py` · `gozlem/karar.py` · `cekirdek/korunum.py` · `olcum/paket_defteri.py` · `kosum/dugum.py` · `gonderim.py` · `kosu.py` · `teslim.py` · `kayip.py`; tanımlar `v2/13` §07). Mekanizma yalnız bir protokol `Karar.kopyalar` döndürünce devreye girer; regresyon matrisindeki hiçbir protokol döndürmez.

## Komutlar (dondurulmuş kopyadan, `kosu.sh`)

    py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k231
    py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k223 k231 --izin teshis.koken_kovalari

Süre ~45 dk (`uret`), karşılaştırma < 1 dk.

## Ölçüt

- **81/81 vaka bulgusuz** (`BIREBIR`, izinli farklar dışında). Farklar yalnız "her koşuda değişen" ve "kaynak koduna bağlı" sınıflarında (kod özeti ve onu içeren koşu kimliği).
- İzinli: `teshis.koken_kovalari` — K-225'te `gm_hiz_sigma_ms` DÜNYA TANIMI'na, `gm_alfa` DUYARSIZ'a geçti (k223'ten sonra; simülatörün davranışı değişmedi).
- Satırların `korunum` bölümünde `kopya_uretilen` · `kopya_bastirilan` alanı **yok** (kopya kullanılmadı).
- Biri tutmazsa kopya defteri davranışı değiştirmiştir; değişiklik geri alınmadan ya da sebebi bulunmadan devam edilmez.

## Kopya yolunun kendisi

Regresyon matrisi kopya yolunu sınamaz; sınayan `tests2/test_kopya.py` (4 test: karar kuralları · korunum geçişleri ve rapor · küçük ağda kaynakta kopyalayan sınav protokolüyle uçtan uca defter, mutabakat ve eşin protokole sorulmadan gitmesi · kopyasız koşuda satıra alan girmemesi). Ölçmeden önce koşuldu: dokunulan modüllerin testleriyle birlikte 310 + 11 geçti, mimari denetimi ihlalsiz. Kopya yolu regresyon matrisine JarmRout donarken onun vakalarıyla girer.
