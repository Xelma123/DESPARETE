#!/bin/sh
# K-244 kuyruğunun kalanı — kuyruk 15 Ekim ~21:04'te dışarıdan kesildi
# (`sonuc.md`). Her adım AYRI bir arka plan işi (< ~8 sa; kabuk ~9,5 sa'te
# kesilmişti). Ölçüt kuyruğun `beklenti.md`si (commit `1163f81`). Aynı
# donmuş `kopya/`dan; U1 eşler arası ara kayıttan sürer. Biten adım atlanır.
#     sh arsiv/teshis/rakipler_k244_2026-10-14/kalan.sh u1_esler_arasi|g1c|g2c|g1p
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
ANA="$D/../../.."
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$K" || exit 1
kos() {
    ad=$1; cikti=$2; shift 2
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        echo "$ad zaten bitti"
        return 0
    fi
    echo "$ad basla $(date '+%d.%m %H:%M:%S') (kalan.sh)" >> "$D/zaman.txt"
    "$@" > "$cikti" 2>&1
    rc=$?
    echo "$ad bitti $(date +%H:%M:%S) cikis $rc" >> "$D/zaman.txt"
    return $rc
}
case "$1" in
    u1_esler_arasi)
        # Yarım çıktı ayrı adla; alet ara kayıttan (14/36) sürer.
        kos u1_esler_arasi "$D/U1_esler_arasi_2.txt" py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen esler_arasi --protokol aodv,babel
        rc=$?
        # Tarihli kayıtlar ana dala; `_son` adlıları ana daldakini EZMEZ.
        for f in ciktilar2/aodv_uygunluk/*_esler_arasi_2026*.json; do
            cp -n "$f" "$ANA/ciktilar2/aodv_uygunluk/"
        done
        exit $rc ;;
    g1c) export DESPARETE_DUNYA=referans_2026
         kos g1c "$D/G1c.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c ;;
    g2c) export DESPARETE_DUNYA=referans_2026
         kos g2c "$D/G2c.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 2c ;;
    g1p) export DESPARETE_DUNYA=referans_2026
         kos g1p "$D/G1p.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1p ;;
    *) echo "adim: u1_esler_arasi|g1c|g2c|g1p"; exit 2 ;;
esac
