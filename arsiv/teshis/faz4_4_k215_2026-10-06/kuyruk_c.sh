#!/bin/sh
# U1 prosedür adımları: zarf → OLSR anatomisi (iki çağrı birlikte, 3 + 1 süreç).
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya_b"
ANA="$D/../../.."
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 ZARF_KOK="$K"
cd "$K" || exit 1
echo "zarf basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
py -3.11 -u "$ANA/arsiv/teshis/aodv_sadakat_2026-09-30/aomdv_zarf_hucre.py" esler_arasi statik-yok 1001 0.9923 0.9898 > "$D/zarf.txt" 2>&1
echo "zarf bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
echo "anatomi basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --protokoller olsr --kol bagimsiz --tohumlar 1000,1001,1002 --isci 3 --kayit "$D/anatomi_bagimsiz.json" > "$D/anatomi_bagimsiz.txt" 2>&1 &
py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --protokoller olsr --kol gorev --tohumlar 1001 --isci 1 --kayit "$D/anatomi_gorev.json" > "$D/anatomi_gorev.txt" 2>&1 &
wait
echo "anatomi bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
