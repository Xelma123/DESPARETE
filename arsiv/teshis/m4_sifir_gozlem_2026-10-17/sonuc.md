# M4: temiz evrede sıfır beyan — üst güven sınırı · sonuç

> 17 Ekim 2026 · ölçüt `beklenti.md` (commit `5161bb9`, koşudan önce) · kopya `kopya/` = `5161bb9` (`kopya_ozet.txt`, `arac_hash` 9b9798f3…) · çıktılar `uret.txt` · `mimari.txt` · `mimari_2.txt` · `karsilastir.txt` · `karsilastir_2.txt` · `G1p.txt` · `tam_takim.txt` · `zaman.txt`

## 1 · Testler ✓

`tests2/test_evre.py` 37/37 geçti; ikisi K-249'un yeni testi (tek beyan tespit değil, beş beyanlık patlama tespit). Tam takım 1095 geçti (16 dk, `tam_takim.txt`).

## 2 · Mimari denetimi — beklentiden sapma (ajanın hatası, giderildi)

- **İlk koşu** (kopyada, `mimari.txt`): çıkış 1, bir bulgu. `kalibrasyon/aodv_uygunluk.py::_AODV_K_IZ` köken defterinde yoktu.
- **Sebep:** ajan sözlüğü 16 Ekim'de (AODV-k anatomisinin kaydı) ekledi. O gün mimari denetimini koştu ama yalnız "ihlal" satırına baktı; ayrı duran "bulgu" satırını görmedi.
- **Düzeltme:** `sim2/yapilandirma/kokenler.py`'ye OLCULMUS kaydı eklendi (üreticisi ve ölçüm dizinleriyle). Ana dalda yeniden koşuldu (`mimari_2.txt`): çıkış 0, bulgu yok.
- Köken kaydı simülasyonun davranışını değiştirmez. Regresyon ve G1-P bu kayıttan önceki kopyadan koşuldu.

## 3 · Regresyon k244 → k249 — beklentiden sapma, sebebi bulundu

- **İlk karşılaştırma** (`karsilastir.txt`): kimlik alanları dışında bir alan 87 vakada farklı: `kapsam.modellenmeyen.hareketli_karistirici`. Kuyruk kuralı gereği durdu.
- **Sebep:** k244'ün kopyası `1163f81`'den. Ondan sonra K-245 (`854cdef`, DD-17) `sim2/yapilandirma/kapsam.py`'deki bayat "hareketli karıştırıcı" metnini düzeltti ("derin sızma ~32 m" → "350 s'de ~1,6 km"). Satırın kapsam metni ölçüm değildir. Beklenti bu alanı öngörmemişti.
- **Yeniden karşılaştırma**, bu alana izinle (`karsilastir_2.txt`, `--izin kapsam.modellenmeyen.hareketli_karistirici`): **87/87 bulgusuz, BİREBİR.**
  - Farklı olan yalnız kimlik alanları: `arac_hash`, `kosu_kimligi`, `calisma_kimligi`, zaman damgası.
  - `protokol_hash` 80 vakada farklı: paket düzeyi özet, K-245'in `protokoller/desparete_bayrak.py` başlığı.
- Ölçüt 2 tuttu: M4 taşıyan beş satırda tespit yok, değişmedi. Yeni taban **k249**.
- Üretim 81 dk (12:46–14:07).

## 4 · G1-P yeniden ✓ GEÇTİ

| ölçüt | önce (K-244 kuyruğu) | sonra | sınır |
|---|---|---|---|
| M4 yanlış tespit | 2/8 | **1/8** (OLSRv2 1001) | ≤ 1/8 |
| M3 toparlanma ≠ 0 | 1/8 | 1/8 (Babel 1000) | ≤ 1/8 |
| M1 2 SE dışında | 1/4 | 1/4 (Babel) | ≤ 1/4 |

- Ölçüt 3 tuttu: yalnız Babel 1001'in tespiti kalktı (47 s → yok). Öteki yedi koşunun bütün sayıları birebir aynı.
- Not: karşılaştırma için basılan "eski kural" sütunu da Babel 1001'de değişti (47 → yok; eski kural 4/8 → 3/8). Sebebi `_EskiEvreler`'in `tespit_gecikmesi`'ni miras alması. Bu sütun kapıya girmez.
- G1-P koşusu 28 dk sürdü (14:09–14:37).

## 5 · Kapanış

Ölçüt 4 ve 5:

- G1ç ve G2ç + G4ç yeniden koşulmadı; gerekçesi beklentide.
- Kuyruk beklentisinin donma şartları tamam: AODV-k ve Babel-a dondu (`tests2/test_donma.py`).
- Kuyruğun sonucu `arsiv/teshis/rakipler_k244_2026-10-14/sonuc.md`'de; karar kaydı K-249.
