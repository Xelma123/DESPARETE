# SINANMAMIŞ borcu (48) — kapanış planı (Faz 4.4 hazırlığı)

> 26 Eylül 2026 · ajan · kaynak listesi: `sinanmamis_liste.txt` (`sim2/yapilandirma/kokenler.py`dan) · ön-kayıt şartı: mühürden önce SINANMAMIŞ = 0 ya da borçlular eksen olarak ilan edilir (`v2/06` §9)

Dört yol:
- **(a)** Doğrulanmış bir kaynakla (`v2/02`) referans dünyada kapanır; yeni indirme gerekmez.
- **(b)** Yeni kaynak ister; her indirme için ayrı izin.
- **(c)** Ölçümle kapanır: duyarlılık (DUYARSIZ) ya da kalibrasyon (ÖLÇÜLMÜŞ).
- **(d)** Beyanla eksen/varsayım olarak kalır.

| yol | parametreler | not |
|---|---|---|
| **(a)** | `bit_hizi_bps` (G1, G2) · `cca_s` → referansta 15 µs (G2) · `yeniden_deneme_siniri` → referansta 7 (G12, G13) · `irtifa_maks_m` → referansta 300 m (G9 zarfı, `v2/14` onaylı) · `beacon_araligi_s` (RFC 3561 §10, `02` §R1) · `yakalama_penceresi_s` (önbelge süresinin kendisi → TÜRETİLMİŞ) | köken metni referans değerine göre yeniden yazılır |
| **(c) · Faz 4.1** | `karistirici_taban_dbm` · `REFERANS_KARISTIRICI_DBM` (ρ ölçütü, 4.1b) · `REFERANS_ALAN_M` (4.1a, öğrenci kararından sonra ÖLÇÜLMÜŞ) | |
| **(c) · duyarlılık** | `rician_k_db` (6 · 10 · 15 dB — `v2/14` §2'de planlı) · `gm_adim_s` · `kanal_dilimi_s` · `komsu_omru_katsayisi` · `golgeleme_hucre_m` · `isinma_s` · `olcum_bitis_s` (`v2/06` §8 koşul 1) · `BASARI_ESIGI`/`ATLAMA_ESIGI` · `REFERANS_PAY_DB` | `kalibrasyon/duyarlilik.py` referans dünyada |
| **(b)** | `gps_dikey_sigma_m` · `gps_hiz_sigma_ms` (GNSS alıcı veri sayfası) · `rssi_olcum_sigma_db` (telsiz yonga veri sayfası) · `saat_sapma_ppm` (kristal veri sayfası) · `onay_bayt` (802.11 ACK — G12 kaynağında olabilir, önce oraya bakılır) · `reaktif_*` (G5'in kaynakçası) · `rota_tamponu_*` (NS-2 `aodv_rqueue`) · `yakalama_esigi_db` | indirme listesi öğrenciye ayrı ayrı sunulur |
| **(d)** | `akis_sayisi` · `gorev_grup_sayisi` · `beacon_bayt` · `ttl_baslangic` · `kuyruk_kapasitesi` · `saat_ofset_araligi_s` · `tehdit_*_hiz_kmh` · kalibrasyon örneklem sabitleri (`TOHUMLAR`, `ADIM_S` …) · `BEKLEYEN_UYANDIRMA_TAVANI` (güvenlik sınırı) · `evre.ALFA` (ön-kayıtın α'sı) · `KONTROL_KAPSULLEME` | eksen ya da gerekçeli varsayım olarak ilan; mühür listesinde |

**Önce yapılacak:** (a) satırı Faz 4.4'te tek bir köken yamasıyla kapanır (tahmini borç 48 → ~42); (c) Faz 4.1 bitince (~39).
