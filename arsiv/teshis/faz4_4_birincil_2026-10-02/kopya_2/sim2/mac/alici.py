"""
Alıcı zinciri — düğüm başına TEK radyo, önbelge kilidi ve capture effect.

🔴 KUSUR 2: ALICI ZİNCİRİ KISITI YOKTU
======================================
Eski simülatörde bir düğüm, zamanda çakışan **iki** çerçeveyi de başarıyla
alabiliyordu: her alım bağımsız bir PER çekimiydi ve alıcının o sırada başka
bir şeyle meşgul olup olmadığı hiç sorulmuyordu. Tek radyolu bir telsizde bu
imkânsızdır. Sonuç, çarpışmaların sistematik olarak HAFİF görünmesiydi —
gizli terminal senaryolarında iki çerçeve de "geçiyor" sayılıyordu.

🔒 ÇÖZÜM: durum makinesi ve tek bir değişmez
    bos → onbelge_kilidi → govde_aliyor → bos
    **Aynı anda en fazla BİR kilitli çerçeve.**

🔴 KUSUR 3: CAPTURE EFFECT YOKTU
================================
Gerçek bir alıcı, kilitli olduğu çerçeveden yeterince güçlü bir yenisi
gelirse ona geçer (capture). Bu yoksa güçlü bir komşunun çerçevesi zayıf bir
çerçevenin arkasında sıraya girer ve ağın taşıma kapasitesi olduğundan düşük
ölçülür. Kip `Konfig.yakalama_etkisi_acik` ile ablasyona açıktır.

🔒 BU DOSYADA TEK BİR FİZİK FORMÜLÜ YOK
=======================================
Kusur 5, MAC'in Kat 2 ile Kat 3'ü karıştırmasıydı: `alim_per`, `_girisim_w`,
`_parca_sinirlari` aslında kanal fiziğiydi ve `mac.py` içinde duruyordu.
Burada yalnız **durum makinesi** var; her SINR, PER ve güç sorusu `kanal/`a
sorulur. Bir test bunu AST ile denetler.

⚠️ SEBEP KÜMESİ KAPALI ve TOPLAMI DENETLENİR
============================================
Her alım denemesi **tam olarak bir** sonuç üretir:

    alim_basarili · alim_red_yari_cift · alim_red_mesgul
    alim_red_onbelge · alim_red_per

`alim_yakalama` bunlara ek bir **işarettir**, altıncı bir sonuç değil:
yakalama olduğunda yeni çerçeve `alim_basarili`ya, ezilen eski çerçeve
`alim_red_mesgul`e gider. Toplam her zaman deneme sayısına eşittir ve kapanış
ölçütü budur.
"""

from __future__ import annotations

from dataclasses import dataclass

from sim2.cekirdek.degismezler import asla, dogrula
from sim2.cekirdek.rng import hash_cekimi
from sim2.cekirdek.sayaclar import kume_uyeleri
from sim2.kanal.cerceve import cerceve_kur
from sim2.kanal.girisim import Iletim
from sim2.kanal.kanal import Kanal
from sim2.yapilandirma.konfig import Konfig

__all__ = ["ALIM_SONUCLARI", "DURUMLAR", "AlimSonucu", "AliciZinciri"]

# 🔒 Kapalı küme, ve SAYAÇ KAYIT DEFTERİNDEN türetiliyor.
# "diğer" diye bir sonuç yoktur: sebebi bilinmeyen bir başarısızlık, teşhis
# edilmemiş bir hatadır.
#
# 🔴 Burada elle bir liste yazmak kusur 6'nın ta kendisi olurdu — iki liste
# sessizce ayrışır ve `Σ sebep = toplam` denetimi yanlış bir bütünü ölçerdi.
# Yeni bir sonuç sayacı `sayaclar.TANIMLAR`a `kume="alim_sonucu"` ile
# eklendiğinde buraya OTOMATİK katılır ve toplam denetimine girer.
ALIM_SONUCLARI: tuple[str, ...] = kume_uyeleri("alim_sonucu")

DURUMLAR: tuple[str, ...] = ("bos", "onbelge_kilidi", "govde_aliyor")


@dataclass(frozen=True, slots=True)
class AlimSonucu:
    """Tek bir alım denemesinin sonucu. Sebep her zaman vardır."""

    sebep: str
    iletim: Iletim
    t_s: float
    yakalama: bool = False
    # Başarılı alımda alıcının kilitlendiği güç (W) — RSSI'ın kaynağı
    # (`v2/15` B2). Başarısız sonuçta 0; alım kararına girmez.
    guc_w: float = 0.0

    @property
    def basarili(self) -> bool:
        return self.sebep == "alim_basarili"


class AliciZinciri:
    """Bir düğümün alıcısı. Durum makinesi — fizik `kanal/`da.

    🔒 DEĞİŞMEZ: `_kilitli` aynı anda en fazla bir iletim tutar. Her geçişte
    denetlenir; ihlal `DegismezHatasi` fırlatır, sessizce geçmez.
    """

    __slots__ = ("dugum", "konfig", "kanal", "_kilitli", "_kilit_ani_s",
                 "_kilit_gucu_w", "_gonderiyor", "_bos_bas_s", "_sahte",
                 "_kilitli_s")

    def __init__(self, dugum: int, konfig: Konfig, kanal: Kanal) -> None:
        dogrula(0 <= dugum, "düğüm numarası negatif olamaz")
        self.dugum = dugum
        self.konfig = konfig
        self.kanal = kanal
        self._kilitli: Iletim | None = None
        self._kilit_ani_s = 0.0
        self._kilit_gucu_w = 0.0
        self._gonderiyor = False
        # 🔒 A6 (K-176) — alıcının boşa çıktığı son an ve aldatıcının sahte
        # çerçevesinin biçimi (kilit PER'i için; yalnız gerçekçide).
        self._bos_bas_s = 0.0
        # C3 (K-180): kilitli geçen toplam süre.
        self._kilitli_s = 0.0
        self._sahte = (cerceve_kur(konfig, "veri")
                       if konfig.karistirici_gercekci else None)

    # ------------------------------------------------------------- durum
    @property
    def kilitli_iletim(self) -> Iletim | None:
        """Alıcının kilitlendiği çerçeve — A3 önbelge sezmesi (K-174)."""
        return self._kilitli

    @property
    def durum(self) -> str:
        if self._kilitli is None:
            return "bos"
        bitis_onbelge = self._kilitli.cerceve.onbelge_araligi(
            self._kilitli.baslangic_s)[1]
        return "onbelge_kilidi" if self._kilit_ani_s < bitis_onbelge \
            else "govde_aliyor"

    @property
    def gonderiyor(self) -> bool:
        return self._gonderiyor

    def gonderime_basla(self, t_s: float = 0.0) -> "AlimSonucu | None":
        """🔴 YARIM ÇİFT: gönderirken alınamaz.

        Kilitli bir çerçeve varsa düşer — kendi iletimimiz onu bastırır.

        🔴 DÜŞEN KİLİT BİR SONUÇ DÖNDÜRÜR ve çağıran onu SAYMAK zorundadır.
        Döndürmeseydi o alım denemesi hiçbir sebebe yazılmadan yok olurdu:
        `cerceve_geldi` onu bir deneme olarak saymış, `cerceve_bitti` ise
        kilit boşaldığı için `None` dönerdi. `Σ sebep = toplam deneme`
        kapanış ölçütü sessizce kırılırdı — ve kırılan şey, kusur 2'yi
        yakalayan denetimin ta kendisi olurdu.
        """
        dusen = None if self._kilitli is None else AlimSonucu(
            "alim_red_yari_cift", self._kilitli, t_s)
        if self._kilitli is not None:
            self._kilitli_s += t_s - self._kilit_ani_s          # C3
        self._gonderiyor = True
        self._kilitli = None
        return dusen

    def gonderim_bitti(self, t_s: float | None = None) -> None:
        self._gonderiyor = False
        # A6: yayın sırasında başlayan sahte çerçevenin başı kaçırılmıştır.
        if t_s is not None:
            self._bos_bas_s = t_s

    # ------------------------------------------------- rastgelelik (durumsuz)
    def _cekim(self, etiket: str, gonderen: int, t_s: float) -> float:
        """🔒 Alım kararı HASH'ten, sıralı akıştan değil.

        Bir koşuda kaç alım denemesi olduğu PROTOKOLE göre değişir; sıralı bir
        akış olsaydı çok deneme yapan protokol akışı kaydırır ve iki kol aynı
        tohumda farklı kanallar görürdü.

        Dilim genişliği `Konfig.kanal_dilimi_s` (100 µs): aynı dilimdeki iki
        deneme aynı çekimi paylaşır. Ölçüldü — ardışık denemeler arası en
        küçük fark 124 µs, yani 100 µs'te çakışma olmuyor.

        🔒 Önbelge ve gövde kararları AYNI hash alanından ama FARKLI
        anahtarla çekilir (`etiket`). Aynı anahtar kullanılsaydı önbelgeyi
        geçen her çerçeve gövdeyi de geçerdi ve `alim_red_per` hiç
        ateşlenmezdi. Yeni bir hash ALANI eklemek de gerekmez — anahtarı
        genişletmek eski çekimleri kaydırmaz.
        """
        dilim = int(t_s / self.konfig.kanal_dilimi_s)
        return hash_cekimi("kanal_karar", self.konfig.tohum, gonderen,
                           self.dugum, dilim, etiket)

    # ------------------------------------------------------------ olaylar
    def cerceve_geldi(self, iletim: Iletim, t_s: float
                      ) -> tuple[AlimSonucu | None, AlimSonucu | None]:
        """Bir çerçevenin ÖNBELGESİ geldi. İki sonuç dönebilir:

            (yeni_cerceve_sonucu, ezilen_cerceve_sonucu)

        `None` = "henüz belli değil, gövde bitince karara bağlanacak".
        Yakalama olduğunda ikinci alan dolar: ezilen çerçeve o anda
        `alim_red_mesgul` olarak kapanır.
        """
        dogrula(iletim.gonderen != self.dugum,
                "düğüm kendi çerçevesini almaya çalışamaz")

        if self._gonderiyor:
            return AlimSonucu("alim_red_yari_cift", iletim, t_s), None

        onbelge_hata = self.kanal.onbelge_alim_per(
            iletim.gonderen, self.dugum, iletim.cerceve, iletim.baslangic_s,
            verici_w=iletim.guc_w)
        kilitlenebilir = self._cekim("onbelge", iletim.gonderen,
                                     iletim.baslangic_s) >= onbelge_hata
        yeni_guc = self.kanal.girisim.sinyal_w(
            iletim.gonderen, self.dugum, t_s, verici_w=iletim.guc_w)

        # ---------------------------------------------------------- boşta
        if self._kilitli is None:
            # 🔒 A6: aldatıcının sahte çerçevesine kilitliyse alınamaz.
            if self.sahte_kilitli_mi(t_s, yeni_guc):
                return AlimSonucu("alim_red_mesgul", iletim, t_s), None
            if not kilitlenebilir:
                return AlimSonucu("alim_red_onbelge", iletim, t_s), None
            self._kilitle(iletim, t_s, yeni_guc)
            return None, None

        # -------------------------------------------------------- kilitli
        if self._yakalanir_mi(yeni_guc, t_s) and kilitlenebilir:
            ezilen = AlimSonucu("alim_red_mesgul", self._kilitli, t_s,
                                yakalama=True)
            self._kilitle(iletim, t_s, yeni_guc)
            return None, ezilen
        return AlimSonucu("alim_red_mesgul", iletim, t_s), None

    def cerceve_bitti(self, iletim: Iletim, t_s: float) -> AlimSonucu | None:
        """Çerçevenin gövdesi bitti. Kilitliyse gövde kararı verilir.

        Kilitli değilse `None` döner: o çerçeve `cerceve_geldi`de zaten
        karara bağlanmıştı ve İKİNCİ KEZ sayılmamalıdır.
        """
        if self._kilitli is None or self._kilitli is not iletim:
            return None
        self._kilitli_s += t_s - self._kilit_ani_s              # C3
        self._kilitli = None
        self._bos_bas_s = t_s
        govde_hata = self.kanal.alim_per(
            iletim.gonderen, self.dugum, iletim.cerceve, iletim.baslangic_s,
            verici_w=iletim.guc_w)
        if self._cekim("govde", iletim.gonderen,
                       iletim.baslangic_s) < govde_hata:
            return AlimSonucu("alim_red_per", iletim, t_s)
        return AlimSonucu("alim_basarili", iletim, t_s,
                          guc_w=self._kilit_gucu_w)

    # ---------------------------------------- C1 · C3 (K-180)
    def kapat(self, t_s: float) -> None:
        """Düğüm öldü: telsiz kapanır; açık kilit o anda biter."""
        if self._kilitli is not None:
            self._kilitli_s += t_s - self._kilit_ani_s
        self._kilitli = None

    def kilitli_sure_s(self, t_s: float) -> float:
        """Kilitli geçen toplam süre — `t_s`e kadar açık kilit dâhil."""
        acik = 0.0 if self._kilitli is None else t_s - self._kilit_ani_s
        return self._kilitli_s + acik

    # ---------------------------------------- A6 · aldatıcı kilidi (K-176)
    def sahte_kilitli_mi(self, t_s: float,
                         yeni_guc_w: float | None = None) -> bool:
        """Alıcı şu an aldatıcının sahte çerçevesine KİLİTLİ mi — tembel model.

        Her sahte çerçeve için olay üretmek (saniyede ~400 çerçeve × düğüm)
        yerine sorulduğu anda hesaplanır: çerçevenin BAŞINDA alıcı boştaydı
        (`_bos_bas_s` ≤ başlangıç, yayında değil) ve önbelgesi o anki SNR ile
        önbelge PER'ini geçti (hash, `kanal_karar` alanı `sahte` anahtarı).
        Gerçek çerçeve yakalama koşulunu sağlarsa sahteyi ezer.
        ⚠️ Beyan: sahte önbelgenin PER'inde öteki girişim ihmal edilir; sahte
        çerçevenin gerçek çerçeveyi ORTASINDAN yakalaması modellenmez (o
        durumda sahte zaten SINR'da girişimdir).
        """
        k = self.kanal.karistirici
        if (self._sahte is None or k is None or not k.csma_gorunur
                or self._kilitli is not None or self._gonderiyor):
            return False
        konum = self.kanal.topoloji.konum(self.dugum, t_s)
        for bas, guc_w, kimlik in k.sahte_cerceveler(self.dugum, konum, t_s):
            if bas < self._bos_bas_s or guc_w <= 0.0:
                continue
            if (yeni_guc_w is not None and self.konfig.yakalama_etkisi_acik
                    and yeni_guc_w >= 10.0 ** (self.konfig.yakalama_esigi_db
                                               / 10.0) * guc_w
                    and t_s - bas <= self.konfig.yakalama_penceresi_s):
                continue
            per = self.kanal.sahte_onbelge_per(self._sahte, guc_w)
            if hash_cekimi("kanal_karar", self.konfig.tohum, kimlik,
                           self.dugum, int(bas / self.konfig.kanal_dilimi_s),
                           "sahte") >= per:
                return True
        return False

    # ------------------------------------------------------------- içsel
    def _kilitle(self, iletim: Iletim, t_s: float, guc_w: float) -> None:
        if self._kilitli is not None:                           # C3: yakalama
            self._kilitli_s += t_s - self._kilit_ani_s
        self._kilitli = iletim
        self._kilit_ani_s = t_s
        self._kilit_gucu_w = guc_w
        dogrula(self._kilitli is not None, "kilit kurulamadı")

    def _yakalanir_mi(self, yeni_guc_w: float, t_s: float) -> bool:
        """Capture effect: yeni çerçeve eskisini ezer mi?

        İki koşul birlikte: **güç farkı** eşiği aşmalı VE yeni çerçeve
        yakalama penceresi İÇİNDE gelmiş olmalı. Pencere koşulu olmasaydı
        alıcı, neredeyse bitmiş bir gövdeyi bırakıp yeni bir önbelgeye geçer
        ve gerçekte imkânsız bir davranış üretirdi — gerçek alıcılar gövde
        çözümüne başladıktan sonra kilidi kolay bırakmaz.
        """
        if not self.konfig.yakalama_etkisi_acik:
            return False
        if self._kilit_gucu_w <= 0.0:
            return True
        esik = 10.0 ** (self.konfig.yakalama_esigi_db / 10.0)
        if yeni_guc_w < esik * self._kilit_gucu_w:
            return False
        return (t_s - self._kilit_ani_s) <= self.konfig.yakalama_penceresi_s


def sonuc_dogrula(sayimlar: dict[str, int], deneme: int) -> None:
    """🔒 Kapanış ölçütü: `Σ sebep = toplam deneme`.

    Sebep kümesi kapalı olduğu için toplamın denemeye eşit olmaması, bir
    denemenin ya hiç sayılmadığı ya İKİ KEZ sayıldığı anlamına gelir.
    """
    bilinmeyen = set(sayimlar) - set(ALIM_SONUCLARI)
    if bilinmeyen:
        asla(f"bilinmeyen alım sonucu: {sorted(bilinmeyen)}")
    toplam = sum(sayimlar.get(s, 0) for s in ALIM_SONUCLARI)
    dogrula(toplam == deneme,
            "alım sonuçlarının toplamı deneme sayısına eşit değil — bir "
            "deneme ya hiç sayılmadı ya iki kez sayıldı")
