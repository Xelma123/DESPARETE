"""
Protokol arayüzü — simülatörün protokolden gördüğü TEK yüzey.

🔒 KATMAN KURALI
================
`protokoller/` paketi `sim2/` DIŞINDADIR ve yalnız `gozlem/`i görür.
Bir protokol `kanal/`, `dunya/`, `olcum/` ya da `Konfig`e ulaşamaz; ulaşmaya
çalışırsa içe aktarma grafiği testi konuşur. Kâhin bilginin protokole
sızmasının yapısal panzehiri budur — disiplin değil, grafik.

🔒 DÖRT KANCA, HER BİRİ AYRI SÖZLEŞMELİ
=======================================
    sonraki_atlama(gozlem) -> Karar      kararın kendisi
    beacon_yuku(gozlem)    -> dict       BAYT bedeli ödenerek taşınan bilgi
    beacon_alindi(...)                   komşudan gelen yükün işlenmesi
    teshis(dugum)          -> dict       yalnız sonuç satırına, karara GİRMEZ

🔒 HER KANCA GÖZLEM ALIR (K-131, denetim B4)
============================================
Gözlem yalnız veri gönderme kararında üretilseydi protokol kendi ölçtüğü
gürültüyü beacon'a koyamaz, zamanlayıcıyla örnekleyemez ve
`kanal_mesgul_mu`yu hep "boş" görürdü (gözlem, kanal boş bulunduğu anda
üretiliyordu). `05` §6'nın karıştırma sezimi için saydığı alanlar bu
yüzden her kancada sunulur. Yüzey büyümedi, yalnız sunulma anı değişti;
bu çağrılarda `Gozlem.paket` `None`dur.

`beacon_yuku` ve `teshis` ikisi de sözleşme denetiminden geçer (`yuk.py` ve
`teshis.py`): tip, boyut ve NaN reddi. Eski depoda `teshis`in sözleşmesi
YOKTU ve sekiz sözleşme dışı yükün sekizi de kabul edilmişti; dördü sonuç
yazıcısını koşu bittikten SONRA düşürdü.

⚠️ VARSAYILAN GERÇEKLEMELER YOK
===============================
Kancaların varsayılan bir gövdesi yoktur. Olsaydı, kancayı yazmayı unutan
bir protokol sessizce "beacon'a hiçbir şey koymayan" bir protokol olurdu ve
bu bir tasarım kararı gibi görünürdü. `Protokol` bir `Protocol` tipidir:
eksik kanca, çağrı anında `AttributeError` verir.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from sim2.gozlem.karar import Karar
from sim2.gozlem.pencere import Gozlem, PaketGorunumu

__all__ = ["Protokol", "KontrolluProtokol", "SonucBildirimliProtokol",
           "DuyanProtokol", "DUYULAN_TURLER", "KANCALAR"]

KANCALAR: tuple[str, ...] = (
    "sonraki_atlama", "beacon_yuku", "beacon_alindi", "teshis",
)


@runtime_checkable
class Protokol(Protocol):
    """Bir yönlendirme protokolünün simülatöre gösterdiği yüzey."""

    ad: str

    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        """Bu paket şimdi kime gönderilsin?

        🔒 Dönüş tipi `Karar`dır, `int | None` değil: protokolün *"rotam
        koptu"* diyebilmesi Δ, COR ve üç kopma sayacının ön koşulu.
        """
        ...

    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        """Beacon'a konacak alanlar. Her biri BAYT bedeli öder.

        Komşusunun girişim seviyesini ya da kuyruk durumunu kullanmak isteyen
        protokol, o alanları buraya koymak ve bedelini ödemek zorundadır.

        🔒 `gozlem.paket` `None`dur. Gözlem burada verilir ki protokol KENDİ
        ölçtüğü gürültüyü ya da kuyruk doluluğunu beacon'a koyabilsin.
        """
        ...

    def beacon_alindi(self, gozlem: Gozlem, komsu: int,
                      yuk: tuple[tuple[str, object], ...]) -> None:
        """Komşudan beacon geldi. `yuk` DONMUŞ bir demettir.

        `gozlem.saat_s` ALICININ kendi saatidir. Gönderenin saati, ancak
        gönderen onu `beacon_yuku`na koyup bedelini ödediyse gelir — ve o
        zaman da ofsetle sapmayı içerir.

        🔒 GÖZLEM ALIR (K-131): protokolün en sık dış olayı; "duyulan
        beacon" ile "ölçülen gürültü" sezim için yan yana gelir (`05` §6).

        ⚠️ Bu kanca bir şey DÖNDÜREMEZ (niyet üretmez, yalnız kaydeder) —
        yani gözlem burada EYLEME değil, yalnız protokolün kendi geçmişine
        (`05` §3.4) girer.
        """
        ...

    def teshis(self, dugum: int) -> dict:
        """Sonuç satırına yazılacak teşhis sayaçları.

        🔴 Buradan dönen hiçbir şey karara giremez; yalnız rapora gider.
        Sözleşmesi `teshis.py`de denetlenir.
        """
        ...


@runtime_checkable
class KontrolluProtokol(Protokol, Protocol):
    """Kontrol düzlemini kullanan protokol — K-112, `v2/13-KONTROL-DUZLEMI.md`.

    🔒 Beş kancanın HEPSİ ya da HİÇBİRİ (`gozlem/kontrol.py::KONTROL_KANCALARI`).
    Hepsini taşımayan bir protokol `Karar.niyetler` dolduramaz; kısmi taşıyan
    kurulumda reddedilir. Her kanca bir NİYET DEMETİ döndürür (boşsa `()`).
    """

    def zamanlayicilar(self) -> dict:
        """PERİYODİK zamanlayıcıların ilanı `{etiket: periyot_s}` — BİR KEZ."""
        ...

    def zamanlayici_doldu(self, gozlem: Gozlem, etiket: str) -> tuple:
        """İlan edilmiş periyodik zamanlayıcı doldu.

        🔒 `gozlem.saat_s` düğümün KENDİ saatidir ve `gozlem.dugum` kimliğidir.
        """
        ...

    def uyandi(self, gozlem: Gozlem, etiket: str) -> tuple:
        """Bir `Uyandirma` niyeti doldu (DİNAMİK zamanlayıcı)."""
        ...

    def kontrol_alindi(self, gozlem: Gozlem, gonderen: int, bicim: str,
                       yuk: tuple[tuple[str, object], ...],
                       yayin: bool) -> tuple:
        """🔒 YALNIZ BAŞARILI TESLİMDE çağrılır (sözleşme kararı 4).

        Yayında her başarılı alıcı için AYRI çağrılır; unicast'ta yalnız
        hedefte. Çözülemeyen, çarpışan ya da başkasına adreslenmiş çerçeve
        bu kancaya HİÇ gelmez.
        """
        ...

    def iletim_basarisiz(self, gozlem: Gozlem, hedef: int | None,
                         tur: str) -> tuple:
        """MAC bir UNICAST çerçeveden VAZGEÇTİ — bağ kopması geri bildirimi.

        🔒 Y3 · R3. `tur` "veri" ya da "kontrol"; `hedef` gönderenin denediği
        komşudur. Gönderenin KENDİ MAC'inin bildiği bir olaydır (`05` §3.1
        zaman aşımı), yeni bir kâhin bilgisi değil. Başarıyı ve tekrar
        sayısını isteyen protokol `SonucBildirimliProtokol`ü de taşır
        (22 Eylül 2026, K-151).
        """
        ...


@runtime_checkable
class SonucBildirimliProtokol(Protokol, Protocol):
    """Her unicast sonucunu isteyen protokol — Y1, 22 Eylül 2026 (K-151).

    🔴 NEDEN: `son_iletim_sonucu` yalnız EN SON sonucu taşır ve iki gözlem
    arasında kaç iletim olduğunu söylemez; aynı "onay" iki gözlemde görünürse
    bir mi iki mi başarı olduğu ayırt edilemez. Kaliteyi yakın geçmişin
    sonuçlarından ve tekrar sayısından hesaplayan bir protokol (DESPARETE'nin
    M0.1 profili) bu yüzden gerçeklenemiyordu.

    🔒 Bilgi GÖNDERENİN KENDİ MAC'inindir (`05` §3.1): kaç kez denediğini ve
    onay alıp almadığını bilir; gerçek radyolar bunu raporlar. Kâhin bilgisi
    değildir, gözlem yüzeyi BÜYÜMEZ (`Gozlem` alanları aynı).

    🔒 İSTEĞE BAĞLIDIR ve kontrol kancalarının hepsi-ya-hiç kuralına girmez:
    taşımayan protokol hiç çağrılmaz ve sonuçları birebir aynı kalır.
    """

    def iletim_sonucu(self, gozlem: Gozlem, hedef: int, basarili: bool,
                      tekrar: int, tur: str) -> None:
        """Bir unicast çerçevenin sonucu kesinleşti.

        `hedef` denenen komşu · `basarili` onay geldi mi · `tekrar` ilk
        denemeden SONRAKİ yeniden iletim sayısı (ilk denemede başarı → 0;
        vazgeçmede yeniden deneme sınırı) · `tur` "veri" ya da "kontrol".

        🔒 NİYET DÖNDÜRMEZ — yalnız protokolün kendi geçmişine girer.
        Başarısızlıkta `iletim_basarisiz`den ÖNCE çağrılır: protokolün ölçümü
        onarım kararından önce güncellenmiş olur.
        """
        ...


# 🔒 DUYULAN ÇERÇEVE TÜRLERİ — `cerceve_duyuldu`nun `tur` argümanı. Kapalı
# küme: `konay` kontrol çerçevesinin onayıdır, `onay` veri çerçevesininki.
DUYULAN_TURLER: tuple[str, ...] = ("veri", "onay", "beacon", "kontrol",
                                   "konay")


@runtime_checkable
class DuyanProtokol(Protokol, Protocol):
    """Çözülen HER çerçeveyi isteyen protokol — `v2/15` B1 (K-170 onayı).

    🔴 NEDEN: protokol yalnız kendisine teslim edilen kontrol mesajını ve
    elindeki paketi görüyordu. Gerçek bir telsiz ise çözdüğü her çerçevenin
    başlığını (gönderen adresi dâhil) ve alınan gücünü (RSSI) sürücüye
    raporlar; kulak misafiri dinleme ve "bu paket bana hangi komşudan geldi"
    bilgisi buradan gelir. Paketin geldiği komşuyu bilmeden bir kaynağa geri
    yol öğrenilemez — geçitten çıkan komut bu yüzden taşınamıyordu (K-171
    bulgusu).

    🔒 İSTEĞE BAĞLIDIR ve hepsi-ya-hiç kuralına girmez: taşımayan protokol
    hiç çağrılmaz ve satırı birebir aynı kalır.
    """

    def cerceve_duyuldu(self, gozlem: Gozlem, gonderen: int, tur: str,
                        hedef: int | None, rssi_dbm: int,
                        paket: PaketGorunumu | None) -> None:
        """Bu düğüm bir çerçeveyi BAŞARIYLA çözdü — bana ya da başkasına.

        `gonderen` çerçeveyi gönderen komşu (802.11 başlığındaki verici
        adresi) · `tur` `DUYULAN_TURLER`den · `hedef` çerçevenin adreslendiği
        düğüm (yayında `None`; onayda onaylanan göndericidir) · `rssi_dbm`
        telsizin raporladığı alınan güç, ölçüm hatasıyla, tamsayı dBm ·
        `paket` yalnız veri çerçevesinde başlık görünümü.

        🔒 NİYET DÖNDÜRMEZ. Çerçevenin işlenmesinden (teslim, onay, kontrol
        kancası) ÖNCE çağrılır: sürücü çerçeveyi raporlar, sonra üst katman
        işler. `gozlem.paket` `None`dur — duyulan paket elde taşınan paket
        değildir. Karıştırıcı çerçeveleri bu kancaya GELMEZ; yalnız
        düğümlerin çözülen çerçeveleri gelir (sızıntı yok).
        """
        ...


# 🔒 KANAL DOLULUĞU — `v2/15` B3 (K-179). Protokol sınıfı isteğe bağlı
# `kanal_dolulugu_ister: bool` özniteliğiyle `Gozlem.mesgul_sure_s`i ister
# (yoksa `None` — ölçülmedi). Olay başına maliyeti yalnız isteyen öder.

# 🔒 VERİ BAŞLIĞI — Y2, 22 Eylül 2026 (K-151). Protokol sınıfı isteğe bağlı
# `veri_baslik_bayt: int` özniteliğiyle her veri paketine eklediği yönlendirme
# başlığının boyunu bildirir (yoksa 0). Simülatör veri çerçevesini o kadar
# uzatır ve baytı yönlendirme ek yüküne sayar. AODV, OLSR ve AOMDV veri
# paketine ayrı bir yönlendirme başlığı eklemez: 0.
