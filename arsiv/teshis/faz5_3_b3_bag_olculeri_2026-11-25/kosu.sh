#!/bin/sh
# Faz 5-3 · B3 teşhisi — bağın iki ölçüsü aynı bağda, bizim çekirdeğimizin
# trafiğinde; iki hücre, dondurulmuş `kopya/`dan. Ölçütler `beklenti.md`,
# koşudan önce commit'li. İki adım (hücre başına; her biri 8 saatin altında);
# biten adım atlanır, kesilen adım ara kayıttan (`kayit_*.jsonl.gz`) sürer.
#     sh arsiv/teshis/faz5_3_b3_bag_olculeri_2026-11-25/kosu.sh <hücre>|hepsi|duman
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"                       # ölçüm: dondurulmuş kopya
KOK="$(cd "$D/../../.." && pwd)"   # duman: çalışma ağacı (beklentinin commit'i)
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
TOHUM="--tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8"
ADIMLAR="ikiz birincil"
kos() {
    h=$1
    if grep -q "^$h bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$h zaten bitti"
        return 0
    fi
    cd "$K" || return 1
    echo "$h basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    # shellcheck disable=SC2086
    py -3.11 -u "$D/olcum.py" --dunya referans_2026 --hucre "$h" $TOHUM \
        --kayit "$D/kayit_$h.json.gz" >> "$D/olcum_$h.txt" 2>&1
    rc=$?
    echo "$h bitti $(date '+%d.%m %H:%M:%S') cikis $rc" >> "$D/zaman.txt"
    return $rc
}
# Duman: kısa pencere, tohum 1003, iki hücre kaydediciyle. Satırlar B2
# teşhisinin duman koşusundaki kaydedicisiz satırlarla birebir olmalı (karar
# hesabının K0'ı). Ölçüm değil, hiçbir karara girmez. Beklentinin commit'inden
# SONRA, çalışma ağacından (kod o commit'le aynı).
duman() {
    cd "$KOK" || return 1
    mkdir -p "$D/duman"
    for h in $ADIMLAR; do
        py -3.11 -u "$D/olcum.py" --dunya referans_2026 --kisa --hucre "$h" \
            --tohumlar 1003 --isci 1 --kayit "$D/duman/kayit_$h.json.gz" \
            > "$D/duman/olcum_$h.txt" 2>&1 &
    done
    wait
    py -3.11 "$D/sonuc_hesap.py" "$D/duman" > "$D/duman_kisa.txt" 2>&1
}
case "$1" in
    duman) duman ;;
    hepsi)
        for a in $ADIMLAR; do
            kos "$a" || exit 1
        done ;;
    *)
        for a in $ADIMLAR; do
            if [ "$1" = "$a" ]; then
                kos "$a"
                exit $?
            fi
        done
        echo "adim: hepsi|duman|$ADIMLAR"; exit 2 ;;
esac
