#!/bin/sh
# K-215 · kuyruk A: regresyon k215 → çözünürlük R (kopya_k215'ten, sırayla).
D="$(cd "$(dirname "$0")" && pwd)"
ANA="$D/../../.."
K="$D/kopya"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$K" || exit 1
mkdir -p ciktilar2/regresyon
echo "uret basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k215 > "$D/uret.txt" 2>&1
echo "uret bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
cp ciktilar2/regresyon/k215.jsonl "$ANA/ciktilar2/regresyon/k215.jsonl"
R="$ANA/arsiv/teshis/faz4_4_k215_2026-10-06"
echo "R basla $(date +%H:%M:%S)" >> "$R/zaman.txt"
py -3.11 -u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40 > "$R/cozunurluk.txt" 2>&1
echo "R bitti $(date +%H:%M:%S) cikis $?" >> "$R/zaman.txt"
