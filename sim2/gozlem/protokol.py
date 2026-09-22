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

🔴 KANCALAR ARTIK GÖZLEM ALIYOR — 16 Eylül 2026 (denetim B4, `04` K-131)
========================================================================
Gözlem penceresi TEK BİR YERDE üretiliyordu: veri gönderme kararı. Kontrol
düzleminin beş kancasının hiçbiri ve `beacon_yuku` gözlem almıyordu. Üç
sonucu vardı ve üçü de Aşama 3'ün tasarım uzayını farkında olmadan
daraltıyordu:

  · Protokol KENDİ ÖLÇTÜĞÜ gürültüyü beacon'a koyamıyordu — koyarken
    ölçemiyordu.
  · Zamanlayıcıyla gürültü örnekleyemiyordu.
  · `kanal_mesgul_mu` yapısal olarak neredeyse SABİTTİ: ölçüldü, 24 558 karar
    anının yalnız **%2,17**'sinde `True`. Çünkü gözlem tam da düğümün geri
    çekilmesi bitip kanalı BOŞ BULDUĞU anda üretiliyordu; alan protokole hep
    *"kanal boş"* diyordu.

`05` §6 karıştırma sezimi için gereken alanları sayıyor: ölçülen gürültü, son
iletim sonucu, kanal meşguliyeti, duyulan beacon, son duyulma anı, kuyruk
uzunluğu. İkisi bu yüzden kullanılamaz durumdaydı.

🔒 YÜZEY BÜYÜMEDİ, yalnız NE ZAMAN sunulduğu değişti. `Gozlem` zaten düğüm
kimliğini ve yerel saati taşıyor, yani kancalardan hiçbir bilgi EKSİLMEDİ —
donanım ölçümleri eklendi. Bu çağrılarda `Gozlem.paket` `None`dur: elde
taşınan bir paket yoktur.

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
from sim2.gozlem.pencere import Gozlem

__all__ = ["Protokol", "KontrolluProtokol", "SonucBildirimliProtokol",
           "KANCALAR"]

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
        ölçtüğü gürültüyü ya da kuyruk doluluğunu beacon'a koyabilsin —
        16 Eylül 2026'ya kadar koyarken ölçemiyordu.
        """
        ...

    def beacon_alindi(self, gozlem: Gozlem, komsu: int,
                      yuk: tuple[tuple[str, object], ...]) -> None:
        """Komşudan beacon geldi. `yuk` DONMUŞ bir demettir.

        `gozlem.saat_s` ALICININ kendi saatidir. Gönderenin saati, ancak
        gönderen onu `beacon_yuku`na koyup bedelini ödediyse gelir — ve o
        zaman da ofsetle sapmayı içerir.

        🔒 GÖZLEM ALIR — 16 Eylül 2026 (öğrenci kararı, K-131). Bu, protokolün
        gördüğü EN SIK dış olaydır ve `05` §6 karıştırma sezimi için gereken
        alanlar arasında *"duyulan beacon"* ile *"ölçülen gürültü"*yü BİRLİKTE
        sayar. Eski imzayla protokol beacon'ı alırken kendi gürültüsünü
        ölçemiyordu; ikisini yan yana koymak tam da sezimin istediği şeydi.

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

        🔒 `gozlem.saat_s` düğümün KENDİ saatidir ve `gozlem.dugum` kimliğidir;
        eski imzanın verdiği her şey duruyor (16 Eylül 2026, K-131).
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


# 🔒 VERİ BAŞLIĞI — Y2, 22 Eylül 2026 (K-151). Protokol sınıfı isteğe bağlı
# `veri_baslik_bayt: int` özniteliğiyle her veri paketine eklediği yönlendirme
# başlığının boyunu bildirir (yoksa 0). Simülatör veri çerçevesini o kadar
# uzatır ve baytı yönlendirme ek yüküne sayar. AODV, OLSR ve AOMDV veri
# paketine ayrı bir yönlendirme başlığı eklemez: 0.
