"""
Paket.

Her paketin kimliği, doğum anı ve TTL'i vardır. Bunlar olmadan
korunum denklemi tutsa bile paketlerin nerede kaybolduğu bilinemez.

⚠️ Paket nesnesi PROTOKOL TARAFINDAN GÖRÜLÜR — yani buradaki her alan
gözlem sözleşmesine tabidir. Bir alan eklemek, protokole yeni bir bilgi
vermek demektir ve 05-GOZLEM-PENCERESI.md'ye yazılmadan yapılamaz.

Örneğin `dogum_s` alanı: bir paketin ne zaman doğduğu, o paketi TAŞIYAN
düğüm tarafından bilinebilir mi? Evet — kaynak düğüm bunu başlığa yazabilir.
Ama saatler senkron olmadığı için başka bir düğüm bunu KENDİ saatiyle
karşılaştıramaz. Bu yüzden `dogum_s` yalnızca ölçüm/teşhis içindir ve
protokol kararına giremez. (05-GOZLEM-PENCERESI.md, "Saat senkronu yok")
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Paket:
    kimlik: int
    kaynak: int
    hedef: int
    bayt: int

    # --- teşhis/ölçüm alanları: protokol kararına GİREMEZ -----------------
    dogum_s: float = 0.0
    teslim_s: float | None = None

    # --- protokolün görebileceği alanlar ----------------------------------
    ttl: int = 32
    atlama_sayisi: int = 0

    # Ziyaret edilen düğümler: yalnızca TEŞHİS için (döngü tespiti).
    # ⚠️ Protokol bunu göremez — gerçek bir pakette böyle bir liste taşımak
    # bayta mal olurdu ve o bayt sayılmıyor.
    _ziyaret: list[int] = field(default_factory=list, repr=False)

    @property
    def gecikme_s(self) -> float | None:
        if self.teslim_s is None:
            return None
        return self.teslim_s - self.dogum_s

    def atla(self, dugum: int) -> None:
        """Bir atlama ilerlet. TTL burada azalır — tek yerde."""
        self.atlama_sayisi += 1
        self.ttl -= 1
        self._ziyaret.append(dugum)

    @property
    def dongude_mi(self) -> bool:
        """TEŞHİS: aynı düğüm ikinci kez ziyaret edildi mi?

        Bu, TTL ölümlerinin gerçekten döngüden mi yoksa sadece uzun
        yoldan mı geldiğini ayırt eder. İkisi farklı hastalıklardır.
        """
        return len(self._ziyaret) != len(set(self._ziyaret))
