"""
Mobilite — 3B Gauss-Markov, ve onun kapalı hâli olan sabit topoloji.

🔒 NEDEN GAUSS-MARKOV
=====================
Literatürün FANET için standart saydığı model. Random Waypoint elenmiştir ve
elenme gerekçesi ölçülmüş bir hatadır: RWP *"sonsuz ivme ve ani yön değişimi
gibi fiziksel olarak imkânsız davranışlar"* üretir ve ortalama hızı durağan bir
değere yakınsamaz — yani tarama sessizce başka bir şeyi ölçer.

    v_n = α·v_{n−1} + (1−α)·v̄ + √(1−α²)·σ·x_n

Aynı özyineleme hız, azimut ve pitch için ayrı ayrı koşar. `(v_n − v̄)`nin
otokorelasyonu tam olarak `α^k`dır; bu, modülün kapanış ölçütüdür.

🔴 ÜÇ AKIŞ AYRI
===============
Hız, azimut ve pitch yenilikleri **üç ayrı akıştan** çekilir. Tek akışta
olsalardı güncelleme sırası (hız → azimut → pitch) sonucu etkilerdi — oysa o
sıra bir modelleme kararı değil, bir yazım tercihidir.

🔒 YÖRÜNGE ÖNCEDEN HESAPLANIR
=============================
`konum(dugum, t)` **saf bir fonksiyon** olmak zorunda: kanal katmanı onu parça
başına, sıra dışı zamanlarda çağırır. Bu yüzden yörünge kurulumda tik
çözünürlüğünde hesaplanır ve tikler arası **doğrusal aradeğerleme** yapılır
(tik boyunca sabit hız — modelin kendi varsayımı). 40 düğüm × 700 tik = 28 000
nokta; bellek önemsiz, belirlenimcilik tam.

⚠️ MOBİLİTE BİR EKSENDİR
========================
`Sabit` kolu silinmez: literatürün U1 sanity testi (*"statik + bağlı →
PDR ≈ 1"*) yalnızca orada koşabilir.

🔴 BURADAKİ BAĞLANTILILIK TABLOSU KALDIRILDI — 9 Eylül 2026.
Eski tablo (*"statik %73,3 · mobil %82,4"*) iki kere çürüdü: üreticisi
kolun ESKİ adını kullandığı için aylardır **koşmuyordu**, ve ölçtüğü graf
280 m'lik teşhis diskiydi — K-096 o diskin veri yolunda hiçbir yeri
kapamadığını zaten ölçmüştü. Bugün aynı disk her iki kolda da %0,0 veriyor;
veri taşıyan kanal grafiğinde ise statik kol 270/270 anda TEK PARÇA.
Tam kayıt ve bugünkü sayılar `yapilandirma/senaryolar.py` başlığında.

🔒 Bu modülün kararlarından hiçbiri o tabloya dayanmıyordu: `Sabit` kolu
U1 için, `GaussMarkov3B` literatürün standardı olduğu için, `GorevTabanli3B`
ise ölçülen bir bağıl hız farkı için var. `Formasyon3B` (Y6, 11 Eylül 2026)
öğrenci onayıyla eklendi: yerleşim noktasında istasyon tutan sürü.
"""

from __future__ import annotations

import math
from typing import Protocol, Sequence

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import Akislar
from sim2.dunya.geometri import Kutu, Nokta3

__all__ = ["Mobilite", "Sabit", "GaussMarkov3B", "GorevTabanli3B",
           "Formasyon3B", "GecitliMobilite", "mobilite_kur"]


# ==========================================================================
# 🔴 SINIR DAVRANIŞI — 4 Eylül 2026'da ÖLÇÜMLE DÜZELTİLDİ
# ==========================================================================
# Yansıma tek başına YETMİYORDU ve bu ölçüldü. Yansıma ANLIK azimutu
# çeviriyordu ama Gauss-Markov özyinelemesi düğümü kendi sabit ORTALAMA
# yönüne geri çekiyor; o ortalama hâlâ duvarı gösteriyordu. Sonuç: düğümler
# duvara yapışıyordu.
#
#   30 tohum × 350 s, düzeltmeden ÖNCE
#     kenardan ortalama uzaklık   180 m  →   21 m   (düzgün dağılımda 166,7 m)
#     kenardan ortanca uzaklık    170 m  →    5 m
#     ortalama derece            7,2    → 11,2     (duvarda yığılma)
#     tam bağlı zaman oranı              %11,1     (en kötü tohum %0,9)
#     t = 350'de ortalama irtifa         117,0 m   (kutu tavanı 120 m)
#
# Ölçülecek olan şey karıştırma değil, **duvara yapışmış bir sürü** olurdu.
# Derecenin ARTIP bağlantılılığın DÜŞMESİ imzasıydı: yığılma yerel dereceyi
# büyütür, ağı ise kopuk kümelere böler.
#
# 🔒 ÇÖZÜM: yansımada ORTALAMA YÖN DE AYNALANIR.
# Anlık yön ile ortalama yön aynı dönüşümü görür; süreç duvara göre bakışımlı
# kalır ve hiçbir bölge ayrıcalıklı olmaz.
#
# ⚠️ ELENEN ALTERNATİF — "sınır marjı" (Camp–Boleng–Davies'in tarif ettiği
# ele alış: düğüm marja girince ortalama yön içeri çevrilir). İki biçimi de
# denendi ve ikisi de ÖLÇÜMLE elendi:
#   · geçici itme  → marj çizgisi bir ÇEKİM YÜZEYİ oluyor. Kenardan ortanca
#     uzaklık tam olarak marja oturdu (50→50,6 · 100→100,4 · 150→150,2 ·
#     200→200,0) ve derece 6,76'dan 11,93'e tırmandı.
#   · kalıcı çevirme → bu kez MERKEZE topluyor: kenardan ortalama uzaklık
#     192–218 m (düzgün 166,7) ve derece 8,39–10,20 (düzgün 7,27).
# Aynalama iki yapaylığın da dışında: ayarlanacak bir marj parametresi bile
# yok, dolayısıyla "marjı seçerek sonucu seçme" imkânı da yok.


# 🔒 İSTASYON TUTMA ZAMAN SABİTİ — türetilmiş bir seçim, ayar düğmesi değil.
# Üye istasyonuna bu zaman sabitiyle yaklaşır. 2 s, mobilite tikinin (0,5 s)
# dört katıdır: daha kısası tik çözünürlüğünde salınım üretir, daha uzunu
# üyeyi merkezin arkasında `hız × sabit` kadar geride bırakır (20 m/s'te
# 2 s → 40 m gecikme, grup yarıçapının altında).
ISTASYON_TUTMA_S: float = 2.0


def _istasyonlari_izle(*, baslangic: Sequence[Nokta3], hedef, kutu: Kutu,
                       rj, tik_sayisi: int, alfa: float, adim_s: float,
                       gurultu_ms: float, hiz_maks_ms: float
                       ) -> tuple[tuple[tuple[Nokta3, ...], ...], int]:
    """🔒 İSTASYON TUTMA — görev ve formasyon kollarının ORTAK fiziği.

    Düğüm kendi konumuna ve hızına sahiptir; `hedef(i, k)`nin verdiği
    istasyonuna `ISTASYON_TUTMA_S` zaman sabitiyle çekilir. Hız özyinelemesi
    Gauss-Markov'unkidir (`alfa`, `gurultu_ms`), hız zarfı `hiz_maks_ms`tir ve
    düğüm kutuda herkes gibi yansır. İki kol bu fiziği iki kez yazmaz
    (Y6'da görev kolundan buraya taşındı; görev kolunun satırları regresyonla
    birebir doğrulandı).

    Döner: `(iz, duvar_temasi)` — `duvar_temasi` yansıyan düğüm-tik sayısı.
    🔒 Gürültü çekim sırası tik → düğüm → eksen (x, y, z); değişirse aynı tohum
    başka bir yörünge verir.
    """
    n = len(baslangic)
    kok = math.sqrt(1.0 - alfa * alfa)
    p = list(baslangic)
    v = [[0.0, 0.0, 0.0] for _ in range(n)]
    iz: list[list[Nokta3]] = [[p[i]] for i in range(n)]
    temas = 0
    for k in range(1, tik_sayisi):
        for i in range(n):
            hdf = hedef(i, k)
            simdi = (p[i].x, p[i].y, p[i].z)
            for e in range(3):
                cekim = (hdf[e] - simdi[e]) / ISTASYON_TUTMA_S
                v[i][e] = (alfa * v[i][e] + (1.0 - alfa) * cekim
                           + kok * rj.gauss(0.0, gurultu_ms))
            # Düğüm kendi uçağının hız zarfını aşamaz.
            buyukluk = math.sqrt(v[i][0] ** 2 + v[i][1] ** 2 + v[i][2] ** 2)
            if buyukluk > hiz_maks_ms:
                olcek = hiz_maks_ms / buyukluk
                v[i][0] *= olcek
                v[i][1] *= olcek
                v[i][2] *= olcek
            yeni = Nokta3(p[i].x + v[i][0] * adim_s,
                          p[i].y + v[i][1] * adim_s,
                          p[i].z + v[i][2] * adim_s)
            if not kutu.icinde_mi(yeni):
                temas += 1
                x_ayna, y_ayna, z_ayna = kutu.ayna_ekseni(yeni)
                yeni, _, _ = kutu.yansit(yeni, 0.0, 0.0)
                if x_ayna:
                    v[i][0] = -v[i][0]
                if y_ayna:
                    v[i][1] = -v[i][1]
                if z_ayna:
                    v[i][2] = -v[i][2]
            p[i] = yeni
            iz[i].append(yeni)
    return tuple(tuple(satir) for satir in iz), temas


def _katla(deger: float, alt: float, ust: float) -> float:
    """`deger`i `[alt, ust]` aralığına YANSITARAK katlar — üçgen dalga.

    Formasyonun istasyon kayması için: kayan istasyon kenara gelince geri
    döner; kutuda ışınlanmaz ve kenarda yığılmaz. Saf fonksiyon.
    """
    genislik = ust - alt
    if genislik <= 0.0:
        return alt
    u = (deger - alt) % (2.0 * genislik)
    return alt + (u if u <= genislik else 2.0 * genislik - u)


def _sarmala(aci: float) -> float:
    """Açıyı `(−π, π]` aralığına indirger."""
    return (aci + math.pi) % (2 * math.pi) - math.pi


def _aci_farki(hedef: float, simdi: float) -> float:
    """En kısa yoldan `hedef − simdi`.

    🔴 Ham açı çıkarması yanlış olurdu: azimut +3,0 ve ortalama −3,0 iken
    doğrusal karışım kısa yolu (±π üzerinden 0,28 rad) değil UZUN yolu
    (0 üzerinden 6,0 rad) seçer ve düğüm hedefinden uzaklaşırken "hedefe
    yaklaşmış" olur.
    """
    return _sarmala(hedef - simdi)


class Mobilite(Protocol):
    """Düğüm konumunun zaman fonksiyonu."""

    hareketli: bool
    mobilite_kolu: str

    def konum(self, dugum: int, t_s: float) -> Nokta3: ...


# ==========================================================================
class Sabit:
    """Konumlar koşu boyunca değişmez — doğrulama ve U1 kolu."""

    __slots__ = ("_konumlar", "hareketli", "mobilite_kolu")

    def __init__(self, konumlar: Sequence[Nokta3]) -> None:
        self._konumlar = tuple(konumlar)
        self.hareketli = False
        self.mobilite_kolu = "statik"

    def konum(self, dugum: int, t_s: float) -> Nokta3:
        return self._konumlar[dugum]


# ==========================================================================
class GaussMarkov3B:
    """3B Gauss-Markov mobilite.

    Parametreler literatürün taktik İHA bandından:
        α = 0,85 · adım 0,5 s · hız U(10, 30) m/s
        pitch: ortalama **0**, σ = 0,05 rad (≈2,9°)

    🔴 ORTALAMA PİTCH 0,05'TEN 0'A ÇEKİLDİ — 4 Eylül 2026.
    0,05 rad'lık bir ORTALAMA, her düğümün KALICI olarak tırmanması demektir:
    v·sin(0,05) ≈ 1 m/s düşey hız. Tavanın etkisinden arınmış geniş bir bandda
    (0–5000 m) ölçüldü — 350 s'de ortalama irtifa sürüklenmesi:

        ortalama pitch 0,00 rad  →   +8 m
        ortalama pitch 0,05 rad  → +299 m

    Sürüklenme, dipol anten kararının dayandığı *"düz uçuş"* varsayımıyla
    çelişir. Ortalama 0 · σ = 0,05 ile tipik |pitch| ≈ 0,04 rad (2,3°):
    varsayım gerçekten sağlanıyor.

    ⚠️ DÜRÜSTLÜK NOTU — bu kusur tek başına ölçülemezdi.
    Düzeltmeden önceki kodda t = 350 s'de ortalama irtifa **117,0 m** (tavan
    120 m) çıkıyordu, yani irtifa boyutu çöküyordu. Ama o çöküş, sınır
    kusuruyla BİRLİKTE oluşuyordu: ortalama yön aynalanmadığı için tavana
    çarpan düğüm orada kalıyordu. Aynalama düzeltildikten sonra +0,05'lik
    ortalama pitch tek başına irtifayı çökertmiyor (ölçüldü: 72,6 ± 28,7 m
    ↔ sıfır ortalamada 68,4 ± 28,9 m) — testereli bir tarama üretiyor.
    Yani pitch kararı bir ÇÖKÜŞ düzeltmesi değil, bir VARSAYIM tutarlılığı
    kararıdır ve gerekçesi budur.
    """

    __slots__ = ("_kutu", "_adim_s", "_iz", "_tik_sayisi", "hareketli", "mobilite_kolu")

    def __init__(self, *, baslangic: Sequence[Nokta3], kutu: Kutu,
                 akislar: Akislar, kosu_bitis_s: float,
                 alfa: float = 0.85, adim_s: float = 0.5,
                 hiz_min_ms: float = 10.0, hiz_maks_ms: float = 30.0,
                 hiz_sigma_ms: float = 3.0,
                 azimut_sigma_rad: float = 0.3,
                 pitch_ort_rad: float = 0.0,
                 pitch_sigma_rad: float = 0.05) -> None:
        dogrula(0.0 <= alfa < 1.0, "alfa [0, 1) aralığında olmalı")
        dogrula(adim_s > 0.0, "mobilite adımı pozitif olmalı")
        self.hareketli = True
        self.mobilite_kolu = "bagimsiz"
        self._kutu = kutu
        self._adim_s = adim_s
        n = len(baslangic)
        # Son tik, koşu bitişini AŞMALI ki aradeğerleme sınırda kalmasın.
        self._tik_sayisi = int(math.ceil(kosu_bitis_s / adim_s)) + 2

        r_h = akislar["mobilite_hiz"]
        r_a = akislar["mobilite_azimut"]
        r_p = akislar["mobilite_pitch"]

        # Düğüm başına ORTALAMA yön: hepsi aynı yöne gitmesin.
        hiz_ort = [r_h.uniform(hiz_min_ms, hiz_maks_ms) for _ in range(n)]
        azimut_ort = [r_a.uniform(-math.pi, math.pi) for _ in range(n)]

        hiz = list(hiz_ort)
        azimut = list(azimut_ort)
        pitch = [pitch_ort_rad] * n
        # 🔒 Ortalama azimut ve pitch DÜĞÜM BAŞINA tutulur ve yansımada
        # ANLIK yönle birlikte aynalanır — sınır kuralının ikinci yarısı budur.
        pitch_ort = [pitch_ort_rad] * n

        kok = math.sqrt(1.0 - alfa * alfa)
        iz: list[list[Nokta3]] = [[p] for p in baslangic]
        p_simdi = list(baslangic)

        for _ in range(self._tik_sayisi - 1):
            for i in range(n):
                p_once = p_simdi[i]
                hiz[i] = (alfa * hiz[i] + (1 - alfa) * hiz_ort[i]
                          + kok * r_h.gauss(0.0, hiz_sigma_ms))
                # Hız negatife düşerse "geri uçmak" demek olur; modelde yön
                # azimutta taşınır, hız BÜYÜKLÜKTÜR.
                hiz[i] = abs(hiz[i])
                # 🔴 AÇI FARKI SARMALANIR. Ham açılarda doğrusal karışım,
                # azimut +3,0 ve ortalama −3,0 iken kısa yol (±π üzerinden
                # 0,28 rad) yerine UZUN yolu (0 üzerinden 6,0 rad) seçerdi —
                # düğüm hedefinden uzaklaşarak "hedefe yaklaşmış" olurdu.
                azimut[i] = _sarmala(
                    azimut[i] + (1 - alfa) * _aci_farki(azimut_ort[i], azimut[i])
                    + kok * r_a.gauss(0.0, azimut_sigma_rad))
                pitch[i] = (alfa * pitch[i] + (1 - alfa) * pitch_ort[i]
                            + kok * r_p.gauss(0.0, pitch_sigma_rad))

                yol = hiz[i] * adim_s
                yatay = yol * math.cos(pitch[i])
                yeni = Nokta3(p_once.x + yatay * math.cos(azimut[i]),
                              p_once.y + yatay * math.sin(azimut[i]),
                              p_once.z + yol * math.sin(pitch[i]))
                if not kutu.icinde_mi(yeni):
                    x_ayna, y_ayna, z_ayna = kutu.ayna_ekseni(yeni)
                    yeni, azimut[i], pitch[i] = kutu.yansit(
                        yeni, azimut[i], pitch[i])
                    # 🔴 ORTALAMA YÖN DE AYNALANIR. Yalnız anlık yön
                    # çevrilseydi özyineleme düğümü duvarı gösteren eski
                    # ortalamaya geri çeker ve düğüm duvara yapışırdı.
                    azimut_ort[i] = Kutu.aci_aynala(
                        azimut_ort[i], x_ayna, y_ayna)
                    if z_ayna:
                        pitch_ort[i] = -pitch_ort[i]
                p_simdi[i] = yeni
                iz[i].append(yeni)

        self._iz = tuple(tuple(satir) for satir in iz)

    # ------------------------------------------------------------------ okuma
    def konum(self, dugum: int, t_s: float) -> Nokta3:
        """Tikler arası doğrusal aradeğerleme — tik boyunca sabit hız."""
        if t_s <= 0.0:
            return self._iz[dugum][0]
        ham = t_s / self._adim_s
        k = int(ham)
        if k >= self._tik_sayisi - 1:
            return self._iz[dugum][self._tik_sayisi - 1]
        f = ham - k
        a = self._iz[dugum][k]
        b = self._iz[dugum][k + 1]
        return Nokta3(a.x + f * (b.x - a.x),
                      a.y + f * (b.y - a.y),
                      a.z + f * (b.z - a.z))

    def tik_konumlari(self, dugum: int) -> tuple[Nokta3, ...]:
        """Doğrulama için ham tik dizisi (aradeğerlemesiz)."""
        return self._iz[dugum]

    @property
    def tik_sayisi(self) -> int:
        return self._tik_sayisi


# ==========================================================================
class GorevTabanli3B:
    """Görev tabanlı grup mobilitesi — koordineli sürü.

    🔴 NEDEN VAR
    ============
    Bağımsız Gauss-Markov'da her İHA kendi rastgele yönünü seçer; kimse
    kimseyle koordine değildir. Ölçüldü — komşular arası bağıl hız **26,0 m/s**
    (mümkün olan en yüksek değer) ve çok atlamalı bir rotanın ömrü **2,4 s**.
    Gerçek bir operasyonda 40 İHA 40 ayrı yöne gitmez: bir sektörü tutar, bir
    tarama yapar, bir hedefi izler — yani **birlikte** hareket eder.

    ÖLÇÜLEN KAZANÇ (kalibre edilmiş parametrelerle, bağımsız kola göre):
        bağıl hız 0,66× · bağ ömrü 0,78× · rota ömrü **1,24×**
    Ilımlı, ve sebebi ölçütün kendisi — derece eşitleme kısıtı müfrezeleri
    gevşek olmaya zorluyor. Ayrıntı `yapilandirma/senaryolar.py`de.
    Üretici: `python kalibrasyon/mobilite_gercekcilik.py`

    🔒 YAPI (RPGM — Referans Noktası Grup Mobilitesi ruhunda)
    ========================================================
      · `grup_sayisi` müfreze. Her müfrezenin bir GÖREV MERKEZİ var ve o
        merkez, bağımsız kolun kullandığı **aynı Gauss-Markov koduyla**
        alanda dolaşıyor. Tek fizik, tek kod yolu — ikinci bir hareket
        modeli yazılmıyor.
      · Üyeler merkezin çevresinde bir İSTASYON tutuyor (küre içinde düzgün,
        yarıçap `grup_yaricapi_m`).
      · Üyeler istasyonlarının çevresinde küçük, kendilerine ait bir titreşim
        yapıyor — formasyon rijit değil. Rijit olsaydı kol, kayan bir
        başlangıç noktasıyla STATİK koldan ibaret olurdu.

    🔒 İKİ TÜRETİLMİŞ BÜYÜKLÜK — ayar düğmesi DEĞİL
    ===============================================
      · **Dikey yarıçap = yatayın dörtte biri.** Hava formasyonları yatıktır;
        100 m'lik bir irtifa bandında 400 m yatay yayılımlı bir formasyona
        400 m dikey vermek fiziksel olarak anlamsız olurdu.
      · **Merkezler daraltılmış bir kutuda dolaşır** (her kenardan yarıçap
        kadar içeride). Üyeleri kelepçelemek yerine bu seçildi: kelepçeleme
        onları duvarda yığar ve bağımsız kolda düzeltilen kusuru geri getirir.

    ⚠️ ÜÇ KOL AYNI t=0 YERLEŞİMİNİ PAYLAŞAMAZ
    =========================================
    "Formasyonda" ile "düzgün rastgele" farklı dağılımlardır. Kolları
    karşılaştırılabilir yapan şey yerleşimin aynılığı değil, YOĞUNLUĞUN
    eşitliğidir — parametreler bu yüzden ortalama dereceyi eşitleyecek biçimde
    seçilir. Ölçüt `yapilandirma/senaryolar.py`de, taramadan ÖNCE ilan edildi.
    """

    __slots__ = ("_iz", "_adim_s", "_tik_sayisi", "hareketli", "mobilite_kolu",
                 "grup_of", "sektor_kokeni")

    def __init__(self, *, dugum_sayisi: int, kutu: Kutu, akislar: Akislar,
                 kosu_bitis_s: float, grup_sayisi: int = 8,
                 grup_yaricapi_m: float = 100.0,
                 jitter_hiz_ms: float = 2.0,
                 alfa: float = 0.85, adim_s: float = 0.5,
                 hiz_min_ms: float = 10.0, hiz_maks_ms: float = 30.0,
                 hiz_sigma_ms: float = 3.0,
                 azimut_sigma_rad: float = 0.3,
                 pitch_ort_rad: float = 0.0,
                 pitch_sigma_rad: float = 0.05) -> None:
        dogrula(grup_sayisi >= 1, "en az bir müfreze gerekli")
        dogrula(grup_sayisi <= dugum_sayisi,
                "müfreze sayısı düğüm sayısını aşamaz")
        dogrula(grup_yaricapi_m > 0.0, "grup yarıçapı pozitif olmalı")
        dogrula(jitter_hiz_ms >= 0.0, "titreşim hızı negatif olamaz")
        self.hareketli = True
        self.mobilite_kolu = "gorev"
        self._adim_s = adim_s

        # 🔒 TÜRETİLMİŞ, ayar düğmesi değil: formasyon yatıktır ve dikey
        # yayılımı hem yatay yayılımın hem de irtifa bandının dörtte birini
        # aşamaz. İkinci kelepçe olmasaydı 300 m yarıçaplı bir formasyon
        # 100 m'lik bir bandda 150 m dikey yayılım isterdi — imkânsız.
        bant = kutu.yukseklik_m - kutu.taban_m
        yaricap_dikey = min(grup_yaricapi_m, bant) / 4.0
        dogrula(2.0 * grup_yaricapi_m < min(kutu.en_m, kutu.boy_m),
                "grup çapı alandan büyük olamaz")
        dogrula(2.0 * yaricap_dikey < bant,
                "grup dikey çapı irtifa bandından büyük olamaz")

        # --- müfreze merkezleri: TAM kutuda, aynı GM koduyla ---------------
        # 🔴 İLK YAZIMDA MERKEZLER DARALTILMIŞ BİR KUTUDA DOLAŞIYORDU
        # (her kenardan yarıçap kadar içeride), ki üyeler kutunun dışına
        # taşmasın. Tarama bunu ölçümle çürüttü: daraltma etkin alanı
        # ρ = 150 m'de %49'a, ρ = 350 m'de **%9'a** indiriyor ve sürüyü
        # sıkıştırıyordu. Ortalama derece 14,8–20,4 çıktı (hedef 7,45) ve
        # ilan edilmiş ölçütü HİÇBİR aday geçemedi. Ölçülen şey
        # koordinasyon değil, alanın küçültülmesiydi — 3B'ye geçerken
        # yaşanan tuzağın aynısı.
        # 🔒 HER MÜFREZE BİR SEKTÖR TUTAR — modelin görev yapısı budur.
        # Serbest dolaşan merkezler de ölçümle elendi: 8 müfreze 1000×1000'de
        # bağımsız dolaşınca rastgele üst üste biniyor ve ortalama derece
        # 10–17 arasında geziniyordu (hedef 7,45). Bir gözetleme görevinde
        # müfrezeler üst üste binmez; harekât alanı bölüşülür. Sektör, "dış
        # dünyaya göre hareket"in modeldeki karşılığıdır: müfrezenin nereye
        # gideceğini rastgelelik değil, GÖREVİ belirler.
        sutun = math.ceil(math.sqrt(grup_sayisi))
        satir = math.ceil(grup_sayisi / sutun)
        sektor_en = kutu.en_m / sutun
        sektor_boy = kutu.boy_m / satir
        sektor_kutu = Kutu(sektor_en, sektor_boy,
                           yukseklik_m=kutu.yukseklik_m, taban_m=kutu.taban_m)
        self.sektor_kokeni = tuple(
            ((g % sutun) * sektor_en, (g // sutun) * sektor_boy)
            for g in range(grup_sayisi))

        rm = akislar["gorev_merkez"]
        merkez_baslangic = [
            Nokta3(rm.uniform(0.0, sektor_en), rm.uniform(0.0, sektor_boy),
                   rm.uniform(kutu.taban_m, kutu.yukseklik_m))
            for _ in range(grup_sayisi)]
        yerel = GaussMarkov3B(
            baslangic=merkez_baslangic, kutu=sektor_kutu, akislar=akislar,
            kosu_bitis_s=kosu_bitis_s, alfa=alfa, adim_s=adim_s,
            hiz_min_ms=hiz_min_ms, hiz_maks_ms=hiz_maks_ms,
            hiz_sigma_ms=hiz_sigma_ms, azimut_sigma_rad=azimut_sigma_rad,
            pitch_ort_rad=pitch_ort_rad, pitch_sigma_rad=pitch_sigma_rad)
        self._tik_sayisi = yerel.tik_sayisi
        # Sektör yereli → dünya koordinatı.
        merkez_izi = tuple(
            tuple(Nokta3(p.x + self.sektor_kokeni[g][0],
                         p.y + self.sektor_kokeni[g][1], p.z)
                  for p in yerel.tik_konumlari(g))
            for g in range(grup_sayisi))

        # --- üye istasyonları: küre içinde DÜZGÜN -------------------------
        ri = akislar["gorev_istasyon"]
        self.grup_of = tuple(i % grup_sayisi for i in range(dugum_sayisi))
        istasyon: list[tuple[float, float, float]] = []
        for _ in range(dugum_sayisi):
            # 🔴 Yarıçap KÜP KÖKLE ölçeklenir. Düz `uniform` olsaydı üyeler
            # merkeze yığılır ve "grup yarıçapı" ilan edilen şeyi anlatmazdı.
            u = ri.random() ** (1.0 / 3.0)
            aci = ri.uniform(-math.pi, math.pi)
            kos = ri.uniform(-1.0, 1.0)
            sin = math.sqrt(max(0.0, 1.0 - kos * kos))
            istasyon.append((grup_yaricapi_m * u * sin * math.cos(aci),
                             grup_yaricapi_m * u * sin * math.sin(aci),
                             yaricap_dikey * u * kos))

        # --- üyeler: İSTASYONA UÇARLAR, oraya yerleştirilmezler -----------
        # 🔒 Üye kendi konumuna ve hızına sahip; istasyonuna doğru
        # `ISTASYON_TUTMA_S` zaman sabitiyle çekiliyor ve kutuda herkes gibi
        # yansıyor. Rijit yerleştirme yerine bu seçildi çünkü:
        #   · konum SÜREKLİ kalır (kanal onu parça başına örnekliyor),
        #   · üye kutudan taşamaz, dolayısıyla merkezleri daraltmaya —
        #     yani alanı küçültmeye — gerek kalmaz,
        #   · rijit formasyon kolu, kayan bir başlangıç noktasıyla STATİK
        #     koldan ibaret yapardı.
        rj = akislar["gorev_jitter"]
        p = [Nokta3(
            min(max(merkez_izi[self.grup_of[i]][0].x
                    + istasyon[i][0], 0.0), kutu.en_m),
            min(max(merkez_izi[self.grup_of[i]][0].y
                    + istasyon[i][1], 0.0), kutu.boy_m),
            min(max(merkez_izi[self.grup_of[i]][0].z
                    + istasyon[i][2], kutu.taban_m), kutu.yukseklik_m))
            for i in range(dugum_sayisi)]

        def hedef(i: int, k: int) -> tuple[float, float, float]:
            m = merkez_izi[self.grup_of[i]][k]
            dx, dy, dz = istasyon[i]
            return (m.x + dx, m.y + dy, m.z + dz)

        # 🔒 Fizik formasyon koluyla ORTAK (`_istasyonlari_izle`).
        self._iz, _ = _istasyonlari_izle(
            baslangic=p, hedef=hedef, kutu=kutu, rj=rj,
            tik_sayisi=self._tik_sayisi, alfa=alfa, adim_s=adim_s,
            gurultu_ms=jitter_hiz_ms, hiz_maks_ms=hiz_maks_ms)

    def konum(self, dugum: int, t_s: float) -> Nokta3:
        """Tikler arası doğrusal aradeğerleme — bağımsız kolla aynı kural."""
        if t_s <= 0.0:
            return self._iz[dugum][0]
        ham = t_s / self._adim_s
        k = int(ham)
        if k >= self._tik_sayisi - 1:
            return self._iz[dugum][self._tik_sayisi - 1]
        f = ham - k
        a, b = self._iz[dugum][k], self._iz[dugum][k + 1]
        return Nokta3(a.x + f * (b.x - a.x), a.y + f * (b.y - a.y),
                      a.z + f * (b.z - a.z))

    def tik_konumlari(self, dugum: int) -> tuple[Nokta3, ...]:
        return self._iz[dugum]


# ==========================================================================
class GecitliMobilite:
    """Yere toplama: geçit düğümü sabit bir istasyonda, öteki düğümler iç modelde.

    Şartname: `v2/07-SIMULATOR-TASARIMI.md` §18 Y4. Geçit, sürü çerçevesinde
    konum tutan röle İHA'dır; koşu boyunca yeri değişmez.

    🔒 İÇ MODELİN ÇEKİMLERİ DEĞİŞMEZ. Geçidin yerleşim ve yörünge çekimleri,
    kullanılmasa da, iç modelde eskisi gibi tüketilir. Düğümler birbirinden
    bağımsız evrildiği için öteki düğümlerin yörüngeleri aynı tohumdaki eşler
    arası kolla BİREBİR aynıdır; iki desen aynı dünyada karşılaştırılır.
    """

    __slots__ = ("_ic", "_gecit", "_nokta", "hareketli", "mobilite_kolu")

    def __init__(self, ic: Mobilite, gecit: int, nokta: Nokta3) -> None:
        self._ic = ic
        self._gecit = gecit
        self._nokta = nokta
        self.hareketli = ic.hareketli
        self.mobilite_kolu = ic.mobilite_kolu

    def konum(self, dugum: int, t_s: float) -> Nokta3:
        if dugum == self._gecit:
            return self._nokta
        return self._ic.konum(dugum, t_s)

    def tik_konumlari(self, dugum: int) -> tuple[Nokta3, ...]:
        """Doğrulama için: iç modelin tik dizisi; geçit için sabit nokta."""
        iz = self._ic.tik_konumlari(dugum)
        return (self._nokta,) * len(iz) if dugum == self._gecit else iz


# ==========================================================================
class Formasyon3B:
    """Formasyon — her düğüm yerleşimdeki noktasını İSTASYON olarak tutar.

    Şartname: `v2/07-SIMULATOR-TASARIMI.md` §18 Y6 (öğrenci onayı 11 Eylül
    2026). Kutu sürüyle birlikte hareket eden gözlem çerçevesi olduğu için
    (`Konfig.olcek`) sürünün ortak hareketi ağa görünmez; görünen şey düğümün
    istasyonu çevresindeki manevrasıdır.

    🔒 YENİ SERBEST SAYI YOK
    ========================
      · istasyon = yerleşim çekimi → t = 0 konumları statik kolla AYNI,
        yoğunluk eşit, derece eşitlemesi gerekmez (görev kolunun aksine)
      · tutma zaman sabiti `ISTASYON_TUTMA_S`; fizik görev koluyla ortak
        (`_istasyonlari_izle`)
      · manevra gürültüsü araç dinamiğinin türetilmiş iki sayısından:
        `gm_alfa` ve `gm_hiz_sigma_ms`

    🔒 ÇEKİM SIRASI — `formasyon_jitter`
    ====================================
    Önce düğüm başına kayma yönü (kayma sıfır olsa da çekilir), sonra tik →
    düğüm → eksen gürültüsü. Yön çekimi kaymadan bağımsız olduğu için
    `istasyon_kayma_hiz_ms` oynatıldığında gürültü dizisi aynı kalır.

    ⚠️ DUVAR TEMASI SIFIR DEĞİL — ölçüldü (`v2/04` K-118). İstasyonu tabana
    ya da tavana birkaç metreden yakın düşen düğüm, manevra gürültüsüyle
    arada bir sınıra değer ve yansır. `duvar_temasi` bu düğüm-tik sayısıdır.
    """

    __slots__ = ("_iz", "_adim_s", "_tik_sayisi", "_istasyon", "_kutu",
                 "_kayma_hiz_ms", "_kayma_yonu", "duvar_temasi", "hareketli",
                 "mobilite_kolu")

    def __init__(self, *, baslangic: Sequence[Nokta3], kutu: Kutu,
                 akislar: Akislar, kosu_bitis_s: float,
                 alfa: float = 0.85, adim_s: float = 0.5,
                 hiz_maks_ms: float = 30.0, hiz_sigma_ms: float = 3.0,
                 kayma_hiz_ms: float = 0.0) -> None:
        dogrula(0.0 <= alfa < 1.0, "alfa [0, 1) aralığında olmalı")
        dogrula(adim_s > 0.0, "mobilite adımı pozitif olmalı")
        dogrula(kayma_hiz_ms >= 0.0, "istasyon kayma hızı negatif olamaz")
        self.hareketli = True
        self.mobilite_kolu = "formasyon"
        self._adim_s = adim_s
        self._kutu = kutu
        # Son tik, koşu bitişini AŞMALI ki aradeğerleme sınırda kalmasın.
        self._tik_sayisi = int(math.ceil(kosu_bitis_s / adim_s)) + 2
        self._istasyon = tuple(baslangic)
        self._kayma_hiz_ms = kayma_hiz_ms
        rj = akislar["formasyon_jitter"]
        self._kayma_yonu = tuple(
            (math.cos(a), math.sin(a))
            for a in [rj.uniform(-math.pi, math.pi) for _ in self._istasyon])
        self._iz, self.duvar_temasi = _istasyonlari_izle(
            baslangic=self._istasyon,
            hedef=lambda i, k: self._istasyon_xyz(i, k * adim_s),
            kutu=kutu, rj=rj, tik_sayisi=self._tik_sayisi, alfa=alfa,
            adim_s=adim_s, gurultu_ms=hiz_sigma_ms, hiz_maks_ms=hiz_maks_ms)

    def _istasyon_xyz(self, dugum: int, t_s: float
                      ) -> tuple[float, float, float]:
        b = self._istasyon[dugum]
        if self._kayma_hiz_ms == 0.0:
            return (b.x, b.y, b.z)
        yol = self._kayma_hiz_ms * max(t_s, 0.0)
        cos_a, sin_a = self._kayma_yonu[dugum]
        return (_katla(b.x + yol * cos_a, 0.0, self._kutu.en_m),
                _katla(b.y + yol * sin_a, 0.0, self._kutu.boy_m), b.z)

    def istasyon_konumu(self, dugum: int, t_s: float) -> Nokta3:
        """Düğümün `t_s` anındaki istasyonu — saf fonksiyon; kapılar ve teşhis."""
        return Nokta3(*self._istasyon_xyz(dugum, t_s))

    def konum(self, dugum: int, t_s: float) -> Nokta3:
        """Tikler arası doğrusal aradeğerleme — öteki kollarla aynı kural."""
        if t_s <= 0.0:
            return self._iz[dugum][0]
        ham = t_s / self._adim_s
        k = int(ham)
        if k >= self._tik_sayisi - 1:
            return self._iz[dugum][self._tik_sayisi - 1]
        f = ham - k
        a, b = self._iz[dugum][k], self._iz[dugum][k + 1]
        return Nokta3(a.x + f * (b.x - a.x), a.y + f * (b.y - a.y),
                      a.z + f * (b.z - a.z))

    def tik_konumlari(self, dugum: int) -> tuple[Nokta3, ...]:
        return self._iz[dugum]

    @property
    def tik_sayisi(self) -> int:
        return self._tik_sayisi


# ==========================================================================
def mobilite_kur(*, kol: str, baslangic: Sequence[Nokta3],
                 kutu: Kutu, akislar: Akislar, kosu_bitis_s: float,
                 grup_sayisi: int = 8, grup_yaricapi_m: float = 100.0,
                 jitter_hiz_ms: float = 2.0,
                 istasyon_kayma_hiz_ms: float = 0.0, **gm) -> Mobilite:
    """🔒 Mobilite bir KONFİGÜRASYON BAYRAĞIDIR, kod düzenlemesi değil.

    Kod düzenlemesiyle üretilen bir kol kaynağından ayırt edilemez —
    kaybolmuş bir deneydir.
    """
    if kol == "statik":
        return Sabit(baslangic)
    if kol == "bagimsiz":
        return GaussMarkov3B(baslangic=baslangic, kutu=kutu, akislar=akislar,
                             kosu_bitis_s=kosu_bitis_s, **gm)
    if kol == "gorev":
        return GorevTabanli3B(
            dugum_sayisi=len(baslangic), kutu=kutu, akislar=akislar,
            kosu_bitis_s=kosu_bitis_s, grup_sayisi=grup_sayisi,
            grup_yaricapi_m=grup_yaricapi_m, jitter_hiz_ms=jitter_hiz_ms, **gm)
    if kol == "formasyon":
        # Yalnız istasyon tutmanın kullandığı araç dinamiği sayıları geçer.
        return Formasyon3B(
            baslangic=baslangic, kutu=kutu, akislar=akislar,
            kosu_bitis_s=kosu_bitis_s, kayma_hiz_ms=istasyon_kayma_hiz_ms,
            **{a: gm[a] for a in ("alfa", "adim_s", "hiz_maks_ms",
                                  "hiz_sigma_ms") if a in gm})
    raise ValueError(f"bilinmeyen mobilite kolu: {kol!r}")
