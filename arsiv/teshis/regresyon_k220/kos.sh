#!/bin/sh
D="$(cd "$(dirname "$0")" && pwd)"
ANA="$D/../../.."
cd "$D/kopya" || exit 1
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
mkdir -p ciktilar2/regresyon
echo "uret basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k220 > "$D/uret.txt" 2>&1
echo "uret bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
cp ciktilar2/regresyon/k220.jsonl "$ANA/ciktilar2/regresyon/k220.jsonl"
cd "$ANA" || exit 1
py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k215 k220 --izin kimlik.kurulum_hash,kimlik.tedavi_hash,konfig.iletim_menzili_m,konfig.nominal_bag_m,teshis.koken_kovalari > "$D/karsilastir.txt" 2>&1
echo "karsilastir bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
