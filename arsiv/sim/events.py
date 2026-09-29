"""
Olay kuyruğu — kesikli olay simülasyonunun kalbi.

Gerçek zaman yok, kare yok, sabit adım yok. Yalnızca olaylar:
"12.483. saniyede şu olacak". En erken olay çıkarılır, çalıştırılır, doğurduğu
yeni olaylar kuyruğa eklenir.

BELİRLENİMCİLİK
---------------
Aynı tohum birebir aynı sonucu vermek zorunda (06-ON-KAYIT.md, K2).
Bunu bozabilecek tek şey, aynı zamana denk gelen iki olayın sırasının
belirsiz olmasıdır. Bu yüzden kuyruk anahtarı (zaman, sira_no) çiftidir:
sira_no monoton artan bir sayaçtır, yani eşit zamanlı olaylar EKLENME
SIRASINA göre çalışır. Bu keyfi ama belirlenimci bir kuraldır.

⚠️ Olay nesnelerinin kendisi ASLA karşılaştırılmaz. Karşılaştırılsaydı, iki
olay nesnesinin sırası bellek adresine bağlı olabilirdi — sessiz bir
belirlenimsizlik kaynağı.
"""

from __future__ import annotations

import heapq
from typing import Any, Callable


class GecmisZamanHatasi(RuntimeError):
    """Şimdiki zamandan önceye olay eklenmeye çalışıldı."""


class OlayKuyrugu:
    def __init__(self) -> None:
        self._yigin: list[tuple[float, int, Callable[..., Any], tuple]] = []
        self._sira: int = 0
        self.simdi: float = 0.0
        self.islenen_olay: int = 0

    # ------------------------------------------------------------------ ekle
    def ekle(self, zaman: float, geri_cagri: Callable[..., Any], *args: Any) -> None:
        """Belirtilen zamanda çalışacak bir olay ekler.

        Geçmişe olay eklemek sessizce yutulmaz — hata fırlatır. Sebep: geçmişe
        eklenen bir olay ya hiç çalışmaz ya yanlış sırada çalışır; ikisi de
        haftalar sonra "neden bu paket kaybolmuş" diye aranır.
        """
        if zaman < self.simdi:
            raise GecmisZamanHatasi(
                f"geçmişe olay eklenemez: t={zaman!r} < şimdi={self.simdi!r}"
            )
        heapq.heappush(self._yigin, (zaman, self._sira, geri_cagri, args))
        self._sira += 1

    def gecikmeyle_ekle(self, gecikme: float, geri_cagri: Callable[..., Any],
                        *args: Any) -> None:
        """Şimdiden itibaren `gecikme` saniye sonrasına olay ekler."""
        if gecikme < 0:
            raise GecmisZamanHatasi(f"negatif gecikme: {gecikme!r}")
        self.ekle(self.simdi + gecikme, geri_cagri, *args)

    # ----------------------------------------------------------------- koştur
    def kostur(self, bitis_s: float) -> None:
        """Kuyruğu `bitis_s` anına kadar işler.

        Bitiş anından SONRAKİ olaylar işlenmez ve kuyrukta kalır. Simdi,
        koşu sonunda tam olarak bitis_s'e ayarlanır — böylece koşu sonu
        sayımları her kolda aynı ana denk gelir.
        """
        while self._yigin and self._yigin[0][0] <= bitis_s:
            zaman, _sira, geri_cagri, args = heapq.heappop(self._yigin)
            # Değişmez: işlenen olayların zamanı asla azalmaz.
            assert zaman >= self.simdi, "olay zamanı geriye gitti"
            self.simdi = zaman
            geri_cagri(*args)
            self.islenen_olay += 1
        self.simdi = bitis_s

    # ------------------------------------------------------------------ durum
    def bekleyen_olay_sayisi(self) -> int:
        return len(self._yigin)

    def bos_mu(self) -> bool:
        return not self._yigin
