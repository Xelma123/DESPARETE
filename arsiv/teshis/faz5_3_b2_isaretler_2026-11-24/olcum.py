"""
Faz 5-3 · B2 TEŞHİSİ — karıştırma işaretleri, bizim çekirdeğimizin trafiğinde
(`beklenti.md`). Ölçüm aleti; protokolün parçası değildir.

    cd <kod kökü: dondurulmuş kopya ya da depo kökü>
    PYTHONIOENCODING=utf-8 py -3.11 -u <bu dosya> --dunya referans_2026 \
        --hucre ikiz|birincil|dayaniklilik|cephe \
        --tohumlar 1003,…,1010 --isci 8 --kayit <yol.json> [--kisa]

Kod ÇALIŞMA DİZİNİNDEN içe aktarılır (`kosu.sh` dondurulmuş kopyaya geçer);
saf işlevler (`isaret.py`) bu dosyanın dizininden. Hangi dosyadan geldikleri
çıktının başına yazılır.

🔒 KOŞU AYNI KOŞUDUR. Her koşu kayıp anatomisi aletinin işçisiyle
(`kalibrasyon/kayip_anatomisi.py::_is`) olduğu gibi yapılır. Kaydedici
simülatörün ve protokolün yöntemlerine YALNIZ OKUYAN sarmalayıcılar takar,
koşudan sonra geri alır. Tek ek: düğümlerin kanal meşgul integrali açılır
(`Dugum._doluluk`; teşhis (d) Babel'de aynı yolla birebirdi). Çekirdek
`mesgul_sure_s`'i okumaz: `karistirma_durumu` kapalıyken `KendiDurum.saniye`
hemen döner. Denetim (`beklenti.md` kural 0): ikiz ve birincilde satırlar döngü
kuralları ölçümünün `geri_sinir` kolu (aynı kod, aynı tohum) ile birebir;
dumanda dayanıklılık ve cephe kaydedicisiz koşuyla birebir.

🔒 KOL: `desparete5_cekirdek` (CEKIRDEK: karıştırmaya karşı mekanizmalar
kapalı; geri gönderme yasağı ve sınırlı yükselme açık).

🔒 HÜCRELER (`formasyon · yere_toplama`, tam pencere)
    ikiz          karıştırıcısız (`--sinif yok`), hayalet çizelge 10:20
    birincil      `derin_sizma`, 15 s açık · 15 s sessiz
    dayaniklilik  `derin_sizma`, 10 · 20 (`@tehdit_acik_s=10+tehdit_sessiz_s=20`)
    cephe         `cephe_hatti` (3 sabit yer karıştırıcısı, sürekli yayın)

🔒 KAYDEDİLENLER (simülatörün saati; protokolün göremeyeceği etiketler yalnız
değerlendirmede, `05` §8)
    düğüm-saniye (her düğüm, her 1 s): kanal meşgul payı (‰) · çözülen çerçeve
        · CRC hatası · selam kaybı payı (‰; B1 sayımıyla, `isaret.py`) ·
        gönderdiği veri çerçevelerinin denemesi, başarısız denemesi,
        vazgeçmesi, başarısız denemeli ayrı komşu sayısı · etki alanı
        (E · G · U; karıştırıcısızda −).
    evre (her 1 s): o önce · a açık · s sessiz · g geçiş · i ikiz; açık
        dönemlerin uçları ikiye bölmeyle.
    bağ kuralları (göndericide, `isaret.KURALLAR`): temiz sınıflarda (ikiz ·
        önce · sessiz · açık dönemde uzak alıcı) ateşlenme sayısı ve paydası;
        açık dönem başına, alıcısı E ya da G olan bağların gecikmesi.
    bitin ulaşması: açık dönemde G alanındaki düğümün selamlarından tanıdık
        komşularına ulaşan pay, alıcının alanına göre.

İç denetimler: dilimlere yazılan meşgul süresi düğümlerin toplamına; çözülen
çerçeve, CRC hatası, MAC sonucu ve selam kurma sayıları simülatörün ve
protokolün sayaçlarına eşit.

⚠️ Ana deney tohumları (2000–2039) KOŞULMAZ.
"""

from __future__ import annotations

import bisect
import json
import math
import os
import sys
import time
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

# Kod çalışma dizininden (dondurulmuş kopya); saf işlevler bu dizinden.
if os.getcwd() not in sys.path[:1]:
    sys.path.insert(0, os.getcwd())
BURASI = Path(__file__).resolve().parent
if str(BURASI) not in sys.path:
    sys.path.insert(1, str(BURASI))

import isaret as I  # noqa: E402

ETIKET = "desparete5_cekirdek"
# hücre → (sınıf, aile, hayalet çizelge, konfig farkı)
HUCRE = {
    "ikiz": ("yok", "derin_sizma", "10:20", ""),
    "birincil": ("surekli", "derin_sizma", "", ""),
    "dayaniklilik": ("surekli", "derin_sizma", "",
                     "tehdit_acik_s=10+tehdit_sessiz_s=20"),
    "cephe": ("surekli", "cephe_hatti", "", ""),
}
TEMIZ = ("ikiz", "once", "sessiz", "uzak")
ONCEKI_S = 10.0               # dönemden önce çalışan bağ penceresi


def _dagit(tablo: dict, anahtar: int, bas: float, bitis: float) -> None:
    """[bas, bitis) aralığını 1 s'lik dilimlere oranla böler."""
    if bitis <= bas:
        return
    k = int(math.floor(bas))
    while bas < bitis:
        sinir = min(bitis, float(k + 1))
        tablo[(anahtar, k)] += sinir - bas
        bas = sinir
        k += 1


class Kaydedici:
    """Bir koşunun kaydı. `tak()` sarmalayıcıları takar, dönen işlev geri
    alır."""

    def __init__(self) -> None:
        self.kur = None
        self.kosu = None
        self.mesgul: defaultdict = defaultdict(float)   # (düğüm, dilim) → s
        self.cozulen: Counter = Counter()
        self.phy: Counter = Counter()
        self.mac: list = []          # (gönderen, alıcı, onay, deneme, t, tür)
        self.selam_kur: list = []    # (gönderen, sıra, t)
        self.selam_al: list = []     # (alıcı, gönderen, t, sıra, aralık)

    # ------------------------------------------------------------------
    def tak(self):
        import sim2.kosum.kurulum as KM
        from protokoller.desparete5 import Desparete5
        from protokoller.desparete5_bicim import SELAM_E
        from protokoller.desparete5_selam import selam_coz
        from sim2.kosum import kontrol
        from sim2.kosum.dugum import Dugum
        from sim2.kosum.kosu import Kosu
        from sim2.mac.alici import AliciZinciri

        k = self
        asil = {
            "kurulum": KM.kurulum_yap, "kostur": Kosu.kostur,
            "mesgul": Dugum.mesgul_guncelle, "phy": Dugum.phy_hata_say,
            "bitti": AliciZinciri.cerceve_bitti,
            "sonuc": kontrol.iletim_sonucu,
            "selam_kur": Desparete5._selam_kur,
            "kontrol": Desparete5.kontrol_alindi,
        }

        def kurulum_yap(*a, **kw):
            kur = asil["kurulum"](*a, **kw)
            k.kur = kur
            return kur

        def kostur(self):
            k.kosu = self
            for d in self.dugumler:
                d._doluluk = True
            sonuc = asil["kostur"](self)
            for d in self.dugumler:
                d.mesgul_guncelle(self.kur.konfig.kosu_bitis_s)
            return sonuc

        def mesgul_guncelle(self, t_s):
            """`Dugum.mesgul_guncelle`in AYNISI (aynı sınırlar, aynı orta
            nokta okuması); meşgul parçalar dilimlere de yazılır."""
            if not self._doluluk:
                return
            bas = self._mesgul_son_s
            if t_s <= bas:
                return
            self._mesgul_son_s = t_s
            sinirlar = {bas, t_s}
            kr = self.kur.kanal.karistirici
            if kr is not None:
                sinirlar.update(kr.gecis_anlari(bas, t_s))
                if kr.hareketli:
                    adim = self.kur.konfig.karistirici_denetim_araligi_s
                    sinirlar.update(bas + i * adim for i in
                                    range(1, int((t_s - bas) / adim) + 1))
            s = sorted(a for a in sinirlar if bas <= a <= t_s)
            for a, b in zip(s, s[1:]):
                if b > a and self.kanal_mesgul_mu(0.5 * (a + b)):
                    self._mesgul_toplam_s += b - a
                    _dagit(k.mesgul, self.kimlik, a, b)

        def phy_hata_say(self):
            k.phy[(self.kimlik, int(self.kur.olaylar.simdi))] += 1
            return asil["phy"](self)

        def cerceve_bitti(self, iletim, t_s):
            s = asil["bitti"](self, iletim, t_s)
            if s is not None and s.basarili:
                k.cozulen[(self.dugum, int(t_s))] += 1
            return s

        def iletim_sonucu(kosu, d, hedef, basarili, deneme, tur):
            if hedef is not None and d.sonuc_kancasi:
                k.mac.append((d.kimlik, int(hedef), bool(basarili),
                              int(deneme), kosu.olaylar.simdi, tur))
            return asil["sonuc"](kosu, d, hedef, basarili, deneme, tur)

        def _selam_kur(self, sira, aralik_s, t):
            k.selam_kur.append((self.kimlik, int(sira), k.kur.olaylar.simdi))
            return asil["selam_kur"](self, sira, aralik_s, t)

        def kontrol_alindi(self, gozlem, gonderen, bicim, yuk, yayin):
            if bicim == SELAM_E.ad:
                sira, aralik, *_ = selam_coz(yuk, self.kimlik)
                k.selam_al.append((self.kimlik, int(gonderen),
                                   k.kur.olaylar.simdi, int(sira),
                                   float(aralik)))
            return asil["kontrol"](self, gozlem, gonderen, bicim, yuk, yayin)

        KM.kurulum_yap = kurulum_yap
        Kosu.kostur = kostur
        Dugum.mesgul_guncelle = mesgul_guncelle
        Dugum.phy_hata_say = phy_hata_say
        AliciZinciri.cerceve_bitti = cerceve_bitti
        kontrol.iletim_sonucu = iletim_sonucu
        Desparete5._selam_kur = _selam_kur
        Desparete5.kontrol_alindi = kontrol_alindi

        def geri():
            KM.kurulum_yap = asil["kurulum"]
            Kosu.kostur = asil["kostur"]
            Dugum.mesgul_guncelle = asil["mesgul"]
            Dugum.phy_hata_say = asil["phy"]
            AliciZinciri.cerceve_bitti = asil["bitti"]
            kontrol.iletim_sonucu = asil["sonuc"]
            Desparete5._selam_kur = asil["selam_kur"]
            Desparete5.kontrol_alindi = asil["kontrol"]
        return geri

    # ------------------------------------------------------------------
    def ozet(self) -> dict:
        from kalibrasyon.kayip_anatomisi import _etki_alani
        from sim2.kanal.yayilim import dbm_to_w

        kur = self.kur
        kfg = kur.konfig
        N = kfg.dugum_sayisi
        S = int(math.floor(kfg.kosu_bitis_s + 1e-9))
        bas_s, bitis_s = kfg.olcum_penceresi
        ilk = int(math.ceil(bas_s - 1e-9))
        son = int(math.floor(bitis_s + 1e-9))            # [ilk, son)
        kar = kur.kanal.karistirici
        uyeler = getattr(kar, "uyeler", (kar,)) if kar is not None else ()
        acilma = kfg.karistirici_baslangic_s
        ed_w = dbm_to_w(kfg.ed_esigi_dbm)

        def devrede(t_s: float) -> bool:
            return any(u.devrede_mi(t_s) for u in uyeler)

        # --- evre (teşhis (d)'nin tanımı) ------------------------------
        ev = []
        for T in range(S):
            a, b = float(T), float(T + 1)
            if kar is None:
                e = "i"
            elif b <= acilma:
                e = "o"
            elif a < acilma:
                e = "g"
            else:
                d3 = {devrede(a + 1e-6), devrede(a + 0.5), devrede(b - 1e-6)}
                e = "g" if len(d3) > 1 else ("a" if d3.pop() else "s")
            ev.append(e)
        evre = "".join(ev)

        def gecis_ani(sol: float, sag: float) -> float:
            ilk_durum = devrede(sol)
            for _ in range(40):
                orta = 0.5 * (sol + sag)
                if devrede(orta) == ilk_durum:
                    sol = orta
                else:
                    sag = orta
            return sag

        donemler: list[list[float]] = []
        if kar is not None:
            T = ilk
            while T < son:
                if evre[T] != "a":
                    T += 1
                    continue
                T0 = T
                while T < son and evre[T] == "a":
                    T += 1
                if devrede(float(T0 - 1)):
                    continue                 # pencereden önce başlamış dönem
                a = gecis_ani(float(T0 - 1), T0 + 1e-6)
                b = (float(son) if T >= son
                     else gecis_ani(T - 1e-6, float(T + 1)))
                donemler.append([round(a, 6), round(b, 6)])

        # --- etki alanı (düğüm × saniye) --------------------------------
        if kar is None:
            z = ["-" * S for _ in range(N)]
        else:
            kod = {"ed": "E", "girisim": "G", "uzak": "U"}
            z = ["".join(kod[_etki_alani(kur, n, T + 0.5, ed_w)]
                         for T in range(S)) for n in range(N)]

        # --- düğüm-saniye: meşgul, çözülen, CRC, MAC ----------------------
        def dizi(f) -> list[list[int]]:
            return [[f(n, T) for T in range(S)] for n in range(N)]

        m = dizi(lambda n, T: int(round(1000.0 * self.mesgul.get((n, T), 0.0))))
        c = dizi(lambda n, T: self.cozulen.get((n, T), 0))
        p = dizi(lambda n, T: self.phy.get((n, T), 0))
        a_ = [[0] * S for _ in range(N)]
        f_ = [[0] * S for _ in range(N)]
        v_ = [[0] * S for _ in range(N)]
        kom: defaultdict = defaultdict(set)
        cerceve: defaultdict = defaultdict(list)          # (i, j) → [(t, d, ok)]
        for i, j, ok, den, t, tur in self.mac:
            if tur != "veri":
                continue
            cerceve[(i, j)].append((t, den, ok))
            T = int(t)
            if 0 <= T < S:
                a_[i][T] += den
                basarisiz = den - (1 if ok else 0)
                f_[i][T] += basarisiz
                v_[i][T] += 0 if ok else 1
                if basarisiz > 0:
                    kom[(i, T)].add(j)
        k_ = [[len(kom.get((n, T), ())) for T in range(S)] for n in range(N)]

        # --- B1 sayımı: bağ başına, ve düğümün selam kaybı ---------------
        gelis: defaultdict = defaultdict(list)            # (i, j) → [(t, sıra, a)]
        alinan_sira: set = set()
        for i, j, t, sira, aralik in self.selam_al:
            gelis[(i, j)].append((t, sira, aralik))
            alinan_sira.add((i, j, sira))
        sim: dict = {}
        for anahtar, liste in gelis.items():
            liste.sort()
            g, sifir = I.bag_simule(liste, kfg.kosu_bitis_s)
            sim[anahtar] = (g, sifir, [x[0] for x in liste],
                            [max(x[2], I.ARALIK_EN_AZ) for x in liste])
        komsu_g: defaultdict = defaultdict(list)          # i → [goruntu]
        for (i, j), (g, _, _, _) in sim.items():
            komsu_g[i].append(g)
        s_ = [[-1] * S for _ in range(N)]
        for n in range(N):
            gl = komsu_g.get(n, [])
            for T in range(S):
                x = I.selam_kaybi(gl, T + 1)          # saniyenin sonu
                if x is not None:
                    s_[n][T] = int(round(1000.0 * x))

        # --- bağ kuralları ---------------------------------------------
        def sinif(j: int, t: float) -> str | None:
            T = int(math.floor(t))
            if not ilk <= T < son:
                return None
            e = evre[T]
            if e == "g":
                return None
            if e == "i":
                return "ikiz"
            if e == "o":
                return "once"
            if e == "s":
                return "sessiz"
            return {"U": "uzak", "G": "G", "E": "E"}[z[j][T]]

        veri_ad = [ad for ad, _, _ in I.VERI_KURALLARI]
        ses_ad = [ad for ad, _, _ in I.SES_KURALLARI]
        fa = {ad: {s: 0 for s in TEMIZ} for ad in veri_ad + ses_ad}
        veri_payda = {s: [0, 0] for s in TEMIZ}           # [çerçeve, bağ-saniye]
        ses_payda = {s: 0 for s in TEMIZ}                 # kullanılabilir bağ-saniye
        # Birimler: veri_birim — veri taşıyan bağ (bütün kurallar, aynı
        # birimlerde: veri kuralları sonra sessizlik kuralları sırasıyla);
        # ses_birim — kullanılabilir her bağ (yalnız sessizlik kuralları).
        veri_birim: list = []        # [alan, hız, dönem, gecikme…]
        ses_birim: list = []         # [alan, dönem, gecikme…]
        bos = ([], [], [], [])
        for (i, j), liste in cerceve.items():
            liste.sort()
            _, sifir_ij, gt, ga = sim.get((i, j), bos)
            ates = I.veri_ates(liste, gt, ga)
            ates_ses_ij = I.ses_ates(sifir_ij)
            bagsn: dict = {s: set() for s in TEMIZ}
            for t, _, _ in liste:
                s = sinif(j, t)
                if s in veri_payda:
                    veri_payda[s][0] += 1
                    bagsn[s].add(int(t))
            for s in TEMIZ:
                veri_payda[s][1] += len(bagsn[s])
            for ad in veri_ad:
                for t in ates[ad]:
                    s = sinif(j, t)
                    if s in fa[ad]:
                        fa[ad][s] += 1
            for q, (on, off) in enumerate(donemler):
                orta = min(S - 1, int((on + off) / 2))
                zj = z[j][orta]
                if zj not in "EG":
                    continue
                once = [t for t, _, ok in liste if on - ONCEKI_S <= t < on]
                if not any(ok for t, _, ok in liste
                           if on - ONCEKI_S <= t < on):
                    continue
                if not any(on <= t < off for t, _, _ in liste):
                    continue
                hiz = "r" if len(once) / ONCEKI_S > 1.5 else "y"
                gec = [I.ilk_ates(ates[ad], on, off) for ad in veri_ad]
                gec += [I.ilk_ates(ates_ses_ij[ad], on, off) for ad in ses_ad]
                veri_birim.append([zj, hiz, q] + [
                    None if x is None else round(x, 3) for x in gec])
        for (i, j), (g, sifir, gt, _) in sim.items():
            ates = I.ses_ates(sifir)
            for T in range(ilk, son):
                x = g[T + 1] if T + 1 < len(g) else None
                if (x is None or x[4] < T + 1 - I.TANIDIK_S or x[3] is None
                        or x[3] < I.KULLANILABILIR_DR):
                    continue
                s = sinif(j, T + 0.5)
                if s in ses_payda:
                    ses_payda[s] += 1
            for ad in ses_ad:
                for t, dr in ates[ad]:
                    if dr is None or dr < I.KULLANILABILIR_DR:
                        continue
                    s = sinif(j, t)
                    if s in fa[ad]:
                        fa[ad][s] += 1
            for q, (on, off) in enumerate(donemler):
                orta = min(S - 1, int((on + off) / 2))
                zj = z[j][orta]
                if zj not in "EG":
                    continue
                k0 = bisect.bisect_left(gt, on - ONCEKI_S)
                if not (k0 < len(gt) and gt[k0] < on):
                    continue
                x = g[int(math.floor(on))]
                if x is None or x[3] is None or x[3] < I.KULLANILABILIR_DR:
                    continue
                gec = [I.ilk_ates(ates[ad], on, off) for ad in ses_ad]
                ses_birim.append([zj, q] + [
                    None if x is None else round(x, 3) for x in gec])

        # --- bitin ulaşması --------------------------------------------
        kur_dugum: defaultdict = defaultdict(list)        # j → [(t, sıra)]
        for j, sira, t in self.selam_kur:
            kur_dugum[j].append((t, sira))
        bit = {"E": [0, 0], "G": [0, 0], "U": [0, 0]}
        for on, off in donemler:
            orta = min(S - 1, int((on + off) / 2))
            for j in range(N):
                if z[j][orta] != "G":
                    continue
                gonderilen = [sr for t, sr in kur_dugum.get(j, ())
                              if on <= t < off]
                if not gonderilen:
                    continue
                for i in range(N):
                    if i == j or (i, j) not in sim:
                        continue
                    gt = sim[(i, j)][2]
                    k0 = bisect.bisect_left(gt, on - ONCEKI_S)
                    if not (k0 < len(gt) and gt[k0] < on):
                        continue                          # tanıdık değil
                    zi = z[i][orta]
                    for sr in gonderilen:
                        bit[zi][0] += 1
                        bit[zi][1] += (i, j, sr) in alinan_sira

        return {
            "pencere": [ilk, son], "S": S, "N": N,
            "evre": evre, "donemler": donemler,
            "ds": {"m": m, "c": c, "p": p, "s": s_, "a": a_, "f": f_,
                   "v": v_, "k": k_, "z": z},
            "kural_veri": veri_ad, "kural_ses": ses_ad,
            "fa": fa, "veri_payda": veri_payda, "ses_payda": ses_payda,
            "veri_birim": veri_birim, "ses_birim": ses_birim,
            "bit": bit,
            "sayim": {
                "mesgul_s": round(sum(self.mesgul.values()), 6),
                "mesgul_dugum": round(sum(d._mesgul_toplam_s
                                          for d in self.kosu.dugumler), 6),
                "cozulen": sum(self.cozulen.values()),
                "phy": sum(self.phy.values()),
                "mac": len(self.mac), "selam_kur": len(self.selam_kur),
                "selam_al": len(self.selam_al), "bag": len(sim)},
        }

    @staticmethod
    def denetle(r: dict) -> list[str]:
        """İç denetimler — boş liste: hepsi geçti."""
        z = r["kaydedici"]["sayim"]
        s = r["sayaclar"]
        t = r["teshis_toplam"]
        hata = []
        if abs(z["mesgul_s"] - z["mesgul_dugum"]) > 1e-6 * max(
                1.0, z["mesgul_dugum"]):
            hata.append(f"meşgul dilimler {z['mesgul_s']} ≠ düğümler "
                        f"{z['mesgul_dugum']}")
        for ad, sayac in (("cozulen", "alim_basarili"), ("phy", "alim_red_per"),
                          ("mac", "sonuc_bildirimi")):
            if z[ad] != int(s.get(sayac, 0)):
                hata.append(f"{ad} {z[ad]} ≠ {sayac} {s.get(sayac)}")
        if z["selam_kur"] != int(t.get("protokol.selam_gonderilen", -1)):
            hata.append(f"selam kurma {z['selam_kur']} ≠ protokol "
                        f"{t.get('protokol.selam_gonderilen')}")
        if z["selam_al"] <= 0:
            hata.append("hiç selam alınmadı")
        return hata


def _is(is_) -> dict:
    """Havuz işçisi — bir (hücre, tohum) koşusu: anatomi + kayıt."""
    import traceback

    import kalibrasyon.kayip_anatomisi as KA

    hucre, tohum, kisa = is_
    sinif_, aile, hayalet, fark = HUCRE[hucre]
    etiket = ETIKET + (f"@{fark}" if fark else "")
    t0 = time.perf_counter()
    kay = Kaydedici()
    geri = kay.tak()
    try:
        r = KA._is((etiket, tohum, "formasyon", aile, kisa, sinif_,
                    KA._cizelge_oku(hayalet)))
        r["kol"] = "cekirdek"
        r["hucre"] = hucre
        r["kaydedici"] = kay.ozet()
        r["kaydedici_denetim"] = kay.denetle(r)
        r["sure_s"] = round(time.perf_counter() - t0, 1)
        return r
    except Exception as hata:                               # noqa: BLE001
        return {"kol": "cekirdek", "hucre": hucre, "protokol": etiket,
                "tohum": tohum, "hata": f"{type(hata).__name__}: {hata}",
                "iz": traceback.format_exc()[-2000:]}
    finally:
        geri()


def _arg(argv: list[str], ad: str, varsayilan: str) -> str:
    if ad in argv:
        i = argv.index(ad)
        deger = argv[i + 1]
        del argv[i:i + 2]
        return deger
    return varsayilan


def main() -> int:
    from kalibrasyon import dunya_secimi as DS
    from sim2.cekirdek.degismezler import dogrula
    import protokoller.desparete5 as P5

    argv = sys.argv[1:]
    DS.secimi_oku(argv)
    kisa = "--kisa" in argv
    if kisa:
        argv.remove("--kisa")
    hucre = _arg(argv, "--hucre", "ikiz")
    tohumlar = [int(t) for t in _arg(argv, "--tohumlar", "1003").split(",")]
    isci = int(_arg(argv, "--isci", "8"))
    kayit_yolu = _arg(argv, "--kayit", "")
    dogrula(not argv, f"tanınmayan argüman: {argv}")
    dogrula(hucre in HUCRE, f"hücre {tuple(HUCRE)}: {hucre}")
    dogrula(not any(2000 <= t <= 2039 for t in tohumlar),
            "ana deney tohumları (2000–2039) mühürden önce koşulmaz")
    sinif_, aile, hayalet, fark = HUCRE[hucre]
    print("=" * 78)
    print(f"B2 TEŞHİSİ — dünya {DS.secili()} · {hucre} (formasyon-{sinif_}"
          f"{', ' + aile if sinif_ != 'yok' else ''}"
          f"{', hayalet ' + hayalet if hayalet else ''}"
          f"{', ' + fark if fark else ''}) · kol {ETIKET} · tohum {tohumlar}"
          f"{' · KISA PENCERE' if kisa else ''}")
    print(f"  kod: {Path(P5.__file__).resolve()}")
    print(f"  saf işlevler: {Path(I.__file__).resolve()}")
    print("=" * 78, flush=True)
    isler = [(hucre, t, kisa) for t in tohumlar]
    ara = Path(kayit_yolu + "l") if kayit_yolu else None
    sonuc: list[dict] = []
    if ara is not None and ara.exists():
        for satir in ara.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                r = json.loads(satir)
                if "hata" not in r:
                    sonuc.append(r)
        bitti = {r["tohum"] for r in sonuc}
        isler = [i for i in isler if i[1] not in bitti]
        print(f"  ara kayıttan {len(sonuc)} koşu okundu, {len(isler)} koşu "
              f"kaldı ({ara})", flush=True)
    hatalar = 0
    if isler:
        with Pool(min(isci, len(isler))) as havuz:
            for n, r in enumerate(havuz.imap_unordered(_is, isler,
                                                       chunksize=1), 1):
                if ara is not None:
                    with ara.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                if "hata" in r:
                    hatalar += 1
                    print(f"  HATA {n}/{len(isler)} {r['tohum']}: "
                          f"{r['hata']}\n{r['iz']}", flush=True)
                    continue
                sonuc.append(r)
                denetim = r["kaydedici_denetim"]
                print(f"  {n:>3}/{len(isler)} {r['tohum']} · PDR(pencere) "
                      f"{r['pdr_pencere']:.4f} · denetim "
                      f"{'tamam' if not denetim else denetim} · "
                      f"{r['sure_s']:.0f} s", flush=True)
    if kayit_yolu:
        Path(kayit_yolu).write_text(
            json.dumps({"dunya": DS.secili(), "hucre": hucre, "kisa": kisa,
                        "sonuc": sorted(sonuc, key=lambda r: r["tohum"])},
                       ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")
    print(f"\n  {len(sonuc)} koşu kayıtta · hata {hatalar}")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
