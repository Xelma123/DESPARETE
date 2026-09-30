# Evre metrikleri — çizelgeli karıştırıcı için öneri (denetim B8) — ⛔ GERİ ÇEKİLDİ (30 Eylül, yerine `evre_cizelgeli_oneri.md` v2; kusurları v2 §2)

> 30 Eylül 2026 gece · ajan · ön-kayıt metriği olduğu için uygulanmadan önce öğrenciye (K-203: tanım kapanışta yazılır).

## Sorun

`08`in dört metriği (M1 şok derinliği · M2 toparlanma tamlığı · M3 toparlanma süresi · M4 tespit gecikmesi) TEK bir açılma basamağı varsayar: TEMİZ `[50, T_j)` · ŞOK `[T_j, T_j+15)` · TOPARLANMA `[T_j+15, 320)`. Birincil hücrenin karıştırıcısı ise `T_j = 150`'den sonra **15 s açık · 15 s sessiz** çizelgeyle çalışıyor (~5,7 çevrim). ŞOK penceresi ilk açık evreyle çakışıyor, TOPARLANMA penceresi açık ve sessiz evreleri karıştırıyor: bugün birincil hücrenin M1–M4'ü anlamlı değil (K-200'de gözlendi).

## Öneri — evre katlama (epoch folding), sıfır yeni serbest sayı

Çizelgeli karıştırıcıda ölçüm penceresi üç evreye ayrılır: **TEMİZ** `[50, T_j)` · **AÇIK** (açık dönemlerin birleşimi) · **SESSİZ** (sessiz dönemlerin birleşimi). Paket doğum anına göre kovalanır (bugünkü `pdr_pencere` gibi).

| metrik | tanım | soru |
|---|---|---|
| **M1ç · açık evre kaybı** | PDR(TEMİZ) − PDR(AÇIK) | karıştırma sürerken ne kadar kaybediliyor |
| **M2ç · sessizde toparlanma tamlığı** | PDR(SESSİZ) / PDR(TEMİZ) | karıştırıcı susunca protokol temiz düzeye dönüyor mu (birincil hücrenin sınadığı "zamansal uyum", K-192) |
| **M3ç · sessizde toparlanma süresi** | sessiz dönemler başlangıçlarına göre hizalanır; her 1 s'lik faz kovasında PDR bütün çevrimlerden havuzlanır; ilk kova ki PDR ≥ PDR(TEMİZ) − z·SE | susma sonrası kaç saniyede toparlanıyor |
| **M4ç · açılmada tespit gecikmesi** | açık dönemler başlangıçlarına göre hizalanır; her 1 s'lik faz kovasında kopma beyanı çevrimlerden havuzlanır; ilk kova ki beyan sayısı TEMİZ evrenin boş dağılımını (negatif binom, K-196) aşar, Bonferroni kova sayısıyla | açılmayı kaç saniyede fark ediyor |

Sabitler bugünkülerin aynısı: ızgara 1 s (RFC 3561 `HELLO_INTERVAL`), tek α = 0,05 (z ve Bonferroni), SE kümelenmeye dayanıklı (K-196). Yeni serbest sayı yok: faz kovası = ızgara, katlama periyodu = çizelgenin kendisi (açık + sessiz). Havuzlama ~5 çevrimden → faz kovası başına ~200 paket (tek çevrimde ~40; SE ~0,07 bilgisiz olurdu).

Tek basamaklı karıştırıcıda (öteki aileler) bugünkü M1–M4 aynen kalır; çizelgeli karıştırıcıda M1ç–M4ç hesaplanır, ikisi aynı satırda karışmaz.

## Kapılar (uygulamadan önce yazılı)

- **G1ç boş kol:** karıştırıcısız kolda (aynı çizelgeyle "hayalet" evreler) M1ç 2 SE içinde, M2ç 1'den 2 SE içinde, M3ç = 0, M4ç sansürlü — gerçek protokollerle (G1-P gibi, 2 tohum × 4 protokol).
- **G2ç tutarlılık:** kâhinde M1ç > 0 (karıştırıcı gerçekten etkili) ve M2ç ≈ 1 (kâhin sessizde anında temiz).

## Maliyet

Son işlem (paket ve rota defterinden), sıcak yola dokunmaz; `sim2/olcum/evre.py`ye bir dal + test. Kapılar ~20–30 dk hesap.

## Karar istenen

1. Tanım bu mu (ya da değişiklik)?
2. Birincil metrik zaten PDR (pencere) — evre metrikleri betimleyici/mekanizma kanıtı olarak kalır (`06` §3); bu değişmiyor.
