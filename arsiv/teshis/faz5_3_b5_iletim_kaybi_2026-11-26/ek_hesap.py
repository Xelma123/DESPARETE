"""
Faz 5-3 · B5 teşhisi — ek sayılar (koşudan SONRA yazıldı; karar girdisi
değil). Kayıtlardan okur; simülasyon yok.

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> > ek_hesap.txt

E1 · kayıp anatomisinin alanıyla iletim kaybı (öngörü 2)
E2 · iki kopya kuralının açık evredeki ateşleme payı ve kapsadığı kaybın
     ağırlıklı payı (öngörü 13; C'nin kazancıyla bedelinin yan yana okunması)
E3 · J2'nin (ağırlıklı, anında) tohum başına 0,02'yi geçtiği tohum sayısı
E4 · kurtarmanın ikizdeki karşılığı: vazgeçen telemetri kararlarında k1
     temizse p₇'si, penceredeki doğuma oranla (genel kazancın üst sınırı;
     fark-içinde-fark için)
E5 · karar sayısının ve kaybın koşu başına aralığı (öngörü 15)
"""

from __future__ import annotations

import statistics as ist
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))

import iletim as L  # noqa: E402
import sonuc_hesap as SH  # noqa: E402


def main() -> None:
    kayit = SH.oku(D)
    rs = kayit["birincil"]

    print("== E1 · kayıp anatomisinin alanıyla iletim kaybı (birincil, açık "
          "doğum) ==")
    pay = {a: [] for a in ("ed", "girisim", "uzak")}
    for r in rs:
        n = r["karistirici_evresi"]["acik"]["dogan"]
        for a in pay:
            pay[a].append(r["dogum_evre_dusen"].get(
                f"iletim_basarisiz|acik|{a}", 0) / n)
    print("  " + " · ".join(f"{a} {ist.mean(v):.4f}" for a, v in pay.items())
          + "\n")

    print("== E2 · kopya kuralları: açık evre kararlarında ateşleme ve "
          "kapsadığı kaybın ağırlıklı payı ==")
    for kural in ("C1", "C2"):
        ates = payda = 0
        kazanc = []
        sinif: Counter = Counter()
        for r in rs:
            kl = SH.kararlar(r)
            n = SH.dogan(r)
            for o in kl:
                if o.evre != "a":
                    continue
                payda += 1
                kanit = bool(o.kanit & L.KANIT_A)
                if kanit and o.k1 >= 0 and (kural == "C1" or o.bO < 0):
                    ates += 1
            w = 0.0
            for o, _ in SH.kayiplar(r, kl):
                kanit = bool(o.kanit & L.KANIT_A)
                if kanit and o.k1 >= 0 and (kural == "C1" or o.bO < 0):
                    s = o.sinif("A")
                    if s != "J1":                  # J1'i katman zaten çözer
                        w += o.p7k1 or 0.0
                        sinif[s] += 1
            kazanc.append(w / n)
        print(f"  {kural} · açık evre kararlarının {SH.yuzde(ates / payda)}'i "
              f"ateşler · J1 dışında kapsadığı kaybın ağırlıklı payı "
              f"{ist.mean(kazanc):.4f} · sınıflar {dict(sorted(sinif.items()))}")
    print()

    print("== E3 · J2 (ağırlıklı, anında) tohum başına ==")
    A = SH.k1_paylar(rs, "A")
    j2 = {t: p["agirlik"]["J2"] for t, p in sorted(A.items())}
    print("  " + " · ".join(f"{t} {v:.4f}" for t, v in j2.items()))
    print(f"  0,02'yi geçen tohum {sum(v >= SH.ELEME for v in j2.values())}/8\n")

    print("== E4 · kurtarmanın ikizdeki karşılığı (genel kazancın üst sınırı) "
          "==")
    for h in ("ikiz", "birincil"):
        v = []
        for r in kayit[h]:
            evre = r["karistirici_evresi"]
            n = sum(evre[e]["dogan"] for e in ("once", "acik", "sessiz"))
            w = 0.0
            for o in SH.kararlar(r):
                if o.ok == 0 and o.k1 >= 0 and L.temiz(o.zk1, o.p7k1):
                    w += o.p7k1
            v.append(w / n)
        print(f"  {h:<9} vazgeçen kararlarda temiz k1'in p₇'si, penceredeki "
              f"doğuma oranla: {ist.mean(v):.4f} (tohum başına "
              f"{' '.join(f'{x:.3f}' for x in v)})")
    print("  (bütün evreler; vazgeçme onayı kaybolmuş ama alıcıya ulaşmış "
          "paketleri de içerir, yani üst sınırdır)\n")

    print("== E5 · koşu başına telemetri kararı ve açık doğumlu kayıp ==")
    for h in ("ikiz", "birincil"):
        k = [len(r["kaydedici"]["karar"]) for r in kayit[h]]
        y = [len(r["kaydedici"]["kayip"]) for r in kayit[h]]
        print(f"  {h:<9} karar {min(k)}–{max(k)} (ortalama {ist.mean(k):.0f})"
              f" · kayıp {min(y)}–{max(y)} (ortalama {ist.mean(y):.0f})")
    print()

    print("== E6 · yayın ekleri saniye cinsinden (koşu başına ortalama, "
          "350 s'lik koşu) ==")
    for h in ("ikiz", "birincil"):
        veri, c1, c2, d = [], [], [], []
        for r in kayit[h]:
            T = r["kaydedici"]["T_veri_s"]
            veri.append(SH.veri_yayin_s(r))
            a1 = a2 = ad = 0.0
            for o in SH.kararlar(r):
                if o.k1 < 0:
                    continue
                kanit = bool(o.kanit & L.KANIT_A)
                kopya = (o.Mk1 + o.Ck1) / L.MALIYET_BIRIM * T
                if kanit:
                    a1 += kopya
                    if o.bO < 0:
                        a2 += kopya
                if o.ok == 0:
                    ad += o.Mk1 / L.MALIYET_BIRIM * T
            c1.append(a1)
            c2.append(a2)
            d.append(ad)
        print(f"  {h:<9} veri yayın süresi {ist.mean(veri):.0f} s · ek: C1 "
              f"{ist.mean(c1):.0f} s · C2 {ist.mean(c2):.1f} s · D "
              f"{ist.mean(d):.0f} s")


if __name__ == "__main__":
    main()
