"""
Koşu — olay döngüsü ve çekişme. Bütün katmanların birleştiği yer.

🔒 SEKİZ OLAY, BAŞKA YOK
========================
    dogum · beacon · geri_cekilme_bitti · difs_bitti
    iletim_bitti · cerceve_geldi · cerceve_bitti · onay_penceresi

Yayılım gecikmesi modellenmez: 600 m'de 2 µs, slotun (20 µs) onda biri.
Kapsam belgesine yazılır.

🔒 ÜÇ DOSYA, ÜÇ SORUMLULUK
==========================
    kosu.py      olayı al, durumu ilerlet · çekişmeyi sür
    gonderim.py  çerçeveyi havaya ver · yeniden dene · vazgeç
    teslim.py    paketi el değiştir · onayla · deftere yaz

Tek dosyadayken 214 kod satırıydı ve olay döngüsü kendi doğurduğu ayrıntının
içinde kayboluyordu. Bölünme mekanikti ve sonucun BİREBİR aynı kaldığı
ölçülerek doğrulandı.

🔴 GERİ ÇEKİLME SÜRÜMLE GEÇERSİZLENİR
=====================================
`OlayKuyrugu` iptal desteklemiyor (taşınan, denetlenmiş modül). Her
zamanlanmış bitiş bir SÜRÜM taşır; ateşlendiğinde düğümün güncel sürümüyle
karşılaştırılır ve eskiyse yok sayılır. Bayat bir olay karar veremez.

🔴 DONMA VE UYANMA — YOKLAMA YOK
================================
Bir iletim başladığında onu **duyan** ve geri sayan düğümler dondurulur;
donan düğüm, meşguliyetin biteceği an DOĞRUDAN hesaplanarak
(`Dugum.mesgul_bitisi_s`) DIFS sonrasına uyandırılır. *"Her DIFS'te bir bak"*
demek koşu başına milyonlarca ölü olay üretirdi.

🔒 BEACON DA ÇEKİŞİR
====================
Beacon, düğüm gönderiyorsa ya da kanal meşgulse **atlanır**;
`beacon_gonderilen` yalnız fiilen gönderilenleri sayar. Çekişmeden
yayınlansaydı çarpışma oranı sistematik yükselir ve ölçülen şey kontrol
düzleminin bedeli değil, modelin kuralsızlığı olurdu.
"""

from __future__ import annotations

from sim2.kanal.girisim import Iletim
from sim2.kosum import kontrol
from sim2.kosum.dugum import Dugum
from sim2.kosum.gonderim import (alim_say, beacon_cercevesi, gonder,
                                 iletime_basla, vazgec, veri_cercevesi_kur)
from sim2.kosum.kurulum import Kurulum
from sim2.kosum.teslim import onay_alindi, veri_alindi
from sim2.olcum.kopma import fiziksel_kopma_say

__all__ = ["Kosu"]


class Kosu:
    """Tek bir koşu. `kostur()` bir kez çağrılır, sonra sonuç okunur."""

    __slots__ = ("kur", "dugumler", "olaylar", "_temizleme_s",
                 "_beacon_onbellegi", "veri_cercevesi", "veri_baslik_bayt",
                 "veri_baslik_sure_s")

    def __init__(self, kur: Kurulum, protokol_fabrikasi) -> None:
        self.kur = kur
        self.olaylar = kur.olaylar
        self.dugumler = tuple(Dugum(i, kur, protokol_fabrikasi(i))
                              for i in range(kur.dugum_sayisi))
        # 🔒 Y2 · K-151 — protokolün veri başlığı (`gonderim.py`).
        (self.veri_cercevesi, self.veri_baslik_bayt,
         self.veri_baslik_sure_s) = veri_cercevesi_kur(kur, self.dugumler)
        # Havadaki iletim defterini budama gecikmesi. Sürmekte olan bir alımın
        # girişim penceresi en çok bir veri çerçevesi kadar geriye bakar; daha
        # erken budamak girişim hesabından iletim düşürürdü. Budanmasaydı
        # `Ortam.aktif()` koşu boyunca yüz binlerce iletimi tarardı.
        self._temizleme_s = 2.0 * self.veri_cercevesi.sure_s
        # Yuk boyutuna gore beacon cercevesi onbellegi — SAF memo.
        self._beacon_onbellegi: dict = {}

    def kostur(self) -> None:
        k = self.kur.konfig
        for dogum in self.kur.trafik.cizelge:
            self.olaylar.ekle(dogum.t_s, self._dogum, dogum)
        # 🔒 Y3 · R2 — beacon protokol başına kapatılabilir. Fazlar yine
        # KURULUMDA çekilir, yani akış kaymaz ve öteki kollar etkilenmez.
        for n, faz in enumerate(self.kur.beacon_fazlari):
            if self.dugumler[n].kontrol.kosum_beaconi:
                self.olaylar.ekle(faz, self._beacon, n)
        kontrol.zamanlayicilari_kur(self)
        self.olaylar.ekle(k.olcum_penceresi[0], self.kur.sayaclar.pencere_baslat)
        self.olaylar.ekle(k.olcum_penceresi[1], self.kur.sayaclar.pencere_bitir)
        self.olaylar.kostur(k.kosu_bitis_s)
        self.kur.sayaclar.artir("islenen_olay", self.olaylar.islenen_olay)
        self._fiziksel_kopmalari_say()

    def _fiziksel_kopmalari_say(self) -> None:
        """🔴 `kopma_fiziksel`in AÇIK TAAHHÜDÜ — son işlem, sıcak yol yok.

        Payda olmadan `algilama_duyarliligi` her koşuda `None` dönüyordu ve
        Risk 3'ün nicel yarısı ölüydü. Tanım, ızgara ve karıştırıcının neden
        dışarıda kaldığı `olcum/kopma.py` başlığında.

        🔒 Ölçüm PENCERESİNDE sayılır: sayacın pencere ikizi ile ham değeri
        bu yüzden eşittir ve bu bilinçlidir — ısınmadaki çalkantı, ölçülen
        algılama oranının paydasına giremez.

        🔴 BU YÜZDEN `pencere_icinde_olculdu` — 16 Eylül 2026 (B2).
        Sayaçlar artık pencere kapanınca DONUYOR. Bu çağrı koşu bittikten
        SONRA yapılır, yani sıradan `artir` ile yazılsaydı ikize HİÇ
        giremezdi. Ölçüldü (`bagimsiz-surekli`, tohum 1000): ham 49, ikiz
        49 → **0** olurdu ve `algilama_duyarliligi_pencere` 0,0 yerine
        `None` dönerdi — Risk 3'ün nicel yarısı sessizce ölürdü.
        """
        k = self.kur.konfig
        bas_s, bitis_s = k.olcum_penceresi
        sonuc = fiziksel_kopma_say(
            yayilim=self.kur.kanal.yayilim, topoloji=self.kur.topoloji,
            dugum_sayisi=self.kur.dugum_sayisi,
            sinr_esigi_db=k.sinr_esigi_db, bas_s=bas_s, bitis_s=bitis_s)
        self.kur.sayaclar.pencere_icinde_olculdu("kopma_fiziksel",
                                                 sonuc["kopma"])
        self.kur.rota_defteri.fiziksel_kopma(sonuc["kopma"])

    # ==================================================================
    # OLAYLAR
    # ==================================================================
    def _dogum(self, dogum) -> None:
        paket = self.kur.trafik.paket_kur(dogum, self.kur.paket_sayaci)
        d = self.dugumler[paket.kaynak]
        if d.kuyruga_al(paket, uretim=True):
            self.cekismeye_basla(d)

    def _beacon(self, n: int) -> None:
        t, d = self.olaylar.simdi, self.dugumler[n]
        d.komsu_temizle(t)
        if not (d.alici.gonderiyor or d.kanal_mesgul_mu(t)):
            yuk, ek_bayt = d.beacon_yuku(t)
            # 🔒 TEK KAYNAK: bedel çerçevenin boyutundan okunur. `Dugum`
            # artık ayrıca saymıyor — yoksa yük çift faturalanırdı.
            cerceve = beacon_cercevesi(self, ek_bayt)
            s = self.kur.sayaclar
            s.artir("beacon_gonderilen")
            s.artir("kontrol_cerceve")
            s.ekle("kontrol_bayt", cerceve.bayt)
            s.ekle("kontrol_airtime_s", cerceve.sure_s)
            gonder(self, n, Iletim(n, cerceve, t,
                                   self.kur.kanal.yayilim.verici_gucu_w),
                   ("beacon", yuk))
        sonraki = t + self.kur.konfig.beacon_araligi_s
        if sonraki <= self.kur.konfig.kosu_bitis_s:
            self.olaylar.ekle(sonraki, self._beacon, n)

    def _geri_cekilme_bitti(self, n: int, surum: int) -> None:
        d = self.dugumler[n]
        if surum != d.surum or d.dcf.durum != "geri_cekilme":
            return
        t = self.olaylar.simdi
        d.bekleyen_slotlari_dus(t)
        # 🔴 `ayni_an_haric=True` — aynı slotta başlayan iletim ERTELETMEZ.
        # DCF'nin birincil çarpışma mekanizması budur; gerekçesi
        # `Dugum.kanal_mesgul_mu`da ölçüsüyle birlikte yazılı.
        if d.kanal_mesgul_mu(t, ayni_an_haric=True) or d.dcf.geri_sayim > 0:
            self.geri_cekilmeyi_zamanla(d)
            return
        (kontrol.iletime_basla if kontrol.sirada_mi(d) else iletime_basla)(self, d)
        kontrol.gelenleri_uygula(self, d)

    def _difs_bitti(self, n: int, surum: int) -> None:
        d = self.dugumler[n]
        if surum == d.surum and d.dcf.durum == "geri_cekilme":
            self.geri_cekilmeyi_zamanla(d)

    def _iletim_bitti(self, n: int, iletim: Iletim, yuk) -> None:
        t, d = self.olaylar.simdi, self.dugumler[n]
        d.alici.gonderim_bitti()
        if yuk[0] == "veri":
            z = self.kur.zamanlar
            self.olaylar.ekle(t + z.sifs_s + z.onay_s + z.slot_s,
                              self._onay_penceresi, n, d.surum)
        elif yuk[0] == "kontrol":
            kontrol.iletim_bitti(self, d, yuk)
        self.kur.kanal.ortam.bitenleri_at(t - self._temizleme_s)

    def _cerceve_geldi(self, n: int, iletim: Iletim, yuk) -> None:
        yeni, ezilen = self.dugumler[n].alici.cerceve_geldi(
            iletim, self.olaylar.simdi)
        alim_say(self, yeni)
        alim_say(self, ezilen)

    def _cerceve_bitti(self, n: int, iletim: Iletim, yuk) -> None:
        d = self.dugumler[n]
        sonuc = d.alici.cerceve_bitti(iletim, self.olaylar.simdi)
        alim_say(self, sonuc)
        if sonuc is None or not sonuc.basarili:
            return
        d.alim_kaydet(iletim.cerceve.bayt)
        tip, bilgi = yuk
        if tip == "beacon":
            d.beacon_isle(iletim.gonderen, bilgi, self.olaylar.simdi)
        elif tip == "onay":
            onay_alindi(self, n, bilgi)
        elif tip == "veri":
            veri_alindi(self, d, iletim.gonderen, bilgi)
        else:
            kontrol.cerceve_alindi(self, d, iletim.gonderen, tip, bilgi)

    def _onay_penceresi(self, n: int, surum: int) -> None:
        d = self.dugumler[n]
        if surum == d.surum and d.kontrol.onay_bekleniyor:
            return kontrol.onay_zaman_asimi(self, d)
        if surum != d.surum or not d.onay_bekleniyor:
            return
        d.onay_bekle(False)
        d.iletim_sonucu("zaman_asimi")
        # 🔒 SEBEBE GÖRE AYIR. `devredildi` doğruysa alıcı çerçeveyi çözmüş
        # ve paket el değiştirmiştir; kaybolan şey ONAYDIR. Yanlışsa veri
        # hiç ulaşmamıştır. Gönderen ikisini ayırt edemez (gözlem penceresi
        # ikisine de "zaman_asimi" der) ama ÖLÇÜM ayırt edebilir ve etmelidir.
        self.kur.sayaclar.artir("mac_onaysiz_onay" if d.devredildi
                                else "mac_onaysiz_veri")
        deneme = d.dcf.deneme           # 🔒 Y1 — sayaç sıfırlanmadan önce
        if d.dcf.onay_gelmedi():
            # 🔒 Y3 · R3 — hedef, uçuştan İNDİRİLMEDEN önce okunur.
            hedef = d.ucus_hedefi
            vazgec(self, d)
            kontrol.iletim_sonucu(self, d, hedef, False, deneme, "veri")
            kontrol.iletim_basarisiz(self, d, hedef, "veri")
        else:
            self.geri_cekilmeyi_zamanla(d)

    # ==================================================================
    # ÇEKİŞME
    # ==================================================================
    def cekismeye_basla(self, d: Dugum) -> None:
        """Kuyrukta iş var ve düğüm boşta — çekişmeye gir.

        🔒 Uçuşta bir paket varken çağrılırsa hiçbir şey yapmaz: aynı anda
        iki paket uçuşta olamaz ve `Dugum.ucusa_al` bunu değişmez olarak
        denetler. Burada sessizce dönmek, çağıranların (doğum, teslim,
        vazgeçme) sıralamayı düşünmek zorunda kalmamasını sağlar.
        """
        if (d.dcf.durum != "bos" or d.ucustaki is not None
                or (d.kuyruk.bos_mu and d.kontrol.bos_mu)):
            return
        d.dcf.cerceve_hazir()
        self.geri_cekilmeyi_zamanla(d)

    def geri_cekilmeyi_zamanla(self, d: Dugum) -> None:
        """Sayacı işlet ya da dondur. Her çağrı SÜRÜMÜ artırır."""
        t = self.olaylar.simdi
        surum = d.yeni_surum()
        if d.kanal_mesgul_mu(t):
            self.olaylar.ekle(d.mesgul_bitisi_s(t) + self.kur.zamanlar.difs_s,
                              self._difs_bitti, d.kimlik, surum)
            return
        bitis = d.bitis_ani_s(t)
        d.bekleme_baslat(t, bitis)
        self.olaylar.ekle(bitis, self._geri_cekilme_bitti, d.kimlik, surum)

    def dondur(self, d: Dugum, t_s: float) -> None:
        """Duyulan bir iletim başladı — sayaç DONAR (802.11'in kuralı).

        🔴 TAAHHÜTLÜ düğüm dondurulmaz: geri çekilmesi bu ana kadar zaten
        bitmiştir ve göndermek üzeredir. Dondurulsaydı, aynı slotta biten iki
        geri çekilmeden ikincisi hiç gönderemez ve çarpışma yok olurdu.
        """
        if d.dcf.durum == "geri_cekilme" and not d.taahhutlu_mu(t_s):
            d.bekleyen_slotlari_dus(t_s)
            self.geri_cekilmeyi_zamanla(d)
