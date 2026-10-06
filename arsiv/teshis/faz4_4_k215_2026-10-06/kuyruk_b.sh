#!/bin/sh
# K-215 · kuyruk B (R güncellendikten sonra, kopya_b'den, sırayla; ~22 sa):
# sınırdaki 6 parametre 20 tohumla → protokol kontrolleri → U1 iki desen →
# evre kapıları 1c · 2c. Her adımın çıktısı ayrı dosyada; kesilirse biten
# adımlar kalır, U1 ara kayıttan sürer.
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya_b"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 TESHIS_KOK="$K"
cd "$K" || exit 1
kos() {
    ad=$1; shift
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        return 0
    fi
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    "$@" > "$D/$ad.txt" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
}
T="py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil --tohum 20"
kos S1 $T golgeleme_hucre_m gm_adim_s
kos S2 $T kanal_dilimi_s yakalama_esigi_db
kos S3 $T cbr_titresim_s sim2/dunya/mobilite.py::ISTASYON_TUTMA_S
kos protokol_kontrol py -3.11 -u "$D/protokol_kontrol.py"
kos U1_yere_toplama py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aodv,olsr,aomdv
kos U1_esler_arasi py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen esler_arasi --protokol aodv,olsr,aomdv
export DESPARETE_DUNYA=referans_2026
kos G1c py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c
kos G2c py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 2c
