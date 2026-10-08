#!/bin/sh
# Faz 4.5 · doğrulama listesi, kopyadan, sırayla.
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D/kopya" || exit 1
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
kos() {
    ad=$1; shift
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    "$@" > "$D/$ad.txt" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
}
kos 1_anlamlilik py -3.11 -u kalibrasyon/anlamlilik_sabitleri.py
export DESPARETE_DUNYA=referans_2026
kos 2_bag_kumesi py -3.11 -u kalibrasyon/bag_kumesi.py a
kos 3_li py -3.11 -u kalibrasyon/li_replikasyonu.py --dunya referans_2026
kos 4_kontrol_duzlemi py -3.11 -u kalibrasyon/kontrol_duzlemi_kapilari.py
kos 5_denetim_ornekleme py -3.11 -u kalibrasyon/denetim_ornekleme.py
kos 6_ust_referans py -3.11 -u kalibrasyon/ust_referans.py --kapi
kos 7_evre py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py
unset DESPARETE_DUNYA
kos 8_uretici_duman py -3.11 -u kalibrasyon/uretici_duman.py
