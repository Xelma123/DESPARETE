# Regresyon k204 → k215 — beklenen farklar (ölçmeden önce)

> 6 Ekim 2026 · ajan · K-215 kod partisinden sonra, dondurulmuş kopyadan, yanında ağır iş yok.
> `py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k215` → `karsilastir k204 k215 --izin <aşağıda> --degisen <aşağıda>`

## k204'ten beri değişen (K-214, K-215)

1. **`AODV-j`** — başlangıç durumu −∞ (AOMDV miras alır). AODV ve AOMDV koşan bütün vakalar değişebilir: eski dünyada `k-statik-surekli-aodv` · `k-statik-surekli-aomdv` · `t-statik-surekli-aodv-dugum_kaybi`; referansta `r-referans-statik-surekli-aodv` · `u-birincil-aodv` · `u-birincil-aomdv` · `u-statik-surekli_darbeli-aodv` · `u-statik-reaktif-aodv` · `u-statik-aldatici-aodv` · `u-statik-taramali-aodv` · `u-statik-surekli-aodv-cephe_hatti` · `u-gorev-surekli-aomdv-esler_arasi`.
2. **Kâhinin sönümleme örneği 6 → 48** — yalnız HAREKETLİ kollarda (statikte tek örnek): `c-bagimsiz-surekli-en_guvenilir_kahin` · `c-bagimsiz-surekli-en_kisa_yol_kahin` · `c-gorev-surekli-en_guvenilir_kahin` · `c-gorev-surekli-en_kisa_yol_kahin` · `h-formasyon-surekli-en_guvenilir_kahin` · `u-birincil-en_guvenilir_kahin`.
3. **Referans dünyada TTL 32 → 64 ve beacon 32 → 84 B** — `konfig.ttl_baslangic` ve `konfig.beacon_bayt` bütün referans vakalarında farklı (izinli). Davranış: beacon kullanan referans vakaları (`r-referans-statik-yok-dogrudan_komsu` · `r-referans-bagimsiz-surekli-dogrudan_komsu` · `u-birincil-en_guvenilir_kahin`) ve TTL ölümü olan OLSR vakaları (`u-birincil-olsr` · `u-bagimsiz-surekli-olsr-dugum_kaybi`) değişebilir.
4. **Rician K eksen** (`TEDAVI_ALANLARI`'na girdi) → `kimlik.kurulum_hash` ve `kimlik.tedavi_hash` BÜTÜN vakalarda farklı (izinli).
5. **Köken defteri** → `teshis.koken_kovalari` bütün vakalarda farklı (izinli). Değişen kayıtlar: `ttl_baslangic` · `beacon_araligi_s` · `beacon_bayt` → KAYNAK; `komsu_omru_katsayisi` · `gps_dikey_sigma_m` · `gps_hiz_sigma_ms` · `rssi_olcum_sigma_db` → DUYARSIZ; `gorev_grup_sayisi` · `gm_pitch_sigma_rad` · `kahin.py::ATLAMA_ESIGI` → KOL_TANIMI; `rician_k_db` → TEDAVI; `kahin.py::SONUMLEME_ORNEGI` · `kontrol.py::BEKLEYEN_UYANDIRMA_TAVANI` → ÖLÇÜLMÜŞ; yeni `dunya.py::REFERANS_TTL` (KAYNAK) ve K-213'te eklenen üç kalibrasyon kaydı.
6. Kod kimliği (otomatik).

## Değişmemesi gerekenler

- **DESPARETE** (`u-statik-yok-desparete` · `u-birincil-desparete` · `k-statik-surekli-desparete-yere_toplama`): metrik ve korunum BİREBİR — beacon kapalı, TTL ölümü yok (k204'te 0), kâhin ve AODV kodu okumaz.
- Eski dünyanın OLSR'ı (`k-statik-surekli-olsr`): BİREBİR (TTL eski dünyada 32 kalır).
- Eski dünyanın statik kâhinleri (`c-statik-*`, `f-statik-surekli-en_guvenilir_kahin-tam`, `g-statik-*`, `i-statik-surekli-en_guvenilir_kahin-hava_eslik`): BİREBİR (tek örnek).
- Eski dünyanın bütün sınav ve basit protokol vakaları (`a-` `b-` `d-` `e-` `f-` `g-bagimsiz` `h-formasyon-surekli-dogrudan_komsu` `i-` `j-` `l-` `m-` `n-` `o-` `p-` `q-` `s-` `t-bagimsiz`): BİREBİR.

Kural: yukarıdakiler dışında her fark BULGU'dur.
