# Teşhis — regresyon k223'ün iki büyük farkı (ölçmeden önce)

> 9 Ekim 2026 · ajan · tetik: `regresyon_k223/beklenti.md`nin önceden yazılı kuralı ("bir referans satırında |ΔPDR| > 0,10 ise sebebi U1'den önce teşhis edilir"). Kısa pencerede, tek tohumda (1003): `u-birincil-desparete` 0,6928 → 0,5760 (−0,117) · `u-birincil-olsr` 0,3297 → 0,4699 (+0,140). DESPARETE'nin kodu değişmedi (yalnız deneme sayısı); OLSR'da iki değişiklik birlikte (§8.2.1 + deneme sayısı).
> `TESHIS_KOK=<kopya_a> py -3.11 -u arsiv/teshis/denetim_duzeltme_2026-10-09/teshis_birincil.py` — birincil hücre, regresyonun kısa penceresi ve kimlik etiketleri, tohum 1003–1010 (Faz 5 geliştirme tohumları), kollar: DESPARETE · AODV · `OLSR-d` × deneme sınırı {7 eski, 6 yeni} + `OLSR-c` (`olsr_c.py` = `git show c8b1b44:protokoller/olsr.py`, birebir) × 7. 56 koşu, 8 işçi, ~70 dk.

## T0 · Kimlik — beyan edilmemiş değişiklik kapısı (geçmezse kuyruk B başlamaz)

1003'te `pdr_pencere` ve düşme sebepleri, regresyon satırlarıyla BİREBİR:
- DESPARETE@7 · AODV@7 · `OLSR-c`@7 = k220'nin `u-birincil-*` satırları (eski kod + eski deneme sayısı);
- DESPARETE@6 · AODV@6 · `OLSR-d`@6 = k223'ünkiler.
Biri tutmazsa k220 ile k223 arasında beyan edilmemiş bir davranış farkı vardır → kusur aranır.

## T1 · Deneme sayısının etkisi (8 tohum, eşleştirilmiş)

Δ_MAC = PDR(6) − PDR(7), protokol başına ortalama ± SE. Yön önceden bilinmiyor.
- DESPARETE: Δ_MAC ortalaması ≤ −0,05 **ve** AODV'ninkinden 2 SE'den fazla aşağıdaysa (fark-farkı, tohum başına) → **v0.4.1 deneme sayısına duyarlı** (yeniden deneme başarısızlığını sinyal olarak kullanan mekanizmalar) → Faz 5.0'ın girdisi; K-200'ün sayıları 8 denemeyle ölçülmüştü. Değilse 1003'teki −0,117 tek tohumun kısa pencere salınımı.
- Taban protokoller için engel değil: U1 gerçek hâlleri ölçer.

## T2 · §8.2.1'in etkisi (8 tohum, eşleştirilmiş)

Δ_8.2.1 = PDR(`OLSR-d`@7) − PDR(`OLSR-c`@7). Hangi yönde çıkarsa çıksın düzeltme kalır (sadakat kuralı, K-207). Ortalama ≥ +0,05 ise OLSR'ın birincil hücredeki eski sayıları (K-200: 0,418) onu olduğundan düşük gösteriyordu → K-224'te yazılır.

## T3 · 1003'teki +0,140'ın ayrışması

Δ_toplam = [`OLSR-d`@6 − `OLSR-d`@7] + [`OLSR-d`@7 − `OLSR-c`@7] — iki terim yazılır.
