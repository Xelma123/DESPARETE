"""
Faz 5-3 · B5 teşhisinin karar hesabı (`beklenti.md` "Karar kuralı", K0–K5).
Kayıtlardan okur; simülasyon yok.

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> [<klasör>] > sonuc_hesap.txt

<klasör> verilmezse bu dosyanın dizini (`kayit_<hücre>.json.gz`).
  · `duman/`: kısa pencere, tek tohum; yarılar yoktur, hüküm verilmez; K0
    duman kaydıyla karşılaştırılır, öteki bölümler betimlenir.
  · `mekanik/`: mekanik denetim (`beklenti.md` "Aletin denetimi"); yalnız
    K0'ın iç denetimleri ve bölümlerin hatasız hesaplandığı yazılır, hiçbir
    sayı basılmaz.
"""

from __future__ import annotations

import gzip
import json
import statistics as ist
import sys
from collections import Counter, defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))

import iletim as L  # noqa: E402

HUCRELER = ("ikiz", "birincil")
SECIM = (1003, 1004, 1005, 1006)
DOGRULAMA = (1007, 1008, 1009, 1010)
YENI = D.parent / "faz5_3_yeni_cekirdek_2026-11-19"
# --- karar kuralının eşikleri (`beklenti.md`) -----------------------------------
ELEME = 0.02                  # ağırlıklı pay, `PDR_açık` birimi
TEMIZ_SAPMA = 0.02            # temiz kararların sapma payı
GEREKEN = 0.048               # hedefe (~0,713) eksik (`eğim0` 0,665)
ERKEN_S = 3.0
SINIFLAR = ("J1", "J2", "J3", "J4", "J5", "U1", "U2")
ALANLAR = ("pdr", "pdr_pencere", "uretilen", "teslim", "sayaclar",
           "teshis_toplam")


def oku(klasor: Path) -> dict[str, list]:
    kayit: dict[str, list] = {}
    for h in HUCRELER:
        yol = klasor / f"kayit_{h}.json.gz"
        if yol.exists():
            with gzip.open(yol, "rt", encoding="utf-8") as f:
                k = json.load(f)
            kayit[h] = [r for r in k["sonuc"] if "hata" not in r]
    return kayit


def fmt(x, ondalik=3) -> str:
    return "—" if x is None else f"{x:.{ondalik}f}"


def yuzde(x) -> str:
    return "—" if x is None else f"%{100.0 * x:.2f}"


def ceyrek(x: list[float]) -> str:
    if not x:
        return "—"
    if len(x) == 1:
        return f"{x[0]:.2f}"
    q = ist.quantiles(x, n=4, method="inclusive")
    return f"{q[1]:.2f} ({q[0]:.2f}–{q[2]:.2f})"


def bant(p7: float) -> int:
    """Kayıp anatomisinin bantları: 0 iyi · 1 orta · 2 kötü."""
    return 0 if p7 >= 0.90 else (1 if p7 >= 0.50 else 2)


# ==============================================================================
# Karar satırı ve sınıf
# ==============================================================================
class Karar:
    __slots__ = ("t", "i", "j", "evre", "zj", "gecit", "kanit", "k1", "k1_O",
                 "zk1", "p7k1", "Mk1", "Ck1", "bO", "zbO", "p7bO", "p7j",
                 "tetik", "den", "ok", "kayip", "Mj")

    @classmethod
    def kur(cls, satir: list, alanlar: list) -> "Karar":
        o = cls()
        d = dict(zip(alanlar, satir))
        o.t = d["t_ms"] / 1000.0
        o.i, o.j, o.evre, o.zj = d["i"], d["j"], d["evre"], d["zj"]
        o.gecit, o.kanit = bool(d["j_gecit"]), d["kanit"]
        o.k1, o.k1_O, o.zk1 = d["k1"], d["k1_O"], d["zk1"]
        o.p7k1 = None if d["p7k1"] < 0 else d["p7k1"] / 1000.0
        o.Mk1, o.Ck1 = d["Mk1"], d["Ck1"]
        o.bO, o.zbO = d["bO"], d["zbO"]
        o.p7bO = None if d["p7bO"] < 0 else d["p7bO"] / 1000.0
        o.p7j = d["p7j"] / 1000.0
        o.tetik, o.den, o.ok = d["tetik"], d["den"], d["ok"]
        o.kayip, o.Mj = bool(d["kayip"]), d["Mj"]
        return o

    def sinif(self, bicim: str) -> str:
        maske = L.KANIT_A if bicim == "A" else L.KANIT_G
        return L.sinif(self.zj in "EG", self.gecit, bool(self.kanit & maske),
                       self.k1 >= 0, L.temiz(self.zk1, self.p7k1),
                       self.bO >= 0 and L.temiz(self.zbO, self.p7bO))

    def agirlik(self, sinif: str) -> float:
        if sinif == "J1":
            return self.p7bO or 0.0
        return self.p7k1 if self.k1 >= 0 else 0.0

    def temiz_karar(self) -> bool:
        """Temiz karar (K3): ikiz; birincilde önce ve sessiz; açıkta alıcı U."""
        return self.evre in "ios" or (self.evre == "a" and self.zj == "U")


def kararlar(r: dict) -> list[Karar]:
    kd = r["kaydedici"]
    return [Karar.kur(s, kd["karar_alanlar"]) for s in kd["karar"]]


def kayiplar(r: dict, kl: list[Karar]) -> list[tuple[Karar, list]]:
    kd = r["kaydedici"]
    return [(kl[x[0]], x) for x in kd["kayip"]]


def dogan(r: dict) -> int:
    d = r["kaydedici"]["dogan_acik"]
    return d["telemetri"] + d["komut"]


def veri_yayin_s(r: dict) -> float:
    s = r["sayaclar"]
    return float(s.get("veri_airtime_s", 0.0)) + float(
        s.get("veri_baslik_airtime_s", 0.0))


# ==============================================================================
# K0 · geçerlilik
# ==============================================================================
def k0(kayit: dict, kip: str) -> bool:
    print("== K0 · geçerlilik ==")
    tamam = True
    for h, rs in kayit.items():
        gecersiz = [r["tohum"] for r in rs if not r["gecerli"]]
        denetim = [(r["tohum"], r["kaydedici_denetim"]) for r in rs
                   if r["kaydedici_denetim"]]
        if kip == "mekanik":
            print(f"  {h:<9} geçersiz koşu {'yok' if not gecersiz else 'VAR'}"
                  f" · iç denetim {'tamam' if not denetim else denetim}")
        else:
            print(f"  {h:<9} koşu {len(rs)} · geçersiz {gecersiz or 'yok'} · "
                  f"iç denetim {denetim or 'tamam'}")
        tamam &= not gecersiz and not denetim
    if kip == "mekanik":
        print("  birebirlik: mekanik denetimde karşılaştırma yok")
    else:
        for h in kayit:
            yol = (YENI / "duman" / f"kayit_duman_{h}.json" if kip == "duman"
                   else YENI / f"kayit_egim0_{h}.json")
            if not yol.exists():
                print(f"  birebirlik {h}: karşılaştırma dosyası yok ({yol})")
                tamam = False
                continue
            k = json.loads(yol.read_text(encoding="utf-8"))
            ote = {r["tohum"]: r for r in k["sonuc"]
                   if "hata" not in r and r.get("kol") == "egim0"}
            farkli, eslesen = [], 0
            for r in kayit[h]:
                o = ote.get(r["tohum"])
                if o is None:
                    continue
                eslesen += 1
                f = [x for x in ALANLAR if r.get(x) != o.get(x)]
                if f:
                    farkli.append((r["tohum"], f))
            print(f"  birebirlik {h:<9} ↔ {yol.relative_to(D.parent)}: "
                  f"{eslesen} eşleşen · "
                  f"{'birebir' if eslesen and not farkli else farkli}")
            tamam &= eslesen > 0 and not farkli
    print(f"  hüküm: {'geçerli' if tamam else 'GEÇERSİZ — tablolar kullanılmaz'}"
          "\n")
    return tamam


# ==============================================================================
# K1 · kaybın yeri (S1)
# ==============================================================================
def k1_paylar(rs: list[dict], bicim: str) -> dict[int, dict]:
    """tohum → {"ham": {sınıf: pay}, "agirlik": {...}, "komut": pay, "dogan": n}."""
    out: dict[int, dict] = {}
    for r in rs:
        kl = kararlar(r)
        n = dogan(r)
        ham: Counter = Counter()
        agr: defaultdict = defaultdict(float)
        for o, _ in kayiplar(r, kl):
            s = o.sinif(bicim)
            ham[s] += 1
            agr[s] += o.agirlik(s)
        komut = sum(r["kaydedici"]["komut_kayip"].values())
        out[r["tohum"]] = {
            "ham": {s: ham[s] / n for s in SINIFLAR},
            "agirlik": {s: agr[s] / n for s in SINIFLAR},
            "komut": komut / n, "dogan": n}
    return out


def ort(paylar: dict[int, dict], tur: str, sinif: str) -> float:
    return ist.mean(p[tur][sinif] for p in paylar.values())


def k1(kayit: dict, kip: str) -> dict | None:
    print("== K1 · kaybın yeri (S1): açık dönemde doğan paketlerin iletim "
          "kaybı, karar anına göre ==")
    rs = kayit.get("birincil", [])
    if not rs:
        print("  birincil kaydı yok\n")
        return None
    A = k1_paylar(rs, "A")
    G = k1_paylar(rs, "G")
    if kip == "mekanik":
        print("  K1 · hesaplandı\n")
        return None
    print("  sınıf · ham · ağırlıklı (anında biçim) · ham (gerçekçi biçim) · "
          "tohum başına ağırlıklı (anında)")
    for s in SINIFLAR:
        tb = " ".join(f"{A[t]['agirlik'][s]:.3f}" for t in sorted(A))
        print(f"    {s} · {ort(A, 'ham', s):.4f} · {ort(A, 'agirlik', s):.4f}"
              f" · {ort(G, 'ham', s):.4f} · {tb}")
    komut = ist.mean(p["komut"] for p in A.values())
    toplam = sum(ort(A, "ham", s) for s in SINIFLAR) + komut
    print(f"    komut kaybı · {komut:.4f}")
    print(f"    toplam (iletim kaybı, telemetri + komut) · {toplam:.4f}")
    anat = ist.mean(sum(v for k_, v in r["dogum_evre_dusen"].items()
                        if k_.startswith("iletim_basarisiz|acik|"))
                    / r["karistirici_evresi"]["acik"]["dogan"] for r in rs)
    print(f"    kayıp anatomisinin iletim kaybı · {anat:.4f}")
    j2 = ort(A, "agirlik", "J2")
    j3 = ort(A, "agirlik", "J3")
    u1 = ort(A, "agirlik", "U1")
    j1 = ort(A, "agirlik", "J1")
    elendi = {"B": j2 < ELEME, "C": j3 < ELEME, "D": j2 + j3 + u1 < ELEME}
    if kip == "duman":
        print("  duman: elemeler ve hüküm verilmez\n")
        return {"elendi": elendi}
    print(f"  elemeler (ağırlıklı, anında; eşik {ELEME}):")
    print(f"    B · J2 = {j2:.4f} → {'ELENİR' if elendi['B'] else 'elenmez'}")
    print(f"    C · J3 = {j3:.4f} → {'ELENİR' if elendi['C'] else 'elenmez'}")
    print(f"    D · J2 + J3 + U1 = {j2 + j3 + u1:.4f} → "
          f"{'ELENİR' if elendi['D'] else 'elenmez'}")
    kalan = ["A"] + [a for a in "BCD" if not elendi[a]]
    print(f"  hüküm K1: elenmeyen aileler {' · '.join(kalan)}")
    y = j1 + j2 + j3
    print(f"  hedefe yeter mi (betimleyici): J1 + J2 + J3 (ağırlıklı) = "
          f"{y:.4f} ↔ gereken {GEREKEN}\n")
    return {"elendi": elendi}


# ==============================================================================
# K2 · zaman (S2)
# ==============================================================================
def k2(kayit: dict, kip: str) -> None:
    print("== K2 · zaman (S2): J1 + J2'deki kayıp (anında biçim), saniye ==")
    rs = kayit.get("birincil", [])
    don, alan, kanit, erken, n = [], [], [], 0, 0
    for r in rs:
        kl = kararlar(r)
        for o, x in kayiplar(r, kl):
            s = o.sinif("A")
            if s not in ("J1", "J2"):
                continue
            n += 1
            _, dq, dt_d, dt_a, dt_kA, _, _, _ = x
            if dt_d >= 0:
                don.append(dt_d / 1000.0)
                erken += dt_d / 1000.0 <= ERKEN_S
            if dt_a >= 0:
                alan.append(dt_a / 1000.0)
            if s == "J1" and dt_kA >= 0:
                kanit.append(dt_kA / 1000.0)
    if kip == "mekanik":
        print("  K2 · hesaplandı\n")
        return
    print(f"  kayıp {n} · dönem başından {ceyrek(don)} · alana girişten "
          f"{ceyrek(alan)} · J1'de kanıttan {ceyrek(kanit)}")
    print(f"  dönemin ilk {ERKEN_S:g} s'sinde olan pay "
          f"{yuzde(erken / len(don) if don else None)}\n")


# ==============================================================================
# K3 · hızlı sapmanın tetiği (S3)
# ==============================================================================
def k3_say(kayit: dict, tohumlar: tuple) -> list[dict]:
    """Aday başına yakalama (J2, ağırlıklı) ve temiz sapma (iki hücre)."""
    adaylar = [{"yak_pay": 0.0, "yak_payda": 0.0, "temiz": 0, "temiz_payda": 0,
                "kotu_k1": 0} for _ in L.SAPMA_ADAYLARI]
    for h, rs in kayit.items():
        for r in rs:
            if r["tohum"] not in tohumlar:
                continue
            kl = kararlar(r)
            if h == "birincil":
                for o, _ in kayiplar(r, kl):
                    if o.sinif("A") != "J2":
                        continue
                    w = o.agirlik("J2")
                    for v, a in enumerate(adaylar):
                        a["yak_payda"] += w
                        if o.tetik >> v & 1:
                            a["yak_pay"] += w
            for o in kl:
                if not o.temiz_karar():
                    continue
                for v, a in enumerate(adaylar):
                    a["temiz_payda"] += 1
                    if o.tetik >> v & 1 and o.k1 >= 0:
                        a["temiz"] += 1
                        if bant(o.p7k1) > bant(o.p7j):
                            a["kotu_k1"] += 1
    for a in adaylar:
        a["yakalama"] = (a["yak_pay"] / a["yak_payda"] if a["yak_payda"]
                         else None)
        a["sapma"] = (a["temiz"] / a["temiz_payda"] if a["temiz_payda"]
                      else None)
        a["kotu"] = a["kotu_k1"] / a["temiz"] if a["temiz"] else None
    return adaylar


def k3(kayit: dict, kip: str) -> None:
    print("== K3 · hızlı sapmanın tetiği (S3) ==")
    adlar = [f"{ad} W{W:g}" for ad, _, _, W in L.SAPMA_ADAYLARI]
    if kip in ("duman", "mekanik"):
        tum = tuple(sorted({r["tohum"] for rs in kayit.values() for r in rs}))
        a = k3_say(kayit, tum)
        if kip == "mekanik":
            print("  K3 · hesaplandı\n")
            return
        for ad, x in zip(adlar, a):
            print(f"    {ad:<10} yakalama {yuzde(x['yakalama'])} · temiz sapma "
                  f"{yuzde(x['sapma'])} · k1'in bandı kötü {yuzde(x['kotu'])}")
        print("  duman: seçim yapılmaz\n")
        return
    sec = k3_say(kayit, SECIM)
    dog = k3_say(kayit, DOGRULAMA)
    print("  aday · seçim (yakalama · temiz sapma) · doğrulama (yakalama · "
          "temiz sapma) · sapan temiz kararda k1'in bandı kötü (seçim)")
    for ad, a, b in zip(adlar, sec, dog):
        print(f"    {ad:<10} {yuzde(a['yakalama'])} · {yuzde(a['sapma'])} · "
              f"{yuzde(b['yakalama'])} · {yuzde(b['sapma'])} · "
              f"{yuzde(a['kotu'])}")
    uygun = [v for v, a in enumerate(sec)
             if a["sapma"] is not None and a["sapma"] <= TEMIZ_SAPMA
             and a["yakalama"] is not None]
    if not uygun:
        print("  hüküm K3: tetik yok (hiçbir aday temiz sapma sınırını "
              "geçmedi)\n")
        return
    v = max(uygun, key=lambda q: (sec[q]["yakalama"], -sec[q]["sapma"]))
    b = dog[v]
    dogru = b["sapma"] is not None and b["sapma"] <= TEMIZ_SAPMA
    print(f"  seçilen (seçim yarısı): {adlar[v]}")
    print(f"  hüküm K3: {adlar[v]} · doğrulamada temiz sapma "
          f"{yuzde(b['sapma'])} → {'doğrulandı' if dogru else 'DOĞRULANMADI'}"
          f" · yakalama {yuzde(b['yakalama'])}\n")


# ==============================================================================
# K4 · kopyanın bedeli (S4)
# ==============================================================================
def k4(kayit: dict, kip: str) -> None:
    print("== K4 · kopyanın bedeli (S4), betimleyici ==")
    sat: list[str] = []
    for h, rs in kayit.items():
        for kural in ("C1", "C2"):
            pay: Counter = Counter()
            payda: Counter = Counter()
            yayin = toplam = 0.0
            kapsam: Counter = Counter()
            for r in rs:
                T_veri = r["kaydedici"]["T_veri_s"]
                toplam += veri_yayin_s(r)
                kl = kararlar(r)
                for o in kl:
                    if o.evre == "g":
                        continue
                    grup = (f"açık·{o.zj}" if o.evre == "a"
                            else {"o": "önce", "s": "sessiz", "i": "ikiz"}[
                                o.evre])
                    payda[grup] += 1
                    kanit = bool(o.kanit & L.KANIT_A)
                    uygun = kanit and o.k1 >= 0 and (kural == "C1"
                                                     or o.bO < 0)
                    if uygun:
                        pay[grup] += 1
                        yayin += (o.Mk1 + o.Ck1) / L.MALIYET_BIRIM * T_veri
                for o, _ in kayiplar(r, kl):
                    kanit = bool(o.kanit & L.KANIT_A)
                    if kanit and o.k1 >= 0 and (kural == "C1" or o.bO < 0):
                        kapsam[o.sinif("A")] += 1
            gruplar = " · ".join(f"{g} {yuzde(pay[g] / payda[g])}"
                                 for g in sorted(payda) if payda[g])
            sat.append(f"    {h:<9} {kural} · ateşleme {gruplar} · yayın eki "
                       f"{yuzde(yayin / toplam if toplam else None)} · kapsadığı "
                       f"kayıp {dict(sorted(kapsam.items()))}")
    if kip == "mekanik":
        print("  K4 · hesaplandı\n")
        return
    print("\n".join(sat) + "\n")


# ==============================================================================
# K5 · kurtarmanın kestirimi (S5)
# ==============================================================================
def k5(kayit: dict, kip: str) -> None:
    print("== K5 · kurtarmanın kestirimi (S5), betimleyici ==")
    sat: list[str] = []
    rs = kayit.get("birincil", [])
    if rs:
        A = k1_paylar(rs, "A")
        parca = {s: ort(A, "agirlik", s) for s in ("J2", "J3", "U1")}
        sat.append(f"  ağırlıklı pay (birincil): J2 {parca['J2']:.4f} · J3 "
                   f"{parca['J3']:.4f} · U1 {parca['U1']:.4f} · toplam "
                   f"{sum(parca.values()):.4f}")
    for h, rs in kayit.items():
        yayin = toplam = 0.0
        vaz = vaz_k1 = 0
        for r in rs:
            T_veri = r["kaydedici"]["T_veri_s"]
            toplam += veri_yayin_s(r)
            for o in kararlar(r):
                if o.ok != 0:
                    continue
                vaz += 1
                if o.k1 >= 0:
                    vaz_k1 += 1
                    yayin += o.Mk1 / L.MALIYET_BIRIM * T_veri
        sat.append(f"  {h:<9} vazgeçme {vaz} · k1'i olan {yuzde(vaz_k1 / vaz if vaz else None)}"
                   f" · yayın eki {yuzde(yayin / toplam if toplam else None)}")
    if kip == "mekanik":
        print("  K5 · hesaplandı\n")
        return
    print("\n".join(sat) + "\n")


def main() -> int:
    klasor = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else D
    kip = ("mekanik" if klasor.name == "mekanik"
           else "duman" if klasor.name == "duman" else "tam")
    kayit = oku(klasor)
    print(f"B5 teşhisinin karar hesabı · {klasor} · kip {kip} · hücreler "
          f"{tuple(kayit)}\n")
    if not kayit:
        print("kayıt yok")
        return 1
    gecerli = k0(kayit, kip)
    k1(kayit, kip)
    k2(kayit, kip)
    k3(kayit, kip)
    k4(kayit, kip)
    k5(kayit, kip)
    if kip == "tam" and not gecerli:
        print("UYARI: K0 tutmadı — tablolar kullanılmaz, sebep ölçülür.")
    return 0 if gecerli else 1


if __name__ == "__main__":
    sys.exit(main())
