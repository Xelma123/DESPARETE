# Regresyon k232 → k236 · yeni rakipler JarmRout ve OLSRv2 (K-233 · K-235 · K-236) — beklenti (ölçmeden önce)

> 11 Ekim 2026 · tetik: Faz 4b'nin rakipleri yazıldı ve sadakat denetiminden geçti (`JarmRout-b`, `OLSRv2-b`); simülatör k232'den beri değişmedi. Matrise dört vaka eklendi (`kalibrasyon/regresyon_satirlari.py`, `REFERANS_VAKALARI`): JarmRout ve OLSRv2 birincil hücrede, JarmRout eşler arası hareketli kolda (keşif, RERR, kopya defteri, kaynak rotası), OLSRv2 düğüm kaybında (komşu ve topoloji demetlerinin dolması). Bu dört vakanın satırları iki protokolün regresyon tabanı olur.

## Komutlar (dondurulmuş kopyadan, `kosu.sh`)

    py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k236
    py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k232 k236 --izin teshis.koken_kovalari --yeni u-birincil-jarmrout,u-birincil-olsrv2,u-bagimsiz-surekli-jarmrout-esler_arasi,u-bagimsiz-surekli-olsrv2-dugum_kaybi

Süre ~50 dk (`uret`; birincil hücrenin iki yeni vakası ~15 dk'lık işler, havuzda paralel), karşılaştırma < 1 dk.

## Ölçüt

- **Eski 81 vaka bulgusuz** (`BIREBIR`, izinli farklar dışında). Farklar yalnız "her koşuda değişen" ve "kaynak koduna bağlı" sınıflarında; `kimlik.protokol_hash` bütün vakalarda (`protokoller/` paketi değişti).
- İzinli: `teshis.koken_kovalari` — K-233'te `rssi_olcum_sigma_db` ve `gps_dikey_sigma_m` DUYARSIZ'dan SINANMAMIŞ'a geçti (JarmRout RSSI ve konum okuyor). Her satırda `DUYARSIZ` 11 → 9, `SINANMAMIS` 3 → 5; öteki kovalar aynı.
- **Dört yeni vaka** yalnız k236'da (`--yeni`); her biri geçerli (`korunum_tamam` · `mutabakat_tamam`). JarmRout vakalarında `korunum.kopya_uretilen` > 0 (aynı paket iki yoldan, K-231); OLSRv2 vakalarında kopya alanı yok.
- Eski bir vaka tutmazsa yeni protokollerin eklenmesi ya da köken değişimi başka bir şeyi değiştirmiştir; sebebi bulunmadan devam edilmez.

## Ön koşu (ölçüt değil)

İki hareketli vaka tek başına koşuldu (çökme denetimi): JarmRout eşler arası 193 s, geçerli, `kopya_uretilen` 27 · `kopya_bastirilan` 21; OLSRv2 düğüm kaybı 16 s, geçerli. İki vakanın PDR'si çok düşük (0,064 · 0,008). Bu düzey dünyadan geliyor: bağımsız kol, 5. saniyede açılan sürekli 10 W karıştırıcı ve kısa pencere. Aynı vakada OLSR v1 0,000 veriyordu (k232). Regresyon vakaları başarım değil yol sınar; başarım U1'in ve birincil hücrenin işi.
