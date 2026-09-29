"""
Trafik — sabit bit hızlı (CBR) akışlar: yere toplama (birincil) ve eşler arası.

Yere toplamada her düğümden geçide telemetri (1 pkt/s × 512 B) ve geçitten
birkaç düğüme komut (0,25 pkt/s); eşler arasında 10 akış × 4 pkt/s. İkisi de
40 pkt/s sunar (K-126).

🔒 DOĞUM ÇİZELGESİ KURULUMDA HESAPLANIR
=======================================
Bütün doğum anları kurulumda üretilir ve `trafik_*` akışları orada tükenir.
Koşu sırasında çekim yapılsaydı çekim sayısı protokole göre değişir ve iki
kol FARKLI TRAFİK görürdü. Aynı tohumda her protokol **birebir aynı**
paketleri, aynı anlarda görür.

🔴 ÇİFTLER BAĞLANTIYA GÖRE SEÇİLMEZ
===================================
Kaynak–hedef çiftleri düzgün rastgele seçilir; "ulaşılabilir olsun" diye
koşullanmaz. Koşullansaydı seçim zamanla değişen topolojiye bağlanır ve
kollar arasında farklı çiftler seçilirdi — eşleştirme kırılırdı.

⚠️ HER DÜĞÜM EN ÇOK BİR AKIŞTA (eşler arası)
============================================
`2 × akış_sayısı ≤ düğüm_sayısı` `Konfig`te denetlenir; aynı düğüm iki
akışın kaynağı olsaydı ölçülen şey o düğümün darboğazı olurdu.

🔒 TİTREŞİM NEDEN VAR
=====================
Saf periyodik doğumlar kilitlenir ve her periyotta bir çarpışma fırtınası
olurdu. Faz akış başına rastgele, doğum anı ± `cbr_titresim_s`.
"""

from __future__ import annotations

from dataclasses import dataclass

from sim2.ag.paket import Paket, PaketSayaci
from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import Akislar
from sim2.yapilandirma.konfig import Konfig

__all__ = ["Akis", "Dogum", "TrafikUreteci"]


@dataclass(frozen=True, slots=True)
class Akis:
    """Bir kaynak–hedef çifti ve onun CBR üretimi."""
    kimlik: int
    kaynak: int
    hedef: int


@dataclass(frozen=True, slots=True)
class Dogum:
    """Çizelgelenmiş bir paket doğumu."""
    t_s: float
    akis_kimligi: int


class TrafikUreteci:
    """CBR akışları ve doğum çizelgesi. Kurulumda tam olarak belirlenir."""

    __slots__ = ("konfig", "akislar", "_hizlar", "_cizelge", "_kaynak_sira")

    @staticmethod
    def _yere_toplama(konfig: Konfig, r_cift
                      ) -> tuple[tuple[Akis, ...], tuple[float, ...]]:
        """Geçit dışındaki her düğümden geçide telemetri; geçitten
        `komut_akis_sayisi` düğüme komut (`v2/07` §06.2 · §18 Y4).

        ⚠️ "Her düğüm en çok bir akışta" değişmezi burada GEVŞER: geçit bütün
        telemetrinin hedefi ve komutların kaynağıdır; komut alan düğüm aynı
        zamanda telemetri kaynağıdır. Bedeli şartnamede beyan edilir.
        """
        gecit = konfig.gecit
        digerleri = [i for i in range(konfig.dugum_sayisi) if i != gecit]
        akislar = [Akis(kimlik=k, kaynak=i, hedef=gecit)
                   for k, i in enumerate(digerleri)]
        hizlar = [konfig.telemetri_paket_hizi_hz] * len(akislar)
        for hedef in r_cift.sample(digerleri, konfig.komut_akis_sayisi):
            akislar.append(Akis(kimlik=len(akislar), kaynak=gecit, hedef=hedef))
            hizlar.append(konfig.komut_paket_hizi_hz)
        return tuple(akislar), tuple(hizlar)

    def __init__(self, konfig: Konfig, akislar: Akislar) -> None:
        self.konfig = konfig
        # kaynak → sıradaki `kaynak_sira` (K-157). Akış başına değil KAYNAK
        # başına: yere toplamada geçit birden çok komut akışının kaynağıdır.
        self._kaynak_sira: dict[int, int] = {}
        r_cift = akislar["trafik_ciftleri"]
        r_zaman = akislar["trafik_zamani"]

        if konfig.trafik_deseni == "yere_toplama":
            self.akislar, self._hizlar = self._yere_toplama(konfig, r_cift)
        else:
            dogrula(2 * konfig.akis_sayisi <= konfig.dugum_sayisi,
                    "her düğüm en çok bir akışta yer alabilir")
            # --- çiftler: 2N ayrık düğüm, ikişer eşlenir ------------------
            secilen = r_cift.sample(range(konfig.dugum_sayisi),
                                    2 * konfig.akis_sayisi)
            self.akislar = tuple(
                Akis(kimlik=n, kaynak=secilen[2 * n], hedef=secilen[2 * n + 1])
                for n in range(konfig.akis_sayisi))
            self._hizlar = (konfig.akis_paket_hizi_hz,) * konfig.akis_sayisi
        for hiz in set(self._hizlar):
            dogrula(2.0 * konfig.cbr_titresim_s < 1.0 / hiz,
                    "titreşim periyodun yarısını aşamaz — doğumlar akış içinde "
                    "sıra değiştirir ve IPDV ölçümü anlamını yitirir")

        # --- doğum çizelgesi ---------------------------------------------
        cizelge: list[Dogum] = []
        for akis in self.akislar:
            periyot = 1.0 / self._hizlar[akis.kimlik]
            faz = r_zaman.uniform(0.0, periyot)
            k = 0
            while True:
                temel = faz + k * periyot
                if temel >= konfig.olcum_bitis_s:
                    break
                t = temel + r_zaman.uniform(-konfig.cbr_titresim_s,
                                            konfig.cbr_titresim_s)
                if 0.0 <= t < konfig.olcum_bitis_s:
                    cizelge.append(Dogum(t, akis.kimlik))
                k += 1
        # (zaman, akış) ile sıralanır: aynı ana düşen iki doğumun sırası
        # tohumdan bağımsız ve belirlenimci olmalı.
        cizelge.sort(key=lambda d: (d.t_s, d.akis_kimligi))
        self._cizelge = tuple(cizelge)

    # ------------------------------------------------------------------
    @property
    def cizelge(self) -> tuple[Dogum, ...]:
        return self._cizelge

    @property
    def toplam_dogum(self) -> int:
        return len(self._cizelge)

    def akis(self, kimlik: int) -> Akis:
        return self.akislar[kimlik]

    def paket_kur(self, dogum: Dogum, sayac: PaketSayaci) -> Paket:
        """Çizelgelenmiş bir doğumdan paket üretir."""
        akis = self.akislar[dogum.akis_kimligi]
        sira = self._kaynak_sira.get(akis.kaynak, 0)
        self._kaynak_sira[akis.kaynak] = sira + 1
        return Paket(kimlik=sayac.yeni(), akis_kimligi=akis.kimlik,
                     kaynak=akis.kaynak, hedef=akis.hedef,
                     dogum_s=dogum.t_s, boyut_bayt=self.konfig.paket_bayt,
                     ttl_kalan=self.konfig.ttl_baslangic, kaynak_sira=sira)

    # ---------------------------------------------------------------- teşhis
    def sunulan_hiz_hz(self) -> float:
        """Ölçülen üretim hızı — ilan edilenle karşılaştırmak için."""
        if self.konfig.olcum_bitis_s <= 0.0:
            return 0.0
        return self.toplam_dogum / self.konfig.olcum_bitis_s

    def penceredeki_dogum(self) -> int:
        bas, bitis = self.konfig.olcum_penceresi
        return sum(1 for d in self._cizelge if bas <= d.t_s < bitis)
