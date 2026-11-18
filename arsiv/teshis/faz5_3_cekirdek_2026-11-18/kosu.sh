#!/bin/sh
# Faz 5-3 · yeni sürümün çekirdeği (karıştırmaya karşı mekanizmalar kapalı)
# — karıştırıcısız ikiz ve birincil hücre, dondurulmuş `kopya/`dan. Ölçütler
# `beklenti.md`, koşudan önce commit'li. İki adım (her biri 8 saatin altında);
# biten adım atlanır, kesilen adım ara kayıttan (`kayit_*.jsonl`) sürer.
#     sh arsiv/teshis/faz5_3_cekirdek_2026-11-18/kosu.sh ikiz|birincil|hepsi|duman
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"                  # ölçüm: dondurulmuş kopya
KOK="$(cd "$D/../../.." && pwd)"   # duman: çalışma ağacı (beklentinin commit'i)
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
ORTAK="--dunya referans_2026 --kol formasyon"
TOHUM="--tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8"
kos() {
    ad=$1; sinif=$2; ek=$3
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$ad zaten bitti"
        return 0
    fi
    cd "$K" || return 1
    echo "$ad basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    # shellcheck disable=SC2086
    py -3.11 -u kalibrasyon/kayip_anatomisi.py $ORTAK $TOHUM --sinif "$sinif" \
        $ek --protokoller desparete5_cekirdek \
        --kayit "$D/kayit_cekirdek_$ad.json" >> "$D/anatomi_$ad.txt" 2>&1
    rc=$?
    echo "$ad bitti $(date '+%d.%m %H:%M:%S') cikis $rc" >> "$D/zaman.txt"
    return $rc
}
ikiz()     { kos ikiz yok "--hayalet 10:20"; }
birincil() { kos birincil surekli ""; }
# Duman: kısa pencere, tohum 1003; çekirdek ve Babel (Babel teşhis (c)'nin
# dumanıyla birebir olmalı). Ölçüm değil, hiçbir karara girmez. Beklentinin
# commit'inden SONRA, çalışma ağacından (kod o commit'le aynı).
duman() {
    cd "$KOK" || return 1
    mkdir -p "$D/duman"
    for s in "ikiz yok --hayalet 10:20" "birincil surekli"; do
        # shellcheck disable=SC2086
        set -- $s
        py -3.11 -u kalibrasyon/kayip_anatomisi.py $ORTAK --kisa \
            --tohumlar 1003 --isci 2 --sinif "$2" $3 $4 \
            --protokoller desparete5_cekirdek,babel \
            --kayit "$D/duman/kayit_cekirdek_$1.json" >> "$D/duman_kisa.txt" 2>&1 \
            || return 1
    done
    py -3.11 "$D/sonuc_hesap.py" "$D/duman" >> "$D/duman_kisa.txt" 2>&1
}
case "$1" in
    ikiz|birincil|duman) "$1" ;;
    hepsi) ikiz && birincil ;;
    *) echo "adim: ikiz|birincil|hepsi|duman"; exit 2 ;;
esac
