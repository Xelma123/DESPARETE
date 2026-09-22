"""
Parametre kökenleri — HER SAYININ NEREDEN GELDİĞİ, tek kaynakta.

🔴 NEDEN BU DOSYA VAR
=====================
8 Eylül 2026'da ölçüldü: davranış belirleyen **108 sayısal parametrenin**
çoğunun değeri gerekçesizdi. Yorumlar *"bu parametre neden VAR"* sorusunu
cevaplıyordu, *"neden BU DEĞER"* sorusunu değil. `kuyruk_kapasitesi = 50`ın
yanında *"sonsuz kuyruk yasak"* yazıyordu — neden 50 olduğu yazmıyordu.

Sonucu şuydu: her şey belgelenmiş **görünüyor**, hiçbiri doğrulanamıyordu.
Ve o gün bulunan kusurların hepsi bu boşluktan çıktı — kimsenin kullanmadığı
bir grafikte yapılmış kalibrasyon, ölçülmemiş bir yol kaybı üsteli,
gerekçesiz bir bağ eşiği.

🔒 ÇÖZÜM YAPISAL, DİSİPLİN DEĞİL
================================
`Konfig`in HER alanı burada bir kovaya yazılmak zorundadır. Eksik alan
`Konfig` kurulurken **patlar** — yani gerekçesiz bir parametre depoya
giremez. Bu, `cekirdek/sayaclar.py`nin sayaçlar için yaptığının parametreler
için yapılmış hâlidir.

🔴 `SINANMAMIS` BİR KOVA, BİR MAZERET DEĞİL
===========================================
Bugün alanların çoğu orada ve bu **kasten** böyle: duyarlılık denetimi
yapılmadan hiçbir şeye *"duyarsız"* denemez, `02`de doğrulanmadan hiçbir
şeye *"kaynak"* denemez. Kova sistemi borcu ödemez, **görünür ve sayılabilir**
kılar.

    🔒 ÖN-KAYIT MÜHÜRLENMEDEN ÖNCE `SINANMAMIS` SAYISI SIFIR OLMALIDIR.

⭐ Ve şunu gösterir: 802.11b'nin MAC sabitleri (`slot_s`, `sifs_s`, `cw_min`,
`cw_max`, `onbelge_s`, bit hızları, `onay_bayt`) **tek bir bibliyografik
doğrulamayla** hep birlikte `KAYNAK` kovasına geçer. Borcun büyük kısmı bir
kalemde kapanabilir.
"""

from __future__ import annotations

__all__ = ["KOVALAR", "KOKENLER", "MODUL_KOKENLERI", "DUYARLILIK_BEKLEYEN",
           "kova_sayimi", "eksik_alanlar", "duyarlilik_borcu"]

# ===========================================================================
# KOVALAR — yedisi de tanımlı, sekizincisi yok
# ===========================================================================
KOVALAR: dict[str, str] = {
    "TURETILMIS": "başka parametrelerden hesaplanıyor; serbest değil",
    "OLCULMUS":   "bir kalibrasyon betiği üretti — üretici komut yazılı",
    "KAYNAK":     "doğrulanmış dış kaynak; `02-DOGRULANMIS-KAYNAKLAR.md`de VAR",
    "DUYARSIZ":   "oynatıldı, çekirdek hücrenin çıktısı DEĞİŞMEDİ — beyanla "
                  "değil ÖLÇÜMLE hak edilir",
    "TEDAVI":     "deneyin EKSENİ; iki kolun meşru olarak ayrıldığı alan "
                  "(`kosum/sonuc.py::TEDAVI_ALANLARI` ile AYNI KÜME olmak "
                  "ZORUNDA — test bunu sınıyor)",
    "KOL_TANIMI": "bir kolun NE OLDUĞUNU tanımlayan sabit; eksen DEĞİL, "
                  "`kurulum_hash`in İÇİNDE — duyarlılık borcu taşır",
    "SINANMAMIS": "🔴 gerekçesi yok ya da yetersiz — mühürden önce boşalmalı",
}

# ===========================================================================
# 🔴 `TEDAVI` SÖZCÜĞÜ İKİ ANLAMA GELİYORDU — 8 Eylül 2026, K-104
# ===========================================================================
# Depoda iki ayrı "tedavi" tanımı vardı ve biri YAPISAL OLARAK ZORLANIYORDU:
#
#   · `kosum/sonuc.py::TEDAVI_ALANLARI` = ("kol", "senaryo", "tohum", "not_")
#     — iki kolun MEŞRU olarak ayrılabileceği alanlar. `kurulum_hash` tam
#     olarak bunları dışarıda bırakır; başka bir alanda ayrışan iki koşu,
#     aletin kendi kuralına göre "aynı deneyin iki kolu DEĞİLDİR".
#   · bu defterin `TEDAVI` kovası — on alan taşıyordu.
#
# `darbe_periyodu_s` ve arkadaşları ikinci listedeydi, birincisinde DEĞİL.
# Yani `kurulum_hash`in İÇİNDEydiler: onlarda ayrışan iki koşu zaten
# karşılaştırılamaz. Ayrıca ölçüldü — dördü de deneyde HİÇ oynatılmıyor,
# yalnız birim testlerinde. Bir tedavi *değişkeni* hiç oynatılmıyorsa
# değişken değildir; bir tedavi *seviyesinin tanımıdır*.
#
# 🔒 Çözüm: `TEDAVI` artık TAM OLARAK `TEDAVI_ALANLARI`dır ve bunu bir test
# sınar (`test_TEDAVI_kovasi_TEDAVI_ALANLARI_ile_AYNI`). Kol tanımı sabitleri
# `KOL_TANIMI`na taşındı ve borçları **silinmedi, sayaca bağlandı**.

# 🔴 DUYARLILIK BORCU — düzyazıda değil, SAYAÇTA
# ==============================================
# `KOL_TANIMI`ndaki bir sabit, ait olduğu kolun tanımıdır — bu kova hiç
# boşalmaz. Ama borç orada değil, BURADA durur.
#
#   🔒 ÖN-KAYIT MÜHÜRLENMEDEN ÖNCE: `SINANMAMIS` = 0 **ve** bu küme BOŞ.
#
# 🔴 8 EYLÜL 2026: BEŞİ DE OYNATILDI VE BORÇ KAPANMADI — büyüdü.
# Duyarlılık denetimi beşini de KENDİ CANLI KOLLARINDA oynattı:
#
#     darbe_periyodu_s          🔴 DUYARLI  (x2 → PDR −0,093 · R'nin 2,6 katı)
#     darbe_gorev_cevrimi       🔴 DUYARLI  (x2 → PDR +0,066)
#     taramali_konak_suresi_s   🔴 DUYARLI  (bant testini 2,2 kat asiyor)
#     taramali_konak_sayisi     🔴 DUYARLI  (iki yonde de bant disi)
#     karistirici_konum         ⚠️ KARAR YOK (|Δ| 0,048 > R ama kendi bandi icinde)
#
# 🔒 Yani bu beş sayı **sonucu belirliyor**. Borç artık *"ölçülmedi"* değil,
# *"ölçüldü ve önemli çıktı"*: her biri ya gerekçelendirilecek ya da
# ön-kayıtta bir EKSEN olarak ilan edilip deneyde OYNATILACAK. Sabit tutulan
# ve sonucu belirleyen bir sayı, gerekçesiz kalamaz.
#
# ⚠️ Aynı ölçüm, K-104'ün *"bunlar kol tanımıdır, tedavi değişkeni değil"*
# yargısını da doğruladı ama AKLAMADI: kol tanımı olmak, sonucu
# belirlememek anlamına gelmiyor.
#
# Bir adı buradan silmek, gerekçesine ölçümün ÜRETİCİ KOMUTUNU yazmayı
# gerektirir — `OLCULMUS` kovasının kuralının aynısı.
# ==========================================================================
# 🔴 ÇÖZÜNÜRLÜK EŞİĞİ R — 15 Eylül 2026'da GÜNCELLENDİ (C7, K-128)
# ==========================================================================
# Bu defterdeki `DUYARSIZ` gerekçeleri *"etki R'nin altında"* diyor. O R
# **0,036** yazıyordu ve bu 30 TOHUMLUK bir ölçümdü — oysa ana deney 10
# Eylül'de 40 tohuma çıkarılmıştı (K-113). 40 tohumda çözünürlük DAHA
# KESKİNDİR: R = 2·SD/√n olduğu için n büyüyünce R küçülür.
#
#     30 tohum : R = 0,0361      40 tohum : R = 0,0316
#     Üretici  : `python -u kalibrasyon/cozunurluk.py --tohum 40`
#
# 🔴 VE 0,0316 DA YANLIŞ EŞİKTİ — 16 Eylül 2026 (denetim B5, K-132)
# ==========================================================================
# 0,0316 **TEK KOL** çözünürlüğüdür (atlama kâhini PDR'sinin 2 SE'si). Ama:
#
#   1. Ön-kayıttaki BİRİNCİL TEST eşleştirilmiştir (Wilcoxon, `06` §7).
#   2. Duyarlılık aleti de eşleştirilmiş çalışır: tohum başına FARK ölçer ve
#      bandını farkların kendi yayılımından hesaplar
#      (`kalibrasyon/duyarlilik.py::_esli_fark`), ortalamaların farkından
#      değil.
#
# Yani aklamalar, deneyin gerçekte kullanacağından GEVŞEK bir eşiğe karşı
# yazılmıştı — K-128'in düzelttiği hatanın daha küçük hâli. Doğru eşik
# EŞLEŞTİRİLMİŞ çözünürlüktür:
#
#     40 tohum, eşleştirilmiş : R = 0,0230
#     Üretici : `python -u kalibrasyon/cozunurluk.py --tohum 40`
#               (satır `olcut_bedeli`)
#
# 🔴 O EŞİKTE ÜÇ KAYIT AKLANAMIYOR ve üçü de aşağıda İŞARETLİ:
#     gm_pitch_sigma_rad  |Δ| = 0,030
#     golgeleme_hucre_m   |Δ| = 0,027
#     onay_bayt           |Δ| = 0,025
#
# ⚠️ 0,0230 bugünün EN İYİ eşleştirilmiş kestirimidir, nihai değil: ölçülen
# kontrast İKİ KÂHİN arasındadır. Ana deneyin kontrastı PROTOKOL KOLLARI
# arasında olacak ve gürültüsü Aşama 2'de ölçülecek (`06` §7).
#
# 🔒 Yani aklamalar OLDUĞUNDAN GEVŞEK bir eşiğe karşı yazılmıştı. Yeniden
# denetlendi: deftere yazılı en büyük etki |Δ| = 0,027 (`golgeleme_hucre_m`)
# ve o da 0,0316'nın altında — HİÇBİR sınıflandırma değişmiyor. Eşik
# alıntıları yine de düzeltildi; bayat bir eşik, bir gün yanlış aklayan bir
# eşiktir.
#
# 🟢 BU BORÇ KAPALI — ve zaten kapalıymış (16 Eylül 2026).
# Burada *"|Δ| sayısı yazılı olmayan kayıtlar var (15'in 7'sinde var)"*
# yazıyordu; aynı cümle `DEVIR` §1 ve `v2/12` §3 C7'de de duruyordu. ÖLÇÜLDÜ:
# 15 `DUYARSIZ` kaydının **15'i de** ölçülen |Δ| taşıyor. Üç yerdeki sayı
# düzyazıya bırakıldığı için birlikte bayatlamıştı.
#     Üretici: `PYTHONIOENCODING=utf-8 python kalibrasyon/mimari_denetimi.py`
#              → D12 · "`DUYARSIZ` AKLAMALARI" bölümü
# 🔒 Sayı artık düzyazıda DEĞİL, her koşumda sayılıyor: bir kayda sayısız bir
# aklama girerse D12 onu isimle basar ve nota düşer.
#
# ⚠️ Üç `DUYARSIZ` modül sabiti (`kahin.py` ve `calisma_noktasi.py`daki
# `SONUMLEME_ORNEGI`, `calkanti.py::ETKIN_YARICAP_M`) bu sayımın DIŞINDADIR
# ve sayısızdır; D12 onları ayrıca listeler.
#
# 🔴 KALAN GERÇEK BORÇ, SAYI DEĞİL EŞİK: yukarıdaki R = 0,0316 TEK KOL
# çözünürlüğüdür, ama duyarlılık aleti EŞLEŞTİRİLMİŞ çalışır (tohum başına
# fark, `kalibrasyon/duyarlilik.py`) ve ön-kayıttaki birincil test de
# eşleştirilmiştir (Wilcoxon, `v2/06` §7). Eşleştirilmiş çözünürlük 0,0230'dur
# ve o eşikte ÜÇ kayıt aklanamaz. Ayrıntı ve karar: `v2/12` §3 C7.
# ==========================================================================
DUYARLILIK_BEKLEYEN: frozenset[str] = frozenset({
    "darbe_periyodu_s",
    "darbe_gorev_cevrimi",
    "taramali_konak_suresi_s",
    "taramali_konak_sayisi",
    "karistirici_konum",
    "gecit_konumu",
    "istasyon_kayma_hiz_ms",
    "tehdit_acik_s",
    "tehdit_sessiz_s",
})

# ===========================================================================
# KÖKENLER — `Konfig`in her alanı, tam olarak bir kez
# ===========================================================================
KOKENLER: dict[str, tuple[str, str]] = {
    # ---------------------------------------------------------- tedavi
    "kol":     ("TEDAVI", "koşum etiketi; kurulum_hash dışında"),
    "senaryo": ("TEDAVI", "mobilite × karıştırıcı hücresi"),
    "tohum":   ("TEDAVI", "eşleştirmenin ekseni"),
    "not_":    ("TEDAVI", "serbest not; hiçbir davranışa girmez"),

    # ------------------------------------------------------ zaman ekseni
    "isinma_s": ("SINANMAMIS",
                 "🔴 eski depodan gelen bir devir. `DEVIR §6.2`: 'yeni "
                 "dünyada ölçülmedi'. {50,100,150,200} taraması yapılacak"),
    "olcum_bitis_s": ("SINANMAMIS",
                      "ölçüm penceresinin uzunluğu seçilmedi, devralındı"),
    "kosu_bitis_s": ("DUYARSIZ",
                     "Üretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylül 2026). OLCULEN ETKI |Δ| = 0,000 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. ⚠️ Iddia SINIRLI: tek basina oynatildiginda (OAT) ve YALNIZ calisma noktasi ciktilarina duyarsiz; protokol SIRALAMASINA duyarliligi Faz 3'te olculur. ESKI GEREKCE: boşalma penceresi 30 s; ölçülen en kötü gecikme 71 ms "
                     "— 400 kat fazla. Şok evresi ölçülmeden küçültülmez"),

    # ------------------------------------------------------------ dünya
    "dugum_sayisi": ("OLCULMUS",
                     "40 — 🔴 BU BIR FIZIK BOSLUGU DEGIL, ONAYLANMAMIS BIR "
                     "KAPSAM KARARI. Uretici: `python -u kalibrasyon/"
                     "bag_kumesi.py j` (9 Eylul 2026). OLCULDU: N, olcekle "
                     "SADELESMIYOR (yogunluk sabit tutulsa bile derece 6,23 → "
                     "7,92 → 9,98 cikiyor; sebep SINIR ETKISI — buyuk agda "
                     "kenardaki dugum orani azaliyor). DERECE ESITLENDIGINDE "
                     "geriye TEK etki kaliyor: DERINLIK. "
                     "N=20 → alan 1100 m · derece 7,90 · ort atlama 1,64 · en uzak 3. "
                     "N=40 → alan 1800 m · derece 7,92 · ort atlama 2,22 · en uzak 5. "
                     "N=80 → alan 3000 m · derece 7,35 · ort atlama 3,12 · en uzak 8. "
                     "🔒 ALT SINIR OLCULDU: N=20 esitlenmis derecede 1,64 atlama "
                     "veriyor, yani sartnamenin ACIKCA REDDETTIGI sig rejim "
                     "(§09.4: 'ciftlerin %99,7si bir-iki atlamaydi ve orada "
                     "fark yok cikardi — ama bu farkin yoklugu degil, SORUNUN "
                     "yoklugu'). 🔒 UST SINIR OLCULDU: N=80 kosu basina 2,34 "
                     "kat maliyet (60,8 / 126,9 / 297,2 s). "
                     "⚠️ Olculen band N degeri icin bir ARALIK verir, TEK bir "
                     "sayi vermez — 40 o bandin icinde ve incelenen suru "
                     "buyuklugudur. `03` kural 12: kapsam kararlari ogrenciye "
                     "aittir. 🟢 C1 KOSTU (15 Eylul 2026, K-125). Uretici: `python -u kalibrasyon/dugum_sayisi.py`. Olcut taramadan ONCE ilan edildi (K-124) ve adaylari AYIRAMADI — kopukluk olasiligi 120 tohumda %0,8-3,3 ve butun bantlar cakisiyor, alternatif yol hepsinde %98,6 uzerinde. Olcut harfiyen N=30 secerdi ama o secim gurultuye dayaniyordu ve derinligi 2,21 atlamadan 2,01e indiriyordu. Ogrenci 40ta kalmayi secti: 40, alani kendi ilan edilmis olcutuyle secilmis TEK deger. 🔒 OLCUM N-I SECMEDI, DOGRULADI; secim bir KAPSAM kararidir. ⚠️ Calisma noktasi UCURUM KENARINDA: 1800 m icin eski 30 tohumluk sifir kopukluk gozlemi 120 tohumla %0,8 kopukluk veriyor. ⚠️ Duyarlilik denetiminin −0,183u "
                     "N tek basina oynatildiginda olculdu, yani alan yeniden "
                     "kalibre EDILMEDEN; degistiren biri alan taramasini "
                     "yeniden kosmak zorundadir"),
    "alan_en_m": ("OLCULMUS", "kalibrasyon/calisma_noktasi.py — statik kolda "
                              "30 tohumda kopukluğun sıfır kaldığı EN BÜYÜK"),
    "olcek": ("TURETILMIS",
              "1:50 — iki kısıt birlikte belirledi: seçilen hızlar "
              "ölçeklenince doğrulanmış İHA aralığına düşmeli (45–270 km/h "
              "∈ 30–400, A5a) VE türetilen verici var olabilmeli "
              "(0,03 dBm + 34 dB = 2,5 W). kalibrasyon/calkanti.py §2"),
    "alan_boy_m": ("OLCULMUS",
                   "kalibrasyon/calisma_noktasi.py — alan_en_m ile aynı "
                   "ölçüm; kare alan"),
    # ⚠️ BAYAT ÖLÇÜM. İkisi de gerçekten ölçüldü (tabansız kutuda düğümler
    # 0 m'ye iniyor · 300 m bandında derece %18 düşüyor) AMA o ölçümler
    # 1000 m alanda ve α=3'te yapıldı. K-097 ikisini de değiştirdi; bandın
    # yeni çalışma noktasındaki etkisi ölçülmedi.
    "irtifa_min_m": ("DUYARSIZ",
                     "Üretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylül 2026). OLCULEN ETKI |Δ| = 0,017 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. ⚠️ Iddia SINIRLI: tek basina oynatildiginda (OAT) ve YALNIZ calisma noktasi ciktilarina duyarsiz; protokol SIRALAMASINA duyarliligi Faz 3'te olculur. ESKI GEREKCE: ölçüm var ama ESKİ çalışma noktasında (1000 m, α=3)"),
    "irtifa_maks_m": ("SINANMAMIS",
                      "ölçüm var ama ESKİ çalışma noktasında (1000 m, α=3)"),
    "iletim_menzili_m": ("TURETILMIS",
                         "280 m — BAGIMSIZ BIR SAYI DEGIL, MODELIN UZUNLUK "
                         "BIRIMI. Uretici: `python -u kalibrasyon/bag_kumesi.py i` "
                         "(9 Eylul 2026). CEBIR: SINR(d) = β·PL(R)/PL(d) = "
                         "β·(R/d)^α, yani yalniz R/d ORANI belirleyici. "
                         "OLCULDU: butun uzunluklar λ ile olceklenip "
                         "(alan, irtifa bandi, menzil capasi, golgeleme hucresi) "
                         "karistirici 10α·log10(λ) dB telafi edildiginde kenar "
                         "kumesi λ = 1,25 ve 2,0 icin BIREBIR ayni (Jaccard "
                         "1,0000, derece farki 0,000e+00). 🔒 Belirleyici "
                         "buyukluk `menzil/alan` oranidir ve ALAN zaten o orani "
                         "sabitleyen bir olcutle secildi: kopukluk sifirken en "
                         "buyuk alan (`calisma_noktasi.py`). Yani cift TEK "
                         "serbestlik derecesi tasiyor ve o kalibre edilmis. "
                         "⚠️ Duyarlilik denetiminin −0,655'i (en buyuk etki) "
                         "bunun sonucudur: R'yi TEK BASINA oynatmak R/alan "
                         "oranini oynatir, yani calisma noktasini degistirir. "
                         "Degistiren biri alan taramasini yeniden kosmak "
                         "zorundadir"),

    # ------------------------------------------------------- mobilite
    "gm_alfa": ("TURETILMIS",
                "α = exp(−adım/τ_v), τ_v ≈ 30 s hız korelasyonu — bir ARAÇ "
                "DİNAMİĞİ zamanıdır ve ÖLÇEKLENMEZ. Ölçüldü: Θ'yı "
                "değiştirmiyor (5,95 → 5,93)"),
    "gm_adim_s": ("SINANMAMIS", "mobilite güncelleme adımı; seçilmedi"),
    "gm_hiz_min_ms": ("OLCULMUS",
                      "Üretici: `python -u kalibrasyon/bag_kumesi.py h` "
                      "(9 Eylül 2026). ÖLÇÜT: Θ ≥ 3 (K-101 kapısı) VE ölçekli "
                      "hız 30–400 km/h (`02` A5a) kısıtları altında ÇALKANTIYI "
                      "EN BÜYÜK yapan aday — alan ve güç seçimiyle AYNI biçim. "
                      "Seçilen: Θ = 3,25 · 45–135 km/h. 🔴 DEĞER DEĞİŞMEDİ ama "
                      "GEREKÇESİ DEĞİŞTİ: eski Θ = 5,95 üç yanlılık taşıyordu — "
                      "bağ tanımı 400 m'lik SERT DİSKTİ (rota ömrünü iki kat "
                      "uzun gösteriyor: 89 s ↔ 43 s), soldan kesme ve sağdan "
                      "sansür düzeltilmemişti. 🔒 Sansür düzeltmesi TAŞIYICI: "
                      "ham ortalamayla Θ = 2,59 ve kapı GEÇİLMEZDİ"),
    "gm_hiz_maks_ms": ("OLCULMUS",
                       "`gm_hiz_min_ms` ile AYNI ölçüm ve aynı ölçüt. "
                       "Üretici: `python -u kalibrasyon/bag_kumesi.py h`. "
                       "🔒 Seçilen nokta iki kısıtın kesiştiği TEK adaydır: bir "
                       "sonraki hızlı aday (0,5–1,5 m/s) Θ = 1,78 ile kapının "
                       "ALTINDA, bir sonraki yavaş aday (0,12–0,36 m/s) ise "
                       "22–65 km/h ile doğrulanmış İHA aralığının ALTINDA"),
    "gm_hiz_sigma_ms": ("TURETILMIS",
                        "azami hızın %10'u; hız zarfıyla orantılı"),
    "gm_azimut_sigma_rad": ("TURETILMIS",
                            "koordineli dönüş ω = g·tan(φ)/v. Yerçekimi "
                            "ÖLÇEKLENMEZ, o yüzden GERÇEK hızdan: 90 km/h'de "
                            "30° banka → 0,226 rad/s → 0,5 s adımda 0,11 rad"),
    "gm_pitch_ort_rad": ("TURETILMIS",
                         "0 — kalıcı tırmanış olmaması gerektiği için; "
                         "testle bağlı"),
    # 🟢 20 TOHUMLA YENIDEN OLCULDU ve AKLANDI (16 Eylul 2026, K-132).
    "gm_pitch_sigma_rad": ("DUYARSIZ",
                 "Uretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylul 2026). OLCULEN ETKI |D| = 0,0158 (bagimsiz-surekli kolunda, 20 tohum) — esleştirilmis cozunurlugun (R = 0,0230) ALTINDA ve kendi hata payinin icinde (0,6x). IKI OLCUT DE GECILDI. 🔴 5 TOHUMLUK ESKI KESTIRIM 0,030 IDI ve ESIGIN USTUNDE GORUNUYORDU; 20 tohumla etki yariya indi — az tohumlu bir |D| kestiriminin kendi hata payi vardir ve bu kayit onun ornegidir. Uretici (16 Eylul 2026): `python -u kalibrasyon/duyarlilik.py hareketli gm_pitch_sigma_rad --tohum 20` (73 dk). Iddia SINIRLI: tek basina (OAT) ve yalniz calisma noktasi ciktilarina. ESKI GEREKCE: dikey manevra genliği; seçilmedi"),
    "gorev_grup_sayisi": ("SINANMAMIS",
                          "10 müfreze × 4 üye; müfreze büyüklüğü seçilmedi"),
    "gorev_grup_yaricapi_m": ("OLCULMUS",
                              "Üretici: `python kalibrasyon/calisma_noktasi.py` §4 — bağımsız "
                              "kolla dereceyi eşitleyen yarıçap (|Δderece| ≤ 0,3). "
                              "🔴 ÖLÇÜM BAYAT VE BU YAZILMAK ZORUNDA (9 Eylül 2026, K-111 EK-1): "
                              "ölçüm 5 Eylül'de (K-097) yapıldı; 8 Eylül'de K-101 hızları ~40 kat "
                              "düşürdü ve bu kalibrasyonun ÜRETİCİSİ o tarihten beri KIRIKTI — yani "
                              "hiç yeniden koşulmadı. Bugün ölçüldü (12 tohum): bağımsız kolun "
                              "referans derecesi 7,406 → 6,704 (4,3 SE düşüş); ızgaranın en iyi "
                              "noktası 650 değil 850 m (fark 0,017 ↔ 650'de 0,557). "
                              "⚠️ AMA ÖLÇÜT BU ÖRNEKLEMDE SINANAMIYOR: birleşik 2SE 0,56–0,69, yani "
                              "ilan edilmiş toleransın (0,3) İKİ KATI — ne 650 çürütülebiliyor ne 850 "
                              "doğrulanabiliyor. Toleransı sınanabilir yapmak ~140 tohum ister. Görev "
                              "kolu keşifsel eksende (`07` §15/3), dolayısıyla bu bir KAPSAM kararıdır "
                              "ve ÖĞRENCİYE AÇIKTIR. Yapısal üst sınır: `Konfig` 2r < alan istiyor, "
                              "yani 1800 m'de r < 900 m"),
    "gorev_jitter_hiz_ms": ("TURETILMIS",
                            "azami hızın ~%7'si; hız zarfıyla orantılı"),
    "istasyon_kayma_hiz_ms": ("KOL_TANIMI",
                              "0 m/s — formasyon kolunda istasyonlar "
                              "çekirdekte SABİT (`v2/07` §18 Y6, öğrenci onayı "
                              "11 Eylül 2026). Sıfırdan büyük değer keşifsel "
                              "eksendir: istasyonların yavaş yeniden "
                              "düzenlenmesi. Kaynağı yok; eksen olarak "
                              "oynatılmadan duyarlılık borcu kapanmaz"),

    # ------------------------------------------------- fiziksel katman
    "bit_hizi_bps": ("SINANMAMIS",
                     "802.11b DQPSK 2 Mb/s — standart değer ama `02`de "
                     "DOĞRULANMADI. Bianchi ±%15 dolaylı kısıtlıyor"),
    "temel_bit_hizi_bps": ("DUYARSIZ",
                 "Uretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylul 2026). OLCULEN ETKI |D| = 0,004 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. Iddia SINIRLI: tek basina (OAT) ve yalniz calisma noktasi ciktilarina. ESKI GEREKCE: 802.11b DBPSK 1 Mb/s — `02`de yok"),
    "onbelge_s": ("DUYARSIZ",
                 "Uretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylul 2026). OLCULEN ETKI |D| = 0,007 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. Iddia SINIRLI: tek basina (OAT) ve yalniz calisma noktasi ciktilarina. ESKI GEREKCE: 802.11b uzun önbelge 192 µs — `02`de yok"),
    "bant_genisligi_hz": ("TURETILMIS",
                          "2 MHz. Üretici: `python -u kalibrasyon/bag_kumesi.py i` (9 Eylül 2026). 🔒 CEBİR + ÖLÇÜM: bu sayı `sim2/` içinde YALNIZ gürültü tabanında geçiyor (AST ile tarandı), ve verici gücü gürültü tabanından TÜRETİLİYOR: Pt = N·β·PL(R) ⟹ SINR = β·PL(R)/PL(d), yani N SADELEŞİR. Düğümler arası girişim de ∝ N olduğu için o da sadeleşir; taşıyıcı dinleme eşiği N'dir ve karşılaştırdığı güçler ∝ N. Geriye TEK kalıntı karıştırıcının MUTLAK gücü, yani J/N — ve o ρ ile KALİBRE EDİLİYOR. ÖLÇÜLDÜ: gürültü tabanı X dB yükseltilip karıştırıcı X dB yükseltildiğinde kenar kümesi 133/133 BİREBİR aynı, derece farkı 0,000e+00. 🔒 Yani bu bir FİZİK PARAMETRESİ değil, bir BİRİM SEÇİMİDİR: değeri yalnız *−15 dBm ne demek* sorusunu tanımlar. ⚠️ Duyarlılık denetiminin ölçtüğü −0,112 bununla ÇELİŞMEZ: orada N oynatılırken karıştırıcı yeniden türetilmemişti. Değiştiren biri ρ kalibrasyonunu yeniden koşmak zorundadır. ⚠️ MODEL SINIRI BEYAN EDİLİR: bu modelde bant genişliği ile bit hızı BAĞIMSIZ parametrelerdir; gerçekte bağlıdırlar. Sadeleşme model içinde tamdır."),
    "frekans_hz": ("TURETILMIS",
                   "2,4 GHz — 802.11b bağlılığından TÜRER (standart o bantta çalışır); bit hızı, modülasyon ve MAC sabitleriyle aynı karardan gelir. Üretici: `python -u kalibrasyon/bag_kumesi.py i`. 🔒 İKİ KANALI VAR ve ayrıldı: YOL KAYBI yarısı yukarıdaki cebirle SADELEŞİR (statik kolda ×2 oynatma + karıştırıcı telafisi → kenar kümesi BİREBİR aynı, Jaccard 1,0000). DOPPLER yarısı sadeleşmez ve tek gerçek kanaldır: hareketli kolda aynı oynatma derece farkı 0,10 ve Jaccard 0,9254 veriyor — ilan edilmiş derece toleransının (0,3) ALTINDA. ⚠️ Duyarlılık denetiminin −0,234'ü ağırlıklı olarak yol kaybı kanalıydı, yani karıştırıcı ölçeği artefaktı."),
    "modulasyon": ("DUYARSIZ",
                    "Uretici: `python kalibrasyon/duyarlilik.py statik modulasyon` (9 Eylul 2026). OLCULEN ETKI |D| = 0,007 — deneyin cozunurlugu R = 0,0316 altinda. 🔴 ILK TARAMADA HIC OYNATILMAMISTI (str tipi hicbir dala girmiyordu) ve yanlislikla OLCULEMEDI diye raporlanmisti. ESKI GEREKCE: DQPSK — `02`de yok"),
    "yol_kaybi_usteli": ("TURETILMIS",
                         "α=2: iki-ışın kırılma mesafesi her iki dünyada da "
                         "bağ mesafesinin çok üstünde → serbest uzay. Ölçek "
                         "tutarlılığı da α=3'ü eledi (35 kW). K-097"),
    "sinr_esigi_db": ("TURETILMIS",
                      "β=16: 10 dB çözülebilirlik + 2σ gölgeleme marjı "
                      "(σ=3 dB). Ölçüm ve türetme aynı yere düşüyor. K-091"),
    "gurultu_figuru_db": ("TURETILMIS",
                          "6 dB. Üretici: `python -u kalibrasyon/bag_kumesi.py i` (9 Eylül 2026). 🔒 CEBİR + ÖLÇÜM: bu sayı `sim2/` içinde YALNIZ gürültü tabanında geçiyor (AST ile tarandı), ve verici gücü gürültü tabanından TÜRETİLİYOR: Pt = N·β·PL(R) ⟹ SINR = β·PL(R)/PL(d), yani N SADELEŞİR. Düğümler arası girişim de ∝ N olduğu için o da sadeleşir; taşıyıcı dinleme eşiği N'dir ve karşılaştırdığı güçler ∝ N. Geriye TEK kalıntı karıştırıcının MUTLAK gücü, yani J/N — ve o ρ ile KALİBRE EDİLİYOR. ÖLÇÜLDÜ: gürültü tabanı X dB yükseltilip karıştırıcı X dB yükseltildiğinde kenar kümesi 133/133 BİREBİR aynı, derece farkı 0,000e+00. 🔒 Yani bu bir FİZİK PARAMETRESİ değil, bir BİRİM SEÇİMİDİR: değeri yalnız *−15 dBm ne demek* sorusunu tanımlar. ⚠️ Duyarlılık denetiminin ölçtüğü −0,112 bununla ÇELİŞMEZ: orada N oynatılırken karıştırıcı yeniden türetilmemişti. Değiştiren biri ρ kalibrasyonunu yeniden koşmak zorundadır."),
    "sicaklik_k": ("TURETILMIS",
                   "290 K — gürültü figürünün TANIMLI referans sıcaklığı. Üretici: `python -u kalibrasyon/bag_kumesi.py i` (9 Eylül 2026). 🔒 CEBİR + ÖLÇÜM: bu sayı `sim2/` içinde YALNIZ gürültü tabanında geçiyor (AST ile tarandı), ve verici gücü gürültü tabanından TÜRETİLİYOR: Pt = N·β·PL(R) ⟹ SINR = β·PL(R)/PL(d), yani N SADELEŞİR. Düğümler arası girişim de ∝ N olduğu için o da sadeleşir; taşıyıcı dinleme eşiği N'dir ve karşılaştırdığı güçler ∝ N. Geriye TEK kalıntı karıştırıcının MUTLAK gücü, yani J/N — ve o ρ ile KALİBRE EDİLİYOR. ÖLÇÜLDÜ: gürültü tabanı X dB yükseltilip karıştırıcı X dB yükseltildiğinde kenar kümesi 133/133 BİREBİR aynı, derece farkı 0,000e+00. 🔒 Yani bu bir FİZİK PARAMETRESİ değil, bir BİRİM SEÇİMİDİR: değeri yalnız *−15 dBm ne demek* sorusunu tanımlar. ⚠️ Duyarlılık denetiminin ölçtüğü −0,112 bununla ÇELİŞMEZ: orada N oynatılırken karıştırıcı yeniden türetilmemişti. Değiştiren biri ρ kalibrasyonunu yeniden koşmak zorundadır."),
    "kanal_dilimi_s": ("SINANMAMIS",
                       "hash tabanlı kanal kararının zaman dilimi; seçilmedi"),

    # ---------------------------------------------------------- gölgeleme
    "golgeleme_acik": ("TURETILMIS",
                       "açık; kapalıyken bağlar gerçeğe göre keskin açılıp "
                       "kapanıyor — ablasyon için False yapılabilir"),
    "golgeleme_sigma_db": ("OLCULMUS",
                           "Üretici: `python kalibrasyon/adim4_kapanis.py` "
                           "bölüm D (9 Eylül 2026). PER'in 0,99→0,01 geçiş "
                           "bandı **3,44 dB**, σ = 3,00 dB — aynı mertebede "
                           "(oran 1,15). Yani 'menzil' sert bir daire değil; "
                           "σ kadarlık bir gölgeleme bağı tamamen açıp "
                           "kapatmaya yeter, ve σ'nın bu mertebede olması "
                           "gerekçesi budur. 🔴 ESKİ ÜRETİCİ BAYATTI: ölçüm "
                           "`adim3_oncesi.py`de, TERK EDİLMİŞ bir çalışma "
                           "noktasında (α = 3,0 · eşik 10 dB) yapılmıştı ve "
                           "3,02 dB veriyordu. Mimari denetimi D15 yakaladı; "
                           "bugünkü fizikte yeniden ölçüldü ve iddia AYAKTA"),
    # 🔴 `DUYARSIZ` KOVASINDAN ÇIKTI — 16 Eylül 2026 (K-132):
    # 20 tohumlu yeniden ölçüm aklamayı ÇÜRÜTTÜ.
    "golgeleme_hucre_m": ("SINANMAMIS",
     "50 m gölgeleme korelasyon hücresi. MEKANİZMASI gerekçeli, DEĞERİ ÖLÇÜLMEDİ. 🔴 8 Eylül 2026'da `DUYARSIZ` diye aklanmıştı (|Δ| = 0,027 < R = 0,0316, 5 tohum); 16 Eylül'de 20 TOHUMLA yeniden ölçüldü ve aklama ÇÖKTÜ: OLÇÜLEN ETKİ |Δ| = 0,0605 (`d_atlama`, çarpan 0,5) — ALTI PDR PUANI, eşleştirilmiş çözünürlüğün (0,0230) 2,6 KATI. ⚠️ Kendi hata payı testini GEÇİYOR (0,7x) çünkü tohumlar arası yayılım büyük — tam da `cozunurluk.py`nin *'aklamanın en kötü hâli'* dediği durum, ve alet o gün ikinci ölçütü (R) hiç uygulamıyordu; artık uyguluyor. Üretici: `python -u kalibrasyon/duyarlilik.py statik golgeleme_hucre_m onay_bayt --tohum 20` (16 Eylül 2026, 30,2 dk). 🔒 Mühürden önce: ya kaynakla gerekçelendirilecek ya EKSEN olarak ilan edilecek"),

    # ---------------------------------------------------------- sönümleme
    "sonumleme_acik": ("TURETILMIS", "açık; ablasyon için False"),
    "rician_k_db": ("SINANMAMIS",
                    "6 dB — 🔒 ARTIK KEYFI DEGIL, SINANABILIR BIR FIZIK "
                    "IDDIASI; ama HENUZ DOGRULANMADI. Uretici: `python -u "
                    "kalibrasyon/bag_kumesi.py m` (9 Eylul 2026). "
                    "🔒 (1) BIR IC TUTARSIZLIK SUPHESI KURULDU VE DUSTU: "
                    "`yol_kaybi_usteli = 2` 'yer yansimasi onemsiz' diye "
                    "secilmisti, K = 6 dB ise sacilan gucun dogrudan gorusun "
                    "DORTTE BIRI oldugunu soyluyor. Celismiyorlar: kirilma "
                    "mesafesinin ALTINDA iki-isin alani serbest uzay degerinin "
                    "etrafinda SALINIR — α = 2 ortalamayi, Rician salinimin "
                    "KENDISINI modelliyor. "
                    "🔒 (2) DENKLIK: baskin cok yol bileseni yer yansimasiysa "
                    "P_yansiyan/P_dogrudan = Γ², yani K_dB = −20·log10(Γ). "
                    "**K = 6 dB ⟺ Γ = 0,50.** Sayi artik 'hava-hava icin K ne "
                    "olmali' gibi belirsiz bir soru degil, TEK ve NET bir "
                    "bibliyografik kontrol: bu geometride (irtifa 20-120 m, bag "
                    "~280 m, ~27° siyirma acisi, 2,4 GHz) yer yansima katsayisi "
                    "0,50 mi? `02`ye islenince kova `KAYNAK` olur. "
                    "🔴 (3) OLCULDU, DUYARLI VE DEGENERE DEGIL: K ∈ {0,3,6,10,15} "
                    "dB icin derece 6,00 → 6,20 → 6,65 → 7,10 → 7,55 (%26 "
                    "aralik, ilan edilmis 0,3 derece toleransinin cok ustunde) "
                    "ve kenar kumesi Jaccard'i 0,73-0,86'ya iniyor. "
                    "⚠️ (4) IC TUTARLILIK ISARETI: golgeleme σ'si PER'in "
                    "0,99→0,01 gecis bandiyla (3,44 dB) ayni mertebede oldugu "
                    "icin gerekcelendirilmisti. Ayni olcut K icin: p10 fade "
                    "derinligi K=6'da **5,15 dB** (bandin 1,5 kati), K=10'da "
                    "**3,02 dB** (banda esit), K=15'te 1,57 dB (kozmetik). Yani "
                    "ayni bicimdeki olcut K ≈ 8-10 dB'yi isaret ediyor; 6 dB "
                    "guclu sonumleme ucunda. Bu bir KARAR degil, kaynak "
                    "kontrolune goturulen bir ISARETTIR"),
    # ⚠️ Bayatlamıştı ve 8 Eylül 2026'da YENİDEN ÖLÇÜLDÜ: hızlar 1/50
    # ölçeğe çekilip Doppler tam ölçek hızına bağlanınca T_c dağılımı
    # değişti. Kural aynı kaldı (T_c(p99)/4), değer 240 → 190 µs.
    "sonumleme_parca_suresi_s": ("OLCULMUS",
                                 "kalibrasyon/adim4_sonumleme.py — "
                                 "kural T_c(p99)/4; ölçülen p99 = 764 µs"),

    # ------------------------------------------------------------- alıcı
    "anten_deseni_acik": ("TURETILMIS", "açık; ablasyon için False"),
    "yakalama_etkisi_acik": ("TURETILMIS", "açık; ablasyon için False"),
    "yakalama_esigi_db": ("SINANMAMIS", "10 dB capture eşiği; kaynak yok"),
    "yakalama_penceresi_s": ("SINANMAMIS",
                             "🔴 `onbelge_s` ile AYNI değer, ama ayrı bir "
                             "sabit olarak yazılmış — ikisi bağımsız "
                             "değişebilir. Türetilmeli"),

    # --------------------------------------------------------------- MAC
    "slot_s": ("DUYARSIZ",
                 "Uretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylul 2026). OLCULEN ETKI |D| = 0,005 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. Iddia SINIRLI: tek basina (OAT) ve yalniz calisma noktasi ciktilarina. ESKI GEREKCE: 802.11b 20 µs — `02`de yok, Bianchi dolaylı"),
    "sifs_s": ("DUYARSIZ",
                 "Uretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylul 2026). OLCULEN ETKI |D| = 0,004 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. Iddia SINIRLI: tek basina (OAT) ve yalniz calisma noktasi ciktilarina. ESKI GEREKCE: 802.11b 10 µs — `02`de yok, Bianchi dolaylı"),
    "cca_s": ("SINANMAMIS",
              "4 µs; sıfır olmaması gerekçeli (çarpışma kaynağı) ama DEĞER "
              "gerekçesiz"),
    "cw_min": ("DUYARSIZ",
                 "Uretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylul 2026). OLCULEN ETKI |D| = 0,005 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. Iddia SINIRLI: tek basina (OAT) ve yalniz calisma noktasi ciktilarina. ESKI GEREKCE: 802.11b 31 — `02`de yok, Bianchi dolaylı"),
    "cw_max": ("TURETILMIS",
               "1023 — 🔒 YENIDEN DENEME SINIRI VERILDIGINDE ERISILEMEZ, ve bu "
               "aritmetikle kanitlanip olcumle DOGRULANDI. `onay_gelmedi` her "
               "basarisizlikta cw = min(2·cw+1, cw_max) yapiyor; cw_min = 31 ve "
               "yeniden deneme siniri 4 oldugundan dizi 31 → 63 → 127 → 255 → "
               "**511** ile duruyor ve besinci basarisizlikta vazgeciliyor. "
               "1023 icin ALTI katlanma gerekirdi. ÖLÇÜLDÜ (stres altinda, "
               "dongu ureten kosum aleti, 849 vazgecme uretilen bir kosumda): "
               "cw_max 1023 → 511 degistirildiginde parmak izi BIREBIR AYNI. "
               "Uretici: `python -u kalibrasyon/bag_kumesi.py l`. "
               "🔴 KOSULLU BIR ATALETTIR: `yeniden_deneme_siniri` 5'in ustune "
               "cikarsa cw_max CANLI hale gelir ve bu kayit gecersizlesir"),
    "yeniden_deneme_siniri": ("SINANMAMIS",
                              "🔴 4 = UZUN çerçeve sınırı; bizim 512 baytlık "
                              "çerçevemiz RTS eşiğinin altında, yani KISA "
                              "sınır (7) geçerli. Ölçüldü: etkisi yok"),
    # 🔴 `DUYARSIZ` KOVASINDAN ÇIKTI — 16 Eylül 2026 (K-132):
    # 20 tohumlu yeniden ölçüm aklamayı ÇÜRÜTTÜ.
    "onay_bayt": ("SINANMAMIS",
     "802.11 ACK 14 bayt — kaynak `02`de DOĞRULANMADI. 🔴 8 Eylül 2026'da `DUYARSIZ` diye aklanmıştı (|Δ| = 0,025 < R = 0,0316, 5 tohum); 16 Eylül'de 20 TOHUMLA yeniden ölçüldü ve aklama ÇÖKTÜ: etki kendi hata payının 1,1 KATI, yani BAND testini KAYBEDİYOR (|Δ| = 0,0226; R testini kıl payı geçiyor). Az tohumlu tarama onu görememişti. Üretici: `python -u kalibrasyon/duyarlilik.py statik golgeleme_hucre_m onay_bayt --tohum 20` (16 Eylül 2026, 30,2 dk). 🔒 Mühürden önce `02` §S2'nin 802.11b sabitleri öbeğinde kapanır"),

    # -------------------------------------------------------------- saat
    "saat_senkron": ("TURETILMIS",
                     "False; bedava kusursuz senkron yasak — ablasyon için "
                     "True"),
    "saat_ofset_araligi_s": ("SINANMAMIS", "±0,5 s; kaynak yok"),
    "saat_sapma_ppm": ("SINANMAMIS", "20 ppm kristal sapması; kaynak yok"),

    # ------------------------------------------------------------ trafik
    # ⚠️ BAYAT ÖLÇÜM. 10×4×512 gerçekten ölçüldü (tek çarpışma alanının
    # %36,9'u; %54'te bütün protokoller birlikte çöküyor) AMA o doluluk
    # 1000 m alanda, α=3'te ve 1,8 atlamalı yollarda hesaplandı. Şimdi alan
    # 1800 m, α=2 ve yollar 2,2 atlama — doluluk DEĞİŞTİ ve yeniden
    # ölçülmedi. Yük, karıştırıcının etkisini belirleyen ana eksenlerden
    # biri olduğu için bu bayatlık önemsiz değil.
    "paket_bayt": ("DUYARSIZ",
                   "Üretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylül 2026). OLCULEN ETKI |Δ| = 0,019 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. ⚠️ Iddia SINIRLI: tek basina oynatildiginda (OAT) ve YALNIZ calisma noktasi ciktilarina duyarsiz; protokol SIRALAMASINA duyarliligi Faz 3'te olculur. ESKI GEREKCE: ölçüm var ama ESKİ çalışma noktasında (1000 m, α=3)"),
    "akis_sayisi": ("SINANMAMIS",
                    "10 — paket_bayt ile aynı gerekçe; duyarlılık ölçümü "
                    "ESKİ çalışma noktasından (1000 m, α = 3) ve BAYAT. "
                    "🟡 15 Eylül 2026'da C3 ölçütüyle İLK KEZ sınandı ve "
                    "geçti (`python -u kalibrasyon/yere_toplama_yuku.py "
                    "esler`): 10 × 4,0 = 40 pkt/s'te kâhin PDR 0,9987, iki "
                    "katında 0,9967. Ölçüm DEĞERİ seçmedi, güvenli tarafta "
                    "olduğunu gösterdi; bayat duyarlılık borcu DEVAM EDİYOR "
                    "(K-126)"),
    "akis_paket_hizi_hz": ("SINANMAMIS",
                           "4,0 — `akis_sayisi` ile AYNI kayıt; ikisi tek "
                           "yükü (10 × 4,0 = 40 pkt/s) birlikte tanımlar "
                           "(K-126)"),
    "cbr_titresim_s": ("DUYARSIZ",
                       "Üretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylül 2026). OLCULEN ETKI |Δ| = 0,006 — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. ⚠️ Iddia SINIRLI: tek basina oynatildiginda (OAT) ve YALNIZ calisma noktasi ciktilarina duyarsiz; protokol SIRALAMASINA duyarliligi Faz 3'te olculur. ESKI GEREKCE: 50 ms; periyodik kilitlenmeyi kırma gerekçesi var, "
                       "DEĞERİ yok"),
    # ---------------------------------------------- trafik deseni (Y4, K-116)
    "trafik_deseni": ("TEDAVI",
                      "trafik deseni ekseni: `esler_arasi` · `yere_toplama` "
                      "(`v2/07` §06.2, §18 Y4; öğrenci onayı 10–11 Eylül 2026)"),
    # ------------------------------------------- tehdit senaryosu (Y5b)
    "tehdit_senaryosu": ("TEDAVI",
                         "karıştırıcı kümesinin biçimi: `tekli_merkez` · "
                         "`cephe_hatti` · `derin_sizma` · `hedef_koruma` · "
                         "`hava_eslik` (`v2/07` §05.3.1, §18 Y5; öğrenci "
                         "kararları 11 Eylül 2026, K-119)"),
    "tehdit_acik_s": ("KOL_TANIMI",
                      "15 s = OLSR TOP_HOLD_TIME (RFC 3626 §18, `02` §R2): "
                      "açık dönem protokolün topoloji bilgisinin bayatlama "
                      "süresine eşit. Tek bir gerçek değer iddiası yok; "
                      "keşifsel 3 s (AODV ACTIVE_ROUTE_TIMEOUT) ve 45 s (K-119)"),
    "tehdit_sessiz_s": ("KOL_TANIMI",
                        "15 s — açık süreyle aynı çapa; keşifsel 5 s (OLSR "
                        "TC_INTERVAL) ve 45 s: rota onarımına zaman kalıyor mu "
                        "(K-119). Derin sızma aracı yalnız bu dönemde taşınır"),
    "tehdit_arac_hiz_kmh": ("SINANMAMIS",
                            "60 km/h — yer aracı; mertebe için varsayım, kaynak "
                            "yok (`v2/07` §05.3.1). Ölçekte 0,33 m/s; yalnız "
                            "susarken taşındığı için koşu içi yol ~32 m"),
    "tehdit_hava_hiz_kmh": ("SINANMAMIS",
                            "200 km/h — hava platformu; mertebe için varsayım, "
                            "kaynak yok (`v2/07` §05.3.1). Ölçekte 1,1 m/s"),
    "gecit_konumu": ("KOL_TANIMI",
                     "`kenar` — derinliği artırır, yer istasyonları cephe "
                     "gerisinde durur (`v2/07` §06.2); `merkez` keşifsel eksen"),
    "telemetri_paket_hizi_hz": ("OLCULMUS",
                                "1,0 pkt/s. 🟢 C3 KOSTU (15 Eylul 2026, K-126). Uretici: `python -u kalibrasyon/yere_toplama_yuku.py`. "
                                "Olcut TARAMADAN ONCE ilan edildi (K-124): karistiricisiz kolda kahin PDR >= 0,95 "
                                "tutan EN BUYUK telemetri hizi. Olcut harfiyen 2,0 seciyordu (PDR 0,9841) ama "
                                "eksen dengesini BOZUYORDU: 39x1,0 + 4x0,25 = 40,0 pkt/s ve `esler_arasi` da "
                                "10x4,0 = 40,0 sunuyor; `trafik_deseni` bir TEDAVI ekseni oldugu icin 2,0 o "
                                "ekseni IKI KAT YUKLE karistirirdi. Ogrenci 1,0'da kaldi. 🔒 OLCUM HIZI SECMEDI, "
                                "DOGRULADI: 1,0 esigi 0,9923 ile geciyor ve ucurumdan %150 uzakta (2,5'te tek "
                                "tohumlar esigin altina dusuyor, 3,0'da cokuyor). ⚠️ `02` §S4 kaynak boslugu "
                                "KAPANMADI — 1,0 hala literatur capasi tasimiyor; degisen sey olculmus bir UST "
                                "SINIRI ve beyan edilmis bir gerekcesi olmasidir"),
    "komut_akis_sayisi": ("TURETILMIS",
                          "4 — çift yönlü yolları sınar, yükteki payı küçük. "
                          "🔒 Sayı 40 pkt/s DENGESİNİ kuran yerdir: 39×1,0 + "
                          "4×0,25 = 40,0 ve `esler_arasi` da 10×4,0 = 40,0 "
                          "sunar. Ayrı bir seçim değil, o eşitliğin parçası "
                          "(K-126)"),
    "komut_paket_hizi_hz": ("TURETILMIS",
                            "0,25 — telemetriye ORANLA gider (telemetri × "
                            "0,25) ve C3 taramasında o oranla birlikte "
                            "oynadı; ayrı bir eksen açmak taramayı iki "
                            "boyutlu yapardı ve komut akışı yükün küçük "
                            "parçasıdır. 40 pkt/s dengesinin parçası (K-126)"),

    # -------------------------------------------------------- kuyruk/TTL
    # ==================================================================
    # ROTA BEKLEME TAMPONU — `Karar.beklet` (16 Eylul 2026, K-131)
    # ==================================================================
    # 🔴 IKISI DE BU PROJEDE OLCULMEDI ve bu ACIKCA yaziliyor. Degerler
    # NS-2'nin AODV gerceklemesinin GELENEGINDEN alindi; bir gelenek bir
    # olcum degildir. `03` §2.1'in ayrimi burada gecerli: *"olctum, etkisi
    # yok"* (DUYARSIZ) ile *"olcemedim"* (SINANMAMIS) ayri seylerdir ve
    # ikincisini birincisi sanmak gerekcesiz bir sayiyi aklar.
    #
    # 🔒 Ikisi de PROTOKOLSUZ KAPANAMAZ — kuyruk kapasitesi, TTL, beacon
    # araligi ve komsu omrunun yanina besinci ve altinci olarak giriyorlar
    # (`v2/12` §5). Bugunku dort kosum aletinin hicbiri `beklet` dondurmuyor,
    # yani tampon hic devreye girmiyor ve bir olcum SIFIR uretirdi — kuyruk
    # kapasitesinin 9 Eylul'de coken gerekcesinin ta kendisi. Verdikt Asama
    # 2'de, gercek bir AODV ile verilir.
    "rota_tamponu_kapasitesi": ("SINANMAMIS",
                                "64 paket; RFC 3561 §6.3 tamponlamayi SART "
                                "kosar ama bir SAYI vermez. 64, NS-2'nin "
                                "`aodv_rqueue` gelenegidir (RQUEUE_MAX_LEN). "
                                "Sonlu olmasi gerekceli: tavansiz bir tampon "
                                "sonsuz kuyruktur ve gecikme metrigini "
                                "anlamsizlastirir (`ag/kuyruk.py` ayni "
                                "gerekce). DEGERI gerekcesiz — Asama 2'de "
                                "gercek AODV ile olculecek"),
    "rota_tamponu_omru_s": ("SINANMAMIS",
                            "30,0 s; NS-2'nin `RQUEUE_TIMEOUT` gelenegi. "
                            "Sure tavani AYRI bir tavandir ve gereklidir: "
                            "paket sayisi tavani, az sayida paketin SONSUZA "
                            "kadar beklemesini engellemez. DEGERI gerekcesiz. "
                            "⚠️ Olcum penceresi 270 s oldugu icin 30 s ONEMLI "
                            "bir sure — bu parametre PDR'yi ve gecikmeyi "
                            "dogrudan oynatabilir ve Asama 2'de once o "
                            "olculecek"),

    "kuyruk_kapasitesi": ("SINANMAMIS",
                          "50; sonlu olmasi gerekceli, DEGERI degil. "
                          "🔴 ESKI GEREKCE COKTU (9 Eylul 2026): 'mevcut yukte "
                          "hic tasmiyor' iddiasi `aktarilan_paket = 0` olan bir "
                          "kosumdan geliyordu — o alet tek bir paketi bile ara "
                          "dugumde ILERI ILETMEDI, yani kuyruk mekanizmasi hic "
                          "devreye girmedi. Test, parametre ne olursa olsun "
                          "sifir uretirdi. Cok atlamali bir kosum aletiyle ayni "
                          "olcum: kuyruk 50/50 DOLU, 226 tasma. "
                          "Uretici: `python -u kalibrasyon/bag_kumesi.py k l`. "
                          "🔒 Iki kosum aleti soruyu BRAKETLIYOR ama "
                          "CEVAPLAMIYOR (biri mekanizmaya dokunmuyor, oteki "
                          "kasten dongu uretiyor); verdikt Faz 3'te GERCEK bir "
                          "taban cizgisiyle verilir ve kapinin on kosulu artik "
                          "bos gecmeyi engelliyor"),
    "ttl_baslangic": ("SINANMAMIS",
                      "32 — 🔴 BU KAYIT AYNI GUN ICINDE BIR KEZ `TURETILMIS` "
                      "YAPILDI VE GERI ALINDI; sebep kayda geciyor. Turetme su "
                      "idi: dongusuz bir yonlendirmede yol uzunlugu ag CAPINI "
                      "asamaz; cap olculdu (N=40'ta en uzak cift 5 atlama, "
                      "`bag_kumesi.py j`), TTL 32 → marj 6,4x. 🔒 O TURETME "
                      "AYAKTA ama yalnizca bir ALT SINIR veriyor (TTL > cap), "
                      "DEGERI vermiyor. Ve deger onemli cikti: stres altinda "
                      "(dongu ureten kosum aleti) TTL'i YARIYA indirmek PDR'yi "
                      "0,185'ten **0,391**'e cikardi — deneyin cozunurlugunun "
                      "(R = 0,0316) **6,5 KATI**. Uretici: `python -u "
                      "kalibrasyon/bag_kumesi.py l`. Sebep acik: dongudeki "
                      "paketler erken oldugunde kapasite gercek trafige kaliyor. "
                      "⚠️ Etkinin BUYUKLUGU protokolun ne siklikta dongu "
                      "yaptigina baglidir ve GERCEK bir protokol henuz yok; "
                      "kosum aleti KASTEN dongu uretiyor, yani UST SINIRI "
                      "temsil ediyor. Verdikt Faz 3'te, gercek taban "
                      "cizgileriyle. 🔴 ESKI GEREKCE IKI KEZ YANLISTI: "
                      "'ag capi ~3' TESHIS DISKINDEN geliyordu (K-096'da "
                      "gecersiz), ve 'hic baglamiyor' iddiasi "
                      "`aktarilan_paket = 0` olan bir kosumdan — TTL yalniz "
                      "aktarmada azalir, orada ateslenemezdi"),

    "beacon_araligi_s": ("SINANMAMIS",
                         "1 s = AODV `HELLO_INTERVAL` (RFC 3561 §10, `02` "
                         "§R1). Değerin kökeni belli AMA 'hiçbir taban "
                         "çizgisini zayıflatmıyor' iddiası ÖLÇÜLMEDİ: OLSR "
                         "kendi RFC'sinin iki katı hızda beacon yayınlıyor "
                         "(`02` §R3). Ölçülmeden KAYNAK denemez"),
    "beacon_bayt": ("SINANMAMIS", "32 bayt; hiçbir gerekçe yazılmamış"),
    "komsu_omru_katsayisi": ("SINANMAMIS",
                             "10× beacon aralığı; 'protokolü kısıtlamasın' "
                             "gerekçeli ama DEĞER seçilmedi"),

    # --------------------------------------------------------- karıştırıcı
    "karistirici_guc_override_dbm": ("KOL_TANIMI",
                                     "karıştırıcı şiddeti. 🔒 DUYARLILIK "
                                     "BORCU TAŞIMAZ ve sebebi ölçüm: bu "
                                     "sabit duyarlılık denetimini BEKLEMİYOR, "
                                     "çünkü ρ taraması onu zaten yedi güçte "
                                     "oynatıyor (−30 … −6 dBm) ve çalışma "
                                     "noktası o taramanın sonucudur. "
                                     "Varsayılanı `None`: koşu, kalibre "
                                     "edilmiş tabanı kullanır. "
                                     "Üretici: kalibrasyon/karistirici_gucu.py"),
    "karistirici_baslangic_s": ("TURETILMIS",
                               "ölçüm penceresinden: temiz evre 100 s "
                               "(4 000 paket, PDR SE ≈ 0,005), karıştırılmış "
                               "evre 170 s. Toparlanma rota ömrü (89 s) ve "
                               "protokol zamanlayıcıları mertebesinde"),
    "karistirici_konum": ("KOL_TANIMI",
                          "⚠️ OLCULDU, KARAR VERILEMEDI (8 Eylul 2026): etki |D| = 0,048, deneyin cozunurlugu R=0,036'nin USTUNDE ama tohumlar arasi yayilim buyuk oldugu icin kendi hata payi ICINDE. Yani ne duyarsiz denebilir ne duyarli — daha cok tohum gerekiyor. Uretici: `python kalibrasyon/duyarlilik.py statik`. None → alan merkezi. 🔴 Tehdit modeli yeniden "
                          "tasarlanınca yer referanslı geçişe dönecek"),
    # 🔒 DÖRDÜ TEDAVİYE TAŞINDI — 8 Eylül 2026. Bunlar bir donanımın
    # fiziğini iddia etmiyor; "darbeli/taramalı karıştırıcı" KOLUNUN TANIMI.
    # Böyle bir sabitin dış kaynağı olmaz, gerçek bir düşman da onu seçer.
    # 🔴 BORÇ SİLİNMEDİ, YER DEĞİŞTİRDİ: TEDAVİ değişkenleri ön-kayıtta kol
    # tanımı olarak İLAN EDİLİR ve Faz 1 duyarlılık denetiminde OYNATILIR.
    "darbe_periyodu_s": ("KOL_TANIMI",
                         "🔴 OLCULDU VE DUYARLI CIKTI (8 Eylul 2026): kendi kolunda (statik-surekli_darbeli) x2 oynatildiginda PDR **0,093** dusuyor — deneyin cozunurlugu R=0,036'nin 2,6 kati. `statik-surekli` kolunda 'OLCULEMEDI' cikmisti; yanlis kolda bakmak onu aklardi. Uretici: `python kalibrasyon/duyarlilik.py darbeli`. 2,7 s — darbeli kolun tanımı. Tek KISIT rezonans "
                         "yasağı ve ÖLÇÜLDÜ: beacon 1,0 s'ye oran 2,7 (tekrar "
                         "öncesi 10 ayrı faz), trafik 0,25 s'ye oran 10,8 "
                         "(54 ayrı faz). İkisi de tam sayı değil — darbe "
                         "hiçbir periyodik olaya kilitlenmiyor"),
    "darbe_gorev_cevrimi": ("KOL_TANIMI",
                            "🔴 OLCULDU VE DUYARLI CIKTI (8 Eylul 2026): x2 oynatildiginda PDR **0,066** yukseliyor (R=0,036'nin 1,8 kati). Uretici: `python kalibrasyon/duyarlilik.py darbeli`. %50 — darbeli kolun tanımı; açık/kapalı simetri "
                            "noktası, yani en az bilgi taşıyan seçim. Tepe "
                            "telafisi buradan türer ve ölçülerek doğrulandı: "
                            "yayılan ortalama tam −15,00 dBm"),
    "taramali_konak_suresi_s": ("KOL_TANIMI",
                                "🔴 OLCULDU VE DUYARLI CIKTI (8 Eylul 2026): kendi kolunda x0,5'te bant testini 2,2 kat asiyor. Uretici: `python kalibrasyon/duyarlilik.py taramali`. 100 ms — taramalı kolun tanımı; kanalımız "
                                "saniyede ~3,3 kez ziyaret ediliyor. "
                                "⚠️ ÖN-KAYITLI TAHMİN: bu, en hızlı protokol "
                                "zamanlayıcısından (AODV 1 s) 10 kat hızlı "
                                "olduğu için protokoller taramalıyı "
                                "SEYRELTİLMİŞ SÜREKLİ karıştırıcı gibi "
                                "görebilir. Öyleyse sınıf bu konak süresinde "
                                "yeni bir soru sormuyordur — YANLIŞLANABİLİR"),
    "taramali_konak_sayisi": ("KOL_TANIMI",
                              "🔴 OLCULDU VE DUYARLI CIKTI (8 Eylul 2026): iki yonde de bant disi (1,3x ve 1,7x). Uretici: `python kalibrasyon/duyarlilik.py taramali`. 3 konak — taramalı kolun tanımı. ⚠️ ŞİDDET "
                              "SONUCU VAR: ortalama gücü 10·log10(1/3) = "
                              "−4,77 dB düşürüyor, ölçülen −19,88 dBm. "
                              "'Taramalı zayıf çıktı' bulgusu mekanizmaya "
                              "tek başına yazılamaz"),

    # 🔴 İKİSİ SINANMAMIS KALIYOR — bunlar kol tanımı DEĞİL, bir donanımın
    # zamanlamasını İDDİA EDİYOR: değerleri karıştırıcının çerçeve gövdesine
    # değip değmediğini belirliyor. Kaynak gerekir, seçim yetmez.
    "reaktif_sezme_s": ("DUYARSIZ",
                        "Üretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylül 2026). OLCULEN ETKI |Δ| = 0,013 (statik-reaktif kolunda) — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. ⚠️ Iddia SINIRLI: tek basina oynatildiginda (OAT) ve YALNIZ calisma noktasi ciktilarina duyarsiz; protokol SIRALAMASINA duyarliligi Faz 3'te olculur. ESKI GEREKCE: 16 µs sezme; bir alıcının enerji sezme süresini "
                        "iddia ediyor ve `02`de doğrulanmış kaynağı YOK"),
    "reaktif_patlama_s": ("DUYARSIZ",
                          "Üretici: `python kalibrasyon/duyarlilik.py` + `python kalibrasyon/cozunurluk.py` (8 Eylül 2026). OLCULEN ETKI |Δ| = 0,013 (statik-reaktif kolunda) — deneyin cozunurlugu R = 0,0316'nin ALTINDA ve kendi hata payi icinde. ⚠️ Iddia SINIRLI: tek basina oynatildiginda (OAT) ve YALNIZ calisma noktasi ciktilarina duyarsiz; protokol SIRALAMASINA duyarliligi Faz 3'te olculur. ESKI GEREKCE: 144 µs patlama; çevrim %90 görev çevrimi veriyor "
                          "ve gövdenin %90,6'sını kapsıyor — o HESAPLANDI "
                          "ama 144'ün kendisi seçilmedi"),
}


# ===========================================================================
# MODÜL SABİTLERİ — `Konfig` dışındaki davranış belirleyen sayılar
# ===========================================================================
# 🔒 Aynı kovalar, aynı kural. Anahtar `dosya::AD` biçimindedir; mimari
# denetiminin D12 kapısı `sim2/` altındaki modül düzeyi sayısal sabitleri
# tarar ve burada olmayanı BULGU sayar.
#
# ⚠️ Bu sözlük `yapilandirma/` altında ama `kanal/`, `mac/`, `gozlem/`
# sabitlerine atıf yapıyor. Katman ihlali DEĞİL: yalnız DİZGİ tutar, hiçbir
# şey içe aktarmaz. Tek bir köken kaydı olması, ikinci bir kayıt defterinin
# doğmasından iyidir.
MODUL_KOKENLERI: dict[str, tuple[str, str]] = {
    # ------------------------------------------ kontrol düzlemi (K-112)
    "sim2/kanal/cerceve.py::KONTROL_KAPSULLEME": (
        "SINANMAMIS",
        "MAC 24 + FCS 4 + LLC/SNAP 8 + IPv4 20 + UDP 8 = 64 B. IP/UDP/LLC "
        "boyutları RFC 791/768/1042'nin tanımıdır; 802.11 MAC başlığı ve FCS "
        "IEEE 802.11-2016 §9'dadır. ⚠️ Hiçbiri `02`de AÇILIP DOĞRULANMADI, "
        "dolayısıyla `KAYNAK` denemez. Tek bibliyografik kontrolle kapanır. "
        "🔒 Bugün hiçbir ölçülmüş sonucu etkilemez: yalnız `kontrol` çerçeve "
        "tipinde kullanılır ve o tipi kuran protokol henüz yok"),
    "sim2/kosum/kontrol.py::BEKLEYEN_UYANDIRMA_TAVANI": (
        "SINANMAMIS",
        "Düğüm başına bekleyen DİNAMİK uyandırma tavanı. 🔒 Bir güvenlik "
        "sınırıdır, fizik değil: aşıldığında koşu deterministik olarak DURUR "
        "(sözleşme kararı 2), yani TAMAMLANAN hiçbir koşunun sonucunu "
        "değiştiremez — yalnız patolojik bir koşunun ne zaman durduğunu "
        "belirler. ⚠️ Değeri ilk gerçek protokolde (Faz 3) ölçülen tepe "
        "bekleyen sayısından türetilmeli; tepe her koşuda teşhise yazılıyor"),
    # ------------------------------------------------- fiziksel sabitler
    "sim2/kanal/yayilim.py::BOLTZMANN": (
        "KAYNAK", "SI tanımlı sabit; tartışma konusu değil"),
    "sim2/kanal/yayilim.py::ISIK_HIZI": (
        "KAYNAK", "SI tanımlı sabit; tartışma konusu değil"),

    # --------------------------------------------------------- türetilmiş
    "sim2/kanal/yayilim.py::REFERANS_MESAFE_M": (
        "TURETILMIS",
        "1 m — log-mesafe modelinin referansı. Serbest bir seçim değil: "
        "PL(1 m) kapalı formda hesaplanıyor ve model onun üstüne kuruluyor"),

    # ---------------------------------------------- performans (sonucu değiştirmez)
    "sim2/kanal/sonumleme.py::YENILIK_ONBELLEK_SINIRI": (
        "OLCULMUS",
        "kalibrasyon/sonumleme_onbellegi.py — 1 000 000 · 250 000 · 100 000 "
        "sınırlarının ÜÇÜ de sınırsız hâlle BİREBİR aynı sonucu verdi; "
        "ıskalama artışı sırasıyla %0,09 · %0,36 · %0,88"),
    "sim2/kanal/yayilim.py::KOSE_ONBELLEK_SINIRI": (
        "OLCULMUS",
        "1<<19 gölgeleme köşe önbelleği. 🟢 18 Eylül 2026'da ÖLÇÜLDÜ "
        "(`python -u kalibrasyon/sonumleme_onbellegi.py 4`): sınır 1 024 ↔ "
        "4 194 304 arasında **4 096 kat** oynatıldı, DÖRT değerde de sonuç "
        "satırı VE ham teslim imzası BİREBİR aynı çıktı (hareketli kol, "
        "`bagimsiz-yok` 1000, 50 s). Ölçüt taramadan ÖNCE yazıldı. Bedel "
        "yalnız süre: en küçük sınırda %7 yavaşlama (133 → 142 s). Saf "
        "memo olduğu artık bir iddia değil, bir kapı"),

    # ------------------------------------------------------- karıştırıcı
    "sim2/yapilandirma/senaryolar.py::MOBILITE_BOLUNME": (
        "OLCULMUS",
        "Üretici: `python -u kalibrasyon/dugum_sayisi.py --bolunme` "
        "(16 Eylül 2026, B6). Dört mobilite kolu × 40 ana deney tohumu × "
        "ölçüm penceresindeki dokuz an; bağ tanımı KÂHİN GRAFİĞİ — çalışma "
        "noktasının seçildiği tanımın aynısı (C1 · `calisma_noktasi.py`). "
        "Bölünmüş (kol, tohum) çifti 15/160: bagimsiz 6 · gorev 7 · "
        "formasyon 2 · statik 0. 🔒 Statik kolun SIFIR çıkması bir KONTROLDÜR: "
        "bölünme yalnız hareketten doğabilir, orada sıfır çıkmasaydı ölçümün "
        "kendisi bozuk olurdu. 🔴 En kötü hücre formasyon/2011: dokuz anın "
        "yedisinde bölünmüş. ⚠️ Karıştırıcı bu tanımın DIŞINDA (`-yok` "
        "senaryoları) ve dokuz AN örneklenir, süreklilik değil — sayı bir "
        "ALT SINIRDIR. ⚠️ İlk ölçüm yalnız t = 0'da ve statik kolda "
        "yapılmıştı, 0/40 verip YANILTMIŞTI."),
    "sim2/yapilandirma/senaryolar.py::BOLUNME_OLCULEN_ARALIK": (
        "KOL_TANIMI",
        "Ana deney tohumları (2000–2039), `06` §2. Hangi tohumların "
        "ölçüldüğünü tanımlar; bu aralığın DIŞINDAKİ bir tohumda "
        "`bolunme_payi` `None` döner — *'bölünme yok'* ile *'bakılmadı'* "
        "ayrı (`None ≠ 0`). Duyarlılık borcu YOK: bir ölçümün kapsamıdır, "
        "sonucu belirleyen bir değer değildir."),
    "sim2/yapilandirma/senaryolar.py::MOBILITE_THETA": (
        "OLCULMUS",
        "Üretici: `python -u kalibrasyon/theta_kollari.py` (14 Eylül 2026; "
        "6 tohum × 350 s × 40 çift). Kol başına (Θ_OLSR, Θ_AODV, hiç "
        "kopmayan çift oranı). Bağ tanımı yavaş SINR ≥ eşik — "
        "`kopma_fiziksel` ile AYNI; soldan kesme ve Kaplan–Meier düzeltmesi "
        "K-101'in gövdesinden. Bağımsız kolda 3,25 birebir yeniden "
        "üretildi. 🔴 Formasyonun 2,31'i ASAĞI YANLIDIR ve tablodaki üçüncü "
        "sayı bunu söyler: çiftlerin %92,1'i hiç kopmuyor, ölçüme yalnız "
        "eşiğin kıyısındakiler giriyor (K-122)"),
    "sim2/yapilandirma/senaryolar.py::KARISTIRICI_GUCU_DBM": (
        "OLCULMUS",
        "kalibrasyon/karistirici_gucu.py — REFERANS sınıfta (`surekli`) "
        "seçildi: 30 tohumun hiçbirinde birden fazla çok üyeli bileşen "
        "yokken ρ en büyük → −15,0 dBm · ρ = 0,258. Beş sınıfın beşinde "
        "aynı TABAN; eşitleme yayılan ortalama güç üzerinden yapılır "
        "(etkiyi eşitlemek döngüsel olurdu). Ölçülen ortalamalar: sürekli "
        "−15,00 · darbeli −15,00 · aldatıcı −15,10 · taramalı −19,88 dBm"),

    # ------------------------------------------------------------ model
    "sim2/kanal/sonumleme.py::FIR_EN_COK_KATSAYI": (
        "TURETILMIS",
        "64 × 190 µs = 12,2 ms. Marjinal varyans `c` ile "
        "düzeltildiği için derinliği değil yalnız korelasyonun taşındığı "
        "mesafeyi belirliyor"),
    "sim2/kanal/sonumleme.py::BAGIL_HIZ_TABANI_MS": (
        "SINANMAMIS",
        "1 m/s tabanı; sıfır hızın M'i patlatmasını engelliyor ama DEĞER "
        "seçilmedi. K-102'den sonra TAM ÖLÇEK Doppler hızına uygulanıyor "
        "ve orada çiftlerin yalnız %0,1'inde bağlıyor (önce %84,4 idi) — "
        "yani artık baskın değil, ama değeri hâlâ türetilmedi"),
    "sim2/dunya/mobilite.py::ISTASYON_TUTMA_S": (
        "SINANMAMIS",
        "2 s istasyon tutma zaman sabiti; araç dinamiğinden türetilmeli. "
        "Y6'dan beri görev VE formasyon kolları ortak kullanıyor "
        "(`_istasyonlari_izle`), yani borç iki kolu birden taşıyor"),

    # --------------------------------------------------- rapor şeması
    # 🔒 D12'nin KÖR NOKTASI kapatılınca göründü (8 Eylül 2026): denetim
    # önce yalnız SKALER sabitleri tarıyordu, sayı TABLOLARI defterden
    # tamamen kaçıyordu.
    "sim2/olcum/metrikler.py::YUZDELIKLER": (
        "TURETILMIS",
        "(50, 95, 99) — ortanca + iki kuyruk. Bir DEĞER seçimi değil, "
        "sonuç şemasının kapalı listesi: sonradan eklemek eski satırları "
        "karşılaştırılamaz yapar. Karara değil rapora girer"),

    # ------------------------------------------------- evre metrik kafesi
    # 🔴 İKİSİ DE RFC DEĞERİDİR AMA `KAYNAK` DEĞİLDİR — ve bu ayrım önemli.
    # `02-DOGRULANMIS-KAYNAKLAR.md` RFC 3561/3626'yı *"Faz 1'in girdisi"*
    # diye listeliyor: ikinci el bir taramadan geldiler, birincil kaynak
    # AÇILMADI. Kova kuralı net — `KAYNAK` yalnız `02`de doğrulanmış olandır.
    #
    # ⭐ VE BU TEK BİR DOĞRULAMAYLA KAPANIR, ÜÇ KARARI BİRDEN TAŞIYARAK:
    # aynı iki RFC, K-101'in Θ paydasını (OLSR TOP_HOLD_TIME) ve K-103'ün
    # bağlantılılık kısıtının zaman anlamını (AODV ACTIVE_ROUTE_TIMEOUT) da
    # çıpalıyor. Üç karar da bugün açılmamış bir kaynağa dayanıyor.
    "sim2/olcum/evre.py::IZGARA_ADIMI_S": (
        "KAYNAK",
        "1 s — RFC 3561 §10, AODV `HELLO_INTERVAL` = '1,000 Milliseconds'. "
        "Birincil belge 8 Eylül 2026'da açıldı ve `02` §R1'e işlendi. Evre "
        "kafesinin ÇÖZÜNÜRLÜĞÜ: iki taban çizgisinin komşu yenileme "
        "aralıkları AODV 1 s ve OLSR 2 s (RFC 3626 §18), yani 1 s EN "
        "HIZLISIDIR — daha ince bir ızgara hiçbir protokolün "
        "gösteremeyeceği bir hızı ölçmeye çalışırdı"),
    "sim2/olcum/evre.py::PENCERE_S": (
        "KAYNAK",
        "15 s — RFC 3626 §18, OLSR `TOP_HOLD_TIME` = '3 x TC_INTERVAL' ve "
        "`TC_INTERVAL` = '5 seconds'. Birincil belge 8 Eylül 2026'da açıldı "
        "ve `02` §R2'ye işlendi. Evre kafesinin DURAĞANLIĞI: en yavaş taban "
        "çizgisinin topoloji bilgisini tuttuğu süre. AYNI ÇAPA Θ'nın "
        "paydasıdır (K-101) — iki yerde iki farklı çapa kullanmak, ikisinin "
        "ayrışması demek olurdu"),
    "sim2/olcum/evre.py::ALFA": (
        "SINANMAMIS",
        "0,05 — evre metriklerinin TEK anlamlılık sabiti (Y10, K-123). "
        "Ön-kayıt (`06` §7) tek bir aile düzeyi hedefi ilan ediyor ve iki "
        "eski sabit (2,0 · 0,01) artık buradan TÜRÜYOR; `BANT_SE_KATI` "
        "`z(1 − α/2)` olduğu için ayrı bir kayıt taşımıyor. 🔴 Değerin "
        "KENDİSİ hâlâ bir gelenek: `02`de doğrulanmış bir kaynağa bağlı "
        "değil. Ölçülen şey değer değil KURAL — Bonferroni'yle boş "
        "hipotezde yanlış alarm %2,2–3,4, eski kuralda %37–70. Üretici: "
        "`python -u kalibrasyon/anlamlilik_sabitleri.py`"),

    # ------------------------------------------------- gözlem yükü faturası
    "sim2/gozlem/yuk.py::YUK_BOOL_BAYT": (
        "TURETILMIS", "1 bayt — bir bool'un kablodaki asgari bedeli"),
    "sim2/gozlem/yuk.py::YUK_FLOAT_BAYT": (
        "TURETILMIS", "4 bayt — tek duyarlıklı float; çift duyarlık bir "
                      "protokol için savunulamaz bir lüks"),
    "sim2/gozlem/yuk.py::YUK_INT_TABAN_BAYT": (
        "TURETILMIS", "1 bayt taban; büyüklüğe göre büyüyor"),

    # ------------------------------------------------------ teşhis sınırları
    "sim2/gozlem/teshis.py::TESHIS_EN_UZUN_AD_BAYT": (
        "TURETILMIS", "teşhis sözlüğü rapora girer, karara girmez; sınırlar "
                      "bellek koruması"),
    "sim2/gozlem/teshis.py::TESHIS_EN_UZUN_DIZGI_BAYT": (
        "TURETILMIS", "aynı gerekçe"),
    "sim2/gozlem/teshis.py::TESHIS_EN_COK_ALAN": (
        "TURETILMIS", "aynı gerekçe"),
    "sim2/gozlem/teshis.py::TESHIS_EN_COK_ELEMAN": (
        "TURETILMIS", "aynı gerekçe"),

    # =======================================================================
    # ÖLÇÜM ALETLERİ — `kalibrasyon/` · 9 Eylül 2026, D13 kapısıyla eklendi
    # =======================================================================
    # 🔴 NEDEN BURADALAR. `sim2/` 52 dosya ve 12 kapıyla korunuyordu,
    # `kalibrasyon/` 24 dosya ve TEK kapıyla ("import edilebiliyor mu").
    # 8–9 Eylül oturumundaki kusurların HEPSİ korumasız yarıdaydı: kapalı bir
    # karıştırıcıyı ölçen üç tablo, eşleştirilmemiş bir istatistik, sınırda
    # çöken bir hata payı, hiç oynatılmamış bir parametre.
    #
    # 🔒 Bir ölçüm aletinin sayısı, modelin sayısından daha az tehlikeli
    # DEĞİLDİR — ölçtüğü şeyi o belirler. `ATLAMA_ESIGI` bunun en net örneği:
    # çalışma noktası ρ = 0,258, o eşikle tanımlanmış bir grafikte ölçüldü.

    # ------------------------------------------------- kâhin grafiği
    "kalibrasyon/kahin.py::ATLAMA_ESIGI": (
        "OLCULMUS",
        "0,90 — bir bağın 'kullanılabilir' sayılması için gereken atlama "
        "başarısı. Üretici: `python -u kalibrasyon/bag_kumesi.py b d` "
        "(9 Eylül 2026). ÖLÇÜT: kararların DEĞİŞMEDİĞİ platonun EN KÜÇÜK "
        "değeri — yani bağ kümesini en büyük yapan eşik, kararların sabit "
        "kalması kısıtı altında. Bu, alan seçimi (kopukluk sıfırken en büyük "
        "alan) ve karıştırıcı gücü (ayrılma yokken en büyük ρ) ölçütleriyle "
        "AYNI biçimdedir. ÖLÇÜLEN PLATO: {0,90; 0,95; 0,99} üçünde de "
        "seçilen güç −15,0 dBm ve ölçüt bedelinin tabandan farkı hem kendi "
        "2 SE bandının hem R = 0,036'nın içinde. ⚠️ BU KAYIT 30 TOHUMLUK R'ye karşı yazıldı ve 40 tohumluk R = 0,0316 ile YENİDEN SINANMADI: farkın sayısı kayıtta olmadığı için denetlenemedi (K-128). 0,80'de ölçüt bedeli "
        "+0,030 (DUYARLI), 0,70'te +0,055 (DUYARLI) ve seçilen güç "
        "−12,0 dBm'e KAYIYOR. 🔴 İKİ SINIR BEYAN EDİLİR: (a) ölçüt taramayı "
        "GÖRDÜKTEN SONRA formüle edildi — plato ölçüldü, sonra 'platonun alt "
        "kenarı' kuralı yazıldı; (b) plato kenarı yalnız TARANAN ızgarada "
        "(0,70·0,80·0,90·0,95·0,99) bilinir, gerçek kenar (0,80; 0,90] "
        "aralığındadır. ⚠️ Standart ×0,5 oynatması (0,45) bu platonun "
        "DIŞINDADIR; yani bu sayı `DUYARSIZ` DEĞİLDİR — bandıyla birlikte "
        "ölçülmüştür ve band aşağı yönde bağlayıcıdır"),
    "kalibrasyon/kahin.py::SONUMLEME_ORNEGI": (
        "DUYARSIZ",
        "6 ornek. Uretici: `python -u kalibrasyon/bag_kumesi.py c e` (9 Eylul 2026) + `python kalibrasyon/adim4_kapanis.py` bolum E. DONUK kolda K SONUCU HIC DEGISTIRMIYOR (K = 1…32 icin derece 8,100000, alti ornekleme fazinda yayilim TAM SIFIR) — kanitli. HAREKETLI kolda IKI AYRI OLCUM ve IKISI FARKLI SEY SOYLUYOR: (a) GRAFIK duzeyinde kestiricinin kendi gurultusu K ile DUSUYOR — derece yayilimi K=4'te 0,65, K=8'de 0,40, K=16'da 0,25; (b) ama K'nin besledigi ASIL karar olan KAHIN PDR'sinde gurultu K ile DUSMUYOR: faz yayilimi K=4'te 0,071, K=8'de 0,030, K=16'da 0,045 — tekduze DEGIL, ucu de R = 0,0316 mertebesinde. 🔒 YORUM: daha iyi bir grafik kestirimi daha KARARLI bir rota secimi uretmiyor; yakin rotalar arasindaki esitlikler kucuk tahmin degisimleriyle yer degistiriyor. Yani K'yi buyutmenin OLCULEBILIR bir faydasi YOK ve deger 6'da BIRAKILDI. ⚠️ UC BEYAN EDILEN SINIR: (1) PDR olcumu yalniz 3 tohum — yayilim kestiricisinin kendisi gurultulu, K egrisi cozulmedi; (2) iddia yalniz taranan aralik icin (4…16); (3) fazlar ornekleme ADIMI oynatilarak uretildi ve ilk ornek butun fazlarda ORTAK, yani olculen gurultu ~1/K kadar EKSIK. 🔴 ONCEKI ARA SONUC GERI ALINDI: derece yayilimini gorev kolu esitlemesinin 0,3 toleransiyla karsilastirip 'K = 16 gerekli' demistim — o tolerans BASKA bir karara ait. Kararin kendi birimi PDR ve orada fark yok"),
    "kalibrasyon/kahin.py::SONUMLEME_ADIMI_S": (
        "TURETILMIS",
        "5 ms — sönümleme tutarlılık süresinden (~2 ms) BÜYÜK seçildi ki "
        "örnekler bağımsız olsun; küçük seçilseydi aynı fade tekrar sayılırdı"),
    "kalibrasyon/kahin.py::ETX_TAVANI": (
        "TURETILMIS",
        "1e9 — p = 0 olan bağlar için sonsuz yerine büyük bir sayı; "
        "Dijkstra'yı basitleştirir ve bu bağlar zaten hiç seçilmez. Bir DEĞER "
        "seçimi değil, sonsuzun sonlu karşılığı"),

    # ------------------------------------------------- çalışma noktası
    "kalibrasyon/calisma_noktasi.py::BASARI_ESIGI": (
        "SINANMAMIS",
        "0,90 — `kahin.py::ATLAMA_ESIGI` ile AYNI sayı ve aynı borç. İkisinin "
        "aynı olması bilinçli (iki yerde iki eşik olsaydı ayrışırlardı) ama "
        "değer hâlâ türetilmedi"),
    "kalibrasyon/calisma_noktasi.py::SONUMLEME_ORNEGI": (
        "DUYARSIZ",
        "6 ornek. Uretici: `python -u kalibrasyon/bag_kumesi.py c e` (9 Eylul 2026) + `python kalibrasyon/adim4_kapanis.py` bolum E. DONUK kolda K SONUCU HIC DEGISTIRMIYOR (K = 1…32 icin derece 8,100000, alti ornekleme fazinda yayilim TAM SIFIR) — kanitli. HAREKETLI kolda IKI AYRI OLCUM ve IKISI FARKLI SEY SOYLUYOR: (a) GRAFIK duzeyinde kestiricinin kendi gurultusu K ile DUSUYOR — derece yayilimi K=4'te 0,65, K=8'de 0,40, K=16'da 0,25; (b) ama K'nin besledigi ASIL karar olan KAHIN PDR'sinde gurultu K ile DUSMUYOR: faz yayilimi K=4'te 0,071, K=8'de 0,030, K=16'da 0,045 — tekduze DEGIL, ucu de R = 0,0316 mertebesinde. 🔒 YORUM: daha iyi bir grafik kestirimi daha KARARLI bir rota secimi uretmiyor; yakin rotalar arasindaki esitlikler kucuk tahmin degisimleriyle yer degistiriyor. Yani K'yi buyutmenin OLCULEBILIR bir faydasi YOK ve deger 6'da BIRAKILDI. ⚠️ UC BEYAN EDILEN SINIR: (1) PDR olcumu yalniz 3 tohum — yayilim kestiricisinin kendisi gurultulu, K egrisi cozulmedi; (2) iddia yalniz taranan aralik icin (4…16); (3) fazlar ornekleme ADIMI oynatilarak uretildi ve ilk ornek butun fazlarda ORTAK, yani olculen gurultu ~1/K kadar EKSIK. 🔴 ONCEKI ARA SONUC GERI ALINDI: derece yayilimini gorev kolu esitlemesinin 0,3 toleransiyla karsilastirip 'K = 16 gerekli' demistim — o tolerans BASKA bir karara ait. Kararin kendi birimi PDR ve orada fark yok"),
    "kalibrasyon/calisma_noktasi.py::UZAK_KESME_M": (
        "TURETILMIS",
        "1200 m — bu mesafenin ötesinde PER zaten 1; hesap kısaltması. "
        "Sonucu değiştiremez, yalnız işi azaltır"),
    "kalibrasyon/calisma_noktasi.py::ALANLAR": (
        "TEDAVI",
        "(1000…2000 m) — alan büyüklüğü TARAMASININ ekseni. Bir değer değil, "
        "aranan aralık; çalışma noktası (1800 m) bu taramanın SONUCU"),

    # ------------------------------------------------- çalkantı (Θ)
    "kalibrasyon/calkanti.py::OLSR_TOP_HOLD_S": (
        "KAYNAK",
        "15 s — RFC 3626 §18, OLSR `TOP_HOLD_TIME` = 3 × `TC_INTERVAL` ve "
        "`TC_INTERVAL` = 5 s. Birincil belge 8 Eylül 2026'da açıldı, `02` §R2. "
        "Θ'nın PAYDASI budur"),
    "kalibrasyon/duyarlilik.py::R_ESLESTIRILMIS": (
        "OLCULMUS",
        "0,0230 — deneyin ESLESTIRILMIS cozunurlugu. Uretici: "
        "`python -u kalibrasyon/cozunurluk.py --tohum 40` (15 Eylul 2026, C7; "
        "satir `olcut_bedeli`). 🔒 Bu sabit `duyarlilik.py`nin KARARINA girer: "
        "bir parametre, etkisi kendi bandinin ICINDE **ve** R'den KUCUK ise "
        "`DUYARSIZ` olur; biri yetmez. 16 Eylul 2026'ya kadar alet yalnizca "
        "band ayagini uyguluyordu ve R yalniz duzyazidaydi — o bosluga "
        "fiilen dusuldu (`golgeleme_hucre_m`: 6 PDR puanlik etki 'duyarsiz' "
        "diye aklaniyordu). 🔒 ESLESTIRILMIS olan secildi, en gevsek olan "
        "degil: on-kayittaki birincil test de (Wilcoxon, `06` §7) bu aletin "
        "kendi farki da (`_esli_fark`) eslestirilmistir. 🔒 BAYATLIK KAPISI: "
        "`cozunurluk.py` R'yi yeniden olcer ve bu sabitle karsilastirir; "
        "0,0005'ten cok ayrisirsa kirmizi yanar."),
    "kalibrasyon/calkanti.py::ETKIN_YARICAP_M": (
        "DUYARSIZ",
        "400 m — rota ömrü TARAMASINDA 'bağ var' sayılan yarıçap. "
        "🔒 ARTIK BİR KARAR TAŞIMIYOR: Θ 9 Eylül 2026'da YAVAŞ SINR "
        "tanımıyla yeniden türetildi (`python -u kalibrasyon/bag_kumesi.py h`) "
        "ve hızlar oradan geliyor. Bu yarıçap yalnız `calkanti.py`nin HIZLI "
        "TARAMASINDA kullanılıyor — bir teşhis. Ölçüldü: disk gölgelemeyi "
        "görmediği için rota ömrünü İKİ KAT uzun gösteriyor (89 s ↔ 43 s), "
        "yani K-096'nın 'tek yarıçap bağ kümesini temsil edemez' ölçümü "
        "(Jaccard 0,53) rota ömründe de doğrulandı"),
    "kalibrasyon/calkanti.py::ADIM_S": (
        "SINANMAMIS",
        "1 s — rota ömrü örnekleme adımı. Ölçülen ömür (89 s) adımın çok "
        "üstünde, yani muhtemelen duyarsız — ama ÖLÇÜLMEDİ"),
    "kalibrasyon/calkanti.py::BITIS_S": (
        "TURETILMIS",
        "350 s — `Konfig.kosu_bitis_s` ile aynı koşu uzunluğu; Θ ölçümü "
        "gerçek koşuyla aynı zaman ölçeğinde yapılsın diye"),
    "kalibrasyon/calkanti.py::CIFT_SAYISI": (
        "SINANMAMIS",
        "40 çift — tohum başına izlenen kaynak-hedef çifti. Örnekleme "
        "büyüklüğü; Θ'nın hata payını belirliyor ama seçilmedi"),
    "kalibrasyon/karistirici_gucu.py::TESHIS_X": (
        "TURETILMIS",
        "0,60 — teşhis varyantının batıya kaydırılmış x'i (depodaki 0,75 "
        "yerine). Bir ölçüt değil, *konum mu suçlu* sorusunun ikinci "
        "noktası; cevap HAYIR çıktı (K-127)"),
    "kalibrasyon/yere_toplama_yuku.py::MARJ_HIZLARI": (
        "TURETILMIS",
        "(2,25 · 2,50) — ilan edilmiş ızgaranın 2,0 ile 3,0 arasındaki "
        "boşluğunu dolduran iki nokta. 🔒 Bir ÖLÇÜT DEĞİL: seçilen hızı "
        "büyütemez, yalnız çalışma noktasının uçuruma uzaklığını ölçer "
        "(K-126)"),
    "kalibrasyon/yere_toplama_yuku.py::ESLER_HIZLARI": (
        "TURETILMIS",
        "(4,0 · 8,0) — bugünkü eşler arası akış hızı ve İKİ KATI; ikincisi "
        "*iki deseni 80 pkt/s'te eşitlemek mümkün mü* sorusunun cevabıdır "
        "(geçti, ama kullanılmadı: öğrenci 1,0'da kaldı — K-126)"),
    "kalibrasyon/yere_toplama_yuku.py::ADAYLAR_HZ": (
        "TEDAVI",
        "(0,5…3,0 pkt/s) — telemetri hızı TARAMASININ ekseni. Bir değer "
        "değil, aranan aralık; bugünkü varsayılan (1,0) içeride, seçilen "
        "hız bu taramanın SONUCU (K-126)"),
    "kalibrasyon/yere_toplama_yuku.py::KOMUT_ORANI": (
        "TURETILMIS",
        "0,25 — komut hızı telemetriye ORANLA gider; bugünkü çiftin "
        "(1,0 ↔ 0,25) oranı korunur. Ayrı bir eksen açmak taramayı iki "
        "boyutlu yapardı ve komut akışı yükün küçük parçasıdır"),
    "kalibrasyon/yere_toplama_yuku.py::TESLIM_ESIGI": (
        "TEDAVI",
        "0,95 — ilan edilmiş ölçüt (K-124): karıştırıcısız kolda kâhin "
        "PDR bu eşiğin üstünde kalmalı. Ölçütün kendisi; taramadan ÖNCE "
        "öğrenci onayıyla yazıldı, ölçülen bir sayı değil"),
    "kalibrasyon/yere_toplama_yuku.py::YAN_GOZLEM_PENCERESI": (
        "TURETILMIS",
        "Kısa pencere (ısınma 10 s · ölçüm 30 s · koşu 50 s) — regresyon "
        "matrisinin kısa vakalarıyla AYNI. Yan gözlem bir KAPI değildir ve "
        "hareketli kolda tam uzunluk kâhin koşusu 10 dakikanın üstünde "
        "sürüyor (ölçüldü)"),
    "kalibrasyon/dugum_sayisi.py::ADAYLAR": (
        "TEDAVI",
        "(30…50) — düğüm sayısı TARAMASININ ekseni; `12` §3 C1 aralığı. "
        "Bir değer değil, aranan küme. Sonuç: adaylar ayrılamadı (K-125)"),
    "kalibrasyon/dugum_sayisi.py::ALAN_CAPASI_M": (
        "OLCULMUS",
        "1800 m — N = 40 için ölçülmüş alan çapası "
        "(`kalibrasyon/calisma_noktasi.py`); tarama alanı bundan türer "
        "(alan = 1800 × karekök(N/40)), yani yoğunluk sabit kalır"),
    "kalibrasyon/dugum_sayisi.py::CAPA_N": (
        "TURETILMIS",
        "40 — çapanın ölçüldüğü düğüm sayısı; `ALAN_CAPASI_M` ile AYNI "
        "ölçümden gelir, ondan ayrı bir seçim değildir"),
    "kalibrasyon/dugum_sayisi.py::ALTERNATIF_ORAN": (
        "TEDAVI",
        "0,90 — ilan edilmiş sert kısıt (K-124): geçide düğüm-ayrık ikinci "
        "yolu olan kaynakların en az bu payı. Ölçütün kendisi; taramadan "
        "ÖNCE öğrenci onayıyla yazıldı, ölçülen bir sayı değil"),
    "kalibrasyon/aodv_uygunluk.py::U1_ESIK_STATIK": (
        "TEDAVI",
        "0,90 — U1'in statik koldaki ölçütü (`06` §4.3): AODV'nin PDR'si, "
        "AYNI konfigürasyonda koşan ETX kâhininin PDR'sine bu orandan az "
        "olamaz. Ölçütün kendisi; öğrenci kararı (K-136), ölçülen bir sayı "
        "DEĞİL. ⚠️ Ölçüm GÖRÜLDÜKTEN SONRA seçildi ve bu, ön-kayıt "
        "disiplininin zayıf tarafıdır — U1 bir kabul kapısı olduğu ve hiçbir "
        "sonuç iddiası ona dayanmadığı için taşınıyor; gerekçe dosyanın "
        "başlığında açık. Üretici: "
        "`python -u kalibrasyon/aodv_uygunluk.py`"),
    "kalibrasyon/aodv_uygunluk.py::U1_ESIK_HAREKETLI": (
        "TEDAVI",
        "0,60 — U1'in hareketli koldaki ölçütü. Statikten düşük olmasının "
        "sebebi `06` §4.3'te zaten yazılı: kâhin her an en güvenilir yolu "
        "BİLİR, gerçek protokol onu HELLO gecikmesi kadar sonra öğrenir. "
        "Ölçütün kendisi; öğrenci kararı (K-136). Aynı zayıflık beyanı "
        "`U1_ESIK_STATIK`teki gibidir. Üretici: "
        "`python -u kalibrasyon/aodv_uygunluk.py`"),
    "kalibrasyon/aodv_uygunluk.py::TOHUMLAR": (
        "TEDAVI",
        "(1000, 1001, 1002) — GELİŞTİRME tohumları. Ana deney tohumları "
        "(2000–2039) burada koşulmaz: `06` §0.2 *'hiçbir kolda koşulmaz'* "
        "der ve mühür bozulmaz. Üç tohum bir kabul kapısı için yeterlidir; "
        "U1 bir hipotez testi değildir, güç hesabı gerektirmez"),
    "kalibrasyon/sonumleme_onbellegi.py::KOSE_SINIRLARI": (
        "TEDAVI",
        "(1<<22, 1<<19, 1<<14, 1<<10) — gölgeleme köşe önbelleği sınırının "
        "TARAMA ekseni, bir değer değil. Aralık 4 096 kat seçildi: memo saf "
        "değilse bu genişlikte kesinlikle ayrışır. Varsayılan (1<<19) "
        "aralığın ortasında. Üretici: "
        "`python -u kalibrasyon/sonumleme_onbellegi.py 4`"),
    "kalibrasyon/aodv_uygunluk.py::ACIKLANMIS_DUSUK": (
        "TEDAVI",
        "U1-B'nin açıklanmış düşük hücreleri, PROTOKOL BAŞINA (`06` §4.4 "
        "madde 3 · K-137 · K-142: bir protokolün açıklaması öbürünü aklamaz). "
        "Bir eşik değil, bir MUAFİYET listesi ve girmesinin şartı ÖLÇÜM: "
        "kaybın protokolün kendi mekanizmasından geldiği gösterilmiş olmalı. "
        "🔒 Liste iki yönden denetleniyor — listede olmayan düşük hücre ve "
        "artık düşük olmayan liste kaydı, ikisi de kapıyı kırmızı yakar"),
    "kalibrasyon/aodv_uygunluk.py::U3_SURELERI_S": (
        "TEDAVI",
        "(60, 120) s — U3 yük profilinin ÖLÇÜM ekseni, bir değer değil. İki "
        "süre, yükün süreyle nasıl büyüdüğünü tek bir oranla söyler: ~2 sabit "
        "hız, belirgin biçimde 2'nin altı başta yığılan yük. Küçük test "
        "dünyası `tests2/test_kosum.py::_konfig`. Üretici: "
        "`python -u kalibrasyon/aodv_uygunluk.py u3` (K-144)"),
    "kalibrasyon/aodv_uygunluk.py::DUMAN_PENCERESI": (
        "TURETILMIS",
        "Kısa pencere (ısınma 10 s · ölçüm 40 s · koşu 50 s) — duman kesiti "
        "SAYIYI ÜRETMEZ. Tam pencerede tek bir (AODV, kâhin) çifti 505 s "
        "sürüyor, yani `uretici_duman.py`nin 'ucuz kesit' sözleşmesi tam "
        "pencereyle tutturulamaz. `yere_toplama_yuku.py::YAN_GOZLEM_PENCERESI` "
        "ile AYNI idiom ve aynı beyan"),
    "kalibrasyon/aodv_uygunluk.py::DUMAN_TOHUMLARI": (
        "TEDAVI",
        "(1000,) — duman kesitinin tohumu; `TOHUMLAR`ın ilki. Kesit SAYIYI "
        "ÜRETMEZ, yalnız aletin hâlâ koştuğunu gösterir (`uretici_duman.py` "
        "sözleşmesi): tam koşum 24 koşumdur, duman 2'dir"),
    "kalibrasyon/formasyon_olcumu.py::YARICAP_M": (
        "SINANMAMIS",
        "530 m — komşu çift süzgeci; kullanılabilir bağ yarıçapının mertebesi "
        "(`Konfig.gorev_grup_yaricapi_m` notu, K-097), ölçümden ELLE "
        "aktarıldı. Bir ölçüt değil: bağıl hız teşhisinin hangi çiftlere "
        "bakacağını söyler (K-118)"),
    "kalibrasyon/formasyon_olcumu.py::ORNEK_ADIM_S": (
        "SINANMAMIS",
        "5 s — bağıl hız örnekleme aralığı; mobilite tikinden (0,5 s) büyük, "
        "ölçüm penceresinden (270 s) çok küçük. Değeri seçilmedi (K-118)"),
    "kalibrasyon/theta_kollari.py::AODV_ACTIVE_ROUTE_S": (
        "KAYNAK",
        "3 s — RFC 3561 §10, AODV `ACTIVE_ROUTE_TIMEOUT` = '3,000 Milliseconds'. "
        "Birincil belge 8 Eylül 2026'da açıldı ve `02` §R1'e işlendi; "
        "`olcum/evre.py::IZGARA_ADIMI_S` ile AYNI kaynak. Θ'nın ikinci paydası"),

    # ------------------------------------------------- görev kolu
    "kalibrasyon/gorev_kalibrasyonu.py::DERECE_TOLERANSI": (
        "TEDAVI",
        "0,3 — görev kolunun bağımsız kolla EŞİTLENDİĞİ ölçüt. Bir fizik "
        "sabiti değil, deney tasarımı kararı: iki kol aynı derecede "
        "buluşsun ki fark mobilite YAPISINDAN gelsin"),
    "kalibrasyon/gorev_kalibrasyonu.py::UYE_TABANI": (
        "SINANMAMIS",
        "4 — müfreze başına en az üye. Müfrezelerin klik olmasını engelleyen "
        "alt sınır; değeri seçilmedi"),

    # ------------------------------------------------- ölçüm tasarımı
    "kalibrasyon/duyarlilik.py::TOHUMLAR": (
        "SINANMAMIS",
        "5 tohum — duyarlilik taramasinin orneklem buyuklugu. 🔴 ONCE `OLCULMUS` yazmistim ve YANLISTI: `cozunurluk.py` 30 tohumun cozunurlugunu olcuyor, 5 tohumun YETERLILIGINI degil. Deger secildi. Sonucu beyan edilmis bir sinirdir: 5 tohumla `2 SE` kati bir %95 testi degil, olcut kasten asimetrik. Daraltmanin yolu tohum sayisini artirmaktir"),
    "kalibrasyon/duyarlilik.py::CARPANLAR": (
        "TURETILMIS",
        "(0,5; 2,0) — ölçekten bağımsız TEK çarpan. Süre, sayı, mesafe, "
        "oran; hepsinde aynı anlama gelir. Mutlak bir ±X her parametre için "
        "ayrı gerekçe isterdi"),
    "kalibrasyon/evre_metrikleri_kapilari.py::TOHUMLAR": (
        "SINANMAMIS",
        "3 tohum — evre metriklerinin doğrulama kapıları için. Kapı verdikti "
        "KOL ORTALAMASINDA veriliyor, ama 3 tohum az; kapılar bir gün "
        "sınırda kalırsa ilk artırılacak sayı budur"),
    "kalibrasyon/iki_cift.py::TOHUMLAR": (
        "TURETILMIS",
        "3 tohum — iki çift probu DETERMİNİSTİK bir soru soruyor ('iki uzak "
        "iletim aynı anda başarılı mı') ve ölçülen oranlar tohumdan bağımsız "
        "çıktı (1,000 · 1,000 · 1,000). Daha fazla tohum bilgi eklemiyor"),

    # ------------------------------------------------- Li replikasyonu
    "kalibrasyon/li_replikasyonu.py::BAND": (
        "TURETILMIS",
        "(0,10; 0,20) — ÖN-KAYITLI kabul bandı, `09` §04'te ölçümden ÖNCE "
        "ilan edildi. Li'nin 1/7 = 0,143'ü etrafında ±%40; iki farklı 802.11 "
        "uygulaması arasında beklenen ayrımın mertebesi. Sonradan "
        "GENİŞLETİLMEYECEK"),
    "kalibrasyon/li_replikasyonu.py::IDEAL_MAC_TAVANI": (
        "KAYNAK",
        "0,25 — Li vd. §3.2, ideal MAC'te zincirin uçtan uca verimi tek "
        "atlamanın 1/4'ü. `02` A5b'de doğrulanmış"),
    "kalibrasyon/li_replikasyonu.py::TOHUMLAR": (
        "TURETILMIS",
        "5 tohum — zincir TEMİZ kanalda koşuyor (gölgeleme ve sönümleme "
        "kapalı), dolayısıyla tohumlar arası varyans yalnız trafik fazından "
        "geliyor ve küçük. Ölçüldü: 2 SE değerleri 0,19–4,68 pkt/s"),

    # ------------------------------------------------- yeniden kullanım
    "kalibrasyon/yeniden_kullanim.py::BAG_M": (
        "TURETILMIS",
        "280 m = `Konfig.iletim_menzili_m`, yani GÜÇ ÇAPASI. 'Bir atlama = "
        "bir iletim menzili' yapı gereği doğru olsun diye. ⚠️ Elle yazılmış "
        "bir kopya; `Konfig`ten okunmalı"),
    "kalibrasyon/yeniden_kullanim.py::AYRIMLAR": (
        "TEDAVI", "çiftler arası mesafe TARAMASININ ekseni; yeniden kullanım "
                  "mesafesi bu taramanın SONUCU"),
    "kalibrasyon/yeniden_kullanim.py::ALFALAR": (
        "TEDAVI",
        "(2,0; 3,0; 4,0) — yol kaybı üsteli taramasının ekseni. 🔒 α = 3 ve 4 "
        "bu projede KULLANILMIYOR; tarama bir öneri değil, girişim/iletim "
        "oranı türetmesinin SINAVI"),
    "kalibrasyon/yeniden_kullanim.py::ESIK": (
        "TURETILMIS",
        "1,5 — iki çift tam paralelse toplam verim 2,0, tamamen "
        "serileştirilmişse 1,0. Orta nokta; ölçülen değerler zaten 1,05 ya da "
        "2,00 çıkıyor, yani eşik hiçbir kararı belirlemiyor"),
    "kalibrasyon/yeniden_kullanim.py::SACILMA_SINIRI": (
        "TURETILMIS",
        "1,35 — çarpanın α'dan bağımsız sayılması için izin verilen saçılma. "
        "Izgara 1 atlama çözünürlüklü olduğu için 3 atlamalık bir ölçümde tek "
        "adımlık belirsizlik zaten ±%33; sınır ondan dar seçilemez. "
        "Ölçülen saçılma 1,08"),

    # ------------------------------------------------- bağ kümesi (9 Eylül)
    "kalibrasyon/bag_kumesi.py::ESIKLER": (
        "TEDAVI",
        "(0,50…0,99) — bağ eşiği TARAMASININ ekseni. Bir değer değil, aranan "
        "aralık; `ATLAMA_ESIGI`nin platosu bu taramanın SONUCU. Alt sınır "
        "0,50: altında `ETX_TAVANI` kelepçesi geri türetmeyi bozar"),
    "kalibrasyon/bag_kumesi.py::K_ADAYLARI": (
        "TEDAVI",
        "(1…32) — sönümleme örnek sayısı taramasının ekseni; ikişer katlar, "
        "`duyarlilik.py::CARPANLAR` ile aynı 'ölçekten bağımsız tek çarpan' "
        "gerekçesi"),
    "kalibrasyon/bag_kumesi.py::KAYDIRMALAR": (
        "TURETILMIS",
        "(0…35 ms, 7 ms adımlı) — örnekleme fazı kaydırmaları. İki kısıt "
        "birlikte belirledi: tutarlılık süresinden (~1,7 ms) BÜYÜK olmalı ki "
        "çekimler bağımsız olsun (küçük olsaydı ölçülen saçılma kestiricinin "
        "gürültüsünü OLDUĞUNDAN KÜÇÜK gösterirdi), ve dünyayı oynatmayacak "
        "kadar küçük olmalı (35 ms'de düğüm 2,6 cm gider; gölgeleme hücresi "
        "50 m). G-b kapısı ikinci kısıtı her koşumda sınıyor"),
    "kalibrasyon/bag_kumesi.py::DERECE_TOLERANSI": (
        "TURETILMIS",
        "0,3 — `gorev_kalibrasyonu.py::DERECE_TOLERANSI`nin AYNISI, elle "
        "yazılmış bir kopya değil bilinçli bir atıf: bölüm C grafik "
        "düzeyindeki saçılmayı o kararın kendi toleransıyla okur. ⚠️ KARAR "
        "BU BÖLÜMDEN ÇIKMAZ — K'nin beslediği asıl karar PDR'dir ve o "
        "bölüm E'de `COZUNURLUK_R` ile okunur"),
    "kalibrasyon/bag_kumesi.py::COZUNURLUK_R": (
        "OLCULMUS",
        "0,036 — deneyin çözünürlüğü. Üretici: `python kalibrasyon/"
        "cozunurluk.py` (30 tohum, R = 2·SD/√30). Burada elle yazılmış bir "
        "KOPYADIR; kaynağı `cozunurluk.py`dir ve ikisi ayrışırsa kaynak "
        "geçerlidir"),
    "kalibrasyon/bag_kumesi.py::GUCLER": (
        "TEDAVI",
        "(−30…−6 dBm) — `karistirici_gucu.tarama`nın varsayılan ekseniyle "
        "AYNI. Aynı olması ZORUNLU: eşik taraması, güç seçimini yeniden "
        "koşturuyor ve iki tarama farklı ızgarada olsaydı sonuçlar "
        "karşılaştırılamazdı"),

    # ------------------------------------------ veri onayı semantiği (10 Eylül)
    "kalibrasyon/onay_semantigi.py::COZUNURLUK_R": (
        "OLCULMUS",
        "0,0318 — 40 tohumluk çözünürlük (atlama kâhini PDR'si, en gevşek "
        "çıktı). Üretici: `python -u kalibrasyon/cozunurluk.py --tohum 40` "
        "(10 Eylül 2026, K-113). Onay semantiği ölçümünün karar eşiği; "
        "burada elle yazılmış bir KOPYADIR, kaynağı `cozunurluk.py`dir ve "
        "ikisi ayrışırsa kaynak geçerlidir"),
}


# ===========================================================================
# DENETİM
# ===========================================================================
def eksik_alanlar(alan_adlari) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """`(kökeni yazılmamış alanlar, artık var olmayan köken kayıtları)`."""
    adlar = set(alan_adlari)
    kayitli = set(KOKENLER)
    return (tuple(sorted(adlar - kayitli)), tuple(sorted(kayitli - adlar)))


def duyarlilik_borcu() -> tuple[str, ...]:
    """Faz 1 duyarlılık denetiminin HÂLÂ oynatmadığı kol tanımı sabitleri.

    🔒 Bu, `SINANMAMIS`in kardeş sayacıdır. `KOL_TANIMI` kovası hiç boşalmaz
    (bir kolun tanımı silinmez), ama borç bu kümede durur ve BOŞALIR.
    Ön-kayıt mührü ikisinin de sıfır olmasını ister.
    """
    return tuple(sorted(DUYARLILIK_BEKLEYEN))


def kova_sayimi() -> dict[str, int]:
    """Kova başına parametre sayısı — sonuç satırına yazılır."""
    sayim = {k: 0 for k in KOVALAR}
    for kova, _ in KOKENLER.values():
        sayim[kova] += 1
    for kova, _ in MODUL_KOKENLERI.values():
        sayim[kova] += 1
    return sayim
