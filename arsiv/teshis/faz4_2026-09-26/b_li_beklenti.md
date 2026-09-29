# 4.2 · Li replikasyonu referans dünyada — beklenti (ölçmeden önce)

> 26 Eylül 2026 · ajan · komut: `python -u kalibrasyon/li_replikasyonu.py --dunya referans_2026`

## Ölçüt (değişmez, `v2/09`)

H1: uzun zincirde uçtan uca verim / tek atlama verimi ≈ **1/7** (bant 0,10–0,20). Eski dünyada **0,0871, TUTMADI** (25 Eylül koşumu, `DEVIR.md` doğrulama listesi satır 11).

## `v2/14` §9'un öngörüsü (onaylı, 25 Eylül)

> İşlem kazancıyla girişim/iletim oranı düşer; oran 0,0871'den yukarı, banda doğru kayar.

## Ajanın ek değerlendirmesi — yazılışından sonra fark edilen karşı etki

`v2/14` öngörüsü yalnız ALIŞI (SIR) hesaba katıyordu. Referans dünyada taşıyıcı dinleme artık **güç kipinde**:
- önbelge sezme, alıcı kilidiyle −97 dBm'e kadar gider (1 Mb/s PLCP);
- nominal bağ aralığı 1664 m iken sezme menzili ~10 km'dir, yani zincirde **~6 atlama**.

Bu durumda düğüm, 6 atlama ötedeki iletimi de duyup erteler ve uzamsal yeniden kullanım AZALIR. Etkiler ters yönde:
- işlem kazancı → alış ötekini tolere eder → oran ↑;
- geniş sezme menzili → erteleme → oran ↓.

**Birincil öngörü:** oran **[0,05; 0,12]**. Sezme menzili baskın çıkar, `v2/14`ün "yukarı kayar" öngörüsü büyük olasılıkla **tutmaz**.

**Yanlışlanırsa:**
- Oran > 0,12 çıkarsa işlem kazancı baskındır; `v2/14` öngörüsü tutar.
- Her iki durumda H1'in tutmama nedeni duyma bölümüyle (`d`) ayrıştırılır.

## Sonuç (`b_li.txt`) — YANLIŞLANDI

- H1 = **0,0426** (bant 0,10–0,20) → TUTMADI.
  - Öngörüm [0,05; 0,12] ✗, altında.
  - `v2/14` öngörüsü ("0,0871'den yukarı") ✗, aşağı indi.
- Tek atlama 833 pkt/s; 2 atlamada 107 (0,128) — sert bir düşüş.
- Duyma menzili bölümü nedenin duyma menzili OLMADIĞINI gösteriyor: oran 2,0'da bile 0,049.

## Ek beklenti — ayrıştırma (`b_li_ayristirma.py`, ölçmeden önce)

**Şüphe:** ARF, çarpışmayla kaybolan çerçeveyi kanal hatası sanıp hızı 1 Mb/s'e düşürüyor. Çok atlamada çerçeveler 11 kat uzuyor. Literatürde bilinen bir ARF zaafı; K-177'de kaynak ns-3 ARF.

**Öngörü:**
- A8 − ARF (sabit 2 Mb/s, Li'nin kurulumu gibi) → H1 **0,08–0,15**.
- Güç kipi ve yayılım gecikmesi tek başına oranı çok değiştirmez.

**Yanlışlanırsa:** ARF'siz de < 0,06 çıkarsa neden güç kipi taşıyıcı dinlemedir (~6 atlamalık sezme menzili); o anahtar ayrıca kapatılır.

## Sonuç — ayrıştırma (`b_li_ayristirma.txt`)

| kol | tek atlama pkt/s | 11 düğüm pkt/s | H1 |
|---|---|---|---|
| A8 | 832,8 | 33,88 | 0,0407 |
| **A8 − ARF (sabit 2 Mb/s)** | 354,6 | 45,04 | **0,1270 — bantta ✓** |
| A8 − güç kipi | 832,8 | 21,39 | 0,0257 |
| A8 − yayılım gecikmesi | 840,9 | 34,22 | 0,0407 |
| A8 − ARF − güç kipi | 354,6 | 32,69 | 0,0922 |

- Öngörü (A8 − ARF → 0,08–0,15) ✓.
- **Li replikasyonu, Li'nin koşulunda (sabit hız) referans dünyada TUTUYOR** (0,127; eski dünyada 0,087 tutmuyordu).
- `v2/14` §9 öngörü 1 ("işlem kazancı ve güç kipiyle banda doğru") sabit hızda ✓. Güç kipi oranı yükseltiyor (0,092 → 0,127), aksini beklemiştim ✗.
- **H1'i bozan ARF.** Çok atlamalı çekişmede çarpışmayla kaybolan çerçeveyi kanal hatası sanıp hızı düşürür; uzun zincirin mutlak verimi de düşer (45 → 34 pkt/s). Bu ARF'nin literatürde bilinen zaafıdır. Bütün protokollere aynı MAC'le eşit etki eder; referans dünyada açık kalır, beyan edilir.
