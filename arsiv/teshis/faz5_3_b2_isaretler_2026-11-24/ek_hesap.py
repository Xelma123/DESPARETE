"""
B2 teşhisi · kuraldan sonra görülenler (koşudan SONRA yazıldı; karar girdisi
değil). Kayıtlardan okur; simülasyon yok.

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> > ek_hesap.txt

E1 kanal kilidi: E alanındaki düğüm-dönemlerde m'nin dönem başından itibaren
   seyri; ilk m ≥ 0,55 saniyesinin dağılımı; birim başına kapsama.
E2 kendi durumumun birleşimi: kanal kilidi kuralı VEYA girişim kuralı,
   E ve G alanındaki düğüm-dönemlerde.
E3 girişim kuralının işaretleri dönem başında ve cephe hattında sonra: s ve
   c / (dönemden önceki 30 s'nin c ortalaması).
E4 göndericinin iki seçilen kuralının birleşimi (VAZ3 veya DEN7x3).
E5 bitin ulaşması: selam başına ulaşma payından kaba kestirim.
E6 alanın dönem içinde değişmesi (yer–hava görüş hattının açılıp kapanması):
   birimin, dönemin ortasındaki alanında geçirdiği saniyelerin payı; alana
   ilk giriş saniyesi; açık dönemde alan değişimlerinin sıklığı.
E7 alana GİRİŞTEN itibaren gecikme: kanal kilidi kuralı E birimlerinde,
   girişim kuralı G birimlerinde (birim tanımı K1–K2'ninkiyle aynı; yalnız
   gecikmenin başlangıcı dönem başı yerine alana ilk giriş).
E8 (25 Kasım, kanal kilidi kararından sonra eklendi; E1–E7'nin çıktısı
   değişmez) K1'in birimiyle ulaşılabilecek en yüksek erken yakalama: alana
   ilk girişi, dönem başından 3 s içinde karara izin veren E birimlerinin
   payı; yanında ED(0,55)'in K1'in yoluyla hesaplanan erken yakalaması.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))

import isaret as I  # noqa: E402
import sonuc_hesap as SH  # noqa: E402

ED = ("ED", 0.55)                         # K1'in seçtiği
GK = ("G", 0.4, 0.6, 2, 1)                 # K2'nin seçtiği
kayit = SH.oku(D)
hazir = {h: [(r["tohum"], SH.hazirla(r)) for r in rs]
         for h, rs in kayit.items()}


def birimler(h: str, alan: str):
    for tohum, x in hazir[h]:
        for n, q, a, on, off, son in x["birim"]:
            if a == alan:
                yield tohum, x, n, q, on, off, son


def durum_ed(x) -> np.ndarray:
    return np.array(x["m"]) >= ED[1] - 1e-12


def durum_g(x) -> np.ndarray:
    return np.array([I.durum(I.g_isareti(x["m"][n], x["c"][n], x["s"][n],
                                         x["a"][n], x["f"][n], x["k"][n],
                                         GK[1], GK[2], oy=False),
                             GK[3], GK[4]) for n in range(x["N"])],
                    dtype=bool)


print("== E1 · kanal kilidi: E alanındaki düğüm-dönemlerde meşgul payı (m) ==")
for h in ("birincil", "dayaniklilik", "cephe"):
    seri = [[] for _ in range(8)]
    ilk, kapsama = [], []
    for _, x, n, q, on, off, _ in birimler(h, "E"):
        T0 = int(on)
        bitis = min(int(off), x["S"])
        for d in range(8):
            if T0 + d < bitis:
                seri[d].append(x["m"][n][T0 + d])
        ilk.append(next((d for d in range(bitis - T0)
                         if x["m"][n][T0 + d] >= ED[1]), None))
        mm = np.array(x["m"][n][T0:bitis])
        kapsama.append(float((mm >= ED[1]).mean()) if mm.size else None)
    print(f"  {h}: birim {len(ilk)}")
    for d in range(8):
        if seri[d]:
            v = np.array(seri[d])
            print(f"    +{d} s: ortanca {np.median(v):.2f} · çeyrekler "
                  f"{np.quantile(v, .25):.2f}–{np.quantile(v, .75):.2f} · "
                  f"m ≥ 0,55 payı {(v >= ED[1]).mean():.2f} (n {v.size})")
    c = Counter("yok" if k is None else (str(k) if k < 6 else "≥6")
                for k in ilk)
    print("    ilk m ≥ 0,55 saniyesi (dönem başından): " + " · ".join(
        f"{k}: {c[k]}" for k in ("0", "1", "2", "3", "4", "5", "≥6", "yok")
        if c[k]))
    kp = np.array([k for k in kapsama if k is not None])
    print(f"    birim başına kapsama (dönemin m ≥ 0,55 saniyelerinin payı): "
          f"< 0,2: {(kp < 0.2).sum()} · 0,2–0,8: "
          f"{((kp >= 0.2) & (kp < 0.8)).sum()} · ≥ 0,8: {(kp >= 0.8).sum()}")
print()

print("== E2 · kendi durumumun birleşimi: kanal kilidi VEYA girişim kuralı ==")
for h in ("birincil", "dayaniklilik", "cephe"):
    for alan in ("E", "G"):
        sonuc = {"ED": [], "G": [], "ED|G": []}
        for _, x in hazir[h]:
            de, dg = durum_ed(x), durum_g(x)
            for n, q, a, on, off, son in x["birim"]:
                if a != alan:
                    continue
                for ad, dur in (("ED", de), ("G", dg), ("ED|G", de | dg)):
                    sonuc[ad].append(I.donem_olcusu(list(dur[n]), on, off,
                                                    son)[0])
        parca = []
        for ad, gl in sonuc.items():
            if gl:
                erken = sum(g is not None and g <= SH.ERKEN_S for g in gl)
                ici = sum(g is not None for g in gl)
                parca.append(f"{ad} erken {erken / len(gl):.3f} · dönem içinde "
                             f"{ici / len(gl):.3f}")
        if parca:
            print(f"  {h:<13} {alan} (n {len(sonuc['ED'])}): " + " | ".join(parca))
print()

print("== E3 · girişim kuralının işaretleri G alanındaki düğüm-dönemlerde ==")
print("  saniye · ortanca s · ortanca c / (dönemden önceki 30 s'nin c ortalaması)")
for h, anlar in (("birincil", (0, 1, 2, 3, 5)), ("dayaniklilik", (0, 1, 2, 3, 5)),
                 ("cephe", (0, 1, 2, 3, 5, 10, 20, 40, 80, 160))):
    print(f"  {h}")
    for d in anlar:
        sv, cv = [], []
        for _, x, n, q, on, off, _ in birimler(h, "G"):
            T = int(on) + d
            if T >= min(int(off), x["S"]):
                continue
            onceki = x["c"][n][max(0, int(on) - 30):int(on)]
            taban = sum(onceki) / len(onceki) if onceki else None
            if x["s"][n][T] is not None:
                sv.append(x["s"][n][T])
            if taban:
                cv.append(x["c"][n][T] / taban)
        if sv and cv:
            print(f"    +{d:>3} s: s {np.median(sv):.2f} · c oranı "
                  f"{np.median(cv):.2f} (n {len(cv)})")
print()

print("== E4 · göndericinin birleşik kuralı: VAZ3 veya DEN7x3 (bütün tohumlar) ==")
k0 = kayit["ikiz"][0]["kaydedici"]
adlar = k0["kural_veri"] + k0["kural_ses"]
iv, id_ = adlar.index("VAZ3"), adlar.index("DEN7x3")
fa = {}
for ad in ("VAZ3", "DEN7x3"):
    o = SH.bag_olcu(kayit["ikiz"], ad, "E")
    fa[ad] = o["fa_ikiz"]
print(f"  ikizde yanlış alarm: VAZ3 {fa['VAZ3']:.2f}‰ · DEN7x3 {fa['DEN7x3']:.2f}‰"
      f" · birleşimin üst sınırı {fa['VAZ3'] + fa['DEN7x3']:.2f}‰")
for alan in ("E", "G"):
    for h in ("birincil", "dayaniklilik"):
        g = []
        for r in kayit[h]:
            for u in r["kaydedici"]["veri_birim"]:
                if u[0] != alan:
                    continue
                a, b = u[3 + iv], u[3 + id_]
                g.append(min(x for x in (a, b) if x is not None)
                         if (a is not None or b is not None) else None)
        if g:
            erken = sum(x is not None and x <= SH.ERKEN_S for x in g) / len(g)
            ici = sum(x is not None for x in g) / len(g)
            print(f"  {alan} · {h:<13} erken {erken:.3f} · dönem içinde "
                  f"{ici:.3f} (n {len(g)})")
print()

print("== E5 · bitin ulaşması: selam başına ulaşma payından kaba kestirim ==")
print("  (selamlar bağımsız sayılırsa) bir uzak komşuya n selamdan en az birinin "
      "ulaşma olasılığı")
for h in ("birincil", "dayaniklilik", "cephe"):
    b = [0, 0]
    for r in kayit[h]:
        u = r["kaydedici"]["bit"]["U"]
        b[0] += u[0]
        b[1] += u[1]
    p = b[1] / b[0]
    print(f"  {h:<13} p {p:.3f} · n=1 {p:.2f} · n=2 {1 - (1 - p) ** 2:.2f} · "
          f"n=3 {1 - (1 - p) ** 3:.2f} · n=5 {1 - (1 - p) ** 5:.2f}")
print()

print("== E6 · alanın dönem içinde değişmesi (yer–hava görüş hattı) ==")
KOD = {"U": SH.SINIF["uzak"], "G": SH.SINIF["G"], "E": SH.SINIF["E"]}
for h in ("birincil", "dayaniklilik", "cephe"):
    for alan in ("E", "G"):
        pay, ilk = [], []
        for _, x, n, q, on, off, _ in birimler(h, alan):
            T0, T1 = int(on), min(int(off), x["S"])
            kd = x["kod"][n][T0:T1]
            if kd.size == 0:
                continue
            pay.append(float((kd == KOD[alan]).mean()))
            ilk.append(next((d for d in range(kd.size) if kd[d] == KOD[alan]),
                            None))
        if not pay:
            continue
        p = np.array(pay)
        c = Counter("yok" if d is None else (str(d) if d < 4 else
                                             ("4–6" if d < 7 else "≥7"))
                    for d in ilk)
        print(f"  {h:<13} {alan} (n {len(pay)}): dönemin bu alanda geçen payı "
              f"ortanca {np.median(p):.2f} · tamamı bu alanda {(p == 1.0).mean():.2f}"
              f" · alana ilk giriş (dönem başından, s): " + " · ".join(
                  f"{k}: {c[k]}" for k in ("0", "1", "2", "3", "4–6", "≥7",
                                           "yok") if c[k]))
    gecis = toplam = 0
    for _, x in hazir[h]:
        kod = x["kod"]
        acik = (kod >= KOD["U"])
        ayni = acik[:, 1:] & acik[:, :-1]
        gecis += int(((kod[:, 1:] != kod[:, :-1]) & ayni).sum())
        toplam += int(ayni.sum())
    print(f"  {h:<13} açık dönemde ardışık iki saniye arasında alan değişimi: "
          f"{gecis} / {toplam} ({100 * gecis / toplam:.2f}%)")
print()

print("== E7 · alana GİRİŞTEN itibaren gecikme ==")
for h in ("birincil", "dayaniklilik", "cephe"):
    for alan, ad in (("E", "kanal kilidi ED(0,55)"), ("G", "girişim G")):
        gec = []
        for _, x in hazir[h]:
            dur = durum_ed(x) if alan == "E" else durum_g(x)
            for n, q, a, on, off, son in x["birim"]:
                if a != alan:
                    continue
                T0, T1 = int(on), min(int(off), x["S"])
                kd = x["kod"][n][T0:T1]
                giris = next((T0 + d for d in range(kd.size)
                              if kd[d] == KOD[alan]), None)
                if giris is None:
                    continue
                T = next((T for T in range(giris, T1) if dur[n][T]), None)
                gec.append(None if T is None else T + 1 - giris)
        if gec:
            var = [g for g in gec if g is not None]
            print(f"  {h:<13} {ad:<22} birim {len(gec)} · girişten 3 s içinde "
                  f"{sum(g <= SH.ERKEN_S for g in var) / len(gec):.3f} · dönem "
                  f"içinde {len(var) / len(gec):.3f} · gecikme ortancası "
                  f"{(np.median(var) if var else float('nan')):.1f} s")
print()

print("== E8 · K1'in birimiyle ulaşılabilecek en yüksek erken yakalama ==")
print("  birim K1'inki: dönemin ortasında E alanında olan düğüm-dönem; gecikme "
      "dönem başından, karar saniye sonunda")
print("  tavan: alana ilk giriş saniyesinin sonu dönem başından en çok 3 s sonra "
      "olan birimlerin payı. Alan saniyenin ortasında okunur;")
print("  kural geçiş saniyesinde alan etiketinden önce de ateşlenebilir, tavan "
      "bu yüzden yaklaşıktır")
for yari_ad, tohumlar in (("seçim", SH.SECIM), ("doğrulama", SH.DOGRULAMA)):
    for hucreler in (("birincil",), ("dayaniklilik",), SH.KARISTIRMA):
        say = tavan = erken = 0
        for h in hucreler:
            for tohum, x in hazir[h]:
                if tohum not in tohumlar:
                    continue
                dur = durum_ed(x)
                for n, q, alan, on, off, son in x["birim"]:
                    if alan != "E":
                        continue
                    say += 1
                    T0, T1 = int(on), min(int(off), x["S"])
                    kd = x["kod"][n][T0:T1]
                    giris = next((T0 + d for d in range(kd.size)
                                  if kd[d] == KOD["E"]), None)
                    if giris is not None and giris + 1 - on <= SH.ERKEN_S + 1e-9:
                        tavan += 1
                    g = I.donem_olcusu(list(dur[n]), on, off, son)[0]
                    if g is not None and g <= SH.ERKEN_S:
                        erken += 1
        if say:
            print(f"  {yari_ad:<9} {' + '.join(hucreler):<23} birim {say:>3} · "
                  f"tavan {tavan / say:.3f} ({tavan}/{say}) · ED(0,55) erken "
                  f"{erken / say:.3f} ({erken}/{say})")
