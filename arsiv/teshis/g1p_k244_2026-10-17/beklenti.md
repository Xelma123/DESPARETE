# G1-P kaldı — M4'ün yanlış tespitlerinin sebebi · beklenti (ölçmeden önce)

> 17 Ekim 2026 · tetik: K-244 kuyruğunun G1-P'si (`arsiv/teshis/rakipler_k244_2026-10-14/G1p.txt`).
>
> - M4 yanlış tespit 2/8, sınır 1/8. M3 1/8 ve M1 1/4 tutuyor.
> - Yanlış tespit veren iki koşu OLSRv2 ve Babel, ikisi de tohum 1001'de, ikisi de hayalet açılmadan 47 s sonra.
> - Kuyruğun kuralı (§3): *"yeni bir protokol yüzünden kalırsa sebep ölçülür ve yürütücüye bildirilir."* G1-P'yi daha önce AODV, OLSR, AOMDV ve DESPARETE geçmişti (K-196); OLSRv2 ve Babel ilk kez giriyor.
>
> Betik `teshis.py`, donmuş kopyadan (`1163f81`).

## Ölçmeden önce bilinen

- **M4'ün tanımı** (`sim2/olcum/evre.py`, `tespit_gecikmesi`): boş dağılım, temiz evrenin 1 s kovalarındaki kopma beyanı sayısının ortalaması ve varyansıyla kurulan negatif binomdur; varyans ≤ ortalama ise Poisson. Eşik pencere başına α / taranan pencere.
- **Hiç beyan etmeyen protokol** (`beyan_etmiyor`) M4'ün dışındadır. Ama temiz evrede 0, sonra ≥ 1 beyan eden protokolde boş dağılım Poisson(0) olur ve eşik 0'dır: ilk beyan "tespit" sayılır. G1-P kaydında Babel 1001 bu durumda (ortalama 0, varyans 0).
- **Kopma beyanı:** Babel ve OLSRv2 bir rotanın sonraki atlaması olan komşu kullanılamaz olunca "kopma" beyan eder (`babel.py` `_beyanlar`, `olsrv2.py`).

## Düzen

- Dört protokol (AODV · OLSRv2 · Babel · DESPARETE), tohum 1001. G1-P'nin yapılandırması: `statik-yok`, yere toplama, tam pencere.
- 4 işçi, ~25 dk (G1-P'de en uzun koşu AODV, 21 dk).
- Her kopma beyanı düğüm, komşu ve zamanla yazılır. M4'ün iç sayıları yeniden hesaplanır.

## Ölçüt

1. **Kimlik:** tespit anları ve temiz ortalamalar G1-P kaydıyla aynı olmalı. Tutmazsa yorumlanmaz.
2. **Babel'in tespiti:** temiz evrede kopma beyanı 0 ise sebep **boş dağılımın yozlaşması** sayılır: eşik 0, tek beyan tespit. Protokolün davranışı değil, metriğin seyrek beyan eden protokoldeki sınırıdır.
3. **Ortak olay:** OLSRv2 ile Babel'in tespit penceresi çevresinde (±2 s) beyan ettiği bağlar karşılaştırılır.
   - Ortak bir bağ varsa sebep **iki protokolden bağımsız bir kanal olayı**dır: aynı tohumda aynı bağ aynı anda kopuyor. M4 karıştırıcıdan bağımsız gerçek bir kopmayı tespit ediyor.
   - Ortak bağ yoksa OLSRv2'nin tespiti kendi beyan kümelenmesinden gelir ve ayrıca incelenir.
4. **Karar:** sebep ölçülünce yürütücüye bildirilir; G1-P'yi geçirmek bir kural değişikliği ister. Seçenekler sonuçla birlikte sunulur. O karara kadar evre metrikleri bir sonuç için kullanılmaz (`v2/08`). AODV-k ve Babel'in donması kuyruk beklentisine göre G1-P'ye bağlıdır.

## Öngörü (ölçüt değil)

- Babel: temiz evrede 0 beyan.
- OLSRv2 ile Babel aynı bağı (ya da aynı düğümün bağlarını) aynı saniyede beyan ediyor. AODV ve DESPARETE'nin beyan hızı yüksek ya da kümelenmesi geniş olduğu için aynı olay onların eşiğini aşmıyor.
