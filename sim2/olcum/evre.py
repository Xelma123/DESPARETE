"""
Evre metrikleri — şok · toparlanma · tespit. Adım ⑤.

Tasarım kararı: `v2/08-EVRE-METRIKLERI.md`.
Doğrulama kapıları: `python kalibrasyon/evre_metrikleri_kapilari.py`

🔴 NEDEN BU MODÜL VAR
=====================
Bir anti-jamming yönlendirme protokolünün asıl iddiası *"ne kadar
bozuldum"* değil, **"ne kadar hızlı toparlandım"**dır. Karıştırıcının bir
AÇILMA ANI olduğu için (`kanal/karistirici.py`) bu artık ölçülebilir — ama
yalnız evre sınırları ve "toparlandı" ölçütü **sonuç görülmeden** tanımlıysa.

🔒 TEK α — iki anlamlılık sabiti ondan TÜRER (Y10)
==================================================
`ALFA` evre metriklerinin tek anlamlılık sabitidir ve ön-kayıttan gelir.
M3'ün bandı `z(1 − α/2)`, M4'ün eşiği pencere başına `α / taranan pencere`
(Bonferroni). Eskiden iki ayrı sabit vardı (2,0 ve 0,01); ikisi de
gerekçesizdi ve M4'ün aile düzeyi yanlış alarmı %37–70'e çıkıyordu.

🔴 HATA PAYI KÜMELENMEYE DAYANIKLI (K-196, 28 Eylül 2026)
=========================================================
İlk hâl paket ve beyan BAĞIMSIZLIĞI varsayıyordu: M1/M3'ün SE'si yalnız
Agresti–Caffo (binom), M4'ün boş hipotezi yalnız Poisson. Kâhinle (G1) doğru
— kayıplar bağımsız. Gerçek protokolde kayıp ve kopma beyanı zamanda
KÜMELENİYOR (rota boşalması, komşu kaybı dalgaları): karıştırıcısız kolda
OLSR 3/3 tohumda "tespit" etti, şok derinliği ±0,06–0,09 çıktı (K-193).
Düzeltme SERBEST PARAMETRE GETİRMEZ, iki moment de koşunun KENDİ temiz
evresinden kestirilir:
    M1 · M3   SE = max(Agresti–Caffo, s_L · √(1 + L/T))  — `_kume_se`
    M4        1 s kova sayımlarının ortalaması VE varyansıyla negatif binom
              (varyans ≤ ortalama ise Poisson — bağımsız kolda eşik aynı)
`s_L`: temiz evredeki kayan `L` pencerelerinin PDR'lerinin standart sapması;
`√(1 + L/T)`: temizin kendi kestirim hatası (T/L bağımsız blok varsayımı).
⚠️ Beyan edilen bedel: kümelenen kolda band ve eşik genişler — gerçek bir
etki daha geç "tespit" edilir, "toparlandı" demek kolaylaşır. Alternatifi,
karıştırıcısız kolda tespit gören bir metrikti.

🔒 SIFIR SERBEST PARAMETRE — ölçüm kafesi iki RFC sabitinden türer
==================================================================
    ızgara adımı  S = 1 s   — RFC 3561, AODV HELLO_INTERVAL
    pencere       L = 15 s  — RFC 3626, OLSR TOP_HOLD_TIME

`S` ÇÖZÜNÜRLÜKTÜR: hiçbir taban çizgisi komşu bilgisini bundan hızlı
tazeleyemez, dolayısıyla daha ince bir ızgara gürültü ölçer.
`L` DURAĞANLIKTIR: *"ağ artık kararlı"* denebilecek en kısa süre; daha dar
bir pencere geçici bir sıçramayı toparlanma sanar.

⚠️ İkisinin farklı taban çizgilerinden gelmesi tutarsızlık DEĞİL: *"ne
sıklıkta bakabilirim"* ile *"ne kadar bakarsam kararlı bir sayı görürüm"*
ayrı sorulardır. Tek çapaya indirmenin ikisinden birini nasıl bozduğu
`08-EVRE-METRIKLERI.md` §06/1'de ölçülerek yazılı.

🔴 İLK TASARIMDA ŞOK PENCERESİ 3 s İDİ — GEREKÇE YANLIŞTI
==========================================================
Gerekçe şuydu: *"3 s = AODV ACTIVE_ROUTE_TIMEOUT; en hızlı taban çizgisi
bile bu süreden önce tepki veremez."* **Yanlış.** O sabit, bir rotanın
KULLANILMADIĞI için geçersizleşme süresidir; bağ arızası tespiti değildir.
AODV bir bağ koptuğunda MAC yeniden deneme sınırı dolar dolmaz RERR üretir —
milisaniyeler mertebesinde.

🔒 Sonucu: *"hiçbir protokolün tepki veremeyeceği pencere"* diye bir şey
YOKTUR ve şok derinliğini toparlanma hızından bir zaman penceresiyle tamamen
ayırmak İMKÂNSIZDIR. Hızlı toparlanan bir protokolün çukuru gerçekten daha
sığdır; bu fizik, kusur değil. Doğru yol ayırmaya çalışmak değil, **ne
ölçüldüğünü açıkça söylemektir** — `sok_derinligi`nin belgesine bak.

🔒 PAKET, DOĞUM ANINA GÖRE KOVALANIR
====================================
`pdr_pencere`nin tanımıyla aynı: bir evrenin PDR'si, o evrede DOĞAN
paketlerin kaçının teslim edildiğidir. Teslim anı evreden sonraya düşse bile
paket doğduğu evreye yazılır — sorulan şey *"o anda sunulan trafiğin ne
kadarı geçti"*dir.

⚠️ Evre sınırı, uçtan uca gecikme kadar bulanıklaşır. Bugün ölçülen p99
5–6 ms, ızgara adımı 1 s: **%0,6**. 🔴 Ama bu sayı PROTOKOLE BAĞLIDIR —
gerçek bir AODV rota keşfi sırasında paketi kuyrukta tutar. `G4` kapısı bunu
her kolda yeniden ölçtürür (`bulaniklik_orani`).

🔴 SANSÜR SAYIYA ÇEVRİLMEZ
==========================
Toparlanmayan bir koşu *"pencere sonunda toparlandı"* diye ortalamaya
girmez; `None` döner. Aksi hâlde hiç toparlanmayan bir protokol, ölçüm
penceresinin uzunluğu kadar iyi görünürdü. `rota_olaylari.py`nin Δ için
kurduğu kuralın aynısı; ikinci bir kural koymak ikisinin ayrışabileceği
anlamına gelirdi.

🔒 ÇİZELGELİ KARIŞTIRICI (K-207 onayı · K-209) — `cizelge=(açık_s, sessiz_s)`
=================================================================================
Tek basamaklı tanım (TEMİZ · ŞOK · TOPARLANMA) karıştırıcı açılıp kapanınca
bozulur: TOPARLANMA açık ve sessiz dönemleri karıştırır. Çizelge verilince
(birincil hücrenin `derin_sizma`sı; boş kolda "hayalet" çizelge):
    M1  aynı — ŞOK `[T_j; T_j + min(L, açık))`, yani ilk açık dönem
    M2  `PDR(bütün sessiz dönemler) / PDR(TEMİZ)`
    M3  TANIMSIZ (`None`, sebep `cizelgeli`): sessiz dönem durağanlık
        penceresinden (L) uzun değil — yerine bir metrik uydurulmaz
    M4  tarama İLK açık dönemle sınırlı; Bonferroni sayısı ondan türer
Sürekli karıştırıcıda dördü ve satırın alanları BİREBİR aynı kalır; yeni
alanlar yalnız çizelgeli satırda. Betimleyici teşhis (karar kuralı yok):
çevrim başına açık/sessiz PDR, katlanmış ızgara profili, evre sızıntısı.
Öneri ve gerekçe `arsiv/teshis/faz4_kapanis_2026-09-30/evre_cizelgeli_oneri.md`.

🔒 BU MODÜL SON İŞLEMDİR — sıcak yola dokunmaz
==============================================
Paket defteri zaten paket başına doğum ve teslim anını, rota defteri zaten
beyanları zaman damgasıyla tutuyor. Yeni sayaç yok, yeni olay yok. Bu bir
tercih değil KISIT: metrikler sıcak yola sayaç eklemeyi gerektirseydi,
ölçümün maliyeti sonuca karışırdı.
"""

from __future__ import annotations

import math
from statistics import NormalDist

from sim2.cekirdek.degismezler import dogrula
from sim2.olcum.paket_defteri import PaketDefteri
from sim2.olcum.rota_olaylari import RotaDefteri

__all__ = ["IZGARA_ADIMI_S", "PENCERE_S", "ALFA", "BANT_SE_KATI",
           "Evreler", "evre_sozlugu"]

# 🔒 RFC 3561 · AODV HELLO_INTERVAL = 1 000 ms. ÇÖZÜNÜRLÜK.
IZGARA_ADIMI_S: float = 1.0

# 🔒 RFC 3626 · OLSR TOP_HOLD_TIME = 3 × TC_INTERVAL = 15 s. DURAĞANLIK.
PENCERE_S: float = 15.0

# 🔒 TEK α — Y10 (`v2/07` §18 Y10 · `08` §05.3 · `04` K-123).
# Ön-kayıt (`06` §7) TEK bir aile düzeyi hedefi ilan ediyor; evre
# metriklerinin iki eski sabiti (bant için 2,0 · tespit için 0,01) artık
# buradan TÜRER. İkisi ayrı dururken birbirinden habersizdi: biri %2,5'lik
# bir kuyruk, öteki %1'lik başka bir kuyruk varsayıyordu ve ikisi de
# gerekçesizdi.
ALFA: float = 0.05

# 🔒 M3'ün bandı — TÜRETİLMİŞ: iki yanlı `z(1 − α/2)` = 1,95996. Elle 1,96
# yazmak α ile İKİNCİ bir doğru kaynağı doğururdu; α değişirse band da
# değişmek zorunda.
BANT_SE_KATI: float = NormalDist().inv_cdf(1.0 - ALFA / 2.0)


def _negatif_binom_esigi(ort: float, var: float, alfa: float) -> int:
    """En küçük k öyle ki P(X > k) ≤ alfa; X negatif binom, ortalaması `ort`,
    varyansı `var` (momentlerle: `r = ort² / (var − ort)`, `p = ort / var`).

    🔒 `var ≤ ort` ise aşırı yayılım YOK → `_poisson_esigi(ort)`; yani
    beyanları zamanda bağımsız olan bir kolda eşik eskisiyle BİREBİR aynı.
    Olasılıklar log uzayında toplanır (büyük `ort`ta alt taşma olmasın).
    """
    dogrula(ort >= 0.0 and var >= 0.0, "moment negatif olamaz")
    if var <= ort:
        return _poisson_esigi(ort, alfa)
    r = ort * ort / (var - ort)
    # 🔒 `1 − p` doğrudan `(var − ort) / var` — `log1p` bu depoda PER
    # gövdesinin imzası, `kanal.py` dışında yasak (`test_TEK_per_govdesi_VAR`).
    log_p, log_q = math.log(ort / var), math.log((var - ort) / var)
    sabit = r * log_p - math.lgamma(r)
    birikim = 0.0
    k = 0
    while True:
        birikim += math.exp(sabit + math.lgamma(k + r) - math.lgamma(k + 1)
                            + k * log_q)
        if 1.0 - birikim <= alfa or k > 100_000:    # patolojiye karşı emniyet
            return k
        k += 1


def _poisson_esigi(lam: float, alfa: float) -> int:
    """En küçük k öyle ki P(X > k) ≤ alfa, X ~ Poisson(lam).

    🔒 Kapalı formda: kuyruk toplanır. `lam = 0` ise eşik 0'dır.
    🔴 K-249: M4 bu fonksiyona artık 0 VERMEZ. Temiz evrede hiç beyan yoksa
    hız "0" değil, sıfır gözlemle uyumlu üst güven sınırıdır
    (`Evreler._sifir_gozlem_ust_siniri`). Eski okuma ("boş hipotez 'hiç beyan
    yok' ise bir beyan onu çürütür") sonlu bir temiz evrede yanlıştı: G1-P'de
    karıştırıcısız Babel'in koşudaki TEK beyanı "tespit" sayılıyordu.
    """
    dogrula(lam >= 0.0, "Poisson ortalaması negatif olamaz")
    if lam == 0.0:
        return 0
    terim = math.exp(-lam)
    birikim = terim
    k = 0
    while 1.0 - birikim > alfa:
        k += 1
        terim *= lam / k
        birikim += terim
        if k > 10_000:                     # patolojik lam'a karşı emniyet
            break
    return k


class Evreler:
    """Ölçüm penceresinin üç evresi ve üstünde tanımlı dört metrik.

    🔒 Evre sınırları KONFİGDEN türer, elle yazılmaz:
        TEMİZ       [ölçüm başı; T_j)
        ŞOK         [T_j; T_j + L)
        TOPARLANMA  [T_j + L; ölçüm sonu)
    Bölümleme TAMDIR — boşluk yok.
    """

    __slots__ = ("bas_s", "acilma_s", "bitis_s", "izgara_s", "pencere_s",
                 "cizelge", "_dogum", "_teslim", "_teslim_cift")

    def __init__(self, paket_defteri: PaketDefteri, bas_s: float,
                 acilma_s: float, bitis_s: float,
                 izgara_s: float = IZGARA_ADIMI_S,
                 pencere_s: float = PENCERE_S,
                 cizelge: tuple[float, float] | None = None) -> None:
        dogrula(bas_s <= acilma_s < bitis_s,
                f"açılma anı ölçüm penceresinde olmalı: "
                f"[{bas_s}; {bitis_s}) içinde {acilma_s}")
        dogrula(izgara_s > 0.0 and pencere_s > 0.0,
                "ızgara ve pencere pozitif olmalı")
        self.bas_s = bas_s
        self.acilma_s = acilma_s
        self.bitis_s = bitis_s
        self.izgara_s = izgara_s
        self.pencere_s = pencere_s
        if cizelge is not None:
            dogrula(cizelge[0] > 0.0 and cizelge[1] > 0.0,
                    f"çizelgede açık ve sessiz süre pozitif olmalı: {cizelge}")
        self.cizelge = cizelge
        # Doğum anları (payda) ve teslim edilenlerin doğum anları (pay).
        # 🔒 İkisi de AYNI kümeden türer — pay ile paydanın farklı kümelerden
        # gelmesi, `pdr_pencere`de bir kez düzeltilmiş bir kusurdu.
        self._dogum = sorted(d for _, _, d in paket_defteri.dogumlar())
        self._teslim = sorted(t.dogum_s for t in paket_defteri.kayitlar())
        self._teslim_cift = tuple((t.dogum_s, t.teslim_s)
                                  for t in paket_defteri.kayitlar())

    # ------------------------------------------------------------ yardımcı
    @staticmethod
    def _aralikta(sirali: list[float], a: float, b: float) -> int:
        from bisect import bisect_left
        return bisect_left(sirali, b) - bisect_left(sirali, a)

    def pdr(self, a: float, b: float) -> tuple[float | None, int]:
        """`[a; b)` aralığında DOĞAN paketlerin teslim oranı ve payda.

        🔴 Payda 0 ise `None` — 0,0 DEĞİL. Ölçülmemiş bir hücreyi ortalamaya
        sokmak, kollar arası karşılaştırmayı yanlı yapar.
        """
        payda = self._aralikta(self._dogum, a, b)
        if payda == 0:
            return None, 0
        return self._aralikta(self._teslim, a, b) / payda, payda

    @staticmethod
    def _se(p1: float, n1: int, p2: float, n2: int) -> float:
        """İki oranın FARKININ standart hatası — Agresti–Caffo.

        🔴 WALD KESTİRİCİSİ BU PROJEDE YAPISAL OLARAK BOZUK — ilk yazımda
        oradaydı ve bir kapıyı düşürdü.

        Wald: `SE² = p(1−p)/n`. `p = 1` olduğunda **tam olarak sıfır** verir.
        Ve bu projede `p = 1` istisna değil KURAL: karıştırıcısız kolda kâhin
        PDR'si 1,000 ölçülüyor — gerçekçilik kapısının (§10/4) talebi tam
        olarak budur. Yani hata payı, en çok ihtiyaç duyulduğu yerde çöküyor.

        🔒 Agresti–Caffo, iki oranın FARKI için belgelenmiş düzeltmedir: her
        örneğe bir başarı ve bir başarısızlık eklenir. Sınırda çökmez ve
        SERBEST PARAMETRE GETİRMEZ — ek, tam olarak sıfır/bir sınırındaki
        dejenerasyonu kaldıracak kadardır.

        ⚠️ Bunun bedeli beyan edilir: band, Wald'a göre biraz GENİŞTİR, yani
        "toparlandı" demek biraz daha kolaydır. Alternatifi, sıfır genişlikte
        bir bandın hiçbir zaman sağlanmamasıydı.
        """
        x1, x2 = p1 * n1, p2 * n2
        m1, m2 = n1 + 2, n2 + 2
        t1, t2 = (x1 + 1.0) / m1, (x2 + 1.0) / m2
        return math.sqrt(t1 * (1.0 - t1) / m1 + t2 * (1.0 - t2) / m2)

    def _kume_se(self) -> float | None:
        """TEMİZ ile tek bir `L` penceresinin PDR farkının KÜMELENMEYE
        DAYANIKLI standart hatası (K-196): `s_L · √(1 + L/T)`.

        `s_L` temiz evredeki kayan pencerelerin (ızgara adımıyla, `[t; t+L)`
        temizin içinde) PDR'lerinin örneklem standart sapmasıdır — pencere
        düzeyindeki GERÇEK oynaklık, paket bağımsızlığı varsaymaz. `L/T`
        temizin kendi kestirim hatası (T/L bağımsız blok). Temizde iki
        pencere yoksa `None` → yalnız Agresti–Caffo.

        ⚠️ Beyanlı sınırlar: kayan pencereler örtüşür (s_L'nin kendisi
        gürültülüdür); temiz evre kümelenmenin karakteristik süresinden kısa
        ise s_L aşağı yanlıdır. Pencere ile temiz arasındaki ilinti yok
        sayılır — pozitifse band gereğinden geniş (tutucu).
        """
        uzunluk = self.acilma_s - self.bas_s
        pdrler: list[float] = []
        k = 0
        while True:
            t = self.bas_s + k * self.izgara_s
            if t + self.pencere_s > self.acilma_s:
                break
            p, _ = self.pdr(t, t + self.pencere_s)
            if p is not None:
                pdrler.append(p)
            k += 1
        if len(pdrler) < 2:
            return None
        ort = math.fsum(pdrler) / len(pdrler)
        s = math.sqrt(math.fsum((p - ort) ** 2 for p in pdrler)
                      / (len(pdrler) - 1))
        return s * math.sqrt(1.0 + self.pencere_s / uzunluk)

    def _fark_se(self, p1: float, n1: int, p2: float, n2: int,
                 kume: float | None) -> float:
        """🔒 M1 ve M3'ün TEK hata payı: Agresti–Caffo ile kümelenmeye
        dayanıklı SE'nin BÜYÜĞÜ. Kayıplar bağımsızsa ikisi AYNI büyüklüğü
        (binom) kestirir — max yalnız kestirim gürültüsü kadar genişletir;
        temizde PDR = 1 ise (kâhin) `s_L = 0` ve eski davranış birebir."""
        se = self._se(p1, n1, p2, n2)
        return se if kume is None else max(se, kume)

    def donemler(self, acik: bool) -> tuple[tuple[float, float], ...]:
        """Çizelgenin açık (ya da sessiz) dönemleri, `[T_j; ölçüm sonu)`na
        kırpılmış; son kısmi dönem dâhil. Çizelge yoksa boş."""
        if self.cizelge is None:
            return ()
        acik_s, sessiz_s = self.cizelge
        periyot = acik_s + sessiz_s
        cikti: list[tuple[float, float]] = []
        k = 0
        while self.acilma_s + k * periyot < self.bitis_s:
            t0 = self.acilma_s + k * periyot
            a, b = (t0, t0 + acik_s) if acik else (t0 + acik_s, t0 + periyot)
            a, b = min(a, self.bitis_s), min(b, self.bitis_s)
            if b > a:
                cikti.append((a, b))
            k += 1
        return tuple(cikti)

    def pdr_birlesim(self, araliklar) -> tuple[float | None, int]:
        """Birden çok aralıkta DOĞAN paketlerin havuzlanmış teslim oranı."""
        payda = sum(self._aralikta(self._dogum, a, b) for a, b in araliklar)
        if payda == 0:
            return None, 0
        pay = sum(self._aralikta(self._teslim, a, b) for a, b in araliklar)
        return pay / payda, payda

    def izgara(self) -> tuple[float, ...]:
        """Açılmadan sonraki ızgara anları; pencere ölçüm sonunu AŞMAZ."""
        anlar: list[float] = []
        k = 0
        while True:
            t = self.acilma_s + k * self.izgara_s
            if t + self.pencere_s > self.bitis_s:
                break
            anlar.append(t)
            k += 1
        return tuple(anlar)

    # ------------------------------------------------------------- evreler
    @property
    def sok_araligi(self) -> tuple[float, float]:
        # 🔒 Çizelgede ŞOK ilk açık dönemden taşmaz (`min(L, açık)`); birincil
        # hücrede açık = L = 15 s, yani ŞOK bugünküyle birebir.
        uzunluk = (self.pencere_s if self.cizelge is None
                   else min(self.pencere_s, self.cizelge[0]))
        return (self.acilma_s, min(self.acilma_s + uzunluk, self.bitis_s))

    @property
    def toparlanma_araligi(self) -> tuple[float, float]:
        return (min(self.acilma_s + self.pencere_s, self.bitis_s),
                self.bitis_s)

    # ------------------------------------------------------------ metrikler
    def sok_derinligi(self) -> tuple[float | None, float | None]:
        """M1 — `PDR(temiz) − PDR(şok)` ve farkın standart hatası.

        🔴 NE ÖLÇTÜĞÜ AÇIKÇA YAZILIR: bu sayı *"darbe ne kadar sertti"* ile
        *"ilk `L` saniyede ne kadar toparlandım"*ı BİRLİKTE ölçer. Hızlı
        toparlanan bir protokolün şoku gerçekten daha sığdır ve bu gerçek bir
        üstünlüktür, artefakt değil. Ayrıştıran şey `toparlanma_suresi`dir;
        ikisi BİRLİKTE okunur.

        🔴 "En dip nokta" burada DEĞİL: bir eğrinin minimumu aşağı yanlı bir
        kestiricidir (pencere sayısı arttıkça düşer). Teşhis olarak
        `en_dip()`te duruyor, sonuç olarak değil.
        """
        temiz, n_t = self.pdr(self.bas_s, self.acilma_s)
        sok, n_s = self.pdr(*self.sok_araligi)
        if temiz is None or sok is None:
            return None, None
        return temiz - sok, self._fark_se(temiz, n_t, sok, n_s,
                                          self._kume_se())

    def toparlanma_tamligi(self) -> float | None:
        """M2 — `PDR(toparlanma) / PDR(temiz)`.

        🔒 `> 1` KIRPILMAZ: kırpmak bozuk bir ölçümü gizlemek olurdu.
        """
        temiz, _ = self.pdr(self.bas_s, self.acilma_s)
        # 🔒 Çizelgede TOPARLANMA = bütün sessiz dönemlerin birleşimi (K-209).
        top, _ = (self.pdr(*self.toparlanma_araligi) if self.cizelge is None
                  else self.pdr_birlesim(self.donemler(acik=False)))
        if temiz is None or top is None or temiz == 0.0:
            return None
        return top / temiz

    def toparlanma_suresi(self) -> float | None:
        """M3 — PDR'nin temizin `z(1−α/2)·SE` bandına döndüğü İLK an.

        Dönmezse `None`; sansür sayıya çevrilmez.

        🔴 Şartnamedeki *"temizin %X'i"* ölçütü ÖLDÜRÜLDÜ. `%X` serbest bir
        parametredir ve serbest bir parametre eğriler görüldükten sonra
        seçilir. Band, koşunun KENDİ paket sayımlarından hesaplanır.

        ⚠️ Beyan edilen sınır: band, `p̂` 0 ya da 1'e yakın olmadığında
        genişler; gürültülü bir kolda "toparlandı" demek daha kolaydır. Bu
        yüzden `sok_derinligi`nin SE'si sonuç sözlüğünde birlikte durur.
        K-196'dan beri SE kümelenmeye dayanıklı (`_fark_se`) — kümelenen
        kolda band o koşunun KENDİ temiz oynaklığı kadar genişler.
        """
        # 🔒 Çizelgede TANIMSIZ (K-209): sessiz dönem `L`den uzun değil;
        # sebep sözlükte `toparlanma_suresi_tanimsiz` alanında.
        if self.cizelge is not None:
            return None
        temiz, n_t = self.pdr(self.bas_s, self.acilma_s)
        if temiz is None:
            return None
        kume = self._kume_se()
        for t in self.izgara():
            p, n = self.pdr(t, t + self.pencere_s)
            if p is None:
                continue
            if p >= temiz - BANT_SE_KATI * self._fark_se(temiz, n_t, p, n,
                                                         kume):
                return t - self.acilma_s
        return None

    def en_dip(self) -> tuple[float | None, int]:
        """🔴 TEŞHİS — sonuç değil. Izgara üzerindeki EN DÜŞÜK pencere PDR'si.

        Kestirici aşağı yanlıdır ve yanlılık pencere sayısına bağlıdır; bu
        yüzden pencere sayısı DEĞERLE BİRLİKTE döner. Yanlılığın büyüklüğü
        boş kolda (G1) doğrudan görünür.
        """
        degerler = [p for p in (self.pdr(t, t + self.pencere_s)[0]
                                for t in self.izgara()) if p is not None]
        if not degerler:
            return None, 0
        return min(degerler), len(degerler)

    def tespit_gecikmesi(self, rota_defteri: RotaDefteri) -> float | None:
        """M4 — beyan hızının temiz evrenin Poisson kuyruğunu aştığı ilk an.

        🔴 "AÇILMADAN SONRAKİ İLK BEYAN" YETMEZ: protokoller karıştırıcı
        olmadan da sürekli kopma beyan eder (sönümleme, hareket). İlk beyanı
        almak çoğu zaman karıştırıcıyla İLGİSİ OLMAYAN bir olayı ölçmektir.
        Boş hipotez bu yüzden AYNI KOŞUNUN kendi temiz evresinden kestirilir.

        🔒 Susan protokol hızlı görünemez: `beyan_etmiyor` ise `None` döner.
        `algilama_duyarliligi` ile aynı disiplin; ikinci bir kural koymak
        ikisinin ayrışabileceği anlamına gelirdi.

        🔴 K-196: boş hipotez temiz kovaların ortalaması VE varyansıyla
        negatif binom — beyanlar kümeleniyorsa Poisson kuyruğu fazla incedir
        (karıştırıcısız OLSR 3/3 tohumda "tespit" ediyordu, K-193).
        """
        if rota_defteri.beyan_etmiyor:
            return None
        sirali = sorted(rota_defteri.beyan_anlari("kopma"))
        ort, var = self._kova_momentleri(sirali)
        if ort == 0.0:
            # 🔴 K-249 (G1-P, 17 Ekim 2026): temizde SIFIR beyan → hız 0
            # değil, sıfır gözlemle uyumlu üst sınır; Poisson (var = ort).
            # Yalnız tespiti kaldırabilir ya da geciktirebilir.
            ort = var = self._sifir_gozlem_ust_siniri()
        # 🔒 BONFERRONI (Y10): eşik pencere BAŞINA `α / taranan pencere`.
        # Tek bir pencere için α kullanmak, ~170 pencere tarandığında aile
        # düzeyi yanlış alarmı %37–70'e çıkarıyordu — ölçüldü, üretici:
        # `python -u kalibrasyon/anlamlilik_sabitleri.py`.
        # 🔒 Çizelgede tarama İLK açık dönemle sınırlı (K-209): sonraki
        # dönemlerdeki bir tespit "ilk açılmayı kaçırdı" demektir, gecikme
        # değil (K-200 partisinde tespitlerin hepsi 2. ya da 3. dönemdeydi).
        son = (self.bitis_s if self.cizelge is None
               else min(self.acilma_s + self.cizelge[0], self.bitis_s))
        taranan = max(int((son - self.acilma_s) / self.izgara_s), 1)
        esik = _negatif_binom_esigi(ort, var, ALFA / taranan)
        k = 1
        while True:
            t = self.acilma_s + k * self.izgara_s
            if t > son:
                return None
            if self._aralikta(sirali, t - self.izgara_s, t) > esik:
                return t - self.acilma_s
            k += 1

    def cizelge_teshisi(self) -> dict[str, object]:
        """🔴 BETİMLEYİCİ — karar kuralı yok (K-209). Çizelgeli satırda:
        çevrim başına açık/sessiz PDR · katlanmış ızgara profili (çevrimler
        havuzlanır; özdeş çevrim varsayımı beyanlı — karıştırıcı her sessizde
        taşınır) · evre sızıntısı (teslim edilen paketlerden doğduğu evreden
        BAŞKA evrede teslim edilenlerin oranı; G4ç'nin ölçüsü)."""
        acik_s, sessiz_s = self.cizelge
        periyot = acik_s + sessiz_s
        acik, sessiz = self.donemler(True), self.donemler(False)
        cevrim = []
        for i, a in enumerate(acik):
            s_ = sessiz[i] if i < len(sessiz) else None
            cevrim.append([self.pdr(*a)[0],
                           None if s_ is None else self.pdr(*s_)[0]])
        kova = round(periyot / self.izgara_s)
        profil = []
        for j in range(kova):
            araliklar = []
            k = 0
            while True:
                a = self.acilma_s + k * periyot + j * self.izgara_s
                if a >= self.bitis_s:
                    break
                araliklar.append((a, min(a + self.izgara_s, self.bitis_s)))
                k += 1
            profil.append(self.pdr_birlesim(araliklar)[0])

        def evre(t: float) -> str | None:
            if t < self.acilma_s:
                return None
            return "acik" if (t - self.acilma_s) % periyot < acik_s else "sessiz"
        sayilan = [(evre(d), evre(t)) for d, t in self._teslim_cift
                   if self.acilma_s <= d < self.bitis_s]
        sizinti = (sum(1 for a, b in sayilan if a != b) / len(sayilan)
                   if sayilan else None)
        return {"evre_cevrim_pdr": cevrim, "evre_katli_profil": profil,
                "evre_sizinti": sizinti}

    def _sifir_gozlem_ust_siniri(self) -> float:
        """Temiz evrede sıfır beyan: kova başına hızın tek yanlı (1 − α) üst
        güven sınırı, `−ln α / n` (Poisson; n = temiz evrenin kova sayısı).

        🔒 Sıfır sayım "hız 0" demek değildir; yalnız hızın bu sınırın
        altında olduğunu söyler. Yeni sabit yok: α modülün tek α'sı (K-123).
        G1-P'de (100 kova) λ ≈ 0,030 → eşik 2, yani bir saniyede en az üç
        beyan tespit sayılır.
        """
        n = max((self.acilma_s - self.bas_s) / self.izgara_s, 1.0)
        return -math.log(ALFA) / n

    def _kova_momentleri(self, sirali: list[float]) -> tuple[float, float]:
        """TEMİZ evrenin ızgara kovalarındaki beyan sayısının ortalaması ve
        örneklem varyansı (n − 1).

        🔒 Kovalar `[bas + i·S; bas + (i+1)·S)`, yalnız TAM olanlar. İki tam
        kova yoksa varyans kestirilemez: ortalama eskisi gibi (kesirli kova
        sayısıyla) ve varyans = ortalama döner → Poisson, yani K-196 öncesi
        davranış birebir.
        """
        tam = int((self.acilma_s - self.bas_s) / self.izgara_s + 1e-9)
        if tam < 2:
            temiz_sayi = self._aralikta(sirali, self.bas_s, self.acilma_s)
            kova_sayisi = max((self.acilma_s - self.bas_s) / self.izgara_s,
                              1.0)
            ort = temiz_sayi / kova_sayisi
            return ort, ort
        sayimlar = [self._aralikta(sirali, self.bas_s + i * self.izgara_s,
                                   self.bas_s + (i + 1) * self.izgara_s)
                    for i in range(tam)]
        ort = math.fsum(sayimlar) / tam
        var = math.fsum((c - ort) ** 2 for c in sayimlar) / (tam - 1)
        return ort, var


def evre_sozlugu(paket_defteri: PaketDefteri, rota_defteri: RotaDefteri,
                 bas_s: float, acilma_s: float, bitis_s: float,
                 gecikme_p99_s: float | None = None,
                 izgara_s: float = IZGARA_ADIMI_S,
                 pencere_s: float = PENCERE_S,
                 cizelge: tuple[float, float] | None = None
                 ) -> dict[str, object]:
    """Sonuç satırına giren evre metrikleri.

    🔒 Karıştırıcısız kolda açılma anı ölçüm penceresine düşse bile evreler
    TANIMLIDIR ve bu KASTEN böyle: G1 kapısı (*"boş kolda metrikler susuyor
    mu"*) ancak metrikler orada da hesaplanırsa çalışır. Boş kolda beklenen
    şey metriğin YOKLUĞU değil, SIFIRA YAKIN OLMASIDIR.
    """
    e = Evreler(paket_defteri, bas_s, acilma_s, bitis_s, izgara_s, pencere_s,
                cizelge)
    derinlik, derinlik_se = e.sok_derinligi()
    # 🔴 En dip çizelgede açık/sessizi karıştıran pencerelerden olurdu → yok.
    dip, dip_pencere = e.en_dip() if cizelge is None else (None, 0)
    temiz, temiz_n = e.pdr(bas_s, acilma_s)
    sok, sok_n = e.pdr(*e.sok_araligi)
    top, top_n = e.pdr(*e.toparlanma_araligi)
    cikti: dict[str, object] = {
        "evre_izgara_s": izgara_s,
        "evre_pencere_s": pencere_s,
        "evre_acilma_s": acilma_s,
        "pdr_temiz": temiz, "pdr_temiz_n": temiz_n,
        "pdr_sok": sok, "pdr_sok_n": sok_n,
        "pdr_toparlanma": top, "pdr_toparlanma_n": top_n,
        "sok_derinligi": derinlik,
        "sok_derinligi_se": derinlik_se,
        "toparlanma_tamligi": e.toparlanma_tamligi(),
        "toparlanma_suresi_s": e.toparlanma_suresi(),
        "tespit_gecikmesi_s": e.tespit_gecikmesi(rota_defteri),
        # 🔴 TEŞHİS — sonuç değil; yanlılığı pencere sayısına bağlı.
        "en_dip_pdr": dip,
        "en_dip_pencere_sayisi": dip_pencere,
        # 🔴 G4 KAPISI: doğum-anına-göre kovalamanın bulanıklığı. 1'i
        # aşarsa evre atfetme kuralı yeniden yazılmalıdır.
        "bulaniklik_orani": (None if gecikme_p99_s is None
                             else gecikme_p99_s / izgara_s),
    }
    if cizelge is not None:
        # 🔒 Yalnız çizelgeli satırda — sürekli karıştırıcının satırı birebir.
        acik_p, acik_n = e.pdr_birlesim(e.donemler(acik=True))
        sessiz_p, sessiz_n = e.pdr_birlesim(e.donemler(acik=False))
        cikti.update({
            "evre_cizelge_s": list(cizelge),
            "pdr_acik": acik_p, "pdr_acik_n": acik_n,
            "pdr_sessiz": sessiz_p, "pdr_sessiz_n": sessiz_n,
            "toparlanma_suresi_tanimsiz": "cizelgeli",
            # G4ç: M1 ve M2 bütün-evre toplamları → ölçüt p99 < açık süre.
            "bulaniklik_orani_evre": (None if gecikme_p99_s is None
                                      else gecikme_p99_s / cizelge[0]),
            **e.cizelge_teshisi(),
        })
    return cikti
