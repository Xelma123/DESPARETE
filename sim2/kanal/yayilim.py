"""
Yayılım — kanalın YAVAŞ bileşenleri: yol kaybı · gölgeleme · anten deseni.

Hızlı sönümleme burada DEĞİL (`kanal/sonumleme.py`): `kopma_fiziksel` yavaş
SINR üzerinden tanımlıdır; hızlı sönümleme saniyede yüzlerce kez eşiği geçer
ve onu kopma saymak sayacı gürültüye çevirirdi.

🔒 VERİCİ GÜCÜ
==============
Referans dünyada verici gücü GİRDİDİR: EIRP 20 dBm (`v2/14` §1). Eski
dünyada menzilden türetilir — menzil *"girişimsiz SINR'in tam olarak eşiğe
(β) eşit olduğu mesafe"*dir ve güç ondan çıkar:

    N  = k·T·B·F                          (gürültü tabanı)
    Pr(R) = N·β                           (menzilde alınan güç)
    Pt = Pr(R) · 10^(PL(R)/10)

🔒 ANTEN DESENİ
===============
Yarım dalga dipol, düz uçuş varsayımıyla (Gauss-Markov'un ortalama pitch =
0 değeriyle tutarlı). İzotropik varsaymak modeli tam da yakın komşularda
iyimser yapardı. Uçuş yatıklığı (attitude) modellenmez ve beyan edilir.

🔒 GÖLGELEME — bağ-simetrik ve KONUMA BAĞLI
===========================================
Hash bağın kimliğine VE bağ ortasının hücresine bakar; hücre köşeleri
arasında trilineer yumuşatma yapılır. Böylece hareket eden düğüm gölgeleme
alanında **sürekli** ilerler, ışınlanmaz. Bağ-simetriklik `min(i,j), max(i,j)`
ile sağlanır: A→B ile B→A aynı gölgelemeyi görür. Gölgelemesiz bir modelde
bağlar gerçeğe göre keskin açılıp kapanır (PER'in geçiş bandı ~3 dB).
"""

from __future__ import annotations

import math

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import normal_cekimi
from sim2.dunya.geometri import Nokta3, mesafe, yukselis_acisi_rad
from sim2.yapilandirma.konfig import Konfig

__all__ = ["BOLTZMANN", "ISIK_HIZI", "REFERANS_MESAFE_M", "Yayilim",
           "dbm_to_w", "w_to_dbm", "db_to_lin", "lin_to_db"]

BOLTZMANN = 1.380649e-23
ISIK_HIZI = 299792458.0
REFERANS_MESAFE_M = 1.0


def dbm_to_w(dbm: float) -> float:
    return 10.0 ** (dbm / 10.0) / 1000.0


def w_to_dbm(w: float) -> float:
    return 10.0 * math.log10(w * 1000.0)


def db_to_lin(db: float) -> float:
    return 10.0 ** (db / 10.0)


def lin_to_db(lin: float) -> float:
    return 10.0 * math.log10(lin)


# Köşe önbelleğinin üst sınırı (~2^19 giriş). Aşılınca boşaltılır.
KOSE_ONBELLEK_SINIRI = 1 << 19
# 🔒 K-190: yavaş kayıp önbelleğinin tavanı. Değer SONUCU DEĞİŞTİREMEZ —
# anahtar tam girdidir (kimlikler + iki konum), dolunca boşaltılır ve
# değer yeniden AYNI işlemle hesaplanır; yalnız süreyi belirler.
YAVAS_ONBELLEK_SINIRI = 1 << 18

class Yayilim:
    """Yavaş kanal. Saf: aynı girdi her zaman aynı çıktıyı verir."""

    __slots__ = ("konfig", "gurultu_w", "verici_gucu_w", "_pl_referans_db",
                 "_hucre_m", "_sigma_db", "_golge_onbellek",
                 "_yavas_onbellek")

    def __init__(self, konfig: Konfig) -> None:
        self.konfig = konfig
        self.gurultu_w = self.gurultu_tabani_w(konfig)
        self._pl_referans_db = 20.0 * math.log10(
            4.0 * math.pi * REFERANS_MESAFE_M * konfig.frekans_hz / ISIK_HIZI)
        if konfig.verici_eirp_dbm is None:
            # Pt, MENZİL TANIMINDAN türetilir — bağımsız bir parametre değil.
            hedef_alinan_w = self.gurultu_w * db_to_lin(konfig.sinr_esigi_db)
            self.verici_gucu_w = hedef_alinan_w * db_to_lin(
                self.yol_kaybi_db(konfig.nominal_bag_m))
        else:
            # 🔒 A7 (K-178): güç GİRDİ (EIRP; anten deseni en büyük kazanca
            # göre normalize — kayıp ≥ 0). Menzil ondan türemiş olmalı:
            # menzilde ortalama SNR `menzil_snr_db` — tutarlılık kapısı.
            self.verici_gucu_w = dbm_to_w(konfig.verici_eirp_dbm)
            snr = lin_to_db(self.verici_gucu_w / db_to_lin(
                self.yol_kaybi_db(konfig.nominal_bag_m)
                - konfig.alici_anten_kazanci_dbi) / self.gurultu_w)
            dogrula(abs(snr - konfig.menzil_snr_db) < 0.05,
                    f"menzil verici gücüyle tutarsız: menzilde SNR {snr:.3f} "
                    f"dB ≠ {konfig.menzil_snr_db:.3f} dB — "
                    "`kanal/dunya.py::referans_2026` kullanın")
        self._hucre_m = konfig.golgeleme_hucre_m
        self._sigma_db = konfig.golgeleme_sigma_db if konfig.golgeleme_acik else 0.0
        # 🔒 KÖŞE ÖNBELLEĞİ — SONUCU DEĞİŞTİRMEZ, yalnız hızlandırır.
        # `normal_cekimi` tam sayı anahtarların SAF bir fonksiyonudur; aynı
        # anahtar her zaman aynı sayıyı verir. Ölçüldü: gölgeleme çekimi koşu
        # süresinin %52'siydi (10,4 milyon çekim / 354 bin olay), çünkü her
        # SINR parçası aynı bağın aynı hücre köşelerini yeniden çekiyordu.
        # Önbellek dolduğunda TAMAMEN boşaltılır; bu da belirlenimcidir (aynı
        # erişim dizisi → aynı boşaltma anları) ve değerler yeniden
        # üretilebilir olduğu için hiçbir bilgi kaybolmaz.
        self._golge_onbellek: dict[tuple[int, int, int, int, int], float] = {}
        self._yavas_onbellek: dict[tuple, float] = {}

    # ------------------------------------------------------------- gürültü
    @staticmethod
    def gurultu_tabani_w(konfig: Konfig) -> float:
        """N = k·T·B·F — analitik doğrulama hedefi.

        290 K'de 2 MHz bant için k·T·B ≈ −111,0 dBm; 6 dB gürültü figürüyle
        ≈ −105,0 dBm.
        """
        termal = (BOLTZMANN * konfig.sicaklik_k * konfig.bant_genisligi_hz)
        return termal * db_to_lin(konfig.gurultu_figuru_db)

    # ------------------------------------------------------------ yol kaybı
    def yol_kaybi_db(self, mesafe_m: float) -> float:
        """PL(d) = PL(1 m) + 10·α·log10(d),  PL(1 m) = 20·log10(4π·f/c).

        2,4 GHz'de PL(1 m) ≈ 40,05 dB — analitik olarak doğrulanır.
        """
        d = max(mesafe_m, REFERANS_MESAFE_M)
        return self._pl_referans_db + 10.0 * self.konfig.yol_kaybi_usteli \
            * math.log10(d / REFERANS_MESAFE_M)

    # -------------------------------------------------------- anten deseni
    def anten_kaybi_db(self, yukselis_rad: float) -> float:
        """Yarım dalga dipolün **bir ucundaki** kaybı, kapalı formda.

            F(φ) = cos(½π·sin φ) / cos φ          (φ = yataya göre yükseliş)
            kayıp_dB = −20·log10 F(φ)

        φ = 0'da F = 1 (kayıp 0); φ → 90°'de F → 0 (dipolün ekseni boyunca
        yayın yok). Kapalı form olduğu için analitik doğrulanabilir.

        🔴 BİR BAĞDA İKİ ANTEN VARDIR: `bag_anten_kaybi_db` iki ucu toplar.
        Tek uç sayılsaydı bağ bütçesi sistematik olarak iyimser olurdu.
        """
        if not self.konfig.anten_deseni_acik:
            return 0.0
        phi = abs(yukselis_rad)
        kos = math.cos(phi)
        if kos <= 1e-12:                      # dipol ekseni — yayın yok
            return 60.0                       # kelepçe: −60 dB pratikte sıfır
        f = math.cos(0.5 * math.pi * math.sin(phi)) / kos
        if f <= 1e-6:
            return 60.0
        return min(-20.0 * math.log10(f), 60.0)

    def bag_anten_kaybi_db(self, a: Nokta3, b: Nokta3) -> float:
        """İki ucun toplam anten kaybı. Bağ-simetrik: yükseliş açısı aynıdır."""
        phi = yukselis_acisi_rad(a, b)
        return 2.0 * self.anten_kaybi_db(phi)

    # ---------------------------------------------------------- gölgeleme
    def golgeleme_db(self, i: int, j: int, a: Nokta3, b: Nokta3) -> float:
        """Log-normal X_σ — bağ-simetrik, konuma bağlı, SÜREKLİ.

        Bağ ortasının bulunduğu hücrenin sekiz köşesinden çekilen bağımsız
        normaller, trilineer ağırlıklarla harmanlanır.

        🔴 AĞIRLIKLAR VARYANSI DÜŞÜRÜR ve bu düzeltilir. `Σ wₖ = 1` olduğu
        için `Var(Σ wₖ Xₖ) = Σ wₖ²` ve bu, hücre merkezinde 1/8'e kadar iner
        — düzeltilmeseydi ilan edilen σ, alanın çoğunda GERÇEKLEŞMEZDİ.
        `√(Σ wₖ²)`ye bölmek varyansı her yerde tam olarak 1 yapar ve ağırlıklar
        konumla sürekli değiştiği için alan sürekli kalır.
        """
        if self._sigma_db <= 0.0:
            return 0.0
        ox = 0.5 * (a.x + b.x)
        oy = 0.5 * (a.y + b.y)
        oz = 0.5 * (a.z + b.z)
        h = self._hucre_m
        gx, gy, gz = ox / h, oy / h, oz / h
        cx, cy, cz = math.floor(gx), math.floor(gy), math.floor(gz)
        fx, fy, fz = gx - cx, gy - cy, gz - cz
        alt, ust = min(i, j), max(i, j)
        onbellek = self._golge_onbellek

        toplam = 0.0
        agirlik_kare = 0.0
        for dx in (0, 1):
            wx = fx if dx else 1.0 - fx
            for dy in (0, 1):
                wy = fy if dy else 1.0 - fy
                for dz in (0, 1):
                    wz = fz if dz else 1.0 - fz
                    w = wx * wy * wz
                    if w == 0.0:
                        continue
                    anahtar = (alt, ust, cx + dx, cy + dy, cz + dz)
                    deger = onbellek.get(anahtar)
                    if deger is None:
                        deger = normal_cekimi("golgeleme", self.konfig.tohum,
                                              *anahtar)
                        if len(onbellek) >= KOSE_ONBELLEK_SINIRI:
                            onbellek.clear()
                        onbellek[anahtar] = deger
                    toplam += w * deger
                    agirlik_kare += w * w
        if agirlik_kare <= 0.0:
            return 0.0
        return self._sigma_db * toplam / math.sqrt(agirlik_kare)

    # ------------------------------------------------------- alınan güç
    def yavas_kayip_db(self, i: int, j: int, a: Nokta3, b: Nokta3) -> float:
        """Yol kaybı + anten + gölgeleme. Hızlı sönümleme DÂHİL DEĞİL.

        🔒 K-190 — ÖNBELLEKLİ, SONUÇ BİT BİT AYNI: saf bir fonksiyondur
        (kimlikler ve iki konum); anahtar TAM girdidir, değer aynı işlemle
        hesaplanır. Referans dünyada koşu süresinin ~%45'i buradaydı
        (`arsiv/teshis/faz4_2026-09-26/j_profil.txt`); statik kolda her çift
        tek kez hesaplanır, hareketli kolda aynı anda tekrarlanan çağrılar.
        """
        anahtar = (i, j, a, b)
        onbellek = self._yavas_onbellek
        deger = onbellek.get(anahtar)
        if deger is None:
            deger = (self.yol_kaybi_db(mesafe(a, b))
                     + self.bag_anten_kaybi_db(a, b)
                     + self.golgeleme_db(i, j, a, b)
                     - self.konfig.alici_anten_kazanci_dbi)  # A7 (K-178)
            if len(onbellek) >= YAVAS_ONBELLEK_SINIRI:
                onbellek.clear()
            onbellek[anahtar] = deger
        return deger

    def yavas_alinan_w(self, i: int, j: int, a: Nokta3, b: Nokta3,
                       verici_w: float | None = None) -> float:
        pt = self.verici_gucu_w if verici_w is None else verici_w
        return pt / db_to_lin(self.yavas_kayip_db(i, j, a, b))

    def yavas_sinr_db(self, i: int, j: int, a: Nokta3, b: Nokta3,
                      girisim_w: float = 0.0) -> float:
        """🔒 `kopma_fiziksel` BU büyüklükle tanımlanır (Adım 8 taahhüdü).

        Hızlı sönümleme dışarıda: saniyede yüzlerce kez eşiği geçer ve onu
        kopma saymak sayacı gürültüye çevirirdi.
        """
        s = self.yavas_alinan_w(i, j, a, b)
        return lin_to_db(s / (self.gurultu_w + girisim_w))

    def bag_kopuk_mu(self, i: int, j: int, a: Nokta3, b: Nokta3,
                     girisim_w: float = 0.0) -> bool:
        return self.yavas_sinr_db(i, j, a, b, girisim_w) < self.konfig.sinr_esigi_db

    # ---------------------------------------------------------------- teşhis
    def menzilde_yavas_sinr_db(self) -> float:
        """Menzil sınırında, gölgelemesiz ve antensiz SINR — β'ya eşit olmalı.

        Verici gücünün türetiminin kendi tanımıyla tutarlı olduğunu gösteren
        kapalı devre kontrol.
        """
        pr = self.verici_gucu_w / db_to_lin(
            self.yol_kaybi_db(self.konfig.nominal_bag_m)
            - self.konfig.alici_anten_kazanci_dbi)
        return lin_to_db(pr / self.gurultu_w)


dogrula(REFERANS_MESAFE_M > 0.0, "referans mesafe pozitif olmalı")
