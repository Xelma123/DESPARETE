#!/bin/sh
# Faz 5-2 (b) · v0.4.1'in iki kapalı seçeneği ve iletim başarısızlığının sebebi
# — dondurulmuş `kopya/`dan. Ölçütler `beklenti.md`, koşudan önce commit'li.
# İki adım (taban ~2 sa 15 dk · seçenek ~4 sa); biten adım atlanır, kesilen
# adım ara kayıttan (`kayit_*.jsonl`) sürer.
#     sh arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/kosu.sh taban|secenek|hepsi
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
cd "$K" || exit 1
ORTAK="--dunya referans_2026 --kol formasyon --sinif yok --tohumlar 1003,1004,1005,1006 --isci 8"
TABAN="desparete,babel,en_guvenilir_kahin"
SECENEK="desparete~hedefli_canlilik,desparete~onarim_edinimi,desparete~hedefli_canlilik+onarim_edinimi"
kos() {
    ad=$1; kollar=$2
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$ad zaten bitti"
        return 0
    fi
    echo "$ad basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    # shellcheck disable=SC2086
    py -3.11 -u kalibrasyon/kayip_anatomisi.py $ORTAK --protokoller "$kollar" \
        --kayit "$D/kayit_$ad.json" >> "$D/anatomi_$ad.txt" 2>&1
    rc=$?
    echo "$ad bitti $(date '+%d.%m %H:%M:%S') cikis $rc" >> "$D/zaman.txt"
    return $rc
}
case "$1" in
    taban)   kos taban "$TABAN" ;;
    secenek) kos secenek "$SECENEK" ;;
    hepsi)   kos taban "$TABAN" && kos secenek "$SECENEK" ;;
    *) echo "adim: taban|secenek|hepsi"; exit 2 ;;
esac
