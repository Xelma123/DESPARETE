# KR-E · Düğüm kaybında birincil metrik — beklenti (ölçmeden önce)

> 26 Eylül 2026 · karar öğrencinin devriyle ajanın (K-182) · uygulama ajan

## Karar

- **Birincil metrik PDR kalır.** Kohortu, doğduğu anda kaynağı ve hedefi yaşayan paketlerdir.
  - Ölü kaynak zaten doğurmaz.
  - Ölü hedefe doğan paket kohort dışında kalır, çünkü hiçbir protokol onu teslim edemez.
  - Ölüm anları hash'ten ve protokolden bağımsızdır; her kolda aynı paketler dışarıda kalır, dolayısıyla hiçbir protokol bundan yarar sağlayamaz.
  - Kayıp yoksa PDR bugünkü PDR'nin birebir aynısıdır.
- **İkincil (raporlanır): `gorev_teslim_orani`** = teslim / planlanan talep.
  - Planlanan talep = doğan + ölü hedefe doğan + ölü kaynağın doğuramadığı.
  - Düğüm kaybının göreve bedelini bu oran okur: kayıplı ve kayıpsız hücre karşılaştırması bununla yapılır.
- **Neden ikisi ayrı:** K-180'de PDR, tek atlamada 5 ölümle 0,459'dan 0,476'ya çıktı. Bu, protokoller arası karşılaştırmayı bozmaz (ölümler her kolda aynı), ama "kayıp ne kadar zarar verdi" sorusunu yanlış yanıtlar. Görev oranı o soruyu yanıtlar.

## Tam takım

- 889 + 2 = **891 passed**.

## Regresyon `k181 ↔ k182`

**Simülasyon birebir aynı.** Değişen yalnız ölçüm: korunum, sayaçlar ve teslim kümesi aynı kalır.

- `t-` dışı 65 vaka birebir. İzinli yeni alanlar:
  - `metrikler.gorev_teslim_orani` ve `_pencere` — her satırda `pdr` ve `pdr_pencere`ye birebir eşit;
  - `ham.olu_hedefe_dogum_s` ve `ham.uretilmeyen_dogum_s` — boş.
- `t-` vakaları ilan edilmiş değişen:
  - `korunum` bölümü k181 ile aynı;
  - PDR ≥ k181'deki (pay aynı, payda küçülür);
  - `gorev_teslim_orani` ≈ teslim / ikizin üretimi:
    - tek atlama ≈ 688/1598 ≈ **0,43** — ikizin PDR'si 0,459'un ALTINDA; kayıp artık görünür;
    - AODV ≈ 956/1600 ≈ **0,60**.
