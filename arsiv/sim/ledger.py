"""
Korunum defteri.

    üretilen = teslim + düşen + kuyrukta + uçuşta

Bu eşitlik HER KOŞUDA otomatik kontrol edilir. Tutmayan koşunun sonucu
geçersiz işaretlenir ve analize girmez. (06-ON-KAYIT.md, Aile 0 / K1)

NEDEN BU KADAR ERKEN YAZILIYOR
-------------------------------
Sessiz paket kaybı bu alanın en zor bulunan hata sınıfıdır. Radyo ve MAC
katmanları bu defter olmadan yazılsaydı, kaybolan paketleri haftalar sonra
fark ederdik — ve o zamana kadar üretilmiş her sayı şüpheli olurdu.

TASARIM KARARI: DEFTER TEK GEÇİŞ NOKTASIDIR
--------------------------------------------
Paket durumu doğrudan değiştirilemez; yalnızca bu sınıfın metotlarıyla
değiştirilir. Böylece bir geçişi "unutmak" mümkün değildir: sayaçlar
negatife düşerse hemen patlar, sona kalmaz.

KAPSAM
------
Defter TÜM KOŞU üzerinden tutulur (0 → koşu bitişi).
Metrikler ise yalnızca ÖLÇÜM PENCERESİ üzerinden hesaplanır.
İkisi ayrı defterdir — ısınmada üretilip pencerede teslim edilen bir paket,
pencereye sıkıştırılmış bir korunum denklemini kırardı ve her koşuda sahte
alarm üretirdi. Sahte alarma alışan bir proje, gerçek alarmı kaçırır.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# Düşme sebepleri kapalı bir kümedir: "diğer" diye bir sebep yoktur.
# Sebebi bilinmeyen bir düşüş, teşhis edilmemiş bir hatadır.
DUSME_SEBEPLERI = (
    "kuyruk_tasmasi",     # varış kuyruğu dolu
    "ttl",                # TTL tükendi (muhtemelen döngü)
    "iletim_basarisiz",   # yeniden deneme hakkı bitti
    "hedef_yok",          # sonraki atlama seçilemedi
)


class KorunumHatasi(RuntimeError):
    """Bir sayaç negatife düştü ya da denklem tutmadı."""


@dataclass
class KorunumDefteri:
    uretilen: int = 0
    teslim: int = 0
    kuyrukta: int = 0
    ucusta: int = 0
    dusen: dict[str, int] = field(
        default_factory=lambda: {s: 0 for s in DUSME_SEBEPLERI}
    )

    # ------------------------------------------------------------- geçişler
    def uret(self, adet: int = 1) -> None:
        """Kaynak düğüm bir paket üretti → kaynağın kuyruğuna girdi."""
        self.uretilen += adet
        self.kuyrukta += adet

    def kuyruktan_al(self, adet: int = 1) -> None:
        """Paket kuyruktan alındı, iletiliyor."""
        self.kuyrukta -= adet
        self.ucusta += adet
        self._dogrula_negatif()

    def ucustan_kuyruga(self, adet: int = 1) -> None:
        """İletim başarılı, paket bir sonraki düğümün kuyruğuna geçti."""
        self.ucusta -= adet
        self.kuyrukta += adet
        self._dogrula_negatif()

    def teslim_et(self, adet: int = 1) -> None:
        """Paket nihai hedefine ulaştı."""
        self.ucusta -= adet
        self.teslim += adet
        self._dogrula_negatif()

    def dus(self, sebep: str, nereden: str, adet: int = 1) -> None:
        """Paket düştü.

        `nereden` açıkça sorulur ("kuyruk" | "ucus") çünkü paketin hangi
        havuzdan çıktığı bilinmeden korunum denklemi tutmaz. Varsayılan
        değer bilerek yoktur: varsayılan bir değer, çağıran tarafın
        düşünmediği anlamına gelir.
        """
        if sebep not in self.dusen:
            raise KorunumHatasi(
                f"bilinmeyen düşme sebebi: {sebep!r}. Sebepler kapalı bir "
                f"kümedir; yeni sebep DUSME_SEBEPLERI'ne eklenmelidir."
            )
        if nereden == "kuyruk":
            self.kuyrukta -= adet
        elif nereden == "ucus":
            self.ucusta -= adet
        else:
            raise KorunumHatasi(f"nereden 'kuyruk' veya 'ucus' olmalı: {nereden!r}")
        self.dusen[sebep] += adet
        self._dogrula_negatif()

    # --------------------------------------------------------------- kontrol
    @property
    def dusen_toplam(self) -> int:
        return sum(self.dusen.values())

    def denklem_tutuyor_mu(self) -> bool:
        sol = self.uretilen
        sag = self.teslim + self.dusen_toplam + self.kuyrukta + self.ucusta
        return sol == sag

    def kontrol(self) -> dict[str, object]:
        """Sonuç satırına yazılacak korunum raporu.

        İstisna fırlatmaz — koşu bitiminde çağrılır ve sonucu satıra yazılır.
        Tutmuyorsa satır `korunum_tamam=False` ile işaretlenir ve analiz o
        satırı DIŞLAR. Böylece bozuk bir koşu sessizce ortalamaya karışmaz.
        """
        sag = self.teslim + self.dusen_toplam + self.kuyrukta + self.ucusta
        return {
            "korunum_tamam": self.uretilen == sag,
            "uretilen": self.uretilen,
            "teslim": self.teslim,
            "dusen_toplam": self.dusen_toplam,
            "dusen": dict(self.dusen),
            "kuyrukta": self.kuyrukta,
            "ucusta": self.ucusta,
            "fark": self.uretilen - sag,
        }

    # ----------------------------------------------------------------- içsel
    def _dogrula_negatif(self) -> None:
        if self.kuyrukta < 0 or self.ucusta < 0 or self.teslim < 0:
            raise KorunumHatasi(
                f"sayaç negatife düştü: kuyrukta={self.kuyrukta} "
                f"ucusta={self.ucusta} teslim={self.teslim}"
            )
