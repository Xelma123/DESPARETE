"""
Kat 2 — Radyo.

    mesafe ──► yol kaybı ──► alınan güç ─┐
                                          ├──► SINR ──► paket hata olasılığı
    gürültü + karıştırıcı + girişim ──────┘

TEK DOĞRU KAYNAĞI İLKESİ
========================
Bu modüldeki hiçbir sayı elle yazılmamıştır. Hepsi ya fiziksel sabittir
(Boltzmann, ışık hızı) ya da konfigürasyondan TÜRETİLİR.

En kritik türetim: verici gücü.

    İletim menzili R, "girişimsiz SINR'in tam olarak eşiğe (β) eşit olduğu
    mesafe" olarak TANIMLANIR. Buradan:

        Pt = N + β + YolKaybı(R)          [dB cinsinden]

    Yani Pt bağımsız bir parametre değil. Böylece topolojinin geometrik
    menzili ile radyonun fiziği ASLA çelişemez — çelişselerdi, hangi
    düğümlerin komşu olduğu iki farklı cevap verirdi ve sonuçlar sessizce
    yanlış olurdu.

SERT GEÇİŞ UYARISI — rapora girer
==================================
Gölgeleme yok (K-015/6), yani yayılım belirlenimci. Sonucu: bağ kalitesi
mesafeyle çok hızlı düşer.

    d = R      →  PER ≈ %17   (kullanılabilir ama kayıplı)
    d = 1,2·R  →  PER ≈ %100  (ölü)

Bu, gerçek RF ortamına göre bir basitleştirmedir: gölgeleme bu geçişi
yumuşatır. ⚠️ Ve H1.2 (dirsek hipotezi) için doğrudan bir tehdittir —
ağ seviyesindeki dirsek, bağ seviyesindeki keskinliğin yansıması olabilir.
Bu yüzden H1.2'ye bir mekanizma kontrolü eklendi: bağ PER eğrisi ile ağ
PDR eğrisi AYRI ölçülür ve dirsek noktaları karşılaştırılır.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .config import Konfig

# Fiziksel sabitler
BOLTZMANN = 1.380649e-23        # J/K
ISIK_HIZI = 2.99792458e8        # m/s

# Referans mesafe: yol kaybı formülü bunun altında geçerli değildir.
# Klemplenmezse d→0'da güç sonsuza gider.
REFERANS_MESAFE_M = 1.0


# --------------------------------------------------------------------------
# Birim dönüşümleri
# --------------------------------------------------------------------------

def dbm_to_w(dbm: float) -> float:
    return 10.0 ** ((dbm - 30.0) / 10.0)


def w_to_dbm(w: float) -> float:
    if w <= 0.0:
        return float("-inf")
    return 10.0 * math.log10(w) + 30.0


def db_to_lin(db: float) -> float:
    return 10.0 ** (db / 10.0)


def lin_to_db(lin: float) -> float:
    if lin <= 0.0:
        return float("-inf")
    return 10.0 * math.log10(lin)


# --------------------------------------------------------------------------
# Radyo
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Radyo:
    """Yayılım ve hata modeli. Durum tutmaz — saf fonksiyonlar."""

    yol_kaybi_usteli: float
    frekans_hz: float
    gurultu_gucu_w: float
    verici_gucu_w: float
    bit_hizi_bps: float

    # ------------------------------------------------------------------ kur
    @staticmethod
    def kur(kon: Konfig) -> "Radyo":
        gurultu_w = Radyo.gurultu_tabani_w(kon)
        # Pt, menzil tanımından TÜRETİLİR — bağımsız parametre değil.
        hedef_alinan_w = gurultu_w * db_to_lin(kon.sinr_esigi_db)
        yol_kaybi_lin = db_to_lin(
            Radyo.yol_kaybi_db_statik(
                kon.iletim_menzili_m, kon.yol_kaybi_usteli, kon.frekans_hz
            )
        )
        return Radyo(
            yol_kaybi_usteli=kon.yol_kaybi_usteli,
            frekans_hz=kon.frekans_hz,
            gurultu_gucu_w=gurultu_w,
            verici_gucu_w=hedef_alinan_w * yol_kaybi_lin,
            bit_hizi_bps=kon.bit_hizi_bps,
        )

    # --------------------------------------------------------------- gürültü
    @staticmethod
    def gurultu_tabani_w(kon: Konfig) -> float:
        """Termal gürültü + alıcı gürültü figürü:  N = k·T·B·F

        Analitik doğrulama hedefi (Aile 0, K3): 290 K'de 1 MHz bant için
        k·T·B ≈ -114 dBm; 6 dB gürültü figürüyle ≈ -108 dBm.
        """
        termal_w = BOLTZMANN * kon.sicaklik_k * kon.bant_genisligi_hz
        return termal_w * db_to_lin(kon.gurultu_figuru_db)

    # -------------------------------------------------------------- yol kaybı
    @staticmethod
    def yol_kaybi_db_statik(mesafe_m: float, ustel: float, frekans_hz: float) -> float:
        """Log-mesafe yol kaybı, 1 m referansta serbest uzay (Friis) ile bağlı.

            PL(d) = PL(d0) + 10·α·log10(d/d0)
            PL(d0) = 20·log10(4π·d0·f / c)

        2,4 GHz'de PL(1 m) ≈ 40,0 dB — bu sayı Aile 0'da analitik olarak
        doğrulanacak.
        """
        d = max(mesafe_m, REFERANS_MESAFE_M)
        pl_referans = 20.0 * math.log10(
            4.0 * math.pi * REFERANS_MESAFE_M * frekans_hz / ISIK_HIZI
        )
        return pl_referans + 10.0 * ustel * math.log10(d / REFERANS_MESAFE_M)

    def yol_kaybi_db(self, mesafe_m: float) -> float:
        return self.yol_kaybi_db_statik(
            mesafe_m, self.yol_kaybi_usteli, self.frekans_hz
        )

    def alinan_guc_w(self, mesafe_m: float, verici_gucu_w: float | None = None) -> float:
        pt = self.verici_gucu_w if verici_gucu_w is None else verici_gucu_w
        return pt / db_to_lin(self.yol_kaybi_db(mesafe_m))

    # ------------------------------------------------------------------ SINR
    def sinr_lin(self, sinyal_w: float, girisim_w: float = 0.0) -> float:
        return sinyal_w / (self.gurultu_gucu_w + girisim_w)

    def sinr_db(self, sinyal_w: float, girisim_w: float = 0.0) -> float:
        return lin_to_db(self.sinr_lin(sinyal_w, girisim_w))

    # ------------------------------------------------- paket hata olasılığı
    def bit_hata_orani(self, sinr_lineer: float) -> float:
        """Eşevresiz DBPSK:  BER = ½·e^(−γ)

        Neden bu model:
        - Kapalı form → ANALİTİK OLARAK DOĞRULANABİLİR (Aile 0, K3)
        - 802.11b'nin 1 Mbit/s modülasyonuna karşılık gelir
        - Sert eşik değil, düzgün bir geçiş verir

        Sert eşik (SINR ≥ β → başarı) kullanılmadı çünkü H1.2'nin dirseğini
        model tarafından İNŞA EDİLMİŞ hâle getirirdi.
        """
        if sinr_lineer <= 0.0:
            return 0.5
        return 0.5 * math.exp(-sinr_lineer)

    def paket_hata_olasiligi(self, sinr_lineer: float, bayt: int) -> float:
        """PER = 1 − (1 − BER)^(8·bayt)

        Bit hataları bağımsız varsayılır (patlamalı hata yok). Bu bir
        basitleştirmedir ve rapora yazılır: gerçek kanallarda hatalar
        kümelenir, bu da aynı ortalama BER'de PER'i DÜŞÜRÜR.
        """
        ber = self.bit_hata_orani(sinr_lineer)
        bit = 8 * bayt
        if ber <= 0.0:
            return 0.0
        if ber >= 0.5:
            return 1.0
        # log uzayında: (1-ber)^bit taşmasın
        return -math.expm1(bit * math.log1p(-ber))

    # ---------------------------------------------------------------- teşhis
    def menzilde_per(self, menzil_m: float, bayt: int) -> float:
        s = self.alinan_guc_w(menzil_m)
        return self.paket_hata_olasiligi(self.sinr_lin(s), bayt)


# --------------------------------------------------------------------------
# Karıştırıcılar
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Karistirici:
    """Geniş bantlı gürültü kaynağı.

    ⚠️ Karıştırıcı ağın bir üyesi DEĞİLDİR: paket almaz, göndermez, kanalı
    dinlemez. Yalnızca gürültü yayar. Tepkisel karıştırıcı (iletimi duyup
    üstüne basan) kapsam dışıdır — MAC ile iç içe geçmiş, ayrı bir araştırma.
    (04-NEDEN-BOYLE.md, K-008)
    """

    # 🔴 B-14 — HİÇBİR ALANIN VARSAYILANI YOKTUR, BİLEREK.
    # ---------------------------------------------------------------------
    # Önceki hâlde dört alan `Konfig`in ikinci bir kopyasıydı
    # (`periyot_s=2,7 · gorev_cevrimi=0,5 · hiz_ms=15,0 ·
    # `yorunge_yaricap_m=300,0`). Bugün zararsızdı çünkü tek çağıran
    # `senaryodan()` hepsini açıkça geçiyor — ama tam olarak bu desen bir kez
    # gerçek bir hataya yol açtı: `rng.kanal_cekimi`in varsayılan dilimi
    # 1 ms'de kalırken `Konfig` 100 µs'ye inmişti (K-024). Orada varsayılan
    # aynı gerekçeyle kaldırıldı; burada kaldırılmamıştı.
    #
    # `faz_kesri` de zorunlu: varsayılanı `0.0` idi, yani REZONANS KORUMASININ
    # KAPALI hâli. Fazı geçmeyi unutan bir çağrı, darbe trenini her tohumda
    # aynı anda başlatır ve `03` B6'nın rezonans tuzağını sessizce geri
    # getirirdi.
    #
    # ⚖️ Denetim metnindeki "hiz_ms = 15,0, K-026'nın yanlış dediği değer"
    # gerekçesi ARTIK GEÇERSİZDİR: K-035 hızı zaten 15 m/s'ye geri döndürdü,
    # yani iki değer bugün çakışıyor. Duran gerekçe yapısaldır — çakışıyor
    # olmaları, ikinci kopya olmadıkları anlamına gelmez.
    #
    # Regresyon: `test_b14_karistiricinin_hicbir_alaninda_varsayilan_yok`
    guc_w: float
    konum: tuple[float, float]
    yol_kaybi_usteli: float
    frekans_hz: float

    # darbeli
    darbeli: bool
    periyot_s: float
    gorev_cevrimi: float
    # 🔴 ADI 20 AĞUSTOS'TA DEĞİŞTİ: `faz_s` -> `faz_kesri` (B-38).
    # Alan SANİYE DEĞİL, birimsiz bir TUR/PERİYOT KESRİDİR (∈ [0,1)):
    #     acik_mi  : evre = ((zaman_s / periyot_s) + faz_kesri) % 1.0
    #     konum_t  : aci  = 2π * ((hiz*zaman_s)/cevre + faz_kesri)
    # `_s` soneki taşıyan bir alana saniye geçen bir çağıran — ör.
    # `faz_kesri=1.35` ("yarım periyot") — sessizce 0,35 alırdı. Bugün hata
    # yoktu; B-14 alanı zorunlu yaptığı için her çağıran onu açıkça
    # dolduruyor, yani yanlış birim geçme yolu AÇIKTI.
    faz_kesri: float                  # 🔴 her tohumda rastgelelenir — rezonans koruması

    # hareketli
    hareketli: bool
    hiz_ms: float
    yorunge_yaricap_m: float

    # ----------------------------------------------------------------- konum
    def konum_t(self, zaman_s: float) -> tuple[float, float]:
        """Hareketli karıştırıcı: merkez etrafında dairesel, BELİRLENİMCİ yörünge.

        Belirlenimci seçildi çünkü rastgele bir yörünge, tohumlar arası
        varyansa karıştırıcı hareketini de katardı ve protokol farkını
        gizlerdi. Yörüngenin başlangıç fazı ise rastgeledir.
        """
        if not self.hareketli:
            return self.konum
        cevre = 2.0 * math.pi * self.yorunge_yaricap_m
        aci = 2.0 * math.pi * ((self.hiz_ms * zaman_s) / cevre + self.faz_kesri)
        return (
            self.konum[0] + self.yorunge_yaricap_m * math.cos(aci),
            self.konum[1] + self.yorunge_yaricap_m * math.sin(aci),
        )

    # ------------------------------------------------------------------ açık
    def acik_mi(self, zaman_s: float) -> bool:
        if not self.darbeli:
            return True
        # Faz kaydırması: darbe treni her tohumda farklı yerden başlar.
        evre = ((zaman_s / self.periyot_s) + self.faz_kesri) % 1.0
        return evre < self.gorev_cevrimi

    # ------------------------------------------------------------------- güç
    def alinan_guc_w(self, alici_konum: tuple[float, float], zaman_s: float) -> float:
        """Alıcıdaki karıştırıcı gürültü gücü. Kapalıysa sıfır."""
        if not self.acik_mi(zaman_s):
            return 0.0
        jx, jy = self.konum_t(zaman_s)
        d = max(math.hypot(alici_konum[0] - jx, alici_konum[1] - jy),
                REFERANS_MESAFE_M)
        pl_db = Radyo.yol_kaybi_db_statik(d, self.yol_kaybi_usteli, self.frekans_hz)
        return self.guc_w / db_to_lin(pl_db)

    # ------------------------------------------------------------- fabrika
    @staticmethod
    def senaryodan(kon: Konfig, akislar) -> "Karistirici | None":
        """Senaryodan karıştırıcı kurar. S0'da None döner.

        🔴 Faz `karistirici_faz` AKIŞINDAN çekilir — kendi akışından.
        Ortak bir akış kullanılsaydı, darbe fazı protokolün çektiği rastgele
        sayı adedine bağlı olurdu ve iki kol farklı karıştırıcı görürdü.
        """
        if not kon.karistirici_var_mi:
            return None
        faz = akislar["karistirici_faz"].random()
        return Karistirici(
            guc_w=dbm_to_w(kon.karistirici_guc_dbm),
            konum=kon.karistirici_merkez,
            yol_kaybi_usteli=kon.yol_kaybi_usteli,
            frekans_hz=kon.frekans_hz,
            darbeli=kon.karistirici_darbeli,
            periyot_s=kon.darbe_periyodu_s,
            gorev_cevrimi=kon.darbe_gorev_cevrimi,
            faz_kesri=faz,
            hareketli=kon.karistirici_hareketli,
            hiz_ms=kon.karistirici_hiz_ms,
            yorunge_yaricap_m=kon.karistirici_yorunge_yaricap_m,
        )

    # ---------------------------------------------------------------- ortalama
    @property
    def ortalama_guc_carpani(self) -> float:
        """Darbeli karıştırıcının ortalama gücü tepe gücünün bu katıdır.

        ⭐ H1.3 (aynı ORTALAMA güçte sabit vs darbeli) bu çarpanla kurulur:
        darbeli karıştırıcının tepe gücü, sabit olanın ortalama gücüne
        eşitlenmek için 1/görev_çevrimi ile yükseltilir.
        """
        return self.gorev_cevrimi if self.darbeli else 1.0
