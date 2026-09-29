# 4.3 · U1 yeni kod hâlleriyle — beklenti ve karar kuralları (ölçmeden önce)

> 29 Eylül 2026 · ajan · öğrenci onayı ("dediğin her şeyi onaylıyorum", DESPARETE'nin eklenmesi dâhil) · dondurulmuş kopya `kopya/` (bu dizinde)
> Komut (kopyanın içinden, 8 işçi, yanında başka ağır iş yok):
> `PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aodv,olsr,aomdv,desparete`
> sonra aynısı `--desen esler_arasi --protokol aodv,olsr,aomdv`

## Ne ölçülüyor

Referans dünya · 4 kol (`statik/bagimsiz/gorev/formasyon-yok`) × tohum 1000–1002 · tam pencere (50 · 320 · 350 s) · `AODV-f` · `OLSR-c` · `AOMDV-b` · DESPARETE v0.4.1 (yalnız yere toplamada; bilgi amaçlı, donma kararına girmez). Kâhin desen başına bir kez koşulur, protokoller paylaşır (aracın 29 Eylül değişikliği; duman kesitinde eski araçla birebir: AODV 0,8255 · OLSR 0,4653 · AOMDV 0,8718 · DESPARETE 0,9018 · kâhin 0,9931).

27 Eylül'ün referans dünya U1 kayıtları bayat: kara liste (K-194), OLSR §13 kapalı (K-196), sönümleme blok üreteci (K-198) sonrasında koşulmadı.

## Ölçüt (değişmez: K-136, K-137, K-192)

- **U1-U** (defter kapanıyor · teslim var · kâhin aşılmıyor) geçmeli. Kalırsa protokol donmaz, yazılım kusuru aranır. Kâhin aşımı: çözünürlükten fazlaysa üç kâhinin zarfına bakılır (K-192 b).
- **U1-B**: statik ≥ 0,90 · hareketli ≥ 0,60. Eşik altı her hücre ölçümle açıklanır: kusur izleri (kuyruk/tampon düşüşü, döngü/TTL) dışlanır ve mekanizma düşük hücreleri sıralar (K-192 c). Araç: `kalibrasyon/kayip_anatomisi.py --sinif yok --kol <kol> --tohumlar <t>`. OLSR'ın düşük hücreleri "açıklanmış, sıralamasız" (K-196).
- **Donma kuralı:** üç taban protokolde U1-U iki desende de geçer ve yere toplamadaki eşik altı hücreler açıklanırsa kod hâlleri `AODV-f · OLSR-c · AOMDV-b` DONAR (K kaydı). Eşler arası keşifseldir; oradaki düşük hücre donmayı durdurmaz, bulgu olarak yazılır.

## Öngörü

| | statik | hareketli |
|---|---|---|
| AODV | 1000 eşik altı (eski kayıt 0,736; duman 0,831), 1001 geçer | 0,60–0,85, çoğu geçer |
| AOMDV | AODV'ye yakın, biraz üstü | AODV'nin biraz üstü |
| OLSR | eşik altı (eski 0,53–0,80; duman 0,469) | 0,40–0,65, çoğu eşik altı |
| DESPARETE | 0,85–0,95 | bilinmiyor |

Kâhin aşımı beklenmiyor. Statik kolda sönümleme donuk (K-198): statik hücreler tohum gerçekleşmesine çok duyarlı, 27 Eylül'ün sayılarından sapabilir.

## Süre

27 Eylül kayıtlarının koşu süreleri ÷ ~3,8 (K-198 hızlanması) → yere toplama (60 koşu) ~5–7 sa, eşler arası (48 koşu) ~4–6 sa. Her koşu bitince ara kayda (`ciktilar2/aodv_uygunluk/u1_ara_referans_2026_<desen>.jsonl`) yazılır; kesilirse aynı komut kaldığı yerden sürer.
