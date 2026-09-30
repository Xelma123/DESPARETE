"""AODV statik-yok döngüleri — TTL ile ölen paketlerin yolu ve döngüyü kuran rota.

30 Eylül 2026 · ajan · U1-B açıklamasının 1. koşulu kaldı: AODV'de TTL düşüşü
var (statik 1000: 42), başlangıç TTL 32, yollar ~1,8 atlama → rota döngüsü.
Ölçmeden önce yazılan adaylar (kod okumasından):
  H-a · BAYAT RREP KABULÜ: `_rrep_isle` geçersiz girdiyi sıra numarasına
        bakmadan günceller; RFC 3561 §6.7 yalnız sıra numarası bilinmiyorsa,
        daha büyükse ya da EŞİT ve (rota etkin değil ya da atlama azsa) izin
        verir. Gelen sıra < girdideki sıra iken kabul = bayat kabul.
  H-b · ARA DÜĞÜM KEŞFİ: rota girdisi `gecerli` ama süresi dolmuş (ya da
        sonraki atlama komşu listesinde yok) iken ARA düğüm paketi tamponlar
        ve sıra numarasını ARTIRMADAN keşif başlatır; yukarıdaki düğüm eski
        (bu düğümden geçen) rotasıyla cevap verebilir.
  H-c · öteki (ters rota, komşu rotası, eşit sıra).
Karar kuralı: bir aday döngülü paketlerin çoğunluğunda döngüyü kuran girdiyi
açıklıyorsa kusur odur; RFC'ye göre düzeltilir, yeniden ölçülür. Hiçbiri
değilse döngü ayrıca incelenir. Simülatöre dokunmaz (yalnız sarmalar).

    PYTHONIOENCODING=utf-8 py -3.11 -u arsiv/teshis/u1_2026-09-29/aciklama/dongu_izi.py [tohum]
"""
import collections
import os
import pathlib
import sys

# `DONGU_KOK` verilirse o kod ağacı koşar (ör. U1'in dondurulmuş kopyası = AODV-f).
KOK = pathlib.Path(os.environ.get("DONGU_KOK")
                   or pathlib.Path(__file__).resolve().parents[4])
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from protokoller import aodv as A  # noqa: E402
from sim2.kosum.dugum import Dugum  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

TOHUM = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
assert DS.referans_mi()
kfg = DS.konfig(kol="anatomi", senaryo="statik-yok", tohum=TOHUM,
                trafik_deseni="yere_toplama")
kur = kurulum_yap(kfg)


def ozet(r):
    return None if r is None else (r.sonraki, r.atlama, r.hedef_sira,
                                   r.gecerli, round(r.son_gecerli_s, 3))


yol: dict[int, list] = collections.defaultdict(list)     # paket → kararlar
hedef_of: dict[int, int] = {}
kurulum: dict[tuple[int, int], list] = collections.defaultdict(list)
sayac = collections.Counter()
asil_karar = Dugum.sonraki_atlama


def karar_izle(self, paket, t_s):
    once = ozet(self.protokol._rota.get(paket.hedef))
    kaynak_mi = paket.kaynak == self.kimlik
    karar = asil_karar(self, paket, t_s)
    hedef_of[paket.kimlik] = paket.hedef
    yol[paket.kimlik].append((round(kur.olaylar.simdi, 4), self.kimlik,
                              karar.sonraki,
                              bool(karar.beklet), once, paket.ttl_kalan))
    if karar.beklet and not kaynak_mi and once is not None and once[3]:
        sayac["H-b ara dugum tamponu+kesfi (girdi gecerli)"] += 1
    if karar.beklet and not kaynak_mi:
        sayac["ara dugum tamponladi (hepsi)"] += 1
    return karar


def sar(ad):
    asil = getattr(A.AODV, ad)

    def sarili(self, *a, **k):
        # 🔒 KÜRESEL saat: `simdi_s` düğümün YEREL saatidir (ofset + sapma);
        # paket kararlarıyla aynı eksende sıralamak için olay saati.
        simdi = kur.olaylar.simdi
        once = {h: ozet(r) for h, r in self._rota.items()}
        gelen = a[1] if ad == "_rrep_isle" else None
        sonuc = asil(self, *a, **k)
        for h, r in self._rota.items():
            yeni, eski = ozet(r), once.get(h)
            if eski is not None and eski[:3] == yeni[:3] and eski[3] == yeni[3]:
                continue
            bayat = (ad == "_rrep_isle" and eski is not None and not eski[3]
                     and gelen["hedef"] == h and gelen["hedef_sira"] < eski[2])
            if bayat:
                sayac["H-a bayat RREP kabulu (hepsi)"] += 1
            kurulum[(self.kimlik, h)].append((simdi, ad, eski, yeni, bayat))
            if eski is not None and eski[2] != 0 and yeni[2] < eski[2]:
                sayac[f"sira DUSURDU · {ad}"] += 1
        return sonuc
    setattr(A.AODV, ad, sarili)
    return lambda: setattr(A.AODV, ad, asil)


geri = [sar(ad) for ad in ("_rrep_isle", "_ters_rota", "_komsu_rotasi")]
Dugum.sonraki_atlama = karar_izle
try:
    kosu = Kosu(kur, _fabrika("aodv", kfg))
    kosu.kostur()
finally:
    Dugum.sonraki_atlama = asil_karar
    for g in geri:
        g()

# --- döngülü paketler: iletim zincirinde aynı düğüme ikinci uğrama --------
neden = collections.Counter()
ornek = []
dongulu = 0
for pk, v in yol.items():
    iletim = [(t, d, s) for t, d, s, b, _, _ in v if s is not None]
    gorulen: dict[int, int] = {}
    dongu = None
    for i, (t, d, s) in enumerate(iletim):
        if d in gorulen:
            dongu = iletim[gorulen[d]:i]
            break
        gorulen[d] = i
    if dongu is None:
        continue
    dongulu += 1
    h = hedef_of[pk]
    # Döngüdeki her düğümün, döngüye girdiği andan önceki SON rota değişikliği.
    etiket = []
    for t, d, s in dongu:
        gecmis = [e for e in kurulum[(d, h)] if e[0] <= t]
        e = gecmis[-1] if gecmis else None
        etiket.append("yok" if e is None else
                      ("H-a" if e[4] else e[1]))
    anahtar = "H-a" if "H-a" in etiket else "+".join(sorted(set(etiket)))
    neden[anahtar] += 1
    if len(ornek) < 4 and dongu[0][0] >= 50.0 and (
            anahtar != "H-a" or len(sys.argv) < 3):
        ornek.append((pk, h, dongu[0][0], [(d, s) for _, d, s in dongu],
                      [[e for e in kurulum[(d, h)] if e[0] <= t][-2:]
                       for t, d, _ in dongu]))

penceredeki = sum(1 for v in yol.values() if v[0][0] >= 50.0 and any(
    x[1] == y[1] for i, x in enumerate(v) for y in v[:i] if x[2] is not None
    and y[2] is not None))
print(f"kod {KOK.name} · aodv {A.__doc__.splitlines()[1][:60]}")
print(f"tohum {TOHUM} · paket {len(yol)} · döngülü paket {dongulu} "
      f"(ölçüm penceresinde doğan {penceredeki})")
print("sayaç:", dict(sayac))
print("döngüyü kuran son değişiklik (paket başına):", dict(neden))
for pk, h, t0, zincir, son in ornek:
    print(f"\n  paket {pk} → hedef {h} · t {t0:.3f} · döngü {zincir}")
    for (d, _), ks in zip(zincir, son):
        for e in ks:
            print(f"     düğüm {d}: {e[0]:.3f} {e[1]:<14} {e[2]} → {e[3]}"
                  f"{'  ⚠ BAYAT' if e[4] else ''}")

# --- koşu özeti: PDR ve AODV sayaçları (düzeltme öncesi/sonrası kıyası) ---
pd = kur.paket_defteri
toplam = collections.Counter()
for d in kosu.dugumler:
    toplam.update(d.protokol._sayac)
print(f"PDR(pencere) {pd.pencerede_teslim / max(pd.pencerede_uretilen, 1):.4f} · "
      + " · ".join(f"{k} {toplam[k]}" for k in (
          "kesif_basarili", "kesif_basarisiz", "rota_gecersizlestirilen",
          "rreq_uretilen", "rrep_uretilen", "rerr_uretilen")))
print("dusus (tum kosu):", {k: v for k, v in kur.korunum.dusen.items() if v})
