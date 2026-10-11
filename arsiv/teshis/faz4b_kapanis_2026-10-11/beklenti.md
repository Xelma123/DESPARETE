# Faz 4b kapanış ölçümleri — U1 (JarmRout · OLSRv2) ve çizelgeli evre kapıları — beklenti (ölçmeden önce)

> 11 Ekim 2026 · `v2/12` §1.1 adım 3 · kod `JarmRout-b` (K-233 · K-234) · `OLSRv2-b` (K-235 · K-236), U1 aracına ve çizelgeli kapılara yeni rakipler eklendi (`kalibrasyon/aodv_uygunluk.py` `PROTOKOLLER`; `kalibrasyon/evre_metrikleri_kapilari.py` `CIZ_PROTOKOLLER` = AODV · OLSRv2 · JarmRout · DESPARETE). **Önkoşul:** regresyon k236 bulgusuz (`arsiv/teshis/regresyon_k236/`). Simülatör K-224'ten beri değişmedi: R = 0,0126 ve G3ç (yalnız kâhinle koşar) geçerli kalır, yeniden koşulmaz.

## Kuyruk (`kuyruk.sh`, dondurulmuş kopyadan, ~12 sa)

1. `py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol jarmrout,olsrv2` (~4,5 sa)
2. aynısı `--desen esler_arasi` (~3,5 sa)
3. `DESPARETE_DUNYA=referans_2026 py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c` (G1ç, ~1 sa 45 dk)
4. aynısı `2c` (G2ç + G4ç, ~2 sa 20 dk)

Süreler K-224'ün koşumlarından (U1 üç protokolle 6 sa · 4 sa 15 dk); JarmRout'un keşif seli uzatabilir.

## U1 — ölçüt (eşikler değişmez: statik 0,90 · hareketli 0,60, K-136; R 0,0126)

1. **U1-U** (keşif · çok atlamalı teslim · korunum · kâhin aşılmıyor) iki protokolde iki desende ✅ olmalı. Kâhin aşımı R'den büyükse K-192 (b) zarf prosedürü (koşullu adım: `arsiv/teshis/aodv_sadakat_2026-09-30/aomdv_zarf_hucre.py <desen> <kol> <tohum> <protokol PDR> <ETX PDR>`): zarfın içindeyse kayıt, zarfı da aşıyorsa yazılım hatası aranır. U1-U kalırsa protokol donmaz, kusur aranır.
2. **U1-B, yere toplama** (birincil desen): eşik altındaki her hücre için koşullu adım `py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol <kol> --protokoller <protokol> --tohumlar <t>`. İki protokol de kaynağına kural kural sadık (K-234 · K-235 · K-236), bu yüzden eşik altı protokolün kendi sınırı sayılır (K-207). Bu sayım ancak anatomi şu dört şartın hepsini sağlarsa geçerli:
   - korunum ve mutabakat tamam; çelişki ve atfsız düşüş yok;
   - döngü/TTL düşüşü 0;
   - JarmRout'ta `rotasiz_paket` 0, OLSRv2'de `gecersiz_mesaj` 0 (teşhis);
   - en büyük düşüş sebebi protokolün mekanizmasıyla uyumlu (rota yok · `rota_gecersiz` · iletim başarısızlığı).

   Şartlardan biri tutmazsa kusur aranır, protokol donmaz. Açıklanan hücre `ACIKLANMIS_DUSUK_REFERANS`a sürüm etiketiyle (`JarmRout-b` · `OLSRv2-b`, U1 tarihi) girer, kayıt `hukum` ile yeniden değerlendirilir.
3. **Eşler arası keşifseldir:** oradaki düşük hücreler açıklanmamış bulgu kalır, donmayı durdurmaz (K-218 gibi).

## Çizelgeli evre kapıları — ölçüt (değişmez, `v2/08` §08)

- **G1ç:** M4 yanlış tespit ≤ 1/8 koşu · M1 kol ortalaması 2 SE dışında ≤ 1/4 protokol · D iki tohumda da dışarıda kalan protokol yok.
- **G2ç + G4ç:** kâhinin M1'i etkili ve D'si boş kolunkine göre 2 SE içinde; her protokolde p99 < açık süre.
- Kalan kapı Faz 5'ten önce teşhis edilir. Yeni bir protokol yüzünden kalırsa sebep ölçülür ve yürütücüye bildirilir.

## Donma (yeni K kaydı)

U1-U iki desende ✅ · U1-B yere toplamada temiz · G1ç ve G2ç + G4ç geçti → `JarmRout-b` ve `OLSRv2-b` **donar**. `tests2/test_donma.py`nin `DONMUS` tablosuna `jarmrout.py` · `jarmrout_bicim.py` · `olsrv2.py` · `olsrv2_bicim.py` · `olsrv2_rfc5444.py`nin özetleri girer. Ardından tam takım ve mimari denetimi.

## Öngörüler (ölçüt değil)

- **OLSRv2:** statik kolda oranlar eşiğin üstünde (DAT kayıplı bağdan kaçınır, durağan ağda topoloji tam). Hareketli kollarda TC aralığı (5 s), T_HOLD (15 s) ve DAT'ın 64 s'lik penceresi değişime geç uyar; bazı hücreler 0,60'a yakın ya da altında olabilir.
- **JarmRout:** statik kolda iki yol aynı paketi taşır, oran yüksek beklenir. Ama 40 düğümde yinelenen RREQ'ların yeniden yayını (makalenin C_hop kuralı) ve paket başına iki kopya kanalı yükler. Hareketli kollarda kaynak rotaları bayatlar (RERR yalnız MAC vazgeçince). Oranın yönü belirsiz.
