#!/bin/sh
# K-244 kuyruğu — regresyon k244 · U1 (AODV-k · Babel, iki desen) · G1ç ·
# G2ç + G4ç · G1-P — dondurulmuş `kopya/`dan, ~12–16 sa. Ölçüt `beklenti.md`,
# koşudan önce commit'li. Kesilirse biten adım atlanır. Regresyon temiz
# değilse kuyruk durur.
#     sh arsiv/teshis/rakipler_k244_2026-10-14/kuyruk.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya"
ANA="$D/../../.."
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
DEGISEN=k-statik-surekli-aodv,k-statik-surekli-aomdv,r-referans-statik-surekli-aodv,t-statik-surekli-aodv-dugum_kaybi,u-birincil-aodv,u-birincil-aomdv,u-gorev-surekli-aomdv-esler_arasi,u-statik-aldatici-aodv,u-statik-reaktif-aodv,u-statik-surekli-aodv-cephe_hatti,u-statik-surekli_darbeli-aodv,u-statik-taramali-aodv
YENI=u-birincil-babel,u-bagimsiz-surekli-babel-dugum_kaybi
cd "$K" || exit 1
# Çıkış kodu komuttan hemen sonra alınır (k236 · k243 betiklerindeki
# `$(date)` sonrası `$?` hatası, K-243).
kos() {
    ad=$1; cikti=$2; shift 2
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        return 0
    fi
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    "$@" > "$cikti" 2>&1
    rc=$?
    echo "$ad bitti $(date +%H:%M:%S) cikis $rc" >> "$D/zaman.txt"
    return $rc
}
mkdir -p ciktilar2/regresyon ciktilar2/aodv_uygunluk
kos uret "$D/uret.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k244 || exit 1
cp -n ciktilar2/regresyon/k244.jsonl "$ANA/ciktilar2/regresyon/k244.jsonl"
kos mimari "$D/mimari.txt" py -3.11 kalibrasyon/mimari_denetimi.py
cd "$ANA" || exit 1
if ! kos karsilastir "$D/karsilastir.txt" py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k243 k244 --degisen "$DEGISEN" --yeni "$YENI"; then
    echo "regresyon temiz degil: kuyruk durdu $(date +%H:%M:%S)" >> "$D/zaman.txt"
    exit 1
fi
cd "$K" || exit 1
kos u1_yere_toplama "$D/U1_yere_toplama.txt" py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aodv,babel
kos u1_esler_arasi "$D/U1_esler_arasi.txt" py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen esler_arasi --protokol aodv,babel
cp -n ciktilar2/aodv_uygunluk/*.json "$ANA/ciktilar2/aodv_uygunluk/" 2>/dev/null
export DESPARETE_DUNYA=referans_2026
kos g1c "$D/G1c.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c
kos g2c "$D/G2c.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 2c
kos g1p "$D/G1p.txt" py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1p
echo "kuyruk bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
