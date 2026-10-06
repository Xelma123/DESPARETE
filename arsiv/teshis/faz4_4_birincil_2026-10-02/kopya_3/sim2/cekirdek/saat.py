"""
Saat — düğüm başına, senkron DEĞİL.

🔴 KUSUR 9: TEK KÜRESEL SAAT YAPISAL BİR KÂHİN KANALIYDI
========================================================
Eski simülatörde tek bir zaman vardı ve her düğüm onu görüyordu. Bunun
sonucu şuydu: bir protokol beacon'a zaman damgası koyduğu anda **bedava
kusursuz senkronizasyon** kazanıyordu — gerçek bir telsiz ağında en pahalı
şeylerden biri, simülatörde sıfır bedelle. Ve hiçbir test bunu göremezdi,
çünkü ortada bir "kural ihlali" yoktu; sadece simülatörün zamanı fazla
mükemmeldi.

🔒 ÇÖZÜM: YASAK DEĞİL, FİZİK
============================
Zaman damgası koymak yasaklanmıyor. Düğümlerin saatleri gerçekten ayrışıyor:

    ofset ~ U(−0,5, +0,5) s      açılışta rastgele
    sapma ~ N(0, 20) ppm         kristal toleransı

Protokol beacon'a `saat_s` yazabilir; alıcı onu kendi saatiyle
karşılaştırdığında **ofseti ve sapmayı görür**. Yani senkronizasyon isteyen
protokol onu kurmak zorunda kalır — tıpkı gerçekte olduğu gibi. Bedava
kusursuz senkron yasaklanmadan **imkânsız** hâle gelir.

🔒 TİP SINIRI
=============
`YerelZaman` ayrı bir tiptir. Küresel zamanla yerel zamanı karıştırmak bir
tip hatasıdır ve tip denetleyicisi yakalar; çalışma anında ise `Gozlem`in
`saat_s` alanı yalnız `YerelZaman` kabul eder.

⚠️ 20 ppm NE DEMEK
==================
350 s'lik bir koşuda 20 ppm = 7 ms sapma. Beacon aralığı 1 s olduğuna göre
sapma tek başına küçüktür; ASIL ayrışmayı ±0,5 s'lik ofset yapar. İkisi
birlikte, "komşumun saatine göre şu an" sorusunu ölçüm hatasıyla dolu bir
soru hâline getirir — gerçekte de öyledir.

🔒 ABLASYON: `Konfig.saat_senkron`
==================================
`True` yapıldığında ofset ve sapma sıfırlanır; yerel zaman küresel zamana
birebir eşit olur. Böylece *"saat senkronizasyonu olsaydı ne olurdu"* sorusu
ölçülebilir bir kol hâline gelir, bir varsayım olarak kalmaz.
"""

from __future__ import annotations

from typing import NewType

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import Akislar

__all__ = ["YerelZaman", "Saatler"]

# 🔒 Küresel zamandan AYRI bir tip. Karıştırmak tip hatasıdır.
YerelZaman = NewType("YerelZaman", float)


class Saatler:
    """Düğüm başına saat. Kurulumda çekilir, koşu boyunca değişmez.

    🔒 Ofset ve sapma **kurulumda** çekilir ve `saat_ofset`/`saat_sapma`
    akışları orada tükenir. Koşu sırasında çekilseydi, çekim sayısı protokole
    göre değişir ve iki kol farklı saatler görürdü — mobilite ve trafikte
    olduğu gibi.
    """

    __slots__ = ("dugum_sayisi", "_ofset", "_sapma", "senkron")

    def __init__(self, *, dugum_sayisi: int, ofset_araligi_s: float,
                 sapma_ppm: float, senkron: bool, akislar: Akislar) -> None:
        """🔒 `Konfig` ALMAZ — katman yönü gereği.

        `cekirdek` katmanı `yapilandirma`dan öncedir ve onu içe aktaramaz.
        Parametreler açıkça verilir; `Konfig`ten okuyup buraya taşımak
        `kosum/` katmanının işidir. İlk yazımda `Konfig` alıyordu ve mimari
        denetimi katman yönü ihlali olarak yakalardı.
        """
        dogrula(dugum_sayisi >= 1, "en az bir düğüm gerekli")
        dogrula(ofset_araligi_s >= 0.0, "saat ofset aralığı negatif olamaz")
        dogrula(sapma_ppm >= 0.0, "saat sapması negatif olamaz")
        self.dugum_sayisi = dugum_sayisi
        self.senkron = senkron
        n = dugum_sayisi
        if senkron:
            # 🔒 ABLASYON: kusursuz senkron. Akışlardan ÇEKİM YAPILMAZ ki
            # ablasyon kolu, öteki kolların rastgeleliğini kaydırmasın.
            self._ofset = (0.0,) * n
            self._sapma = (0.0,) * n
        else:
            r_ofset = akislar["saat_ofset"]
            r_sapma = akislar["saat_sapma"]
            self._ofset = tuple(
                r_ofset.uniform(-ofset_araligi_s, ofset_araligi_s)
                for _ in range(n))
            # ppm → oransal sapma
            self._sapma = tuple(
                r_sapma.gauss(0.0, sapma_ppm) * 1e-6 for _ in range(n))

    # ------------------------------------------------------------------
    def ofset_s(self, dugum: int) -> float:
        """Açılış ofseti — ÖLÇÜM içindir, protokol bunu göremez."""
        return self._ofset[dugum]

    def sapma_ppm(self, dugum: int) -> float:
        """Kristal sapması, ppm — ÖLÇÜM içindir."""
        return self._sapma[dugum] * 1e6

    def yerel(self, dugum: int, t_kuresel: float) -> YerelZaman:
        """Düğümün KENDİ saatinin gösterdiği an.

            t_yerel = t + ofset + sapma · t

        🔴 Protokolün gördüğü tek zaman budur. İki düğümün aynı anda okuduğu
        değerler farklıdır ve fark, ofsetle sapmanın toplamıdır.
        """
        return YerelZaman(t_kuresel * (1.0 + self._sapma[dugum])
                          + self._ofset[dugum])

    def kuresel(self, dugum: int, t_yerel: float) -> float:
        """Yerel zamandan küresele — 🔴 YALNIZ ÖLÇÜM İÇİN.

        Protokol bunu çağıramaz: `gozlem/` yüzeyinde yoktur ve `olcum/`
        dışındaki hiçbir modül `Saatler`i içe aktarmaz (AST testi).
        """
        return (t_yerel - self._ofset[dugum]) / (1.0 + self._sapma[dugum])

    def fark_s(self, a: int, b: int, t_kuresel: float) -> float:
        """İki düğümün saatleri arasındaki fark — teşhis ve ölçüm.

        Bir protokol `a`nın damgasını `b`nin saatiyle karşılaştırdığında tam
        olarak bu kadar yanılır.
        """
        return float(self.yerel(a, t_kuresel)) - float(self.yerel(b, t_kuresel))

    def en_buyuk_fark_s(self, t_kuresel: float) -> float:
        """Ağdaki en büyük saat ayrışması — sonuç satırına yazılır."""
        degerler = [float(self.yerel(i, t_kuresel))
                    for i in range(self.dugum_sayisi)]
        return max(degerler) - min(degerler)
