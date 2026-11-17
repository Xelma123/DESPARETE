# Faz 5-3 · kural kâğıtlarının bağımsız denetiminin kapanışı

> 17 Kasım 2026 · rapor `DENETIM-RAPORU-KURAL-2026-11-17.md` (denetlenen hâl `94c0ed6`; istem `DENETIM-PROMPT-KURAL-2026-11-17.md`) · hüküm: "kodlamaya hazır değil" · bulgular: 3 engelleyici, 10 önemli, 7 küçük; hepsi belge düzeyinde.
>
> Engelleyici üç bulgu kaynağından doğrulandı (RFC 8966 §3.5.1; `sim2/kosum/kosu.py:215–216`; KK-03'ün tablosu). Karar gerektiren üç noktada önerilen seçenekler kabul edildi. KK-01 ve KK-03 yeniden yazıldı; öteki kâğıtlar düzeltildi.

## Kararlar

| bulgu | karar | yer |
|---|---|---|
| B-11 · karıştırılan göndericinin bağları | Kendim karıştırılırken MAC sonuçları bağ kanıtı sayılmaz, veri tetiğine girmez; ardıl korunur | KK-03 kural 8 · KK-01 kural 6, 13 · `17` T-9 |
| B-2 · veri tetiği ↔ karıştırma kanıtı | Yeni durum ASKIDA: veri tetiğiyle bağ hemen kullanımdan çıkar; `ASKIDA_SURE` içinde karıştırma kanıtı gelirse KARIŞTIRILIYOR (hatıra tetikten önceki ölçüden), gelmezse KÖTÜ; ceza yalnız karıştırma kanıtsız tekrarlarda katlanır; KARIŞTIRILIYOR'a girişte veri penceresi boşaltılır | KK-01 kural 7–9, 11 · KK-00 `ASKIDA_SURE` · `17` T-2 |
| B-10 · tur değişimi tetiği | RFC'ye ve T-17'ye uyuldu: yalnız bekleyen bir isteği karşılayan tur değişimi hemen selam gönderir; iletilen istekler `ISTEK_ANIMSA` süre tutulur, yanıt istek yolundan geri yayılır | KK-02 kural 3 · KK-04 kural 9 · KK-00 `ISTEK_ANIMSA` |

## Düzeltmeler

| bulgu | yapılan | yer |
|---|---|---|
| B-1 | ∞ ilan her zaman uygulanabilir; `A` yalnız sonlu ilanlı; yok sayma yalnız sonlu uygulanamaz ilan için; seçili ardıldan ∞ gelince ardıl hemen bırakılır | KK-04 kural 1, 2, 4, 7 · `17` T-13 |
| B-3 | "Kendi" sebebi kalktı (B-11); KARIŞTIRILIYOR'a `T_HATIRA` üst süresi: dolunca `gecmis` boşaltılır, bağ KÖTÜ'den yeniden ölçülür | KK-03 kural 9 · KK-01 kural 10 |
| B-4 | Aynı olayda sıra: önce karıştırma kanıtı, sonra veri tetiği, sonra ETX eşikleri; `k` sıfır varsa KÖTÜ denetimi onlar hariç; tablo kurallarla eşlendi; sebep küme, hepsi kalkınca bitti | KK-01 kural 9, 15 · KK-03 kural 9 |
| B-5 | Dondurmadan çıkıştan sonraki ilk selamda boşluk için 0 eklenmez, sıfırlama yok, `beklenen ← sıra + 1` | KK-01 kural 2, 13 |
| B-6 | `aralik` = bir sonraki planlı selama kadarki üst sınır (katlamadan sonraki `I`'nın 1,1 katı) | KK-02 alan tablosu, kural 2 · KK-01 kural 3 |
| B-7 | `s`'nin algoritması (tanıdık komşu, 4 s, gelen + ham zaman aşımı); payda 0 → işaret yok; eşiğin kâhin sayımla ve 4 s Hello'yla ölçüldüğü yazıldı | KK-03 kural 1–3 · KK-00 `KAYIP_ESIGI` |
| B-8 | İstek yalnız en az bir OLAĞAN komşunun sonlu ama uygulanamaz ilanı varsa; öteki bütün durumlar açıkça istek yok | KK-04 kural 8 |
| B-9 | Uygulanabilirlik her seçimde güncel FD ile hesaplanır, saklanmaz | KK-04 kural 1 |
| B-12 | `VERI_EN_AZ` = 4 çerçeve | KK-01 kural 6 · KK-00 |
| B-13 | Mekanizma → kâğıt/kural → bayrak → sınıf → kapalıyken tablosu; kapının "hepsi kapalı" yapılandırması; `uyarlanir_aralik` kapalıyken ara ilan sürer; `alici_bildirimi` kapalıyken alan kalır, bit 0 | KK-00 · KK-02 |
| B-14 | A/B ölçütü sınıfa göre (karıştırmaya karşı · genel); yer karıştırıcılı aile beklentide eklenir ya da gerekçesiyle çıkarılır | KK-00 · KK-01, KK-02, KK-04 "Sınanması" |
| B-15 | `I_MIN · I_MAX` dayanağı (5–7 s; yalnız `d_r ≥ 0,8` için < 10 s); `ISTEK_YINELEME` (sayı Babel'in, aralık bu tasarımın); `ISTEK_ATLAMA` = 64 (RFC 8966 §3.8.2.1); `T_HATIRA`'nın çekincesi | KK-00 |
| B-16 | Ardılsız ya da ardılı isteyen olan düğüm isteği iletmez; RFC'den farkı "bu tasarımın basitleştirmesi" diye yazıldı | KK-04 kural 9 |
| B-17 | Yok sayma sayacının başlangıcı, yenilenmemesi, erken bitişi, süre dolunca uygulanan ilan ve `Uyandirma` | KK-04 kural 7 |
| B-18 | Birimler ve nicemleme; `sira` ve tur başlangıcı, modüler karşılaştırma; eşit maliyet sırası; `c̄` tanımı; "işaretsiz saniye"; kaynak değişimi; `k`'nın sınırı; silme süresinin duraklaması; kendi karıştırılmamdan çıkınca istek; "2 ardışık" varış sırasıyla; KK-01 kural numaraları | KK-00 genel kural 3 · KK-01 · KK-03 · KK-04 |
| B-19 | Niyet döndüremeyen kancalarda değişim bir sonraki niyetli kancada uygulanır; `ilk_bekletme` yaş sınırı | KK-00 genel kural 1 · KK-05 kural 3, 4, 6 |
| B-20 | T-18'in sınır türü (atlama başına; sayı sınırı ve başlık alanı alınmadı, gerekçesiyle); KÖTÜ'ye girişte olay sayısı uygulanmaz (T-11'in kalanı); `17` §7 madde 8–9 tanı kaydında | KK-05 kural 5 · KK-01 kural 12 · KK-00 tanı kaydı |

## Sorunlar bölümünden

| sorun | yer |
|---|---|
| S-1 veri tetiğinin ikizdeki yanlış alarmı | KK-00 tanı kaydı · KK-01 "Sınanması" |
| S-2 tur isteğinin gidiş-dönüşü | KK-00 tanı kaydı · KK-05 "Sınanması" |
| S-3 sessiz evre bedeli | KK-00 tanı kaydı |
| S-4 girişim bitinin gidip gelmesi | KK-00 tanı kaydı · KK-03 "Sınanması" |
| S-5 ağın çapı | KK-00 `ISTEK_ATLAMA` ve tanı kaydı |
| S-6 eşiklerin Babel trafiğinden gelmesi | KK-00 `KAYIP_ESIGI` · KK-03 kural 2 |
| S-7 hatıranın aşınması | değişiklik yok (bilinen sınır) |
| S-8 RFC §3.8.2.2'nin ikinci paragrafı | değişiklik yok (olası iyileştirme; T-13 kararlaştırmamış) |

## İkinci okuma (17 Kasım)

Aynı denetçi düzeltmeleri yeniden okudu: `DENETIM-RAPORU-KURAL-2026-11-17-ikinci.md` (denetlenen hâl `94c0ed6` + commit'lenmemiş düzeltmeler, `git diff 94c0ed6 | md5sum` = `1269e7c9046c33859368d7cd1d6a5e6f`). **Hüküm: kodlamaya geçmeye engel yok.** B-1 ve B-3 tam kapandı; B-2 karıştırıcıya çok yakın alıcıda tam, girişim alıcısında değere bağlı; B-13 kısmen.

Kodlamayla birlikte kapatılacak açık bulgular (ayrıntı ikinci raporun §2'sinde):

| bulgu | konu | ne zaman |
|---|---|---|
| Y-3 | ED'de girişim işareti de çıktığı için kaynak girişime dönüyor; ED işaretinin görüldüğü saniyede kaynak ED kalmalı | KK-03 kodlanırken |
| Y-2 | ASKIDA iken kendi "karıştırılıyorum" durumum başlarsa bağ girişteki ölçüyle OLAĞAN'a dönmeli, ceza sayılmamalı | KK-01 kodlanırken |
| Y-1 | `ASKIDA_SURE`'nin bit kanıtının gecikmesini kapsayan alt sınırı (~6,6 s); KÖTÜ'de gelen geç kanıt cezayı kaldırmalı | `veri_kotu_tetigi` ve `karistirma_durumu` A/B'lerinin beklentisinden önce |
| Y-4 | ASKIDA'nın beklemesi karıştırmaya karşı sınıfta olmalı; `karistirma_durumu` kapalıyken `ASKIDA_SURE = 0` (kapının yönü tutucu kalsın) | mekanizma kapısının beklentisinden önce |
| Y-5 | `uyarlanir_aralik` kapalıyken ara ilan `I`'yı değiştirmemeli | `uyarlanir_aralik` A/B'sinden önce |
| Y-6 | kendi "karıştırılıyorum" durumuma üst süre (küçük bir karar) | uzun açık dönemli herhangi bir hücreden önce |
| Y-7 … Y-12 | hatıranın kaynağı · KÖTÜ → OLAĞAN'da bit ve ∞'un tur alanı · dayanak sayıları · `kacan`'da geri alma · istek kaydının tazelenmesi ve `ISTEK_ANIMSA` · `d_r`'nin listeye girişi | kodla birlikte |
| Z-1 … Z-4 | ASKIDA'nın yanlış alarm bedeli · yeni turun yayılma penceresi · B-11'in kanal bedeli · kenar bağlarda ASKIDA tavanı | tanı kaydında izlenir |
