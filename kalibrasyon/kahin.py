"""
KÂHİN YÖNLENDİRİCİLER — kıyas için, protokol değil.

🔴 NEDEN YENİDEN YAZILDI (5 Eylül 2026, K-096 · K-097)
======================================================
Eski kâhin `Topoloji`nin komşuluk grafiğinde BFS yapıyordu. O grafik
`nominal_bag_m` (280 m) yarıçaplı sert bir disktir ve **verici gücünün
türetildiği çapadır** — veri yolunda hiçbir yeri kapamaz. Alan 1800 m'ye
çıkınca o diskin derecesi 2,57'ye indi, yani kâhin **kopuk bir grafikte**
yönlendirmeye çalışıyordu.

⚠️ Ve daha derin bir sorun ölçüldü: **tek bir yarıçap gerçek bağ kümesini
temsil edemiyor.** Derece eşitlense bile (r = 560 m'de 8,23 ↔ 8,25)
kenarların yalnız yarısı örtüşüyor — Jaccard 0,53. Sebebi gölgeleme:
σ = 3 dB, α = 2'de mesafede ±%41 demek. "Menzil" bir daire değil, kenarları
1,4 kat oynayan bulanık bir buluttur. Yani sorun yarıçapın YANLIŞ olması
değil, tek bir yarıçapın YETMEMESİdir.

🔒 ÇÖZÜM: KÂHİN GRAFİĞİ KANALDAN GELİR — SÖNÜMLEME DÂHİL
========================================================
Bağ kalitesi, alıcıdaki gerçek anlık güçten hesaplanır:

    SINR   = sinyal_w(i, j, t) / gurultu_w      (yol kaybı × gölgeleme × sönümleme)
    p      = (1 − PER_veri) · (1 − PER_onay)    (tek deneme başarısı)
    atlama = 1 − (1 − p)^(deneme_siniri + 1)    (yeniden denemelerle)
    ETX    = 1 / p                               (beklenen iletim sayısı)

🔴 İLK YAZIMDA SÖNÜMLEME DIŞARIDAYDI ve gerekçesi de yazılmıştı: *"sönümleme
saniyede yüzlerce kez değişir, onu bağ kalitesine katmak anlık bir fadingi
bağın kalıcı özelliği saymak olurdu."* **Gerekçe yanlıştı** ve sonucu ölçüldü:

    statik-yok, tohum 1002, eşikli graftaki 161 bağ
        tek deneme başarısı, yavaş kanal   : ort 0,881 · en kötü 0,374
        tek deneme başarısı, sönümleme dâhil: ort 0,710 · en kötü **0,000**
        kâhinin "iyi" sandığı ama gerçekte atlama < 0,90 olan bağ: **%26**

Yani kâhin, komşu tablosundaki hayalet bağ tuzağının (K-094) aynısına kendi
düşmüştü — ve bunu "biraz iyimser" diye beyan etmiştim. "Biraz" değildi.

⚠️ STATİK KOLDA SÖNÜMLEME ZATEN DONDURULMUŞTUR. Orada ortalama alınacak bir
şey yok: her bağın tek bir donmuş kazancı vardır ve bağın kalıcı kalitesi
odur. Hareketli kolda ise doğru büyüklük ORTALAMADIR — sönümleme ~2 ms'de
dekorele olur, hiçbir yönlendirici onu izleyemez; izlenebilir olan
ortalamasıdır.

🔒 GİRİŞİM KASTEN DIŞARIDA — ve bu sefer gerekçe ÖLÇÜLDÜ. Girişimi katmak
grafiği anlık trafikle titretirdi. Yükün gerçekten etkisiz olduğu sınandı:
yük 8 kat düşürüldüğünde (40 → 5 pkt/s) PDR 0,511 → 0,511 ve onaysız oranı
%68,5 → %68,4. Kayıp tıkanıklıktan değil, bağ kalitesinden.

🔴 İKİ KÂHİN, İKİ AYRI SORU — ve farkları ÖLÇÜLEBİLİR OLSUN DİYE ikisi de var
=============================================================================
  · `EnKisaYolKahin`  — mükemmel topoloji bilgisi, **en az atlama** ölçütü.
  · `EnGuvenilirKahin` — mükemmel topoloji bilgisi, **en az beklenen iletim**
    (ETX) ölçütü. Gerçek tavan budur.

Aradaki fark, atlama sayısı ölçütünün bedelidir: en az atlama, en uzun —
yani en kötü — bağı seçer. Gerçek protokolle `EnKisaYolKahin` arasındaki
fark ise protokolün körlüğünün bedelidir. Bugüne kadar ikisi tek bir sayıya
karışmıştı.

⚠️ AMA `EnKisaYolKahin` KORUMALIDIR — ve bu beyan edilmelidir.
BFS, `ATLAMA_ESIGI`ni geçen bağlardan kurulu grafikte çalışır; yani **kötü
bir bağ seçmesi zaten engellenmiştir**. Gerçek bir atlama-sayısı protokolünün
(AODV) böyle bir koruması yoktur: komşu tablosu beacon'dan kurulur ve beacon,
veriden daha uzağa gider (K-094). Dolayısıyla:

    ETX-kâhin − atlama-kâhin  = ölçütün bedeli, İYİ BİR BAĞ KÜMESİ VERİLMİŞKEN
    atlama-kâhin − protokol   = körlüğün bedeli (hayalet bağ + bayatlık)

İkincisi, atlama ölçütünün gerçek dünyadaki asıl bedelini de içerir. Ayrı
ayrı ölçmek isteyen, eşiği kaldırılmış üçüncü bir kâhin yazmalıdır — ama o
zaman "kâhin" adı hak edilmez, çünkü kasten kötü seçim yapar.

🔒 ÖLÇÜLDÜ (statik-yok, tohum 1000, 1 560 çift, 5 Eylül 2026):
    ortalama atlama      : atlama-kâhin 2,17 ↔ ETX-kâhin 2,19
    ortalama toplam ETX  : atlama-kâhin 2,605 ↔ ETX-kâhin **2,421**  (−%7,1)
    aynı yolu seçtiği    : %63,7
    ETX-kâhinin daha pahalı olduğu çift: 0   ← Dijkstra'nın doğruluk kapısı

🔒 BU DOSYA `kalibrasyon/` ALTINDADIR ve öyle kalmalı: kâhin erişimi bir
KIYAS ALETİdir. `protokoller/` altındaki hiçbir şey buradan içe aktarma
yapmamalıdır — mimari denetimi (D7) kâhin sızıntısını zaten arıyor.
"""

from __future__ import annotations

import heapq
import math
import sys
from collections import deque
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.dunya.geometri import mesafe  # noqa: E402
from sim2.gozlem.karar import Karar  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.tehdit import en_buyuk_hiz_ms  # noqa: E402
from sim2.kanal.yayilim import dbm_to_w  # noqa: E402
from sim2.yapilandirma.konfig import HIZLAR_BPS  # noqa: E402

__all__ = ["KanalGrafigi", "EnKisaYolKahin", "EnGuvenilirKahin",
           "ATLAMA_ESIGI", "dilim_suresi_s", "SONUMLEME_ORNEGI",
           "SONUMLEME_ADIMI_S"]

# Bir bağın "kullanılabilir" sayılması için gereken atlama başarısı.
# `kalibrasyon/calisma_noktasi.py` ile AYNI EŞİK ve artık AYNI KESTİRİCİ:
# ikisi de sönümlemeyi içerir. Ölçülen derece 7,20 (kâhin) ↔ 7,24
# (kalibrasyon, aynı alan) — fark örnekleme gürültüsü mertebesinde.
#
# 🔴 Bu eşik YALNIZ `EnKisaYolKahin` içindir. `EnGuvenilirKahin` eşik
# kullanmaz: zayıf bağ dışlanmaz, PAHALI olur. Eşik koymak ölçütün işini
# elle yapmak olurdu.
ATLAMA_ESIGI: float = 0.90

# Hareketli kolda sönümleme ortalaması için örnek sayısı ve aralığı.
# Aralık, sönümleme tutarlılık süresinden (~2 ms) BÜYÜK seçildi ki örnekler
# bağımsız olsun; küçük seçilseydi aynı fade tekrar sayılırdı.
# Donuk (statik) kolda tek örnek alınır — ölçüldü, K = 2…48 aynı sonucu
# veriyor, çünkü sönümleme orada zamanla değişmiyor.
# 🔴 K-214/K-215: 6 örnekte kâhin YAKINSAMAMIŞTI — ETX kâhininin PDR'si
# 6 → 48 örnekte birincil hücrede +0,039, bağımsız-yokta +0,065 (plato 12 ve
# 24). Koşu süresi örnek sayısından bağımsız → 48.
SONUMLEME_ORNEGI: int = 48
SONUMLEME_ADIMI_S: float = 0.005


def dilim_suresi_s(konfig) -> float:
    """Grafik ne sıklıkta yeniden kurulmalı — TÜRETİLİR, elle yazılmaz.

    🔒 Bağ kalitesini değiştiren şey konum değil, GÖLGELEME hücresinin
    değişmesidir: gölgeleme `golgeleme_hucre_m` ölçeğinde korelasyonludur,
    bir düğüm o mesafeyi kat edene kadar bağın yavaş kalitesi aynı kalır.
    Bağıl hız en kötü hâlde iki düğümün azami hızının toplamıdır.

        dilim = golgeleme_hucre_m / (2 · gm_hiz_maks_ms)

    ⚠️ ELLE 0,5 s YAZILMIŞTI ve bu, mobilite adımına bakarak seçilmişti —
    yanlış büyüklük. Sönümleme örneklemesi eklenince grafik kurulumu
    961 ms'ye çıktı; 0,5 s'de bir kurmak koşuya %53 eklerdi. Türetilmiş
    değer bugün ~0,8 s, hızlar 1/50 ölçeğe çekilince ~23 s olur ve maliyet
    kendiliğinden erir.

    🔒 Alt sınır çerçeve süresinden büyük, üst sınır ölçüm penceresinin
    küçük bir payı olacak biçimde kelepçelenir: kâhinin bilgisi hiçbir
    zaman ölçüm penceresiyle kıyaslanabilir ölçüde bayat olmamalı.

    🔒 Y5b (`v2/07` §18 Y5): karıştırıcı da hareket edebilir. Düğüm ile
    karıştırıcının bağıl hızı en kötü hâlde `gm_hiz_maks_ms + karıştırıcı
    hızı`dır; payda iki düğümün ve düğüm–karıştırıcı çiftinin büyüğüdür.
    Sabit karıştırıcıda ifade bugünküyle bit bit aynıdır.
    """
    hiz = max(konfig.gm_hiz_maks_ms, 1e-6)
    bagil = max(2.0 * hiz, hiz + en_buyuk_hiz_ms(konfig))
    return min(max(konfig.golgeleme_hucre_m / bagil, 0.1), 10.0)

# ETX'in üst sınırı — p = 0 olan bağlar için. Sonsuz yerine büyük bir sayı
# kullanmak Dijkstra'yı basitleştirir; bu bağlar zaten hiç seçilmez.
ETX_TAVANI: float = 1e9


class KanalGrafigi:
    """Bütün düğümlerin paylaştığı kâhin grafik — KANALDAN kurulur.

    🔒 Hareketsiz topolojide bir kez kurulur ve donar: konumlar ve gölgeleme
    değişmediğine göre bağ kalitesi de değişemez.
    """

    __slots__ = ("kur", "dilim_s", "_dilim", "_komsu", "_etx", "_donuk",
                 "_veri", "_onay", "_kesme_m", "_ornek", "_ed_w", "_imza")

    def __init__(self, kur, dilim_s: float | None = None) -> None:
        self.kur = kur
        self.dilim_s = (dilim_suresi_s(kur.konfig)
                        if dilim_s is None else dilim_s)
        self._dilim = -1
        self._imza: tuple | None = None
        self._komsu: list[list[int]] = []
        self._etx: list[dict[int, float]] = []
        self._donuk = not kur.topoloji.hareketli
        k = kur.konfig
        # 🔒 Faz 4.0 (K-183) · HIZ UYARLAMASI: bağ ARF'nin TABANINDA (en
        # düşük hız) ölçülür — zayıf bağ gerçekte oraya iner ve ayakta kalır
        # (K-181 ayrıştırması: MAC vazgeçmesi 135 → 0). Kâhin "her şeyi
        # bilir"; bağın taşıyabileceği en güvenilir hızı da bilir.
        self._veri = cerceve_kur(k, "veri", hiz_bps=(
            min(HIZLAR_BPS) if k.hiz_uyarlamasi else None))
        self._onay = cerceve_kur(k, "onay")
        # 🔒 Faz 4.0 (K-183) · ED SUSTURMASI (güç kipi, A3): karıştırıcıdan
        # aldığı enerji ED eşiğini aşan verici kanalı ALAMAZ — i→j bağı yok.
        # Onay kanal dinlemeden SIFS sonra gider; yalnız verici kilitlenir,
        # grafik YÖNLÜ olur. Geometrik kipte `None` ve grafik birebir eski.
        # ⚠️ Beyan: eski dünyada (geometrik kip) aldatıcının CSMA susturması
        # da kâhinde yoktu; o dünya artık deneyde kullanılmıyor, değişmedi.
        self._ed_w = (dbm_to_w(k.ed_esigi_dbm)
                      if k.tasiyici_dinleme == "guc" else None)
        # Bu mesafenin ötesinde SINR gürültü tabanının altında; bağ olamaz.
        # Girişim menzili tam olarak o sınırdır ve konfigden TÜRETİLİR.
        # 🔒 K-183: simülatörün DUYMA KÜMESİYLE aynı sınır — işlem kazancıyla
        # ×çarpan^(1/α) genişler (referansta ~28 km; 1 Mb/s bağı ~7,4 km'ye
        # uzanır, girişim menzili 5,97 km'de kesseydi kâhin onları atardı).
        # Kazanç kapalıyken çarpan 1 → birebir eski sınır.
        self._kesme_m = kur.duyanlar_menzili_m
        self._ornek = SONUMLEME_ORNEGI

    # ------------------------------------------------------------ bağ kalitesi
    def _tek_deneme_basarisi(self, i: int, j: int, t_s: float) -> float:
        """Bir atlamanın tek deneme başarısı — SÖNÜMLEME DÂHİL, girişim hariç.

        🔴 İLK YAZIMDA SÖNÜMLEME DIŞARIDAYDI ve kâhin kendi hayalet bağlarını
        üretiyordu. Ölçüldü (statik-yok, t=1002): eşikli grafikteki bağların
        **%26'sı** sönümleme hesaba katılınca %90 eşiğinin altındaydı; tek
        deneme başarısının ortalaması 0,881 → 0,710, en kötü bağ 0,374 → 0,000.
        Yani kâhin, komşu tablosundaki hayalet bağ tuzağının (K-094) aynısına
        kendi düşmüştü.

        ⚠️ STATİK KOLDA SÖNÜMLEME DONDURULMUŞTUR (`sonumleme.py`). Orada
        "ortalama almak" diye bir şey yok: her bağın tek bir donmuş kazancı
        var ve bağın kalıcı kalitesi odur. Bu yüzden donuk kolda TEK örnek
        alınır — daha fazlası aynı sayıyı tekrar hesaplamaktan ibarettir.
        Ölçüldü: K = 2, 4, 8, 16, 48 aynı sonucu veriyor.

        ⚠️ Hareketli kolda sönümleme zamanla değişir ve doğru büyüklük
        ORTALAMASIDIR: sönümleme ~2 ms'de dekorele olur, hiçbir yönlendirici
        onu izleyemez; izlenebilir olan ortalamasıdır.

        🔒 GİRİŞİM KASTEN DIŞARIDA. `alim_per` o anda havada olan iletimleri
        de sayardı ve yönlendirme grafiği anlık trafikle titrerdi. Burada
        ölçülen şey bağın kendi kalitesidir, yükün altındaki hâli değil.
        Yükün etkisi ölçüldü ve bu grafiği değiştirmemesi gerektiğini
        doğruladı: yük 8 kat düşürüldüğünde PDR kılını kıpırdatmadı.
        """
        kanal = self.kur.kanal
        girisim = kanal.girisim
        gurultu = kanal.yayilim.gurultu_w
        top = self.kur.topoloji
        kar = kanal.karistirici
        ornek = 1 if self._donuk else self._ornek
        toplam = 0.0
        for adim in range(ornek):
            t = t_s + adim * SONUMLEME_ADIMI_S
            t2 = t + self._veri.sure_s
            if self._susturulmus_mu(i, t):
                continue                    # K-183: verici kanalı alamaz
            # 🔴 KARIŞTIRICI PAYDAYA GİRER — 8 Eylül 2026.
            # Eskiden girmiyordu ve kâhin karıştırılan bölgeyi GÖRMÜYORDU:
            # etrafından dolaşmıyor, içinden geçiyordu. Bir TAVAN aleti için
            # bu eksikti — kâhinin tanımı "her şeyi bilir"dir ve karıştırıcı
            # her şeyin içindedir.
            n1 = gurultu + (0.0 if kar is None else
                            kar.alinan_guc_w(j, top.konum(j, t), t))
            n2 = gurultu + (0.0 if kar is None else
                            kar.alinan_guc_w(i, top.konum(i, t2), t2))
            sinr_veri = girisim.sinyal_w(i, j, t) / n1
            sinr_onay = girisim.sinyal_w(j, i, t2) / n2
            toplam += ((1.0 - kanal.kahin_per(self._veri, sinr_veri))
                       * (1.0 - kanal.kahin_per(self._onay, sinr_onay)))
        return toplam / ornek

    def _susturulmus_mu(self, i: int, t_s: float) -> bool:
        """K-183 · Güç kipinde verici `i` karıştırıcı yüzünden kanalı
        alamıyor mu — `Dugum._guc_mesgul_mu`nun karıştırıcı dalıyla aynı
        kural: ED eşiği ya da görünür (aldatıcı) önbelge gürültünün üstünde.
        Öteki iletimler sayılmaz (girişim kasten dışarıda, yukarıda)."""
        if self._ed_w is None:
            return False
        kar = self.kur.kanal.karistirici
        if kar is None:
            return False
        konum = self.kur.topoloji.konum(i, t_s)
        if (kar.csma_guc_w(i, konum, t_s)
                > self.kur.kanal.yayilim.gurultu_w):
            return True
        return kar.alinan_guc_w(i, konum, t_s) >= self._ed_w

    def _kur(self, t_s: float) -> None:
        n = self.kur.dugum_sayisi
        top = self.kur.topoloji
        konum = [top.konum(i, t_s) for i in range(n)]
        deneme = self.kur.konfig.yeniden_deneme_siniri + 1
        self._komsu = [[] for _ in range(n)]
        self._etx = [dict() for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if mesafe(konum[i], konum[j]) > self._kesme_m:
                    continue
                if self._ed_w is not None:
                    # K-183: YÖNLÜ — iki yön ayrı ölçülür (susturma asimetrik)
                    self._yon_ekle(i, j, self._tek_deneme_basarisi(i, j, t_s),
                                   deneme)
                    self._yon_ekle(j, i, self._tek_deneme_basarisi(j, i, t_s),
                                   deneme)
                    continue
                p = self._tek_deneme_basarisi(i, j, t_s)
                if p <= 0.0:
                    continue
                etx = min(1.0 / p, ETX_TAVANI)
                self._etx[i][j] = etx
                self._etx[j][i] = etx
                if 1.0 - (1.0 - p) ** deneme >= ATLAMA_ESIGI:
                    self._komsu[i].append(j)
                    self._komsu[j].append(i)

    def _yon_ekle(self, i: int, j: int, p: float, deneme: int) -> None:
        """K-183: tek yönlü bağ i→j (veri i'den, onay j'den)."""
        if p <= 0.0:
            return
        self._etx[i][j] = min(1.0 / p, ETX_TAVANI)
        if 1.0 - (1.0 - p) ** deneme >= ATLAMA_ESIGI:
            self._komsu[i].append(j)

    def _tazele(self, t_s: float) -> None:
        # 🔴 "DONUK" KISAYOLU YALNIZ KARIŞTIRICISIZ KOLDA GEÇERLİ.
        # Hareketsiz topolojide konumlar ve gölgeleme değişmez, ama
        # karıştırıcı ZAMANLA DEĞİŞİR: bir açılma anı vardır ve sınıfına
        # göre darbeli/reaktif olabilir. Grafiği bir kez kurup dondurmak,
        # kâhinin karıştırıcıyı hiç görmemesi demek olurdu.
        if self._donuk and self.kur.kanal.karistirici is None:
            if self._dilim == 0:
                return
            self._dilim = 0
            self._kur(t_s)
            return
        dilim = int(t_s / self.dilim_s)
        imza = self._devrede_imzasi(t_s)
        if dilim == self._dilim and imza == self._imza:
            return
        self._dilim = dilim
        self._imza = imza
        self._kur(t_s)

    def _devrede_imzasi(self, t_s: float) -> tuple:
        """🔴 K-195 · KARIŞTIRICININ ÇİZELGESİ GRAFİĞİ YENİLER.

        Dilim yalnız HAREKETTEN türüyordu (`dilim_suresi_s`); referans
        dünyada 10 s'ye kırpılır. Karıştırıcının açılma anı ve yayın
        çizelgesi (`derin_sizma`: 15 s açık · 15 s sessiz) dilimden bağımsız
        değişir — kâhin geçişten sonra 10 s'ye kadar ESKİ karıştırma durumunu
        görüyor, açık karıştırıcının içinden geçiyordu (birincil hücre
        dumanında kâhin PDR 0,63; başarısız bağlarının %39'u o anda kötü).
        Karıştırıcının `gecis_anlari`ı yalnız SINIF zamanlamasını (darbe,
        tarama) verir, açılmayı ve çizelgeyi vermez; bu yüzden her üyenin
        `devrede_mi` durumu okunur ve değişince grafik yeniden kurulur.
        Karıştırıcısız kolda imza boştur — davranış birebir.
        ⚠️ Sınıf içi hızlı zamanlama (darbe 2,7 s, tarama 0,1 s) bu imzaya
        GİRMEZ; kâhin onları dilim anındaki anlık durumla görür (bugünkü
        davranış, beyanlı)."""
        kar = self.kur.kanal.karistirici
        if kar is None:
            return ()
        return tuple(u.devrede_mi(t_s)
                     for u in getattr(kar, "uyeler", (kar,)))

    # ------------------------------------------------------------- sorgular
    def en_kisa_yol_sonraki(self, kaynak: int, hedef: int) -> int | None:
        """En AZ ATLAMA — kullanılabilir bağ grafiğinde BFS."""
        self._tazele(self.kur.olaylar.simdi)
        if kaynak == hedef:
            return None
        onceki: dict[int, int | None] = {kaynak: None}
        kuyruk = deque([kaynak])
        while kuyruk:
            u = kuyruk.popleft()
            if u == hedef:
                break
            for v in self._komsu[u]:
                if v not in onceki:
                    onceki[v] = u
                    kuyruk.append(v)
        if hedef not in onceki:
            return None
        dugum = hedef
        while onceki[dugum] != kaynak:
            dugum = onceki[dugum]  # type: ignore[assignment]
            if dugum is None:
                return None
        return dugum

    def en_guvenilir_sonraki(self, kaynak: int, hedef: int) -> int | None:
        """En AZ BEKLENEN İLETİM — ETX ağırlıklı Dijkstra.

        🔒 Eşik YOK: zayıf bağlar dışlanmaz, PAHALI olur. Eşik koymak,
        ölçütün işini elle yapmak olurdu.
        """
        self._tazele(self.kur.olaylar.simdi)
        if kaynak == hedef:
            return None
        n = self.kur.dugum_sayisi
        uzaklik = [math.inf] * n
        onceki: list[int | None] = [None] * n
        uzaklik[kaynak] = 0.0
        yigin: list[tuple[float, int]] = [(0.0, kaynak)]
        gorulen = [False] * n
        while yigin:
            d, u = heapq.heappop(yigin)
            if gorulen[u]:
                continue
            gorulen[u] = True
            if u == hedef:
                break
            for v, agirlik in self._etx[u].items():
                yeni = d + agirlik
                if yeni < uzaklik[v]:
                    uzaklik[v] = yeni
                    onceki[v] = u
                    heapq.heappush(yigin, (yeni, v))
        if uzaklik[hedef] >= ETX_TAVANI or onceki[hedef] is None:
            return None
        dugum = hedef
        while onceki[dugum] != kaynak:
            dugum = onceki[dugum]  # type: ignore[assignment]
            if dugum is None:
                return None
        return dugum

    # ------------------------------------------------------------- teşhis
    def ozet(self, t_s: float = 0.0) -> dict[str, float]:
        """Grafiğin durumu — karara girmez, rapora girer."""
        self._tazele(t_s)
        n = self.kur.dugum_sayisi
        derece = sum(len(k) for k in self._komsu) / n
        ulasilan = 0
        bilinen: set[int] = set()
        bilesenler: list[int] = []
        erisim: list[set[int]] = []
        for kaynak in range(n):
            gorulen = {kaynak}
            kuyruk = deque([kaynak])
            while kuyruk:
                u = kuyruk.popleft()
                for v in self._komsu[u]:
                    if v not in gorulen:
                        gorulen.add(v)
                        kuyruk.append(v)
            ulasilan += len(gorulen)
            erisim.append(gorulen)
            if kaynak not in bilinen:
                bilinen |= gorulen
                bilesenler.append(len(gorulen))
        # 🔴 BİLEŞEN YAPISI — "kaç çift ulaşılamaz" YETMEZ.
        # Karıştırıcının dibinde boğulan TEK bir düğüm ile ağın İKİ BÜYÜK
        # parçaya ayrılması aynı ulaşılabilirlik sayısını verebilir ama
        # bilimsel olarak taban tabana zıttır: birincisi incelenen olgunun
        # kendisi, ikincisi ölçümü geçersiz kılan bir confound.
        cok_uyeli = sum(1 for b in bilesenler if b > 1)
        # 🔴 K-186 — YÖNLÜ GRAFİKTE BFS KÜMELERİ BİLEŞEN DEĞİLDİR. Güç
        # kipinde (ED susturması) susan düğümün yalnız GELEN bağı var; bir
        # kaynaktan erişilen küme başkasınınkiyle üst üste biner ve
        # `bilesenler` hem boyut hem sayı olarak yanıltır (en büyük %97,5
        # iken "ikinci ≥ %10" okundu). Simetrik (eski dünya) grafikte ikisi
        # birebir aynıdır. Doğru yapı GÜÇLÜ bağlı bileşenlerdir: iki yönlü
        # haberleşebilen kümeler; susan düğüm tek başına bir bileşendir
        # (boğulma).
        atandi = [False] * n
        guclu: list[int] = []
        for u in range(n):
            if atandi[u]:
                continue
            uye = [v for v in erisim[u] if u in erisim[v]]
            for v in uye:
                atandi[v] = True
            guclu.append(len(uye))
        guclu.sort(reverse=True)
        return {"derece": derece, "ulasilabilirlik": ulasilan / (n * n),
                "en_buyuk_bilesen": max(bilesenler) / n if bilesenler else 0.0,
                "cok_uyeli_bilesen": float(cok_uyeli),
                "yalniz_dugum": float(sum(1 for b in bilesenler if b == 1)),
                # K-186: güçlü bağlı bileşenler — "büyük bölünme" ölçüsü
                "gb_en_buyuk": guclu[0] / n,
                "gb_ikinci": guclu[1] / n if len(guclu) > 1 else 0.0}


class _KahinTabani:
    """Ortak yüzey — protokol arayüzünün kâhin karşılığı."""

    __slots__ = ("kimlik", "_grafik")

    def __init__(self, kimlik: int, grafik: KanalGrafigi) -> None:
        self.kimlik = kimlik
        self._grafik = grafik

    def beacon_yuku(self, gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk) -> None:
        return None

    def teshis(self, dugum: int) -> dict:
        return {}


class EnKisaYolKahin(_KahinTabani):
    """🔴 KÂHİN — mükemmel topoloji bilgisi, EN AZ ATLAMA ölçütü.

    ⚠️ BU BİR TAVAN DEĞİLDİR. En az atlama, en uzun — yani en kötü — bağı
    seçer; kâhin, atlama sayısıyla yönlendiren protokollere atfedilen
    patolojinin tam içindedir. Tavan için `EnGuvenilirKahin`e bak.
    """

    ad = "en_kisa_yol_kahin"
    __slots__ = ()

    def sonraki_atlama(self, gozlem) -> Karar:
        if gozlem.paket is None:
            return Karar()
        return Karar(sonraki=self._grafik.en_kisa_yol_sonraki(
            self.kimlik, gozlem.paket.hedef))


class EnGuvenilirKahin(_KahinTabani):
    """🔴 KÂHİN — mükemmel topoloji bilgisi, EN AZ BEKLENEN İLETİM (ETX).

    🔴 "TAVAN" DEĞİL — İDDİA 9 EYLÜL 2026'DA ÇÜRÜTÜLDÜ.
    Burada şöyle yazıyordu: *"GERÇEK TAVAN BUDUR: hiçbir protokol, bağ
    kalitelerini tam bilen ve beklenen iletim sayısını küçülten bir
    yönlendiriciden daha iyisini yapamaz."* **Evrensel bir cümleydi ve tek
    karşı örnek onu çürütür.** Ölçüldü (`python -u kalibrasyon/bag_kumesi.py
    d`, `statik-surekli`, 15 tohum): `EnKisaYolKahin`, bağ eşiği 0,99 iken
    15 tohumun **6'sında** bu kâhini GEÇİYOR; bugünkü eşikte (0,90) 2'sinde.

    🔒 SEBEP FİZİKSEL: ETX **beklenen İLETİM sayısını** küçültür, **TESLİMİ**
    değil. Yeniden deneme sınırı SONLU (5 deneme) olduğu için ikisi ayrışır:
    toplam ETX'i düşük bir yol, içinde beş denemede de geçemeyen bir bağ
    taşıyabilir. Karıştırma altında ayrışma büyüyor.

    ⚠️ NE DEĞİŞMEDİ: kol ORTALAMASINDA bu kâhin her eşikte önde (ölçüt
    bedeli hiçbir eşikte negatife dönmüyor). Yani "daha kötü" değil,
    **ÜST SINIR DEĞİL**. Bir protokolün bu sayıyı geçmesi kusur işareti
    DEĞİLDİR. Aynı düzeltme K-096'da `EnKisaYolKahin`e yapılmıştı — orada
    sebep ölçütün kendi bedeliydi, burada sonlu yeniden deneme sınırı.

    🔒 Karıştırıcı gücü yine de bu kolda kalibre edilir ve gerekçesi
    DEĞİŞMEDİ: çalışma noktası hiçbir protokolün ölçütüne borçlu olmasın
    diye. Kalibrasyon bir "tavan" iddiası taşımıyor, bir REFERANS taşıyor.
    """

    ad = "en_guvenilir_kahin"
    __slots__ = ()

    def sonraki_atlama(self, gozlem) -> Karar:
        if gozlem.paket is None:
            return Karar()
        return Karar(sonraki=self._grafik.en_guvenilir_sonraki(
            self.kimlik, gozlem.paket.hedef))
