# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
import sys, time
sys.path.insert(0, "."); sys.path.insert(0, "tests2")
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.kosu import Kosu
from sim2.kosum.sonuc import sonuc_satiri
from protokoller.desparete import DESPARETE
from test_kosum import _konfig

senaryo = sys.argv[1] if len(sys.argv) > 1 else "statik-yok"
bitis = float(sys.argv[2]) if len(sys.argv) > 2 else 12.0
t0 = time.perf_counter()
kfg = _konfig(senaryo, 1000, bitis, trafik_deseni="yere_toplama")
kur = kurulum_yap(kfg)
kosu = Kosu(kur, lambda i: DESPARETE(i, sink=kfg.gecit))
kosu.kostur()
satir = sonuc_satiri(kur, kosu.dugumler, "desparete")
print(f"senaryo {senaryo} · {bitis} s · süre {time.perf_counter()-t0:.1f} s · gecit {kfg.gecit}")
print("korunum gecerli:", satir["korunum"]["gecerli"])
kd = satir["teshis"].get("kontrol_duzlemi", {})
print("tepe bekleyen uyandirma:", kd.get("tepe_bekleyen_uyandirma"))
print("bicim dökümü (tum):", {a: v["cerceve"] for a, v in kd["bicim"]["tum"].items()})
m = satir["metrikler"]
print("pdr:", m.get("pdr"), "· teslim:", m.get("teslim_paket"), "· kontrol_cerceve:", m.get("kontrol_cerceve"))
for n, d in enumerate(kosu.dugumler):
    p = d.protokol; T = p.teshis(n)
    kom = {j: p.komsular.durum(j)[0] for j in sorted(p.komsular._kayit)}
    print(f"{n:>2} ilan_al {T['ilan_alinan']:>3} kayit {T['komsu_kayit']} act {T['komsu_active']} "
          f"pn {T['probe_nitelik']:>2} pb {T['probe_bosta']:>2} ph {T['probe_hata']} "
          f"→A {T['gecis_active']:>2} →S {T['gecis_stale']} →Su {T['gecis_suspect']} →E {T['gecis_expired']} "
          f"hiz {T['aday_hiz_siniri']} kom {kom}")
s = kosu.dugumler[0].protokol.komsular
print("geçidin komşu ölçümleri (Q,H,U,R,C,N_Q):")
for j in s.aktifler():
    o = s.kayit(j).son_olcum
    print(f"  {j:>2}: {o.q},{o.h},{o.u},{o.r},{o.c},{o.n_q}")
