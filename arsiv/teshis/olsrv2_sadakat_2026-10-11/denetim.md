# OLSRv2 — RFC 7181 · 6130 · 5444 · 7779'a kural kural sadakat denetimi (K-235)

> 11 Ekim 2026 · K-208'in kalıbıyla (AODV) · kaynaklar `protokol_kaynaklari/` (ham metin) · hakem olsrd2 (`uygulama_kaynaklari/olsrd2/`, commit `477e716`), yalnız RFC'nin seçeneğe bıraktığı ya da kendi içinde çeliştiği yerde · kod `protokoller/olsrv2.py` · `olsrv2_bicim.py` (beyan tablosu) · `olsrv2_rfc5444.py` (tel biçimi) · tasarım `arsiv/teshis/olsrv2_2026-10-11/tasarim.md`. Karar kuralı: MUST ve SHOULD uygulanır, MAY beyan edilir (19 Eylül).

## 1 · RFC 5444 · 5497 · 7181 §6 — tel biçimi

| yer | kural | sözü | kod | hüküm |
|---|---|---|---|---|
| 5444 §5.1 | paket başlığı: sürüm 0, bayraklar, isteğe bağlı paket sıra numarası | MUST | `paket_kodla` · `paket_coz` | ✓ |
| 5444 §5.2 | mesaj başlığı: tür, bayraklar, adres boyu − 1, boy, isteğe bağlı kaynak · hop limit · hop count · sıra | MUST | `mesaj_kodla` · `_mesaj_oku` | ✓ |
| 5444 §5.3 | adres bloğu: baş · kuyruk · orta · önek | MUST | tek blok, kazandırıyorsa baş | ✓ |
| 5444 §5.4 | TLV: tür uzantısı · tek/çok indeks · değer · çok değerli | MUST | `_tlv` · `_adres_tlvleri` | ✓ RFC 6130 Ek B'nin iki örneği (45 · 29 bayt) bayt bayt |
| 5444 §5.5 | bozuk öğe → mesaj ya da paket sessizce atılır | MUST | `BicimHatasi` → paket atılır | ✓ |
| 5497 §5 | zaman kodu (1 + a/8)·2^b·C, C = 1/1024 s | MUST | `zaman_kodla` · `zaman_coz` | ✓ 6 s → 100 (RFC 6130 Ek B) |
| 7181 §6.2 | metrik kodu (257 + a)·2^b − 256, v'den küçük olmayan en küçük | MUST | `metrik_kodla` · `metrik_coz` | ✓ |

## 2 · RFC 6130 — NHDP

| yer | kural | sözü | kod | hüküm |
|---|---|---|---|---|
| §7 | süre `şimdi ≥ t` olunca dolmuş | MUST | `_durum` (`t > şimdi` geçerli) | ✓ |
| §7.1 | L_status: PENDING → LOST (L_lost) → SYMMETRIC → HEARD → LOST | MUST | `_durum`; bağ kalitesi yok, PENDING ve L_lost oluşmaz | ✓ |
| §10.1 · §11 | HELLO: VALIDITY_TIME (MUST), periyodikte INTERVAL_TIME (SHOULD); yerel adres LOCAL_IF THIS_IF; bekleyen olmayan her bağ LINK_STATUS'la; simetrik komşular; kayıp komşular OTHER_NEIGHB LOST; her bilgi her REFRESH_INTERVAL'da | MUST · SHOULD | `_hello_kur` (REFRESH = HELLO aralığı, her HELLO'da hepsi) | ✓ |
| §11.2.1 · RFC 5148 §5.1 | periyodik HELLO titreşimi: aralık U(0, HP_MAXJITTER) kısalır | SHOULD | `Uyandirma(2 − 0,5, jitter 0,5)` | ✓ |
| §12.1 | geçersiz HELLO: hop limit ≠ 1 · hop count ≠ 0 · VALIDITY_TIME ≠ 1 · INTERVAL_TIME > 1 · yerel adresim LOCAL_IF'te · LOCAL_IF ile LINK_STATUS/OTHER_NEIGHB aynı adreste | MUST | `_hello_gecerli` (bilinmeyen değerle reddetmek RFC 7188 §4.1 ile kaldırıldı) | ✓ |
| §12.3 | Neighbor Set (tek adres: kaldırılan/kayıp adres listesi boş) | MUST | `_hello_isle` | ✓ |
| §12.5 | Link Set: yeni demet (EXPIRED, L_time = şimdi + geçerlilik); benim adresim HEARD/SYMMETRIC → L_SYM_time; LOST → L_SYM dolar, HEARD ise L_time = şimdi + L_HOLD; L_HEARD = max(şimdi + geçerlilik, L_SYM); HEARD/SYMMETRIC'te L_time = max(L_time, L_HEARD + L_HOLD) | MUST | `_hello_isle` adım adım | ✓ |
| §12.6 | 2-Hop Set yalnız gönderenle bağ SYMMETRIC iken; SYMMETRIC ilan edilen eklenir, LOST/HEARD silinir; gönderen ve yerel adres hariç | MUST | `_hello_isle` | ✓ |
| §12 son paragraf | §13 sonuçları hemen | MUST | 2-Hop'tan önce `_bag_gecisleri` | ✓ |
| §13.1 | SYMMETRIC olunca N_symmetric; Lost Neighbor demeti silinir | MUST | `_bag_gecisleri` | ✓ |
| §13.2 | SYMMETRIC'ten düşünce ya da silinince 2-Hop demetleri silinir, N_symmetric false, Lost Neighbor (N_HOLD) | MUST | `_simetrik_degil` | ✓ |
| §13.3 | L_HEARD dolunca ya da bağ silinince komşu silinir | MUST | `_bag_gecisleri` | ✓ |
| §13 · §15.2 (7181) | değişime yanıt HELLO | MAY | yok | ○ beyan (olsrd2 de periyodik) |
| §14 | bağ kalitesi | MAY | yok, §15.4 değerleri | ○ beyan |
| §15 | değerler: HELLO 2 s · REFRESH 2 s · H_HOLD 6 s · L_HOLD 6 s · N_HOLD 6 s · HP_MAXJITTER 0,5 s | — | `olsrv2_bicim.py` | ✓ |

## 3 · RFC 7181 — OLSRv2

| yer | kural | sözü | kod | hüküm |
|---|---|---|---|---|
| §7 | kaynak adresi tek ve eşsiz; arayüz adresine eşit olabilir | MUST · MAY | düğüm adresi | ✓ |
| §8.1 · §15.3.2.1 | L_in_metric HEARD/SYMMETRIC olunca belirli; başka değer yoksa MAXIMUM_METRIC; SYMMETRIC bağda L_out_metric = komşunun benim adresime ilan ettiği gelen bağ metriği | MUST | `_hello_isle`; DAT her saniye günceller | ✓ |
| §13.2 | aynı anda gönderilen mesajlar bir pakette | SHOULD | her pakette tek mesaj; bağımsız titreşimli zamanlayıcılarda eş zamanlı mesaj yok | ✓ beyan |
| §13.3.1 | MPR_WILLING (bayrak üst dört bit, yönlendirme alt dört bit) · CONT_SEQ_NUM | MUST | `_ISTEK` · `_tc_kur` | ✓ |
| §13.3.2 | LINK_METRIC 16 bit: tür/yön bitleri + üs + mantis; eşit değerli bitler birleşebilir | MUST · MAY | `_metrik_degeri`; HELLO'da gelen ve giden aynı kodlanırsa tek değer | ✓ |
| §14.1 | kendi mesajı atılır; hop limit > 1 ve hop count < 255 ise iletme düşünülür | MUST | `_tc_al` | ✓ |
| §14.2 | işleme: simetrik olmayan göndericiden İSTEĞE BAĞLI; Processed Set | MUST · OPTIONAL | işlenir (olsrd2) | ✓ beyan |
| §14.3 | iletme: gönderen simetrik değilse at; Received Set; Forwarded Set; gönderen bayrak MPR seçicisiyse hop limit −1, hop count +1, ilet | MUST | `_tc_al` · `iletim_icin` (mesajın geri kalanı değişmez) | ✓ |
| §13.2 · RFC 5148 §5.3 | iletme titreşimi U(0, F_MAXJITTER) | SHOULD | `Uyandirma(20 µs, jitter 0,5)`; paket sıra numarası çıkışta | ✓ (20 µs simülatörün alt sınırı) |
| §15.1 | HELLO'ya kaynak adresi, MPR_WILLING, bağ/komşu metrikleri, MPR TLV'si | MUST | `_hello_kur` | ✓ |
| §15.3.1 | ek geçersizlik: MPR_WILLING > 1 · kaynak adresi bende · kaynak adresine LINK_STATUS/OTHER_NEIGHB · aynı tür/yönde iki metrik · SYMMETRIC olmayan adreste MPR | MUST | `_hello_gecerli` | ✓ |
| §15.3.2 | N_orig_addr · istekler · MPR seçicisi bayrakları · 2-Hop metrikleri | MUST | `_hello_isle` | ✓ |
| §15.3.2.3 · §17.3 m. 5 | yönlendirme MPR seçicisi → ilan; seçici olmayanı ilan etmek MAY | MUST · MAY | yalnız seçiciler (olsrd2) | ✓ beyan |
| §16.1 | TC: kaynak · sıra · hop limit 255 · CONT_SEQ_NUM COMPLETE · VALIDITY_TIME (T_HOLD) · ilan edilen her komşu ROUTABLE_ORIG + giden komşu metriği; INTERVAL_TIME MAY | MUST · MAY | `_tc_kur` (INTERVAL_TIME ve hop count olsrd2 gibi var) | ✓ |
| §16.2 | ilanı varsa TC_INTERVAL'da TC; ilan boşalınca A_HOLD_TIME boyunca boş TC; yanıt TC MAY; üretimde titreşim (RFC 5148 SHOULD) | MUST · MAY · SHOULD | `_tc_kur` · `Uyandirma(5 − 0,5, jitter 0,5)` | ✓ · yanıt TC yok (beyan) |
| §16.3.1 | geçersiz TC: kaynak ya da sıra yok · VALIDITY_TIME ≠ 1 · CONT_SEQ_NUM > 1 ya da adres varken yok · kaynak adresi bende · kaynak adresi NBR_ADDR_TYPE'ta | MUST | `_tc_al` · `_tc_isle` | ✓ |
| §16.3.3.1 | AR_seq_number > ANSN → at; değilse AR güncellenir | MUST | `_tc_isle` | ✓ testle |
| §16.3.3.2 | Router Topology: bilinmeyen metrik → sil, değilse ekle/güncelle | MUST | `_tc_isle` | ✓ |
| §16.3.3.3 | Routable Address Topology | MUST | Router Topology'nin aynı düğümleri (tek adres); rota hesabında o kenarlar §19.1 gereği zaten kullanılmaz | ✓ beyan |
| §16.3.4 | COMPLETE: eski ANSN'li demetler silinir | MUST | `_tc_isle` | ✓ testle |
| §17.2 | L_out_metric bilinmiyorsa SYMMETRIC değil; SYMMETRIC değilse L_mpr_selector false | MUST | `_bag_gecisleri` | ✓ |
| §17.3 | N_in/out_metric simetrik bağların en küçüğü; N_symmetric false → MPR ve seçici bayrakları false | MUST | `_n_metrik` · `_simetrik_degil` | ✓ |
| §17.4 | ANSN: ilan değişince, ilan edilen silinince ya da N_out_metric değişince | MUST | `_guncelle` (ilan kümesi ve metrikleri karşılaştırılır) | ✓ |
| §17.5 | AR dolunca kaynağın topoloji demetleri silinir | MUST | `_temizle` | ✓ |
| §17.6 · §18.6 | MPR'ler koşullar değişince yeniden; her zaman yeniden hesap MAY | MUST · MAY | her değişimde yeniden | ✓ |
| §18.3 | MPR kümesi: WILL_ALWAYS içinde; her 2-atlama kapsanır, en kısa uzaklık korunur | MUST | `mpr_sec` | ✓ 40 rastgele grafikte testle |
| §18.4 | bayrak MPR'leri arayüz başına, A (metrikli) ya da B | MUST · seçim | A (olsrd2) | ✓ beyan |
| §18.5 | yönlendirme MPR'leri gelen komşu metriğiyle | MUST | d2 için N2_in_metric — metindeki "N2_out_metric" aynı paragrafın izin koşuluyla ve §4.6'yla çelişiyor; olsrd2 gelen | ✓ beyan |
| §18.1 · Ek B | istek SHOULD dikkate alınır; Ek B: WILL_ALWAYS → tek kapsayan → W, R, D; adım 4 İSTEĞE BAĞLI | SHOULD · MAY | W → R → D → küçük adres; adım 4 yok | ✓ |
| §19 · Ek C | omurga üzerinde en küçük toplam metrik; eşit metrikte az atlama (SHOULD); Ek C.1 tercihi | MUST · SHOULD | `_rota_hesapla` (Dijkstra) | ✓ |
| §19.1 · Ek C.7 | 2-atlama kenarları İSTEĞE BAĞLI; başka yolu olana tercih edilmez; Z omurga düğümüyse kullanılmaz | OPTIONAL · MUST | var; metrik N2_out_metric (Ek C.7'nin "N_out_metric"i §19.1'le çelişiyor; olsrd2 N2) | ✓ beyan |
| §20 | TC 5 s · T_HOLD 15 s · A_HOLD 15 s · RX/P/F_HOLD 30 s · TC_HOP_LIMIT 255 · istekler 7 | — | `olsrv2_bicim.py` | ✓ (olsrd2'nin kendi varsayılanları — 300 s geçerlilik — alınmadı) |
| §21 | 16 bit sarmalı sıra karşılaştırması | MUST | `_sira_buyuk` | ✓ |

## 4 · RFC 7779 — DAT

| yer | kural | sözü | kod | hüküm |
|---|---|---|---|---|
| §8.1 | yeni bağda kuyruklar sıfır, zamanlar tanımsız | MUST | `_Bag` | ✓ |
| §9.2 | HELLO'da INTERVAL_TIME · her pakette arayüz sıra numarası | SHOULD | `_hello_kur` · `_paket` | ✓ |
| §9.3 | her paketten sonra alınan/toplam (sıra farkı, 256'dan büyükse 1), paket zamanı, kayıp aralık sıfırlanır | SHOULD | `_dat_paket` | ✓ |
| §9.4 | HELLO'dan sonra hello aralığı (INTERVAL_TIME, yoksa VALIDITY_TIME) | MUST | `_dat_hello` | ✓ |
| §10.1 · §10.2 | paket zaman aşımı; her saniye metrik: (2^24/8)·min(toplam/alınan, 8)/(hız/1000), kayıp aralıklarla ölçek, alınan < 1 → MAXIMUM_METRIC; kuyruk kaydı | MUST | `_dat_yenile` (zaman aşımları yenilemeden önce toplu işlenir; yalnız metrikte kullanıldıkları için eşdeğer) | ✓ formül testle |
| §8 | gelen hız dış süreçten; sabit yapılandırma izinli | — | sabit 1 Mbit/s | ✓ beyan |

## 5 · Uygulanmayanlar (beyan)

RFC 7183 bütünlük koruması (tehdit modelinde mesaj sahteciliği yok; öteki rakipler de imzasız; olsrd2'de ayrı eklenti) · RFC 7187 yönlendirme MPR iyileştirmesi (MAY) · RFC 7466 (bağ kalitesiyle birlikte seçenek) · değişime yanıt HELLO/TC (MAY) · bağ kalitesi (MAY) · bağ katmanı bildirimi (RFC'de yok).

## 6 · Sonuç

Gerekçesiz sapma yok. RFC metninin kendi içindeki iki tutarsızlık (§18.5'in d2'si, Ek C.7'nin metriği) normatif bağlamla ve hakemle çözüldü, beyan tablosunda. Doğrulama `tests2/test_olsrv2.py` 49/49: tel biçimi bayt bayt, zaman ve metrik kodları, gidiş-dönüş ve iletmede yalnız hop alanlarının değişmesi, 40 rastgele grafikte MPR özellikleri, DAT formülü, iki düğümde HELLO'yla simetrik bağ kurulumu ve 6 s'de düşmesi, TC'nin ANSN sırası, küçük ağda uçtan uca korunum ve tam rota. Kod hâli **`OLSRv2-a`**.
