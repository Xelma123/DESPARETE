#!/bin/sh
# Döngü izinin YENİDEN koşusu (düzeltilmiş araç, 3 süreç) + Babel'in zarf
# aşımı teşhisi (5 işçi) — aynı anda, toplam 8 işçi. İlk koşunun izi eksikti
# (rota kuruluşları kaydedilmiyordu; `ilk_kosu_eksik_iz/`). İkisi de donmuş
# kopyadan; ölçütler kendi dizinlerinin `beklenti.md`sinde, koşudan önce
# commit'li.
#     sh arsiv/teshis/aodv_k_dongu_2026-10-16/kos2.sh
D="$(cd "$(dirname "$0")" && pwd)"
T="$D/../babel_zarf_asim_2026-10-16"
K="$(cd "$D/../rakipler_k244_2026-10-14/kopya" && pwd)"
ANA="$(cd "$D/../../.." && pwd)"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$ANA" || exit 1
iz() {
    echo "iz2 $1 $2 basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    DONGU_KOK="$K" py -3.11 -u "$D/dongu_izi.py" "$1" "$2" \
        > "$D/dongu_$1_$2.txt" 2>&1
    rc=$?
    echo "iz2 $1 $2 bitti $(date +%H:%M:%S) cikis $rc" >> "$D/zaman.txt"
}
teshis() {
    echo "teshis basla $(date '+%d.%m %H:%M:%S') · kopya rakipler_k244 (1163f81)" >> "$T/zaman.txt"
    KOK="$K" py -3.11 -u "$T/teshis.py" > "$T/teshis.txt" 2>&1
    rc=$?
    echo "teshis bitti $(date +%H:%M:%S) cikis $rc" >> "$T/zaman.txt"
}
echo "kos2 basla $(date '+%d.%m %H:%M:%S') · kopya rakipler_k244 (1163f81) · HEAD $(git rev-parse --short HEAD)" >> "$D/zaman.txt"
iz bagimsiz-yok 1000 &
iz gorev-yok 1000 &
iz gorev-yok 1001 &
teshis &
wait
echo "kos2 bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
