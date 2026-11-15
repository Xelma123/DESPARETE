#!/bin/sh
# Faz 5-2 (c) · rakiplerin, kâhinin ve v0.4.1'in üç geliştirme hücresindeki
# çizgisi — dondurulmuş `kopya/`dan. Ölçütler `beklenti.md`, koşudan önce
# commit'li. Beş adım (her biri 8 saatin altında); biten adım atlanır, kesilen
# adım ara kayıttan (`kayit_*.jsonl`) sürer.
#     sh arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/kosu.sh \
#         ikiz|birincil|dayaniklilik|v041_ikiz|v041_karistirma|rakipler|hepsi
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
cd "$K" || exit 1
ORTAK="--dunya referans_2026 --kol formasyon --tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8"
# Uzun koşan kol önce: son dalganın boşta beklemesi kısalır.
RAKIP="aodv,babel,olsrv2,en_guvenilir_kahin"
E="@tehdit_acik_s=10+tehdit_sessiz_s=20"
kos() {
    ad=$1; sinif=$2; kollar=$3; ek=$4
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$ad zaten bitti"
        return 0
    fi
    echo "$ad basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    # shellcheck disable=SC2086
    py -3.11 -u kalibrasyon/kayip_anatomisi.py $ORTAK --sinif "$sinif" $ek \
        --protokoller "$kollar" --kayit "$D/kayit_$ad.json" \
        >> "$D/anatomi_$ad.txt" 2>&1
    rc=$?
    echo "$ad bitti $(date '+%d.%m %H:%M:%S') cikis $rc" >> "$D/zaman.txt"
    return $rc
}
ikiz()            { kos ikiz yok "$RAKIP" "--hayalet 10:20"; }
birincil()        { kos birincil surekli "$RAKIP" ""; }
dayaniklilik()    { kos dayaniklilik surekli \
                        "aodv$E,babel$E,olsrv2$E,en_guvenilir_kahin$E" ""; }
v041_ikiz()       { kos v041_ikiz yok desparete "--hayalet 10:20"; }
v041_karistirma() { kos v041_karistirma surekli "desparete,desparete$E" ""; }
case "$1" in
    ikiz|birincil|dayaniklilik|v041_ikiz|v041_karistirma) "$1" ;;
    rakipler) ikiz && birincil && dayaniklilik ;;
    hepsi)    ikiz && birincil && dayaniklilik && v041_ikiz && v041_karistirma ;;
    *) echo "adim: ikiz|birincil|dayaniklilik|v041_ikiz|v041_karistirma|rakipler|hepsi"; exit 2 ;;
esac
