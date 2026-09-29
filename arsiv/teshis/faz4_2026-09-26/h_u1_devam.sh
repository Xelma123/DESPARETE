#!/usr/bin/env bash
# 4.3 devamı (K-190): kopmuş OLSR süreci (PID 32388) bitene kadar bekler,
# sonra AOMDV yere toplamayı koşar. Eşler arası desen öğrenciye soruldu.
K="C:/Users/Xelma123/AppData/Local/Temp/claude/C--Users-Xelma123-Desktop-desparete-pls/5cdbe106-8289-49e7-a318-3bb30615ea86/scratchpad/kopya_43"
D="C:/Users/Xelma123/Desktop/desparete_pls/arsiv/teshis/faz4_2026-09-26"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
while tasklist //FI "PID eq 32388" | grep -q python; do sleep 60; done
echo "olsr yere_toplama bitti (kopmus surec) $(date +%H:%M)" >> "$D/h_u1_ozet.txt"
cd "$K"
bas=$(date +%s)
python -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aomdv > "$D/h_u1_aomdv_yere_toplama.txt" 2>&1
echo "aomdv yere_toplama cikis=$? sure=$(( $(date +%s) - bas )) s" >> "$D/h_u1_ozet.txt"
echo "YERE_TOPLAMA_BITTI" >> "$D/h_u1_ozet.txt"
