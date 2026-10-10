# Ek ölçüt — `gm_alfa`nın yeniden ölçümü (ölçmeden önce)

> 10 Ekim 2026 · ajan · tetik: B1'de (`B1_duyarlilik.txt`) `gm_alfa ×2` GEÇERSİZ (α = 1,966 ∉ [0, 1)) ve `×0,5` (α = 0,49) τ'yu 29 s'den 0,7 s'ye indiren, "yarıya" denemeyecek bir oynatma. Ölçüm aletinin tasarım hatası — ölçüt (DUYARSIZ ⇔ |Δ| < R ve band içinde) DEĞİŞMEDİ.
> Düzeltme: `duyarlilik.py::KORELASYON_KATSAYILARI` — α = exp(−adım/τ) zaman sabitinden oynatılır, τ×c ⇔ α^(1/c): ×0,5 → 0,9663 · ×2 → 0,9915 (test `test_KORELASYON_KATSAYISI_…`). Emsal: olasılık sabitleri kayıp payından, dBm ±3 dB.

- `py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil gm_alfa` (5 tohum; ~20 dk), dondurulmuş kopyadan (`kopya_c`), R = 0,0126.
- Kural `beklenti.md` B1'deki gibi: sınırda (DUYARLI ama |Δ| ≤ 1,3R ve band ≤ 1,8× · ya da duyarsız ama |Δ| ≥ 0,7R) → `--tohum 20` (~1,5 sa), sonucu 5 tohumluğun yerine geçer. DUYARSIZ → köken DUYARSIZ; DUYARLI → öğrenciye.
- B1'in `gm_alfa ×0,5` satırı (α = 0,49) hükme girmez; `sonuc.md`de gerekçesiyle yazılır.
- `gm_hiz_sigma_ms` (B1: ×2'de 2,2R, band 2,9× — sınırda değil, DUYARLI) yeniden ölçülmez → öğrencinin kararı.
