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

# `Beyan` ve `BEYAN_TIPLERI` `gozlem/kontrol.py`dedir (K-134: kancalar da
# beyan döndürür; tersi bir içe aktarma döngüsü olurdu) ve buradan
# yeniden dışa verilir.
__all__ = ["BEYAN_TIPLERI", "Beyan", "Karar"]


@dataclass(frozen=True, slots=True)
class Karar:
    """Protokolün bir gözleme verdiği cevap.

    🔒 ÜÇ SONUÇ (denetim B1, K-131)
    ===============================
        sonraki = n              → "şu komşuya gönder"
        sonraki = None           → "gönderme"; paket DÜŞER
        beklet  = True           → "bekleme tamponunda tut, birazdan yine sor"

    🔒 DÜŞME SEBEBİ BEYANA BAKAR (K-134)
    ====================================
        sonraki=None                              → `hedef_yok`
        sonraki=None + Beyan("rota_gecersiz")     → `rota_gecersiz`
        sonraki=None + Beyan("politika")          → `politika` (K-171)

    AODV'de bu gerçek bir ayrımdır: rota HİÇ bulunamadı ile rota VARDI ve
    koptu (RFC 3561 §6.11) ayrı şeylerdir; karıştırma altında oranları
    protokolün davranışını anlatır.

    Bekletme RFC 3561 §6.3'ün şartıdır: tamponsuz bir tepkisel protokol
    her kopmadan sonra keşif bitene kadar doğan paketi kaybeder, proaktif
    protokol kaybetmezdi — gizli bir asimetri (`06` §8 koşul 3).
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

    # 🔒 UÇTAN UCA KOPYA — D-23 · K-231 (`13` §07). Gönderilen paketin eşleri
    # bu komşulara da gider: her eş düğümün kuyruğunun SONUNA girer ve kuyruk
    # başına gelince protokole yeniden sorulmadan o komşuya iletilir (karar
    # kopya anında verildi). Hedefte ilk varan teslim sayılır; eşlerin yayın
    # süresi VERİ yüküdür. Varsayılan BOŞ: kopya istemeyen protokolün
    # davranışı ve sonuç satırı birebir aynı.
    kopyalar: tuple[int, ...] = ()

    # 🔒 KAYNAK ROTASI — K-232 (DSR ailesi, RFC 4728 §6.7). `rota` verilirse
    # gönderilen paketin başlığındaki kaynak rotası odur; `kopya_rotalari`
    # (boş ya da `kopyalar` kadar) eşlerinkini verir. Başlıkta yazan adres
    # başına bayt çerçeveyi uzatır ve yönlendirme ek yüküne sayılır. Varsayılan
    # `None`: paketin rotası değişmez — rota taşımayan protokol birebir aynı.
    rota: tuple[int, ...] | None = None
    kopya_rotalari: tuple[tuple[int, ...], ...] = ()

    def __post_init__(self) -> None:
        niyetleri_dogrula(self.niyetler)
        if self.kopyalar:
            dogrula(self.sonraki is not None and not self.beklet,
                    "`kopyalar` yalnız gönderilen pakette verilir "
                    "(`sonraki` dolu, `beklet` değil)")
            dogrula(len(set(self.kopyalar)) == len(self.kopyalar)
                    and self.sonraki not in self.kopyalar,
                    "kopya komşuları tekil ve `sonraki`den farklı olmalı")
        if self.rota is not None:
            dogrula(self.sonraki is not None and not self.beklet,
                    "`rota` yalnız gönderilen pakette verilir")
        if self.kopya_rotalari:
            dogrula(len(self.kopya_rotalari) == len(self.kopyalar),
                    "`kopya_rotalari` her eş için bir rota vermeli")
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
