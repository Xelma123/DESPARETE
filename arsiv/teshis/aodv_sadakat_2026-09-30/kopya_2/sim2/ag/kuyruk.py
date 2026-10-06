"""
Kuyruk — düğüm başına sonlu FIFO.

🔴 SONSUZ KUYRUK YASAK
======================
Sonsuz kuyruk gecikme metriğini anlamsızlaştırır: ağ ne kadar yüklenirse
yüklensin paket düşmez, yalnız gecikme büyür ve PDR yapay olarak 1'e yakın
kalır. Gerçek bir telsizde tampon sonludur ve taşma bir KAYIP sebebidir.
Kapasite `Konfig.kuyruk_kapasitesi`den gelir ve sıfır olamaz.

🔒 DÜŞME KORUNUM DEFTERİNDEN GEÇER
==================================
Kuyruk paketi kendi başına "yok etmez". Taşma olduğunda çağıran, defterin
`dus("kuyruk_tasmasi", nereden="kuyruk")` geçişini yapmak ZORUNDADIR.
`Kuyruk` bunu kendi yapmaz çünkü defter tek geçiş noktasıdır ve iki farklı
yerden düşürmek denklemi çift sayardı.

⚠️ TEPE DOLULUK AYRI İZLENİR
============================
`en_yuksek_doluluk` bir `tepe` sayacıdır ve **farkla türetilemez**: pencere
içindeki en yüksek değer, pencere sonu ile başı arasındaki fark değildir.
`cekirdek/sayaclar.py` bunu ayrı izler; kuyruk yalnız anlık doluluğu bildirir.
"""

from __future__ import annotations

from collections import deque

from sim2.ag.paket import Paket
from sim2.cekirdek.degismezler import dogrula

__all__ = ["Kuyruk"]


class Kuyruk:
    """Sonlu FIFO. Dolu kuyruğa gelen paket KABUL EDİLMEZ (kuyruk sonu atma).

    🔒 Kuyruk sonu atma (drop-tail) seçildi; alternatifler ve neden elendiği:
      · *baştan atma* — en eski paket düşer; gecikme dağılımını yapay olarak
        sıkıştırır ve p95'i olduğundan iyi gösterir
      · *rastgele erken atma (RED)* — bir tıkanıklık denetimi mekanizmasıdır;
        buradaki soru yönlendirme, tıkanıklık denetimi değil. Eklenseydi
        ölçülen fark protokolün değil, RED ayarının farkı olabilirdi
    """

    __slots__ = ("kapasite", "_sira")

    def __init__(self, kapasite: int) -> None:
        dogrula(kapasite > 0, "kuyruk kapasitesi sonlu ve pozitif olmalı")
        self.kapasite = kapasite
        self._sira: deque[Paket] = deque()

    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._sira)

    @property
    def dolu_mu(self) -> bool:
        return len(self._sira) >= self.kapasite

    @property
    def bos_mu(self) -> bool:
        return not self._sira

    def ekle(self, paket: Paket) -> bool:
        """Paketi kuyruğa alır. Dolu ise `False` — çağıran DÜŞÜRMEK zorunda.

        🔴 Dönüş değeri yok sayılamaz: `False` dönerse paket hiçbir yerde
        değildir ve defterden geçirilmezse korunum denklemi kırılır. Testi var.
        """
        if self.dolu_mu:
            return False
        self._sira.append(paket)
        return True

    def al(self) -> Paket:
        """Sıradaki paketi çıkarır. Boş kuyruktan almak bir DEĞİŞMEZ ihlalidir."""
        dogrula(bool(self._sira), "boş kuyruktan paket alınamaz")
        return self._sira.popleft()

    def bak(self) -> Paket:
        """Sıradakine çıkarmadan bakar — MAC iletime hazırlanırken kullanır."""
        dogrula(bool(self._sira), "boş kuyrukta bakılacak paket yok")
        return self._sira[0]

    def tumu(self) -> tuple[Paket, ...]:
        """Koşu sonunda kuyrukta kalanlar — korunum denkleminin bir terimi."""
        return tuple(self._sira)

    def bosalt(self) -> tuple[Paket, ...]:
        kalan = tuple(self._sira)
        self._sira.clear()
        return kalan
