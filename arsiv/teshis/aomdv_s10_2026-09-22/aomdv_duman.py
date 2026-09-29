import sys, time
from pathlib import Path
KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK)); sys.path.insert(0, str(KOK / "tests2"))
from protokoller.aodv import AODV
from protokoller.aomdv import AOMDV
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import sonuc_satiri
from test_kosum import _konfig

for senaryo, sure in (("statik-yok", 60.0), ("bagimsiz-yok", 60.0)):
    for sinif in (AODV, AOMDV):
        t0 = time.perf_counter()
        kur = kurulum_yap(_konfig(senaryo, 1000, sure))
        kosu = Kosu(kur, sinif)
        kosu.kostur()
        s = sonuc_satiri(kur, kosu.dugumler, "d")
        m, k = s["metrikler"], s["korunum"]
        top = {}
        for d in s["teshis"]["dugum"]:
            for a, v in d.items():
                if isinstance(v, (int, float)):
                    top[a] = top.get(a, 0) + v
        print(senaryo, sinif.__name__, "pdr", round(m["pdr"], 4), "gecerli", k["gecerli"],
              "dusen", k["dusen"], "kontrol", m["kontrol_cerceve"],
              "delta_p50", m.get("rota_kurtarma_delta_p50_s"), f"{time.perf_counter()-t0:.1f}s")
        print("   ", {a: v for a, v in top.items() if a in (
            "rreq_uretilen", "rreq_iletilen", "rreq_yeni_yol", "rrep_uretilen",
            "rrep_iletilen", "rerr_uretilen", "yol_dusen", "yedek_yola_gecis",
            "cevap_siniri", "yol_toplam", "cok_yollu_girdi", "rota_gecerli",
            "kesif_basarili")})
