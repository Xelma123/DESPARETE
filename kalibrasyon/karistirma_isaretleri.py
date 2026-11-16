"""
Karıştırmanın yerel işaretleri — Faz 5-2 teşhis (d), 16 Kasım 2026.

    PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/karistirma_isaretleri.py \\
        --dunya referans_2026 --kol formasyon --sinif yok|surekli \\
        --tohumlar 1003,1004 --isci 8 --protokoller babel[@farklar] \\
        --kayit yol.json [--kisa]

🔒 SORULAR (`arsiv/teshis/faz5_2_isaretler_2026-11-16/beklenti.md`):
    S1  protokolün görebildiği işaretler karıştırıcının ED ve girişim
        bölgelerinde, karıştırılmayan düğümlerden ne kadar ayrışıyor
        (`v2/17` T-5); bağ düzeyinde "düşük teslim + güçlü sinyal"
        tutarlılığı karıştırılan bağı kötü bağdan ayırıyor mu;
    S2  ardışık MAC vazgeçmelerinin dizileri karıştırılan ve karıştırılmayan
        bağda ne uzunlukta, karıştırma başlayınca n'inci ardışık vazgeçme ne
        kadar sürede geliyor (T-10);
    S3  bağ kalitesi ne hızla değişiyor (selam aralığının üst sınırı, T-1).

🔒 PROTOKOLÜN GÖREBİLDİĞİ (`v2/05` §3), BİRİM BAŞINA:
    düğüm × 1 s dilim — kanal meşgul süresi (`mesgul_sure_s`, 802.11k
        sayacı) · bunun çözülen çerçevelerin hava süresiyle açıklanamayan
        kısmı · CRC hatası (`phy_hata`) · çözülen çerçeve (`alinan_cerceve`)
        · son çözülen çerçeveden beri geçen süre · son 4 s'de tanıdık
        komşulardan beklenen selamların kaçırılan payı (Babel Hello'sunun
        sıra numarası; "tanıdık": son 16 s'de selamı duyulmuş);
    bağ (gönderen → alıcı) × 5 s dilim — deneme başarısı (MAC sonucu) ·
        göndericinin aynı komşudan son 10 s'de duyduğu çerçevelerin RSSI'ı
        (`cerceve_duyuldu`nun formülü: kilitlenilen güç + σ hatası);
    bağ — art arda MAC vazgeçmesi dizileri ve çerçeve başına deneme.
Çözülen çerçevenin hava süresini gerçek telsiz çerçevenin PLCP başlığından
bilir; gözlem penceresinde bugün yok — protokol kullanacaksa `05` §7 yolu
ya da boyuttan tahmin (`beklenti.md` §0).

🔒 ETİKETLER YALNIZ DEĞERLENDİRMEDE (`05` §8): evre (önce · açık · sessiz;
dilimin içinde geçiş varsa "gecis" ve dışarıda) · düğümün ETKİ ALANI
(`kayip_anatomisi._etki_alani`: karıştırıcı açık olsaydı alınacak ortalama
güç; ED ≥ −76 dBm · girişim ≥ gürültü tabanı · uzak). Bağ birimleri ALICININ
alanıyla etiketlenir (SINR kaybı alıcıda). Karıştırıcısız kolda tek sınıf
"ikiz". S3 kâhinin bağ ölçüsünden (`KanalGrafigi._tek_deneme_basarisi`),
yalnız karıştırıcısız kolda.

🔒 DAVRANIŞ AYNI: protokole kanca EKLENMEZ. Simülatörün `Dugum.mesgul_guncelle`
(aynı integral, dilimlere bölünerek kaydedilir; düğümler `_doluluk` açık
koşar — Babel `mesgul_sure_s` okumaz) · `Dugum.phy_hata_say` ·
`AliciZinciri.cerceve_bitti` · `kontrol.iletim_sonucu` · `Dugum.sonraki_atlama`
ve Babel'in `_hello_kur` · `_hello_al` yöntemleri bu işçi sürecinde SARILIR,
koşu sonunda geri alınır. Kanıt iki katlı: (1) koşu içinde kaydedilen
meşgul süresi düğümün kendi toplamına, çözülen çerçeve ve CRC hatası
simülatörün sayaçlarına EŞİT olmak zorundadır, değilse araç patlar;
(2) satırın PDR'si ve sayaçları teşhis (c)'nin aynı tohumdaki Babel
satırına eşit olmalıdır (`sonuc_hesap.py` §0 denetler).

⚠️ Ana deney tohumları (2000–2039) KOŞULMAZ.
"""

from __future__ import annotations

import bisect
import json
import math
import sys
import time
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from sim2.cekirdek.degismezler import dogrula  # noqa: E402

DILIM_S = 1.0                 # düğüm-saniye birimi
BAG_DILIM_S = 5.0             # bağ birimi (S1b)
RSSI_PENCERE_S = 10.0         # göndericinin komşudan duyduğu RSSI penceresi
SELAM_PENCERE_S = 4.0         # selam kaybı penceresi (Babel Hello aralığı)
TANIDIK_S = 16.0              # komşu "tanıdık": son 16 s'de selamı duyulmuş
BAG_EN_AZ_CERCEVE = 3         # bağ biriminin en az çerçevesi
DIZI_TAVAN = 30               # vazgeçme dizisi uzunluğu tavanı
DENEME_TAVAN = 8
GECIKME_N = (1, 2, 3, 4, 5)   # S2: n'inci ardışık vazgeçme
ONCEKI_BASARI_S = 10.0        # S2: açılmadan önce çalışan bağ
S3_GECIKMELER = (1, 2, 4, 8, 16, 32)
S3_BAG_SAYISI = 80
S3_EN_AZ_KARAR = 50
SESSIZLIK_TAVAN_S = 30.0

# İşaret → (alt, üst, kutu sayısı). Tamsayı sayaçlar birim genişlikte kutu.
KUTULAR: dict[str, tuple[float, float, int]] = {
    "mesgul": (0.0, 1.0, 50),
    "aciklanamayan": (0.0, 1.0, 50),
    "phy": (0.0, 100.0, 100),
    "cozulen": (0.0, 300.0, 300),
    "sessizlik": (0.0, SESSIZLIK_TAVAN_S, 300),
    "selam_kaybi": (0.0, 1.0, 20),
}
TESLIM_KUTU = 10              # 0,1 genişlik
RSSI_ALT_DBM, RSSI_GENISLIK_DB, RSSI_KUTU = -110.0, 2.0, 40


def kutu(isaret: str, x: float) -> int:
    alt, ust, n = KUTULAR[isaret]
    return min(n - 1, max(0, int((x - alt) / (ust - alt) * n)))


def rssi_kutusu(rssi: float | None) -> str:
    if rssi is None:
        return "yok"
    return str(min(RSSI_KUTU - 1,
                   max(0, int((rssi - RSSI_ALT_DBM) / RSSI_GENISLIK_DB))))


def dagit(tablo: dict, anahtar: int, bas: float, bitis: float) -> None:
    """[bas, bitis) aralığını 1 s'lik dilimlere oranla böler."""
    if bitis <= bas:
        return
    k = int(math.floor(bas / DILIM_S))
    while bas < bitis:
        sinir = min(bitis, (k + 1) * DILIM_S)
        tablo[(anahtar, k)] += sinir - bas
        bas = sinir
        k += 1


def vazgecme_dizileri(sonuclar: list[bool]) -> list[tuple[int, int]]:
    """Art arda başarısız (False) dizileri: (başladığı sıra, uzunluk)."""
    diziler: list[tuple[int, int]] = []
    bas = None
    for i, b in enumerate(sonuclar):
        if not b and bas is None:
            bas = i
        elif b and bas is not None:
            diziler.append((bas, i - bas))
            bas = None
    if bas is not None:
        diziler.append((bas, len(sonuclar) - bas))
    return diziler


def nci_vazgecme(olaylar: list[tuple[float, bool]], t_bas: float,
                 t_son: float, n: int) -> float | None:
    """`t_bas`tan sonra n'inci ARDIŞIK vazgeçmenin anı − t_bas (yoksa None).
    Başarı sayacı sıfırlar; `t_bas`tan önceki olaylar sayılmaz."""
    say = 0
    for t, b in olaylar:
        if t < t_bas:
            continue
        if t >= t_son:
            break
        say = 0 if b else say + 1
        if say >= n:
            return t - t_bas
    return None


def _is_guvenli(is_) -> dict:
    import traceback
    try:
        return _is(is_)
    except Exception as hata:                               # noqa: BLE001
        return {"protokol": is_[0], "tohum": is_[1],
                "hata": f"{type(hata).__name__}: {hata}",
                "iz": traceback.format_exc()[-2000:]}


def _is(is_) -> dict:
    """Havuz işçisi — bir (protokol, tohum) koşusu ve işaretleri."""
    from kalibrasyon.aodv_uygunluk import _fabrika
    from kalibrasyon.kahin import KanalGrafigi
    from kalibrasyon.kayip_anatomisi import _etki_alani, _konfig_farklari
    from protokoller.babel import Babel
    from sim2.cekirdek.rng import normal_cekimi
    from sim2.kanal.yayilim import dbm_to_w
    from sim2.kosum import kontrol
    from sim2.kosum.dugum import Dugum
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.mac.alici import AliciZinciri

    etiket, tohum, kol, aile, kisa, sinif = is_
    protokol, _, farklar = etiket.partition("@")
    dogrula(protokol == "babel",
            f"kaydedici Babel'in Hello sırasını okur: {etiket!r}")
    t0 = time.perf_counter()
    # 🔒 `kayip_anatomisi._is` ile AYNI konfig — teşhis (c)'nin Babel
    # satırına birebirlik bu sayede denetlenebilir.
    pencere = (dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
                    olcum_bitis_s=40.0, kosu_bitis_s=50.0) if kisa else {})
    ek = {} if sinif == "yok" else {"tehdit_senaryosu": aile}
    kfg = DS.konfig(kol="anatomi", senaryo=f"{kol}-{sinif}", tohum=tohum,
                    trafik_deseni="yere_toplama", **ek, **pencere,
                    **_konfig_farklari(farklar))
    kur = kurulum_yap(kfg)
    kar = kur.kanal.karistirici
    acilma = kfg.karistirici_baslangic_s
    uyeler = getattr(kar, "uyeler", (kar,)) if kar is not None else ()
    bas_s, bitis_s = kfg.olcum_penceresi
    ed_w = dbm_to_w(kfg.ed_esigi_dbm)

    # ---------------------------------------------------- kayıt tabloları
    mesgul: defaultdict = defaultdict(float)        # (düğüm, dilim) → s
    hava: defaultdict = defaultdict(float)          # çözülen hava süresi
    cozulen: Counter = Counter()                    # (düğüm, dilim)
    son_cozum: dict[tuple[int, int], float] = {}    # dilimdeki son çözüm
    phy: Counter = Counter()
    rssi_top: defaultdict = defaultdict(float)      # (alıcı, gönderen, dilim)
    rssi_n: Counter = Counter()
    mac: list[tuple[int, int, bool, int, float]] = []
    selam_gonder: list[tuple[int, int, float]] = []  # (gönderen, sıra, t)
    selam_al: dict[tuple[int, int, int], float] = {}  # (alıcı, gön., sıra)
    selam_duyma: defaultdict = defaultdict(list)     # (alıcı, gön.) → t
    kararlar: Counter = Counter()

    asil_mesgul = Dugum.mesgul_guncelle
    asil_phy = Dugum.phy_hata_say
    asil_karar = Dugum.sonraki_atlama
    asil_bitti = AliciZinciri.cerceve_bitti
    asil_sonuc = kontrol.iletim_sonucu
    asil_hello_kur = Babel._hello_kur
    asil_hello_al = Babel._hello_al

    def mesgul_sar(self, t_s):
        """`Dugum.mesgul_guncelle`in AYNISI (aynı sınırlar, aynı orta nokta
        okuması); meşgul parçalar dilimlere de yazılır."""
        if not self._doluluk:
            return
        bas = self._mesgul_son_s
        if t_s <= bas:
            return
        self._mesgul_son_s = t_s
        sinirlar = {bas, t_s}
        k = self.kur.kanal.karistirici
        if k is not None:
            sinirlar.update(k.gecis_anlari(bas, t_s))
            if k.hareketli:
                adim = self.kur.konfig.karistirici_denetim_araligi_s
                sinirlar.update(bas + i * adim
                                for i in range(1, int((t_s - bas) / adim) + 1))
        s = sorted(a for a in sinirlar if bas <= a <= t_s)
        for a, b in zip(s, s[1:]):
            if b > a and self.kanal_mesgul_mu(0.5 * (a + b)):
                self._mesgul_toplam_s += b - a
                dagit(mesgul, self.kimlik, a, b)

    def phy_sar(self):
        phy[(self.kimlik, int(self.kur.olaylar.simdi // DILIM_S))] += 1
        return asil_phy(self)

    def karar_sar(self, paket, t_s):
        karar = asil_karar(self, paket, t_s)
        if karar.sonraki is not None:
            kararlar[(self.kimlik, int(karar.sonraki))] += 1
        return karar

    def bitti_sar(self, iletim, t_s):
        s = asil_bitti(self, iletim, t_s)
        if s is not None and s.basarili:
            n = self.dugum
            dilim = int(t_s // DILIM_S)
            dagit(hava, n, t_s - iletim.cerceve.sure_s, t_s)
            cozulen[(n, dilim)] += 1
            if son_cozum.get((n, dilim), -1.0) < t_s:
                son_cozum[(n, dilim)] = t_s
            # `kontrol.cerceve_duyuldu`nun formülü (durumsuz hash çekimi).
            g = iletim.gonderen
            hata_db = kfg.rssi_olcum_sigma_db * normal_cekimi(
                "kanal_karar", kfg.tohum, g, n,
                int(t_s / kfg.kanal_dilimi_s), "rssi")
            rssi = round(10.0 * math.log10(s.guc_w * 1e3) + hata_db)
            rssi_top[(n, g, dilim)] += rssi
            rssi_n[(n, g, dilim)] += 1
        return s

    def sonuc_sar(kosu, d, hedef, basarili, deneme, tur):
        if hedef is not None:
            mac.append((d.kimlik, int(hedef), bool(basarili), int(deneme),
                        kosu.olaylar.simdi))
        return asil_sonuc(kosu, d, hedef, basarili, deneme, tur)

    def hello_kur_sar(self, simdi):
        tlv = asil_hello_kur(self, simdi)
        selam_gonder.append((self.kimlik, self._hello_sira, simdi))
        return tlv

    def hello_al_sar(self, n, h, simdi):
        selam_al[(self.kimlik, n, h.sira)] = simdi
        selam_duyma[(self.kimlik, n)].append(simdi)
        return asil_hello_al(self, n, h, simdi)

    Dugum.mesgul_guncelle = mesgul_sar
    Dugum.phy_hata_say = phy_sar
    Dugum.sonraki_atlama = karar_sar
    AliciZinciri.cerceve_bitti = bitti_sar
    kontrol.iletim_sonucu = sonuc_sar
    Babel._hello_kur = hello_kur_sar
    Babel._hello_al = hello_al_sar
    try:
        kosu = Kosu(kur, _fabrika(protokol, kfg))
        for d in kosu.dugumler:
            d._doluluk = True
        kosu.kostur()
        for d in kosu.dugumler:
            d.mesgul_guncelle(kfg.kosu_bitis_s)
    finally:
        Dugum.mesgul_guncelle = asil_mesgul
        Dugum.phy_hata_say = asil_phy
        Dugum.sonraki_atlama = asil_karar
        AliciZinciri.cerceve_bitti = asil_bitti
        kontrol.iletim_sonucu = asil_sonuc
        Babel._hello_kur = asil_hello_kur
        Babel._hello_al = asil_hello_al

    satir = sonuc_satiri(kur, kosu.dugumler, protokol)
    kr = satir["korunum"]
    m = satir["metrikler"]
    sayac = {k: v for k, v in kur.sayaclar.disa_ver().items()
             if isinstance(v, (int, float)) and not isinstance(v, bool)}
    # --- (1) koşu içi eşitlikler ----------------------------------------
    mesgul_dugum = sum(d._mesgul_toplam_s for d in kosu.dugumler)
    dogrula(abs(sum(mesgul.values()) - mesgul_dugum)
            <= 1e-6 * max(1.0, mesgul_dugum),
            f"dilimlere yazılan meşgul süresi {sum(mesgul.values())} ≠ "
            f"düğümlerin toplamı {mesgul_dugum}")
    dogrula(sum(cozulen.values()) == sayac.get("alim_basarili", 0),
            f"kaydedilen çözüm {sum(cozulen.values())} ≠ sayaç "
            f"{sayac.get('alim_basarili')}")
    dogrula(sum(phy.values()) == sayac.get("alim_red_per", 0),
            f"kaydedilen CRC hatası {sum(phy.values())} ≠ sayaç "
            f"{sayac.get('alim_red_per')}")

    # --- etiketler (yalnız değerlendirme) -------------------------------
    alan_onbellek: dict[tuple[int, int], str] = {}

    def alan(n: int, dilim: int) -> str:
        a = alan_onbellek.get((n, dilim))
        if a is None:
            a = alan_onbellek[(n, dilim)] = _etki_alani(
                kur, n, (dilim + 0.5) * DILIM_S, ed_w)
        return a

    evre_onbellek: dict[int, str] = {}

    def devrede(t_s: float) -> bool:
        return any(u.devrede_mi(t_s) for u in uyeler)

    def evre(dilim: int) -> str:
        """🔴 16 Kasım (duman): sürekli sınıfın `gecis_anlari`'ı boş döner;
        geçiş, dilimin başı · ortası · sonu örneklenerek sezilir."""
        e = evre_onbellek.get(dilim)
        if e is not None:
            return e
        a, b = dilim * DILIM_S, (dilim + 1) * DILIM_S
        if kar is None:
            e = "ikiz"
        elif b <= acilma:
            e = "once"
        elif a < acilma:
            e = "gecis"
        else:
            durum = {devrede(a + 1e-6), devrede(a + 0.5 * DILIM_S),
                     devrede(b - 1e-6)}
            e = ("gecis" if len(durum) > 1 else
                 "acik" if durum.pop() else "sessiz")
        evre_onbellek[dilim] = e
        return e

    def gecis_ani(sol: float, sag: float) -> float:
        """`devrede` durumunun `sol`la `sag` arasında değiştiği an."""
        ilk_durum = devrede(sol)
        for _ in range(40):
            orta = 0.5 * (sol + sag)
            if devrede(orta) == ilk_durum:
                sol = orta
            else:
                sag = orta
        return sag

    def sinif_(n: int, dilim: int) -> str | None:
        e = evre(dilim)
        if e == "gecis":
            return None
        return "ikiz" if e == "ikiz" else f"{e}|{alan(n, dilim)}"

    N = kfg.dugum_sayisi
    ilk = int(math.ceil(bas_s / DILIM_S - 1e-9))
    son = int(math.floor(bitis_s / DILIM_S + 1e-9))      # [ilk, son)

    # --- S1a · düğüm-saniye ---------------------------------------------
    # Selam kaybı: tanıdık komşunun her selamı beklenir.
    for dizi in selam_duyma.values():
        dizi.sort()
    duyanlar: defaultdict = defaultdict(set)             # gönderen → alıcılar
    for (i, j) in selam_duyma:
        duyanlar[j].add(i)
    beklenen: Counter = Counter()                        # (alıcı, dilim)
    kacan: Counter = Counter()
    for j, sira, t in selam_gonder:
        for i in duyanlar[j]:
            dizi = selam_duyma[(i, j)]
            k = bisect.bisect_left(dizi, t)
            if k == 0 or dizi[k - 1] < t - TANIDIK_S:
                continue                                 # tanıdık değil
            dilim = int(t // DILIM_S)
            beklenen[(i, dilim)] += 1
            if (i, j, sira) not in selam_al:
                kacan[(i, dilim)] += 1

    hist: dict[str, dict[str, Counter]] = defaultdict(
        lambda: defaultdict(Counter))
    birim_n: Counter = Counter()
    pencere_dilim = int(round(SELAM_PENCERE_S / DILIM_S))
    for n in range(N):
        son_t = -math.inf
        for dilim in range(0, son):
            if (n, dilim) in son_cozum:
                son_t = max(son_t, son_cozum[(n, dilim)])
            if dilim < ilk:
                continue
            s = sinif_(n, dilim)
            if s is None:
                continue
            birim_n[s] += 1
            h = hist[s]
            m_s = mesgul.get((n, dilim), 0.0)
            h["mesgul"][kutu("mesgul", m_s / DILIM_S)] += 1
            h["aciklanamayan"][kutu("aciklanamayan", max(
                0.0, m_s - hava.get((n, dilim), 0.0)) / DILIM_S)] += 1
            h["phy"][kutu("phy", phy.get((n, dilim), 0))] += 1
            h["cozulen"][kutu("cozulen", cozulen.get((n, dilim), 0))] += 1
            h["sessizlik"][kutu("sessizlik", min(
                SESSIZLIK_TAVAN_S, (dilim + 1) * DILIM_S - son_t))] += 1
            bek = sum(beklenen.get((n, dilim - q), 0)
                      for q in range(pencere_dilim))
            if bek:
                kac = sum(kacan.get((n, dilim - q), 0)
                          for q in range(pencere_dilim))
                h["selam_kaybi"][kutu("selam_kaybi", kac / bek)] += 1
            else:
                h["selam_kaybi"]["yok"] += 1

    # --- MAC olayları: bağ başına zaman sırası --------------------------
    mac.sort(key=lambda x: x[4])
    bag_olay: defaultdict = defaultdict(list)            # (i, j) → [(t, b, d)]
    for i, j, b, d, t in mac:
        bag_olay[(i, j)].append((t, b, d))

    # --- S1b · bağ × 5 s: deneme başarısı × RSSI ------------------------
    oran = int(round(BAG_DILIM_S / DILIM_S))
    rssi_pencere = int(round(RSSI_PENCERE_S / DILIM_S))
    bag_hist: dict[str, Counter] = defaultdict(Counter)
    for (i, j), olaylar in bag_olay.items():
        grup: defaultdict = defaultdict(list)
        for t, b, d in olaylar:
            grup[int(t // BAG_DILIM_S)].append((b, d))
        for q, liste in grup.items():
            if len(liste) < BAG_EN_AZ_CERCEVE:
                continue
            dilimler = range(q * oran, (q + 1) * oran)
            if dilimler[0] < ilk or dilimler[-1] >= son:
                continue
            siniflar = {sinif_(j, k) for k in dilimler}
            if None in siniflar or len({evre(k) for k in dilimler}) != 1:
                continue
            s = sinif_(j, q * oran + oran // 2)
            basari = sum(b for b, _ in liste)
            deneme = sum(d for _, d in liste)
            teslim = min(TESLIM_KUTU - 1, int(basari / deneme * TESLIM_KUTU))
            son_k = (q + 1) * oran
            top = sum(rssi_top.get((i, j, k), 0.0)
                      for k in range(son_k - rssi_pencere, son_k))
            say = sum(rssi_n.get((i, j, k), 0)
                      for k in range(son_k - rssi_pencere, son_k))
            bag_hist[s][f"{teslim}|{rssi_kutusu(top / say if say else None)}"
                        ] += 1

    # --- S2 · vazgeçme dizileri, çerçeve başına deneme, tespit süresi ---
    dizi_hist: dict[str, Counter] = defaultdict(Counter)
    cerceve_n: Counter = Counter()
    deneme_hist: dict[str, Counter] = defaultdict(Counter)
    for (i, j), olaylar in bag_olay.items():
        for t, b, d in olaylar:
            dilim = int(t // DILIM_S)
            if not ilk <= dilim < son:
                continue
            s = sinif_(j, dilim)
            if s is None:
                continue
            cerceve_n[s] += 1
            deneme_hist[s][min(DENEME_TAVAN, d)] += 1
        sonuclar = [b for _, b, _ in olaylar]
        for k, uzunluk in vazgecme_dizileri(sonuclar):
            dilim = int(olaylar[k][0] // DILIM_S)
            if not ilk <= dilim < son:
                continue
            s = sinif_(j, dilim)
            if s is not None:
                dizi_hist[s][min(DIZI_TAVAN, uzunluk)] += 1

    # Açık dönemler "açık" dilimlerden kurulur; uçlar ikiye bölmeyle tam
    # bulunur (`gecis_anlari` sürekli sınıfta boş).
    acik_donemler: list[tuple[float, float]] = []
    if kar is not None:
        k = ilk
        while k < son:
            if evre(k) != "acik":
                k += 1
                continue
            k0 = k
            while k < son and evre(k) == "acik":
                k += 1
            if devrede((k0 - 1) * DILIM_S):
                continue                    # pencereden önce başlamış dönem
            a = gecis_ani((k0 - 1) * DILIM_S, k0 * DILIM_S + 1e-6)
            b = (son * DILIM_S if k >= son
                 else gecis_ani(k * DILIM_S - 1e-6, (k + 1) * DILIM_S))
            acik_donemler.append((a, b))
    gecikme: dict[str, dict[str, list]] = defaultdict(
        lambda: defaultdict(list))
    for a, b in acik_donemler:
        dilim = int(a // DILIM_S)
        for (i, j), olaylar in bag_olay.items():
            al = alan(j, dilim)
            if al == "uzak":
                continue
            onceki = any(a - ONCEKI_BASARI_S <= t < a and bb
                         for t, bb, _ in olaylar)
            sonra = any(a <= t < b for t, _, _ in olaylar)
            if not (onceki and sonra):
                continue
            ikili = [(t, bb) for t, bb, _ in olaylar]
            for n in GECIKME_N:
                g = nci_vazgecme(ikili, a, b, n)
                gecikme[al][str(n)].append(None if g is None else round(g, 2))

    # --- S3 · bağ kalitesinin değişim hızı (kâhin; yalnız ikiz) ---------
    s3 = None
    if kar is None:
        grafik = KanalGrafigi(kur)
        dnm = kfg.yeniden_deneme_siniri + 1
        secilen = [b for b, v in kararlar.most_common(S3_BAG_SAYISI)
                   if v >= S3_EN_AZ_KARAR]
        bant_degisti: Counter = Counter()
        fark_top: defaultdict = defaultdict(float)
        cift: Counter = Counter()

        def bant(p: float) -> int:
            return 0 if p >= 0.90 else (1 if p >= 0.50 else 2)

        for (i, j) in secilen:
            seri = [1.0 - (1.0 - grafik._tek_deneme_basarisi(
                i, j, (k + 0.5) * DILIM_S)) ** dnm for k in range(ilk, son)]
            for tau in S3_GECIKMELER:
                for a, b in zip(seri, seri[tau:]):
                    cift[tau] += 1
                    bant_degisti[tau] += bant(a) != bant(b)
                    fark_top[tau] += abs(a - b)
        s3 = {"bag": len(secilen),
              "bant_degisim": {str(t): bant_degisti[t] / cift[t]
                               for t in S3_GECIKMELER if cift[t]},
              "ort_fark": {str(t): fark_top[t] / cift[t]
                           for t in S3_GECIKMELER if cift[t]}}

    def sozluk(c: Counter) -> dict:
        return {str(k): v for k, v in sorted(c.items(), key=lambda x: str(x[0]))}

    return {"protokol": etiket, "tohum": tohum, "gecerli": kr["gecerli"],
            "pdr": m["pdr"], "pdr_pencere": m["pdr_pencere"],
            "pdr_acik_satir": m.get("pdr_acik"),
            "uretilen": kr["uretilen"], "teslim": kr["teslim"],
            "sayaclar": sayac,
            "dugum_saniye_n": dict(birim_n),
            "dugum_saniye": {s: {isaret: sozluk(c) for isaret, c in h.items()}
                             for s, h in hist.items()},
            "bag_teslim_rssi": {s: sozluk(c) for s, c in bag_hist.items()},
            "cerceve_n": dict(cerceve_n),
            "deneme": {s: sozluk(c) for s, c in deneme_hist.items()},
            "vazgecme_dizisi": {s: sozluk(c) for s, c in dizi_hist.items()},
            "acik_donem": len(acik_donemler),
            "tespit_gecikmesi_s": {a: dict(v) for a, v in gecikme.items()},
            "s3": s3,
            "denetim": {"mesgul_s": round(mesgul_dugum, 3),
                        "cozulen": sum(cozulen.values()),
                        "phy": sum(phy.values()), "mac_olay": len(mac),
                        "selam_gonderilen": len(selam_gonder),
                        "selam_alinan": len(selam_al)},
            "sure_s": round(time.perf_counter() - t0, 1)}


def _arg(argv: list[str], ad: str, varsayilan: str) -> str:
    if ad in argv:
        i = argv.index(ad)
        deger = argv[i + 1]
        del argv[i:i + 2]
        return deger
    return varsayilan


def main() -> int:
    DS.secimi_oku()
    argv = sys.argv[1:]
    kisa = "--kisa" in argv
    if kisa:
        argv.remove("--kisa")
    kol = _arg(argv, "--kol", "formasyon")
    aile = _arg(argv, "--aile", "derin_sizma")
    sinif = _arg(argv, "--sinif", "surekli")
    dogrula(sinif in ("surekli", "yok"), f"sinif surekli|yok: {sinif!r}")
    protokoller = _arg(argv, "--protokoller", "babel").split(",")
    tohumlar = [int(t) for t in _arg(argv, "--tohumlar", "1003").split(",")]
    isci = int(_arg(argv, "--isci", "8"))
    kayit_yolu = _arg(argv, "--kayit", "")
    dogrula(not argv, f"tanınmayan argüman: {argv}")
    dogrula(not any(2000 <= t <= 2039 for t in tohumlar),
            "ana deney tohumları (2000–2039) mühürden önce koşulmaz")
    print("=" * 78)
    print(f"KARISTIRMA ISARETLERI — dunya {DS.secili()} · {kol}-{sinif} · "
          f"aile {aile if sinif != 'yok' else '—'} · tohum {tohumlar}"
          f"{' · KISA PENCERE' if kisa else ''}")
    print("=" * 78)
    isler = [(p, t, kol, aile, kisa, sinif) for p in protokoller
             for t in tohumlar]
    # K-198 gibi: her koşu biter bitmez ara kayda; kesintiden sonra sürer.
    ara = Path(kayit_yolu + "l") if kayit_yolu.endswith(".json") else (
        Path(kayit_yolu + ".jsonl") if kayit_yolu else None)
    sonuc: list[dict] = []
    if ara is not None and ara.exists():
        for satir in ara.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                r = json.loads(satir)
                if "hata" not in r:
                    sonuc.append(r)
        bitti = {(r["protokol"], r["tohum"]) for r in sonuc}
        isler = [i for i in isler if (i[0], i[1]) not in bitti]
        print(f"  ara kayıttan {len(sonuc)} koşu okundu, {len(isler)} koşu "
              f"kaldı ({ara})", flush=True)
    hatalar = 0
    if isler:
        with Pool(min(isci, len(isler))) as havuz:
            for n, r in enumerate(havuz.imap_unordered(_is_guvenli, isler,
                                                       chunksize=1), 1):
                if ara is not None:
                    with ara.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                if "hata" in r:
                    hatalar += 1
                    print(f"  HATA {n}/{len(isler)} {r['protokol']} "
                          f"{r['tohum']}: {r['hata']}\n{r['iz']}", flush=True)
                    continue
                sonuc.append(r)
                print(f"  {n:>3}/{len(isler)} {r['protokol']:<42} "
                      f"{r['tohum']} · PDR(pencere) {r['pdr_pencere']:.4f} · "
                      f"{r['sure_s']:.0f} s · {r['denetim']}", flush=True)
    if kayit_yolu:
        Path(kayit_yolu).write_text(
            json.dumps({"dunya": DS.secili(), "kol": kol, "sinif": sinif,
                        "aile": aile, "kisa": kisa, "sonuc": sonuc},
                       ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  {len(sonuc)} koşu · {hatalar} hata")
    return 1 if hatalar else 0


if __name__ == "__main__":
    raise SystemExit(main())
