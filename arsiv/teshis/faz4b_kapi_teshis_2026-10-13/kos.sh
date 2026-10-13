#!/bin/sh
# G1ç ve G4ç'nin JarmRout yüzünden kalması — teşhis (dondurulmuş kopyadan,
# `faz4b_kapanis2_2026-10-12/kopya` = d3fd674).
#     sh arsiv/teshis/faz4b_kapi_teshis_2026-10-13/kos.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/../faz4b_kapanis2_2026-10-12/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 DESPARETE_DUNYA=referans_2026
cd "$K" || exit 1
echo "teshis basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
py -3.11 -u "$D/kapi_teshis.py" 1003 1004 --kayit "$D/kapi_teshis.json" > "$D/kapi_teshis.txt" 2>&1
echo "teshis bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
