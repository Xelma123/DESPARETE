"""Faz 5-2 (b) · beklentinin karar kuralını kayıtlara uygular (simülasyon yok).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc_hesap.py [kayıt.json]

Argümansız: bu dizindeki `kayit_taban.json` ve `kayit_secenek.json`. Tek bir
kayıt dosyası verilirse (duman koşusunun denemesi) yalnız o okunur.
"""
import json
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
ILK = D.parent / "faz5_2_anatomi_2026-11-14" / "kayit_ikiz.json"
T = "desparete"
C = "desparete~hedefli_canlilik"
O = "desparete~onarim_edinimi"
CO = "desparete~hedefli_canlilik+onarim_edinimi"
SECENEK = {C: ("hedefli_canlilik",), O: ("onarim_edinimi",),
           CO: ("hedefli_canlilik", "onarim_edinimi")}
TABAN = (T, "babel", "en_guvenilir_kahin")
KOLLAR = (T, C, O, CO, "babel", "en_guvenilir_kahin")
AD = {T: "T", C: "C", O: "O", CO: "CO", "babel": "Babel",
      "en_guvenilir_kahin": "kâhin"}
GRUP = {"rota_gecersiz": "R", "hedef_yok": "R", "tampon_asimi": "R",
        "iletim_basarisiz": "I", "kuyruk_tasmasi": "K", "ttl": "T"}
ALIM = ("alim_basarili", "alim_red_mesgul", "alim_red_yari_cift",
        "alim_red_onbelge", "alim_red_per")
CALKANTI = ("komsu.gecis_expired", "alan.ardil_degisti", "alan.onarima_girdi",
            "alan.ulasilamaz", "protokol.solicit_gonderilen",
            "protokol.istek_gonderilen", "alan.tur_artirildi",
            "komsu.probe_bosta", "protokol.ilan_gonderilen",
            "protokol.veri_bekletilen", "protokol.tampon_kota_disi")


def oku(yollar):
    sonuc, kisa = [], False
    for yol in yollar:
        if yol.exists():
            k = json.loads(yol.read_text(encoding="utf-8"))
            sonuc += k["sonuc"]
            kisa = kisa or bool(k.get("kisa"))
    return ({p: sorted((r for r in sonuc if r["protokol"] == p),
                       key=lambda r: r["tohum"]) for p in KOLLAR}, kisa)


def pencere(rs):
    """Pencerede doğan paketlerin akıbeti, doğana oran (havuzlanmış)."""
    dogan = sum(e["dogan"] for r in rs
                for e in r["karistirici_evresi"].values())
    teslim = sum(e["teslim"] for r in rs
                 for e in r["karistirici_evresi"].values())
    g = Counter()
    for r in rs:
        for k, v in r["dogum_evre_dusen"].items():
            g[GRUP.get(k.split("|")[0], "?")] += v
    return {"pdr": teslim / dogan, **{k: g[k] / dogan for k in "RIKT"}}


def topla(rs, anahtar):
    c = Counter()
    for r in rs:
        c.update({k: v for k, v in (r.get(anahtar) or {}).items()
                  if isinstance(v, (int, float))})
    return c


def gecerlilik(kol, kisa):
    print("== 0 · GEÇERLİLİK ==")
    for p, rs in kol.items():
        for r in rs:
            acik = r["desparete_acik"]
            if acik is None:
                durum = "—"
            else:
                beklenen = set(SECENEK.get(p, ()))
                gorulen = {a for a in ("hedefli_canlilik", "onarim_edinimi")
                           if a in acik}
                durum = ("tamam" if gorulen == beklenen
                         else f"UYUŞMUYOR {sorted(gorulen)}")
            print(f"  {AD[p]:<6} {r['tohum']} korunum {r['gecerli']} · çelişki "
                  f"{r['dogum_celiski']} · atfsız {r['dogum_atfsiz'] or 0} · "
                  f"açık seçenekler {durum}")
    if kisa:
        print("  (kısa pencere: ilk ölçümle karşılaştırma yapılmaz)")
        return
    ilk = {(r["protokol"], r["tohum"]): r["pdr_pencere"] for r in
           json.loads(ILK.read_text(encoding="utf-8"))["sonuc"]}
    print("  taban kolların pencere PDR'si, ilk ölçümün ikiz kaydıyla:")
    for p in TABAN:
        for r in kol[p]:
            y = ilk.get((p, r["tohum"]))
            print(f"    {AD[p]:<6} {r['tohum']} {r['pdr_pencere']:.6f} ↔ "
                  f"{'yok' if y is None else format(y, '.6f')} "
                  f"{'birebir' if y is not None and abs(r['pdr_pencere'] - y) < 1e-12 else 'FARKLI'}")


def s1(kol):
    print("\n== 1 · S1 — seçeneğin etkisi (pencere, T'ye göre) ==")
    if not kol[T]:
        return
    t = pencere(kol[T])
    print(f"  {'T':<3} PDR {t['pdr']:.4f} · R {t['R']:.4f} · İ {t['I']:.4f} · "
          f"K {t['K']:.4f} · T {t['T']:.4f}")
    for p in (C, O, CO):
        rs = kol[p]
        if not rs:
            continue
        o = pencere(rs)
        fark = o["pdr"] - t["pdr"]
        esli = [pencere([r])["pdr"] - pencere([x])["pdr"]
                for r in rs for x in kol[T] if x["tohum"] == r["tohum"]]
        arti, eksi = sum(f > 0 for f in esli), sum(f < 0 for f in esli)
        hukum = ("YARARLI" if fark >= 0.02 and arti >= 3 else
                 "ZARARLI" if fark <= -0.02 and eksi >= 3 else
                 "ayırt edilemedi")
        print(f"  {AD[p]:<3} PDR {o['pdr']:.4f} · ΔPDR {fark:+.4f} · ΔR "
              f"{o['R'] - t['R']:+.4f} · Δİ {o['I'] - t['I']:+.4f} · K "
              f"{o['K']:.4f} · T {o['T']:.4f} → {hukum}")
        print("      tohum başına ΔPDR: " + " · ".join(
            f"{r['tohum']} {f:+.4f}" for r, f in zip(rs, esli)))
    print("  çalkantı ve kontrol (ağ toplamı, tohum ortalaması, bütün koşu):")
    for p in (T, C, O, CO):
        rs = kol[p]
        if not rs:
            continue
        ts, sy = topla(rs, "teshis_toplam"), topla(rs, "sayaclar")
        giris = Counter()
        for r in rs:
            for k, v in r["desparete_onarim"]["sayim"].items():
                giris[k.split("|")[1]] += v
        n = len(rs)
        print(f"    {AD[p]:<3} " + " · ".join(
            f"{a.split('.')[1]} {ts[a] / n:.0f}" for a in CALKANTI)
            + f" · onarım bölümü {sum(giris.values()) / n:.0f} (adaysız "
            f"{giris['adaysiz'] / max(sum(giris.values()), 1):.0%})"
            f" · kontrol çerçevesi {sy['kontrol_cerceve'] / n:.0f} · kontrol "
            f"kanal süresi {sy['kontrol_airtime_s'] / n:.1f} s")


def iletim(rs):
    """Bütün koşu: atlama ve deneme düzeyinde gerçekleşen ↔ beklenen."""
    sy = topla(rs, "sayaclar")
    karar = sum(r["karar_sayisi"] for r in rs)
    dusus = sum(sum(r["basarisiz_bant"].values()) for r in rs)
    d = sum(r["veri_deneme"] for r in rs)
    h = topla(rs, "veri_hedefte_sonuc")
    o = {"karar": karar, "d": d,
         "f_a": dusus / karar,
         "b_a": sum(r["karar_beklenen_basarisiz"] for r in rs) / karar,
         "f_d": 1.0 - sy["mac_gonderim_basarili"] / d,
         "b_d": sum(r["veri_deneme_beklenen_basarisiz"] for r in rs) / d,
         "g": sy["mac_gonderim_basarili"] / d,
         "g0": 1.0 - sum(r["veri_deneme_beklenen_basarisiz"] for r in rs) / d,
         "onay_kaybi": sy["mac_onaysiz_onay"] / d,
         "veri_ulasmadi": sy["mac_onaysiz_veri"] / d,
         "duyma_disi": (d - sum(h.values())) / d,
         "onbelge+govde": (h["alim_red_onbelge"] + h["alim_red_per"]) / d}
    o.update({a: h[a] / d for a in ALIM})
    return o


def s2(kol, kisa):
    print("\n== 2 · S2 — iletim başarısızlığının ayrımı (bütün koşu) ==")
    O_ = {p: iletim(rs) for p, rs in kol.items() if rs}
    for p, o in O_.items():
        print(f"  {AD[p]:<6} atlama: gerçekleşen {o['f_a']:.2%} · beklenen "
              f"{o['b_a']:.2%} · fazla {o['f_a'] - o['b_a']:+.2%} | deneme "
              f"(karar başına {o['d'] / o['karar']:.2f}): gerçekleşen "
              f"{o['f_d']:.1%} · beklenen {o['b_d']:.1%} · fazla "
              f"{o['f_d'] - o['b_d']:+.1%}")
        print(f"         deneme başarısı g {o['g']:.3f} = g0 {o['g0']:.3f} × k "
              f"{o['g'] / o['g0']:.3f} · bağımsız denemeyle atlama "
              f"başarısızlığı (1 − g)^7 = {(1 - o['g']) ** 7:.2%}")
        print(f"         adreslenen alıcıda: başarılı {o['alim_basarili']:.1%}"
              f" · meşgul {o['alim_red_mesgul']:.1%} · yarı çift "
              f"{o['alim_red_yari_cift']:.1%} · önbelge "
              f"{o['alim_red_onbelge']:.1%} · gövde {o['alim_red_per']:.1%} · "
              f"duyma dışı {o['duyma_disi']:.1%} | onay kaybı "
              f"{o['onay_kaybi']:.1%}")
    if T in O_ and "babel" in O_:
        t, b = O_[T], O_["babel"]
        import math
        lg = math.log(t["g"] / b["g"])
        lg0 = math.log(t["g0"] / b["g0"])
        pi = lg0 / lg if lg else float("nan")
        print(f"  g(T)/g(Babel) = {t['g'] / b['g']:.3f} = g0 oranı "
              f"{t['g0'] / b['g0']:.3f} × k oranı "
              f"{(t['g'] / t['g0']) / (b['g'] / b['g0']):.3f} · bağ seçiminin "
              f"payı π = {pi:.2f} → "
              + ("BAĞ SEÇİMİ" if pi >= 0.5
                 else "BAĞIN KENDİ KALİTESİ DIŞINDA"))
        F, B = t["f_a"] - b["f_a"], t["b_a"] - b["b_a"]
        print(f"  atlama düzeyi (ilk yazılan oran, betimleyici): F = "
              f"{F:+.2%} · B = {B:+.2%} · B/F = "
              f"{(B / F if F else float('nan')):.2f}")
        fark = {a: t[a] - b[a] for a in (
            "alim_red_mesgul", "alim_red_yari_cift", "onbelge+govde",
            "onay_kaybi", "duyma_disi")}
        print("  alt ayrım, deneme düzeyinde T − Babel: " + " · ".join(
            f"{a} {v:+.1%}" for a, v in sorted(fark.items(),
                                               key=lambda x: -x[1]))
            + f" | beklenen farkı b_d {t['b_d'] - b['b_d']:+.1%} · toplam "
            f"f_d {t['f_d'] - b['f_d']:+.1%}")
    print("  deneme hızı — pay (adreslenen alıcıda başarı):")
    enaz = {}
    for p, rs in kol.items():
        if not rs:
            continue
        hz, hh = topla(rs, "veri_deneme_hiz"), topla(rs, "veri_hedefte_hiz")
        d = sum(hz.values())
        sirali = sorted(hz, key=float)
        enaz[p] = hz[sirali[0]] / d
        print(f"    {AD[p]:<6} " + " · ".join(
            f"{float(h) / 1e6:g} Mb/s {hz[h] / d:.1%} "
            f"({hh[h + '|alim_basarili'] / hz[h]:.1%})" for h in sirali))
    if T in enaz and "babel" in enaz:
        f = enaz[T] - enaz["babel"]
        print(f"    en düşük hızdaki pay, T − Babel: {f:+.1%} → "
              + ("hız uyarlaması iki kolda farklı çalışıyor"
                 if abs(f) >= 0.10 else "fark 10 puanın altında"))
    print("  kanal yükü (ağ toplamı, tohum ortalaması, bütün koşu):")
    ks = {}
    for p, rs in kol.items():
        if not rs:
            continue
        sy, n = topla(rs, "sayaclar"), len(rs)
        sure = 50.0 if kisa else 350.0
        veri = (sy["veri_airtime_s"] + sy["veri_baslik_airtime_s"]) / n
        gonderim = sum(r["enerji_s"]["enerji_gonderim_s"] for r in rs) / n
        ks[p] = sy["kontrol_airtime_s"] / n
        print(f"    {AD[p]:<6} kontrol çerçevesi {sy['kontrol_cerceve'] / n:.0f}"
              f" · kontrol kanal süresi {ks[p]:.1f} s · veri kanal süresi "
              f"{veri:.1f} s · toplam gönderim {gonderim:.1f} s "
              f"(koşu süresinin %{100 * gonderim / sure:.0f}'i, ağ toplamı) · "
              f"veri denemesi "
              f"{sy['mac_deneme'] / n:.0f}")
    if T in ks and "babel" in ks and ks["babel"]:
        o = ks[T] / ks["babel"]
        print(f"    kontrol kanal süresi, T / Babel = {o:.2f} → "
              + ("BELİRGİN YÜKSEK" if o >= 1.5 else
                 "BELİRGİN DÜŞÜK" if o <= 1 / 1.5 else "BENZER"))


def main():
    if len(sys.argv) > 1:
        kol, kisa = oku([Path(sys.argv[1]).resolve()])
    else:
        kol, kisa = oku([D / "kayit_taban.json", D / "kayit_secenek.json"])
    if not any(kol.values()):
        print("kayıt yok")
        return
    gecerlilik(kol, kisa)
    s1(kol)
    s2(kol, kisa)


if __name__ == "__main__":
    main()
