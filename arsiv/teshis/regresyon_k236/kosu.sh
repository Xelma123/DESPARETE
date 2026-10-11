#!/bin/sh
# K-236 · regresyon k232 → k236 (yeni rakipler JarmRout ve OLSRv2) — dondurulmuş `kopya/`dan,
# ~50 dk. Ölçüt `beklenti.md`, koşudan önce commit'li. Kesilirse biten adım
# atlanır.
#     sh arsiv/teshis/regresyon_k236/kosu.sh
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
kos uret "$D/uret.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k236
cp -n ciktilar2/regresyon/k236.jsonl "$ANA/ciktilar2/regresyon/k236.jsonl"
cd "$ANA" || exit 1
kos karsilastir "$D/karsilastir.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k232 k236 --izin teshis.koken_kovalari --yeni u-birincil-jarmrout,u-birincil-olsrv2,u-bagimsiz-surekli-jarmrout-esler_arasi,u-bagimsiz-surekli-olsrv2-dugum_kaybi
echo "kosu bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
