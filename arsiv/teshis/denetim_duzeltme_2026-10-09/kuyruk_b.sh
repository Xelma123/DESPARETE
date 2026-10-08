#!/bin/sh
# K-223 · kuyruk B (kopya_b'den — R güncellendikten SONRA dondurulur; ~17 sa):
# D-07 duyarlılığı → U1 iki desen → evre kapıları. Ölçütler `beklenti.md`
# (B1–B3). Sınırdaki D-07 kaydı (`--tohum 20`) ve U1'in koşullu prosedür
# adımları (zarf, anatomi) sonuçlara göre ayrıca, aynı kopyadan.
#     sh arsiv/teshis/denetim_duzeltme_2026-10-09/kuyruk_b.sh
D="$(cd "$(dirname "$0")" && pwd)"
K="$D/kopya_b"
ANA="$D/../../.."
export PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1
cd "$K" || exit 1
kos() {
    ad=$1; shift
    if grep -q "^$ad bitti .* cikis 0$" "$D/zaman.txt" 2>/dev/null; then
        return 0
    fi
    echo "$ad basla $(date +%H:%M:%S)" >> "$D/zaman.txt"
    "$@" > "$D/$ad.txt" 2>&1
    echo "$ad bitti $(date +%H:%M:%S) cikis $?" >> "$D/zaman.txt"
}
kos B1_duyarlilik py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil gm_alfa gm_hiz_sigma_ms
kos B2_U1_yere_toplama py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aodv,olsr,aomdv
kos B2_U1_esler_arasi py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen esler_arasi --protokol aodv,olsr,aomdv
mkdir -p "$D/u1_kayitlari"
cp -n ciktilar2/aodv_uygunluk/*.json ciktilar2/aodv_uygunluk/*.jsonl "$D/u1_kayitlari/" 2>/dev/null
export DESPARETE_DUNYA=referans_2026
kos B3_G1c py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 1c
kos B3_G2c py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 2c
kos B3_G3c py -3.11 -u kalibrasyon/evre_metrikleri_kapilari.py 3c
echo "kuyruk B bitti $(date +%H:%M:%S)" >> "$D/zaman.txt"
