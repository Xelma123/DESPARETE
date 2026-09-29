"""
🔴 H1.1'İN ÖN-KAYITLI MEKANİZMA KAPISI (B-30).

`06-ON-KAYIT.md` H1.1 şunu ilan ediyor:

    "mekanizma kontrolü 'seçilen rotalarda ARA BÖLGE BAĞI
     (0,05 ≤ PER ≤ 0,9) kaç kez kullanıldı' olacak. Bu sayaç düşmüyorsa,
     teslimdeki fark başka bir sebepten geliyor demektir ve SONUCA BAKILMAZ."

İkinci bağımsız denetim (B-30) bu sayacın **sonuç şemasında hiç olmadığını**
buldu: 34 anahtar vardı, hiçbiri bu değildi. Ve `03` B5 / K-041 gereği şema
Aile 1 başlamadan dondurulmalı — sonra eklenirse o güne kadarki bütün
satırlar karşılaştırılamaz olur.

⚠️ KÂHİN AYRIMI: sayaç `mac.bag_gercek_per`i kullanır — simülatörün bildiği
GERÇEK bağ kalitesi. `05` §D: gerçek değer yalnızca teşhise, protokolün
tahmini yalnızca karara girer. Bu testler o ayrımı da korur.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import (  # noqa: E402
    AKTARICILAR, en_kisa_yol, kalite_ablasyonu,
)
from sim.config import Konfig  # noqa: E402
from sim.gozlem import (  # noqa: E402
    IZINLI_GOZLEM_ALANLARI, Gozlem, KomsuKaydi,
)
from sim.kosucu import Kosu  # noqa: E402


def _kos(aktarici=en_kisa_yol, **kw):
    kon = Konfig(kol="t", senaryo=kw.pop("senaryo", "S2"),
                 trafik=kw.pop("trafik", "orta"), tohum=kw.pop("tohum", 1), **kw)
    return Kosu(kon, aktarici).kostur()


def test_b30_mekanizma_sayaci_semada_var_ve_tam():
    """Sayaç şemada olmalı ve üç kova toplamı paydaya eşit olmalı."""
    s = _kos()
    for alan in ("ara_bolge_karar", "iyi_bag_karar", "olu_bag_karar",
                 "yonlendirme_karari", "karar_bag_per_ortalama",
                 "ara_bolge_per_bandi", "protokol_teshis"):
        assert alan in s, f"{alan!r} şemada yok — H1.1 ölçülemez"

    toplam = s["yonlendirme_karari"]
    assert toplam > 1000, f"karar sayısı fazla küçük ({toplam}) — test zayıf (Y7)"
    assert (s["iyi_bag_karar"] + s["ara_bolge_karar"] + s["olu_bag_karar"]
            == toplam), "kovalar paydayı tüketmiyor"


def test_b30_band_on_kayitla_ayni_ve_tek_kaynakta():
    """Bant `Konfig`te tek yerde; sonuç satırı onu TAŞIYOR.

    K-020'nin "11–17 ara bölge" sayısı bandı yazmadığı için yeniden
    üretilemedi (ikinci denetim §8-1). Bant sonuç satırında yazılı olmazsa
    aynı şey bu sayaç için de olur.
    """
    kon = Konfig(kol="t")
    assert kon.ara_bolge_per_bandi == (0.05, 0.9)
    assert _kos()["ara_bolge_per_bandi"] == [0.05, 0.9]


def _oran(sonuc: dict, alan: str) -> float:
    """Karar BAŞINA oran — mutlak sayı değil.

    Ayrı bir yüklem olarak duruyor çünkü `03` B5: *"karar üreten yüklemleri
    AYRI ve TEST EDİLEBİLİR yaz."* Gerçek koşularda mutlak sayıyla aynı
    kararı verdiği için, bağlayıcılığı ancak böyle gösterilebiliyor.
    """
    n = sonuc["yonlendirme_karari"]
    return sonuc[alan] / n if n else 0.0


def test_b30_sayac_bag_kalitesine_DUYARLI():
    """🔴 KAPININ ASIL SORUSU: sayaç mekanizmayı ayırt ediyor mu?

    `03` B4: "Kör mekanizma ölçütü — ölçütün, sorduğun soruya duyarlı
    olduğunu AYRICA doğrula."

    `en_kisa_yol` bağ kalitesine **tanım gereği kördür**; `gurultuden_kacan`
    gözlemden gürültü okuyup ondan kaçar. İkincisi ara bölge bağını belirgin
    biçimde AZ kullanmalı — kullanmıyorsa sayaç mekanizmayı ölçmüyordur.
    """
    kor = _kos(AKTARICILAR["en_kisa_yol"])
    kacan = _kos(AKTARICILAR["gurultuden_kacan"])

    p_kor = kor["ara_bolge_karar"] / kor["yonlendirme_karari"]
    p_kacan = kacan["ara_bolge_karar"] / kacan["yonlendirme_karari"]

    assert p_kor > 2 * p_kacan, (
        f"ara bölge kullanımı: kör {100*p_kor:.2f}% vs kaçan "
        f"{100*p_kacan:.2f}% — sayaç bağ kalitesine duyarlı değil"
    )
    # 🔴 B-45: ORAN, mutlak sayı DEĞİL. İlk yazımı `kor["olu_bag_karar"] >
    # kacan["olu_bag_karar"]` diyordu; iki kolun karar sayısı 7 342'ye karşı
    # 72 775 — **10 kat**. Mutlak sayı karşılaştırması, kararı az veren bir
    # kolu tanım gereği "iyi" gösterirdi.
    #
    # ⚠️ ÖLÇÜLDÜ: bugünkü aktarıcı çiftinde iki biçim AYNI kararı veriyor
    # (2 236 > 140 hem mutlak hem oran olarak). Yani bu düzeltmenin
    # bağlayıcılığı GERÇEK KOŞULARLA gösterilemiyor — mutlak biçime dönen
    # bir mutasyon bu testten sağ çıkıyor. Yüklem bu yüzden ayrıldı ve
    # sentetik girdiyle ayrıca sınanıyor: `test_b45_oran_yuklemi_...`
    o_kor = _oran(kor, "olu_bag_karar")
    o_kacan = _oran(kacan, "olu_bag_karar")
    assert o_kor > o_kacan, (
        f"ölü bağ kullanımı: kör {100*o_kor:.2f}% vs kaçan "
        f"{100*o_kacan:.2f}%")

    # 🔴 B-45: BU İKİ ÖLÇÜT TEK BAŞINA YETMEZ — null model sınavını
    # `test_b45_...` yapar. Ara bölge oranı yol GEOMETRİSİNE duyarlıdır;
    # bilgi taşımayan bir kol da bu ölçütü geçebilir.


def test_b30_karar_bag_kalitesi_karistirici_gucuyle_monoton_kotulesiyor():
    """Y8 — sayacın tetiklendiği yolu göster.

    ⚠️ İLK YAZIMI YANLIŞ BİR VARSAYIMA DAYANIYORDU ve kırıldı: *"karıştırma
    artınca ara bölge kullanımı artar."* ÖLÇÜLDÜ, artmıyor —

        güç   iyi    ARA    ölü   ort PER
        S0    9595    959      0   0,0085
        -10   7994   2240    320   0,0701
        +2    4469    637   2236   0,3282
        +4    2525   2532   2224   0,3755
        +11    640    320   2809   0,8076

    Ara bölge bir **ORTA DİLİM**. K-020 bağ geçişinin çok keskin olduğunu
    ölçtü *(PER %1→%99 yalnızca 2,79 dB'de)*; dolayısıyla karıştırma bağları
    bandın İÇİNDEN GEÇİRİP ölü kovaya taşıyor, bantta biriktirmiyor. Sayı
    güce göre **monoton değil**.

    🔴 SONUCU — bu sayaç YALNIZCA AYNI ÇALIŞMA NOKTASINDA İKİ KOL ARASINDA
    karşılaştırılabilir; güçler arası okunamaz. H1.1'in kapısı zaten öyle
    kurulmuş *(S2'de, kollar arası)*, ama bu sınır yazılı olmalıydı.

    Monoton olan büyüklük **ortalama bağ PER'idir**; kapının tetiklendiğini
    o gösterir.
    """
    onceki = -1.0
    for guc in (None, -10.0, -4.0, 0.0, 2.0, 4.0, 8.0, 11.0):
        kw = {} if guc is None else dict(karistirici_guc_override_dbm=guc)
        s = _kos(senaryo="S0" if guc is None else "S2", **kw)
        per = s["karar_bag_per_ortalama"]
        assert per > onceki, (
            f"güç {guc}: ortalama karar PER'i {per:.4f} ≤ önceki {onceki:.4f} "
            f"— sayaç karıştırıcı gücüne duyarlı değil"
        )
        onceki = per

    # Karıştırıcısız kolda ÖLÜ bağ kararı olmamalı; karıştırma onu doğurur.
    assert _kos(senaryo="S0")["olu_bag_karar"] == 0
    assert _kos(senaryo="S2")["olu_bag_karar"] > 1000


def test_b30_gercek_per_gozlem_penceresine_SIZMIYOR():
    """🔴 `05` §D: gerçek değer teşhise, protokolün tahmini karara.

    `bag_gercek_per` bir KÂHİN büyüklüktür. Gözlem yüzeyinde adı geçen
    hiçbir alan olmamalı ve `Gozlem` bu bilgiyi taşımamalı.
    """
    yasak = {"bag_gercek_per", "gercek_per", "ara_bolge", "per"}
    assert not (yasak & set(IZINLI_GOZLEM_ALANLARI)), IZINLI_GOZLEM_ALANLARI

    k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol)
    g = k._gozlem_uret(0, None)
    assert not any(a in yasak for a in vars(g)), vars(g).keys()


def test_b30_protokol_teshis_slotu_acik_ve_bos():
    """Aile 0'da boş; Aile 1'in protokolleri `05` §D'nin dört sayacını yazar.

    Slot ŞİMDİ açık olmalı: şema sonradan değiştirilirse eski satırlar
    karşılaştırılamaz (`03` B5).
    """
    s = _kos()
    assert isinstance(s["protokol_teshis"], dict)
    assert s["protokol_teshis"] == {}, "Aile 0'da protokol teşhisi olmamalı"


# ==========================================================================
# 🔴 B-45 — MEKANİZMA KAPISI BİLGİYİ Mİ ÖLÇÜYOR, GEOMETRİYİ Mİ?
#
# Üçüncü bağımsız denetim `03` B1'in istediğini yaptı: aynı yapısal etkiyi
# üreten ama SIFIR bilgi taşıyan bir null model kurdu. Sonuç: null model
# `ara_bolge_karar` ölçütünü geçiyordu — yani ölçüt *"bu kol bağ kalitesi
# bilgisi kullanıyor"* ile *"bu kol kaç atlama yapıyor"*u ayırt edemiyordu.
#
# Ön-kayıt (H1.1) bu sayaca bir KAPI bağlamış: *"bu sayaç düşmüyorsa,
# teslimdeki fark başka bir sebepten geliyor demektir ve SONUCA BAKILMAZ."*
# Ayırt edemeyen bir kapı, kapı değildir.
#
# ÇÖZÜM — `secim_avantaji_ortalama`: null modeli ayrı bir kol yerine
# ÖLÇÜMÜN İÇİNE koyar.
#
#     avantaj = (o an ulaşılabilir komşuların ortalama gerçek PER'i)
#             − (protokolün seçtiği bağın gerçek PER'i)
#
# Bilgi taşımayan her kol için beklenen değer **tanım gereği 0**.
# ==========================================================================

def _null_rastgele(kon):
    """SIFIR BİLGİ — komşulardan birini belirlenimci sözde-rastgele seçer."""
    def sonraki(g):
        if not g.komsular:
            return None
        adaylar = sorted(k.dugum for k in g.komsular)
        i = (g.dugum * 2654435761 + len(adaylar) * 40503) % len(adaylar)
        return adaylar[i]
    return sonraki


def _null_kuyruk(kon):
    """İLGİSİZ ALAN — bağ kalitesiyle ilgisi olmayan bir gözlem alanı okur."""
    def sonraki(g):
        if not g.komsular:
            return None
        return min(sorted(g.komsular, key=lambda k: k.dugum),
                   key=lambda k: k.bildirdigi_kuyruk).dugum
    return sonraki


def test_b45_secim_avantaji_NULL_MODELDE_sifira_yakin():
    """🔴 Kapının null model sınavı.

    İki farklı *"bilgi taşımayan"* kol — biri rastgele seçen, biri bağ
    kalitesiyle ilgisiz bir alan okuyan — sıfıra yakın avantaj almalı.
    Almıyorsa ölçüt bilgiyi değil başka bir şeyi ölçüyordur.

    ⚠️ İki null kolun ortalama atlaması **çok farklıdır** (ölçüldü: 15,50 ve
    6,00). Ölçüt buna rağmen ikisini de sıfıra yakın veriyorsa, yol
    geometrisinden bağımsız demektir — eski `ara_bolge_karar` ölçütünün
    başaramadığı tam olarak buydu.

    🔴 21 AĞUSTOS 2026 — BU TESTİN İDDİASI ÇÜRÜTÜLDÜ (B-65, K-056).
    ---------------------------------------------------------------------
    `abs(av) < 0.02` eşiği **TEK TOHUMDA (1) kalibre edilmişti** ve ayarlama
    tohumlarının **7/8'inde düşüyor**. Dördüncü bağımsız denetim ölçtü;
    devralan ajan birebir yeniden üretti:

        tohum      1       2       3       4       5       6       7       8
        null   +0,008  −0,029  +0,075  +0,199  +0,052  +0,069  +0,041  +0,017

    Null'un tohumlar arası **std'si 0,063** — eşiğin **üç katı**. Tohum 1'de
    görülen +0,008, eşiğin altındaki **tek** çekimdi. `03` kural 2
    *("tek/az tohumlu sonuç raporlama")* ön-kaydın KENDİ kapısında ihlal
    edilmişti.

    SEBEP ÖLÇÜLDÜ: kestirimin beklenen değeri yalnızca **karar başına**
    düzgün rastgeleleştirme altında sıfırdır. Her gerçek protokol (ve
    projenin iki null'ü de) **kalıcı** seçim yapar; kalıcılık tek başına
    ~+0,06 avantaj satın alır.

    Bu test artık mutlak eşik SINAMAZ — kapı `test_b65_…`e taşındı. Burada
    kalan tek iddia, ölçümün **yeterli veriye** dayandığıdır.
    """
    for ad, fab in (("rastgele", _null_rastgele), ("kuyruk", _null_kuyruk)):
        s = _kos(fab)
        assert s["secim_avantaji_karar"] > 1000, (
            f"{ad}: yalnızca {s['secim_avantaji_karar']} karar — ölçüm zayıf")


def test_b45_secim_avantaji_BILGILI_kolu_NULLDAN_ayiriyor():
    """Ölçüt, bilgi taşıyan kolu null modelden AYIRT ETMELİ.

    `gurultuden_kacan` gözlemden gürültü okuyup ondan kaçar — ortalamadan
    İYİ bağ seçmeli. `en_kisa_yol` bağ kalitesine tanım gereği kördür ve
    (H1.1'in mekanizması) ortalamadan KÖTÜ bağ seçmeli.

    🔴 21 AĞUSTOS 2026 — `kacan > 3·abs(nul)` ÖLÇÜTÜ DE ÇÜRÜTÜLDÜ
    (B-65): 8 tohumun **5'inde** düşüyor, çünkü `nul` kalıcılık yüzünden
    sıfırda değil. `kor < −0.05` ise **2/8** tohumda düşüyor (tohum 6 ve 8;
    tohum 8'de kalite körü kol **pozitif** avantaj alıyor: +0,009).

    Kapı `test_b65_…`e taşındı. Burada kalan tek iddia, tohum 1'de
    **yönlerin** doğru olduğudur — bu bir KAPI DEĞİL, bir duman testidir.
    """
    kacan = _kos(AKTARICILAR["gurultuden_kacan"])["secim_avantaji_ortalama"]
    kor = _kos(AKTARICILAR["en_kisa_yol"])["secim_avantaji_ortalama"]

    assert kacan > 0, f"gürültüden kaçan kol avantaj kazanmıyor: {kacan:+.5f}"
    assert kor < kacan, (
        f"kalite körü kol ({kor:+.5f}), bilgili koldan ({kacan:+.5f}) daha "
        f"iyi bağ seçiyor — yön ters")


def test_b45_secim_avantaji_ATLAMA_SAYISINDAN_bagimsiz():
    """🔴 Y11 — ölçütün kapsamı dışındaki vaka: çok atlamalı ama BİLGİSİZ kol.

    Eski ölçüt (`ara_bolge_karar` oranı) tam burada düşüyordu: 15,5 atlama
    yapan bilgisiz bir kol, 1,57 atlama yapan bilgili koldan **daha yüksek**
    ara bölge oranı alıyordu. Yeni ölçüt bu iki kolu doğru sıralamalı.
    """
    nul = _kos(_null_rastgele)
    kacan = _kos(AKTARICILAR["gurultuden_kacan"])

    # Kurulum varsayımı: atlama sayıları GERÇEKTEN çok farklı olmalı
    assert nul["ortalama_atlama"] > 2 * kacan["ortalama_atlama"], (
        f"kurulum varsayımı tutmuyor: null {nul['ortalama_atlama']:.2f} vs "
        f"kaçan {kacan['ortalama_atlama']:.2f}")

    # Eski ölçüt bu iki kolu YANLIŞ sıralıyor — kayda geçsin
    p_nul = nul["ara_bolge_karar"] / nul["yonlendirme_karari"]
    p_kacan = kacan["ara_bolge_karar"] / kacan["yonlendirme_karari"]
    assert p_nul > p_kacan, (
        "beklenen: eski ölçüt bilgisiz kolu bilgili koldan KÖTÜ gösteriyor "
        "(B-45'in kanıtı). Bu tutmuyorsa kurulum değişmiş demektir.")

    # Yeni ölçüt DOĞRU sıralıyor
    assert kacan["secim_avantaji_ortalama"] > nul["secim_avantaji_ortalama"], (
        f"yeni ölçüt de yanlış sıralıyor: kaçan "
        f"{kacan['secim_avantaji_ortalama']:+.5f} vs null "
        f"{nul['secim_avantaji_ortalama']:+.5f}")


# ==========================================================================
# 🔴 B-84 (BEŞİNCİ DENETİM) — ABLASYON İKİ EKSENİ BİRDEN DEĞİŞTİRİYORDU
#
# `06` ön-kaydı diyordu ki: *"aynı protokol, aynı kalıcılık, aynı topoloji …
# **Tek fark BİLGİ**."* Ölçümle YANLIŞTI.
#
# `kalite_ablasyonu` komşu demetini `sorted(..., key=dugum)` hâliyle geri
# veriyordu; asıl kol demeti DOĞAL sırasında görüyordu. Ölçüldü:
#
#     >1 komşulu karar : 72 071
#     SIRASIZ gelen    : 66 863   (%92,8)
#
# Yani ablasyon kolu ile asıl kol arasında **ikinci bir fark** vardı ve o
# fark bilgi değildi. Sıraya duyarlı, SIFIR kalite bilgisi taşıyan bir kolda
# ölçülen farkın **%100'ü** bu artefaktdı (TAM ablasyon farkı ile
# YALNIZCA-SIRALAMA farkı beş ondalığa kadar birebir aynı çıktı):
#
#     sira_kolu · TAM ablasyon      ort=+0,01205  std=0,08091  4/8
#     sira_kolu · YALNIZCA SIRALAMA ort=+0,01205  std=0,08091  4/8
#
# Artefaktın std'si 0,081; kapının ayırt etmesi gereken gerçek sinyal
# +0,0283 (std 0,0230). Gürültü tabanı sinyalin **2,9 katı.**
#
# 🔴 DÜZELTİLDİ (K-064): permüte edilen DEĞERLER komşuların ORİJİNAL
# sırasına geri yazılıyor. Ölçüldü, düzeltmeden SONRA:
#
#     sira_kolu · TAM ablasyon      ort=+0,00000  std=0,00000  0/8
#     kapının üç sayısı             +0,02827 · +0,05931 · +0,08758  DEĞİŞMEDİ
#
# 🔴 VE BU YÜZDEN AŞAĞIDAKİ İKİ TEST VAR (Y11): kapının kendi kolu
# (`gurultuden_kacan`) kendi içinde `sorted` yapıyor, yani **sıra-KÖR**.
# Sıralama ekseni geri konsa kapının sayıları DEĞİŞMEZ ve kapı bunu
# **göremez.** Düzeltmeyi koruyan şey kapı değil, bu iki testtir.
# ==========================================================================


def _sirasiz_gozlem(dugumler=(7, 3, 9, 1)):
    """Komşuları KASITLI OLARAK sırasız bir gözlem — sentetik, koşusuz."""
    from sim.gozlem import Gozlem, KomsuKaydi

    return Gozlem(
        dugum=0, saat_s=100.0, olculen_gurultu_w=1e-12, kanal_mesgul_mu=False,
        kuyruk_uzunlugu=0, kuyruk_kapasitesi=64, son_iletim_sonucu=None,
        son_iletim_hedefi=None, gonderilen_bayt=0, alinan_bayt=0,
        komsular=tuple(
            KomsuKaydi(dugum=d, son_duyulma_s=99.0, duyulan_beacon=3,
                       bildirdigi_gurultu_w=1e-12 * (i + 1),
                       bildirdigi_kuyruk=i, bildirdigi_konum=None)
            for i, d in enumerate(dugumler)),
        paket=None)


def test_b84_ablasyon_KOMSU_SIRASINI_koruyor():
    """🔴 B-84 — ablasyonun TEK ekseni bilgi olmalı, sıra DEĞİL.

    Ucuz ve doğrudan: sarmalayıcıya kasıtla sırasız bir demet verilir ve
    çıkışın **aynı sırada** olduğu gösterilir. Bu test kırılırsa ablasyon
    yeniden iki eksen değiştiriyor demektir.

    ⚠️ Kapı bunu göremez — `gurultuden_kacan` sıra-kördür (B-84).
    """
    from sim.config import Konfig
    from dogrulama.aktaricilar import kalite_ablasyonu

    goruldu = {}

    def kaydeden(kon):
        def s(g):
            goruldu["sira"] = [k.dugum for k in g.komsular]
            goruldu["degerler"] = [k.bildirdigi_gurultu_w for k in g.komsular]
            return None
        return s

    g = _sirasiz_gozlem()
    giren = [k.dugum for k in g.komsular]
    assert giren != sorted(giren), "kurulum varsayımı: demet sırasız olmalı"

    kalite_ablasyonu(kaydeden)(Konfig(kol="t"))(g)

    assert goruldu["sira"] == giren, (
        f"🔴 ablasyon komşu SIRASINI değiştirdi: {giren} → {goruldu['sira']}. "
        f"Bu, `06`'nın *'tek fark BİLGİ'* cümlesini ölçümle yanlışlar ve "
        f"sıraya duyarlı bir kolda kapının gürültü tabanını 3,5 kat büyütür "
        f"(B-84).")

    # Y8 — ablasyon GERÇEKTEN bir şey yapmalı, yoksa test boştur
    asil = [k.bildirdigi_gurultu_w for k in g.komsular]
    assert goruldu["degerler"] != asil, (
        "ablasyon hiçbir değeri permüte etmemiş — null bilgi yok etmiyor")
    assert sorted(goruldu["degerler"]) == sorted(asil), (
        "ablasyon DAĞILIMI bozdu; yalnızca eşleştirmeyi yok etmeliydi")


def test_b84_SIRAYA_DUYARLI_kol_ablasyondan_ETKILENMIYOR():
    """🔴 Y11 — yapısal testin KAPSAMI DIŞINDA bir vaka.

    Yukarıdaki test sarmalayıcının sırayı koruduğunu gösterir. Bu test
    **davranıştan** sorar: kalite alanını hiç OKUMAYAN ama komşu sırasına
    duyarlı bir kol, kendi ablasyonundan **tam olarak sıfır** fark almalı.

    Düzeltmeden önce bu fark +0,01205 (std 0,08091, 4/8 pozitif) idi ve
    tamamı artefaktdı.

    ⚠️ Dört tam koşu (~30 sn). Ucuz değil ama kapının göremediği ekseni
    yalnızca bu ölçer.
    """
    from dogrulama.aktaricilar import kalite_ablasyonu

    def sira_kolu(kon):
        """SIFIR kalite bilgisi; yalnızca SIRAYA duyarlı."""
        def s(g):
            if g.paket is None or not g.komsular:
                return None
            for k in g.komsular:
                if k.dugum == g.paket.hedef:
                    return k.dugum
            return g.komsular[0].dugum
        return s

    abl = kalite_ablasyonu(sira_kolu)
    for t in (1, 2):
        kol = _kos(sira_kolu, tohum=t)["secim_avantaji_ortalama"]
        nul = _kos(abl, tohum=t)["secim_avantaji_ortalama"]
        assert kol == nul, (
            f"tohum {t}: kalite alanını HİÇ OKUMAYAN bir kol ablasyondan "
            f"{kol - nul:+.5f} fark aldı. Ablasyon bilgiden BAŞKA bir şeyi "
            f"de değiştiriyor (B-84).")


def test_b45_oran_yuklemi_MUTLAK_SAYIDAN_farkli_karar_verebiliyor():
    """🔴 Y10 — oran biçiminin KIRILABİLİR olduğu gösteriliyor.

    Bugünkü aktarıcı çiftinde mutlak sayı ve oran aynı kararı veriyor;
    ölçüldü (mutlak biçime dönen mutasyon `test_b30_..._DUYARLI`dan sağ
    çıkıyor). Bir iddianın doğru olduğunu göstermek, onun **yanlış
    olabileceği bir durumu** göstermeyi gerektirir.

    Aşağıdaki iki sentetik sonuç, gerçek bir tehlikeyi temsil ediyor: çok
    karar veren bir kol, ORANI düşük olduğu hâlde MUTLAK sayıda öne geçer.
    """
    az_karar = {"yonlendirme_karari": 7342, "olu_bag_karar": 2236}    # %30,5
    cok_karar = {"yonlendirme_karari": 72775, "olu_bag_karar": 3000}  # %4,1

    # mutlak sayı YANLIŞ sıralıyor
    assert cok_karar["olu_bag_karar"] > az_karar["olu_bag_karar"]

    # oran DOĞRU sıralıyor
    assert _oran(az_karar, "olu_bag_karar") > _oran(cok_karar, "olu_bag_karar")

    # ve sıfır kararda çökmüyor (Y7: "0 karar" ile "0 ölü bağ" ayrı şeyler)
    assert _oran({"yonlendirme_karari": 0, "olu_bag_karar": 0},
                 "olu_bag_karar") == 0.0


# ==========================================================================
# 🔴 B-48 · B-49 — ŞEMA ALANLARI GERÇEKTEN TAŞIYOR MU?
#
# İkisi de aynı sınıftan: alan sonuç satırında var, ama SABİTLENDİĞİNDE
# hiçbir test görmüyor. `03` B5: "bildirim ≠ kullanım".
# ==========================================================================

def test_b48_bant_KONFIGDEN_turuyor_varsayilandan_degil():
    """🔴 Bant alanı sabitlenebiliyordu; test yalnızca VARSAYILANI sınıyordu.

    Bu alan tam olarak *"K-020'nin sayısı bandı yazmadığı için yeniden
    üretilemedi"* diye eklendi. Varsayılan dışı bir bantla koşulduğunda
    satır hâlâ `[0.05, 0.9]` yazıyorsa, alan yalan söylüyor demektir.
    """
    ozel = (0.2, 0.7)
    s = Kosu(Konfig(kol="t", senaryo="S2", tohum=1,
                    ara_bolge_per_bandi=ozel), AKTARICILAR["en_kisa_yol"]).kostur()
    assert s["ara_bolge_per_bandi"] == list(ozel), (
        f"satır {s['ara_bolge_per_bandi']} yazıyor, konfig {list(ozel)}")

    # Y8 — bandın DEĞİŞTİRİLMESİ sayacı gerçekten etkilemeli, yoksa
    # alanın doğru olması bir şey ifade etmez
    varsayilan = _kos(AKTARICILAR["en_kisa_yol"])
    assert s["ara_bolge_karar"] != varsayilan["ara_bolge_karar"], (
        "bant değişti ama sayaç aynı — bant hiç kullanılmıyor olabilir")


def test_b49_protokol_teshis_slotu_gercekten_TASIYOR():
    """🔴 Slot açıldı ama taşıdığı hiç gösterilmedi.

    Mevcut test `== {}` diye bakıyordu; Aile 0'da doğru cevap zaten `{}`
    olduğu için test **boruyu değil boşluğu** sınıyordu. Slotu sabit `{}`
    yapan bir mutasyon 284/284 testten sağ çıkmıştı.

    🔴 21 AĞUSTOS 2026 — TESTİN KENDİ YOLU BİR SIZINTIYDI (B-68, K-056).
    ---------------------------------------------------------------------
    İlk yazımı slota yazabilmek için fabrikanın `__dict__`ine **`Kosu`
    nesnesini enjekte ediyordu** (`yazan_fabrika._kosu = k`). Dördüncü
    bağımsız denetim ölçtü: `sim/` + `dogrulama/` altında slota yazan tek
    satır yoktu, yani **meşru bir yol hiç yoktu** ve testin gösterdiği yol
    bir ŞABLON olsaydı Aile 1'in protokolleri `topo`, `karistirici` ve
    `bag_gercek_per` dâhil her şeye ulaşırdı — `03` kural 5'in tam hedefi.
    `test_c5_1b`in sızıntı taraması `Gozlem`den başladığı için o kanalı
    **göremezdi**.

    Artık meşru kanca var: `protokol.teshis(dugum) → dict | None`,
    `beacon_yuku` deseniyle birebir aynı — isteğe bağlı, protokolün KENDİ
    örneğine ait, simülatöre referans taşımıyor.
    """
    def yazan_fabrika(kon):
        ic = AKTARICILAR["en_kisa_yol"](kon)
        sayac = {"n": 0}

        def sonraki(g):
            sayac["n"] += 1
            return ic(g)

        # 🔴 MEŞRU YOL — `Kosu`ya hiçbir referans yok.
        sonraki.teshis = lambda dugum: {"karar_sayisi": sayac["n"]}
        return sonraki

    s = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), yazan_fabrika).kostur()

    assert "karar_sayisi" in s["protokol_teshis"], (
        "slota yazılan teşhis sonuç satırına ULAŞMIYOR — boru kopuk")
    kayitlar = s["protokol_teshis"]["karar_sayisi"]
    assert isinstance(kayitlar, dict) and len(kayitlar) > 1, (
        f"teşhis düğüm bazında taşınmıyor: {kayitlar!r}")
    assert sum(kayitlar.values()) > 1000, (
        f"toplam {sum(kayitlar.values())} karar — Y8: yol yeterince "
        f"tetiklenmemiş")

    # Kontrol kolu: yazmayan protokolde slot BOŞ kalmalı
    bos = _kos(AKTARICILAR["en_kisa_yol"])
    assert bos["protokol_teshis"] == {}


# ==========================================================================
# 🔴 B-65 (K-056) — H1.1'İN MEKANİZMA KAPISI, ÜÇÜNCÜ VE SON HÂLİ
#
# İki kez yanlış şey ölçüldü:
#   B-45 · `ara_bolge_karar` oranı  → YOL GEOMETRİSİ
#   B-65 · `secim_avantaji` mutlak eşiği → SEÇİMİN KALICILIĞI
#
# Üçüncü hâl her ikisini de **yapısal olarak** ortadan kaldırıyor: kol,
# KENDİ ablasyonuna karşı **eşleştirilmiş** okunuyor. İki kolun yapısı,
# kalıcılığı ve topolojisi birebir aynı; tek fark BİLGİ.
#
# 🔒 Mutlak eşik YOKTUR ve olamaz — `03` kural 2.
# ==========================================================================

# 🔴 A-12 (ALTINCI DENETİM) — İKİNCİ DOĞRU KAYNAĞI KALDIRILDI.
#
# Bu iki sabit burada ELLE İKİNCİ KEZ yazılıydı; aslı
# `dogrulama/mekanizma_kapisi.py`de. Denetçi ölçtü: hiçbir test ikisini
# birbirine bağlamıyordu. `KAPI_TOHUMLARI` 8'den 10'a çıkarılsa serbestlik
# derecesi 9 olur (t = 2,262) ve **bir kopya güncellenip diğeri unutulurdu.**
# B-07'nin "ikinci doğru kaynağı" dersi ve Y12, tam olarak bunu yasaklıyor.
#
# Artık kapının kendi sabitleri içe aktarılıyor: tek kaynak.
from dogrulama.mekanizma_kapisi import (  # noqa: E402
    EN_AZ_POZITIF, KAPI_TOHUMLARI, NULL_CEKIM_SAYISI, _T_975_7,
)


def test_b65_mekanizma_kapisi_ESLESTIRILMIS_ablasyona_karsi():
    """🔴 H1.1'İN KAPISI. Kol, kendi ablasyonundan anlamlı olarak iyi mi?

    ÖLÇÜM: her tohumda `gurultuden_kacan` ve onun **kalite ablasyonu**
    (aynı protokol, komşuların bildirdiği gürültü aralarında permüte —
    permütasyon düğüm başına SABİT, yani kalıcılık korunuyor).

    KAPI — `06` ÜÇ koşul sayar; bu test bunlardan İKİSİNİ uygular:
      1. Eşleştirilmiş fark ≥ 7/8 tohumda pozitif (işaret testi p ≤ 0,035)
      2. Farkın %95 güven aralığı sıfırı dışlıyor

    🔒 Üçüncü koşul (`ara_bolge_karar`/`olu_bag_karar` ORAN cinsinden
    raporlanır, mutlak sayı kullanılmaz) bir RAPORLAMA şartıdır ve
    `test_b45_oran_yuklemi_MUTLAK_SAYIDAN_farkli_karar_verebiliyor`
    tarafından zorlanır — orada oran yükleminin KIRILABİLİR olduğu da
    gösterilir (Y10).

    ⚠️ B-92 (beşinci denetim): bu docstring eskiden *"iki koşul birden"*
    diyordu ve `06` *"bu ÜÇÜ"* diyordu. Sayı uyuşmazlığı düzeltildi; hiçbir
    koşul kaldırılmadı.

    ⚠️ Bu test 16 tam koşu yapar (~2 dk). Ucuz değildir ve olamaz: B-65 tam
    olarak *tek koşuya* güvenmekten doğdu.
    """
    import statistics

    fab = AKTARICILAR["gurultuden_kacan"]
    abl = kalite_ablasyonu(fab)
    farklar = []
    for t in KAPI_TOHUMLARI:
        kol = _kos(fab, tohum=t)["secim_avantaji_ortalama"]
        nul = _kos(abl, tohum=t)["secim_avantaji_ortalama"]
        farklar.append(kol - nul)

    pozitif = sum(1 for x in farklar if x > 0)
    assert pozitif >= 7, (
        f"eşleştirilmiş fark yalnızca {pozitif}/8 tohumda pozitif: "
        f"{[f'{x:+.4f}' for x in farklar]}. Bilgi ölçülemiyor.")

    ort = statistics.mean(farklar)
    sh = statistics.stdev(farklar) / len(farklar) ** 0.5
    alt = ort - _T_975_7 * sh
    assert alt > 0, (
        f"farkın %95 GA'sı sıfırı içeriyor: ort={ort:+.5f} "
        f"alt={alt:+.5f}. Kapı GEÇMEZ.")


def test_b65_MUTLAK_ESIK_KULLANILAMAZ_kalicilik_avantaj_satin_aliyor():
    """🔴 Neden mutlak eşiğe DÖNÜLEMEZ — ölçümle sabitlenmiş.

    Bu test bir düzeltme değil, bir **çit**: biri *"ablasyon zaten sıfır,
    doğrudan eşik koyalım"* derse burada durur.

    Bilgi taşımayan ama KALICI bir kol, tanım gereği sıfır avantaj ALMAZ:
    kalıcılık tek başına ~+0,06 satın alır. Karar başına karıştıran bir null
    ise ~0 verir (−0,0006) ve **yanıltıcıdır**.
    """
    import statistics

    abl = kalite_ablasyonu(AKTARICILAR["gurultuden_kacan"])
    v = [_kos(abl, tohum=t)["secim_avantaji_ortalama"] for t in KAPI_TOHUMLARI]
    ort = statistics.mean(v)
    assert ort > 0.02, (
        f"kalıcı ablasyon null'u {ort:+.5f} — 0,02 eşiğinin altında. "
        f"Kurulum değişmiş olabilir; B-65'in ölçümü +0,0599 idi. Eğer bu "
        f"gerçekten sıfıra indiyse kapı yeniden tasarlanmalı, ama mutlak "
        f"eşiğe DÖNÜLMEMELİ: sebep ölçülmeden değiştirilemez (Y9).")


def test_b65_ablasyon_BELIRLENIMCI_ve_bilgiyi_yok_ediyor():
    """Ablasyonun kendisi Y7: ne yaptığını doğrular.

    (a) Aynı tohumda iki koşu **birebir** aynı sonuç verir — Ç2 korunur.
    (b) Ablasyon gerçekten bir şey DEĞİŞTİRİR; kolun kararlarını aynen
        bırakmıyor.
    """
    fab = AKTARICILAR["gurultuden_kacan"]
    abl = kalite_ablasyonu(fab)

    a = _kos(abl, tohum=3)
    b = _kos(abl, tohum=3)
    assert a == b, "ablasyon belirlenimci değil — Ç2 kırılır"

    duz = _kos(fab, tohum=3)
    assert a["secim_avantaji_ortalama"] != duz["secim_avantaji_ortalama"], (
        "ablasyon hiçbir şeyi değiştirmiyor — permütasyon uygulanmamış olabilir")


def test_b68_teshis_kancasi_KOSUYA_referans_gerektirmiyor():
    """🔴 Kancanın kendisi bir sızıntı kapısı olmamalı.

    Kaynak denetimi: `sim/` altında `protokol_teshis`e yazan tek yer
    `_protokol_teshislerini_topla`dır ve o da yalnızca protokolün KENDİ
    kancasını çağırır. Testler `Kosu` nesnesini fabrikaya enjekte edemez.
    """
    # ⚠️ DİZGİ ARAMASI YETMEZ: ilk yazımı `"_kosu = k" not in kaynak`
    # diyordu ve KENDİ DOCSTRING'İMDEKİ örneği yakalayıp kırıldı. Bir
    # kaynak denetimi, prozayı koddan ayırt edemiyorsa ölçüt değildir —
    # bu yüzden AST üzerinden, gerçek ATAMA aranıyor.
    import ast as _ast

    agac = _ast.parse((Path(__file__).resolve().parent /
                       "test_mekanizma_kapisi.py").read_text(encoding="utf-8"))
    enjeksiyon = [d for d in _ast.walk(agac)
                  if isinstance(d, _ast.Assign)
                  for h in d.targets
                  if isinstance(h, _ast.Attribute) and h.attr.startswith("_kosu")]
    assert not enjeksiyon, (
        f"{len(enjeksiyon)} yerde fabrikaya `Kosu` benzeri bir nesne "
        f"enjekte ediliyor — B-68'in şablon riski geri gelmiş")

    kos_kaynak = (Path(__file__).resolve().parent.parent / "sim" / "kosucu.py"
                  ).read_text(encoding="utf-8")
    yazan = [x for x in kos_kaynak.splitlines()
             if "protokol_teshis" in x and "setdefault" in x]
    assert len(yazan) == 1, (
        f"slota yazan {len(yazan)} yer var; tek meşru yol beklenirdi")


# ==========================================================================
# 🔴 B-115 (ALTINCI DENETİM) — ÖN-KAYITLI KAPININ İKİ MÜHÜRLÜ PARAMETRESİNİ
#    HİÇBİR TEST KORUMUYORDU
#
# Ölçüldü (denetçi): `NULL_CEKIM_SAYISI` ve `tuz` `tests/` altında **hiç
# geçmiyordu**. `test_b65_*` bilerek m = 1 kullanıyor (maliyet), yani kapının
# fiilen kullandığı m = 5 yolu test edilmemişti. Etkisi ölçüldü:
#
#     m = 5 -> m = 1 : kapının nokta kestirimi 0,03372 -> 0,02506  (−%26)
#     tuz yok sayılırsa : 5 çekim BİREBİR aynı olur (bugün 5/5 ayrık)
#
# 🔴 Y12, bu sabitler mühürlenmeden **BİR GÜN ÖNCE** kalıcı kural olmuştu
# (K-060, 25 Ağustos) ve onlara uygulanmamıştı.
#
# ⚠️ Bu testler UCUZDUR: hiçbiri tam koşu yapmaz. Kapının kendi ölçütü
# pahalıdır ve pahalı bir koruma pratikte SUSAR — Y12'nin tam gerekçesi.
# ==========================================================================

def test_b115_m_MUHURLU_ve_06_ILE_AYNI_satirdan_okunuyor():
    """🔴 Y12 — mühürlü `m`, `06`nın beyanıyla AYNI olmak zorunda.

    `06` mührü *"m = 5"* diyor ve *"SONRADAN BÜYÜTÜLEMEZ"* (kural 3: eşiği
    geriye dönük gevşetmeme). Kodda sessizce değiştirilirse ön-kayıt ile
    araç ayrışır ve **hiçbir şey konuşmaz** — B-115 tam olarak buydu.
    """
    import re

    kok = Path(__file__).resolve().parent.parent
    on_kayit = (kok / "v2" / "06-ON-KAYIT.md").read_text(encoding="utf-8")

    beyan = re.search(r"NULL ÇEKİM SAYISI\s*—\s*m\s*=\s*(\d+)", on_kayit)
    assert beyan is not None, (
        "🔴 `06`da mühürlü `m` beyanı bulunamadı — mühür kaybolmuş olabilir")
    assert int(beyan.group(1)) == NULL_CEKIM_SAYISI, (
        f"🔴 `06` m = {beyan.group(1)} diyor, kod m = {NULL_CEKIM_SAYISI} "
        f"kullanıyor. Ön-kayıt ile araç AYRIŞMIŞ (B-115 · `03` kural 3).")

    assert on_kayit.count("SONRADAN BÜYÜTÜLEMEZ") >= 1, (
        "🔴 `06`nın *m büyütülemez* mührü metinden kaybolmuş")


def test_b115_serbestlik_derecesi_TOHUM_SAYISINDAN_turetiliyor():
    """🔴 A-12 — `_T_975_7` elle yazılmış bir sabit; tohum sayısına BAĞLI.

    `KAPI_TOHUMLARI` 8'den 10'a çıkarılsa serbestlik derecesi 9 olur
    (t = 2,262) ve sabit sessizce yanlışlaşır. Bugüne kadar hiçbir test
    ikisini bağlamıyordu — üstelik sabit İKİ dosyada duruyordu.

    ⚠️ Tablo yalnızca bugünkü tasarım noktasını taşıyor; başka bir n
    seçilirse değeri **ölçülüp** buraya yazılmak zorundadır (`scipy` bu
    depoda kasten YOKTUR — `08` madde 21).
    Üretici: `python -c "from scipy.stats import t; print(t.ppf(0.975, 7))"`
    """
    T_TABLOSU = {7: 2.365, 9: 2.262, 14: 2.145, 29: 2.045}

    sd = len(KAPI_TOHUMLARI) - 1
    assert sd in T_TABLOSU, (
        f"🔴 `KAPI_TOHUMLARI` {len(KAPI_TOHUMLARI)} tohuma çıkmış "
        f"(serbestlik derecesi {sd}) ama `_T_975_7` için tablo değeri YOK. "
        f"Sabit ölçülüp güncellenmeli — yoksa GA yanlış hesaplanır (A-12).")
    assert abs(_T_975_7 - T_TABLOSU[sd]) < 5e-4, (
        f"🔴 t sabiti serbestlik derecesiyle uyuşmuyor: sd={sd} için "
        f"{T_TABLOSU[sd]} gerekiyor, yazılı olan {_T_975_7} (A-12).")

    assert EN_AZ_POZITIF <= len(KAPI_TOHUMLARI), (
        "işaret testi eşiği tohum sayısından büyük — kapı hiç geçemez")


def _sahte_gozlem(dugum: int, komsu_sayisi: int) -> Gozlem:
    """Tam koşu YAPMADAN ablasyonu sınamak için asgari gözlem."""
    komsular = tuple(
        KomsuKaydi(dugum=100 + i, son_duyulma_s=1.0, duyulan_beacon=1,
                   bildirdigi_gurultu_w=float(i + 1) * 1e-12,
                   bildirdigi_kuyruk=i, bildirdigi_konum=None,
                   bildirdigi_yuk=None)
        for i in range(komsu_sayisi))
    return Gozlem(dugum=dugum, saat_s=1.0, olculen_gurultu_w=1e-12,
                  kanal_mesgul_mu=False, kuyruk_uzunlugu=0,
                  kuyruk_kapasitesi=10, son_iletim_sonucu=None,
                  son_iletim_hedefi=None, gonderilen_bayt=0, alinan_bayt=0,
                  komsular=komsular)


def _ablasyon_permutasyonu(tuz: int, komsu_sayisi: int = 6) -> tuple:
    """`tuz` ile kurulan ablasyonun ürettiği DEĞER SIRASI — ucuz.

    🔴 Formül YENİDEN YAZILMIYOR: aracın kendi `kalite_ablasyonu`su
    çağrılıyor ve gördüğü değerler bir sahte protokolle kaydediliyor.
    """
    gorulen = {}

    def fabrika(kon):
        def prot(g):
            gorulen["degerler"] = tuple(
                k.bildirdigi_gurultu_w for k in g.komsular)
            return None
        return prot

    abl = kalite_ablasyonu(fabrika, tuz=tuz)
    abl(Konfig(kol="t", senaryo="S2", tohum=1))(
        _sahte_gozlem(7, komsu_sayisi))
    return gorulen["degerler"]


def test_b115_tuz_BES_AYRIK_CEKIM_uretiyor():
    """🔴 `tuz` olmadan m = 5, m = 1'e SESSİZCE döner.

    Ablasyon permütasyonu `hash(anahtar) ^ tuz` ile tohumlanıyor. `tuz`
    yok sayılırsa beş "bağımsız" çekim **birebir aynı** olur: kapı beş kez
    aynı null'u ortalar, varyans azalması sıfırdır ve `06`nın m = 5
    gerekçesi kâğıtta kalır. Hiçbir test bunu görmüyordu (B-115).

    ⚠️ Kapsam: burada ölçülen şey **ayrıklık**, bağımsızlık değil.
    Bağımsızlık 200 000 anahtarla ayrıca ölçüldü (altıncı denetim, A-5):
    çift-eşitlik oranı 1/k! referansıyla ayırt edilemez.
    """
    cekimler = [_ablasyon_permutasyonu(s) for s in range(NULL_CEKIM_SAYISI)]

    # 🔴 Y8 — ablasyon gerçekten bir şey yapıyor mu (boş küme tuzağı)
    duz = tuple(sorted(cekimler[0]))
    assert any(tuple(c) != duz for c in cekimler) or len(set(cekimler)) > 1, (
        "ablasyon hiçbir permütasyon üretmiyor — ölçüt bozuk (Y7)")

    assert len(set(cekimler)) == NULL_CEKIM_SAYISI, (
        f"🔴 `tuz` {NULL_CEKIM_SAYISI} AYRIK çekim üretmiyor: "
        f"{len(set(cekimler))} ayrık. m = {NULL_CEKIM_SAYISI} sessizce "
        f"m = 1'e dönmüş olabilir (B-115).")


def test_b115_tuz_SIFIR_eski_davranisin_BIREBIR_aynisi():
    """🔒 `tuz=0` ön-kayıtlı kapının ESKİ sayılarını değiştirmemeli.

    K-064 bunu ilan etti (`x ^ 0 == x`) ve kapının üç sayısının değişmediğini
    ölçtü — ama **hiçbir test bunu bağlamıyordu.** `tuz` varsayılanı bir gün
    1 yapılsa, ön-kayıtlı kapının tüm geçmiş sayıları sessizce geçersizleşirdi.
    """
    assert _ablasyon_permutasyonu(0) == _ablasyon_permutasyonu(tuz=0), (
        "ablasyon belirlenimci değil — Ç2 kırılmış olurdu")

    import inspect
    imza = inspect.signature(kalite_ablasyonu)
    assert imza.parameters["tuz"].default == 0, (
        "🔴 `kalite_ablasyonu`nun `tuz` varsayılanı 0 DEĞİL — ön-kayıtlı "
        "kapının geçmiş sayıları geçersizleşir (K-064 · B-115).")
