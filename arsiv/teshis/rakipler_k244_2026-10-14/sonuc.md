# K-244 kuyruğu — sonuç (15–17 Ekim; kesinti, teşhisler ve kalan adımlar dâhil)

> 15 Ekim 2026 · ölçüt `beklenti.md` (commit `1163f81`, koşudan önce) · `kopya/` = `1163f81` (150 dosya birebir, `kopya_ozet.txt`; `arac_hash` 106324a5…) · çıktılar `uret.txt` · `karsilastir.txt` · `mimari.txt` · `U1_yere_toplama.txt` · `U1_esler_arasi.txt` (yarım)

**Kesinti:** kuyruk 11:28'de başladı. Arka plan kabuğu ~21:04'te dışarıdan sonlandı (~9,5 sa; çalışan süreç kalmadı, zaman dosyasında son adımın "bitti" satırı yok). Biten adımlar sağlam. Eşler arası U1'in 14/36 koşusu ara kayıtta; alet aynı kodla yeniden başlatılınca oradan sürer. G1ç, G2ç + G4ç ve G1-P koşulmadı.

## 1 · Regresyon k243 → k244 ✓

- İlan edilen 12 AODV/AOMDV vakası değişti ve geçerli.
- Yeni iki Babel vakası geçerli; `gecersiz_paket` 0.
- Öteki 73 vaka birebir; farklar yalnız kod kimliği.
- Mimari denetimi ihlalsiz, çıkış 0.
- `uret` 78,6 dk.

Yeni taban **k244**.

## 2 · U1, yere toplama (`aodv_uygunluk.py` çıkış 1)

### Babel — U1-U KALDI (kâhin aşımı), U1-B TEMİZ

Bütün hücreler eşiğin üstünde: oran statik 0,989–0,992, hareketli 0,899–1,032. Ama altı hareketli hücrede oran 1 + R'yi (1,0126) aşıyor:

| kol | tohum | Babel | ETX kâhini | oran |
|---|---|---|---|---|
| bağımsız | 1001 | 0,9095 | 0,8882 | 1,024 |
| bağımsız | 1002 | 0,8548 | 0,8334 | 1,026 |
| görev | 1001 | 0,8957 | 0,8679 | 1,032 |
| görev | 1002 | 0,9198 | 0,8998 | 1,022 |
| formasyon | 1001 | 0,9517 | 0,9467 | 1,005 |
| formasyon | 1002 | 0,9549 | 0,9495 | 1,006 |

- Formasyonun iki hücresi R içinde (1,005 · 1,006). Öteki dördü için beklentinin koşullu adımı geçerli: K-192 (b), üç kâhinin zarfı.
- Babel kopya göndermez; sızdırmazlık taraması (`tests2/test_kosum.py`) ve mimari denetimi kâhin erişimi bulmuyor. ETX kâhini kesin tavan değildir (K-110).
- Rota tamponu girişi 0: Babel bekletmez.

### AODV-k — U1-U GEÇTİ, U1-B KALDI

| kol | tohum | AODV-k | kâhin | oran | AODV-j kaydı | karar |
|---|---|---|---|---|---|---|
| statik | 1000 | 0,8441 | 0,9905 | 0,852 | 0,8944 | KAYIT SAPTI |
| statik | 1001 | 0,8445 | 0,9868 | 0,856 | 0,9205 | açıklanmamış |
| statik | 1002 | 0,8079 | 0,9945 | 0,812 | 0,8628 | KAYIT SAPTI |
| bağımsız | 1000 | 0,3900 | 0,8204 | 0,475 | 0,5560 | KAYIT SAPTI |
| bağımsız | 1001 | 0,5560 | 0,8882 | 0,626 | | geçti |
| bağımsız | 1002 | 0,4802 | 0,8334 | 0,576 | | açıklanmamış |
| görev | 1000 | 0,4451 | 0,9078 | 0,490 | | açıklanmamış |
| görev | 1001 | 0,5172 | 0,8679 | 0,596 | | açıklanmamış |
| görev | 1002 | 0,5868 | 0,8998 | 0,652 | | geçti |
| formasyon | 1000–1002 | | | 0,604–0,677 | | geçti |

AODV-k, AODV-j'nin kayıtlı oranlarının 0,04–0,08 altında. PDR olarak AODV-j → AODV-k (K-224 kaydı, aynı tohumlar): statik 0,886 · 0,908 · 0,858 → 0,844 · 0,845 · 0,808; bağımsız 0,456 · 0,631 · 0,549 → 0,390 · 0,556 · 0,480; görev 0,567 · 0,590 · 0,631 → 0,445 · 0,517 · 0,587; formasyon 0,696 · 0,752 · 0,663 → 0,580 · 0,641 · 0,625. K-242 ve K-244'ün AODV değişikliklerinden biri ya da birkaçı yere toplamada AODV'yi zayıflatıyor. Bu, değişikliklerin beklenen yönüne (titreşim, önceki atlama ve karşılıksız RREP güçlendirir) ters. Sebep ölçülmeden AODV-k donmaz.

## 3 · Teşhisler (her biri kendi beklentisiyle, tek ağır iş)

1. **AODV-k'nin düşüşü** (`arsiv/teshis/aodv_k_ab_2026-10-15/`): A/B'de düşüşün kaynağı ns-3'ün iki varsayılanı (karşılıksız RREP +0,0225, yayın titreşimi +0,024). Gerçekleme ikisine sadık → (a), AODV-k değişmez.
2. **AODV-k'nin yedi düşük hücresi:**
   - Anatomi (`arsiv/teshis/aodv_k_anatomi_2026-10-16/`): kimlik ve korunum tamam; en büyük düşüş statikte `iletim_basarisiz`, hareketlide `rota_gecersiz`.
   - Anatominin beklentisi TTL için "< %1" yazmıştı; bu kuyruğun §2.2'si "0" istiyor. Önce yazılan kural uygulandı; üç hücre (birer TTL düşüşü) açıklanmış listeden çıkarıldı.
   - Döngü izi (`arsiv/teshis/aodv_k_dongu_2026-10-16/`): ilk koşunun aracı rota kuruluşlarını kaydetmiyordu, düzeltilip yeniden koşuldu. Üç döngü RFC §6.5 · §6.7 (i) · (iii) · §6.11'den, ns-3'le aynı (K-207 madde 2) → yedi hücre açıklanmış.
3. **Babel'in kâhin aşımı:**
   - Yere toplamada dört hücre zarfın içinde (`arsiv/teshis/babel_zarf_2026-10-15/`).
   - Eşler arasında beş aşım: ikisi zarfın içinde, üçü zarfı da aşıyor (`arsiv/teshis/babel_zarf_esler_2026-10-16/`).
   - Hata araması temiz; kâhinin fazla kaybı `iletim_basarisiz`'da (`arsiv/teshis/babel_zarf_asim_2026-10-16/`). Kayıt K-248'in kuralıyla.

## 4 · U1, eşler arası (`U1_esler_arasi_2.txt`, ara kayıttan 22 koşu, 16 Ekim 15:43–17:29)

- **AODV-k:** U1-U geçti. Kâhin aşımı statik 1001'de 1,0051, R içinde. U1-B'de görev 1001 (0,593) keşifsel desenin açıklanmamış bulgusu; donmayı durdurmaz (§2.3).
- **Babel:** sekiz aşım. U1-U K-248'den sonra geçti, U1-B temiz.

## 5 · Evre kapıları (`kalan.sh`, her adım ayrı arka plan işi)

| kapı | koşu | sonuç |
|---|---|---|
| G1ç (`G1c.txt`) | 17 Ekim 01:45–03:33 | ✓ M4 0/8 · M1 2 SE dışında 1/4 (Babel −0,018, 2 SE 0,0177) · D iki tohumda dışarıda yok |
| G2ç + G4ç (`G2c.txt`) | 03:33–05:49 | ✓ kâhinin M1'i etkili, D 2 SE içinde · p99 < açık süre |
| G1-P (`G1p.txt`) | 05:49–06:11 | ✗ M4 2/8 (OLSRv2 1001 · Babel 1001, ikisi de açılmadan 47 s sonra) |

- **G1-P'nin teşhisi** (`arsiv/teshis/g1p_k244_2026-10-17/`):
  - Babel koşu boyunca tek bir kopma beyan ediyor ve temiz evresi boş: boş dağılım Poisson(0), eşik 0.
  - OLSRv2'nin tespiti kendi beyan kümelenmesinden (17 > 16); ortak bağ yok.
- **K-249 kuralı** (yürütücü): temizde sıfır beyanda M4'ün hızı sıfır gözlemin üst güven sınırı. Regresyon k249 birebir; G1-P yeniden 1/8 · 1/8 · 1/4 → **geçti** (`arsiv/teshis/m4_sifir_gozlem_2026-10-17/`).
- **Betimleyici** (birincil hücre, `PDR_açık`, 1003 · 1004; iki tohum hüküm vermez):

| | 1003 | 1004 |
|---|---|---|
| kâhin | 0,748 | 0,844 |
| Babel | 0,547 | 0,787 |
| DESPARETE | 0,518 | 0,603 |
| OLSRv2 | 0,409 | 0,499 |
| AODV-k | 0,353 | 0,421 |

## 6 · Donma ve kapanış

- **Donma şartları** (beklenti, "Donma") tamam: regresyon temiz (k244, ardından k249) · U1-U iki desende ✅ · U1-B yere toplamada temiz · G1ç, G2ç + G4ç, G1-P geçti.
- **`AODV-k` ve `Babel-a` dondu:** `tests2/test_donma.py`'de `aodv.py` · `aodv_bicim.py` yenilendi, `babel.py` · `babel_bicim.py` eklendi. Özetler bu kuyruğun kopyasıyla (`1163f81`) birebir.
- **Doğrulama:** tam takım 1095 geçti (`arsiv/teshis/m4_sifir_gozlem_2026-10-17/tam_takim.txt`) · mimari denetimi ihlalsiz ve bulgusuz (`mimari_2.txt`).
- Karar kaydı **K-249**.

## 7 · Süreler (bu kuyrukta ölçülen, 350 s'lik koşu, 8 işçi)

| protokol | birincil hücre (G2ç) | karıştırıcısız ikiz (G1ç) |
|---|---|---|
| kâhin | 0,75–0,89 sa | 0,52–0,58 sa (boş kol) |
| OLSRv2 | 1,06–1,09 sa | 0,82–0,92 sa |
| Babel | 1,35–1,43 sa | 1,06–1,07 sa |
| DESPARETE v0.4.1 | 1,37–1,45 sa | 1,33–1,38 sa |
| AODV-k | 2,11–2,20 sa | 1,78–1,80 sa |
