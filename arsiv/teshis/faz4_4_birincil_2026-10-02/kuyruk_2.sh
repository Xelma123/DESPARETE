#!/bin/sh
# TTL ölçümü bitince sırayla: sönümleme yakınsaması → protokol taraması (K-214).
D="$(cd "$(dirname "$0")" && pwd)"
until grep -q "ttl bitti" "$D/zaman.txt"; do sleep 60; done
cd "$D/../../.." || exit 1
export TESHIS_KOK="$D/kopya_2" PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
for ad in sonumleme_yakinsama protokol_tarama; do
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    py -3.11 -u "$D/$ad.py" > "$D/$ad.txt" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
done
