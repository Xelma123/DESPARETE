#!/bin/sh
# Faz 4b kapanış ölçümleri, ikinci kuyruk (K-238) — dondurulmuş `kopya/`dan.
# Ölçüt `beklenti.md`, koşudan önce commit'li. Kesilirse biten adım atlanır.
#     sh arsiv/teshis/faz4b_kapanis2_2026-10-12/kuyruk.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 DESPARETE_DUNYA=referans_2026
cd "$K" || exit 1
kos() {
    ad=$1; cikti=$2; shift 2
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        return 0
    fi
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    "$@" > "$cikti" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
}
cp "$D/kopya_payi.py" "$K/kopya_payi.py"
mkdir -p ciktilar2
# Adım 1 — paralel: kopya payı · dört temsilci anatomi · G1ç.
kos kopya_payi "$D/kopya_payi.txt" py -3.11 -u kopya_payi.py statik-yok 1001 esler_arasi 0.9827 &
for h in statik:1002 bagimsiz:1000 gorev:1000 formasyon:1000; do
    k=${h%%:*}; t=${h##*:}
    kos "anatomi_$k" "$D/anatomi_${k}_$t.txt" py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol "$k" --protokoller jarmrout --tohumlar "$t" --isci 1 --kayit "$D/anatomi_${k}_$t.json" &
done
kos g1c "$D/G1c.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c &
wait
# Adım 2 — G2ç + G4ç.
kos g2c "$D/G2c.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 2c
echo "kuyruk bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
