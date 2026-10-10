#!/bin/sh
# K-225 · Faz 4.5 doğrulama listesi son kodla (kopya_d'den, sırayla; ~2 sa).
# Ölçütler `beklenti_dogrulama.md`, commit'li olarak önce.
#     sh arsiv/teshis/denetim_duzeltme_2026-10-09/kuyruk_d.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya_d"
ANA="$D/../../.."
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$K" || exit 1
kos() {
    ad=$1; shift
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        return 0
    fi
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    "$@" > "$D/$ad.txt" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
}
export DESPARETE_DUNYA=referans_2026
kos D1_bag_kumesi py -3.11 -u kalibrasyon/bag_kumesi.py a
kos D2_li py -3.11 -u kalibrasyon/li_replikasyonu.py --dunya referans_2026
kos D3_li_sabit_hiz py -3.11 -u "$ANA/arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py" "$K"
kos D4_kontrol_duzlemi py -3.11 -u kalibrasyon/kontrol_duzlemi_kapilari.py
kos D5_denetim_ornekleme py -3.11 -u kalibrasyon/denetim_ornekleme.py
kos D5c_denetim_C py -3.11 -u kalibrasyon/denetim_ornekleme.py c
kos D6_ust_referans py -3.11 -u kalibrasyon/ust_referans.py --kapi
kos D7_evre py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py
unset DESPARETE_DUNYA
kos D8_uretici_duman py -3.11 -u kalibrasyon/uretici_duman.py
echo "kuyruk D bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
