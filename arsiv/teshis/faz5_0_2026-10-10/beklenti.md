# Faz 5.0 · Birincil hücrede kayıp anatomisi — beklenti ve karar kuralı (ölçmeden önce)

> 10 Ekim 2026 · `v2/12` §1.1 · denetim D-22 · birincil metrik `PDR_açık` (K-222). Bu dosya `arsiv/teshis/faz5_0_2026-09-30/beklenti.md`nin yerini alır; o beklenti hiç koşulmadı (K-215 öncesi kod, pencere PDR'si, yalnız DESPARETE ve kâhin). Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz.

## Soru

Karıştırıcı açıkken paket nerede ve neden ölüyor, ve DESPARETE v0.4.1 karıştırıcı açılınca neden kâhinden ve AODV'den daha çok kaybediyor?

## Başlangıç çizgisi (mevcut kayıtlardan, simülasyon yok)

Üretici `baslangic_cizgisi.py` (çıktısı `baslangic_cizgisi.txt`): G1ç ve G2ç kapı koşuları, bugünkü kod (K-224), tohum 1003 · 1004, tam pencere.

| kol | `PDR_açık` birincil | ikiz (hayalet çizelge) | karıştırma kaybı |
|---|---|---|---|
| kâhin | 0,734 · 0,827 | 0,902 · 0,955 | −0,168 · −0,128 |
| AODV | 0,401 · 0,536 | 0,602 · 0,698 | −0,201 · −0,161 |
| AOMDV | 0,348 · 0,521 | 0,585 · 0,782 | −0,238 · −0,261 |
| OLSR | 0,258 · 0,193 | 0,525 · 0,518 | −0,266 · −0,326 |
| DESPARETE | 0,476 · 0,538 | 0,757 · 0,786 | −0,281 · −0,248 |

Fark-içinde-fark (DESPARETE − rakip): AODV −0,080 · −0,086 · AOMDV −0,043 · +0,014 · OLSR −0,015 · +0,078 · kâhin −0,113 · −0,120. v0.4.1'in AODV'ye üstünlüğü karıştırmadan bağımsızdır; karıştırıcı açılınca DESPARETE AODV'den ve kâhinden daha çok kaybeder. Sessiz evrede ise toparlanır (G2ç: D −0,001 · +0,002; AODV −0,045 · −0,057). İki tohum bir iddia için yetmez; Faz 5'in başlangıç çizgisidir.

## Düzen

    PYTHONIOENCODING=utf-8 DESPARETE_DUNYA=referans_2026 py -3.11 -u kalibrasyon/kayip_anatomisi.py \
        --dunya referans_2026 --kol formasyon --aile derin_sizma \
        --protokoller desparete,aodv,aomdv,olsr,en_guvenilir_kahin \
        --tohumlar 1003,1004,1005,1006 --isci 8 --kayit <bu dizin>/kayit.json

- Birincil hücre (`formasyon · yere_toplama · derin_sizma · sürekli`, 10 W), tam pencere (ısınma 50 · açılma 150 · ölçüm sonu 320 · koşu 350 s), geliştirme tohumları 1003–1006. 5 kol × 4 tohum = 20 koşu; uzun koşan kollar önce sıralı.
- Alet, kayıp anatomisinin doğum evresi ekiyle (10 Ekim; düşen paketin doğduğu evreye atıf). Ekin gerçek koşuda sınaması `duman_kisa.txt` (kısa pencere, 1003, beş kol; ölçüm değil, hiçbir karara girmez): beş kolda çelişki 0, atfsız düşüş yok, her evrede `doğan = teslim + Σ düşen` (kalan 0). Satırın `pdr_acik`ıyla çapraz denetim kısa pencerede yapılamaz (açılma pencerenin dışında, evre metrikleri tanımsız) — tam koşuda yapılır. Dumandan sonra yalnız `kalan`ın yazımı değişti (tamsayı sayımlardan; `-0.000` artığı).
- Dondurulmuş kopyadan (`kopya/`, bu beklentinin commit'iyle dosya özeti birebir: `kopya_ozet.txt`), kabuk betiğiyle, saatler `zaman.txt`e. Yanında başka ağır iş yok.
- Süre tahmini ~5 sa (±1): 8 işçide koşu başına DESPARETE ~2 sa, AODV ~2 sa, AOMDV ~1,8 sa, OLSR ~1,2 sa, kâhin ~0,9 sa (K-200 partisinin süreleri; 20 koşu ≈ 2,5 dalga).

## Tanımlar

- **Doğum evresi:** önce `[50; 150)` · açık · sessiz (karıştırıcının çizelgesi, `[150; 320)`). Pencerede doğan her paketin akıbeti doğduğu evreye yazılır: `doğan = teslim + Σ_sebep düşen + kalan`.
- **Karıştırmaya özgü kayıp, sebep başına:** `Δ_s = oran_s(açık) − oran_s(önce)`, oran doğana göre, 4 tohum havuzlanmış. `Σ_s Δ_s + Δ_kalan = −ΔPDR` (tam ayrışma). Ayrı ikiz koşusu gerekmez: ikizde açık ile önce arasındaki fark tohum başına ±0,03 içindedir (G1ç).
- **DESPARETE'nin fazladan kaybı:** `E_s = Δ_s(DESPARETE) − Δ_s(kâhin)`; ayrıca AODV'ye göre. Sebepler gruplanır:
  - **R · rota yok:** `rota_gecersiz` · `hedef_yok` · `tampon_asimi` (paket kullanılabilir bir rota beklerken öldü)
  - **İ · iletim:** `iletim_basarisiz` (seçilen bağda MAC vazgeçti)
  - **K · erişim:** `kuyruk_tasmasi` (kuyruk taştı; ED kilidinde susan verici ya da tıkanıklık)
  - **T · döngü:** `ttl`
- `E = −[ΔPDR(DESPARETE) − ΔPDR(kâhin)] = Σ_G E_G + E_kalan`; grubun payı `E_G / Σ_G max(E_G, 0)` (kalan, koşu sonunda yolda olan, gruplara girmez).

## Karar kuralı (4 tohum toplamı)

0. **Geçerlilik:** her koşuda korunum geçerli · doğum evresi çelişkisi 0 · atfsız düşüş yok (`dugum_kaybi` dışında) · aletin açık evre PDR'si satırın `pdr_acik`ıyla birebir · 1003 ve 1004'te `PDR_açık` G2ç'nin değerleriyle birebir (aynı kod ve konfig; değilse davranışın aynı kaldığı iddiası düşer, sebep aranır). Biri tutmazsa tablolar kullanılmaz.
1. `E` **< 0,05** ise fazladan kayıp bu tasarımla çözülemeyecek kadar küçüktür → hedef ve öncelik değişmez (5.1 → 5.3 → 5.4), bulgu yazılır.
2. **T payı ≥ %10** ya da DESPARETE'nin hop sınırı sayacı (`veri_hop_siniri`; Hop Limit 16, paket `hedef_yok` olarak düşer, formasyonda rota ≪ 16 atlama) **> 0** ise önce döngünün sebebi bulunur (uygulanabilirlik koşulu DESPARETE'yi döngüsüz tutmalı); mekanizma seçilmez. Dumanda sayaç 0.
3. Aksi hâlde payı **≥ %50** olan grup ilk hedeftir:
   - **R** → ilk mekanizma *ardılı karıştırılan alanın hızlı geçişi*: 5.4'ün önceden hazır yedek ardılı ve 5.1'in kanıtıyla erken kaçış. Alt ayrım `rota_gecersiz` anında alanın durumundan (açık evre; REPAIRING'de düşüş = tampon kotası dolu, UNREACHABLE = ulaşılamaz): kota taşması ≥ %50 → onarım tamponunun kotası (karıştırmaya özgü değildir, ikiz ölçütünü geçmesi gerekir); ulaşılamaz ≥ %50 → girişi açlıksa tur isteği, adaysızsa yedek ardıl. Öncelik önerisi 5.1 → 5.4 → 5.3, yürütücünün kararına sunulur.
   - **İ** → 5.1 ilk (karıştırma kanıtı maliyete); başarısız iletimlerin alıcısı açık evrede girişim/ed alanındaysa kaçınılabilir sayılır. Öncelik aynen.
   - **K** → kanal erişim kilidi. Yönlendirme yalnız trafiği ed alanındaki rölelerden çevirerek etkiler (5.1'in kanal doluluğu kanıtı). Kaynağı ed alanında olan paketin kaybı kâhinde de varsa fizik sınırıdır; Faz 5'in hedefinden çıkarılır.
   - Hiçbir grup %50'ye ulaşmazsa büyük paydan başlanır, ikincisi sıradaki mekanizma olur.
4. **Faz 5'in yön gösterici hedefi** (ön-kayıtlı hipotez değil): `E`'nin kaçınılabilir kısmının en az yarısını kapatmak ve fark-içinde-farkı AODV'ye göre sıfırın üstüne taşımak. Mekanizma başına ölçüt `v2/12` Faz 5'teki gibi kalır: birincil hücrede `PDR_açık` artışı ve karıştırıcısız kolda zarar yok.

Aynı tablolar taban protokoller için Aile 1'in betimlemesine girer (karar yok).

## Öngörü

- `E` ≈ 0,11 (fark-içinde-farkla tutarlı, ±0,03).
- **R baskın** (%50–75): DESPARETE'nin ardılı karıştırılınca alan onarıma girer; onarım 6 s'ye kadar sürer ve o sırada gelen paketler tampon kotasına ya da ulaşılamaz alana takılır. AODV ise MAC başarısızlığında hemen RERR ve yeni keşifle döner.
- İ ikinci (%20–40); K küçük, çünkü kâhin de aynı ed kilidini yaşar ve fark kâhine göre ölçülür. T ≈ 0.
- DESPARETE'nin açık evredeki veri kararlarında girişim/ed alanındaki ardılların payı AODV'ninkinden yüksek (kalite metriği karıştırıcı açılmadan önce iyi olan merkez bağları seçer).
- AODV'de fazladan kayıp (kâhine göre) küçük ve çoğunlukla İ.
