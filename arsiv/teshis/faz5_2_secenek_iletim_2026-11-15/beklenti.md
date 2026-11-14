# Faz 5-2 · v0.4.1'in iki kapalı seçeneği ve iletim başarısızlığının sebebi — beklenti ve karar kuralı (ölçmeden önce)

> 15 Kasım 2026 · `v2/12` §1.2, 5-2'nin teşhis ölçümü (b) · dayanak `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` (karar kuralı madde 1 ve 3). Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz. Bu bir teşhistir, hipotez testi değildir; eşikler karar kolaylığıdır. Öngörüler duman koşusunun sonucu görülmeden yazıldı ve sonradan değiştirilmedi; karar kuralının 2. maddesinin ölçüsü duman koşusundan sonra düzeltildi (aşağıda, "Duman koşusundan sonra").

## Sorular

- **S1 · seçenekler.** v0.4.1'de kapalı duran iki mekanizma karıştırıcısız hücrede teslimi, "rota yok" kaybını ve komşuluk çalkantısını nasıl değiştiriyor?
  - `hedefli_canlilik`: ardıl ve en iyi iki uygulanabilir yedek, trafik yokken de yoklanarak canlı tutulur (K-165).
  - `onarim_edinimi`: onarıma giren röle olağan duyuruyu beklemek yerine yol ister.
- **S2 · iletim başarısızlığı.** İlk ölçümde DESPARETE'nin atlama başına başarısızlığı %6,5, kâhininki %3,3, Babel'inki %2,3 çıktı; başarısızlıkların %87'si kâhinin "iyi" dediği bağlardaydı. Fark seçilen bağın kendi kalitesinden mi, ağın öteki iletimlerinden mi geliyor? Kontrol trafiği kanalda iki protokolde ne kadar yer kaplıyor?

## Düzen

    # adım 1 · taban kollar
    PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 \
        --kol formasyon --sinif yok \
        --protokoller desparete,babel,en_guvenilir_kahin \
        --tohumlar 1003,1004,1005,1006 --isci 8 --kayit <bu dizin>/kayit_taban.json
    # adım 2 · seçenek kolları
    PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 \
        --kol formasyon --sinif yok \
        --protokoller "desparete~hedefli_canlilik,desparete~onarim_edinimi,desparete~hedefli_canlilik+onarim_edinimi" \
        --tohumlar 1003,1004,1005,1006 --isci 8 --kayit <bu dizin>/kayit_secenek.json

- Hücre: `formasyon · yere_toplama`, karıştırıcısız ikiz (`--sinif yok`). Tam pencere (ısınma 50 · ölçüm sonu 320 · koşu 350 s). Geliştirme tohumları 1003–1006. 6 kol × 4 tohum = 24 koşu.
- Kollar: **T** `desparete` (v0.4.1) · **C** `desparete~hedefli_canlilik` · **O** `desparete~onarim_edinimi` · **CO** ikisi birlikte · `babel` · `en_guvenilir_kahin`. Seçenek kolunda yalnız adı verilen alan açılır, ötekiler v0.4.1'deki gibidir (`kayip_anatomisi._desparete_kolu`, testi `tests2/test_kayip_anatomisi.py`).
- Alet eki (bu commit): veri denemesinin adreslenen alıcıdaki sonucu ve hızı, girişimsiz beklenen başarısızlık, simülatörün kendi sayaçları. Simülatör ve protokoller değişmedi; alet yalnız sayar.
- Dondurulmuş kopyadan (`kopya/`, bu beklentinin commit'iyle dosya özeti birebir: `kopya_ozet.txt`), `kosu.sh` ile iki ayrı adımda; saatler `zaman.txt`e. Yanında başka ağır iş yok.
- Aletin gerçek koşuda sınaması `duman_kisa.txt` (kısa pencere, 1003, altı kol; ölçüm değil, hiçbir karara girmez).
- Karar kuralının hesabı `sonuc_hesap.py` (koşudan önce yazıldı; yalnız `kayit_*.json` ve ilk ölçümün `kayit_ikiz.json`ını okur).
- Süre tahmini ~6,5 sa (±1,5): adım 1 ~2 sa 15 dk (ilk ölçümün ikiz adımı aynı kollarla 2 sa 12 dk sürdü), adım 2 ~4 sa (12 DESPARETE koşusu 8 işçide; ilk ölçümde koşu başına 1,7–2,1 sa; seçenekler kontrol trafiğini artırırsa uzar).

## Tanımlar

- **Gruplar** ilk ölçümdeki gibi: R `rota_gecersiz` · `hedef_yok` · `tampon_asimi` · İ `iletim_basarisiz` · K `kuyruk_tasmasi` · T `ttl`; oranlar pencerede doğan pakete göre, 4 tohum havuzlanmış.
- **Seçeneğin etkisi:** `ΔPDR(kol) = PDR(kol) − PDR(T)`, havuzlanmış ve tohum başına eşli; `ΔR`, `Δİ` aynı farkla.
- **Çalkantı sayaçları** (ağ toplamı, tohum ortalaması): silinen komşu `komsu.gecis_expired` · ardıl değişimi `alan.ardil_degisti` · onarıma giriş `alan.onarima_girdi` · yol isteği `protokol.solicit_gonderilen` · tur artışı `alan.tur_artirildi` · onarım bölümlerinde adaysız girişin payı.
- **İletim başarısızlığı** (bütün koşu, 0–350 s):
  - *atlama düzeyi:* gerçekleşen `f_a = iletim_basarisiz düşüşü / veri kararı`; girişimsiz beklenen `b_a = Σ (1 − p_atlama) / veri kararı`.
  - *deneme düzeyi* (yeniden denemeler dâhil, `d = mac_deneme`): gerçekleşen `f_d = 1 − mac_gonderim_basarili / d`; girişimsiz beklenen `b_d = Σ (1 − p) / d`.
  - `p` kâhinin tek deneme başarısıdır (veri ve onay; sönümleme dâhil, öteki iletimlerin girişimi hariç, ARF tabanında), karar ya da deneme anının 5 saniyelik diliminde; `p_atlama = 1 − (1 − p)^7` (yeniden deneme sınırı 6).
  - *fazla* `= gerçekleşen − beklenen`: bağın kendi kalitesinin açıklamadığı kısım.
  - *deneme başarısının çarpanları:* gerçekleşen `g = 1 − f_d`, girişimsiz beklenen `g0 = 1 − b_d`, ağın öteki iletimlerinden sağ çıkan pay `k = g / g0`; yani `g = g0 · k`.
  - *adreslenen alıcıdaki sonuç*, denemeye oranla: başarılı · yarı çift (alıcı o an gönderiyordu) · meşgul (alıcı başka çerçeveye kilitliydi) · önbelge · gövde · duyma dışı. Onay kaybı ayrıca: `mac_onaysiz_onay / d`.
  - *deneme hızı:* hız uyarlamasının (ARF, K-177) o komşu için seçtiği hız (1 · 2 · 5,5 · 11 Mb/s); kol başına denemelerin hıza dağılımı ve her hızda adreslenen alıcıdaki başarı.
- **Kanal yükü** (350 s, ağ toplamı): kontrol çerçevesi sayısı `kontrol_cerceve` · kontrol kanal süresi `kontrol_airtime_s` · veri kanal süresi `veri_airtime_s + veri_baslik_airtime_s` · toplam gönderim süresi `enerji_gonderim_s` (onaylar dâhil).

Sınır: kâhinin bağ ölçüsü 5 saniyelik dilimin ortalamasıdır; dilim içindeki değişimi ve hız uyarlamasının seçtiği hızı görmez. Beklenen değerin düzeyi bu yüzden bir alt sınırdır; kollar arası fark ve kâhin kolunun kendi fazlası referans alınır.

## Karar kuralı (4 tohum toplamı)

0. **Geçerlilik.** Her koşuda korunum geçerli · doğum çelişkisi 0 · atfsız düşüş yok. Aletin iki iç denetimi geçmiş olmalı (sayılan deneme `mac_deneme`ye, adreslenen alıcıdaki başarılı alım `veri_alim_hedefte`ye eşit; değilse koşu hata verir). **T, Babel ve kâhin kollarının pencere PDR'si ilk ölçümün `kayit_ikiz.json`ındaki değerlerle 12/12 birebir** (alet eki davranışı değiştirmedi). Seçenek kollarında `desparete_acik` listesi adı verilen alanı içerir, T'de içermez. Biri tutmazsa tablolar kullanılmaz.
1. **S1 · seçeneğin etkisi** (C, O, CO ayrı ayrı, T'ye göre):
   - **yararlı:** havuzlanmış `ΔPDR` ≥ +0,02 ve 4 tohumun en az 3'ünde pozitif;
   - **zararlı:** `ΔPDR` ≤ −0,02 ve en az 3'ünde negatif;
   - ikisi de değilse **"4 tohumda ayırt edilemedi"**.
   - Her kolda `ΔR` ve `Δİ` yazılır. Bu madde bir benimseme kararı değildir; komşuluk ve onarım konularındaki tasarım seçeneklerinin girdisidir:
     - C'de `ΔR` < 0 ve `Δİ` > 0 ise "yedeği canlı tutmak rota kaybını azaltıyor, bedeli yoklama trafiği" → canlılık kanıtının trafik üretmeyen yolu (dinleme) aranır;
     - C'de `ΔR` ≥ 0 ise "yedeği canlı tutmak rota kaybını azaltmıyor" → rota kaybının sebebi yedek yokluğu değil, uygulanabilirlik kuralıdır;
     - O'da solicit ve tur artışı sayaçları T'ye göre yazılır.
2. **S2 · DESPARETE ↔ Babel farkının ayrımı** (T ve Babel kolları):
   - Deneme düzeyinde `g(T) / g(Babel) = [g0(T) / g0(Babel)] · [k(T) / k(Babel)]`. Bağ seçiminin payı `π = ln[g0(T) / g0(Babel)] / ln[g(T) / g(Babel)]`.
   - `π` ≥ 0,5 → **"bağ seçimi"**: fark çoğunlukla seçilen bağların kendi kalitesinden; önce bağ maliyeti ele alınır.
   - `π` < 0,5 → **"bağın kendi kalitesi dışında"**: fark çoğunlukla `k`'de. Alt ayrım, deneme düzeyinde T − Babel farkının en büyük olduğu sonuç:
     - **meşgul** (alıcı başka çerçeveyi dinlerken gelen veri: gizli uç) ya da **yarı çift** (alıcı kendisi gönderiyordu) → ağın öteki iletimleri; önce komşuluk çalkantısı ve kontrol trafiği ele alınır;
     - **önbelge + gövde** (kilitlenen çerçevenin bozulması) → hıza göre okunur: fark en düşük hızın üstündeki denemelerde toplanıyorsa hız uyarlamasıyla bağ seçiminin etkileşimi (ardıl sık değişince hız o komşuya oturmuyor), en düşük hızda da sürüyorsa girişimle bozulma;
     - **onay kaybı** → dönüş yönü.
   - Deneme hızı (betimleyici): en düşük hızdaki deneme payı T ile Babel arasında ≥ 10 puan farklıysa "hız uyarlaması iki kolda farklı çalışıyor" yazılır.
   - Kanal yükü: T'nin kontrol kanal süresi Babel'inkinin ≥ 1,5 katıysa "belirgin yüksek", ≤ 1/1,5 katıysa "belirgin düşük", arası "benzer" yazılır. "Benzer" ya da "düşük" çıkarsa "kontrol trafiği kanalı dolduruyor" açıklaması tek başına desteklenmez.
   - Atlama düzeyi betimleyici: `f_a`, `b_a` ve ilk yazılan oran `B / F` (`F = f_a(T) − f_a(Babel)`, `B = b_a(T) − b_a(Babel)`) yazılır; `f_a`, bağımsız denemelerin vereceği `(1 − g)^7` ile karşılaştırılır.
3. **Kâhin** yalnız referanstır: aynı tablolar yazılır; kâhinin `k`'si, bağ ölçüsünün görmediği kaybın en iyi bağ seçimiyle ne kadar olduğunu gösterir.

## Öngörü

S1:
- **C:** silinen komşu en az %15 azalır, kontrol çerçevesi en az %10 artar, onarıma giriş azalır. `ΔR` −0,005 … −0,02, `Δİ` 0 … +0,02. Net `ΔPDR` −0,02 … +0,02: **ayırt edilemez.**
- **O:** yol isteği en az 10 kat, tur artışı en az 3 kat artar. Onarımların %96'sı zaten aynı turda 0,15 saniyede kapandığı için kazanç küçük, kontrol bedeli büyük: `ΔPDR` ≤ −0,02, **zararlı.**
- **CO:** O'ya yakın, **zararlı.**

S2:
- Girişimsiz beklenen atlama başarısızlığı küçük: `b_a` DESPARETE %0,3–1,5 · kâhin %0,1–1 · Babel ≤ %0,5. Gerçekleşen değerlerin (%6,5 · %3,3 · %2,3) çoğu üç kolda da "fazla"dır.
- `B / F` < 0,3 → **"bağın kendi kalitesi dışında".**
- Alt ayrımda T − Babel farkının en büyüğü meşgul ile önbelge + gövde toplamındadır; yarı çiftin payı farkın %20'sinden azdır.
- Bir atlama yedi denemenin hepsi başarısız olunca düşer; atlama başına %6,5 başarısızlık bağımsız denemelerle açıklanamaz (deneme başına %68 gerekirdi). Başarısızlıklar kümelidir: aynı atlamanın denemeleri birlikte başarısız oluyor. Deneme düzeyinde `f_d` DESPARETE'de %25–45.
- Deneme hızı: DESPARETE daha uzun bağ seçtiği için en düşük hızdaki deneme payı Babel'dekinden yüksektir (en az 5 puan).
- Kanal yükü (güven düşük): DESPARETE'nin kontrol çerçevesi sayısı Babel'inkinden fazla (1,2–2 kat), kontrol kanal süresi "benzer" (oran 1/1,5 … 1,5).

## Duman koşusundan sonra (ölçümden önce)

Duman koşusu (`duman_kisa.txt`: kısa pencere, tohum 1003, altı kol) aleti sınadı: çıkış 0, iki iç denetim altı kolda geçti, taban kolların kısa pencere PDR'si ilk ölçümün duman koşusuyla birebir (DESPARETE 0,7730 · Babel 0,8631 · kâhin 0,8681).

Aynı koşu kuralın 2. maddesinin ilk ölçüsündeki bir kusuru gösterdi. İlk yazılan ölçü atlama düzeyindeydi (`B / F`). Dumanda üç taban kolda da veri denemelerinin yarısından fazlası adreslenen alıcıda başarısızdı (başarı DESPARETE %38 · kâhin %42 · Babel %47; alıcı meşgul üçünde de %29–32). Denemelerin çoğu başarısızken atlama başarısızlığı deneme başarısızlığının yedinci kuvvetiyle değişir: deneme başına küçük bir bağ kalitesi farkı atlama düzeyinde katlanır, `b_a` ise bunu göremez (yedi denemenin yalnız bağ yüzünden başarısız olmasını sayar). Atlama düzeyindeki oran bu yüzden bağ seçiminin payını sistematik olarak küçük gösterir. Ölçü deneme düzeyine ve çarpan biçimine çevrildi (`π`); eşik (0,5) ve dallar aynı kaldı. İlk yazılan oran da sonuçta yazılır.

Öngörüler değiştirilmedi. `B / F` < 0,3 öngörüsü ilk ölçüye göre değerlendirilir; `π` için ölçümden önce yazılmış öngörü yoktur. Duman tek tohum ve 40 saniyelik penceredir; yukarıdaki sayılar ölçüm değildir, hiçbir karara girmez.
