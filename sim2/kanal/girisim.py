"""
Girişim — havadaki iletimlerin defteri ve alıcıdaki toplam girişim gücü.

🔒 PARÇA SINIRLARININ İKİ KAYNAĞI
=================================
Bir çerçeve iki farklı sebeple parçalanır ve ikisi de gereklidir:

  1. **Sönümleme ızgarası** — kanal çerçeve süresince değişiyor (ölçüldü:
     ortancada 1,06, p95'te 1,98 kez). `kanal/sonumleme.py`den gelir.
  2. **Girişim olayları** — başka bir iletim çerçevenin ORTASINDA başlayabilir
     ya da bitebilir. O anda SINR sıçrar; parçalanmasaydı sıçrama ortalamaya
     gömülür ve gizli terminal çarpışmaları sistematik olarak hafif görünürdü.

İkisinin BİRLEŞİMİ alınır. Yalnız biri alınsaydı öteki etki sessizce
ortalamaya karışırdı.

⚠️ GİRİŞİMCİNİN KENDİ BAĞI DA SÖNÜMLENİR
========================================
Girişim gücü, girişimcinin alıcıya olan bağının yavaş kaybı ve **kendi**
hızlı sönümlemesiyle hesaplanır. Sönümlemesiz sayılsaydı girişim gerçekten
daha kararlı görünür, çarpışmalar sistematik olarak fazla ya da az tahmin
edilirdi.

🔴 ALICI KENDİ GÜCÜNÜ GİRİŞİME KATAMAZ
======================================
Eski simülatörde bu bir `assert` ile korunuyordu ve `-O` altında kalkıyordu.
Burada `haric` parametresi zorunlu ve `dogrula` ile denetlenir.
"""

from __future__ import annotations

from dataclasses import dataclass

from sim2.cekirdek.degismezler import dogrula
from sim2.dunya.topoloji import Topoloji
from sim2.kanal.cerceve import Cerceve
from sim2.kanal.sonumleme import Sonumleme
from sim2.kanal.yayilim import Yayilim
from sim2.yapilandirma.konfig import Konfig

__all__ = ["Iletim", "Ortam", "Girisim"]


@dataclass(frozen=True, slots=True)
class Iletim:
    """Havadaki tek bir çerçeve. Dondurulmuş: süresi sonradan uzatılamaz."""

    gonderen: int
    cerceve: Cerceve
    baslangic_s: float
    guc_w: float

    @property
    def bitis_s(self) -> float:
        return self.baslangic_s + self.cerceve.sure_s

    def aktif_mi(self, t_s: float) -> bool:
        return self.baslangic_s <= t_s < self.bitis_s

    def kesisiyor_mu(self, bas_s: float, bitis_s: float) -> bool:
        return self.baslangic_s < bitis_s and bas_s < self.bitis_s


class Ortam:
    """Havadaki iletimlerin defteri — ortamın kendisi, rastgelelik yok."""

    __slots__ = ("_iletimler",)

    def __init__(self) -> None:
        self._iletimler: list[Iletim] = []

    def ekle(self, iletim: Iletim) -> None:
        dogrula(iletim.cerceve.sure_s > 0.0, "sıfır süreli iletim eklenemez")
        self._iletimler.append(iletim)

    def bitenleri_at(self, t_s: float) -> None:
        """Artık hiçbir alımı etkileyemeyecek iletimleri düşürür.

        ⚠️ Yalnız BELLEK içindir. Bir iletimi erken atmak onu girişim
        hesabından da düşürürdü; eşik bu yüzden `bitis_s <= t_s`.
        """
        self._iletimler = [i for i in self._iletimler if i.bitis_s > t_s]

    def aktif(self, t_s: float) -> tuple[Iletim, ...]:
        return tuple(i for i in self._iletimler if i.aktif_mi(t_s))

    def pencerede(self, bas_s: float, bitis_s: float) -> tuple[Iletim, ...]:
        return tuple(i for i in self._iletimler
                     if i.kesisiyor_mu(bas_s, bitis_s))

    def bos_mu(self) -> bool:
        return not self._iletimler


class Girisim:
    """Alıcıdaki girişim gücü ve parça sınırları."""

    __slots__ = ("konfig", "topoloji", "yayilim", "sonumleme", "ortam",
                 "karistirici")

    def __init__(self, konfig: Konfig, topoloji: Topoloji, yayilim: Yayilim,
                 sonumleme: Sonumleme, ortam: Ortam,
                 karistirici=None) -> None:
        self.konfig = konfig
        self.topoloji = topoloji
        self.yayilim = yayilim
        self.sonumleme = sonumleme
        self.ortam = ortam
        self.karistirici = karistirici

    # -------------------------------------------------------- parçalama
    def parca_sinirlari(self, bas_s: float, sure_s: float
                        ) -> tuple[float, ...]:
        """Sönümleme ızgarası ∪ girişim olayları. Modül başlığındaki nota bak."""
        dogrula(sure_s > 0.0, "çerçeve süresi pozitif olmalı")
        bitis_s = bas_s + sure_s
        kenarlar = set(self.sonumleme.parca_sinirlari(bas_s, sure_s))
        for iletim in self.ortam.pencerede(bas_s, bitis_s):
            for kenar in (iletim.baslangic_s, iletim.bitis_s):
                if bas_s < kenar < bitis_s:
                    kenarlar.add(kenar)
        if self.karistirici is not None:
            for kenar in self.karistirici.gecis_anlari(bas_s, bitis_s):
                if bas_s < kenar < bitis_s:
                    kenarlar.add(kenar)
        return tuple(sorted(kenarlar))

    # ------------------------------------------------------- girişim gücü
    def girisim_w(self, alici: int, t_s: float, haric: int) -> float:
        """`alici`de, `haric` dışındaki her kaynaktan gelen toplam güç.

        🔴 `haric` zorunlu: alıcı kendi almakta olduğu çerçeveyi girişim
        sayarsa SINR yapay olarak 0 dB'e oturur ve hiçbir çerçeve alınamaz.
        """
        dogrula(haric != alici, "alıcı kendi kendine gönderemez")
        toplam = 0.0
        alici_konum = self.topoloji.konum(alici, t_s)
        for iletim in self.ortam.aktif(t_s):
            if iletim.gonderen == haric or iletim.gonderen == alici:
                continue
            gonderen_konum = self.topoloji.konum(iletim.gonderen, t_s)
            yavas = self.yayilim.yavas_alinan_w(
                iletim.gonderen, alici, gonderen_konum, alici_konum,
                verici_w=iletim.guc_w)
            toplam += yavas * self.sonumleme.guc_kazanci(
                iletim.gonderen, alici, t_s)
        if self.karistirici is not None:
            toplam += self.karistirici.alinan_guc_w(alici, alici_konum, t_s)
        return toplam

    def sinyal_w(self, gonderen: int, alici: int, t_s: float,
                 verici_w: float | None = None) -> float:
        """İstenen çerçevenin alıcıdaki anlık gücü — yavaş × hızlı."""
        a = self.topoloji.konum(gonderen, t_s)
        b = self.topoloji.konum(alici, t_s)
        yavas = self.yayilim.yavas_alinan_w(gonderen, alici, a, b,
                                            verici_w=verici_w)
        return yavas * self.sonumleme.guc_kazanci(gonderen, alici, t_s)

    # ------------------------------------------------------------- CSMA
    def kanal_mesgul_mu(self, dinleyen: int, t_s: float,
                        esik_w: float | None = None) -> bool:
        """Taşıyıcı dinleme. Eşik verilmezse gürültü tabanının kendisi.

        ⚠️ Karıştırıcının CSMA'ya görünüp görünmediği SINIFA bağlıdır ve
        `karistirici` modülünde tanımlanır: aldatıcı karıştırıcı geçerli
        görünümlü önbelge bastığı için taşıyıcı dinleme onu MEŞGUL görmek
        zorundadır; sürekli gürültü karıştırıcısı için bu geçerli değildir.
        """
        esik = self.yayilim.gurultu_w if esik_w is None else esik_w
        alici_konum = self.topoloji.konum(dinleyen, t_s)
        for iletim in self.ortam.aktif(t_s):
            if iletim.gonderen == dinleyen:
                continue
            if self.sinyal_w(iletim.gonderen, dinleyen, t_s,
                             verici_w=iletim.guc_w) >= esik:
                return True
        # 🔒 Y5: yalnız CSMA'ya GÖRÜNEN üyelerin gücü (`csma_guc_w`). Tek
        # karıştırıcıda eski iki adımlı denetimle birebir aynıdır.
        if self.karistirici is not None and self.karistirici.csma_ya_gorunur(t_s):
            if self.karistirici.csma_guc_w(dinleyen, alici_konum, t_s) >= esik:
                return True
        return False
