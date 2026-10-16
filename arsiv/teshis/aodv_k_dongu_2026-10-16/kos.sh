#!/bin/sh
# AODV-k döngü izi (3 hücre, 3 süreç) + Babel'in eşler arası zarfı (5 işçi) —
# aynı anda, toplam 8 işçi. İkisi de donmuş kopyadan; ölçütler kendi
# dizinlerinin `beklenti.md`sinde, koşudan önce commit'li.
#     sh arsiv/teshis/aodv_k_dongu_2026-10-16/kos.sh
D="$(cd "$(dirname "$0")" && pwd)"
Z="$D/../babel_zarf_esler_2026-10-16"
K="$(cd "$D/../rakipler_k244_2026-10-14/kopya" && pwd)"
ANA="$(cd "$D/../../.." && pwd)"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$ANA" || exit 1
iz() {
    echo "iz $1 $2 basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    DONGU_KOK="$K" py -3.11 -u "$D/dongu_izi.py" "$1" "$2" \
        > "$D/dongu_$1_$2.txt" 2>&1
    rc=$?
    echo "iz $1 $2 bitti $(date +%H:%M:%S) cikis $rc" >> "$D/zaman.txt"
}
zarf() {
    echo "zarf basla $(date '+%d.%m %H:%M:%S') · kopya rakipler_k244 (1163f81)" >> "$Z/zaman.txt"
    KOK="$K" py -3.11 -u "$Z/zarf.py" > "$Z/zarf.txt" 2>&1
    rc=$?
    echo "zarf bitti $(date +%H:%M:%S) cikis $rc" >> "$Z/zaman.txt"
}
echo "kos basla $(date '+%d.%m %H:%M:%S') · kopya rakipler_k244 (1163f81) · HEAD $(git rev-parse --short HEAD)" >> "$D/zaman.txt"
iz bagimsiz-yok 1000 &
iz gorev-yok 1000 &
iz gorev-yok 1001 &
zarf &
wait
echo "kos bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
