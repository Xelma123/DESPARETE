#!/bin/sh
# Faz 5-3 · açlık teşhisi — karıştırıcısız ikizde çekirdek (ilk ölçümün
# koşusunun aynısı) ve veri tetiği kapalı kol, açlık kaydıyla; dondurulmuş
# `kopya/`dan. Ölçütler `beklenti.md`, koşudan önce commit'li. İki adım (her
# biri 8 saatin altında); biten adım atlanır, kesilen adım ara kayıttan
# (`kayit_*.jsonl`) sürer.
#     sh arsiv/teshis/faz5_3_aclik_2026-11-18/kosu.sh cekirdek|vtk0|hepsi|duman
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"                  # ölçüm: dondurulmuş kopya
KOK="$(cd "$D/../../.." && pwd)"   # duman: çalışma ağacı (beklentinin commit'i)
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
TOHUM="--tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8"
kos() {
    kol=$1
    if grep -q "^$kol bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$kol zaten bitti"
        return 0
    fi
    cd "$K" || return 1
    echo "$kol basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    # shellcheck disable=SC2086
    py -3.11 -u "$D/aclik_teshisi.py" --dunya referans_2026 --kollar "$kol" \
        $TOHUM --kayit "$D/kayit_$kol.json" >> "$D/teshis_$kol.txt" 2>&1
    rc=$?
    echo "$kol bitti $(date '+%d.%m %H:%M:%S') cikis $rc" >> "$D/zaman.txt"
    return $rc
}
# Duman: kısa pencere, tohum 1003, iki kol birlikte (2 işçi). Çekirdek kolu
# ilk ölçümün duman kaydıyla birebir olmalı. Ölçüm değil, hiçbir karara
# girmez. Beklentinin commit'inden SONRA, çalışma ağacından.
duman() {
    cd "$KOK" || return 1
    mkdir -p "$D/duman"
    py -3.11 -u "$D/aclik_teshisi.py" --dunya referans_2026 --kisa \
        --kollar cekirdek,vtk0 --tohumlar 1003 --isci 2 \
        --kayit "$D/duman/kayit_duman.json" >> "$D/duman_kisa.txt" 2>&1 \
        || return 1
    py -3.11 "$D/sonuc_hesap.py" "$D/duman" >> "$D/duman_kisa.txt" 2>&1
}
case "$1" in
    cekirdek|vtk0) kos "$1" ;;
    duman) duman ;;
    hepsi) kos cekirdek && kos vtk0 ;;
    *) echo "adim: cekirdek|vtk0|hepsi|duman"; exit 2 ;;
esac
