#!/bin/sh
# AODV-k'nin U1 düşük hücreleri — kayıp anatomisi, donmuş kopyadan. Üç kol
# paralel (3 + 2 + 2 işçi, tek ağır iş). Ölçüt `beklenti.md`, koşudan önce
# commit'li.
#     sh arsiv/teshis/aodv_k_anatomi_2026-10-16/anatomi.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/../rakipler_k244_2026-10-14/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$K" || exit 1
kos() {
    kol=$1; tohumlar=$2; isci=$3
    echo "$kol basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 \
        --sinif yok --kol "$kol" --protokoller aodv --tohumlar "$tohumlar" \
        --isci "$isci" --kayit "$D/anatomi_$kol.json" \
        > "$D/anatomi_$kol.txt" 2>&1
    rc=$?
    echo "$kol bitti $(date +%H:%M:%S) cikis $rc" >> "$D/zaman.txt"
}
echo "anatomi basla $(date '+%d.%m %H:%M:%S') · kopya rakipler_k244 (1163f81)" >> "$D/zaman.txt"
kos statik 1000,1001,1002 3 &
kos bagimsiz 1000,1002 2 &
kos gorev 1000,1001 2 &
wait
echo "anatomi bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
