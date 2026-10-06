"""
Fiziksel kopma — `kopma_fiziksel` sayacı ve algılama duyarlılığının paydası.

    algilama_duyarliligi = kopma_algilanan / kopma_fiziksel

Hiç beyan etmeyen bir protokolün kopma sayacı 0 çıkar ve "hiç kopma
yaşamadı" gibi görünür — oysa yalnız susmuştur; bu oran onu ayırır.

🔒 TANIM — sayaç kaydının kendi cümlesi
=======================================
Bir bağ, **yavaş SINR**'i eşiğin altına indiğinde kopar:

    yavaş SINR = yol kaybı + anten deseni + gölgeleme
    HIZLI SÖNÜMLEME HARİÇ · GİRİŞİM HARİÇ · KARIŞTIRICI HARİÇ

Hızlı sönümleme saniyede yüzlerce kez eşiği geçer. Karıştırıcı da dışarıda:
darbeli ve taramalı karıştırıcının her salınımı 1 s'lik ızgarada bir kopma
sayılır, payda şişer ve her protokol kör görünürdü. Bedeli beyan edilir:
`algilama_duyarliligi` bir TOPOLOJİ ÇALKANTISI algılama ölçüsüdür, karıştırma
algılama ölçüsü değil — karıştırmanın etkisi evre metrikleriyle ölçülür.

🔒 IZGARA — `olcum/evre.py::IZGARA_ADIMI_S` ile AYNI (1 s, AODV
`HELLO_INTERVAL`): hiçbir taban protokol komşu bilgisini bundan hızlı
tazeleyemez. Izgaradan kısa süren kopma görünmez; bu sayının özelliğidir.

🔒 SON İŞLEMDİR — konum ve gölgeleme zamanın saf fonksiyonlarıdır, sayım koşu
bittikten sonra yapılır ve sıcak yola dokunmaz. İlk ızgara noktası durumu
kurar, kopma saymaz (`[baş + ızgara, bitiş)`).

🔒 STATİK KOLDA SONUÇ TAM OLARAK SIFIRDIR — bir kapı: değişebilecek hiçbir
şey yoktur.

⚠️ AĞ BÖLÜNMESİ BURADA ÖLÇÜLMEZ: yavaş SINR grafiği, erişilebilir grafikten
(kâhin grafiği) çok seyrektir ve hep bölünmüş görünürdü. Bölünme
kalibrasyon tarafında kâhin grafiğinde ölçülür (`kalibrasyon/dugum_sayisi.py
--bolunme`). Aynı sebeple `kopma_fiziksel` "ağın bağları koptu" diye
okunmamalıdır: seyrek yavaş SINR grafiğinin geçişlerini sayar.
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
