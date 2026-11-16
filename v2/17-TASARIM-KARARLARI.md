# 17 · TASARIM KARARLARI — DESPARETE'nin yeni sürümü

> Faz 5-2'nin çıktısı (`12` §1.2, K-252). Her konuda: ölçülmüş kanıt, kararım ve gerekçesi, ödünç alınan her özelliğin kaynağı. Seçeneklerin ayrıntısı ve kaynak notları `protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md`de, ölçümler `arsiv/teshis/faz5_2_*/sonuc.md`de. Köşeli parantezli numaralar `16`nın kaynaklarıdır.
>
> Sayısal değerler (aralıklar, pencereler, eşikler) burada seçilmez; 5-3'te kural kâğıtlarında yazılır ve geliştirme tohumlarında ölçülerek ayarlanır. Zaman sabitleri tek bir karıştırıcı çizelgesine göre ayarlanmaz; dayanıklılık hücresi bunun için var (`06` §0.4.5).
>
> Kararlar `T-n` diye numaralanır; kod yorumları bu numaralara atıf verir. Güncel: 16 Kasım 2026.

---

## 0 · İlkeler

**İlke 1 · Kısa bağ karıştırmaya dayanıklıdır, ama tek ölçüt değildir (16 Kasım).**

Alıcıya ulaşan sinyal, bağın uzunluğunun karesiyle zayıflar (ters kare yasası; simülatörde yol kaybı üsteli α = 2, `sim2/yapilandirma/konfig.py`). Karıştırıcının alıcıya ulaşan gücü ise bağın uzunluğuna değil, karıştırıcının alıcıya uzaklığına bağlıdır. Bağ yarıya kısalınca sinyal dört katına çıkar (+6 dB), karıştırıcının gücü aynı kalır; kısa bağın karıştırmaya karşı payı (marjı) büyüktür. Az atlamalı, uzun bağlı yollara yaslanmak elektronik harbe dayanıklılık hedefime terstir.

Bu, yalnız kısa bağ kullanılacağı anlamına gelmez: her fazladan atlama kanalda bir gönderim, bir kayıp olasılığı ve biraz gecikme daha demektir. Kısa bağı ayrı bir kuralla zorlamıyorum; bağın maliyeti ölçülen teslim oranından gelir (T-2). Karıştırma başlayınca payı küçük olan uzun bağların teslimi önce düşer, maliyetleri artar ve rotalar kendiliğinden kısa bağlara kayar.

- Ölçülen (karıştırıcısız ikiz; `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5): v0.4.1 paket başına 2,72 atlama yapıyor, atlama başına başarısızlığı %6,49, seçtiği bağın ortanca mesafesi 7,0–8,2 km; Babel'de 3,74 atlama, %2,32, 5,9–7,0 km. Bu hücrede Babel'in daha kısa bağlardan daha çok atlaması kazanıyor (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5). Sonuç bizim hücrelerimiz içindir, genel bir yargı değildir.

**İlke 2 · Ölçmeyi bırakmamak: kendini onaran ağ (16 Kasım).**

İHA'ların formasyonunu ve yörüngesini değiştiremem; yalnız paketin hangi yoldan gideceğini seçerim. Bu yüzden bir bağın bugünkü kötülüğü kalıcı sayılmaz: karıştırma biter, İHA'lar yaklaşır, bağ düzelir. Kullanmadığım bağı da ölçmeye devam ederim; düzelen bağ kendiliğinden yeniden kullanılır. Böylece ağ, kopan yerlerini dışarıdan bir müdahale olmadan onarır. Uygulaması T-1 ve T-3'te.

---

## 1 · Komşu ve bağ kalitesi (16 Kasım)

**Ölçülmüş kanıt** (karıştırıcısız ikiz; `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5 · `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md`):
- v0.4.1'de selam yok; komşu yoklama ve MAC onayıyla bilinir, 5 s duyulmayınca silinir. Koşu başına 15 171 komşu silinmesi ↔ Babel'de 315.
- Alınan duyuruların %64'ü, gönderen komşu "etkin" sayılmadığı için işlenmiyor.
- Ardıl ortalama 1,3 saniyede bir değişiyor.
- Yedekleri yoklamayla canlı tutmak (`hedefli_canlilik`) rota kaybını azaltmadı. v0.4.1'in kontrol trafiğinin kanalda kapladığı süre Babel'inkinin 2,69 katı.
- İletim farkı alıcıya ulaşan çerçevenin bozulmasında; yaklaşık yarısı seçilen bağın kalitesinden.

**T-1 · Komşunun varlığı: dinleme ve seyrek selam.**
- Komşudan çözülen her çerçeve (veri, onay, kontrol) o komşunun yaşadığının kanıtıdır. Bedeli yoktur (`13` §02.5, `cerceve_duyuldu`, K-172).
- Her düğüm sıra numaralı küçük bir selam yayar. Selam, ters yönün ölçülebilmesi için duyduğum komşuları ve her birinden aldığım selam oranını da bildirir (T-2).
- Selam aralığı uyarlanır: komşuluk sakinken uzar, değişince kısalır. Aralığın bir üst sınırı vardır; bağın kötüleştiği ya da düzeldiği ne kadar sürede fark edilecek, bu sınır belirler (T-3).
- Komşu yalnız hiç duyulmayınca (ne selamı ne başka bir çerçevesi) silinir. Kötü kalite silme sebebi değildir (T-3).
- Gerekçe: düzenli selam bütün komşuları ve iki yönü bilir ama sabit bir yük getirir. Yalnız kendi trafiğinden kanıt (v0.4.1) kullanılmayan komşuyu bilemez ve yedekleri bayatlatır. Yalnız dinleme, benden komşuya giden yönü göremez. Karma, en çok bilgiyi en az yükle verir.
- Ödünç: selam ve ters yön bildirimi ETX [36] ve Babel [4]; uyarlanır aralık Trickle [62] (RFC 6206'da ilanlar için, burada selama uygulanır); dinleme ilk taslağımdan (`arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/`, Protokol Taslağı v0 §6).

**T-2 · Bağ kalitesi: iki yönlü teslim oranı.**
- Bağın maliyeti beklenen gönderim sayısıdır: `ETX = 1 / (d_f · d_r)`. `d_f` komşunun benden aldığı selam oranı (komşu bildirir), `d_r` benim komşudan aldığım selam oranı. Kaç selamın kaybolduğu sıra numarasından bilinir. Yol maliyeti, bağ maliyetlerinin toplamıdır.
- Kullandığım bağlarda kendi unicast gönderimlerimin sonucu (`iletim_sonucu`, K-151) ek örnek olarak girer. Sebep: selam küçüktür ve büyük veri paketinin kaybını olduğundan iyi gösterir [36].
- Dinlenen çerçeveler komşunun varlığını kanıtlar, teslim oranını tek başına vermez: komşunun kaç çerçeve gönderdiği bilinmeden "kaçını duydum" bir oran değildir.
- Sinyal gücü (RSSI) maliyete girmez; yalnız bağlam olarak kullanılır [57].
- Gerekçe: teslim oranı kaliteyi doğrudan ölçer, en çok sınanmış ölçüdür ve raporda açıkça savunulabilir. v0.4.1'in M0.1'i yalnız kendi unicast sonuçlarını kullandığı için az trafik taşıyan iyi bir bağı belirsizlik cezasıyla pahalı gösteriyordu.
- Ödünç: ETX [36]; selam geçmişinden ölçme biçimi Babel [4].

**T-3 · Kötü bağ: kullanılmaz ama unutulmaz.**
- Beklenen gönderim sayısı bir üst sınırı aşan bağ yönlendirmede kullanılmaz. RPL'nin MRHOF'u bu sınırı 4 koyuyor [64].
- Bağ komşu listesinde kalır ve olağan selamlarla ölçülmeye devam eder. Bunun için ek yoklama gönderilmez: yedekleri yoklamayla canlı tutmak rota kaybını azaltmadı, kontrol trafiği zaten Babel'inkinin 2,69 katı.
- Kullanıma dönüş iki eşiklidir (histerezis): bağ, kullanımdan çıktığı eşikten belirgin biçimde iyi olunca yeniden aday olur. Tek eşikte, eşiğin çevresinde dolaşan bir bağ sürekli girip çıkar ve rotalar salınır (v0.4.1'de ardıl 1,3 saniyede bir değişiyor).
- Karıştırma bitince ya da İHA'lar yaklaşınca bağ kendiliğinden geri gelir (İlke 2).
- Bu iki eşik bağın kullanılabilirliği içindir; bir rotadan ötekine geçişin histerezisi ayrı bir konudur (bırakma zamanı).
- Ödünç: üst sınır ve histerezis MRHOF [64]; Babel'in histerezisi [55].

**T-4 · Kanal yoğunluğu bağ maliyetine girmez.**
- Gerekçe: yüke bağlı ölçü bir geri besleme döngüsü kurar: az yüklü yol seçilir, yüklenir, pahalılaşır, terk edilir; rotalar salınır [55]. Yoğunluk, karıştırma kanıtında ya da eşit maliyetli adaylar arasında ikincil ölçüt olarak ayrıca düşünülebilir.

**5-3'e kalanlar:** selam aralığının alt ve üst sınırı ve hangi olayın "değişim" sayılacağı · teslim oranının penceresi ya da düzgünleştirmesi · iki eşiğin değerleri · veri sonuçlarının ve dinlenen çerçevelerin ölçüye katılma biçimi · selamın biçimi ve boyutu (`13` §02.1, `MesajBicimi`).
