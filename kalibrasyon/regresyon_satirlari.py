"""
REGRESYON SATIRLARI — bir `sim2` değişikliği ölçülmüş sonuçları değiştirdi mi?

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/regresyon_satirlari.py uret <etiket>
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/regresyon_satirlari.py karsilastir <a> <b> [--izin onek,onek] [--yeni onek,onek] [--sifir alan,alan] [--degisen vaka_onek,...]

Bağlam: `v2/07-SIMULATOR-TASARIMI.md` §18 Y0 · K-114.

🔴 NEDEN BU ALET VAR
====================
K-112 kontrol düzlemini eklerken 35 sonuç satırını "önce/sonra" alan alan
karşılaştırdı ve birebir aynı buldu — ama karşılaştırma betiği geçici bir
dizinde kaldı, depoya girmedi. Yani "35/35 birebir" iddiası bugün yeniden
üretilemiyor. Bu alet onun depodaki hâlidir ve Aşama 1'deki her `sim2`
değişikliğinden önce ve sonra koşar.

🔒 NE YAPAR
===========
  · `uret <etiket>` — sabit bir vaka matrisini koşar ve her koşunun TAM
    sonuç satırını `ciktilar2/regresyon/<etiket>.jsonl`e yazar (satır başına
    `fsync`). Dosya zaten varsa DURUR: satırlar üst üste eklenirse çoğalır.
  · `karsilastir <a> <b>` — satırları vaka kimliğiyle (`not_`) eşler, bütün
    bölümleri alan alan karşılaştırır ve farkları üç sınıfa ayırır:
        her koşuda değişen   → çalışma kimliği, zaman damgası
        kaynak koduna bağlı  → araç özeti ve onu içeren koşu kimliği
        BULGU                → geri kalan her fark
    `--izin` ile önceden ilan edilmiş, BİLEREK değişen alan önekleri verilir
    (ör. tanımı değişen `metrikler.psr`). İzinli fark ayrı basılır, gizlenmez.
    `--yeni` ile matrise BİLEREK eklenmiş vakaların kimlik önekleri verilir;
    yalnız sonraki dosyada bulunmaları bulgu sayılmaz ama ayrı basılırlar.
    `--sifir` ile, iki dosyada da bulunan HER vakada sonraki dosyada VAR ve
    SIFIR olması ilan edilmiş alanlar verilir (desen `--izin`inkiyle aynı).
    🔴 NEDEN (23 Eylül 2026, K-151 kapanışı): izinli bir alanın farkı
    basılır ama DEĞERİ basılmaz — *"yeni sayaç 44 vakanın hepsinde 0"* gibi
    bir beklenti bu yüzden ya elle okunuyordu ya hiç sınanmıyordu. Artık
    çıkış koduna bağlı.
    `--degisen` ile davranışı BİLEREK değişen vakaların kimlik önekleri
    verilir (ör. bir protokolün varsayılan profili değişti, K-173): o vaka
    alan karşılaştırmasından çıkar, farklı alan sayısıyla ayrı basılır ve
    GEÇERLİ olmak zorundadır. Alan izni bütün vakalara uygulandığı için o
    vakanın her metriğine izin vermek öteki vakaların farkını gizlerdi.

🔒 VAKA MATRİSİ — hangi yolu neden sınıyor
===========================================
  · 3 statik kol × en yakın kimlik, kısa pencere — çok atlama, döngü, TTL
  · 12 hareketli kol × doğrudan komşu, kısa — bağımsız ve görev kollarının
    bütün karıştırıcı kolları (süre gerekçesi `vakalar()` içinde)
  · formasyon × 2, kısa — tek atlama ve kâhin grafiği (Y6; kimliği `h-` ile
    başlar, çapraz çarpıma girmez — gerekçe `vakalar()` içinde)
  · tehdit aileleri × 5, kısa — cephe hattı · derin sızma · hedef koruma ·
    hava eşlik (Y5b; kimliği aile adıyla biter, hava eşlik ayrıca kâhinle)
  · 6 karıştırıcı × doğrudan komşu, kısa — tek atlama, kuyruk taşması,
    hedef yok dalı
  · 3 mobilite kolu × iki kâhin, kısa — kâhin grafiği yolu
  · yüklü beacon × 2, kısa — beacon yükünün kanalda ödenmesi (K-111)
  · kontrol düzlemi sınav protokolü × 2, kısa — K-112 mekanizmasının her yolu
  · yere toplama × 2, kısa — geçit, telemetri ve komut akışları, kayıp yeri
    (Y4; kimliği `-yere_toplama` ile biter)
  · başlıklı ve sonuç bildirimli sınav protokolü × 1, kısa — protokolün veri
    başlığının çerçeveyi uzatması ve ek yüke sayılması, her unicast sonucunun
    bildirimi (K-151 Y1 · Y2; kimliği `j-` ile başlar, 23 Eylül 2026'da
    eklendi — o güne kadar iki yol da matriste YOKTU)
  · 4 tam uzunluk — evre metrikleri, ham bölüm, tam pencere. Süreye göre
    seçildi: statik kolda ETX kâhini, hareketli kollarda doğrudan komşu
    (ölçülen süreler ve gerekçe `vakalar()` içinde)
  · 🔒 REFERANS DÜNYA `u-` (30 Eylül 2026, Faz 4 kapanışı): deneylerin
    dünyasında gerçek protokoller — birincil hücre × dört protokol + ETX
    kâhini · dört karıştırıcı sınıfı · yer karıştırıcısı ailesi · düğüm kaybı
    · eşler arası · karıştırıcısız DESPARETE; kısa pencere. Anahtarlar
    addan değil `REFERANS_VAKALARI` tablosundan (`_kos`). Faz 4b'nin
    rakipleri (K-236): JarmRout ve OLSRv2 birincil hücrede, JarmRout eşler
    arası hareketli kolda (keşif, RERR, kopya, kaynak rotası), OLSRv2 düğüm
    kaybında (komşu ve topoloji demetlerinin dolması). Üçüncü rakip Babel
    (K-242 · K-244): birincil hücrede ve düğüm kaybında

Vaka başına duvar saati basılır ama satıra yazılmaz; sonraki koşumun bandı
bu sayılardan verilir.

⚠️ SINIR: bu bir KAPI değil, bir karşılaştırma aletidir. "Birebir aynı"
yalnız bu matrisin yolları için geçerlidir; matrisin dokunmadığı bir yol
değişmiş olabilir. Yeni bir mekanizma eklendiğinde matrise vakası da eklenir.
"""

from __future__ import annotations

import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
for _yol in (KOK, KOK / "tests2"):
    if str(_yol) not in sys.path:
        sys.path.insert(0, str(_yol))

from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import SatirYazici, sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from sim2.yapilandirma.senaryolar import (KARISTIRICI_SINIFLARI,  # noqa: E402
                                          MOBILITE_KOLLARI, SENARYOLAR,
                                          TEHDIT_SENARYOLARI)

DIZIN = KOK / "ciktilar2" / "regresyon"

# Her koşuda değişmesi GEREKEN alanlar — fark değil, tanım.
HER_KOSUDA_DEGISEN = ("kimlik.calisma_kimligi", "kimlik.zaman_damgasi_utc")
# Kaynak kodunun özetine bağlı alanlar — kod değişince değişmeleri GEREKİR.
# 🔒 `protokol_hash` `protokoller/` paketinin özetini taşır (K-171): herhangi
# bir protokol dosyası değişince bütün vakalarda değişmesi GEREKİR.
KOD_KIMLIGI = ("kimlik.arac_hash", "kimlik.kosu_kimligi",
               "kimlik.protokol_hash")

# 🔴 ÜÇÜNCÜ BİR SINIF VAR AMA OTOMATİK DEĞİL — 15 Eylül 2026'da öğrenildi.
# `teshis.koken_kovalari.*` her satırda taşınır ve KÖKEN DEFTERİ her
# değiştiğinde 44 vakada birden oynar. O gün beklenen farklar ilan edilirken
# *"köken metin eklemeleri yalnız `arac_hash`e girer"* denmişti — YANLIŞ; ve
# karşılaştırma beyanı aştı (K-127).
#
# 🔒 BU SINIF BİLEREK OTOMATİK DEĞİL. Otomatik izin verilseydi bir
# parametrenin sessizce TEDAVI'den DUYARSIZ'a kayması da görünmez olurdu —
# oysa görünmesi gereken tam olarak odur. Doğru kullanım: taban alındığından
# beri köken defteri değiştiyse, farkı ilan ederken HANGİ kayıtların
# değiştiği tek tek yazılır ve `--izin teshis.koken_kovalari` ile geçilir.


# 🔒 REFERANS DÜNYA VAKALARI — 30 Eylül 2026 (Faz 4 kapanışı, denetim B6).
# O güne kadar referans dünyada yalnız üç `r-` vakası vardı; dört protokol
# yalnız ESKİ dünyada (`k-`) sınanıyordu. Kimlik → (senaryo, protokol, tohum,
# `referans_2026`e ek alanlar). Hepsi kısa pencere; tohum 1003 birincil
# hücrenin geliştirme tohumu (K-200), öteki vakalarda 1010.
# OLSR ve AOMDV vakaları Faz 4'ün rakipleridir (K-229'dan beri rakip değil);
# donmuş kodlarının regresyonu için matriste kalır.
_BIRINCIL = {"tehdit_senaryosu": "derin_sizma", "trafik_deseni": "yere_toplama"}
_YT = {"trafik_deseni": "yere_toplama"}
REFERANS_VAKALARI: dict[str, tuple[str, str, int, dict]] = {
    **{f"u-birincil-{p}": ("formasyon-surekli", p, 1003, _BIRINCIL)
       for p in ("aodv", "olsr", "aomdv", "desparete", "en_guvenilir_kahin")},
    **{f"u-statik-{j}-aodv": (f"statik-{j}", "aodv", 1010, _YT)
       for j in ("surekli_darbeli", "reaktif", "aldatici", "taramali")},
    "u-statik-surekli-aodv-cephe_hatti": (
        "statik-surekli", "aodv", 1010,
        {"tehdit_senaryosu": "cephe_hatti", **_YT}),
    "u-bagimsiz-surekli-olsr-dugum_kaybi": (
        "bagimsiz-surekli", "olsr", 1010,
        {"kayip_dugum_sayisi": 5, "kayip_bas_s": 15.0, "kayip_bitis_s": 35.0,
         **_YT}),
    "u-gorev-surekli-aomdv-esler_arasi": (
        "gorev-surekli", "aomdv", 1010, {"trafik_deseni": "esler_arasi"}),
    "u-statik-yok-desparete": ("statik-yok", "desparete", 1010, _YT),
    # Faz 4b (K-233 · K-235 · K-236): yeni rakipler.
    **{f"u-birincil-{p}": ("formasyon-surekli", p, 1003, _BIRINCIL)
       for p in ("jarmrout", "olsrv2")},
    "u-bagimsiz-surekli-jarmrout-esler_arasi": (
        "bagimsiz-surekli", "jarmrout", 1010,
        {"trafik_deseni": "esler_arasi"}),
    "u-bagimsiz-surekli-olsrv2-dugum_kaybi": (
        "bagimsiz-surekli", "olsrv2", 1010,
        {"kayip_dugum_sayisi": 5, "kayip_bas_s": 15.0, "kayip_bitis_s": 35.0,
         **_YT}),
    # Üçüncü rakip Babel (K-242 · K-244): birincil hücre; düğüm kaybı
    # hareketli kolda (geri çekme ve yinelemeleri, açlıkta sıra isteği, rota
    # isteği, IHU tutmasının dolması).
    "u-birincil-babel": ("formasyon-surekli", "babel", 1003, _BIRINCIL),
    "u-bagimsiz-surekli-babel-dugum_kaybi": (
        "bagimsiz-surekli", "babel", 1010,
        {"kayip_dugum_sayisi": 5, "kayip_bas_s": 15.0, "kayip_bitis_s": 35.0,
         **_YT}),
    # Denetim 2026-10-08 D-13: kısa pencerede TEMİZ evre boş kalıyor ve
    # çizelgeli evre yolu (M1 · M2 · M4, `pdr_acik` — K-222'nin birincil
    # metriği) regresyonda hiç sınanmıyordu. Bu vaka kendi penceresini taşır:
    # TEMİZ 10–40 s, karıştırıcı 40 s'de açılır, iki açık/sessiz çevrim.
    "u-birincil-evre-en_guvenilir_kahin": (
        "formasyon-surekli", "en_guvenilir_kahin", 1003,
        {**_BIRINCIL, "karistirici_baslangic_s": 40.0, "isinma_s": 10.0,
         "olcum_bitis_s": 100.0, "kosu_bitis_s": 110.0}),
}


# ==========================================================================
def vakalar() -> tuple[tuple[str, str, str, int, bool], ...]:
    """(vaka kimliği, senaryo, protokol, tohum, tam uzunluk mu)."""
    cikti: list[tuple[str, str, str, int, bool]] = []
    # 🔒 DÖNGÜ/TTL YALNIZ ÜÇ STATİK KOLDA — 11 Eylül 2026, ölçüldü.
    # İlk üretimde 18 senaryonun hepsi `en_yakin_kimlik`le koştu ve üretim
    # 32,4 dk sürdü. Bu vakalar toplam sürenin %65'iydi; en uzunu
    # `a-bagimsiz-reaktif` 1330 s (10 işçi 8 fiziksel çekirdekte, süreç başına
    # ~2,1 kat yavaş). Döngü ve TTL dalları mobilite × karıştırıcıdan
    # bağımsızdır. Mobilite × karıştırıcı kolları tek atlamalı `m-`
    # vakalarında, hareketli kolda çok atlama `c-` kâhin vakalarında sınanır.
    for s in ("statik-yok", "statik-surekli", "statik-surekli_darbeli"):
        cikti.append((f"a-{s}-en_yakin_kimlik", s, "en_yakin_kimlik", 1000,
                      False))
    # 🔒 FORMASYON KOLU ÇAPRAZ ÇARPIMA GİRMEZ — 11 Eylül 2026 (Y6).
    # Kol yalnız mobilite yolunu değiştirir; mobilite × karıştırıcı ve kâhin
    # grafiği etkileşimi öteki hareketli kollarda sınanıyor. Tam çarpım 8 vaka
    # (~1 900 işlemci-saniye) ekler ve üretimin üst bandını 30 dk'nın üstüne
    # taşırdı. Kolun kendi yolu aşağıdaki iki `h-` vakasıyla sınanır.
    carpimda = tuple(m for m in MOBILITE_KOLLARI if m != "formasyon")
    for s in sorted(SENARYOLAR):
        if (not s.startswith("statik-")
                and SENARYOLAR[s].mobilite_kolu in carpimda):
            cikti.append((f"m-{s}-dogrudan_komsu", s, "dogrudan_komsu", 1000,
                          False))
    for j in KARISTIRICI_SINIFLARI:
        s = f"statik-{j}"
        cikti.append((f"b-{s}-dogrudan_komsu", s, "dogrudan_komsu", 1001,
                      False))
    for m in carpimda:
        s = f"{m}-surekli"
        for k in ("en_guvenilir_kahin", "en_kisa_yol_kahin"):
            cikti.append((f"c-{s}-{k}", s, k, 1002, False))
    # Y6 · formasyon: tek atlama ve kâhin grafiği; karıştırıcılı ve kısa.
    for k in ("dogrudan_komsu", "en_guvenilir_kahin"):
        cikti.append((f"h-formasyon-surekli-{k}", "formasyon-surekli", k,
                      1006, False))
    # Y5b · tehdit aileleri: statik kolda tek atlama, kısa; hava eşlik kâhinle
    # de (hareketli karıştırıcıda kâhin tazelemesi). Kimliği aile adıyla biter.
    for aile in TEHDIT_SENARYOLARI:
        if aile != "tekli_merkez":
            cikti.append((f"i-statik-surekli-dogrudan_komsu-{aile}",
                          "statik-surekli", "dogrudan_komsu", 1007, False))
    cikti.append(("i-statik-surekli-en_guvenilir_kahin-hava_eslik",
                  "statik-surekli", "en_guvenilir_kahin", 1007, False))
    for s in ("statik-surekli", "bagimsiz-surekli"):
        cikti.append((f"d-{s}-yuklu", s, "yuklu", 1003, False))
        cikti.append((f"e-{s}-kontrol_sinav", s, "kontrol_sinav", 1004, False))
    # 🔒 TAM UZUNLUK VAKALARI SÜREYE GÖRE SEÇİLDİ — 11 Eylül 2026, ölçüldü.
    # Kısa pencerede koşu süresi; tam uzunluk (350 s) bunun en çok ~7 katı:
    #   protokol            statik-surekli  bagimsiz-surekli  gorev-surekli_darbeli
    #   en_yakin_kimlik          117,7 s         378,6 s            175,2 s
    #   en_guvenilir_kahin        ~53 s          ~170 s                —
    #   dogrudan_komsu            11,7 s          76,1 s             64,4 s
    # Döngü üreten `en_yakin_kimlik` tam uzunlukta hareketli kolda ~44 dk
    # sürerdi; ilk düzeltme onu ölçmeden seçmişti (K-114 §2.4). Tam uzunluğun
    # sınadığı şey (evre metrikleri, ham bölüm, tam pencere) protokolden
    # bağımsızdır. Çok atlama ve kâhin grafiği tam uzunlukta ucuz olan statik
    # kolda, hareketli kollarda ise kısa vakalarda sınanır.
    cikti.append(("f-statik-yok-dogrudan_komsu-tam", "statik-yok",
                  "dogrudan_komsu", 1000, True))
    cikti.append(("f-statik-surekli-en_guvenilir_kahin-tam", "statik-surekli",
                  "en_guvenilir_kahin", 1000, True))
    cikti.append(("f-bagimsiz-surekli-dogrudan_komsu-tam",
                  "bagimsiz-surekli", "dogrudan_komsu", 1001, True))
    cikti.append(("f-gorev-surekli_darbeli-dogrudan_komsu-tam",
                  "gorev-surekli_darbeli", "dogrudan_komsu", 1002, True))
    # Y4 · yere toplama (`v2/07` §18 Y4). Kimliği `-yere_toplama` ile biten
    # vaka bu desenle koşar (`_kos`). Çok atlama geçide kâhinle statik kolda,
    # hareketli kolda tek atlama; ikisi de karıştırıcılı ve kısa.
    cikti.append(("g-statik-surekli-en_guvenilir_kahin-yere_toplama",
                  "statik-surekli", "en_guvenilir_kahin", 1005, False))
    cikti.append(("g-bagimsiz-surekli-dogrudan_komsu-yere_toplama",
                  "bagimsiz-surekli", "dogrudan_komsu", 1005, False))
    # K-151 · Y1 + Y2: karıştırıcılı statik kol — hem başarılı hem vazgeçilen
    # unicast sonucu doğsun; başlık her veri çerçevesini uzatsın.
    cikti.append(("j-statik-surekli-baslikli_sonuc", "statik-surekli",
                  "baslikli_sonuc", 1008, False))
    # 🔒 K-171 (`v2/15` A1) · GERÇEK PROTOKOLLER. Matris 25 Eylül'e kadar
    # yalnız sınav protokolleri ve kâhinlerle koşuyordu; asıl karşılaştırılan
    # dört protokolün yolları (RREQ/RERR, HELLO/TC, çok yol, DESPARETE'nin
    # kontrol düzlemi ve politika düşmesi) hiçbir vakada sınanmıyordu.
    # Karıştırıcılı statik kol, kısa; DESPARETE kendi işletme deseninde
    # (yere toplama, varsayılan profil — `aodv_uygunluk._fabrika` ile aynı;
    # `k171`/`k172`de v0.4, K-172'den sonra v0.4.1).
    for p in ("aodv", "olsr", "aomdv"):
        cikti.append((f"k-statik-surekli-{p}", "statik-surekli", p, 1009,
                      False))
    cikti.append(("k-statik-surekli-desparete-yere_toplama", "statik-surekli",
                  "desparete", 1009, False))
    # 🔒 K-173 · `v2/15` A2 — işlem kazancı AÇIK (B = 22 MHz, NF 7 dB).
    # Kimliği `-islem_kazanci` ile biten vaka bu anahtarla koşar (`_kos`).
    # Tek atlama, karıştırıcılı statik kol: kazanç girişime karşı işler.
    cikti.append(("l-statik-surekli-dogrudan_komsu-islem_kazanci",
                  "statik-surekli", "dogrudan_komsu", 1010, False))
    # 🔒 K-174 · `v2/15` A3 — güce dayalı taşıyıcı dinleme + ED-CCA. Kimliğinde
    # `-tasiyici_guc` geçen vaka bu kiple koşar (`_kos`). Sabit ve hareketli
    # (hava eşlik) karıştırıcı: ED donması, geçiş ve 10 ms yeniden denetim.
    cikti.append(("n-statik-surekli-dogrudan_komsu-tasiyici_guc",
                  "statik-surekli", "dogrudan_komsu", 1010, False))
    cikti.append(("n-statik-surekli-dogrudan_komsu-tasiyici_guc-hava_eslik",
                  "statik-surekli", "dogrudan_komsu", 1010, False))
    # 🔒 K-175 · `v2/15` A5 — yayılım gecikmesi; kimliğinde
    # `-yayilim_gecikmesi` geçen vaka o anahtarla koşar. Geometrik ve güç
    # kipinde (varış penceresi iki yolda da ayrı yazıldı).
    cikti.append(("o-statik-surekli-dogrudan_komsu-yayilim_gecikmesi",
                  "statik-surekli", "dogrudan_komsu", 1010, False))
    cikti.append(("o-statik-surekli-dogrudan_komsu-tasiyici_guc"
                  "-yayilim_gecikmesi",
                  "statik-surekli", "dogrudan_komsu", 1010, False))
    # 🔒 K-176 · `v2/15` A6 — karıştırıcı gerçekçiliği; kimliğinde
    # `-karistirici_gercekci` geçen vaka o anahtarla koşar. Yer karıştırıcısı
    # (yer–hava kanalı) · aldatıcı kilidi (geometrik ve güç kipinde) ·
    # reaktif eşik · hareketli kolda karıştırıcı bağı sönümlemesi.
    for kimlik, senaryo in (
            ("p-statik-surekli-dogrudan_komsu-karistirici_gercekci"
             "-cephe_hatti", "statik-surekli"),
            ("p-statik-aldatici-dogrudan_komsu-karistirici_gercekci",
             "statik-aldatici"),
            ("p-statik-aldatici-dogrudan_komsu-tasiyici_guc"
             "-karistirici_gercekci", "statik-aldatici"),
            ("p-statik-reaktif-dogrudan_komsu-karistirici_gercekci",
             "statik-reaktif"),
            ("p-bagimsiz-surekli-dogrudan_komsu-karistirici_gercekci",
             "bagimsiz-surekli")):
        cikti.append((kimlik, senaryo, "dogrudan_komsu", 1010, False))
    # 🔒 K-177 · `v2/15` A4 — hız uyarlaması (işlem kazancıyla): veri yolu
    # tek atlamada, kontrol düzleminin unicast'ı sınav protokolüyle.
    cikti.append(("q-statik-surekli-dogrudan_komsu-islem_kazanci"
                  "-hiz_uyarlamasi", "statik-surekli", "dogrudan_komsu",
                  1010, False))
    cikti.append(("q-bagimsiz-surekli-kontrol_sinav-islem_kazanci"
                  "-hiz_uyarlamasi", "bagimsiz-surekli", "kontrol_sinav",
                  1010, False))
    # 🔒 K-178 · `v2/15` A7 — referans dünya (1:1, EIRP 20 dBm, 7 km, 40
    # düğüm). K-181'den (A8) beri `referans_2026` bütün anahtarları açar;
    # `k180` ↔ `k181` bu üç vakanın A7 → A8 farkıdır.
    cikti.append(("r-referans-statik-yok-dogrudan_komsu", "statik-yok",
                  "dogrudan_komsu", 1010, False))
    cikti.append(("r-referans-bagimsiz-surekli-dogrudan_komsu",
                  "bagimsiz-surekli", "dogrudan_komsu", 1010, False))
    cikti.append(("r-referans-statik-surekli-aodv", "statik-surekli", "aodv",
                  1010, False))
    # 🔒 K-179 · `v2/15` B3 — gözlem v2 alanları (doluluk yalnız isteyen
    # protokolde çalışır; bu sınav protokolü ister ve teşhise yazar).
    cikti.append(("s-statik-surekli-doluluk_sinav-tasiyici_guc",
                  "statik-surekli", "doluluk_sinav", 1010, False))
    # 🔒 K-180 · `v2/15` C1 — düğüm kaybı (5 İHA, 15–35 s): kuyruk, tampon,
    # uçuş ve onay bekleyen deneme; rota protokolünde ve tek atlamada.
    # Tohumlar İKİZ vakayla aynı (`m-bagimsiz-surekli-dogrudan_komsu`,
    # `k-statik-surekli-aodv`): ilk ölüme kadar ikizle aynı koşu.
    cikti.append(("t-bagimsiz-surekli-dogrudan_komsu-dugum_kaybi",
                  "bagimsiz-surekli", "dogrudan_komsu", 1000, False))
    cikti.append(("t-statik-surekli-aodv-dugum_kaybi", "statik-surekli",
                  "aodv", 1009, False))
    cikti += [(kimlik, senaryo, protokol, tohum, False)
              for kimlik, (senaryo, protokol, tohum, _ek)
              in REFERANS_VAKALARI.items()]
    return tuple(cikti)


def _fabrika(protokol: str, kur):
    """Protokol fabrikası — İŞÇİDE kurulur, havuzdan geçmez."""
    if protokol == "dogrudan_komsu":
        from protokoller.kosum_kosumu import DogrudanKomsu
        return lambda i: DogrudanKomsu()
    if protokol == "en_yakin_kimlik":
        from protokoller.kosum_kosumu import EnYakinKimlik
        return lambda i: EnYakinKimlik()
    if protokol in ("en_guvenilir_kahin", "en_kisa_yol_kahin"):
        from kalibrasyon.kahin import (EnGuvenilirKahin, EnKisaYolKahin,
                                       KanalGrafigi)
        grafik = KanalGrafigi(kur)
        tip = (EnGuvenilirKahin if protokol == "en_guvenilir_kahin"
               else EnKisaYolKahin)
        return lambda i: tip(i, grafik)
    if protokol == "yuklu":
        from test_kosum import _YukluProtokol
        return lambda i: _YukluProtokol()
    if protokol == "kontrol_sinav":
        from test_kontrol_duzlemi import SinavProtokolu, yeni_kayit
        kayit = yeni_kayit()
        return lambda i: SinavProtokolu(i, kayit)
    if protokol == "baslikli_sonuc":
        from protokoller.kosum_kosumu import DogrudanKomsu

        class BaslikliSonuc(DogrudanKomsu):
            """K-151 · 36 B veri başlığı (DESPARETE'ninki) + sonuç bildirimi."""
            veri_baslik_bayt = 36

            def iletim_sonucu(self, gozlem, hedef, basarili, tekrar, tur):
                return None
        return lambda i: BaslikliSonuc()
    if protokol == "doluluk_sinav":
        from protokoller.kosum_kosumu import DogrudanKomsu

        class DolulukSinav(DogrudanKomsu):
            """B3 (K-179): gözlem v2 alanlarını ister, son gözlemi teşhise
            yazar — kanal doluluğu, PHY hatası, alınan çerçeve, GPS."""
            kanal_dolulugu_ister = True

            def __init__(self):
                self._son = None

            def sonraki_atlama(self, gozlem):
                self._son = gozlem
                return super().sonraki_atlama(gozlem)

            def teshis(self, dugum):
                g = self._son
                if g is None:
                    return {}
                return {"mesgul_sure_s": g.mesgul_sure_s,
                        "phy_hata": g.phy_hata,
                        "alinan_cerceve": g.alinan_cerceve,
                        "konum_x": g.kendi_konum[0],
                        "hiz_x": g.kendi_hiz[0]}
        return lambda i: DolulukSinav()
    if protokol in ("aodv", "olsr", "aomdv"):
        from protokoller.aodv import AODV
        from protokoller.aomdv import AOMDV
        from protokoller.olsr import OLSR
        tip = {"aodv": AODV, "olsr": OLSR, "aomdv": AOMDV}[protokol]
        return lambda i: tip(i)
    if protokol == "jarmrout":
        from protokoller.jarmrout import JarmRout
        return lambda i: JarmRout(i)
    if protokol == "olsrv2":
        from protokoller.olsrv2 import OLSRv2
        return lambda i: OLSRv2(i)
    if protokol == "babel":
        from protokoller.babel import Babel
        return lambda i: Babel(i)
    if protokol == "desparete":
        from protokoller.desparete import DESPARETE
        from protokoller.desparete_bayrak import PROFIL_V02, SECENEK_V041
        gecit = kur.konfig.gecit
        return lambda i: DESPARETE(i, gecit, bayraklar=PROFIL_V02,
                                   secenekler=SECENEK_V041)
    raise ValueError(f"bilinmeyen protokol: {protokol!r}")


def _kos(vaka: tuple[str, str, str, int, bool]) -> dict:
    kimlik, senaryo, protokol, tohum, tam = vaka
    pencere = {} if tam else dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
                                  olcum_bitis_s=40.0, kosu_bitis_s=50.0)
    if kimlik in REFERANS_VAKALARI:
        from sim2.kanal.dunya import referans_2026
        ek = REFERANS_VAKALARI[kimlik][3]
        kur = kurulum_yap(referans_2026(kol="regresyon", senaryo=senaryo,
                                        tohum=tohum, not_=kimlik,
                                        **{**pencere, **ek}))
        kosu = Kosu(kur, _fabrika(protokol, kur))
        kosu.kostur()
        return sonuc_satiri(kur, kosu.dugumler, protokol)
    # Y4: kimliği `-yere_toplama` ile biten vaka o desenle koşar.
    desen = ({"trafik_deseni": "yere_toplama"}
             if kimlik.endswith("-yere_toplama") else {})
    # Y5b: kimliği bir tehdit ailesinin adıyla biten vaka o aileyle koşar.
    tehdit = next(({"tehdit_senaryosu": a} for a in TEHDIT_SENARYOLARI
                   if a != "tekli_merkez" and kimlik.endswith(f"-{a}")), {})
    # A2 (K-173): kimliği `-islem_kazanci` ile biten vaka o anahtarla koşar.
    kazanc = ({"islem_kazanci": True, "bant_genisligi_hz": 22e6,
               "gurultu_figuru_db": 7.0}
              if "-islem_kazanci" in kimlik else {})
    # A4 (K-177): kimliğinde `-hiz_uyarlamasi` geçen vaka (işlem kazancı ister).
    if "-hiz_uyarlamasi" in kimlik:
        kazanc["hiz_uyarlamasi"] = True
    # A3 (K-174): kimliğinde `-tasiyici_guc` geçen vaka güç kipinde koşar.
    dinleme = ({"tasiyici_dinleme": "guc"} if "-tasiyici_guc" in kimlik
               else {})
    # A5 (K-175): kimliğinde `-yayilim_gecikmesi` geçen vaka.
    if "-yayilim_gecikmesi" in kimlik:
        dinleme["yayilim_gecikmesi"] = True
    # C1 (K-180): kimliğinde `-dugum_kaybi` geçen vaka.
    if "-dugum_kaybi" in kimlik:
        dinleme.update(kayip_dugum_sayisi=5, kayip_bas_s=15.0,
                       kayip_bitis_s=35.0)
    # A6 (K-176): kimliğinde `-karistirici_gercekci` geçen vaka.
    if "-karistirici_gercekci" in kimlik:
        dinleme["karistirici_gercekci"] = True
    # A7 (K-178): `r-referans-` önekli vaka referans dünyada koşar.
    if kimlik.startswith("r-referans-"):
        from sim2.kanal.dunya import referans_2026
        kazanc.pop("islem_kazanci", None)
        kazanc.pop("bant_genisligi_hz", None)
        kazanc.pop("gurultu_figuru_db", None)
        kfg = referans_2026(kol="regresyon", senaryo=senaryo, tohum=tohum,
                            not_=kimlik, **pencere, **desen, **tehdit,
                            **kazanc, **dinleme)
    else:
        kfg = Konfig(kol="regresyon", senaryo=senaryo, tohum=tohum,
                     not_=kimlik, **pencere, **desen, **tehdit, **kazanc,
                     **dinleme)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, _fabrika(protokol, kur))
    kosu.kostur()
    return sonuc_satiri(kur, kosu.dugumler, protokol)


def _is(vaka):
    """Havuz işçisi. 🔒 Modül düzeyinde — Windows `spawn`.

    Duvar saati satıra YAZILMAZ (her koşuda değişir, karşılaştırmayı bozardı);
    yalnız basılır ki sonraki koşumun bandı ölçümden gelsin.
    """
    t0 = time.perf_counter()
    try:
        return vaka, _kos(vaka), None, time.perf_counter() - t0
    except Exception as hata:                       # noqa: BLE001
        return (vaka, None, f"{type(hata).__name__}: {hata}",
                time.perf_counter() - t0)


# ==========================================================================
def uret(etiket: str, isci: int) -> int:
    yol = DIZIN / f"{etiket}.jsonl"
    if yol.exists():
        print(f"  🔴 {yol} zaten var — üstüne yazılmaz, satırlar çoğalırdı. "
              f"Başka bir etiket seçin.")
        return 1
    liste = vakalar()
    print(f"REGRESYON SATIRLARI — {len(liste)} vaka → {yol}")
    t0 = time.perf_counter()
    hatalar = 0
    en_uzun = (0.0, "")
    with SatirYazici(yol) as yazici, Pool(isci) as havuz:
        for i, (vaka, satir, hata, sure) in enumerate(
                havuz.imap_unordered(_is, liste, chunksize=1), start=1):
            en_uzun = max(en_uzun, (sure, vaka[0]))
            if hata is not None:
                hatalar += 1
                print(f"  🔴 {vaka[0]}: {hata}")
                continue
            yazici.yaz(satir)
            print(f"  {i:>3}/{len(liste)} {vaka[0]:<52} "
                  f"gecerli={satir['korunum']['gecerli']} · {sure:.0f} s",
                  flush=True)
    print(f"  sure: {(time.perf_counter() - t0) / 60.0:.1f} dk · en uzun vaka: "
          f"{en_uzun[1]} {en_uzun[0]:.0f} s · hata: {hatalar}")
    return 1 if hatalar else 0


def _duzlestir(nesne, onek: str = "") -> dict[str, object]:
    """İç içe sözlüğü noktalı yollara açar. Listeler DEĞER olarak kalır."""
    cikti: dict[str, object] = {}
    if isinstance(nesne, dict):
        for anahtar, deger in nesne.items():
            yol = f"{onek}.{anahtar}" if onek else str(anahtar)
            cikti.update(_duzlestir(deger, yol))
    else:
        cikti[onek] = nesne
    return cikti


def _oku(etiket: str) -> dict[str, dict]:
    yol = DIZIN / f"{etiket}.jsonl"
    satirlar: dict[str, dict] = {}
    with open(yol, encoding="utf-8") as dosya:
        for no, metin in enumerate(dosya, start=1):
            satir = json.loads(metin)
            kimlik = satir["kimlik"]["not_"]
            if kimlik in satirlar:
                raise ValueError(f"{yol}:{no} vaka iki kez yazılmış: {kimlik}")
            satirlar[kimlik] = satir
    return satirlar


def _eslesir(alan: str, onek: str) -> bool:
    """Yıldızsız önek yalnız TAM bir yol bölümüyle eşleşir (`metrikler.psr`,
    `metrikler.psr_pencere`yi kapsamaz); `*` ile biten önek düz metin
    önekidir (`metrikler.kontrol_*`)."""
    if onek.endswith("*"):
        return alan.startswith(onek[:-1])
    return alan == onek or alan.startswith(onek + ".")


def karsilastir(a: str, b: str, izin: tuple[str, ...],
                yeni: tuple[str, ...] = (), sifir: tuple[str, ...] = (),
                degisen: tuple[str, ...] = ()) -> int:
    sa, sb = _oku(a), _oku(b)
    print(f"REGRESYON KARSILASTIRMASI — {a} ({len(sa)} satir) ↔ "
          f"{b} ({len(sb)} satir)")
    # 🔒 `--yeni` önekindeki vaka YALNIZ SONRAKİ dosyada olabilir: matrise
    # bilerek eklenmiştir ve karşılaştıracağı satır yoktur. Ayrı basılır,
    # gizlenmez; geçersizse bulgudur. Önceki dosyada olup sonrakinde olmayan
    # vaka her zaman bulgudur.
    eksik: list[str] = []
    for kimlik in sorted(set(sa) ^ set(sb)):
        if kimlik in sb and any(kimlik.startswith(o) for o in yeni):
            gecerli = sb[kimlik]["korunum"]["gecerli"]
            print(f"  (yeni vaka) yalniz {b}: {kimlik} · gecerli={gecerli}")
            if gecerli:
                continue
        eksik.append(kimlik)
        print(f"  🔴 yalniz bir dosyada ya da gecersiz: {kimlik}")
    birebir = 0
    bulgu: dict[str, list[str]] = {}
    izinli: dict[str, list[str]] = {}
    beklenen: dict[str, int] = {}
    sifir_ihlal: dict[str, list[str]] = {}
    sifir_sayi: dict[str, int] = {}
    # 🔒 `--degisen` — K-173. Vaka önekiyle İLAN EDİLMİŞ davranış değişikliği
    # (ör. bir protokolün varsayılan profili değişti). Alan izni bütün
    # vakalara uygulanır; bir vakanın her metriğine izin vermek öteki
    # vakalardaki farkları da gizlerdi. İlan edilen vaka alan
    # karşılaştırmasından ÇIKAR, ayrı basılır ve GEÇERLİ olmak zorundadır.
    degisen_vaka: list[str] = []
    for kimlik in sorted(set(sa) & set(sb)):
        if any(kimlik.startswith(o) for o in degisen):
            da, db = _duzlestir(sa[kimlik]), _duzlestir(sb[kimlik])
            n = sum(1 for alan in set(da) | set(db)
                    if alan not in HER_KOSUDA_DEGISEN
                    and da.get(alan, "<yok>") != db.get(alan, "<yok>"))
            gecerli = sb[kimlik]["korunum"]["gecerli"]
            print(f"  (ilan edilmis degisen vaka) {kimlik} · {n} alan farkli "
                  f"· gecerli={gecerli}")
            if not gecerli:
                eksik.append(kimlik)
            degisen_vaka.append(kimlik)
    for kimlik in sorted(set(sa) & set(sb)):
        if kimlik in degisen_vaka:
            continue
        da, db = _duzlestir(sa[kimlik]), _duzlestir(sb[kimlik])
        vaka_bulgu = False
        for alan in sorted(set(da) | set(db)):
            if da.get(alan, "<yok>") == db.get(alan, "<yok>"):
                continue
            if alan in HER_KOSUDA_DEGISEN or alan in KOD_KIMLIGI:
                beklenen[alan] = beklenen.get(alan, 0) + 1
                continue
            if any(_eslesir(alan, o) for o in izin):
                izinli.setdefault(alan, []).append(kimlik)
                continue
            bulgu.setdefault(alan, []).append(kimlik)
            vaka_bulgu = True
        birebir += 0 if vaka_bulgu else 1
        # 🔒 `--sifir`: ilan edilmiş alan sonraki dosyada VAR ve SIFIR olmalı.
        for onek in sifir:
            eslesen = [alan for alan in db if _eslesir(alan, onek)]
            if not eslesen:
                sifir_ihlal.setdefault(f"{onek} <yok>", []).append(kimlik)
            for alan in eslesen:
                sifir_sayi[alan] = sifir_sayi.get(alan, 0) + 1
                if db[alan] != 0:
                    sifir_ihlal.setdefault(alan, []).append(kimlik)
    print()
    print(f"  bulgusuz vaka : {birebir}/"
          f"{len(set(sa) & set(sb)) - len(degisen_vaka)}"
          + (f" (+{len(degisen_vaka)} ilan edilmis degisen)"
             if degisen_vaka else ""))
    for alan, n in sorted(beklenen.items()):
        print(f"  (beklenen) {alan:<48} {n} vakada farkli")
    for alan, vakalar_ in sorted(izinli.items()):
        print(f"  (izinli)   {alan:<48} {len(vakalar_)} vakada farkli")
    for alan, vakalar_ in sorted(bulgu.items()):
        print(f"  🔴 BULGU   {alan:<48} {len(vakalar_)} vakada farkli "
              f"· ilk: {vakalar_[0]}")
    ortak = len(set(sa) & set(sb)) - len(degisen_vaka)
    for alan, n in sorted(sifir_sayi.items()):
        if alan not in sifir_ihlal:
            print(f"  (sifir)    {alan:<48} {n}/{ortak} vakada 0")
    for alan, vakalar_ in sorted(sifir_ihlal.items()):
        print(f"  🔴 SIFIR DEGIL {alan:<44} {len(vakalar_)} vakada "
              f"· ilk: {vakalar_[0]}")
    temiz = not bulgu and not eksik and not sifir_ihlal
    print()
    print(f"  {'🟢 BIREBIR (izinli farklar disinda)' if temiz else '🔴 FARK VAR'}")
    return 0 if temiz else 1


if __name__ == "__main__":
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    arguman = sys.argv[1:]
    if len(arguman) >= 2 and arguman[0] == "uret":
        # 🔒 Varsayılan 8 işçi — `03` §1: *"ağır koşumda makine kullanılabilir
        # kalır"* (17 Eylül: 4 işçi · 21 Eylül öğrenci: 8 çekirdek). Önceden
        # 10'a SABİTTİ ve kural yazıldıktan sonra da öyle kaldı; kapanış
        # paketi hazırlanırken görüldü. Başka sayı isteyen `--isci N` verir.
        isci = 8
        if "--isci" in arguman:
            isci = int(arguman[arguman.index("--isci") + 1])
        raise SystemExit(uret(arguman[1], isci=isci))
    if len(arguman) >= 3 and arguman[0] == "karsilastir":
        def _onekler(bayrak: str) -> tuple[str, ...]:
            if bayrak not in arguman:
                return ()
            return tuple(o for o in arguman[arguman.index(bayrak) + 1]
                         .split(",") if o)
        raise SystemExit(karsilastir(arguman[1], arguman[2],
                                     _onekler("--izin"), _onekler("--yeni"),
                                     _onekler("--sifir"),
                                     _onekler("--degisen")))
    print(__doc__)
    raise SystemExit(2)
