#!/bin/sh
# Faz 5-2 (d) · karıştırmanın yerel işaretleri — Babel-a'nın üç geliştirme
# hücresinde, dondurulmuş `kopya/`dan. Ölçütler `beklenti.md`, koşudan önce
# commit'li. Üç adım (her biri 8 saatin altında); biten adım atlanır, kesilen
# adım ara kayıttan (`kayit_*.jsonl`) sürer.
#     sh arsiv/teshis/faz5_2_isaretler_2026-11-16/kosu.sh \
#         ikiz|birincil|dayaniklilik|hepsi
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
cd "$K" || exit 1
ORTAK="--dunya referans_2026 --kol formasyon --tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8"
E="@tehdit_acik_s=10+tehdit_sessiz_s=20"
kos() {
    ad=$1; sinif=$2; kol=$3
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$ad zaten bitti"
        return 0
    fi
    echo "$ad basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    # shellcheck disable=SC2086
    py -3.11 -u kalibrasyon/karistirma_isaretleri.py $ORTAK --sinif "$sinif" \
        --protokoller "$kol" --kayit "$D/kayit_$ad.json" \
        >> "$D/isaret_$ad.txt" 2>&1
    rc=$?
    echo "$ad bitti $(date '+%d.%m %H:%M:%S') cikis $rc" >> "$D/zaman.txt"
    return $rc
}
ikiz()         { kos ikiz yok babel; }
birincil()     { kos birincil surekli babel; }
dayaniklilik() { kos dayaniklilik surekli "babel$E"; }
case "$1" in
    ikiz|birincil|dayaniklilik) "$1" ;;
    hepsi) ikiz && birincil && dayaniklilik ;;
    *) echo "adim: ikiz|birincil|dayaniklilik|hepsi"; exit 2 ;;
esac
