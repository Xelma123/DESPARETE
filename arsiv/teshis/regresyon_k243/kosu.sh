#!/bin/sh
# K-242 · regresyon k236 → k243 (kalıcı görüş hattı, AODV'nin yeni sürümü,
# kapı sertleştirmeleri) — dondurulmuş `kopya/`dan, ~70 dk. Ölçüt
# `beklenti.md`, koşudan önce commit'li. Kesilirse biten adım atlanır.
#     sh arsiv/teshis/regresyon_k243/kosu.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
ANA="$D/../../.."
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
DEGISEN=k-statik-surekli-aodv,k-statik-surekli-aomdv,r-referans-statik-surekli-aodv,t-statik-surekli-aodv-dugum_kaybi,u-birincil-aodv,u-birincil-aomdv,u-gorev-surekli-aomdv-esler_arasi,u-statik-aldatici-aodv,u-statik-reaktif-aodv,u-statik-surekli-aodv-cephe_hatti,u-statik-surekli_darbeli-aodv,u-statik-taramali-aodv,u-birincil-desparete,u-birincil-en_guvenilir_kahin,u-birincil-evre-en_guvenilir_kahin,u-birincil-jarmrout,u-birincil-olsr,u-birincil-olsrv2
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
kos uret "$D/uret.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k243
cp -n ciktilar2/regresyon/k243.jsonl "$ANA/ciktilar2/regresyon/k243.jsonl"
kos mimari "$D/mimari.txt" py -3.11 kalibrasyon/mimari_denetimi.py
cd "$ANA" || exit 1
kos karsilastir "$D/karsilastir.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k236 k243 --izin kimlik.kurulum_hash,konfig.a2g_durum_dilimi_s,teshis.koken_kovalari --degisen "$DEGISEN"
echo "kosu bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
