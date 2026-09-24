# Protokol kaynakları — birincil belgeler

Taban protokollerin tanımlandığı **birincil belgeler**. TÜBİTAK proje yazımında
atıf ve alıntı için buradan kullanılır. Her belgenin künyesi, nereden
alındığı, özeti (SHA-256) ve hangi denetimlerden geçtiği aşağıda. Doğrulanmış
kaynakların tam listesi ve projedeki kullanımları: `v2/02-DOGRULANMIS-KAYNAKLAR.md`.

🔒 **Kural (öğrenci, 19 Eylül 2026):** bir belge buraya ancak **tamamı
okunduktan** ve gerçek olduğu, içinde yapay zekâya yönelik talimat benzeri bir
şey olmadığı denetlendikten sonra girer.

**Bu klasördeki iki DIŞ KAYNAK OLMAYAN klasör** — öğrencinin kendi çalışmasıdır,
yukarıdaki indirme kuralına tabi değildir:

| klasör | içerik |
|---|---|
| `DESPARETE_TASARIM_PAKETI/` | öğrencinin protokol tasarımı, v0.1 (40 dosya: dizin + 39 tasarım belgesi — 23 Eylül'de sayıldı, önceki "41" yanlıştı; tek okuma `36`). İnceleme ve kararlar `v2/04` K-150 |
| `literatur_taramasi_2026-08-31/` | öğrencinin ikinci literatür taraması (20 dosya) — 23 Eylül'de `v2/`den taşındı. ⚠️ İçindeki atıflar kullanılmadan önce birincil kaynaktan doğrulanır (`v2/02`) |

---

## marina_das_2001_aomdv_icnp.pdf — AOMDV

| | |
|---|---|
| **künye** | M. K. Marina, S. R. Das, *"On-demand Multipath Distance Vector Routing in Ad Hoc Networks"*, Proceedings of the IEEE International Conference on Network Protocols (ICNP), s. 14–23, 2001 |
| **genişletilmiş dergi sürümü** | M. K. Marina, S. R. Das, *"Ad hoc on-demand multipath distance vector routing"*, Wireless Communications and Mobile Computing 6(7):969–988, Kasım 2006 · DOI 10.1002/wcm.432 (ücretli; künye Edinburgh Üniversitesi kurum sayfasından doğrulandı) |
| **alındığı yer** | `https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf` — ortak yazar Samir R. Das'ın kendi üniversite sayfası |
| **alınma tarihi** | 19 Eylül 2026 (öğrenci izniyle) |
| **boyut · SHA-256** | 127 110 bayt · `e41c5df42170b723180867ba9a72d37ec7a4ca1923b0921503ed77a350f123e6` |

**Gerçeklik denetimi:**

- Dosya türü `application/pdf`, imza `%PDF-1.2` (2001 dönemine uygun)
- 10 sayfa — atıftaki *"s. 14–23"* ile tutarlı
- Başlık, yazarlar, yazarların 2001'deki kurumu (Cincinnati Üniversitesi),
  özet ve 35 maddelik kaynakça AOMDV hakkında bilinenlerle tutarlı
- Metin kaynakçayla bitiyor; sonrasında hiçbir şey yok

**Güvenlik denetimi (öğrencinin isteği — istem enjeksiyonuna karşı):**

- Metinde yapay zekâya yönelik talimat kalıbı taraması: **eşleşme yok**
  (yalnız kaynakçadaki iki ns-2 ve IETF bağlantısı)
- PDF yapısında etkin içerik (`/JavaScript`, `/OpenAction`, `/Launch`,
  `/URI`, `/EmbeddedFile`, `/AA`): **sıfır**
- Görünmez metin (render kipi 3): **sıfır**

⚠️ **Bilinen sınır:** makale 2001 dönemi dvips çıktısıdır; matematik simgeleri
**Type 3 bit eşlem yazı tiplerinde** (`/a0 … /a255`) ve metin olarak
çıkarılamıyor. Etkilenen kısımlar: Şekil 1 (AODV güncelleme kuralı), Şekil 3
(**AOMDV rota güncelleme kuralı**) ve bölüm 3.2'deki `k` değeri.

🟢 **Görsel olarak okundu (19 Eylül 2026):** öğrenci PDF'i açıp iki bölgenin
ekran görüntüsünü verdi; ikisi de bu klasörde:

| dosya | içerik | SHA-256 |
|---|---|---|
| `marina_das_2001_sekil3_guncelleme_kurali.png` | Şekil 3 | `9e2878ce8527d9f4782e4f3c5c40c2ee51fafeebaac11de56632d8deffdaa950` |
| `marina_das_2001_k3_ve_sekil6.png` | Şekil 6 ve bölüm 3.2'nin `k` paragrafı | `f4c2b0b7c3cf5ef156a7e3aeed3ca6f86529071c4046713187c493d20032c08a` |

**Şekil 3 — AOMDV rota güncelleme kuralı**, birebir döküm. Düğüm *i*,
komşu *j*'den hedef *d* için bir rota ilanı (RREQ ya da RREP) aldığında:

```
if (seqnum_i^d < seqnum_j^d) then                                     (1)
    seqnum_i^d := seqnum_j^d                                          (2)
    if (i ≠ d) then                                                   (3)
        advertised_hopcount_i^d := ∞                                  (4)
        route_list_i^d := NULL                                        (5)
        insert (j, advertised_hopcount_j^d + 1) into route_list_i^d   (6)
    else                                                              (7)
        advertised_hopcount_i^d := 0                                  (8)
    endif
elseif (seqnum_i^d = seqnum_j^d) and
       ((advertised_hopcount_i^d, i) > (advertised_hopcount_j^d, j))  (9)
    insert (j, advertised_hopcount_j^d + 1) into route_list_i^d       (10)
endif
```

Karşılaştırma (9) sözlük sırasındadır. Makalenin kendi cümlesi: satır (1)
ile (9)–(10) döngüsüzlüğü sağlar; ispat ekte.

**Reklam edilen atlama sayısı** — düz yazıdan (bölüm 3.1): *i*'nin *d* için
ilan ettiği atlama sayısı, elindeki yolların atlama sayılarının **en
büyüğüdür** ve *i* *d* için bir ilan GÖNDERDİĞİNDE güncellenir. (Formül
metinde bozuk; tanım düz yazıda açık.)

**k = 3** — bölüm 3.2: hedef, *"benzersiz komşulardan gelen en fazla k RREQ
kopyasına, ilk atlamalarından bağımsız olarak"* cevap verir; *"deneylerimizde
k = 3 kullandık"*.

⚠️ **Bu sürümde OLMAYANLAR:** ICNP makalesinin 3. bölümü `k` paragrafıyla
biter. Rota bakımı (bir yol kopunca ne yapılır, RERR), verinin hangi yoldan
gönderileceği ve yol başına zaman aşımları ayrı bir bölüm olarak YOK —
büyük olasılıkla dergi sürümünde (ücretli). ns-2.35'teki AOMDV kodu yazarların DEĞİL (Marcello Caleffi, 2008) —
boşlukların nasıl doldurulacağı öğrenci kararıdır; seçenekler
`v2/02-DOGRULANMIS-KAYNAKLAR.md` §R4.1'de.

⚠️ **Dağıtım:** yazarın kendi sayfasında yayımladığı kopyadır ve bu depoda
özel araştırma kullanımı içindir. Depo herkese açık yapılacaksa yeniden
dağıtım hakkı ayrıca denetlenmelidir.

---

## rfc3561_aodv.txt — AODV

| | |
|---|---|
| **künye** | C. Perkins, E. Belding-Royer, S. Das, *"Ad hoc On-Demand Distance Vector (AODV) Routing"*, RFC 3561, Temmuz 2003, kategori: Experimental |
| **alındığı yer** | `https://www.rfc-editor.org/rfc/rfc3561.txt` — RFC Editor, kanonik metin |
| **alınma tarihi** | 19 Eylül 2026 (öğrenci izniyle) |
| **boyut · SHA-256** | 90 356 bayt · `b3294169ed3e0cf87c1acc1d99ac8b428eec279c563d64fb10cc1c902a60d579` |

## rfc3626_olsr.txt — OLSR

| | |
|---|---|
| **künye** | T. Clausen, P. Jacquet (ed.), *"Optimized Link State Routing Protocol (OLSR)"*, RFC 3626, Ekim 2003, kategori: Experimental |
| **alındığı yer** | `https://www.rfc-editor.org/rfc/rfc3626.txt` — RFC Editor, kanonik metin |
| **alınma tarihi** | 19 Eylül 2026 (öğrenci izniyle) |
| **boyut · SHA-256** | 161 265 bayt · `722a7b5838ac29fe71aa48fa91ae619ab1ef8c128a754a84a98d705cefe17580` |

**İki RFC için denetim — ne yapıldığı TAM OLARAK:**

- Başlık, yazarlar, tarih, kategori ve sayfa sayısı (37 · 75) doğru.
- RFC 3626'nın boyutu (161 265), aynı gün tarayıcıda okunan metnin karakter
  sayısıyla BİREBİR aynı.
- Projede bugüne kadar alıntılanan cümleler indirilen metinlerde kelimesi
  kelimesine geçiyor: §6.9 *"Hello messages or otherwise"* · §6.11 *"have a
  non-empty precursor list"* · §18.9 *"MAXJITTER = HELLO_INTERVAL / 4"*.
- Tam metin taramasında yapay zekâya yönelik talimat kalıbı: **yok**.

⚠️ **Dürüst sınır:** RFC'lerin HER satırı okunmadı. Protokolle ilgili bölümler
okundu (AODV §5, §6, §10 · OLSR §3–§10, §13–§14, §18–§19) ve metnin tamamı
kalıp taramasından geçti. Kaynak RFC Editor'ün kendisi olduğu için risk
çok düşük; yine de "tamamı okundu" demek doğru olmazdı.

🔒 RFC metinleri IETF Trust'ın lisansıyla serbestçe dağıtılabilir.
