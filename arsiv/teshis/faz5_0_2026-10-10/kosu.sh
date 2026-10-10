#!/bin/sh
# Faz 5.0 · kayıp anatomisi, birincil hücre — dondurulmuş `kopya/`dan, ~5 sa.
# Ölçütler `beklenti.md`, koşudan önce commit'li. Kesilirse aynı komut
# kaldığı yerden sürer (alet `kayit.jsonl`deki koşuları atlar).
#     sh arsiv/teshis/faz5_0_2026-10-10/kosu.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
export DESPARETE_DUNYA=referans_2026
cd "$K" || exit 1
echo "anatomi basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 \
    --kol formasyon --aile derin_sizma \
    --protokoller desparete,aodv,aomdv,olsr,en_guvenilir_kahin \
    --tohumlar 1003,1004,1005,1006 --isci 8 \
    --kayit "$D/kayit.json" >> "$D/anatomi.txt" 2>&1
echo "anatomi bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
