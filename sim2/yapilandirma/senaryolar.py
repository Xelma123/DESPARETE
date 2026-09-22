"""
Deney kolları — mobilite ekseni × karıştırıcı ekseni.

🔒 MOBİLİTE BİR EKSENDİR, BİR AYAR DEĞİL (onaylı karar 8)
=========================================================

🔴 BURADAKİ ESKİ TABLO ÇÜRÜDÜ — 9 Eylül 2026. İki kere.
========================================================
Burada şu tablo duruyordu ve üç ayrı kararın gerekçesiydi:

    kol          tam bağlı zaman oranı   en kötü tohum
    statik-yok           %73,3               %0,0
    mobil-yok            %82,4              %71,5      ← kolun ESKİ adı

**Birinci çürüme — üreticisi koşmuyordu.** `adim3_kapanis.py` kolun eski
adını (`mobil-yok`) kullanıyordu; üçüncü kol eklenirken (4 Eylül) kollar
yeniden adlandırıldı ve betik güncellenmedi. O tarihten beri `ValueError`
ile patlıyordu, yani bu sayılar **yeniden üretilemiyordu**. Tablodaki eski
kol adı, sayıların da o tarihten kaldığının kanıtıdır: terk edilmiş bir
çalışma noktası (alan 1000 m · yol kaybı üsteli 3 · SINR eşiği 10 dB).

**İkinci çürüme — ölçtüğü grafik zaten geçersizdi.** Bu sayılar
`Topoloji.anlik`ten, yani 280 m yarıçaplı SERT DİSKTEN geliyor. K-096 tam
olarak o diskin veri yolunda hiçbir yeri kapamadığını ölçtü.

🔒 BUGÜN ÖLÇÜLEN — iki grafik, iki ayrı cevap:
    Üretici (teşhis diski): `python kalibrasyon/adim3_kapanis.py`
        statik-yok    tam bağlı zaman %0,0 · derece 2,53
        bagimsiz-yok  tam bağlı zaman %0,0 · derece 2,49
        500 tohumda bağlı yerleşim oranı: **%0,0**
    Üretici (kanal grafiği): `python kalibrasyon/denetim_ornekleme.py d`
        statik-yok  30 tohum × 9 an → **270/270 TEK PARÇA**,
        yalnız düğüm **0**, derece **8,76**

🔴 YANİ ESKİ TABLONUN İKİ SONUCUNDAN BİRİ DÜŞTÜ:
  · *"Statik kolda tohumların %26,7'si tamamen kopuk, bu yüzden U1 'bağlı'
    bir tohum süzgeci kullanır"* — **DÜŞTÜ.** Veri taşıyan grafikte hiçbir
    tohum kopuk değil; süzgeç gereksiz. ⚠️ Ve süzgeç zaten **hiçbir yerde
    UYGULANMAMIŞTI** — beş dosyada beyan ediliyordu, kodda karşılığı yoktu.
    Çalışma noktası (1800 m) zaten *"kopukluğun sıfır kaldığı en büyük alan"*
    ölçütüyle seçilmişti; kopukluğun sıfır olması o seçimin SONUCUDUR.
  · *"Hareketli kolda PDR ≈ 1 imkânsızdır"* — **AYAKTA**, ama bu tabloyla
    değil. Dayanağı bugün ölçülmüş bir sayı: kâhin tavanı `bagimsiz-yok`
    kolunda 0,917 ve 0,831 (üretici: `python kalibrasyon/pdr_tavani.py 1`).
    Sonuç aynı, gerekçe artık canlı bir ölçüme dayanıyor.

🔒 ÜÇ KOLUN VAR OLUŞ SEBEBİ BU TABLODAN GELMİYOR ve etkilenmiyor: kollar,
*"mobilite modeli değişince protokol sıralaması değişiyor mu"* sorusunu bir
VARSAYIM olmaktan çıkarıp ölçülen bir sonuca çevirmek için var (aşağıya bak).

🔴 KARIŞTIRICI GÜÇLERİ HENÜZ YOK — ve boş olmaları kasıtlı
===========================================================
Eski depoda `S2 = +2 dBm` çalışma noktası **2B, gölgelemesiz, sönümlemesiz**
bir dünyada ve 1 Mb/s / 1 MHz bantta seçilmişti. Yeni fizikte:

    gürültü tabanı  1 MHz −107,98 dBm  →  2 MHz −104,96 dBm
    düğüm Pt (menzilden TÜRETİLİR)     →  +15,49 dBm  →  +18,50 dBm

Yani eski güç, düğüme göre 3 dB daha zayıf bir karıştırıcıya karşılık gelir.
Aynı göreli farkı korumak +5,01 dBm ister — ama bu da **cevap değil**, çünkü
gölgeleme ve sönümleme teslim eğrisini ayrıca kaydırır.
Üretici: `python kalibrasyon/adim3_oncesi.py`

🔒 SEÇİM ÖLÇÜTÜ — TARAMA KOŞULMADAN ÖNCE İLAN EDİLDİ (4 Eylül 2026)
===================================================================
    Karıştırıcı gücü, uçtan uca teslim oranını taramanın DİNAMİK
    ARALIĞININ ORTASINA en yakın getiren güçtür; kısıt: ulaşılabilirlik
    (MAC sonrası, en az bir yönde bağ kurulabilen çift oranı) ≥ %90.

Neden orta nokta: metrik orada her iki yönde de en çok başlığa sahiptir.
Tabanda ve tavanda protokol farkları sıkışır ve tarama *"hiçbir şey fark
etmiyor"* der — oysa ölçülemeyen şey farkın yokluğu değil, başlığın yokluğudur.

⚠️ Eski depoda aynı ölçüt **taramayı gördükten sonra** yazılmıştı ve bu
kayda geçmişti (*"ön-kayıtlı bir seçim değil, betimleyici gerekçe"*). Bu kez
ölçüt taramadan önce, karıştırıcı kodu yazılmadan önce burada.
"""

from __future__ import annotations

from dataclasses import dataclass

from sim2.cekirdek.degismezler import dogrula

__all__ = [
    "MOBILITE_KOLLARI", "MOBILITE_THETA", "TRAFIK_DESENLERI",
    "MOBILITE_BOLUNME", "BOLUNME_OLCULEN_ARALIK", "bolunme_payi",
    "TEHDIT_SENARYOLARI", "KARISTIRICI_SINIFLARI",
    "SenaryoTanimi",
    "SENARYOLAR", "UYGULANMAMIS_KARISTIRICI", "KARISTIRICI_GUCU_DBM",
    "senaryo_adi",
]

# --------------------------------------------------------------------- eksen 1
# 🔒 ÜÇ KOL — öğrenci kararı, 4 Eylül 2026. Önce iki koldu ({statik, mobil});
# üçüncüsü bir ÖLÇÜMÜN sonucu olarak eklendi.
#
# ÖLÇÜLEN: bağımsız Gauss-Markov'da komşular arası bağıl hız 26,0 m/s ve
# çok atlamalı bir rotanın ömrü **2,4 saniye**. Protokolün rota keşfi ~0,1 s
# sürdüğüne göre ağ sürekli yeniden keşif rejiminde.
# Üretici: `python kalibrasyon/mobilite_gercekcilik.py`
#
# 🔒 GÖREV KOLUNUN ÖLÇÜLEN KAZANCI — abartılmadan:
#     büyüklük            bağımsız    görev    oran
#     ortalama derece         7,45     7,55   1,01×   (ölçütle EŞİTLENDİ)
#     tam bağlı zaman        %82,0    %83,8   1,02×   (ölçütle eşitlendi)
#     bağıl hız          26,0 m/s  16,6 m/s   0,66×   ← SONUÇ
#     bağ ömrü             15,1 s    11,8 s   0,78×   ← SONUÇ
#     rota ömrü             2,4 s     3,0 s   1,24×   ← SONUÇ
#
# ⚠️ Kazanç ILIMLI, ve sebebi ölçütün kendisi: dereceyi eşitleme kısıtı,
# müfrezeleri GEVŞEK olmaya zorluyor (seçilen yarıçap 250 m ≈ telsiz
# menzili). Bu yoğunlukta "sıkı koordinasyon" ile "bağımsız kolla aynı
# derece" aynı anda sağlanamıyor — sıkı gruplar yerel dereceyi 10–17'ye
# çıkarıyor (tarama tablosu). Yani ölçülen şey *koordinasyonun tavanı*
# değil, *bu çalışma noktasında koordinasyonun sığabildiği kadarı*.
#
# 🔴 İLK ÖLÇÜM YANLIŞTI ve düzeltildi. Rota ömrü ölçümü sabit kaynak/hedef
# çiftleri kullanıyordu ((0,20), (1,21)...) ve grup ataması `i % grup_sayisi`
# olduğu için bu çiftler AYNI MÜFREZEDE kalıyordu: ölçülen şey çok atlamalı
# bir rota değil, grup içi bir yoldu ve kazancı **10,7 kat** gösteriyordu.
# Gerçek kazanç 1,24 kat. Ölçüm artık trafik modeliyle aynı mantıkta —
# rastgele kaynak/hedef çiftleri — çalışıyor.
#
# 🔴 Bu, modeli "yanlış" yapmaz: bağımsız Gauss-Markov, FANET yönlendirme
# literatürünün fiilen standart modelidir. Ama tasarım uzayının BİR UÇ
# KÖŞESİNDE durur (mümkün olan en yüksek bağıl hız) ve tek başına
# kullanıldığında bu köşe sessizce seçilmiş olur.
#
# Üç kolla birlikte *"mobilite modeli değişince protokol sıralaması değişiyor
# mu"* sorusu bir VARSAYIM olmaktan çıkıp ÖLÇÜLEN BİR SONUÇ olur. Değişmiyorsa
# sonuçlar sağlamdır; değişiyorsa bu başlı başına bir bulgudur. İki hâlde de
# kazanç var — tek kolla ikisi de bilinemez.
#
# 🔒 DÖRDÜNCÜ KOL `formasyon` — öğrenci onayı, 11 Eylül 2026 (`v2/07` §18 Y6).
# Her düğüm yerleşimdeki noktasını İSTASYON olarak tutar: t = 0 statik kolla
# aynıdır, yoğunluk eşit olduğu için derece eşitlemesi gerekmez ve yeni serbest
# sayı yoktur. İstasyon tutma fiziği görev koluyla ortaktır
# (`dunya/mobilite.py`).
MOBILITE_KOLLARI: tuple[str, ...] = ("statik", "bagimsiz", "gorev", "formasyon")

# 🔒 Θ — MOBİLİTE KOLU BAŞINA VE İKİ PAYDAYLA (`v2/07` §03.3 · §18 Y7).
# Üretici: `python -u kalibrasyon/theta_kollari.py` (14 Eylül 2026;
# 6 tohum × 350 s × 40 çift, bağ tanımı yavaş SINR ≥ eşik).
# Değerler: (Θ_OLSR, Θ_AODV, hiç KOPMAYAN çift oranı).
#
#   kol          τ_KM    Θ_OLSR   Θ_AODV   kopmayan
#   statik         —        —        —       %100    hiçbir rota kopmuyor
#   bagimsiz     48,8 s    3,25    16,27     %40,4
#   gorev        59,8 s    3,99    19,93     %27,5
#   formasyon    34,6 s    2,31    11,53     %92,1   🔴 kapının ALTINDA
#
# 🔒 Θ_AODV = Θ_OLSR × 5: paydalar OLSR `TOP_HOLD_TIME` 15 s ve AODV
# `ACTIVE_ROUTE_TIMEOUT` 3 s (RFC 3626 · RFC 3561). Bir kol OLSR'ın
# zarfının dışında kalırken AODV'ninkinin içinde olabilir; §03.3 ikisinin
# birden raporlanmasını bu yüzden istiyor.
#
# 🔴 FORMASYONUN SAYISI OLDUĞU GİBİ OKUNAMAZ — ve bunu ÜÇÜNCÜ SAYI söyler.
# Kestirici yalnız GÖZLENEN ömürleri kullanır: her çiftin ilk ömrü atılır
# (yaşı bilinmez, soldan kesme) ve koşu sonunda yaşayan rota sansürlüdür.
# Formasyonda çiftlerin %92,1'i hiç kopmuyor, yani ölçüme yalnız eşiğin
# kıyısında titreyen %7,9 giriyor. 2,31 bu yüzden kolun tipik rota ömrü
# DEĞİL, bir ALT SINIRDIR: kapının altında görünmesi mobilitenin
# çalkantısından değil, örneklemin kim olduğundan geliyor. Kopmayan oranı
# her sonuç satırının kapsam bölümüne de yazılır ki sayı yalnız
# dolaşmasın.
#
# ⚠️ Statik kolda Θ TANIMSIZ (`None`): hiçbir rota kopmadığı için ölçülebilir
# ömür yok. Bu bir eksiklik değil, kolun tanımı.
MOBILITE_THETA: dict[str, tuple[float | None, float | None, float]] = {
    "statik": (None, None, 1.000),
    "bagimsiz": (3.25, 16.27, 0.404),
    "gorev": (3.99, 19.93, 0.275),
    "formasyon": (2.31, 11.53, 0.921),
}

# ==========================================================================
# 🔴 AĞ BÖLÜNMESİ — ANA DENEY TOHUMLARINDA ÖLÇÜLDÜ (B6 · `04` K-132)
# ==========================================================================
# C1 (K-125) çalışma noktasının kopukluk uçurumunun KENARINDA olduğunu
# ölçmüştü: 120 tohumla kopukluk olasılığı %0,8. 40 tohumluk ana deneyde en az
# bir kopuk tohum görme olasılığı ~%27. Böyle bir tohumda teslim oranı
# **protokolden bağımsız** bir sebeple çöker ve betimleyici tablolar, güven
# aralıkları ve özellikle evre metrikleri anlamsızlaşır — ama satır bunu
# SÖYLEMİYORDU.
#
# 🔴 VE İLK ÖLÇÜM YANILTICIYDI. t = 0'da, statik kolda bakıldı: **0/40**,
# yani "sorun yok" görünüyordu. Pencere boyunca ve HAREKETLİ kollarda
# bakılınca tablo değişti — bölünme hareketten doğuyor ve tek bir ana
# bakmak onu göremiyor:
#
#     statik     0/40   (kontrol kolu — burada sıfır çıkmasaydı ÖLÇÜM bozuktu)
#     bagimsiz   6/40
#     gorev      7/40
#     formasyon  2/40   🔴 tohum 2011 dokuz anın YEDİSİNDE bölünmüş
#
# Bölünmelerin neredeyse hepsinde 39 ulaşılamaz çift var: TEK bir düğüm
# menzil dışına düşüyor. `gorev`de iki tohumda 76 çift = iki düğüm.
#
# 🔒 BAĞ TANIMI KÂHİN GRAFİĞİDİR — çalışma noktasının SEÇİLDİĞİ tanım (C1 ve
# `calisma_noktasi.py`), yani bu sayı o kararla doğrudan kıyaslanabilir.
# ⚠️ Ölçüm `-yok` senaryolarında yapıldı: KARIŞTIRICI bu tanımın DIŞINDA.
# Ölçülen şey TOPOLOJİNİN bölünmesidir; karıştırmanın açtığı geçici kopukluk
# evre metrikleriyle ölçülür.
# ⚠️ Dokuz an örneklenir, süreklilik değil: sayı bölünmenin OLDUĞUNU söyler,
# tam süresini değil. Bir alt sınır olarak okunur.
#
# 🔒 Bölünmüş bir tohum ATILMAZ — atmak seçilim yanlılığı olurdu. Satır onu
# SÖYLER (`kapsam.bolunme_payi`) ve analiz katmanı orada ayrıca okur.
#
# Üretici: `python -u kalibrasyon/dugum_sayisi.py --bolunme` (16 Eylül 2026)
# ⚠️ ARALIK, `range` DEĞİL — ve bunu mimari denetimi öğretti (16 Eylül 2026).
# İlk yazımda `range(2000, 2040)` idi; D12'nin tarayıcısı yalnız SAYISAL
# sabitleri ve SAYI TABLOLARINI görüyor, bir `range(...)` ÇAĞRISINI değil.
# Sonuç: köken kaydı yazılmış ama sabit görülmemiş — yani ÖLÜ KAYIT, ve
# denetimin kendi cümlesiyle *"defterin güvenilirliğini bitirir"*. Sayı
# demeti hem tarayıcıya görünür hem aynı şeyi söyler.
BOLUNME_OLCULEN_ARALIK: tuple[int, int] = (2000, 2040)
# Yalnız SIFIRDAN BÜYÜK kayıtlar tutulur; ölçülen ama bölünmeyen tohum
# `0.0` okur, ÖLÇÜLMEYEN tohum `None` — *"bölünme yok"* ile *"bakılmadı"*
# aynı şey değildir (`None ≠ 0`).
MOBILITE_BOLUNME: dict[str, dict[int, float]] = {
    "statik": {},
    "bagimsiz": {
        2007: 0.1111,
        2011: 0.1111,
        2021: 0.2222,
        2023: 0.1111,
        2028: 0.3333,
        2035: 0.2222,
    },
    "gorev": {
        2001: 0.1111,
        2007: 0.1111,
        2009: 0.3333,
        2019: 0.2222,
        2020: 0.3333,
        2032: 0.2222,
        2034: 0.4444,
    },
    "formasyon": {
        2006: 0.1111,
        2011: 0.7778,
    },
}


def bolunme_payi(mobilite_kolu: str, tohum: int) -> float | None:
    """Bu (kol, tohum) çiftinde ağın bölünmüş olduğu an payı.

    `None` = ÖLÇÜLMEDİ (tohum ana deney kümesinde değil). `0.0` = ölçüldü ve
    bölünme görülmedi. İkisi ayrı şeydir ve karıştırılırsa kalibrasyon
    tohumları sessizce "temiz" diye okunur.
    """
    bas, son = BOLUNME_OLCULEN_ARALIK
    if not bas <= tohum < son:
        return None
    return MOBILITE_BOLUNME.get(mobilite_kolu, {}).get(tohum, 0.0)

# 🔒 TRAFİK DESENLERİ — `v2/07` §06.2 · §18 Y4. Mobilite × karıştırıcıdan ayrı
# bir TEDAVİ eksenidir ve senaryo adına girmez: girseydi senaryo matrisi
# ikiye katlanır, bugünkü adlar bayatlardı. `esler_arasi` varsayılandır ve
# bugünkü satırları birebir üretir.
TRAFIK_DESENLERI: tuple[str, ...] = ("esler_arasi", "yere_toplama")

# 🔒 TEHDİT SENARYOLARI — `v2/07` §05.3.1 · §18 Y5 (öğrenci kararları 11 Eylül
# 2026, `v2/04` K-119). Karıştırıcı KÜMESİNİN biçimi; sinyal sınıfı senaryo
# adından gelir. Trafik deseni gibi ayrı bir TEDAVİ eksenidir ve senaryo adına
# girmez. İlk değer varsayılandır ve bugünkü tek merkez karıştırıcıyı birebir
# kurar. Tanımlar katman yönü gereği `kanal/tehdit.py`de.
TEHDIT_SENARYOLARI: tuple[str, ...] = (
    "tekli_merkez", "cephe_hatti", "derin_sizma", "hedef_koruma", "hava_eslik")

# 🔒 GÖREV KOLUNUN PARAMETRE SEÇİM ÖLÇÜTÜ — TARAMA KOŞULMADAN ÖNCE İLAN EDİLDİ
# ===========================================================================
#     GEÇERLİLİK KOŞULU: müfreze başına en az 4 üye (40 düğüm → grup sayısı
#     ≤ 10). Daha küçük bir "müfreze" tactical bir alt birim değildir ve kol
#     sessizce bağımsız kola dönerdi.
#
#     SEÇİM: bu koşulu sağlayan (grup sayısı, grup yarıçapı) adayları
#     arasından, ORTALAMA DERECEYİ bağımsız kolunkiyle eşitleyen
#     (|Δderece| ≤ 0,3) ve bu kısıt altında TAM BAĞLI ZAMAN ORANI bağımsız
#     kola en yakın olan çift.
#
# ⚠️ GEÇERLİLİK KOŞULU SONRADAN EKLENDİ — 4 Eylül 2026, tarama koşulmadan
# önce ama tek bir deneme noktası görüldükten sonra (G=8, ρ=100 → derece
# 10,75). Sebep: ilk hâliyle ölçüt YOZ bir çözümü kabul ediyordu — çok
# sayıda minik "grup" + büyük yarıçap, dereceyi de bağlantılılığı da
# tutturur ama fiilen bağımsız hareketten ayırt edilemez. Yani ölçüt, kolun
# VAR OLUŞ SEBEBİNİ elemeye açıktı.
#
# 🔒 Bu bir eşik gevşetmesi DEĞİLDİR: eklenen şey bir başarı eşiği değil,
# "müfreze nedir" tanımıdır ve sonucun yönünü seçmez. Kayda geçirilmesinin
# sebebi, taramadan önce yazılmış olmasının tek başına yetmemesi — ne zaman
# ve neyi gördükten sonra yazıldığı da yazılmalı.
#
# 🔴 Bağıl hız ve rota ömrü ölçüt DEĞİL, SONUÇTUR. Onlara göre ayarlamak,
# kolun var oluş sebebi olan sayıyı seçmek — yani cevabı seçmek — olurdu.
#
# Derece kısıtı neden ZORUNLU: üç kol aynı t=0 yerleşimini paylaşamaz, çünkü
# "formasyonda" ile "düzgün rastgele" farklı dağılımlardır. Kolları
# karşılaştırılabilir yapan şey yerleşimin aynılığı değil, YOĞUNLUĞUN
# eşitliğidir. Eşitlenmezse ölçülen fark koordinasyonun değil, ağın
# seyrekliğinin farkı olur — 3B'ye geçerken yaşanan tuzağın aynısı.

# --------------------------------------------------------------------- eksen 2
# Onaylı karar 5: beş sınıf + darbeli. `darbeli` ayrı bir eksen DEĞİL, sürekli
# karıştırıcının bir kipidir — ortalama gücü sabit karşılığına eşitlenir ve
# sorulan soru *"aynı ortalama güçte darbeli olmak fark eder mi"*dır.
KARISTIRICI_SINIFLARI: tuple[str, ...] = (
    "yok",             # taban — karıştırma yok
    "surekli",         # sabit güçte kesintisiz gürültü
    "surekli_darbeli", # aynı ORTALAMA güç, darbeli
    "reaktif",         # 🔴 durum tutar: iletim-başladı olayına tepki verir
    "aldatici",        # geçerli görünümlü önbelge — CSMA'ya GÖRÜNÜR
    "taramali",        # konaklar arasında gezinir
)

# 🔴 Adım 4 gelene kadar yalnız `yok` uygulanmıştır. Uygulanmamış bir sınıfla
# Konfig kurmak `NotImplementedError` fırlatır — sessizce etkisiz kalmak
# yerine gürültülü biçimde durur. Sebebi eski depoda ölçüldü: bildirilmiş ama
# uygulanmamış bir bayrak, sonuç satırına etiket olarak yazılıyor ve satır
# *"karıştırıcı kolu"* diye işaretlenmiş oluyordu. Etiket otomatik taşınıyor
# ve yalan söylüyordu.
# 🟢 4 Eylül 2026: BEŞ SINIFIN BEŞİ DE UYGULANDI (`kanal/karistirici.py`),
# liste boşaldı. Kapı kalkmadı, YER DEĞİŞTİRDİ: artık "uygulanmamış sınıf"
# değil, "ölçülmemiş güç" engelliyor — `KARISTIRICI_GUCU_DBM` boş olduğu için
# bir karıştırıcı kolunu koşmak `karistirici_guc_override_dbm` vermeyi
# zorunlu kılıyor ve bunu `kanal/karistirici.py` denetliyor.
UYGULANMAMIS_KARISTIRICI: frozenset[str] = frozenset()

# 🟢 ÖLÇÜLDÜ VE DOLDURULDU — 8 Eylül 2026.
# Üretici: `PYTHONIOENCODING=utf-8 python kalibrasyon/karistirici_gucu.py tarama`
#
# 🔒 TEK SAYI, BEŞ SINIF. Çalışma noktası bir kez seçilir ve REFERANS SINIFTA
# (`surekli`) seçilir — zaman yapısı olmayan tek sınıf odur, dolayısıyla ρ
# orada örtüşmesiz okunur. Ölçüt: 30 tohumun hiçbirinde birden fazla çok üyeli
# bileşen yokken ρ en büyük. Seçilen: **−15,0 dBm · ρ = 0,258**.
#
# 🔴 HER SINIFA AYRI GÜÇ VERİLMEDİ, ÇÜNKÜ BU DÖNGÜSEL OLURDU. Sınıfları
# "aynı ρ'yu üretsinler" diye ayarlamak, ρ bağımlı değişken olduğu için
# deneyin aradığı mekanizma farkını kalibrasyonla silmek demektir. Eşitleme
# karıştırıcının HARCADIĞI şey üzerinden yapılır: yayılan ortalama güç.
#
# 🔒 Buradaki sayı TEPE değil TABAN gücüdür; `Konfig.karistirici_guc_dbm`
# darbeli sınıfa `tepe_telafisi_db` ekleyerek ORTALAMAYI −15 dBm'de tutar.
#
# ⚠️ `taramali` beyan edilmiş bir istisnadır: tepesi eşit, ortalaması konak
# sayısına bölünür (≈ −19,8 dBm). `karistirici.py`de gerekçeli, ama bir ŞİDDET
# farkıdır — "taramalı zayıf çıktı" bulgusu mekanizmaya tek başına yazılamaz.
KARISTIRICI_GUCU_DBM: dict[str, float | None] = {
    "yok": None,             # 🔒 karıştırıcı yok — `None` burada DOĞRU
    "surekli": -15.0,        # referans: ölçüt bu sınıfta koştu
    "surekli_darbeli": -15.0,  # taban; tepe telafisiyle ortalama eşitlenir
    "reaktif": -15.0,
    "aldatici": -15.0,
    "taramali": -15.0,       # ⚠️ tepe eşit, ortalama 1/3 — beyan edilmiş
}


@dataclass(frozen=True, slots=True)
class SenaryoTanimi:
    """Bir kolun TAM tanımı. Kod düzenlemesiyle üretilen kol kaybolmuş deneydir."""
    ad: str
    mobilite_kolu: str
    karistirici_sinifi: str

    @property
    def hareketli(self) -> bool:
        """🔒 Türetilmiş: `statik` dışındaki her kol hareketlidir."""
        return self.mobilite_kolu != "statik"

    @property
    def darbeli(self) -> bool:
        return self.karistirici_sinifi == "surekli_darbeli"

    @property
    def karistirici_var_mi(self) -> bool:
        return self.karistirici_sinifi != "yok"


def senaryo_adi(mobilite_kolu: str, karistirici_sinifi: str) -> str:
    return f"{mobilite_kolu}-{karistirici_sinifi}"


SENARYOLAR: dict[str, SenaryoTanimi] = {
    senaryo_adi(m, j): SenaryoTanimi(senaryo_adi(m, j), m, j)
    for m in MOBILITE_KOLLARI
    for j in KARISTIRICI_SINIFLARI
}

# Kurulum denetimi — modül yüklenirken bir kez.
dogrula(len(SENARYOLAR) == len(MOBILITE_KOLLARI) * len(KARISTIRICI_SINIFLARI),
        "senaryo çapraz çarpımı eksik")
dogrula(set(KARISTIRICI_GUCU_DBM) == set(KARISTIRICI_SINIFLARI),
        "güç tablosu ile sınıf listesi ayrışmış — ikinci bir doğru kaynağı")
dogrula("statik-yok" in SENARYOLAR, "U1 sanity kolu (statik-yok) yok")
dogrula(set(MOBILITE_THETA) == set(MOBILITE_KOLLARI),
        "Θ tablosu mobilite kollarıyla ayrışmış — bir kol Θ'sız kalırdı")
