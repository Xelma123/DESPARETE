#!/bin/sh
# K-249 · M4'ün sıfır gözlem kuralı: yeni donmuş kopya → regresyon k249 →
# mimari → karşılaştırma k244 → k249 → G1-P. Ölçüt `beklenti.md`, koşudan
# önce commit'li. Kesilirse biten adım atlanır. Regresyon temiz değilse durur.
#     sh arsiv/teshis/m4_sifir_gozlem_2026-10-17/kos.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
ANA="$(cd "$D/../../.." && pwd)"
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$ANA" || exit 1
kos() {
    ad=$1; cikti=$2; shift 2
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        return 0
    fi
    echo "$ad basla $(date '+%d.%m %H:%M:%S')" >> "$D/zaman.txt"
    "$@" > "$cikti" 2>&1
    rc=$?
    echo "$ad bitti $(date +%H:%M:%S) cikis $rc" >> "$D/zaman.txt"
    return $rc
}
if [ ! -d "$K" ]; then
    py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py "$K" > "$D/kopya_ozet.txt" 2>&1 || exit 1
    echo "kopya donduruldu $(date '+%d.%m %H:%M:%S') · HEAD $(git rev-parse --short HEAD)" >> "$D/zaman.txt"
fi
cd "$K" || exit 1
mkdir -p ciktilar2/regresyon
kos uret "$D/uret.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k249 || exit 1
cp -n ciktilar2/regresyon/k249.jsonl "$ANA/ciktilar2/regresyon/k249.jsonl"
kos mimari "$D/mimari.txt" py -3.11 kalibrasyon/mimari_denetimi.py
cd "$ANA" || exit 1
if ! kos karsilastir "$D/karsilastir.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k244 k249; then
    echo "regresyon temiz degil: durdu $(date +%H:%M:%S)" >> "$D/zaman.txt"
    exit 1
fi
cd "$K" || exit 1
export DESPARETE_DUNYA=referans_2026
kos g1p "$D/G1p.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1p
echo "kos bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
