"""
Kat 3 — Kanal erişimi (CSMA/CA).

🔴 BU KAT PAZARLIK DIŞI.
Li replikasyonundaki 1/7 sayısı ancak taşıyıcı dinleme, iletim menzilinden
GENİŞ girişim menzili ve gizli terminal modellenirse çıkar.

ÜÇ MODELLEME KARARI
===================

1) TAŞIYICI DİNLEME EŞİĞİ = GÜRÜLTÜ TABANI
   Böylece taşıyıcı dinleme menzili tam olarak girişim menziline eşit olur
   (603 m). Ayrı bir eşik yazılsaydı üçüncü bir "doğru" kaynağı doğardı.

2) 🔴 KARIŞTIRICI TAŞIYICI DİNLEMEYİ TETİKLEMEZ — yalnızca gürültüye girer
   Gerekçe sayısal: 802.11 enerji algılama eşiği ~-62 dBm. Karıştırıcımız
   (+2 dBm) 100 m mesafede bile yalnızca -98 dBm üretir, yani eşiğin 36 dB
   altında. Geniş bantlı gürültü ayrıca algılanabilir bir önbelge taşımaz.

   ⚠️ Bu karar karıştırmayı GERÇEĞE GÖRE HAFİFLETİR: gerçek bir sistemde
   yeterince güçlü bir karıştırıcı düğümleri kanalı meşgul sanmaya zorlar ve
   hiç konuşturmaz. Bizim modelimizde düğümler konuşur, paketleri düşer.
   Rapora yazılır.

3) ALIM, PAKET SÜRESİ BOYUNCA PARÇA PARÇA HESAPLANIR
   Girişim paket ortasında başlayıp bitebilir. Tek bir anlık SINR yerine,
   girişim kümesinin sabit kaldığı her aralık ayrı hesaplanır ve hata
   olasılıkları birleştirilir. Tek anlık SINR, kısmi çakışmaları ya
   olduğundan ağır ya olduğundan hafif gösterirdi.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .config import Konfig
from .events import OlayKuyrugu
from .packet import Paket
from .radio import Karistirici, Radyo
from .rng import kanal_cekimi
from .topology import Topoloji

YAYIN = -1          # alan = YAYIN -> yayin cercevesi, onay beklenmez


@dataclass
class Iletim:
    gonderen: int
    alan: int
    baslangic_s: float
    bitis_s: float
    tur: str                  # veri | onay | yayin
    paket: Paket | None = None
    sira: int = -1            # MAC sira numarasi (kopya tespiti icin)
    icerik: object = None     # yayin cercevesinin tasidigi veri
    # 🔴 B-70 (K-056): cercevenin GERCEK boyutu. Alici kredisi bundan
    # okunur; yoksa yuk tasiyan bir beacon aliciya EKSIK kredilenir.
    bayt: int = 0


@dataclass
class DugumMAC:
    """Bir düğümün MAC durum makinesi."""
    durum: str = "bos"        # bos | geri_cekilme | gonderiyor | onay_bekliyor
    cw: int = 31
    deneme: int = 0
    kalan_slot: int = 0
    sayac_basladi_s: float = -1.0
    jeton: int = 0            # iptal edilmis olaylari tanimak icin
    paket: Paket | None = None
    hedef: int = -1
    sira: int = -1            # bu cerceveye atanmis MAC sira numarasi
    bekleyen_yayin: object = None   # (bayt, icerik, yuk_bayt)
    # Alici bu paketi HERHANGI bir denemede kabul etti mi?
    # Yeniden deneme hakki bitince paketin dusup dusmeyecegini bu belirler.
    alici_kabul_etti: bool = False


class KanalErisimi:
    """Tüm düğümlerin MAC durumu + paylaşılan kanal."""

    def __init__(self, kon: Konfig, topo: Topoloji, radyo: Radyo,
                 olaylar: OlayKuyrugu, karistirici: Karistirici | None,
                 akislar) -> None:
        self.kon = kon
        self.topo = topo
        self.radyo = radyo
        self.olaylar = olaylar
        self.karistirici = karistirici
        self._rnd = akislar["mac_geri_cekilme"]

        n = topo.dugum_sayisi
        self.mac = [DugumMAC(cw=kon.cw_min) for _ in range(n)]
        self.aktif: list[Iletim] = []

        # Tasiyici dinleme komsulugu: alinan guc >= gurultu tabani.
        # Deterministik oldugu icin bir kez hesaplanir.
        self.cs_komsu: list[set[int]] = [set() for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and topo.girisim_menzilinde_mi(i, j):
                    self.cs_komsu[i].add(j)

        # 🔴 Kopya tespiti MAC SIRA NUMARASIYLA yapilir, rota katmaninin
        # paket kimligiyle DEGIL.
        #
        # Ilk yazimi paket kimligini kullaniyordu ve bir yonlendirme
        # DONGUSUNU kopya saniyordu: A->B->A->B'de ikinci A->B "zaten
        # gorulmus" diye atiliyordu ve TTL hic devreye girmiyordu.
        # 802.11'de sira numarasi her yeni gonderimde GONDEREN tarafindan
        # atanir; dongude geri gelen paket yeni numara alir, kopya sayilmaz.
        # Kopya YALNIZCA ayni cercevenin yeniden iletimidir.
        self.kopya_onbellegi: list[set[tuple[int, int]]] = [set() for _ in range(n)]
        self._sira_sayaci = [0] * n

        # Geri cagrilar - kosucu baglar
        # alim_gerceklesti : alici paketi KABUL ETTI -> defter burada guncellenir
        # gonderim_bitti   : gonderen serbest kaldi  -> defter DEGISMEZ
        # iletim_basarisiz : alici hic kabul etmedi  -> paket DUSER
        self.alim_gerceklesti = lambda paket, gonderen, alan: None
        # 🔴 B-02: hedef ve GONDERENIN GORDUGU sonuc tasiniyor.
        # Onceki surumde `son_iletim_hedefi` her zaman -1'di; protokol
        # "onay geldi"yi biliyor ama HANGI KOMSUYA ait oldugunu bilmiyordu.
        # 05 §B'nin bag kalitesi icin izin verdigi TEK kanal buydu.
        self.gonderim_bitti = lambda paket, gonderen, hedef, sonuc: None
        self.iletim_basarisiz = lambda paket, gonderen, hedef: None
        self.yayin_alindi = lambda gonderen, alan, icerik: None

        # Sayaclar
        self.gonderilen_veri = 0
        self.gonderilen_onay = 0
        # 🔴 B-20 — AIRTIME SAYAÇLARI.
        # Kontrol yükü BAYT cinsinden sayılıyor (`03` B3, doğru). Ama bu
        # düzenekte gerçek kıt kaynak KANAL ZAMANIDIR ve önbelge (192 µs)
        # her çerçeveye sabit ekleniyor: 14 baytlık bir ONAY 112 µs sürerken
        # önbelgesi 192 µs'dir. Ölçüldü (denetim B-20): kontrol payı bayt
        # cinsinden %2,84, AIRTIME cinsinden %5,11 — 1,8 kat.
        #
        # Aynı baytı farklı sayıda çerçeveye bölen iki protokol bayt
        # metriğinde EŞİT, airtime'da 2 kat farklı görünür. K-009'un "eşit
        # kontrol bütçesi" adalet şartı bayt üzerinden kurulmuştu; her iki
        # birim de raporlanmadan o şart doğrulanamaz.
        self.veri_airtime_s = 0.0
        self.kontrol_airtime_s = 0.0
        self.basarisiz_alim = 0
        self.kayip_onay = 0
        self.kopya_alim = 0
        self.kontrol_bayt = 0
        # 🔴 B-47: `kontrol_bayt`ın protokolün KENDİ koyduğu alanlardan
        # gelen kısmı. AYNI OLAYDA sayılır (fiilen iletilen beacon);
        # üretilip eskiyen beacon havaya çıkmaz, yükü de harcanmaz.
        self.yayin_yuk_bayt = 0
        self.veri_bayt = 0
        self.toplam_deneme = 0
        # 🔴 B-01: DUGUM BASINA sayaclar.
        # Onceki surumde `Gozlem` alanlari `self.veri_bayt` / `kontrol_bayt`
        # KURESEL sayaclarindan besleniyordu — yani protokol, agin tamaminin
        # bayt trafigini goruyordu. Gercek bir telsizin olcemeyecegi bir
        # buyukluk, dogrudan karara giriyordu (kural 5 ihlali).
        # Bagimsiz denetim bunu 7344 kararin 7343'unde olctu.
        self.dugum_gonderilen_bayt = [0] * n
        self.dugum_alinan_bayt = [0] * n

        self.gonderilen_yayin = 0
        self.alinan_yayin = 0
        self.kacirilan_yayin = 0      # MAC mesgulken uretilip eskiyen beacon
        # Her dugumun SON iletim araligi. Yari cift yonlu kontrolu bunun
        # uzerinden yapilir; anlik duruma bakmak YETMEZ (asagida).
        self.gonderim_araligi: list[tuple[float, float]] = [(-1.0, -1.0)] * n

        # Kanal izi — VARSAYILAN OLARAK KAPALI.
        # Ç2.3 icin: iki farkli protokol kolunun ayni tohumda AYNI kanal
        # gerceklemesini gordugunu tam kosuda dogrulamak. Acikken her cekim
        # (gonderen, alan, dilim) -> deger olarak kaydedilir.
        self.kanal_izi: dict[tuple[int, int, int], float] | None = None

        self._kurulum_bitti = True

    def __setattr__(self, ad: str, deger) -> None:
        """Kurulumdan sonra BILINMEYEN bir oznitelige atama yasak.

        🔴 Sebep gercek bir olay: geri cagri adlari degistiginde eski adla
        yapilan atama (`mac.iletim_tamamlandi = ...`) Python'da sessizce yeni
        bir oznitelik yaratir ve geri cagri HIC ATESLENMEZ. Belirtisi yoktur;
        paketler kaybolur ve testler "0 == 0" diye gecer.
        """
        if getattr(self, "_kurulum_bitti", False) and not hasattr(self, ad):
            raise AttributeError(
                f"KanalErisimi'nde '{ad}' diye bir alan yok. "
                f"Geri cagri adlari: alim_gerceklesti, gonderim_bitti, "
                f"iletim_basarisiz, yayin_alindi"
            )
        object.__setattr__(self, ad, deger)

    # ================================================================== gonder
    def gonder(self, dugum: int, paket: Paket, hedef: int) -> None:
        """Yönlendirme katmanı bir paketi bir komşuya vermek istiyor."""
        m = self.mac[dugum]
        if m.durum != "bos":
            raise RuntimeError(f"düğüm {dugum} meşgulken gönderim istendi")
        m.paket, m.hedef = paket, hedef
        m.cw, m.deneme = self.kon.cw_min, 0
        m.alici_kabul_etti = False
        m.sira = self._sira_sayaci[dugum]      # cerceve basina bir kez
        self._sira_sayaci[dugum] += 1
        self._geri_cekilme_basla(dugum)

    def bos_mu(self, dugum: int) -> bool:
        return self.mac[dugum].durum == "bos"

    # ------------------------------------------------------------------ yayin
    def yayin_gonder(self, dugum: int, bayt: int, icerik: object,
                     yuk_bayt: int = 0) -> None:
        """Beacon yayini: ONAY YOK, YENIDEN DENEME YOK.

        802.11'de yayin cerceveleri onaylanmaz. Bunun sonucu gercektir ve
        olcume girer: karistirma altinda beacon KAYBOLUR, komsu GORUNMEZ olur.
        Komsulugun bedava olmamasinin sebebi budur.

        MAC mesgulse beacon BEKLETILIR. Bir sonraki beacon gelmeden
        gonderilemezse eskisi DUSER ve `kacirilan_yayin` sayilir — kontrol
        duzlemi butcesinin gercekten harcanip harcanmadigi boylece gorunur.
        """
        m = self.mac[dugum]
        if m.durum != "bos":
            if m.bekleyen_yayin is not None:
                self.kacirilan_yayin += 1
            m.bekleyen_yayin = (bayt, icerik, yuk_bayt)
            return
        self._yayin_ilet(dugum, bayt, icerik, yuk_bayt)

    def _yayin_ilet(self, dugum: int, bayt: int, icerik: object,
                    yuk_bayt: int = 0) -> None:
        m = self.mac[dugum]
        m.durum = "yayin_geri_cekilme"
        m.bekleyen_yayin = (bayt, icerik, yuk_bayt)
        m.kalan_slot = self._rnd.randint(0, self.kon.cw_min)
        m.jeton += 1
        self.olaylar.gecikmeyle_ekle(
            self.kon.difs_s + m.kalan_slot * self.kon.slot_s,
            self._yayin_geri_cekilme_bitti, dugum, m.jeton)

    def _yayin_geri_cekilme_bitti(self, dugum: int, jeton: int) -> None:
        m = self.mac[dugum]
        if jeton != m.jeton or m.durum != "yayin_geri_cekilme":
            return
        if self.kanal_mesgul(dugum) or self.radyo_mesgul(dugum):
            m.jeton += 1
            self.olaylar.gecikmeyle_ekle(
                self.kon.difs_s + self.kon.slot_s,
                self._yayin_geri_cekilme_bitti, dugum, m.jeton)
            return

        bayt, icerik, yuk_bayt = m.bekleyen_yayin
        m.bekleyen_yayin = None
        m.durum = "gonderiyor"
        sure = self.kon.cerceve_suresi_s(bayt)
        # 🔴 B-70: gercek boyut Iletim'e yaziliyor (asagida alici okuyor)
        il = Iletim(dugum, YAYIN, self.olaylar.simdi,
                    self.olaylar.simdi + sure, "yayin", None, -1, icerik,
                    bayt)
        self.gonderilen_yayin += 1
        self.kontrol_bayt += bayt
        self.yayin_yuk_bayt += yuk_bayt          # B-47, AYNI OLAYDA
        self.kontrol_airtime_s += sure                   # B-20
        self.dugum_gonderilen_bayt[dugum] += bayt
        self.gonderim_araligi[dugum] = (il.baslangic_s, il.bitis_s)
        self._iletim_basla(il)
        self.olaylar.gecikmeyle_ekle(sure, self._yayin_bitti, dugum, il)

    def _yayin_bitti(self, dugum: int, il: Iletim) -> None:
        # Her alici icin AYRI degerlendirilir: biri duyar, digeri duymaz.
        alicilar = [j for j in range(self.topo.dugum_sayisi)
                    if self.topo.iletim_menzilinde_mi(dugum, j)]
        basarililar = [j for j in alicilar if self._alim_basarili_mi(il, alici=j)]
        self._iletim_bitir(il)
        self.mac[dugum].durum = "bos"
        for j in basarililar:
            self.alinan_yayin += 1
            # 🔴 B-70 (K-056) — ALICI GERCEK CERCEVE BOYUTUNU alir.
            # Onceki sürüm sabit `kon.beacon_bayt` kredilendiriyordu:
            # 57 baytlik (32+25) bir beacon icin alici 32 bayt goruyordu.
            # Bir kosuda 1 668 050 bayt (66 722 alim x 25) kredilenmedi.
            # Veri ve onay yollarinda boyle bir asimetri YOK — bu, B-47
            # kanalinin getirdigi tutarsizlikti.
            #
            # `alinan_bayt` bir GOZLEM PENCERESI alanidir; yuk tasiyan
            # bir kolun komsulari aldiklari bayti olduğundan AZ gorurdu.
            self.dugum_alinan_bayt[j] += il.bayt or self.kon.beacon_bayt
            self.yayin_alindi(dugum, j, il.icerik)
        self._bekleyeni_kostur(dugum)

    def _bekleyeni_kostur(self, dugum: int) -> None:
        m = self.mac[dugum]
        if m.durum == "bos" and m.bekleyen_yayin is not None:
            bayt, icerik, yuk_bayt = m.bekleyen_yayin
            m.bekleyen_yayin = None
            self._yayin_ilet(dugum, bayt, icerik, yuk_bayt)

    # ---------------------------------------------------------- geri cekilme
    def _geri_cekilme_basla(self, dugum: int) -> None:
        m = self.mac[dugum]
        m.durum = "geri_cekilme"
        m.kalan_slot = self._rnd.randint(0, m.cw)
        self.toplam_deneme += 1
        self._geri_cekilme_planla(dugum)

    def _geri_cekilme_planla(self, dugum: int) -> None:
        m = self.mac[dugum]
        if self.kanal_mesgul(dugum):
            m.sayac_basladi_s = -1.0        # donduruldu
            return
        m.sayac_basladi_s = self.olaylar.simdi
        m.jeton += 1
        gecikme = self.kon.difs_s + m.kalan_slot * self.kon.slot_s
        self.olaylar.gecikmeyle_ekle(gecikme, self._geri_cekilme_bitti,
                                     dugum, m.jeton)

    def _geri_cekilme_bitti(self, dugum: int, jeton: int) -> None:
        m = self.mac[dugum]
        if jeton != m.jeton or m.durum != "geri_cekilme":
            return                          # iptal edilmis olay
        if self.kanal_mesgul(dugum) or self.radyo_mesgul(dugum):
            self._geri_cekilme_planla(dugum)
            return
        self._ilet(dugum)

    def radyo_mesgul(self, dugum: int) -> bool:
        """Dugumun KENDI vericisi hala yayinda mi?

        🔴 Bu kontrol 18 Agustos 2026'da eklendi ve gercek bir hatayi
        kapatiyor: onay gercek iletim yapildiginda bir dugum, kendi onayi
        havadayken kendi verisini gondermeye baslayabiliyordu.

        Sira: veri alimi biter -> +SIFS'te ONAY gider -> +DIFS'te geri
        cekilme devam eder. SIFS (10 us) < DIFS (50 us) oldugu icin onay
        once baslar; ama geri cekilme sifir slot cekmisse dugum +50 us'de
        veri gondermeye kalkiyordu ve KENDI ONAYINI EZIYORDU.

        `kanal_mesgul` bunu goremez cunku dugumun kendi iletimlerini bilerek
        dislar (kendi verisine karsi taşiyici dinleme yapilmaz). Bu ayri bir
        kontrol olmak zorunda: tasiyici dinleme BASKASINI duymakla ilgili,
        bu ise YARI CIFT YONLU radyonun fiziksel siniriyla.

        Belirtisi: 2+ atlamali zincirde ~%30 onay kaybi. Ç4.4 on-kayitli
        bandin disina cikilmasi bu hatayi ortaya cikardi.
        """
        return self.gonderim_araligi[dugum][1] > self.olaylar.simdi

    def _kanal_mesgullesti(self, dugum: int) -> None:
        """Geri sayımı dondur — 802.11 davranışı."""
        m = self.mac[dugum]
        if m.durum != "geri_cekilme" or m.sayac_basladi_s < 0:
            return
        gecen = self.olaylar.simdi - m.sayac_basladi_s - self.kon.difs_s
        if gecen > 0:
            m.kalan_slot = max(0, m.kalan_slot - int(gecen / self.kon.slot_s))
        m.sayac_basladi_s = -1.0
        m.jeton += 1                        # planlanmis olayi gecersiz kil

    def _kanal_bosaldi(self, dugum: int) -> None:
        m = self.mac[dugum]
        if m.durum == "geri_cekilme" and m.sayac_basladi_s < 0:
            self._geri_cekilme_planla(dugum)

    # ------------------------------------------------------------------ iletim
    def _ilet(self, dugum: int) -> None:
        m = self.mac[dugum]
        m.durum = "gonderiyor"
        m.jeton += 1
        sure = self.kon.cerceve_suresi_s(m.paket.bayt)
        il = Iletim(dugum, m.hedef, self.olaylar.simdi,
                    self.olaylar.simdi + sure, "veri", m.paket, m.sira)
        self.gonderilen_veri += 1
        self.veri_bayt += m.paket.bayt
        self.veri_airtime_s += sure                      # B-20
        self.dugum_gonderilen_bayt[dugum] += m.paket.bayt
        self.gonderim_araligi[dugum] = (il.baslangic_s, il.bitis_s)
        self._iletim_basla(il)
        self.olaylar.gecikmeyle_ekle(sure, self._veri_bitti, dugum, il, m.jeton)

    def _iletim_basla(self, il: Iletim) -> None:
        self.aktif.append(il)
        # 🔴 Mesgul bildirimi CCA GECIKMESI KADAR ERTELENIR.
        # Aninda bildirilseydi, geri sayimi ayni slotta biten iki dugumden
        # ikincisi digerini sifir gecikmeyle gorur ve susardi -> ayni-slot
        # carpismasi hic olmazdi. Oysa 802.11 in temel cakisma kaynagi budur.
        self.olaylar.gecikmeyle_ekle(self.kon.cca_s, self._mesgul_bildir, il)

    def _mesgul_bildir(self, il: Iletim) -> None:
        if not any(x is il for x in self.aktif):
            return
        for d in self.cs_komsu[il.gonderen]:
            self._kanal_mesgullesti(d)

    def _iletim_bitir(self, il: Iletim) -> None:
        # Kimlik uzerinden cikar: dataclass __eq__ DEGER karsilastirir ve
        # ayni alanlara sahip iki cerceve birbiriyle karistirilabilirdi.
        for i, x in enumerate(self.aktif):
            if x is il:
                del self.aktif[i]
                break
        for d in self.cs_komsu[il.gonderen]:
            if not self.kanal_mesgul(d):
                self._kanal_bosaldi(d)

    def _veri_bitti(self, dugum: int, il: Iletim, jeton: int) -> None:
        # Alim basarisi, iletim AKTIF LISTEDEN CIKARILMADAN hesaplanir:
        # yoksa kendi iletimi girisim listesinde bulunamaz ve cakisan
        # cerceveler yanlislikla basarili sayilir.
        basarili = self._alim_basarili_mi(il)
        self._iletim_bitir(il)

        m = self.mac[dugum]
        m.durum = "onay_bekliyor"
        alici = il.alan

        if basarili:
            # PAKET BURADA EL DEGISTIRIR - onayin gelisinde DEGIL.
            # Onay kaybolsa bile alici paketi almistir; defter bunu
            # yansitmak zorunda, yoksa paket hem alicida olur hem gonderende
            # dusmus sayilir ve korunum kirilir.
            self.dugum_alinan_bayt[alici] += il.paket.bayt
            anahtar = (il.gonderen, il.sira)
            if anahtar in self.kopya_onbellegi[alici]:
                self.kopya_alim += 1        # kopya: veri atilir, onay YINE gider
            else:
                self.kopya_onbellegi[alici].add(anahtar)
                m.alici_kabul_etti = True
                self.alim_gerceklesti(il.paket, il.gonderen, alici)
            # Alici SIFS sonra onay gonderir.
            # Tasiyici dinleme YOK: SIFS onceligi 802.11 in tanimidir.
            self.olaylar.gecikmeyle_ekle(self.kon.sifs_s, self._onay_ilet,
                                         alici, il.gonderen)
        else:
            self.basarisiz_alim += 1

        # Zaman asimi her halukarda kurulur; onay gelirse jeton bayatlar.
        self.olaylar.gecikmeyle_ekle(
            self.kon.sifs_s + self.kon.onay_suresi_s + self.kon.slot_s,
            self._onay_zaman_asimi, dugum, m.jeton)

    # ------------------------------------------------------------ onay iletimi
    def _onay_ilet(self, alici: int, veri_gonderen: int) -> None:
        """Onay GERCEK bir iletimdir: kanali mesgul eder, girisim yapar,
        kaybolabilir. (Modelleme karari 4)"""
        sure = self.kon.onay_suresi_s
        onay = Iletim(alici, veri_gonderen, self.olaylar.simdi,
                      self.olaylar.simdi + sure, "onay")
        self.gonderilen_onay += 1
        self.kontrol_bayt += self.kon.onay_bayt
        self.kontrol_airtime_s += sure                   # B-20
        self.dugum_gonderilen_bayt[alici] += self.kon.onay_bayt
        self.gonderim_araligi[alici] = (onay.baslangic_s, onay.bitis_s)
        self._iletim_basla(onay)
        self.olaylar.gecikmeyle_ekle(sure, self._onay_bitti, onay)

    def _onay_bitti(self, onay: Iletim) -> None:
        ulasti = self._alim_basarili_mi(onay)
        self._iletim_bitir(onay)
        if ulasti:
            self.dugum_alinan_bayt[onay.alan] += self.kon.onay_bayt
            self._onay_geldi(onay.alan)
        else:
            self.kayip_onay += 1

    def _onay_geldi(self, dugum: int) -> None:
        m = self.mac[dugum]
        if m.durum != "onay_bekliyor":
            return
        m.jeton += 1                        # zaman asimini gecersiz kil
        paket, hedef = m.paket, m.hedef
        m.durum, m.paket, m.hedef = "bos", None, -1
        self.gonderim_bitti(paket, dugum, hedef, "onay")
        self._bekleyeni_kostur(dugum)

    def _onay_zaman_asimi(self, dugum: int, jeton: int) -> None:
        m = self.mac[dugum]
        if jeton != m.jeton or m.durum != "onay_bekliyor":
            return                          # onay gelmis, olay bayat
        m.deneme += 1
        if m.deneme > self.kon.yeniden_deneme_siniri:
            paket, kabul, hedef = m.paket, m.alici_kabul_etti, m.hedef
            m.durum, m.paket, m.hedef = "bos", None, -1
            m.jeton += 1
            if kabul:
                # Paket ALICIDA. Dusurmek onu ikiye cikarirdi.
                # ⚠️ Ama GONDERENIN GORDUGU sey ZAMAN ASIMIDIR: onay hic
                # gelmedi. Alicinin kabul ettigi bilgisi simulatoruna aittir,
                # gonderene degil. Buraya "onay" yazmak KAHINLIK olurdu.
                self.gonderim_bitti(paket, dugum, hedef, "zaman_asimi")
            else:
                self.iletim_basarisiz(paket, dugum, hedef)
            return
        m.cw = min(self.kon.cw_max, 2 * m.cw + 1)   # ikili ustel geri cekilme
        self._geri_cekilme_basla(dugum)

    # =============================================================== alim
    def kanal_mesgul(self, dugum: int) -> bool:
        """Taşıyıcı dinleme. ⚠️ Karıştırıcı BURAYA GİRMEZ (karar 2)."""
        simdi = self.olaylar.simdi
        for il in self.aktif:
            if il.gonderen == dugum or il.gonderen not in self.cs_komsu[dugum]:
                continue
            # CCA gecikmesi dolmadan bir iletim ALGILANAMAZ.
            if il.baslangic_s + self.kon.cca_s <= simdi:
                return True
        return False

    def olculen_gurultu_w(self, dugum: int) -> float:
        """Dugumun KENDI antenindeki toplam gurultu + girisim gucu.

        Gozlem penceresinin izin verdigi bir olcumdur: her telsiz gurultu
        tabanini olcer. Karistiricinin KONUMU degil, yalnizca onun burada
        yarattigi GUC gorunur.
        """
        toplam = self.radyo.gurultu_gucu_w
        simdi = self.olaylar.simdi
        for il in self.aktif:
            if il.gonderen == dugum:
                continue
            if il.baslangic_s <= simdi < il.bitis_s:
                toplam += self.radyo.alinan_guc_w(
                    self.topo.mesafe(il.gonderen, dugum))
        if self.karistirici is not None:
            toplam += self.karistirici.alinan_guc_w(
                self.topo.konumlar[dugum], simdi)
        return toplam

    def _girisim_w(self, alici: int, il: Iletim, an_s: float) -> float:
        toplam = 0.0
        for baska in self.aktif:
            # 🔴 B-72 (K-056) — `baska.gonderen == alici` DALI
            # TETIKLENEMEZ: 246 378 cagrinin 0'inda. `alim_per` zaten
            # yari cift yonlu ortusmeyi kontrol edip None donuyor,
            # dolayisiyla alici cerceve suresince gonderemez.
            #
            # Deponun kendi kurali (`config.py`, `mac.py`):
            # *"Tetiklenemeyen bir kontrol, koruma saglamadan koruma
            # izlenimi verir."* Ayni gerekcyeyle iki kontrol zaten
            # assert'e cevrilmisti; bu ucuncusu.
            #
            # 🔴 ASIL RISK: yari cift yonlu kontrolu bir gun kalkarsa bu
            # dal SESSIZCE dogru cevabi vermeye baslar ve hatayi MASKELER.
            assert not (baska is not il and baska.gonderen == alici
                        and baska.baslangic_s <= an_s < baska.bitis_s), (
                f"alici {alici} kendi iletimini yaparken alim degerlendiriliyor "
                f"— yari cift yonlu kontrolu (alim_per) devre disi kalmis olmali")
            if baska is il:
                continue
            if baska.baslangic_s <= an_s < baska.bitis_s:
                toplam += self.radyo.alinan_guc_w(
                    self.topo.mesafe(baska.gonderen, alici))
        if self.karistirici is not None:
            toplam += self.karistirici.alinan_guc_w(
                self.topo.konumlar[alici], an_s)
        return toplam

    def _parca_sinirlari(self, il: Iletim) -> list[float]:
        sinirlar = {il.baslangic_s, il.bitis_s}
        for baska in self.aktif:
            for t in (baska.baslangic_s, baska.bitis_s):
                if il.baslangic_s < t < il.bitis_s:
                    sinirlar.add(t)
        kj = self.karistirici
        if kj is not None and kj.darbeli:
            p = kj.periyot_s
            k = math.floor(il.baslangic_s / p) - 1
            while k * p <= il.bitis_s:
                for kesir in (0.0, kj.gorev_cevrimi):
                    t = (k + kesir - kj.faz_kesri) * p
                    if il.baslangic_s < t < il.bitis_s:
                        sinirlar.add(t)
                k += 1
        return sorted(sinirlar)

    # ======================================================================
    # 🔴 TEŞHİS — KÂHİN. Karara GİREMEZ, yalnızca rapora girer.
    # `05-GOZLEM-PENCERESI.md` §D: "Aynı büyüklük iki farklı yerden okunuyor:
    # GERÇEK değer → yalnızca teşhis ve rapor · protokolün TAHMİNİ → yalnızca
    # karar. Bu iki kanalın karışması, tüm sonuçları geçersiz kılar."
    # ======================================================================
    def bag_gercek_per(self, gonderen: int, alici: int, an_s: float) -> float:
        """Bir bağın O ANKİ gerçek paket hata olasılığı — çekişmesiz.

        🔴 BU BİR KÂHİN BÜYÜKLÜKTÜR. Gözlem penceresine ASLA girmez;
        yalnızca `Kosu.sonuc()` teşhis sayaçlarını besler.

        ÇEKİŞME DAHİL DEĞİL — bilerek. Girişim yalnızca karıştırıcıdan
        alınır, eşzamanlı iletimlerden değil. Sebep: sorulan soru "bu bağın
        KALİTESİ nedir", "şu an kanal ne kadar kalabalık" değil. Aynı tanım
        `dogrulama/kurulum_kalibrasyonu.py`de bağ kullanılabilirliği için
        kullanılıyor; iki yerde iki tanım olsaydı ikinci bir "doğru" kaynağı
        doğardı (B-07'nin hata sınıfı).
        """
        if gonderen == alici or alici < 0:
            return 1.0
        sinyal = self.radyo.alinan_guc_w(self.topo.mesafe(gonderen, alici))
        girisim = 0.0
        if self.karistirici is not None:
            girisim = self.karistirici.alinan_guc_w(
                self.topo.konumlar[alici], an_s)
        return self.radyo.paket_hata_olasiligi(
            self.radyo.sinr_lin(sinyal, girisim), self.kon.paket_bayt)

    def alim_per(self, il: Iletim, alici: int | None = None) -> float | None:
        """Bu cerceve icin paket hata olasiligi. Yari cift yonlu carpisma
        varsa None doner (olasilik degil, kesin basarisizlik).

        AYRI METOT OLMASININ SEBEBI: `_alim_basarili_mi` yalnizca bool
        dondurur ve PER'i test edilemez kilar. Ç3.2 (parca parca hesabin
        sabit girisimde tek parca hesapla ayni sonucu vermesi) bu metoda
        dayanir.
        """
        if alici is None:
            alici = il.alan
        if alici < 0:
            return None
        g_bas, g_bit = self.gonderim_araligi[alici]
        if g_bas < il.bitis_s and il.baslangic_s < g_bit:
            return None

        sinyal = self.radyo.alinan_guc_w(self.topo.mesafe(il.gonderen, alici))
        noktalar = self._parca_sinirlari(il)
        log_basari = 0.0
        for a, b in zip(noktalar, noktalar[1:]):
            gir = self._girisim_w(alici, il, 0.5 * (a + b))
            ber = self.radyo.bit_hata_orani(self.radyo.sinr_lin(sinyal, gir))
            # 🔴 B-116 (ALTINCI DENETİM) — TETİKLENEMEYEN KONTROL, `assert`E
            # ÇEVRİLDİ. Burada `if ber >= 0.5: return 1.0` vardı ve o dal
            # ASLA çalışmıyordu: `bit_hata_orani` 0,5'i yalnızca
            # `sinr_lineer <= 0` iken döndürür, alınan güç ise sonlu
            # mesafede DAİMA pozitiftir (`pt / db_to_lin(yol_kaybı)`).
            #
            # Ölçüldü (27 Ağu, 3 senaryo, bağımsız olarak):
            #     540 021 çağrı · ber == 0,5: 0 · ber > 0,5: 0
            #
            # Deponun kendi kuralı: *"tetiklenemeyen bir kontrol, koruma
            # sağlamadan koruma İZLENİMİ verir."* Üç kez uygulandı
            # (B-13 · B-72 · B-98); bu dördüncüsü.
            #
            # ⚠️ `python -O` altında kalkar (`08` madde 29) — ama kalktığında
            # sessiz bir yanlış cevap ÜRETMEZ: `log1p(-ber)` 0,5 için de
            # tanımlıdır. Kaybolan tek şey, varsayımın sesli olması.
            assert ber < 0.5, (
                f"BER doyma varsayımı KIRILDI: ber={ber!r} ≥ 0,5. "
                f"`alim_per` bu durumu artık ele almıyor (B-116); SINR "
                f"modeli değiştiyse dal geri konmalı.")
            log_basari += (b - a) * self.kon.bit_hizi_bps * math.log1p(-ber)
        return -math.expm1(log_basari)

    def _alim_basarili_mi(self, il: Iletim, alici: int | None = None) -> bool:
        if alici is None:
            alici = il.alan
        if alici < 0:
            return False

        # 🔴 YARI CIFT YONLU — ARALIK ORTUSMESIYLE kontrol edilir.
        #
        # Ilk yazimi "alici SU AN gonderiyor mu" diye soruyordu ve YANLISTI:
        # iki cerceve ayni anda bitince, once islenen kendi durumunu
        # "onay_bekliyor" yapiyor, sonra islenen ise aliciyi bos goruyor ve
        # cakisma sessizce kayboluyordu. Bir test bunu yakaladi.
        #
        # Dogrusu: alici, bu cercevenin SURESI BOYUNCA herhangi bir an
        # gonderiyorduysa duyamaz.
        g_bas, g_bit = self.gonderim_araligi[alici]
        if g_bas < il.bitis_s and il.baslangic_s < g_bit:
            return False

        per = self.alim_per(il, alici)
        # 🔴 OLU DAL -> DEGISMEZ (19 Agustos 2026, sag kalan ayiklamasi).
        # `alim_per` yalnizca iki durumda None doner: alici < 0, ve yari cift
        # yonlu ortusme. IKISI DE YUKARIDA zaten kontrol edildi; buraya
        # gelindiginde None IMKANSIZDIR. Olculdu: 4 554 068 cagrida 0 None.
        #
        # Onceki hali `if per is None: return False` idi -- yani tetiklenemeyen
        # bir kontrol. `config.py`nin kendi kurali: "Tetiklenemeyen bir
        # kontrol, koruma saglamadan koruma izlenimi verir." (B-13 sinifi)
        #
        # Assert olarak DURUYOR cunku yukaridaki iki kontrolden biri silinirse
        # bu satir sessizce yanlis cevap vermek yerine PATLAR.
        assert per is not None, (
            "alim_per None dondu: yukaridaki alici<0 / yari cift yonlu "
            "kontrollerinden biri kaldirilmis olmali"
        )
        cekim = kanal_cekimi(self.kon.tohum, il.gonderen, alici,
                             il.baslangic_s, self.kon.kanal_dilimi_s)
        if self.kanal_izi is not None:
            dilim = int(il.baslangic_s // self.kon.kanal_dilimi_s)
            self.kanal_izi[(il.gonderen, alici, dilim)] = cekim
        return cekim >= per
