"""
DESPARETE 5 · rota seçimi, döngüsüzlük, açlık — KK-04 (T-11 · T-12 · T-13 ·
T-14 · T-15).

Saf modül. Tek hedef geçittir. Bağların durumu ve maliyeti KK-01'in tablosundan
(`BagTablosu`) okunur; bu modül komşuların ilanlarını, uygulanabilirlik
uzaklığını (FD), ardılı, yok saymayı, açlıktaki tur isteğini ve iletilen
istekleri tutar.

🔒 DÖNGÜSÜZLÜK (RFC 8966 §3.5.1, §3.7.3)
Uygulanabilirlik her seçimde güncel FD ile hesaplanır, saklanmaz (B-9).
∞ ilan (geri çekme) her zaman uygulanabilirdir (B-1). FD, bu turda İLAN
ETTİĞİM sonlu maliyetlerin en küçüğüdür: hesapladığım değil, gönderdiğim
(T-12); selam kurulurken `ilan_edildi` ile güncellenir.

🔒 TUR YALNIZ İSTEKLE VE YALNIZ GEÇİTTE ARTAR (T-13; KK-04/10)
Geçidin turu 1'den başlar. Açlıkta istenen tur `FD.tur + 1`'dir; isteği
karşılayabilen ilk düğüm hemen selam gönderir, karşılayamayan ardılına iletir
ve yanıtı istek yolundan geri yaymak için kaydı `ISTEK_ANIMSA` tutar.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from protokoller.desparete5_bicim import (
    SONSUZ, Bayraklar, Degerler, maliyet_topla, sira_artir, sira_buyuk)

__all__ = ["Rota"]

_INF = math.inf


@dataclass(slots=True)
class _Aclik:
    """Açlıktaki tur isteği dizisi (KK-04/8)."""
    istenen: int
    kalan: int              # kalan yineleme
    sonraki_t: float        # sonraki yineleme
    dizi_t: float           # dizinin yeniden başlayacağı an


class Rota:
    """Bir düğümün geçide rotası."""

    __slots__ = ("d", "b", "kimlik", "gecit_mi", "tur_gecit", "ilanlar",
                 "ardil", "kabul", "C", "fd", "son_ilan_C", "yoksay_bitis",
                 "aclik", "iletilen", "giden", "olay", "sayac", "_aclik_t")

    def __init__(self, kimlik: int, gecit: int, degerler: Degerler,
                 bayraklar: Bayraklar) -> None:
        self.d = degerler
        self.b = bayraklar
        self.kimlik = kimlik
        self.gecit_mi = kimlik == gecit
        self.tur_gecit = 1                       # KK-04/10
        self.ilanlar: dict[int, tuple[int, int]] = {}   # j → (tur, C)
        self.ardil: int | None = None
        self.kabul: tuple[int, int] | None = None       # ardılın kabul edilen ilanı
        self.C = 0 if self.gecit_mi else SONSUZ
        self.fd: tuple[int, int] | None = None
        self.son_ilan_C: int | None = None
        self.yoksay_bitis = _INF                 # KK-04/7
        self.aclik: _Aclik | None = None
        # İletilen istekler (KK-04/9): istenen tur → [kaydın bitişi, son iletim]
        self.iletilen: dict[int, list[float]] = {}
        self.giden: list[tuple[int | None, int, int]] = []  # (hedef, istenen, kalan)
        self.olay = False                        # hemen selam (KK-02/3)
        self.sayac: dict[str, int] = {
            "ardil_degisti": 0, "zorunlu_gecis": 0, "istege_bagli_gecis": 0,
            "aclik": 0, "geri_cekme_alinan": 0, "uygulanamaz_yoksayilan": 0,
            "yoksay_doldu": 0, "aclik_istegi": 0, "yoksay_istegi": 0,
            "istek_yanitlanan": 0, "istek_iletilen": 0,
            "istek_bastirilan": 0, "istek_karsilandi": 0, "tur_artirildi": 0,
            # Tanı (KK-00 tanı kaydı; karara girmez): açlıktan çıkış sayısı
            # ve açlıkta geçen toplam süre — tur isteğinin gidiş-dönüşünün
            # üst sınırı.
            "aclik_bitti": 0, "aclik_sure_ms": 0,
        }
        self._aclik_t: float | None = None

    # ------------------------------------------------------------------
    # KK-04/1 · uygulanabilirlik
    # ------------------------------------------------------------------
    def uygulanabilir(self, tur: int, C: int) -> bool:
        if C >= SONSUZ:
            return True                          # geri çekme (RFC §3.5.1)
        if self.fd is None:
            return True
        fd_tur, fd_C = self.fd
        return sira_buyuk(tur, fd_tur) or (tur == fd_tur and C < fd_C)

    # ------------------------------------------------------------------
    # İlan alınınca — KK-02/6 · KK-04/7
    # ------------------------------------------------------------------
    def ilan_al(self, j: int, t: float, tur: int, C: int) -> None:
        self.ilanlar[j] = (tur, C)
        if self.gecit_mi or j != self.ardil:
            return
        if C >= SONSUZ:
            # ∞ yok sayılmaz: kabul edilir, seçim ardılı hemen bırakır.
            self.kabul = (tur, C)
            self.yoksay_bitis = _INF
            self.sayac["geri_cekme_alinan"] += 1
        elif self.uygulanabilir(tur, C):
            self.kabul = (tur, C)
            self.yoksay_bitis = _INF
        else:
            # Sonlu ve uygulanamaz: yok sayılır, ardıl son kabul edilen
            # ilanla kalır; ilk yok saymada ardıla tek alıcılı tur isteği
            # (RFC §3.5.3, §3.8.2.2). Sonraki yok saymalar süreyi yenilemez.
            self.sayac["uygulanamaz_yoksayilan"] += 1
            if self.yoksay_bitis == _INF:
                self.yoksay_bitis = t + self.d.ISTEK_ARA_S
                self.giden.append((j, self._istenen(), self.d.ISTEK_ATLAMA))
                self.sayac["yoksay_istegi"] += 1

    def _istenen(self) -> int:
        """İstenen tur: FD'nin turunun bir fazlası (RFC §3.8.2.1)."""
        return sira_artir(self.fd[0] if self.fd is not None else 0)

    # ------------------------------------------------------------------
    # Seçim — KK-04/2–5, 8
    # ------------------------------------------------------------------
    def sec(self, t: float, baglar, kendi_donuk: bool) -> None:
        """`baglar`: KK-01'in tablosu (`kullanilir_mi`, `maliyet`, `etx`,
        `durum`). `kendi_donuk`: kendi "karıştırılıyorum" dondurmam
        sürüyor (KK-04/8: istek gitmez)."""
        if self.gecit_mi:
            return
        for j in [j for j in self.ilanlar if baglar.durum(j) is None]:
            del self.ilanlar[j]                  # silinen komşu
        aday: dict[int, tuple] = {}
        for j in sorted(self.ilanlar):
            if not baglar.kullanilir_mi(j):
                continue
            tur, C = (self.kabul if j == self.ardil and self.kabul is not None
                      else self.ilanlar[j])
            if C >= SONSUZ or not self.uygulanabilir(tur, C):
                continue
            maliyet = maliyet_topla(baglar.maliyet(j), C)
            if maliyet >= SONSUZ:
                continue
            aday[j] = (maliyet, baglar.etx(j), tur, C)
        eski = self.ardil

        def anahtar(j: int) -> tuple:
            # Eşit maliyette: mevcut ardıl, düşük ETX, küçük adres (KK-04/3).
            m, e, _, _ = aday[j]
            return (m, 0 if j == eski else 1, e, j)

        if not aday:
            yeni = None
        elif eski in aday:
            en_iyi = min(aday, key=anahtar)
            if not self.b.istege_bagli_esik:
                yeni = en_iyi
            elif (en_iyi != eski and aday[en_iyi][0]
                  < (1.0 - self.d.GECIS_ORANI) * aday[eski][0]):
                yeni = en_iyi                    # KK-04/5 (T-11)
            else:
                yeni = eski
            if yeni != eski:
                self.sayac["istege_bagli_gecis"] += 1
        else:
            yeni = min(aday, key=anahtar)        # KK-04/4: zorunlu geçiş
            if eski is not None:
                self.sayac["zorunlu_gecis"] += 1
        if yeni != eski:
            self.sayac["ardil_degisti"] += 1
            self.yoksay_bitis = _INF
            self.kabul = None if yeni is None else aday[yeni][2:]
            if yeni is None:
                self.sayac["aclik"] += 1
                self._aclik_t = t
            elif eski is None and self._aclik_t is not None:
                self.sayac["aclik_bitti"] += 1
                self.sayac["aclik_sure_ms"] += int(round(
                    (t - self._aclik_t) * 1000.0))
                self._aclik_t = None
        self.ardil = yeni
        self.C = SONSUZ if yeni is None else aday[yeni][0]
        self._aclik_sec(t, baglar, kendi_donuk)
        self._iletilenleri_karsila()

    def _aclik_kosulu(self, baglar) -> bool:
        """KK-04/8: en az bir OLAĞAN komşunun sonlu ama uygulanamaz ilanı
        varsa yeni tur yardım eder; yoksa istek gitmez."""
        return any(baglar.kullanilir_mi(j) and C < SONSUZ
                   and not self.uygulanabilir(tur, C)
                   for j, (tur, C) in sorted(self.ilanlar.items()))

    def _aclik_sec(self, t: float, baglar, kendi_donuk: bool) -> None:
        if self.ardil is not None or kendi_donuk \
                or not self._aclik_kosulu(baglar):
            self.aclik = None
            return
        if self.aclik is None:
            self._aclik_baslat(t)

    def _aclik_baslat(self, t: float) -> None:
        """İstek hemen çok-yayınla; `ISTEK_YINELEME` kez daha 0,5 s arayla
        (Babel'in "en çok üç kez yeniden gönderilir"i); açlık sürerse dizi
        `ISTEK_ARA`'da yinelenir."""
        d = self.d
        self.aclik = _Aclik(istenen=self._istenen(), kalan=d.ISTEK_YINELEME,
                            sonraki_t=t + d.ISTEK_YINELEME_ARA_S,
                            dizi_t=t + d.ISTEK_ARA_S)
        self.giden.append((None, self.aclik.istenen, d.ISTEK_ATLAMA))
        self.sayac["aclik_istegi"] += 1

    def kendi_bitti(self, t: float, baglar) -> None:
        """KK-04/8: kendi karıştırılmamdan çıkınca açlık sürüyorsa istek
        hemen gider."""
        self.sec(t, baglar, kendi_donuk=False)

    # ------------------------------------------------------------------
    # İlan değeri ve FD — KK-04/6
    # ------------------------------------------------------------------
    def ilan(self) -> tuple[int, int]:
        """Selamın (tur, maliyet) alanları. Rotası olmayan düğüm ∞ ilan eder
        ve daha yeni bir tur ilan etmez: tur alanı FD'nin turu (Y-8)."""
        if self.gecit_mi:
            return self.tur_gecit, 0
        if self.ardil is not None:
            return self.kabul[0], self.C
        return (self.fd[0] if self.fd is not None else 0), SONSUZ

    def ilan_edildi(self, tur: int, C: int, t: float | None = None) -> None:
        """Selam kurulurken: FD ilan edilen (nicemlenmiş) değerle güncellenir
        (KK-02/7). `t` eğimin arayüzü içindir (KK-04/14), burada kullanılmaz."""
        self.son_ilan_C = C
        if C >= SONSUZ or self.gecit_mi:
            return
        if self.fd is None or sira_buyuk(tur, self.fd[0]):
            self.fd = (tur, C)
        elif tur == self.fd[0] and C < self.fd[1]:
            self.fd = (tur, C)

    # ------------------------------------------------------------------
    # Tur isteği — KK-04/9
    # ------------------------------------------------------------------
    def istek_al(self, g: int, t: float, istenen: int, kalan: int) -> None:
        d = self.d
        if self.gecit_mi:
            if sira_buyuk(istenen, self.tur_gecit):
                self.tur_gecit = sira_artir(self.tur_gecit)   # en çok 1
                self.sayac["tur_artirildi"] += 1
            self.olay = True
            self.sayac["istek_yanitlanan"] += 1
            return
        if self._karsilar(istenen):
            self.olay = True
            self.sayac["istek_yanitlanan"] += 1
            return
        if self.ardil is None or self.ardil == g or kalan < 2:
            return            # bu tasarımın basitleştirmesi (B-16)
        kayit = self.iletilen.get(istenen)
        if kayit is not None and t - kayit[1] < d.ISTEK_TEKRAR_S:
            kayit[0] = t + d.ISTEK_ANIMSA_S     # Y-11: kayıt tazelenir
            self.sayac["istek_bastirilan"] += 1
            return
        self.iletilen[istenen] = [t + d.ISTEK_ANIMSA_S, t]
        self.giden.append((self.ardil, istenen, kalan - 1))
        self.sayac["istek_iletilen"] += 1

    def _karsilar(self, istenen: int) -> bool:
        """Seçili rotamın turu ≥ istenen ve maliyetim sonlu. Yalnız duyduğum
        ama rotamın dayanmadığı bir tur yanıt sayılmaz."""
        return (self.ardil is not None and self.C < SONSUZ
                and not sira_buyuk(istenen, self.kabul[0]))

    def _iletilenleri_karsila(self) -> None:
        """Tutulan bir istek varken seçili rotamın turu ≥ istenen olursa
        hemen selam ve kayıt silinir: yanıt istek yolundan geri yayılır."""
        for istenen in sorted(self.iletilen):
            if self._karsilar(istenen):
                del self.iletilen[istenen]
                self.olay = True
                self.sayac["istek_karsilandi"] += 1

    # ------------------------------------------------------------------
    # Zaman olayları
    # ------------------------------------------------------------------
    def zaman_isle(self, t: float, baglar, kendi_donuk: bool) -> None:
        d = self.d
        if self.yoksay_bitis <= t:
            # KK-04/7: süre doldu; ardılın son alınan ilanı uygulanır,
            # uygulanamıyorsa seçim ardılı bırakır.
            self.yoksay_bitis = _INF
            self.sayac["yoksay_doldu"] += 1
            if self.ardil is not None and self.ardil in self.ilanlar:
                self.kabul = self.ilanlar[self.ardil]
        a = self.aclik
        if a is not None:
            if a.dizi_t <= t:
                self.aclik = None
                if self.ardil is None and not kendi_donuk \
                        and self._aclik_kosulu(baglar):
                    self._aclik_baslat(t)
            elif a.kalan > 0 and a.sonraki_t <= t:
                a.kalan -= 1
                a.sonraki_t += d.ISTEK_YINELEME_ARA_S
                self.giden.append((None, a.istenen, d.ISTEK_ATLAMA))
                self.sayac["aclik_istegi"] += 1
        for istenen in [i for i, k in self.iletilen.items() if k[0] <= t]:
            del self.iletilen[istenen]

    def son_tarih(self) -> float:
        en = self.yoksay_bitis
        a = self.aclik
        if a is not None:
            en = min(en, a.dizi_t)
            if a.kalan > 0:
                en = min(en, a.sonraki_t)
        for bitis, _ in self.iletilen.values():
            en = min(en, bitis)
        return en

    # ------------------------------------------------------------------
    def istekleri_al(self) -> list[tuple[int | None, int, int]]:
        g, self.giden = self.giden, []
        return g

    def olay_oku(self) -> bool:
        o, self.olay = self.olay, False
        return o
