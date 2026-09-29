#!/usr/bin/env bash
# 4.3 — U1 referans dünyada, dondurulmuş kopyadan, sırayla. Her koşunun
# çıktısı arsive; JSON kayıtları kopyanın ciktilar2'sinde (sonra taşınır).
K="C:/Users/Xelma123/AppData/Local/Temp/claude/C--Users-Xelma123-Desktop-desparete-pls/5cdbe106-8289-49e7-a318-3bb30615ea86/scratchpad/kopya_43"
D="C:/Users/Xelma123/Desktop/desparete_pls/arsiv/teshis/faz4_2026-09-26"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$K"
for desen in yere_toplama; do
  for p in olsr aomdv; do
    bas=$(date +%s)
    python -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen "$desen" --protokol "$p" > "$D/h_u1_${p}_${desen}.txt" 2>&1
    echo "$p $desen cikis=$? sure=$(( $(date +%s) - bas )) s" >> "$D/h_u1_ozet.txt"
  done
done
echo "BITTI" >> "$D/h_u1_ozet.txt"
