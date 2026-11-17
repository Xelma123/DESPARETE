"""
DESPARETE 5 · bağın durumu ve ölçüsü — KK-01 (T-2 · T-3 · T-7 · T-9 · İlke 2)
ve bağa ait karıştırma kanıtı — KK-03 B (kural 5–9).

Saf modül: simülatörü bilmez, yalnız zamanı (`t`, düğümün kendi saati) ve
olayları alır. Protokolün ana sınıfı her kancanın başında `zaman_isle(t)`yi,
sonra olayı (`selam_al`, `veri_sonucu`, `cerceve_duyuldu`) çağırır ve
`son_tarih()` ile bir sonraki uyanmayı kurar.

🔒 DÖRT DURUM (KK-01 "Durumlar")
    OLAĞAN          kullanılır, ölçülür
    ASKIDA          kullanılmaz, ölçülür; karıştırma kanıtı beklenir
    KÖTÜ            kullanılmaz, selamla ölçülür
    KARIŞTIRILIYOR  kullanılmaz, ölçü donar; kalite hatırlanır

🔒 AYNI OLAYDA SIRA (KK-01/15): önce karıştırma kanıtı (→ KARIŞTIRILIYOR),
sonra veri tetiği (→ ASKIDA), en son selam ETX'inin eşikleri. Kanıt önce
denendiği için "sondaki k sıfır" hiçbir zaman KÖTÜ'ye yol açmaz;
`karistirma_durumu` kapalıyken istisna yoktur, sessiz komşu ETX'ten KÖTÜ olur.

🔒 GÖLGE GEÇMİŞ (KK-03/2; Y-10): kendi karıştırılma durumumdaki selam kaybı
payı `s`, hiç dondurulmayan ayrı bir sayımdan okunur: kural 2–3'ün aynısı
(zaman aşımı, sıra boşluğu, geri alma), her olay anıyla.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field

from protokoller.desparete5_bicim import (
    ORAN_EN_COK, Bayraklar, Degerler, maliyet_birimi, sira_artir, sira_farki)

__all__ = ["OLAGAN", "ASKIDA", "KOTU", "KARISTIRILIYOR", "SEBEP_BIT",
           "SEBEP_SESSIZLIK", "Bag", "BagTablosu", "k_sessizlik",
           "sondaki_sifirsiz", "oran", "etx"]

OLAGAN, ASKIDA, KOTU, KARISTIRILIYOR = ("olagan", "askida", "kotu",
                                        "karistiriliyor")
SEBEP_BIT, SEBEP_SESSIZLIK = "bit", "sessizlik"
_SONSUZ = math.inf


# ==========================================================================
# Saf yardımcılar
# ==========================================================================
def oran(gecmis) -> float | None:
    """KK-01/4: `d_r` = 1'ler / örnek sayısı; boşsa tanımsız."""
    n = len(gecmis)
    return sum(gecmis) / n if n else None


def etx(d_f: float | None, d_r: float | None) -> float:
    """KK-01/5: 1 / (d_f · d_r); biri 0 ya da tanımsızsa ∞."""
    if not d_f or not d_r:
        return _SONSUZ
    return 1.0 / (d_f * d_r)


def sondaki_sifirsiz(gecmis) -> tuple[int, ...]:
    """Geçmişin sonundaki ardışık 0'lar atılmış hâli (sessizlikten önceki
    kalite; KK-01/9, KK-03/6)."""
    g = tuple(gecmis)
    i = len(g)
    while i and g[i - 1] == 0:
        i -= 1
    return g[:i]


def sondaki_sifir(gecmis) -> int:
    return len(gecmis) - len(sondaki_sifirsiz(gecmis))


def k_sessizlik(d_r: float | None, n: int) -> int:
    """KK-03/6: k = min(N, max(3, ⌈log 0,01 / log(1 − d_r)⌉)); `d_r`
    tanımsızsa k = N. Anlamı: bağın kendi kayıp oranıyla %1'den düşük
    olasılıkla açıklanabilecek sessizlik."""
    if d_r is None or d_r <= 0.0:
        return n
    if d_r >= 1.0:
        return 3
    x = math.log(0.01) / math.log(1.0 - d_r)
    return min(n, max(3, math.ceil(x - 1e-9)))


# ==========================================================================
# Bir komşu bağı — KK-01 "Tuttuğu"
# ==========================================================================
@dataclass(slots=True)
class Bag:
    komsu: int
    gecmis: deque                       # 1 geldi · 0 gelmedi; en yeni sonda
    beklenen: int                       # beklenen sıra
    son_selam_t: float                  # zaman aşımının ve MAC kanıtının dayanağı
    son_alim_t: float                   # gerçekten son alınan selam ("tanıdık")
    a: float                            # komşunun son ilan ettiği aralık
    asim_t: float                       # bir sonraki zaman aşımı (∞: donuk)
    son_duyulma_t: float                # komşudan çözülen son çerçeve
    d_f: float | None = None            # komşunun benim için bildirdiği oran
    d_f_t: float = -_SONSUZ             # beni son listelediği an (Y-12)
    veri: deque = field(default_factory=deque)   # (t, deneme, başarılı)
    durum: str = KOTU
    bit: bool = False                   # son selamdaki `karistiriliyorum`
    mac_ardisik: int = 0                # ardışık MAC vazgeçmesi (KK-03/7)
    dondurma_cikisi: bool = False       # sonraki selamda boşluk sayılmaz
    # ASKIDA
    askida_bitis_t: float = _SONSUZ
    askida_gecmis: tuple = ()
    askida_d_f: float | None = None
    # KARIŞTIRILIYOR
    sebepler: set = field(default_factory=set)
    hatira: tuple = ((), None)          # (geçmiş, d_f)
    karisma_t: float = _SONSUZ
    temiz_ardisik: int = 0              # bit = 0 olan ardışık selam
    # KÖTÜ ve ceza
    ceza_bitis_t: float = -_SONSUZ
    ceza_bekliyor: bool = False
    ceza_s: float = 0.0
    son_veri_kotu_t: float = -_SONSUZ
    # gölge geçmiş (KK-03/2; hiç donmaz)
    ham_beklenen: int = 0
    ham_asim_t: float = _SONSUZ
    ham_olay: deque = field(default_factory=deque)   # (t, 0|1)

    @property
    def d_r(self) -> float | None:
        return oran(self.gecmis)


# ==========================================================================
# Bağ tablosu
# ==========================================================================
class BagTablosu:
    """Bütün komşu bağları ve "kendim karıştırılıyorum" dondurması."""

    __slots__ = ("d", "b", "baglar", "kendi_donuk", "kendi_giris_t",
                 "degisti", "yeni_komsu", "sayac")

    def __init__(self, degerler: Degerler, bayraklar: Bayraklar) -> None:
        self.d = degerler
        self.b = bayraklar
        self.baglar: dict[int, Bag] = {}
        self.kendi_donuk = False         # KK-01/13 yürürlükte
        self.kendi_giris_t = _SONSUZ
        self.degisti = False             # kullanılabilirlik değişti
        self.yeni_komsu = False          # KK-02/3'ün olayı
        self.sayac: dict[str, int] = {
            "yeni_komsu": 0, "komsu_silindi": 0, "kotu_selam": 0,
            "kotu_donus": 0, "askida_giris": 0, "veri_kotu": 0,
            "karisma_bit": 0, "karisma_sessizlik": 0, "karisma_mac": 0,
            "karisma_kotuden": 0, "karisma_bitti": 0, "karisma_ust_sure": 0,
            "askida_kendi": 0, "df_bayat": 0,
        }

    # ------------------------------------------------------------------
    # Sorgular
    # ------------------------------------------------------------------
    def kullanilir_mi(self, j: int) -> bool:
        bag = self.baglar.get(j)
        return bag is not None and bag.durum == OLAGAN

    def kullanilir_kume(self) -> frozenset[int]:
        return frozenset(j for j, bag in self.baglar.items()
                         if bag.durum == OLAGAN)

    def durum(self, j: int) -> str | None:
        bag = self.baglar.get(j)
        return None if bag is None else bag.durum

    def etx(self, j: int) -> float:
        bag = self.baglar.get(j)
        return _SONSUZ if bag is None else etx(bag.d_f, bag.d_r)

    def maliyet(self, j: int) -> int:
        """Bağ maliyeti, ETX × 64 tamsayı (KK-00 genel kural 3)."""
        return maliyet_birimi(self.etx(j))

    def liste(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """Selamın komşu listesi (KK-02; Y-12): en az `ORNEK_EN_AZ` örneği
        olan komşular ve `d_r` × 255 (aşağı yuvarlanır), adrese göre."""
        komsu, deger = [], []
        for j in sorted(self.baglar):
            g = self.baglar[j].gecmis
            if len(g) >= self.d.ORNEK_EN_AZ:
                komsu.append(j)
                deger.append(int(math.floor(oran(g) * ORAN_EN_COK)))
        return tuple(komsu), tuple(deger)

    def selam_kaybi(self, t: float) -> float | None:
        """KK-03/2: `s` = Σ kaçan / Σ (gelen + kaçan), tanıdık komşular
        (son `TANIDIK_S`'de selamı alınmış) için son `KAYIP_PENCERE_S`'de,
        gölge geçmişten. Payda 0 ise tanımsız."""
        gelen = kacan = 0
        alt = t - self.d.KAYIP_PENCERE_S
        for j in sorted(self.baglar):
            bag = self.baglar[j]
            if bag.son_alim_t < t - self.d.TANIDIK_S:
                continue
            for te, v in bag.ham_olay:
                if alt < te <= t:
                    if v:
                        gelen += 1
                    else:
                        kacan += 1
        toplam = gelen + kacan
        return kacan / toplam if toplam else None

    def son_tarih(self) -> float:
        """En erken zaman olayı — protokolün bir sonraki uyanması."""
        en = _SONSUZ
        for bag in self.baglar.values():
            for te, _ in self._bekleyenler(bag):
                en = min(en, te)
        return en

    # ------------------------------------------------------------------
    # Zaman olayları — her biri kendi anında, sırayla
    # ------------------------------------------------------------------
    def _bekleyenler(self, bag: Bag) -> list[tuple[float, str]]:
        d = self.d
        olay: list[tuple[float, str]] = []
        if bag.asim_t < _SONSUZ:
            olay.append((bag.asim_t, "asim"))
        if bag.ham_asim_t < _SONSUZ:
            olay.append((bag.ham_asim_t, "ham"))
        if bag.durum == ASKIDA:
            olay.append((bag.askida_bitis_t, "askida"))
        elif bag.durum == KARISTIRILIYOR:
            olay.append((bag.karisma_t + d.T_HATIRA_S, "hatira"))
        elif bag.durum == KOTU and bag.ceza_bekliyor:
            olay.append((bag.ceza_bitis_t, "ceza"))
        if not self.kendi_donuk:
            olay.append((bag.son_duyulma_t + d.T_SILME_S, "silme"))
            if (bag.d_f is not None and bag.durum != KARISTIRILIYOR):
                olay.append((bag.d_f_t + d.T_SILME_S, "df"))
        return olay

    _ONCELIK = {"ham": 0, "asim": 1, "askida": 2, "hatira": 3, "ceza": 4,
                "df": 5, "silme": 6}

    def zaman_isle(self, t: float) -> None:
        for j in sorted(self.baglar):
            bag = self.baglar.get(j)
            while bag is not None:
                hazir = [(te, self._ONCELIK[ad], ad)
                         for te, ad in self._bekleyenler(bag) if te <= t]
                if not hazir:
                    break
                te, _, ad = min(hazir)
                if ad == "silme":
                    self._sil(j)
                    bag = None
                    continue
                getattr(self, "_z_" + ad)(bag, te)

    def _z_asim(self, bag: Bag, te: float) -> None:
        """KK-01/3: beklenen selam gelmedi → 0; sonra her `a`da bir 0."""
        bag.gecmis.append(0)
        bag.beklenen = sira_artir(bag.beklenen)
        bag.asim_t = te + bag.a
        # KK-01/15: önce kanıt (KK-03/6 sessizlik), sonra ETX eşiği.
        if self._sessizlik_kaniti(bag):
            self._karisma_gir(bag, te, SEBEP_SESSIZLIK)
        elif bag.durum == OLAGAN and self.etx(bag.komsu) > self.d.E_CIK:
            self._kotu(bag, te, cezali=False)
            self.sayac["kotu_selam"] += 1

    def _z_ham(self, bag: Bag, te: float) -> None:
        bag.ham_olay.append((te, 0))
        bag.ham_beklenen = sira_artir(bag.ham_beklenen)
        bag.ham_asim_t = te + bag.a
        self._ham_buda(bag, te)

    def _z_askida(self, bag: Bag, te: float) -> None:
        """KK-01/8: süre içinde kanıt gelmedi → KÖTÜ (veri sebepli)."""
        self._kotu(bag, te, cezali=True)

    def _z_hatira(self, bag: Bag, te: float) -> None:
        """KK-01/10 üst süre: "bitti" gelmeden `T_HATIRA` doldu → geçmiş
        boşaltılır, bağ KÖTÜ'den yeniden ölçülür (cezasız)."""
        bag.gecmis.clear()
        bag.sebepler.clear()
        bag.karisma_t = _SONSUZ
        bag.asim_t = bag.son_selam_t + self.d.ZAMAN_ASIMI_KATSAYI * bag.a
        self.sayac["karisma_ust_sure"] += 1
        self._kotu(bag, te, cezali=False)

    def _z_ceza(self, bag: Bag, te: float) -> None:
        bag.ceza_bekliyor = False
        self._kotu_donus(bag, te, bag.bit)

    def _z_df(self, bag: Bag, te: float) -> None:
        """Y-12: komşu beni `T_SILME` boyunca listelemedi → `d_f` tanımsız."""
        bag.d_f = None
        self.sayac["df_bayat"] += 1
        if bag.durum == OLAGAN:
            self._kotu(bag, te, cezali=False)
            self.sayac["kotu_selam"] += 1

    def _sil(self, j: int) -> None:
        """KK-01/14: `T_SILME` boyunca hiçbir çerçeve duyulmadı."""
        bag = self.baglar.pop(j)
        if bag.durum == OLAGAN:
            self.degisti = True
        self.sayac["komsu_silindi"] += 1

    # ------------------------------------------------------------------
    # Selam — KK-01/1–2 · KK-03/5, 9
    # ------------------------------------------------------------------
    def selam_al(self, j: int, t: float, sira: int, aralik_s: float,
                 bildirilen: float | None, bit: bool) -> None:
        """`bildirilen`: j'nin benim için bildirdiği oran; j beni
        listelemiyorsa `None` (Y-12: bilinmiyor, `d_f` değişmez)."""
        d, b = self.d, self.b
        bit = bool(bit) and b.karistirma_durumu and b.alici_bildirimi
        # Sıfır aralık zaman aşımını sonsuz döngüye sokardı; alanın birimi
        # 0,01 s, en küçük anlamlı değer de o.
        aralik_s = max(float(aralik_s), 0.01)
        bag = self.baglar.get(j)
        if bag is None:
            self._yeni(j, t, sira, aralik_s, bildirilen, bit)
            return
        bag.son_duyulma_t = t
        bag.son_alim_t = t
        self._ham_selam(bag, t, sira, aralik_s)
        if bildirilen is not None:
            bag.d_f_t = t
        # KK-01/15 · KK-03/5: kanıt önce — selam yazılmadan, hatıra bu
        # selamdan önceki ölçüden.
        if bit and bag.durum in (OLAGAN, ASKIDA):
            self._karisma_gir(bag, t, SEBEP_BIT)
        if bag.durum == KARISTIRILIYOR:
            self._izle(bag, t, sira, aralik_s, bit)
            bag.asim_t = _SONSUZ                 # ölçü donuk (KK-01/9)
            # KK-03/9: iki sebebin "bitti"si de bit = 0 olan 2 ardışık selam.
            if bit:
                bag.sebepler.add(SEBEP_BIT)
                bag.temiz_ardisik = 0
            else:
                bag.temiz_ardisik += 1
                if bag.temiz_ardisik >= 2:
                    self._karisma_cik(bag, t)
            return
        if self.kendi_donuk:                    # KK-01/13: yalnız izlenir
            self._izle(bag, t, sira, aralik_s, bit)
            bag.asim_t = _SONSUZ
            return
        self._gecmise_yaz(bag, sira)
        if bildirilen is not None:
            bag.d_f = bildirilen
        self._izle(bag, t, sira, aralik_s, bit)
        if bag.durum == OLAGAN and self.etx(j) > d.E_CIK:
            self._kotu(bag, t, cezali=False)
            self.sayac["kotu_selam"] += 1
        elif bag.durum == KOTU:
            self._kotu_donus(bag, t, bit)

    def _yeni(self, j: int, t: float, sira: int, aralik_s: float,
              bildirilen: float | None, bit: bool) -> None:
        """KK-01/1: ilk selamıyla kayda girer, KÖTÜ'de başlar (cezasız).
        Kendim karıştırılırken ilk örnek de yazılmaz (KK-01/13)."""
        bag = Bag(komsu=j, gecmis=deque(maxlen=self.d.N),
                  beklenen=sira_artir(sira), son_selam_t=t, son_alim_t=t,
                  a=aralik_s, asim_t=_SONSUZ, son_duyulma_t=t, bit=bit,
                  ham_beklenen=sira_artir(sira))
        bag.ham_olay.append((t, 1))
        bag.ham_asim_t = t + self.d.ZAMAN_ASIMI_KATSAYI * aralik_s
        if self.kendi_donuk:
            bag.dondurma_cikisi = True
        else:
            bag.gecmis.append(1)
            bag.asim_t = t + self.d.ZAMAN_ASIMI_KATSAYI * aralik_s
            if bildirilen is not None:
                bag.d_f, bag.d_f_t = bildirilen, t
        self.baglar[j] = bag
        self.yeni_komsu = True
        self.sayac["yeni_komsu"] += 1

    def _izle(self, bag: Bag, t: float, sira: int, aralik_s: float,
              bit: bool) -> None:
        """Her durumda: beklenen, son selam anı, aralık (KK-01/2 son madde)."""
        bag.beklenen = sira_artir(sira)
        bag.son_selam_t = t
        bag.a = aralik_s
        bag.bit = bit
        bag.asim_t = t + self.d.ZAMAN_ASIMI_KATSAYI * aralik_s

    def _gecmise_yaz(self, bag: Bag, sira: int) -> None:
        """KK-01/2 — ileri sarma, yeniden başlama, geri alma (RFC 8966
        Ek A; G-4: geç gelen selamda fazla sayılan bütün kayıtlar geri
        alınır) ve dondurmadan çıkış."""
        n = self.d.N
        g = bag.gecmis
        if bag.dondurma_cikisi:
            bag.dondurma_cikisi = False
            g.append(1)
            return
        fark = sira_farki(sira, bag.beklenen)
        if 0 <= fark <= n:
            g.extend([0] * fark)
        elif fark < 0 and -fark <= n:
            for _ in range(min(-fark, len(g))):
                g.pop()
        else:                                   # yeniden başlamış komşu
            g.clear()
        g.append(1)

    def _ham_selam(self, bag: Bag, t: float, sira: int,
                   aralik_s: float) -> None:
        """Gölge geçmiş (KK-03/2, Y-10): aynı kural, hiç donmaz; boşluğun
        0'ları bulunduğu anda, geri alma son 0'ları siler."""
        n = self.d.N
        fark = sira_farki(sira, bag.ham_beklenen)
        h = bag.ham_olay
        if 0 < fark <= n:
            h.extend([(t, 0)] * fark)
        elif fark < 0 and -fark <= n:
            for _ in range(-fark):
                if h and h[-1][1] == 0:
                    h.pop()
        h.append((t, 1))
        bag.ham_beklenen = sira_artir(sira)
        bag.ham_asim_t = t + self.d.ZAMAN_ASIMI_KATSAYI * aralik_s
        self._ham_buda(bag, t)

    def _ham_buda(self, bag: Bag, t: float) -> None:
        alt = t - self.d.KAYIP_PENCERE_S
        h = bag.ham_olay
        while h and h[0][0] <= alt:
            h.popleft()

    def cerceve_duyuldu(self, j: int, t: float) -> None:
        """KK-01/1: selamı olmayan çerçeve yalnız var olan kaydı tazeler."""
        bag = self.baglar.get(j)
        if bag is not None:
            bag.son_duyulma_t = t

    # ------------------------------------------------------------------
    # Veri sonucu — KK-01/6–7 · KK-03/7–8
    # ------------------------------------------------------------------
    def veri_sonucu(self, j: int, t: float, basarili: bool, tekrar: int,
                    tur: str) -> None:
        d, b = self.d, self.b
        bag = self.baglar.get(j)
        if bag is None or self.kendi_donuk:     # KK-01/13 · KK-03/8
            return
        if tur == "veri":
            bag.veri.append((t, tekrar + 1, bool(basarili)))
            while len(bag.veri) > d.VERI_PENCERE:
                bag.veri.popleft()
        bag.mac_ardisik = 0 if basarili else bag.mac_ardisik + 1
        if bag.durum not in (OLAGAN, ASKIDA):
            return
        # KK-01/15: önce kanıt (KK-03/7), sonra veri tetiği.
        if (b.karistirma_durumu and not basarili
                and bag.mac_ardisik >= d.MAC_ARDISIK
                and t - bag.son_selam_t > 2.0 * bag.a):
            self.sayac["karisma_mac"] += 1
            self._karisma_gir(bag, t, SEBEP_SESSIZLIK)
            return
        if (b.veri_kotu_tetigi and bag.durum == OLAGAN and tur == "veri"
                and self.etx_veri(bag, t) > d.E_CIK):
            self._askida_gir(bag, t)

    def etx_veri(self, bag: Bag, t: float) -> float:
        """KK-01/6: son `VERI_PENCERE` çerçevede (en çok 10 s geriye) en az
        `VERI_EN_AZ` varsa Σ deneme / Σ başarılı; başarı yoksa ∞."""
        alt = t - self.d.VERI_PENCERE_S
        kayit = [(n, ok) for te, n, ok in bag.veri if te >= alt]
        if len(kayit) < self.d.VERI_EN_AZ:
            return 0.0
        basari = sum(1 for _, ok in kayit if ok)
        return (sum(n for n, _ in kayit) / basari) if basari else _SONSUZ

    # ------------------------------------------------------------------
    # Geçişler
    # ------------------------------------------------------------------
    def _sessizlik_kaniti(self, bag: Bag) -> bool:
        """KK-03/6: geçmişin sonunda ardışık k sıfır (bağ OLAĞAN ya da
        ASKIDA, `karistirma_durumu` açık)."""
        if not self.b.karistirma_durumu or bag.durum not in (OLAGAN, ASKIDA):
            return False
        g = bag.gecmis
        k = k_sessizlik(oran(sondaki_sifirsiz(g)), self.d.N)
        return sondaki_sifir(g) >= k

    def _askida_gir(self, bag: Bag, t: float) -> None:
        """KK-01/7: veri denemeleri bağı kötü gösterdi; bağ hemen kullanımdan
        çıkar. `karistirma_durumu` kapalıyken bekleme yok (Y-4): doğrudan
        KÖTÜ ve ceza."""
        self.sayac["askida_giris"] += 1
        if not self.b.karistirma_durumu:
            self._kotu(bag, t, cezali=True)
            return
        d = self.d
        bag.askida_gecmis = tuple(bag.gecmis)
        bag.askida_d_f = bag.d_f
        k = k_sessizlik(oran(sondaki_sifirsiz(bag.gecmis)), d.N)
        sure = min(max((k + 1) * bag.a, d.ASKIDA_TABAN_S), d.ASKIDA_TAVAN_S)
        bag.askida_bitis_t = t + sure
        bag.durum = ASKIDA
        self.degisti = True

    def _karisma_gir(self, bag: Bag, t: float, sebep: str) -> None:
        """KK-01/9: OLAĞAN, ASKIDA (ya da Y-8 ile KÖTÜ) → KARIŞTIRILIYOR.
        Hatıra: ASKIDA'dan geliyorsa girişteki ölçü (Y-7), değilse bugünkü;
        ikisinde de sondaki 0'lar atılır."""
        if bag.durum == ASKIDA:
            hatira = (sondaki_sifirsiz(bag.askida_gecmis), bag.askida_d_f)
        else:
            hatira = (sondaki_sifirsiz(bag.gecmis), bag.d_f)
        if bag.durum == OLAGAN:
            self.degisti = True
        bag.hatira = hatira
        bag.veri.clear()
        bag.sebepler = {sebep}
        bag.karisma_t = t
        bag.temiz_ardisik = 0
        bag.askida_bitis_t = _SONSUZ
        bag.ceza_bekliyor = False
        bag.asim_t = _SONSUZ                     # ölçü donar
        bag.durum = KARISTIRILIYOR
        self.sayac["karisma_" + sebep] += 1

    def _karisma_cik(self, bag: Bag, t: float) -> None:
        """KK-01/10: bütün sebeplerin "bitti"si geldi. Hatıra geri yüklenir
        (`hatirlanan_kalite` kapalıysa geçmiş boşaltılır); hatıranın ETX'i
        `E_CIK`ı aşmıyorsa OLAĞAN, aşıyorsa KÖTÜ (cezasız)."""
        if self.b.hatirlanan_kalite:
            bag.gecmis = deque(bag.hatira[0], maxlen=self.d.N)
            bag.d_f = bag.hatira[1]
        else:
            bag.gecmis.clear()
        bag.sebepler.clear()
        bag.karisma_t = _SONSUZ
        bag.veri.clear()
        bag.dondurma_cikisi = True
        bag.asim_t = t + self.d.ZAMAN_ASIMI_KATSAYI * bag.a
        self.sayac["karisma_bitti"] += 1
        if etx(bag.d_f, bag.d_r) <= self.d.E_CIK:
            bag.durum = OLAGAN
            bag.ceza_bekliyor = False
            self.degisti = True
        else:
            self._kotu(bag, t, cezali=False)

    def _kotu(self, bag: Bag, t: float, cezali: bool) -> None:
        """KK-01/11: KÖTÜ'ye giriş. Veri sebepli girişte en az `T_CEZA`;
        önceki veri sebepli KÖTÜ'den beri 60 s geçmediyse süre ×2 (en çok
        40 s)."""
        d = self.d
        if bag.durum == OLAGAN:
            self.degisti = True
        bag.durum = KOTU
        bag.askida_bitis_t = _SONSUZ
        if cezali:
            if t - bag.son_veri_kotu_t < d.CEZA_YINELEME_S:
                bag.ceza_s = min(2.0 * bag.ceza_s, d.T_CEZA_EN_COK_S)
            else:
                bag.ceza_s = d.T_CEZA_S
            bag.son_veri_kotu_t = t
            bag.ceza_bitis_t = t + bag.ceza_s
            bag.ceza_bekliyor = True
            self.sayac["veri_kotu"] += 1
        else:
            bag.ceza_bekliyor = False
            bag.ceza_bitis_t = -_SONSUZ

    def _kotu_donus(self, bag: Bag, t: float, bit: bool) -> None:
        """KK-01/12: KÖTÜ → OLAĞAN, `ETX_selam < E_DON`, en az `ORNEK_EN_AZ`
        örnek ve ceza dolmuş. Y-8: o selamın biti 1 ise doğrudan
        KARIŞTIRILIYOR."""
        d = self.d
        if bag.durum != KOTU or bag.ceza_bekliyor or t < bag.ceza_bitis_t:
            return
        if len(bag.gecmis) < d.ORNEK_EN_AZ or self.etx(bag.komsu) >= d.E_DON:
            return
        if bit and self.b.karistirma_durumu and self.b.alici_bildirimi:
            self.sayac["karisma_kotuden"] += 1
            self._karisma_gir(bag, t, SEBEP_BIT)
            return
        bag.durum = OLAGAN
        self.degisti = True
        self.sayac["kotu_donus"] += 1

    # ------------------------------------------------------------------
    # Kendim karıştırılıyorum — KK-01/13 · Y-2 · Y-6
    # ------------------------------------------------------------------
    def kendi_basla(self, t: float) -> None:
        """Hiçbir komşunun geçmişine, `d_f`sine, verisine yazılmaz; zaman
        aşımı 0 eklemez; silme durur. Y-2: ASKIDA'daki bağ girişteki ölçüyle
        OLAĞAN'a döner, veri penceresi boşalır, ceza sayılmaz."""
        if not self.b.karistirma_durumu or self.kendi_donuk:
            return
        self.kendi_donuk = True
        self.kendi_giris_t = t
        for j in sorted(self.baglar):
            bag = self.baglar[j]
            bag.mac_ardisik = 0
            if bag.durum == ASKIDA:
                bag.gecmis = deque(bag.askida_gecmis, maxlen=self.d.N)
                bag.d_f = bag.askida_d_f
                bag.veri.clear()
                bag.askida_bitis_t = _SONSUZ
                bag.durum = OLAGAN
                self.degisti = True
                self.sayac["askida_kendi"] += 1
            if bag.durum != KARISTIRILIYOR:
                bag.asim_t = _SONSUZ

    def kendi_bitir(self, t: float) -> None:
        """Dondurma biter (durum bitti ya da Y-6'nın üst süresi doldu).
        Her komşunun son selam anı şimdiye çekilir, ilk selamında boşluk
        sayılmaz; silme süresi kaldığı yerden sürer."""
        if not self.kendi_donuk:
            return
        self.kendi_donuk = False
        gecen = t - self.kendi_giris_t
        for j in sorted(self.baglar):
            bag = self.baglar[j]
            if bag.son_duyulma_t >= self.kendi_giris_t:
                bag.son_duyulma_t = t
            else:
                bag.son_duyulma_t += gecen
            bag.mac_ardisik = 0
            bag.son_selam_t = t
            bag.dondurma_cikisi = True
            if bag.durum != KARISTIRILIYOR:
                bag.asim_t = t + self.d.ZAMAN_ASIMI_KATSAYI * bag.a
        self.kendi_giris_t = _SONSUZ

    # ------------------------------------------------------------------
    def bayraklari_oku(self) -> tuple[bool, bool]:
        """(kullanılabilirlik değişti mi, yeni komşu var mı) — okununca
        sıfırlanır."""
        sonuc = (self.degisti, self.yeni_komsu)
        self.degisti = self.yeni_komsu = False
        return sonuc
