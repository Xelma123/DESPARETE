"""
Faz 5-3 · B6 (kontrol iletileri) için hesap: bugünkü selamın sıklığı ve
bedeli. Yeni koşu yok; B5 teşhisinin kayıtlarından okur (`eğim0` kolu, ikiz
ve birincil, 8 tohum, tam koşu).

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> > kontrol_bedeli.txt

Simülatör veri çerçevelerinin MAC onaylarını da kontrol çerçevesi sayar
(`sim2/kosum/teslim.py`, `kontrol_cerceve` · `kontrol_airtime_s`). "Kontrol
payı" (kontrol kanal süresi / toplam gönderim süresi; yeni çekirdek
ölçümünün tanımı, `arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/
sonuc_hesap.py`) bu yüzden onayları içerir. Burada ikisi ayrılır:
- onay sayısı = kontrol çerçevesi − kontrol iletimi;
- onayın süresi ve boyu referans dünyanın onay çerçevesinden.

Babel-a aynı ayrımla teşhis (c)'nin kayıtlarından okunur
(`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/kayit_{ikiz,birincil}.json`;
aynı tohumlar 1003–1010).
"""

from __future__ import annotations

import json
import statistics as ist
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
KOK = D.parents[2]
B5 = D.parent / "faz5_3_b5_iletim_kaybi_2026-11-26"
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(B5))

import sonuc_hesap as SH  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.dunya import referans_2026  # noqa: E402

N_DUGUM = 40


def aralik(v: list[float], fmt: str = "{:.0f}") -> str:
    return (f"{fmt.format(ist.mean(v))} ({fmt.format(min(v))}–"
            f"{fmt.format(max(v))})")


def main() -> None:
    k = referans_2026(kol="formasyon")
    onay = cerceve_kur(k, "onay")
    print("== Çerçeve süreleri (referans dünya, temel hız) ==")
    print(f"  MAC onayı {onay.bayt} bayt · {onay.sure_s * 1e3:.3f} ms")
    for n in (0, 15, 30, 39):
        c = cerceve_kur(k, "kontrol", mesaj_bayt=9 + 2 * n,
                        hiz_bps=k.temel_bit_hizi_bps)
        print(f"  selam, {n:>2} komşulu liste: {c.bayt} bayt · "
              f"{c.sure_s * 1e3:.3f} ms (sabit alanlar 9 bayt + komşu başına "
              f"2 bayt + 64 bayt kapsülleme)")
    print()

    kayit = SH.oku(B5)
    for h, rs in kayit.items():
        a: dict[str, list[float]] = {}

        def ekle(ad: str, x: float) -> None:
            a.setdefault(ad, []).append(x)

        for r in rs:
            s = r["sayaclar"]
            t = r["teshis_toplam"]
            T = r["kaydedici"]["S"]
            top = r["enerji_s"]["enerji_gonderim_s"]
            iletim = s["kontrol_iletim"]
            onay_n = s["kontrol_cerceve"] - iletim
            onay_s = onay_n * onay.sure_s
            ileti_s = s["kontrol_airtime_s"] - onay_s
            ekle("selam", t["selam.selam"])
            ekle("ara ilan", t["selam.ara_ilan"])
            ekle("ara ilan payı", t["selam.ara_ilan"] / t["selam.selam"])
            ekle("düğüm başına saniyede selam",
                 t["selam.selam"] / (N_DUGUM * T))
            ekle("yeni komşu", t["bag.yeni_komsu"])
            ekle("silinen komşu", t["bag.komsu_silindi"])
            ekle("tur isteği", t["protokol.tur_istegi_gonderilen"])
            ekle("kontrol iletimi (yeniden denemeler dâhil)", iletim)
            ekle("MAC onayı", onay_n)
            ekle("ileti başına bayt",
                 (s["kontrol_bayt"] - onay_n * onay.bayt) / iletim)
            ekle("kontrol kanal süresi, s", s["kontrol_airtime_s"])
            ekle("  protokolün iletileri, s", ileti_s)
            ekle("  MAC onayları, s", onay_s)
            ekle("toplam gönderim süresi, s", top)
            ekle("kontrol payı", s["kontrol_airtime_s"] / top)
            ekle("  protokolün iletilerinin payı", ileti_s / top)
            ekle("  MAC onaylarının payı", onay_s / top)

        print(f"== {h} · koşu başına, 8 tohumun ortalaması (en az–en çok) ==")
        yaz(a)

    # Babel-a, aynı ayrımla (teşhis (c)'nin kayıtları, aynı tohumlar)
    rc = D.parent / "faz5_2_rakip_cizgisi_2026-11-15"
    for h in ("ikiz", "birincil"):
        with open(rc / f"kayit_{h}.json", encoding="utf-8") as f:
            rs = [r for r in json.load(f)["sonuc"] if r["protokol"] == "babel"]
        a = {}
        for r in rs:
            s = r["sayaclar"]
            top = r["enerji_s"]["enerji_gonderim_s"]
            iletim = s["kontrol_iletim"]
            onay_n = s["kontrol_cerceve"] - iletim
            onay_s = onay_n * onay.sure_s
            ileti_s = s["kontrol_airtime_s"] - onay_s
            for ad, x in (("kontrol iletimi (yeniden denemeler dâhil)", iletim),
                          ("ileti başına bayt",
                           (s["kontrol_bayt"] - onay_n * onay.bayt) / iletim),
                          ("kontrol kanal süresi, s", s["kontrol_airtime_s"]),
                          ("  protokolün iletileri, s", ileti_s),
                          ("  MAC onayları, s", onay_s),
                          ("kontrol payı", s["kontrol_airtime_s"] / top),
                          ("  protokolün iletilerinin payı", ileti_s / top),
                          ("  MAC onaylarının payı", onay_s / top)):
                a.setdefault(ad, []).append(x)
        print(f"== Babel-a · {h} · koşu başına, {len(rs)} tohumun ortalaması "
              f"(teşhis (c)'nin kayıtları) ==")
        yaz(a)


def yaz(a: dict[str, list[float]]) -> None:
    for ad, v in a.items():
        if "payı" in ad:
            print(f"  {ad:<44} {aralik([100 * x for x in v], '%{:.2f}')}")
        elif ad in ("düğüm başına saniyede selam", "ileti başına bayt"):
            print(f"  {ad:<44} {aralik(v, '{:.2f}')}")
        elif ad.endswith(", s"):
            print(f"  {ad:<44} {aralik(v, '{:.1f}')}")
        else:
            print(f"  {ad:<44} {aralik(v)}")
    print()


if __name__ == "__main__":
    main()
