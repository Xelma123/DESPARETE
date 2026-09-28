"""
Metrikler — literatürün asgari kümesinin YEDİSİ de bir koşudan.

Eski simülatör 7 metrikten yalnız **2**'sini üretiyordu. Eksik olanlar:
PSR · p95 gecikme · NRL · üç kopma sayacı · Δ · COR. Bu modül yedisini de
tek koşudan çıkarır.

🔒 SAYAÇLARDAN TÜRETİLENLER BURADA YENİDEN HESAPLANMAZ
======================================================
`pdr`, `psr`, `nrl_*`, `cor`, `algilama_duyarliligi` — hepsi
`cekirdek/sayaclar.py`nin `Turev` kayıtlarıdır ve pencere ikizleriyle
birlikte oradan gelir. Burada yalnızca **ham listeler gerektiren** metrikler
hesaplanır: gecikme yüzdelikleri, IPDV ve Δ. Bir toplamdan yüzdelik
çıkarılamaz; tek tek gecikmeler gerekir.

Sayaçlardaki bir oranı burada yeniden hesaplamak kusur 6'nın ta kendisi
olurdu — iki hesap sessizce ayrışır.

⚠️ YÜZDELİK GÖVDESİ İKİ YERDE OLACAK — ve bu BİLİNÇLİ
=====================================================
`analiz/` katmanı simülatörden hiçbir şey içe aktaramaz (JSONL üzerinde
çalışır), dolayısıyla yüzdelik hesabının ikinci bir gerçeklemesi orada
olacak. Yedekliliği DENETLENEBİLİR kılan şey, ham listenin sonuç satırında
bulunmasıdır: `analiz/`in doğrulama kapılarından biri *"satırdaki
yüzdelikler ham listeden yeniden üretilebiliyor mu"* olacak. Ham liste
olmasaydı iki gerçekleme sessizce ayrışırdı.

🔴 BOŞ ÖRNEKLEMDE `None`, SIFIR DEĞİL
=====================================
Hiç teslim yoksa gecikme yüzdeliği YOKTUR. `0.0` döndürmek ölçülmemiş bir
hücreyi ortalamaya sokmak olur ve kollar arası karşılaştırmayı yanlı yapar.
"""

from __future__ import annotations

import math
import statistics as ist
from typing import Mapping, Sequence

from sim2.cekirdek.degismezler import dogrula
from sim2.olcum.evre import evre_sozlugu
from sim2.olcum.paket_defteri import PaketDefteri
from sim2.olcum.rota_olaylari import RotaDefteri

__all__ = ["YUZDELIKLER", "yuzdelik", "ozet_istatistik", "metrik_sozlugu"]

# Sonuç şemasının istediği yüzdelikler. Kapalı liste: sonradan eklemek
# şemayı değiştirir ve eski satırları karşılaştırılamaz yapar.
YUZDELIKLER: tuple[int, ...] = (50, 95, 99)


def yuzdelik(ornekler: Sequence[float], p: int) -> float | None:
    """`p`. yüzdelik — DOĞRUSAL ARADEĞERLEMELİ, gövdesi DONDURULMUŞ.

    🔒 Tanım açıkça yazılır çünkü literatürde tek bir "p95" tanımı yoktur;
    en yakın-sıra ile aradeğerlemeli tanım küçük örneklemlerde gözle görülür
    biçimde ayrışır. `analiz/`in ikinci gerçeklemesi BU tanımı kullanmak
    zorundadır ve ham listeyle karşılaştırılarak denetlenir.

        sirali = sorted(ornekler)
        k      = (n − 1) · p/100
        sonuc  = sirali[⌊k⌋] + (k − ⌊k⌋) · (sirali[⌈k⌉] − sirali[⌊k⌋])

    Boş örneklemde `None` — sıfır DEĞİL.
    """
    dogrula(0 <= p <= 100, "yüzdelik [0, 100] aralığında olmalı")
    if not ornekler:
        return None
    sirali = sorted(ornekler)
    if len(sirali) == 1:
        return sirali[0]
    k = (len(sirali) - 1) * (p / 100.0)
    alt = math.floor(k)
    ust = math.ceil(k)
    if alt == ust:
        return sirali[alt]
    return sirali[alt] + (k - alt) * (sirali[ust] - sirali[alt])


def ozet_istatistik(ornekler: Sequence[float], onek: str
                    ) -> dict[str, float | None]:
    """`ort` + istenen yüzdelikler. Boş örneklemde hepsi `None`."""
    if not ornekler:
        return {f"{onek}_ort_s": None,
                **{f"{onek}_p{p}_s": None for p in YUZDELIKLER}}
    return {f"{onek}_ort_s": ist.mean(ornekler),
            **{f"{onek}_p{p}_s": yuzdelik(ornekler, p) for p in YUZDELIKLER}}


def metrik_sozlugu(sayaclar: dict[str, float | None],
                   paket_defteri: PaketDefteri,
                   rota_defteri: RotaDefteri,
                   acilma_s: float | None = None,
                   akis_siniflari: Mapping[int, str] | None = None,
                   enerji_j: Sequence[float] | None = None
                   ) -> dict[str, object]:
    """Sonuç satırının `metrikler` bölümü.

    🔒 `sayaclar` OLDUĞU GİBİ geçer: `pdr`, `psr`, `nrl_*`, `cor`,
    `algilama_duyarliligi` ve pencere ikizleri kayıt defterinden gelir.
    Buraya eklenen tek şey ham liste gerektiren metriklerdir.

    🔒 `acilma_s` KARIŞTIRICININ AÇILMA ANIDIR ve verilirse evre metrikleri
    (şok · toparlanma · tespit) eklenir. Bir `Konfig` değil bir SAYI alıyor:
    `olcum/` katmanının `yapilandirma/`ya bağlanması, ölçüm defterlerini
    konfigürasyona bağımlı kılardı.

    ⚠️ Verilmezse evre metrikleri YOKTUR — `None` DEĞİL, hiç yok. İkisi ayrı
    şeydir: *"ölçülmedi"* ile *"ölçüldü ve tanımsız çıktı"*.

    🔒 `akis_siniflari` (K-171) aynı gerekçeyle bir HARİTA alır, geçidi
    değil: verilirse sınıf başına `pdr_<sınıf>` ve pencere ikizi eklenir,
    verilmezse bu alanlar hiç yoktur.
    """
    cikti: dict[str, object] = dict(sayaclar)

    # --- PDR: TEK TANIM, kohort DOĞUMA göre --------------------------
    # 🔒 Sayaç kayıt defterinden bilerek çıkarıldı (8 Eylül 2026). Orada
    # pencere ikizi fark alarak türüyordu ve pay ile payda FARKLI kümelerden
    # geliyordu. Burada ikisi de aynı kümeden: pencerede DOĞAN paketler.
    # Pencerede doğup pencere kapandıktan sonra teslim edilen bir paket
    # teslim SAYILIR — boşalma penceresi tam bunun için var.
    cikti["pdr"] = (paket_defteri.teslim / paket_defteri.uretilen
                    if paket_defteri.uretilen else None)
    cikti["pdr_pencere"] = (
        paket_defteri.pencerede_teslim / paket_defteri.pencerede_uretilen
        if paket_defteri.pencerede_uretilen else None)
    # --- görev teslim oranı (KR-E, K-182): payda PLANLANAN talep -------
    # 🔒 Birincil metrik PDR'dir ve kohortu doğumda iki ucu yaşayan
    # paketlerdir; bu İKİNCİL oran düğüm kaybının göreve bedelini okur
    # (ölü kaynağın üretemediği ve ölü hedefe doğan paketler paydada).
    # Kayıp yokken PDR'ye birebir eşittir.
    for yalniz_pencere, sonek in ((False, ""), (True, "_pencere")):
        plan = paket_defteri.planlanan(yalniz_pencere)
        teslim = (paket_defteri.pencerede_teslim if yalniz_pencere
                  else paket_defteri.teslim)
        cikti[f"gorev_teslim_orani{sonek}"] = teslim / plan if plan else None
    # --- PDR yön ayrımı: aynı tanım, sınıf başına (K-171) --------------
    if akis_siniflari is not None:
        for yalniz_pencere, sonek in ((False, ""), (True, "_pencere")):
            sayim = paket_defteri.sinif_sayimi(akis_siniflari, yalniz_pencere)
            for sinif in sorted(sayim):
                uretilen, teslim = sayim[sinif]
                cikti[f"pdr_{sinif}{sonek}"] = (teslim / uretilen
                                                if uretilen else None)

    # --- enerji (`v2/15` C3, K-180): ağ toplamı ve düğüm başına dağılım --
    if enerji_j is not None:
        cikti["enerji_toplam_j"] = math.fsum(enerji_j)
        cikti["enerji_dugum_p50_j"] = yuzdelik(enerji_j, 50)
        cikti["enerji_dugum_p95_j"] = yuzdelik(enerji_j, 95)
        cikti["enerji_dugum_maks_j"] = max(enerji_j) if enerji_j else None

    # --- gecikme ve IPDV: tam koşu ve pencere ikizi -------------------
    for yalniz_pencere, sonek in ((False, ""), (True, "_pencere")):
        gecikme = paket_defteri.gecikmeler(yalniz_pencere)
        for ad, deger in ozet_istatistik(gecikme, "gecikme").items():
            cikti[ad + sonek] = deger
        ipdv = paket_defteri.ipdv(yalniz_pencere)
        cikti[f"ipdv_ort_s{sonek}"] = ist.mean(ipdv) if ipdv else None
        cikti[f"ipdv_p95_s{sonek}"] = yuzdelik(ipdv, 95)
        cikti[f"teslim_sayisi{sonek}"] = (paket_defteri.pencerede_teslim
                                          if yalniz_pencere
                                          else paket_defteri.teslim)

    # --- rota olayları: Δ, COR, duyarlılık ----------------------------
    delta = rota_defteri.delta_ler()
    # 🔴 Protokol hiç beyan etmiyorsa Δ `None` — 0 DEĞİL.
    for ad, deger in ozet_istatistik(delta, "rota_kurtarma_delta").items():
        cikti[ad] = deger
    cikti["kopma_algilanan_olcum"] = rota_defteri.kopma_algilanan
    cikti["kopma_rota_gecersiz_olcum"] = rota_defteri.kopma_rota_gecersiz
    cikti["kopma_fiziksel_olcum"] = rota_defteri.kopma_fiziksel().rapora()
    cikti["rota_kurtarildi_olcum"] = rota_defteri.rota_kurtarildi
    cikti["rota_etkilendi_olcum"] = rota_defteri.rota_etkilendi
    cikti["kapanmamis_kopma"] = rota_defteri.kapanmamis_kopma()
    cikti["algilama_duyarliligi_olcum"] = rota_defteri.algilama_duyarliligi()
    cikti["cor_olcum"] = rota_defteri.cor()
    # 🔴 RİSK 3'ÜN ETİKETİ — hiç beyan etmeyen kol burada işaretlenir.
    cikti["beyan_etmiyor"] = rota_defteri.beyan_etmiyor

    # --- evre metrikleri: şok · toparlanma · tespit (adım ⑤) -----------
    # 🔒 Evre sınırları ölçüm penceresinden ve açılma anından TÜRER.
    # Gecikme p99 buraya G4 kapısı için geçer: doğum-anına-göre kovalamanın
    # bulanıklığı `p99 / ızgara adımı`dır ve her kolda raporlanır.
    bas_s, bitis_s = (paket_defteri.pencere_bas_s,
                      paket_defteri.pencere_bitis_s)
    if acilma_s is None:
        pass
    elif bas_s <= acilma_s < bitis_s:
        cikti.update(evre_sozlugu(
            paket_defteri, rota_defteri, bas_s=bas_s, acilma_s=acilma_s,
            bitis_s=bitis_s,
            gecikme_p99_s=cikti.get("gecikme_p99_s_pencere")))
    else:
        # 🔴 SESSİZ ATLAMA YOK. Açılma anı pencerenin dışındaysa evreler
        # TANIMSIZDIR — ama bunu yazmadan atlamak, 8 Eylül 2026'da üç
        # kalibrasyon tablosunu boşaltan hatanın aynısı olurdu: ölçülmemiş
        # bir şey, ölçülmüş gibi görünür. Satır sebebini KENDİ söyler.
        cikti["evre_metrikleri_yok"] = (
            f"acilma ani {acilma_s} olcum penceresinin "
            f"[{bas_s}; {bitis_s}) disinda")
    return cikti
