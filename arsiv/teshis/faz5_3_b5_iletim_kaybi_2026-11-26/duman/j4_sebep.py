"""Duman tohumunda (1003, birincil, kısa pencere) J4'ün sebebi: aday olmayan
komşuların dışlanma sebebi ve göndericinin kendi B2 durumu ile alanı.
Teşhisin aletini değiştirmez; aynı kaydediciyi takıp aynı koşuyu yapar.

    cd <depo kökü>; py -3.11 <bu dosya>
"""
import math
import os
import sys
from collections import Counter, defaultdict
from dataclasses import replace

sys.path.insert(0, os.getcwd())
TESHIS = os.path.join(os.getcwd(), "arsiv", "teshis",
                      "faz5_3_b5_iletim_kaybi_2026-11-26")
sys.path.insert(1, TESHIS)

import olcum as O  # noqa: E402
import iletim as L  # noqa: E402

B1S = L.B1S
DUGUMLER = (12, 39)


def main():
    import kalibrasyon.aodv_uygunluk as AU
    import kalibrasyon.kayip_anatomisi as KA
    from kalibrasyon import dunya_secimi as DS
    from kalibrasyon.kayip_anatomisi import _etki_alani
    from sim2.kanal.yayilim import dbm_to_w

    DS.secimi_oku(["--dunya", "referans_2026"])
    kay = O.Kaydedici()
    geri = kay.tak()
    AU.DESPARETE5_PROFILLERI[O.ETIKET] = replace(
        AU.DESPARETE5_PROFILLERI["desparete5_cekirdek"], **O.FARK)
    try:
        KA._is((O.ETIKET, 1003, "formasyon", O.AILE, True, "surekli", ()))
    finally:
        del AU.DESPARETE5_PROFILLERI[O.ETIKET]
        geri()
    kur = kay.kur
    kfg = kur.konfig
    N = kfg.dugum_sayisi
    S = int(math.floor(kfg.kosu_bitis_s + 1e-9))
    kar = kur.kanal.karistirici
    uyeler = getattr(kar, "uyeler", (kar,))
    ed_w = dbm_to_w(kfg.ed_esigi_dbm)
    gecit = kfg.gecit

    def acik_mi(t):
        return t >= kfg.karistirici_baslangic_s and any(
            u.devrede_mi(t) for u in uyeler)

    # selamlar, ilanlar, onaylar
    gelis_b1 = defaultdict(list)
    gelis_bs = defaultdict(list)
    ilanlar = defaultdict(list)
    for i, j, t, sira, aralik, oran, tur, C in kay.selam_al:
        gelis_b1[(i, j)].append((t, sira, aralik, oran))
        gelis_bs[(i, j)].append((t, sira, aralik))
        ilanlar[(i, j)].append((t, tur, C, aralik))
    tazele = defaultdict(list)
    for i, j, ok, den, t, tur in kay.mac:
        if ok:
            tazele[(i, j)].append(t)
    # göndericinin kendi B2 durumu (yalnız bu düğümler)
    m = {n: [min(1.0, kay.mesgul.get((n, T), 0.0)) for T in range(S)]
         for n in DUGUMLER}
    c = {n: [kay.cozulen.get((n, T), 0) for T in range(S)] for n in DUGUMLER}
    kod = {}
    for n in DUGUMLER:
        gl = [L.I.bag_simule(sorted(v), kfg.kosu_bitis_s)[0]
              for (i, j), v in gelis_bs.items() if i == n]
        s = [L.I.selam_kaybi(gl, T + 1) for T in range(S)]
        kod[n] = L.durum_dizileri(m[n], c[n], s)[0]
    fd_t = defaultdict(list)
    fd_v = defaultdict(list)
    for n, sira, t, tur, C, ft, fc in kay.selam_kur:
        fd_t[n].append(t)
        fd_v[n].append(None if ft < 0 else (ft, fc))
    import bisect

    def fd_ani(n, t):
        q = bisect.bisect_left(fd_t[n], t) - 1
        return fd_v[n][q] if q >= 0 else None

    def son_ilan(i, k, t):
        v = ilanlar.get((i, k), [])
        tl = [x[0] for x in v]
        q = bisect.bisect_left(tl, t) - 1
        return v[q] if q >= 0 else None

    tele_akis = {a.kimlik for a in kur.trafik.akislar if a.hedef == gecit}
    dogum = {kim: akis for kim, akis, d in kur.paket_defteri.dogumlar()}
    for n in DUGUMLER:
        kararlar = [(t, j) for t, i, j, kim in kay.karar
                    if i == n and dogum.get(kim) in tele_akis and acik_mi(t)]
        Ti = [t for t, _ in kararlar]
        komsu = sorted({k for (i, k) in gelis_b1 if i == n})
        b1 = {k: B1S.b1_selam(gelis_b1[(n, k)], tazele.get((n, k), []), Ti)
              for k in komsu}
        sebep = Counter()
        kendi = Counter()
        alan_n = Counter()
        aday_yok = 0
        for x, (t, j) in enumerate(kararlar):
            T = int(t)
            fd = fd_ani(n, t)
            adaylar = 0
            sb = Counter()
            for k in komsu:
                if k == j:
                    continue
                d_r, n_s, d_f, kayitli = b1[k][x]
                if not kayitli:
                    sb["kayitsiz"] += 1
                    continue
                M = (L.SONSUZ if n_s < L.ORNEK_EN_AZ
                     else L.maliyet_M(B1S.e_selam(d_f, d_r)))
                il = son_ilan(n, k, t)
                if M >= L.SONSUZ:
                    sb["bag_kullanilmaz(df yok)" if d_f is None else
                       "bag_kullanilmaz(dr 0)" if not d_r else
                       "bag_kullanilmaz"] += 1
                    continue
                if il is None:
                    sb["ilan_yok"] += 1
                    continue
                if il[2] >= L.SONSUZ:
                    sb["ilan_sonsuz"] += 1
                    continue
                if not L.ilan_taze(t, il[0], il[3]):
                    sb["ilan_bayat"] += 1
                    continue
                if not L.uygulanabilir(il[1], il[2], fd):
                    sb["uygulanamaz"] += 1
                    continue
                adaylar += 1
            if adaylar == 0:
                aday_yok += 1
                sebep.update(sb)
                kendi[L.durum_ani(kod[n], t)] += 1
                alan_n[_etki_alani(kur, n, T + 0.5, ed_w)] += 1
        print(f"düğüm {n}: açık evrede telemetri kararı {len(kararlar)} · "
              f"başka aday yok {aday_yok}")
        print(f"  aday olmayan komşuların sebebi (karar × komşu): "
              f"{dict(sebep.most_common())}")
        print(f"  göndericinin kendi B2 durumu: {dict(kendi)}")
        print(f"  göndericinin etki alanı: {dict(alan_n)}")


if __name__ == "__main__":
    main()
