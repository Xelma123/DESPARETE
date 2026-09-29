# K-178 · A7 referans dünyanın girdileri — ölçmeden ÖNCE yazılan beklenti (26 Eylül 2026)

Adım: `v2/15` A7. `dunya` = "olcek_1_50" (varsayılan) | "referans_2026" (`sim2/kanal/dunya.py::referans_2026`). Referansta verici gücü GİRDİ (EIRP 20 dBm); alıcı dipol kazancı 2,15 dBi; menzil ve eşikler PER modelinden türer. Değerler `v2/14`ten:
- 1:1 ölçek, 7 km alan, 50–300 m irtifa, 40–120 km/h;
- 22 MHz, NF 7, K 10 dB;
- yeniden deneme 7, CCA 15 µs;
- karıştırıcı tabanı 30 dBm (geçici).

## 0 · Kapı (ölçüldü, `turetim.py`) — `bag_butcesi.py` ile aynı sayılar
- Gürültü −93,55 dBm.
- Nominal bağ (PER %10 + 10 dB) **1 664 m** (betik 1,65 km).
- Sönümsüz duyarlılık menzili **5 261 m** (betik 5,2 km).
- β = PER %50 + 2σ = **6,05 dB** (β mesafesi 2 974 m).
- Girişim menzili (SNR 0 dB) 5 968 m.
- 🔴 İlk denemede nominal bağ 1 299 m çıktı: bağ bütçesi alıcıdaki dipol kazancını (2,15 dBi) sayıyor, model saymıyordu (güç türetildiği için eski dünyada sadeleşiyordu). `alici_anten_kazanci_dbi` eklendi (eski dünyada 0).

## 1 · Tam takım
→ 874 + 4 (A7) = **878 passed**.

## 2 · Regresyon `k177 ↔ k178`
`python kalibrasyon/regresyon_satirlari.py karsilastir k177 k178 --yeni r- --izin "kimlik.kurulum_hash,konfig.dunya,konfig.verici_eirp_dbm,konfig.menzil_snr_db,konfig.alici_anten_kazanci_dbi,konfig.karistirici_taban_dbm,kapsam.dunya,teshis.koken_kovalari"`
- Ortak **61/61 birebir**. Eski dünyada güç türetimi, girişim oranı, yol kaybı (−0,0 dB kazanç) ve karıştırıcı gücü aynı yoldan.
- Farklar yalnız: kod kimliği · `kurulum_hash` · beş yeni konfig alanı · `kapsam.dunya` · köken kovaları (TÜRETİLMİŞ +3, KAYNAK +1, SINANMAMIŞ +1).
- Üç yeni `r-referans-…` vakası geçerli.
- Süre ~33–40 dk: referans dünyada her düğüm her düğümü duyuyor, alım denemeleri artar.
