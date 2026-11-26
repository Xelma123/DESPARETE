"""
Faz 5-3 · B5 TEŞHİSİ — iletim kaybının yeri: karıştırılan alıcı, sıradaki
aday ve kanıtın zamanı (`beklenti.md`). Ölçüm aleti; protokolün parçası
değildir.

    cd <kod kökü: dondurulmuş kopya ya da depo kökü>
    PYTHONIOENCODING=utf-8 py -3.11 -u <bu dosya> --dunya referans_2026 \
        --hucre ikiz|birincil --tohumlar 1003,…,1010 --isci 8 \
        --kayit <yol.json.gz> [--kisa]

Kod ÇALIŞMA DİZİNİNDEN içe aktarılır (`kosu.sh` dondurulmuş kopyaya geçer);
saf işlevler (`iletim.py`) bu dosyanın dizininden. Hangi dosyadan geldikleri
çıktının başına yazılır.

🔒 KOŞU AYNI KOŞUDUR. Her koşu kayıp anatomisi aletinin işçisiyle
(`kalibrasyon/kayip_anatomisi.py::_is`) olduğu gibi yapılır. Kaydedici
simülatörün ve protokolün yöntemlerine YALNIZ OKUYAN sarmalayıcılar takar,
koşudan sonra geri alır. Tek ek: düğümlerin kanal meşgul integrali açılır
(`Dugum._doluluk`; B2 ve B3 teşhislerinde birebirdi). Denetim (`beklenti.md`
K0): satırlar yeni çekirdek ölçümünün `eğim0` satırlarıyla birebir.

🔒 KOL: `desparete5_egim0` = `CEKIRDEK`'ten `egim`, `vazgecme_tetigi`,
`duzgun_gecis` kapalı (yeni çekirdek ölçümünün tanımı). Koşu süresince
`aodv_uygunluk.DESPARETE5_PROFILLERI`ne eklenir ve çıkarılır.

🔒 HÜCRELER (`formasyon · yere_toplama`, tam pencere)
    ikiz      karıştırıcısız (`--sinif yok`), hayalet çizelge 10:20
    birincil  `derin_sizma`, 15 s açık · 15 s sessiz

🔒 KAYDEDİLENLER (simülatörün saati; kâhin, evre ve alan yalnız
değerlendirmede, `05` §8)
    karar — her TELEMETRİ kararında (sonraki atlaması verilen paket):
        evre · alıcının karar anındaki alanı (karıştırıcı kapalıysa U) · ardıl
        geçit mi · ardılın kanıt maskesi (`iletim.K_*`) · sıradaki aday k1 ve
        en iyi O adayı (sınıf, alan, kâhinin p₇'si, M, ilanı) · ardılın p₇'si
        ve M'si · hızlı sapma tetiklerinin maskesi (`iletim.SAPMA_ADAYLARI`) ·
        o atlamanın MAC sonucu · kaybın kararı mı · yalnız uygulanabilirlik
        yüzünden aday olmayan en iyi komşu (kayıtlı, bağı kullanılır, ilanı
        taze ve sonlu; alanı ve p₇'si; S6, dumandan sonra eklendi). Görünüm
        yeni tasarımın kurallarıyla, yalnız karardan önceki olaylarla
        hesaplanır (`iletim.py`).
    kayıp — her kayıp için: kararın sırası, açık dönem, dönem başından,
        alana girişten ve kanıtın başlangıcından gecikme, düşüş anı, düşüş
        anında alıcının etki alanı (kayıp anatomisinin tanımı).
    toplamlar — açık dönemde doğan telemetri ve komut; kayıp, alana göre;
        komut kaybı; bir veri çerçevesinin 1 Mb/s'deki süresi.

İç denetimler: meşgul dilimleri düğümlerin toplamına; çözülen çerçeve, MAC
sonucu, selam kurma, karar ve vazgeçme sayıları simülatörün ve protokolün
sayaçlarına eşit; her karar bir MAC sonucuyla eşleşiyor; her alınan selamın
kurulma kaydı var; paket en çok bir kez düşüyor; her kaybın kararı var;
kayıp alana göre kayıp anatomisiyle aynı.

⚠️ Ana deney tohumları (2000–2039) KOŞULMAZ.
"""

from __future__ import annotations

import bisect
import gzip
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

import iletim as L  # noqa: E402

B1S = L.B1S
ETIKET = "desparete5_egim0"
KOL = "egim0"
# CEKIRDEK'ten farkları (yeni çekirdek ölçümünün `egim0` kolu)
FARK = {"egim": False, "vazgecme_tetigi": False, "duzgun_gecis": False}
AILE = "derin_sizma"
HUCRE = {"ikiz": ("yok", "10:20"), "birincil": ("surekli", "")}
KARAR_ALANLAR = ("t_ms", "i", "j", "evre", "zj", "j_gecit", "kanit", "k1",
                 "k1_O", "zk1", "p7k1", "Mk1", "Ck1", "bO", "zbO", "p7bO",
                 "p7j", "tetik", "den", "ok", "kayip", "Mj",
                 # S6 (dumandan sonra eklendi, `beklenti.md` duman notu)
                 "uK", "zuK", "p7uK")
KAYIP_ALANLAR = ("karar", "donem", "dt_donem_ms", "dt_alan_ms",
                 "dt_kanit_A_ms", "dt_kanit_G_ms", "t_dusus_ms", "z_dusus")


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


def _ms(x: float | None) -> int:
    return -1 if x is None else int(round(1000.0 * x))


def _bin(x: float | None) -> int:
    return -1 if x is None else int(round(1000.0 * x))


class Kaydedici:
    """Bir koşunun kaydı. `tak()` sarmalayıcıları takar, dönen işlev geri
    alır."""

    def __init__(self) -> None:
        self.kur = None
        self.kosu = None
        self.mesgul: defaultdict = defaultdict(float)   # (düğüm, saniye) → s
        self.cozulen: Counter = Counter()               # (düğüm, saniye) → adet
        self.mac: list = []          # (gönderen, alıcı, onay, deneme, t, tür)
        self.selam_kur: list = []    # (düğüm, sıra, t, tur, C, fd_tur, fd_C)
        self.selam_al: list = []     # (alıcı, gönderen, t, sıra, aralık, oran, tur, C)
        self.karar: list = []        # (t, düğüm, sonraki, paket kimliği)
        self.dusus: list = []        # (t, düğüm, hedef, paket kimliği) — vazgeçme
        self.dusus_sebep: Counter = Counter()
        self._indirilen: dict = {}   # düğüm → (paket kimliği, hedef)

    # ------------------------------------------------------------------
    def tak(self):
        import sim2.kosum.kurulum as KM
        from protokoller.desparete5 import Desparete5
        from protokoller.desparete5_bicim import SELAM
        from protokoller.desparete5_selam import selam_coz
        from sim2.kosum import kontrol
        from sim2.kosum.dugum import Dugum
        from sim2.kosum.kosu import Kosu
        from sim2.mac.alici import AliciZinciri

        k = self
        asil = {
            "kurulum": KM.kurulum_yap, "kostur": Kosu.kostur,
            "mesgul": Dugum.mesgul_guncelle,
            "bitti": AliciZinciri.cerceve_bitti,
            "sonuc": kontrol.iletim_sonucu,
            "selam_kur": Desparete5._selam_kur,
            "kontrol": Desparete5.kontrol_alindi,
            "karar": Dugum.sonraki_atlama,
            "indir": Dugum.ucustan_indir,
            "yer": Dugum._kayip_yeri,
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
            """`Dugum.mesgul_guncelle`in AYNISI (B2 ve B3 teşhislerinin
            sarmalayıcısı); meşgul parçalar dilimlere de yazılır."""
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
            tur, C = self.rota.ilan()                 # okuma; yan etkisiz
            sonuc = asil["selam_kur"](self, sira, aralik_s, t)
            fd = self.rota.fd
            k.selam_kur.append((self.kimlik, int(sira), k.kur.olaylar.simdi,
                                int(tur), int(C),
                                -1 if fd is None else int(fd[0]),
                                -1 if fd is None else int(fd[1])))
            return sonuc

        def kontrol_alindi(self, gozlem, gonderen, bicim, yuk, yayin):
            if bicim == SELAM.ad:
                sira, aralik, tur, C, _, oran = selam_coz(yuk, self.kimlik)
                k.selam_al.append((self.kimlik, int(gonderen),
                                   k.kur.olaylar.simdi, int(sira),
                                   float(aralik),
                                   None if oran is None else float(oran),
                                   int(tur), int(C)))
            return asil["kontrol"](self, gozlem, gonderen, bicim, yuk, yayin)

        def sonraki_atlama(self, paket, t_s):
            karar = asil["karar"](self, paket, t_s)
            if karar.sonraki is not None:
                k.karar.append((k.kur.olaylar.simdi, self.kimlik,
                                int(karar.sonraki), paket.kimlik))
            return karar

        def ucustan_indir(self):
            hedef = self._ucus_hedefi
            paket = asil["indir"](self)
            k._indirilen[self.kimlik] = (paket.kimlik, hedef)
            return paket

        def _kayip_yeri(self, sebep):
            k.dusus_sebep[sebep] += 1
            if sebep == "iletim_basarisiz":
                kim, hedef = k._indirilen.get(self.kimlik, (None, None))
                k.dusus.append((self.kur.olaylar.simdi, self.kimlik, hedef,
                                kim))
            return asil["yer"](self, sebep)

        KM.kurulum_yap = kurulum_yap
        Kosu.kostur = kostur
        Dugum.mesgul_guncelle = mesgul_guncelle
        AliciZinciri.cerceve_bitti = cerceve_bitti
        kontrol.iletim_sonucu = iletim_sonucu
        Desparete5._selam_kur = _selam_kur
        Desparete5.kontrol_alindi = kontrol_alindi
        Dugum.sonraki_atlama = sonraki_atlama
        Dugum.ucustan_indir = ucustan_indir
        Dugum._kayip_yeri = _kayip_yeri

        def geri():
            KM.kurulum_yap = asil["kurulum"]
            Kosu.kostur = asil["kostur"]
            Dugum.mesgul_guncelle = asil["mesgul"]
            AliciZinciri.cerceve_bitti = asil["bitti"]
            kontrol.iletim_sonucu = asil["sonuc"]
            Desparete5._selam_kur = asil["selam_kur"]
            Desparete5.kontrol_alindi = asil["kontrol"]
            Dugum.sonraki_atlama = asil["karar"]
            Dugum.ucustan_indir = asil["indir"]
            Dugum._kayip_yeri = asil["yer"]
        return geri

    # ------------------------------------------------------------------
    def ozet(self) -> dict:
        from kalibrasyon.kahin import KanalGrafigi
        from kalibrasyon.kayip_anatomisi import BAG_DILIMI_S, _etki_alani
        from sim2.kanal.yayilim import dbm_to_w

        kur, kosu = self.kur, self.kosu
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
        gecit = kfg.gecit

        def devrede(t_s: float) -> bool:
            return any(u.devrede_mi(t_s) for u in uyeler)

        def acik_mi(t_s: float) -> bool:
            """Kayıp anatomisinin "açık" evresi (`evre_adi`)."""
            return kar is not None and t_s >= acilma and devrede(t_s)

        # --- evre ve açık dönemler (B2 teşhisinin tanımı) -------------------
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

        donemler: list[list[float]] = []      # açık dönemler [a, b)
        if kar is not None:
            T = 0
            while T < S:
                if evre[T] != "a":
                    T += 1
                    continue
                T0 = T
                while T < S and evre[T] == "a":
                    T += 1
                a = gecis_ani(float(T0 - 1), T0 + 1e-6)
                b = (float(S) if T >= S
                     else gecis_ani(T - 1e-6, float(T + 1)))
                donemler.append([round(a, 6), round(b, 6)])
        don_bas = [x[0] for x in donemler]

        def donem(t_s: float) -> int:
            q = bisect.bisect_right(don_bas, t_s) - 1
            return q if q >= 0 and t_s < donemler[q][1] else -1

        # --- etki alanı (düğüm × saniye; karıştırıcısızda U) ---------------
        if kar is None:
            z = ["U" * S for _ in range(N)]
        else:
            kd = {"ed": "E", "girisim": "G", "uzak": "U"}
            z = ["".join(kd[_etki_alani(kur, n, T + 0.5, ed_w)]
                         for T in range(S)) for n in range(N)]

        # --- B2'nin işaretleri: m, c, s (düğüm × saniye) --------------------
        m = [[min(1.0, self.mesgul.get((n, T), 0.0)) for T in range(S)]
             for n in range(N)]
        c = [[self.cozulen.get((n, T), 0) for T in range(S)]
             for n in range(N)]
        gelis_b1: defaultdict = defaultdict(list)   # (i, j) → [(t, sıra, a, oran)]
        gelis_bs: defaultdict = defaultdict(list)   # (i, j) → [(t, sıra, a)]
        ilanlar: defaultdict = defaultdict(list)    # (i, j) → [(t, tur, C, a)]
        for i, j, t, sira, aralik, oran, tur, C in self.selam_al:
            gelis_b1[(i, j)].append((t, sira, aralik, oran))
            gelis_bs[(i, j)].append((t, sira, aralik))
            ilanlar[(i, j)].append((t, tur, C, aralik))
        for x in (gelis_b1, gelis_bs, ilanlar):
            for v in x.values():
                v.sort(key=lambda y: y[0])
        ilan_t = {a: [y[0] for y in v] for a, v in ilanlar.items()}
        komsu_g: defaultdict = defaultdict(list)
        for (i, j), liste in gelis_bs.items():
            g_, _ = L.I.bag_simule(liste, kfg.kosu_bitis_s)
            komsu_g[i].append(g_)
        s = [[L.I.selam_kaybi(komsu_g.get(n, []), T + 1) for T in range(S)]
             for n in range(N)]

        # --- B2'nin durumu ve kendi aralıklar -------------------------------
        kod: list[str] = []
        haric: list[list] = []
        for n in range(N):
            k_, ed_, g_ = L.durum_dizileri(m[n], c[n], s[n])
            kod.append(k_)
            haric.append(L.kendi_araliklar(ed_, g_))

        # --- selamın biti (kurulduğu andaki durum) ---------------------------
        bit: dict = {}
        for n, sira, t, *_ in self.selam_kur:
            bit[(n, sira)] = L.durum_ani(kod[n], t) != "-"
        bit_yok = sum(1 for i, j, t, sira, *_ in self.selam_al
                      if (j, sira) not in bit)

        # --- MAC sonuçları ----------------------------------------------------
        veri: defaultdict = defaultdict(list)     # (i, j) → [(t, deneme, onay)]
        tazele: defaultdict = defaultdict(list)   # (i, j) → [t] (onaylanan)
        sonuc_dugum: defaultdict = defaultdict(list)  # i → [(t, j, den, onay)]
        for i, j, ok, den, t, tur in self.mac:
            if tur == "veri":
                veri[(i, j)].append((t, den, ok))
                sonuc_dugum[i].append((t, j, den, ok))
            if ok:
                tazele[(i, j)].append(t)
        for x in (veri, tazele, sonuc_dugum):
            for v in x.values():
                v.sort(key=lambda y: y if isinstance(y, float) else y[0])

        # --- bağ başına kanıt ve tetik aralıkları -----------------------------
        bild: dict = {}
        for (i, j), liste in gelis_b1.items():
            if j == gecit:
                continue
            sel = [(t, bit.get((j, sira), False)) for t, sira, _, _ in liste]
            bild[(i, j)] = L.bildirim_gercekci(sel, tazele.get((i, j), []))
        gond: dict = {}
        vyok: dict = {}
        tetik: dict = {}
        for (i, j), liste in veri.items():
            h = haric[i]
            if j != gecit:
                gond[(i, j)] = L.gonderici_araliklari(liste, h)
            vyok[(i, j)] = L.veri_yok_araliklari(liste, h)
            tetik[(i, j)] = [L.sapma_araliklari(L.tetik_anlari(liste, h, ai, n_),
                                                W)
                             for _, ai, n_, W in L.SAPMA_ADAYLARI]

        # --- FD (selam kurulurken güncellenen değer) --------------------------
        fd_t: defaultdict = defaultdict(list)
        fd_v: defaultdict = defaultdict(list)
        for n, sira, t, tur, C, ft, fc in self.selam_kur:
            fd_t[n].append(t)
            fd_v[n].append(None if ft < 0 else (ft, fc))

        def fd_ani(n: int, t_s: float):
            q = bisect.bisect_left(fd_t[n], t_s) - 1     # t'den ÖNCE
            return fd_v[n][q] if q >= 0 else None

        def son_ilan(i: int, k_: int, t_s: float):
            tl = ilan_t.get((i, k_))
            if not tl:
                return None
            q = bisect.bisect_left(tl, t_s) - 1
            return ilanlar[(i, k_)][q] if q >= 0 else None

        # --- paketler: doğum, teslim, düşüş -----------------------------------
        tele_akis = {a.kimlik for a in kur.trafik.akislar if a.hedef == gecit}
        teslim = {kd_.kimlik for kd_ in kur.paket_defteri.kayitlar()}
        dogum = {kim: (akis, d) for kim, akis, d in kur.paket_defteri.dogumlar()}
        acik_dogan = {kim for kim, (_, d) in dogum.items()
                      if bas_s <= d < bitis_s and acik_mi(d)}
        dusus_paket: dict = {}
        cift_dusus = 0
        for t, n, hedef, kim in self.dusus:
            if kim in dusus_paket:
                cift_dusus += 1
            dusus_paket[kim] = (t, n, hedef)
        kayip = sorted((kim for kim in acik_dogan
                        if kim not in teslim and kim in dusus_paket),
                       key=lambda q: dusus_paket[q][0])

        # --- kararlar ve MAC sonuçlarının eşleşmesi ---------------------------
        karar_dugum: defaultdict = defaultdict(list)   # i → [(t, j, paket)]
        for t, i, j, kim in self.karar:
            karar_dugum[i].append((t, j, kim))
        eslesmeyen = 0
        sonuc_karar: dict = {}          # (i, sıra) → (deneme, onay)
        for i, kl in karar_dugum.items():
            sl = sonuc_dugum.get(i, [])
            if len(sl) not in (len(kl), len(kl) - 1):
                eslesmeyen += abs(len(kl) - len(sl))
            for q, (t, j, kim) in enumerate(kl):
                if q < len(sl):
                    ts, js, den, ok = sl[q]
                    if js != j or ts < t or (q + 1 < len(kl)
                                             and ts > kl[q + 1][0]):
                        eslesmeyen += 1
                        continue
                    sonuc_karar[(i, q)] = (den, ok)
        # kaybın kararı: düşüş düğümünde o pakete verilen son karar
        kayip_karar: dict = {}
        kayip_kararsiz = 0
        for kim in kayip:
            t_d, n, _ = dusus_paket[kim]
            adaylar_ = [q for q, (t, _, km) in enumerate(karar_dugum.get(n, []))
                        if km == kim and t <= t_d]
            if not adaylar_:
                kayip_kararsiz += 1
                continue
            kayip_karar[(n, adaylar_[-1])] = kim

        # --- kâhin -------------------------------------------------------------
        grafik = KanalGrafigi(kur)
        onbellek: dict = {}

        def p7_kahin(i: int, k_: int, t_s: float) -> float:
            dilim = int(t_s / BAG_DILIMI_S)
            anahtar = (i, k_, dilim)
            p = onbellek.get(anahtar)
            if p is None:
                p = onbellek[anahtar] = L.p7(grafik._tek_deneme_basarisi(
                    i, k_, (dilim + 0.5) * BAG_DILIMI_S))
            return p

        # --- her telemetri kararında görünüm ----------------------------------
        komsular_i: defaultdict = defaultdict(list)
        for (i, j) in gelis_b1:
            komsular_i[i].append(j)
        satirlar: list = []
        kayip_satir: list = []
        sinir = (L.K_BILDIRIM_A | L.K_GONDERICI | L.K_VERI_YOK)
        BOS_B1 = (None, 0, None, False)
        for i in sorted(karar_dugum):
            kl = karar_dugum[i]
            tele = [q for q, (t, j, kim) in enumerate(kl)
                    if dogum.get(kim, (None,))[0] in tele_akis]
            if not tele:
                continue
            Ti = [kl[q][0] for q in tele]
            b1 = {k_: B1S.b1_selam(gelis_b1[(i, k_)], tazele.get((i, k_), []),
                                   Ti)
                  for k_ in komsular_i.get(i, [])}
            for x, q in enumerate(tele):
                t, j, kim = kl[q]
                T = min(S - 1, int(math.floor(t)))
                acik = acik_mi(t)
                fd = fd_ani(i, t)

                def maske(k_: int, b1k) -> int:
                    msk = 0
                    if k_ != gecit:
                        if L.icinde(bild.get((i, k_), ()), t):
                            msk |= L.K_BILDIRIM_G
                        if b1k[3] and L.durum_ani(kod[k_], t) != "-":
                            msk |= L.K_BILDIRIM_A
                        if L.icinde(gond.get((i, k_), ()), t):
                            msk |= L.K_GONDERICI
                    if L.icinde(vyok.get((i, k_), ()), t):
                        msk |= L.K_VERI_YOK
                    return msk

                def M_ani(b1k) -> int:
                    if not b1k[3] or b1k[1] < L.ORNEK_EN_AZ:
                        return L.SONSUZ
                    return L.maliyet_M(B1S.e_selam(b1k[2], b1k[0]))

                b1j = b1[j][x] if j in b1 else BOS_B1
                Mj = M_ani(b1j)
                msk = maske(j, b1j)
                il_j = son_ilan(i, j, t)
                if il_j is None or not L.ilan_taze(t, il_j[0], il_j[3]):
                    msk |= L.K_ILAN_BAYAT
                if Mj >= L.SONSUZ:
                    msk |= L.K_KULLANILMAZ
                aday: list = []
                engelli: list = []      # S6: yalnız FD yüzünden aday değil
                ilan_C: dict = {}
                for k_ in komsular_i.get(i, []):
                    if k_ == j:
                        continue
                    b1k = b1[k_][x]
                    Mk = M_ani(b1k)
                    il = son_ilan(i, k_, t)
                    if L.aday_mi(b1k[3], Mk, il, t, fd):
                        sk = maske(k_, b1k) & sinir
                        aday.append((k_, L.maliyet_topla(Mk, il[2]), Mk,
                                     "S" if sk else "O"))
                        ilan_C[k_] = il[2]
                    elif L.aday_mi(b1k[3], Mk, il, t, None):
                        sk = maske(k_, b1k) & sinir
                        engelli.append((k_, L.maliyet_topla(Mk, il[2]), Mk,
                                        "S" if sk else "O"))
                sirali = L.sirala(aday)
                k1 = sirali[0] if sirali else None
                bO = next((a_ for a_ in sirali if a_[3] == "O"), None)
                uK = L.sirala(engelli)[0] if engelli else None

                def alan(k_: int) -> str:
                    return z[k_][T] if acik else "U"

                p7j = p7_kahin(i, j, t)
                tmsk = 0
                for v, ara in enumerate(tetik.get((i, j), ())):
                    if L.icinde(ara, t):
                        tmsk |= 1 << v
                den, ok = sonuc_karar.get((i, q), (-1, None))
                kay = (i, q) in kayip_karar
                satirlar.append([
                    _ms(t), i, j, evre[T], alan(j), int(j == gecit), msk,
                    -1 if k1 is None else k1[0],
                    -1 if k1 is None else int(k1[3] == "O"),
                    "-" if k1 is None else alan(k1[0]),
                    -1 if k1 is None else _bin(p7_kahin(i, k1[0], t)),
                    -1 if k1 is None else k1[2],
                    -1 if k1 is None else ilan_C[k1[0]],
                    -1 if bO is None else bO[0],
                    "-" if bO is None else alan(bO[0]),
                    -1 if bO is None else _bin(p7_kahin(i, bO[0], t)),
                    _bin(p7j), tmsk, den,
                    -1 if ok is None else int(ok), int(kay), Mj,
                    -1 if uK is None else uK[0],
                    "-" if uK is None else alan(uK[0]),
                    -1 if uK is None else _bin(p7_kahin(i, uK[0], t))])
                if kay:
                    t_d = dusus_paket[kayip_karar[(i, q)]][0]
                    dq = donem(t)
                    giris = (L.alan_girisi(z[j], donemler[dq][0], t)
                             if dq >= 0 and acik else None)
                    bas_A, bas_G = [], []
                    if msk & L.K_BILDIRIM_A:
                        bas_A.append(L.durum_bilinme_ani(kod[j], t))
                    if msk & L.K_BILDIRIM_G:
                        bas_G.append(L.aralik_basi(bild[(i, j)], t))
                    for bit_, ara in ((L.K_GONDERICI, gond.get((i, j), ())),
                                      (L.K_VERI_YOK, vyok.get((i, j), ()))):
                        if msk & bit_:
                            b_ = L.aralik_basi(ara, t)
                            bas_A.append(b_)
                            bas_G.append(b_)
                    if msk & L.K_ILAN_BAYAT and il_j is not None:
                        b_ = il_j[0] + L.ILAN_OMUR_KAT * max(
                            il_j[3], B1S.ARALIK_EN_AZ)
                        bas_A.append(b_)
                        bas_G.append(b_)
                    bas_A = [b_ for b_ in bas_A if b_ is not None]
                    bas_G = [b_ for b_ in bas_G if b_ is not None]
                    kayip_satir.append([
                        len(satirlar) - 1, dq,
                        _ms(t - donemler[dq][0]) if dq >= 0 else -1,
                        _ms(t - giris) if giris is not None else -1,
                        _ms(t - min(bas_A)) if bas_A else -1,
                        _ms(t - min(bas_G)) if bas_G else -1,
                        _ms(t_d), z[j][min(S - 1, int(t_d))]])

        # --- komut kaybı ve kaybın alana göre sayımı (anatominin tanımı) -------
        kd2 = {"E": "ed", "G": "girisim", "U": "uzak"}
        kayip_alan: Counter = Counter()
        komut_kayip: Counter = Counter()
        for kim in kayip:
            t_d, _, hedef = dusus_paket[kim]
            a_ = kd2[z[hedef][min(S - 1, int(t_d))]] if kar is not None \
                else "uzak"
            kayip_alan[a_] += 1
            if dogum[kim][0] not in tele_akis:
                komut_kayip[a_] += 1
        dogan_tele = sum(1 for kim in acik_dogan if dogum[kim][0] in tele_akis)
        return {
            "pencere": [ilk, son], "S": S, "N": N, "gecit": gecit,
            "evre": evre, "donemler": donemler,
            "T_veri_s": round(kosu.veri_cercevesi.sure_s, 9),
            "karar_alanlar": list(KARAR_ALANLAR),
            "kayip_alanlar": list(KAYIP_ALANLAR),
            "sapma_adaylari": [[ad, W] for ad, _, _, W in L.SAPMA_ADAYLARI],
            "karar": satirlar, "kayip": kayip_satir,
            "dogan_acik": {"telemetri": dogan_tele,
                           "komut": len(acik_dogan) - dogan_tele},
            "kayip_alan": dict(kayip_alan), "komut_kayip": dict(komut_kayip),
            "sayim": {
                "mesgul_s": round(sum(self.mesgul.values()), 6),
                "mesgul_dugum": round(sum(d._mesgul_toplam_s
                                          for d in kosu.dugumler), 6),
                "cozulen": sum(self.cozulen.values()),
                "mac": len(self.mac), "selam_kur": len(self.selam_kur),
                "selam_al": len(self.selam_al), "karar": len(self.karar),
                "karar_tele": len(satirlar), "dusus": len(self.dusus),
                "eslesmeyen": eslesmeyen, "bit_yok": bit_yok,
                "cift_dusus": cift_dusus, "kayip": len(kayip),
                "kayip_kararsiz": kayip_kararsiz,
                "kahin_cagri": len(onbellek)},
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
        for ad, sayac in (("cozulen", "alim_basarili"),
                          ("mac", "sonuc_bildirimi"),
                          ("dusus", "mac_vazgecme")):
            if z[ad] != int(s.get(sayac, 0)):
                hata.append(f"{ad} {z[ad]} ≠ {sayac} {s.get(sayac)}")
        if z["selam_kur"] != int(t.get("protokol.selam_gonderilen", -1)):
            hata.append(f"selam kurma {z['selam_kur']} ≠ protokol "
                        f"{t.get('protokol.selam_gonderilen')}")
        tele = int(t.get("protokol.veri_gonderilen", -1))
        komut = int(t.get("protokol.komut_gonderilen", -1))
        if (z["karar_tele"], z["karar"]) != (tele, tele + komut):
            hata.append(f"karar {z['karar_tele']}/{z['karar']} ≠ protokol "
                        f"{tele}/{tele + komut}")
        for ad in ("eslesmeyen", "bit_yok", "cift_dusus", "kayip_kararsiz"):
            if z[ad]:
                hata.append(f"{ad} {z[ad]}")
        if z["selam_al"] <= 0:
            hata.append("hiç selam alınmadı")
        if not r["kaydedici"]["karar"]:
            hata.append("karar yok")
        anat = {k.split("|")[2]: v for k, v in r["dogum_evre_dusen"].items()
                if k.startswith("iletim_basarisiz|acik|")}
        if anat != r["kaydedici"]["kayip_alan"]:
            hata.append(f"kayıp alana göre {r['kaydedici']['kayip_alan']} ≠ "
                        f"anatomi {anat}")
        return hata


def _is(is_) -> dict:
    """Havuz işçisi — bir (hücre, tohum) koşusu: anatomi + kayıt."""
    import traceback
    from dataclasses import replace

    import kalibrasyon.aodv_uygunluk as AU
    import kalibrasyon.kayip_anatomisi as KA

    hucre, tohum, kisa = is_
    sinif_, hayalet = HUCRE[hucre]
    t0 = time.perf_counter()
    kay = Kaydedici()
    eklendi = False
    geri = kay.tak()
    try:
        if ETIKET in AU.DESPARETE5_PROFILLERI:
            raise RuntimeError(f"{ETIKET} profillerde zaten var")
        AU.DESPARETE5_PROFILLERI[ETIKET] = replace(
            AU.DESPARETE5_PROFILLERI["desparete5_cekirdek"], **FARK)
        eklendi = True
        r = KA._is((ETIKET, tohum, "formasyon", AILE, kisa, sinif_,
                    KA._cizelge_oku(hayalet)))
        r["kol"] = KOL
        r["hucre"] = hucre
        t1 = time.perf_counter()
        r["kaydedici"] = kay.ozet()
        r["kaydedici_denetim"] = kay.denetle(r)
        r["sure_s"] = round(time.perf_counter() - t0, 1)
        r["ozet_s"] = round(time.perf_counter() - t1, 1)
        return r
    except Exception as hata:                               # noqa: BLE001
        return {"kol": KOL, "hucre": hucre, "protokol": ETIKET,
                "tohum": tohum, "hata": f"{type(hata).__name__}: {hata}",
                "iz": traceback.format_exc()[-2000:]}
    finally:
        if eklendi:
            del AU.DESPARETE5_PROFILLERI[ETIKET]
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
    dogrula(not kayit_yolu or kayit_yolu.endswith(".json.gz"),
            "kayıt `.json.gz` olmalı")
    sinif_, hayalet = HUCRE[hucre]
    print("=" * 78)
    print(f"B5 TEŞHİSİ — dünya {DS.secili()} · {hucre} (formasyon-{sinif_}"
          f"{', ' + AILE if sinif_ != 'yok' else ''}"
          f"{', hayalet ' + hayalet if hayalet else ''}) · kol {ETIKET} · "
          f"tohum {tohumlar}{' · KISA PENCERE' if kisa else ''}")
    print(f"  kod: {Path(P5.__file__).resolve()}")
    print(f"  saf işlevler: {Path(L.__file__).resolve()} · "
          f"{Path(L.I.__file__).resolve()} · {Path(B1S.__file__).resolve()}")
    print("=" * 78, flush=True)
    isler = [(hucre, t, kisa) for t in tohumlar]
    ara = Path(kayit_yolu[:-len(".json.gz")] + ".jsonl.gz") if kayit_yolu else None
    sonuc: list[dict] = []
    if ara is not None and ara.exists():
        with gzip.open(ara, "rt", encoding="utf-8") as f:
            for satir in f:
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
                    with gzip.open(ara, "at", encoding="utf-8") as f:
                        f.write(json.dumps(r, ensure_ascii=False,
                                           separators=(",", ":")) + "\n")
                if "hata" in r:
                    hatalar += 1
                    print(f"  HATA {n}/{len(isler)} {r['tohum']}: "
                          f"{r['hata']}\n{r['iz']}", flush=True)
                    continue
                sonuc.append(r)
                denetim = r["kaydedici_denetim"]
                kd = r["kaydedici"]
                print(f"  {n:>3}/{len(isler)} {r['tohum']} · karar "
                      f"{len(kd['karar'])} · kayıp {len(kd['kayip'])} · "
                      f"denetim {'tamam' if not denetim else denetim} · "
                      f"{r['sure_s']:.0f} s (özet {r['ozet_s']:.0f} s)",
                      flush=True)
    if kayit_yolu:
        with gzip.open(kayit_yolu, "wt", encoding="utf-8") as f:
            f.write(json.dumps(
                {"dunya": DS.secili(), "hucre": hucre, "kisa": kisa,
                 "sonuc": sorted(sonuc, key=lambda r: r["tohum"])},
                ensure_ascii=False, separators=(",", ":")))
    print(f"\n  {len(sonuc)} koşu kayıtta · hata {hatalar}")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
