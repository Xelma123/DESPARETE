# Faz 5-2 · bağımsız denetimin kapanışı

> 17 Kasım 2026 · rapor `DENETIM-RAPORU-5-2-2026-11-17.md` (denetlenen hâl `98b3875`; istem `DENETIM-PROMPT-5-2-2026-11-17.md`) · hüküm: "5-2 bu hâliyle kapatılmamalı; aşağıdaki işler yapılınca kapatılabilir" · bulgular: 2 engelleyici, 10 önemli, 10 küçük; hepsi belge ve karar düzeyinde.
>
> Engelleyici iki bulgu kaynağından ayrıca doğrulandı (gözlem sözleşmesi `v2/05` §3.3a; RFC 8966 §3.5.1, §3.5.3, §3.8.2.2). Karar gerektiren beş noktada seçimlerim aşağıda; gerisi metin düzeltmesi. Tam test takımı denetimden önce koşuldu: `1101 passed` (17 Kasım, 19 dk 42 sn).

## Kararlar

| bulgu | karar |
|---|---|
| E-1 · açıklanamayan meşguliyet sözleşmede yok | ED bölgesinin kanıtı sözleşmedeki kanal meşguliyetinden (`mesgul_sure_s`): G 0,978 · 0,976, ikizde yanlış alarm %0,035. Sözleşme genişletilmez; açıklanamayan meşguliyet kanıta girmez (`v2/17` T-5). |
| E-2 · uygulanamaz güncelleme | Güncelleme yok sayılır, seçili rota son kabul edilen maliyetiyle kalır ve yeni tur istenir; güncelleme uygulanırsa rota hemen bırakılır. FD, bu turda ilan ettiğim sonlu maliyetlerin en küçüğüdür (`v2/17` T-12, T-13). |
| Ö-5 · selamın aralığı | Selam o anki aralığını taşır (`v2/17` T-1, T-16). |
| Ö-6 · bağın durum makinesi | "Karıştırılıyor" iken toplanan örnekler bağ ölçüsüne girmez, hatırlanan kalite korunur (`v2/17` T-7); üç durumun geçişleri 5-3'ün ilk kural kâğıdında (§7 madde 1). |
| Ö-7 · tamponun sınırı | Sınırın türü 5-3'te (§7 madde 4); gecikme tavanlı `PDR_açık` (5 s) ve gecikmenin p99'u her A/B'de raporlanır (`v2/17` T-19). |
| Ö-9 · takvim | Mühür tarihi güncel değil diye işaretlendi, 5-3'ten sonra yeniden yazılır (`v2/12` §1, Faz 6; `v2/04` §8). Takvim şimdi yeniden planlanmadı. |

## Metin düzeltmeleri

| bulgu | yapılan | yer |
|---|---|---|
| Ö-1 | Kimlik paragrafı (d)'nin gösterdiğiyle sınırlandı: ED'de düğümün kendi kanal ölçümü; girişimde birkaç işaret ve birkaç saniye, biçimi ve başarısı 5-3'te | `v2/17` kimlik |
| Ö-2 | (d)'nin düğüm düzeyi selam kaybı ile komşu başına "sessizleşen komşu" ayrıldı; komşu başına işaretler ölçüm listesine girdi | `v2/17` T-5, T-6, §7 madde 6 |
| Ö-3 | S3'ün yorumu ölçünün kendisine indirildi (7 denemelik atlama başarısı, doymuş ölçü) | `v2/17` T-1 · `v2/12` §1.2 · teşhis (d) `sonuc.md` §4, §5, §8 |
| Ö-4 | (d)'nin koşulu (Babel trafiği, sürekli sınıf) yazıldı; yeni sürümle ve başka sınıfta yeniden ölçüm listeye girdi | `v2/17` T-5, §7 madde 9 |
| Ö-8 | Faz 5'in eski mekanizma tablosu ve eksikler satırı `17`ye bağlandı | `v2/12` §2 Faz 5 ve §3 kaba plan · `v2/04` §6 |
| Ö-10 | 5-3'ün açılış listesi | `v2/17` §7 |
| K-1 | T-3'ün ödünç satırı: iki eşikli kullanılabilirlik kendi uyarlamam | `v2/17` T-3 |
| K-2 | Puñal'in aktarımı düzeltildi (teslim oranı ve en uzun boşta kalma süresi iki türü de gösteriyor) | `v2/17` T-5 |
| K-3 | DSDV "De Couto 2003'te aktarıldığı gibi"; en eskiyi düşürme "seçimim" | `v2/17` kimlik, T-12, T-18 |
| K-4 | [4]'ün durumu `02` G3 ile hizalandı; T-13'ün bölüm atıfları | `v2/16` · `v2/17` T-13 |
| K-5 | T-12'nin gerekçesi TTL grubuyla; R'nin 0'ı T-13'e taşındı | `v2/17` T-12, T-13 |
| K-6 | Düğüm sayıları iki hücre için ayrı | `v2/17` T-6 · teşhis (d) `sonuc.md` §0, §8 |
| K-7 | Tespit sürelerinin yalnız ulaşılan bağların ortancası olduğu yazıldı | `v2/17` T-10 |
| K-8 | Evre farklarına teşhis (c)'nin çekincesi eklendi | `v2/17` §3 |
| K-9 | Kaydedicinin kırık atfı düzeltildi; meşgul süresi kopyası için koruma testi (simülatörün gövdesiyle sözdizim ağacı eşitliği); öteki sentetik testler kaydedici yeniden kullanılırsa | `kalibrasyon/karistirma_isaretleri.py` · `tests2/test_karistirma_isaretleri.py` · `v2/17` §7 madde 13 |
| K-10 | Bayat tarih ve test sayısı; T-5'in gelecek zamanlı cümlesi | `v2/12` · `v2/17` T-5 |

## Sorunlar bölümünden

- §2.1 (`gecis_anlari` boş, meşgul integrali geçişte bölünmüyor): beyan `v2/05` §3.3b'ye taşındı.
- §2.2 (alanlar karıştırmadan önce de temizden ayrışıyor) ve §2.3 (çizelgeli karıştırmada tur artışı): `v2/17` §7 madde 7 ve 10.
- §2.4 (Puñal'in işbirliği bulgusunun düzeneği): `v2/17` T-6 ve §7 madde 6.
- §2.6 (`06` §0.4.5'in eski adları): `v2/17` §7 madde 11; mühürden önce hizalanır.
- §2.7 (T-5'in tek bir geçerli işaret listesi): T-5 yeniden düzenlendi.
- §2.5 (T-8'in Puñal'e ters seçimi) ve §2.8 (KR-2 açık): değişiklik yok; KR-2 §7 madde 4'te.

Bu düzeltmelerle 5-2 kapanır; sırada 5-3 (`v2/12` §1.2, açılış listesi `v2/17` §7).
