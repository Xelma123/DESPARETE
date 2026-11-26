#!/bin/sh
# Faz 5-3 · B5 teşhisi — iletim kaybının yeri (karıştırılan alıcı, sıradaki
# aday, kanıtın zamanı); iki hücre, dondurulmuş `kopya/`dan. Ölçütler
# `beklenti.md`, koşudan önce commit'li. İki adım (hücre başına; her biri
# 8 saatin altında); biten adım atlanır, kesilen adım ara kayıttan
# (`kayit_*.jsonl.gz`) sürer.
#     sh arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26/kosu.sh <hücre>|hepsi|duman|mekanik [<klasör>]
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"                       # ölçüm: dondurulmuş kopya
KOK="$(cd "$D/../../.." && pwd)"   # duman ve mekanik: çalışma ağacı
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
# Kısa koşu: kısa pencere, tek tohum, iki hücre yan yana, kaydediciyle; sonra
# karar hesabı. Çalışma ağacından.
kisa() {
    tohum=$1
    hedef=$2
    cd "$KOK" || return 1
    mkdir -p "$hedef"
    for h in $ADIMLAR; do
        py -3.11 -u "$D/olcum.py" --dunya referans_2026 --kisa --hucre "$h" \
            --tohumlar "$tohum" --isci 1 --kayit "$hedef/kayit_$h.json.gz" \
            > "$hedef/olcum_$h.txt" 2>&1 &
    done
    wait
    py -3.11 "$D/sonuc_hesap.py" "$hedef" > "$hedef/sonuc_hesap.txt" 2>&1
}
case "$1" in
    # Mekanik denetim: öngörüler yazıldıktan sonra, commit'ten önce; ölçülen
    # tohumların dışındaki 1001. Klasörün adı `mekanik` olmalı: karar hesabı
    # o kipte yalnız iç denetimleri ve bölümlerin hesaplandığını yazar, sayı
    # basmaz.
    mekanik)
        hedef=${2:-"$D/mekanik"}
        case "$hedef" in
            */mekanik) ;;
            *) echo "klasörün adı mekanik olmalı: $hedef"; exit 2 ;;
        esac
        kisa 1001 "$hedef" ;;
    # Duman: beklentinin commit'inden SONRA; tohum 1003. Satırlar yeni çekirdek
    # ölçümünün duman kaydındaki `eğim0` satırlarıyla birebir olmalı (K0).
    # Ölçüm değil, hiçbir karara girmez.
    duman) kisa 1003 "$D/duman" ;;
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
        echo "adim: hepsi|duman|mekanik|$ADIMLAR"; exit 2 ;;
esac
