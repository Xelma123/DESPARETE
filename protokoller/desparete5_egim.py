"""
DESPARETE 5 · rota seçimi ve döngü bekçisi — KK-04 (19 Kasım; T-11 · T-12 ·
T-13 · T-14 · T-15 · T-17).

Saf modül; `egim` bayrağı açıkken `Rota`nın (18 Kasım'ın KK-04'ü,
`desparete5_rota.py`) yerine geçer ve aynı arayüzü verir. Tek hedef geçittir.
Bağların durumu, maliyeti ve "veriye uygun değil" işareti KK-01'in
tablosundan (`BagTablosu`) okunur.

🔒 DÖNGÜ ÖNLENMEZ, YAKALANIR (T-12; CTP [68], RPL [63])
Ardıl, olağan ve sonlu ilanlı komşular arasında en ucuz yoldur; önce
maliyeti benim son ilan ettiğimden küçük ("yokuş aşağı") komşulara bakılır,
yoksa son çare. Döngüsüzlük garanti değildir. Döngü veri yolunda iki yoldan
yakalanır, başlığa değer yazılmaz (`13` §02.5):
  · bayat bilgi: veri getiren komşunun ilanı benim maliyetimden büyük değil
    → selam (KK-04/8);
  · kesin döngü: aynı paket daha büyük atlama sayısıyla geri geldi → iki
    komşu kısa süre dışlanır, ardıl yeniden seçilir, selam (KK-04/9).

🔒 TUR YOK (T-13): selamda tur alanı yok (`SELAM_E`), tur isteği yok, FD yok.

🔒 DÖNGÜNÜN KURULMASI ZORLAŞTIRILIR (20 Kasım; RPL [63] §11.1, §8.2.2.4)
  · geri gönderme yasağı (`geri_yasagi`, KK-04/13): ardıl, paketi bana
    getiren komşuysa o paket D'deki başka bir adaya gider, yoksa bekletilir
    (`geri_alternatif`; karar `Desparete5.sonraki_atlama`da);
  · sınırlı yükselme (`sinirli_yukselme`, KK-04/14): maliyetim, son
    `YUKSELME_UNUT_S` içinde ilan ettiğim en küçük sonlu maliyetin (L)
    `YUKSELME_PAYI` fazlasını aşamaz; ∞ ilanından sonra yokuş aşağının ölçütü
    L'dir. İkisi kapalıyken davranış 19 Kasım'ınkidir.
"""

from __future__ import annotations

import math
from collections import deque

from protokoller.desparete5_bicim import (
    SONSUZ, Bayraklar, Degerler, maliyet_topla)

__all__ = ["Egim"]

_INF = math.inf


class _Animsa:
    """Süreli kayıt: anahtar → değer; `sure`den yaşlı kayıt silinir.
    Kayıtlar zaman sırasıyla eklendiği için budama kuyruğun başından yapılır."""

    __slots__ = ("sure", "kayit", "kuyruk")

    def __init__(self, sure: float) -> None:
        self.sure = sure
        self.kayit: dict = {}
        self.kuyruk: deque = deque()        # (t, anahtar)

    def yaz(self, anahtar, deger, t: float) -> None:
        self.kayit[anahtar] = (deger, t)
        self.kuyruk.append((t, anahtar))

    def oku(self, anahtar, t: float):
        k = self.kayit.get(anahtar)
        if k is None or t - k[1] > self.sure:
            return None
        return k[0]

    def buda(self, t: float) -> None:
        alt = t - self.sure
        q = self.kuyruk
        while q and q[0][0] < alt:
            te, anahtar = q.popleft()
            k = self.kayit.get(anahtar)
            if k is not None and k[1] == te:
                del self.kayit[anahtar]


class Egim:
    """Bir düğümün geçide rotası — KK-04 (19 Kasım)."""

    __slots__ = ("d", "b", "kimlik", "gecit_mi", "ilanlar", "ardil", "C",
                 "son_ilan_C", "ms", "disla", "gonderilen", "getiren",
                 "olay", "_bayat_bildirildi", "sayac", "_yolsuz_t",
                 "_ilan_gecmisi")

    def __init__(self, kimlik: int, gecit: int, degerler: Degerler,
                 bayraklar: Bayraklar) -> None:
        self.d = degerler
        self.b = bayraklar
        self.kimlik = kimlik
        self.gecit_mi = kimlik == gecit
        self.ilanlar: dict[int, int] = {}            # j → C_j
        self.ardil: int | None = None
        self.C = 0 if self.gecit_mi else SONSUZ
        self.son_ilan_C: int | None = None           # C_ilan (KK-04)
        self.ms: dict[int, list[float]] = {}         # j → [ms_j, son güncelleme]
        self.disla: dict[int, float] = {}            # j → dışlamanın bitişi
        # KK-04/9: (kaynak, kaynak_sira) → (atlama sayısı, gönderdiğim komşu)
        self.gonderilen = _Animsa(degerler.DONGU_ANIMSA_S)
        # KK-04/9: (kaynak, kaynak_sira) → paketi bana getiren komşu
        self.getiren = _Animsa(degerler.DONGU_ANIMSA_S)
        self.olay = False                            # hemen selam (KK-02/3)
        self._bayat_bildirildi = False               # son selamdan beri
        self.sayac: dict[str, int] = {
            "ardil_degisti": 0, "zorunlu_gecis": 0, "istege_bagli_gecis": 0,
            "veri_gecis": 0, "son_care": 0, "yol_yok": 0, "yol_yok_bitti": 0,
            "yol_yok_sure_ms": 0, "tavan_asimi": 0, "bayat_bilgi": 0,
            "dongu": 0, "dislama": 0,
            # 20 Kasım (KK-04/13–14); karar başına
            "geri_yasagi": 0, "geri_bekletme": 0, "yukselme_kopma": 0,
        }
        self._yolsuz_t: float | None = None
        # KK-04/14: (an, ilan edilen sonlu maliyet), zaman sırasıyla
        self._ilan_gecmisi: deque = deque()

    # ------------------------------------------------------------------
    # İlanlar — KK-02/6–7
    # ------------------------------------------------------------------
    def ilan_al(self, j: int, t: float, tur, C: int) -> None:
        """Selamdan `C_j` (tur yok; 18 Kasım biçimi gelse de yok sayılır)."""
        self.ilanlar[j] = int(C)

    def ilan(self) -> tuple[int, int]:
        """Selamın (tur, maliyet) alanları; eğimde tur alanı yoktur, 0
        yalnız arayüzün biçimidir (`Desparete5` onu selama yazmaz)."""
        return 0, (0 if self.gecit_mi else self.C)

    def ilan_edildi(self, tur: int, C: int, t: float | None = None) -> None:
        """KK-02/7: ilan edilen (nicemlenmiş) maliyet `C_ilan` olur. Sonlu
        ilan, anıyla birlikte L'nin geçmişine yazılır (KK-04/14; `t`
        verilmezse yazılmaz)."""
        self.son_ilan_C = C
        self._bayat_bildirildi = False
        if t is not None and C < SONSUZ and not self.gecit_mi:
            self._ilan_gecmisi.append((float(t), int(C)))

    # ------------------------------------------------------------------
    # Sınırlı yükselme ve aday küme — KK-04/2–3, 14
    # ------------------------------------------------------------------
    def _L(self, t: float) -> int | None:
        """KK-04/14: son `YUKSELME_UNUT_S` içinde ilan ettiğim en küçük
        sonlu maliyet; bayrak kapalıysa ya da yoksa None."""
        if not self.b.sinirli_yukselme:
            return None
        q = self._ilan_gecmisi
        alt = t - self.d.YUKSELME_UNUT_S
        while q and q[0][0] < alt:
            q.popleft()
        return min((C for _, C in q), default=None)

    def _adaylar(self, baglar, L: int | None) -> tuple[dict, set]:
        """KK-04/2: aday küme `A` (j → m_j) ve yalnız sınırlı yükselme
        yüzünden dışarıda kalanlar. Durumu değiştirmez."""
        tavan = self.d.maliyet_tavani
        sinir = _INF if L is None else L + self.d.yukselme_payi
        A: dict[int, int] = {}
        sinir_disi: set[int] = set()
        for j in sorted(self.ilanlar):
            Cj = self.ilanlar[j]
            if (Cj >= SONSUZ or not baglar.kullanilir_mi(j)
                    or j in self.disla):
                continue
            m = maliyet_topla(baglar.maliyet(j), Cj)
            if m > tavan:
                continue                             # KK-04/10
            if m > sinir:
                sinir_disi.add(j)                    # KK-04/14
                continue
            A[j] = m
        return A, sinir_disi

    def _c_ref(self, L: int | None) -> int:
        """KK-04/3: yokuş aşağının ölçütü `C_ilan`; ∞ ilanından sonra
        (sınırlı yükselmede) L; ikisi de yoksa ∞ (`D = A`)."""
        C_ref = self.son_ilan_C if self.son_ilan_C is not None else SONSUZ
        if C_ref >= SONSUZ and L is not None:
            C_ref = L
        return C_ref

    # ------------------------------------------------------------------
    # Seçim — KK-04/1–7, 10–11
    # ------------------------------------------------------------------
    def sec(self, t: float, baglar, kendi_donuk: bool) -> None:
        """`baglar`: KK-01'in tablosu (`kullanilir_mi`, `maliyet`, `etx`,
        `durum`, `veriye_uygun`). `kendi_donuk` eğimde kullanılmaz
        (KK-04/12: seçim aynı kurallarla sürer)."""
        if self.gecit_mi:
            return
        d, b = self.d, self.b
        for j in [j for j in self.ilanlar if baglar.durum(j) is None]:
            del self.ilanlar[j]                      # silinen komşu
        for j in [j for j, s in self.disla.items() if s <= t]:
            del self.disla[j]
        L = self._L(t)
        A, sinir_disi = self._adaylar(baglar, L)
        # KK-04/6: düzgünleştirilmiş maliyet
        for j in [j for j in self.ms if j not in A]:
            del self.ms[j]
        for j, m in A.items():
            k = self.ms.get(j)
            if k is None:
                self.ms[j] = [float(m), t]
            else:
                dt = max(0.0, t - k[1])
                k[0] += (m - k[0]) * (1.0 - math.exp(-dt / d.DUZ_S))
                k[1] = t
        C_ref = self._c_ref(L)
        eski = self.ardil

        def uygun(j: int) -> bool:
            return baglar.veriye_uygun(j, t)

        D = [j for j in A if self.ilanlar[j] < C_ref]
        Dk = set(D)
        U = [j for j in A if j not in Dk]
        gruplar = ([j for j in D if uygun(j)], [j for j in D if not uygun(j)],
                   [j for j in U if uygun(j)], [j for j in U if not uygun(j)])

        def anahtar(j: int) -> tuple:
            # Eşitlikte: mevcut ardıl, düşük ETX, küçük adres (KK-04/4).
            return (A[j], 0 if j == eski else 1, baglar.etx(j), j)

        yeni, sebep, son_care = eski, None, False
        if eski is None or eski not in A:
            yeni = None
            for k, G in enumerate(gruplar):
                if G:
                    yeni = min(G, key=anahtar)
                    son_care = k >= 2
                    break
            sebep = "zorunlu" if eski is not None else None
            # Tanı: ardıl yalnız sınırlı yükselme yüzünden A'da değilse
            # yükselme kopması (KK-04/14); olağan, sonlu ilanlı ve
            # dışlanmamışken başka sebeple A'da değilse tavan (KK-04/10).
            if eski is not None and eski in sinir_disi:
                self.sayac["yukselme_kopma"] += 1
            elif (eski is not None
                    and self.ilanlar.get(eski, SONSUZ) < SONSUZ
                    and baglar.kullanilir_mi(eski)
                    and eski not in self.disla):
                self.sayac["tavan_asimi"] += 1
        elif not uygun(eski):
            adaylar = [j for j in gruplar[0] if j != eski]
            if adaylar:
                yeni = min(adaylar, key=anahtar)
                sebep = "veri"
        else:
            adaylar = [j for j in gruplar[0] if j != eski]
            m_a = A[eski]
            if b.duzgun_gecis:
                ms_a = self.ms[eski][0]
                gecen = [j for j in adaylar
                         if A[j] < m_a and self.ms[j][0] < ms_a]
            elif b.istege_bagli_esik:
                gecen = [j for j in adaylar
                         if A[j] < (1.0 - d.GECIS_ORANI) * m_a]
            else:
                gecen = [j for j in adaylar if A[j] < m_a]
            if gecen:
                yeni = min(gecen, key=anahtar)
                sebep = "istege"
        if yeni != eski:
            self.sayac["ardil_degisti"] += 1
            if sebep == "zorunlu":
                self.sayac["zorunlu_gecis"] += 1
            elif sebep == "veri":
                self.sayac["veri_gecis"] += 1
            elif sebep == "istege":
                self.sayac["istege_bagli_gecis"] += 1
            if son_care:
                self.sayac["son_care"] += 1
                self.olay = True                     # KK-04/7
            if yeni is None:
                self.sayac["yol_yok"] += 1
                self._yolsuz_t = t
            elif eski is None and self._yolsuz_t is not None:
                self.sayac["yol_yok_bitti"] += 1
                self.sayac["yol_yok_sure_ms"] += int(round(
                    (t - self._yolsuz_t) * 1000.0))
                self._yolsuz_t = None
        self.ardil = yeni
        self.C = SONSUZ if yeni is None else A[yeni]

    def kendi_bitti(self, t: float, baglar) -> None:
        self.sec(t, baglar, kendi_donuk=False)

    # ------------------------------------------------------------------
    # Döngü bekçisi — KK-04/8–9
    # ------------------------------------------------------------------
    def veri_duyuldu(self, gonderen: int, paket, t: float) -> None:
        """KK-04/8 (`cerceve_duyuldu`; niyet döndürmez): bana iletilmek
        üzere telemetri geldi. Göndereni kesin döngü için kaydedilir; ilanı
        benim maliyetimden büyük değilse bayat bilgi → değişim olayı."""
        if self.gecit_mi:
            return
        self.getiren.yaz((paket.kaynak, paket.kaynak_sira), gonderen, t)
        Cs = self.ilanlar.get(gonderen)
        if self.C >= SONSUZ or (Cs is not None and Cs <= self.C):
            if not self._bayat_bildirildi:
                self._bayat_bildirildi = True
                self.sayac["bayat_bilgi"] += 1
            self.olay = True

    def dongu_denetle(self, paket, t: float) -> None:
        """KK-04/9 (`sonraki_atlama`, seçimden önce): paket daha büyük
        atlama sayısıyla geri geldiyse iki komşu `DONGU_DISLA_S` süre
        dışlanır ve selam gider; seçim ardından yapılır."""
        if self.gecit_mi:
            return
        anahtar = (paket.kaynak, paket.kaynak_sira)
        onceki = self.gonderilen.oku(anahtar, t)
        if onceki is None or paket.atlama_sayisi <= onceki[0]:
            return                                   # yeni paket ya da MAC tekrarı
        self.sayac["dongu"] += 1
        dislanan = {onceki[1]}
        getiren = self.getiren.oku(anahtar, t)
        if getiren is not None:
            dislanan.add(getiren)
        for j in sorted(dislanan):
            self.disla[j] = t + self.d.DONGU_DISLA_S
            self.sayac["dislama"] += 1
        self.olay = True

    def gonderildi(self, paket, komsu: int, t: float) -> None:
        """KK-04/9: iletilen telemetri paketinin atlama sayısı ve komşusu."""
        self.gonderilen.yaz((paket.kaynak, paket.kaynak_sira),
                            (paket.atlama_sayisi, komsu), t)

    # ------------------------------------------------------------------
    # Geri gönderme yasağı — KK-04/13
    # ------------------------------------------------------------------
    def getiren_oku(self, paket, t: float) -> int | None:
        """Paketi bana getiren komşu (`cerceve_duyuldu`'nun kaydı)."""
        return self.getiren.oku((paket.kaynak, paket.kaynak_sira), t)

    def geri_alternatif(self, g: int, t: float, baglar) -> int | None:
        """KK-04/13: ardıl paketi getiren g iken bu paketin gideceği komşu:
        `D`'deki öteki adaylardan en iyisi (önce veriye uygun olanlar, G1;
        sonra G2); yoksa None (paket bekletilir). Yokuş yukarı aday
        kullanılmaz. Ardıl ve öteki durum değişmez; yalnız sayılır. Aynı
        anda `sec`ten sonra çağrılır."""
        L = self._L(t)
        A, _ = self._adaylar(baglar, L)
        C_ref = self._c_ref(L)
        D = [j for j in A if j != g and self.ilanlar[j] < C_ref]
        G = ([j for j in D if baglar.veriye_uygun(j, t)]
             or [j for j in D if not baglar.veriye_uygun(j, t)])
        if not G:
            self.sayac["geri_bekletme"] += 1
            return None
        self.sayac["geri_yasagi"] += 1
        return min(G, key=lambda j: (A[j], baglar.etx(j), j))

    # ------------------------------------------------------------------
    # Zaman ve 18 Kasım arayüzünün boş kalan parçaları
    # ------------------------------------------------------------------
    def zaman_isle(self, t: float, baglar, kendi_donuk: bool) -> None:
        self.gonderilen.buda(t)
        self.getiren.buda(t)
        q, alt = self._ilan_gecmisi, t - self.d.YUKSELME_UNUT_S
        while q and q[0][0] < alt:
            q.popleft()

    def son_tarih(self) -> float:
        return _INF

    def istek_al(self, g: int, t: float, istenen: int, kalan: int) -> None:
        """Tur isteği yok (T-13); eğimde böyle bir ileti gönderilmez."""
        return None

    def istekleri_al(self) -> list:
        return []

    def olay_oku(self) -> bool:
        o, self.olay = self.olay, False
        return o
