#!/bin/sh
# K-223 · kuyruk A (kopya_a'dan, sırayla; ~2,5 sa): regresyon k223 → R →
# OLSR anatomisi. Ölçütler `beklenti.md` (A1–A3), commit'li olarak önce.
# Kesilirse biten adımlar atlanır; anatomi ara kayıttan sürer.
#     sh arsiv/teshis/denetim_duzeltme_2026-10-09/kuyruk_a.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya_a"
ANA="$D/../../.."
R="$ANA/arsiv/teshis/regresyon_k223"
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
kos A1_uret "$R/uret.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k223
cp -n ciktilar2/regresyon/k223.jsonl "$ANA/ciktilar2/regresyon/k223.jsonl"
cd "$ANA" || exit 1
kos A1_karsilastir "$R/karsilastir.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k220 k223 --izin kapsam.rota_tamponu.kaynak,teshis.koken_kovalari --degisen r-referans-,u-,k-statik-surekli-olsr --yeni u-birincil-evre-
kos A1_denetle "$R/denetle.txt" py -3.11 arsiv/teshis/regresyon_k223/denetle.py
cd "$K" || exit 1
kos A2_R "$D/A2_cozunurluk.txt" py -3.11 -u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40
kos A3_anatomi "$D/A3_anatomi_statik.txt" py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol statik --protokoller olsr --tohumlar 1000,1001,1002 --isci 3 --kayit "$D/A3_anatomi_statik.json"
echo "kuyruk A bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
