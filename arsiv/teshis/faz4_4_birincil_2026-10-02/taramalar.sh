#!/bin/sh
# Faz 4.4 parametre taramaları — birincil hücre, kopya_2'den, sırayla (K-213).
# Dört parti: elektrik kesilirse biten partiler kalır. Taban her partide
# yeniden koşulur (aynı tohumlar, aynı sonuç; partiyi bağımsız kılar).
#     sh arsiv/teshis/faz4_4_birincil_2026-10-02/taramalar.sh
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D/kopya_2" || exit 1
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
kos() {
    ad=$1; shift
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil "$@" > "$D/$ad.txt" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
}
kos T1a rician_k_db golgeleme_hucre_m gm_adim_s gm_pitch_sigma_rad yakalama_esigi_db kuyruk_kapasitesi
kos T1b cbr_titresim_s saat_ofset_araligi_s saat_sapma_ppm kanal_dilimi_s sim2/dunya/mobilite.py::ISTASYON_TUTMA_S
kos T2 beacon_araligi_s beacon_bayt komsu_omru_katsayisi kalibrasyon/kahin.py::ATLAMA_ESIGI kalibrasyon/kahin.py::SONUMLEME_ORNEGI
kos E gps_dikey_sigma_m gps_hiz_sigma_ms rssi_olcum_sigma_db
