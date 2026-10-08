"""
DCF — 802.11 dağıtık koordinasyon fonksiyonu (CSMA/CA, temel erişim).

🔒 BU DOSYADA TEK BİR FİZİK FORMÜLÜ YOK
=======================================
Kusur 5, MAC'in Kat 2 ile Kat 3'ü karıştırmasıydı: `alim_per`, `_girisim_w`,
`_parca_sinirlari` aslında kanal fiziğiydi ve `mac.py` içinde duruyordu.
Burada yalnız **çekişme mantığı** var: geri çekilme sayacı, çekişme
penceresinin katlanması, yeniden deneme sayacı. SINR, PER, güç ve süre
soruları `kanal/`a sorulur; süreler `Cerceve`den hazır gelir. Bir test AST ile
denetler.

🔒 TEMEL ERİŞİM (RTS/CTS YOK) — beyan edilir
============================================
RTS/CTS açılsaydı gizli terminal tablosu kökten değişirdi ve ölçülen fark
yönlendirmenin değil, el sıkışmanın farkı olabilirdi. Ayrıca Bianchi'nin
doygunluk modeli de temel erişim içindir; kapanış ölçütü onunla
karşılaştırma olduğu için ikisi aynı varsayımda olmak zorunda.
Kapsam belgesine yazılır.

🔒 GERİ ÇEKİLME AKIŞI DÜĞÜM BAŞINA
==================================
`mac_geri_cekilme` sıralı bir akıştır ve **düğüm başına alt akış** kullanılır.
Tek akış olsaydı, çok ileti yapan bir düğüm ötekilerin geri çekilme dizisini
kaydırır ve düğümler arasında sessiz bir kuplaj doğardı — `protokol_kesif`
ile aynı sebep.

⚠️ Aynı düğümün kendi dizisi, protokol daha çok ilettiği için ilerler. Bu
DÜZELTİLEBİLİR bir şey değil: iletim sayısı protokolün kendi davranışıdır.
Düzeltilebilir olan düğümler arası kuplajdır ve o kapatıldı.

🔴 KAZANIM: `alim_red_yari_cift` İLK KEZ BURADA ATEŞLENİR
=========================================================
Adım 6a'da alıcı zinciri yazıldı ama hiçbir düğüm göndermediği için yarım
çiftlik dalı hiç koşmuyordu (ölçüldü: %0,0). DCF gönderime başlayınca
alıcı zinciri `gonderime_basla()` çağrısını görür ve dal ateşlenir.
"""

from __future__ import annotations

from dataclasses import dataclass

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import Akislar
from sim2.kanal.cerceve import Cerceve
from sim2.yapilandirma.konfig import Konfig

__all__ = ["DCF_DURUMLARI", "DcfZamanlari", "Dcf"]

DCF_DURUMLARI: tuple[str, ...] = (
    "bos",              # gönderilecek çerçeve yok
    "geri_cekilme",     # sayaç işliyor, kanal boş oldukça azalıyor
    "gonderiyor",       # havada
    "onay_bekliyor",    # SIFS + onay penceresi
)


@dataclass(frozen=True, slots=True)
class DcfZamanlari:
    """DCF'nin süreleri. Hepsi `Konfig`ten ve `Cerceve`den GELİR.

    🔒 Burada hiçbir çerçeve süresi HESAPLANMAZ — `Cerceve` hazır getirir.
    Hesaplansaydı kusur 1'in ikinci bir kopyası doğardı.
    """

    slot_s: float
    sifs_s: float
    difs_s: float
    cca_s: float
    veri_s: float
    onay_s: float

    @property
    def basari_turu_s(self) -> float:
        """Başarılı bir iletimin kanalı meşgul ettiği toplam süre.

        DIFS + veri + SIFS + onay. Bianchi'nin `T_s`si.
        """
        return self.difs_s + self.veri_s + self.sifs_s + self.onay_s

    @property
    def carpisma_turu_s(self) -> float:
        """Çarpışmanın kanalı meşgul ettiği süre — Bianchi'nin `T_c`si.

        Temel erişimde gönderen, onay zaman aşımına kadar bekler; eşit
        uzunluklu çerçevelerde bu DIFS + veri kadardır.
        """
        return self.difs_s + self.veri_s

    @staticmethod
    def kur(konfig: Konfig, veri: Cerceve, onay: Cerceve) -> "DcfZamanlari":
        return DcfZamanlari(
            slot_s=konfig.slot_s, sifs_s=konfig.sifs_s,
            difs_s=konfig.difs_s, cca_s=konfig.cca_s,
            veri_s=veri.sure_s, onay_s=onay.sure_s)


class Dcf:
    """Bir düğümün çekişme durumu. Fizik yok, yalnız sayaçlar.

    🔒 DEĞİŞMEZLER
      · geri çekilme sayacı asla negatif olmaz
      · çekişme penceresi `[cw_min, cw_max]` dışına çıkmaz
      · `gonderime_hazir` yalnız sayaç sıfırken doğrudur
    """

    __slots__ = ("dugum", "konfig", "_akis", "_cw", "_sayac", "_deneme",
                 "_durum")

    def __init__(self, dugum: int, konfig: Konfig, akislar: Akislar) -> None:
        dogrula(dugum >= 0, "düğüm numarası negatif olamaz")
        dogrula(1 <= konfig.cw_min <= konfig.cw_max,
                "çekişme penceresi tutarsız")
        self.dugum = dugum
        self.konfig = konfig
        # 🔒 Düğüm başına ALT AKIŞ — modül başlığındaki nota bak.
        self._akis = akislar.dugum("mac_geri_cekilme", dugum)
        self._cw = konfig.cw_min
        self._sayac = 0
        self._deneme = 0
        self._durum = "bos"

    # ------------------------------------------------------------- durum
    @property
    def durum(self) -> str:
        return self._durum

    @property
    def cekisme_penceresi(self) -> int:
        return self._cw

    @property
    def geri_sayim(self) -> int:
        return self._sayac

    @property
    def deneme(self) -> int:
        return self._deneme

    @property
    def gonderime_hazir(self) -> bool:
        return self._durum == "geri_cekilme" and self._sayac == 0

    # ---------------------------------------------------------- geçişler
    def cerceve_hazir(self) -> None:
        """Kuyruğa çerçeve geldi — çekişme başlar, pencere sıfırlanır."""
        dogrula(self._durum == "bos",
                "boşta olmayan DCF'ye yeni çerçeve verilemez")
        self._cw = self.konfig.cw_min
        self._deneme = 0
        self._durum = "geri_cekilme"
        self._sayac = self._geri_cekilme_cek()

    def slot_gecti(self, adet: int = 1) -> None:
        """Kanal `adet` slot boyunca BOŞ kaldı — sayaç o kadar azalır.

        🔴 Kanal meşgulken bu çağrılmaz: 802.11'de sayaç donar. Donmasaydı
        meşgul kanalda bekleyen düğümler sırayla değil aynı anda patlar ve
        çarpışma oranı yapay olarak yükselirdi.

        ⚠️ `adet` toplu azaltma içindir: olay güdümlü sürücü slot slot olay
        üretmez (350 s × 20 µs = 17,5 milyon olay/düğüm olurdu), boş kalan
        aralığı bir kerede geçirir. Tek tek çağırmakla BİREBİR aynı sonucu
        vermek zorunda ve testi var.
        """
        dogrula(self._durum == "geri_cekilme",
                "geri çekilmede olmayan DCF'de slot işlenemez")
        dogrula(adet >= 0, "slot sayısı negatif olamaz")
        self._sayac = max(0, self._sayac - adet)

    def gonderime_basladi(self) -> None:
        dogrula(self.gonderime_hazir, "sayaç sıfırlanmadan gönderilemez")
        self._durum = "gonderiyor"
        self._deneme += 1

    def onay_bekle(self) -> None:
        dogrula(self._durum == "gonderiyor", "gönderilmeden onay beklenemez")
        self._durum = "onay_bekliyor"

    def onay_geldi(self) -> None:
        """Başarı: pencere sıfırlanır, düğüm boşa döner."""
        dogrula(self._durum in ("gonderiyor", "onay_bekliyor"),
                "beklenmeyen durumda onay")
        self._cw = self.konfig.cw_min
        self._deneme = 0
        self._sayac = 0
        self._durum = "bos"

    def onay_gelmedi(self) -> bool:
        """Başarısızlık. Dönen değer: **vazgeçildi mi**.

        Çekişme penceresi katlanır (`cw_max`te doyar) ve yeni bir geri
        çekilme çekilir. Yeniden deneme sınırı aşılırsa `True` döner ve
        çağıran paketi `iletim_basarisiz` sebebiyle DÜŞÜRMEK zorundadır.
        """
        dogrula(self._durum in ("gonderiyor", "onay_bekliyor"),
                "beklenmeyen durumda başarısızlık")
        if self._deneme > self.konfig.yeniden_deneme_siniri:
            self._cw = self.konfig.cw_min
            self._deneme = 0
            self._sayac = 0
            self._durum = "bos"
            return True
        self._cw = min(2 * self._cw + 1, self.konfig.cw_max)
        self._durum = "geri_cekilme"
        self._sayac = self._geri_cekilme_cek()
        return False

    def vazgec(self) -> None:
        """Çerçeve dışarıdan iptal edildi (rota geçersiz, TTL, kuyruk)."""
        self._cw = self.konfig.cw_min
        self._deneme = 0
        self._sayac = 0
        self._durum = "bos"

    # ------------------------------------------------------------- içsel
    def _geri_cekilme_cek(self) -> int:
        """`[0, cw]` aralığında düzgün — 802.11'in kuralı.

        `cw` kapsayıcıdır: `cw_min = 31` iken 32 olası değer vardır ve
        Bianchi'nin `W = 32`si budur.
        """
        deger = self._akis.randint(0, self._cw)
        dogrula(0 <= deger <= self._cw, "geri çekilme aralık dışı")
        return deger
