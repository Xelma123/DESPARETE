"""
KURULUM KALİBRASYONU — K-017 ve K-019'un ÜRETİCİ KOMUTU (B-08).

🔴 NEDEN BU DOSYA VAR
=====================
Bağımsız denetim (`aile0_audit.md`, B-08) iki şey buldu:

  1. K-017 ve K-019 kayıtlarında **"Üretici:" satırı YOK** ve depoda o
     sayıları üreten hiçbir betik yok. Kural 1: *"Her sayının yanında
     üretici komut ve kaynak dosya yazılır."*
  2. K-019'un tablosu **projenin BİRİNCİL ÇALIŞMA NOKTASINI** (S2 = +2 dBm)
     seçen tablodur ve **yeniden üretilemez** durumdadır.

Ayrıca K-019 kendi kaydında şunu taahhüt etmişti:

  > *"MAC'in yeniden iletimleri devreye girince kullanılabilir bağ tanımı
  >  değişir; kalibrasyon mühürden önce tekrarlanacak."*

MAC/onay 18 Ağustos'ta girdi (K-027). Tekrarlandığına dair kayıt yoktu.

Kullanım:
    python dogrulama/kurulum_kalibrasyonu.py          # A + B
    python dogrulama/kurulum_kalibrasyonu.py --a      # yalnız K-017
    python dogrulama/kurulum_kalibrasyonu.py --b      # yalnız K-019
    python dogrulama/kurulum_kalibrasyonu.py --c      # uçtan uca çapraz kontrol

🔴 TOHUMLAR: yalnızca AYARLAMA kümesi (1–30). Ana deney tohumları
(2000–2029) bu betikte hiçbir amaçla geçmez (K-025).
"""

from __future__ import annotations

import math
import sys
from collections import deque
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

from sim.config import Konfig                                    # noqa: E402
from sim.radio import Karistirici, Radyo, dbm_to_w               # noqa: E402
from sim.rng import Akislar                                      # noqa: E402
from sim.topology import Topoloji                                # noqa: E402

AYARLAMA_TOHUMLARI = tuple(range(1, 31))


# ==========================================================================
# BÖLÜM A — K-017: ağ parametreleri ve bağlantı koşullamasının önyargısı
# ==========================================================================

def _baglantili_mi(konumlar: np.ndarray, menzil: float) -> bool:
    """Tek bir yerleşim bağlı mı — BFS."""
    n = len(konumlar)
    d2 = ((konumlar[:, None, :] - konumlar[None, :, :]) ** 2).sum(-1)
    komsu = d2 <= menzil * menzil
    np.fill_diagonal(komsu, False)
    gorulen = np.zeros(n, bool)
    gorulen[0] = True
    kuyruk = deque([0])
    while kuyruk:
        i = kuyruk.popleft()
        for j in np.nonzero(komsu[i] & ~gorulen)[0]:
            gorulen[j] = True
            kuyruk.append(int(j))
    return bool(gorulen.all())


def _dereceler(konumlar: np.ndarray, menzil: float) -> np.ndarray:
    d2 = ((konumlar[:, None, :] - konumlar[None, :, :]) ** 2).sum(-1)
    komsu = d2 <= menzil * menzil
    np.fill_diagonal(komsu, False)
    return komsu.sum(1)


def bolum_a(cekim: int = 200_000) -> None:
    """K-017'nin sayıları — bağımsız çekimle.

    🔴 DERECE KAYMASI: K-017 **+%0,9** yazıyor. Denetim **−%0,362 ± 0,036**
    ölçtü (işaret ters). K-035'te öğrenci transkripsiyon hatasını kabul
    etti. Burada üçüncü kez, üretici komutla ölçülüyor.
    """
    kon = Konfig(kol="kalibrasyon")
    n, alan, menzil = kon.dugum_sayisi, kon.alan_m, kon.iletim_menzili_m
    rng = np.random.default_rng(20260819)

    print("=" * 78)
    print("BÖLÜM A — K-017: ağ parametreleri (40 düğüm / 280 m)")
    print("=" * 78)
    print(f"Bağımsız çekim  : {cekim:,}".replace(",", " "))
    print(f"Parametreler    : n={n} · alan={alan:.0f} m · menzil={menzil:.0f} m")
    print()

    bagli = 0
    d_kosulsuz: list[np.ndarray] = []
    d_kosullu: list[np.ndarray] = []
    for _ in range(cekim):
        k = rng.uniform(0.0, alan, size=(n, 2))
        d = _dereceler(k, menzil)
        d_kosulsuz.append(d)
        if _baglantili_mi(k, menzil):
            bagli += 1
            d_kosullu.append(d)

    ort_kosulsuz = float(np.mean([d.mean() for d in d_kosulsuz]))
    ort_kosullu = float(np.mean([d.mean() for d in d_kosullu]))

    # Analitik referans: E[derece] = (n-1)·P(iki nokta menzil içinde).
    # Kare alanda düzgün iki nokta için kapalı form.
    r = menzil / alan
    p_menzil = (math.pi * r ** 2 - 8.0 / 3.0 * r ** 3 + 0.5 * r ** 4)
    analitik = (n - 1) * p_menzil

    # 🔴 KAYMA ANALİTİK DEĞERE GÖRE HESAPLANIR — örneklem hatası SIFIR.
    # Ölçülen koşulsuz ortalamaya göre hesaplasaydık, koşullu örneklem
    # koşulsuzun ALT KÜMESİ olduğu için ikisi korelasyonlu olurdu ve farkın
    # standart hatası yanlış çıkardı. Analitik referansta o sorun yok;
    # ölçülen koşulsuz ortalama yalnızca ÇAPRAZ KONTROL olarak basılır.
    kayma = 100.0 * (ort_kosullu - analitik) / analitik
    se = float(np.std([d.mean() for d in d_kosullu], ddof=1)
               / math.sqrt(len(d_kosullu)))
    kayma_se = 100.0 * se / analitik

    oran = bagli / cekim
    # Reddetme örneklemesinde ortalama deneme = 1/p
    ort_deneme = 1.0 / oran if oran else float("inf")

    print(f"{'büyüklük':<34} {'K-017 iddiası':>14} {'ölçülen':>16}")
    print("-" * 78)
    print(f"{'doğal bağlantı oranı':<34} {'%82':>14} {'%' + f'{100*oran:.2f}':>16}")
    print(f"{'ortalama deneme':<34} {'1,20':>14} {ort_deneme:>16.4f}")
    print(f"{'ortalama derece (koşulsuz, ölçülen)':<34} {'7,5':>14} {ort_kosulsuz:>16.5f}")
    print(f"{'  ANALİTİK kapalı form (referans)':<34} {'—':>14} {analitik:>16.5f}")
    print(f"{'ortalama derece (koşullu)':<34} {'—':>14} {ort_kosullu:>16.5f}")
    print(f"{'DERECE KAYMASI':<34} {'+%0,9':>14} "
          f"{'%' + f'{kayma:+.3f} ± {kayma_se:.3f}':>16}")
    print()
    if kayma < 0:
        print("🔴 İŞARET TERS — koşullama dereceyi DÜŞÜRÜYOR, yükseltmiyor.")
        print("   K-017'nin '+%0,9' değeri YANLIŞTIR (K-035'te kabul edildi).")
    print(f"   Nitel sonuç değişmiyor: |kayma| = %{abs(kayma):.3f} < %1.")
    print()

    # Gerçek `Topoloji.uret` akışında deneme sayısı ve topoloji özeti
    print("GERÇEK `Topoloji.uret` AKIŞINDA (30 ayarlama tohumu):")
    denemeler, atlamalar, caplar, dereceler = [], [], [], []
    for t in AYARLAMA_TOHUMLARI:
        topo = Topoloji.uret(Konfig(kol="kalibrasyon", tohum=t), Akislar(t))
        ozet = topo.ozet()
        dereceler.append(ozet["ortalama_derece"])
        # atlama/çap: en büyük bileşende BFS
        bilesen = topo.en_buyuk_bilesen()
        uzunluklar = []
        for s in bilesen:
            mesafe = {s: 0}
            kuyruk = deque([s])
            while kuyruk:
                u = kuyruk.popleft()
                for v in topo.geometrik_komsular(u):
                    if v not in mesafe:
                        mesafe[v] = mesafe[u] + 1
                        kuyruk.append(v)
            uzunluklar += [d for d in mesafe.values() if d > 0]
        if uzunluklar:
            atlamalar.append(sum(uzunluklar) / len(uzunluklar))
            caplar.append(max(uzunluklar))
    print(f"   ortalama atlama : {np.mean(atlamalar):.3f}   (K-017: 2,90)")
    print(f"   çap             : {np.mean(caplar):.2f} "
          f"[{min(caplar)} · {max(caplar)}]   (K-017: 6,6 [5·12])")
    print(f"   ortalama derece : {np.mean(dereceler):.3f}   (K-017: 7,5)")
    print()


# ==========================================================================
# BÖLÜM B — K-019: karıştırıcı gücü kalibrasyonu
# ==========================================================================
#
# 🔴 "SAPMA GEREKEN ÇİFT" TANIMI — YENİDEN İLAN EDİLDİ
# =====================================================
# Denetim raporu §7-1: *"K-019'un 'sapma gereken çift' metriğinin kod
# karşılığını bulamadım."* Ben de bulamadım; orijinal tanım KURTARILAMAZ.
# Aşağıdaki tanım YENİDİR, açıkça ilan edilir ve K-038'de kayda geçer:
#
#   BAĞ KULLANILABİLİR  ⇔  PER(u→v) ≤ PER_menzil
#     PER_menzil = karıştırmasız, tam menzilde (280 m) bir veri çerçevesinin
#     hata olasılığı = 0,169693. Keyfi bir eşik DEĞİL: modelin kendi menzil
#     tanımının (SINR = β) PER karşılığı. Böylece "kullanılabilir bağ",
#     karıştırma altında da karıştırmasız menzil tanımıyla TUTARLI kalır.
#
#   SAPMA GEREKEN ÇİFT  ⇔  d_karıştırmalı(s,d) > d_karıştırmasız(s,d)
#     Yani karıştırmasız minimum-atlama yollarının HEPSİ koptu; atlama
#     sayısına bakan bir protokol sapmak ZORUNDA. Beraberlik belirsizliği
#     yok (bir yol seçmeyi gerektirmiyor).
#
#   ⚠️ GRAF YÖNLÜDÜR: karıştırıcı ALICIYI etkiler, dolayısıyla u→v ile
#   v→u aynı kullanılabilirlikte olmayabilir.
#
# İKİ BAĞ TANIMI — K-019'un kendi taahhüdü
# =========================================
#   MAC ÖNCESİ : tek deneme.               PER ≤ PER_menzil
#   MAC SONRASI: 5 deneme (yeniden_deneme_siniri=4 → 1+4 iletim).
#                Etkin hata = PER^5;  PER^5 ≤ PER_menzil
#                ⇔ PER ≤ PER_menzil^(1/5) = 0,7013
# ==========================================================================

GUC_TARAMASI_DBM = (-10.0, -7.0, -4.0, -1.0, 0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 11.0)


def _bag_matrisi(topo: Topoloji, radyo: Radyo, kon: Konfig,
                 kj: Karistirici | None, esik_per: float) -> np.ndarray:
    """Yönlü kullanılabilirlik matrisi: bag[u, v] = u→v kullanılabilir mi."""
    n = topo.dugum_sayisi
    bag = np.zeros((n, n), bool)
    for v in range(n):
        girisim = 0.0 if kj is None else kj.alinan_guc_w(topo.konumlar[v], 0.0)
        for u in range(n):
            if u == v:
                continue
            sinyal = radyo.alinan_guc_w(topo.mesafe(u, v))
            per = radyo.paket_hata_olasiligi(
                radyo.sinr_lin(sinyal, girisim), kon.paket_bayt)
            bag[u, v] = per <= esik_per
    return bag


def _mesafe_matrisi(bag: np.ndarray) -> np.ndarray:
    """Yönlü BFS ile atlama mesafeleri; ulaşılamayan = -1."""
    n = len(bag)
    uzak = np.full((n, n), -1, int)
    for s in range(n):
        uzak[s, s] = 0
        kuyruk = deque([s])
        while kuyruk:
            u = kuyruk.popleft()
            for v in np.nonzero(bag[u] & (uzak[s] < 0))[0]:
                uzak[s, v] = uzak[s, u] + 1
                kuyruk.append(int(v))
    return uzak


def bolum_b(tohum_sayisi: int = 30) -> None:
    kon0 = Konfig(kol="kalibrasyon")
    radyo0 = Radyo.kur(kon0)
    per_menzil = radyo0.menzilde_per(kon0.iletim_menzili_m, kon0.paket_bayt)
    esikler = {
        "MAC öncesi (1 deneme)": per_menzil,
        "MAC sonrası (5 deneme)": per_menzil ** (1.0 / 5.0),
    }

    print("=" * 78)
    print("BÖLÜM B — K-019: karıştırıcı gücü kalibrasyonu")
    print("=" * 78)
    print("🔴 'Sapma gereken çift' TANIMI YENİDEN İLAN EDİLDİ (orijinali")
    print("   kurtarılamadı — denetim §7-1). Tanım dosya başında yazılı.")
    print()
    print(f"Tohum           : {tohum_sayisi} ayarlama tohumu (1–{tohum_sayisi})")
    print(f"PER eşiği       : menzil sınırındaki PER = {per_menzil:.6f}")
    print(f"  MAC öncesi    : PER ≤ {esikler['MAC öncesi (1 deneme)']:.4f}")
    print(f"  MAC sonrası   : PER ≤ {esikler['MAC sonrası (5 deneme)']:.4f}"
          f"   (etkin PER^5 ≤ {per_menzil:.4f})")
    print("Graf            : YÖNLÜ (karıştırıcı alıcıyı etkiler)")
    print()

    topolar = [Topoloji.uret(Konfig(kol="kalibrasyon", tohum=t), Akislar(t))
               for t in AYARLAMA_TOHUMLARI[:tohum_sayisi]]

    for tanim, esik in esikler.items():
        print("-" * 78)
        print(f"BAĞ TANIMI: {tanim}")
        print("-" * 78)
        print(f"{'güç':>7} {'ulaşılabilir çift':>22} {'sapma gereken çift':>22}")
        print(f"{'':>7} {'ort ± SH  (std)':>22} {'ort ± SH  (std)':>22}")
        satirlar = []

        for guc in GUC_TARAMASI_DBM:
            ulas, sapma = [], []
            for topo, t in zip(topolar, AYARLAMA_TOHUMLARI[:tohum_sayisi]):
                kon = Konfig(kol="kalibrasyon", tohum=t, senaryo="S2",
                             karistirici_guc_override_dbm=guc)
                radyo = Radyo.kur(kon)
                kj = Karistirici(
                    guc_w=dbm_to_w(guc), konum=kon.karistirici_merkez,
                    yol_kaybi_usteli=kon.yol_kaybi_usteli,
                    frekans_hz=kon.frekans_hz, darbeli=False,
                    periyot_s=kon.darbe_periyodu_s,
                    gorev_cevrimi=kon.darbe_gorev_cevrimi, faz_kesri=0.0,
                    hareketli=False, hiz_ms=kon.karistirici_hiz_ms,
                    yorunge_yaricap_m=kon.karistirici_yorunge_yaricap_m)

                d_temiz = _mesafe_matrisi(_bag_matrisi(topo, radyo, kon, None, esik))
                d_karis = _mesafe_matrisi(_bag_matrisi(topo, radyo, kon, kj, esik))

                n = topo.dugum_sayisi
                maske = ~np.eye(n, dtype=bool)
                # Payda: karıştırmasız ULAŞILABİLİR çiftler
                temiz_ulasir = (d_temiz >= 0) & maske
                toplam = int(temiz_ulasir.sum())
                if not toplam:
                    continue
                hala_ulasir = temiz_ulasir & (d_karis >= 0)
                ulas.append(100.0 * hala_ulasir.sum() / toplam)
                # Sapma: hâlâ ulaşılabilir AMA mesafe arttı
                sapti = hala_ulasir & (d_karis > d_temiz)
                sapma.append(100.0 * sapti.sum() / toplam)

            isaret = " <- S2" if guc == 2.0 else (" <- S1" if guc == -4.0 else "")
            u_ort, u_sh = float(np.mean(ulas)), float(np.std(ulas, ddof=1) / math.sqrt(len(ulas)))
            s_ort, s_sh = float(np.mean(sapma)), float(np.std(sapma, ddof=1) / math.sqrt(len(sapma)))
            satirlar.append((guc, u_ort, u_sh, s_ort, s_sh))
            print(f"{guc:>+6.0f}  {u_ort:>10.1f} ± {u_sh:<4.1f} ({np.std(ulas):>4.1f})"
                  f"  {s_ort:>9.1f} ± {s_sh:<4.1f} ({np.std(sapma):>4.1f}){isaret}")

        # 🔴 SEÇİM ÖLÇÜTÜ KODLA UYGULANIR — prozayla değil (`03` B5:
        # "yargıyı elle yazmak"). K-019'un kendi ölçütü, birebir:
        #   "sapma gereken çift oranını en büyükle, ulaşılabilirliği
        #    %90'ın ALTINA düşürmeden."
        secim = eski_olcut(satirlar)
        if secim is not None:
            print()
            print(f"  ⇒ ÖLÇÜTÜN SEÇTİĞİ GÜÇ: {secim[0]:+.0f} dBm "
                  f"(ulaşılabilir %{secim[1]:.1f}, sapma %{secim[3]:.1f})")
            s2 = next((r for r in satirlar if r[0] == 2.0), None)
            if s2 and abs(secim[0] - 2.0) > 1e-9:
                # Karar sınırda mı? SH cinsinden uzaklık.
                z = (s2[1] - 90.0) / s2[2] if s2[2] else float("inf")
                print(f"    🔴 S2 (+2 dBm) DEĞİL. S2'de ulaşılabilir "
                      f"%{s2[1]:.1f} ± {s2[2]:.1f} — %90 eşiğinden "
                      f"{z:+.1f} SH uzakta.")
        else:
            print()
            print("  ⇒ ⚠️ Hiçbir güç %90 ulaşılabilirlik tabanını sağlamıyor.")
        print()

    print("K-019'un ilan ettiği tablo (karşılaştırma için):")
    print("    -10 dBm: ulaşılabilir %99,8 · sapma %8,5")
    print("     -4 dBm: ulaşılabilir %99,5 · sapma %18,3   <- S1")
    print("      0 dBm: ulaşılabilir %98,0 · sapma %29,4")
    print("     +2 dBm: ulaşılabilir %93,5 · sapma %37,2   <- S2")
    print("     +4 dBm: ulaşılabilir %87,7 · sapma %43,5")
    print("     +6 dBm: ulaşılabilir %77,4 · sapma %49,4")
    print("    +10 dBm: ulaşılabilir %57,2 · sapma %60,6")
    print()
    print("SEÇİM ÖLÇÜTÜ (K-019, değişmedi): sapma gereken çift oranını en")
    print("büyükle, ulaşılabilirliği %90'ın ALTINA düşürmeden.")


# ==========================================================================
# KARAR ÜRETEN YÜKLEMLER — ayrı ve TEST EDİLEBİLİR
#
# `03` B5: "Analiz kodunu üretim kodu kadar ciddiye al ve karar üreten
# yüklemlerini AYRI ve test edilebilir yaz." Bu iki fonksiyon çalışma
# noktasını seçiyor; gövdenin içine gömülü kalsalardı sınanamazlardı.
# Regresyon: `tests/test_kalibrasyon.py`
# ==========================================================================

def eski_olcut(satirlar):
    """K-019'un ÖLÇÜTÜ: sapmayı en büyükle, ulaşılabilirlik ≥ %90.

    `satirlar`: (güç, ulaşılabilir%, ulaş_SH, sapma%, sapma_SH) demetleri.
    Döner: seçilen satır ya da None (hiçbiri tabanı sağlamıyorsa).

    ⚠️ Bu ölçüt ARTIK YÜRÜRLÜKTE DEĞİL (K-039). Karşılaştırma için duruyor:
    raporda iki ölçütün seçtiği nokta da yazılacak.
    """
    uygun = [r for r in satirlar if r[1] >= 90.0]
    return max(uygun, key=lambda r: r[3]) if uygun else None


ULASILABILIRLIK_TABANI = 90.0      # % — K-039'un ilan ettiği kısıt


# 🔴 B-60 (K-053) — KISITIN ATLANMASI ARTIK AÇIK BİR BEYAN.
# Önceki imza `ulasilabilirlik=None` idi ve varsayılan, ilan edilen
# *"ulaşılabilirlik ≥ %90"* kısıtını **sessizce atlıyordu**. Docstring
# *"yalnızca birim testleri için"* diyordu — bu bir YORUM, koruma değil;
# B-29'un kendi hata sınıfının zayıflatılmış hâli.
class _UlasilabilirlikYok:
    """🔴 B-71 (K-056) — NÖBETÇİ ARTIK DİZGİ DEĞİL.

    Önceki sürüm `"__ULASILABILIRLIK_YOK__"` dizgisiydi ve kimlik (`is`)
    karşılaştırmasına dayanıyordu. Dördüncü bağımsız denetim kırdı: CPython
    aynı literali **interning** ile aynı nesneye bağlıyor, yani düz bir
    dizgi literali de nöbetçi sayılıyordu — ve kısıt **sessizce atlanıp**
    B-29'un engellemek için yazıldığı **+6 dBm** seçiliyordu.

    Daha kötüsü, çalışma anında üretilen aynı değer
    *(`"__ULASILABILIRLIK_" + "YOK__"`)* interning'e girmez ve `is` **False**
    döner: aynı değer iki farklı davranış üretir. Depo bu hata sınıfını
    `rng.py`de (`hash()` tuzlanması) zaten adlandırmıştı.

    Tekil bir nesne bu belirsizliği ortadan kaldırır.
    """

    __slots__ = ()

    def __repr__(self) -> str:      # hata mesajlarında okunur kalsın
        return "ULASILABILIRLIK_YOK"


ULASILABILIRLIK_YOK = _UlasilabilirlikYok()


def yeni_olcut(egri, ulasilabilirlik):
    """K-039'un ÖLÇÜTÜ — İKİ KOŞULU BİRDEN.

        Çalışma noktası, uçtan uca teslim oranını taramanın DİNAMİK
        ARALIĞININ ORTASINA en yakın getiren güçtür;
        **ULAŞILABİLİRLİK ≥ %90 kısıtı altında.**

    `egri`            : (güç, teslim_oranı) demetleri
    `ulasilabilirlik` : {güç: ulaşılabilir çift %} — MAC sonrası bağ tanımı
    Döner: (taban, tavan, orta, seçilen_satır)

    🔴 B-29 — KISITIN YARISI KODA HİÇ GİRMEMİŞTİ.
    ---------------------------------------------------------------------
    K-039 *"Uygulandığında (kod, proza değil)"* diye yazıyordu, ama bu
    fonksiyon ulaşılabilirliği **argüman olarak bile almıyordu**. İkinci
    bağımsız denetim kırdı:

        yeni_olcut([(-10, .90), (0, .70), (6, .51), (11, .12)]) -> +6 dBm

    +6 dBm'in ölçülen ulaşılabilirliği **%84,8** — ilan edilen tabanın
    altında, ve ölçüt onu seçiyordu. Bugün bağlayıcı değildi (S2'de %97,0),
    ama K-039'un kendi *"BUNU NE DEĞİŞTİRİR"* satırı radyo modeli ya da
    menzil tanımı değişirse tablonun değişeceğini yazıyor. O gün ölçüt
    kısıtı sormadan bir nokta seçecekti.

    🔴 B-60 (K-053) — KISITIN ATLANMASI ARTIK AÇIK BİR BEYAN.
    ---------------------------------------------------------------------
    Önceki imza `ulasilabilirlik=None` idi ve **varsayılan**, ilan edilen
    kısıtı sessizce atlıyordu. Docstring *"yalnızca birim testleri
    içindir"* diyordu — bu bir YORUM, koruma değil. Üçüncü bağımsız
    denetim bunu B-29'un kendi hata sınıfının **zayıflatılmış hâli** diye
    işaretledi: kısıt koda girmişti, ama atlanması hâlâ sessizdi.

    Artık argüman **zorunlu**; atlamak isteyen `ULASILABILIRLIK_YOK`
    nöbetçisini AÇIKÇA geçmek zorunda.
    """
    if ulasilabilirlik is not ULASILABILIRLIK_YOK:
        # 🔴 B-71 (K-056) — HARİTA EĞRİYİ KAPSAMAK ZORUNDA.
        # Eksik bir anahtar `.get(g, 0.0)` ile **sessizce eleme** demekti:
        # denetim ölçtü, `0` anahtarı eksik olunca çalışma noktası
        # `(0, 0.70)` → `(-10, 0.90)` olarak SESSİZCE değişiyordu.
        # `03` B5: "yanlış sayı, çalışmayan koddan tehlikelidir çünkü sessizdir."
        eksik = {g for g, _ in egri} - set(ulasilabilirlik)
        if eksik:
            raise ValueError(
                f"ulaşılabilirlik haritası eğriyi kapsamıyor; eksik güçler: "
                f"{sorted(eksik)}. Eksik anahtar sessizce ELEME demektir ve "
                f"çalışma noktasını fark ettirmeden değiştirir.")
        uygun = [r for r in egri
                 if ulasilabilirlik[r[0]] >= ULASILABILIRLIK_TABANI]
        if not uygun:
            raise ValueError(
                f"hiçbir güç %{ULASILABILIRLIK_TABANI:.0f} ulaşılabilirlik "
                f"tabanını sağlamıyor — çalışma noktası seçilemez"
            )
    else:
        uygun = list(egri)

    # Dinamik aralık TARAMANIN TAMAMINDAN okunur, uygun alt kümeden değil:
    # aralık ölçümün duyarlılık ekseni, kısıt ise seçilebilirlik ekseni.
    tavan = max(o for _, o in egri)
    taban = min(o for _, o in egri)
    orta = 0.5 * (tavan + taban)
    return taban, tavan, orta, min(uygun, key=lambda r: abs(r[1] - orta))


# ==========================================================================
# BÖLÜM C — UÇTAN UCA ÇAPRAZ KONTROL
#
# 🔴 NEDEN VAR: Bölüm B bir GRAF METRİĞİDİR. Çalışma noktası seçimi, sonunda
# ölçülecek büyüklüğe — UÇTAN UCA TESLİM ORANINA — dayanmak zorundadır.
# Graf metriği o büyüklükle monoton ilişkili DEĞİLSE, ölçüt yanlış eksende
# seçim yapıyor demektir. `03` B3: "metrik gerçekten onu mu ölçüyor?"
# ==========================================================================

CAPRAZ_TOHUMLAR = (1, 7, 13, 19, 23)


def bolum_c() -> None:
    from dogrulama.olcum import olc
    from dogrulama.aktaricilar import en_kisa_yol
    import statistics as ist

    print("=" * 78)
    print("BÖLÜM C — uçtan uca teslim oranı taraması (gerçek simülatör)")
    print("=" * 78)
    print(f"Tohum: {CAPRAZ_TOHUMLAR} · sabit karıştırıcı · orta trafik")
    print("⚠️ KÂHİN aktarıcı (`en_kisa_yol`) — mutlak değer değil, EĞRİNİN")
    print("   ŞEKLİ okunur: çalışma noktası dinamik aralığın neresinde?")
    print()
    print(f"{'güç':>6} {'teslim oranı':>20}   {'not':<28}")
    print("-" * 78)
    egri = []
    for guc in GUC_TARAMASI_DBM:
        oranlar = [
            olc(Konfig(kol="capraz", senaryo="S2", trafik="orta", tohum=t,
                       karistirici_guc_override_dbm=guc),
                en_kisa_yol)["teslim_orani"]
            for t in CAPRAZ_TOHUMLAR
        ]
        ort, std = ist.mean(oranlar), ist.stdev(oranlar)
        egri.append((guc, ort))
        not_ = ""
        if guc == 2.0:
            not_ = "<- S2 (birincil çalışma noktası)"
        elif guc == -4.0:
            not_ = "<- S1"
        print(f"{guc:>+6.0f} {ort:>13.4f} ± {std:<5.4f}   {not_:<28}")
    print()

    # ======================================================================
    # 🔴 YENİ SEÇİM ÖLÇÜTÜ — K-039'da ilan edildi, BURADA UYGULANIYOR
    # ======================================================================
    # K-019'un ölçütü ("sapma gereken çift oranını en büyükle") YENİDEN
    # UYGULANAMAZ: metriğin kod karşılığı kurtarılamadı (denetim §7-1).
    # Yerine geçen ölçüt, aynı ilkenin ÜRETİLEBİLİR hâlidir:
    #
    #   Çalışma noktası, uçtan uca teslim oranını taramanın DİNAMİK
    #   ARALIĞININ ORTASINA en yakın getiren güçtür; ulaşılabilirlik
    #   (MAC sonrası bağ tanımı) ≥ %90 kısıtı altında.
    #
    # NEDEN ORTA NOKTA: metrik orada her iki yönde de en çok başlığa
    # sahiptir — bir protokol hem iyileşme hem kötüleşme gösterebilir.
    # Tabanda veya tavanda farklar sıkışır. `03` B3'ün "yalnızca zorlayıcı
    # noktada ölçme" ve "durağan bir referans noktası da olmalı"
    # uyarılarının ikisini birden karşılar.
    #
    # ⚠️ DÜRÜSTLÜK NOTU: bu ölçüt taramayı GÖRDÜKTEN SONRA yazıldı.
    # Ön-kayıtlı bir seçim DEĞİLDİR; mevcut çalışma noktasının BETİMLEYİCİ
    # gerekçesidir. K-039 bunu açıkça kaydeder.
    # 🔴 B-29 — kısıt artık ÖLÇÜLÜP geçiriliyor, prozada kalmıyor.
    # Bağ tanımı MAC SONRASI (5 deneme) — simülatörün fiilen uyguladığı hâl.
    kon0 = Konfig(kol="kalibrasyon")
    radyo0 = Radyo.kur(kon0)
    esik = radyo0.menzilde_per(kon0.iletim_menzili_m, kon0.paket_bayt) ** 0.2
    ulasim = {}
    topolar = [Topoloji.uret(Konfig(kol="kalibrasyon", tohum=t), Akislar(t))
               for t in CAPRAZ_TOHUMLAR]
    for guc, _ in egri:
        oranlar = []
        for topo, t in zip(topolar, CAPRAZ_TOHUMLAR):
            kon = Konfig(kol="kalibrasyon", tohum=t, senaryo="S2",
                         karistirici_guc_override_dbm=guc)
            kj = Karistirici(
                guc_w=dbm_to_w(guc), konum=kon.karistirici_merkez,
                yol_kaybi_usteli=kon.yol_kaybi_usteli,
                frekans_hz=kon.frekans_hz, darbeli=False,
                periyot_s=kon.darbe_periyodu_s,
                gorev_cevrimi=kon.darbe_gorev_cevrimi, faz_kesri=0.0,
                hareketli=False, hiz_ms=kon.karistirici_hiz_ms,
                yorunge_yaricap_m=kon.karistirici_yorunge_yaricap_m)
            radyo = Radyo.kur(kon)
            d_temiz = _mesafe_matrisi(_bag_matrisi(topo, radyo, kon, None, esik))
            d_kar = _mesafe_matrisi(_bag_matrisi(topo, radyo, kon, kj, esik))
            n = topo.dugum_sayisi
            maske = ~np.eye(n, dtype=bool)
            temiz_ulasir = (d_temiz >= 0) & maske
            if temiz_ulasir.sum():
                oranlar.append(100.0 * ((temiz_ulasir & (d_kar >= 0)).sum()
                                        / temiz_ulasir.sum()))
        ulasim[guc] = float(np.mean(oranlar)) if oranlar else 0.0

    print(f"  ulaşılabilirlik kısıtı : ≥ %{ULASILABILIRLIK_TABANI:.0f} "
          f"(MAC sonrası bağ tanımı)")
    elenen = [g for g, _ in egri if ulasim[g] < ULASILABILIRLIK_TABANI]
    if elenen:
        print(f"  kısıtla ELENEN güçler  : "
              f"{', '.join(f'{g:+.0f} dBm (%{ulasim[g]:.1f})' for g in elenen)}")
    taban, tavan, orta, secim = yeni_olcut(egri, ulasim)
    print(f"  dinamik aralık : [{taban:.4f} · {tavan:.4f}]  →  orta = {orta:.4f}")
    print(f"  ⇒ ÖLÇÜTÜN SEÇTİĞİ GÜÇ: {secim[0]:+.0f} dBm "
          f"(teslim {secim[1]:.4f}, ortadan {abs(secim[1]-orta):.4f} uzakta)")
    if abs(secim[0] - 2.0) < 1e-9:
        print("     ✅ S2 = +2 dBm ile UYUŞUYOR — çalışma noktası değişmiyor.")
    else:
        print(f"     🔴 S2 (+2 dBm) İLE UYUŞMUYOR — karar gözden geçirilmeli.")
    print()
    print("🔴 OKUMA: Bölüm B'nin ölçütü 'sapma gereken çift'i en büyüklüyor.")
    print("   Ama o metrik uçtan uca teslimle MONOTON İLİŞKİLİ DEĞİL: metrik")
    print("   +4/+6 dBm'de tepe yaparken teslim oranı oralarda zaten %25–36'ya")
    print("   düşmüş oluyor — yani ölçüt, hiçbir protokolün kazanamayacağı bir")
    print("   noktayı işaret ediyor. Bu tam olarak `03` B3'ün 'yalnızca")
    print("   zorlayıcı noktada ölçme' tuzağı ve K-019'un KAÇINMAK İSTEDİĞİ şey.")


def main() -> None:
    yalniz_a = "--a" in sys.argv
    yalniz_b = "--b" in sys.argv
    yalniz_c = "--c" in sys.argv
    print()
    print("KURULUM KALİBRASYONU — K-017 ve K-019'un üretici komutu (B-08)")
    print("Tohumlar: AYARLAMA kümesi. Ana deney tohumları (2000–2029) KOŞULMAZ.")
    print()
    tek = yalniz_a or yalniz_b or yalniz_c
    if yalniz_a or not tek:
        bolum_a(cekim=200_000 if "--hizli" not in sys.argv else 20_000)
    if yalniz_b or not tek:
        bolum_b()
    if yalniz_c or not tek:
        bolum_c()


if __name__ == "__main__":
    from dogrulama.olcum import kayit
    with kayit("kurulum_kalibrasyonu"):
        main()
