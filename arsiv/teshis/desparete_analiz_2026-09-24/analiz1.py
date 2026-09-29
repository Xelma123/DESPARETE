# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-162 — DESPARETE v0.2 analizi: kayıp dökümü, bağ kalitesi, alan ve komşu.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_analiz_2026-09-24/analiz1.py
Tam ölçek (N = 40), yere toplama, C, v0.2; 30 s (ısınma 10 · ölçüm 15 ·
boşalma 5),
tohum 1000; dört `-yok` kolu × (DESPARETE, ETX kâhini).

🔒 KÂHİN BİLGİSİ YALNIZ ÖLÇÜMDE. DESPARETE'nin kararları değişmez: alt
sınıf yalnız kararı OKUR ve o anki gerçek bağ kalitesini (`KanalGrafigi`,
girişim hariç, sönümleme dâhil) kaydeder. Bir SONUÇ değil: keşif analizi.
"""
import statistics as ist
import sys
import time
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 25.0, "kosu_bitis_s": 30.0}
KOLLAR = ("statik-yok", "bagimsiz-yok", "gorev-yok", "formasyon-yok")
BANT = ((0.5, "<0,5"), (0.7, "0,5-0,7"), (0.9, "0,7-0,9"), (1.01, ">=0,9"))


def _bant(p):
    for ust, ad in BANT:
        if p < ust:
            return ad
    return ">=0,9"


def kos(is_):
    kol, kahin = is_
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_alan import FORWARDABLE
    from protokoller.desparete_bayrak import PROFIL_V02
    from protokoller.desparete_komsu import ACTIVE
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    kfg = Konfig(kol="u1", senaryo=kol, tohum=1000,
                 trafik_deseni="yere_toplama", **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    grafik = KanalGrafigi(kur)
    g = kfg.gecit
    olcum = {"bag": Counter(), "uyusma": Counter(), "karar": Counter(),
             "alan": Counter(), "komsu_kapsam": [], "komsu_fazla": [],
             "onarim_sure": [], "onarim_sonu": Counter()}
    onarim_bas: dict = {}

    if kahin:
        kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
    else:
        class Olcen(DESPARETE):
            __slots__ = ()

            def sonraki_atlama(self, gozlem):
                k = super().sonraki_atlama(gozlem)
                p = gozlem.paket
                if p is None:
                    return k
                t = kur.olaylar.simdi
                if k.sonraki is not None:
                    olcum["karar"]["ilet"] += 1
                    grafik._tazele(t)
                    etx = grafik._etx[self.kimlik].get(k.sonraki)
                    olcum["bag"][_bant(0.0 if etx is None else 1.0 / etx)] += 1
                    en_iyi = grafik.en_guvenilir_sonraki(self.kimlik, g)
                    olcum["uyusma"]["ayni" if en_iyi == k.sonraki
                                    else "farkli"] += 1
                elif k.beklet:
                    olcum["karar"]["beklet"] += 1
                else:
                    olcum["karar"]["dusur_" + str(self.alanlar.durum(p.hedef))] += 1
                return k

            def zamanlayici_doldu(self, gozlem, etiket):
                sonuc = super().zamanlayici_doldu(gozlem, etiket)
                if etiket == "metrik" and self.kimlik != g:
                    t = kur.olaylar.simdi
                    durum = str(self.alanlar.durum(g))
                    grafik._tazele(t)
                    yol = grafik.en_guvenilir_sonraki(self.kimlik, g) is not None
                    olcum["alan"][(durum, "kahin_yolu_var" if yol
                                   else "kahin_yolu_yok")] += 1
                    kullanilir = set(grafik._komsu[self.kimlik])
                    aktif = set(self.komsular.aktifler())
                    if kullanilir:
                        olcum["komsu_kapsam"].append(
                            len(kullanilir & aktif) / len(kullanilir))
                    if aktif:
                        olcum["komsu_fazla"].append(
                            len(aktif - kullanilir) / len(aktif))
                return sonuc

            def _alan_olaylari(self, t):
                for o, h in self.alanlar.olaylar:
                    if h != g:
                        continue
                    anahtar = self.kimlik
                    if o == "onarim":
                        onarim_bas.setdefault(anahtar, t)
                    elif o in ("iletilebilir", "ulasilamaz") \
                            and anahtar in onarim_bas:
                        olcum["onarim_sure"].append(t - onarim_bas.pop(anahtar))
                        olcum["onarim_sonu"][o] += 1
                return super()._alan_olaylari(t)

        kosu = Kosu(kur, lambda i: Olcen(i, g, bayraklar=PROFIL_V02))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m, kor = satir["metrikler"], satir["korunum"]
    dusen = kor.get("dusen", {})
    uretilen = kor.get("uretilen")
    teslim = round((m["pdr"] or 0) * uretilen)
    cikti = {"pdr": m["pdr"], "uretilen": uretilen, "teslim": teslim,
             "dusen": dusen,
             "yolda": uretilen - teslim - sum(dusen.values()),
             "gecikme_p50_s": m.get("gecikme_p50_s"),
             "gecikme_p95_s": m.get("gecikme_p95_s"),
             "kontrol_veri_airtime": (round(m.get("kontrol_airtime_s") or 0, 1),
                                      round(m.get("veri_airtime_s") or 0, 1))}
    if not kahin:
        kd = satir["teshis"]["kontrol_duzlemi"]
        cikti["cerceve"] = {a: b["cerceve"] for a, b in
                            kd["bicim"]["tum"].items()}
        p = [d.protokol for d in kosu.dugumler]
        cikti["probe_tur"] = {a: sum(q.komsular.sayac[a] for q in p) for a in (
            "probe_nitelik", "probe_hata", "probe_dogrulama", "probe_bosta",
            "yanit_fazla", "yanit_eslesen", "gecis_expired", "gecis_suspect",
            "gecis_stale")}
        cikti["alan_sayac"] = {a: sum(q.alanlar.sayac[a] for q in p) for a in (
            "onarima_girdi", "ulasilamaz", "ardil_degisti", "koruma")}
        cikti["karar"] = dict(olcum["karar"])
        cikti["bag_kalitesi"] = dict(olcum["bag"])
        cikti["kahinle_uyusma"] = dict(olcum["uyusma"])
        cikti["alan_durumu"] = {f"{a}|{b}": v for (a, b), v in
                                sorted(olcum["alan"].items())}
        kk, kf = olcum["komsu_kapsam"], olcum["komsu_fazla"]
        cikti["komsu_kapsam_ort"] = round(ist.mean(kk), 3) if kk else None
        cikti["komsu_fazla_ort"] = round(ist.mean(kf), 3) if kf else None
        s = sorted(olcum["onarim_sure"])
        cikti["onarim"] = {"sayi": len(s), "sonu": dict(olcum["onarim_sonu"]),
                           "p50_s": round(s[len(s) // 2], 2) if s else None,
                           "p90_s": round(s[int(len(s) * 0.9)], 2) if s else None}
    return kol, kahin, cikti, time.perf_counter() - t0


if __name__ == "__main__":
    isler = [(k, h) for k in KOLLAR for h in (False, True)]
    sira = sorted(isler, key=lambda g: (g[0].startswith("statik"), g[1]))
    with Pool(8) as havuz:
        sonuc = havuz.map(kos, sira, chunksize=1)
    for kol, kahin, c, sure in sorted(sonuc, key=lambda r: (KOLLAR.index(r[0]), r[1])):
        print(f"== {kol} · {'kahin' if kahin else 'DESPARETE v0.2'} · {sure:.0f} s",
              flush=True)
        for a, v in c.items():
            print(f"   {a}: {v}")
