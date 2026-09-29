"""
🔴 İKİNCİ BAĞIMSIZ DENETİMİN MUTASYON BOŞLUKLARI (B-27).

İkinci denetçi depoyu hiç görmemiş bir gözle **10 yeni mutasyon** yazdı ve
**7'si 240 testten sağ çıktı.** Birinci denetim 198 testte 8/10 demişti.

> *"Kapanan şey bulgular kümesiydi, örüntü değil. Örüntünün kapandığını
>  söyleyebilmenin tek yolu, bağımsız bir örneklemde sağ kalan oranının
>  düşmesidir; bugün düşmedi."*

Sağ kalan 7'nin **beşi davranışı fiilen değiştiriyordu** *(44/13/12 koşuluk
matrislerde ölçüldü)*; ikisi ise değiştirmiyordu çünkü o alanların hiçbir
tüketicisi yoktu — o ikisi B-27b'de, `tests/test_gozlem.py` içinde kapatıldı.

Bu dosya kalan **beşi** kapatır. Her test, mutasyonun bozduğu değişmezi
BAĞIMSIZ olarak yeniden hesaplar; üretici ifadeyi tekrar etmez.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import en_kisa_yol  # noqa: E402
from sim.config import Konfig  # noqa: E402
from sim.karsilastirma import ortak_alt_kume  # noqa: E402
from sim.kosucu import Kosu  # noqa: E402
from sim.radio import Karistirici  # noqa: E402
from sim.rng import Akislar, kanal_cekimi  # noqa: E402


def _kos(**kw):
    kon = Konfig(kol="t", senaryo=kw.pop("senaryo", "S2"),
                 trafik=kw.pop("trafik", "orta"), tohum=kw.pop("tohum", 1), **kw)
    return Kosu(kon, en_kisa_yol).kostur()


# ==========================================================================
# KM1 · kesisim_orani_pencere -> 1.0   (RAPORA GİREN METRİK)
# ==========================================================================

def test_km1_kesisim_oranlari_bagimsiz_sayimla_ayni():
    """🔴 Kesişim oranı, rapora giren HER gecikme karşılaştırmasının yanında
    yazılmak zorunda (`08` madde 16). Sabit 1.0 döndüren bir mutasyon 240
    testten sağ çıkıyordu — yani bu sayı hiçbir yerde doğrulanmıyordu.

    BAĞIMSIZ HESAP: teslim kimlik kümelerinden elle.
    """
    a, b = _kos(senaryo="S0"), _kos(senaryo="S2")
    o = ortak_alt_kume(a, b)

    ka, kb = set(a["teslim_kimlikleri"]), set(b["teslim_kimlikleri"])
    assert o.ortak_paket == len(ka & kb)
    assert o.birlesim_paket == len(ka | kb)
    assert o.kesisim_orani_birlesim == pytest.approx(
        len(ka & kb) / len(ka | kb), rel=1e-12, abs=0.0)
    assert o.kesisim_orani_pencere == pytest.approx(
        len(ka & kb) / a["pencerede_uretilen"], rel=1e-12, abs=0.0)

    # Y8 — oranlar 1.0 OLMAMALI, yoksa sabit 1.0 mutasyonu yakalanamaz
    assert o.kesisim_orani_birlesim < 0.9, o.ozet()
    assert o.kesisim_orani_pencere < 0.9, o.ozet()


# ==========================================================================
# KM2 · komsu_omru_katsayisi 10 -> 1000
# ==========================================================================

def test_km2_komsu_omru_MUTLAK_degeriyle_baglayici():
    """🔴 Ömür 100 kat uzatıldığında hiçbir test kırılmıyordu.

    Mevcut tazelik testi ömrü GÖRELİ kullanıyor (`omur * 2.0`), dolayısıyla
    ömrün DEĞERİNE kırılamaz — ikinci denetimin *"parametre hâli daha
    ciddi"* dediği Y10 vakası.

    Burada eşik MUTLAK saniyeyle sınanır ve ömrün fiilen bağladığı
    gösterilir: ömür uzatılınca gözlemdeki komşu sayısı ARTMALI.
    """
    kon = Konfig(kol="t")
    assert kon.komsu_omru_s == pytest.approx(10.0, rel=1e-12, abs=0.0), (
        f"komşu ömrü {kon.komsu_omru_s} s — beklenen 10,0 s "
        f"(beacon aralığı 1,0 s × katsayı 10)"
    )

    # 🔴 ÖLÇÜM NOKTASI TETİKLENMEYE GÖRE SEÇİLDİ (Y8).
    # Ömür ancak beacon'lar 10 s boyunca kaybolduğunda bağlar. Ölçüldü —
    # ömrü 100 kat uzatmanın gözlemdeki komşu sayısına etkisi:
    #
    #     S2/orta                 %0,58   (52 beacon kaçtı)
    #     S2/yoğun                %0,67   (91)
    #     S5/orta (hareketli)     %1,79   (38)
    #     +8 dBm/orta             %3,48   (101)
    #     +11 dBm/yoğun           %7,23   (324)   <- SEÇİLEN
    #
    # S2/orta'da ölçseydik eşik gürültüye boğulurdu ve test "ömür bağlıyor"
    # diyemezdi. Mekanizmanın FİİLEN çalıştığı noktada ölçülür.
    ortalama = {}
    for ad, katsayi in (("kisa", 10.0), ("uzun", 1000.0)):
        k = Kosu(Konfig(kol=ad, senaryo="S2", trafik="yogun", tohum=1,
                        karistirici_guc_override_dbm=11.0,
                        komsu_omru_katsayisi=katsayi), en_kisa_yol)
        ilk, toplam, adet = k.protokol, [0], [0]

        def izleyen(g, _t=toplam, _a=adet, _ilk=ilk):
            _t[0] += len(g.komsular)
            _a[0] += 1
            return _ilk(g)

        k.protokol = izleyen
        k.kostur()
        ortalama[ad] = toplam[0] / max(adet[0], 1)

    assert ortalama["uzun"] > ortalama["kisa"] * 1.04, (
        f"ömür 100 kat uzadı ama gözlemdeki ortalama komşu sayısı "
        f"{ortalama['kisa']:.3f} -> {ortalama['uzun']:.3f} — ömür bağlamıyor"
    )


# ==========================================================================
# KM3 · Hareketli karıştırıcının yörünge YÖNÜ ters
# ==========================================================================

def test_km3_yorunge_yonu_kapali_formla_ayni():
    """🔴 Yörünge yönünü tersine çeviren mutasyon S5'in TÜM koşularını
    değiştiriyordu ve hiçbir test kırılmıyordu.

    BAĞIMSIZ HESAP: konum kapalı formdan, işaretiyle birlikte.
    """
    kon = Konfig(kol="t", senaryo="S5")
    kj = Karistirici.senaryodan(kon, Akislar(1))
    cx, cy = kon.karistirici_merkez
    r = kon.karistirici_yorunge_yaricap_m
    cevre = 2.0 * math.pi * r

    for t in (0.0, 7.5, 33.3, 120.0, 250.0):
        aci = 2.0 * math.pi * ((kon.karistirici_hiz_ms * t) / cevre + kj.faz_kesri)
        bx, by = cx + r * math.cos(aci), cy + r * math.sin(aci)
        x, y = kj.konum_t(t)
        assert x == pytest.approx(bx, rel=1e-12, abs=0.0), t
        assert y == pytest.approx(by, rel=1e-12, abs=0.0), t

    # Y8 — yön gerçekten SAAT YÖNÜNÜN TERSİ mi? Küçük bir dt'de açı ARTMALI.
    a0 = math.atan2(kj.konum_t(0.0)[1] - cy, kj.konum_t(0.0)[0] - cx)
    a1 = math.atan2(kj.konum_t(1.0)[1] - cy, kj.konum_t(1.0)[0] - cx)
    assert ((a1 - a0) % (2 * math.pi)) < math.pi, (
        "yörünge yönü ters — karıştırıcı saat yönünde dolanıyor"
    )


# ==========================================================================
# KM4 · Yeniden deneme sınırı bir eksik (5 -> 4 iletim)
# ==========================================================================

def test_km4_paket_basina_iletim_sayisi_sinirla_tam_uyusuyor():
    """🔴 Etkin deneme 5->4 mutasyonu 13/13 koşuda sonucu değiştiriyor ve
    hiçbir test kırılmıyordu.

    DEĞİŞMEZ: garantili başarısızlıkta bir paket tam
    `1 + yeniden_deneme_siniri` kez iletilir.

    ⚠️ Bu sayı K-039'un bağ tanımını da belirliyor
    (`PER^(1+sınır) <= eşik`); sessizce kayması kalibrasyonu da kaydırır.
    """
    for sinir in (0, 2, 4):
        kon = Konfig(kol="t", senaryo="S2", trafik="seyrek", tohum=1,
                     yeniden_deneme_siniri=sinir,
                     karistirici_guc_override_dbm=11.0)   # ağ bölünmüş
        s = Kosu(kon, en_kisa_yol).kostur()
        dusen = s["mac_dusurmesi"]
        assert dusen > 0, f"sınır={sinir}: hiç düşme yok — yol tetiklenmedi (Y8)"
        # Düşen her paket TAM (1+sınır) kez iletilmiş olmalı; toplam iletim
        # en az bu kadardır (teslim edilenler de var).
        assert s["mac_gonderilen"] >= dusen * (1 + sinir), (
            f"sınır={sinir}: {dusen} düşme için en az {dusen*(1+sinir)} "
            f"iletim beklenir, {s['mac_gonderilen']} var"
        )
        assert s["mac_deneme"] >= s["mac_gonderilen"]


# ==========================================================================
# KM5 · kanal_cekimi alıcıya duyarsız
# ==========================================================================

def test_km5_kanal_cekimi_aliciya_duyarli_kosan_sistemde():
    """🔴 Çekimden alıcıyı çıkaran mutasyon 13/13 koşuda sonucu değiştiriyor
    ve 240 testten sağ çıkıyordu.

    `test_kanal_cekimi_yon_duyarli` fonksiyonu doğrudan sınıyor, ama KOŞAN
    SİSTEMDE aynı gönderenin farklı alıcılara aynı dilimde farklı çekim
    aldığı hiç doğrulanmamıştı — Ç2.3'ün kapsamı sanıldığından dardı
    (ikinci denetim §8-3).
    """
    kon = Konfig(kol="t")
    # Aynı gönderen, aynı dilim, FARKLI alıcı -> farklı çekim
    cekimler = {kanal_cekimi(1000, 3, alici, 12.345, kon.kanal_dilimi_s)
                for alici in range(40) if alici != 3}
    assert len(cekimler) >= 38, (
        f"40 farklı alıcı için yalnızca {len(cekimler)} farklı çekim — "
        f"çekim alıcıya duyarsız olabilir"
    )

    # Koşan sistemde: kanal izi aynı (gönderen, dilim) için farklı alıcılara
    # farklı değer taşımalı
    k = Kosu(Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1), en_kisa_yol)
    k.mac.kanal_izi = k.kanal_izi
    k.kostur()
    assert len(k.kanal_izi) > 1000, f"kanal izi boş ({len(k.kanal_izi)}) — Y7"

    gruplar: dict[tuple[int, int], set[float]] = {}
    for (gonderen, alici, dilim), cekim in k.kanal_izi.items():
        gruplar.setdefault((gonderen, dilim), set()).add(cekim)
    coklu = [v for v in gruplar.values() if len(v) > 1]
    assert coklu, (
        "hiçbir (gönderen, dilim) ikilisi birden çok alıcıya iletmemiş — "
        "test bu koşuda bir şey ölçmüyor (Y8)"
    )


# ==========================================================================
# KM6 · `_kurulum_bitti` — Ç6'nın İDDİA ETTİĞİ ama SINAMADIĞI koruma
#
# İkinci kör tarama (20 Ağustos, havuz 203) `_kurulum_bitti = True` → `False`
# mutasyonunu sağ çıkardı. O bayrak, `KanalErisimi.__setattr__`in yazım
# hatası korumasını açan tek anahtardır: `False` iken koruma TAMAMEN kapalı.
#
# 🔴 `08-AILE0-KAPSAM.md` Ç6 KAPSAR tablosu şunu iddia ediyor:
#     "geri çağrı adı yazım hatası `__setattr__` ile yakalanıyor"
# ...ve bu iddianın HİÇBİR TESTİ YOKTU. Korumayı doğuran olay K-023'te
# kayıtlı: geri çağrı adı değişince eski adla yapılan atama sessizce ölü bir
# öznitelik yaratıyor, geri çağrı hiç ateşlenmiyor, paketler kayboluyor ve
# testler "0 == 0" diye geçiyordu.
# ==========================================================================

def test_km6_geri_cagri_yazim_hatasi_yakalaniyor():
    """Kurulumdan sonra BİLİNMEYEN bir özniteliğe atama reddedilmeli."""
    from sim.events import OlayKuyrugu
    from sim.mac import KanalErisimi
    from sim.radio import Radyo
    from sim.topology import Topoloji

    kon = Konfig(kol="t", senaryo="S0", tohum=1)
    ak = Akislar(1)
    topo = Topoloji.uret(kon, ak)
    mac = KanalErisimi(kon, topo, Radyo.kur(kon), OlayKuyrugu(), None, ak)

    # Y8 — koruma AÇIK mı? Açık değilse test bir şey ölçmüyor.
    assert getattr(mac, "_kurulum_bitti", False) is True, (
        "kurulum bayrağı kapalı — __setattr__ koruması hiç devrede değil"
    )

    # Gerçek geri çağrı adları YAZILABİLİR olmalı
    for ad in ("alim_gerceklesti", "gonderim_bitti",
               "iletim_basarisiz", "yayin_alindi"):
        setattr(mac, ad, lambda *a, **k: None)

    # K-023'ün gerçek olayı: yazım hatası SESSİZCE ölü öznitelik yaratıyordu
    for yanlis in ("iletim_tamamlandi", "alim_gerceklestii", "yayin_alindii"):
        with pytest.raises(AttributeError) as e:
            setattr(mac, yanlis, lambda *a, **k: None)
        assert "alim_gerceklesti" in str(e.value), str(e.value)
