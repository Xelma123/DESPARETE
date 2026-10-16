"""AODV-k · TTL ile ölen paketlerin döngüsü — döngüyü kuran rota değişiklikleri.

16 Ekim 2026 · tetik: anatomi (`arsiv/teshis/aodv_k_anatomi_2026-10-16/`
sonuc.md §0). Bağımsız 1000 · görev 1000 · görev 1001'de birer TTL düşüşü var;
kuyruğun ön-kaydı "döngü/TTL düşüşü 0" ister ve K-207 madde 2'ye göre döngü
izi alınır. `arsiv/teshis/aodv_sadakat_2026-09-30/dongu_izi.py`nin (K-205)
genelleştirmesi:
  - kol ve tohum argüman; yapılandırma U1'inki (`kol="u1"`);
  - rota tablosunu değiştirebilen bütün yöntemler sarılır; her değişiklik
    onu yapan EN İÇTEKİ sarılı yönteme yazılır (iç içe çağrıda çift sayım
    yok); silinen girdi de yazılır.
Simülatöre ve protokole dokunmaz (yalnız sarmalar). Ölçüt `beklenti.md`de.

    DONGU_KOK=<donmuş kopya> PYTHONIOENCODING=utf-8 py -3.11 -u \
        arsiv/teshis/aodv_k_dongu_2026-10-16/dongu_izi.py <kol> <tohum>
"""
import collections
import os
import pathlib
import sys

KOK = pathlib.Path(os.environ.get("DONGU_KOK")
                   or pathlib.Path(__file__).resolve().parents[3])
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from protokoller import aodv as A  # noqa: E402
from sim2.kosum.dugum import Dugum  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402

KOL, TOHUM = sys.argv[1], int(sys.argv[2])
assert DS.referans_mi()
# `DONGU_KISA=1` yalnız betiğin duman sınaması (kayıp anatomisinin kısa
# penceresi); sonuç satırı ondan üretilmez.
KISA = (dict(karistirici_baslangic_s=5.0, isinma_s=10.0, olcum_bitis_s=40.0,
             kosu_bitis_s=50.0) if os.environ.get("DONGU_KISA") else {})
kfg = DS.konfig(kol="u1", senaryo=KOL, tohum=TOHUM,
                trafik_deseni="yere_toplama", **KISA)
kur = kurulum_yap(kfg)

SARILAN = ("kontrol_alindi", "uyandi", "zamanlayici_doldu", "sonraki_atlama",
           "iletim_sonucu", "iletim_basarisiz", "_rreq_isle", "_rrep_isle",
           "_rerr_isle", "_ters_rota", "_komsu_rotasi", "_gecersizlestir",
           "_bag_koptu", "_bakim", "_kurtarma")


def ozet(r):
    return None if r is None else (r.sonraki, r.atlama, r.hedef_sira,
                                   r.gecerli, round(r.son_gecerli_s, 3))


yol: dict[int, list] = collections.defaultdict(list)     # paket → kararlar
hedef_of: dict[int, int] = {}
kurulum: dict[tuple[int, int], list] = collections.defaultdict(list)
sayac = collections.Counter()
asil_karar = Dugum.sonraki_atlama
yigin: list[dict] = []          # iç içe sarılı çağrıların anlık görüntüleri


def karar_izle(self, paket, t_s):
    once = ozet(self.protokol._rota.get(paket.hedef))
    karar = asil_karar(self, paket, t_s)
    hedef_of[paket.kimlik] = paket.hedef
    yol[paket.kimlik].append((round(kur.olaylar.simdi, 4), self.kimlik,
                              karar.sonraki, bool(karar.beklet), once,
                              paket.ttl_kalan))
    return karar


def kaydet(cagri) -> None:
    """Çağrının görüntüsünden bu yana yapılan değişiklikleri o çağrının adına
    yazar ve görüntüyü bugüne ilerletir."""
    ad, self, once, simdi, gelen = cagri
    sonra = {h: ozet(r) for h, r in self._rota.items()}
    for h in set(once) | set(sonra):
        eski, yeni = once.get(h), sonra.get(h)
        if eski == yeni or (eski is not None and yeni is not None
                            and eski[:4] == yeni[:4]):
            continue
        bayat = (ad == "_rrep_isle" and eski is not None and not eski[3]
                 and gelen.get("hedef") == h and eski[2] != A.SONSUZ_SIRA
                 and gelen.get("hedef_sira", 0) < eski[2])
        if bayat:
            sayac["H-a bayat RREP kabulu"] += 1
        kurulum[(self.kimlik, h)].append((simdi, ad, eski, yeni, bayat))
        if (eski is not None and yeni is not None
                and eski[2] != A.SONSUZ_SIRA
                and yeni[2] != A.SONSUZ_SIRA and yeni[2] < eski[2]):
            sayac[f"sira DUSURDU · {ad}"] += 1
    once.clear()
    once.update(sonra)


def sar(ad):
    asil = getattr(A.AODV, ad)

    def sarili(self, *a, **k):
        # 🔒 KÜRESEL saat: `simdi_s` düğümün yerel saatidir; paket
        # kararlarıyla aynı eksende sıralamak için olay saati.
        # 🔴 16 Ekim düzeltmesi (ilk koşudan sonra): ilk sürüm iç çağrıdan
        # dönerken dış çağrının görüntüsüne BÜTÜN tabloyu yazıyordu; dış
        # çağrının iç çağrıdan önce yaptığı değişiklik (rota kurup
        # `_kurtarma`'yı çağıran üç yöntemin kuruluşu) kayboluyordu. Şimdi
        # iç çağrıya girerken dış çağrının o ana kadarki değişiklikleri
        # kendi adına yazılır; sonda zincir sürekliliği denetlenir.
        if yigin:
            kaydet(yigin[-1])
        cagri = (ad, self, {h: ozet(r) for h, r in self._rota.items()},
                 kur.olaylar.simdi, a[1] if ad == "_rrep_isle" else None)
        yigin.append(cagri)
        try:
            sonuc = asil(self, *a, **k)
        finally:
            yigin.pop()
        kaydet(cagri)
        if yigin:
            # Dış çağrının görüntüsü bu çağrının sonundaki duruma ilerler:
            # aradaki değişikliklerin hepsi bu çağrı (ya da içi) adına yazıldı.
            dis = yigin[-1][2]
            dis.clear()
            dis.update(cagri[2])
        return sonuc
    setattr(A.AODV, ad, sarili)
    return lambda: setattr(A.AODV, ad, asil)


geri = [sar(ad) for ad in SARILAN]
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
ayrinti = []
dongulu = 0
for pk, v in yol.items():
    iletim = [(t, d, s, ttl) for t, d, s, b, _, ttl in v if s is not None]
    gorulen: dict[int, int] = {}
    dongu = None
    for i, (t, d, s, _) in enumerate(iletim):
        if d in gorulen:
            dongu = iletim[gorulen[d]:i]
            break
        gorulen[d] = i
    if dongu is None:
        continue
    dongulu += 1
    h = hedef_of[pk]
    ttl_oldu = min(x[3] for x in iletim) <= 1
    etiket = []
    for t, d, s, _ in dongu:
        gecmis = [e for e in kurulum[(d, h)] if e[0] <= t]
        e = gecmis[-1] if gecmis else None
        etiket.append("yok" if e is None else ("H-a" if e[4] else e[1]))
    anahtar = "H-a" if "H-a" in etiket else "+".join(sorted(set(etiket)))
    neden[anahtar] += 1
    ayrinti.append((ttl_oldu, pk, h, dongu[0][0], len(iletim),
                    [(d, s) for _, d, s, _ in dongu],
                    [[e for e in kurulum[(d, h)] if e[0] <= t][-3:]
                     for t, d, _, _ in dongu]))

# --- zincir sürekliliği: ardışık iki kaydın ilkinin sonu ikincisinin başı ---
bosluk = toplam_gecis = 0
for degisimler in kurulum.values():
    for e1, e2 in zip(degisimler, degisimler[1:]):
        toplam_gecis += 1
        y1, e2_eski = e1[3], e2[2]
        if (y1 is None) != (e2_eski is None) or (
                y1 is not None and y1[:4] != e2_eski[:4]):
            bosluk += 1

satir = sonuc_satiri(kur, kosu.dugumler, "u1")
print(f"kod {KOK} · aodv {A.__doc__.splitlines()[1][:70]}")
print(f"{'KISA · ' if KISA else ''}{KOL} · tohum {TOHUM} · PDR {satir['metrikler']['pdr']:.4f} · "
      f"korunum gecerli {satir['korunum']['gecerli']}")
print("dusus (tum kosu):", {k: v for k, v in kur.korunum.dusen.items() if v})
print(f"paket {len(yol)} · döngülü paket {dongulu} · TTL ile ölen "
      f"{sum(1 for x in ayrinti if x[0])}")
print(f"zincir sürekliliği: {bosluk} boşluk / {toplam_gecis} ardışık kayıt "
      f"(0 olmalı; değilse iz eksik)")
print("sayaç:", dict(sayac))
print("döngüyü kuran son değişiklik (paket başına):", dict(neden))
ayrinti.sort(key=lambda x: (not x[0], x[3]))
for ttl_oldu, pk, h, t0, n, zincir, son in ayrinti[:25]:
    print(f"\n  {'TTL ILE OLDU · ' if ttl_oldu else ''}paket {pk} → hedef {h}"
          f" · t {t0:.3f} · iletim {n} · döngü {zincir}")
    for (d, _), ks in zip(zincir, son):
        for e in ks:
            print(f"     düğüm {d}: {e[0]:.3f} {e[1]:<16} {e[2]} → {e[3]}"
                  f"{'  ⚠ BAYAT' if e[4] else ''}")
