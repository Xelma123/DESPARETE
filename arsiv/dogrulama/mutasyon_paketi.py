"""
Ç1.3 / S-B — MUTASYON PAKETİ.

🔴 SORDUĞU SORU: testlerimiz gerçekten bir şey ölçüyor mu?

Bir test paketinin geçmesi, hiçbir şeyi kanıtlamaz. Kanıt, **kod kasten
bozulduğunda testin KIRILMASIDIR.** Kırılmayan bir test, o kod yolunda
hiçbir koruma sağlamıyor demektir.

NASIL ÇALIŞIR
=============
Her mutasyon için:
  1. Depo geçici bir dizine kopyalanır
  2. Tek bir metin değişikliği uygulanır — uygulanmadıysa HATA
  3. TAM test paketi o kopyada koşulur
  4. Hangi testlerin kırıldığı toplanır

🔴 BAŞARISIZLIK ÖLÇÜTÜ — ÜÇ KOŞUL BİRDEN (B-21, 19 Ağustos 2026)
==================================================================
  1. TABAN TEMİZ olmalı — mutasyonsuz kopyada test paketi geçmeli
  2. Her mutasyon EN AZ BİR testi kırmalı
  3. Kırılanlar arasında `beklenen_test` BULUNMALI

⚠️ Mutasyonlar geçici kopyada uygulanır; asıl depo hiç değişmez.

🔴 NEDEN 1. VE 3. KOŞUL SONRADAN EKLENDİ — Y7, DÖRDÜNCÜ KEZ
============================================================
Bu paket 19 Ağustos 11:01'de koşuldu ve **17/17** yazdı. Çıktıdaki örüntü:
17 mutasyonun 17'sinde de `test_hareketli_karistirici_yorungesi_dilimle_hizali`
ve `test_c1_3_mutasyon_hangi_kontrol_yakaliyor` kırılıyordu. Birincisi
depoda ARTIK YOK; ikisi de o an TABANDA kırıktı (K-036 bunu kaydediyor:
"mutasyonsuz kopyada 2 test başarısızdı"). Testler 11:18'de düzeltildi —
yani **17/17 sayısı kirli bir tabandan üretildi ve bir daha koşulmadı.**

Taban kırıkken bu araç her mutasyona "yakalandı" der: kırılan test, mutasyonun
bozduğu yolla ilgisiz olabilir. Kör tarayıcıya (`kor_mutasyon.py`) taban
kontrolü K-036'da eklenmişti; KAPI KRİTERİNİ (Ç1.3) üreten bu dosyaya
eklenmemişti.

3. koşul aynı hatanın ikinci yarısını kapatır: `beklenen_yakalayici` alanı
BİLDİRİLMİŞTİ ama hiçbir yerde KONTROL EDİLMİYORDU — `03` B5'in
"bildirim ≠ kullanım" tuzağı, doğrulama aracının kendi içinde.

> Y7: bir doğrulama aracı, NE KOŞTUĞUNU kendisi doğrulamak zorunda.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path

# 🔴 ALT SÜREÇ ÇIKTISI UTF-8 OLARAK ÇÖZÜLÜR (20 Ağu 2026).
# `subprocess.run(..., text=True)` kodlama verilmezse çıktıyı YEREL KOD
# SAYFASIYLA çözer. Bu makinede o cp1254 ve çocuk süreç UTF-8 basıyor
# (PYTHONIOENCODING ayarlı). Türkçe "Ş" (U+015E → C5 9E) gibi karakterler
# cp1254'te TANIMSIZ olduğu için ebeveyn `UnicodeDecodeError` fırlatır ve
# araç, işini bitirmişken çöker. Ölçüldü: bir doğrulama koşusu tam olarak
# böyle düştü. `errors="replace"` ile ayrıştırma asla çökmez.

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

# 🔴 B-100 — kopyalama kuralı TEK KAYNAKTAN okunur (`dogrulama/kopya.py`).
# Burada elle yazılmış iki liste vardı, biri `"v2"`yi dışlıyor ve kapıyı
# düşürüyordu; ikisi birbirinden de ayrışmıştı (`*.txt`).
from dogrulama.kopya import depoyu_kopyala                       # noqa: E402

# --------------------------------------------------------------------------
# 🔴 ZAMAN AŞIMI BÜTÇESİ — ELLE TUTULAN KAPI SABİTİ (25 Ağustos 2026, K-058)
#
# Bu sabit bir kez SESSİZCE yanlış oldu ve kapıyı düşürdü. Paket 324 → 354
# teste (8,6–10,2 dk → 12,7 dk) büyüdü; `timeout` 1200 sn'de kaldı. `Pool(8)`
# altında mutant başına gerçek süre 18,5–20+ dk'ya çıktı ve **35 mutantın
# 31'i zaman aşımına uğradı.** Kapı bunu "mutasyon uygulanamadı" diye
# raporladı — hiç yapmadığı bir teşhis (aşağıya bkz.).
#
# 🔴 Bu sabitleri değiştiren, ÖLÇÜM TARİHİNİ de değiştirir. Bunları birbirine
# bağlayan ucuz test: `tests/test_kapi_secimleri.py::test_b78_*`
#
# Üretici (tek koşu, 10 çekirdek, boş makine):
#     python -m pytest tests -q
# Üretici (çekişme, kapının kendi yolundan — 8 mutant, Pool(8)):
#     scratchpad/c13_tani.py  → 7/8 zaman aşımı, biten tek mutant 18,5 dk
# --------------------------------------------------------------------------
# 🔴 BU İKİSİ BİR ÇİFTTİR — AYNI KOŞUDA ölçülür, ayrı ayrı güncellenmez.
# Biri güncellenip diğeri ölçülmezse koruma sessizce boşalır.
# 🔴 26 AĞU (K-067) — ÇİFT ARTIK VERİYE BAĞLI, TEK OKUMAYA DEĞİL.
#
# BEŞ TEMİZ koşu (hepsi boş makine, RC=0) ölçüldü ve makinenin kendisi
# koşudan koşuya **%15,8** oynuyor:
#
#     371 test / 851,78 sn  ->  2,2959 sn/test   (Zincir A)
#     373 test / 878,24 sn  ->  2,3545 sn/test   (Zincir B)
#     376 test / 966,11 sn  ->  2,5694 sn/test   (Zincir C)  <- EN KÖTÜ
#     382 test / 852,18 sn  ->  2,2308 sn/test   (Zincir D)
#     386 test / 856,75 sn  ->  2,2196 sn/test   (Zincir E)  <- en iyi
#     388 test / 908,69 sn  ->  2,3420 sn/test   (B-57 sonu)
#
# 🔴 EN KÜÇÜK okumayı yazmak marjı OLDUĞUNDAN İYİ gösterir — K-058'in yönü.
# Bu yüzden `_gereken_zaman_asimi_s` artık son okumayı değil **EN KÖTÜ
# GÖZLENEN test başına maliyeti** kullanıyor:
#     marj son okumaya göre 1,56×  ·  EN KÖTÜ gözleme göre **1,36×**
#
# ⚠️ Bu, deponun kendi kuralının uygulanması: *"tahminini ÖLÇTÜĞÜN EN BÜYÜK
# süreden kur, ortalamadan değil"* (süre tahmini bu depoda BEŞ kez tutmadı).
# 🔴 27 AĞUSTOS 2026 — ÇİFT DÖRDÜNCÜ KEZ TAZELENDİ, VE BU KEZ SEBEP
# TEST SAYISI DEĞİL: TEST BAŞINA MALİYET İKİYE KATLANDI.
#
#     422 test / 1 850,63 sn  ->  **4,3854 sn/test**   (önceki en kötü 2,5694)
#
# 🔴 Y12'NİN KENDİ YAZILI SINIRI ATEŞLEDİ. `test_b78_*` süreyi test
# SAYISIYLA ölçekliyor ve bayat `TEST_BASINA_EN_KOTU_S`u kullanıyordu:
# 422 test için 1 482 sn "gerekiyor" dedi, yazılı 1 800 sn geçti — oysa
# gerçekte 2 776 sn gerekiyordu. Koruma SUSTU, çünkü kaydığı eksen
# ölçtüğü eksen değildi:
#
#     | vaka                                        | yakalanır mı |
#     | Paket büyüdü, sabit güncellenmedi           | ✅           |
#     | Çarpanlardan biri dejenere edildi           | ✅           |
#     | 🔴 ÖLÇÜM ÇİFTİNİN KENDİSİ TAZELENMEDİ       | ❌ HAYIR     |
#
# Bu boşluk K-060'ta **bilerek bırakılmış ve beşinci denetimin şüphe
# listesine konmuştu.** Bugün fiilen ateşledi: `taban_kontrolu()` TEMİZ bir
# tabanı "kırık" diye raporladı — K-058'in birebir tekrarı, ama bu kez
# 150 dakikalık kapı KOŞULMADAN önce görüldü.
#
# ⚠️ Test başına maliyetin NEDEN ikiye katlandığı bu satırın konusu DEĞİL
# ve ayrıca ölçülüyor: Faz 3'ün üç değişikliği de A/B ile sınandı ve
# hiçbiri sebep değil (tarama %3 · iki `assert` %0). Aynı dosya aynı kodla
# iki farklı anda 163,53 ve 305 sn verdi. Sebep ne olursa olsun sabit
# ÖLÇÜLEN EN BÜYÜK süreden kurulur — deponun kendi kuralı.
#
# Üretici: `python -c "...from dogrulama.mutasyon_paketi import taban_kontrolu..."`
OLCULEN_KOSULAR = ((371, 851.78), (373, 878.24), (376, 966.11),
                   (382, 852.18), (386, 856.75), (388, 908.69),
                   (422, 1850.63),                     # <- EN KÖTÜ (4,3854)
                   (422, 986.73),                      # AYNI paket, aynı gün
                   (427, 892.66),                      # 2,0906 (Faz 4)
                   # 🔴 B-167 / B0.9 (3 Eylül 2026) — YENİ EN İYİ OKUMA.
                   # 492 test, boş makine, RC = 0: **1,888 sn/test** —
                   # yazılı bandın EN İYİSİNİN de altında (2,0906).
                   # Sekizinci denetim 2,081 ölçmüştü; bu ondan da düşük.
                   # 🔒 Band artık **1,888 – 4,3854 = ×2,32**.
                   # `TEST_BASINA_EN_KOTU_S` DEĞİŞMEZ (en kötüden türer),
                   # ama okuyan kişi bandın gerçek genişliğini görmek
                   # zorunda — bu makine tek bir sayıyla tarif edilemiyor.
                   (492, 928.68))                      # <- EN İYİ (B0.9)
# 🔴 SON İKİ SATIR AYNI PAKETİN AYNI GÜNKÜ İKİ OKUMASIDIR: 1 850,63 ve
# 986,73 sn — **×1,88**. Üçüncü bir okuma 1 832,95 sn, dördüncüsü
# (427 test) **892,66 sn** verdi — yani sn/test bandı **2,0906–4,3854,
# 2,10 KAT**. Yani bu
# makinenin salınımı yazılı `%15,8` DEĞİL, neredeyse İKİ KAT.
#
# ⚠️ Rahatsız eden okuma ATILMADI: ikisi de burada. `TEST_BASINA_EN_KOTU_S`
# en kötüsünden türüyor (deponun kuralı), ama okuyan kişi bandın gerçek
# genişliğini görmek zorunda — tek bir sayı bu makineyi tarif etmiyor.
TEST_BASINA_EN_KOTU_S = max(s / n for n, s in OLCULEN_KOSULAR)   # 4,3854

PAKET_TEST_SAYISI = 422          # ölçüldü 27 Ağu 2026 — boş makine, RC=0
PAKET_SURESI_S = 1850.63         # ölçüldü AYNI koşuda: 30,8 dk · 10 çekirdek
#   (önceki çiftler yukarıdaki `OLCULEN_KOSULAR`da duruyor)
#
# 🔴 26 AĞU — ÇİFT ÜÇÜNCÜ KEZ TAZELENDİ (K-065, Zincir C).
# ⚠️ ÖNCE 1 362 sn ÖLÇÜLDÜ VE BU YANLIŞTI: makine çekişmeliydi. Ayırt
# eden şey ÖNCEDEN İLAN EDİLEN bir koşuldu — "~940 sn çıkarsa çekişme,
# ~1360 çıkarsa gerileme" — ve DEĞİŞMEMİŞ bir aracın süresi (0,4 -> 0,7
# -> 0,4 dk) çekişmeyi doğruladı. Boş makinede 966,1 sn.
# 🔒 Bu, çiftin neden AYNI ve BOŞ koşudan okunması gerektiğinin ölçülmüş
# örneğidir: çekişmeli bir okuma sabiti %41 şişirirdi.
#   (ondan önceki: 367 test / 828,3 sn — 25 Ağu)
#
# 🔴 26 AĞU — ÇİFT İKİNCİ KEZ TAZELENDİ (K-064, Zincir B): B-84'ün iki
# koruma testi eklendi (371 -> 373). ⚠️ Test BAŞINA maliyet 2,296 -> 2,354 sn
# (+%2,5) — iki testin biri DÖRT tam koşu yapıyor, yani ortalamanın çok
# üstünde. Bu, A-10'un (beşinci denetim, ANLAŞILMAYANLAR) işaret ettiği
# şeydir: `_gereken_zaman_asimi_s` süreyi test SAYISIYLA DOĞRUSAL ölçekler,
# ama testler eşit maliyetli DEĞİLDİR. Bugün emniyet payı bunu karşılıyor;
# A-10 Zincir E'de ele alınacak.
#   (ondan önceki: 354 test / 762,0 sn — 25 Ağu, kapı düşmeden önce)
#
# 🔴 26 AĞU — ÇİFT NEDEN TAZELENDİ (K-062): B-82/B-83'ün dört testi eklendi
# (367 -> 371) ve `yuk_bayt`ın Y7 öz-denetimi ÖLÇÜM yoluna geçti; ölçüldü,
# o fonksiyon 1,44x yavaşladı. Test BAŞINA maliyet 2,257 -> 2,296 sn (+%1,7),
# yani yavaşlama pakete YANSIMADI — ama çift yine de AYNI KOŞUDAN yeniden
# okundu, çünkü Y12'nin beyan edilmiş kör noktası tam olarak budur:
# "biri güncellenip diğeri ölçülmezse koruma sessizce boşalır".

# ==========================================================================
# 🔴 B-90 (BEŞİNCİ DENETİM) — 1,60 ÖLÇÜLEN HER GÖZLEMİN ALTINDAYDI
#
# Eski gerekçe: *"8 yollu koşuda biten TEK mutant 18,5 dk sürdü (1,46×);
# diğer 7'si 20 dk'da HÂLÂ bitmemişti … güvenli tarafa 1,60."*
#
# Beşinci denetim üst sınırı ÖLÇTÜ: kendi 35 mutasyonluk kampanyasında
# **11 mutant tam paketi bitirdi** ve çarpanları şunlar çıktı
# (taban: bu makinede tek koşu, boş makine, 768,56 sn):
#
#     1,548 · 1,673 · 1,726 · 1,730 · 1,737 · 1,744 · 1,746 · 1,762 ·
#     1,771 · 1,775 · 1,780        ortanca 1,744 · maksimum 1,780
#
# 🔴 **11 gözlemin 10'u yazılı 1,60'ın ÜSTÜNDE.** Yani `_gereken_zaman_asimi_s`
# gereken süreyi SİSTEMATİK OLARAK EKSİK tahmin ediyordu — ve bu, K-058'in
# kapıyı düşürüp sebebini YANLIŞ raporlayan hatasının **aynı sınıfıdır**:
# koruma geçerken kapı zaman aşımına düşebilir.
#
# 🔒 26 AĞUSTOS 2026 — ÇARPAN 1,60 -> 1,80 (K-066, öğrenci kararı).
# Ölçülen maksimumun (1,780) hemen üstü.
#
# ⚠️ SINIRI, KURALLA BİRLİKTE YAZILIYOR (Y11): bu ölçüm `Pool(6)` altında
# ve denetçinin kendi betikleri EŞZAMANLI koşarken yapıldı; kapı `Pool(8)`
# kullanıyor. 🔴 **`Pool(8)` çarpanı BUGÜNE KADAR HİÇ ÖLÇÜLMEDİ** — denetçinin
# kendi beyanı. 1,80 hâlâ bir ALT SINIR olabilir. Deponun kuralı geçerli:
# *"ölçülemeyen bir üst sınıra 'ölçüldü' denmez."*
#
# 🔒 Y12: sabit artık VERİYE BAĞLI. `OLCULEN_CEKISME` aşağıda duruyor ve
# `tests/test_kapi_secimleri.py::test_b90_*` çarpanın ölçülen maksimumun
# ALTINA düşmesini engelliyor.
# ==========================================================================

# Beşinci denetimin ölçtüğü 11 gözlem — tam paketi BİTİREN mutantlar,
# Pool(6), taban 768,56 sn. Üretici: aile0_audit.md §B-90.
OLCULEN_CEKISME = (1.5478, 1.6734, 1.7257, 1.7297, 1.7370, 1.7440,
                   1.7463, 1.7620, 1.7711, 1.7753, 1.7803)

CEKISME_CARPANI = 1.80
EMNIYET_PAYI = 1.50              # ölçüm boş makinede yapıldı; gerçek koşuda
                                 # arka planda başka iş olabilir

MUTANT_ZAMAN_ASIMI_S = 7200      # 🔴 27 Ağu: 3600 -> 7200 (120 dk).
                                 # Gereken: 1 850,63 × 1,80 × 1,50 =
                                 # 4 997 sn (83,3 dk) · marj 1,44×.
                                 # Eski 3600 sn YETMİYORDU ve hiçbir
                                 # test bunu görmüyordu (Y12'nin sınırı).
#   (26 Ağu: 2,5694 × 382 × 1,80 × 1,50 = 2 650 sn — EN KÖTÜ gözlemden.
#    Çarpan ARTIK ölçülen
#    maksimumun üstünde (B-90 kapandı, K-066).
#    ⚠️ Marj üç zincirde 1,81 -> 1,38'e indi: paket her zincirde
#    büyüyor. 3 600 sn bugün yeterli ama SONSUZ değil — paket ~2 400
#    sn'yi aşarsa zaman aşımı da büyütülmeli.
#    ⚠️ A-10 (AÇIK): en pahalı tek test 45,7 sn (b87 entegrasyonu,
#    2 tam koşu) — ortalama testin ~18 katı. `_gereken_zaman_asimi_s`
#    süreyi test SAYISIYLA doğrusal ölçekliyor ve bunu GÖRMEZ.)
TABAN_ZAMAN_ASIMI_S = 4200       # taban TEK başına koşar, çekişme yok
                                 # 🔴 27 Ağu: 1800 -> 4200 (70 dk).
                                 # Gereken: 1 850,63 × 1,50 = 2 776 sn
                                 # (46,3 dk) · marj 1,51×. Eski 1800 sn
                                 # TEMİZ bir tabanı 'kırık' raporladı —
                                 # K-058'in birebir tekrarı, ama kapı
                                 # koşulmadan önce görüldü.


@dataclass(frozen=True)
class Mutasyon:
    ad: str
    dosya: str
    eski: str
    yeni: str
    ne_bozuyor: str
    beklenen_yakalayici: str     # insan için: hangi sözleşme korunuyor
    beklenen_test: str           # 🔴 makine için: KIRILMASI GEREKEN test adı


MUTASYONLAR = [
    Mutasyon(
        ad="M1_dus_silindi",
        dosya="sim/kosucu.py",
        eski='        self.defter.dus("iletim_basarisiz", nereden="ucus")\n'
             '        self.mac_dusurmesi += 1',
        yeni='        self.mac_dusurmesi += 1',
        ne_bozuyor="MAC düşürmesinde defter güncellenmiyor — paket askıda kalıyor",
        beklenen_yakalayici="boşaltma kontrolü (Ç1.4), korunum DEĞİL",
        beklenen_test="test_c1_4_bosaltma_boruyu_bosaltiyor",
    ),
    Mutasyon(
        ad="M2_kanal_sirali_akisa_cevrildi",
        dosya="sim/mac.py",
        eski="        cekim = kanal_cekimi(self.kon.tohum, il.gonderen, alici,\n"
             "                             il.baslangic_s, self.kon.kanal_dilimi_s)",
        yeni="        cekim = self._rnd.random()   # MUTASYON: sirali akis",
        ne_bozuyor="Kanal çekimi durumsuz değil — protokoller farklı kanal görür",
        beklenen_yakalayici="Ç2.3 (iki kol aynı kanalı görüyor)",
        beklenen_test="test_c2_3_iki_kol_ayni_kanali_goruyor",
    ),
    Mutasyon(
        ad="M3_cca_gecikmesi_sifirlandi",
        dosya="sim/config.py",
        eski="    cca_s: float = 4e-6",
        yeni="    cca_s: float = 0.0",
        ne_bozuyor="Aynı slotta geri sayımı biten iki düğüm asla çarpışmaz",
        beklenen_yakalayici="aynı-slot çarpışma testi",
        beklenen_test="test_cca_ayni_slot_carpismasini_uretiyor",
    ),
    Mutasyon(
        ad="M4_yari_cift_yonlu_kaldirildi",
        dosya="sim/mac.py",
        eski="        g_bas, g_bit = self.gonderim_araligi[alici]\n"
             "        if g_bas < il.bitis_s and il.baslangic_s < g_bit:\n"
             "            return None",
        yeni="        pass   # MUTASYON: yari cift yonlu kontrolu YOK",
        ne_bozuyor="Bir düğüm gönderirken aynı anda alabiliyor",
        beklenen_yakalayici="yarı çift yönlü testi",
        beklenen_test="test_yari_cift_yonlu_sinr_den_bagimsiz_calisiyor",
    ),
    Mutasyon(
        ad="M5_girisim_menzili_daraltildi",
        dosya="sim/config.py",
        eski="        beta_lin = 10.0 ** (self.sinr_esigi_db / 10.0)\n"
             "        return beta_lin ** (1.0 / self.yol_kaybi_usteli)",
        yeni="        return 1.0001   # MUTASYON: girisim menzili = iletim menzili",
        ne_bozuyor="Gizli terminal geometrisi yok olur — Li replikasyonu imkânsız",
        beklenen_yakalayici="gizli terminal + girişim oranı testleri",
        beklenen_test="test_girisim_orani_turetilmis_ve_tutarli",
    ),
    Mutasyon(
        ad="M6_radyo_mesgul_kaldirildi",
        dosya="sim/mac.py",
        eski="        if self.kanal_mesgul(dugum) or self.radyo_mesgul(dugum):\n"
             "            self._geri_cekilme_planla(dugum)",
        yeni="        if self.kanal_mesgul(dugum):\n"
             "            self._geri_cekilme_planla(dugum)",
        ne_bozuyor="Düğüm kendi onayı havadayken kendi verisini gönderiyor (K-027)",
        beklenen_yakalayici="Li regresyon testi (plato kayar)",
        beklenen_test="test_uzun_zincir_platosu",
    ),
    Mutasyon(
        ad="M7_komsuluk_menzilden_turetildi",
        dosya="sim/kosucu.py",
        eski="        taze = tuple(k for k in self.komsu_tablosu[dugum].values()\n"
             "                     if simdi - k.son_duyulma_s <= omur)",
        yeni="        from .gozlem import KomsuKaydi as _KK\n"
             "        taze = tuple(_KK(j, simdi, 1, 0.0, 0,\n"
             "                         self.topo.konumlar[j])\n"
             "                     for j in self.topo.geometrik_komsular(dugum))",
        ne_bozuyor="Komşuluk beacon'dan değil MENZİL TABLOSUNDAN — kâhin",
        beklenen_yakalayici="Ç5.3 (t=0'da tablo boş, menzilden türetilmiyor)",
        beklenen_test="test_c5_3d_komsuluk_menzil_tablosundan_turetilmiyor",
    ),
]

# --------------------------------------------------------------------------
# 🔴 BAĞIMSIZ DENETİMİN MUTASYONLARI (19 Ağustos 2026)
#
# Sıfır bağlamlı bir denetçi bu 10 mutasyonu yazdı ve 8'i 198 testlik
# paketten SAĞ ÇIKTI. Kendi 7 mutasyonum 7/7 yakalanıyordu — ama onlar
# ZATEN TEST EDİLMİŞ yollardan seçilmişti. Seçim yanlılığı.
#
# Boşluklar `tests/test_denetim_boslukları.py` ile kapatıldı; bu liste
# kapanışın REGRESYONUDUR.
# --------------------------------------------------------------------------
MUTASYONLAR += [
    Mutasyon("D1_gozlem_bayt_sifirlandi", "sim/kosucu.py",
             "gonderilen_bayt=self.mac.dugum_gonderilen_bayt[dugum],",
             "gonderilen_bayt=0,",
             "Gozlem bayt alani bilgi tasimiyor",
             "test_b01_bayt_alanlari_dugume_ait_aga_degil",
             "test_b01_bayt_alanlari_dugume_ait_aga_degil"),
    Mutasyon("D2_gonderim_sonucu_tersine", "sim/kosucu.py",
             'self.son_sonuc[gonderen] = (sonuc, hedef)',
             'self.son_sonuc[gonderen] = ("zaman_asimi", hedef)',
             "Gonderim sonucu her zaman zaman_asimi",
             "test_b02_son_iletim_hedefi_gercek_komsuyu_tasiyor",
             "test_b02_son_iletim_hedefi_gercek_komsuyu_tasiyor"),
    Mutasyon("D3_komsu_tazelik_filtresi_kaldirildi", "sim/kosucu.py",
             "if simdi - k.son_duyulma_s <= omur)",
             "if True)",
             "Komsu hic bayatlamiyor",
             "test_d3_bayat_komsu_gozlemden_dusuyor",
             "test_d3_bayat_komsu_gozlemden_dusuyor"),
    # ⚠️ 26 AĞU (K-067): deseni B-98'in düzeltmesi bozdu — `bas, bit = ...`
    # ile `pencere = [...]` arasına bir yorum bloğu girdi ve mutasyon
    # UYGULANAMAZ oldu. Ucuz ön kontrol bunu **0,3 dk**'da yakaladı; kapı
    # 150 dk sonra yakalayacaktı. Desen artık FİLTRENİN KENDİSİNE bağlı,
    # komşu satırların arasına değil. Mutasyonun NİYETİ değişmedi.
    Mutasyon("D4_olcum_penceresi_isinmaya_tasti", "sim/kosucu.py",
             """        pencere = [p for p in self.trafik.uretilen_paketler
                   if bas <= p.dogum_s]""",
             """        bas -= 10.0   # MUTASYON: pencere isinmaya tasti
        pencere = [p for p in self.trafik.uretilen_paketler
                   if bas <= p.dogum_s]""",
             "Olcum penceresi 10 s isinmaya tasiyor",
             "test_d4_olcum_penceresi_isinmaya_tasmiyor",
             "test_d4_olcum_penceresi_isinmaya_tasmiyor"),
    Mutasyon("D5_beacon_bayti_sayilmiyor", "sim/mac.py",
             """        self.gonderilen_yayin += 1
        self.kontrol_bayt += bayt""",
             """        self.gonderilen_yayin += 1""",
             "Beacon bayti kontrol yukune yazilmiyor",
             "test_d5_beacon_baytlari_kontrol_yukune_yaziliyor",
             "test_d5_beacon_baytlari_kontrol_yukune_yaziliyor"),
    Mutasyon("D6_karistirici_girisim_yapmiyor", "sim/mac.py",
             """        if self.karistirici is not None:
            toplam += self.karistirici.alinan_guc_w(
                self.topo.konumlar[alici], an_s)
        return toplam""",
             """        return toplam""",
             "Karistirici veri aliminda girisim yapmiyor",
             "cok sayida test",
             "test_karistirici_alimi_bozuyor"),
    Mutasyon("D7_kanal_cekimi_cerceve_sonundan", "sim/mac.py",
             """        cekim = kanal_cekimi(self.kon.tohum, il.gonderen, alici,
                             il.baslangic_s, self.kon.kanal_dilimi_s)""",
             """        cekim = kanal_cekimi(self.kon.tohum, il.gonderen, alici,
                             il.bitis_s, self.kon.kanal_dilimi_s)""",
             "Kanal cekimi cerceve SONUNDAN anahtarlaniyor",
             "test_c2_3_iki_kol_ayni_kanali_goruyor",
             "test_c2_3_iki_kol_ayni_kanali_goruyor"),
    Mutasyon("D8_kuyruk_kapasitesi_bir_fazla", "sim/queues.py",
             "if len(self._paketler) >= self.kapasite:",
             "if len(self._paketler) > self.kapasite:",
             "Kuyruk kapasitesi fiilen +1",
             "test_d8_kuyruk_kapasitesi_tam_olarak_uyuluyor",
             "test_d8_kuyruk_kapasitesi_tam_olarak_uyuluyor"),
    Mutasyon("D9_yakinsama_esigi_anlamsizlastirildi", "sim/kosucu.py",
             '"yakinsadi": fark < 0.05,',
             '"yakinsadi": fark < 0.99,',
             "Yakinsama esigi her seyi 'yakinsadi' yapiyor",
             "test_d9_yakinsama_esigi_gercekten_ayirt_ediyor",
             "test_d9_yakinsama_esigi_gercekten_ayirt_ediyor"),
    Mutasyon("D10_beacon_sahte_konum", "sim/kosucu.py",
             '"konum": self.topo.konumlar[dugum],',
             '"konum": (0.0, 0.0),',
             "Beacon herkese (0,0) konumu bildiriyor",
             "test_d10_beacon_gercek_konum_bildiriyor",
             "test_d10_beacon_gercek_konum_bildiriyor"),
]


def zaman_asimi_sebebi(saniye: float) -> str:
    """Zaman aşımının rapor metni.

    🔴 Ayrı fonksiyon, çünkü satır içindeyken mutasyonla SINANAMIYORDU:
    metni "mutasyon uygulanamadı"ya çeviren mutasyon (M-C7) sağ kaldı —
    testler sınıflandırıcıyı çağırıyor, metni ÜRETEN yeri değil (Y11).
    """
    return (f"ZAMAN AŞIMI — {saniye:.0f} sn içinde bitmedi "
            f"(mutasyon UYGULANDI, paket bitiremedi)")


def desen_tutmadi_sebebi(dosya: str) -> str:
    """Mutasyon deseninin kaynakta bulunamamasının rapor metni."""
    return f"mutasyon uygulanamadı (desen kaynakta yok): {dosya}"


def gecersiz_sebebi(r: dict) -> str:
    """Geçersiz bir mutant koşusunun raporlanacak sebebi.

    🔴 Y7 — ARAÇ, YAPMADIĞI TEŞHİSİ RAPOR EDEMEZ (25 Ağustos 2026, K-058).

    Bu fonksiyon var, çünkü yerinde duran tek satır ("mutasyon uygulanamadı")
    **üç ayrı olayı** aynı etikete indiriyordu ve o etiket üçünden yalnızca
    birinde doğruydu:

    | gerçek olay | eski etiket | doğru mu |
    |---|---|---|
    | desen kaynakta yok | "mutasyon uygulanamadı" | ✅ |
    | alt süreç zaman aşımı | "mutasyon uygulanamadı" | 🔴 **HAYIR** — mutasyon UYGULANDI |
    | başka istisna | "mutasyon uygulanamadı" | 🔴 **HAYIR** |

    25 Ağustos'ta kapı Ç1.3'te düştü ve 31 mutant için "uygulanamadı" yazdı.
    Desen üç ayrı ölçümde 35/35 tuttu; gerçek olay zaman aşımıydı. Rapor,
    teşhisi kaynak deseni aramaya saptırdı — hiç orada olmayan bir hataya.

    Ayrı bir fonksiyon olmasının sebebi Y2: satır içindeyken mutasyonla
    sınanamıyordu ve fiilen sınanmamıştı (M-C6 sağ kalmıştı).
    """
    sebep = r.get("hata")
    if not sebep:
        # Y7 — "hata" alanı var ama boşsa sessizce doğru görünmemeli
        return f"geçersiz (sebep BİLDİRİLMEDİ · tür={r.get('tur', '?')})"
    return str(sebep)


def cokme_sebebi(cikis_kodu: int, stdout: str) -> str | None:
    """Mutant koşusu ÇÖKTÜ mü, ve **neden**? `None` = çökme yok.

    🔴 Y7 — B-88 (BEŞİNCİ DENETİM, 26 Ağustos 2026).

    Burada **elle yazılmış tek bir etiket** vardı:

        gecersiz.append((r["ad"], "mutant koşturulamadı (çökme/collect hatası)"))

    ve K-058'in kapattığı hatanın **birebir aynısını**, bir katman yukarıda
    tekrarlıyordu: **üç ayrı olay tek etikete iniyordu.** Beşinci denetim
    mutasyonla sınadı — o satırın etiketini K-058'in *yanlış olduğu ölçülen*
    etiketiyle değiştirdi ve **367 testin 367'si geçti.** Yani kapı, aynı
    yanlış teşhisi bir daha yapabilirdi ve hiçbir test konuşmazdı.

    🔴 VE İKİNCİ KUSUR AYNI SATIRDAYDI (A-9): çökme ölçütü
    `"ERROR" in p.stdout` idi — bir **alt dizgi araması**, teşhis değil.
    `pytest` her başarısız `assert` için özet satırında **"AssertionError"**
    basar ve içinde `"ERROR"` geçer; yani ölçüt, testleri kıran **her**
    mutantta `True` oluyordu. Zarar vermiyordu çünkü ikinci koşul
    (`not r["sayi"]`) onu bastırıyordu — yani koruma **tesadüfen** işliyordu.

    Ayrı bir fonksiyon olmasının sebebi Y2: satır içindeyken mutasyonla
    sınanamıyordu. Zorlayan test:
    `tests/test_kapi_secimleri.py::test_b88_*`
    """
    satirlar = stdout.splitlines()
    if any("during collection" in s for s in satirlar):
        return ("collect hatası — mutant import/collect EDİLEMEDİ, "
                "hiçbir test koşmadı")
    if any(s.startswith("ERROR ") for s in satirlar):
        return ("pytest ERROR bölümü — test KURULUMU düştü "
                "(fixture/import), değişmez sınanmadı")
    if cikis_kodu not in (0, 1):
        return f"pytest standart dışı çıkış kodu: {cikis_kodu}"
    return None


def _kosu(m: Mutasyon) -> dict:
    gecici = Path(tempfile.mkdtemp(prefix=f"mut_{m.ad}_"))
    try:
        hedef = depoyu_kopyala(gecici / "depo")
        yol = hedef / m.dosya
        metin = yol.read_text(encoding="utf-8")
        if m.eski not in metin:
            return {"ad": m.ad, "tur": "desen",
                    "hata": desen_tutmadi_sebebi(m.dosya)}
        yol.write_text(metin.replace(m.eski, m.yeni, 1), encoding="utf-8")

        p = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-q", "--tb=no",
             "-p", "no:cacheprovider"],
            cwd=hedef, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=MUTANT_ZAMAN_ASIMI_S,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        kirilan = [s.split()[1].split("::")[-1]
                   for s in p.stdout.splitlines()
                   if s.startswith("FAILED") and len(s.split()) > 1]
        # Çökme de bir yakalamadır (istisna fırlatan mutasyon).
        # 🔴 B-88/A-9: artık alt dizgi araması değil, TİPLİ bir teşhis.
        sebep = cokme_sebebi(p.returncode, p.stdout)
        return {"ad": m.ad, "kirilan": kirilan, "sayi": len(kirilan),
                "cokme": sebep is not None, "cokme_sebebi": sebep,
                "ne_bozuyor": m.ne_bozuyor,
                "beklenen": m.beklenen_yakalayici}
    # 🔴 Y7 — ZAMAN AŞIMI, "DESEN BULUNAMADI" DEĞİLDİR (25 Ağu 2026, K-058).
    #
    # Bu iki durum tek bir `"hata"` alanına düşüyordu ve raporlama katmanı
    # ikisine de sabit "mutasyon uygulanamadı" etiketini basıyordu. O etiket
    # KAYNAK DESENİ hakkında bir iddiadır; zaman aşımında araç desene hiç
    # bakmamıştır bile — desen zaten TUTMUŞTUR, mutasyon UYGULANMIŞTIR.
    #
    # Kapı 25 Ağustos'ta tam olarak böyle düştü: 31 mutant için "uygulanamadı"
    # yazdı, desen üç ayrı ölçümde 35/35 tuttu, gerçek olay zaman aşımıydı.
    # Raporun kendisi teşhisi YANLIŞ YÖNE saptırdı.
    except subprocess.TimeoutExpired as e:
        return {"ad": m.ad, "tur": "zaman_asimi",
                "hata": zaman_asimi_sebebi(e.timeout)}
    except Exception as e:                       # noqa: BLE001
        return {"ad": m.ad, "tur": "istisna", "hata": repr(e)[:200]}
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


# --------------------------------------------------------------------------
# 🔴 BU OTURUMUN BULGULARI (19 Ağustos 2026) — B-06/B-07/B-14/B-22/B-23
#
# Her biri, bu oturumda kapatılan bir boşluğun REGRESYONUDUR. D11–D13 özellikle
# önemli: üçü de, `abs=0.0` düzeltmesinden ÖNCE hiçbir testi kırmıyordu.
# --------------------------------------------------------------------------
MUTASYONLAR += [
    Mutasyon("D11_girisim_toplamsal_degil", "sim/mac.py",
             """            if baska.baslangic_s <= an_s < baska.bitis_s:
                toplam += self.radyo.alinan_guc_w(
                    self.topo.mesafe(baska.gonderen, alici))""",
             """            if baska.baslangic_s <= an_s < baska.bitis_s:
                toplam = max(toplam, self.radyo.alinan_guc_w(
                    self.topo.mesafe(baska.gonderen, alici)))""",
             "Girisim toplamsal degil, EN GUCLU olan aliniyor",
             "Ç3.1 (girisim toplamsal)",
             "test_c3_1_girisim_toplamsal"),
    Mutasyon("D12_karistirici_gucu_iki_kat", "sim/radio.py",
             "        return self.guc_w / db_to_lin(pl_db)",
             "        return 2.0 * self.guc_w / db_to_lin(pl_db)",
             "Karistiricinin alicida yarattigi guc 2 KAT (+3,01 dB)",
             "B-23 (mutlak analitik kontrol)",
             "test_b23_karistirici_alinan_gucu_kapali_formla_birebir"),
    Mutasyon("D13_tepe_telafisi_cakili", "sim/config.py",
             "        return 10.0 * math.log10(1.0 / self.darbe_gorev_cevrimi)",
             "        return 10.0 * math.log10(1.0 / 0.5)",
             "Tepe telafisi gorev cevriminden turetilmiyor (eski modul sabiti)",
             "Ç3.3 (darbeli ortalama guc, parametrize)",
             "test_c3_3_darbeli_ortalama_guc_kosan_sistemde_esit"),
    Mutasyon("D14_uygulanmamis_bayrak_sessizce_kabul", "sim/config.py",
             "        for _ad in self.UYGULANMAMIS_BAYRAKLAR:",
             "        for _ad in ():",
             "Bildirilmis ama uygulanmamis bayrak sessizce True yapilabiliyor",
             "B-06 (bildirim != kullanim)",
             "test_b06_bildirilen_her_bool_bayrak_ya_etkilidir_ya_hata_verir"),
    # ⚠️ Mutasyon SON iki alana uygulanır. İlk yazımı `darbeli`/`periyot_s`e
    # varsayılan koyuyordu ve dataclass KURULAMIYORDU ("varsayılansız alan
    # varsayılanlının ardından gelemez") — yani mutant hiç import edilemiyor,
    # 0 test "kırılıyor" ve araç bunu YAKALANMADI sanıyordu. Geçersiz bir
    # mutasyon, korumasız bir kod yolunun kanıtı değildir.
    Mutasyon("D15_karistirici_varsayilanlari_geri", "sim/radio.py",
             """    hiz_ms: float
    yorunge_yaricap_m: float""",
             """    hiz_ms: float = 15.0
    yorunge_yaricap_m: float = 300.0""",
             "Karistirici alanlarina varsayilan geri geldi (ikinci dogru kaynagi)",
             "B-14 (varsayilan yasagi)",
             "test_b14_karistiricinin_hicbir_alaninda_varsayilan_yok"),
]

# --------------------------------------------------------------------------
# 🔴 KÖR TARAMANIN SAĞ KALANLARI (19 Ağustos 2026)
#
# `kor_mutasyon.py` temiz tabanla koşunca 12 mutant sağ kaldı.
# `sag_kalan_ayikla.py` 44 koşuluk bir matriste ölçtü: 4'ü davranışı
# GERÇEKTEN değiştiriyordu. Bunlar o dördünün regresyonudur.
#
# ⚠️ S04 ana matriste "eşdeğer" görünüyordu — `ttl_olumu` orada 0'dır.
# Uç durumlar eklenince karar döndü. Y8'in somut hâli.
# --------------------------------------------------------------------------
MUTASYONLAR += [
    Mutasyon("D16_ttl_olumu_bir_gec", "sim/kosucu.py",
             "        elif paket.ttl <= 0:",
             "        elif paket.ttl < 0:",
             "TTL sifira dusen pakete bir atlama daha hediye ediliyor",
             "S04 (TTL sinir degismezi)",
             "test_s04_ttl_sifira_dusunce_paket_olur"),
    Mutasyon("D17_toplam_deneme_isareti", "sim/mac.py",
             "        self.toplam_deneme += 1",
             "        self.toplam_deneme -= 1",
             "toplam_deneme sayaci ters yone sayiyor",
             "S05 (deneme >= iletim degismezi)",
             "test_s05_toplam_deneme_iletim_sayisindan_az_olamaz"),
    Mutasyon("D18_kopya_alim_isareti", "sim/mac.py",
             "                self.kopya_alim += 1        # kopya: veri atilir, onay YINE gider",
             "                self.kopya_alim -= 1        # kopya: veri atilir, onay YINE gider",
             "kopya_alim sayaci ters yone sayiyor (onay kaybinin kaniti)",
             "S07 (kopya alim degismezi)",
             "test_s07_kopya_alim_negatif_olamaz_ve_gerceklesiyor"),
    Mutasyon("D19_atlama_sayisi_isareti", "sim/packet.py",
             "        self.atlama_sayisi += 1",
             "        self.atlama_sayisi -= 1",
             "atlama_sayisi ters yone sayiyor (ortalama_atlama RAPORA GIRER)",
             "S08 (sayac ile ziyaret listesi tutarliligi)",
             "test_s08_atlama_sayisi_ziyaret_listesiyle_tutarli"),
]

# --------------------------------------------------------------------------
# 🔴 B-09 / B-10 REGRESYONU (19 Ağustos 2026, K-040)
# --------------------------------------------------------------------------
MUTASYONLAR += [
    # ⚠️ İLK YAZIMI HATALIYDI ve kapı raporu onu YAKALADI (K-042).
    # `slot_s`i 1 ns yapmak marjı BOZMUYOR: baskın terim önbelgedir (192 µs).
    # Ölçüldü: en küçük ara 688 → 628 µs, eşik 229 → 209 µs, dilim hâlâ
    # 100 µs — değişmez tutuyor. Mutasyon "yakalandı" sayılıyordu ama onu
    # kıran testler zamanlamayla ilgili BAŞKA testlerdi.
    # Doğrusu: K-024'ün MARJ KARARINI geri al (100 µs → 1 ms).
    Mutasyon("D20_kanal_dilimi_marji_bozuldu", "sim/config.py",
             "    kanal_dilimi_s: float = 1e-4",
             "    kanal_dilimi_s: float = 1e-3",
             "Kanal dilimi 1 ms'ye geri -> marj degismezi kirilir",
             "B-09 (Ç6.2 artik gercek degismez)",
             "test_dilim_en_kucuk_cerceveyle_bile_guvenli"),
    Mutasyon("D21_beacon_fazi_trafik_akisina_bindi", "sim/kosucu.py",
             '        r = self.akislar["beacon_faz"]',
             '        r = self.akislar["trafik_zamani"]',
             "Beacon fazi kendi akisi yerine CBR akisindan cekiliyor",
             "B-10 (her akis ya kullanilir ya beyan edilir)",
             "test_b10_her_akis_ya_kullaniliyor_ya_beyan_edilmis"),
]

# --------------------------------------------------------------------------
# 🔴 B-19 / B-20 REGRESYONU (19 Ağustos 2026, K-041)
# --------------------------------------------------------------------------
MUTASYONLAR += [
    Mutasyon("D22_ortak_alt_kume_semasi_bozuldu", "sim/kosucu.py",
             '            "teslim_kimlikleri": [p.kimlik for p in teslim],',
             '            "teslim_kimlikleri": [],',
             "Sonuc semasi paket bazli teslim bilgisini tasimiyor",
             "B-19 (ortak alt kume karsilastirmasi)",
             "test_b19_ortak_alt_kume_secilim_yanliligini_ortaya_cikariyor"),
    Mutasyon("D23_onay_airtime_i_sayilmiyor", "sim/mac.py",
             """        self.kontrol_bayt += self.kon.onay_bayt
        self.kontrol_airtime_s += sure                   # B-20""",
             """        self.kontrol_bayt += self.kon.onay_bayt""",
             "Onay cerceveleri kontrol airtime'ina yazilmiyor",
             "B-20 (airtime = cerceve sayisi x sure)",
             "test_b20_airtime_cerceve_surelerinin_toplamina_esit"),
]

# --------------------------------------------------------------------------
# 🔴 İKİNCİ BAĞIMSIZ DENETİMİN SAĞ KALANLARI (20 Ağustos 2026, K-044)
#
# Denetçi 10 yeni mutasyon yazdı, 7'si 240 testten sağ çıktı. Beşinin
# davranışı fiilen değiştirdiği ayrıca ölçüldü; bunlar o beşin regresyonu.
# (Diğer ikisi "tüketicisi yok" sınıfıydı → B-27b, test_gozlem.py)
# --------------------------------------------------------------------------
MUTASYONLAR += [
    Mutasyon("D24_kesisim_orani_sabit", "sim/karsilastirma.py",
             "        return self.ortak_paket / self.pencere_paket if self.pencere_paket else 0.0",
             "        return 1.0",
             "Kesisim orani sabit 1.0 — rapora giren metrik yalan soyluyor",
             "B-27/KM1 (kesisim orani bagimsiz sayimla)",
             "test_km1_kesisim_oranlari_bagimsiz_sayimla_ayni"),
    Mutasyon("D25_komsu_omru_yuz_kat", "sim/config.py",
             "    komsu_omru_katsayisi: float = 10.0",
             "    komsu_omru_katsayisi: float = 1000.0",
             "Komsu omru 100 kat — bayat komsu hic dusmuyor",
             "B-27/KM2 (omur mutlak degeriyle baglayici)",
             "test_km2_komsu_omru_MUTLAK_degeriyle_baglayici"),
    Mutasyon("D26_yorunge_yonu_ters", "sim/radio.py",
             "        aci = 2.0 * math.pi * ((self.hiz_ms * zaman_s) / cevre + self.faz_kesri)",
             "        aci = -2.0 * math.pi * ((self.hiz_ms * zaman_s) / cevre + self.faz_kesri)",
             "Hareketli karistirici ters yone doluyor (S5'in TUM kosulari)",
             "B-27/KM3 (yorunge kapali formla)",
             "test_km3_yorunge_yonu_kapali_formla_ayni"),
    Mutasyon("D27_deneme_siniri_bir_eksik", "sim/mac.py",
             "        if m.deneme > self.kon.yeniden_deneme_siniri:",
             "        if m.deneme >= self.kon.yeniden_deneme_siniri:",
             "Paket basina iletim 5 yerine 4 — K-039'un bag tanimini da kaydirir",
             "B-27/KM4 (iletim sayisi sinirla uyusuyor)",
             "test_km4_paket_basina_iletim_sayisi_sinirla_tam_uyusuyor"),
    Mutasyon("D28_kanal_cekimi_aliciya_duyarsiz", "sim/rng.py",
             '        struct.pack("<i", int(alan)),',
             '        b"",',
             "Kanal cekimi aliciyi gormuyor — Ç2.3'un kapsami sanildigindan dar",
             "B-27/KM5 (cekim aliciya duyarli)",
             "test_km5_kanal_cekimi_aliciya_duyarli_kosan_sistemde"),
]


def taban_kontrolu() -> tuple[bool, str]:
    """🔴 Y7 — MUTASYONSUZ KOPYADA TEST PAKETİ GEÇİYOR MU?

    Geçmiyorsa "yakalandı" sayımı ANLAMSIZDIR: zaten kırık olan bir test her
    mutantta kırılır ve araç %100 skor uydurur. Tam olarak bu yaşandı
    (dosya başlığına bakın).

    ⚠️ Kontrol, mutantlarla AYNI YOLDAN yapılır — aynı `copytree`, aynı
    `cwd`, aynı pytest çağrısı. Farklı bir yoldan yapılsaydı, kopyalama
    kaynaklı bir kırıklığı göremezdi.

    🔴 VE UZUN SÜRE ÖYLE DEĞİLDİ (B-100, altıncı denetim). Bu fonksiyon
    `"*.txt"`i dışlıyordu, `_kosu` dışlamıyordu: iddia edilen *"aynı yol"*
    ölçülmemişti ve tutmuyordu. İkisi de artık `depoyu_kopyala()` çağırıyor —
    tek uygulama, ayrışacak ikinci liste yok.
    """
    gecici = Path(tempfile.mkdtemp(prefix="mut_taban_"))
    try:
        hedef = depoyu_kopyala(gecici / "depo")
        p = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-q", "--tb=line",
             "-p", "no:cacheprovider"],
            cwd=hedef, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=TABAN_ZAMAN_ASIMI_S,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        son = [x for x in p.stdout.splitlines()
               if " passed" in x or " failed" in x]
        return p.returncode == 0, (son[-1] if son else p.stdout[-300:])
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


def paketi_kostur() -> dict:
    """🔴 TEK GİRİŞ NOKTASI — hem `main()` hem kapı raporu bunu çağırır.

    İki ayrı uygulama olsaydı, kapı raporu taban kontrolünü atlayabilirdi;
    K-033'ün dersi tam olarak buydu.

    Dönen sözlük:
        taban_tamam / taban_ozet     : Y7 koşulu
        sonuclar                     : mutasyon başına ham çıktı
        yakalanan / toplam           : kaç mutasyon en az bir test kırdı
        beklenen_kirilmadi           : beklenen testi KIRILMAYAN mutasyonlar
        evrensel_kiricilar           : TÜM mutantlarda kırılan testler (uyarı)
        gecti                        : üç koşul birden
    """
    taban_tamam, taban_ozet = taban_kontrolu()
    if not taban_tamam:
        return {"taban_tamam": False, "taban_ozet": taban_ozet,
                "sonuclar": [], "yakalanan": 0, "toplam": len(MUTASYONLAR),
                "beklenen_kirilmadi": [], "evrensel_kiricilar": [],
                "gecti": False}

    with Pool(min(len(MUTASYONLAR), 8)) as havuz:
        sonuclar = havuz.map(_kosu, MUTASYONLAR)

    beklenen = {m.ad: m.beklenen_test for m in MUTASYONLAR}
    yakalanan = 0
    beklenen_kirilmadi: list[tuple[str, str]] = []
    kirilan_kumeler: list[set[str]] = []

    gecersiz: list[tuple[str, str]] = []
    for r in sonuclar:
        if "hata" in r:
            gecersiz.append((r["ad"], gecersiz_sebebi(r)))
            continue
        # 🔴 Y7 — ÇÖKME "YAKALANMADI" DEĞİLDİR.
        # Mutant import/collect edilemiyorsa hiçbir test KIRILMAZ (0 FAILED)
        # ve araç bunu "korumasız kod yolu" sanar. İlk koşuda tam olarak bu
        # oldu: D15, dataclass'ı kurulamaz yapıyordu. Geçersiz bir mutasyon
        # ne kanıt ne de suçlamadır — ayrı raporlanır ve kapıyı DÜŞÜRÜR,
        # çünkü o mutasyon hiçbir şey ölçmemiştir.
        if r["cokme"] and not r["sayi"]:
            # 🔴 B-88: DÖRDÜNCÜ geçersizlik yolu. Etiket artık elle
            # yazılmıyor; `cokme_sebebi()` üretiyor ve o mutasyonla
            # sınanabiliyor (K-058'in dersi, bir katman yukarıda).
            gecersiz.append((r["ad"], r.get("cokme_sebebi")
                             or "çökme sebebi BİLDİRİLMEDİ (Y7)"))
            continue
        if r["sayi"]:
            yakalanan += 1
        kirilan_kumeler.append(set(r["kirilan"]))
        bek = beklenen[r["ad"]]
        # ⚠️ Parametrize edilmiş testler `test_x[0.25]` diye raporlanır.
        # Düz `in` karşılaştırması Ç3.3 gibi parametrize kapıları YANLIŞLIKLA
        # "beklenen kırılmadı" sayardı — kapı sebepsiz düşerdi.
        r["beklenen_kirildi"] = any(
            t == bek or t.startswith(bek + "[") for t in r["kirilan"])
        if not r["beklenen_kirildi"]:
            beklenen_kirilmadi.append((r["ad"], bek))

    # ⚠️ Taban temiz olsa bile: her mutantta kırılan bir test, mutasyona
    # DUYARSIZ bir kırıklığın işaretidir. Kapıyı düşürmez, ama görünür olur.
    evrensel = sorted(set.intersection(*kirilan_kumeler)) if kirilan_kumeler else []

    return {"taban_tamam": True, "taban_ozet": taban_ozet,
            "sonuclar": sonuclar, "yakalanan": yakalanan,
            "toplam": len(MUTASYONLAR),
            "beklenen_kirilmadi": beklenen_kirilmadi,
            "gecersiz": gecersiz,
            "evrensel_kiricilar": evrensel,
            "gecti": (yakalanan == len(MUTASYONLAR)
                      and not beklenen_kirilmadi and not gecersiz)}


def liste_dogrula(adet: int | None = None) -> str | None:
    """🔴 B-149 (Y7) — ARAC NE KOSTUGUNU KENDISI DOGRULAR.

    Doner: sorun varsa hata metni, yoksa `None`.

    🔒 NEDEN AYRI FONKSIYON: bu denetim once `main()`in govdesindeydi ve
    Y12 kampanyasi onu GERI ALAN bir mutasyonu YAKALAYAMADI — cunku
    koruma `BEKLENEN_MUTASYON` ADININ `main()`de gectigini sinamisti ve
    ad, kontrol `if False:` yapildiktan sonra da hata METNINDE duruyordu.
    `03` B5'in *"bildirim != kullanim"* tuzagi, korumanin kendisinde.
    Ayri bir yuklem DAVRANISSAL olarak sinanabilir (`03` B5: *"karar
    ureten yuklemlerini AYRI ve test edilebilir yaz"*).

    Neyi engelliyor: alti yeni mutasyon `if __name__ == "__main__"`
    blogunun ALTINA eklenmisti; betik yolu 35, ice aktarma yolu 41
    goruyordu ve `main()` bunu hic denetlemedigi icin
    `✅ Ç1.3 GECTI — 35/35` basip cikis kodu 0 veriyordu.
    """
    from dogrulama.aile0_kapi_raporu import BEKLENEN_MUTASYON
    n = len(MUTASYONLAR) if adet is None else adet
    if n != BEKLENEN_MUTASYON:
        return (f"LISTE {n} != kapinin bekledigi {BEKLENEN_MUTASYON} — "
                f"paket EKSIK ya da FAZLA kosardi. (B-149: blok "
                f"`__main__` korumasinin ALTINDA kalmis olabilir.)")
    return None


def main() -> None:
    print("=" * 78)
    print("MUTASYON PAKETİ — testlerimiz gerçekten bir şey ölçüyor mu?")
    print("=" * 78)
    # 🔴 B-149 — BETIK YOLU KENDI SAYISINI DOGRULAR (Y7).
    sorun = liste_dogrula()
    if sorun:
        print(f"🔴 {sorun}")
        sys.exit(1)
    print(f"{len(MUTASYONLAR)} mutasyon, her biri TAM test paketiyle sınanıyor.")
    # Ölçüldü: 22 mutasyon → 18,0/18,2 dk · 26 mutasyon → 22,2 dk
    # (19 Ağustos 2026). 26 mutasyonda 22,2 dk. Tahmin değil, ölçüm.
    print("Tahmini süre: ~3 dk taban + ~19 dk mutasyonlar (paralel) = ~22 dk")
    print()

    t0 = time.perf_counter()
    print("TABAN KONTROLU — mutasyonsuz kopyada test paketi geçiyor mu? (Y7)")
    r = paketi_kostur()
    print(f"  {r['taban_ozet']}")
    if not r["taban_tamam"]:
        print()
        print("!! TABAN KIRIK — mutasyonsuz kopyada testler geçmiyor.")
        print("   'Yakalandı' sayımı ANLAMSIZ olurdu; paket durduruldu.")
        print("   🔴 Ç1.3 GEÇMEDİ.")
        sys.exit(1)
    print("  OK taban temiz — 'yakalandı' sayımı anlamlı")
    print()

    for s_ in r["sonuclar"]:
        print("-" * 78)
        if "hata" in s_:
            print(f"🔴 {s_['ad']}: {s_['hata']}")
            continue
        if not s_["sayi"]:
            durum = "🔴 YAKALANMADI"
        elif not s_["beklenen_kirildi"]:
            durum = "🔴 YANLIŞ TEST"
        else:
            durum = "✅ YAKALANDI"
        print(f"{durum}  {s_['ad']}")
        print(f"    bozan     : {s_['ne_bozuyor']}")
        print(f"    beklenen  : {s_['beklenen']}")
        print(f"    kırılan   : {s_['sayi']} test")
        for t in s_["kirilan"][:6]:
            print(f"                {t}")
        if s_["sayi"] > 6:
            print(f"                ... +{s_['sayi']-6} test daha")

    if r.get("gecersiz"):
        print()
        print("!" * 78)
        print("🔴 GEÇERSİZ MUTASYON — mutant koşturulamadı, hiçbir şey ölçmedi:")
        for ad, sebep in r["gecersiz"]:
            print(f"     {ad}  ({sebep})")
        print("   Çökme YAKALANMA DEĞİLDİR; mutasyon düzeltilmeden kapı geçmez.")
        print("!" * 78)

    if r["evrensel_kiricilar"]:
        print()
        print("!" * 78)
        print("⚠️ EVRENSEL KIRICI — bu test(ler) TÜM mutantlarda kırıldı:")
        for t in r["evrensel_kiricilar"]:
            print(f"     {t}")
        print("   Mutasyona duyarsız olabilir; taban temiz olsa bile denetlenmeli.")
        print("!" * 78)

    print()
    print("=" * 78)
    print(f"Süre: {(time.perf_counter()-t0)/60:.1f} dk")
    if r.get("gecersiz"):
        print("🔴 Ç1.3 GEÇMEDİ — geçersiz mutasyon var (yukarı bakın).")
        sys.exit(1)
    if r["beklenen_kirilmadi"]:
        print("🔴 Ç1.3 GEÇMEDİ — beklenen testi kırılmayan mutasyonlar:")
        for ad, bek in r["beklenen_kirilmadi"]:
            print(f"     {ad}  ->  {bek}")
        print("   Bir mutasyonun 'yakalanması', DOĞRU testin kırılması demektir.")
        sys.exit(1)
    print(f"✅ Ç1.3 GEÇTİ — {r['yakalanan']}/{r['toplam']} mutasyon, "
          f"her biri KENDİ beklenen testiyle yakalandı (taban temiz).")




# --------------------------------------------------------------------------
# 🔴 B-149 · B-150 (SEKIZINCI DENETIM) — BU BLOK TASINDI VE YENIDEN
# NUMARALANDI.
#
# B-149: blok `if __name__ == "__main__": main()` korumasinin ALTINDAYDI.
# Olculdu (AST ile modul govdesi koruma dugumune kadar calistirilarak):
#     ice aktarma yolu (kapinin yolu) : len(MUTASYONLAR) = 41  ✅
#     betik  yolu (belgelenmis komut) : len(MUTASYONLAR) = 35  🔴
# ve `main()` `BEKLENEN_MUTASYON`u HIC kontrol etmiyordu (o kontrol
# yalnizca `aile0_kapi_raporu.py:521`de). Yani
# `python dogrulama/mutasyon_paketi.py` "✅ Ç1.3 GECTI — 35/35" basip
# cikis kodu 0 veriyordu. Y12'nin "elle tutulan sabit" dersinin ikizi:
# bu kez sabit DOGRU, KOD YOLU yanlisti.
#
# B-150: `D26` `D27` `D28` IKISER mutasyon adlandiriyordu
# (radio/mac/rng <-> karsilastirma). Tam adlar benzersiz oldugu icin
# arac calisiyordu, ama kayitlardaki "D26" gondermesi TEKIL DEGILDI.
# 🔒 Bos aralik: D32-D37.
# --------------------------------------------------------------------------
# 🔴 B-131 (YEDINCI BAGIMSIZ DENETIM) — `sim/karsilastirma.py` PAKETE GIRDI
#
# Modul 322 satir ve Aile 1'in HER gecikme karsilastirmasi ondan geciyor;
# pakette YALNIZCA 1 mutasyon vardi (kosucu 11 · mac 11). B0.5 modulun
# kapsamini olctu (16 hedefli mutasyon) ve 6'sinin SAG KALDIGINI buldu;
# altisi da kapatildi. 🔴 Ama o 16 mutasyon PAKETE GIRMEDIGI icin kapi
# modulu hala 1 mutasyonla sinayacakti — Y13: bir kapanis iddiasi,
# degisikligin KODDA bulundugu gosterilmeden kayda gecmez.
#
# 🔒 NEDEN 16 DEGIL 6: kapi her mutant icin TAM PAKETI kosuyor
# (`Pool(8)`). 16 mutasyon ~2 dalga, ~60-70 dk ekler. Zaten yakalanan
# 10 mutasyon pakete girse de kapiya ek GUVENCE getirmez — paket onlari
# nasilsa yakaliyor. Eklenenler, denetimde SAG KALMIS ve B0.5'te
# kapatilmis ALTI KANITLANMIS BOSLUKTUR: biri silinirse kapi konusur.
# --------------------------------------------------------------------------
MUTASYONLAR += [
    Mutasyon('D32_gecikme_farki_ISARET', "sim/karsilastirma.py",
             '        return self.ortalama_gecikme_b_s - self.ortalama_gecikme_a_s',
             '        return self.ortalama_gecikme_a_s - self.ortalama_gecikme_b_s',
             "Gecikme farkinin ISARETI ters — 'kotulesti' ile 'iyilesti' yer degistirir",
             'B-120 denetimi / M2 (sag kalmisti)',
             'test_b05_gecikme_ve_p95_farkinin_YONU_dogru'),
    Mutasyon('D33_p95_farki_ISARET', "sim/karsilastirma.py",
             '        return self.yuzdelik_b["p95"] - self.yuzdelik_a["p95"]',
             '        return self.yuzdelik_a["p95"] - self.yuzdelik_b["p95"]',
             "p95 farkinin ISARETI ters — §8.1b'nin butun yargisi tersine doner",
             'B-120 denetimi / M3 (sag kalmisti)',
             'test_b05_gecikme_ve_p95_farkinin_YONU_dogru'),
    Mutasyon('D34_kontrol_payi_PAYDA', "sim/karsilastirma.py",
             '    return {"bayt": 100.0 * kb / (kb + vb),',
             '    return {"bayt": 100.0 * kb / vb,',
             "Kontrol payinin paydasi TOPLAM degil — oran %100'u asabilir",
             'B-120 denetimi / M7 (sag kalmisti)',
             'test_b05_kontrol_payi_paydasi_TOPLAM_pay_degil'),
    Mutasyon('D35_evren_hash_KONTROLU_YOK', "sim/karsilastirma.py",
             '    if sonuc_a["pencere_evren_hash"] != sonuc_b["pencere_evren_hash"]:',
             '    if False:',
             'B-26 geri alinir: farkli PAKET EVRENI karsilastirilir (Y11: kurulum_hash golgeliyordu)',
             'B-120 denetimi / M12 (sag kalmisti)',
             'test_b05_EVREN_hash_kontrolu_BAGIMSIZ_calisiyor'),
    Mutasyon('D36_uzunluk_KONTROLU_YOK', "sim/karsilastirma.py",
             '        if len(kim) != len(gec):',
             '        if False:',
             'B-67 geri alinir: `dict(zip())` sessizce KIRPAR (Y11: E5 golgeliyordu)',
             'B-120 denetimi / M13 (sag kalmisti)',
             'test_b67_SATIR_ICI_bozuk_yapi_reddediliyor'),
    Mutasyon('D37_kardinalite_KONTROLU_YOK', "sim/karsilastirma.py",
             '        if uretilen is not None and len(kim) > uretilen:',
             '        if False:',
             "B-85 geri alinir: kesisim orani %100'u asabilir (denetci %328,5 gormustu)",
             'B-120 denetimi / M15 (sag kalmisti)',
             'test_b05_KARDINALITE_kontrolu_calisiyor'),
]


if __name__ == "__main__":
    main()
