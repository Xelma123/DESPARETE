# K-244 kuyruğu — regresyon k244 · U1 (`AODV-k` · Babel, iki desen) · çizelgeli evre kapıları · G1-P — beklenti (ölçmeden önce)

> 14 Ekim 2026 · `v2/12` §1.1 adım 6f · kod K-244'ün commit'i (`AODV-k`: K-243 + karşılıksız RREP ve RERR'in iletim biçimi; Babel: `protokoller/babel*.py`) · dondurulmuş kopyadan (`kopya/`, commit'le birebir, `kopya_ozet.txt`) · `kuyruk.sh`. Simülatörün davranışı K-243'ten beri değişmedi (yalnız `sim2/kanal/cerceve.py`'de yorum): R = 0,0126 ve G3ç geçerli kalır, yeniden koşulmaz.

## Kuyruk (sırayla, tek ağır iş; ~12–16 sa)

1. **Regresyon** (~2 sa):
   - `uret k244`
   - `karsilastir k243 k244 --degisen <12 vaka> --yeni u-birincil-babel,u-bagimsiz-surekli-babel-dugum_kaybi`
   - mimari denetimi
   - Karşılaştırma temiz değilse (çıkış ≠ 0) kuyruk durur.
2. **U1, yere toplama:** `aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aodv,babel` (~3–5 sa)
3. **U1, eşler arası:** aynısı `--desen esler_arasi` (~3–4 sa)
4. **G1ç:** `evre_metrikleri_kapilari.py 1c` (~1,5–2 sa)
5. **G2ç + G4ç:** `evre_metrikleri_kapilari.py 2c` (~2–2,5 sa)
6. **G1-P:** `evre_metrikleri_kapilari.py 1p` (~45 dk)

Süreler önceki koşulardan (K-224: üç protokolle U1 6 sa · 4 sa 15 dk; K-239: kapılar). Babel'in birincil hücre regresyon vakası tek süreçte 357 s sürdü.

## 1 · Regresyon k243 → k244

**Değişmesi gereken 12 vaka** (`--degisen`; her biri geçerli olmalı: `korunum_tamam` · `mutabakat_tamam`):
- `k-statik-surekli-aodv` · `k-statik-surekli-aomdv` · `r-referans-statik-surekli-aodv` · `t-statik-surekli-aodv-dugum_kaybi`
- `u-birincil-aodv` · `u-birincil-aomdv` · `u-gorev-surekli-aomdv-esler_arasi`
- `u-statik-aldatici-aodv` · `u-statik-reaktif-aodv` · `u-statik-surekli-aodv-cephe_hatti` · `u-statik-surekli_darbeli-aodv` · `u-statik-taramali-aodv`

Sebep: G bayrağı ve karşılıksız RREP, RERR'in iletim biçimi. AODV `iletim_sonucu` taşıdığı için `sonuc_bildirimi` sayacı da değişir. AOMDV aynı yardımcıları devralır.

**Yeni iki vaka** (`--yeni`): `u-birincil-babel` · `u-bagimsiz-surekli-babel-dugum_kaybi`. Geçerli olmalı; teşhiste `gecersiz_paket` 0.

**Öteki 73 vaka bulgusuz** (`BIREBIR`). İzinli fark yalnız kod kimliği (`arac_hash`, `kosu_kimligi`, `protokol_hash`; araç otomatik geçer). `Konfig` ve köken defteri değişmedi, `--izin` yok.

Bu 73 vakadan biri metrikte ya da hamda değişirse ilan edilmemiş bir yola dokunulmuştur; sebebi bulunmadan devam edilmez (kuyruk durur). 12 vakadan biri değişmezse o da incelenir.

**Mimari denetimi:** `Yapisal ihlal YOK`, çıkış kodu 0.

## 2 · U1 (eşikler değişmez: statik 0,90 · hareketli 0,60, K-136; R 0,0126)

1. **U1-U** (keşif ya da rota kurulumu · çok atlamalı teslim · korunum · kâhin aşılmıyor) iki protokolde, iki desende ✅ olmalı.
   - Kâhin aşımı R'den büyükse K-192 (b) zarf prosedürü: `arsiv/teshis/aodv_sadakat_2026-09-30/aomdv_zarf_hucre.py <desen> <kol> <tohum> <protokol PDR> <ETX PDR>`. Zarfın içindeyse kayıt; zarfı da aşıyorsa yazılım hatası aranır.
   - U1-U kalırsa protokol donmaz, kusur aranır.
2. **U1-B, yere toplama** (birincil desen).
   - **`AODV-k`:** üç kayıtlı hücre (`statik-yok` 1000 · 1002, `bagimsiz-yok` 1000; açıklama K-207) kapıda kayıtlı oranla karşılaştırılır (DD-07). Fark R'yi aşarsa "KAYIT SAPTI" olur ve açıklama yeniden ölçülür. Yeni eşik altı hücre de aynı yoldan geçer.
   - **Babel:** eşik altı her hücre için koşullu adım.
   - Her iki durumda koşullu adım: `kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol <kol> --protokoller <protokol> --tohumlar <t>`. Açıklama yalnız anatomi dört şartın hepsini sağlarsa geçerli:
     - korunum ve mutabakat tamam; çelişki ve atfsız düşüş yok;
     - döngü/TTL düşüşü 0;
     - Babel'de `gecersiz_paket` 0;
     - en büyük düşüş sebebi protokolün mekanizmasıyla uyumlu (rota yok · `rota_gecersiz` · iletim başarısızlığı).
   - Açıklanan hücre `ACIKLANMIS_DUSUK_REFERANS`a ve `KAYITLI_ORAN`a sürüm etiketiyle (`AODV-k` · `Babel-a`) girer.
   - Şartlardan biri tutmazsa kusur aranır, protokol donmaz.
3. **Eşler arası keşifseldir:** düşük hücreler açıklanmamış bulgu kalır, donmayı durdurmaz (K-218). AODV'nin eşler arası kâhin aşımı kaydı (`statik-yok` 1001, AODV-j 1,0002) yeni oranla yargılanır.

## 3 · Çizelgeli evre kapıları — ölçüt değişmez (`v2/08` §08)

Rakip kümesi AODV · OLSRv2 · Babel · DESPARETE; tohumlar 1003 · 1004.
- **G1ç:** M4 yanlış tespit ≤ 1/8 koşu · M1 kol ortalaması 2 SE dışında ≤ 1/4 protokol · D iki tohumda da dışarıda kalan protokol yok.
- **G2ç + G4ç:** kâhinin M1'i etkili ve D'si boş kolunkine göre 2 SE içinde; her protokolde p99 < açık süre.
- JarmRout'un `EVRE_YORUMLANAMAZ` kaydı koşulmayan protokolün kaydıdır, ölü sayılmaz.
- Kalan kapı Faz 5'ten önce teşhis edilir; yeni bir protokol yüzünden kalırsa sebep ölçülür ve yürütücüye bildirilir.

## 4 · G1-P — ölçüt K-196

Referans dünya `statik-yok`, yere toplama, AODV · OLSRv2 · Babel · DESPARETE × 1000 · 1001, tam pencere.
- M4 yanlış tespit ≤ 1/8.
- M3 ≠ 0 ≤ 1/8.
- M1 2 SE dışında ≤ 1/4 protokol.

## Donma (yeni K kaydı)

Regresyon temiz · U1-U ✅ · U1-B yere toplamada temiz · G1ç, G2ç + G4ç ve G1-P geçti → `AODV-k` ve `Babel-a` donar. `tests2/test_donma.py`nin tablosunda `aodv.py` · `aodv_bicim.py` yenilenir, `babel.py` · `babel_bicim.py` eklenir. Ardından tam takım ve mimari denetimi.

## Öngörüler (ölçüt değil)

- **`AODV-k`:** karşılıksız RREP hedefe kaynağa giden rotayı erken kurar. Yere toplamada trafik tek yönlü olduğu için etkisi küçük, eşler arasında daha büyük olabilir. Tek-yayın RERR'in MAC yeniden denemesi kopma haberini daha güvenilir taşır. U1 oranlarının yönü küçük ve vakaya bağlı.
- **Babel:**
  - Statik kolda oranlar yüksek beklenir (ETX kayıplı bağdan kaçınır, proaktif).
  - Hareketli kollarda Hello 4 s, IHU tutma 42 s ve rota süresi 56 s değişime geç uyar; kopmada rota ancak Hello geçmişi boşalınca ya da geri çekmeyle düşer. Bazı hücreler 0,60'a yakın ya da altında olabilir.
  - Kontrol yükü OLSRv2'den biraz yüksek, AODV'den düşük beklenir. Birincil hücre dumanında 11 134 çerçeve; k243'te OLSRv2 8 229, AODV 32 741.
