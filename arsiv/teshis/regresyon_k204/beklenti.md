# Regresyon k203 → k204 — beklenen farklar (ölçmeden önce)

> 30 Eylül 2026 gece · ajan · U1 (`AODV-i` + `AOMDV-e`) ve evre kapılarından sonra, dondurulmuş kopyadan, yanında ağır iş yok.
> `py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k204` → `karsilastir k203 k204 --degisen <aşağıdaki vakalar>`

## k203'ten beri değişen

1. **`AODV-i`** (K-208, K-210): AODV koşan vakalar değişebilir: `k-statik-surekli-aodv` · `t-statik-surekli-aodv-dugum_kaybi` · `r-referans-statik-surekli-aodv` · `u-birincil-aodv` · `u-statik-surekli_darbeli-aodv` · `u-statik-reaktif-aodv` · `u-statik-aldatici-aodv` · `u-statik-taramali-aodv` · `u-statik-surekli-aodv-cephe_hatti`.
2. **`AOMDV-e`** (K-208, K-210: devralınan kısım + kendi işleyicilerinde RFC tabanı ve öncüller): `k-statik-surekli-aomdv` · `u-birincil-aomdv` · `u-gorev-surekli-aomdv-esler_arasi`.
3. **Evre metrikleri v2** (K-209): çizelgeli (`derin_sizma`) satırlarda evre alanları değişir ve yenileri eklenir: `i-statik-surekli-dogrudan_komsu-derin_sizma` · `u-birincil-*` (5 vaka; aodv ve aomdv yukarıda zaten).
4. Kod kimliği (otomatik) ve köken kovaları değişmedi (Konfig alanı eklenmedi → `kurulum_hash` her vakada aynı).

## Değişmemesi gerekenler

OLSR, DESPARETE, kâhin ve basit sınav protokollerinin sürekli karıştırıcılı ve karıştırıcısız bütün vakaları BİREBİR (evre alanları dâhil — sürekli karıştırıcıda evre satırı birebir, `test_K209_SUREKLI_karistiricida_SATIR_BIREBIR`). `u-birincil-olsr` · `u-birincil-desparete` · `u-birincil-en_guvenilir_kahin`'de yalnız evre alanları değişebilir; metrikler ve korunum birebir.

Kural: yukarıdakiler dışında her fark BULGU'dur.
