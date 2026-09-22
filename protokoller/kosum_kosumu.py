"""
Koşum protokolleri — **taban çizgisi DEĞİL**, simülatörün kendi test aleti.

🔴 BUNLAR AODV/OLSR/AOMDV YERİNE GEÇMEZ
=======================================
Buradaki iki protokol, Adım 9'un olay döngüsünü sınamak için vardır: paketin
gerçekten aktığını, defterin tuttuğunu ve düşme sebeplerinin ateşlendiğini
görmek. Hiçbiri literatürden bir protokol değildir ve hiçbiri sonuç
tablosuna girmez. Taban çizgileri Adım 11'de yazılacak.

🔒 KÂHİN ERİŞİMİ YOK
====================
İkisi de yalnız `Gozlem`i görür: komşu tablosu (beacon'dan), kendi kuyruğu,
kendi saati. Konum, topoloji, `Konfig`, kanal — hiçbiri görünmez. Katman
kuralını içe aktarma grafiği testi bağlar.
"""

from __future__ import annotations

from sim2.gozlem.karar import Karar
from sim2.gozlem.pencere import Gozlem

__all__ = ["DogrudanKomsu", "EnYakinKimlik"]


class DogrudanKomsu:
    """Hedef doğrudan komşuysa gönderir, değilse `hedef_yok`.

    Tek atlamalı teslim, kuyruk taşması ve `hedef_yok` dalını sınar.
    Çok atlama üretmez — onu `EnYakinKimlik` yapar.
    """

    ad = "dogrudan_komsu"
    __slots__ = ()

    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        if gozlem.paket is None:
            return Karar()
        hedef = gozlem.paket.hedef
        for komsu in gozlem.komsular:
            if komsu.dugum == hedef:
                return Karar(sonraki=hedef)
        return Karar()

    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem: Gozlem, komsu: int,
                      yuk: tuple[tuple[str, object], ...]) -> None:
        return None

    def teshis(self, dugum: int) -> dict:
        return {}


class EnYakinKimlik:
    """Hedef komşu değilse, KİMLİĞİ hedefe en yakın komşuya iletir.

    🔴 Kasten kötü bir sezgi: düğüm numaraları uzayda bir anlam taşımaz, bu
    yüzden yol seçimi rastgeleye yakındır ve **döngü üretir**. İstenen tam
    olarak budur — TTL ölümü, tekrar bastırma ve `aktarilan_paket` dalları
    ancak çok atlamalı ve döngülü bir trafikte ateşlenir. Bir taban çizgisi
    olarak kullanılması anlamsız olurdu; koşum aleti olarak yeri var.
    """

    ad = "en_yakin_kimlik"
    __slots__ = ()

    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        if gozlem.paket is None or not gozlem.komsular:
            return Karar()
        hedef = gozlem.paket.hedef
        adaylar = [k.dugum for k in gozlem.komsular]
        if hedef in adaylar:
            return Karar(sonraki=hedef)
        return Karar(sonraki=min(adaylar, key=lambda n: (abs(n - hedef), n)))

    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem: Gozlem, komsu: int,
                      yuk: tuple[tuple[str, object], ...]) -> None:
        return None

    def teshis(self, dugum: int) -> dict:
        return {}
