#!/bin/sh
# K-231 · regresyon k223 → k231 (kopya defteri) — dondurulmuş `kopya/`dan,
# ~45 dk. Ölçüt `beklenti.md`, koşudan önce commit'li. Kesilirse biten adım
# atlanır.
#     sh arsiv/teshis/regresyon_k231/kosu.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
ANA="$D/../../.."
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
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
mkdir -p ciktilar2/regresyon
kos uret "$D/uret.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k231
cp -n ciktilar2/regresyon/k231.jsonl "$ANA/ciktilar2/regresyon/k231.jsonl"
cd "$ANA" || exit 1
kos karsilastir "$D/karsilastir.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k223 k231 --izin teshis.koken_kovalari
echo "kosu bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
