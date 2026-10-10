"""
Düğüm kaybı — `v2/15` C1 · K-180.

Bir İHA vurulur ya da arızalanır: TELSİZİ KAPANIR. Gönderemez, alamaz;
kuyruğundaki, rota tamponundaki ve uçuştaki (el değiştirmemiş) veri paketleri
`dugum_kaybi` sebebiyle düşer. Onay beklerken ölürse o deneme `mac_kayip_askida`
kovasına girer (iletim sonucu kapalı kümesi kapanmaya devam eder).

🔒 PROTOKOLE HABER VERİLMEZ — gerçekte de verilmez; komşuları onun
sessizliğinden anlar. Ölen düğümün protokol mantığı zamanlayıcılarıyla
çalışmayı sürdürebilir, ama ürettiği hiçbir şey havaya çıkmaz (kontrol
kuyruğu defterde "kuyrukta" kalır, taşarsa taşma sayılır).

🔴 HAVADAKİ KENDİ ÇERÇEVESİ BİTMEDEN ÖLMEZ (ajan kusuru, K-180'de
yakalandı): ölüm, düğümün son çerçevesinin EN UZAK alıcıya varışına
ertelenir — en çok bir çerçeve süresi + `maks_gecikme_s` (~12 ms). Ertelenmeseydi
alıcı çerçeveyi yine çözer ve paketi, ölümde `dugum_kaybi` ile düşmüş
paketin ölü göndericisinden "devralırdı": değişmez patlar, koşu çöker
(`arsiv/teshis/c_senaryo_eksenleri_2026-09-26/yayin_ortasinda_olum.py`,
gecikme kapalı ve açık). Beyan: yarıda kesilen çerçeve modellenmez; ölüm
anı zaten hash'ten keyfîdir, birkaç ms kayması onu değiştirmez.

⚠️ Beyan: kâhin grafiği ve fiziksel kopma sayımı ölü düğümün bağlarını
geometriden okumaya devam eder (Faz 5'te gerekirse).
"""

from __future__ import annotations

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import hash_cekimi

__all__ = ["olum_anlari", "dugum_oldur"]


def olum_anlari(konfig) -> tuple[float | None, ...]:
    """Düğüm başına ölüm anı (`None` = ölmez). Hangi düğümler ve anları
    hash'ten — protokolden bağımsız, aynı tohumda aynı. Geçit ölmez."""
    n = konfig.dugum_sayisi
    if konfig.kayip_dugum_sayisi == 0:
        return (None,) * n
    adaylar = [i for i in range(n) if i != konfig.gecit]
    dogrula(konfig.kayip_dugum_sayisi <= len(adaylar),
            "ölecek düğüm sayısı aday sayısını aşıyor")
    sira = sorted(adaylar, key=lambda i: hash_cekimi(
        "kanal_karar", konfig.tohum, "kayip", i))
    secilen = set(sira[:konfig.kayip_dugum_sayisi])
    bas, bitis = konfig.kayip_bas_s, konfig.kayip_bitis_s
    return tuple(
        (bas + (bitis - bas) * hash_cekimi("kanal_karar", konfig.tohum,
                                           "kayip_an", i))
        if i in secilen else None for i in range(n))


def dugum_oldur(kosu, n: int) -> None:
    d = kosu.dugumler[n]
    t = kosu.olaylar.simdi
    son = d.son_gonderim_bitis_s + kosu.kur.maks_gecikme_s
    if d.alici.gonderiyor or t < son:
        # Aynı andaki alım olayları önce işlesin diye `t`de de yeniden
        # sıraya girer; o anda gönderim bitmiştir ve ölüm gerçekleşir.
        kosu.olaylar.ekle(max(t, son), dugum_oldur, kosu, n)
        return
    d.mesgul_guncelle(t)
    d.olu = True
    d.olum_s = t
    kosu.kur.paket_defteri.olu_dugumler.add(n)      # KR-E (K-182)
    d.yeni_surum()                      # bekleyen DCF olayları bayatlar
    if d.onay_bekleniyor:
        kosu.kur.sayaclar.artir("mac_kayip_askida")
        d.onay_bekle(False)
    if d.ucustaki is not None:
        if not d.devredildi:
            d.dus("dugum_kaybi", nereden="ucus")
        d.ucustan_indir()
    while not d.kuyruk.bos_mu:
        d.kuyruk.al()
        d.dus("dugum_kaybi", nereden="kuyruk")
    while d.bekleyenler:
        d.bekleyenler.popleft()
        d.dus("dugum_kaybi", nereden="kuyruk")
    d._tampon_son_tarih.clear()
    d._kopya_sonraki.clear()                            # D-23 · K-231
    d.alici.kapat(t)
