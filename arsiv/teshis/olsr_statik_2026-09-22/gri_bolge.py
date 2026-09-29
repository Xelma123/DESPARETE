"""Gri bölge — yapısal ölçüm, simülasyon KOŞMAZ.

OLSR'ın kullandığı her bağ (i → j) için:
  p_kontrol : j'nin kısa bir kontrol çerçevesinin i'de TEK seferde çözülme
              olasılığı (i'nin histerezisi j'den gelen paketlerle beslenir)
  p_veri    : veri + onay çiftinin tek deneme başarısı (kâhin grafiğinin tanımı)
  p_atlama  : 1 − (1 − p_veri)^(yeniden deneme + 1)
Statik kolda sönümleme donuk → t = 0 değeri bağın kalıcı kalitesidir.
"""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "kalibrasyon"))

from kahin import KanalGrafigi  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

MESAJ_BAYT = (36, 60)      # tipik TC · tipik HELLO (RFC biçiminden, ~4 komşu blok başına)

R = json.loads((Path(__file__).parent / "olsr_teshis.json").read_text(encoding="utf-8"))
for r in R:
    kfg = Konfig(kol="u1", senaryo=r["kol"], tohum=r["tohum"])
    kur = kurulum_yap(kfg)
    grafik = KanalGrafigi(kur)
    kanal = kur.kanal
    gurultu = kanal.yayilim.gurultu_w
    ctrl = {m: cerceve_kur(kfg, "kontrol", mesaj_bayt=m) for m in MESAJ_BAYT}
    toplam_bas = sum(b["basarisiz"] for b in r["baglar"])
    gri_bas = gri_kul = 0
    satirlar = []
    for b in r["baglar"]:
        i, j = b["i"], b["j"]
        sinr = kanal.girisim.sinyal_w(j, i, 0.0) / gurultu
        pk = {m: 1.0 - kanal.kahin_per(c, sinr) for m, c in ctrl.items()}
        gri = pk[60] >= 0.8 and b["p_atlama"] < 0.9
        if gri:
            gri_bas += b["basarisiz"]
            gri_kul += b["kullanim"]
        satirlar.append((b["basarisiz"], i, j, b["kullanim"], pk[36], pk[60],
                         b["p_tek"], b["p_atlama"], gri))
    satirlar.sort(reverse=True)
    print(f"=== {r['ad']} {r['kol']} {r['tohum']}  pdr {r['pdr']:.4f}  "
          f"veri basarisizligi {toplam_bas}")
    print(f"  GRI BOLGE (p_kontrol60 >= 0,80 ve p_atlama < 0,90): "
          f"basarisizligin {gri_bas}/{toplam_bas} = {gri_bas / max(toplam_bas, 1):.1%}"
          f" · kullanim {gri_kul}")
    print("   bas   bag       kul  p_k36  p_k60  p_veri p_atlama gri")
    for s in satirlar[:8]:
        print(f"  {s[0]:4d} {s[1]:3d}->{s[2]:<3d} {s[3]:5d}  {s[4]:.3f}  {s[5]:.3f}"
              f"  {s[6]:.3f}  {s[7]:.4f}  {'EVET' if s[8] else ''}")
