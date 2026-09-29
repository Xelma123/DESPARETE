"""
AİLE 0 ÇIKIŞ KAPILARI — Ç1, Ç2, Ç3.

Bu dosya, Aile 0'ın bir sonraki aşamaya geçmeye hazır olup olmadığını
belirleyen kriterleri koda bağlar. Buradaki her test bir çıkış kriteridir;
kırılırsa Aile 0 kapanmaz.

⚠️ Ç1.1'in TAM hâli (540 koşu) `dogrulama/kapi_korunum.py`de. Burada onun
hızlı bir alt kümesi var — testler her çalıştırmada koşacak kadar hafif
olmalı, yoksa koşulmaz olurlar.
"""

from __future__ import annotations

import math
import os
import statistics as ist
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

from dogrulama.aktaricilar import en_kisa_yol, hedefe_en_yakin  # noqa: E402
from sim.config import SENARYOLAR, Konfig  # noqa: E402
from sim.events import OlayKuyrugu  # noqa: E402
from sim.kosucu import Kosu  # noqa: E402
from sim.mac import Iletim, KanalErisimi  # noqa: E402
from sim.radio import Karistirici, Radyo, w_to_dbm  # noqa: E402
from sim.rng import Akislar  # noqa: E402
from sim.topology import Topoloji  # noqa: E402


# ==========================================================================
# Ç1 — KORUNUM, GERÇEK MAC YOLUNDAN
# ==========================================================================

@pytest.mark.parametrize("senaryo", SENARYOLAR)
def test_c1_1_korunum_her_senaryoda(senaryo):
    """Ç1.1 — korunum denklemi her senaryoda tutar."""
    k = Kosu(Konfig(kol="kapi", senaryo=senaryo, tohum=1), en_kisa_yol)
    k.kostur()
    assert k.defter.kontrol()["korunum_tamam"] is True, k.defter.kontrol()


def test_c1_1_korunum_uc_durumlarda():
    """Ç1.1 — uç yapılandırmalarda da tutar."""
    uc = [
        dict(kuyruk_kapasitesi=1, trafik="yogun", cbr_araligi_s=0.05),
        dict(ttl_baslangic=2),
        dict(yeniden_deneme_siniri=0),
        dict(karistirici_guc_override_dbm=11.0),   # ağ bölünmüş
    ]
    for ek in uc:
        k = Kosu(Konfig(kol="kapi", senaryo="S2", tohum=1, **ek), en_kisa_yol)
        k.kostur()
        assert k.defter.kontrol()["korunum_tamam"] is True, (ek, k.defter.kontrol())


def test_c1_3_mutasyon_hangi_kontrol_yakaliyor():
    """🔴 Ç1.3 — MUTASYON KONTROLÜ.

    ⭐ BU TEST BİR ŞEY ÖĞRETTİ VE ONU BURAYA YAZIYORUM:

    Korunum denklemi TEK BAŞINA yeterli bir dedektör DEĞİL. Bir `dus()`
    çağrısı silindiğinde paket "uçuşta" sayacında asılı kalır ve

        üretilen = teslim + düşen + kuyrukta + uçuşta

    eşitliği HÂLÂ TUTAR. Denklem yalnızca eşleşmeyen artır/azalt çiftlerini
    görür; kayıp bir geçişi görmez.

    Üç dedektör birlikte çalışır:
      1. denklem        → doğrudan sayaç oynaması
      2. negatif koruma → yanlış havuzdan düşürme (anında patlar)
      3. BOŞALTMA (Ç1.4) → kayıp geçiş / askıda kalan paket

    Bu test üçünü de ayrı ayrı tetikler. Herhangi biri yakalamazsa Aile 0
    kapanmaz.
    """
    from sim.ledger import KorunumHatasi

    # --- Önce sağlam koşu: bozulacak yol GERÇEKTEN çalışıyor mu? ----------
    saglam = Kosu(Konfig(kol="kapi", senaryo="S2", tohum=1), en_kisa_yol)
    saglam.kostur()
    assert saglam.mac_dusurmesi > 0, "iletim_basarisiz yolu hiç tetiklenmedi"
    assert saglam.defter.kontrol()["korunum_tamam"] is True
    saglam_boru = (saglam.defter.kuyrukta + saglam.defter.ucusta) / saglam.defter.uretilen
    assert saglam_boru < 0.01

    # --- MUTASYON 1: dus() silindi -> BOŞALTMA yakalamalı ----------------
    m1 = Kosu(Konfig(kol="kapi", senaryo="S2", tohum=1), en_kisa_yol)

    def dussuz(paket, gonderen, hedef):
        m1.mac_dusurmesi += 1          # `dus()` YOK
        m1._uyandir(gonderen)

    m1.mac.iletim_basarisiz = dussuz
    m1.kostur()
    rapor1 = m1.defter.kontrol()
    boru1 = (m1.defter.kuyrukta + m1.defter.ucusta) / m1.defter.uretilen
    assert rapor1["korunum_tamam"] is True, (
        "beklenmedik: denklem bu mutasyonu yakaladı — dedektör analizi yanlış"
    )
    assert boru1 > 0.01, (
        f"boşaltma kontrolü kayıp geçişi yakalamadı: boruda kalan {boru1:.4f}"
    )
    assert m1.defter.ucusta == m1.mac_dusurmesi, (
        "askıda kalan paket sayısı silinen geçiş sayısına eşit olmalı"
    )

    # --- MUTASYON 2: yanlış havuzdan düşürme -> NEGATİF KORUMA -----------
    m2 = Kosu(Konfig(kol="kapi", senaryo="S2", tohum=1), en_kisa_yol)

    def yanlis_havuz(paket, gonderen, hedef):
        m2.defter.dus("iletim_basarisiz", nereden="kuyruk")   # olması gereken: "ucus"
        m2._uyandir(gonderen)

    m2.mac.iletim_basarisiz = yanlis_havuz
    with pytest.raises(KorunumHatasi):
        m2.kostur()

    # --- MUTASYON 3: doğrudan sayaç oynaması -> DENKLEM ------------------
    m3 = Kosu(Konfig(kol="kapi", senaryo="S0", tohum=1), en_kisa_yol)
    m3.kostur()
    assert m3.defter.kontrol()["korunum_tamam"] is True
    m3.defter.teslim += 7
    assert m3.defter.kontrol()["korunum_tamam"] is False
    assert m3.defter.kontrol()["fark"] == -7


def test_c1_4_bosaltma_boruyu_bosaltiyor():
    """Ç1.4 — koşu sonunda boruda kalan paket oranı < %1."""
    for trafik in ("seyrek", "orta", "yogun"):
        k = Kosu(Konfig(kol="kapi", senaryo="S2", tohum=1, trafik=trafik),
                 en_kisa_yol)
        k.kostur()
        oran = (k.defter.kuyrukta + k.defter.ucusta) / k.defter.uretilen
        assert oran < 0.01, (trafik, oran)


# ==========================================================================
# Ç2 — BELİRLENİMCİLİK, TAM KOŞUDA
# ==========================================================================

@pytest.mark.parametrize("senaryo", ["S0", "S2", "S4", "S5"])
def test_c2_1_ayni_tohum_birebir_ayni(senaryo):
    """Ç2.1 — aynı tohum, birebir aynı sonuç sözlüğü."""
    def kos():
        return Kosu(Konfig(kol="kapi", senaryo=senaryo, tohum=3),
                    en_kisa_yol).kostur()
    assert kos() == kos()


def test_c2_2_pythonhashseed_den_bagimsiz():
    """Ç2.2 — farklı PYTHONHASHSEED, aynı sonuç.

    Bir yerde yerleşik `hash()` kullanılsaydı aynı tohum farklı günlerde
    farklı sonuç verirdi ve sebebi asla bulunamazdı.

    🔴 26 AĞUSTOS 2026 — B-94 (BEŞİNCİ DENETİM) İLE GENİŞLETİLDİ.
    Bu test iki yönden dardı:

      1. Deponun `hash()` KULLANAN TEK karar yolunu **hiç koşmuyordu.**
         `dogrulama/aktaricilar.py::kalite_ablasyonu` permütasyonu
         `random.Random(hash(anahtar) ^ tuz)` ile tohumlanıyor — ve o,
         **ön-kayıtlı H1.1 kapısının null modelidir.** Ç2 yalnızca
         `en_kisa_yol` ile koşuyordu; o kolda `hash()` yok.
      2. **47 sonuç alanından 3'ünü** karşılaştırıyordu.

    Artık iki kol da koşuluyor ve **tam sonuç sözlüğünün** parmak izi
    karşılaştırılıyor.

    🔴 Y7/Y8 — ARACIN KENDİSİ DE DOĞRULANIYOR. `PYTHONHASHSEED`in fiilen
    etkili olduğu **ölçülerek** gösterilir (`hash("dizgi")` üç koşuda üç
    farklı değer verir). Bu olmadan test, ortam değişkeni hiç işlemese bile
    geçerdi — *"boş küme de 0 kırık verir"* (Y7).

    ⚠️ Bugün tutmasının sebebi ölçüldü ve BEYAN EDİLMİŞ bir garanti değil:
    `anahtar` bir **tamsayı demeti** ve CPython tamsayı/demet hash'lerini
    tuzlamaz. `anahtar`a bir gün bir DİZGİ eklenirse (ör. `alan` adı —
    `kalite_ablasyonu`nun imzasında var) kapının null modeli
    `PYTHONHASHSEED`e bağlı olur. Bu test o günü yakalar.
    """
    kod = (
        f"import hashlib, sys; sys.path.insert(0, r'{KOK}');"
        "from sim.config import Konfig;"
        "from sim.kosucu import Kosu;"
        "from dogrulama.aktaricilar import ("
        "en_kisa_yol, AKTARICILAR, kalite_ablasyonu);"
        "iz = lambda s: hashlib.blake2b("
        "repr(sorted(s.items())).encode(), digest_size=12).hexdigest();"
        "K = lambda f: Kosu(Konfig(kol='k', senaryo='S2', tohum=3), f).kostur();"
        "a = K(en_kisa_yol);"
        "b = K(kalite_ablasyonu(AKTARICILAR['gurultuden_kacan']));"
        # 🔴 hash() YOLU: ablasyon kolu. Ayrıca aracın canlılığı: dizgi hash'i
        "print(iz(a), iz(b), hash((7, (1, 2, 3, 40))), hash('ayni_dizgi'))"
    )
    ciktilar = []
    for tohum_env in ("0", "1", "12345"):
        p = subprocess.run([sys.executable, "-c", kod], capture_output=True,
                           text=True, env={**os.environ,
                                           "PYTHONHASHSEED": tohum_env})
        assert p.returncode == 0, p.stderr[-2000:]
        ciktilar.append(p.stdout.strip().split())

    # 🔴 Y8 — ARAÇ CANLI MI: PYTHONHASHSEED gerçekten dizgi hash'ini
    # değiştiriyor mu? Değiştirmiyorsa bu testin tamamı boştur.
    dizgi_hashleri = {c[3] for c in ciktilar}
    assert len(dizgi_hashleri) == 3, (
        f"PYTHONHASHSEED dizgi hash'ini DEĞİŞTİRMİYOR ({dizgi_hashleri}) — "
        f"bu test hiçbir şey doğrulamıyor (Y7).")

    # Ç2.2'nin ASIL değişmezi: iki kolun TAM sonuç sözlüğü ve tamsayı demeti
    # hash'i üç koşuda da aynı olmalı.
    for i, ad in ((0, "en_kisa_yol tam sonuç"),
                  (1, "kalite_ablasyonu tam sonuç (hash() YOLU)"),
                  (2, "hash((7,(1,2,3,40)))")):
        degerler = {c[i] for c in ciktilar}
        assert len(degerler) == 1, (
            f"{ad}: PYTHONHASHSEED'e bağlı — Ç2 KIRILDI. {degerler}")

    # 🔴 Y8 — ablasyon kolu asıl koldan FARKLI sonuç vermeli, yoksa
    # "hash() yolu koşuldu" iddiası boştur.
    assert ciktilar[0][0] != ciktilar[0][1], (
        "ablasyon kolu ile en_kisa_yol AYNI sonucu verdi — hash() yolunun "
        "koşulduğu gösterilemiyor")


def test_c2_3_iki_kol_ayni_kanali_goruyor():
    """🔴 Ç2.3 — TAM KOŞUDA: iki farklı protokol kolu, aynı tohum, aynı kanal.

    Bu kırılırsa eşleştirilmiş istatistik geçersizdir: kollar arasındaki fark
    protokol davranışından değil, farklı kanal gerçeklemesinden gelir.

    Birim testi (`test_rng.py`) bunu oyuncak bir kurulumda sınıyordu; burada
    gerçek MAC, gerçek karıştırıcı ve gerçek trafikle sınanıyor.
    """
    izler = []
    for aktarici in (en_kisa_yol, hedefe_en_yakin):
        k = Kosu(Konfig(kol="kapi", senaryo="S2", tohum=3), aktarici)
        k.mac.kanal_izi = {}
        k.kostur()
        izler.append(k.mac.kanal_izi)

    a, b = izler
    # İki kol gerçekten FARKLI davranmalı, yoksa test boş olur.
    assert len(a) != len(b) or a.keys() != b.keys(), (
        "iki aktarıcı aynı davrandı — test ayırt edici değil"
    )
    ortak = set(a) & set(b)
    assert len(ortak) > 50, f"ortak üçlü çok az: {len(ortak)}"
    for anahtar in ortak:
        assert a[anahtar] == b[anahtar], (
            f"aynı (gönderen, alan, dilim) farklı çekim verdi: {anahtar}"
        )


# ==========================================================================
# Ç3 — YENİ ANALİTİK KONTROLLER
# ==========================================================================

def _mac_duzenek(konumlar, senaryo="S0", tohum=1):
    kon = Konfig(kol="kapi", senaryo=senaryo, tohum=tohum,
                 dugum_sayisi=len(konumlar))
    topo = Topoloji(konumlar=tuple(konumlar),
                    iletim_menzili_m=kon.iletim_menzili_m,
                    girisim_menzili_m=kon.girisim_menzili_m)
    ak, ol = Akislar(tohum), OlayKuyrugu()
    kj = Karistirici.senaryodan(kon, ak)
    return kon, topo, ol, KanalErisimi(kon, topo, Radyo.kur(kon), ol, kj, ak)


def test_c3_1_girisim_toplamsal():
    """Ç3.1 — iki eşzamanlı vericinin girişimi TOPLAMSAL olmalı."""
    kon, topo, ol, mac = _mac_duzenek([(0, 0), (200, 0), (400, 0), (500, 0)])
    hedef = Iletim(0, 1, 0.0, 0.01, "veri")
    a = Iletim(2, 3, 0.0, 0.01, "veri")
    b = Iletim(3, 2, 0.0, 0.01, "veri")

    mac.aktif = [hedef, a]
    g_a = mac._girisim_w(1, hedef, 0.005)
    mac.aktif = [hedef, b]
    g_b = mac._girisim_w(1, hedef, 0.005)
    mac.aktif = [hedef, a, b]
    g_ab = mac._girisim_w(1, hedef, 0.005)

    # 🔴 B-22: `abs=0.0` ZORUNLU. pytest.approx'un varsayılan MUTLAK
    # toleransı 1e-12'dir ve yalnızca `rel` verildiğinde tolerans
    # max(rel*beklenen, 1e-12) olur. Karşılaştırılan güçler ~1e-14 W
    # olduğu için taban her farkı yutuyordu: bu iddia KIRILAMIYORDU.
    assert g_ab == pytest.approx(g_a + g_b, rel=1e-12, abs=0.0)
    # Kapalı formla da doğrula
    elle = (mac.radyo.alinan_guc_w(topo.mesafe(2, 1))
            + mac.radyo.alinan_guc_w(topo.mesafe(3, 1)))
    assert g_ab == pytest.approx(elle, rel=1e-12, abs=0.0)


def test_c3_2_parca_parca_hesap_sabit_girisimde_tek_parcaya_esit():
    """Ç3.2 — girişim sabitse, parça parça hesap tek parça hesapla aynı.

    Parçalama mekanizması kısmi çakışmalar için var. Çakışma yokken
    fazladan bir şey yapmamalı; yapıyorsa parçalama hatalı.
    """
    kon, topo, ol, mac = _mac_duzenek([(0, 0), (250, 0)], senaryo="S2")
    il = Iletim(0, 1, 1.0, 1.0 + kon.paket_suresi_s, "veri")
    mac.aktif = [il]

    # Sabit karıştırıcı → parça sınırı yalnızca baş ve son olmalı
    assert mac._parca_sinirlari(il) == [il.baslangic_s, il.bitis_s]

    per_parcali = mac.alim_per(il)

    sinyal = mac.radyo.alinan_guc_w(topo.mesafe(0, 1))
    gir = mac.karistirici.alinan_guc_w(topo.konumlar[1], 1.0)
    bit = kon.paket_suresi_s * kon.bit_hizi_bps
    ber = mac.radyo.bit_hata_orani(mac.radyo.sinr_lin(sinyal, gir))
    per_tek = -math.expm1(bit * math.log1p(-ber))

    # 🔴 B-22: `abs=0.0` ZORUNLU. pytest.approx'un varsayılan MUTLAK
    # toleransı 1e-12'dir ve yalnızca `rel` verildiğinde tolerans
    # max(rel*beklenen, 1e-12) olur. Karşılaştırılan güçler bir OLASILIK (≤1)
    # olduğu için taban her farkı yutuyordu: bu iddia KIRILAMIYORDU.
    assert per_parcali == pytest.approx(per_tek, rel=1e-12, abs=0.0)


def test_c3_2b_darbeli_karistirici_parcalama_uretiyor():
    """Kontrol kolu: darbeli karıştırıcıda parça sınırı ARTMALI.

    Bu kol olmadan üstteki testin 'parçalama çalışıyor' ile 'parçalama hiç
    devreye girmiyor' arasındaki farkı ayırt edemeyiz.
    """
    kon, topo, ol, mac = _mac_duzenek([(0, 0), (250, 0)], senaryo="S4")
    uzun = Iletim(0, 1, 1.0, 1.0 + 5.0, "veri")     # 5 s: çok darbe kapsar
    mac.aktif = [uzun]
    assert len(mac._parca_sinirlari(uzun)) > 2


@pytest.mark.parametrize("gorev", [0.10, 0.25, 0.50, 0.75])
def test_c3_3_darbeli_ortalama_guc_kosan_sistemde_esit(gorev):
    """🔴 Ç3.3 — H1.3'ün TAMAMI bu eşitliğe dayanıyor.

    Şimdiye kadar eşitlik yalnızca konfigürasyonda doğrulanmıştı. Burada
    koşan sistemde, zaman üzerinden ÖRNEKLENEREK ölçülüyor.

    🔴 B-07: ÖNCEDEN YALNIZCA VARSAYILAN GÖREV ÇEVRİMİNDE KOŞUYORDU.
    Tepe telafisi bir modül sabitiydi (`_TEPE_TELAFI_DB`), görev çevrimi ise
    ayrı bir `Konfig` alanı — ikisi bağımsız değişebiliyordu. Denetimin
    ölçtüğü: görev çevrimi 0,25'te S1↔S3 farkı **−3,010 dB**, 0,10'da
    **−6,988 dB**. Yani `darbe_gorev_cevrimi` bir tarama ekseni olarak
    kullanıldığı an H1.3 sessizce başka bir soruya dönüşüyordu.

    Telafi artık `Konfig.tepe_telafisi_db`den türetiliyor; bu test onu
    görev çevriminin dört değerinde birden sınar.
    """
    nokta = (300.0, 500.0)
    for sabit, darbeli in (("S1", "S3"), ("S2", "S4")):
        kon_s = Konfig(kol="k", senaryo=sabit, darbe_gorev_cevrimi=gorev)
        kon_d = Konfig(kol="k", senaryo=darbeli, darbe_gorev_cevrimi=gorev)
        kj_s = Karistirici.senaryodan(kon_s, Akislar(1))
        kj_d = Karistirici.senaryodan(kon_d, Akislar(1))

        # Darbe periyoduyla ölçüşmeyen bir adım: örnekler kilitlenmesin
        n = 20011
        adim = kon_d.darbe_periyodu_s * 7.0 / n
        ort_s = ist.mean(kj_s.alinan_guc_w(nokta, i * adim) for i in range(n))
        ort_d = ist.mean(kj_d.alinan_guc_w(nokta, i * adim) for i in range(n))

        # 🔴 B-22: `abs=0.0` ZORUNLU. pytest.approx'un varsayılan MUTLAK
        # toleransı 1e-12'dir ve yalnızca `rel` verildiğinde tolerans
        # max(rel*beklenen, 1e-12) olur. Karşılaştırılan güçler ~1e-14 W
        # olduğu için taban her farkı yutuyordu: bu iddia KIRILAMIYORDU.
        assert ort_d == pytest.approx(ort_s, rel=0.02, abs=0.0), (
            f"{sabit} vs {darbeli}: {w_to_dbm(ort_s):.2f} vs "
            f"{w_to_dbm(ort_d):.2f} dBm — H1.3'ün eşit ortalama güç koşulu bozuk"
        )


def test_c3_4_onay_airtime_i_verimde_gorunuyor():
    """Ç3.4 — onay çerçevesinin süresi ölçülen verimde görünmeli.

    Tek atlama, çekişmesiz. Analitik döngü:
        DIFS + ort.geri çekilme + veri + SIFS + onay
    Ölçülen verim bunun %2'si içinde olmalı. Onay airtime'ı sayılmasaydı
    ölçülen verim analitikten belirgin YÜKSEK çıkardı.
    """
    from dogrulama.onay_denetim import sayacli_kosu
    r = sayacli_kosu(1, 1, 0.85)
    kon = r["kon"]
    dongu = (kon.difs_s + (kon.cw_min / 2) * kon.slot_s
             + kon.cerceve_suresi_s(kon.paket_bayt)
             + kon.sifs_s + kon.onay_suresi_s)
    beklenen = kon.paket_bayt * 8 / dongu
    assert r["verim_bps"] == pytest.approx(beklenen, rel=0.02), (
        r["verim_bps"], beklenen)


def test_c3_4b_onay_kanali_mesgul_ediyor():
    """Onay gerçekten kanalı meşgul ediyor mu — yoksa yalnızca gecikme mi?"""
    kon, topo, ol, mac = _mac_duzenek([(0, 0), (200, 0), (400, 0)])
    onay = Iletim(1, 0, 0.0, kon.onay_suresi_s, "onay")
    mac.aktif = [onay]
    ol.simdi = kon.cca_s * 2
    assert mac.kanal_mesgul(2) is True, "onay taşıyıcı dinlemeyi tetiklemiyor"


def test_c3_4c_radyo_mesgul_kendi_iletimini_goruyor():
    """🔴 K-027 regresyonu — düğüm kendi vericisi yayındayken susmalı."""
    kon, topo, ol, mac = _mac_duzenek([(0, 0), (200, 0)])
    mac.gonderim_araligi[0] = (0.0, 0.01)
    ol.simdi = 0.005
    assert mac.radyo_mesgul(0) is True
    ol.simdi = 0.02
    assert mac.radyo_mesgul(0) is False


# ==========================================================================
# 🔴 B-117 / M07 (ALTINCI DENETİM) — PARÇALAMA YOK SAYILINCA HİÇBİR TEST
#    KONUŞMUYORDU
#
# Mutasyon: `noktalar = self._parca_sinirlari(il)` -> `[baslangic, bitis]`.
# Yani parça sınırları HESAPLANMAYA DEVAM EDİYOR ama `alim_per` onları
# YOK SAYIYOR. Ölçüldü (27 Ağu, 4 yapılandırma × 65 sayısal alan):
#
#     S0/t3  43/65 alan farklı · teslim 0,9974 -> 1,0000
#     S2/t1  48/65             · teslim 0,2973 -> 0,2995
#     S3/t2  49/65             · teslim 0,6563 -> 0,6641
#     S4/t9  51/65             · teslim 0,7264 -> 0,7297
#
# 🔴 VE MEVCUT İKİ KORUMA DA SUSUYOR — ölçüldü, `test_kapi_aile0.py` +
# `test_mac.py` mutantla **48 passed**:
#
#   · `test_c3_2`  parçalı == tek parça der, ama SABİT girişimde.
#                  Mutasyon ikisini HER ZAMAN eşitler -> geçer.
#   · `test_c3_2b` `_parca_sinirlari` >2 sınır üretiyor mu bakar.
#                  Mutasyon o fonksiyona DOKUNMUYOR -> geçer.
#
# İkisi de TEK YÖNLÜ: *"eşit olmalı"* diyorlar, *"eşit OLMAMALI"* diyen yok.
# Y11'in tam tarifi.
#
# ⚠️ VE ÖLÇÜM DENETÇİNİN ÇERÇEVESİNİ GENİŞLETTİ: denetçi bunu darbeli
# karıştırıcıya bağlamıştı; ölçüm S0'da — KARIŞTIRICISIZ — en büyük teslim
# kaymasını gösterdi. Parçalamanın asıl işi KISMİ ÇAKIŞMA; karıştırıcı
# ikincil eksen. Bu test ikisini de kapsar.
# ==========================================================================

def _tek_parca_per(mac, topo, il, alici: int) -> float:
    """`alim_per`in parçalama OLMADAN vereceği değer — çerçeve ORTASINDAN.

    `test_c3_2`nin tek-parça hesabının aynısı; orada sabit girişimde
    eşitlik için kullanılıyor, burada FARKLILIK için.
    """
    sinyal = mac.radyo.alinan_guc_w(topo.mesafe(il.gonderen, alici))
    gir = mac._girisim_w(alici, il, 0.5 * (il.baslangic_s + il.bitis_s))
    bit = (il.bitis_s - il.baslangic_s) * mac.kon.bit_hizi_bps
    ber = mac.radyo.bit_hata_orani(mac.radyo.sinr_lin(sinyal, gir))
    return -math.expm1(bit * math.log1p(-ber))


def test_b117_m07_KISMI_CAKISMADA_parcalama_tek_parcadan_FARKLI():
    """🔴 Kısmi çakışmada parçalı hesap tek parçadan AYRILMAK ZORUNDA.

    Kurulum: girişimci, hedef çerçevenin yalnızca SON %30'unu örtüyor.
    Çerçeve ortası girişimin DIŞINDA kalıyor — yani tek parça hesabı
    girişimi HİÇ görmüyor, parçalı hesap %30'unda görüyor.

    🔴 Y8 — bozulan yolun tetiklendiği ÖNCE gösterilir: parça sınırı > 2.
    """
    kon, topo, ol, mac = _mac_duzenek([(0, 0), (250, 0), (300, 0)],
                                      senaryo="S0")
    bas, bit = 1.0, 1.0 + kon.paket_suresi_s
    il = Iletim(0, 1, bas, bit, "veri")
    # girişimci: son %30'u örtüyor, çerçeve ORTASINI kapsamıyor
    ortala = bas + 0.70 * (bit - bas)
    baska = Iletim(2, 0, ortala, bit + 0.5 * (bit - bas), "veri")
    mac.aktif = [il, baska]

    # 🔴 Y8 — parçalama gerçekten devrede mi
    sinirlar = mac._parca_sinirlari(il)
    assert len(sinirlar) > 2, (
        f"parça sınırı {len(sinirlar)} — kısmi çakışma sınır ÜRETMEDİ, "
        f"kurulum bu boşluğu sınamıyor (Y8)")
    assert bas < ortala < bit

    parcali = mac.alim_per(il)
    tek = _tek_parca_per(mac, topo, il, 1)

    # 🔴 ASIL ÖLÇÜT: ikisi AYNI OLAMAZ. `pytest.approx` mutlak taban
    # KULLANILMIYOR (B-22/Y10): karşılaştırılan büyüklük bir olasılık.
    assert parcali != pytest.approx(tek, rel=1e-9, abs=0.0), (
        f"🔴 kısmi çakışmada parçalı hesap ({parcali!r}) tek parça hesapla "
        f"({tek!r}) AYNI — `alim_per` parça sınırlarını YOK SAYIYOR "
        f"(B-117/M07). Girişim çerçevenin son %30'unda; tek parça onu "
        f"göremez, parçalı görmek ZORUNDA.")
    assert parcali > tek, (
        "parçalı hesap girişimi GÖRDÜĞÜ için PER'i daha yüksek olmalı")


def test_b117_m07_DARBELI_karistiricida_da_FARKLI():
    """🔴 İkinci eksen: darbeli karıştırıcı çerçeveyi bölüyor.

    Denetçinin işaret ettiği eksen. Kısmi çakışmadan bağımsız olarak
    sınanır — biri kapanıp diğeri açık kalmasın.
    """
    kon, topo, ol, mac = _mac_duzenek([(0, 0), (250, 0)], senaryo="S4")
    kj = mac.karistirici
    assert kj is not None and kj.darbeli, "S4 darbeli olmalı — kurulum bozuk"

    # Bir darbe sınırının İÇİNE düşen bir çerçeve seç (Y8)
    p = kj.periyot_s
    sinir = (1.0 + kj.gorev_cevrimi - kj.faz_kesri) * p
    bas = sinir - 0.4 * kon.paket_suresi_s
    il = Iletim(0, 1, bas, bas + kon.paket_suresi_s, "veri")
    mac.aktif = [il]

    sinirlar = mac._parca_sinirlari(il)
    assert len(sinirlar) > 2, (
        f"darbe sınırı çerçevenin İÇİNE düşmedi (sınır {len(sinirlar)}) — "
        f"kurulum bu boşluğu sınamıyor (Y8)")

    parcali = mac.alim_per(il)
    tek = _tek_parca_per(mac, topo, il, 1)
    assert parcali != pytest.approx(tek, rel=1e-9, abs=0.0), (
        f"🔴 darbe sınırı çerçeveyi böldüğü hâlde parçalı ({parcali!r}) ve "
        f"tek parça ({tek!r}) hesap AYNI — B-117/M07")
