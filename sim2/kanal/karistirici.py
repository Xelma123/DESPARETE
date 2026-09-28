"""
Karıştırıcı — beş sınıf. İkisi mimariyi değiştiriyor.

🔴 KARIŞTIRICI ZAMANIN SAF FONKSİYONU DEĞİL
===========================================
Eski simülatörde karıştırıcı `guc(t)` idi: zamanın saf bir fonksiyonu.
İki sınıf bunu kırıyor ve tasarım buna göre yapıldı:

  · **reaktif** — kanalı dinler; enerji sürdükçe sezer (16 µs) ve patlar
    (144 µs), sonra yeniden sezer. Yani ORTAMA bağlıdır, saatine değil.
  · **aldatıcı** — geçerli görünümlü önbelge basar. Taşıyıcı dinleme onu
    MEŞGUL görmek zorundadır; eski *"karıştırıcı CSMA'yı tetiklemez"* beyanı
    bu sınıf için kalkar.

🔒 REAKTİF KARIŞTIRICININ RASTGELELİĞİ HASH'TEN
===============================================
Sezme başarısı `reaktif_sezme` HASH alanından çekilir, sıralı akıştan değil.
Sebebi ölçülebilir: bir koşuda kaç iletim olduğu PROTOKOLE göre değişir.
Sıralı bir akış olsaydı, çok iletim yapan protokol akışı ileri kaydırır ve
karıştırıcı kollar arasında farklı davranırdı — karşılaştırma yapısal olarak
kırılırdı.

🔒 GÜÇ EŞİTLEMESİ — hangi sınıf neyi eşitliyor, AÇIKÇA
======================================================
  · `surekli_darbeli` **ortalama gücü** `surekli` ile eşitler (tepe telafisi
    `Konfig.tepe_telafisi_db`den türetilir). Sorduğu soru: *aynı ortalama
    güçte darbeli olmak fark eder mi?*
  · `taramali` **tepe gücü** eşit tutar; ortalaması konak sayısına bölünür.
    Sorduğu soru farklıdır: *aynı vericiyle kanallar arasında gezinen bir
    karıştırıcı ne yapar?* Ortalamayı da eşitlemek onu darbelinin kopyası
    yapardı ve sınıf gereksizleşirdi.
Bu ayrım BEYAN EDİLİR; ön-kayıtta hipotezler buna göre yazılır.

🟢 GÜÇLER ÖLÇÜLDÜ — 8 Eylül 2026
================================
`senaryolar.KARISTIRICI_GUCU_DBM` beş sınıfta da **−15,0 dBm** taban
gücündedir. Nokta REFERANS sınıfta (`surekli`) seçildi — zaman yapısı
olmayan tek sınıf odur — ve ölçüt şuydu: 30 tohumun hiçbirinde birden fazla
çok üyeli bileşen yokken ρ (engellenen bağ oranı) en büyük. ρ = 0,258.
Üretici: `python kalibrasyon/karistirici_gucu.py`

🔴 Sınıflara AYRI güç verilmedi: her sınıfa aynı ρ'yu verdirmek, ρ bağımlı
değişken olduğu için aradığımız mekanizma farkını kalibrasyonla SİLMEK
olurdu. Eşitleme yukarıdaki gibi yayılan ORTALAMA güç üzerindendir ve
ölçülerek doğrulandı: sürekli −15,00 · darbeli −15,00 · aldatıcı −15,10 ·
taramalı −19,88 dBm (son satır beyan edilmiş asimetri).

🔒 Kapı KALKMADI: tablo yeni bir sınıf için `None` kalırsa koşum yine durur.
Sessizce bir varsayılan güç kullanmak, çalışma noktasını ölçmeden seçmektir.

🔒 Y5a · ÇOKLU VE HAREKETLİ KARIŞTIRICI MEKANİZMASI — 11 Eylül 2026
====================================================================
Şartname: `v2/07-SIMULATOR-TASARIMI.md` §05.3 · §18 Y5. Bir karıştırıcı artık
bir `KaristiriciTanimi`dan da kurulabilir: platform × yörünge × yayın düzeni ×
sınıf × güç payı. Birden çok tanım `KaristiriciKumesi` olur ve tek
karıştırıcının arayüzünü AYNEN sunar. Aileler (Y5b) `kanal/tehdit.py`de
tanımlıdır (öğrenci kararları 11 Eylül 2026, `v2/04` K-119); tanım
verilmediğinde `karistirici_kur` bugünkü tek merkez karıştırıcıyı birebir
kurar.

  · Konum ve yayın çizelgesi zamanın SAF fonksiyonudur; rastgelelik yok.
  · Gölgeleme kimliği üye başına `-(indeks + 1)`; ilk üye bugünkü `-1`.
  · Aynı sınıftan birden çok üyenin hash çekimleri bağımsızdır: indeks > 0
    ise anahtara eklenir, ilk üyenin anahtarı bugünküyle aynı kalır.
  · Taşıyıcı dinleme yalnız CSMA'ya görünen üyelerin gücüne bakar
    (`csma_guc_w`); tek karıştırıcıda eski iki adımlı denetimle aynıdır.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Protocol

from sim2.cekirdek.degismezler import asla, dogrula
from sim2.cekirdek.rng import hash_cekimi
from sim2.dunya.geometri import Nokta3
from sim2.dunya.topoloji import Topoloji
from sim2.kanal.cerceve import cerceve_kur
from sim2.kanal.girisim import Ortam
from sim2.kanal.yayilim import Yayilim, dbm_to_w
from sim2.kanal.yer_hava import YerHavaKanali
from sim2.yapilandirma.konfig import Konfig

__all__ = ["Karistirici", "KaristiriciTabani", "Surekli", "Darbeli",
           "Reaktif", "Aldatici", "Taramali", "Yorunge", "Yayin",
           "KaristiriciTanimi", "KaristiriciKumesi", "karistirici_kur"]


class Karistirici(Protocol):
    sinif: str
    # 🔒 SINIF DÜZEYİNDE BEYAN. `csma_ya_gorunur(t)` ANLIK durumu söyler;
    # bu bayrak sınıfın taşıyıcı dinlemeyi HİÇ tetikleyip tetiklemediğini.
    # İkisi ayrı sorudur: geri çekilme donması, karıştırıcının kapalı olduğu
    # anlarda bile "bu sınıf beni dondurabilir mi" bilgisine ihtiyaç duyar ve
    # bunu her seferinde geçiş anlarını tarayarak sormak pahalıdır.
    csma_gorunur: bool

    def alinan_guc_w(self, alici: int, alici_konum: Nokta3,
                     t_s: float) -> float: ...

    def csma_guc_w(self, alici: int, alici_konum: Nokta3,
                   t_s: float) -> float: ...

    def csma_ya_gorunur(self, t_s: float) -> bool: ...

    def gecis_anlari(self, bas_s: float, bitis_s: float
                     ) -> tuple[float, ...]: ...

    def sahte_cerceveler(self, dugum: int, dugum_konum: Nokta3, t_s: float
                         ) -> tuple[tuple[float, float, int], ...]: ...

    @property
    def hareketli(self) -> bool:
        """Konumu zamanla değişiyor mu — A3 yeniden denetimi (K-174)."""
        ...


# ==========================================================================
# Y5a · TANIM
# ==========================================================================
_PLATFORMLAR: tuple[str, ...] = ("sabit_yer", "arac", "hava")
_YORUNGELER: tuple[str, ...] = ("sabit", "dogrusal", "sessizde")
_YAYIN_DUZENLERI: tuple[str, ...] = ("surekli", "gorev_cevrimli",
                                     "yay_sus_tasin")


@dataclass(frozen=True, slots=True)
class Yorunge:
    """Konumun zaman fonksiyonu — rastgelelik yok.

    `baslangic` alan oranıdır ([0, 1]²); irtifa bandın ortasıdır, bugünkü
    karıştırıcıyla aynı. `dogrusal`da hız ölçekli çerçevededir (m/s) ve hareket
    koşunun başından başlar: karıştırıcı yayın yapmadan önce de oradadır.
    Alanın dışına çıkabilir; kutu bir gözlem çerçevesidir, duvar değil.

    `sessizde` (Y5b, `v2/04` K-119): hız YALNIZ yayın çizelgesinin sessiz
    dönemlerinde işler — yay–sus–taşın. Açılmadan önce ve açık dönemlerde
    yerinde durur; yol = hız × o ana kadar sessiz geçen süre.
    """
    baslangic: tuple[float, float]
    tur: str = "sabit"
    hiz_ms: float = 0.0
    yon_rad: float = 0.0


@dataclass(frozen=True, slots=True)
class Yayin:
    """Görev düzeyinde yayın çizelgesi — senaryonun açılma anına göre.

    `surekli`: `ofset_s`ten sonra hep devrede. `gorev_cevrimli` ve
    `yay_sus_tasin`: `acik_s` devrede, `sessiz_s` sessiz, tekrar. İkisinin
    zaman çizelgesi aynıdır; fark platformun sessizlikte yer değiştirmesidir
    ve o `Yorunge`den gelir.

    ⚠️ Çizelge geçişleri parça sınırlarına EKLENMEZ — açılma anıyla aynı beyan:
    en çok bir parça (~190 µs) geç çözülür. Fiziksel katmandaki
    `surekli_darbeli` sınıfından ayrı bir desendir.
    """
    duzen: str = "surekli"
    ofset_s: float = 0.0
    acik_s: float = 0.0
    sessiz_s: float = 0.0


@dataclass(frozen=True, slots=True)
class KaristiriciTanimi:
    """Bir karıştırıcı: platform × yörünge × yayın × sinyal sınıfı × güç payı.

    `sinif` boşsa senaryo adındaki sınıf kullanılır. `guc_payi`, ailenin
    toplam gücünden bu üyenin payıdır; ailenin eşitlemesi Y5b'de belirlenir,
    tek karıştırıcıda 1'dir.
    """
    platform: str
    yorunge: Yorunge
    yayin: Yayin = field(default_factory=Yayin)
    sinif: str | None = None
    guc_payi: float = 1.0


def _tanim_dogrula(t: KaristiriciTanimi) -> None:
    dogrula(t.platform in _PLATFORMLAR, f"bilinmeyen platform: {t.platform!r}")
    bx, by = t.yorunge.baslangic
    dogrula(0.0 <= bx <= 1.0 and 0.0 <= by <= 1.0,
            "başlangıç alan oranı [0, 1] aralığında olmalı")
    dogrula(t.yorunge.tur in _YORUNGELER,
            f"bilinmeyen yörünge: {t.yorunge.tur!r}")
    dogrula(t.yorunge.hiz_ms >= 0.0, "hız negatif olamaz")
    dogrula(t.yorunge.tur != "sabit" or t.yorunge.hiz_ms == 0.0,
            "sabit yörüngede hız sıfır olmalı")
    dogrula(t.platform != "sabit_yer" or t.yorunge.tur == "sabit",
            "sabit yer platformu hareket edemez")
    dogrula(t.yorunge.tur != "sessizde"
            or (t.yayin.duzen != "surekli" and t.yayin.sessiz_s > 0.0),
            "yalnız susarken taşınma, sessiz dönemi olan çevrimli bir yayın "
            "ister")
    y = t.yayin
    dogrula(y.duzen in _YAYIN_DUZENLERI, f"bilinmeyen yayın düzeni: {y.duzen!r}")
    dogrula(y.ofset_s >= 0.0, "yayın ofseti negatif olamaz")
    dogrula(y.duzen == "surekli" or (y.acik_s > 0.0 and y.sessiz_s >= 0.0),
            "çevrimli yayında açık süre pozitif, sessiz süre negatif olmayan "
            "olmalı")
    dogrula(t.guc_payi > 0.0, "güç payı pozitif olmalı")


# ==========================================================================
class KaristiriciTabani:
    """Ortak yayılım: konum sabittir, güç oradan alıcıya taşınır.

    🔒 KONUM SABİT ve alanın merkezinde. Rastgele bir konum, tohumlar arası
    varyansa *karıştırıcının nereye düştüğünü* de katardı ve protokol farkını
    gizlerdi. Sabit merkez tohumlar arasında KARŞILAŞTIRILABİLİRDİR.

    ⚠️ "SABİT KONUM" HAREKETLİ ÇERÇEVEDE NE DEMEK — 8 Eylül 2026
    ============================================================
    Kutu, sürüyle birlikte hareket eden bir gözlem çerçevesidir. Orada
    çakılı duran bir karıştırıcı, ilk bakışta *"sürüyle formasyonda uçan
    karıştırıcı"* gibi görünür ve savunulamaz.

    Aritmetik bunun bu zaman ölçeğinde ÖNEMSİZ olduğunu söylüyor: sürünün
    gerçek transit hızı ~150 km/h, 1:50 ölçekte 0,83 m/s. Ölçüm penceresi
    270 s boyunca yer referanslı bir karıştırıcı çerçevede yalnızca **225 m**
    yol alır — kutunun %12,5'i ve kendi engelleme yarıçapının yarısından az.

    🔒 Yani "sabit konum", bir koşu boyunca yer referanslı bir karıştırıcının
    İYİ BİR YAKLAŞIMIDIR. Geçişi gerçekten modellemek ~2 000 s'lik koşular
    ister (altı kat maliyet) ve bu bir KEŞİFSEL eksendir, çekirdek deneyin
    parçası değil.

    🔴 AÇILMA ANI — projenin asıl iddiasını ÖLÇÜLEBİLİR yapan şey
    ============================================================
    Karıştırıcı eskiden koşunun başından sonuna açıktı. Ölçüm penceresi
    tamamen karıştırılmış dönemin içinde kalıyordu ve **geçici tepki diye
    bir şey yoktu**: ölçülen tek şey kararlı hâldeki bozulmaydı.

    Oysa projenin beyan edilmiş beklentisi *"ilk şokta %50'nin altına düşer,
    mesh tepki verince %70–80'e çıkar"* bir GEÇİCİ TEPKİ tarifidir. Ve bir
    anti-jamming yönlendirme protokolünün asıl iddiası *"ne kadar bozuluyor"*
    değil, **"ne kadar hızlı toparlanıyor"**dur.

    Açılma bir ANAHTARLAMA olayıdır — karıştırıcılar açılır. Ölçüm penceresi
    böylece iki evreye ayrılır ve toparlanma metriği mümkün olur:

        TEMİZ         [ölçüm_başı, karistirici_baslangic_s)
        KARIŞTIRILMIŞ [karistirici_baslangic_s, ölçüm_sonu)

    ⚠️ Açılma anı `gecis_anlari`na EKLENMEZ: parça sınırına düşmediğinde
    açılma en çok bir parça süresi (190 µs) kadar geç çözülür. 270 s'lik bir
    pencerede bu 10⁻⁶ mertebesindedir ve beyan edilir.

    🔒 Y5a: `tanim` verilirse konum `Yorunge`den, devrede olma `Yayin`dan, güç
    `guc_payi`ndan gelir; `indeks` gölgeleme kimliğini ve hash anahtarını
    ayırır. Tanım verilmezse yukarıdaki davranış BİREBİR aynıdır.
    """

    sinif = "taban"

    __slots__ = ("konfig", "yayilim", "topoloji", "ortam", "konum", "tepe_w",
                 "_baslangic_s", "_tanim", "_indeks", "_golge_kimligi",
                 "_sonumleme", "_a2g")

    def __init__(self, konfig: Konfig, yayilim: Yayilim, topoloji: Topoloji,
                 ortam: Ortam, tanim: KaristiriciTanimi | None = None,
                 indeks: int = 0) -> None:
        guc_dbm = konfig.karistirici_guc_dbm
        dogrula(guc_dbm is not None,
                f"'{konfig.karistirici_sinifi}' sınıfının gücü ÖLÇÜLMEDİ: "
                "`senaryolar.KARISTIRICI_GUCU_DBM` bu sınıf için `None`. Ya "
                "orayı bir kalibrasyonla doldurun "
                "(`kalibrasyon/karistirici_gucu.py`) ya da bu koşuma "
                "`karistirici_guc_override_dbm` verin. Sessiz bir varsayılan, "
                "çalışma noktasını ölçmeden seçmek olurdu.")
        dogrula(indeks >= 0, "üye indeksi negatif olamaz")
        self.konfig = konfig
        self.yayilim = yayilim
        self.topoloji = topoloji
        self.ortam = ortam
        if tanim is None:
            x, y = konfig.karistirici_merkez
        else:
            _tanim_dogrula(tanim)
            x = tanim.yorunge.baslangic[0] * konfig.alan_en_m
            y = tanim.yorunge.baslangic[1] * konfig.alan_boy_m
        # Başlangıç konumu; hareketli üyede zamanla `konum_t` değişir.
        self.konum = Nokta3(x, y, 0.5 * (konfig.irtifa_min_m
                                         + konfig.irtifa_maks_m))
        # 🔒 A6 (K-176): yer platformu yerde ve bağı yer–hava kanalıyla;
        # sönümleme `karistirici_kur` bağlar. Kapalıyken ikisi de yok.
        self._sonumleme = None
        self._a2g = None
        if (konfig.karistirici_gercekci and tanim is not None
                and tanim.platform in ("sabit_yer", "arac")):
            self.konum = Nokta3(x, y, konfig.yer_karistirici_yukseklik_m)
            self._a2g = YerHavaKanali(konfig.tohum, konfig.a2g_ortam,
                                      konfig.a2g_durum_dilimi_s)
        self.tepe_w = dbm_to_w(float(guc_dbm))
        if tanim is not None:
            self.tepe_w *= tanim.guc_payi
        self._baslangic_s = konfig.karistirici_baslangic_s
        self._tanim = tanim
        self._indeks = indeks
        # 🔒 Üye başına gölgeleme kimliği; ilk üye bugünkü `-1`.
        self._golge_kimligi = -(indeks + 1)

    # ------------------------------------------------------------------
    @property
    def _uye_anahtari(self) -> tuple[int, ...]:
        """Hash anahtarına eklenen üye kimliği — ilk üyede BOŞ (bugünkü çekim)."""
        return () if self._indeks == 0 else (self._indeks,)

    @property
    def hareketli(self) -> bool:
        """Konumu zamanla değişiyor mu — A3 yeniden denetimi (K-174)."""
        return self._tanim is not None and self._tanim.yorunge.tur != "sabit"

    def konum_t(self, t_s: float) -> Nokta3:
        """Karıştırıcının `t` anındaki konumu — zamanın saf fonksiyonu."""
        if self._tanim is None or self._tanim.yorunge.tur == "sabit":
            return self.konum
        y = self._tanim.yorunge
        sure = t_s if y.tur == "dogrusal" else self._sessiz_gecen_s(t_s)
        yol = y.hiz_ms * sure
        return Nokta3(self.konum.x + yol * math.cos(y.yon_rad),
                      self.konum.y + yol * math.sin(y.yon_rad), self.konum.z)

    def _sessiz_gecen_s(self, t_s: float) -> float:
        """Açılmadan `t_s`e kadar SESSİZ geçen toplam süre (`sessizde` yörünge).

        Çizelge `devrede_mi` ile aynıdır: açılma + ofsetten sonra `acik_s`
        açık, `sessiz_s` sessiz, tekrar. Açılmadan önce 0.
        """
        y = self._tanim.yayin
        t0 = self._baslangic_s + y.ofset_s
        if t_s <= t0:
            return 0.0
        tur, faz = divmod(t_s - t0, y.acik_s + y.sessiz_s)
        return tur * y.sessiz_s + max(0.0, faz - y.acik_s)

    def _yayilim_kaybi_w(self, alici: int, alici_konum: Nokta3,
                         t_s: float) -> float:
        """Karıştırıcıdan alıcıya gelen güç — TEPE güçte, kapalıysa çarpan 0.

        🔴 Gölgeleme bağ kimliğine bağlı olduğu için karıştırıcıya sabit ve
        düğümlerden ayrı bir kimlik verilir (`-1`): aksi hâlde karıştırıcı
        bağının gölgelemesi bir düğüm çiftininkiyle çakışırdı. Kümede her
        üyenin kimliği ayrıdır.
        """
        g = self.tepe_w / (10.0 ** (self._kayip_db(alici, alici_konum, t_s)
                                    / 10.0))
        if self._sonumleme is not None:                     # A6
            g *= self._sonumleme.karistirici_kazanci(
                self._golge_kimligi, alici, t_s, self._bagil_hiz_ms(alici, t_s))
        return g

    def _kayip_db(self, dugum: int, dugum_konum: Nokta3, t_s: float) -> float:
        """Yavaş kayıp; yer platformunda + yer–hava ek kaybı (A6)."""
        kaynak = self.konum_t(t_s)
        kayip = self.yayilim.yavas_kayip_db(self._golge_kimligi, dugum,
                                            kaynak, dugum_konum)
        if self._a2g is not None:
            kayip += self._a2g.ek_kayip_db(self._golge_kimligi, dugum, kaynak,
                                           dugum_konum, t_s)
        return kayip

    def _bagil_hiz_ms(self, dugum: int, t_s: float) -> float:
        """Karıştırıcı ile düğümün bağıl hız büyüklüğü — sönümlemenin Doppler'i."""
        h = 1e-3
        a0, a1 = self.konum_t(t_s), self.konum_t(t_s + h)
        b0 = self.topoloji.konum(dugum, t_s)
        b1 = self.topoloji.konum(dugum, t_s + h)
        vx = ((a1.x - a0.x) - (b1.x - b0.x)) / h
        vy = ((a1.y - a0.y) - (b1.y - b0.y)) / h
        vz = ((a1.z - a0.z) - (b1.z - b0.z)) / h
        return math.sqrt(vx * vx + vy * vy + vz * vz)

    def sahte_cerceveler(self, dugum: int, dugum_konum: Nokta3, t_s: float
                         ) -> tuple[tuple[float, float, int], ...]:
        """`t`de süren sahte çerçeveler — `(başlangıç, alınan güç, kimlik)`.
        Yalnız aldatıcı üretir (A6)."""
        return ()

    def acik_mi(self, t_s: float) -> bool:
        """Sınıfın KENDİ zamanlaması — darbe, reaktif, taramalı vb."""
        raise NotImplementedError

    def devrede_mi(self, t_s: float) -> bool:
        """Karıştırıcı AÇILDI MI? Sınıf zamanlamasından bağımsız kapı.

        🔒 Tek kapı: `alinan_guc_w` bunu uygular ve karıştırıcının BÜTÜN
        etkileri güçten geçer — girişim de, taşıyıcı dinleme de
        (`Dugum.karistirici_mesgul_mu` gücün gürültü tabanını aşmasını arar).
        İkinci bir kapı koymak, ikisinin ayrışabileceği anlamına gelirdi.

        Y5a: tanımlı üyede kapı `Yayin` çizelgesini de uygular.
        """
        if self._tanim is None:
            return t_s >= self._baslangic_s
        y = self._tanim.yayin
        t0 = self._baslangic_s + y.ofset_s
        if t_s < t0:
            return False
        if y.duzen == "surekli":
            return True
        return ((t_s - t0) % (y.acik_s + y.sessiz_s)) < y.acik_s

    def alinan_guc_w(self, alici: int, alici_konum: Nokta3,
                     t_s: float) -> float:
        if not self.devrede_mi(t_s) or not self.acik_mi(t_s):
            return 0.0
        return self._yayilim_kaybi_w(alici, alici_konum, t_s)

    csma_gorunur: bool = False

    def csma_ya_gorunur(self, t_s: float) -> bool:
        """Varsayılan: HAYIR. Gürültü karıştırıcısı geçerli bir önbelge
        basmadığı için taşıyıcı dinleme onu çerçeve olarak görmez."""
        return False

    def csma_guc_w(self, alici: int, alici_konum: Nokta3,
                   t_s: float) -> float:
        """Taşıyıcı dinlemenin gördüğü güç — CSMA'ya görünmüyorsa 0.

        🔒 Tek karıştırıcıda `csma_ya_gorunur` + `alinan_guc_w` ile birebir
        aynıdır; kümede yalnız görünen üyeler toplanır.
        """
        if not self.csma_ya_gorunur(t_s):
            return 0.0
        return self.alinan_guc_w(alici, alici_konum, t_s)

    def gecis_anlari(self, bas_s: float, bitis_s: float) -> tuple[float, ...]:
        return ()


# ==========================================================================
class Surekli(KaristiriciTabani):
    """Kesintisiz gürültü. Referans sınıf."""

    sinif = "surekli"
    __slots__ = ()

    def acik_mi(self, t_s: float) -> bool:
        return True


# ==========================================================================
class Darbeli(KaristiriciTabani):
    """Aynı ORTALAMA güçte darbeli — tepe, görev çevriminden telafi edilir.

    ⚠️ Kümede aynı sınıftan üyeler aynı fazda darbelenir (eşgüdümlü); faz
    ayrımı bir aile kararıdır (Y5b).
    """

    sinif = "surekli_darbeli"
    __slots__ = ("_periyot", "_acik_sure")

    def __init__(self, konfig, yayilim, topoloji, ortam, tanim=None,
                 indeks=0) -> None:
        super().__init__(konfig, yayilim, topoloji, ortam, tanim, indeks)
        self._periyot = konfig.darbe_periyodu_s
        self._acik_sure = konfig.darbe_periyodu_s * konfig.darbe_gorev_cevrimi
        dogrula(self._periyot > 0.0, "darbe periyodu pozitif olmalı")

    def acik_mi(self, t_s: float) -> bool:
        return (t_s % self._periyot) < self._acik_sure

    def gecis_anlari(self, bas_s: float, bitis_s: float) -> tuple[float, ...]:
        """Açılma/kapanma anları — parça sınırlarına eklenir.

        Eklenmeseydi darbenin çerçeve ORTASINDA başlaması ortalamaya gömülür
        ve darbeli karıştırıcı sürekli olanın zayıf bir kopyası gibi ölçülürdü.
        """
        cikti: list[float] = []
        k = math.floor(bas_s / self._periyot)
        while k * self._periyot <= bitis_s:
            for an in (k * self._periyot, k * self._periyot + self._acik_sure):
                if bas_s < an < bitis_s:
                    cikti.append(an)
            k += 1
        return tuple(sorted(cikti))


# ==========================================================================
class Reaktif(KaristiriciTabani):
    """🔴 ORTAMA tepki verir — zamanın saf fonksiyonu DEĞİL.

    Bir iletim başladıktan `reaktif_sezme_s` sonra sezer ve
    `reaktif_patlama_s` boyunca patlar. Sezme başarısı `reaktif_sezme` HASH
    alanından çekilir: bir koşudaki iletim sayısı protokole göre değiştiği
    için sıralı bir akış kolları desenkronize ederdi.

    🔴 YENİDEN SİLAHLANIR — tek atışlık DEĞİL, ve bu ölçümle düzeltildi.
    İlk yazımda karıştırıcı iletim başına BİR kez patlıyordu. Zamanlama
    hesaplandı ve tasarım kırık çıktı:

        iletim başlar     t =    0 µs
        sezme biter       t =   16 µs
        patlama biter     t =  160 µs
        ÖNBELGE biter     t =  192 µs   ← gövde ancak burada başlıyor

    Yani tepki verdiği çerçevenin **gövdesine hiç değmiyordu**: kapsadığı
    gövde payı %0,0. Tek atışlık bir reaktif karıştırıcı, 2240 µs'lik bir
    çerçeveye karşı yalnız önbelgeyi tırmalayan bir şeydir.

    Gerçek bir reaktif karıştırıcı kanalı SÜREKLİ dinler: enerji durdukça
    sezer, patlar, yeniden sezer. Çevrim `sezme + patlama` = 160 µs ve görev
    çevrimi %90; gövdenin kapsanan payı **%90,6**. Sezme süresi tek seferlik
    bir gecikme değil, her çevrimin bedelidir.
    """

    sinif = "reaktif"
    __slots__ = ("_sezme", "_patlama", "_cevrim", "_esik_w")

    def __init__(self, konfig, yayilim, topoloji, ortam, tanim=None,
                 indeks=0) -> None:
        super().__init__(konfig, yayilim, topoloji, ortam, tanim, indeks)
        self._sezme = konfig.reaktif_sezme_s
        self._patlama = konfig.reaktif_patlama_s
        self._cevrim = self._sezme + self._patlama
        self._esik_w = dbm_to_w(konfig.reaktif_esik_dbm)
        dogrula(self._sezme >= 0.0 and self._patlama > 0.0,
                "reaktif sezme/patlama süreleri geçersiz")

    def _sezildi_mi(self, iletim) -> bool:
        """Sezme olasılığı (köken defterinde, A6) — gerçekçide ayrıca iletimin
        karıştırıcıda alınan gücü eşiği aşmalı (menzilsiz duyma yok)."""
        dilim = int(iletim.baslangic_s / self.konfig.kanal_dilimi_s)
        if hash_cekimi("reaktif_sezme", self.konfig.tohum, iletim.gonderen,
                       "sezme", dilim, *self._uye_anahtari
                       ) >= self.konfig.reaktif_sezme_olasiligi:
            return False
        if not self.konfig.karistirici_gercekci:
            return True
        konum = self.topoloji.konum(iletim.gonderen, iletim.baslangic_s)
        alinan = iletim.guc_w / (10.0 ** (self._kayip_db(
            iletim.gonderen, konum, iletim.baslangic_s) / 10.0))
        return alinan >= self._esik_w

    def acik_mi(self, t_s: float) -> bool:
        for iletim in self.ortam.aktif(t_s):
            if not self._sezildi_mi(iletim):
                continue
            # Çevrim içindeki konum: [0, sezme) sessiz, [sezme, çevrim) patlama.
            faz = (t_s - iletim.baslangic_s) % self._cevrim
            if faz >= self._sezme:
                return True
        return False

    def gecis_anlari(self, bas_s: float, bitis_s: float) -> tuple[float, ...]:
        cikti: list[float] = []
        for iletim in self.ortam.pencerede(bas_s, bitis_s):
            k = 0
            while True:
                cevrim_bas = iletim.baslangic_s + k * self._cevrim
                if cevrim_bas > min(bitis_s, iletim.bitis_s):
                    break
                for an in (cevrim_bas + self._sezme,
                           cevrim_bas + self._cevrim):
                    if bas_s < an < bitis_s and an < iletim.bitis_s:
                        cikti.append(an)
                k += 1
        return tuple(sorted(set(cikti)))


# ==========================================================================
class Aldatici(KaristiriciTabani):
    """🔴 CSMA'YA GÖRÜNÜR — geçerli görünümlü çerçeve basar.

    Sahte çerçeveler arka arkaya, aralarında bir DIFS boşlukla gönderilir:
    ortalığı sürekli meşgul gösteren, kurallara uyuyormuş gibi davranan
    açgözlü bir istasyon taklidi. Taşıyıcı dinleme onu meşgul GÖRMEK
    ZORUNDADIR; eski *"karıştırıcı CSMA'yı tetiklemez"* beyanı burada kalkar.
    """

    sinif = "aldatici"
    csma_gorunur = True
    __slots__ = ("_cerceve_s", "_bosluk_s", "_periyot")

    def __init__(self, konfig, yayilim, topoloji, ortam, tanim=None,
                 indeks=0) -> None:
        super().__init__(konfig, yayilim, topoloji, ortam, tanim, indeks)
        self._cerceve_s = cerceve_kur(konfig, "veri").sure_s
        self._bosluk_s = konfig.difs_s
        self._periyot = self._cerceve_s + self._bosluk_s

    def _cerceve_indeksi(self, t_s: float) -> int:
        return int(math.floor(t_s / self._periyot))

    def acik_mi(self, t_s: float) -> bool:
        return (t_s % self._periyot) < self._cerceve_s

    def csma_ya_gorunur(self, t_s: float) -> bool:
        return self.acik_mi(t_s)

    def sahte_cerceveler(self, dugum: int, dugum_konum: Nokta3, t_s: float
                         ) -> tuple[tuple[float, float, int], ...]:
        if not self.acik_mi(t_s):
            return ()
        bas = self._cerceve_indeksi(t_s) * self._periyot
        return ((bas, self.alinan_guc_w(dugum, dugum_konum, bas),
                 self._golge_kimligi),)

    def sahte_icerik(self, t_s: float) -> float:
        """Sahte çerçevenin içeriği — `aldatici_icerik` hash alanından.

        İçerik alıcının önbelge kilidini kurup kurmayacağını etkiler
        (Adım 6a); burada yalnız üretilir ve sınıfın hash alanını kullanır.
        """
        return hash_cekimi("aldatici_icerik", self.konfig.tohum,
                           self._cerceve_indeksi(t_s), *self._uye_anahtari)

    def gecis_anlari(self, bas_s: float, bitis_s: float) -> tuple[float, ...]:
        cikti: list[float] = []
        k = self._cerceve_indeksi(bas_s)
        while k * self._periyot <= bitis_s:
            for an in (k * self._periyot, k * self._periyot + self._cerceve_s):
                if bas_s < an < bitis_s:
                    cikti.append(an)
            k += 1
        return tuple(sorted(cikti))


# ==========================================================================
class Taramali(KaristiriciTabani):
    """Konaklar arasında gezinir; yalnız bizim kanalımızdayken etkilidir.

    🔒 TEPE gücü `surekli` ile eşittir, ortalaması konak sayısına bölünür —
    modül başlığındaki güç eşitlemesi notuna bak. Konak dizisi
    `taramali_konak` hash alanından gelir.
    """

    sinif = "taramali"
    __slots__ = ("_konak_s", "_konak_sayisi")

    def __init__(self, konfig, yayilim, topoloji, ortam, tanim=None,
                 indeks=0) -> None:
        super().__init__(konfig, yayilim, topoloji, ortam, tanim, indeks)
        self._konak_s = konfig.taramali_konak_suresi_s
        self._konak_sayisi = konfig.taramali_konak_sayisi
        dogrula(self._konak_s > 0.0, "konak süresi pozitif olmalı")
        dogrula(self._konak_sayisi >= 1, "en az bir konak gerekli")

    def _konak(self, t_s: float) -> int:
        indeks = int(math.floor(t_s / self._konak_s))
        cekim = hash_cekimi("taramali_konak", self.konfig.tohum, indeks,
                            *self._uye_anahtari)
        return int(cekim * self._konak_sayisi)

    def acik_mi(self, t_s: float) -> bool:
        return self._konak(t_s) == 0            # 0 = bizim kanalımız

    def gecis_anlari(self, bas_s: float, bitis_s: float) -> tuple[float, ...]:
        cikti: list[float] = []
        k = int(math.floor(bas_s / self._konak_s))
        while k * self._konak_s <= bitis_s:
            an = k * self._konak_s
            if bas_s < an < bitis_s:
                cikti.append(an)
            k += 1
        return tuple(cikti)


# ==========================================================================
class KaristiriciKumesi:
    """Birden çok karıştırıcı — tek karıştırıcının arayüzünü AYNEN sunar.

    Şartname: `v2/07-SIMULATOR-TASARIMI.md` §18 Y5. Alınan güç üyelerin
    toplamı, geçiş anları birleşimleridir. 🔒 Taşıyıcı dinleme yalnız CSMA'ya
    görünen üyelerin gücüne bakar (`csma_guc_w`). Tek üyeli bir küme
    kurulmaz: `karistirici_kur` o üyeyi doğrudan döndürür.
    """

    sinif = "kume"
    __slots__ = ("uyeler", "csma_gorunur")

    def __init__(self, uyeler) -> None:
        dogrula(len(uyeler) >= 2, "küme en az iki üyeli olmalı")
        self.uyeler: tuple[KaristiriciTabani, ...] = tuple(uyeler)
        self.csma_gorunur = any(u.csma_gorunur for u in self.uyeler)

    def alinan_guc_w(self, alici: int, alici_konum: Nokta3,
                     t_s: float) -> float:
        return sum(u.alinan_guc_w(alici, alici_konum, t_s)
                   for u in self.uyeler)

    def csma_guc_w(self, alici: int, alici_konum: Nokta3,
                   t_s: float) -> float:
        return sum(u.csma_guc_w(alici, alici_konum, t_s) for u in self.uyeler)

    def csma_ya_gorunur(self, t_s: float) -> bool:
        return any(u.csma_ya_gorunur(t_s) for u in self.uyeler)

    def gecis_anlari(self, bas_s: float, bitis_s: float) -> tuple[float, ...]:
        anlar: set[float] = set()
        for u in self.uyeler:
            anlar.update(u.gecis_anlari(bas_s, bitis_s))
        return tuple(sorted(anlar))

    def devrede_mi(self, t_s: float) -> bool:
        return any(u.devrede_mi(t_s) for u in self.uyeler)

    def sahte_cerceveler(self, dugum: int, dugum_konum: Nokta3, t_s: float
                         ) -> tuple[tuple[float, float, int], ...]:
        return tuple(c for u in self.uyeler
                     for c in u.sahte_cerceveler(dugum, dugum_konum, t_s))

    @property
    def hareketli(self) -> bool:
        return any(u.hareketli for u in self.uyeler)

    def acik_mi(self, t_s: float) -> bool:
        return any(u.acik_mi(t_s) for u in self.uyeler)


# ==========================================================================
_SINIFLAR = {
    "surekli": Surekli,
    "surekli_darbeli": Darbeli,
    "reaktif": Reaktif,
    "aldatici": Aldatici,
    "taramali": Taramali,
}


def karistirici_kur(konfig: Konfig, yayilim: Yayilim, topoloji: Topoloji,
                    ortam: Ortam,
                    tanimlar: tuple[KaristiriciTanimi, ...] | None = None,
                    sonumleme=None) -> Karistirici | None:
    """Senaryodan karıştırıcı. `yok` için `None` — sarmalayıcı DEĞİL.

    Boş bir "hiçbir şey yapmayan karıştırıcı" nesnesi döndürmek, her girişim
    hesabına ölü bir çağrı eklerdi ve "karıştırıcı var mı" sorusu koddan
    okunamaz olurdu.

    Y5a: `tanimlar` verilmezse bugünkü tek merkez karıştırıcı BİREBİR kurulur.
    Verilirse her tanım bir üye olur; tek üye doğrudan, birden çoğu
    `KaristiriciKumesi` olarak döner.
    """
    sinif = konfig.karistirici_sinifi
    if sinif == "yok":
        return None
    if tanimlar is None:
        tip = _SINIFLAR.get(sinif)
        if tip is None:
            asla(f"karıştırıcı sınıfı tanımlı ama kurucusu yok: {sinif!r}")
        uyeler = [tip(konfig, yayilim, topoloji, ortam)]
    else:
        dogrula(len(tanimlar) >= 1, "tanım listesi boş olamaz")
        uyeler = []
        for indeks, tanim in enumerate(tanimlar):
            uye_sinifi = tanim.sinif or sinif
            tip = _SINIFLAR.get(uye_sinifi)
            dogrula(tip is not None,
                    f"bilinmeyen karıştırıcı sınıfı: {uye_sinifi!r}")
            uyeler.append(tip(konfig, yayilim, topoloji, ortam, tanim, indeks))
    # 🔒 A6 (K-176): karıştırıcı bağlarına sönümleme — yalnız gerçekçide.
    if konfig.karistirici_gercekci:
        for u in uyeler:
            u._sonumleme = sonumleme
    return uyeler[0] if len(uyeler) == 1 else KaristiriciKumesi(uyeler)
