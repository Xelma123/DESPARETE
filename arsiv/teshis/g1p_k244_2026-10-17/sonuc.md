# G1-P kaldı — M4'ün yanlış tespitlerinin sebebi · sonuç

> 17 Ekim 2026 · ölçüt `beklenti.md` (commit `24985ea`, koşudan önce) · kopya `1163f81` · koşu 12:18–12:35, 17 dk (beklenti ~25 dk) · çıktılar `teshis.txt` · `teshis.jsonl` · `zaman.txt`

## 1 · Kimlik: tuttu

Dört protokolün tespit anları ve temiz evre ortalamaları G1-P kaydıyla aynı. Hayalet açılma 150 s; tespit pencereleri [196; 197) s.

| protokol | temiz ort · var (1 s kova) | eşik | tespit | koşudaki kopma beyanı |
|---|---|---|---|---|
| AODV-k | 22,25 · 25,93 | 42 | yok | 7 590 |
| OLSRv2 | 3,54 · 5,79 | 16 | 47 s (17 beyan) | 1 321 |
| Babel | 0 · 0 | 0 | 47 s (1 beyan) | **1** |
| DESPARETE | 2,35 · 2,92 | 11 | yok | 903 |

## 2 · Babel: boş dağılımın yozlaşması (ölçüt 2)

- Babel koşunun tamamında tek bir kopma beyan ediyor: 1 → 31, 196,203 s.
- Temiz evrede beyan 0 olduğu için M4'ün boş dağılımı Poisson(0) ve eşiği 0. Bu tek beyan "tespit" sayılıyor.
- Hiç beyan etmeyen protokol M4'ün dışında (`beyan_etmiyor`; Babel 1000 böyle). Bir kez beyan eden protokol ise ilk beyanında tespit ediyor. Sebep protokolün davranışı değil, metriğin seyrek beyan eden protokoldeki sınırı.

## 3 · OLSRv2: kendi beyan kümelenmesi (ölçüt 3)

- 196. saniyede 17 kopma beyanı var; eşik 16, yani bir fazla.
- [194; 198) s içinde 32 ayrı bağ beyan ediliyor; temiz ortalama saniyede 3,5. Beyanlar 27, 22, 9, 10, 13, 18 ve 28 numaralı düğümlerin çevresinde toplanıyor.
- Babel'in tek bağıyla (1–31) **ortak bağ yok.** Ölçüte göre OLSRv2'nin tespiti kendi beyan kümelenmesinden geliyor. İki protokolün aynı saniyeye düşmesi bu verilerle açıklanmıyor.
- Betimleyici: AODV aynı aralıkta 83 beyan veriyor; temiz ortalaması saniyede 22, yani olağan hızında. Bunların 12 bağı OLSRv2'ninkilerle ortak. DESPARETE 13 beyan veriyor, 1 bağı ortak. AODV'nin hızı yüksek olduğu için ortaklık bir ortak olayın kanıtı sayılmaz.
- OLSRv2'nin kümelenmesinin sebebi (Hello kaybı patlaması mı, kanal mı) ölçülmedi.

## 4 · Karar yürütücüde

G1-P'nin M4 maddesi 2/8; sınır 1/8.

- Babel'in yanlış tespiti metriğin sınırından geliyor.
- OLSRv2'ninki tek başına 1/8, sınırın içinde.

Kapıyı geçirmek bir kural değişikliği ister. O karara kadar evre metrikleri bir sonuç için kullanılmaz, AODV-k ile Babel donmaz.
