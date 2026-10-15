# K-244 kuyruğu — ara sonuç (kuyruk kesildi; kalanlar ayrı koşulacak)

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

## 3 · Sıradaki (her biri ayrı beklentiyle, tek ağır iş)

1. **AODV-k'nin düşüşünün teşhisi** (`arsiv/teshis/aodv_k_ab_2026-10-15/`): değişikliklerin tek tek geri alındığı A/B, statik kolda (~1,5 sa).
2. **Babel'in kâhin aşımı:** K-192 (b) zarf prosedürü, dört hücre (~2 sa).
3. **Kalan kuyruk:** U1 eşler arası (ara kayıttan) · G1ç · G2ç + G4ç · G1-P. Bunlar AODV'nin teşhisinin sonucuna bağlı: AODV kodu değişirse U1 ve regresyon yeniden koşulur.
