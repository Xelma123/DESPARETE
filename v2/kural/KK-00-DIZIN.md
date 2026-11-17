# KK-00 · Kural kâğıtları — dizin, ayarlar, bayraklar

> Faz 5-3 (`12` §1.2). Kararlar `17`de (T-1…T-20); kural kâğıtları onları kurallara, formüllere ve başlangıç değerlerine çevirir. Kod bu kâğıtlardan yazılır; kod yorumları `KK-n` ve `T-n`e atıf verir. Değerler başlangıçtır, geliştirme tohumlarında (1003–1010) A/B ile ayarlanır. Güncel: 17 Kasım 2026.

## Kâğıtlar

| # | konu | kararlar |
|---|---|---|
| KK-01 | bağın durumu ve ölçüsü | T-2 · T-3 · T-7 · T-9 · İlke 2 |
| KK-02 | selam ve ara ilan | T-1 · T-16 · T-17 |
| KK-03 | karıştırma kanıtı | T-5 · T-6 · T-8 · T-10 |
| KK-04 | rota seçimi, döngüsüzlük, açlık | T-11 · T-12 · T-13 · T-14 · T-15 |
| KK-05 | bekletme ve komutun yolu | T-18 · T-20 |

Her kâğıtta: amaç ve sınıf · gördüğü · tuttuğu · kurallar · değerler · örnek · sınanması · kaynak.

## Başlangıç değerleri (tek yer)

| ad | değer | kâğıt | dayanak |
|---|---|---|---|
| `N` selam geçmişi | 16 | KK-01 | Babel'in geçmişi [4] |
| `ORNEK_EN_AZ` | 4 selam | KK-01 | yeni komşu ancak ölçülünce aday |
| `E_CIK` · `E_DON` | 4 · 3 (ETX) | KK-01 | MRHOF üst sınırı 4 [64]; iki eşik T-3 |
| `VERI_PENCERE` | son 8 veri çerçevesi, ≤ 10 s | KK-01 | T-2'nin veri örneği |
| `T_HATIRA` | 30 s | KK-01 | teşhis (d) S3: 32 s'de bant değişmiyor |
| `T_CEZA` | 10 s; 60 s içinde yinelenirse ×2, en çok 40 s | KK-01 | veriyle KÖTÜ'ye düşen bağın gidip gelmesini önler |
| `T_SILME` | 30 s hiç duyulmazsa | KK-01 | İlke 2; 15 s'lik karıştırmada silinmesin |
| `ZAMAN_ASIMI` | 1,5 × komşunun aralığı | KK-01, KK-03 | Babel'in katsayısı (`protokoller/babel_bicim.py`) |
| `I_MIN` · `I_MAX` | 0,5 s · 2 s | KK-02 | 3 kaçan selam × 2 s = 6 s < 10 s açık dönem (§7 madde 3) |
| `SELAM_ARASI_EN_AZ` | 0,5 s (= `I_MIN`) | KK-02 | T-17'nin sıklık sınırı; değişimler birleşir |
| `ILAN_ESIGI` | %15 | KK-02 | maliyet değişiminin "önemli" sayılması |
| `ED_ESIGI` | kanal meşgul payı ≥ 0,62 | KK-03 | teşhis (d): %80 yakalama, ikizde %0,035 yanlış alarm |
| `DUSUS_ORANI` | çözülen < 0,5 × kendi ortalaması | KK-03 | teşhis (d): girişimde 49 ↔ 99/s |
| `KAYIP_ESIGI` | selam kaybı ≥ 0,6 | KK-03 | teşhis (d): girişimde 0,69 ↔ temiz 0,44 |
| `GIRIS_SANIYE` · `CIKIS_SANIYE` | 2 · 3 ardışık saniye | KK-03 | T-10 |
| `SESSIZ_SELAM` | en az 3 ardışık beklenen selam; bağın kendi kaybıyla olasılığı < %1 olacak kadar | KK-03 | T-6; temizde selam kaybı 0,44 (teşhis (d)) |
| `MAC_ARDISIK` | 3 vazgeçme | KK-03 | teşhis (d): `n* = 3` |
| `GECIS_ORANI` | %10 | KK-04 | Ramachandran [54]; T-11 |
| `ISTEK_YINELEME` | 3 kez, 0,5 s arayla | KK-04 | Babel [4] |
| `ISTEK_ARA` | 5 s | KK-04 | açlık sürerse istek dizisinin yinelenmesi |
| `ISTEK_ATLAMA` | 8 | KK-04 | isteğin geçide doğru iletilme sınırı |
| `TUTMA_EN_COK` | 2 s (atlama başına) | KK-05 | T-18 |
| `IZ_TAZELIK` | 3 s | KK-05 | telemetri saniyede bir |

## Ablasyon bayrakları ve sınıflar (K-247: sınıf ve amaç ölçmeden önce)

| bayrak | kâğıt | sınıf | kapalıyken |
|---|---|---|---|
| `karistirma_durumu` | KK-01, KK-03 | karıştırmaya karşı | kanıt yok; bağlar yalnız ETX'le |
| `alici_bildirimi` | KK-03 | karıştırmaya karşı | selamdaki bit gönderilmez, okunmaz |
| `hatirlanan_kalite` | KK-01 | karıştırmaya karşı | kanıt kalkınca bağ yeniden ölçülerek döner |
| `veri_kotu_tetigi` | KK-01 | genel | ETX yalnız selamdan |
| `uyarlanir_aralik` | KK-02 | genel | selam sabit `I_MAX`'ta |
| `istege_bagli_esik` | KK-04 | genel | her hesapta en ucuz ardıl |
| `bekletme` | KK-05 | genel | yol yoksa paket düşer |
| `cogaltma` | (ileride) | karıştırmaya karşı | son çare; varsayılan kapalı (T-14) |

## Her A/B'de

- Birincil ölçü: birincil hücrede `PDR_açık` artışı **ve** karıştırıcısız ikizde zarar yok; dayanıklılık hücresi ayrıca (`12` Faz 5).
- Her A/B'de ayrıca: kontrol trafiğinin kanal süresindeki payı · gecikme tavanlı `PDR_açık` (5 s) · gecikmenin p99'u (T-19).
- Beklenti koşudan önce yazılır (D-05).
