"""
Korunum defteri.

    üretilen = teslim + düşen + kuyrukta + uçuşta

Her koşuda otomatik kontrol edilir. Tutmayan koşunun sonucu **geçersiz**
işaretlenir ve analize girmez.

🔒 DEFTER TEK GEÇİŞ NOKTASIDIR
==============================
Paket durumu doğrudan değiştirilemez; yalnızca bu sınıfın metotlarıyla.
Böylece bir geçişi *"unutmak"* mümkün değildir: sayaç negatife düşerse **anında**
patlar, koşu sonuna kalmaz. Sessiz paket kaybı bu alanın en zor bulunan hata
sınıfıdır ve tek yapısal panzehiri budur.

🔒 KAPSAM — defter TÜM KOŞU, metrikler PENCERE
==============================================
Defter [0, koşu_bitişi] üzerinden tutulur; metrikler yalnız ölçüm penceresinden
hesaplanır. İkisi **ayrı defterdir**: ısınmada üretilip pencerede teslim edilen
bir paket, pencereye sıkıştırılmış bir korunum denklemini kırar ve her koşuda
sahte alarm üretirdi. Sahte alarma alışan bir proje gerçek alarmı kaçırır.

⚠️ NE DEMEZ — ve bu ölçülerek bulundu
=====================================
Denklemin tutması *"hiçbir paket kaybolmuyor"* **demez**. İki ayrı kör nokta
var ve ikisinin de ayrı bir kontrolü olmak zorunda:

  1. Bir geçişin kendisi silinirse (paket "uçuşta" asılı kalırsa) eşitlik yine
     tutar. Onu yakalayan şey koşu sonundaki **boşalma kontrolüdür**:
     `ucusta` ve `kuyrukta` boşalma penceresinden sonra sıfıra yakın olmalı.
  2. 🔴 Defterin MODELİ gerçekten ayrışabilir. Dolu kuyruk paketi reddeder,
     çağıran `dus(...)` yapmayı unutur — defter hâlâ "kuyrukta" der ve denklem
     TUTAR (`5 = 0 + 0 + 5 + 0`). Paket sessizce yok olmuştur.
     Onu yakalayan şey `mutabakat()`tır: defterin sayaçları fiilen
     kuyruklarda ve havada olan paket sayısına eşit olmak zorundadır.

Bu ikincisi, denklemi kırmaya çalışan bir test denklemi KIRAMAYINCA bulundu.
"""

from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ["DUSME_SEBEPLERI", "KorunumHatasi", "KorunumDefteri"]


# Kapalı küme: "diğer" diye bir sebep yoktur. Sebebi bilinmeyen bir düşüş,
# teşhis edilmemiş bir hatadır.
#
# 🔴 `rota_gecersiz` BAŞTAN BURADA (sim2'de eklendi):
# Δ (rota kurtarma gecikmesi), COR ve üç kopma sayacı, protokolün *"rotam
# koptu"* diyebilmesini gerektiriyor — ve o beyan bir paketi düşürebilir.
# Sebep listesi bir ŞEMA taahhüdüdür: sonradan eklemek eski satırları
# karşılaştırılamaz yapar. Bu yüzden protokoller yazılmadan ÖNCE burada.
DUSME_SEBEPLERI: tuple[str, ...] = (
    "kuyruk_tasmasi",     # varış kuyruğu dolu
    "ttl",                # TTL tükendi (muhtemelen döngü)
    "iletim_basarisiz",   # yeniden deneme hakkı bitti
    "hedef_yok",          # sonraki atlama seçilemedi
    "rota_gecersiz",      # protokol rotayı geçersiz ilan etti
    # 🔒 ROTA BEKLEME TAMPONUNUN TAVANI AŞILDI — 16 Eylül 2026 (K-131).
    # `Karar.beklet` paketi düşürmez, düğümün tamponuna koyar. Tamponun İKİ
    # tavanı vardır (paket sayısı ve süre) ve aşım SESSİZ DEĞİLDİR: ayrı bir
    # sebeple deftere yazılır. Sebep listesi bir ŞEMA TAAHHÜDÜDÜR — sonradan
    # eklemek eski satırları karşılaştırılamaz yapar; `rota_gecersiz` de tam
    # bu yüzden protokoller yazılmadan ÖNCE eklenmişti, bu da öyle.
    "tampon_asimi",
    # 🔒 PROTOKOL POLİTİKASI GEREĞİ DÜŞTÜ — 25 Eylül 2026 (`v2/15` A1, K-171).
    # Rota YOK değil, protokol bu paketi BİLEREK taşımıyor (DESPARETE v0.1
    # tek-sink profili geçit dışı hedefe giden komutu taşımaz — K-160 §10 C).
    # `hedef_yok`a karışsaydı "rota bulunamadı" ile "tasarım gereği
    # taşınmadı" aynı sayıda toplanır ve iki kol arasındaki fark yanlış
    # okunurdu. Protokol bunu `Beyan("politika")` ile söyler.
    "politika",
    # 🔒 DÜĞÜM KAYBI — `v2/15` C1 (K-180): telsiz kapandı, kuyruk, tampon ve
    # uçuştaki (el değiştirmemiş) paket düştü.
    "dugum_kaybi",
)

_NEREDEN = ("kuyruk", "ucus")


class KorunumHatasi(RuntimeError):
    """Bir sayaç negatife düştü ya da bilinmeyen bir geçiş istendi."""


@dataclass
class KorunumDefteri:
    uretilen: int = 0
    teslim: int = 0
    kuyrukta: int = 0
    ucusta: int = 0
    # D-23 · K-231 — uçtan uca kopya: üretilen eş · hedefte bastırılan eş.
    # Kopya yoksa ikisi 0 kalır ve rapora girmez (satır birebir).
    kopya_uretilen: int = 0
    kopya_bastirilan: int = 0
    dusen: dict[str, int] = field(
        default_factory=lambda: {s: 0 for s in DUSME_SEBEPLERI})

    # -------------------------------------------------------------- geçişler
    def uret(self, adet: int = 1) -> None:
        """Kaynak düğüm paket üretti → kendi kuyruğuna girdi."""
        self.uretilen += adet
        self.kuyrukta += adet

    def kuyruktan_al(self, adet: int = 1) -> None:
        """Paket kuyruktan alındı, iletiliyor."""
        self.kuyrukta -= adet
        self.ucusta += adet
        self._dogrula_negatif()

    def ucustan_kuyruga(self, adet: int = 1) -> None:
        """İletim başarılı; paket sonraki düğümün kuyruğuna geçti."""
        self.ucusta -= adet
        self.kuyrukta += adet
        self._dogrula_negatif()

    def teslim_et(self, adet: int = 1) -> None:
        """Paket nihai hedefine ulaştı."""
        self.ucusta -= adet
        self.teslim += adet
        self._dogrula_negatif()

    def kopya_uret(self, adet: int = 1) -> None:
        """Protokol gönderilen paketin eşini istedi → eş, düğümün kuyruğuna
        girdi (D-23 · K-231). Eş bundan sonra asıl paketle aynı geçişlerden
        geçer; düşerse `dus`, hedefe ilk o varırsa `teslim_et`."""
        self.kopya_uretilen += adet
        self.kuyrukta += adet

    def kopya_bastir(self, adet: int = 1) -> None:
        """Eş hedefe vardı ama paket zaten teslim edilmişti → havadan
        çıkar, ikinci kez TESLİM SAYILMAZ (D-23 · K-231)."""
        self.ucusta -= adet
        self.kopya_bastirilan += adet
        self._dogrula_negatif()

    def dus(self, sebep: str, nereden: str, adet: int = 1) -> None:
        """Paket düştü.

        🔒 `nereden` açıkça sorulur ve **varsayılanı yoktur**: paketin hangi
        havuzdan çıktığı bilinmeden denklem tutmaz, ve bir varsayılan değer
        çağıranın düşünmediği anlamına gelir.
        """
        if sebep not in self.dusen:
            raise KorunumHatasi(
                f"bilinmeyen düşme sebebi: {sebep!r}. Sebepler kapalı bir "
                f"kümedir; yeni sebep DUSME_SEBEPLERI'ne eklenmelidir — ve bu "
                f"bir şema değişikliğidir.")
        if nereden == "kuyruk":
            self.kuyrukta -= adet
        elif nereden == "ucus":
            self.ucusta -= adet
        else:
            raise KorunumHatasi(
                f"nereden {_NEREDEN} içinden olmalı: {nereden!r}")
        self.dusen[sebep] += adet
        self._dogrula_negatif()

    # --------------------------------------------------------------- kontrol
    @property
    def dusen_toplam(self) -> int:
        return sum(self.dusen.values())

    def denklem_tutuyor_mu(self) -> bool:
        # D-23 · K-231: kopya yoksa iki terim 0'dır — denklem eskisinin aynısı.
        return (self.uretilen + self.kopya_uretilen
                == self.teslim + self.kopya_bastirilan + self.dusen_toplam
                + self.kuyrukta + self.ucusta)

    def kontrol(self) -> dict[str, object]:
        """Sonuç satırına yazılacak korunum raporu.

        🔒 **İstisna fırlatmaz.** Koşu bitiminde çağrılır; tutmuyorsa satır
        `korunum_tamam=False` ile işaretlenir ve analiz o satırı **dışlar**.
        Böylece bozuk bir koşu sessizce ortalamaya karışmaz.
        """
        sag = (self.teslim + self.kopya_bastirilan + self.dusen_toplam
               + self.kuyrukta + self.ucusta)
        sol = self.uretilen + self.kopya_uretilen
        rapor = {
            "korunum_tamam": sol == sag,
            "uretilen": self.uretilen,
            "teslim": self.teslim,
            "dusen_toplam": self.dusen_toplam,
            "dusen": dict(self.dusen),
            "kuyrukta": self.kuyrukta,
            "ucusta": self.ucusta,
            "fark": sol - sag,
        }
        # 🔒 D-23 · K-231: kopya kullanılmadıysa alan EKLENMEZ — kopya
        # istemeyen protokolün satırı birebir aynı kalır. Kopya varsa
        # `dusen_toplam` EŞ düzeyindedir (eşi teslim edilmiş paketin düşen
        # eşi de sayılır); paket düzeyi PDR paket defterindedir.
        if self.kopya_uretilen:
            rapor["kopya_uretilen"] = self.kopya_uretilen
            rapor["kopya_bastirilan"] = self.kopya_bastirilan
        return rapor

    # ------------------------------------------------------------ mutabakat
    def mutabakat(self, kuyrukta_gercek: int, ucusta_gercek: int
                  ) -> dict[str, object]:
        """🔴 DEFTERİN MODELİNİ GERÇEKLE KARŞILAŞTIRIR.

        Bu metot 4 Eylül 2026'da, denklemi KIRMAYA çalışan bir test denklemi
        kıramayınca eklendi. Ölçülen kör nokta şudur:

            kuyruk dolu → `Kuyruk.ekle` paketi REDDEDİYOR
            çağıran `dus(...)` yapmayı unutuyor
            defter hâlâ "kuyrukta 5" diyor  →  denklem TUTUYOR (5 = 0+0+5+0)

        Yani paket sessizce yok oldu ve korunum denklemi bunu **görmedi**.
        Görmemesi bir hata değil, tanımının sınırı: denklem defterin KENDİ
        geçişlerinin tutarlılığını ölçer, defterin gerçeği doğru modelleyip
        modellemediğini değil.

        🔒 Onu ölçen şey budur: defterin `kuyrukta`/`ucusta` sayaçları, fiilen
        kuyruklarda ve havada olan paket sayısına EŞİT olmalı. Koşu sonunda
        çağrılır ve sonuç satırına yazılır.

        ⚠️ `kontrol()` gibi bu da **istisna fırlatmaz**: bozuk koşu
        işaretlenir, analiz onu dışlar.
        """
        return {
            "mutabakat_tamam": (self.kuyrukta == kuyrukta_gercek
                                and self.ucusta == ucusta_gercek),
            "kuyrukta_defter": self.kuyrukta,
            "kuyrukta_gercek": kuyrukta_gercek,
            "ucusta_defter": self.ucusta,
            "ucusta_gercek": ucusta_gercek,
            "kuyruk_farki": self.kuyrukta - kuyrukta_gercek,
            "ucus_farki": self.ucusta - ucusta_gercek,
        }

    # ----------------------------------------------------------------- içsel
    def _dogrula_negatif(self) -> None:
        if self.kuyrukta < 0 or self.ucusta < 0 or self.teslim < 0:
            raise KorunumHatasi(
                f"sayaç negatife düştü: kuyrukta={self.kuyrukta} "
                f"ucusta={self.ucusta} teslim={self.teslim}")
