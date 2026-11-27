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
     fark-içinde-fark için). Düzeltme (27 Kasım): ilk hesap pencerenin
     dışındaki (0–50 s) kararları da sayıyordu, payda ise yalnız penceredeki
     doğumdu; iki sayı yan yana yazılır, geçerli olan pencere içindekidir.
E5 · karar sayısının ve kaybın koşu başına aralığı (öngörü 15)

Ana seçeneğin kararı için eklenenler (27 Kasım; yine kuraldan sonra):
E7 · J1'de ardılın kanıtının kaynağı: yalnız karıştırma katmanının kanıtı
     (bildirim, gönderici) mı, çekirdeğin bir kanıtı da (veri yok, ilan
     bayat, kullanılmaz) var mı. Katman kapatılınca (mekanizma kapısının
     kolu) çekirdeğin kanıtı kalır; katmanın kendine ait payı birincisidir.
E8 · K6'nın temiz engelli komşusu, ardılın durumuna göre: hangi kayıplarda
     "ardıl S'de, olağan aday yok" durumu bir tur isteğini tetikleyebilirdi
     (RFC 8966 §3.8.2.2'nin ikinci paragrafı, B4'te yok); hangisinde B4
     kural 11 zaten ister (açlık); hangisinde ardılın kanıtı yok.
E9 · temiz kararlarda ardılın ilanının bayatlığı: o kararlarda ardıla
     giden çerçevenin onay payı, ardılın bağının bandı, ardıldan başka aday
     olup olmadığı (`ILAN_OMUR_KAT`'ın girdisi).
E10 · J3 ve J4, alıcının alanına ve ardılın kanıtına göre (B5 kâğıdının
     son çaredeki ardıl için bekletme sorusu; 27 Kasım).
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
        v, v_hepsi = [], []
        for r in kayit[h]:
            evre = r["karistirici_evresi"]
            n = sum(evre[e]["dogan"] for e in ("once", "acik", "sessiz"))
            lo, hi = r["kaydedici"]["pencere"]
            w = w_hepsi = 0.0
            for o in SH.kararlar(r):
                if o.ok == 0 and o.k1 >= 0 and L.temiz(o.zk1, o.p7k1):
                    w_hepsi += o.p7k1
                    if lo <= o.t < hi:
                        w += o.p7k1
            v.append(w / n)
            v_hepsi.append(w_hepsi / n)
        print(f"  {h:<9} vazgeçen kararlarda temiz k1'in p₇'si, penceredeki "
              f"doğuma oranla: {ist.mean(v):.4f} (tohum başına "
              f"{' '.join(f'{x:.3f}' for x in v)}) · ilk hesap, pencere "
              f"dışındaki kararlarla: {ist.mean(v_hepsi):.4f}")
    print("  (pencere içindeki kararlar, bütün evreler; vazgeçme onayı "
          "kaybolmuş ama alıcıya ulaşmış paketleri de içerir, yani üst "
          "sınırdır)\n")

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
    print()

    e7(rs)
    e8(rs)
    e9(kayit)
    print()
    e10(rs)


KATMAN = L.K_BILDIRIM_A | L.K_GONDERICI
CEKIRDEK = L.K_VERI_YOK | L.K_ILAN_BAYAT | L.K_KULLANILMAZ
ADAY_DISI = L.K_ILAN_BAYAT | L.K_KULLANILMAZ


def e7(rs: list[dict]) -> None:
    print("== E7 · J1'de ardılın kanıtının kaynağı (birincil; ağırlıklı, açık "
          "doğana oranla) ==")
    adlar = ("yalnız katman (bildirim, gönderici)", "çekirdeğin kanıtı da var",
             "  veri yok", "  ilan bayat", "  kullanılmaz", "J1 toplamı")
    pay: dict[str, list] = {a: [] for a in adlar}
    for r in rs:
        n = SH.dogan(r)
        kl = SH.kararlar(r)
        a = dict.fromkeys(adlar, 0.0)
        for o, _ in SH.kayiplar(r, kl):
            if o.sinif("A") != "J1":
                continue
            w = o.agirlik("J1")
            a["J1 toplamı"] += w
            if o.kanit & CEKIRDEK:
                a["çekirdeğin kanıtı da var"] += w
                for ad, b in (("  veri yok", L.K_VERI_YOK),
                              ("  ilan bayat", L.K_ILAN_BAYAT),
                              ("  kullanılmaz", L.K_KULLANILMAZ)):
                    if o.kanit & b:
                        a[ad] += w
            elif o.kanit & KATMAN:
                a["yalnız katman (bildirim, gönderici)"] += w
        for ad in adlar:
            pay[ad].append(a[ad] / n)
    for ad in adlar:
        v = pay[ad]
        print(f"  {ad:<38} {ist.mean(v):.4f} (tohum başına "
              f"{' '.join(f'{x:.3f}' for x in v)})")
    print("  (çekirdeğin alt satırları örtüşebilir: bir karar birden çok "
          "sebep taşıyabilir)\n")


def e8(rs: list[dict]) -> None:
    print("== E8 · K6'nın temiz engelli komşusu, ardılın durumuna göre "
          "(birincil; p₇ ile ağırlıklı, açık doğana oranla) ==")
    adlar = ("a1 · ardıl aday dışı, başka aday yok: açlık, B4 kural 11 ister",
             "a2 · ardılın kanıtı var, olağan aday yok: yeni kural ister",
             "     bunun yalnız katman kanıtlı kısmı",
             "b  · ardılın kanıtı var, olağan aday var (k1 kirli)",
             "c  · ardılın kanıtı yok")
    for s in ("J3", "J4", "U2"):
        pay: dict[str, list] = {a: [] for a in adlar}
        for r in rs:
            n = SH.dogan(r)
            kl = SH.kararlar(r)
            a = dict.fromkeys(adlar, 0.0)
            for o, _ in SH.kayiplar(r, kl):
                if o.sinif("A") != s:
                    continue
                if not (o.uK >= 0 and L.temiz(o.zuK, o.p7uK)):
                    continue
                w = o.p7uK
                if not o.kanit & L.KANIT_A:
                    a[adlar[4]] += w
                elif o.k1 >= 0 and o.k1_O == 1:
                    a[adlar[3]] += w
                elif o.kanit & ADAY_DISI and o.k1 < 0:
                    a[adlar[0]] += w
                else:
                    a[adlar[1]] += w
                    if o.kanit & KATMAN and not o.kanit & CEKIRDEK:
                        a[adlar[2]] += w
            for ad in adlar:
                pay[ad].append(a[ad] / n)
        print(f"  {s}")
        for ad in adlar:
            print(f"    {ad:<66} {ist.mean(pay[ad]):.4f}")
    print()


def e9(kayit: dict) -> None:
    print("== E9 · temiz kararlarda ardılın ilanının bayatlığı (pencere içi) "
          "==")
    for h, rs in kayit.items():
        g: dict[str, list] = {}
        for r in rs:
            lo, hi = r["kaydedici"]["pencere"]
            for o in SH.kararlar(r):
                if not o.temiz_karar() or not lo <= o.t < hi:
                    continue
                m = o.kanit & L.KANIT_A
                ad = ("kanıt yok" if not m else "yalnız ilan bayat"
                      if m == L.K_ILAN_BAYAT else "öteki kanıtlar")
                x = g.setdefault(ad, [0, 0, 0, 0])
                x[0] += 1
                x[1] += o.ok == 1
                x[2] += o.p7j >= 0.90
                x[3] += o.k1 < 0
        for ad in ("kanıt yok", "yalnız ilan bayat", "öteki kanıtlar"):
            n, ok, iyi, tek = g[ad]
            print(f"  {h:<9} {ad:<18} karar {n:>7} · ardıla giden çerçevenin "
                  f"onayı {SH.yuzde(ok / n)} · ardılın bağı iyi bantta "
                  f"{SH.yuzde(iyi / n)} · ardıldan başka aday yok "
                  f"{SH.yuzde(tek / n)}")


def e10(rs: list[dict]) -> None:
    print("== E10 · J3 ve J4, alıcının alanına ve ardılın kanıtına göre "
          "(birincil; ham, açık doğana oranla) ==")
    for s in ("J3", "J4"):
        pay: dict[tuple, list] = {}
        for x, r in enumerate(rs):
            n = SH.dogan(r)
            kl = SH.kararlar(r)
            a: dict[tuple, int] = {}
            for o, _ in SH.kayiplar(r, kl):
                if o.sinif("A") != s:
                    continue
                if not o.kanit & L.KANIT_A:
                    k = "kanıt yok"
                elif o.kanit & L.K_BILDIRIM_A:
                    k = "kanıt var, bildirim de"
                else:
                    k = "kanıt var, bildirimsiz"
                a[(o.zj, k)] = a.get((o.zj, k), 0) + 1
            for anahtar in set(pay) | set(a):
                pay.setdefault(anahtar, [0.0] * x).append(a.get(anahtar, 0) / n)
        print(f"  {s}")
        for alan_ in ("E", "G"):
            toplam = 0.0
            for k in ("kanıt var, bildirim de", "kanıt var, bildirimsiz",
                      "kanıt yok"):
                v = pay.get((alan_, k), [0.0] * len(rs))
                v = v + [0.0] * (len(rs) - len(v))
                toplam += ist.mean(v)
                print(f"    {alan_} · {k:<24} {ist.mean(v):.4f}")
            print(f"    {alan_} · toplam                   {toplam:.4f}")
    print("  (bildirim anında biçimdedir: kanal kilidindeki alıcı gerçekte "
          "selam gönderemez)")


if __name__ == "__main__":
    main()
