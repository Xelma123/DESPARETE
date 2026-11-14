#!/bin/sh
# Faz 5-2 · DESPARETE ↔ Babel kayıp anatomisi — dondurulmuş `kopya/`dan.
# Ölçütler `beklenti.md`, koşudan önce commit'li. İki adım, her biri ~3 sa;
# biten adım atlanır, kesilen adım ara kayıttan (`kayit_*.jsonl`) sürer.
#     sh arsiv/teshis/faz5_2_anatomi_2026-11-14/kosu.sh ikiz|birincil|hepsi
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
cd "$K" || exit 1
ORTAK="--dunya referans_2026 --kol formasyon --protokoller desparete,babel,en_guvenilir_kahin --tohumlar 1003,1004,1005,1006 --isci 8"
kos() {
    ad=$1; shift
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$ad zaten bitti"
        return 0
    fi
    echo "$ad basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    # shellcheck disable=SC2086
    py -3.11 -u kalibrasyon/kayip_anatomisi.py $ORTAK "$@" \
        --kayit "$D/kayit_$ad.json" >> "$D/anatomi_$ad.txt" 2>&1
    rc=$?
    echo "$ad bitti $(date '+%d.%m %H:%M:%S') cikis $rc" >> "$D/zaman.txt"
    return $rc
}
case "$1" in
    ikiz)     kos ikiz --sinif yok ;;
    birincil) kos birincil --aile derin_sizma ;;
    hepsi)    kos ikiz --sinif yok && kos birincil --aile derin_sizma ;;
    *) echo "adim: ikiz|birincil|hepsi"; exit 2 ;;
esac
