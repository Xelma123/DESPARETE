"""
PDR TAVANI — saldırı yokken ağ ne kadar teslim EDEBİLİR?

🔒 REFERANS DÜNYADA (Faz 4.5, K-219): ESKİ dünyanın aleti — çekirdek hücreleri
eski dünyanındır. Referansta kâhin tavanının yerini U1'in kâhin sütunu tuttu
(statik 0,99–1,00 · hareketli 0,84–0,98; `aodv_uygunluk.py`, K-217).

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/pdr_tavani.py

🔴 NEDEN BU ÖLÇÜM VAR
=====================
Adım 9'un kapanış koşularında PDR %10–30 çıktı. Beklenti (öğrenci, 5 Eylül
2026): *"saldırı yokken %95–100; harp altında ilk şokta %50 altı, mesh tepki
verince %70–80."* Aradaki fark iki şeyden BİRİ olabilir:

    (a) simülatörde bir kusur       → düzeltilmeli
    (b) koşum protokollerinin aptallığı → beklenen, sorun değil

İkisini ayıran tek şey, YÖNLENDİRMEYİ MÜKEMMEL yapan bir kolla ölçmektir.

🔴 "TAVAN" SÖZCÜĞÜ 5 EYLÜL 2026'DA HAK EDİLDİ — ÖNCESİNDE DEĞİLDİ
==================================================================
Bu dosya eskiden yalnız `EnKisaYolKahin` ile koşuyordu ve ona "tavan"
diyordu. **Değildi.** O kâhin en az ATLAMA ile yönlendirir; en az atlama ise
en uzun — yani en kötü — bağı seçer. Yani ölçtüğü sayı, ölçütün kendi
bedelini içeriyordu. Ölçüldü: statik kolda üç tohumda PDR 1,000 · 0,832 ·
0,708 — mükemmel topoloji bilgisiyle bile. Ayrıntı K-096.

Artık İKİ kâhin koşuyor ve aradaki fark ÖLÇÜLÜYOR:

    en_guvenilir_kahin − en_kisa_yol_kahin  =  atlama sayısı ölçütünün bedeli
    en_kisa_yol_kahin  − gerçek protokol    =  protokolün körlüğünün bedeli

Bugüne kadar bu iki bedel tek bir sayıya karışmıştı. Karıştırıcı gücü
`en_guvenilir_kahin` kolunda kalibre edilir; böylece çalışma noktası hiçbir
protokolün ölçütüne borçlu olmaz.

🔴 BU BİR PROTOKOL DEĞİLDİR — `protokoller/` ALTINDA DEĞİL
==========================================================
Kâhinler gerçek kanalı görür: konumları, gölgelemeyi, her bağın başarı
olasılığını. Hiçbir gerçek protokol bunu bilemez. Bu yüzden `protokoller/`
paketine KONULMADI — oraya konsaydı içe aktarma grafiği testi haklı olarak
patlardı ve daha kötüsü, bir gün yanlışlıkla taban çizgisi diye
raporlanabilirdi. Burası `kalibrasyon/`: ölçüm aleti. Kâhinlerin kendisi
`kalibrasyon/kahin.py`dedir.

🔴 "TAVAN" SÖZCÜĞÜ İKİNCİ KEZ DARALTILDI — 9 Eylül 2026
=======================================================
5 Eylül'de `EnKisaYolKahin` "tavan" olmaktan çıkarılmıştı (ölçütün kendi
bedeli sayının içindeydi, K-096). Şimdi aynı daraltma `EnGuvenilirKahin`
için de gerekli oldu ve sebebi FARKLI: **ETX beklenen İLETİM sayısını
küçültür, TESLİMİ değil.** Yeniden deneme sınırı sonlu (5 deneme) olduğu
için ikisi ayrışır.

Ölçüldü (`python -u kalibrasyon/bag_kumesi.py d`, `statik-surekli`,
15 tohum): bağ eşiği 0,99 iken `EnKisaYolKahin` 15 tohumun **6'sında**
`EnGuvenilirKahin`i GEÇİYOR; bugünkü eşikte (0,90) 2'sinde.

🔒 Kol ORTALAMASINDA `EnGuvenilirKahin` her eşikte önde — yani "daha kötü"
değil, **ÜST SINIR DEĞİL**. Bu dosyanın ürettiği sayılar bir tavan değil,
**bir kâhinin performansıdır**. Faz 3'te bir protokolün bu sayıyı geçmesi
kusur işareti DEĞİLDİR ve öyle okunmamalıdır.

⚠️ TAVAN "ULAŞILABİLİR" DEMEK DEĞİL
===================================
Kâhin, yönlendirmeyi mükemmel yapar ama MAC'i, kanalı, kuyruğu ve TTL'i
değiştirmez. Yani ölçtüğü şey: *"yönlendirme hiç hata yapmasaydı bu ağ,
bu yükte, bu fizikte ne teslim ederdi."* Gerçek protokoller bunun ALTINDA
kalır. Tavan %95'in çok altındaysa sorun yönlendirmede DEĞİLDİR.
"""

from __future__ import annotations

import statistics as ist
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import dogrula  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import korunum_bolumu  # noqa: E402
from sim2.olcum.metrikler import metrik_sozlugu  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from kalibrasyon.kahin import (EnGuvenilirKahin,  # noqa: E402
                               EnKisaYolKahin, KanalGrafigi)

KAHINLER = {EnGuvenilirKahin.ad: EnGuvenilirKahin,
            EnKisaYolKahin.ad: EnKisaYolKahin}


# ==========================================================================
def kos(senaryo="statik-yok", tohum=1000, bitis=120.0,
        kahin=EnGuvenilirKahin, **ek):
    """Bir kâhin kolu koşar. Varsayılan kâhin GÜVENİLİR olandır — tavan odur."""
    # 🔴 `setdefault("karistirici_guc_override_dbm", 0.0)` KALDIRILDI.
    # İki sebeple ölüydü: (a) bu dosyadaki üç bölümün üçü de yalnız `-yok`
    # senaryosu koşuyor, yani satır hiç ateşlenmiyordu; (b) güç 8 Eylül'de
    # ÖLÇÜLDÜ (−15,0 dBm) ve o satır ateşlenseydi kalibre edilmiş noktayı
    # 15 dB ezerdi. Ölü bir varsayılan, bir gün canlanan bir varsayılandır.
    # 🔒 Pencere `bitis`ten TÜRER ama çağıran AÇIKÇA ezebilir. Ezilemezse
    # karıştırıcının açılma anını pencerenin dışında tutmak imkânsız olurdu:
    # oranlar sabitken pencere her zaman açılma anının iki yanına düşer ve
    # okunan PDR iki evrenin ortalaması olur.
    pencere = {"isinma_s": 0.1 * bitis, "olcum_bitis_s": 0.85 * bitis,
               "kosu_bitis_s": bitis}
    pencere.update({ad: ek.pop(ad) for ad in list(ek) if ad in pencere})
    konfig = DS.konfig(kol="tavan", senaryo=senaryo, tohum=tohum,
                    **pencere, **ek)
    kur = kurulum_yap(konfig)
    grafik = KanalGrafigi(kur)
    t0 = time.perf_counter()
    kosu = Kosu(kur, lambda i: kahin(i, grafik))
    kosu.kostur()
    sure = time.perf_counter() - t0
    k = korunum_bolumu(kur, kosu.dugumler)
    # 🔒 PDR sayaclardan DEGIL metrik sozlugunden okunur:
    # tek tanim orada (kohort doguma gore).
    s = metrik_sozlugu(kur.sayaclar.disa_ver(),
                       kur.paket_defteri, kur.rota_defteri)
    return kur, k, s, sure


def satir(etiket, k, s, sure):
    pdr = (s["pdr"] or 0.0)
    psr = (s["psr"] or 0.0)
    d = k["dusen"]
    print(f"  {etiket:<34} {pdr:>6.3f} {psr:>6.3f} {k['uretilen']:>7} "
          f"{k['teslim']:>7} {d['ttl']:>6} {d['hedef_yok']:>8} "
          f"{d['iletim_basarisiz']:>8} {d['kuyruk_tasmasi']:>8} {sure:>7.1f}")


def basliklar():
    print(f"  {'kol':<34} {'pdr':>6} {'psr':>6} {'uretilen':>7} "
          f"{'teslim':>7} {'ttl':>6} {'hedefyok':>8} {'iletimX':>8} "
          f"{'kuyrukX':>8} {'sure_s':>7}")


def _bolum(baslik: str) -> None:
    print()
    print("=" * 116)
    print(baslik)
    print("=" * 116)


def tavan() -> None:
    _bolum("1 - TAVAN  (en guvenilir kahin, KARISTIRICI YOK)")
    basliklar()
    for senaryo, tohumlar in (("statik-yok", (1000, 1001, 1002)),
                              ("bagimsiz-yok", (1000, 1001))):
        for tohum in tohumlar:
            _, k, s, sure = kos(senaryo, tohum)
            satir(f"{senaryo} tohum={tohum}", k, s, sure)


def olcut_bedeli() -> None:
    """🔴 Atlama sayısı ölçütünün bedeli — iki kâhin, AYNI tohum, AYNI dünya."""
    _bolum("2 - OLCUTUN BEDELI  (ayni tohumda iki kahin)")
    basliklar()
    for senaryo in ("statik-yok", "bagimsiz-yok"):
        for tohum in (1000, 1001):
            for ad, sinif in KAHINLER.items():
                _, k, s, sure = kos(senaryo, tohum, kahin=sinif)
                satir(f"{senaryo} t={tohum} {ad}", k, s, sure)
    print("\n  🔒 Ayni tohumda iki kol AYNI dunyayi, AYNI trafigi, AYNI kanali")
    print("     gorur (hash tabanli akislar). Aradaki fark yalnizca OLCUT.")


def yuk_taramasi() -> None:
    _bolum("3 - YUK TARAMASI  (PDR yuke mi takiliyor? en guvenilir kahin)")
    basliklar()
    for ad, ek in (("10 akis x 4.0 pkt/s", {}),
                   ("10 akis x 2.0 pkt/s", dict(akis_paket_hizi_hz=2.0)),
                   ("10 akis x 1.0 pkt/s", dict(akis_paket_hizi_hz=1.0)),
                   ("5 akis x 4.0 pkt/s", dict(akis_sayisi=5)),
                   ("2 akis x 4.0 pkt/s", dict(akis_sayisi=2)),
                   ("1 akis x 4.0 pkt/s", dict(akis_sayisi=1))):
        _, k, s, sure = kos("statik-yok", 1000, **ek)
        satir(ad, k, s, sure)


def karistirilmis_tavan(tohum_sayisi: int = 3) -> None:
    """🔴 KARIŞTIRMA ALTINDA TAVAN — bu sayının ÜRETİCİSİ yoktu.

    *"Karıştırma altında ulaşılabilir tavan %95,9"* üç belgede kesin bir
    sayı gibi duruyordu (`karistirici_gucu.py` başlığı, K-103, `DEVIR.md`)
    ama onu üreten bir betik **yoktu**: bu dosyanın üç bölümü de yalnız
    `-yok` kolunu koşuyor. Yani kural 7 *(her sayı üretici komutunu taşır)*
    çiğnenmişti. Bölüm burada, sayının kendisi için.

    🔒 ÖLÇÜM PENCERESİ TAMAMEN KARIŞTIRILMIŞ EVREDEDİR. Varsayılan kurulumda
    karıştırıcı 150 s'de açılır ve pencere [50; 320) — yani pencerenin üçte
    biri TEMİZ. O pencerede okunan PDR bir "karıştırma altındaki tavan"
    değil, iki evrenin ortalamasıdır. Burada açılma anı 25 s'ye çekilir:
    ısınma (50 s) varsayılanında kalır, pencere [50; 170) ve karıştırıcı
    pencere açılmadan 25 s önce zaten devrededir.

    🔒 KOL EŞLEŞTİRİLMİŞTİR: temiz ve karıştırılmış kol AYNI tohumu, AYNI
    pencereyi ve AYNI kâhini kullanır. Hash tabanlı akışlar sayesinde iki
    kol aynı dünyayı ve aynı trafiği görür; tek fark karıştırıcıdır.

    ⚠️ VARSAYILAN 3 TOHUM — bu bir ÇAPRAZ KONTROLDÜR, SONUÇ SATIRI DEĞİL.
    Kural 8 sonuç için ≥30 tohum istiyor. Tohum sayısı komut satırından
    verilir: `python kalibrasyon/pdr_tavani.py 4x30`.
    """
    _bolum(f"4 - KARISTIRMA ALTINDA TAVAN  ({tohum_sayisi} tohum, "
           f"pencere TAMAMEN karistirilmis)")
    basliklar()
    ek = dict(karistirici_baslangic_s=25.0, isinma_s=50.0,
              olcum_bitis_s=170.0, kosu_bitis_s=200.0)
    # 🔴 KAPI: pencere TAMAMEN karıştırılmış evrede olmalı. Bu satır olmasa
    # bir gün biri `bitis`i değiştirir, pencere açılma anının iki yanına
    # düşer ve "karıştırma altındaki tavan" sessizce iki evrenin ortalaması
    # olur — tam olarak bu bölümün düzeltmek için var olduğu hata.
    dogrula(ek["karistirici_baslangic_s"] <= ek["isinma_s"],
            "olcum penceresi tamamen karistirilmis evrede olmali: "
            f"acilma {ek['karistirici_baslangic_s']} s, "
            f"pencere basi {ek['isinma_s']} s")
    pdrler: dict[str, list[float]] = {"statik-yok": [], "statik-surekli": []}
    for tohum in range(1000, 1000 + tohum_sayisi):
        for senaryo in ("statik-yok", "statik-surekli"):
            _, k, s, sure = kos(senaryo, tohum, bitis=200.0, **ek)
            satir(f"{senaryo} tohum={tohum}", k, s, sure)
            pdrler[senaryo].append(s["pdr"] or 0.0)
    print()
    for senaryo, degerler in pdrler.items():
        print(f"  {senaryo:<16} PDR ort {ist.mean(degerler):.3f}  "
              f"tohumlar: {', '.join(f'{d:.3f}' for d in degerler)}")
    if tohum_sayisi < 30:
        print(f"\n  ⚠️ {tohum_sayisi} TOHUM — CAPRAZ KONTROL, SONUC DEGIL.")
        print("     Kural 8 sonuc icin >=30 tohum istiyor. Tohumlar arasi")
        print("     yayilim buyuk oldugu icin ortalama tek basina okunamaz.")


if __name__ == "__main__":
    DS.secimi_oku()                         # Faz 4 (K-183): --dunya
    print(f"  DUNYA: {DS.secili()}")
    BOLUMLER = {"1": tavan, "2": olcut_bedeli, "3": yuk_taramasi,
                "4": karistirilmis_tavan}
    secim = sys.argv[1:] or list(BOLUMLER)
    for ham in secim:
        # `4x30` = bolum 4, 30 tohumla. Tohum sayisi ELLE DEGIL komuttan.
        bolum_adi, _, adet = ham.partition("x")
        if bolum_adi not in BOLUMLER:
            raise SystemExit(f"bilinmeyen bolum: {bolum_adi!r}")
        if adet:
            BOLUMLER[bolum_adi](int(adet))
        else:
            BOLUMLER[bolum_adi]()
