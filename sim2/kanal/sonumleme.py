"""
Hızlı sönümleme — Rician, PARÇA başına, zaman-korelasyonlu, **DURUMSUZ**.

🔴 TASARIMIN KİLİT TAŞI
=======================
AR(1) doğal olarak durumludur: `h_k = ρ·h_{k−1} + …`. Durumlu yazılsaydı,
kanalın gördüğü dizi *hangi protokolün kaç kez çektiğine* bağlı olurdu ve iki
kol aynı tohumda **farklı kanallar** görürdü. 30 tohum bunu kurtarmaz;
eşleştirme yapısal olarak kırılır.

🔒 ÇÖZÜM: HASH'LENMİŞ YENİLİKLER ÜZERİNDE FIR

    h_k = c · Σ_{m=0}^{M−1} ρ^m · w_{k−m}
    w_n = normal_cekimi("sonumleme_i" | "sonumleme_q", tohum, i, j, n)
    ρ   = exp(−Δt / T_c)
    c   = 1 / √(Σ_{m=0}^{M−1} ρ^{2m})        ← varyansı TAM 1 yapar

`k` mutlak zamandan türer (`k = ⌊t/Δt⌋`), `w` yalnız `(bağ, indeks)`e bağlıdır.
Rastgele erişimli, sıra duyarsız, AR(1) ile aynı istatistik. Aynı tohumda iki
farklı protokol **birebir aynı** sönümleme izini görür — bu bir disiplin değil,
yapısal bir sonuçtur.

⚠️ NEDEN `c` GEREKLİ — kesme varyansı düşürür
=============================================
`√(1−ρ²)` ile ölçeklemek yalnız M → ∞ için doğrudur. Sonlu M'de varyans
`1−ρ^{2M}` olur; yavaş bağlarda (ρ → 1) bu 1'in çok altına iner ve sönümleme
ilan edilenden **sığ** olurdu. `c` ile marjinal varyans her ρ ve M için tam
olarak 1'dir. Bedeli: M·Δt'den uzun gecikmelerde otokorelasyon kesilir —
15,4 ms, yani ~7 çerçeve süresi. Çerçeve İÇİ korelasyon tamdır ve ölçülen
büyüklük odur.

🔒 PARÇA SÜRESİ ÖLÇÜLEREK SEÇİLDİ — KURAL: T_c(p99) / 4
=======================================================
Kural sabittir ve şudur: *en hızlı %1'lik bağda bile tutarlılık süresi DÖRT
örnekle çözülmeli.* Değer o kuraldan TÜRER, elle seçilmez.

⚠️ 8 Eylül 2026'da YENİDEN ÖLÇÜLDÜ. Hızlar 1/50 ölçeğe çekilince (K-101)
ve Doppler tam ölçek hızına bağlanınca T_c dağılımı değişti:

    eski ölçüm (26 m/s geometrik, Doppler ayrımı YOK)
        ortanca T_c 2,10 ms → çerçeve/T_c 1,06 · p99 0,97 ms → dt 240 µs
    yeni ölçüm (0,64 m/s geometrik → 31,8 m/s Doppler)
        ortanca T_c 1,663 ms → çerçeve/T_c **1,35**
        p95     T_c 0,887 ms → çerçeve/T_c **2,52**
        p99     T_c 0,764 ms → **dt = 191 µs**

Kanal bir çerçeve süresince ortancada ~1,4, p95'te ~2,5 kez değişiyor:
paket başına tek çekim yanlış olurdu. Çerçeve başına ~11,8 parça.
Üretici: `python kalibrasyon/adim4_sonumleme.py`

🔒 K-198 · İKİ ÜRETEÇ, TEK MODEL (`Konfig.sonumleme_uretec`)
===========================================================
`"tekil"`: her `w_n` bir blake2b özeti (`normal_cekimi`) — eski dünya,
birebir. `"blok"`: bağ başına bir blake2b anahtarı, `w_n` SplitMix64'ün
`n`inci çıktısından (`rng.normal_dizisi`), 64'lük bloklar numpy'de; FIR
I ve Q için tek matris çarpımı. Formül, ρ, M ve `c` AYNI; iki üreteç aynı
dağılımdan çeker, aynı sayıları değil. Referans dünyada `"blok"`:
birincil hücrede sönümleme koşunun ~%70'iydi (K-197).

🔒 STATİK KOLDA SÖNÜMLEME DONDURULUR
====================================
Hareket yoksa Doppler yoktur; hareketsiz bir geometride kanal zamanla
değişmez. Saçıcıların kendi hareketi modellenmediği için tutarlı olan şey
sönümlemeyi dondurmaktır. Ek olarak U1 sanity testi (*"statik + bağlı →
PDR ≈ 1"*) ancak böyle anlamlı kalır: çerçeveden çerçeveye bağımsız derin
fadingler PDR'yi taban sebepsiz aşağı çekerdi.
"""

from __future__ import annotations

import math

import numpy as np

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import blok_anahtari, normal_cekimi, normal_dizisi
from sim2.dunya.topoloji import Topoloji
from sim2.kanal.yayilim import ISIK_HIZI
from sim2.yapilandirma.konfig import Konfig

__all__ = ["FIR_EN_COK_KATSAYI", "BAGIL_HIZ_TABANI_MS", "YENILIK_ONBELLEK_SINIRI",
           "AGIRLIK_ONBELLEK_SINIRI", "BLOK_BOYU", "PENCERE_ONBELLEK_SINIRI",
           "Sonumleme"]

# FIR kesme sınırı. Marjinal varyans `c` ile düzeltildiği için bu sayı
# sönümlemenin DERİNLİĞİNİ değil, yalnız korelasyonun ne kadar uzağa
# taşındığını belirler: 64 × 240 µs = 15,4 ms ≈ 7 çerçeve.
FIR_EN_COK_KATSAYI: int = 64

# Bağıl hız tabanı. Sıfıra giden hız T_c'yi sonsuza götürür ve M'i patlatır.
# Taban, en yavaş bağın 15,4 ms'de dekorele olması demektir — kabul edilir,
# çünkü o bağ zaten çerçeve süresince sabittir.
#
# ⚠️ 8 Eylül 2026: hızlar 1/50 ölçeğe çekilince (K-101) bu taban bir anda
# BASKIN hâle geldi — ölçüldü, çiftlerin **%84,4'ünün** geometrik bağıl hızı
# 1,0 m/s'nin altına indi ve sönümleme uydurma bir hızla hesaplanmaya
# başladı. Taban artık DOPPLER hızına uygulanıyor (aşağıya bak) ve orada
# hız ~32 m/s olduğu için bir daha baskın olmuyor.
BAGIL_HIZ_TABANI_MS: float = 1.0

# 🔴 YENİLİK ÖNBELLEĞİNİN SINIRI — sınırsız hâli koşuyu KOŞULAMAZ yapıyordu
# =========================================================================
# Ölçüldü (5 Eylül 2026): hareketli bir kolda önbellek saniyede 372 000 –
# 405 000 girdi biriktiriyor ve girdi başına 190–193 bayt tutuyor. Tam
# uzunlukta (350 s) bir hareketli koşu ~25 GB ister; makinede 15,7 GB var.
# Yani 18 senaryonun 12'si — bütün hareketli kollar — koşulamıyordu.
#
# ⚠️ VE SORUN GÖRÜNMÜYORDU: statik kolda sönümleme donduğu için önbellek
# 1 530 girdide kalıyor. Bugüne kadarki bütün tam uzunluk ölçümleri statik
# koldaydı, dolayısıyla hiçbiri bu duvara çarpmadı.
#
# 🔒 SINIRLAMAK HİÇBİR DEĞERİ DEĞİŞTİREMEZ — bu ölçüm değil, YAPI.
# `_yenilik` saf bir fonksiyonun (`normal_cekimi(alan, tohum, i, j, indeks)`)
# memo'sudur: değer yalnız anahtara bağlıdır, çağrı sırasına değil. Bir
# girdiyi atmak onu yeniden HESAPLATIR, başka bir sayı üretmez.
# Yine de ölçülerek kanıtlandı, çünkü kanıtlanan şey matematik değil
# UYGULAMADIR: üç senaryoda (bagimsiz-yok · bagimsiz-surekli · statik-yok)
# ve üç sınırda (1 000 000 · 250 000 · 100 000) hem tam sonuç satırı hem ham
# teslim dizisi sınırsız hâlle BİREBİR aynı çıktı.
#
# 🔒 POLİTİKA: DOLUNCA TAMAMEN BOŞALT — `yayilim.KOSE_ONBELLEK_SINIRI` ile
# aynı desen. İki kuşaklı bir önbellek denendi: isabet oranına 0,1 puan
# katıyor ama iki sözlük tuttuğu ve tahliyede kopyaladığı için hem iki kat
# bellek hem ~%8 daha yavaş. Ölçülen ıskalama artışı — 1 000 000'de %0,09,
# 250 000'de %0,36, 100 000'de %0,88. Yani çalışma kümesi sınırın çok
# altında; sınırı büyütmenin alacağı bir şey yok.
#
# ⚠️ ÖNBELLEK KOŞUM BAŞINADIR ve öyle kalmalı: anahtar TOHUMU İÇERMEZ.
# Modül düzeyine taşınır ya da koşumlar arasında paylaşılırsa aynı anahtar
# farklı tohumda farklı değere karşılık gelir ve sessizce yanlış sonuç
# üretir. Paylaştırmak isteyen önce anahtara tohumu koymak zorundadır.
#
# 🔴 SINIRIN YETİP YETMEDİĞİ HER KOŞUDA RAPORLANIR (`onbellek_raporu`,
# sonuç satırının `teshis` bölümü). Çalışma noktası değişince (yol kaybı
# üsteli, hızlar) FIR uzar ve çalışma kümesi büyür; sınır bir gün yetmezse
# bedeli SESSİZ bir CPU kaybı olurdu. `tahliye` sayacı bunu görünür kılar:
# ıskalama ≈ tahliye × sınır + kalan girdi (ölçüldü, %0,4 sapıyor).
# Sayaç yalnız tahliyede artar (koşu başına ~30 kez), yani bedavadır —
# her çağrıda sayaç tutmanın bedeli %11 ölçüldü ve reddedildi.
#
# 🟢 KAPANIŞ: 350 s'lik hareketli bir koşu 1 262 s'de tamamlandı; önbellek
# 250 000 girdiyi hiç aşmadı (567 tahliye), korunum + mutabakat TAMAM.
# Bu, `sim2/`de yapılan İLK tam uzunluk hareketli koşusudur.
#
# Üretici: `python kalibrasyon/sonumleme_onbellegi.py`
YENILIK_ONBELLEK_SINIRI: int = 250_000

# FIR ağırlık önbelleğinin tavanı — performans, sonucu DEĞİŞTİREMEZ (saf
# memo, dolunca boşaltılır). Girdi başına ≤ 64 kayan nokta.
AGIRLIK_ONBELLEK_SINIRI: int = 20_000

# 🔒 K-198 · BLOK ÜRETECİ (`Konfig.sonumleme_uretec = "blok"`). Yenilikler
# `BLOK_BOYU`luk bloklarla üretilir; blok `b`nin PENCERESİ `[bB − B; bB + B)`
# indekslerini tutar, yani `k`de biten her FIR penceresi (en çok `B` dokunuş,
# `k ∈ [bB; bB + B)`) TEK bir pencerenin içindedir — birleştirme yok. Blok
# boyu FIR sınırına eşit olmak ZORUNDA (daha kısası bu garantiyi bozar).
BLOK_BOYU: int = FIR_EN_COK_KATSAYI

# Pencere önbelleğinin tavanı — saf memo, sonucu DEĞİŞTİREMEZ (dolunca
# boşaltılır, değer aynı indeksten aynı çıkar). Girdi ~2,3 KB (I ve Q ×
# 2B kayan nokta) → tavanda ~46 MB.
PENCERE_ONBELLEK_SINIRI: int = 20_000


class Sonumleme:
    """Rician sönümleme. Saf ve durumsuz; memo yalnız hızlandırır."""

    __slots__ = ("konfig", "topoloji", "_lambda", "_dt", "_acik",
                 "_k_lin", "_los", "_dagilan", "_memo", "_donuk",
                 "_sinir", "_tahliye", "_olcek", "_agirlik", "_blok",
                 "_pencereler", "_bag_anahtari", "_pencere_sinir", "_usler")

    def __init__(self, konfig: Konfig, topoloji: Topoloji) -> None:
        dogrula(konfig.sonumleme_parca_suresi_s > 0.0,
                "parça süresi pozitif olmalı")
        self.konfig = konfig
        self.topoloji = topoloji
        self._lambda = ISIK_HIZI / konfig.frekans_hz
        self._dt = konfig.sonumleme_parca_suresi_s
        # 🔴 Doppler TAM ÖLÇEK hızından — `tutarlilik_suresi_s`e bak.
        self._olcek = konfig.olcek
        self._acik = konfig.sonumleme_acik
        # Rician K — doğrudan görüş bileşeni ile dağılan bileşenin oranı.
        self._k_lin = 10.0 ** (konfig.rician_k_db / 10.0)
        self._los = math.sqrt(self._k_lin / (self._k_lin + 1.0))
        self._dagilan = math.sqrt(1.0 / (2.0 * (self._k_lin + 1.0)))
        # 🔒 Hareketsiz kolda sönümleme donar (modül başlığındaki nota bak).
        self._donuk = not topoloji.hareketli
        # (alan, i, j, indeks) → yenilik. SAF memo: bağımsızlığı bozmaz,
        # çünkü değer yalnız anahtara bağlı. Risk 1'in ilan edilmiş çözümü.
        # 🔴 SINIRLI — gerekçesi modül başlığında. Sınır kurulumda okunur,
        # koşu ortasında değişmez, ve sözlük KOŞUM BAŞINADIR: anahtar tohumu
        # içermediği için paylaşılan bir önbellek sessizce yanlış olurdu.
        self._memo: dict[tuple[str, int, int, int], float] = {}
        self._sinir = YENILIK_ONBELLEK_SINIRI
        self._tahliye = 0
        # (ρ, M) → (ağırlıklar, √Σ ağırlık²) — `_fir`in ağırlıkları. SAF memo
        # (performans, 28 Eylül 2026): değerler AYNI işlemlerle AYNI sırada
        # üretilir, yalnız tekrarlanmaz; aynı çağrıdaki I ve Q süzgeci aynı
        # (ρ, M)'yi paylaşır.
        self._agirlik: dict[tuple[float, int], tuple[tuple[float, ...],
                                                      float]] = {}
        # K-198 · blok üreteci. (i, j, blok) → (2, 2B) pencere [I; Q];
        # (i, j) → (2, 1) uint64 anahtar. İkisi de KOŞUM BAŞINA — anahtar
        # tohumu içerir ama pencere anahtarı içermez (aynı gerekçe).
        self._blok = konfig.sonumleme_uretec == "blok"
        self._pencereler: dict[tuple[int, int, int], np.ndarray] = {}
        self._bag_anahtari: dict[tuple[int, int], np.ndarray] = {}
        self._pencere_sinir = PENCERE_ONBELLEK_SINIRI
        # FIR ağırlıklarının üsleri, artan indeks sırasıyla: `k − m + 1 … k`
        # indeksinin ağırlığı `ρ^(m−1) … ρ^0` → `_usler[B − m:]`.
        self._usler = np.arange(BLOK_BOYU - 1, -1, -1, dtype=np.float64)

    # ------------------------------------------------------------ yardımcı
    def bagil_hiz_ms(self, i: int, j: int, t_s: float) -> float:
        """Bağın anlık bağıl hız büyüklüğü — Doppler'in kaynağı."""
        # 🔴 Yaklaşma/uzaklaşma hızı DEĞİL, göreli hareketin BÜYÜKLÜĞÜ.
        # Yanal hareket de Doppler yayılımı üretir; yalnız menzil değişimini
        # saymak, paralel uçan iki düğümü "sönümlemesiz" gösterirdi.
        h = 1e-3
        a0 = self.topoloji.konum(i, t_s)
        b0 = self.topoloji.konum(j, t_s)
        a1 = self.topoloji.konum(i, t_s + h)
        b1 = self.topoloji.konum(j, t_s + h)
        vx = ((a1.x - a0.x) - (b1.x - b0.x)) / h
        vy = ((a1.y - a0.y) - (b1.y - b0.y)) / h
        vz = ((a1.z - a0.z) - (b1.z - b0.z)) / h
        return math.sqrt(vx * vx + vy * vy + vz * vz)

    def tutarlilik_suresi_s(self, i: int, j: int, t_s: float) -> float:
        """T_c = 0,423 / f_d,  f_d = v / λ.  🔴 v TAM ÖLÇEK HIZIDIR.

        🔴 DALGA BOYU ÖLÇEKLENEMEZ — bu, ölçek modellemesinin klasik
        kısıtıdır ve beyan edilir.

        Simülatör 1:`olcek` geometrik bir ölçek modelidir. Mesafeler ve
        hızlar ölçeklenir; 2,4 GHz'in dalga boyu **ölçeklenemez**. Doppler
        `f_d = v/λ` olduğuna göre, ölçekli hızı kullanmak sönümlemeyi
        `olcek` kat yavaşlatır ve çerçeve içi kanal değişimini yok eder.

        Korunması gereken boyutsuz büyüklük *"kanal bir çerçeve süresince
        kaç kez değişiyor"*dur ve modülün kendi tasarım hedefi odur
        (ortancada ~1,06). Ölçüldü, 8 Eylül 2026:

            ölçekli hız (0,64 m/s) : T_c 83,1 ms · çerçeve/T_c **0,03**
            tam ölçek  (31,8 m/s)  : T_c  1,66 ms · çerçeve/T_c **1,35** ✔

        Ölçekli hız kullanılsaydı kanal çerçeve boyunca DONARDI: yeniden
        denemeler aynı derin fade'i görür, bağ olduğundan kötü ölçülürdü.

        🔒 Bu bir hile değil, ölçek modellemesinin standart uygulaması —
        aynı anda korunamayan iki benzerlikten ÖNEMLİ olanı korunur ve
        hangisinin feda edildiği yazılır. Burada feda edilen, sönümlemenin
        MUTLAK zaman ölçeğidir; korunan, çerçeveye GÖRE değişim hızıdır.
        """
        v = max(self.bagil_hiz_ms(i, j, t_s) * self._olcek,
                BAGIL_HIZ_TABANI_MS)
        return 0.423 * self._lambda / v

    def _yenilik(self, alan: str, i: int, j: int, indeks: int) -> float:
        """Bir yeniliğin değeri. Önbellek TAVANLIDIR — modül başlığına bak.

        🔒 Tahliye değeri değiştirmez, yeniden hesaplatır: dönen sayı
        `normal_cekimi`in saf çıktısıdır ve yalnız anahtara bağlıdır.
        """
        anahtar = (alan, i, j, indeks)
        deger = self._memo.get(anahtar)
        if deger is None:
            if len(self._memo) >= self._sinir:
                self._memo.clear()
                self._tahliye += 1
            deger = normal_cekimi(alan, self.konfig.tohum, i, j, indeks)
            self._memo[anahtar] = deger
        return deger

    def onbellek_raporu(self) -> dict[str, int]:
        """Teşhis — KARARA GİRMEZ, rapora girer.

        🔴 `iskalama` bir TAHMİNDİR: tahliye başına tavan kadar ıskalama
        olduğu varsayılır ve kalan girdi eklenir. Ölçüldü, gerçek değerden
        %0,4 sapıyor. Tam sayım her çağrıda bir sayaç ister ve %11 CPU'ya
        mal olur — 100 saatlik bir taramada 11 saat.
        """
        if self._blok:
            # K-198 · blok kipinde yenilik memo'su kullanılmaz; aynı dört
            # alan PENCERE önbelleğini anlatır (girdi = pencere).
            return {"sinir": self._pencere_sinir, "tahliye": self._tahliye,
                    "girdi": len(self._pencereler),
                    "iskalama_tahmini": self._tahliye * self._pencere_sinir
                    + len(self._pencereler)}
        return {"sinir": self._sinir, "tahliye": self._tahliye,
                "girdi": len(self._memo),
                "iskalama_tahmini": self._tahliye * self._sinir
                + len(self._memo)}

    def _agirliklar(self, ro: float, m: int
                    ) -> tuple[tuple[float, ...], float]:
        """FIR ağırlıkları `ρ^adım` ve `√Σ ağırlık²` — saf memo.

        🔒 BİREBİR (performans, 28 Eylül 2026): ağırlık eskiden olduğu gibi
        ardışık çarpımla (`ağırlık *= ρ`), kare toplamı aynı sırayla birikir
        — aynı kayan nokta sayıları. Tavan dolunca boşaltılır; değer aynı
        işlemle yeniden üretilir.
        """
        anahtar = (ro, m)
        a = self._agirlik.get(anahtar)
        if a is None:
            agirliklar = []
            agirlik = 1.0
            kare = 0.0
            for _ in range(m):
                agirliklar.append(agirlik)
                kare += agirlik * agirlik
                agirlik *= ro
            if len(self._agirlik) >= AGIRLIK_ONBELLEK_SINIRI:
                self._agirlik.clear()
            a = self._agirlik[anahtar] = (tuple(agirliklar), math.sqrt(kare))
        return a

    def _fir(self, alan: str, i: int, j: int, k: int, ro: float, m: int
             ) -> float:
        # 🔒 BİREBİR (performans, 28 Eylül 2026): toplam aynı ağırlıklarla
        # AYNI sırada birikir; önbellek isabetinde `_yenilik` çağrısı
        # atlanır (ıskalamada o çağrılır — tahliye davranışı aynı). Eskiden
        # her terim bir metot çağrısıydı ve ağırlıklar her çağrıda yeniden
        # üretiliyordu: birincil hücre profilinde sürenin %72'si buradaydı.
        agirliklar, kok = self._agirliklar(ro, m)
        al = self._memo.get
        toplam = 0.0
        for adim in range(m):
            deger = al((alan, i, j, k - adim))
            if deger is None:
                deger = self._yenilik(alan, i, j, k - adim)
            toplam += agirliklar[adim] * deger
        return toplam / kok

    def _pencere(self, i: int, j: int, blok: int) -> np.ndarray:
        """K-198 · `(2, 2B)` pencere: I ve Q yenilikleri, indeks
        `[blok·B − B; blok·B + B)`. Saf memo — tahliye değeri değiştirmez."""
        anahtar = (i, j, blok)
        p = self._pencereler.get(anahtar)
        if p is None:
            bag = self._bag_anahtari.get((i, j))
            if bag is None:
                tohum = self.konfig.tohum
                bag = self._bag_anahtari[(i, j)] = np.array(
                    [[blok_anahtari("sonumleme_i", tohum, i, j)],
                     [blok_anahtari("sonumleme_q", tohum, i, j)]],
                    dtype=np.uint64)
            if len(self._pencereler) >= self._pencere_sinir:
                self._pencereler.clear()
                self._tahliye += 1
            p = self._pencereler[anahtar] = normal_dizisi(
                bag, blok * BLOK_BOYU - BLOK_BOYU, 2 * BLOK_BOYU)
        return p

    def _fir_blok(self, i: int, j: int, k: int, ro: float, m: int
                  ) -> tuple[float, float]:
        """K-198 · `_fir`in blok karşılığı, I ve Q birlikte:
        `h_k = c · Σ_{a<m} ρ^a · w_{k−a}`, `c = 1/√Σ ρ^{2a}` — aynı model.
        `c` kapalı formdan (`(1 − ρ^{2m}) / (1 − ρ²)`); ρ = 0'da 1."""
        blok = k // BLOK_BOYU
        p = self._pencere(i, j, blok)
        bas = k - m + 1 - (blok * BLOK_BOYU - BLOK_BOYU)
        h = p[:, bas:bas + m] @ (ro ** self._usler[BLOK_BOYU - m:])
        kok = (1.0 if ro == 0.0 else
               math.sqrt((1.0 - ro ** (2 * m)) / (1.0 - ro * ro)))
        return float(h[0]) / kok, float(h[1]) / kok

    # ------------------------------------------------------------- ana API
    def guc_kazanci(self, i: int, j: int, t_s: float) -> float:
        """`|g|²` — ortalaması TAM 1 olan Rician güç kazancı.

        K → ∞'da sabit 1'e gider (kapanış ölçütü c); K = 0'da Rayleigh olur.
        """
        if not self._acik:
            return 1.0
        alt, ust = (i, j) if i <= j else (j, i)
        if self._donuk:
            k = 0
            ro = 0.0                       # tek çekim — zamanla değişmez
            m = 1
        else:
            k = int(math.floor(t_s / self._dt))
            tc = self.tutarlilik_suresi_s(alt, ust, t_s)
            ro = math.exp(-self._dt / tc)
            m = FIR_EN_COK_KATSAYI if ro >= 1.0 else min(
                FIR_EN_COK_KATSAYI,
                max(1, math.ceil(math.log(0.01) / (2.0 * math.log(ro)))))
        if self._blok:
            hi, hq = self._fir_blok(alt, ust, k, ro, m)
        else:
            hi = self._fir("sonumleme_i", alt, ust, k, ro, m)
            hq = self._fir("sonumleme_q", alt, ust, k, ro, m)
        gi = self._los + self._dagilan * hi
        gq = self._dagilan * hq
        return gi * gi + gq * gq

    def karistirici_kazanci(self, kimlik: int, dugum: int, t_s: float,
                            bagil_hiz_ms: float) -> float:
        """A6 (K-176) — karıştırıcı ↔ düğüm bağının Rician kazancı.

        Düğüm bağıyla AYNI model ve aynı hash alanları; tek fark bağıl
        hızın çağırandan gelmesi (karıştırıcının konumu topolojide yok) ve
        anahtarın ilk üyesinin karıştırıcı kimliği (negatif — düğüm
        çiftleriyle çakışmaz). İki uç da duruyorsa kanal donar.
        """
        if not self._acik:
            return 1.0
        if self._donuk and bagil_hiz_ms == 0.0:
            k, ro, m = 0, 0.0, 1
        else:
            k = int(math.floor(t_s / self._dt))
            v = max(bagil_hiz_ms * self._olcek, BAGIL_HIZ_TABANI_MS)
            ro = math.exp(-self._dt / (0.423 * self._lambda / v))
            m = FIR_EN_COK_KATSAYI if ro >= 1.0 else min(
                FIR_EN_COK_KATSAYI,
                max(1, math.ceil(math.log(0.01) / (2.0 * math.log(ro)))))
        if self._blok:
            hi, hq = self._fir_blok(kimlik, dugum, k, ro, m)
        else:
            hi = self._fir("sonumleme_i", kimlik, dugum, k, ro, m)
            hq = self._fir("sonumleme_q", kimlik, dugum, k, ro, m)
        gi = self._los + self._dagilan * hi
        gq = self._dagilan * hq
        return gi * gi + gq * gq

    def parca_sinirlari(self, bas_s: float, sure_s: float) -> tuple[float, ...]:
        """Çerçeveyi sönümleme ızgarasına göre parçalara böler.

        🔴 Çerçeve boyunca TEK bir kazanç kullanmak yanlış olurdu: ölçüldü,
        kanal bir çerçeve süresince ortancada 1,06, p95'te 1,98 kez değişiyor.
        Dönen sınırlar `[bas, …, bas+süre]` — girişim olayları `kanal/` içinde
        bunlara EKLENİR, burada değil.
        """
        dogrula(sure_s > 0.0, "çerçeve süresi pozitif olmalı")
        bitis = bas_s + sure_s
        sinirlar = [bas_s]
        ilk = int(math.floor(bas_s / self._dt)) + 1
        kenar = ilk * self._dt
        while kenar < bitis:
            sinirlar.append(kenar)
            kenar += self._dt
        sinirlar.append(bitis)
        return tuple(sinirlar)

    def parca_sayisi(self, sure_s: float) -> int:
        return len(self.parca_sinirlari(0.0, sure_s)) - 1
