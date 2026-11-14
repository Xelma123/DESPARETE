# Faz 5-2 · DESPARETE ↔ Babel kayıp anatomisi — beklenti ve karar kuralı (ölçmeden önce)

> 14 Kasım 2026 · `v2/12` §1.2, 5-2'nin teşhis ölçümü (a) · K-252. Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz. Bu bir teşhistir, hipotez testi değildir; eşikler karar kolaylığıdır.

## Soru

DESPARETE v0.4.1 paketlerini Babel'e göre **nerede ve neden** kaybediyor: karıştırıcı hiç yokken (ikiz hücre) ve karıştırıcı açıkken (birincil hücre)? Babel'le farklardan hangisi ölçümle destekleniyor (`protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md` §8)?

## Başlangıç çizgisi (mevcut kayıtlardan, simülasyon yok)

K-244 kuyruğu, tohum 1003 · 1004 (`arsiv/teshis/rakipler_k244_2026-10-14/G1c.txt` · `G2c.txt`):

| | ikiz `PDR_açık` (hayalet çizelge) | birincil temiz evre | birincil `PDR_açık` | birincil p99 |
|---|---|---|---|---|
| kâhin | 0,902 · 0,955 | 0,893 · 0,964 | 0,748 · 0,844 | 0,5 · 0,2 s |
| Babel | 0,945 · 0,952 | 0,938 · 0,955 | 0,547 · 0,787 | 0,8 · 0,3 s |
| DESPARETE | 0,757 · 0,786 | 0,727 · 0,803 | 0,518 · 0,603 | 4,7 · 4,3 s |

Faz 5.0'da (K-243'ten önceki dünya, alet DD-11'den önce) DESPARETE'nin karıştırıcı açılmadan önceki 100 saniyesinde tohum başına 1 000'den fazla onarım bölümü sayılmıştı (`arsiv/teshis/faz5_0_2026-10-10/kayit.json`, `desparete_onarim.sayim`, `once|…`).

## Düzen

    # adım 1 · ikiz (karıştırıcısız)
    PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 \
        --kol formasyon --sinif yok \
        --protokoller desparete,babel,en_guvenilir_kahin \
        --tohumlar 1003,1004,1005,1006 --isci 8 --kayit <bu dizin>/kayit_ikiz.json
    # adım 2 · birincil
    PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 \
        --kol formasyon --aile derin_sizma \
        --protokoller desparete,babel,en_guvenilir_kahin \
        --tohumlar 1003,1004,1005,1006 --isci 8 --kayit <bu dizin>/kayit_birincil.json

- Hücreler: `formasyon · yere_toplama`, ikiz (`--sinif yok`) ve birincil (`derin_sizma · sürekli`, 10 W). Tam pencere (ısınma 50 · açılma 150 · ölçüm sonu 320 · koşu 350 s). Geliştirme tohumları 1003–1006. 3 kol × 4 tohum × 2 hücre = 24 koşu.
- Dondurulmuş kopyadan (`kopya/`, bu beklentinin commit'iyle dosya özeti birebir: `kopya_ozet.txt`), `kosu.sh` ile iki ayrı adımda; saatler `zaman.txt`e. Yanında başka ağır iş yok.
- Aletin gerçek koşuda sınaması `duman_kisa.txt` (kısa pencere, 1003, üç kol, iki hücre; ölçüm değil, hiçbir karara girmez).
- Karar kuralının hesabı `sonuc_hesap.py` (koşudan önce yazıldı; yalnız `kayit_*.json` okur).
- Süre tahmini ~6 sa (±1,5): adım başına ~3 sa. Dayanak: K-244 kuyruğunda 8 işçide koşu başına DESPARETE 1,3–1,5 sa, Babel 1,1–1,4 sa, kâhin 0,5–0,9 sa; anatomi kaydı koşuyu uzatır (Faz 5.0'da DESPARETE 1,9–2,4 sa).

## Tanımlar

- **Pencerede doğan paketin akıbeti:** `doğan = teslim + Σ_sebep düşen + kalan`. İkizde bütün pencere tek evredir (alet karıştırıcı yokken her paketi `once` sayar); birincilde `once` `[50; 150)` · `acik` · `sessiz`.
- **Gruplar** (Faz 5.0'la aynı): **R · rota yok** `rota_gecersiz` · `hedef_yok` · `tampon_asimi` · **İ · iletim** `iletim_basarisiz` · **K · erişim** `kuyruk_tasmasi` · **T · döngü** `ttl`.
- **Açık** `G = PDR(Babel) − PDR(DESPARETE)`, 4 tohum havuzlanmış: ikizde bütün pencere, birincilde açık evre. `G = Σ_g E_g + E_kalan`, `E_g = oran_g(DESPARETE) − oran_g(Babel)` (oran doğana göre). Grubun payı `max(E_g, 0) / Σ_g max(E_g, 0)`.
- **Karıştırmaya özgü kayıp** (birincil): `Δ = PDR(açık) − PDR(önce)`, kol başına, havuzlanmış; sebep başına aynı fark.
- **Bağ seçimi:** veri kararlarında seçilen bağın kâhin bandı (iyi ≥ 0,90 · orta 0,50–0,90 · kötü < 0,50) ve mesafesi (p50 · p90); başarısız iletimlerin bağ bandı ve mesafesi.
- **DESPARETE onarım bölümleri** (aletin tanımı, DD-11 düzeltilmiş): sayı · girişi (açlık / adaysız) · sonu (aynı tur / yeni tur, `+U` = arada ulaşılamaz) · süre (p50 · p90 · toplam) · `rota_gecersiz` anında alanın durumu (onarımda = kota dolu / ulaşılamaz).
- **Sayaçlar** (betimleyici, `teshis_toplam`): DESPARETE `alan.onarima_girdi` · `alan.ulasilamaz` · `alan.tur_artirildi` · `komsu.gecis_expired` · `protokol.tampon_kota_disi`; Babel `secim_degisti` · `geri_cekme` · `sira_istegi_uretilen` · `uygulanamaz_yoksayilan` · `sira_artirildi`.

Sınır: alet Babel için onarım bölümü saymaz; iki protokol düşüş sebepleri, bağ bantları ve sayaçlarla karşılaştırılır.

## Karar kuralı (4 tohum toplamı)

0. **Geçerlilik.** Her koşuda korunum geçerli · doğum çelişkisi 0 · atfsız düşüş yok (`dugum_kaybi` dışında) · birincilde aletin açık evre PDR'si satırın `pdr_acik`ıyla birebir · 1003 ve 1004'te birincil `PDR_açık` K-244 kuyruğunun G2ç değerleriyle birebir (aynı kod ve konfig; değilse sebep aranır). Biri tutmazsa tablolar kullanılmaz.
1. **İkizde açığın ana kalemi.** Payı ≥ %50 olan grup ana kalemdir; hiçbiri ulaşmazsa en büyük iki pay birlikte okunur.
   - **R ana kalem** → önce onarımla ilgili konular (komşuluk, döngüden kaçınma, yolu bırakma zamanı). Alt ayrım, onarım bölümlerinin girişinden:
     - açlık ≥ %50 → uygulanabilirlik kuralının sıkılığı ve tur isteğinin gecikmesi;
     - adaysız ≥ %50 → yedek komşuların hazır olmaması.
     - `rota_gecersiz` anında alan: onarımda (kota) ≥ %50 → bekletme kotası; ulaşılamaz ≥ %50 → onarımın uzunluğu.
   - **İ ana kalem** → önce bağ kalitesi. Alt ayrım, karar bağlarından: DESPARETE'nin orta + kötü payı Babel'inkinden ≥ 5 yüzde puan yüksekse "metrik kötü bağ seçiyor"; değilse "iyi bağda başarısızlık" (çarpışma, trafik yığılması, kontrol yükü).
   - **K ya da T payı ≥ %10** → önce sebebi bulunur (T için döngü: uygulanabilirlik kuralı döngüsüz tutmalı).
2. **Birincilde karıştırmaya özgü kayıp.** `|Δ(DESPARETE) − Δ(Babel)| < 0,03` ise "4 tohumda ayırt edilemedi" yazılır. Değilse farkın hangi grupta olduğu yazılır. Bu madde, karıştırmaya karşı mekanizmaların neyi hedefleyeceğinin girdisidir.
3. **Sonraki teşhis.** İkizde R payı ≥ %30 ise (b) ölçümü koşulur: v0.4.1'in `hedefli_canlilik` ve `onarim_edinimi` seçenekleri, ikizde, ayrı beklentiyle. Değilse (b) ertelenir ve bağ seçimine dönük bir teşhis tasarlanır.
4. **Kâhin** yalnız referanstır: iki protokolün kâhine oranı yazılır; Babel'in kâhini aşması K-248'in kuralıyla kayda girer, karar değiştirmez.

## Öngörü

- İkizde `G` ≈ 0,17 (±0,04).
- İkizde **R baskın** (pay %55–75), İ ikinci (%25–45), K ve T ≈ 0. Gerekçe: DESPARETE ardılını yitirince onarıma giriyor ve onarımda kota dışı paketi düşürüyor; Babel rotasını koruyor ve MAC başarısızlığına bakmıyor.
- DESPARETE'nin ikizdeki onarım bölümleri tohum başına 1 000'in üstünde; girişlerin çoğu **açlık** (≥ %60); çoğu aynı turda kısa sürede (p50 < 0,5 s) kapanıyor, kaybın çoğu `+U` ile biten uzun bölümlerden.
- `rota_gecersiz` anında alan: ikizde onarımda (kota) ≥ %50.
- Karar bağlarında iki protokolün orta + kötü payı birbirine yakın (fark < 5 puan); Babel'in karar mesafesi (p50) DESPARETE'ninkinden uzun değil.
- Birincilde Babel karıştırıcı açılınca DESPARETE'den daha çok kaybediyor: `Δ(Babel) − Δ(DESPARETE) ≤ −0,03`; Babel'in karıştırmaya özgü kaybı İ grubunda (rotayı koruyup kesik bağa göndermeyi sürdürüyor), DESPARETE'ninki R grubunda.
- Birincilde açık evrede `G` ikizdekinden küçük (0,05–0,15).
