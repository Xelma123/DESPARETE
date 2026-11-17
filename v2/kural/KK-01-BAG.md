# KK-01 · Bağın durumu ve ölçüsü

> Kararlar: T-2 · T-3 · T-7 · T-9 · İlke 2 (`17`). Değerler `KK-00`. Güncel: 17 Kasım 2026.

## Amaç ve sınıf

Her komşu bağının ne kadar iyi olduğunu (ETX) ve şu an kullanılıp kullanılamayacağını bilmek. Ölçü ve iki eşik **genel**; "karıştırılıyor" durumu ve hatırlanan kalite **karıştırmaya karşı** (bayraklar `karistirma_durumu`, `hatirlanan_kalite`).

## Gördüğü

- Komşudan aldığı selamlar: sıra numarası, aralığı, benim için bildirdiği oran (KK-02).
- Kendi tek alıcılı gönderimlerinin sonucu (`iletim_sonucu`: başarılı mı, kaç yeniden deneme; K-151).
- Komşudan çözülen her çerçeve (`cerceve_duyuldu`, K-172): yalnız "hâlâ orada" bilgisi.
- KK-03'ten "karıştırılıyor" ve "bitti" olayları.

## Tuttuğu (komşu başına)

- `gecmis`: son `N` selamın geldi (1) / gelmedi (0) dizisi; `beklenen` sıra numarası; `son_selam_t`; komşunun son ilan ettiği aralık `a`.
- `d_f`: komşunun benim için bildirdiği oran.
- `veri`: son çerçevelerin (deneme, başarılı) çiftleri.
- `durum`: OLAĞAN · KÖTÜ · KARIŞTIRILIYOR; KARIŞTIRILIYOR'da `hatira` (ETX ve dondurulmuş `gecmis`) ve giriş anı.
- `son_duyulma_t`: komşudan çözülen son çerçevenin anı.

## Kurallar

1. **Selam gelince:** sıra numarasıyla `beklenen` arasındaki boşluk kadar `gecmis`e 0, gelen selam için 1 eklenir (Babel'in "ileri sarma"sı, RFC 8966 Ek A). Boşluk `N`'den büyükse komşu yeniden başlamış sayılır, `gecmis` sıfırlanır (Babel'in kuralı).
2. **Gelmeyen selam:** şimdi > `son_selam_t` + `ZAMAN_ASIMI` (1,5 × `a`) ise `gecmis`e bir 0 eklenir ve `beklenen` bir ilerler; sonra her `a`da bir 0 daha. Böylece hiç gelmeyen selam da sayılır. O selam geç gelirse (sıra < `beklenen`) eklenen 0 geri alınır (Babel'in "geri alma"sı, RFC 8966 Ek A).
3. **Teslim oranı:** `d_r = gecmis'teki 1'ler / gecmis'teki örnek sayısı` (en çok `N`).
4. **ETX:** `ETX_selam = 1 / (d_f · d_r)`; `d_f` ya da `d_r` 0 ise ∞ (tek yönlü bağ kullanılmaz). Örnek sayısı `ORNEK_EN_AZ`ın altındaysa bağ henüz aday değildir.
5. **Veri sonucu** (bayrak `veri_kotu_tetigi`): son `VERI_PENCERE` veri çerçevesinde `ETX_veri = Σ deneme / Σ başarılı` (deneme = yeniden deneme + 1; hiç başarı yoksa ∞). Yalnız kullanılabilirliğe girer, maliyete girmez. Sebep: veri denemelerinin başarısı kanal yüküne bağlıdır; maliyete girerse T-4'ün kaçındığı salınım geri gelir. Selam ise büyük paketin kaybını olduğundan iyi gösterir [36]; bu tetik onu yakalar.
   - `ETX_veri > E_CIK` olunca: komşunun selamında `karistiriliyorum` = 1 ya da benim girişim işaretim varsa (KK-03) bağ **KARIŞTIRILIYOR** olur; karıştırma kötü bağ sanılmaz.
   - Yoksa bağ **KÖTÜ** olur ve en az `T_CEZA` KÖTÜ kalır; 60 s içinde yinelenirse süre ikiye katlanır (en çok 40 s). Sebep: KÖTÜ bağa veri gönderilmez, `ETX_veri` 10 s sonra eskir; ceza olmasaydı bağ selam ölçüsüyle hemen geri döner, aynı yere düşer ve gidip gelirdi.
6. **Geçişler:**

| nereden | nereye | koşul |
|---|---|---|
| OLAĞAN | KÖTÜ | `ETX_selam > E_CIK` ya da `ETX_veri > E_CIK` |
| KÖTÜ | OLAĞAN | `ETX_selam < E_DON`, yeterli örnek ve (veriyle düştüyse) `T_CEZA` doldu |
| OLAĞAN | KARIŞTIRILIYOR | KK-03'ün "karıştırılıyor" olayı; `gecmis` (sonundaki ardışık 0'lar atılarak: onlar tespitten önce karıştırmanın biriktirdiği kayıptır), `d_f` ve olayın **sebebi** `hatira`ya alınır; hatıra ETX'i bunlardan hesaplanır (KK-03 "bitti"yi sebebe göre verir) |
| KARIŞTIRILIYOR | OLAĞAN ya da KÖTÜ | KK-03'ün "bitti" olayı; `T_HATIRA` geçmediyse `hatira` geri yüklenir, hatıra ETX'i `E_CIK`ı aşmıyorsa OLAĞAN, aşıyorsa KÖTÜ; `T_HATIRA` geçtiyse `gecmis` boşaltılır ve bağ KÖTÜ'den yeniden ölçülerek döner |
| herhangi biri | silinir | `T_SILME` boyunca komşudan hiçbir çerçeve duyulmadı |

7. **KARIŞTIRILIYOR iken** gelen selamlar `gecmis`e, komşunun bildirdiği oran `d_f`ye yazılmaz (ölçü donar, T-7); ama KK-03'e "selam geldi" olayı olarak verilir. Dönüşte `d_f` hatıradan gelir, komşunun sonraki selamıyla güncellenir. Sezilmeyen zayıf karıştırmada ölçü kendisi düşer ve rotalar kısa bağlara kayar (İlke 1).
9. **Kendim karıştırılırken** (KK-03 kural 4, "karıştırılıyorum") hiçbir komşunun `gecmis`ine yazılmaz: ne gelen selam ne zaman aşımı sayılır. Sebep: karıştırılan benim; komşularıma ölçtüğüm oranları (selamdaki liste) bozarsam, onlar karıştırma bitince bana olan bağları hatırladıkları kaliteyle geri aldıklarında benim bildirdiğim düşük oranla hemen KÖTÜ'ye düşerler ve hatıranın anlamı kalmaz. KK-03'ün selam kaybı sayımı (`s`) bu dondurmadan bağımsız, ham gelen–beklenen sayısından yapılır.
8. KÖTÜ bağ için karıştırma kanıtı izlenmez: zaten kullanılmıyor.

## Örnek

Komşu j'nin son 16 selamından 13'ü geldi: `d_r = 13/16 ≈ 0,81`. j, benim selamlarımın 0,90'ını aldığını bildiriyor: `ETX = 1 / (0,81 × 0,90) ≈ 1,37`, OLAĞAN. Karıştırıcı açılınca KK-03 "karıştırılıyor" der; 1,37 hatıraya alınır. 15 s sonra "bitti" gelir; 15 < 30 olduğu için bağ hemen 1,37'yle OLAĞAN'a döner. Hatıra olmasaydı, 16 selamlık geçmişin yeniden dolması 2 s aralıkla ~30 s sürerdi.

## Sınanması

- `hatirlanan_kalite` açık ↔ kapalı: birincil ve dayanıklılık hücresinde `PDR_açık` ve sessiz dönemin ilk saniyelerindeki teslim; ikizde fark yok.
- `veri_kotu_tetigi` açık ↔ kapalı: ikizde iletim kaybı (İ) ve atlama başına başarısızlık.
- Eşikler (`E_CIK`, `E_DON`): ardıl değişim sıklığı ve KÖTÜ ↔ OLAĞAN geçiş sayısı.

## Kaynak

ETX [36]; selam geçmişi, ileri sarma ve zaman aşımı katsayısı Babel [4] (RFC 8966 Ek A); üst sınır MRHOF [64]; iki eşikli kullanılabilirlik ve hatırlanan kalite bu tasarımın.
