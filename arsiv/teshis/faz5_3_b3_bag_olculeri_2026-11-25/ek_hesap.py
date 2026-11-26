"""
B3 teşhisi · kuraldan sonra görülenler (koşudan ve karar hesabından SONRA
yazıldı; karar girdisi değil). Kayıtlardan okur; simülasyon yok.

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> > ek_hesap.txt

E1 bağın selam ölçüsüne göre dilimlerde (kullanılan bağ, temiz sınıf, ≥ 8
   önceki kayıt, F tanımlı): örnek sayısı, OMH(E_veri) ve OMH(E_selam),
   log2(F / E_selam)'ın ortancası. Selam hangi bağlarda yanılıyor?
E2 önceki tasarımın eşiği (E_selam > 4 → KÖTÜ): kullanılan bağ örneklerinde
   eşiği aşanların payı, onlarda F'nin ortancası ve F ≤ 3 olanların payı;
   ızgarada eşiği aşan bağ-dilimlerde kâhine göre iyi (p ≥ 0,28) olanların
   payı, kullanılan ve kullanılmayan ayrı.
E3 ardıl ile yedeğin aynı terazide karşılaştırılması: ızgarada aynı düğümün
   aynı anda kullanılan (≥ 8 önceki kayıt) ve kullanılmayan bağları;
   kullanılanın E_veri ile E_selam'ı farklı sıraya koyduğu çiftlerin payı
   (kullanılan, E_selam'a göre yedekten ucuzken E_veri'ye göre pahalı ya da
   tersi).
E4 (26 Kasım, çekirdek için A kararından sonra eklendi; E1–E3'ün çıktısı
   değişmez) güvenlik ağının adayı: veri örneklerinde son n kaydın hepsi
   vazgeçme (n ∈ {3, 4, 6, 8}); sınıfa ve açık dönemde alıcının alanına göre;
   bu örneklerde kâhine göre iyi olanlar ve n = 4'te sonraki veri bedeli.
"""

from __future__ import annotations

import math
import statistics as ist
import sys
from collections import defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))

import bag as B  # noqa: E402
import sonuc_hesap as SH  # noqa: E402

kayit = SH.oku(D)
ornek = SH.veri_ornekleri(kayit)


def omh(x):
    return ist.median(x) if x else None


f = SH.fmt

print("== E1 · selam ölçüsünün dilimlerinde iki ölçünün hatası ==")
print("  (kullanılan bağ, temiz sınıf, ≥ 8 önceki kayıt, F tanımlı; iki yarı)")
print("  E_selam dilimi · örnek · OMH E_veri · OMH E_selam · log2(F/E_selam) ortancası")
kume = [o for o in ornek if o.evre in SH.TEMIZ and math.isfinite(o.Es)
        and o.F is not None and len(o.once) >= SH.YETER]
for alt, ust in ((1.0, 1.5), (1.5, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 64.0)):
    k = [o for o in kume if alt <= o.Es < ust]
    if not k:
        continue
    print(f"  [{alt:.1f}, {ust:.1f}) · {len(k):>6} · "
          f"{f(omh([B.hata(SH.ev(o.once, 16), o.F) for o in k]))} · "
          f"{f(omh([B.hata(o.Es, o.F) for o in k]))} · "
          f"{omh([SH.lg(o.F) - SH.lg(o.Es) for o in k]):+.3f}")
print()

print("== E2 · önceki tasarımın selam eşiği (E_selam > 4 → KÖTÜ) ==")
k = [o for o in ornek if o.evre in SH.TEMIZ and o.F is not None
     and len(o.once) >= SH.YETER]
asan = [o for o in k if o.Es > 4.0]
print(f"  kullanılan bağ örnekleri (temiz, ≥ 8 kayıt): {len(k)} · E_selam > 4 "
      f"olan {len(asan)} ({len(asan) / len(k):.4f})")
if asan:
    print(f"    onlarda F'nin ortancası {f(omh([B.TAVAN if math.isinf(o.F) else o.F for o in asan]))}"
          f" · F ≤ 3 olanların payı {sum(o.F <= 3 for o in asan) / len(asan):.3f}"
          f" · E_veri ≤ 3 olanların payı "
          f"{sum((SH.ev(o.once, 16) or 0) <= 3 for o in asan) / len(asan):.3f}")
for ad, kullanilan in (("kullanılan", True), ("kullanılmayan", False)):
    n = iyi = 0
    for h, rs in kayit.items():
        for r in rs:
            for (_t, _i, _j, dr, _ns, df, once, p, evre, _a) in \
                    r["kaydedici"]["izgara"]:
                if evre not in SH.TEMIZ or bool(once) != kullanilan:
                    continue
                Es = B.e_selam(None if df < 0 else df / 1000,
                               None if dr < 0 else dr / 1000)
                if not (math.isfinite(Es) and Es > 4.0):
                    continue
                n += 1
                iyi += p >= 1000 * SH.KAHIN_IYI
    print(f"  ızgara, {ad}: E_selam > 4 olan bağ-dilim {n} · kâhine göre iyi "
          f"(p ≥ 0,28) payı {f(iyi / n if n else None)}")
print()

print("== E3 · ardıl ile yedek aynı terazide (ızgara, temiz sınıf) ==")
print("  aynı düğüm, aynı an: kullanılan bağ (≥ 8 önceki kayıt) × kullanılmayan")
print("  bağ (E_selam sonlu); kullanılanın maliyeti E_veri ya da E_selam")
cift = ters = 0
for h, rs in kayit.items():
    for r in rs:
        grup: defaultdict = defaultdict(list)
        for (t, i, j, dr, _ns, df, once, p, evre, _a) in r["kaydedici"]["izgara"]:
            if evre not in SH.TEMIZ:
                continue
            Es = B.e_selam(None if df < 0 else df / 1000,
                           None if dr < 0 else dr / 1000)
            if math.isfinite(Es):
                grup[(t, i)].append((Es, once))
        for v in grup.values():
            kul = [(Es, SH.ev(once, 16)) for Es, once in v
                   if len(once) >= SH.YETER]
            yed = [Es for Es, once in v if not once]
            for es_k, ev_k in kul:
                for es_y in yed:
                    cift += 1
                    ters += (es_k < es_y) != (SH.kap(ev_k) < es_y)
print(f"  çift {cift} · sıra değişen {ters} ({ters / cift:.4f})" if cift
      else "  çift yok")
print()

print("== E4 · güvenlik ağının adayı: son n veri kaydının hepsi vazgeçme ==")
print("  veri örneği · sınıf (açık dönemde alıcının alanı) · n: koşulu sağlayan /"
      " en az n önceki kaydı olan (pay; kâhine göre iyi olan)")
SINIFLAR = (("temiz", lambda o: o.evre in SH.TEMIZ),
            ("açık · G", lambda o: o.evre == "a" and o.alan == "G"),
            ("açık · E", lambda o: o.evre == "a" and o.alan == "E"),
            ("açık · U", lambda o: o.evre == "a" and o.alan == "U"))
for h in SH.HUCRELER:
    for sinif_ad, uyar in SINIFLAR:
        k = [o for o in ornek if o.hucre == h and uyar(o)]
        if not k:
            continue
        parca = []
        for n in (3, 4, 6, 8):
            kn = [o for o in k if len(o.once) >= n]
            hepsi = [o for o in kn if o.once[-n:] == "x" * n]
            iyi = sum(o.p >= SH.KAHIN_IYI for o in hepsi)
            parca.append(f"{n}: {len(hepsi)}/{len(kn)} "
                         f"({len(hepsi) / len(kn):.4f}; iyi {iyi})"
                         if kn else f"{n}: —")
        print(f"  {h:<9} {sinif_ad:<9} " + " · ".join(parca))
        h4 = [o for o in k if len(o.once) >= 4 and o.once[-4:] == "xxxx"
              and o.F is not None]
        if h4:
            print(f"  {'':<9} {'':<9}   n = 4 ve F tanımlı {len(h4)}: F ortancası "
                  f"{f(omh([SH.kap(o.F) for o in h4]))} · F = ∞ payı "
                  f"{sum(math.isinf(o.F) for o in h4) / len(h4):.3f}")
