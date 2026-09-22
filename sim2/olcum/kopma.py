"""
Fiziksel kopma — `kopma_fiziksel`in AÇIK TAAHHÜDÜ kapanıyor.

🔴 NEDEN BU MODÜL VAR
=====================
`cekirdek/sayaclar.py` `kopma_fiziksel`i *"SINR eşiği altına inen bağ —
GEOMETRİDEN bilinir"* diye tanımlıyor ve üstüne bir türev kuruyor:

    algilama_duyarliligi = kopma_algilanan / kopma_fiziksel

Bu türev, `gozlem/karar.py`nin **Risk 3** dediği şeyin nicel yarısıdır: hiç
beyan etmeyen bir protokolün kopma sayacı 0 çıkar ve tabloda *"hiç kopma
yaşamadı"* gibi görünür — oysa yalnızca susmuştur.

🔴 VE O PAYDA HİÇ SAYILMIYORDU. 9 Eylül 2026'da ölçüldü: canlı bir sonuç
satırında `kopma_fiziksel = 0`, dolayısıyla `algilama_duyarliligi = None`.
`RotaDefteri.fiziksel_kopma()` yalnız TESTLERDEN çağrılıyordu. `dunya/
topoloji.py` bunu bir *"AÇIK TAAHHÜT"* olarak yazmıştı; taahhüt burada
yerine getiriliyor.

🔒 TANIM — sayaç kaydının kendi cümlesi, değiştirilmedi
=======================================================
Bir bağ, **yavaş SINR**'i eşiğin altına indiğinde kopar:

    yavaş SINR = yol kaybı + anten deseni + gölgeleme
    HIZLI SÖNÜMLEME HARİÇ · GİRİŞİM HARİÇ · KARIŞTIRICI HARİÇ

Hızlı sönümleme dışarıda çünkü saniyede yüzlerce kez eşiği geçer; onu kopma
saymak sayacı gürültüye çevirirdi (`kanal/yayilim.py`nin ilan ettiği gerekçe).

🔴 KARIŞTIRICI NEDEN DIŞARIDA — düşünüldü ve ÖLÇÜLEBİLİR bir sebeple elendi
===========================================================================
Karıştırıcıyı paydaya katmak düşünüldü; kâhin grafiği tam olarak bunu yapıyor
(K-104: *"kâhinin tanımı 'her şeyi bilir'dir"*). Burada **elendi** ve sebebi
zamanlamadır: `surekli_darbeli` 2,7 s periyotla %50 görev çevrimi taşıyor,
`taramali` 100 ms konak süresiyle geziniyor. 1 s'lik ızgarada bunların her
salınımı bir "kopma" olarak sayılırdı ve payda şişerdi — sonuçta HER protokol
körmüş gibi görünürdü. Bir metriği, ölçtüğü şeyi hiçbir protokolün
izleyemeyeceği bir hızda tanımlamak, onu tanım gereği başarısız yapar.

⚠️ BUNUN BEYAN EDİLEN BEDELİ: `algilama_duyarliligi` bir **TOPOLOJİ ÇALKANTISI
algılama** ölçüsüdür, bir **karıştırma algılama** ölçüsü DEĞİL. Karıştırmanın
etkisi evre metrikleriyle (şok derinliği · toparlanma) ölçülür; orası onun
yeri. Bu ayrım sonuç bölümünde yazılmalıdır.

🔒 IZGARA — YENİ BİR SAYI GETİRMİYOR
====================================
Örnekleme ızgarası `olcum/evre.py::IZGARA_ADIMI_S` ile AYNI: 1 s, RFC 3561'in
AODV `HELLO_INTERVAL`ı. Gerekçesi de aynı: hiçbir taban çizgisi komşu
bilgisini bundan hızlı tazeleyemez, dolayısıyla daha ince bir ızgara hiçbir
protokolün göremeyeceği bir olayı sayardı. İkinci bir ızgara sabiti tanımlamak
iki sabitin ayrışabilmesi demek olurdu.

⚠️ IZGARADAN KISA SÜREN KOPMA GÖRÜNMEZ ve bu sayının bir ÖZELLİĞİDİR, hatası
değil — `dunya/topoloji.py::bag_olaylari`nın aynı beyanı. Izgara adımı sonuç
satırında `evre_izgara_s` olarak zaten yazılı.

🔒 SON İŞLEMDİR — sıcak yola dokunmaz
=====================================
Konum ve gölgeleme zamanın SAF fonksiyonlarıdır, dolayısıyla bu sayım koşu
bittikten sonra yapılabilir. Ölçüldü: 270 ızgara noktası × 780 çift için
**1,4 s (statik) – 1,7 s (hareketli)**, yani tam uzunluk bir koşunun %1'i.
`olcum/`un "ölçümün maliyeti sonuca karışmamalı" kısıtı korunuyor.

🔒 BAŞLANGIÇ KOŞULU AÇIKÇA SORULDU (`03` kural 14)
==================================================
İlk ızgara noktası **durumu kurar, kopma saymaz**: öncesi yoktur. Yani sayım
`[baş + ızgara, bitiş)` aralığındaki geçişleri kapsar.

🔒 STATİK KOLDA SONUÇ TAM OLARAK SIFIR OLMALIDIR — ve bu bir KAPIDIR.
Konumlar değişmez, gölgeleme konuma bağlıdır, hızlı sönümleme dışarıdadır:
değişebilecek hiçbir şey yoktur. Ölçüldü — statik 0, hareketli 49.
Üretici: `python kalibrasyon/adim9_kapanis.py 1`

🔴 AĞ BÖLÜNMESİ BURAYA KONDU, ÖLÇÜLDÜ ve GERİ ALINDI — 16 Eylül 2026 (B6)
=========================================================================
Denetim B6 satırın *"bu tohumda ağ bölünmüş müydü"* demesini istiyordu ve en
ucuz yer burası görünüyordu: tarama zaten her ızgara noktasında bütün bağ
kümesini kuruyor, bölünmeyi saymak bir BFS ekliyordu.

**Uygulandı, sonra ölçüldü ve GERİ ALINDI.** Bu modülün bağ tanımı YAVAŞ
SINR'dir ve o grafik, ağın gerçekte erişilebilir grafiğinden çok daha
seyrektir. Aynı tohumda, aynı anda ölçüldü (`statik-yok`, t = 200 s):

    yavaş SINR grafiği  :  55 bağ · derece 2,75 · TEK PARÇA DEĞİL
    kâhin grafiği (C1)  : 162 bağ · derece 8,10 · TEK PARÇA

Yani yavaş SINR grafiği **zaten hep bölünmüştür** ve o tanımla bir "bölünme"
alanı her satıra %100 yazardı — ölçtüğü şey ağın bölünmesi değil, tek
denemelik bir eşiğin seyrekliği olurdu. Bir metriğin tanım gereği sabit
çıkması bu projenin kendi tuzak listesinde yazılı (`03` §B3).

🔒 Doğru tanım kâhin grafiğidir (sönümleme dâhil, yeniden denemelerle atlama
başarısı) ve o `kalibrasyon/kahin.py`de yaşıyor — `sim2` onu içe aktaramaz
(katman kuralı). İkinci bir gerçeklemesini buraya yazmak `03` §B5'in *"aynı
kuralı iki yerde yazmak"* hatası olurdu. Ölçüm bu yüzden kalibrasyon
tarafında yapılıyor: `python -u kalibrasyon/dugum_sayisi.py --bolunme`.

⚠️ VE BU, `kopma_fiziksel` HAKKINDA DA BİR ŞEY SÖYLÜYOR: bu sayaç derecesi
2,75 olan bir grafikteki geçişleri sayıyor, derecesi 8,10 olan erişilebilir
grafikteki geçişleri değil. Sayaç kendi tanımına sadıktır ve tanım kaydında
yazılıdır; ama *"ağın bağları koptu"* diye okunmamalıdır.

"""

from __future__ import annotations

from sim2.cekirdek.degismezler import dogrula
from sim2.olcum.evre import IZGARA_ADIMI_S

__all__ = ["fiziksel_kopma_say"]


def fiziksel_kopma_say(*, yayilim, topoloji, dugum_sayisi: int,
                       sinr_esigi_db: float, bas_s: float, bitis_s: float,
                       izgara_s: float = IZGARA_ADIMI_S) -> dict[str, int]:
    """Izgara üzerinde yavaş SINR'i eşiğin altına inen bağ GEÇİŞLERİ.

    🔒 `yayilim` ve `topoloji` ARGÜMAN olarak alınır, içe aktarılmaz: bu
    modül `kanal/`a bağımlı olsaydı `olcum/` katmanı kanalın tamamını görürdü
    ve gözlem sözleşmesinin etrafından dolanan bir yol açılırdı.

    🔒 Bağ SİMETRİKTİR, tek yön yeterlidir: yol kaybı mesafeye, anten kaybı
    yükseliş açısına, gölgeleme `min(i,j), max(i,j)` anahtarına bağlı — üçü de
    yön değiştirince aynı kalıyor (`kanal/yayilim.py`).

    Döner: `{"kopma": …, "acilma": …, "izgara_noktasi": …}`.
    `acilma` bir SONUÇ değil, sağlamadır: sayım gerçekten geçiş sayıyorsa
    hareketli kolda ikisi de sıfırdan büyük olur.
    """
    dogrula(izgara_s > 0.0, "ızgara adımı pozitif olmalı")
    dogrula(bas_s < bitis_s, "ölçüm aralığı ters")

    kopma = acilma = 0
    onceki: set[tuple[int, int]] | None = None
    nokta = 0
    t = bas_s
    while t < bitis_s:
        konum = [topoloji.konum(i, t) for i in range(dugum_sayisi)]
        simdi: set[tuple[int, int]] = set()
        for i in range(dugum_sayisi):
            for j in range(i + 1, dugum_sayisi):
                if yayilim.yavas_sinr_db(i, j, konum[i],
                                         konum[j]) >= sinr_esigi_db:
                    simdi.add((i, j))
        if onceki is not None:
            kopma += len(onceki - simdi)
            acilma += len(simdi - onceki)
        onceki = simdi
        nokta += 1
        t += izgara_s
    return {"kopma": kopma, "acilma": acilma, "izgara_noktasi": nokta}
