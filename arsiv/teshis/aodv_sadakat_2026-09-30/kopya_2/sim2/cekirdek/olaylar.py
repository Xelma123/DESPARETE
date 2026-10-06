"""
Olay kuyruğu — kesikli olay simülasyonunun kalbi.

Gerçek zaman yok, kare yok, sabit adım yok. Yalnızca olaylar: *"12,483.
saniyede şu olacak."* En erken olay çıkarılır, çalıştırılır, doğurduğu yeni
olaylar kuyruğa eklenir.

🔒 BELİRLENİMCİLİK — kuyruk anahtarı `(zaman, sıra_no)`
=======================================================
Aynı tohum birebir aynı sonucu vermek zorunda. Bunu bozabilecek tek şey, aynı
ana denk gelen iki olayın sırasının belirsiz olmasıdır. `sıra_no` monoton artan
bir sayaçtır: eşit zamanlı olaylar **eklenme sırasına** göre koşar. Keyfî ama
belirlenimci bir kural.

⚠️ **Olay nesneleri ASLA karşılaştırılmaz.** Karşılaştırılsaydı iki olayın
sırası bellek adresine bağlanırdı — sessiz bir belirlenimsizlik kaynağı. Bu
yüzden yığın elemanı bir demettir ve `heapq` üçüncü alana asla bakmaz.

🔒 `kostur()` YENİDEN BAŞLATILABİLİR
====================================
Ölçüm penceresi üç ayrı çağrıyla işlenir (ısınma → pencere → boşalma) ve bu
üç çağrı, tek bir çağrıyla **birebir aynı** sonucu vermek zorundadır. Sonda
`simdi = bitis_s` koşulsuz atanır: kuyruk erken boşalsa bile bütün kollar
aynı ana denk gelsin.
"""

from __future__ import annotations

import heapq
from typing import Any, Callable

from sim2.cekirdek.degismezler import dogrula

__all__ = ["GecmisZamanHatasi", "OlayKuyrugu"]


class GecmisZamanHatasi(RuntimeError):
    """Şimdiki zamandan önceye olay eklenmeye çalışıldı."""


class OlayKuyrugu:
    __slots__ = ("_yigin", "_sira", "simdi", "islenen_olay")

    def __init__(self) -> None:
        self._yigin: list[tuple[float, int, Callable[..., Any], tuple]] = []
        self._sira: int = 0
        self.simdi: float = 0.0
        self.islenen_olay: int = 0

    # ------------------------------------------------------------------ ekle
    def ekle(self, zaman: float, geri_cagri: Callable[..., Any],
             *args: Any) -> None:
        """Belirtilen anda çalışacak bir olay ekler.

        Geçmişe olay eklemek **sessizce yutulmaz**. Sebep: geçmişe eklenen bir
        olay ya hiç çalışmaz ya yanlış sırada çalışır; ikisi de haftalar sonra
        *"bu paket neden kaybolmuş"* diye aranır.
        """
        if zaman < self.simdi:
            raise GecmisZamanHatasi(
                f"geçmişe olay eklenemez: t={zaman!r} < şimdi={self.simdi!r}")
        heapq.heappush(self._yigin, (zaman, self._sira, geri_cagri, args))
        self._sira += 1

    def gecikmeyle_ekle(self, gecikme: float, geri_cagri: Callable[..., Any],
                        *args: Any) -> None:
        """Şimdiden `gecikme` saniye sonrasına olay ekler."""
        if gecikme < 0.0:
            raise GecmisZamanHatasi(f"negatif gecikme: {gecikme!r}")
        self.ekle(self.simdi + gecikme, geri_cagri, *args)

    # ---------------------------------------------------------------- koştur
    def kostur(self, bitis_s: float) -> None:
        """Kuyruğu `bitis_s` anına kadar işler.

        Bitiş anından SONRAKİ olaylar işlenmez ve kuyrukta kalır.
        """
        yigin = self._yigin
        while yigin and yigin[0][0] <= bitis_s:
            zaman, _sira, geri_cagri, args = heapq.heappop(yigin)
            # 🔒 Değişmez: işlenen olayların zamanı asla azalmaz.
            dogrula(zaman >= self.simdi, "olay zamanı geriye gitti")
            self.simdi = zaman
            geri_cagri(*args)
            self.islenen_olay += 1
        self.simdi = bitis_s

    # ----------------------------------------------------------------- durum
    def bekleyen_olay_sayisi(self) -> int:
        return len(self._yigin)

    def bos_mu(self) -> bool:
        return not self._yigin
