"""MOBİLİTE MODELİ GERÇEKÇİ Mİ — yönlendirmenin HİSSETTİĞİ büyüklükler.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/mobilite_gercekcilik.py

🔴 SORU
=======
Şu anki model (bağımsız 3B Gauss-Markov, kapalı hacimde yansıma) bir İHA
sürüsünü mü betimliyor, yoksa "kutuda çarpışan parçacıkları" mı? Ortalama
derece ve bağlantılılık DÜZGÜN çıkıyor — ama bunlar yerleşimin istatistikleri.
Yönlendirme protokolü yerleşimi değil, **bağların ne kadar yaşadığını** hisseder.

Bu betik üç büyüklüğü ölçer:
    1. BAĞ ÖMRÜ            — bir komşu ne kadar süre komşu kalıyor
    2. BAĞIL HIZ           — komşu çiftlerin birbirine göre hızı
    3. ROTA ÖMRÜ           — kurulmuş bir çok-atlamalı yolun ayakta kalma süresi

ve bunu ÜÇ MOBİLİTE KOLUNUN hepsi için yapar: statik · bağımsız · görev
tabanlı. Üçü de `sim2/`nin gerçek modelinden gelir; ayrı bir prototip yoktur.
"""
from __future__ import annotations

import collections
import math
import random
import pathlib
import statistics as ist
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import Kutu, Nokta3, mesafe  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

N, R = 40, 280.0
BITIS_S, ADIM_S = 350.0, 0.5
TOHUMLAR = range(1, 16)


# ==========================================================================
# Ölçüm çekirdeği — her iki model için AYNI
# ==========================================================================
def bag_omurleri(izler, r=R):
    """Kesintisiz "komşu" kalma sürelerinin listesi (saniye).

    Koşu başında ve sonunda kesilen ömürler ATILIR (sansürlü gözlem): dâhil
    edilseydi ortalama sistematik olarak KISA çıkardı.
    """
    adet = len(izler[0])
    omurler: list[float] = []
    for i in range(N):
        for j in range(i + 1, N):
            baslangic = None
            for k in range(adet):
                yakin = mesafe(izler[i][k], izler[j][k]) <= r
                if yakin and baslangic is None:
                    baslangic = k
                elif not yakin and baslangic is not None:
                    if baslangic > 0:          # başta kesilmemiş
                        omurler.append((k - baslangic) * ADIM_S)
                    baslangic = None
            # sonda açık kalan ömür atılır
    return omurler


def bagil_hizlar(izler, r=R):
    """Komşu çiftlerin bağıl hız büyüklüğü (m/s) — bağ ömrünün sürücüsü."""
    cikti: list[float] = []
    for k in range(0, len(izler[0]) - 1, 20):     # 10 s'de bir örnekle
        for i in range(N):
            for j in range(i + 1, N):
                if mesafe(izler[i][k], izler[j][k]) > r:
                    continue
                d0 = mesafe(izler[i][k], izler[j][k])
                d1 = mesafe(izler[i][k + 1], izler[j][k + 1])
                a, b = izler[i][k], izler[j][k]
                a2, b2 = izler[i][k + 1], izler[j][k + 1]
                vx = ((a2.x - a.x) - (b2.x - b.x)) / ADIM_S
                vy = ((a2.y - a.y) - (b2.y - b.y)) / ADIM_S
                vz = ((a2.z - a.z) - (b2.z - b.z)) / ADIM_S
                cikti.append(math.sqrt(vx * vx + vy * vy + vz * vz))
                del d0, d1
    return cikti


def _komsuluk(konumlar, r=R):
    return [[j for j in range(N) if j != i and mesafe(konumlar[i], konumlar[j]) <= r]
            for i in range(N)]


def _derinlikler(kom, s):
    d = {s: 0}
    kuyruk = collections.deque([s])
    while kuyruk:
        u = kuyruk.popleft()
        for v in kom[u]:
            if v not in d:
                d[v] = d[u] + 1
                kuyruk.append(v)
    return d


def _yol(kom, s, h):
    onceki = {s: None}
    kuyruk = collections.deque([s])
    while kuyruk:
        u = kuyruk.popleft()
        if u == h:
            yol = []
            while u is not None:
                yol.append(u)
                u = onceki[u]
            return list(reversed(yol))
        for v in kom[u]:
            if v not in onceki:
                onceki[v] = u
                kuyruk.append(v)
    return None


def rota_omurleri(izler, r=R, ornek_sayisi=40, cift_basina=5,
                  olcum_tohumu=20260904):
    """Kurulmuş bir yolun BOZULMADAN ayakta kalma süresi.

    Yönlendirme protokolünün önbelleğindeki rotanın yaşadığı şey budur:
    yol kurulur, atlamalarından biri koptuğunda ömür biter.
    """
    adet = len(izler[0])
    omurler: list[float] = []
    atlamalar: list[int] = []
    adim = max(1, (adet - 1) // ornek_sayisi)
    # 🔒 Ölçüm rastgeleliği AYRI ve sabit tohumlu: simülasyonun akışlarına
    # dokunmaz, ama ölçüm kollar arasında birebir aynı çiftleri seçer.
    rastgele = random.Random(olcum_tohumu)
    for k0 in range(0, adet - 1, adim):
        konum = [izler[i][k0] for i in range(N)]
        kom = _komsuluk(konum, r)
        # 🔴 KAYNAK/HEDEF SEÇİMİ GRUP ATAMASINDAN BAĞIMSIZ OLMALI.
        # İlk yazımda sabit çiftler kullanılıyordu — (0,20), (1,21)... Görev
        # kolunda grup ataması `i % grup_sayisi` olduğu için G ∈ {4,5,10}
        # değerlerinde bu çiftlerin İKİSİ DE AYNI MÜFREZEDE kalıyordu ve
        # ölçülen şey çok atlamalı bir rota değil, GRUP İÇİ bir yoldu.
        # Ölçüm görev kolunun rota ömrünü 10 kattan fazla şişiriyordu.
        #
        # Düzeltme: kaynak sırayla dolaşılır, hedef o andaki EN UZAK
        # ulaşılabilir düğümdür. Grup yapısıyla hizalanması imkânsız.
        # 🔴 KAYNAK/HEDEF RASTGELE — trafik modeliyle AYNI mantık.
        # İlk yazımda sabit çiftler vardı ((0,20), (1,21)...). Görev kolunda
        # grup ataması `i % grup_sayisi` olduğu için G ∈ {4,5,10} değerlerinde
        # bu çiftlerin İKİSİ DE AYNI MÜFREZEDE kalıyordu: ölçülen şey çok
        # atlamalı bir rota değil, grup içi bir yoldu ve görev kolunun rota
        # ömrünü **10 kattan fazla** şişiriyordu.
        #
        # "En uzak ulaşılabilir düğüm" de denendi ve elendi: en kötü hâli
        # ölçüyor, oysa protokol RASTGELE çiftler arasında taşıma yapıyor.
        for _ in range(cift_basina):
            kaynak = rastgele.randrange(N)
            derinlik = _derinlikler(kom, kaynak)
            adaylar = [d for d, h in derinlik.items() if h >= 2]
            if not adaylar:
                continue
            hedef = rastgele.choice(adaylar)
            yol = _yol(kom, kaynak, hedef)
            if not yol or len(yol) < 3:
                continue
            atlamalar.append(len(yol) - 1)
            k = k0
            while k < adet:
                kon = [izler[i][k] for i in range(N)]
                if any(mesafe(kon[a], kon[b]) > r
                       for a, b in zip(yol, yol[1:])):
                    break
                k += 1
            omurler.append((k - k0) * ADIM_S)
    return omurler, atlamalar


def ozet(ad, izler):
    omur = bag_omurleri(izler)
    hiz = bagil_hizlar(izler)
    rota, atlama = rota_omurleri(izler)
    kisa = sum(1 for o in omur if o < 5.0) / len(omur) if omur else float("nan")
    return dict(
        ad=ad,
        bag_ortanca=ist.median(omur) if omur else float("nan"),
        bag_ort=ist.mean(omur) if omur else float("nan"),
        bag_kisa_pay=kisa,
        bagil_hiz=ist.median(hiz) if hiz else float("nan"),
        rota_ortanca=ist.median(rota) if rota else float("nan"),
        rota_ort=ist.mean(rota) if rota else float("nan"),
        atlama=ist.mean(atlama) if atlama else float("nan"),
    )


# ==========================================================================
# ÜÇ KOL — hepsi `sim2/`nin GERÇEK modelinden, prototip yok
# ==========================================================================
# ⚠️ İlk yazımda burada bir "ölçü çubuğu" grup modeli prototipi vardı ve
# `sim2/` dışındaydı. Görev kolu artık gerçekten yazıldığı için prototip
# SİLİNDİ: ölçülen şeyle koşulan şeyin farklı kodlar olması, tam da bu
# projenin kaçındığı hata sınıfıdır.
def izler(senaryo: str, tohum: int, **ek):
    top = topoloji_kur(
        Konfig(kol="olcum", senaryo=senaryo, tohum=tohum, **ek), Akislar(tohum))
    adet = int(BITIS_S / ADIM_S) + 1
    return [[top.konum(i, k * ADIM_S) for k in range(adet)] for i in range(N)]


def main() -> None:
    print("=" * 78)
    print("YONLENDIRMENIN HISSETTIGI BUYUKLUKLER")
    print(f"({len(TOHUMLAR)} tohum x {BITIS_S:.0f} s, ornekleme {ADIM_S} s, "
          f"menzil {R:.0f} m)")
    print("=" * 78)

    for ad, senaryo in (("A - STATIK", "statik-yok"),
                        ("B - BAGIMSIZ Gauss-Markov", "bagimsiz-yok"),
                        ("C - GOREV TABANLI (sektorlu)", "gorev-yok")):
        toplu = []
        for tohum in TOHUMLAR:
            toplu.append(ozet(ad, izler(senaryo, tohum)))
        print()
        print(ad)
        print(f"   bag omru ortanca      : "
              f"{ist.mean(o['bag_ortanca'] for o in toplu):7.1f} s")
        print(f"   bag omru ortalama     : "
              f"{ist.mean(o['bag_ort'] for o in toplu):7.1f} s")
        print(f"   5 s'den kisa bag payi : "
              f"%{100*ist.mean(o['bag_kisa_pay'] for o in toplu):6.1f}")
        print(f"   bagil hiz (ortanca)   : "
              f"{ist.mean(o['bagil_hiz'] for o in toplu):7.1f} m/s")
        print(f"   ROTA omru ortanca     : "
              f"{ist.mean(o['rota_ortanca'] for o in toplu):7.1f} s"
              f"   (ort. {ist.mean(o['rota_ort'] for o in toplu):.1f} s,"
              f" {ist.mean(o['atlama'] for o in toplu):.1f} atlama)")

    print()
    print("=" * 78)
    print("KIYAS NOKTALARI  (protokolun zaman olcekleri)")
    print("=" * 78)
    k = Konfig(kol="olcum")
    print(f"   beacon araligi          : {k.beacon_araligi_s:.1f} s")
    print(f"   komsu kaydi omru        : "
          f"{k.beacon_araligi_s * k.komsu_omru_katsayisi:.1f} s")
    print(f"   bir paketin ucus suresi : ~0,01 s (3 atlama)")
    print("   AODV rota kesfi         : ~0,05-0,2 s (agin capina bagli)")


if __name__ == "__main__":
    main()
