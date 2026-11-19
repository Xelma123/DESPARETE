# Faz 5-3 · açlık teşhisi — çekirdeğin rota yokluğu kaybının kökü, karıştırıcısız ikizde — sonuç

> 19 Kasım 2026 · ölçüt `beklenti.md` (öngörüler ve karar kuralı commit `1947aaf`, dumandan önce; duman notu commit `8c9bbf7`) · koşu (`zaman.txt`): çekirdek 00:48–01:51 (1 sa 3 dk) · vtk0 01:51–02:40 (49 dk); tahmin 2,5–3 sa üst sınırdı · `kopya/` = `8c9bbf7` (164 dosya birebir, satır sonları normalleştirilerek; `kopya_ozet.txt`) · ham çıktı `teshis_*.txt`, kayıt `kayit_*.json` · karar kuralı `sonuc_hesap.py` → `sonuc_hesap.txt` · ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil). Babel ve kâhinin satırları teşhis (c)'nin kaydından.

## 0 · Geçerlilik ✓

- 16 koşunun hepsi kayıtta.
- Her koşuda korunum geçerli, doğum çelişkisi 0, atfsız düşüş yok.
- Aletin iç denetimleri 16 koşuda da geçti: bölüm = `rota.aclik`, kayıp = `rota.aclik` + `rota.zorunlu_gecis`, sebebi bulunamayan açlık 0, veri sebepli çıkış = `bag.veri_kotu`.
- `vtk0`'da veri tetiği kapalı ve `bag.veri_kotu` = 0.
- **Çekirdek kolu 8 tohumun 8'inde ilk ölçümün kaydıyla birebir:** PDR, pencere PDR'si, üretilen, teslim, sayaçların tamamı ve doğum evresine göre düşenler aynı. Kaydedici davranışa dokunmadı.
- Duman koşusunda çekirdek 1003 ilk ölçümün dumanıyla birebirdi (beklenti, son bölüm).

## 1 · S1–S2 — kök (karar)

Kayıp ağırlıklı, köke göre; 8 tohum ortalaması (tohum başına değerler `sonuc_hesap.txt`):

| ölçü | değer | tohum aralığı |
|---|---|---|
| **M1** bağ kökenli | **1,000** | 1,000 – 1,000 |
| **M2** yanlış alarm (bağ kökenlide kâhin bandı iyi) | **0,997** | 0,991 – 1,000 |
| M3 · kökte OLAĞAN ama uygulanamaz komşu | 0,922 | 0,844 – 1,000 |
| — bunun eski turlu olanı | 0,465 | 0,167 – 1,000 |
| M3b · kökte dışlanmış ama uygulanabilir komşu | 0,847 | 0,680 – 1,000 |
| M4 · zincir | 0,305 | 0,000 – 0,461 |

- **Kök sebep** (kayıp ağırlıklı): veri tetiği %99 (`bag:veri`). Selam eşiğinden gelen kökler %1'in altında.
- Sayıyla kök bölümlerin %94'ü veri tetiğinden başlıyor (koşu başına 167 / 176).
- Bağ kökenli köklerde ardıl bağının kâhin bandı: %100 iyi.

**Hüküm: bağ kökenli, yanlış alarm.** Bağ çıkış kuralları gerçekte iyi bağları düşürüyor. Karar kuralının 1. maddesi gereği sıradaki iş bağ çıkışının seçenekleri.

**Kâhin bandının anlamı** (beklentinin duman bölümü): kâhin girişimi dışarıda bırakır. "İyi", bağın yol kaybı ve sönümleme bakımından iyi olduğunu söyler. Rotanın taşıdığı veri tek alıcılıdır ve sekiz denemeyle girişimi çoğunlukla aşar.

## 2 · S4 — zincir

- M4 = 0,305 < 0,5. Kaybın çoğu zincirde değil kök bölümlerde düşüyor, bu yüzden ∞'un yayılma biçimi seçenek listesine girmez.
- Sayıyla bölümlerin %69'u zincir (yukarıdakinin ∞'undan açılıyor), ama kaybın yalnız %31'i onlarda.

## 3 · S5 — veri tetiği kapalı kol (karar)

| | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 | ort |
|---|---|---|---|---|---|---|---|---|---|
| çekirdek | 0,693 | 0,978 | 0,401 | 0,843 | 0,920 | 0,895 | 0,937 | 0,811 | 0,810 |
| **vtk0** | 0,959 | 0,971 | 0,892 | 0,937 | 0,969 | 0,953 | 0,946 | 0,939 | **0,946** |

`PDR(vtk0) − PDR(çekirdek)` = **+0,136**, 7/8 artı (1004 −0,008). Ayrışma kuralıyla **AYRIŞIYOR**.

**Hüküm: vtk0 önde.** Veri tetiği ikizde yararından çok zarar veriyor; tetik kuralı seçenek listesine girer.

Düzeltme: beklentide "T-3'ün tetik kuralı" diye geçen kural, `17`'de T-2'nin ikinci maddesindedir. Cezası T-3'e bağlı KK-01/11'dedir.

| | R kaybı | İ kaybı | bölüm / koşu (pencerede) |
|---|---|---|---|
| çekirdek | 0,139 | 0,049 | 679 |
| vtk0 | 0,003 | 0,052 | 28 (oran 0,03) |

## 4 · Betimleyiciler (çekirdek)

**Bölümler** (koşu başına, pencerede):
- 679 bölüm, 176 kök; zincir payı (sayı) 0,692.
- Süre: medyan 1,13 s · p90 3,92 s · ortalama 1,73 s. ≥ 2 s süren bölüm payı 0,268; kaybın 0,966'sı bu uzun bölümlerde.
- Bölümlerin 0,199'u eski ardılla, 0,857'si yeni turla bitiyor. 0,868'inde istek dizisi başlıyor.
- Kapsama 0,850: 7 tohumda 0,86–0,985; 1004'te 0,214, çünkü orada R grubu çok küçük (0,001).

**Bağ çıkışları** (OLAĞAN'dan, koşu başına, pencerede):
- 902 çıkış: `selam_asim` %38 · veri %34 · `selam_alim` %27. `df_bayat` ve silinme OLAĞAN bir bağı hiç düşürmedi.
- Ardıl bağındaki çıkışların %92'si veri tetiğinden.
- Ardıl bağı çıkışında kâhin bandı iyi olan pay 0,998.

| çıkış sebebi | kâhin bandı iyi | KÖTÜ'de kalış medyanı |
|---|---|---|
| `selam_alim` | 0,996 | 14,3 s |
| `selam_asim` | 0,997 | 12,2 s |
| veri | 0,998 | 22,6 s |

**Tur yayılımı** (pencerede):
- 75 artış; artışlar arası medyan 3,05 s.
- Sonraki artıştan önce yetişen düğüm payı 0,814; yetişme gecikmesi medyanı 1,60 s.

## 5 · Öngörülerle karşılaştırma

| öngörü | sonuç | |
|---|---|---|
| M1 0,60–0,85 | 1,000 | tutmadı (daha yüksek) |
| M2 0,45–0,75 | 0,997 | tutmadı (daha yüksek) |
| hüküm: bağ kökenli, yanlış alarm | bağ kökenli, yanlış alarm | tuttu |
| M3 0,50–0,80 · eski turlu payı 0,15–0,45 | 0,922 · 0,465 | tutmadı · tutmadı (sınırın hemen üstü) |
| M3b 0,20–0,50 | 0,847 | tutmadı |
| M4 0,50–0,75 | 0,305 | tutmadı (daha düşük) |
| kapsama 0,90–1,00 | 0,850 (1004 hariç 0,86–0,985) | tutmadı |
| bölüm 550–700 · kök 150–300 · zincir payı (sayı) 0,55–0,75 | 679 · 176 · 0,692 | tuttu |
| süre medyanı 0,4–1,2 s · p90 4–8 s · ≥ 2 s payı 0,15–0,35 | 1,13 · 3,92 · 0,268 | tuttu · tutmadı (hemen altı) · tuttu |
| ≥ 2 s bölümlerde düşen ≥ 0,95 | 0,966 | tuttu |
| eski ardılla 0,40–0,70 · yeni turla 0,30–0,60 · istek 0,60–0,90 | 0,199 · 0,857 · 0,868 | tutmadı · tutmadı · tuttu |
| bağ çıkışı 800–1100 | 902 | tuttu |
| selam %45–60 · veri %25–35 · `df_bayat` %5–15 · silindi < %10 | %65 · %34 · %0 · %0 | tutmadı · tuttu · tutmadı · tuttu |
| ardıl bağında veri payı 0,45–0,75 | 0,92 | tutmadı |
| ardıl bağında kâhin iyi payı 0,40–0,70; veride selamdan yüksek | 0,998; veri 0,998 ↔ selam 0,996–0,997 | tutmadı; fark yok denecek kadar küçük |
| KÖTÜ'de kalış: veri ≥ 10 s · selam 2–8 s | 22,6 s · 12,2–14,3 s | tuttu · tutmadı |
| tur artışı 60–80 · ara 2–4 s | 75 · 3,05 s | tuttu |
| yetişen 0,30–0,60 · gecikme 1–3 s | 0,814 · 1,60 s | tutmadı · tuttu |
| S5 +0,03 (−0,02 … +0,08), en olası "vtk0 önde" | +0,136, vtk0 önde | hüküm tuttu, büyüklük tutmadı |
| vtk0 bölüm oranı 0,4–0,8 · İ farkı +0,01 … +0,03 | 0,03 · +0,003 | tutmadı · tutmadı |

Öngörülerin yönü doğruydu, ama etkinin büyüklüğünü ve tek bir mekanizmada toplandığını çok küçük tahmin etmişim.

## 6 · Kuraldan sonra görülenler (karar girdisi değil)

`ek_hesap.txt`:

- **vtk0, ikizde Babel'in ve kâhinin üstünde.**
  - Pencere PDR'si: vtk0 0,946 · Babel 0,930 · kâhin 0,917.
  - vtk0 − Babel: +0,016, 8/8 artı. Ortalama 0,02 eşiğinin altında olduğu için ayrışma kuralıyla "8 tohumda ayırt edilemedi".
  - vtk0 − kâhin: +0,029, 7/8 artı. Kâhin yalnız referanstır, tavan değildir (K-248).
  - Gecikmenin p99'u 0,30 s (çekirdek 3,40 · Babel 0,23).
  - Kontrol kanal süresi 22,0 s, payı %6,1 (Babel 67,8 s · %14,7).
  - Bu yalnız karıştırıcısız ikizdir. vtk0 birincil hücrede ölçülmedi.
- **Veri tetiğinin çıkışları** (çekirdek, koşu başına, pencerede):
  - 309 çıkış; %98'i ardıl bağında.
  - %98'i sonra OLAĞAN'a dönüyor (KÖTÜ'de kalış medyanı 22,6 s; ceza 10 s'den başlıyor ve 60 s içinde yinelenirse 40 s'ye kadar katlanıyor).
  - Karıştırma kanıtı kapalıyken tetik doğrudan cezalı KÖTÜ'ye götürüyor (Y-4).
- **Selam da bağı olduğundan kötü gösteriyor.** Selam eşiğiyle çıkan bağlarda, çıkış anında:
  - selamın ölçtüğü `d_f · d_r` ~0,23–0,24;
  - kâhinin tek deneme başarısı ~0,71–0,76.

  Selam eşiği ardıl bağını seyrek düşürdüğü için (ardıl çıkışlarının %8'i) kayba katkısı küçük. Ama vtk0'da kalan açlıkların kökü bu. T-2'nin gerekçesi "selam küçüktür ve büyük veri paketinin kaybını olduğundan iyi gösterir" idi. Bu dünyada ve bu hücrede ise yayın selamı, bağı girişim yüzünden olduğundan kötü gösteriyor. Tek bir dünyanın sonucudur; genellenmez.
- **vtk0'da kalan açlıklar:**
  - Tohum 1005'te 155 bölüm ve 34 kök var, hepsi selam eşiğinden (PDR 0,892, R 0,011).
  - Öteki tohumlarda pencerede 5–19 bölüm var; 1003 dışında hiçbirinde bölümde paket düşmüyor.
