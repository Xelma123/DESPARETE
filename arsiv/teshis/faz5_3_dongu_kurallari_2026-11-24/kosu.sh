#!/bin/sh
# Faz 5-3 · döngü kuralları (KK-04/13 geri gönderme yasağı, KK-04/14 sınırlı
# yükselme) — karıştırıcısız ikiz ve birincil hücre, dondurulmuş `kopya/`dan.
# Ölçütler `beklenti.md`, koşudan önce commit'li. Dört adım (kol × hücre; her
# biri 8 saatin altında); biten adım atlanır, kesilen adım ara kayıttan
# (`kayit_*.jsonl`) sürer.
#     sh arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/kosu.sh <kol>_<hücre>|hepsi|duman
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"                  # ölçüm: dondurulmuş kopya
KOK="$(cd "$D/../../.." && pwd)"   # duman: çalışma ağacı (beklentinin commit'i)
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
TOHUM="--tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8"
ADIMLAR="geri_sinir_ikiz geri_sinir_birincil geri_ikiz geri_birincil"
kos() {
    ad=$1; kol=${ad%_*}; hucre=${ad##*_}
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$ad zaten bitti"
        return 0
    fi
    cd "$K" || return 1
    echo "$ad basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    # shellcheck disable=SC2086
    py -3.11 -u "$D/olcum.py" --dunya referans_2026 --hucre "$hucre" \
        --kollar "$kol" $TOHUM --kayit "$D/kayit_$ad.json" \
        >> "$D/olcum_$ad.txt" 2>&1
    rc=$?
    echo "$ad bitti $(date '+%d.%m %H:%M:%S') cikis $rc" >> "$D/zaman.txt"
    return $rc
}
# Duman: kısa pencere, tohum 1003, iki hücre; iki kol ve 19 Kasım'ın çekirdeği
# (yeni çekirdeğin ölçümünün `cekirdek` duman satırıyla birebir olmalı),
# ayrıca `geri_sinir` kaydedicisiz, doğrudan kayıp anatomisi aletiyle
# (kaydedicili koşuyla birebir olmalı). Ölçüm değil, hiçbir karara girmez.
# Beklentinin commit'inden SONRA, çalışma ağacından (kod o commit'le aynı).
duman() {
    cd "$KOK" || return 1
    mkdir -p "$D/duman"
    for hucre in ikiz birincil; do
        py -3.11 -u "$D/olcum.py" --dunya referans_2026 --kisa \
            --hucre "$hucre" --kollar geri_sinir,geri,c19 \
            --tohumlar 1003 --isci 3 \
            --kayit "$D/duman/kayit_duman_$hucre.json" \
            >> "$D/duman_kisa.txt" 2>&1 || return 1
    done
    ORTAK="--dunya referans_2026 --kol formasyon --kisa --tohumlar 1003 --isci 1 --protokoller desparete5_cekirdek"
    # shellcheck disable=SC2086
    py -3.11 -u kalibrasyon/kayip_anatomisi.py $ORTAK --sinif yok \
        --hayalet 10:20 --kayit "$D/duman/duz_ikiz.json" \
        > "$D/duman/duz_ikiz.txt" 2>&1 &
    p1=$!
    # shellcheck disable=SC2086
    py -3.11 -u kalibrasyon/kayip_anatomisi.py $ORTAK --sinif surekli \
        --kayit "$D/duman/duz_birincil.json" \
        > "$D/duman/duz_birincil.txt" 2>&1 &
    p2=$!
    wait $p1 || return 1
    wait $p2 || return 1
    py -3.11 "$D/sonuc_hesap.py" "$D/duman" >> "$D/duman_kisa.txt" 2>&1
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
