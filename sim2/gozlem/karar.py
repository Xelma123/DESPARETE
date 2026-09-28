"""
Karar — protokolün dönüş tipi. Ve `Beyan`: teşhis ↔ karar sınırı.

🔴 NEDEN DÖNÜŞ TİPİ `int | None` DEĞİL
======================================
Eski simülatörde protokol yalnız "sonraki atlama"yı döndürüyordu. Ama
literatürün asgari metrik kümesi üç kopma sayacı, Δ (rota kurtarma gecikmesi)
ve COR istiyor — ve üçü de protokolün *"rotam koptu"*, *"rotayı kurtardım"*
diyebilmesini gerektiriyor. Bu beyanlar bir yere yazılmak zorunda.

Yazılacakları yer `Karar.beyan`dır ve o alan **yalnız ölçüme gider**:
simülatörün davranışını değiştirmez, hiçbir paketin yolunu belirlemez.
Tek eylem `Karar.sonraki`dir.

🔴 RİSK 3: `Beyan` KÂHİN SIZINTISININ YENİ KAPISI
=================================================
Tehlike şu: hiç beyan etmeyen bir protokolün kopma sayacı **0** çıkar ve
tabloda *"hiç kopma yaşamadı"* gibi görünür — oysa yalnızca susmuştur.

Üç ölçüm bunu kapatır ve üçü de ön-kayıtta ilan edilir:
  a) `algilama_duyarliligi = kopma_algilanan / kopma_fiziksel` her koşuda
     raporlanır. Payda kâhin sayaçtır. Oran 0 ise kol *"beyan etmiyor"* diye
     ETİKETLENİR ve Δ `None` döner — 0 değil.
  b) 30 tohumda beyan sayısı ↔ PDR korelasyonu ölçülür.
  c) `olcum/` dışında hiçbir modül `Beyan`ı içe aktaramaz (AST testi).

🔒 Δ HİÇ BEYAN EDİLMEZSE `None`, SIFIR DEĞİL
============================================
*"Ölçüm yok"* ile *"gecikme sıfır"* aynı şey değildir. Sıfır döndürmek,
ölçülmemiş bir hücreyi ortalamaya sokmak olurdu.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sim2.cekirdek.degismezler import dogrula
from sim2.gozlem.kontrol import (BEYAN_TIPLERI, Beyan,  # noqa: F401
                                 niyetleri_dogrula)

# 🔒 `Beyan` ve `BEYAN_TIPLERI` 16 Eylül 2026'da `gozlem/kontrol.py`ye TAŞINDI
# (`04` K-134): kancaların da beyan döndürebilmesi gerekti ve bu dosya o
# modülü içe aktardığı için tersi bir döngü olurdu. Buradan YENİDEN DIŞA
# VERİLİYOR — `from sim2.gozlem.karar import Beyan` yazan her yer (testler,
# `olcum/`) değişmeden çalışıyor.
__all__ = ["BEYAN_TIPLERI", "Beyan", "Karar"]


@dataclass(frozen=True, slots=True)
class Karar:
    """Protokolün bir gözleme verdiği cevap.

    🔒 ÜÇ SONUÇ, İKİ DEĞİL — 16 Eylül 2026 (denetim B1, `04` K-131)
    ==============================================================
        sonraki = n              → "şu komşuya gönder"
        sonraki = None           → "gönderme"; paket DÜŞER (`hedef_yok`)
        beklet  = True           → "kuyrukta tut, birazdan yine sor"

    🔒 DÜŞME SEBEBİ BEYANA BAKAR — 16 Eylül 2026 (`04` K-134)
    =========================================================
        sonraki=None                              → `hedef_yok`
        sonraki=None + Beyan("rota_gecersiz")     → `rota_gecersiz`
        sonraki=None + Beyan("politika")          → `politika` (K-171)

    🔴 İkinci satır 16 Eylül'e kadar BELGEDE VARDI ama KODDA YOKTU. Ölçüldü:
    her kararda `rota_gecersiz` beyan eden bir sınav protokolünde sayaç 320
    arttı, o sebeple düşüş **0** kaldı — 320 paketin hepsi `hedef_yok` yazdı.
    Sebep listesi protokoller yazılmadan ÖNCE ayrılmıştı (bir ŞEMA
    taahhüdüdür) ama ona giden dal hiç döşenmemişti.

    🔒 AODV'de bu gerçek bir ayrımdır: rota HİÇ bulunamadı (keşif başarısız)
    ile rota VARDI ve koptu (RFC 3561 §6.11 — ara düğüm RERR gönderir ve
    paketi düşürür) ayrı şeylerdir; karıştırma altında ikisinin oranı
    protokolün davranışını anlatır.

    Üçüncüsü 16 Eylül'e kadar YOKTU ve bu, karşılaştırdığımız iki protokol
    ailesinden yalnız BİRİNİ vuruyordu. RFC 3561 §6.3 rota keşfi sırasında
    paketlerin tamponlanmasını ŞART KOŞAR (NS-2'nin AODV'si 64 paketlik bir
    kuyruk tutar). Tamponsuz bir AODV akış başlangıcında ve HER ROTA
    KOPMASINDAN SONRA keşif bitene kadar doğan her paketi kaybederdi; OLSR
    proaktiftir ve rotası neredeyse hep vardır, yani kayıp ona uğramazdı.
    Üstelik etkinin yoğunlaştığı yer kötüydü: karıştırma altında kopma sıktır
    ve onarım yavaştır — yani eksik, iddianın yaşadığı rejimde en büyüktü.

    `06` §8'in üçüncü geçerlilik koşulu (*"gizli asimetri yok"*) ve `03` §2
    ilke 4'ün straw-man uyarısı doğrudan buraya bakıyordu.
    """

    sonraki: int | None = None
    beyan: tuple[Beyan, ...] = field(default_factory=tuple)
    # 🔒 KONTROL DÜZLEMİ NİYETLERİ — K-112, `gozlem/kontrol.py`.
    # `KontrolIstegi` ya da `Uyandirma`. Varsayılan BOŞ: bugünkü dört
    # gerçekleme bu alanı hiç doldurmaz ve davranışları birebir aynı kalır.
    # Doldurmak kontrol kancalarının HEPSİNİ gerektirir (`kosum/kontrol.py`).
    niyetler: tuple = field(default_factory=tuple)

    # 🔒 "KUYRUKTA TUT" — paket düşmez, düğümün rota bekleme tamponuna geçer.
    # Tavanı (paket sayısı VE süre) simülatör uygular ve aşımı ayrı bir düşme
    # sebebiyle (`tampon_asimi`) deftere yazar; disiplin, uyandırma tavanında
    # kurulmuş olanın aynısıdır (`13` §03.5). Protokol sessizce sonsuza kadar
    # bekletemez.
    beklet: bool = False

    def __post_init__(self) -> None:
        niyetleri_dogrula(self.niyetler)
        # 🔴 "Hem gönder hem beklet" bir NİYET DEĞİLDİR. İzin verilseydi
        # çağıranın hangisini uygulayacağı belirsiz kalırdı ve belirsizliği
        # MAC katmanı kendi seçimiyle kapatırdı — yani yönlendirme kararını
        # sessizce simülatör verirdi.
        dogrula(not (self.beklet and self.sonraki is not None),
                "`beklet` ve `sonraki` birlikte verilemez — bekleyen paket "
                "gönderilmez")
        # 🔒 `politika` bir DÜŞME beyanıdır (K-171): gönderilen ya da
        # bekletilen pakette anlamsızdır, `rota_gecersiz` ile birlikte
        # verilirse düşme sebebi belirsiz kalırdı.
        if any(b.tip == "politika" for b in self.beyan):
            dogrula(self.sonraki is None and not self.beklet,
                    "`Beyan('politika')` yalnız `sonraki=None` ve "
                    "`beklet=False` ile verilir — paket düşer")
            dogrula(not any(b.tip == "rota_gecersiz" for b in self.beyan),
                    "`politika` ve `rota_gecersiz` aynı kararda verilemez — "
                    "düşme sebebi tek olmalı")

    @property
    def beyan_var_mi(self) -> bool:
        return bool(self.beyan)

    def beyanlar(self, tip: str) -> tuple[Beyan, ...]:
        dogrula(tip in BEYAN_TIPLERI, "bilinmeyen beyan tipi")
        return tuple(b for b in self.beyan if b.tip == tip)


dogrula(len(set(BEYAN_TIPLERI)) == len(BEYAN_TIPLERI), "beyan tipi tekrarlı")
