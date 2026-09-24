"""
Düğüm — bir İHA'nın koşu sırasındaki bütün davranışı.

🔴 KORUNUM DEFTERİ TEK GEÇİŞ NOKTASIDIR
=======================================
Bu dosyadaki her paket hareketi deftere yazılır. Bir geçişi atlamak, korunum
denklemini VEYA mutabakatı kırar — ve ikisi de her koşuda otomatik denetlenir.
Denklem defterin kendi tutarlılığını, mutabakat defterin gerçeği doğru
modelleyip modellemediğini ölçer; ikisi ayrı kapıdır.

🔒 GERİ ÇEKİLME OLAY GÜDÜMLÜ, SLOT GÜDÜMLÜ DEĞİL
================================================
Slot slot olay üretmek 350 s × 20 µs = **17,5 milyon olay/düğüm** ederdi.
Onun yerine sayaç yalnız kanalın boş kaldığı aralıklarda, bir kerede azalır:

    kanal meşgul oldu  → geçen boş slotları düş, bekleyen bitişi geçersizle
    kanal boşaldı      → DIFS sonra yeniden başlat, yeni bitiş zamanla

Sonuç slot slot işlemekle **birebir aynıdır** ve `Dcf.slot_gecti(adet)`in
testi bunu bağlar.

🔴 OLAY İPTALİ YOK — SÜRÜM SAYACI VAR
=====================================
`OlayKuyrugu` (taşınan, denetlenmiş modül) iptal desteklemiyor ve onu
değiştirmek denetlenmiş bir sözleşmeyi bozmak olurdu. Onun yerine her
zamanlanmış geri çekilme bitişi bir SÜRÜM taşır; ateşlendiğinde düğümün
güncel sürümüyle karşılaştırılır ve eskiyse sessizce yok sayılır. Bayat bir
olayın karar vermesi böylece imkânsız.
"""

from __future__ import annotations

import math

from collections import deque

from sim2.ag.paket import Paket
from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.saat import YerelZaman
from sim2.gozlem.karar import Karar
from sim2.gozlem.pencere import Gozlem, KomsuKaydi, PaketGorunumu
from sim2.gozlem.teshis import teshis_dogrula
from sim2.gozlem.yuk import yuk_bayt, yuku_dondur
from sim2.kanal.girisim import Iletim
from sim2.kosum.kontrol_durum import KontrolDurumu
from sim2.kosum.kurulum import Kurulum
from sim2.mac.alici import AliciZinciri
from sim2.mac.dcf import Dcf

__all__ = ["Dugum"]


class Dugum:
    """Kuyruk · DCF · alıcı zinciri · komşu tablosu · protokol kancaları."""

    __slots__ = ("kimlik", "kur", "protokol", "kuyruk", "dcf", "alici",
                 "_komsular", "_gonderilen_bayt", "_alinan_bayt",
                 "_son_sonuc", "_son_hedef", "_surum", "_bekleme_bas_s",
                 "_bitis_ani_s",
                 "_ucustaki", "_ucus_hedefi", "_ucus_no", "_onay_bekleniyor",
                 "_devredildi", "_son_ucus", "kontrol",
                 "bekleyenler", "_tampon_son_tarih", "sonuc_kancasi")

    def __init__(self, kimlik: int, kur: Kurulum, protokol) -> None:
        self.kimlik = kimlik
        self.kur = kur
        self.protokol = protokol
        self.kuyruk = kur.kuyruklar[kimlik]
        self.dcf = Dcf(kimlik, kur.konfig, kur.akislar)
        self.alici = AliciZinciri(kimlik, kur.konfig, kur.kanal)
        self._komsular: dict[int, KomsuKaydi] = {}
        self._gonderilen_bayt = 0
        self._alinan_bayt = 0
        self._son_sonuc: str | None = None
        self._son_hedef: int | None = None
        self._surum = 0
        self._bekleme_bas_s: float | None = None
        # Planlanan geri çekilme bitişi. 🔴 "TAAHHÜT" anını işaretler:
        # `taahhutlu_mu()`ye bak.
        self._bitis_ani_s: float | None = None
        # 🔴 "Uçuşta" olan paket: kuyruktan ALINMIŞ ama henüz teslim
        # edilmemiş/düşmemiş. Korunum defterindeki `ucusta` terimi budur.
        self._ucustaki: Paket | None = None
        self._ucus_hedefi: int | None = None
        # 🔒 UÇUŞ NUMARASI — düğüm başına monoton artan, her ATLAMA için yeni.
        # Yeniden denemeler aynı numarayı taşır; bir döngüde aynı paketin
        # aynı komşuya ikinci kez gelmesi YENİ bir numara taşır. Tekrar
        # bastırma bunun üzerine kurulduğu için alıcının komşu başına tek bir
        # sayı hatırlaması yeter — paket kimliği kümesi tutmak koşu boyunca
        # milyonlarca giriş biriktirirdi.
        self._ucus_no = 0
        self._onay_bekleniyor = False
        # 🔴 VERİ ALINDI AMA ONAY KAYBOLDU — gerçek 802.11'in temel ikilemi.
        # Alıcı paketi ALMIŞTIR; gönderen bunu bilmez ve yeniden gönderir.
        # `_devredildi`, paketin defterde ARTIK UÇUŞTA OLMADIĞINI söyler:
        # gönderen sonunda vazgeçse bile onu DÜŞÜREMEZ, çünkü paket kaybolmadı,
        # el değiştirdi. Bu ayrım olmasaydı korunum denklemi çift sayardı.
        self._devredildi = False
        # Komşu başına EN SON görülen uçuş numarası. Aynı numara ikinci kez
        # gelirse yeniden denemedir ve bastırılır; daha büyük bir numara yeni
        # bir atlamadır ve döngüde meşru bir yeniden ziyaret olabilir —
        # bastırılsaydı paket sessizce yutulur ve defter ayrışırdı.
        self._son_ucus: dict[int, int] = {}
        # 🔒 KONTROL DÜZLEMİ (K-112). Protokol kontrol kancalarını taşımıyorsa
        # `etkin=False` ve bu nesne koşu boyunca HİÇBİR şey yapmaz.
        self.kontrol = KontrolDurumu(protokol, kur.konfig.kuyruk_kapasitesi,
                                     kur.sayaclar)
        # 🔒 Y1 · K-151 — her unicast sonucunu isteyen protokol. Kurulumda
        # BİR KEZ okunur: taşımayan protokolde iletim başına maliyet yok.
        self.sonuc_kancasi = callable(getattr(protokol, "iletim_sonucu", None))
        # 🔒 ROTA BEKLEME TAMPONU — `Karar.beklet` (K-131, denetim B1).
        # Rota beklerken tutulan paketler. Defterde hâlâ "KUYRUKTA"dırlar:
        # arayüz kuyruğu ile bu tampon arasında paket yer değiştirir, DURUM
        # değiştirmez. Bir geçiş yazılsaydı ikisi ayrı havuz olurdu ve
        # mutabakat kapısı ikisini ayrı sayardı.
        # ⚠️ Bugünkü dört koşum aletinin hiçbiri `beklet` döndürmüyor;
        # bu iki alan koşu boyunca BOŞ kalır ve satır birebir aynıdır.
        self.bekleyenler: deque[Paket] = deque()
        # Paket kimliği → tampon son tarihi. 🔒 İLK girişte kurulur ve
        # yeniden girişlerde TAZELENMEZ: tazelenseydi sık yeniden sorulan bir
        # paket tavanı hiç görmez, yani süre tavanı diye ilan edilen şey
        # uygulanmamış olurdu.
        self._tampon_son_tarih: dict[int, float] = {}

    # ==================================================================
    # GÖZLEM — protokolün gördüğü tek yüzey
    # ==================================================================
    def gozlem(self, t_s: float, paket: Paket | None) -> Gozlem:
        saat = self.kur.saatler.yerel(self.kimlik, t_s)
        gorunum = None
        if paket is not None:
            gorunum = PaketGorunumu(
                hedef=paket.hedef, kaynak=paket.kaynak, ttl=paket.ttl_kalan,
                atlama_sayisi=self.kur.konfig.ttl_baslangic - paket.ttl_kalan,
                bayt=paket.boyut_bayt, kaynak_sira=paket.kaynak_sira)
        return Gozlem(
            dugum=self.kimlik, saat_s=saat,
            olculen_gurultu_w=self.kur.kanal.girisim.girisim_w(
                self.kimlik, t_s, haric=-1) + self.kur.kanal.yayilim.gurultu_w,
            kanal_mesgul_mu=self.kanal_mesgul_mu(t_s),
            kuyruk_uzunlugu=len(self.kuyruk),
            kuyruk_kapasitesi=self.kuyruk.kapasite,
            son_iletim_sonucu=self._son_sonuc,
            son_iletim_hedefi=self._son_hedef,
            gonderilen_bayt=self._gonderilen_bayt,
            alinan_bayt=self._alinan_bayt,
            komsular=tuple(self._komsular.values()),
            paket=gorunum)

    def kanal_mesgul_mu(self, t_s: float,
                        ayni_an_haric: bool = False) -> bool:
        """Taşıyıcı dinleme — GEOMETRİK duyma kümesiyle.

        Gerekçesi `kurulum.py`de: girişim menzilinin ötesinde alınan güç
        gürültü tabanının altındadır, yani dışarıda bırakılan zaten
        duyulmazdı.

        🔴 `ayni_an_haric` — AYNI SLOTTA BAŞLAYAN İLETİMLER SAYILMAZ.
        DCF'nin birincil çarpışma mekanizması, geri çekilmesi aynı slotta
        biten iki düğümün İKİSİNİN DE göndermesidir. Olaylar sırayla
        işlendiği için, bu bayrak olmadan ikinci düğüm birincinin çerçevesini
        "kanal meşgul" görür ve erteler — yani çarpışma sessizce yok olur.
        ÖLÇÜLDÜ (statik-yok, 5 s, tohum 1000): 2842 karar anının **2**'sinde
        eski ve yeni anlam ayrışıyor — %0,07. Kardeş düzeltme
        (`taahhutlu_mu`) 4670 dondurma denemesinin **2**'sini etkiliyor —
        %0,04. Yani etki küçüktür; ama tohumlar arası yayılım zaten %76
        olduğu için koşu düzeyinde bir "önce/sonra" karşılaştırması bu
        büyüklüğü ÖLÇEMEZ ve öyle bir karşılaştırma yapılmadı.

        Küçük olması düzeltmeyi gereksiz yapmaz: Bianchi doğrulaması
        (`tests2/test_mac_dcf.py`) aynı slottaki gönderenlerin HEPSİNİN
        çarpıştığı ayrı bir koşumla yapılmıştı ve koşu döngüsünün onunla
        aynı anlamı taşıması gerekir. Aksi hâlde doğrulanan model ile
        koşturulan model iki farklı şey olurdu.
        """
        for iletim in self.kur.kanal.ortam.aktif(t_s):
            if iletim.gonderen == self.kimlik:
                continue
            if ayni_an_haric and iletim.baslangic_s >= t_s:
                continue
            if self.duyar_mi(iletim.gonderen, t_s):
                return True
        return self.karistirici_mesgul_mu(t_s)

    def karistirici_mesgul_mu(self, t_s: float) -> bool:
        """🔴 KARIŞTIRICI TAŞIYICI DİNLEMEYİ BU DÜĞÜMDE TETİKLİYOR MU?

        İKİ koşul birlikte aranır ve ikisi ayrı sorudur:

          1. SINIF geçerli görünümlü bir önbelge basıyor mu (`csma_ya_gorunur`)
             — gürültü karıştırıcısı basmaz, aldatıcı basar.
          2. O çerçeve BU DÜĞÜMDE gürültü tabanının üstünde mi alınıyor.

        🔴 KUSUR — 5 Eylül 2026'da bulundu ve düzeltildi. Eskiden yalnız (1)
        soruluyordu: `csma_ya_gorunur(t_s)` bir alıcı argümanı almıyor, yani
        karıştırıcı 1 km uzakta bile olsa ALANDAKİ HER DÜĞÜM erteliyordu.
        Ölçüldü: `aldatici` kolunda 320 pakete karşı **0 iletim denemesi,
        0 teslim** — bütün ağ, gücü ne olursa olsun kilitleniyordu. Bu
        fiziksel olarak imkânsızdır: taşıyıcı dinleme bir GÜÇ eşiğidir,
        küresel bir anahtar değil.

        Eşik gürültü tabanıdır — `girisim.kanal_mesgul_mu`nun varsayılanıyla
        aynı; iki yerde iki farklı eşik olsaydı "kanal meşgul" sorusunun iki
        cevabı olurdu.
        """
        k = self.kur.kanal.karistirici
        if k is None or not k.csma_ya_gorunur(t_s):
            return False
        konum = self.kur.topoloji.konum(self.kimlik, t_s)
        # 🔒 Y5: yalnız CSMA'ya görünen üyelerin gücü; tek karıştırıcıda aynı.
        return k.csma_guc_w(self.kimlik, konum,
                            t_s) > self.kur.kanal.yayilim.gurultu_w

    def duyar_mi(self, gonderen: int, t_s: float) -> bool:
        return (self.kur.topoloji.mesafe(gonderen, self.kimlik, t_s)
                <= self.kur.duyanlar_menzili_m)

    def mesgul_bitisi_s(self, t_s: float) -> float:
        """Kanalın boşalabileceği EN ERKEN an — yoklama yerine hesap.

        🔴 Donmuş bir geri çekilmeyi uyandırmanın tek yolu bir olaydır ve
        `OlayKuyrugu` iptal desteklemediği için "her DIFS'te bir bak" demek
        milyonlarca ölü olay üretirdi. Onun yerine meşguliyetin bittiği an
        DOĞRUDAN hesaplanır: duyulan iletimlerin en geç bitişi ve —
        CSMA'ya görünen bir karıştırıcı varsa — onun bir sonraki geçiş anı.
        """
        en_gec = t_s
        for iletim in self.kur.kanal.ortam.aktif(t_s):
            if iletim.gonderen == self.kimlik:
                continue
            if self.duyar_mi(iletim.gonderen, t_s):
                en_gec = max(en_gec, iletim.bitis_s)
        k = self.kur.kanal.karistirici
        if self.karistirici_mesgul_mu(t_s):
            ufuk = t_s + self.kur.konfig.beacon_araligi_s
            gecisler = k.gecis_anlari(t_s, ufuk)
            en_gec = max(en_gec, gecisler[0] if gecisler else ufuk)
        return en_gec

    # ==================================================================
    # KOMŞU TABLOSU — yalnız beacon'dan
    # ==================================================================
    def beacon_isle(self, komsu: int, yuk: tuple[tuple[str, object], ...],
                    t_s: float) -> None:
        saat = self.kur.saatler.yerel(self.kimlik, t_s)
        onceki = self._komsular.get(komsu)
        sozluk = dict(yuk)
        # 🔴 `None ≠ 0` — 16 Eylül 2026 (denetim B4). Burada `sozluk.get(ad, 0)`
        # vardı ve alanı beacon'a KOYMAYAN bir protokolde `0` dönüyordu; yani
        # *"bilgi yok"* ile *"ölçülen değer sıfır"* ayrışmıyordu. Kuralın
        # projedeki tek istisnası burasıydı.
        gurultu = sozluk.get("gurultu_w")
        kuyruk = sozluk.get("kuyruk")
        self._komsular[komsu] = KomsuKaydi(
            dugum=komsu, son_duyulma_s=saat,
            duyulan_beacon=(onceki.duyulan_beacon + 1 if onceki else 1),
            bildirdigi_gurultu_w=(None if gurultu is None else float(gurultu)),
            bildirdigi_kuyruk=(None if kuyruk is None else int(kuyruk)),
            bildirdigi_yuk=yuk)
        # 🔒 K-131 — kanca GÖZLEM alıyor. Gözlem komşu tablosu GÜNCELLENDİKTEN
        # SONRA üretilir: protokol, az önce duyduğu beacon'ı tablosunda görsün
        # ve kendi ölçtüğü gürültüyle yan yana koyabilsin diye.
        self.protokol.beacon_alindi(self.gozlem(t_s, None), komsu, yuk)
        self.kur.sayaclar.artir("beacon_alinan")

    def komsu_temizle(self, t_s: float) -> None:
        """Ömrünü doldurmuş kayıtları düşürür.

        ⚠️ Bu bir PROTOKOL kararı değil, BELLEK sınırlamasıdır. Tazelik
        kararı protokole aittir; `KomsuKaydi.yas_s()` ham yaşı verir.
        """
        saat = float(self.kur.saatler.yerel(self.kimlik, t_s))
        omur = self.kur.konfig.komsu_omru_s
        self._komsular = {k: v for k, v in self._komsular.items()
                          if saat - float(v.son_duyulma_s) <= omur}

    # ==================================================================
    # ÇEKİŞME — olay güdümlü geri çekilme
    # ==================================================================
    def yeni_surum(self) -> int:
        self._surum += 1
        return self._surum

    @property
    def surum(self) -> int:
        return self._surum

    def bekleme_baslat(self, t_s: float, bitis_s: float) -> None:
        self._bekleme_bas_s = t_s
        self._bitis_ani_s = bitis_s

    def taahhutlu_mu(self, t_s: float) -> bool:
        """Geri çekilmesi bu ana kadar bitmiş mi — yani göndermeye TAAHHÜTLÜ.

        🔴 Taahhütlü bir düğüm, aynı anda başlayan bir iletim yüzünden
        DONDURULAMAZ. Dondurulsaydı, geri çekilmesi aynı slotta biten iki
        düğümden ikincisi hiç gönderemez ve DCF'nin birincil çarpışma
        mekanizması modelden düşerdi.
        """
        return self._bitis_ani_s is not None and self._bitis_ani_s <= t_s

    @property
    def geri_sayiyor_mu(self) -> bool:
        """Sayaç işliyor mu — donmuş bir düğümde `False`."""
        return self._bekleme_bas_s is not None

    def bekleyen_slotlari_dus(self, t_s: float) -> None:
        """Boş geçen aralığı sayaçtan düşer. Slot slot işlemekle AYNI."""
        if self._bekleme_bas_s is None or self.dcf.durum != "geri_cekilme":
            return
        bos = self._bos_sure_s(self._bekleme_bas_s, t_s)
        if bos > 0.0:
            self.dcf.slot_gecti(int(math.floor(
                bos / self.kur.zamanlar.slot_s + 1e-9)))
        self._bekleme_bas_s = None
        self._bitis_ani_s = None

    def _bos_sure_s(self, bas_s: float, bitis_s: float) -> float:
        """`[bas, bitiş]` aralığında kanalın BOŞ kaldığı süre.

        🔴 Bu aralıkta duyulan bir İLETİM yoktur — iletim başlangıcı geri
        çekilmeyi dondurur ve aralığı kapatır. Geriye tek meşgul kaynağı
        kalır: CSMA'ya görünen karıştırıcı (`aldatici`). O da sayılmasaydı
        sahte çerçevelerin altında geri çekilme akmaya devam ederdi ve
        aldatıcı karıştırıcı olduğundan **zayıf** ölçülürdü.
        """
        toplam = bitis_s - bas_s
        k = self.kur.kanal.karistirici
        if toplam <= 0.0 or k is None or not k.csma_gorunur:
            return max(0.0, toplam)
        sinirlar = (bas_s,) + tuple(k.gecis_anlari(bas_s, bitis_s)) + (bitis_s,)
        return sum(b - a for a, b in zip(sinirlar, sinirlar[1:])
                   if not self.karistirici_mesgul_mu(0.5 * (a + b)))

    def bitis_ani_s(self, t_s: float) -> float:
        """Geri çekilmenin biteceği an — kanal boş kalırsa."""
        return t_s + self.dcf.geri_sayim * self.kur.zamanlar.slot_s

    # ==================================================================
    # KUYRUK ve KORUNUM
    # ==================================================================
    def kuyruga_al(self, paket: Paket, uretim: bool) -> bool:
        """Paketi kuyruğa alır. 🔴 Her yol deftere yazılır.

        `uretim=True` → paket burada DOĞDU (kaynak düğüm).
        `uretim=False` → başka düğümden geldi (uçuştan kuyruğa).
        """
        if uretim:
            self.kur.korunum.uret()
            self.kur.sayaclar.artir("uretilen_paket")
            self.kur.paket_defteri.dogdu(paket.kimlik, paket.akis_kimligi,
                                         paket.dogum_s)
        if self.kuyruk.ekle(paket):
            self.kur.sayaclar.tepe_guncelle("en_yuksek_doluluk",
                                            len(self.kuyruk))
            return True
        # 🔴 Dolu kuyruk: paket hiçbir yerde değil, DEFTERDEN geçmeli.
        self.kur.korunum.dus("kuyruk_tasmasi", nereden="kuyruk")
        self.kur.sayaclar.artir("kuyruk_tasmasi")
        self._kayip_yeri("kuyruk_tasmasi")
        return False

    def dus(self, sebep: str, nereden: str) -> None:
        self.kur.korunum.dus(sebep, nereden=nereden)
        self._kayip_yeri(sebep)
        if sebep in ("ttl", "hedef_yok", "iletim_basarisiz", "tampon_asimi"):
            self.kur.sayaclar.artir(
                {"ttl": "ttl_olumu", "hedef_yok": "hedef_yok",
                 "iletim_basarisiz": "mac_vazgecme",
                 "tampon_asimi": "tampon_dusen"}[sebep])

    # ==================================================================
    # ROTA BEKLEME TAMPONU — K-131 (denetim B1)
    # ==================================================================
    def beklemeye_al(self, paket: Paket, t_s: float, olaylar) -> None:
        """Protokol *"beklet"* dedi: paket tampona geçer, DÜŞMEZ.

        🔒 İKİ TAVAN, İKİSİ DE İLAN EDİLMİŞ ve ikisi de `tampon_asimi`
        sebebiyle deftere yazılır — sessiz düşürme yok:
          · SÜRE  — ilk girişten `rota_tamponu_omru_s` sonra
          · SAYI  — `rota_tamponu_kapasitesi`; taşmada EN ESKİ düşer

        🔴 Taşmada en eskinin düşmesi (baştan atma), arayüz kuyruğunun
        kuralının TERSİDİR ve bilinçlidir. Arayüz kuyruğu kuyruk sonu atma
        kullanır çünkü orada soru *"hangi paket gecikir"*dır. Burada soru
        *"hangi paket rotayı bekleyerek ÇOKTAN bayatladı"*dır; en eski paket
        en bayat olandır ve NS-2'nin `aodv_rqueue`si de onu atar.
        """
        kfg = self.kur.konfig
        son_tarih = self._tampon_son_tarih.get(paket.kimlik)
        if son_tarih is None:
            son_tarih = t_s + kfg.rota_tamponu_omru_s
            self._tampon_son_tarih[paket.kimlik] = son_tarih
            olaylar.ekle(son_tarih, self.tampon_suresi_doldu, paket.kimlik)
        elif t_s >= son_tarih:
            # ⚠️ Süre tavanı, paket TAMPON DIŞINDAYKEN (yeniden sorulmak
            # üzere kuyruğa konmuşken) dolmuş olabilir; o an ateşlenen olay
            # onu bulamaz. Burası o kapıyı kapatır: süresi dolmuş bir paket
            # tampona GERİ ALINMAZ.
            self.dus("tampon_asimi", nereden="kuyruk")
            self._tampon_son_tarih.pop(paket.kimlik, None)
            return
        while len(self.bekleyenler) >= kfg.rota_tamponu_kapasitesi:
            eski = self.bekleyenler.popleft()
            self.dus("tampon_asimi", nereden="kuyruk")
            self._tampon_son_tarih.pop(eski.kimlik, None)
        self.bekleyenler.append(paket)
        s = self.kur.sayaclar
        s.artir("tampon_giris")
        s.tepe_guncelle("en_yuksek_tampon", len(self.bekleyenler))

    def tampon_suresi_doldu(self, paket_kimligi: int) -> None:
        """Süre tavanı doldu. Paket hâlâ tampondaysa DÜŞER.

        🔒 Tamponda değilse hiçbir şey yapılmaz ve kayıt SİLİNMEZ: paket o an
        yeniden sorulmak üzere arayüz kuyruğundadır ve `beklemeye_al` onu geri
        almayı reddedecektir. Kaydı burada silmek, paketin tavanı bir daha
        hiç görmemesi demek olurdu.
        """
        for i, p in enumerate(self.bekleyenler):
            if p.kimlik == paket_kimligi:
                del self.bekleyenler[i]
                self.dus("tampon_asimi", nereden="kuyruk")
                self._tampon_son_tarih.pop(paket_kimligi, None)
                return

    def tamponu_kuyruga_dok(self) -> bool:
        """Bekleyenleri arayüz kuyruğuna geri koyar — *"yeniden sor"*.

        🔒 Kuyruğun SONUNA konur, başına değil. NS-2'nin AODV'si de rota
        gelince tamponu normal arayüz kuyruğuna basar; başa koymak, rota
        beklerken doğmuş DAHA YENİ paketleri geciktirirdi.

        🔴 KUYRUK DOLARSA DÖKME DURUR, kalanlar tamponda BEKLEMEYE DEVAM EDER.
        İlk yazımda döngü dolu kuyrukta da sürüyordu ve kalan her paket
        `kuyruk_tasmasi` ile düşüyordu: GEÇİCİ bir doluluk tamponun tamamını
        yok ederdi — tamponun var olma sebebinin tam tersi. Bekleyen paketin
        süre tavanı zaten işliyor; onu bir kuyruk doluluğu yüzünden erken
        öldürmenin gerekçesi yok.

        ⚠️ Kalanlar bir sonraki yeniden sormada tekrar denenir. Yeniden sorma
        yalnız dışarıdan olay geldiğinde olur (`kosum/kontrol.py`), yani bu
        bir yoklama döngüsü doğurmaz.
        """
        tasindi = False
        while self.bekleyenler and not self.kuyruk.dolu_mu:
            p = self.bekleyenler.popleft()
            # 🔒 Dolu olmayan kuyruk paketi reddedemez; iddia KIRILABİLİR
            # olsun diye bir değişmez olarak yazılıyor, sessiz bir `else`
            # dalı olarak değil — o dal hiç ateşlenmez ve ateşlenmeyen bir
            # dal, korumadığı bir şeyi koruyormuş gibi görünür.
            dogrula(self.kuyruga_al(p, uretim=False),
                    "dolu olmayan kuyruk paketi reddetti — kuyruk ile "
                    "tampon arasındaki muhasebe ayrışmış")
            tasindi = True
        return tasindi

    def _kayip_yeri(self, sebep: str) -> None:
        """Yere toplamada düşüşün geçide mesafesi — teşhis (`olcum/kayip_yeri`).

        🔒 Korunum defterine giden İKİ çağrı noktasının ikisinden de çağrılır;
        toplamı her koşuda düşen paket sayısına eşit olmak zorundadır.
        """
        k = self.kur.kayip_yeri
        if k is not None:
            k.kaydet(sebep, self.kur.topoloji.mesafe(
                self.kimlik, self.kur.konfig.gecit, self.kur.olaylar.simdi))

    # ==================================================================
    # PROTOKOL KANCALARI
    # ==================================================================
    def sonraki_atlama(self, paket: Paket, t_s: float) -> Karar:
        karar = self.protokol.sonraki_atlama(self.gozlem(t_s, paket))
        dogrula(isinstance(karar, Karar),
                "protokol `Karar` döndürmeli — `int | None` değil")
        for beyan in karar.beyan:
            self.beyan_isle(beyan, t_s)
        if karar.niyetler:
            self.kontrol.niyet_al(karar.niyetler)
        return karar

    def beyan_isle(self, beyan, t_s: float) -> None:
        """Protokolün *"şu oldu"* dediğini deftere ve sayaca yazar.

        🔒 TEK KAYNAK — 16 Eylül 2026 (`04` K-134). Bu gövde `sonraki_atlama`
        içindeydi ve beyan yalnız oradan gelebiliyordu. Kancalar da beyan
        döndürebilir hâle gelince (`kosum/kontrol.py`) ikinci bir kopya
        yazmak gerekirdi; `03` §B5'in *"aynı kuralı iki yerde yazmak"*
        hatası olurdu. Gövde buraya alındı, iki çağıran da buradan geçiyor.

        ⚠️ `Beyan` tipi İÇE AKTARILMIYOR: `kosum/` o tipi görmesi gereken bir
        katman değil (`tests2/test_olcum.py` yalnız `olcum/` ve `gozlem/`e
        izin veriyor). Buraya yalnız DOĞRULANMIŞ bir beyan gelir — kapalı
        kümeyi `gozlem/kontrol.py::niyetleri_dogrula` ve `Beyan.__post_init__`
        bağlar.
        """
        sonuc = self.kur.rota_defteri.beyan_isle(self.kimlik, beyan, t_s)
        # 🔴 COR'UN SAYAÇ İKİZİ DEFTERDEN BESLENİR (19 Eylül 2026, K-141).
        # `rota_etkilendi` sayacı tanımlıydı ama HİÇBİR YERDE artırılmıyordu;
        # sayaçtan türeyen `cor` ve `cor_pencere` paydası sıfır olduğu için
        # HER ZAMAN boş dönüyordu. `rota_kurtarildi` ise her `rota_kuruldu`yu
        # sayıyordu — Δ'yı kapatsın kapatmasın. İkisi de artık defterin
        # döngü muhasebesinden geliyor, yani iki COR hesabı aynı tanımdır.
        if beyan.tip == "kopma":
            self.kur.sayaclar.artir("kopma_algilanan")
            if sonuc == "acildi":
                self.kur.sayaclar.artir("rota_etkilendi")
        elif beyan.tip == "rota_kuruldu":
            if sonuc == "kapandi":
                self.kur.sayaclar.artir("rota_kurtarildi")
        else:
            self.kur.sayaclar.artir("kopma_rota_gecersiz")

    def beacon_yuku(self, t_s: float
                    ) -> tuple[tuple[tuple[str, object], ...], int]:
        """Protokolün beacon'a koyduğu alanlar **ve** bayt bedeli.

        🔴 SAYAÇ ARTIK BURADA ARTMIYOR — 9 Eylül 2026, K-111 EK-2.
        Eskiden bu metot `kontrol_bayt`a yükü ekliyor, `kosu.py` de ayrıca
        çerçeveyi ekliyordu. Bedel çerçevenin BOYUTUNA girdiği için ikisi
        birden sayılsaydı yük **çift faturalanırdı**. Tek kaynak: çerçeve.

        🔒 Ve asıl kusur buydu: yük yalnız SAYAÇTA ödeniyordu. Çerçeve
        kurulumda bir kez kurulmuş, SABİT boyutluydu — yani 250 baytlık bir
        yük çerçeveyi 4,12 kat uzatması gerekirken hiç uzatmıyordu. Yükü
        şişiren bir protokol fizikte BEDAVA taze komşu bilgisi alıyordu:
        fazladan hava süresi yok, fazladan çarpışma riski yok, fazladan
        gövde hatası yok. Gözlem sözleşmesinin *"koymak ve BEDELİNİ
        ÖDEMEK zorundadır"* maddesi yarım uygulanmıştı.

        ⚠️ `yuk_bayt` ÖNCE çağrılır: sözleşme ihlallerinde hangi hatanın
        önce fırlayacağı değişmesin diye (`yuku_dondur` da doğruluyor).
        """
        # 🔒 K-131 — kanca artık GÖZLEM alıyor: protokol kendi ölçtüğü
        # gürültüyü beacon'a koyabilsin diye. `paket=None`: elde paket yok.
        yuk = self.protokol.beacon_yuku(self.gozlem(t_s, None))
        ek_bayt = yuk_bayt(yuk)
        return yuku_dondur(yuk), ek_bayt

    def teshis(self) -> dict:
        return teshis_dogrula(self.kimlik, self.protokol.teshis(self.kimlik))

    # ==================================================================
    # İLETİM DEFTERİ
    # ==================================================================
    def iletim_kaydet(self, iletim: Iletim, hedef: int | None,
                      sonuc: str | None) -> None:
        self._son_sonuc = sonuc
        self._son_hedef = hedef
        self._gonderilen_bayt += iletim.cerceve.bayt

    def iletim_sonucu(self, sonuc: str) -> None:
        """Son iletimin sonucu — gözlem penceresinin SIFIR BAYTLIK bilgisi."""
        self._son_sonuc = sonuc

    def tekrar_mi(self, gonderen: int, ucus_no: int) -> bool:
        """Bu atlamayı bu komşudan daha önce aldık mı?"""
        return ucus_no <= self._son_ucus.get(gonderen, -1)

    def gorduk(self, gonderen: int, ucus_no: int) -> None:
        self._son_ucus[gonderen] = ucus_no

    def alim_kaydet(self, bayt: int) -> None:
        self._alinan_bayt += bayt

    # ------------------------------------------------------- uçuş durumu
    @property
    def ucustaki(self) -> Paket | None:
        return self._ucustaki

    @property
    def ucus_hedefi(self) -> int | None:
        return self._ucus_hedefi

    @property
    def devredildi(self) -> bool:
        return self._devredildi

    @property
    def ucus_no(self) -> int:
        return self._ucus_no

    def devret(self, ucus_no: int) -> None:
        """Paket alıcıya geçti — defterde artık uçuşta DEĞİL."""
        dogrula(self._ucustaki is not None and ucus_no == self._ucus_no,
                "el değiştirme, uçuşta olmayan ya da başka bir atlamaya ait "
                "bir paket için bildirildi")
        self._devredildi = True

    def ucusa_al(self, paket: Paket, hedef: int) -> None:
        dogrula(self._ucustaki is None, "aynı anda iki paket uçuşta olamaz")
        # Paket tamponu geride bıraktı; son tarih kaydı da gitmeli. Kalsaydı
        # sözlük koşu boyunca büyür ve ölü kayıtlar biriktirirdi.
        self._tampon_son_tarih.pop(paket.kimlik, None)
        self._ucustaki = paket
        self._ucus_hedefi = hedef
        self._ucus_no += 1
        self._devredildi = False

    def ucustan_indir(self) -> Paket:
        dogrula(self._ucustaki is not None, "uçuşta paket yok")
        paket = self._ucustaki
        self._ucustaki = None
        self._ucus_hedefi = None
        self._devredildi = False
        return paket

    @property
    def onay_bekleniyor(self) -> bool:
        return self._onay_bekleniyor

    def onay_bekle(self, deger: bool) -> None:
        self._onay_bekleniyor = deger
