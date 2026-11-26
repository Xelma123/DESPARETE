# KK-00 · Kural kâğıtları — dizin, genel kurallar, değerler, bayraklar

> **Önceki tasarım (26 Kasım notu):** bu kâğıt 5-3'ün ilk tasarımının kuralıdır (kararları `17`); bugünkü kodun (`protokoller/desparete5*.py`) ve 18–24 Kasım ölçümlerinin belgesi olarak kalır, yeni tasarım donunca arşive gider. Yeni tasarım `18`de, kuralları `bilesen/`de (K-253).

> Faz 5-3 (`12` §1.2). Kararlar `17`de (T-1…T-20); kural kâğıtları onları kurallara, formüllere ve başlangıç değerlerine çevirir. Kod bu kâğıtlardan yazılır (`protokoller/desparete5*.py`; değerler ve bayraklar `desparete5_bicim.py`); kod yorumları `KK-n` ve `T-n`e atıf verir. Değerler başlangıçtır, geliştirme tohumlarında (1003–1010) A/B ile ayarlanır. Bağımsız denetim: `arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md` ve kapanışı. Güncel: 20 Kasım 2026 (KK-04 kural 13 geri gönderme yasağı ve kural 14 sınırlı yükselme: iki bayrak, iki değer, tanı). Önceki: 19 Kasım (`v2/arsiv/kural/KK-00-DIZIN-2026-11-19.md`: `17` T-2, T-11, T-12, T-13) · 18 Kasım (`v2/arsiv/kural/KK-00-DIZIN-2026-11-18.md`; kodlamayla Y-4 · Y-6 · Y-9 · Y-11).
>
> **Kod:** 19 Kasım'da bu kâğıtlara göre yazıldı; KK-04 kural 13–14 20 Kasım'da kodlandı, iki bayrak kapalıyken 19 Kasım'ın kodu birebir yeniden üretilir (`CEKIRDEK_19K`; küçük test dünyasında 12 koşu: `arsiv/teshis/faz5_3_kod_2026-11-20/esdegerlik.txt`). 18 Kasım'ın davranışı `egim` · `vazgecme_tetigi` · `duzgun_gecis` kapalı, `veri_kotu_tetigi` açık ve `DEGERLER_ESKI`yle birebir yeniden üretilir (küçük test dünyasında sekiz koşuda denetlendi: `arsiv/teshis/faz5_3_kod_2026-11-19/esdegerlik.txt`). 19 Kasım'da gelen değerler aynı gün onaylandı.

## Kâğıtlar

| # | konu | kararlar |
|---|---|---|
| KK-01 | bağın durumu (OLAĞAN · KÖTÜ · KARIŞTIRILIYOR), ölçüsü ve vazgeçme tetiği | T-2 · T-3 · T-7 · T-9 · İlke 2 |
| KK-02 | selam ve ara ilan | T-1 · T-16 · T-17 |
| KK-03 | karıştırma kanıtı | T-5 · T-6 · T-8 · T-9 · T-10 |
| KK-04 | rota seçimi ve döngü bekçisi | T-11 · T-12 · T-13 (kalktı) · T-14 · T-15 · T-17 |
| KK-05 | bekletme ve komutun yolu | T-18 · T-20 |

Her kâğıtta: amaç ve sınıf · gördüğü · tuttuğu · kurallar · örnek · sınanması · kaynak. 18 Kasım'ın kâğıtları `v2/arsiv/kural/`de; kodda `egim` ve `veri_kotu_tetigi` bayraklarıyla yeniden üretilebilir.

## Genel kurallar

1. **Niyet döndüremeyen kancalar** (`iletim_sonucu`, `cerceve_duyuldu`; `sim2/gozlem/protokol.py`): bu kancalarda değişen durum (bağın durumu, işaretler, ardıl, iz, döngü bekçisinin olayı) kaydedilir; gerektirdiği niyet (selam, uyanma; `egim` kapalıyken tur isteği) bir sonraki niyetli kancada, en geç saniyelik zamanlayıcıda verilir.
2. **Aynı olayda sıra:** KK-01 kural 15.
3. **Birimler:** maliyetler ETX × 64 tamsayı (yukarı yuvarlanır; sonlu en çok 0xFFFE, 0xFFFF = ∞); `C_ilan` (`egim` kapalıyken FD) ilan edilen (nicemlenmiş) değeri tutar. Sıra 16 bit, modüler karşılaştırılır (`sira` 0'dan başlar); `egim` kapalıyken tur da 16 bit, geçidin turu 1'den başlar. Bütün süreler yerel saatle (`saat_s`) ölçülür.
4. **Ölçüm beyanları** (yalnız ölçüme gider; anlamları Babel, AODV ve OLSRv2 ile aynı, K-139; 18 Kasım, kodlamada G-2): `kopma(K)` bir önceki kanca sonunda ardılım olan K'nin bağı kullanılamaz oldu (OLAĞAN'dan çıktı ya da silindi) · `rota_kuruldu(K)` K'nin kaybından sonra yeniden ardılım var · `rota_gecersiz` daha önce yolu olan hedefe (geçide ya da izi bilinen komut hedefine) giden paket düştü; yolu hiç bilinmemişse düşüş beyansızdır. "Veriye uygun değil" işareti ve döngü dışlaması bağı kullanılamaz yapmaz; kopma beyanı değildir.
5. **Kancalar** (`protokoller/desparete5.py`): saniyelik zamanlayıcı (kendi durumum; ilk çağrıda selam başlar) · selam, en erken son tarih ve tamponu yeniden sorma için nesil numaralı uyandırmalar · `kontrol_alindi` (selam; `egim` kapalıyken tur isteği) · `iletim_sonucu` (vazgeçme kaydı, MAC kanıtı; niyetsiz) · `iletim_basarisiz` (onun niyetleri) · `cerceve_duyuldu` (komşu hâlâ orada, geri iz, döngü bekçisinin bayat bilgi işareti; niyetsiz) · `sonraki_atlama` (döngü bekçisinin kesin döngü denetimi, geri gönderme yasağı, bekletme). Her niyetli kancanın sonunda sıra: zaman olayları → rota seçimi → selam olayları → (`egim` kapalıyken tur istekleri) → tampon → son tarih → beyanlar. Ölçüm aletlerinde adlar `desparete5` (bütün bayraklar), `desparete5_cekirdek` (karıştırmaya karşı mekanizmalar kapalı), `desparete5_eski_cekirdek` (18 Kasım'ın çekirdeği: `egim`, `vazgecme_tetigi`, `duzgun_gecis`, `geri_yasagi`, `sinirli_yukselme` kapalı, `veri_kotu_tetigi` açık; ilk ölçümü birebir üretmeli) ve `desparete5_cekirdek_19k` (19 Kasım'ın çekirdeği: `geri_yasagi` ve `sinirli_yukselme` kapalı; yeni çekirdeğin ölçümündeki `cekirdek` kolunu birebir üretmeli) (`kalibrasyon/aodv_uygunluk.py`).

## Başlangıç değerleri (tek yer)

| ad | değer | kâğıt | dayanak |
|---|---|---|---|
| `N` selam geçmişi | 16 | KK-01 | Babel'in geçmişi [4] |
| `ORNEK_EN_AZ` | 4 selam | KK-01 | yeni komşu ancak ölçülünce aday |
| `E_CIK` · `E_DON` | 4 · 3 (ETX) | KK-01 | MRHOF üst sınırı 4 [64]; iki eşik T-3 |
| `VAZ_PENCERE` · `VAZ_PENCERE_S` | son 16 veri çerçevesi · en çok 30 s geriye (19 Kasım) | KK-01 | saniyede bir telemetri gönderen uç düğümde 16 çerçeve ~16 s; 30 s bayat kaydı atar |
| `VAZ_ESIK` | 3 vazgeçme (19 Kasım) | KK-01 | açlık teşhisinin tetiksiz kolunda koşu başına ~690 vazgeçme, 34–50 bin karar; en kötü beş bağın dışında vazgeçme payı ~%1. Vazgeçmeler bağımsız sayılırsa böyle bir bağda 16 çerçevede en az 3 vazgeçme olasılığı ~%0,05; vazgeçme payı %5–15 olan kalıcı sorunlu bağda birkaç düzine çerçevede tetiklenir. Vazgeçmeler topaklanabildiği için gerçek yanlış alarm daha yüksek olabilir; tanıda sayılır |
| `VAZ_BEKLE_S` · `VAZ_YINELEME_S` · `VAZ_BEKLE_EN_COK_S` | 5 s · 60 s içinde yinelenirse ×2 · en çok 40 s (19 Kasım) | KK-01 | eski cezanın katlanma yapısı; başlangıç daha kısa, çünkü bağ artık atılmıyor, yalnız sona düşüyor. Kalıcı sorunlu bağın her dönüşü en az 3 vazgeçmeye mal olur |
| `T_HATIRA` | 30 s | KK-01 | karıştırılıyor süresi iki çizelgede 11–15 s; teşhis (d) S3'te kullanılan bağların 7 denemelik başarısı 32 s'de bant değiştirmiyor (doymuş ölçü; tek deneme başarısı ölçülmedi, `17` §7 madde 8) |
| `KENDI_UST_SURE` | 30 s (= `T_HATIRA`) | KK-01 | kendi "karıştırılıyorum" dondurmasının üst süresi; her dondurmanın üst süresi aynı (18 Kasım, Y-6) |
| `T_SILME` | 30 s hiç duyulmazsa | KK-01 | İlke 2; 15 s'lik karıştırmada silinmesin |
| `ZAMAN_ASIMI` | 1,5 × komşunun aralığı | KK-01, KK-03 | Babel'in katsayısı (`protokoller/babel_bicim.py`, `HELLO_ZAMAN_ASIMI_KATSAYISI`) |
| `I_MIN` · `I_MAX` | 0,5 s · 2 s | KK-02 | ilan edilen aralık `I_MAX`'ın 1,1 katı, 2,2 s; `k = 3` iken sessizlik kanıtı son selamdan 7,7 s, karıştırmanın başlangıcından 5,5–7,7 s sonra; yalnız `d_r ≥ 0,8` bağlarda 10 s'lik açık dönemden kısa (`d_r` 0,6 → 12,1–14,3 s); KK-03 kural 7'nin `2·a`'sı 4,4 s; `17` §7 madde 3 (Y-9) |
| `SELAM_ARASI_EN_AZ` | `I_MIN` | KK-02 | T-17'nin sıklık sınırı; değişimler birleşir |
| `ILAN_ESIGI` | %15 | KK-02, KK-04 | maliyet değişiminin "önemli" sayılması |
| `ED_ESIGI` | kanal meşgul payı ≥ 0,62 | KK-03 | teşhis (d): %80 yakalama, ikizde %0,035 yanlış alarm |
| `DUSUS_ORANI` | çözülen < 0,5 × kendi ortalaması | KK-03 | teşhis (d): girişimde 49 ↔ 99/s; kendi ortalamaya göre okuma ölçülmedi (`17` §7 madde 7) |
| `KAYIP_ESIGI` | selam kaybı ≥ 0,6 | KK-03 | teşhis (d): girişimde 0,69 ↔ temiz 0,44; orada beklenen selam göndericinin gerçek selamlarından ve 4 s'lik Hello'yla sayıldı, burada protokolün kendi sayımı (KK-03 kural 2); yeniden ayarlanır; kalabalık riski KK-03 kural 12 |
| `GIRIS_SANIYE` · `CIKIS_SANIYE` | girişim 2 · 3 ardışık saniye; ED 1 · 1 | KK-03 | T-10; ED eşiğinin yanlış alarmı %0,035 |
| `MAC_ARDISIK` | 3 vazgeçme | KK-03 | teşhis (d): `n* = 3` |
| `MALIYET_TAVANI` | 32 ETX (19 Kasım) | KK-04 | bağ ETX'i en çok `E_CIK` = 4; 8 atlamalık en kötü yol 32. Çekirdekte paket başına ~3,7 karar (ilk ölçüm, ikiz). Yeri tanıda yol maliyetinin dağılımıyla sınanır |
| `YUKSELME_PAYI` | 4 ETX (20 Kasım) | KK-04 | bir bağın aday kalabileceği en büyük ETX `E_CIK`: kopan ardılın yerine geçen yol en çok bir bağ kadar pahalı olabilsin. MRHOF'a göre pay, ardıl değiştirme eşiğinden küçük olmamalı [64] (MRHOF'ta 1,5 ETX; bizde iki ölçülü geçiş, eşik yok). İki düğümlü tırmanmada her tur maliyeti en az 2 ETX artırır; pay en çok üç turda aşılır. RFC 6550 varsayılan vermez. Taranmadı; tanıda sınır yüzünden kaybedilen ardıl sayılır |
| `YUKSELME_UNUT_S` | 4 s = 2 × `I_MAX` (20 Kasım) | KK-04 | `L`'nin unutulması (RPL'de yeni sürümün yerine). Bu sürede her komşudan en az bir yeni selam gelir (aralık en çok 2,2 s), bayat ilanlar tazelenmiş olur. Tırmanma ara ilan hızında (en sık 0,5 s'de bir) ilerlediği için pay bu süre dolmadan aşılır. Taranmadı |
| `DUZ_S` | 6 s = 3 × `I_MAX` (19 Kasım) | KK-04 | Babel Ek A.3: düzgünleştirmenin zaman sabiti selam aralığının ~3 katı [4] |
| `DONGU_ANIMSA_S` | 5 s (19 Kasım) | KK-04 | döngüye giren paket birkaç atlamada döner; yoldaki iki bekletmeyi de kapsar |
| `DONGU_DISLA_S` | 2 s (19 Kasım) | KK-04 | dışlanan komşunun düzeltici selamı en geç `I_MAX` içinde gelir; bayat bilgi olayı onu hemen de getirebilir (KK-04 kural 8) |
| `GECIS_ORANI` | %10 | KK-04 | yalnız `duzgun_gecis` kapalıyken; Ramachandran [54]; 16 Kasım'ın T-11'i |
| `ISTEK_YINELEME` · `ISTEK_ARA` · `ISTEK_ANIMSA` · `ISTEK_ATLAMA` | 3 kez, 0,5 s arayla · 5 s · 4 s · 64 | arşivdeki KK-04 | yalnız `egim` kapalıyken (18 Kasım'ın açlık ve tur isteği kuralları); dayanakları arşivdeki KK-00'da |
| `TUTMA_EN_COK` | 1 s, atlama başına (19 Kasım; 18 Kasım'da 2 s) | KK-05 | T-18: telemetri saniyede bir üretilir, 1 s'den eski paketin yerine yenisi zaten vardır; eğimde yol ancak hiç aday kalmayınca yoktur |
| `IZ_TAZELIK` | 3 s | KK-05 | telemetri saniyede bir |

Kalkan değerler (19 Kasım; arşivdeki KK-00'da): `VERI_PENCERE` · `VERI_EN_AZ` (eski veri tetiği) · `ASKIDA_SURE` · `T_CEZA`. Kodda yalnız `veri_kotu_tetigi` açıkken kullanılır.

## Gözlemin kullanımı (`05`; mimari denetimi D17)

| okur | okumaz |
|---|---|
| `mesgul_sure_s` (`kanal_dolulugu_ister`, yalnız `karistirma_durumu` açıkken) · `alinan_cerceve` · `saat_s` (yalnız süreler) · `kontrol_alindi` (selam; `egim` kapalıyken tur isteği) · `iletim_sonucu` · `iletim_basarisiz` · `cerceve_duyuldu`'nun göndereni, türü, hedefi ve veri çerçevesinin başlığı (atlama sayısı dâhil) · karar anında paketin başlığı · geçidin kimliği (yapılandırma) | `olculen_gurultu_w` (yasak, K-227) · `cerceve_duyuldu`'nun RSSI'ı (KK-03 kural 11) · `phy_hata` (teşhis (d)'de zayıf) · `kendi_konum` · `kendi_hiz` · `komsular` (simülatörün beacon listesi; kendi selamı var, `kosum_beaconi = False`) |

## Mekanizmalar, bayraklar, sınıflar (K-247: sınıf ve amaç ölçmeden önce)

| mekanizma | kâğıt · kural | bayrak | sınıf | kapalıyken |
|---|---|---|---|---|
| selamdan ETX, iki eşik, silme | KK-01 1–5, 11–12, 14 | çekirdek | genel | (protokolün temeli) |
| vazgeçme tetiği | KK-01 6–7 | `vazgecme_tetigi` | genel | veri sonucu yalnız KK-03 kural 7'ye girer |
| (eski) veri tetiği, askıda, veri cezası | arşivdeki KK-01 6–8, 11 | `veri_kotu_tetigi` | genel | varsayılan kapalı; yalnız 18 Kasım ölçümlerini yeniden üretmek için; açıkken `vazgecme_tetigi` kapalı olmak zorunda |
| kendi durumum, bağ kanıtı, KARIŞTIRILIYOR, dondurmalar, kendim karıştırılırken MAC'in yok sayılması, gönderemezken selam kurulmaması | KK-03 1–9 · KK-01 9–10, 13 · KK-02 5 | `karistirma_durumu` | karıştırmaya karşı | KK-03 çalışmaz; KARIŞTIRILIYOR'a girilmez; dondurma yok; `alici_bildirimi` ve `hatirlanan_kalite` de kapalı olmak zorunda. `egim` kapalıyken açlıkta isteğin bastırılması (arşivdeki KK-04 kural 8) da bu bayrağa bağlı |
| alıcının biti | KK-02 alan · KK-03 5 | `alici_bildirimi` | karıştırmaya karşı | bit hep 0 gönderilir, okunmaz, değişimi olay değildir (alan kalır, boyut aynı) |
| hatırlanan kalite | KK-01 10 | `hatirlanan_kalite` | karıştırmaya karşı | dönüşte `gecmis` boşaltılır, bağ KÖTÜ'den yeniden ölçülür; dondurmalar sürer |
| uyarlanır aralık | KK-02 2 | `uyarlanir_aralik` | genel | `I` sabit `I_MAX`; ara ilan sürer |
| ara ilan | KK-02 3 | çekirdek | genel | (T-17) |
| maliyet eğimi, yokuş aşağı, son çare, maliyet tavanı, döngü bekçisi | KK-04 1–4, 7–12 | `egim` | genel | 18 Kasım'ın kuralları (arşivdeki KK-04: FD, tur, açlık, tur isteği, yok sayma); selamda tur alanı |
| isteğe bağlı geçiş | KK-04 5–6 | `istege_bagli_esik` · `duzgun_gecis` | genel | `duzgun_gecis` kapalı: %10 oransal eşik; ikisi kapalı: her hesapta daha ucuz aday |
| geri gönderme yasağı (20 Kasım) | KK-04 13 | `geri_yasagi` | genel | paket getiren komşuya da gönderilebilir (19 Kasım'ın davranışı) |
| sınırlı yükselme (20 Kasım) | KK-04 14 | `sinirli_yukselme` | genel | yükselmenin tek sınırı `MALIYET_TAVANI`; ∞ ilanından sonra `D = A` (19 Kasım'ın davranışı) |
| bekletme | KK-05 1–5 | `bekletme` | genel | yol yoksa paket düşer |
| geri iz | KK-05 6–9 | çekirdek | genel | (T-20) |
| seçici çoğaltma | (ileride) | `cogaltma` | karıştırmaya karşı | varsayılan kapalı (T-14) |

**Mekanizma kapısının "hepsi kapalı" yapılandırması** (`06` §0.4.5): `karistirma_durumu`, `alici_bildirimi`, `hatirlanan_kalite` ve `cogaltma` kapalı; genel bayraklar açık. Kapı, karıştırmaya karşı mekanizmalar birlikte kapatılınca `PDR_açık`ın anlamlı düşmesini ister. `vazgecme_tetigi`, `egim`, `duzgun_gecis`, `geri_yasagi` ve `sinirli_yukselme` genel sınıftadır, kapıya girmez (K-247).

## A/B ölçütleri (sınıfa göre)

- **Karıştırmaya karşı:** birincil ve dayanıklılık hücresinde `PDR_açık` artışı **ve** karıştırıcısız ikizde zarar yok (`12` Faz 5).
- **Genel:** katkı karıştırıcısız ikizdeki ablasyonla beyan edilir (K-247; ikizde pencere PDR'si ve mekanizmanın kendi tanı ölçüsü); birincil hücrede zarar yok.
- **Hepsinde:** kontrol trafiğinin kanal süresindeki payı · gecikme tavanlı `PDR_açık` (5 s) · gecikmenin p99'u (T-19).
- `12` Faz 5'in her mekanizmada istediği yer karıştırıcılı aile hücresi beklentide ya eklenir ya gerekçesiyle çıkarılır.
- Beklenti koşudan önce yazılır (D-05).

## Tanı kaydı (her A/B'de sayılır)

- Vazgeçme tetiği: tetik sayısı, tetiklenen bağın kâhin bandı, tetikten sonra ardılın değişip değişmediği ve o bağdaki vazgeçmeler, vazgeçmelerin bağlara dağılımı (en kötü beş bağın payı) (açlık teşhisi; denetim S-1'in yerine).
- Yol seçimi: döngü kanıtı ve bayat bilgi olayı sayısı · son çare seçimi · tavan aşımı · yol yok bölümlerinin sayısı ve süresi · ömür (TTL) kaybı · en uzun atlama sayısı · yol maliyetinin dağılımı · ardıl değişimi, sebebine göre (`17` T-12; S-2 ve S-5'in yerine) · geri gönderme yasağının başka adaya yönlendirdiği ve beklettiği paketler · sınırlı yükselme yüzünden kaybedilen ardıl (KK-04 kural 13–14).
- "Karıştırılıyorum" yanlış alarmı (ikizde), tespit süresi, girişim kaynaklı durumun açık dönemdeki geçiş sayısı (S-4).
- Sessiz dönemin ilk saniyelerindeki teslim (S-3).
- Bağ kalitesinin değişim hızı, tek deneme başarısıyla ve yedekler dâhil (`17` §7 madde 8); başka bir karıştırıcı sınıfı ya da yer karıştırıcılı aile (`17` §7 madde 9).
