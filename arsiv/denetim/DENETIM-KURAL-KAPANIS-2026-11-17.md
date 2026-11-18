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

## Kodlamada kapananlar (18 Kasım)

Bağın durumu (`KK-01`) ve selam (`KK-02`) kodlandı: `protokoller/desparete5_bicim.py` · `desparete5_bag.py` · `desparete5_selam.py`; testler `tests2/test_desparete5_bag.py` · `test_desparete5_selam.py` (46 test). Kâğıtlar kodla birlikte düzeltildi.

| bulgu | yapılan | yer |
|---|---|---|
| Y-2 | Kendi durumum başlarken ASKIDA'daki bağ girişteki ölçüyle OLAĞAN'a döner, veri penceresi boşalır, ceza sayılmaz | KK-01 kural 13 |
| Y-4 | `karistirma_durumu` kapalıyken ASKIDA beklemesi yok: veri tetiği doğrudan KÖTÜ'ye ve cezaya; ASKIDA'nın beklemesi karıştırmaya karşı sınıfta. İlk ölçümün çekirdeğinde bu bayrak kapalı olduğu için kapının beklentisinden önce kapatıldı | KK-01 kural 7 · KK-00 |
| Y-5 | `uyarlanir_aralik` kapalıyken ara ilan `I`'yı değiştirmez | KK-02 kural 3 |
| Y-6 | Kararım (18 Kasım): kendi dondurmamın üst süresi 30 s (`T_HATIRA` ile aynı); süre dolunca bağlar yeniden ölçülür, MAC yeniden kanıttır; bit ve gönderemezken selam kurulmaması durum sürdükçe sürer | `17` T-9 · KK-01 kural 13 · KK-03 kural 8 · KK-00 |
| Y-7 | Hatıra: ASKIDA'dan geliniyorsa girişteki ölçü, değilse bugünkü; sondaki 0'lar atılır, o anki `d_f` | KK-01 kural 9 |
| Y-8 | KÖTÜ'den çıkaran selamın biti 1 ise doğrudan KARIŞTIRILIYOR (∞ ilanın tur alanı rota kâğıdıyla kodlanırken) | KK-01 kural 12 |
| Y-9 | Dayanak sayıları ilan edilen 2,2 s'lik aralıkla düzeltildi | KK-00 |
| Y-10 | `s` dondurulmayan gölge geçmişten: zaman aşımı, sıra boşluğu ve geri alma dâhil | KK-03 kural 2 |
| Y-11 | `ISTEK_ANIMSA` 4 s, yinelemede tazelenir (kuralı rota kâğıdıyla kodlanırken) | KK-00 |
| Y-12 | Listeye en az 4 örnekten sonra girilir; listede olmamak "bilinmiyor" (`d_f` değişmez), 30 s bildirilmezse tanımsız | KK-01 "Gördüğü" · KK-02 alan tablosu, kural 6 |

Kodlamada bulunan boşluklar:

| | yapılan | yer |
|---|---|---|
| G-3 | Sondaki k sıfırın KÖTÜ'ye yol açmaması kuralların sırasından gelir; `karistirma_durumu` kapalıyken istisna yok, sessiz komşu ETX'ten KÖTÜ olur | KK-01 kural 15 |
| G-4 | Geri alma, kaynağındaki gibi fazla sayılan bütün kayıtları geri alır (yalnız sonuncuyu değil) | KK-01 kural 2 |
| G-5 | Selam uyandırma anında kurulur, titreşim uyandırmaya eklenir | KK-02 kural 1 |

Açık kalanlar: Y-3 (karıştırma kanıtının kendi durumu kodlanırken) · Y-1 (karıştırma A/B'lerinin beklentisinden önce) · Y-8'in ikinci yarısı ve Y-11'in kuralı (rota kodlanırken). Tanıda izlenecek bir sorun: olaydan sonra ilan edilen aralık 0,55 s iken iki selam art arda kaybolursa zaman aşımı üç sıfır sayar ve sessizlik kanıtı erken çıkar (yanlış alarm, iki temiz selamla geri döner).

### Rota, bekletme ve geri iz (18 Kasım)

`KK-04` ve `KK-05` kodlandı: `protokoller/desparete5_rota.py` · `desparete5_bekletme.py`; testler `tests2/test_desparete5_rota.py` (14 test; geçit ← X ← Y zincirinde açlık isteğinin geçide gidişi, turun yalnız geçitte bir artması ve yanıtın istek yolundan geri yayılması dâhil).

| | yapılan | yer |
|---|---|---|
| Y-8 (ikinci yarı) | ∞ ilanın tur alanı FD'nin turu, FD yoksa 0 | KK-04 kural 6 |
| Y-11 (kural) | İletilen isteğin kaydı aynı tur için gelen her istekte tazelenir; kayıt isteyeni tutmaz (yanıt çok-yayın) | KK-04 kural 9 |
| G-1 | Geri iz yalnız daha yeni `kaynak_sira`yla güncellenir (v0.4.1'in V11 kuralı): çapraz giden iki paket komutu döngüye sokamaz | KK-05 kural 6 |
| ayrıntı | Yok saymada tek alıcılı istek yalnız ilk yok saymada, istenen `FD.tur + 1`; açlık isteği hemen ve 3 kez daha 0,5 s arayla; iletim kalan atlama ≥ 2 iken bir eksiltilerek | KK-04 kural 7–9 · KK-00 |

Kâğıt dışından: mimari denetiminin D13 bulgusu (teşhis (d) aletinin 16 sabitinin kökeni yazılmamıştı) köken defterine yazılarak kapandı; denetim ihlalsiz ve bulgusuz.

Açık kalanlar: Y-3 (kendi durumum kodlanırken) · Y-1 (karıştırma A/B'lerinin beklentisinden önce).

### Kendi durumum, ana sınıf, bağlama (18 Kasım)

Kendi "karıştırılıyorum" durumum (`KK-03` A) ve bütün parçaları simülatörün kancalarına bağlayan ana sınıf kodlandı: `protokoller/desparete5_kanit.py` · `desparete5.py`; ölçüm aletlerinde `desparete5` ve `desparete5_cekirdek` adlarıyla (`kalibrasyon/aodv_uygunluk.py`). Testler `tests2/test_desparete5_kanit.py` (7) · `test_desparete5.py` (6; küçük test dünyasında uçtan uca: defter kapanır, rotalar kurulur, karıştırma yolları işler, çekirdek profilde karıştırmaya karşı mekanizmalar çalışmaz, koşu belirlenimli, yasak gözlem alanı okunmaz).

| | yapılan | yer |
|---|---|---|
| Y-3 | ED işareti görülen saniyede kaynak ED kalır; girişime yalnız ED'siz bir saniyede geçilir, o an selam hemen gider | KK-03 kural 4 · KK-02 kural 5 |
| G-2 | Ölçüm beyanları (kopma, rota kuruldu, rota geçersiz) Babel ve öteki protokollerle aynı anlamda | KK-00 genel kural 4 |
| ayrıntı | Gönderemezken değişim olayları selam planlamaz (boş uyanma döngüsü olmasın); kancaların sırası | KK-02 kural 5 · KK-00 genel kural 5 |

Bütün açık bulgulardan yalnız Y-1 kaldı (karıştırma A/B'lerinin beklentisinden önce). Küçük test dünyasında görülen ve ölçümde izlenecek iki şey (karar girdisi değil): karıştırıcısız koşuda da birkaç sessizlik kanıtı çıktı (yanlış alarm); sürekli karıştırmada tur birkaç kez arttı (`17` §7 madde 10).
