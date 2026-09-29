"""
Gerçek koşucu — tüm katmanları tek koşuda birleştirir.

    trafik → kuyruk → yönlendirme → MAC → radyo → karıştırıcı
                          ↑                  │
                          └──── korunum defteri ────┘

`skeleton.py`nin YERİNE geçer, yanına değil. İskelet kusursuz kanal
kullanıyordu; buradaki her paket gerçek MAC'ten, gerçek çekişmeden ve gerçek
karıştırıcıdan geçer.

🔴 NEDEN BU DOSYA AİLE 0'IN ÇIKIŞ KOŞULU
=========================================
Korunum denklemi bugüne kadar YALNIZCA kusursuz kanalda doğrulandı. Yeniden
iletim, kuyruk taşması ve MAC düşürmesi yolları hiç sınanmadı. Bu koşucu o
yolları açar; korunum burada tutmazsa Aile 0 kapanmaz.

PAKET DURUM GEÇİŞLERİ — defterle birebir
=========================================
    üretildi          → kuyrukta        (uret)
    kuyruktan alındı  → uçuşta          (kuyruktan_al)
    MAC başarılı, ara → kuyrukta        (ucustan_kuyruga)
    MAC başarılı, son → teslim          (teslim_et)
    MAC başarısız     → düşen           (dus "iletim_basarisiz", ucus)
    TTL bitti         → düşen           (dus "ttl", ucus)
    rota yok          → düşen           (dus "hedef_yok", ucus)
    varış kuyruğu dolu→ düşen           (dus "kuyruk_tasmasi", kuyruk)

Başka geçiş yoktur. Yeni bir geçiş eklemek, defteri de güncellemeyi gerektirir
ve korunum testi bunu anında yakalar.
"""

from __future__ import annotations

import hashlib
import math
import statistics as ist
import struct
from typing import Callable

from .config import Konfig
from .events import OlayKuyrugu
from .gozlem import (Gozlem, KomsuKaydi, PaketGorunumu,
                     teshis_dogrula, yuk_bayt, yuku_dondur)
from .results import kaynak_hash
from .ledger import KorunumDefteri
from .mac import KanalErisimi
from .packet import Paket
from .queues import Kuyruk
from .radio import Karistirici, Radyo
from .rng import Akislar
from .topology import Topoloji
from .traffic import TrafikUreteci

# ==========================================================================
# YÖNLENDİRME ARAYÜZÜ — Kat 4
#
# 🔴 Protokol, karar anında YALNIZCA bir `Gozlem` alır. Simülatöre, topolojiye
# ya da karıştırıcıya erişimi YOKTUR ve olamaz.
#
# Fabrika da yalnızca `Konfig` alır — topoloji ALMAZ. Bu bilinçlidir:
# fabrikaya topoloji verilseydi protokol onu kapatır (closure) ve gözlem
# penceresi anlamsızlaşırdı.
#
# ⚠️ Doğrulama aktarıcıları (dogrulama/aktaricilar.py) topolojiyi
# `Konfig`ten YENİDEN ÜRETEREK elde eder. Bu apaçık bir kâhin hamlesidir,
# `dogrulama/` altında yaşar ve deney kolu olarak kullanılamaz.
# ==========================================================================
Protokol = Callable[[Gozlem], "int | None"]
ProtokolFabrikasi = Callable[[Konfig], Protokol]


# 🔴 KOL ETİKETİ VE TEDAVİ ALANLARI — iki kol arasında FARKLI OLABİLİR.
# Geri kalan her konfigürasyon alanı AYNI olmak zorundadır; aksi hâlde iki
# koşu aynı deneyin iki kolu değil, iki farklı deneydir.
#
# `senaryo` ve güç override'ı burada çünkü tedavi onlar: H1.3 S2↔S4'ü,
# H1.2 güç taramasını karşılaştırır ve ikisi de meşrudur.
TEDAVI_ALANLARI = frozenset({
    "kol", "senaryo", "karistirici_guc_override_dbm",
    "takvimli_tazeleme", "bayat_bilgi_null", "not_",
})


def _evren_hash(paketler) -> str:
    """Ölçüm penceresindeki PAKET EVRENİNİN belirlenimci parmak izi.

    Paketin kimliğini tanımlayan her şey: kimlik · doğum anı · kaynak · hedef.

    🔴 `hash()` DEĞİL blake2b: Python'un yerleşik hash'i çalışmalar arasında
    tuzlanır (PYTHONHASHSEED) ve Ç2'yi kırardı — `rng.py`nin aynı gerekçesi.
    """
    h = hashlib.blake2b(digest_size=16)
    for p in paketler:
        h.update(struct.pack("<qdii", p.kimlik, p.dogum_s, p.kaynak, p.hedef))
    return h.hexdigest()


def _kurulum_hash(kon, topo) -> str:
    """Ölçüm KURULUMUNUN parmak izi — tedavi alanları hariç.

    🔴 NEDEN PAKET EVRENİ YETMİYOR (B-26'nın ikinci yarısı):
    `iletim_menzili_m` 280→300 ya da `alan_m` 1000→1010 yapıldığında paket
    evreni AYNI KALABİLİR (aynı kimlik, aynı doğum, aynı kaynak-hedef) ama
    AĞ farklıdır. O iki koşuyu karşılaştırmak, "aynı paketin iki farklı
    ağdaki gecikmesini" karşılaştırmaktır — bir kol farkı değil, bir
    KURULUM farkıdır.

    Düğüm konumları da hash'e girer: konumlar aynı konfigürasyondan
    türese bile, topoloji koşullaması yeniden çekim yapabilir.
    """
    h = hashlib.blake2b(digest_size=16)
    for ad, deger in sorted(kon.sozluk().items()):
        if ad in TEDAVI_ALANLARI:
            continue
        h.update(f"{ad}={deger!r}".encode("utf-8"))
        h.update(b"")
    for x, y in topo.konumlar:
        h.update(struct.pack("<dd", x, y))
    return h.hexdigest()


class Kosu:
    def __init__(self, kon: Konfig, protokol_fabrikasi: ProtokolFabrikasi) -> None:
        self.kon = kon
        self.akislar = Akislar(kon.tohum)
        self.olaylar = OlayKuyrugu()
        self.defter = KorunumDefteri()

        self.topo = Topoloji.uret(kon, self.akislar)
        self.radyo = Radyo.kur(kon)
        self.karistirici = Karistirici.senaryodan(kon, self.akislar)

        self.kuyruklar: dict[int, Kuyruk] = {
            d: Kuyruk(d, kon.kuyruk_kapasitesi, self.defter, self._uyandir)
            for d in range(kon.dugum_sayisi)
        }

        self.mac = KanalErisimi(kon, self.topo, self.radyo, self.olaylar,
                                self.karistirici, self.akislar)
        self.mac.alim_gerceklesti = self._alim_gerceklesti
        self.mac.gonderim_bitti = self._gonderim_bitti
        self.mac.iletim_basarisiz = self._mac_basarisiz
        self.mac.yayin_alindi = self._beacon_alindi

        self.trafik = TrafikUreteci(kon, self.topo, self.akislar,
                                    self.olaylar, self.kuyruklar)
        # 🔴 A-4 (K-047) — HER DÜĞÜM KENDİ PROTOKOL ÖRNEĞİNİ ALIR.
        #
        # Önceki sürüm fabrikayı koşu başına BİR KEZ çağırıyordu ve o tek
        # çağrılabilir 40 düğümün hepsi için çalışıyordu. Üçüncü bağımsız
        # denetim bunu §ANLAŞILMAYANLAR'da işaretledi *("bulgu mu, bilinçli
        # tasarım mı belirleyemedim")* ve yapısal olarak doğrulandı:
        #
        #   Bir protokol, kapanışında tuttuğu bir sözlüğe düğüm A'nın
        #   gördüğünü yazıp düğüm B'nin kararında okuyabilirdi. Bu, gerçek
        #   bir telsizde KARŞILIĞI OLMAYAN, bedava ve kusursuz bir düğümler
        #   arası bilgi kanalıdır — `03` kural 5'in tam hedefi. Hiçbir test
        #   bunu göremezdi; `08` yalnızca MODÜL global'lerini beyan ediyordu.
        #
        # Bugün zararsızdı (`en_kisa_yol`ın önbelleği `(dugum, hedef)` ile
        # anahtarlı), ama Aile 1'in protokolleri bu arayüzle yazılacak.
        #
        # ⚠️ `self.protokol` bir SEVK EDİCİ olarak duruyor: dışarıdan
        # sarmalanabilir (testler bunu yapıyor) ama kararı her zaman
        # düğümün KENDİ örneği verir.
        # Ölçüldü: 40 fabrika çağrısı 15 ms — koşunun %0,2'si.
        self._protokoller: dict[int, Protokol] = {
            d: protokol_fabrikasi(kon) for d in range(kon.dugum_sayisi)
        }
        self.protokol: Protokol = lambda g: self._protokoller[g.dugum](g)

        # 🔴 KOMŞU TABLOSU — t=0'da BOŞ. Yalnızca beacon'la dolar.
        # Menzil tablosundan türetilmez; karıştırma altında beacon kaybolunca
        # komşu görünmez olur ve bu GERÇEK bir etkidir.
        self.komsu_tablosu: dict[int, dict[int, KomsuKaydi]] = {
            d: {} for d in range(kon.dugum_sayisi)
        }
        # Son iletim sonucu (gözlem penceresinin en ucuz alanı)
        self.son_sonuc: dict[int, tuple[str, int] | None] = {
            d: None for d in range(kon.dugum_sayisi)
        }

        # 🔴 H1.1 MEKANİZMA KAPISI — ön-kayıtlı sayaç (B-30).
        # `06` H1.1: "seçilen rotalarda ara bölge bağı (0,05 ≤ PER ≤ 0,9)
        # kaç kez kullanıldı … bu sayaç düşmüyorsa SONUCA BAKILMAZ."
        # Bant `Konfig.ara_bolge_per_bandi`de, tek yerde.
        #
        # ⚠️ KÂHİN TEŞHİS: `mac.bag_gercek_per` simülatörün bildiği gerçek
        # bağ kalitesidir. Karara GİREMEZ; yalnızca rapora girer
        # (`05` §D'nin dördüncü sayacı).
        self.ara_bolge_karar = 0
        self.iyi_bag_karar = 0
        self.olu_bag_karar = 0
        self.yonlendirme_karari = 0
        self._karar_per_toplam = 0.0

        # 🔴 B-45 (K-050) — SEÇİM AVANTAJI: mekanizma kapısının
        # BİLGİYE duyarlı hâli.
        #
        # Üçüncü bağımsız denetim ölçtü: `ara_bolge_karar` oranı bir kolun
        # bağ kalitesi bilgisi kullanıp kullanmadığını DEĞİL, kaç atlama
        # yaptığını izliyor. Sıfır bilgi taşıyan bir null model, bilgili
        # koldan daha iyi skor alabiliyordu — yani ön-kayıtlı kapı
        # (*"bu sayaç düşmüyorsa sonuca bakılmaz"*) ayırt edemiyordu.
        #
        # Bu sayaç `03` B1'in null modelini AYRI BİR KOL yerine ölçümün
        # İÇİNE koyar:
        #
        #     avantaj = (o an ULAŞILABİLİR komşuların ortalama PER'i)
        #             − (protokolün SEÇTİĞİ bağın PER'i)
        #
        # Bilgi taşımayan her kol için beklenen değer **tanım gereği 0**
        # — kaç atlama yaptığından, kaç karar verdiğinden bağımsız.
        # Pozitif: kol ortalamadan İYİ bağ seçiyor. Negatif: daha kötü.
        #
        # ⚠️ KÂHİN TEŞHİS: `bag_gercek_per` karara giremez (`05` §D).
        # Maliyet ölçüldü: karar başına ~6,4 ek PER hesabı, koşunun %7,4'ü.
        self._secim_avantaj_toplam = 0.0
        self._secim_avantaj_karar = 0

        # Aile 1/2'nin protokolleri `05` §D'nin diğer dört teşhis sayacını
        # (bilginin yaşı · kaydın olmadığı karar oranı · yalnızca
        # başarılardan öğrenme · protokolün kendi kestirimi) buraya yazar.
        # 🔴 SLOT ŞİMDİ AÇILIYOR: şema Aile 1 başladıktan sonra
        # değiştirilemez (`03` B5, B-19'un dersi).
        self.protokol_teshis: dict[str, object] = {}

        # Teşhis sayaçları
        self.ttl_olumu = 0
        self.donguyle_olen = 0
        self.hedef_yok = 0
        self.mac_dusurmesi = 0
        # Ç2.3 için: hangi (gönderen, alan, dilim) üçlüsünde hangi çekim görüldü
        self.kanal_izi: dict[tuple[int, int, int], float] = {}

        # 🔴 B-105 — ölçüm penceresinin iki ucundaki sayaç anlık görüntüleri.
        # `kostur()` doldurur. `None` = koşu yapılmadı; pencere ikizleri
        # `None` döner ve bu bir ölçüm koşusunda HATADIR (testle yasaklı).
        self._pencere_bas: dict[str, float] | None = None
        self._pencere_bit: dict[str, float] | None = None
        self._pencere_doluluk: int | None = None

    # ------------------------------------------------------------------ koştur
    # ======================================================================
    # 🔴 B-105 (ALTINCI DENETİM) — SONUÇ SÖZLÜĞÜ İKİ AYRI PENCEREDEN SAYIYORDU
    #
    # `03` Bölüm C sözleşme 4: *"Isınma ayrı, ölçüm ayrı; TÜM SAYAÇLAR AYNI
    # PENCEREDEN."* Ölçüldü (altıncı denetim + bağımsız olarak yeniden,
    # 27 Ağu, 5 kol × 8 yapılandırma = 40 tam koşu):
    #
    #     teslim / gecikme / atlama : [isinma_s, olcum_bitis_s]  = 270 s
    #     26 KÜMÜLATİF SAYAÇ        : [0, kosu_bitis_s]          = 350 s
    #
    #     pencere DIŞINDA üretilen kontrol baytı : %17,63 – %22,84
    #     raporlanan kontrol payı / pencere içi  : 1,0000 – 1,0860
    #
    # 🔴 VE ÇARPIKLIK KOLA GÖRE DEĞİŞİYOR — yani eşleştirilmiş bir kol
    # karşılaştırması YANLI:
    #     gurultuden_kacan · dongu_yapan   1,004 – 1,047
    #     hedefe_en_yakin  · en_kisa_yol   1,054 – 1,079
    #
    # Bu, `08` madde 25'in BAĞLAYICI oranını doğrudan vuruyor.
    #
    # 🔒 MEKANİZMA — SIFIR TEDİRGİNLİK, ÖLÇÜLDÜ.
    # `Olaylar.kostur(bitis_s)` yeniden başlatılabilir: sonraki olaylar
    # yığında kalır. Üç kez artan sınırla çağırmak, tek çağrıyla BİREBİR
    # aynıdır ve **hiç ek olay yaratmaz**. Ölçüldü (3 kol × 3 yapılandırma):
    # tam sonuç sözlüğü 0/9 farklı — `islenen_olay` DÂHİL.
    #
    # ⚠️ Denetçinin ölçüm yöntemi (koşuya iki gözlem olayı ENJEKTE etmek)
    # `islenen_olay`ı +2 kaydırıyordu; bu yol onu da kaydırmaz.
    # ======================================================================

    def kostur(self) -> dict[str, object]:
        self._beaconlari_basla()
        self.trafik.basla()
        pencere_bas, pencere_bit = self.kon.olcum_penceresi

        # 1 · ısınma
        self.olaylar.kostur(pencere_bas)
        self._pencere_bas = self._sayac_anlik()
        for k in self.kuyruklar.values():
            k.pencere_baslat()

        # 2 · ölçüm penceresi
        self.olaylar.kostur(pencere_bit)
        self._pencere_bit = self._sayac_anlik()
        # 🔴 Maksimum bir FARK DEĞİLDİR: pencere bitiminde okunmak zorunda,
        # yoksa boşalma fazındaki dolulukları da yutar.
        self._pencere_doluluk = max(
            k.pencere_en_yuksek_doluluk for k in self.kuyruklar.values())

        # 3 · boruyu boşalt
        self.olaylar.kostur(self.kon.kosu_bitis_s)
        self._protokol_teshislerini_topla()
        return self.sonuc()

    # 🔴 PENCERE İKİZİ OLAN KÜMÜLATİF ALANLAR — ölçülerek belirlendi.
    # Ölçüt: alan `[0, isinma_s)` aralığında ARTIYOR mu. 27 Ağustos 2026,
    # 4 yapılandırma: 26'sının 26'sı artıyor (pencere dışı pay %11,85–%100).
    # 🔴 ÜRETİCİ ÖLÜ — `scratchpad/` dizini depoda YOK (F-4, `10` §8).
    # Yukarıdaki *"26'sının 26'sı artıyor · %11,85-%100"* sayısı bugün
    # ÜRETİLEMİYOR ve **uydurulmadı** (K-053: eski bir kayda üretici
    # komut uydurmak kural 1'in daha ağır ihlalidir).
    # 🟢 Yakın ölçüm: `python dogrulama/pencere_kapsami.py` — pencere
    # DIŞI payı beş sayaç için ölçer (%18,17-22,86, kontrol_bayt).
    # ⚠️ Ama o araç *"hangi alanlar ısınmada ARTIYOR"* ölçütünü
    # yeniden koşmuyor; listenin kendisi hâlâ 27 Ağustos ölçümünden
    # geliyor ve o ölçüm yeniden üretilemiyor. Beyan budur.
    #
    # ⚠️ `en_yuksek_doluluk` BURADA YOKTUR: maksimumdur, farkla türetilemez.
    # Ayrı izlenir (`Kuyruk.pencere_en_yuksek_doluluk`).
    _PENCERE_SAYACLARI: tuple[str, ...] = (
        "kontrol_bayt", "veri_bayt", "kontrol_airtime_s", "veri_airtime_s",
        "yuk_bayt_toplam", "ttl_olumu", "donguyle_olen", "hedef_yok",
        "mac_dusurmesi", "kuyruk_tasmasi", "mac_gonderilen", "mac_onay",
        "mac_kayip_onay", "mac_kopya_alim", "beacon_gonderilen",
        "beacon_alinan", "beacon_kacirilan", "mac_basarisiz_alim",
        "mac_deneme", "islenen_olay", "ara_bolge_karar", "iyi_bag_karar",
        "olu_bag_karar", "yonlendirme_karari", "secim_avantaji_karar",
    )
    # İki TÜREV ortalamanın payları — sonuç alanı değil, ama ikisi de
    # kümülatif ve biri ön-kayıtlı MEKANİZMA KAPISININ ölçtüğü büyüklük.
    _PENCERE_PAYLARI: tuple[str, ...] = (
        "_karar_per_toplam", "_secim_avantaj_toplam",
    )

    def _sayac_anlik(self) -> dict[str, float]:
        """🔴 Y7 — bu sözlük `sonuc()`in KENDİ ifadelerini yansıtır.

        İkinci bir doğru kaynağıdır ve öyle olduğu için BAĞLANIR:
        `test_b105_pencere_aynasi_SONUC_ile_AYNI` her alan için koşu sonundaki
        anlık değerin `sonuc()[alan]`a eşit olduğunu ölçer. Ayrışırsa test
        kırılır (B-07'nin "ikinci doğru kaynağı" dersi).
        """
        return {
            "kontrol_bayt": self.mac.kontrol_bayt,
            "veri_bayt": self.mac.veri_bayt,
            "kontrol_airtime_s": self.mac.kontrol_airtime_s,
            "veri_airtime_s": self.mac.veri_airtime_s,
            "yuk_bayt_toplam": self.mac.yayin_yuk_bayt,
            "ttl_olumu": self.ttl_olumu,
            "donguyle_olen": self.donguyle_olen,
            "hedef_yok": self.hedef_yok,
            "mac_dusurmesi": self.mac_dusurmesi,
            "kuyruk_tasmasi": sum(k.tasma_sayisi
                                  for k in self.kuyruklar.values()),
            "mac_gonderilen": self.mac.gonderilen_veri,
            "mac_onay": self.mac.gonderilen_onay,
            "mac_kayip_onay": self.mac.kayip_onay,
            "mac_kopya_alim": self.mac.kopya_alim,
            "beacon_gonderilen": self.mac.gonderilen_yayin,
            "beacon_alinan": self.mac.alinan_yayin,
            "beacon_kacirilan": self.mac.kacirilan_yayin,
            "mac_basarisiz_alim": self.mac.basarisiz_alim,
            "mac_deneme": self.mac.toplam_deneme,
            "islenen_olay": self.olaylar.islenen_olay,
            "ara_bolge_karar": self.ara_bolge_karar,
            "iyi_bag_karar": self.iyi_bag_karar,
            "olu_bag_karar": self.olu_bag_karar,
            "yonlendirme_karari": self.yonlendirme_karari,
            "secim_avantaji_karar": self._secim_avantaj_karar,
            "_karar_per_toplam": self._karar_per_toplam,
            "_secim_avantaj_toplam": self._secim_avantaj_toplam,
        }

    def _pencere_alanlari(self) -> dict[str, object]:
        """Pencere ikizleri. `kostur()` çağrılmadıysa hepsi `None`.

        🔴 `None`, "sıfır" DEĞİLDİR ve öyle okunmamalıdır: `03` B2'nin
        *"`nan`ı 'etki yok' sanmak"* uyarısının bu şemadaki hâli. Bir ölçüm
        koşusunda `None` görülmesi bir HATADIR ve testle yasaklanmıştır.
        """
        if self._pencere_bas is None or self._pencere_bit is None:
            bos: dict[str, object] = {
                f"{a}_pencere": None for a in self._PENCERE_SAYACLARI}
            bos["en_yuksek_doluluk_pencere"] = None
            bos["karar_bag_per_ortalama_pencere"] = None
            bos["secim_avantaji_ortalama_pencere"] = None
            return bos

        fark = {a: self._pencere_bit[a] - self._pencere_bas[a]
                for a in (*self._PENCERE_SAYACLARI, *self._PENCERE_PAYLARI)}
        cikti: dict[str, object] = {
            f"{a}_pencere": fark[a] for a in self._PENCERE_SAYACLARI}
        cikti["en_yuksek_doluluk_pencere"] = self._pencere_doluluk
        cikti["karar_bag_per_ortalama_pencere"] = (
            fark["_karar_per_toplam"] / fark["yonlendirme_karari"]
            if fark["yonlendirme_karari"] else None)
        cikti["secim_avantaji_ortalama_pencere"] = (
            fark["_secim_avantaj_toplam"] / fark["secim_avantaji_karar"]
            if fark["secim_avantaji_karar"] else None)
        return cikti

    def _protokol_teshislerini_topla(self) -> None:
        """🔴 B-68 (K-056) — SLOTA GİDEN MEŞRU YOL.

        `protokol_teshis` slotu B-30'da açıldı ve *"Aile 1/2'nin protokolleri
        buraya yazar"* denildi — ama **yazacak bir yol yoktu**: arayüz
        `Gozlem → int | None`, `Gozlem` donmuş ve yüzey taraması simülatöre
        erişimi reddediyor. Dördüncü bağımsız denetim ölçtü (B-68):
        `sim/` + `dogrulama/` altında slota yazan **tek satır yok**.

        🔴 Daha ağırı: B-49'un kapanış testi slota yazabilmek için
        fabrikanın `__dict__`ine **`Kosu` nesnesini enjekte ediyordu**
        (`yazan_fabrika._kosu = k`). O desen bir ŞABLON olsaydı, Aile 1'in
        protokolleri `topo`, `karistirici` ve `bag_gercek_per` dâhil her
        şeye ulaşırdı — `03` kural 5'in tam hedefi. Ve `test_c5_1b`in
        sızıntı taraması `Gozlem`den başladığı için o kanalı **göremezdi**.

        Kanca `beacon_yuku`nun deseniyle birebir aynı: isteğe bağlı,
        protokolün KENDİ örneğine ait, simülatöre referans taşımıyor.
        Şekil: `{sayaç_adı: {düğüm: değer}}`.

        🔴 26 AĞUSTOS 2026 — SÖZLEŞME YAZILDI (B-87, K-065). *"Birebir aynı
        desen"* iddiası **yanlıştı**: `beacon_yuku` `yuk_bayt`tan geçip
        tipi/boyutu denetleniyordu, `teshis` **hiçbir denetimden
        geçmiyordu.** Beşinci denetim sekiz sözleşme dışı yük denedi: 8'i de
        kabul edildi, **4'ü** sonuç yazıcısını koşu BİTTİKTEN SONRA düşürdü,
        biri `YASAK_TIPLER`den bir `Konfig` taşıdı. Artık `teshis_dogrula`
        anında ve tipli (`TeshisHatasi`) reddediyor.
        """
        for dugum in sorted(self._protokoller):
            kanca = getattr(self._protokoller[dugum], "teshis", None)
            if kanca is None:
                continue
            # 🔴 B-87: sözleşme ANINDA ve TİPLİ. Öncesinde hiçbir
            # denetim yoktu; sözleşme dışı yük koşu BİTTİKTEN SONRA sonuç
            # yazıcısını ham bir `TypeError` ile düşürüyordu.
            veri = teshis_dogrula(dugum, kanca(dugum))
            if not veri:
                continue
            for ad, deger in veri.items():
                self.protokol_teshis.setdefault(ad, {})[dugum] = deger

    # ---------------------------------------------------------------- beacon
    def _beaconlari_basla(self) -> None:
        """Her düğüm kendi rastgele fazında beacon yayınlar.

        ⚠️ Faz dağıtılmazsa tüm düğümler aynı anda beacon atmaya çalışır,
        çarpışırlar ve komşuluk sistematik olarak eksik öğrenilir. Bu, "aynı
        periyotlu iki süreç" tuzağının somut hâli.
        """
        # 🔴 B-10: KENDİ AKIŞI. Önceki hâli "trafik_zamani"dan çekiyordu —
        # o akışın tanımı "CBR titreşimi"dir ve `AKIS_ADLARI` listesi
        # "kapalıdır" diyor. Akış paylaşımı, `rng.py`nin önlemek için
        # yazıldığı kuplajı geri getiriyordu.
        r = self.akislar["beacon_faz"]
        for d in range(self.kon.dugum_sayisi):
            faz = r.uniform(0.0, self.kon.beacon_araligi_s)
            self.olaylar.ekle(faz, self._beacon_at, d)

    def _beacon_at(self, dugum: int) -> None:
        # 🔴 B-13: erken dönüş değil DEĞİŞMEZ. Ölçüldü: 42 000 çağrının
        # 0'ında tetiklendi — olay kuyruğu `kosu_bitis_s`ten sonrasını zaten
        # işlemiyor. Tetiklenemeyen bir kontrol koruma sağlamaz.
        assert self.olaylar.simdi <= self.kon.kosu_bitis_s, (
            f"koşu bitiminden sonra beacon: {self.olaylar.simdi} > "
            f"{self.kon.kosu_bitis_s}"
        )
        icerik = {
            "gurultu_w": self.mac.olculen_gurultu_w(dugum),
            "kuyruk": len(self.kuyruklar[dugum]),
            "konum": self.topo.konumlar[dugum],
        }

        # 🔴 B-47 (K-049) — PROTOKOLÜN KENDİ KOYDUĞU ALANLAR.
        #
        # `05` §A2 protokole şu hakkı veriyor: *"o alanları başlığa
        # KOYMAK ve bedelini ÖDEMEK."* Bu hakkın 20 Ağustos'a kadar KOD
        # KARŞILIĞI YOKTU — beacon içeriği burada sabitti ve protokolün
        # herhangi bir çerçeveye bilgi koyma yolu bulunmuyordu. Üçüncü
        # bağımsız denetim ölçtü (B-47): saf gözlemle yazılabilen en iyi
        # şey yerel bir rastgele yürüyüştü (S0'da teslim 0,0997, ortalama
        # atlama 1,00) ve ön-kaydın iki rakip protokolü de kurulamıyordu.
        #
        # Kanca İSTEĞE BAĞLI: taşımayan bir protokol için davranış birebir
        # aynı kalır — Aile 0'ın bütün sayıları korunur.
        #
        # 🔴 BEDEL GERÇEK SERİLEŞTİRMEDEN: `yuk_bayt` tel üzerindeki
        # boyutu hesaplar ve beacon çerçevesine EKLENİR — yani hem
        # `kontrol_bayt`a hem `kontrol_airtime_s`e girer. Protokolün kendi
        # beyanına bırakılsaydı, ucuz görünmek isteyen bir protokol az
        # beyan ederdi ve K-009'un "eşit kontrol düzlemi bütçesi" adalet
        # şartı denetlenemez olurdu.
        ek_bayt = 0
        kanca = getattr(self._protokoller[dugum], "beacon_yuku", None)
        if kanca is not None:
            yuk = kanca(dugum)
            if yuk:
                ek_bayt = yuk_bayt(yuk)      # sözleşme dışıysa fırlatır
                icerik["yuk"] = yuku_dondur(yuk)

        self.mac.yayin_gonder(dugum, self.kon.beacon_bayt + ek_bayt,
                              icerik, ek_bayt)
        self.olaylar.gecikmeyle_ekle(self.kon.beacon_araligi_s,
                                     self._beacon_at, dugum)

    def _beacon_alindi(self, gonderen: int, alan: int, icerik: dict) -> None:
        tablo = self.komsu_tablosu[alan]
        onceki = tablo.get(gonderen)
        tablo[gonderen] = KomsuKaydi(
            dugum=gonderen,
            son_duyulma_s=self.olaylar.simdi,
            duyulan_beacon=(onceki.duyulan_beacon + 1) if onceki else 1,
            bildirdigi_gurultu_w=icerik["gurultu_w"],
            bildirdigi_kuyruk=icerik["kuyruk"],
            bildirdigi_konum=icerik["konum"],
            # 🔴 B-47: bayat olabilir, kaybolabilir — `05` §A2'nin 2. ve
            # 3. kuralı burada kendiliğinden geçerli, çünkü yük beacon'la
            # taşınıyor ve beacon karıştırma altında kayboluyor.
            bildirdigi_yuk=icerik.get("yuk", ()),
        )

    def _gozlem_uret(self, dugum: int, paket: Paket | None) -> Gozlem:
        simdi = self.olaylar.simdi
        omur = self.kon.komsu_omru_s
        taze = tuple(k for k in self.komsu_tablosu[dugum].values()
                     if simdi - k.son_duyulma_s <= omur)
        sonuc = self.son_sonuc[dugum]
        return Gozlem(
            dugum=dugum,
            saat_s=simdi,
            olculen_gurultu_w=self.mac.olculen_gurultu_w(dugum),
            kanal_mesgul_mu=self.mac.kanal_mesgul(dugum),
            kuyruk_uzunlugu=len(self.kuyruklar[dugum]),
            kuyruk_kapasitesi=self.kon.kuyruk_kapasitesi,
            son_iletim_sonucu=sonuc[0] if sonuc else None,
            son_iletim_hedefi=sonuc[1] if sonuc else None,
            # 🔴 B-01: DÜĞÜMÜN KENDİ sayaçları. Önceki sürümde buraya ağ
            # geneli toplam sayaçlar bağlıydı — gerçek bir telsizin
            # ölçemeyeceği bir büyüklük protokolün eline geçiyordu.
            gonderilen_bayt=self.mac.dugum_gonderilen_bayt[dugum],
            alinan_bayt=self.mac.dugum_alinan_bayt[dugum],
            komsular=taze,
            paket=None if paket is None else PaketGorunumu(
                hedef=paket.hedef, kaynak=paket.kaynak, ttl=paket.ttl,
                atlama_sayisi=paket.atlama_sayisi, bayt=paket.bayt),
        )

    # -------------------------------------------------------- düğüm iş döngüsü
    def _uyandir(self, dugum: int) -> None:
        """Kuyruğa paket girdi ya da MAC boşaldı → gönderimi dene."""
        if not self.mac.bos_mu(dugum):
            return
        paket = self.kuyruklar[dugum].bak()
        if paket is None:
            return

        gozlem = self._gozlem_uret(dugum, paket)
        sonraki = self.protokol(gozlem)
        if sonraki is None:
            self.kuyruklar[dugum].al()          # kuyrukta -> uçuşta
            self.defter.dus("hedef_yok", nereden="ucus")
            self.hedef_yok += 1
            self._uyandir(dugum)                # sıradakini dene
            return

        # 🔴 H1.1 mekanizma kapısı — kararın SEÇTİĞİ bağın gerçek kalitesi.
        # Protokol bunu görmez; ölçüm defterine yazılır.
        alt, ust = self.kon.ara_bolge_per_bandi
        per = self.mac.bag_gercek_per(dugum, sonraki, self.olaylar.simdi)
        self.yonlendirme_karari += 1

        # 🔴 B-45 — SEÇİM AVANTAJI. Protokolün SEÇEBİLECEĞİ küme, onun
        # gördüğü komşu listesidir; başka bir küme kullanmak kolu
        # göremediği seçeneklerle yargılamak olurdu.
        adaylar = [k.dugum for k in gozlem.komsular]
        if adaylar:
            toplam = 0.0
            for aday in adaylar:
                toplam += self.mac.bag_gercek_per(
                    dugum, aday, self.olaylar.simdi)
            self._secim_avantaj_toplam += toplam / len(adaylar) - per
            self._secim_avantaj_karar += 1
        self._karar_per_toplam += per
        if per < alt:
            self.iyi_bag_karar += 1
        elif per > ust:
            self.olu_bag_karar += 1
        else:
            self.ara_bolge_karar += 1

        self.kuyruklar[dugum].al()              # kuyrukta -> uçuşta
        self.mac.gonder(dugum, paket, sonraki)

    # ------------------------------------------------------------ MAC geri dönüş
    #
    # 🔴 ÜÇ GERİ ÇAĞRI, ÜÇ FARKLI ANLAM (onay gerçek iletim olduğundan beri):
    #
    #   alim_gerceklesti : alıcı paketi KABUL etti → paket el değiştirir,
    #                      DEFTER BURADA güncellenir
    #   gonderim_bitti   : gönderen serbest kaldı (onay geldi ya da alıcı
    #                      zaten kabul etmişti) → defter DEĞİŞMEZ
    #   iletim_basarisiz : alıcı HİÇ kabul etmedi → paket DÜŞER
    #
    # Onay kaybolduğunda alıcı paketi almıştır ama gönderen bilmez. İkisini
    # ayırmazsak paket hem alıcıda olur hem gönderende düşmüş sayılır — tek
    # paket ikiye çıkar ve korunum kırılır.

    def _alim_gerceklesti(self, paket: Paket, gonderen: int, alan: int) -> None:
        paket.atla(gonderen)
        if alan == paket.hedef:
            # TTL teslimatı engellemez: atlama fiilen gerçekleşti.
            paket.teslim_s = self.olaylar.simdi
            self.defter.teslim_et()
        elif paket.ttl <= 0:
            if paket.dongude_mi:
                self.donguyle_olen += 1
            self.defter.dus("ttl", nereden="ucus")
            self.ttl_olumu += 1
        else:
            self.kuyruklar[alan].ekle(paket, yeni_uretilen=False)
        # ⚠️ Gönderen BURADA uyandırılmaz: hâlâ onay bekliyor.

    def _gonderim_bitti(self, paket: Paket, gonderen: int, hedef: int,
                        sonuc: str) -> None:
        """Gönderen serbest — defterde hiçbir şey değişmez.

        🔴 B-02: `sonuc` GÖNDERENİN GÖRDÜĞÜ şeydir, gerçekte olan değil.
        Yeniden deneme hakkı bitip alıcı paketi kabul etmiş olsa bile
        gönderen ONAY GÖRMEMİŞTİR — o durumda `sonuc == "zaman_asimi"`.
        Buraya "onay" yazmak, simülatörün bilgisini protokole sızdırmak
        olurdu.
        """
        self.son_sonuc[gonderen] = (sonuc, hedef)
        self._uyandir(gonderen)

    def _mac_basarisiz(self, paket: Paket, gonderen: int, hedef: int) -> None:
        """Yeniden deneme bitti VE alıcı hiç kabul etmedi — paket düşer."""
        self.defter.dus("iletim_basarisiz", nereden="ucus")
        self.mac_dusurmesi += 1
        self.son_sonuc[gonderen] = ("zaman_asimi", hedef)
        self._uyandir(gonderen)

    # ------------------------------------------------------------------ sonuç
    def sonuc(self) -> dict[str, object]:
        bas, bit = self.kon.olcum_penceresi
        # 🔴 B-98 (BEŞİNCİ DENETİM) — PENCERENİN ÜST SINIRI ULAŞILAMAZ.
        # `olcum_penceresi[1] == olcum_bitis_s` ve trafik üretimi tam orada
        # duruyor (`traffic.py`), yani `dogum_s > bit` olan paket YOKTUR.
        # Ölçüldü: 5 kol × 12 yapılandırma = **60 koşuda 0 paket**
        # (denetçi 18 koşuda ölçmüştü; örneklem genişletildi ve sonuç
        # değişmedi — B-95/B-97'de aynı genişletme onları ÇÜRÜTMÜŞTÜ).
        #
        # Deponun kendi kuralı: *"tetiklenemeyen bir kontrol, koruma
        # sağlamadan koruma İZLENİMİ verir"* — bu yüzden üst sınır bir
        # FİLTRE değil, bir DEĞİŞMEZ olarak duruyor.
        #
        # ⚠️ `python -O` altında bu `assert` SİLİNİR (B-93, `08` madde 27
        # önerisi). Ölçüm koşuları `-O`suz yapılır.
        #
        # 🔒 Üst sınır bir gün ANLAM KAZANIRSA (ör. `kosu_bitis_s`e kadar
        # üreten bir trafik modeli, ya da daraltılmış bir pencere) bu
        # `assert` PATLAR ve filtre geri konmalıdır — sessizce yanlış sayı
        # üretmek yerine.
        pencere = [p for p in self.trafik.uretilen_paketler
                   if bas <= p.dogum_s]
        assert all(p.dogum_s <= bit for p in pencere), (
            "ölçüm penceresinin ÜST sınırı ilk kez tetiklendi: "
            "`dogum_s > olcum_penceresi[1]` olan paket var. Filtre geri "
            "konmalı (B-98).")
        teslim = [p for p in pencere if p.teslim_s is not None]
        gecikmeler = [p.gecikme_s for p in teslim if p.gecikme_s is not None]

        return {
            "teslim_orani": (len(teslim) / len(pencere)) if pencere else None,
            "pencerede_uretilen": len(pencere),
            "pencerede_teslim": len(teslim),
            "ortalama_gecikme_s": ist.mean(gecikmeler) if gecikmeler else None,
            "ortanca_gecikme_s": ist.median(gecikmeler) if gecikmeler else None,
            "ortalama_atlama": (ist.mean(p.atlama_sayisi for p in teslim)
                                if teslim else None),

            # Kontrol yükü BAYT cinsinden (03 B3: paketle sayılmaz)
            "kontrol_bayt": self.mac.kontrol_bayt,
            "veri_bayt": self.mac.veri_bayt,

            # 🔴 B-20 — kontrol yükü AIRTIME cinsinden de raporlanır.
            # Bu düzenekte gerçek kıt kaynak kanal zamanıdır: önbelge her
            # çerçeveye 192 µs sabit ekler, yani aynı baytı daha çok
            # çerçeveye bölen protokol airtime'da daha pahalıdır. Ölçüldü:
            # kontrol payı bayt %2,84 · airtime %5,12 (1,80 kat).
            "kontrol_airtime_s": self.mac.kontrol_airtime_s,
            "veri_airtime_s": self.mac.veri_airtime_s,

            # 🔴 B-19 — ORTAK ALT KÜME ŞEMASI.
            # Gecikme yalnızca TESLİM EDİLEN paketlerden ölçülür. Farklı
            # teslim oranına sahip iki protokolü ham gecikmede
            # karşılaştırmak, kötü protokolü İYİ gösterir — zor paketleri
            # hiç teslim etmediği için dağılıma girmezler. Ölçüldü
            # (denetim B-19): PDR 0,99 → 0,50 inerken gecikme yalnızca %2
            # artıyor. `03` B3 çözümü: "ortak alt küme üzerinden karşılaştır
            # ve kesişim oranını raporla."
            #
            # Bunun için paket BAZINDA teslim bilgisi gerekiyordu; şema
            # taşımıyordu. Anahtar `kimlik`tir ve DOĞRULANDI: paket evreni
            # (kimlik, doğum, kaynak, hedef) protokolden bağımsızdır —
            # trafik akışlarından üretilir. Regresyon:
            # `test_b19_paket_evreni_protokolden_bagimsiz`.
            #
            # ⚠️ Şema SONRADAN değiştirilemez (`03` B5 "şemanın kaybolması"):
            # Aile 1 başladıktan sonra eklenirse eski satırlar
            # karşılaştırılamaz hâle gelirdi.
            "teslim_kimlikleri": [p.kimlik for p in teslim],
            "teslim_gecikmeleri_s": [p.gecikme_s for p in teslim],
            "pencere_kimlik_araligi": (
                [pencere[0].kimlik, pencere[-1].kimlik] if pencere else None),

            # 🔴 B-26 — PAKET EVRENİ PARMAK İZİ.
            # Önceki koruma yalnızca `pencerede_uretilen` + kimlik aralığına
            # bakıyordu; ikisi de YALNIZCA `trafik_zamani` akışından
            # belirlenir, yani tohum dışında hiçbir konfigürasyon farkı onları
            # değiştiremez. İkinci denetim bunu kırdı: `dugum_sayisi` 40→41
            # yapıldığında iki kolun HİÇBİR paketi ortak değilken koruma
            # karşılaştırmayı kabul etti ve gecikme farkı üretti.
            #
            # Parmak izi paketin KİMLİĞİNİ TANIMLAYAN her şeyi kapsar:
            # kimlik · doğum anı · kaynak · hedef. Aynı parmak izi ⇒ iki kol
            # gerçekten aynı paket evrenini gördü.
            "pencere_evren_hash": _evren_hash(pencere),
            "kurulum_hash": _kurulum_hash(self.kon, self.topo),
            # 🔴 B-46 (K-051) — KOD SÜRÜMÜ.
            # `05` §E'nin sonuç sözleşmesi *"Kod sürümü"*nü ZORUNLU alan
            # sayıyor ve `results.kaynak_hash()` onu üretiyordu — ama
            # sonuç satırı onu TAŞIMIYORDU. Üçüncü bağımsız denetim
            # bunu Y11 ile kırdı: birebir aynı konfigürasyon ve tohum,
            # tek fark simülatör KODU (geri çekilme kaldırılmış), ve
            # `ortak_alt_kume` 7,76 ms'lik bir "gecikme farkı" üretti.
            #
            # B-26'nın dersi *"koruma yalnızca yakalayabildiği durumla
            # sınanamaz"* idi; düzeltmesi KONFİGÜRASYON eksenine
            # yazılmıştı, KOD ekseni açık kalmıştı.
            "kaynak_hash": kaynak_hash(),

            # 🔴 H1.1 MEKANİZMA KAPISI (B-30) — ön-kayıtlı sayaç.
            # Bant: `Konfig.ara_bolge_per_bandi`. Bu üçü kararın SEÇTİĞİ
            # bağın GERÇEK kalitesine göre bölünür; toplamları
            # `yonlendirme_karari`ye eşittir.
            "ara_bolge_karar": self.ara_bolge_karar,
            "iyi_bag_karar": self.iyi_bag_karar,
            "olu_bag_karar": self.olu_bag_karar,
            "yonlendirme_karari": self.yonlendirme_karari,
            "karar_bag_per_ortalama": (
                self._karar_per_toplam / self.yonlendirme_karari
                if self.yonlendirme_karari else None),
            "ara_bolge_per_bandi": list(self.kon.ara_bolge_per_bandi),
            # 🔴 B-45: mekanizma kapısının BİLGİYE duyarlı ölçütü.
            # Sıfır bilgi taşıyan bir kol için beklenen değer 0'dır.
            "secim_avantaji_ortalama": (
                self._secim_avantaj_toplam / self._secim_avantaj_karar
                if self._secim_avantaj_karar else None),
            "secim_avantaji_karar": self._secim_avantaj_karar,
            # Protokol tarafından doldurulan teşhisler (`05` §D). Aile 0'da
            # boş; slot şemayı dondurmak için şimdi açıldı.
            "protokol_teshis": dict(self.protokol_teshis),
            # 🔴 B-47: kontrol yükünün NE KADARI protokolün kendi
            # koyduğu alanlardan geliyor (`kontrol_bayt`ın içinde).
            "yuk_bayt_toplam": self.mac.yayin_yuk_bayt,

            # Teşhis
            "ttl_olumu": self.ttl_olumu,
            "donguyle_olen": self.donguyle_olen,
            "hedef_yok": self.hedef_yok,
            "mac_dusurmesi": self.mac_dusurmesi,
            "kuyruk_tasmasi": sum(k.tasma_sayisi for k in self.kuyruklar.values()),
            "en_yuksek_doluluk": max(k.en_yuksek_doluluk
                                     for k in self.kuyruklar.values()),
            "mac_gonderilen": self.mac.gonderilen_veri,
            "mac_onay": self.mac.gonderilen_onay,
            "mac_kayip_onay": self.mac.kayip_onay,
            "mac_kopya_alim": self.mac.kopya_alim,
            "beacon_gonderilen": self.mac.gonderilen_yayin,
            "beacon_alinan": self.mac.alinan_yayin,
            "beacon_kacirilan": self.mac.kacirilan_yayin,
            "ort_komsu_sayisi": (
                sum(len(t) for t in self.komsu_tablosu.values())
                / self.kon.dugum_sayisi),
            "mac_basarisiz_alim": self.mac.basarisiz_alim,
            "mac_deneme": self.mac.toplam_deneme,

            # Kapı verileri
            "yakinsama": self.yakinsama_kontrolu(),
            "boruda_kalan": self.defter.kuyrukta + self.defter.ucusta,
            "islenen_olay": self.olaylar.islenen_olay,

            "topoloji": self.topo.ozet(),
            "trafik": self.trafik.ozet(),

            # ==============================================================
            # 🔴 `05` §E SONUÇ SÖZLEŞMESİ — BEŞ ZORUNLU ALANIN KALAN DÖRDÜ
            #
            # Üçüncü denetim `05` §E'yi okudu, BEŞ alandan BİRİNİN eksik
            # olduğunu gördü, onu ekletti (`kaynak_hash` — B-46/K-051) ve
            # **kalan dördüne bakmadı.** Altıncı denetim aynı paragrafı
            # yeniden okudu (B-107): 47 alanlık şemada
            #   · tüm konfigürasyon bayrakları : YOK
            #   · tohum                        : YOK (`kurulum_hash`in içinde,
            #                                    tek yönlü, geri çözülemez)
            #   · korunum denklemi sonucu      : YOK (B-104)
            #   · ölçüm penceresi              : YOK
            #     (`pencere_kimlik_araligi` PAKET KİMLİĞİDİR, zaman değil)
            #
            # 🔒 `03` Bölüm C: bu sözleşme **sonradan eklenemez** — Aile 1
            # başlayınca şema donar (B-19'un dersi).
            # ==============================================================
            "konfig": self.kon.sozluk(),
            "olcum_penceresi_s": list(self.kon.olcum_penceresi),

            # 🔴 B-104 — KORUNUM DENKLEMİ SONUÇ SATIRINDA.
            # `03` Bölüm C: *"her koşuda OTOMATİK"*. Ölçüldü (altıncı denetim
            # + bağımsız olarak yeniden): `sim/` altında `defter.kontrol()`
            # çağrısı **0** idi ve 47 anahtarlı sonuçta `korunum_tamam` yoktu.
            # Somut sonucu: `dogrulama/mekanizma_kapisi.py` — AİLE 1'İN HER
            # KOLUNU GEÇİREN KAPI — kol başına 48 tam koşu yapıyor ve
            # hiçbirinde korunumu kontrol etmiyordu.
            #
            # `kontrol()` istisna fırlatmaz: tutmayan satır `korunum_tamam`
            # ile İŞARETLENİR ve analiz onu dışlar. Bozuk bir koşuyu SİLMEK,
            # kaç koşunun bozuk olduğunu da silmek demektir (`results.py`).
            "korunum": self.defter.kontrol(),
            "korunum_tamam": self.defter.kontrol()["korunum_tamam"],

            # 🔴 B-105 — 25 KÜMÜLATİF SAYACIN PENCERE İKİZİ + maksimum +
            # iki türev ortalama. Ayrıntılı gerekçe `kostur()`un üstünde.
            **self._pencere_alanlari(),
        }

    # ------------------------------------------------------- yakınsama (K5)
    def _yakinsama_dilimleri(self) -> tuple[list[tuple[float, float]], str]:
        """Yakınsama dilimlerini üretir — ORTAMIN PERİYODUNA HİZALI.

        🔴 K-035 (bağımsız denetim) düzeltmesi.

        Önceki sürümde pencere her zaman ÜÇ EŞİT dilime bölünüyordu. Hareketli
        karıştırıcının yörünge periyodu bu dilime bölünmediğinde her dilim
        yörüngenin farklı bir fazını görüyor ve kapı, ortada ÖĞRENME sorunu
        olmadığı hâlde ateşliyordu (28/30 koşu).

        O sorun bir kez karıştırıcı HIZI değiştirilerek "çözülmüştü" — yani
        metrik yerine FİZİK ayarlanmıştı. Ölçüldü: bu, faz kaynaklı varyansı
        3,3 kat bastırıyordu (`03` B6 örtüşmesi) ve kural 3/12 ihlaliydi.

        Doğru çözüm budur: dilimler ortamın periyoduna göre kesilir, fiziğe
        dokunulmaz.
        """
        bas, bit = self.kon.olcum_penceresi
        pencere = bit - bas
        kj = self.karistirici

        if kj is not None and kj.hareketli:
            periyot = 2 * math.pi * kj.yorunge_yaricap_m / kj.hiz_ms
            tam_tur = int(pencere // periyot)
            if tam_tur >= 2:
                # Her dilim TAM BİR YÖRÜNGE. Artan kısım DIŞLANIR: kısmi bir
                # yörünge, tam yörüngelerle karşılaştırılamaz.
                return ([(bas + i * periyot, bas + (i + 1) * periyot)
                         for i in range(tam_tur)],
                        f"yörünge-hizalı ({tam_tur} tam tur, {periyot:.1f} s)")
            return [], "pencere < 2 yörünge — kapı uygulanamaz"

        adim = pencere / 3.0
        return ([(bas + i * adim, bas + (i + 1) * adim) for i in range(3)],
                "üç eşit dilim")

    def yakinsama_kontrolu(self) -> dict[str, object]:
        """Dilimler arası teslim oranı sabit mi?

        Isınma asimetriktir: öğrenen bir kol tepkisel bir koldan yavaş
        yakınsar. Yakınsamamış bir kolun sonucu, öğrenmenin kalitesini değil
        yakınsama hızını ölçer — ve ikisi farklı sorulardır.
        """
        dilimler, gerekce = self._yakinsama_dilimleri()
        if not dilimler:
            return {"dilim_oranlari": [], "yakinsadi": None,
                    "en_buyuk_fark": None, "dilim_gerekcesi": gerekce,
                    "teslim_gozlem": 0}

        oranlar: list[float | None] = []
        toplam_teslim = 0
        for a, b in dilimler:
            dilim = [p for p in self.trafik.uretilen_paketler
                     if a <= p.dogum_s < b]
            teslim = sum(1 for p in dilim if p.teslim_s is not None)
            toplam_teslim += teslim
            oranlar.append(teslim / len(dilim) if dilim else None)

        gecerli = [o for o in oranlar if o is not None]
        if len(gecerli) < len(dilimler):
            return {"dilim_oranlari": oranlar, "yakinsadi": None,
                    "en_buyuk_fark": None, "dilim_gerekcesi": gerekce,
                    "teslim_gozlem": toplam_teslim}

        # 🔴 B-11: PDR = 0 dejenere durumu.
        # Hiçbir şey teslim edilmediğinde tüm dilimler 0,0 olur, fark 0,0
        # çıkar ve kapı bu koşuya MÜMKÜN OLAN EN İYİ skoru verir.
        # "Hiçbir şey teslim edilmedi" ile "mükemmel yakınsadı" aynı sayıya
        # eşlenemez. 540 koşuluk matriste tam olarak bir koşu böyleydi.
        if toplam_teslim == 0:
            return {"dilim_oranlari": oranlar, "yakinsadi": None,
                    "en_buyuk_fark": None, "dilim_gerekcesi": gerekce,
                    "teslim_gozlem": 0,
                    "dejenere": "hiç teslim yok — yakınsama tanımsız"}

        fark = max(gecerli) - min(gecerli)
        return {
            "dilim_oranlari": oranlar,
            "en_buyuk_fark": fark,
            "dilim_gerekcesi": gerekce,
            "teslim_gozlem": toplam_teslim,
            # Eşik burada BİLGİ amaçlı; kapı kararı analiz tarafında verilir.
            "yakinsadi": fark < 0.05,
        }
