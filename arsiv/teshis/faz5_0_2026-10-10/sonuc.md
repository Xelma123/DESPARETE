# Faz 5.0 · Birincil hücrede kayıp anatomisi — sonuç

> 10 Ekim 2026 · ölçüt `beklenti.md` (commit `075ce8a`, koşudan önce) · koşu 17:33–22:04 (4 sa 31 dk), `kopya/` = `075ce8a` (138 dosya birebir, `kopya_ozet.txt`) · ham çıktı `anatomi.txt`, kayıt `kayit.json` · karar kuralının uygulanması `sonuc_hesap.py` → `sonuc_hesap.txt`.

## 0 · Geçerlilik ✓

Korunum 20/20 geçerli · doğum evresi çelişkisi 0 · atfsız düşüş yok · aletin açık evre PDR'si satırın `pdr_acik`ıyla 20/20 birebir · 1003 ve 1004'te `PDR_açık` G2ç'nin değerleriyle 10/10 birebir (altı basamak): alet eki davranışı değiştirmedi.

## 1 · `PDR_açık` (1003–1006)

| kol | 1003 | 1004 | 1005 | 1006 | ortalama | DESPARETE − kol |
|---|---|---|---|---|---|---|
| kâhin | 0,734 | 0,827 | 0,737 | 0,821 | 0,780 | −0,259 · −0,289 · −0,230 · −0,137 |
| DESPARETE | 0,476 | 0,538 | 0,507 | 0,684 | 0,551 | |
| AODV | 0,401 | 0,536 | 0,357 | 0,481 | 0,444 | +0,075 · +0,002 · +0,150 · +0,203 |
| AOMDV | 0,348 | 0,521 | 0,356 | 0,493 | 0,429 | +0,128 · +0,017 · +0,150 · +0,190 |
| OLSR | 0,258 | 0,193 | 0,100 | 0,367 | 0,230 | +0,217 · +0,345 · +0,406 · +0,317 |

## 2 · Karıştırmaya özgü kayıp — doğum evresine göre açık − önce, havuzlanmış

| kol | ΔPDR | R · rota yok | İ · iletim | K · erişim | T · döngü |
|---|---|---|---|---|---|
| kâhin | −0,134 | +0,006 | +0,127 | 0 | 0 |
| DESPARETE | −0,204 | +0,171 | +0,033 | 0 | 0 |
| AODV | −0,138 | +0,103 | +0,035 | 0 | 0 |
| AOMDV | −0,166 | +0,135 | +0,031 | 0 | 0 |
| OLSR | −0,274 | +0,238 | +0,033 | +0,001 | +0,001 |

Kalan (koşu sonunda yolda) her kolda 0. Yöntemin denetimi: aynı koşudaki açık − önce ile hesaplanan fazladan kayıp, 1003 · 1004'te ikizle hesaplanan fark-içinde-farkla aynı mertebede — kâhine göre 0,093 · 0,128 (ikizle 0,113 · 0,120), AODV'ye göre 0,059 · 0,122 (ikizle 0,080 · 0,086).

## 3 · Karar kuralı

1. `E` (DESPARETE − kâhin) = **0,071** ≥ 0,05 → kural sürer. Tohum başına 0,093 · 0,128 · 0,028 · 0,033 (dördü pozitif); AODV'ye göre 0,066, tohum başına 0,059 · 0,122 · 0,088 · −0,006.
2. T 0 · DESPARETE'nin hop sınırı sayacı 4/4 tohumda 0 → döngü yok.
3. Grup payları: kâhine göre R +0,165 (pay **%100**) · İ −0,095 · K 0 · T 0; AODV'ye göre R +0,068 (%100) · İ −0,003. → **R baskın: ilk hedef, ardılı karıştırılan alanın hızlı geçişi.**
   Alt ayrım (açık evrede `rota_gecersiz` anında alan): REPAIRING, yani tampon kotası dolu, **%52** · UNREACHABLE %48 → kural kota dalını seçer; eşiğin hemen üstünde, iki dal neredeyse eşit. Ulaşılamaz yarıda onarım bölümlerinin girişi çoğunlukla açlık (açık evre 3 618 / 5 626 = %64) → tur isteği. Öncelik önerisi (5.1 → 5.4 → 5.3) yürütücünün kararına sunulur.
4. Yön gösterici hedef: `E`'nin kaçınılabilir kısmı tamamı (K = 0, fizik sınırı yok) → yarısı ≈ **+0,035** karıştırmaya özgü `PDR_açık` ve AODV'ye göre fark-içinde-fark > 0.

## 4 · Öngörüler

| öngörü | ölçülen | |
|---|---|---|
| `E` ≈ 0,11 ± 0,03 | 0,071 (1005 · 1006 küçük: 0,028 · 0,033) | ✗ |
| R baskın, pay %50–75 | R baskın, pay %100 | yön ✓ · aralık ✗ |
| İ ikinci, %20–40 | İ negatif (−0,095): DESPARETE'nin karıştırmaya özgü iletim başarısızlığı kâhinden az | ✗ |
| K küçük · T ≈ 0 | 0 · 0 | ✓ |
| DESPARETE'nin açık evre kararlarında girişim/ed alanı payı AODV'ninkinden yüksek | %12,4 ↔ %13,2 (kâhin %11,6) | ✗ |
| AODV'nin fazladan kaybı (kâhine göre) küçük ve çoğunlukla İ | +0,004 küçük ✓ · bileşimi R (+0,097) ve İ (−0,092) | yarı |

## 5 · Kuraldan sonra görülenler (karar girdisi değil)

- **R kaybı karıştırıcının alanında değil.** DESPARETE'nin açık evrede doğan paketlerinde `rota_gecersiz` etki alanına göre ed 0,002 · girişim 0,032 · **uzak 0,191** (önce 0,001 · 0,014 · 0,042). Paket, yolu karıştırılan bağdan geçen uzak rölelerde ölüyor: karıştırma bir ardılı koparınca alanın onarımı geçide giden yol boyunca yayılıyor. AODV'de aynı desen (uzak 0,293 ↔ önce 0,177). Karıştırma kanıtı (5.1) yalnız yerel kalırsa bu kaybı tek başına kapatamaz; kayıp onarım dinamiğinde.
- **Kâhin "rota yok" yaşamaz;** karıştırma kaybının tamamı iletim başarısızlığı (ed alanında 0,036, önce 0,002). DESPARETE'nin kâhine göre R fazlasının bir kısmı aynı kaybın başka adla yazılmasıdır (kâhin dener ve başarısız olur, protokol denemeden düşürür); net fark `E`.
- Sessiz evrede de `rota_gecersiz`in %73'ü kota dolu: kota kaybı karıştırmaya özgü değildir.
- DESPARETE'nin karıştırmaya özgü kaybı tohumlar arasında oynak (1006'da AODV'den az). `E` 4 tohumda pozitif, ama büyüklüğü 0,03–0,13 arasında; mekanizma A/B'leri 8 tohumla (1003–1010) koşulmalı.
