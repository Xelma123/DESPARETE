"""
Paket defteri — hangi paket doğdu, hangisi teslim edildi, ne kadar sürede.

🔒 HAM LİSTELER SONUÇ SATIRINA GİRER
====================================
Yüzdelikler ve IPDV burada hesaplanır ama **ham listeler de yazılır**:
`teslim_gecikmeleri_s`, `teslim_akis_kimlikleri`, `teslim_dogum_s`. Sebebi
şu: `analiz/` katmanı simülatörden hiçbir şey içe aktaramaz (JSONL üzerinde
çalışır) ve bu yüzden yüzdelik hesabının İKİNCİ bir gerçeklemesi orada
olacak. İki hesap ancak ham liste satırda olursa **karşılaştırılabilir** —
yoksa ikinci gerçekleme sessizce ayrışır.

⚠️ Bu bilinçli bir yedeklilik: `analiz/`in doğrulama kapılarından biri
"satırdaki yüzdelikler ham listeden yeniden üretilebiliyor mu" olacak.

🔴 PENCERE: DOĞUMA GÖRE
=======================
Bir teslim, paketin **doğduğu an** ölçüm penceresindeyse pencere ikizine
sayılır — teslim edildiği an değil. Sebebi tutarlılık: `uretilen_paket`
sayacının pencere ikizi de doğumları sayar, dolayısıyla
`pdr_pencere = pencerede doğup teslim edilen / pencerede doğan` olur.
Teslime göre sayılsaydı pay ile payda farklı kümelerden gelirdi ve oran
1'i aşabilirdi.

🔒 IPDV AKIŞ İÇİDİR
===================
Gecikme titreşimi bir akışın ardışık paketleri arasında tanımlıdır. Akış
kimliği olmasaydı iki akışın paketleri karışır ve ölçülen titreşim trafiğin
değil, akışların birbirine göre kaymasının titreşimi olurdu. `Paket`
`akis_kimligi` taşıdığı için bu mümkün — alan, metrikler yazılmadan ÖNCE
şemaya konmuştu.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from sim2.cekirdek.degismezler import dogrula

__all__ = ["TeslimKaydi", "PaketDefteri"]


@dataclass(frozen=True, slots=True)
class TeslimKaydi:
    """Teslim edilmiş bir paketin ölçüm kaydı."""

    kimlik: int
    akis_kimligi: int
    dogum_s: float
    teslim_s: float

    @property
    def gecikme_s(self) -> float:
        return self.teslim_s - self.dogum_s


@dataclass
class PaketDefteri:
    """Doğum ve teslim kayıtları. Sayaçlardan AYRI bir defterdir.

    ⚠️ Sayaçlar (`cekirdek/sayaclar.py`) toplamları tutar; bu defter
    **kimlikleri** tutar. İkisi ayrı olmak zorunda: yüzdelik ve IPDV bir
    toplamdan çıkarılamaz, tek tek gecikmeler gerekir.
    """

    pencere_bas_s: float
    pencere_bitis_s: float
    _dogum: dict[int, tuple[int, float]] = field(default_factory=dict)
    _teslim: list[TeslimKaydi] = field(default_factory=list)
    _teslim_kimlikleri: set[int] = field(default_factory=set)
    # 🔒 KR-E (K-182) — DÜĞÜM KAYBINDA PDR'NİN KOHORTU. Doğduğu anda hedefi
    # ölü olan paket PDR'ye GİRMEZ: hiçbir protokol onu teslim edemez ve
    # ölüm anları protokolden bağımsızdır (hash), yani her kolda aynı
    # paketler dışarıda kalır. Ölü kaynağın ÜRETEMEDİĞİ paket zaten doğmaz.
    # İkisi de GÖREV teslim oranının paydasındadır (`planlanan`). Kayıp
    # yokken iki küme boştur ve her şey birebir eskisi gibidir.
    olu_dugumler: set[int] = field(default_factory=set)
    _olu_hedefe_s: list[float] = field(default_factory=list)
    _uretilmeyen_s: list[float] = field(default_factory=list)

    # ------------------------------------------------------------ kayıt
    def dogdu(self, kimlik: int, akis_kimligi: int, dogum_s: float,
              hedef: int | None = None) -> None:
        dogrula(kimlik not in self._dogum, "aynı paket kimliği iki kez doğdu")
        if hedef is not None and hedef in self.olu_dugumler:
            self._olu_hedefe_s.append(dogum_s)          # KR-E: kohort dışı
            return
        self._dogum[kimlik] = (akis_kimligi, dogum_s)

    def uretilmedi(self, dogum_s: float) -> None:
        """KR-E: kaynağı ölü olduğu için doğmayan çizelgeli paket."""
        self._uretilmeyen_s.append(dogum_s)

    def teslim_edildi(self, kimlik: int, teslim_s: float) -> None:
        dogrula(kimlik in self._dogum, "doğmamış paket teslim edilemez")
        dogrula(kimlik not in self._teslim_kimlikleri,
                "aynı paket iki kez teslim edilemez — kopya teslim, PDR'yi "
                "1'in üstüne çıkarır ve hata sessiz kalır")
        akis, dogum = self._dogum[kimlik]
        dogrula(teslim_s >= dogum, "teslim doğumdan önce olamaz")
        self._teslim.append(TeslimKaydi(kimlik, akis, dogum, teslim_s))
        self._teslim_kimlikleri.add(kimlik)

    # ---------------------------------------------------------- sorgular
    def _penceredeyse(self, dogum_s: float) -> bool:
        return self.pencere_bas_s <= dogum_s < self.pencere_bitis_s

    @property
    def uretilen(self) -> int:
        return len(self._dogum)

    @property
    def pencerede_uretilen(self) -> int:
        return sum(1 for _, d in self._dogum.values() if self._penceredeyse(d))

    @property
    def teslim(self) -> int:
        return len(self._teslim)

    def planlanan(self, yalniz_pencere: bool = False) -> int:
        """KR-E: görevin istediği talep — doğan + hedefi ölüyken doğan +
        kaynağı ölü olduğu için doğmayan. Kayıp yokken `uretilen`."""
        if not yalniz_pencere:
            return (self.uretilen + len(self._olu_hedefe_s)
                    + len(self._uretilmeyen_s))
        return (self.pencerede_uretilen
                + sum(1 for d in self._olu_hedefe_s if self._penceredeyse(d))
                + sum(1 for d in self._uretilmeyen_s
                      if self._penceredeyse(d)))

    @property
    def pencerede_teslim(self) -> int:
        return sum(1 for t in self._teslim if self._penceredeyse(t.dogum_s))

    def sinif_sayimi(self, akis_siniflari: Mapping[int, str],
                     yalniz_pencere: bool = False
                     ) -> dict[str, tuple[int, int]]:
        """Akış sınıfı başına `(doğan, teslim)` — kohort DOĞUMA göre (K-171).

        🔒 Haritada olmayan bir akış HATADIR: sınıfsız kalan paket iki
        sınıfın toplamını `uretilen`den ayırır ve fark sessiz kalırdı.
        """
        cikti = {s: [0, 0] for s in set(akis_siniflari.values())}
        for akis, dogum in self._dogum.values():
            if yalniz_pencere and not self._penceredeyse(dogum):
                continue
            dogrula(akis in akis_siniflari, "sınıfı bilinmeyen akış")
            cikti[akis_siniflari[akis]][0] += 1
        for t in self.kayitlar(yalniz_pencere):
            cikti[akis_siniflari[t.akis_kimligi]][1] += 1
        return {s: (u, t) for s, (u, t) in cikti.items()}

    def dogumlar(self, yalniz_pencere: bool = False
                 ) -> tuple[tuple[int, int, float], ...]:
        """Doğan paketler — `(kimlik, akış, doğum_s)`, KİMLİĞE göre sıralı.

        🔒 `evren_hash` bunu kullanır. Sıralamanın kimliğe göre olması şart:
        sözlük ekleme sırası koşuya göre değişebilir ve iki kolun aynı paket
        evrenini taşıyıp taşımadığı sorusu sıralamaya duyarlı olmamalı.
        """
        return tuple(sorted(
            (kimlik, akis, dogum)
            for kimlik, (akis, dogum) in self._dogum.items()
            if not yalniz_pencere or self._penceredeyse(dogum)))

    def kayitlar(self, yalniz_pencere: bool = False) -> tuple[TeslimKaydi, ...]:
        if not yalniz_pencere:
            return tuple(self._teslim)
        return tuple(t for t in self._teslim if self._penceredeyse(t.dogum_s))

    def gecikmeler(self, yalniz_pencere: bool = False) -> tuple[float, ...]:
        return tuple(t.gecikme_s for t in self.kayitlar(yalniz_pencere))

    def pencere_kimlik_araligi(self) -> tuple[int, int] | None:
        """Pencerede doğan paketlerin kimlik aralığı — sonuç satırına yazılır.

        Bir sonuç satırının hangi paketleri kapsadığı buradan okunur; iki
        satırın aynı paketleri sayıp saymadığı ancak böyle denetlenebilir.
        """
        kimlikler = [k for k, (_, d) in self._dogum.items()
                     if self._penceredeyse(d)]
        if not kimlikler:
            return None
        return (min(kimlikler), max(kimlikler))

    # ------------------------------------------------------------- IPDV
    def ipdv(self, yalniz_pencere: bool = False) -> tuple[float, ...]:
        """Akış İÇİ ardışık gecikme farklarının mutlak değeri.

        🔒 Paketler DOĞUM sırasına dizilir, teslim sırasına değil: teslim
        sırası yeniden sıralamayı da içerir ve ölçülen şey titreşim yerine
        sıra bozulması olurdu.
        """
        akisa_gore: dict[int, list[TeslimKaydi]] = {}
        for t in self.kayitlar(yalniz_pencere):
            akisa_gore.setdefault(t.akis_kimligi, []).append(t)
        cikti: list[float] = []
        for kayitlar in akisa_gore.values():
            kayitlar.sort(key=lambda t: (t.dogum_s, t.kimlik))
            for onceki, simdi in zip(kayitlar, kayitlar[1:]):
                cikti.append(abs(simdi.gecikme_s - onceki.gecikme_s))
        return tuple(cikti)

    # ------------------------------------------------------------- ham
    def ham_sozluk(self) -> dict[str, object]:
        """Sonuç satırının `ham` bölümü.

        🔴 Hepsi ŞEMA TAAHHÜDÜ: `teslim_akis_kimlikleri` IPDV'nin akış içi
        sıralaması için, `teslim_dogum_s` yüzdeliklerin yeniden üretilmesi
        için, `pencere_kimlik_araligi` iki satırın aynı paketleri sayıp
        saymadığının denetimi için gerekli.

        🔴 `dogum_s` 8 Eylül 2026'da EKLENDİ ve eksikliği yapısaldı: evre
        metrikleri PDR'yi zaman kovalarında hesaplıyor, yani PAYDA olarak
        **pencerede doğan paketlerin ANLARI** gerekiyor. Defter yalnız
        `pencerede_uretilen` SAYISINI veriyordu; bir sayıdan kova
        çıkarılamaz. O yüzden şok derinliği, toparlanma süresi ve tamlık
        `.jsonl`den YENİDEN ÜRETİLEMİYORDU — `analiz/` katmanının doğrulama
        kapısı (*"satırdaki metrikler ham listeden yeniden üretilebiliyor
        mu"*) tam olarak bu üçünde çalışamazdı.

        🔒 `teslim_dogum_s` ⊂ `dogum_s` olması YEDEKLİLİKTİR ve kasıtlıdır:
        alt küme ilişkisi bozulursa satır kendi içinde tutarsızdır ve
        `analiz/` bunu görebilir. Yedekliliği denetlenebilir kılan şey tam
        olarak budur.
        """
        kayitlar = self.kayitlar()
        return {
            "teslim_kimlikleri": tuple(t.kimlik for t in kayitlar),
            "teslim_gecikmeleri_s": tuple(t.gecikme_s for t in kayitlar),
            "teslim_akis_kimlikleri": tuple(t.akis_kimligi for t in kayitlar),
            "teslim_dogum_s": tuple(t.dogum_s for t in kayitlar),
            # PAYDA: KOŞUNUN TAMAMINDA doğan her paketin anı, sıralı.
            # 🔴 PENCEREYE KIRPILMIYOR — ve bu bir düzeltmedir. İlk yazımda
            # yalnız penceredekiler yazılıyordu, oysa `teslim_*` dizileri
            # koşumun TAMAMINI kapsıyor: pay ile payda FARKLI kümelerden
            # geliyordu ve `teslim_dogum_s ⊄ dogum_s` oluyordu. Bu tam
            # olarak `pdr_pencere`de bir kez düzeltilmiş olan kusurdur.
            # 🔒 Pencere, `kapsam.olcum_penceresi_s` sınırlarıyla FİLTRELENEREK
            # elde edilir — iki dizi de aynı kapsamda olduğu için filtre
            # ikisine de aynı şekilde uygulanır.
            "dogum_s": tuple(sorted(d for _, _, d in self.dogumlar())),
            "pencere_kimlik_araligi": self.pencere_kimlik_araligi(),
            "pencerede_uretilen": self.pencerede_uretilen,
            # KR-E (K-182): görev teslim oranının paydası ham listeden
            # yeniden üretilebilsin diye.
            "olu_hedefe_dogum_s": tuple(sorted(self._olu_hedefe_s)),
            "uretilmeyen_dogum_s": tuple(sorted(self._uretilmeyen_s)),
        }
