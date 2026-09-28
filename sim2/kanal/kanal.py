"""
Kanal — **TEK** `per()`. Kâhin ve gerçek alım aynı gövdeyi çağırır.

🔴 KUSUR 1'İN İKİNCİ YARISI
===========================
`kanal/cerceve.py` bit sayısını tek yerde tanımladı. Burada da PER tek yerde
hesaplanır: `Kanal.per(cerceve, sinr_izi)`. Kâhin ile gerçek alım arasındaki
TEK fark girdideki izin uzunluğudur —

    kâhin        : ((hataya_acik_bit, sinr),)                    tek parça
    gerçek alım  : ((bit₁, sinr₁), (bit₂, sinr₂), …)             çok parça

İkisi ayrı fonksiyon olsaydı sistematik olarak ayrışırlardı; eski simülatörde
tam bu oldu ve ölçüldü (yeni parametrelerde %9,38).

🔒 PARÇALI PER == TEK PARÇA (kapanış ölçütü a)
==============================================
    PER = 1 − Π_k (1 − BER(γ_k))^(bit_k)
Sabit γ'da bu tam olarak `1 − (1−BER)^(Σ bit_k)`ya indirgenir. Eşitlik
yaklaşık değil, **cebirsel**: `Σ bit_k = hataya_acik_bit` olduğu sürece.
Bit paylaşımı süreye göre yapılır ve önbelge payı sıfırdır — önbelge gövde
biti taşımaz.

🔒 MODÜLASYON: DQPSK (2 Mb/s), DBPSK DEĞİL
==========================================
Eski kod `BER = ½·e^(−γ)` kullanıyordu; bu 802.11b'nin **1 Mb/s** modülasyonu
olan DBPSK'nın formülüdür. 2 Mb/s'te DQPSK kullanılır ve kapalı formu farklıdır:

    Pb = Q₁(a, b) − ½·I₀(ab)·e^(−(a²+b²)/2)
    a = √(2γ(1 − 1/√2)),   b = √(2γ(1 + 1/√2))

Q₁ Marcum-Q, I₀ değiştirilmiş Bessel. Kapalı form olduğu için yayınlanmış
BER eğrileriyle **analitik olarak** doğrulanır (bir test bunu yapar).

⚠️ `scipy` bağımlılığı bilinçlidir: Marcum-Q'yu elle yazmak, doğrulanması
gereken ikinci bir sayısal gövde eklerdi. Sürüm `ortam_ozeti()`ne yazılır ki
sonuç satırı hangi kütüphaneyle üretildiğini taşısın.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
from scipy.special import i0e  # type: ignore[import-untyped]
from scipy.stats import ncx2  # type: ignore[import-untyped]

from sim2.cekirdek.degismezler import dogrula
from sim2.dunya.topoloji import Topoloji
from sim2.kanal.cerceve import Cerceve
from sim2.kanal.girisim import Girisim, Ortam
from sim2.kanal.karistirici import karistirici_kur
from sim2.kanal.sonumleme import Sonumleme
from sim2.kanal.tehdit import tehdit_tanimlari
from sim2.kanal.yayilim import Yayilim
from sim2.yapilandirma.konfig import Konfig

__all__ = ["MODULASYONLAR", "cerceve_per", "ber_dbpsk", "ber_dqpsk",
           "ber_dbpsk_dizi", "ber_dqpsk_dizi", "Kanal"]

MODULASYONLAR: tuple[str, ...] = ("dbpsk", "dqpsk", "cck")

_KOK_YARIM = math.sqrt(0.5)


def ber_dbpsk(sinr_lin: float) -> float:
    """Eşevresiz DBPSK — 802.11b'nin 1 Mb/s modülasyonu.

    Pb = ½·e^(−γ). Ablasyon ve literatür karşılaştırması için duruyor.
    """
    if sinr_lin <= 0.0:
        return 0.5
    return 0.5 * math.exp(-sinr_lin)


def ber_dqpsk_dizi(sinr_lin: Sequence[float]) -> "np.ndarray":
    """Diferansiyel eşevresiz QPSK — 802.11b'nin 2 Mb/s modülasyonu.

    Pb = Q₁(a,b) − ½·I₀(ab)·e^(−(a²+b²)/2)

    🔒 Sayısal kararlılık: `I₀(ab)·e^(−(a²+b²)/2)` büyük γ'da taşar/altta
    kalır. `i0e(x) = I₀(x)·e^(−x)` kullanılarak çarpım
    `i0e(ab)·e^(−(a−b)²/2)` biçimine getirilir — matematiksel olarak aynı,
    sayısal olarak güvenli.

    🔴 GÖVDE BURADA, DİZİ ÜZERİNDE — skaler sürüm bunu çağırır.
    İkinci bir skaler gövde yazmak kusur 1'in geri gelmesi olurdu. Dizi
    olmasının sebebi ölçüm: `ncx2.sf`in ÇAĞRI BAŞINA sabit maliyeti
    hesabın kendisinden büyük ve bir SINR izinde ortalama 6,6 parça var.
    Skaler çağrılar koşu süresinin %24'ünü yiyordu.
    """
    g = np.asarray(sinr_lin, dtype=float)
    cikti = np.full(g.shape, 0.5)
    gecerli = g > 0.0
    if not gecerli.any():
        return cikti
    gm = g[gecerli]
    a = np.sqrt(2.0 * gm * (1.0 - _KOK_YARIM))
    b = np.sqrt(2.0 * gm * (1.0 + _KOK_YARIM))
    marcum = ncx2.sf(b * b, 2, a * a)
    duzeltme = 0.5 * i0e(a * b) * np.exp(-0.5 * (a - b) ** 2)
    cikti[gecerli] = np.clip(marcum - duzeltme, 0.0, 0.5)
    return cikti


def ber_dqpsk(sinr_lin: float) -> float:
    """Tek bir SINR için DQPSK BER — gövdesi `ber_dqpsk_dizi`dir."""
    return float(ber_dqpsk_dizi((sinr_lin,))[0])


def ber_dbpsk_dizi(sinr_lin: Sequence[float]) -> list[float]:
    """DBPSK'nın dizi sürümü — skaler gövdeyi DÖNGÜYLE çağırır.

    🔒 DQPSK'nın aksine burada vektörleştirme YOK: `math.exp` zaten ucuz ve
    `np.exp`e geçmek son basamakta ayrışma riski taşırdı. Kazanç sıfıra
    yakınken sayısal bir risk almak, ölçmeden yapılan bir takas olurdu.
    """
    return [ber_dbpsk(g) for g in sinr_lin]


# 🔒 CCK — 5,5 ve 11 Mb/s (`v2/15` A4, K-177). ns-3 `DsssErrorRateModel`in
# GSL sürümü (G1 Pursley–Royster; depodaki kopya): 5,5 Mb/s Eb/N0 = SINR·4,
# 16'lık sembol hatası SEP₁₆(2·Eb/N0), başarı (1 − SEP)^(bit/4); 11 Mb/s
# Eb/N0 = SINR·2, SEP₂₅₆ = 1 − (1 − SEP₁₆(2·Eb/N0))², başarı
# (1 − SEP₂₅₆)^(bit/8). İkisi de BİT BAŞINA aynı biçime iner:
#     b = 1 − (1 − SEP₁₆(2·Eb/N0))^(1/4)
# fark yalnız Eb/N0 çarpanındadır (B/R: ×4, ×2) ve o çerçeveden gelir.
#     SEP₁₆(e) = 1 − ∫_{−β}^{∞} (2Φ(x+β) − 1)^7 φ(x) dx ,  β = √(2e)
# Sayısal kararlılık için Φ(−β) + ∫ [1 − (1 − 2Q(x+β))^7] φ(x) dx biçiminde
# log-ızgarada bir kez hesaplanır (ilk CCK çağrısında) ve aradeğerlenir;
# doğrudan integralle örtüşmesi bir testle bağlanır.
_SEP16_LOG_E = np.linspace(-3.0, 2.5, 1101)
_sep16_log: "np.ndarray | None" = None


def _sep16_tablosu() -> "np.ndarray":
    global _sep16_log
    if _sep16_log is None:
        from scipy.integrate import quad  # type: ignore[import-untyped]
        from scipy.special import ndtr  # type: ignore[import-untyped]
        kok_2pi = math.sqrt(2.0 * math.pi)
        degerler = []
        for le in _SEP16_LOG_E:
            b = math.sqrt(2.0 * 10.0 ** le)

            def f(x: float, b: float = b) -> float:
                q = float(ndtr(-(x + b)))
                return (-math.expm1(7.0 * math.log1p(-2.0 * q))
                        * math.exp(-0.5 * x * x) / kok_2pi)
            ic, _ = quad(f, -b, np.inf, epsabs=0.0, epsrel=1e-10, limit=200)
            degerler.append(max(float(ndtr(-b)) + ic, 1e-300))
        _sep16_log = np.log(np.array(degerler))
    return _sep16_log


def sep16(e: "np.ndarray") -> "np.ndarray":
    """SEP₁₆ — tablodan, log-ızgarada doğrusal aradeğerleme."""
    return np.exp(np.interp(np.log10(e), _SEP16_LOG_E, _sep16_tablosu()))


def ber_cck_dizi(ebn0: Sequence[float]) -> "np.ndarray":
    """CCK'nın bit başına eşdeğer hatası — yukarıdaki biçim."""
    g = np.asarray(ebn0, dtype=float)
    cikti = np.full(g.shape, 0.5)
    gecerli = g > 0.0
    if gecerli.any():
        sep = sep16(2.0 * g[gecerli])
        cikti[gecerli] = np.clip(-np.expm1(0.25 * np.log1p(-sep)), 0.0, 0.5)
    return cikti


_BER = {"dbpsk": ber_dbpsk_dizi, "dqpsk": ber_dqpsk_dizi,
        "cck": ber_cck_dizi}


class Kanal:
    """Kanalın tek giriş noktası. `per()` burada TEKTİR."""

    __slots__ = ("konfig", "topoloji", "yayilim", "sonumleme", "ortam",
                 "girisim", "karistirici", "_ber")

    def __init__(self, konfig: Konfig, topoloji: Topoloji,
                 ortam: Ortam | None = None) -> None:
        if konfig.modulasyon not in MODULASYONLAR:
            raise ValueError(
                f"bilinmeyen modülasyon: {konfig.modulasyon!r} — "
                f"seçenekler: {MODULASYONLAR}")
        self.konfig = konfig
        self.topoloji = topoloji
        self.yayilim = Yayilim(konfig)
        self.sonumleme = Sonumleme(konfig, topoloji)
        self.ortam = Ortam() if ortam is None else ortam
        # 🔒 Karıştırıcı SENARYODAN kurulur, dışarıdan verilmez: elle
        # verilebilseydi "statik-surekli" etiketli iki koşu farklı karıştırıcı
        # taşıyabilir ve sonuç satırındaki etiket yalan söylerdi.
        # Y5b: kümenin biçimi `tehdit_senaryosu`ndan (`kanal/tehdit.py`);
        # `tekli_merkez` tanım üretmez ve bugünkü nesne birebir kurulur.
        self.karistirici = karistirici_kur(konfig, self.yayilim, topoloji,
                                           self.ortam,
                                           tanimlar=tehdit_tanimlari(konfig),
                                           sonumleme=self.sonumleme)
        self.girisim = Girisim(konfig, topoloji, self.yayilim, self.sonumleme,
                               self.ortam, self.karistirici)
        self._ber = _BER[konfig.modulasyon]

    # ==================================================================
    # 🔒 TEK PER GÖVDESİ
    # ==================================================================
    @staticmethod
    def _hata_olasiligi(sinr_izi: Sequence[tuple[float, float]],
                        beklenen_bit: int, ber_dizi_fn,
                        ebn0_carpani: float = 1.0) -> float:
        """🔒 PROJEDEKİ TEK OLASILIK GÖVDESİ.

            hata = 1 − Π_k (1 − BER(γ_k))^(bit_k)

        Üç çağıranı var ve üçü de buraya iner: gövde PER'i (`per`), önbelge
        PER'i (`onbelge_per`) ve kâhin PER'i (`kahin_per`). Aralarındaki tek
        fark **bit sayısı ve BER fonksiyonu**; hesabın kendisi tektir.
        İkinci bir gövde yazmak kusur 1'in geri gelmesi olurdu.

        Bit toplamı `beklenen_bit`e eşit OLMALIDIR: eşitlik bozulursa parçalı
        hesap sessizce tek parçadan ayrışır.

        🔒 BER'in girdisi Eb/N0 = SINR · `ebn0_carpani` (`v2/15` A2, K-173).
        Çarpan çerçeveden gelir (`cerceve_kur` — bit hızı aritmetiğinin tek
        yeri); işlem kazancı kapalıyken 1,0 ve çarpma birebir.
        """
        dogrula(len(sinr_izi) > 0, "boş SINR izi ile hata olasılığı hesaplanamaz")
        toplam_bit = math.fsum(bit for bit, _ in sinr_izi)
        dogrula(abs(toplam_bit - beklenen_bit) < 1e-6,
                "SINR izindeki bit toplamı beklenen bit sayısına eşit değil")
        gecerli = [(bit, sinr) for bit, sinr in sinr_izi if bit > 0.0]
        if not gecerli:
            return 0.0
        berler = ber_dizi_fn([sinr * ebn0_carpani for _, sinr in gecerli])
        log_basari = 0.0
        for (bit, _), ber in zip(gecerli, berler):
            if ber >= 0.5:
                return 1.0
            log_basari += bit * math.log1p(-ber)
            if log_basari < -50.0:            # e^(−50) ≈ 2e−22
                return 1.0
        return -math.expm1(log_basari)

    def per(self, cerceve: Cerceve,
            sinr_izi: Sequence[tuple[float, float]]) -> float:
        """GÖVDE PER'i — çerçevenin yükü, `Konfig.modulasyon` ile."""
        # 🔒 A4: modülasyon çerçeveden (hız uyarlaması kapalıyken
        # `Konfig.modulasyon` — `self._ber` ile aynı fonksiyon).
        return self._hata_olasiligi(sinr_izi, cerceve.hataya_acik_bit,
                                    _BER[cerceve.govde_modulasyonu],
                                    cerceve.govde_ebn0_carpani)

    def onbelge_per(self, cerceve: Cerceve,
                    sinr_izi: Sequence[tuple[float, float]]) -> float:
        """ÖNBELGE PER'i — 192 bit, **TEMEL HIZDA DBPSK**.

        🔒 Gövdeden ayrı olması bir kolaylık değil, fizik: önbelge 1 Mb/s
        DBPSK ile gönderilir, gövde 2 Mb/s DQPSK ile. Ölçülen fark büyük —
        SINR 10 dB'de önbelge %99,6 kilitlenirken gövde %75
        hata alıyor. Tek bir PER'e indirgemek `alim_red_onbelge` ile
        `alim_red_per`i aynı şey saymak olurdu.
        """
        return self._hata_olasiligi(sinr_izi, cerceve.onbelge_bit,
                                    ber_dbpsk_dizi,
                                    cerceve.onbelge_ebn0_carpani)

    def sahte_onbelge_per(self, cerceve: Cerceve, guc_w: float) -> float:
        """A6 (K-176) — aldatıcının sahte önbelgesinin PER'i; yalnız gürültüye
        karşı (beyan: öteki girişim ihmal). Aynı önbelge gövdesi."""
        return self.onbelge_per(
            cerceve, ((float(cerceve.onbelge_bit), guc_w / self.yayilim.gurultu_w),))

    def kahin_per(self, cerceve: Cerceve, sinr_lin: float) -> float:
        """Tek parçalı kâhin PER — **aynı** `per()` gövdesini çağırır.

        Ayrı bir gövdesi olsaydı kusur 1 geri gelirdi. Kâhin sayaçları buradan
        beslenir ve gerçek alımla aynı tanımı kullanır.
        """
        return self.per(cerceve, ((float(cerceve.hataya_acik_bit), sinr_lin),))

    # ==================================================================
    # SINR İZİ
    # ==================================================================
    def _iz(self, gonderen: int, alici: int, cerceve: Cerceve, bas_s: float,
            aralik: tuple[float, float], toplam_bit: int,
            verici_w: float | None) -> tuple[tuple[float, float], ...]:
        """🔒 SINR İZİNİN TEK ÜRETİCİSİ — gövde ve önbelge aynı gövdeden.

        Çerçevenin TAMAMI parçalanır (girişim ve sönümleme sınırları çerçeve
        boyunca geçerlidir), ama bit payı yalnız `aralik` içinde dağıtılır.
        Aralık dışına düşen parçaların payı sıfırdır; böylece bit toplamı her
        zaman tam olarak `toplam_bit` olur ve sabit SINR'de parçalı hesap tek
        parçaya **cebirsel olarak** eşitlenir.
        """
        dogrula(gonderen != alici, "düğüm kendine gönderemez")
        aralik_bas, aralik_bitis = aralik
        aralik_sure = aralik_bitis - aralik_bas
        dogrula(aralik_sure > 0.0, "iz aralığı pozitif süreli olmalı")
        sinirlar = self.girisim.parca_sinirlari(bas_s, cerceve.sure_s)
        gurultu = self.yayilim.gurultu_w

        iz: list[tuple[float, float]] = []
        for parca_bas, parca_bitis in zip(sinirlar, sinirlar[1:]):
            ortusme = min(parca_bitis, aralik_bitis) - max(parca_bas, aralik_bas)
            if ortusme <= 0.0:
                continue
            ortasi = 0.5 * (parca_bas + parca_bitis)
            bit = toplam_bit * (ortusme / aralik_sure)
            s = self.girisim.sinyal_w(gonderen, alici, ortasi, verici_w)
            g = self.girisim.girisim_w(alici, ortasi, haric=gonderen)
            iz.append((bit, s / (gurultu + g)))
        # Kayan nokta artığını son parçaya yükle: bit toplamı TAM olmalı.
        if iz:
            fark = toplam_bit - math.fsum(b for b, _ in iz)
            bit, sinr = iz[-1]
            iz[-1] = (bit + fark, sinr)
        return tuple(iz)

    def sinr_izi(self, gonderen: int, alici: int, cerceve: Cerceve,
                 bas_s: float, verici_w: float | None = None
                 ) -> tuple[tuple[float, float], ...]:
        """GÖVDE izi — bit payı gövde aralığında dağıtılır, önbelgede sıfır."""
        return self._iz(gonderen, alici, cerceve, bas_s,
                        cerceve.govde_araligi(bas_s),
                        cerceve.hataya_acik_bit, verici_w)

    def onbelge_izi(self, gonderen: int, alici: int, cerceve: Cerceve,
                    bas_s: float, verici_w: float | None = None
                    ) -> tuple[tuple[float, float], ...]:
        """ÖNBELGE izi — bit payı yalnız önbelge aralığında.

        Alıcı zinciri kilidi bununla kurar: önbelge o aralıkta çözülemezse
        çerçeve hiç alınmaz ve bu `alim_red_onbelge` olarak sayılır.
        """
        return self._iz(gonderen, alici, cerceve, bas_s,
                        cerceve.onbelge_araligi(bas_s),
                        cerceve.onbelge_bit, verici_w)

    def onbelge_alim_per(self, gonderen: int, alici: int, cerceve: Cerceve,
                         bas_s: float, verici_w: float | None = None) -> float:
        return self.onbelge_per(
            cerceve, self.onbelge_izi(gonderen, alici, cerceve, bas_s,
                                      verici_w))

    def alim_per(self, gonderen: int, alici: int, cerceve: Cerceve,
                 bas_s: float, verici_w: float | None = None) -> float:
        """Gerçek alım PER'i — izi kurar, `per()`e verir. Başka gövde yok."""
        return self.per(cerceve, self.sinr_izi(gonderen, alici, cerceve,
                                               bas_s, verici_w))

    # ------------------------------------------------------------- teşhis
    def menzilde_per(self, cerceve: Cerceve) -> float:
        """Menzil sınırında, girişimsiz, sönümlemesiz PER — analitik hedef."""
        return self.kahin_per(cerceve, 10.0 ** (self.konfig.sinr_esigi_db / 10.0))


def cerceve_per(cerceve: Cerceve, sinr_lin: float) -> float:
    """Tek parçalı PER — `Kanal.per`in AYNI gövdesi, kanal nesnesi olmadan.

    🔒 A7 (K-178): referans dünyanın türetimleri (`kanal/dunya.py`) kanal
    kurmadan PER ister; ikinci bir gövde yazılmaz, statik gövde çağrılır.
    """
    return Kanal._hata_olasiligi(
        ((float(cerceve.hataya_acik_bit), sinr_lin),),
        cerceve.hataya_acik_bit, _BER[cerceve.govde_modulasyonu],
        cerceve.govde_ebn0_carpani)
