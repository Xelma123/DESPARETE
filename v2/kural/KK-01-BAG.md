# KK-01 · Bağın durumu ve ölçüsü

> Kararlar: T-2 · T-3 · T-7 · T-9 · İlke 2 (`17`). Değerler ve genel kurallar `KK-00`. Güncel: 17 Kasım 2026 (kural kâğıtlarının bağımsız denetiminden sonra yeniden yazıldı: B-2 · B-3 · B-4 · B-5 · B-11 · B-12).

## Amaç ve sınıf

Her komşu bağının ne kadar iyi olduğunu (ETX) ve şu an kullanılıp kullanılamayacağını bilmek. Ölçü ve iki eşik **genel** (çekirdek); veri tetiği **genel** (`veri_kotu_tetigi`); "karıştırılıyor" durumu, dondurmalar ve hatırlanan kalite **karıştırmaya karşı** (`karistirma_durumu`, `hatirlanan_kalite`).

## Gördüğü

- Komşudan aldığı selamlar: sıra numarası, aralık (bir sonraki selama kadarki üst sınır), benim için bildirdiği oran (KK-02).
- Kendi veri gönderimlerinin sonucu (`iletim_sonucu`: başarılı mı, kaç yeniden deneme; K-151).
- Komşudan çözülen her çerçeve (`cerceve_duyuldu`, K-172): yalnız "hâlâ orada" bilgisi.
- KK-03'ten bağ kanıtı ("karıştırılıyor", sebebiyle) ve "bitti" olayları; kendi durumum ("karıştırılıyorum").

## Tuttuğu (komşu başına)

- `gecmis`: son `N` selamın geldi (1) / gelmedi (0) dizisi; `beklenen` sıra numarası; `son_selam_t`; komşunun son ilan ettiği aralık `a`.
- `d_f`: komşunun benim için bildirdiği oran.
- `veri`: son veri çerçevelerinin (an, deneme, başarılı) kayıtları.
- `durum`: OLAĞAN · ASKIDA · KÖTÜ · KARIŞTIRILIYOR; ASKIDA'ya giriş anı ve o andaki `gecmis` ile `d_f`; KARIŞTIRILIYOR'da `sebepler` kümesi, `hatira` (`gecmis`, `d_f`) ve giriş anı; KÖTÜ'de ceza bitişi, son veri sebepli KÖTÜ anı ve ceza süresi.
- `son_duyulma_t`: komşudan çözülen son çerçevenin anı; dondurmadan çıkışı işaretleyen bayrak.

## Durumlar

| durum | kullanılır mı | ölçülür mü |
|---|---|---|
| OLAĞAN | evet (aday, KK-04) | evet |
| ASKIDA | hayır | evet; sınıflanmayı bekler |
| KÖTÜ | hayır | evet (selamla) |
| KARIŞTIRILIYOR | hayır | hayır (donar); kalite hatırlanır |

## Kurallar

**Ölçü**

1. **Yeni komşu:** ilk selamıyla kayda girer ve KÖTÜ'de başlar (cezasız). Selamı olmayan çerçeveler yalnız var olan kaydın `son_duyulma_t`sini tazeler.
2. **Selam gelince** (sıra karşılaştırması 16 bit, modüler):
   - `0 ≤ sıra − beklenen ≤ N`: aradaki boşluk kadar `gecmis`e 0, gelen selam için 1 eklenir (Babel'in "ileri sarma"sı, RFC 8966 Ek A);
   - boşluk `N`'den büyük: komşu yeniden başlamış sayılır, `gecmis` sıfırlanır, 1 eklenir;
   - `sıra < beklenen` (geç gelen): zaman aşımıyla eklenmiş son 0 geri alınır, 1 olur ("geri alma");
   - **dondurmadan çıkıştan sonraki ilk selamda** (kural 9, 13): boşluk için 0 eklenmez, sıfırlama yapılmaz, yalnız 1 eklenir;
   - her durumda `beklenen ← sıra + 1`, `son_selam_t ← şimdi`, `a ← selamdaki aralık`.
3. **Zaman aşımı:** şimdi > `son_selam_t` + `ZAMAN_ASIMI` (1,5 × `a`) ise `gecmis`e 0 eklenir, `beklenen` bir ilerler; sonra her `a`da bir 0 daha. `a` komşunun bir sonraki selamına kadarki üst sınır olduğu için olağan aralık değişimi sahte kayıp üretmez (KK-02).
4. **Teslim oranı:** `d_r = gecmis'teki 1'ler / örnek sayısı` (en çok `N`); `gecmis` boşsa tanımsız.
5. **ETX:** `ETX_selam = 1 / (d_f · d_r)`; biri 0 ya da tanımsızsa ∞ (tek yönlü bağ kullanılmaz).
6. **Veri tetiği** (`veri_kotu_tetigi`): son `VERI_PENCERE` veri çerçevesinde (en çok 10 s geriye) en az `VERI_EN_AZ` çerçeve varsa `ETX_veri = Σ deneme / Σ başarılı` (deneme = yeniden deneme + 1; başarı yoksa ∞). Yalnız kullanılabilirliğe girer, maliyete girmez (T-2). Kendim karıştırılırken veri sonuçları pencereye yazılmaz (kural 13).

**Geçişler**

7. **OLAĞAN → ASKIDA:** `ETX_veri > E_CIK`. Bağ hemen kullanımdan çıkar; giriş anındaki `gecmis` ve `d_f` saklanır. Sebep: alıcısı karıştırıcıya çok yakın bağda alıcı hiç selam gönderemez, karıştırma kanıtı veri tetiğinden geç gelir; bağ "kötü" diye sınıflanırsa hatıra yiter ve ceza katlanır.
8. **ASKIDA'dan çıkış:** `ASKIDA_SURE` içinde KK-03'ün bağ kanıtı gelirse → KARIŞTIRILIYOR (hatıra ASKIDA'ya girişteki ölçüden); gelmezse → KÖTÜ (veri sebepli, kural 11).
9. **OLAĞAN ya da ASKIDA → KARIŞTIRILIYOR** (KK-03'ün bağ kanıtıyla): sebep kümeye eklenir; `hatira ← (gecmis` sonundaki ardışık 0'lar atılarak, `d_f)`; `veri` boşaltılır. KARIŞTIRILIYOR iken:
   - gelen selamlar `gecmis`e, bildirilen oran `d_f`ye yazılmaz, zaman aşımı 0 eklemez (ölçü donar, T-7);
   - `beklenen`, `son_selam_t` ve `a` gelen selamlarla izlenir; selam KK-03'e verilir;
   - yeni bir bağ kanıtı gelirse sebebi kümeye eklenir.
10. **KARIŞTIRILIYOR'dan çıkış:**
    - kümedeki her sebebin "bitti"si gelince (KK-03 kural 9): girişten beri `T_HATIRA` geçmediyse hatıra geri yüklenir (`hatirlanan_kalite` kapalıysa `gecmis` boşaltılır); hatıra ETX'i `E_CIK`ı aşmıyorsa OLAĞAN, aşıyorsa KÖTÜ (cezasız). `veri` boş başlar; ilk selamda kural 2'nin dondurma çıkışı uygulanır.
    - **üst süre:** girişten beri `T_HATIRA` geçtiği hâlde hâlâ KARIŞTIRILIYOR ise `gecmis` boşaltılır ve bağ KÖTÜ'ye geçer (cezasız); bağ yeniden ölçülerek döner. Böylece "bitti"si gelmeyen bir giriş bağı süresiz kullanım dışı bırakamaz (İlke 2).
11. **KÖTÜ'ye giriş ve ceza:**
    - OLAĞAN → KÖTÜ: `ETX_selam > E_CIK` (cezasız).
    - ASKIDA → KÖTÜ (veri sebepli): en az `T_CEZA` KÖTÜ kalır. Önceki veri sebepli KÖTÜ'den beri 60 s geçmediyse süre ikiye katlanır (en çok 40 s). Veri tetiğinin karıştırma kanıtıyla KARIŞTIRILIYOR'a dönüştüğü düşüşler sayılmaz. Sebep: KÖTÜ bağa veri gitmez, veri ölçüsü eskir; ceza olmasaydı bağ selam ölçüsüyle hemen döner ve gidip gelirdi.
12. **KÖTÜ → OLAĞAN:** `ETX_selam < E_DON`, örnek sayısı ≥ `ORNEK_EN_AZ` ve ceza (varsa) doldu. KÖTÜ'de karıştırma kanıtı izlenmez (bağ zaten kullanılmıyor). KÖTÜ'ye girişte olay sayısı kuralı (T-10) uygulanmaz: iki eşikli histerezis aynı işi görür (`17` T-11'in 5-3'e kalanı).
13. **Kendim karıştırılırken** (KK-03 kural 4, "karıştırılıyorum"): hiçbir komşunun `gecmis`ine, `d_f`sine ve `veri`sine yazılmaz; zaman aşımı 0 eklemez; `beklenen`, `son_selam_t`, `a` izlenir; silme süresi durur ve çıkışta kaldığı yerden sürer. Çıkışta her komşunun `son_selam_t`si o ana çekilir ve her komşunun ilk selamında kural 2'nin dondurma çıkışı uygulanır. Sebep: karıştırılan benim; komşularıma bildirdiğim oranları bozarsam, karıştırma bitince bana olan bağları hatırladıkları kaliteyle geri alırken benim düşük bildirimimle hemen KÖTÜ'ye düşerler.
14. **Silme:** `T_SILME` boyunca komşudan hiçbir çerçeve duyulmazsa kayıt silinir (her durumdan; kural 13'teki duraklama hariç).

**Aynı olayda sıra** (bir selam, zaman aşımı, MAC sonucu ya da saniyelik iş birden çok geçiş koşulunu doğurursa):

15. Önce KK-03'ün bağ kanıtı (→ KARIŞTIRILIYOR), sonra veri tetiği (→ ASKIDA), en son `ETX_selam` eşikleri. `gecmis`in sonundaki ardışık sıfırlar KK-03 kural 6'nın `k`sına ulaşmışsa KÖTÜ denetimi o sıfırlar hariç yapılır: sessizlik karıştırma olarak sınıflanır. Kenar bağlarda (`k` büyük) `ETX_selam` eşiği sessizlikten önce aşılırsa bağ KÖTÜ olur; bu kabul edilen bir sonuçtur (kenar bağ zaten kötüye yakındır).

## Örnek

Komşu j'nin son 16 selamından 13'ü geldi: `d_r = 13/16 ≈ 0,81`; j benim selamlarımın 0,90'ını aldığını bildiriyor: `ETX = 1 / (0,81 × 0,90) ≈ 1,37`, OLAĞAN. j karıştırıcıya çok yakın kalır ve hiç selam gönderemez; j'ye giden veri çerçeveleri vazgeçmeyle biter. Dördüncü başarısız çerçevede `ETX_veri` 4'ü aşar, bağ ASKIDA'ya geçer ve kullanımdan çıkar (ölçü saklanır). Dört saniye içinde j'den beklenen selamlar gelmez; KK-03 sessizlik kanıtı verir, bağ KARIŞTIRILIYOR olur ve 1,37 hatıraya alınır. Karıştırıcı susunca j'nin iki selamı gelir, bağ 1,37'yle OLAĞAN'a döner; ceza yoktur.

## Sınanması

- `hatirlanan_kalite` açık ↔ kapalı: birincil ve dayanıklılık hücresinde `PDR_açık` ve sessiz dönemin ilk saniyelerindeki teslim; ikizde fark yok.
- `veri_kotu_tetigi` açık ↔ kapalı: ikizde pencere PDR'si, iletim kaybı (İ) ve atlama başına başarısızlık; tanı: veriyle KÖTÜ sayısı bağ başına ve geçide uzaklığa göre (denetim S-1).
- Eşikler (`E_CIK`, `E_DON`): ardıl değişim sıklığı ve KÖTÜ ↔ OLAĞAN geçiş sayısı.

## Kaynak

ETX [36]; selam geçmişi, ileri sarma, geri alma ve zaman aşımı katsayısı Babel [4] (RFC 8966 Ek A; `protokoller/babel_bicim.py`); üst sınır MRHOF [64]; iki eşikli kullanılabilirlik, askıda durumu ve hatırlanan kalite bu tasarımın.
