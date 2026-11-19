"""
DESPARETE 5 — karıştırma altındaki taktik İHA sürüsü için tek hedefli
yönlendirme protokolü. Tasarım kararları `v2/17` (T-1…T-20), kurallar
`v2/kural/KK-00…KK-05`.

Bu dosya parçaları simülatörün kancalarına bağlar; kuralların kendisi saf
modüllerdedir:

    desparete5_bicim     değerler, bayraklar, iletiler (KK-00)
    desparete5_bag       bağın durumu ve ölçüsü, bağa ait kanıt (KK-01, KK-03 B)
    desparete5_selam     selam ve ara ilan (KK-02)
    desparete5_kanit     kendi "karıştırılıyorum" durumum (KK-03 A)
    desparete5_egim      rota seçimi ve döngü bekçisi (KK-04, 19 Kasım; `egim`)
    desparete5_rota      18 Kasım'ın rotası: FD, tur, açlık (`egim` kapalıyken)
    desparete5_bekletme  bekletme ve geri iz (KK-05)

🔒 İKİ TASARIM, BİR SINIF (19 Kasım): `egim` açıkken yol seçimi `Egim`,
selam `SELAM_E` (tur alanı yok), döngü bekçisi `cerceve_duyuldu` ve
`sonraki_atlama`da; kapalıyken 18 Kasım'ın `Rota`sı ve `SELAM`ı, değişmeden.

🔒 KÂHİN ERİŞİMİ YOK. Yalnız `sim2/gozlem/`i içe aktarır ve `KK-00`ın
"gözlemin kullanımı" tablosundakini okur: `mesgul_sure_s` (yalnız
`karistirma_durumu` açıkken ister) · `alinan_cerceve` · `saat_s` ·
kontrol mesajları · MAC sonuçları · çözülen çerçevenin göndereni, türü,
hedefi ve veri başlığı · karar anında paketin başlığı · geçidin kimliği
(yapılandırma). RSSI, ölçülen gürültü, konum ve simülatörün komşu listesi
OKUNMAZ (`kosum_beaconi = False`).

🔒 KANCA SONU (Babel'in gerçeklemesindeki düzenle aynı): her niyetli kancanın
sonunda zaman olayları → rota seçimi → selam olayları → tur istekleri →
tampon uyandırması → en erken son tarihe uyandırma → ölçüm beyanları.
Niyet döndüremeyen kancalar (`iletim_sonucu`, `cerceve_duyuldu`) yalnız
durumu kaydeder; gerektirdiği niyet bir sonraki niyetli kancada, en geç
saniyelik zamanlayıcıda verilir (KK-00 genel kural 1).

🔒 ÖLÇÜM BEYANLARI — Babel, AODV ve OLSRv2 ile aynı anlam (K-139)
    kopma(K)         bir önceki kanca sonunda ardılım olan K'nin bağı
                     kullanılamaz oldu (OLAĞAN'dan çıktı ya da silindi)
    rota_kuruldu(K)  K'nin kaybından sonra yeniden ardılım var
    rota_gecersiz    daha önce yolu olan bir hedefe giden paket düştü
"""

from __future__ import annotations

import math

from sim2.gozlem.karar import Beyan, Karar
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from sim2.gozlem.pencere import Gozlem
from protokoller.desparete5_bag import BagTablosu
from protokoller.desparete5_bekletme import (
    BEKLET, GONDER, Bekletme, GeriIz)
from protokoller.desparete5_bicim import (
    SELAM, SELAM_E, TAM, TUR_ISTEGI, Bayraklar, Degerler)
from protokoller.desparete5_egim import Egim
from protokoller.desparete5_kanit import KendiDurum
from protokoller.desparete5_rota import Rota
from protokoller.desparete5_selam import (
    ETIKET, SelamZamanlayici, onemli_degisim, selam_coz, selam_yuku)

__all__ = ["Desparete5"]

_ZAMAN, _TAMPON, _SANIYE = "zaman:", "tampon:", "saniye"
_INF = math.inf


class Desparete5:
    """DESPARETE'nin Faz 5 sürümü."""

    ad = "desparete5"
    kosum_beaconi = False               # kendi selamı var (KK-02)

    __slots__ = ("kimlik", "gecit", "d", "b", "bag", "selam", "rota",
                 "kendi", "bekletme", "iz", "_basladi", "_planli_s",
                 "_plan_nesil", "_tampon_planli", "_tampon_nesil",
                 "_ardil_onceki", "_beyan_ardil", "_kopuk", "_rota_vardi",
                 "_bit_ilan", "_sayac")

    def __init__(self, kimlik: int, gecit: int | None,
                 bayraklar: Bayraklar = TAM,
                 degerler: Degerler | None = None) -> None:
        if gecit is None:
            raise ValueError("DESPARETE 5 tek hedeflidir: geçit gerekir "
                             "(yere toplama deseni)")
        if not 0 <= kimlik < 256:
            raise ValueError("selamın adres alanı 8 bit: düğüm ≤ 255")
        d = degerler if degerler is not None else Degerler()
        self.kimlik = kimlik
        self.gecit = gecit
        self.d = d
        self.b = bayraklar
        self.bag = BagTablosu(d, bayraklar)
        self.selam = SelamZamanlayici(d, bayraklar)
        self.rota = (Egim(kimlik, gecit, d, bayraklar) if bayraklar.egim
                     else Rota(kimlik, gecit, d, bayraklar))
        self.kendi = KendiDurum(d, bayraklar)
        self.bekletme = Bekletme(d, bayraklar)
        self.iz = GeriIz(d)
        self._basladi = False
        self._planli_s = _INF               # en erken son tarih uyandırması
        self._plan_nesil = 0
        self._tampon_planli = -_INF         # tamponu yeniden sorma uyandırması
        self._tampon_nesil = 0
        self._ardil_onceki: int | None = None
        self._beyan_ardil: int | None = None
        self._kopuk: set[int] = set()
        self._rota_vardi = False
        self._bit_ilan = False
        self._sayac: dict[str, int] = {
            "veri_gonderilen": 0, "veri_bekletilen": 0, "veri_dusen": 0,
            "komut_gonderilen": 0, "komut_bekletilen": 0, "komut_dusen": 0,
            "tur_istegi_gonderilen": 0, "selam_gonderilen": 0,
            "kopma_beyani": 0,
        }

    @property
    def kanal_dolulugu_ister(self) -> bool:
        """`mesgul_sure_s` yalnız karıştırma kanıtı açıkken istenir (KK-03)."""
        return self.b.karistirma_durumu

    # ==================================================================
    # Kanca sonu
    # ==================================================================
    def _zaman(self, t: float) -> None:
        self.bag.zaman_isle(t)
        self.rota.zaman_isle(t, self.bag, self.kendi.dondurma)
        self.bekletme.temizle(t)

    def _bit(self) -> bool:
        return self.b.alici_bildirimi and self.kendi.karistiriliyorum

    def _bitir(self, t: float, ek: tuple = ()) -> tuple:
        self._zaman(t)
        self.rota.sec(t, self.bag, self.kendi.dondurma)
        niyet: list = list(ek)
        # KK-02/3: değişim olayları
        _, yeni_komsu = self.bag.bayraklari_oku()
        olay = yeni_komsu
        olay |= self.rota.olay_oku()
        olay |= onemli_degisim(self.rota.ilan()[1], self.rota.son_ilan_C,
                               self.d.ILAN_ESIGI)
        olay |= self._bit() != self._bit_ilan
        # Gönderemezken selam planlanmaz (KK-02/5): durum bitince hemen gider.
        if olay and self._basladi and not self.kendi.gonderemez:
            u = self.selam.olay(t)
            if u is not None:
                niyet.append(u)
        for hedef, istenen, kalan in self.rota.istekleri_al():
            niyet.append(KontrolIstegi.kur(
                hedef, TUR_ISTEGI, {"istenen": istenen, "kalan": kalan}))
            self._sayac["tur_istegi_gonderilen"] += 1
        # KK-05/3: yol bulununca hemen, bekleyen varken 0,5 s'de bir.
        if self.bekletme.bekleyen_var:
            yol_bulundu = (self.rota.ardil is not None
                           and self._ardil_onceki is None)
            u = self._tampon_uyandir(
                t, 1e-3 if yol_bulundu else self.d.YENIDEN_SOR_S)
            if u is not None:
                niyet.append(u)
        self._ardil_onceki = self.rota.ardil
        # En erken son tarih (bağ ve rota zamanlayıcıları).
        son = min(self.bag.son_tarih(), self.rota.son_tarih())
        if son < _INF and (son < self._planli_s - 1e-9
                           or self._planli_s <= t):
            self._planli_s = son
            self._plan_nesil += 1
            niyet.append(Uyandirma(max(son - t, 1e-3),
                                   f"{_ZAMAN}{self._plan_nesil}"))
        return tuple(niyet) + self._beyanlar()

    def _tampon_uyandir(self, t: float, gecikme: float) -> Uyandirma | None:
        """Simülatör tamponu yalnız bir uyandırmadan sonra döker (K-135).
        Uyandırma iptal edilemez; daha erken bir plan varsa yenisi kurulmaz."""
        if t < self._tampon_planli <= t + gecikme:
            return None
        self._tampon_planli = t + gecikme
        self._tampon_nesil += 1
        return Uyandirma(gecikme, f"{_TAMPON}{self._tampon_nesil}")

    def _beyanlar(self) -> tuple:
        cikti: list = []
        k = self._beyan_ardil
        if k is not None and not self.bag.kullanilir_mi(k):
            cikti.append(Beyan("kopma", komsu=k))
            self._kopuk.add(k)
            self._sayac["kopma_beyani"] += 1
        if self.rota.ardil is not None:
            self._rota_vardi = True
            for j in sorted(self._kopuk):
                cikti.append(Beyan("rota_kuruldu", komsu=j))
            self._kopuk.clear()
        self._beyan_ardil = self.rota.ardil
        return tuple(cikti)

    # ==================================================================
    # Kontrol kancaları
    # ==================================================================
    def zamanlayicilar(self) -> dict:
        return {_SANIYE: 1.0}

    def zamanlayici_doldu(self, gozlem: Gozlem, etiket: str) -> tuple:
        """Saniyelik iş: ilk çağrıda selam başlar; kendi durumum (KK-03 A)."""
        t = float(gozlem.saat_s)
        self._zaman(t)
        ek: list = []
        if not self._basladi:
            self._basladi = True
            u = self.selam.baslat(t)
            if u is not None:
                ek.append(u)
        olay = self.kendi.saniye(t, gozlem.mesgul_sure_s,
                                 gozlem.alinan_cerceve,
                                 self.bag.selam_kaybi(t))
        if "basladi" in olay:
            self.bag.kendi_basla(t)
        if "dondurma_bitti" in olay:
            self.bag.kendi_bitir(t)
            self.rota.kendi_bitti(t, self.bag)
        if "ed_bitti" in olay:
            u = self.selam.ed_bitti(t)
            if u is not None:
                ek.append(u)
        return self._bitir(t, tuple(ek))

    def uyandi(self, gozlem: Gozlem, etiket: str) -> tuple:
        t = float(gozlem.saat_s)
        if etiket.startswith(ETIKET):
            if not self.selam.guncel_mi(etiket):
                return self._bitir(t)
            niyet = self._bitir(t)
            sonuc, sonraki = self.selam.kur(t, self.kendi.gonderemez)
            ek: list = []
            if sonuc is not None:
                ek.append(self._selam_kur(*sonuc))
            if sonraki is not None:
                ek.append(sonraki)
            return tuple(ek) + niyet
        if etiket.startswith(_ZAMAN):
            if int(etiket[len(_ZAMAN):]) == self._plan_nesil:
                self._planli_s = _INF
        elif etiket.startswith(_TAMPON):
            if int(etiket[len(_TAMPON):]) == self._tampon_nesil:
                self._tampon_planli = -_INF
        return self._bitir(t)

    def _selam_kur(self, sira: int, aralik_s: float) -> KontrolIstegi:
        """KK-02: selam o anki bilgiyle kurulur; ilan edilen maliyet
        `C_ilan` olur (eğim kapalıyken (tur, maliyet) FD'yi günceller;
        KK-02/7). Eğimde tur alanı yoktur (`SELAM_E`)."""
        tur, C = self.rota.ilan()
        self.rota.ilan_edildi(tur, C)
        komsu, oran = self.bag.liste()
        bit = self._bit()
        self._bit_ilan = bit
        self._sayac["selam_gonderilen"] += 1
        if self.b.egim:
            return KontrolIstegi.kur(None, SELAM_E, selam_yuku(
                sira, aralik_s, None, C, bit, komsu, oran))
        return KontrolIstegi.kur(None, SELAM, selam_yuku(
            sira, aralik_s, tur, C, bit, komsu, oran))

    def kontrol_alindi(self, gozlem: Gozlem, gonderen: int, bicim: str,
                       yuk, yayin: bool) -> tuple:
        t = float(gozlem.saat_s)
        self._zaman(t)
        if bicim in (SELAM.ad, SELAM_E.ad):
            sira, aralik, tur, C, bit, bildirilen = selam_coz(yuk, self.kimlik)
            self.bag.selam_al(gonderen, t, sira, aralik, bildirilen, bit)
            self.rota.ilan_al(gonderen, t, tur, C)
        elif bicim == TUR_ISTEGI.ad:
            y = dict(yuk)
            self.rota.istek_al(gonderen, t, int(y["istenen"]), int(y["kalan"]))
        return self._bitir(t)

    def iletim_basarisiz(self, gozlem: Gozlem, hedef: int | None,
                         tur: str) -> tuple:
        """Sonuç `iletim_sonucu`nda işlendi (önce o çağrılır); burada
        gerektirdiği niyetler verilir (T-9: vazgeçme kanıttır, karar değil)."""
        return self._bitir(float(gozlem.saat_s))

    # ==================================================================
    # Niyet döndürmeyen kancalar
    # ==================================================================
    def iletim_sonucu(self, gozlem: Gozlem, hedef: int, basarili: bool,
                      tekrar: int, tur: str) -> None:
        """KK-01/6 vazgeçme kaydı (eğim kapalıyken eski veri tetiği) ·
        KK-03/7 MAC kanıtı (K-151)."""
        t = float(gozlem.saat_s)
        self.bag.zaman_isle(t)
        self.bag.veri_sonucu(hedef, t, basarili, tekrar, tur)
        return None

    def cerceve_duyuldu(self, gozlem: Gozlem, gonderen: int, tur: str,
                        hedef: int | None, rssi_dbm: int, paket) -> None:
        """KK-01/1: komşu hâlâ orada · KK-05/6: geri iz · KK-04/8 (eğim):
        döngü bekçisinin bayat bilgi işareti ve paketi getiren komşu. RSSI
        okunmaz (KK-03/11)."""
        t = float(gozlem.saat_s)
        self.bag.cerceve_duyuldu(gonderen, t)
        if (tur == "veri" and hedef == self.kimlik and paket is not None
                and paket.hedef == self.gecit
                and paket.kaynak != self.kimlik):
            self.iz.ogren(paket.kaynak, gonderen, paket.kaynak_sira, t)
            if self.b.egim:
                self.rota.veri_duyuldu(gonderen, paket, t)
        return None

    # ==================================================================
    # Veri kararı — KK-04 ardıl · KK-05 geri iz ve bekletme
    # ==================================================================
    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        t = float(gozlem.saat_s)
        p = gozlem.paket
        # KK-04/9 (eğim): döngüden dönen paket, seçimden önce denetlenir.
        if self.b.egim and p is not None and p.hedef == self.gecit:
            self.rota.dongu_denetle(p, t)
        hepsi = self._bitir(t)
        beyan = tuple(x for x in hepsi if isinstance(x, Beyan))
        niyet = tuple(x for x in hepsi if not isinstance(x, Beyan))
        if p is None:
            return Karar(beyan=beyan, niyetler=niyet)
        telemetri = p.hedef == self.gecit
        if telemetri:
            sonraki, biliniyor = self.rota.ardil, self._rota_vardi
        else:
            sonraki = self.iz.sonraki(p.hedef, t, self.bag.kullanilir_mi)
            biliniyor = self.iz.biliniyor(p.hedef)
        tur = "veri" if telemetri else "komut"
        karar = self.bekletme.karar((p.kaynak, p.kaynak_sira), t,
                                    sonraki is not None)
        if karar == GONDER:
            self._sayac[tur + "_gonderilen"] += 1
            if self.b.egim and telemetri:
                self.rota.gonderildi(p, sonraki, t)      # KK-04/9
            return Karar(sonraki=sonraki, beyan=beyan, niyetler=niyet)
        if karar == BEKLET:
            self._sayac[tur + "_bekletilen"] += 1
            u = self._tampon_uyandir(t, self.d.YENIDEN_SOR_S)
            if u is not None:
                niyet += (u,)
            return Karar(beklet=True, beyan=beyan, niyetler=niyet)
        self._sayac[tur + "_dusen"] += 1
        if biliniyor:
            beyan += (Beyan("rota_gecersiz", komsu=p.hedef),)
        return Karar(beyan=beyan, niyetler=niyet)

    # ==================================================================
    # Koşum beacon'ı kullanılmaz · kimlik · teşhis
    # ==================================================================
    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem: Gozlem, komsu: int, yuk) -> None:
        return None

    def kimlik_parametreleri(self) -> dict:
        """Davranışı değiştiren kurucu değerleri — koşu kimliğine girer
        (K-171)."""
        return {"gecit": self.gecit, "bayraklar": self.b, "degerler": self.d}

    def teshis(self, dugum: int) -> dict:
        """🔴 Yalnız sonuç satırına; karara GİRMEZ (en çok 32 alan)."""
        cikti: dict = {
            "bayraklar_adlari": Bayraklar.adlar(),
            "bayraklar": self.b.degerler(),
            "komsu": len(self.bag.baglar),
            "olagan": len(self.bag.kullanilir_kume()),
            "ardil_var": self.rota.ardil is not None,
            "tur": self.rota.ilan()[0],
            "maliyet": self.rota.C,
        }
        for ad, sayac in (("protokol", self._sayac), ("bag", self.bag.sayac),
                          ("rota", self.rota.sayac),
                          ("selam", self.selam.sayac),
                          ("kendi", self.kendi.sayac),
                          ("bekletme", self.bekletme.sayac),
                          ("iz", self.iz.sayac)):
            cikti[f"{ad}_adlari"] = tuple(sayac)
            cikti[f"{ad}_sayac"] = tuple(sayac.values())
        return cikti
