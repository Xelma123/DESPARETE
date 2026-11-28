# Faz 5-3 · yeni tasarımın bağımsız denetiminin kapanışı

> 28 Kasım 2026 · rapor `DENETIM-RAPORU-TASARIM-2026-11-28.md` (denetlenen hâl `a305643`, tasarım belgeleri `3a71a0b`'deki hâliyle; istem `DENETIM-PROMPT-TASARIM-2026-11-28.md`) · hüküm: "dondurulmaya ve kodlanmaya hazır değil" · bulgular: 1 engelleyici, 5 önemli, 6 küçük; hepsi belge düzeyinde.
>
> Bulguların hepsi kaynağından doğrulandı:
> - E-1'in hesabı (raporun Ek A.1'i) kayıtlardan birebir yeniden üretildi: a2 0,0383 · alt ağaçta 0,0274 · katman kanıtlı 0,0143 · bunun alt ağaçta 0,0109'u · K6 0,1364 · alt ağaçta 0,0829. Babel'in "tercih edilir" koşulu RFC 8966 §3.8.2.2'de ve `protokoller/babel.py`'de okundu.
> - Ö-5'in tablosu B2 teşhisinin kayıtlarından birebir yeniden çıktı (birincilde 1 009, dayanıklılıkta 694 düğüm-saniye).
> - Ö-2'nin eksik sayacı eğim0'ın 16 koşusunun kayıtlarında görüldü; döngü kuralları ölçümünün `sayac` işlevi eksik anahtara 0 döndürüyor.
> - Öteki kaynaklar: RFC 8966 §3.7.2, §3.8.1.1, §3.8.1.2; KK-02 kural 3; 17 Kasım kapanışının B-10 ve B-16 kararları; Babel-a'nın beyanları (`_beyanlar`); simülatörün kontrol kuyruğu (kapasite 50, `sim2/kosum/kontrol_durum.py`) ve eşit anlı olayların sırası (`sim2/cekirdek/olaylar.py`).
>
> Önerilen düzeltmeler onaylandı (28 Kasım). Bileşenlerin ana seçenekleri değişmedi. İkinci okumada (raporun §7'si) engelleyici bulgu kalmadı; tasarım dondurulmaya ve kodlanmaya hazır.

## Kararlar

| bulgu | karar | yer |
|---|---|---|
| E-1 · kural 10a'nın sınıf dalı | İstek yalnız ilan ettiği maliyet benimkinden küçük komşuya gider (`C_j` < C). Yolu benden geçen komşu böylece dışlanır; yeni turdan sonra hedefin uygulanabilir olması da sağlanır (maliyetim düşmedikçe). Kural 10a'dan sonra `YOK_SAYMA_S` boyunca, istenen tur ne olursa olsun, yeni 10a isteği gitmez. Not: kararlı durumda FD maliyetime eşit olduğu için sınıf dalı çoğunlukla geçiş anlarında (eski turlu ilan) ya da maliyetim aynı turda yükseldiğinde çalışır; kazancı küçük, ama artık zararsız. | B4 kural 10a, §3, §6, §8, §11 madde 8, §12 madde 8, §13 madde 16, §14, §15 · `00-DIZIN` `YOK_SAYMA_S` · `18` §2.4 eki, §2.5 · `01-BUTUNLUK` §2, §10 |
| Ö-1 · tur değişimi olayı | RFC 8966 §3.7.2'ye ve 17 Kasım kararına (B-10) dönüldü: selamı yalnız tutulan bir isteği karşılayan tur değişimi ve geçidin istekle artışı öne çeker; öteki tur değişimleri planlı selamla yayılır. B4 kural 15 ile B6 kural 7 aynı cümleyle yazıldı. Ölçülen %2,7'lik selam payı bu kuralla ölçülmüştü. | B6 kural 7, §1, §14 · B4 kural 15, §6, §13 madde 11 · `18` §2.6 · `01-BUTUNLUK` §2 |
| Ö-5 · kilitte selamı susturmak | B6 kural 11 kaldırıldı, numarası korunur. Selam kilitte de kurulur; tam kilitte kontrol kuyruğunda bekler ve kanal açılınca gider. Kilit işaretli saniyelerin %57–66'sında kanal kısmen boştu. B6'nın karıştırma eki kalmadı. | B6 kural 11–12, §1–4, §6, §8–15 · B1 Ö-5, §8, §12 · B2 §9–11 · B5 kural 6, §12 · B7 §8 · `00-DIZIN` bayraklar, gözlem · `18` §1.4, §2.6 · `01-BUTUNLUK` §3, §5, §6, §10 |
| Ö-4 · beyanlar (ikinci okumada Y-1 ile düzeltildi) | B4 kural 18. `kopma(K)`: bir önceki niyetli kancada ardılım olan K, bağı KULLANILMAZ olduğu, silindiği ya da ilanının ömrü dolduğu için aday değil. S'ye düşmek, ∞ ilan, yok saymanın sonu ve daha iyi adaya geçiş kopma değildir. `rota_kuruldu(K)`: K'nin kopmasından sonra yeniden ardılım var. Anlamları Babel-a'nınki (K-139): Babel-a susan komşuyu bağın maliyetiyle (~42 s), DESPARETE ilanın ömrüyle (en çok ~7,7 s) tanır. İlk yazılan tanım ilanın ömrünü saymıyordu; susan ardıl için kopma hiç beyan edilmezdi (Y-1). | B4 kural 16, 18, §9, §13 madde 18, §14 · `18` §1.4 olay sırası 7 · `01-BUTUNLUK` §4, §8 · `00-DIZIN` bayraklar |

## Düzeltmeler

| bulgu | yapılan | yer |
|---|---|---|
| Ö-2 | Kural 17'nin adı "aynı düğüme dönüş"; yalnız tanıdır, 0 olması beklenmez ve hata sayılmaz. Döngünün sınaması ardıl grafiğinde, her olaydan sonra. §15'in "paket aynı düğüme dönemez" çıkarımı düzeltildi. `18` §2.4'teki "ölçüldü: 0" ve döngü kuralları sonucunun eğim0 satırı için "sayaç yoktu, ölçülmedi" notu yazıldı. | B4 kural 17, §2, §3, §11 madde 7, §13 madde 12 ve tanı, §15 · B5 §2, §3, §8, §11 · B7 §2 · `18` §1.4, §2.4 · `00-DIZIN` gözlem · `01-BUTUNLUK` §5 S4, §7, §8 · `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md` |
| Ö-3 | B1'in olay listeleri niyetsiz kancalarda birikir, niyetli kancanın sonunda boşalır. | B1 kural 18, §3, §9 · `18` §1.4 notu · `01-BUTUNLUK` §4 |
| K-1 | Yok saymada uygulanabilirlik kabul edilen ilanla, tazelik son ilanla değerlendirilir; ardıl değişince yok sayma biter. | B4 kural 3 |
| K-2 | Kendi aralığım açılınca (geriye dönük açılan dâhil) göndericinin sayımı sıfırlanır. | B2 kural 12 |
| K-3 | Kilitten sonra kaydı silinmiş paket yeni sayılır, en çok `TUTMA_EN_COK_S` daha bekler. | B7 §8 |
| K-4 | Rota isteğine (h = 1) rotası ∞ olan düğüm ∞'lu selamla yanıt verir (RFC 8966 §3.8.1.1, MUST). | B4 kural 4a, 12, §13 madde 17 |
| K-5 | Rotası ∞ olan düğüm tur isteğini iletmez (RFC 8966 §3.8.1.2; 17 Kasım B-16). | B4 kural 12, §13 madde 17 |
| K-6 | B6 §9'un olay sırası numarası; B2 kural 6'da "girişim işareti olmayan saniye"; B3 kural 7'nin en az kayıt koşulu; B7 kural 3'te daha erken plan varken yeni plan kurulmaması; B2 §12, B3 §12 ve `01-BUTUNLUK` S2'de selamların varış varsayımları. | B6 §9 · B2 kural 6, §12 · B3 kural 7, §12 · B7 kural 3 · `01-BUTUNLUK` §5 |

## Sorunlar bölümünden

| sorun | yapılan |
|---|---|
| S-1 · genel mekanizmalar katmanın işinin büyüğünü görüyor | `01-BUTUNLUK` §10'da yazılı; Aşama 4'ün beklentisine |
| S-2 · 30 s'den uzun kendi aralığının sonunda bütün bağlar bir an KULLANILMAZ | düzeltildi: `d_f`'nin yaşı hariç aralıklar çıkarılarak ölçülür (B1 kural 12) |
| S-3 · kendi karıştırılmamda ölen ardıl | bilinçli sonuç olarak yazıldı (B4 kural 14) |
| S-4 · iki meşgul payı eşiği | Aşama 4'e (`00-DIZIN`); kilit saniyelerinin %37'sinin kâhinin U alanında olduğu not edildi |
| S-5 · yol maliyetinin doyması | bu dünyada oluşmaz; değişiklik yok |
| S-6 · rota isteği yanıtı aralığı kısaltıyor | kontrol payı kestirimine kalem eklendi (`01-BUTUNLUK` §2, ~%0,1–0,3) |
| S-7 · tamponun her uyandırmada dökülmesi | davranışı değiştirmez; değişiklik yok (B7 kural 3 zaten yazıyor) |

## Kestirimler (bağımsız denetimden sonra)

- **Mekanizma kapısı:** katmana ait ölçülmüş üst sınırların toplamı ~0,02 (önce ~0,03). Kural 10a'nın katman payı, alt ağaç hedefleri çıkınca en çok ~0,003; B6 kural 11'in payı kalktı. Kapının geçmesi ölçülmemiş paylara bağlı (B4 kural 4'ün yaşı, B3'ün hariç aralığı). Aşama 4'ün beklentisine "ölçülmüş paylar eşikte" diye yazılır.
- **Kontrol payı:** protokolün iletileri ~%3–3,5, onaylarla ~%6–7. Tur olayı daraltılmasaydı (Ö-1) ve kural 10a sınırlanmasaydı (E-1) bu kestirim iyimser kalırdı.

## İkinci okuma

Raporun §7'si (28 Kasım; okunan hâl: `a305643` ve commit edilmemiş düzeltmeler). Hüküm: **engelleyici bulgu kalmadı**. E-1, Ö-1, Ö-2, Ö-3, Ö-5, K-1…K-6 ve S-2, S-3, S-6 kapandı. Ö-5'te kuralı kaldırmak ve E-1'de `C_j` < C seçimi savunulabilir bulundu.

| bulgu | yapılan | yer |
|---|---|---|
| Y-1 · kopma tanımı susan ardılı dışarıda bırakıyordu (önemli) | Kararım: ilanının ömrü dolduğu için bırakılan ardıl da kopmadır. Doğrulandı: teşhis (c)'nin kayıtlarında Babel-a koşu başına 1,88 (ikiz) ve 6,5 (birincil) kopma beyan ediyor; fiziksel kopma 3,75. | B4 kural 18, §13 madde 18 · `01-BUTUNLUK` §8, §13 |
| Y-2 · `18` §2.4'ün tablosu dipnotla bölünmüştü (küçük) | dipnot tablonun altına alındı | `18` §2.4 |
| Y-3 · B1'de `d_f`'nin süresi üç yerde eski ifadeyle (küçük) | yaş hariç aralıklar çıkarılarak; sınama 6'ya madde | B1 §4, §8, §13 madde 6 |
| kural 10a'nın daralan kapsamı (sorun) | Yazıldı: kararlı durumda sınıf dalı yalnız eski turlu ilanlarda ve maliyetim aynı turda yükseldiğinde çalışır; benden pahalı temiz kardeş dal artık hedef olmaz. "En çok ~0,011", yeni koşulun ancak bir kısmına ulaşabileceği bir üst sınırdır. Kardeş dalları korumak için önerilen ek mekanizma (son birkaç saniyede veri getiren komşuyu dışlamak) alınmadı: gerekli değil, kazancın üst sınırı küçük. | B4 §1, §15 · `18` §2.4 eki, §2.5 |

Bilinmesi gerekenler (bulgu değil):
- Kilitten sonra kuyruktan gelen bayat selamlar bit 1 taşır; alıcıda bağ birkaç milisaniye S görünebilir.
- Ö-1'den sonra yeni tur, istek yolu dışında planlı selamlarla (atlama başına en çok ~2,2 s) yayılır; eski turlu ilanlar daha uzun kalır.

İkisi de tanıda görülür (B4 §13, B6 §13). Denetçiye göre bu değişiklikler tek bir tanım ve metinlerden ibaret olduğu için yeni bir okuma gerekmez.

**Sonuç:** tasarım dondurulmaya ve kodlanmaya hazır. Aşama 3.2 tamam (28 Kasım); sırada 3.3, donma ve büyük ölçümün beklentisi.
