# KK-00 · Kural kâğıtları — dizin, genel kurallar, değerler, bayraklar

> Faz 5-3 (`12` §1.2). Kararlar `17`de (T-1…T-20); kural kâğıtları onları kurallara, formüllere ve başlangıç değerlerine çevirir. Kod bu kâğıtlardan yazılır; kod yorumları `KK-n` ve `T-n`e atıf verir. Değerler başlangıçtır, geliştirme tohumlarında (1003–1010) A/B ile ayarlanır. Bağımsız denetim: `arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md` ve kapanışı. Güncel: 17 Kasım 2026.

## Kâğıtlar

| # | konu | kararlar |
|---|---|---|
| KK-01 | bağın durumu (OLAĞAN · ASKIDA · KÖTÜ · KARIŞTIRILIYOR) ve ölçüsü | T-2 · T-3 · T-7 · T-9 · İlke 2 |
| KK-02 | selam ve ara ilan | T-1 · T-16 · T-17 |
| KK-03 | karıştırma kanıtı | T-5 · T-6 · T-8 · T-9 · T-10 |
| KK-04 | rota seçimi, döngüsüzlük, açlık | T-11 · T-12 · T-13 · T-14 · T-15 |
| KK-05 | bekletme ve komutun yolu | T-18 · T-20 |

Her kâğıtta: amaç ve sınıf · gördüğü · tuttuğu · kurallar · örnek · sınanması · kaynak.

## Genel kurallar

1. **Niyet döndüremeyen kancalar** (`iletim_sonucu`, `cerceve_duyuldu`; `sim2/gozlem/protokol.py`): bu kancalarda değişen durum (bağın durumu, ardıl, iz) kaydedilir; gerektirdiği niyet (selam, tur isteği, uyanma) bir sonraki niyetli kancada, en geç saniyelik zamanlayıcıda verilir.
2. **Aynı olayda sıra:** KK-01 kural 15.
3. **Birimler:** maliyetler ETX × 64 tamsayı (yukarı yuvarlanır; sonlu en çok 0xFFFE, 0xFFFF = ∞); FD ilan edilen (nicemlenmiş) değeri tutar. Sıra ve tur 16 bit, modüler karşılaştırılır (`sira` 0'dan, geçidin turu 1'den başlar). Bütün süreler yerel saatle (`saat_s`) ölçülür.

## Başlangıç değerleri (tek yer)

| ad | değer | kâğıt | dayanak |
|---|---|---|---|
| `N` selam geçmişi | 16 | KK-01 | Babel'in geçmişi [4] |
| `ORNEK_EN_AZ` | 4 selam | KK-01 | yeni komşu ancak ölçülünce aday |
| `E_CIK` · `E_DON` | 4 · 3 (ETX) | KK-01 | MRHOF üst sınırı 4 [64]; iki eşik T-3 |
| `VERI_PENCERE` · `VERI_EN_AZ` | son 8 veri çerçevesi, ≤ 10 s · en az 4 çerçeve | KK-01 | T-2'nin veri örneği; tek başarısız çerçeve tetiklemesin (denetim B-12) |
| `ASKIDA_SURE` | `min((k + 1) · a, 10 s)`, en az 1 s (`k` KK-03 kural 6, `a` komşunun aralığı) | KK-01 | sessizlik kanıtı son selamdan `(k + 0,5) · a` sonra tamamlanır; askıda süre onu bekler |
| `T_HATIRA` | 30 s | KK-01 | karıştırılıyor süresi iki çizelgede 11–15 s; teşhis (d) S3'te kullanılan bağların 7 denemelik başarısı 32 s'de bant değiştirmiyor (doymuş ölçü; tek deneme başarısı ölçülmedi, `17` §7 madde 8) |
| `T_CEZA` | 10 s; 60 s içinde yinelenirse ×2, en çok 40 s | KK-01 | veriyle KÖTÜ'ye düşen bağın gidip gelmesini önler; karıştırma kanıtıyla sınıflanan düşüşler sayılmaz |
| `T_SILME` | 30 s hiç duyulmazsa | KK-01 | İlke 2; 15 s'lik karıştırmada silinmesin |
| `ZAMAN_ASIMI` | 1,5 × komşunun aralığı | KK-01, KK-03 | Babel'in katsayısı (`protokoller/babel_bicim.py`, `HELLO_ZAMAN_ASIMI_KATSAYISI`) |
| `I_MIN` · `I_MAX` | 0,5 s · 2 s | KK-02 | `k = 3` ve `a = 2 s` iken sessizlik kanıtı son selamdan 7 s, karıştırmanın başlangıcından 5–7 s sonra; yalnız `d_r ≥ 0,8` bağlarda 10 s'lik açık dönemden kısa (`d_r` 0,6 → 11–13 s); `17` §7 madde 3 |
| `SELAM_ARASI_EN_AZ` | `I_MIN` | KK-02 | T-17'nin sıklık sınırı; değişimler birleşir |
| `ILAN_ESIGI` | %15 | KK-02 | maliyet değişiminin "önemli" sayılması |
| `ED_ESIGI` | kanal meşgul payı ≥ 0,62 | KK-03 | teşhis (d): %80 yakalama, ikizde %0,035 yanlış alarm |
| `DUSUS_ORANI` | çözülen < 0,5 × kendi ortalaması | KK-03 | teşhis (d): girişimde 49 ↔ 99/s; kendi ortalamaya göre okuma ölçülmedi (`17` §7 madde 7) |
| `KAYIP_ESIGI` | selam kaybı ≥ 0,6 | KK-03 | teşhis (d): girişimde 0,69 ↔ temiz 0,44; orada beklenen selam göndericinin gerçek selamlarından ve 4 s'lik Hello'yla sayıldı, burada protokolün kendi sayımı (KK-03 kural 2); yeniden ayarlanır |
| `GIRIS_SANIYE` · `CIKIS_SANIYE` | girişim 2 · 3 ardışık saniye; ED 1 · 1 | KK-03 | T-10; ED eşiğinin yanlış alarmı %0,035 |
| `MAC_ARDISIK` | 3 vazgeçme | KK-03 | teşhis (d): `n* = 3` |
| `GECIS_ORANI` | %10 | KK-04 | Ramachandran [54]; T-11 |
| `ISTEK_YINELEME` | 3 kez, 0,5 s arayla | KK-04 | sayı Babel'in (`ISTEK_TEKRAR`); aralık bu tasarımın (Babel 2 s'den başlayıp katlıyor) |
| `ISTEK_ARA` | 5 s | KK-04 | açlık sürerse istek dizisinin yinelenmesi; uygulanamaz ilanı yok saymanın üst süresi |
| `ISTEK_ANIMSA` | 2 s | KK-04 | iletilen isteğin yanıtını istek yolundan geri yaymak için (RFC 8966 §3.8.1.2'deki liste) |
| `ISTEK_ATLAMA` | 64 | KK-04 | RFC 8966 §3.8.2.1: ağın çapından büyük; çap tanı kaydında ölçülür |
| `TUTMA_EN_COK` | 2 s (atlama başına) | KK-05 | T-18 |
| `IZ_TAZELIK` | 3 s | KK-05 | telemetri saniyede bir |

## Gözlemin kullanımı (`05`; mimari denetimi D17)

| okur | okumaz |
|---|---|
| `mesgul_sure_s` (`kanal_dolulugu_ister`) · `alinan_cerceve` · `saat_s` (yalnız süreler) · `kontrol_alindi` (selam, tur isteği) · `iletim_sonucu` · `iletim_basarisiz` · `cerceve_duyuldu`'nun göndereni, türü, hedefi ve veri çerçevesinin başlığı · karar anında paketin başlığı · geçidin kimliği (yapılandırma) | `olculen_gurultu_w` (yasak, K-227) · `cerceve_duyuldu`'nun RSSI'ı (KK-03 kural 11) · `phy_hata` (teşhis (d)'de zayıf) · `kendi_konum` · `kendi_hiz` · `komsular` (simülatörün beacon listesi; kendi selamı var, `kosum_beaconi = False`) |

## Mekanizmalar, bayraklar, sınıflar (K-247: sınıf ve amaç ölçmeden önce)

| mekanizma | kâğıt · kural | bayrak | sınıf | kapalıyken |
|---|---|---|---|---|
| selamdan ETX, iki eşik, silme | KK-01 1–5, 11–12, 14 | çekirdek | genel | (protokolün temeli) |
| veri tetiği, ASKIDA, ceza | KK-01 6–8, 11 | `veri_kotu_tetigi` | genel | ETX yalnız selamdan; ASKIDA ve ceza yok |
| kendi durumum, bağ kanıtı, KARIŞTIRILIYOR, dondurmalar, kendim karıştırılırken MAC'in yok sayılması, gönderemezken selam kurulmaması, açlıkta isteğin bastırılması | KK-03 1–9 · KK-01 9–10, 13 · KK-02 5 · KK-04 8 | `karistirma_durumu` | karıştırmaya karşı | KK-03 çalışmaz; KARIŞTIRILIYOR'a girilmez; dondurma yok; MAC sonuçları her zaman veri tetiğine girer; veri tetiğiyle ASKIDA'ya giren bağ süre dolunca KÖTÜ olur |
| alıcının biti | KK-02 alan · KK-03 5 | `alici_bildirimi` | karıştırmaya karşı | bit hep 0 gönderilir, okunmaz, değişimi olay değildir (alan kalır, boyut aynı) |
| hatırlanan kalite | KK-01 10 | `hatirlanan_kalite` | karıştırmaya karşı | dönüşte `gecmis` boşaltılır, bağ KÖTÜ'den yeniden ölçülür; dondurmalar sürer |
| uyarlanır aralık | KK-02 2 | `uyarlanir_aralik` | genel | `I` sabit `I_MAX`; ara ilan sürer |
| ara ilan | KK-02 3 | çekirdek | genel | (T-17) |
| isteğe bağlı geçiş eşiği | KK-04 5 | `istege_bagli_esik` | genel | her hesapta en ucuz aday |
| uygunluk, FD, tur, açlıkta istek, uygulanamaz ilanı yok sayma | KK-04 1–4, 6–11 | çekirdek | genel | (döngüsüzlük) |
| bekletme | KK-05 1–5 | `bekletme` | genel | yol yoksa paket düşer |
| geri iz | KK-05 6–9 | çekirdek | genel | (T-20) |
| seçici çoğaltma | (ileride) | `cogaltma` | karıştırmaya karşı | varsayılan kapalı (T-14) |

**Mekanizma kapısının "hepsi kapalı" yapılandırması** (`06` §0.4.5): `karistirma_durumu`, `alici_bildirimi`, `hatirlanan_kalite` ve `cogaltma` kapalı; genel bayraklar açık. Kapı, karıştırmaya karşı mekanizmalar birlikte kapatılınca `PDR_açık`ın anlamlı düşmesini ister.

## A/B ölçütleri (sınıfa göre)

- **Karıştırmaya karşı:** birincil ve dayanıklılık hücresinde `PDR_açık` artışı **ve** karıştırıcısız ikizde zarar yok (`12` Faz 5).
- **Genel:** katkı karıştırıcısız ikizdeki ablasyonla beyan edilir (K-247; ikizde pencere PDR'si ve mekanizmanın kendi tanı ölçüsü); birincil hücrede zarar yok.
- **Hepsinde:** kontrol trafiğinin kanal süresindeki payı · gecikme tavanlı `PDR_açık` (5 s) · gecikmenin p99'u (T-19).
- `12` Faz 5'in her mekanizmada istediği yer karıştırıcılı aile hücresi beklentide ya eklenir ya gerekçesiyle çıkarılır.
- Beklenti koşudan önce yazılır (D-05).

## Tanı kaydı (her A/B'de sayılır)

- Veriyle KÖTÜ sayısı, bağ başına ve geçide uzaklığa göre (denetim S-1).
- Açlıkta tur isteğinin gidiş-dönüş süresi; tur artışı ve tur isteği sayısı; en uzun atlama sayısı (S-2, S-5; `17` §7 madde 10).
- "Karıştırılıyorum" yanlış alarmı (ikizde), tespit süresi, girişim kaynaklı durumun açık dönemdeki geçiş sayısı (S-4).
- Sessiz dönemin ilk saniyelerindeki teslim (S-3).
- Bağ kalitesinin değişim hızı, tek deneme başarısıyla ve yedekler dâhil (`17` §7 madde 8); başka bir karıştırıcı sınıfı ya da yer karıştırıcılı aile (`17` §7 madde 9).
