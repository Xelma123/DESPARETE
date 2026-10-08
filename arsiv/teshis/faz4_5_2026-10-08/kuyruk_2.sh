#!/bin/sh
D="$(cd "$(dirname "$0")" && pwd)"
ANA="$D/../../.."
cd "$D/kopya_2" || exit 1
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 DESPARETE_DUNYA=referans_2026
kos() {
    ad=$1; shift
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    "$@" > "$D/$ad.txt" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
}
kos 9_denetim_C py -3.11 -u kalibrasyon/denetim_ornekleme.py c
kos 10_li_sabit_hiz py -3.11 -u "$ANA/arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py" "$D/kopya_2"
kos 11_G3c py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 3c
