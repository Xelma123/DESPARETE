#!/bin/sh
# Faz 4b kapanış ölçümleri — U1 (JarmRout · OLSRv2, iki desen) ve çizelgeli
# evre kapıları (G1ç · G2ç + G4ç), dondurulmuş `kopya/`dan, ~12 sa. Ölçüt
# `beklenti.md`, koşudan önce commit'li. Kesilirse biten adım atlanır.
#     sh arsiv/teshis/faz4b_kapanis_2026-10-11/kuyruk.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
ANA="$D/../../.."
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$K" || exit 1
kos() {
    ad=$1; cikti=$2; shift 2
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        return 0
    fi
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    "$@" > "$cikti" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
}
mkdir -p ciktilar2/aodv_uygunluk
kos u1_yere_toplama "$D/U1_yere_toplama.txt" py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol jarmrout,olsrv2
kos u1_esler_arasi "$D/U1_esler_arasi.txt" py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen esler_arasi --protokol jarmrout,olsrv2
export DESPARETE_DUNYA=referans_2026
kos g1c "$D/G1c.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c
kos g2c "$D/G2c.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 2c
cp -n ciktilar2/aodv_uygunluk/*.json "$ANA/ciktilar2/aodv_uygunluk/" 2>/dev/null
echo "kuyruk bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
