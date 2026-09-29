"""
Düğüm kuyruğu — sonlu kapasite, kuyruk sonu atma.

NEDEN SONSUZ KUYRUK YASAK
--------------------------
Sonsuz kuyrukta karıştırma altında paketler atılmaz, sadece BEKLER.
Sonucu: teslim oranı yapay olarak yüksek çıkar, gecikme sınırsız büyür,
ve gecikme metriği anlamını yitirir. Ölçtüğümüz şey ağın dayanıklılığı
değil, belleğin büyüklüğü olur. (07-SIMULATOR-ARAYUZ.md, "KUYRUKLAR")

DEFTERLE BAĞLANTISI
-------------------
Kuyruk, korunum defterini KENDİSİ günceller. Çağıranın "kuyruğa koydum,
bir de deftere yazayım" demesi gerekmez — çünkü bir gün unutulur ve
paketler sessizce kaybolur.
"""

from __future__ import annotations

from collections import deque
from typing import Callable

from .ledger import KorunumDefteri
from .packet import Paket


class Kuyruk:
    """Tek bir düğümün gönderim kuyruğu."""

    def __init__(self, dugum: int, kapasite: int, defter: KorunumDefteri,
                 ekleme_geri_cagrisi: Callable[[int], None] | None = None) -> None:
        if kapasite <= 0:
            raise ValueError("kuyruk kapasitesi pozitif olmalı")
        self.dugum = dugum
        self.kapasite = kapasite
        self._defter = defter
        self._paketler: deque[Paket] = deque()
        # Kuyruğa paket girdiğinde düğümü uyandıran geri çağrı.
        # Olay güdümlü olmak zorunda: periyodik bir yoklama, örnekleme
        # aralığıyla trafik periyodunun kilitlenmesine (aliasing) yol açardı.
        self._uyandir = ekleme_geri_cagrisi
        # Teşhis sayaçları
        self.tasma_sayisi = 0
        self.en_yuksek_doluluk = 0
        # 🔴 B-105 — ÖLÇÜM PENCERESİNE AİT MAKSİMUM.
        # `en_yuksek_doluluk` bir MAKSİMUMDUR, toplam değil: pencere ikizi
        # `son - (bit - bas)` ile TÜRETİLEMEZ. Ölçüldü (27 Ağu, 4 koşu):
        # `gurultuden_kacan` S2/orta/t1'de kuyruk ısınma bitmeden zaten
        # doymuştu (bas=50, bit=50, son=50) — yani tüm koşu maksimumu
        # TAMAMEN ısınmanın ürünüydü. Bu yüzden ayrı izlenir.
        self.pencere_en_yuksek_doluluk = 0

    # ------------------------------------------------------------------ ekle
    def ekle(self, paket: Paket, yeni_uretilen: bool = False) -> bool:
        """Paketi kuyruğa koyar. Kuyruk doluysa paketi DÜŞÜRÜR.

        `yeni_uretilen=True` ise paket bu anda doğmuştur; defterde
        `uret()` çağrılır. Aksi hâlde paket uçuştan gelmiştir.

        Döner: kabul edildiyse True, düştüyse False.
        """
        if yeni_uretilen:
            self._defter.uret()          # üretilen +1, kuyrukta +1
        else:
            self._defter.ucustan_kuyruga()  # uçuşta -1, kuyrukta +1

        if len(self._paketler) >= self.kapasite:
            # Kuyruk sonu atma: yeni gelen düşer.
            # (Baştan atma da bir seçenekti; kuyruk sonu atma seçildi çünkü
            #  daha yaygın ve daha basit. Değiştirilirse deftere kayıt.)
            self._defter.dus("kuyruk_tasmasi", nereden="kuyruk")
            self.tasma_sayisi += 1
            return False

        self._paketler.append(paket)
        n = len(self._paketler)
        self.en_yuksek_doluluk = max(self.en_yuksek_doluluk, n)
        self.pencere_en_yuksek_doluluk = max(self.pencere_en_yuksek_doluluk, n)
        if self._uyandir is not None:
            self._uyandir(self.dugum)
        return True

    # ------------------------------------------------------- ölçüm penceresi
    def pencere_baslat(self) -> None:
        """🔴 B-105 — ölçüm penceresi başlarken pencere maksimumu sıfırlanır.

        ANLIK doluluktan başlar, sıfırdan değil: pencereye hangi dolulukla
        girildiği pencerenin bir olgusudur ve ısınmanın artığı değildir.
        Sıfırdan başlatmak, pencere boyunca hiç `ekle()` çağrılmayan bir
        kuyruğu "boş" gösterirdi — oysa dolu duruyor olabilir.
        """
        self.pencere_en_yuksek_doluluk = len(self._paketler)

    # --------------------------------------------------------------------- al
    def al(self) -> Paket | None:
        """Sıradaki paketi çıkarır ve 'uçuşta' hâline geçirir."""
        if not self._paketler:
            return None
        paket = self._paketler.popleft()
        self._defter.kuyruktan_al()      # kuyrukta -1, uçuşta +1
        return paket

    def bak(self) -> Paket | None:
        """Sıradaki pakete çıkarmadan bakar."""
        return self._paketler[0] if self._paketler else None

    # ------------------------------------------------------------------ durum
    def __len__(self) -> int:
        return len(self._paketler)

    @property
    def doluluk_orani(self) -> float:
        return len(self._paketler) / self.kapasite

    def bos_mu(self) -> bool:
        return not self._paketler

    def kalanlari_bosalt(self, sebep: str = "iletim_basarisiz") -> int:
        """Koşu sonunda kuyrukta kalanları sayar.

        ⚠️ ÇAĞRILMAZ — koşu sonunda kuyrukta kalan paketler DÜŞMÜŞ SAYILMAZ.
        Korunum denklemi onları `kuyrukta` olarak sayar ve öyle raporlanır.
        Düşmüş saymak, boşaltma penceresinin çalışıp çalışmadığını gizlerdi.

        Bu metot yalnızca test kolaylığı için var ve üretim yolunda
        kullanılmamalıdır.
        """
        adet = len(self._paketler)
        for _ in range(adet):
            self._paketler.popleft()
            self._defter.dus(sebep, nereden="kuyruk")
        return adet
