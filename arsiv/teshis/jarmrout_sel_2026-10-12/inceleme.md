# JarmRout'un RREQ seli — inceleme (12 Ekim 2026)

> Tetik: Faz 4b kapanış ölçümlerinde (`arsiv/teshis/faz4b_kapanis_2026-10-11/`) JarmRout'un U1 koşuları 8–11 saat sürdü ve karıştırıcısız dünyada kâhinin çok altında kaldı (yere toplamada 12 hücrenin 11'i eşik altında, oran 0,30–0,55). Kuyruk yürütücünün kararıyla durduruldu. Yürütücünün sorusu: bir şeyi kaçırıyor muyuz, sorun gerçekten protokolde mi, simülatörde mi?
>
> Bütün koşular teşhistir: protokolün ve simülatörün kodu değişmedi; varyantlar teşhis betiği içinde yamalıdır. Betikler ve çıktılar bu klasörde; ağ referans dünya, `statik-yok`, tohum 1000 (U1'de oranı 0,547 olan hücre), 100 s.

## 1 · Makalenin sözde kodu (Şekil 4) — kaçırılan kural yok

Kaynak: IEEE Xplore şekil galerisi, `pu4-2879758-large.gif` (belge 8523684). Ara düğümde yinelenen RREQ:

    else /* Receive duplicated RREQ. */
        if RREQ.C_hop > cache_hop_i[pkt_seq]
            Discard RREQ packet;
        else
            Calculate L_qt and T_ld ...; Append n_i; Add coord_i; Increase C_hop; Rebroadcast RREQ packet;

`cache_hop` yalnız ilk alışta yazılır. Gerçekleme (`protokoller/jarmrout.py` `_rreq_isle`) birebir aynı. Sözde kodda kaynakta yeniden deneme yok (bizdeki RFC 4728 dolgusu); başka bir sel bastırma kuralı da yok. Hedefin, `t_wait`'in, RREP'in ve RERR'in davranışı da gerçeklemeyle aynı.

## 2 · Selin büyüklüğü (`sel.py`, yere toplama)

| ölçü | değer |
|---|---|
| keşif çifti · 100 s'de keşif | 43 · 906 (çift başına ~21) |
| keşif başına RREQ üretimi | 2,3 (keşiflerin %66'sı ikinci denemeye düştü) |
| ilk RREP'in dönüşü | medyan 0,77 s (RFC 4728 RequestPeriod 0,5 s) |
| RREQ başına yeniden yayın | ort. 78, en çok 836 (40 düğüm) |
| kopan yol · RERR | 1 184 · 1 425 (karıştırıcı yok, durağan) |
| kontrol yayın süresi | 100 s'de 218 s (düğümler toplamı) |

Hata izi yok (`rotasiz_paket` 0, keşif tükenmesi 0). Geri besleme döngüsü:
1. Yinelenen RREQ'ların yeniden yayını seli büyütür.
2. Kanal dolar, veri çerçeveleri MAC'te düşer.
3. Yollar kopar, RERR gider ve yeniden keşif başlar.
4. RREP gecikir, kaynak yeniden dener.

## 3 · Hangi halka ne kadar (`varyant.py`)

| varyant | PDR | RREQ yeniden yayını | kontrol yayın süresi |
|---|---|---|---|
| makale harfiyen | 0,599 | 143 834 | 218 s |
| önbellekte en küçük hop (metnin öteki okuması) | 0,703 | 105 817 | 160 s |
| yeniden deneme 1 s (dolgu) | 0,688 | 110 493 | 167 s |
| yinelenen RREQ yayılmaz (DSR; makaleye aykırı) | 0,914 | 14 684 | 28 s |

Selin ~%90'ı makalenin yinelenen RREQ kuralından gelir. Metnin öteki okuması da dolgu da yalnız ~%25 azaltır, çöküşü kaldırmaz.

## 4 · Simülatörden bağımsız sayım (`ideal_sel.py`)

Aynı ağın bağ olasılıkları (kâhinin kanal grafiği), çarpışma ve MAC çekişmesi yok, her İHA'dan geçide RREQ:

| kural | RREQ başına yeniden yayın (ort · en çok) |
|---|---|
| makale harfiyen | 508 · 8 849 |
| önbellekte en küçük hop | 140 · 296 |
| DSR | 38 · 38 |

Kuralın kendi büyütmesi ideal kanalda DSR'nin ~13 katı. Simülatörde aynı kural 70–78 verir: gerçek MAC'teki çarpışmalar kopyaların çoğunu yutar. **Simülatör seli büyütmez, bastırır.** Ağda geçide ortalama uzaklık 2,33 atlama, ortalama derece 8 — makalenin ağıyla (ortalama 2,4 atlama, Şekil 5) aynı derinlik.

## 5 · Eşik: eşzamanlı akış sayısı (`akis.py`, eşler arası)

| akış | PDR | üretilen RREQ | RERR | kontrol yayın süresi |
|---|---|---|---|---|
| 1 | 1,000 | 1 | 1 | 0 s |
| 5 | 0,996 | 14 | 12 | 3 s |
| 10 | 0,995 | 35 | 21 | 7 s |
| 20 | 0,653 | 1 829 | 2 396 | 190 s |

Simülatörümüzde, makalenin rejiminde (tek kaynak, az akış) JarmRout kusursuz çalışır. 10 ile 20 eşzamanlı akış arasında kendini besleyen çöküşe geçer. Yere toplamanın 43 keşif çifti bu eşiğin hep üstündedir.

## 6 · Sonuç

- **Kaçırılan bir şey yok:** gerçekleme makalenin metniyle ve sözde koduyla birebir.
- **Sorun simülatörde değil:** az akışta PDR ≈ 1,00; tekilleştiren varyant çok akışta 0,91; bağımsız ideal sayım kuralın büyütmesini simülatörden daha büyük verir; AODV ve OLSRv2 aynı dünyada çalışır.
- **Sorun protokolün kuralında:** yinelenen RREQ'ların yeniden yayını keşif seli başına 3–13 kat büyütme getirir. Az keşifte zararsızdır; çok sayıda eşzamanlı akışta tıkanıklık, kopan yol ve yeniden keşif döngüsüyle çöker.
- **Makale bu rejimi sınamamış:** tek CBR kaynağı ("The source node generates CBR"), ortalama 2,4 atlama. Makalenin kontrol yükü ölçüsü ("the number of forwarded and received control packets to build routing path") kurulan yolların paketlerini sayar; selin büyüklüğünü göstermez.
