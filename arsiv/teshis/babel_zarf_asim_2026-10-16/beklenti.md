# Babel zarfı aşıyor (eşler arası) — yazılım hatası araması · beklenti (ölçmeden önce)

> 16 Ekim 2026 · tetik: `arsiv/teshis/babel_zarf_esler_2026-10-16/sonuc.md`. Babel görev 1001 (+0,044), görev 1002 (+0,0006) ve formasyon 1001'de (+0,021) üç kâhinin zarfını aşıyor. Kural (o dizinin `beklenti.md`'si, commit `e0ab0b1`): *"yazılım hatası aranır (kâhin sızıntısı, sayım, korunum); Babel donmaz."*
>
> Betik `teshis.py`, donmuş kopyadan (`1163f81`).

## Ölçmeden önce bilinen

- **Sızıntı:** `protokoller/babel.py` yalnız `sim2.gozlem.*` ve `babel_bicim`'i içe aktarıyor. Mimari denetimi ihlalsiz.
- **Sayım:** paket defteri bir paketin iki kez teslimini ve doğmamış paketin teslimini reddediyor (`teslim_edildi`'de `dogrula`). U1'de korunum geçerli.
- **Kâhin grafiği:** `kalibrasyon/kahin.py` grafiği `dilim_suresi_s`'de bir yeniden kurar. Referans dünyada bu 10 s'ye kırpılır; karıştırıcısız kolda başka yenileme yok (K-195). Bağ kalitesi grafikte dilimin başındaki konumlardan ve yavaş kayıptan hesaplanır.

## Düzen

- **Koşular:** üç hücre × üç kol (Babel · ETX kâhini · en olası teslim kâhini). U1'in yapılandırması: eşler arası, referans dünya, tam pencere. 9 koşu, 5 işçi.
- **Eşzamanlılık:** AODV-k'nin döngü izinin yeniden koşusu (3 süreç) aynı anda; toplam 8 işçi.
- **Kayıt:** her koşuda paket başına doğum anı ve teslim kaydı, korunum raporu ve PDR.
- **Süre tahmini:** ~3,5–4 sa. Eşler arası hareketli koşular 40–125 dk sürüyor; 9 iş 5 işçide iki dalga.

## Ölçüt

1. **Kimlik:** her koşunun PDR'si kaydıyla 4 basamak aynı olmalı (Babel ve ETX kâhini U1'le, en olası teslim zarf koşusuyla); korunum geçerli olmalı. Tutmazsa düzen hatalıdır, yorumlanmaz.
2. **Sayım ve korunum kusur izi:** aşağıdakilerden biri, Babel'de yazılım hatasıdır. Hata düzeltilir, Babel'in U1'i ve regresyonu yeniden koşulur.
   - Babel'de kopya üretimi (`kopya_uretilen` > 0);
   - korunum geçersiz;
   - Babel'in doğan paket sayısı kâhinlerinkinden farklı (trafik aynı olmalı).
3. **Kusur izi yoksa: mekanizma** (betimleyici; iki aday ölçmeden önce yazıldı):
   - **M1 · kâhin grafiğinin bayatlığı:** zarf kâhininin teslim oranı dilim içi evreyle düşüyor, Babel'inki düşmüyor. Ölçü: beş kovanın sonuncusu ilkinden R'den (0,0126) fazla düşükse düşüyor sayılır.
   - **M2 · kâhinin düşme sebebi:** zarf kâhininin Babel'e göre fazla düşüşü hangi sebepte toplanıyor (`iletim_basarisiz` · `hedef_yok` · `rota_gecersiz` · `ttl`), toplamlardan.
4. **Karar:**
   - **Kusur izi var:** Babel düzeltilir (yeni K kaydı, U1, regresyon).
   - **Kusur izi yok:** bu hücrelerde ETX kâhini ve zarf üst sınır değildir; M1/M2 mekanizmayı söyler. K-192 (b) zarfı aşan hücreyi kayda almaz; kayıt kuralın değişmesini ister. Bu yüzden karar **yürütücüye** gider (öneriyle). Babel o karara kadar donmaz.

## Öngörü (ölçüt değil)

- **Sayım ve korunum** temiz çıkmalı: Babel kopya göndermiyor ve defter çift teslimi engelliyor.
- **M1:** hareketli kollarda düğümler 10 s'de ~130–170 m yer değiştirir (medyan 47–62 km/h). Bağ menzilinin kenarındaki bağlar için bu, grafiğin dilim sonunda bayat olması demek. Babel'in Hello'su 4 s'de bir.
- **M2:** kâhinin fazla düşüşü `iletim_basarisiz`'da toplanmalı (grafikte iyi görünen ama artık kötü olan bağlar).
