"""
KESİN İŞARET TESTİ — `06` Bölüm 9 koşul 1'in ölçütü.

🔴 NEDEN BU DOSYA VAR
=====================
`06` Bölüm 9: *"Dördü birden sağlanmayan hiçbir SONUÇ raporlanmaz:
**1. Sonuç koşu uzunluğundan bağımsız** …"*. Bu koşul 1 Eylül 2026'da ilk
kez ölçüldü ve **kısmen düştü** — ama ölçümün bir EŞİĞİ yoktu: `10` §7b.3
yalnızca *"15/30 🟢"* ve *"8/30 🔴"* yazdı, hangi oranın geçtiğini söyleyen
bir kural yoktu. Eşiksiz bir yargı, sonuca bakıldıktan sonra seçilmiş
demektir (`03` kural 3).

🔒 ÖLÇÜT — KOŞMADAN ÖNCE İLAN EDİLDİ (B0.2, `12` §2.1)
=======================================================
    Bir kol koşul 1'i GEÇER  ⇔  çift yönlü KESİN işaret testi
                                 (binom, p = 0,5, α = 0,05) REDDETMEZSE.

Ve her kol için `03` B2 gereği **dışlanan etki büyüklüğü** yazılır:
medyan farkın dağılımdan bağımsız %95 güven aralığı, hem metriğin
biriminde hem **tohumlar arası std'nin katı** olarak.

⚖️ Bu ölçüt bugünkü yargıları BİREBİR üretir — yani hiçbir şey
gevşetilmiyor: `en_kisa_yol` 15/30 → p = 1,000 (geçer),
`gurultuden_kacan` 8/30 → p ≈ 0,016 (geçmez).

🔴 BU, R-2'NİN İSTATİSTİK KATMANI DEĞİLDİR
===========================================
R-2 (Wilcoxon · Holm–Bonferroni · güç analizi · NaN koruması) **B4'e**
aittir ve `06` Bölüm 7'nin planıdır. Buradaki tek test Faz 0'ın bir
GEÇERLİLİK kontrolüdür:

  · Holm düzeltmesi UYGULANMAZ — bu bir hipotez ailesi değil (FAZ ≠ AİLE).
  · `scipy` KULLANILMAZ — bağımlılık B4'te, gerekçesiyle gelir.
  · Kesin binom + sıra istatistiği: ikisi de stdlib, ikisi de yaklaşımsız.

🔴 NEDEN t DAĞILIMI DEĞİL, SIRA İSTATİSTİĞİ
============================================
Güven aralığı, kullanılan testle AYNI varsayımları taşımalı. İşaret testi
MEDYANI sınar ve dağılım varsaymaz; ona t tabanlı (normallik varsayan) bir
aralık iliştirmek, aralığı testin söylemediği bir şeye dayandırırdı. Sıra
istatistiği aralığı işaret testinin tam eşleniğidir: aynı binom
dağılımından türer, ve bir t tablosu sabiti gömmeyi gerektirmez.

⚠️ BERABERLİKLER: farkı tam sıfır olan tohumlar DIŞLANIR ve n düşürülür
(klasik işaret testi kuralı). Kaç tohumun dışlandığı **her zaman**
raporlanır — `03` B2: *"`nan` = ölçüm yok"*, ve sıfır fark da bir gözlem
kaybıdır.
"""

from __future__ import annotations

import statistics as ist
from math import comb
from typing import Sequence


def _binom_kuyruk(k: int, n: int) -> float:
    """P(X ≤ k), X ~ Binom(n, 1/2). Kesin — kayan nokta yaklaşımı yok."""
    return sum(comb(n, i) for i in range(k + 1)) / (2 ** n)


def cift_yonlu_p(pozitif: int, n: int) -> float:
    """Çift yönlü kesin işaret testi p değeri.

    Dağılım p = 1/2'de simetriktir; bu yüzden çift yönlü p, küçük kuyruğun
    iki katıdır (1,0 ile sınırlanır).

    🔴 ÇİFT YÖNLÜ olmak zorunda (`03` B2): tek yönlü bir test, ters
    yöndeki bir bulguyu **tanım gereği göremez** — ve bu depoda ters yönde
    çıkan bulgu (gecikme ortalaması) en değerlisiydi.
    """
    if n == 0:
        raise ValueError("n = 0: tüm farklar sıfır, işaret testi tanımsız")
    alt = _binom_kuyruk(pozitif, n)
    ust = _binom_kuyruk(n - pozitif, n)
    return min(1.0, 2.0 * min(alt, ust))


def medyan_guven_araligi(farklar: Sequence[float], alfa: float = 0.05):
    """Medyanın DAĞILIMDAN BAĞIMSIZ %(1−alfa) güven aralığı.

    Sıra istatistiği yöntemi: en büyük `k` bulunur ki 2·P(X ≤ k−1) ≤ alfa;
    aralık sıralı farkların `k`. ve `n+1−k`. elemanıdır (1 tabanlı).

    🔴 `k` bulunamazsa (küçük n'de olur) `None` döner — *"aralık yok"*
    demektir, *"aralık sonsuz"* değil. Bir üst sınır uydurmak, `03` B2'nin
    *"`nan`ı 'etki yok' sanmak"* tuzağıdır.
    """
    n = len(farklar)
    if n == 0:
        return None
    s = sorted(farklar)
    k = 0
    for aday in range(1, n // 2 + 1):
        if 2.0 * _binom_kuyruk(aday - 1, n) <= alfa:
            k = aday
        else:
            break
    if k == 0:
        return None
    return (s[k - 1], s[n - k])


def isaret_testi(farklar: Sequence[float], *,
                 tohum_std: float | None = None,
                 alfa: float = 0.05) -> dict:
    """Eşleştirilmiş farkların işaret testi + dışlanan etki büyüklüğü.

    `tohum_std` verilirse (metriğin o çalışma noktasındaki TOHUMLAR ARASI
    standart sapması), aralık o gürültünün KATI cinsinden de raporlanır —
    bir farkın "küçük" olup olmadığı ancak deneyin kendi gürültüsüne göre
    söylenebilir (`03` B2: *"gürültüden dar tarama"*).
    """
    ham = list(farklar)
    berabere = sum(1 for d in ham if d == 0.0)
    net = [d for d in ham if d != 0.0]
    n = len(net)
    pozitif = sum(1 for d in net if d > 0)

    # 🔴 B-124 (yedinci denetim) — İKİ ESTİMAND, İKİ AYRI ALAN.
    # Önceki hâli `medyan_fark`ı HAM farklardan (sıfırlar dâhil), `ga`yı
    # NET farklardan (sıfırlar dışlanmış) hesaplıyor ve ikisini AYNI
    # satırda basıyordu — oysa bunlar iki AYRI büyüklüğün kestirimidir.
    # Denetimin kırıcı vakası: 20 tohumda fark tam sıfır, 10 tohumda +4/+5
    #   -> `medyan_fark = 0,00` · `ga = [+4,00 · +5,00]`
    #   -> medyan KENDİ GA'sının DIŞINDA
    # Bugünkü veride beraberlik 0–2 olduğu için zarar görünmüyor; ama
    # Faz 1'in sayaç metrikleri (PSR · üç kopma sayacı · COR) çok daha
    # fazla TAM SIFIR fark üretecek.
    # 🔒 İkisi de raporlanır ve hangisinin GA'ya ait olduğu YAZILIR.
    cikti: dict = {
        "n_ham": len(ham), "n": n, "berabere": berabere,
        "pozitif": pozitif,
        "ortalama_fark": ist.mean(ham) if ham else None,
        "medyan_fark": ist.median(ham) if ham else None,        # TÜM farklar
        "medyan_fark_net": ist.median(net) if net else None,    # GA'nın estimandı
        "std_fark": ist.stdev(ham) if len(ham) > 1 else None,
        "p": None, "ga": None, "ga_std_kati": None, "gecti": None,
        # 🔴 B-158 (sekizinci denetim) — `06` Bolum 7'nin DURDURMA KURALI
        # ("eps_rel = GA yari genisligi / nokta tahmini <= %10") ilan
        # edilmisti ve `06` 9.2(b) bir BAND yaziyordu, ama deponun
        # hicbir yerinde onu URETEN kod yoktu (AST/grep: sifir). Sayi
        # elle hesaplanmisti — `03` kural 1, muhre giden bir sayfada.
        "eps_rel": None,
        # 🔴 B-125 — ÖLÇÜT İKİ AYAKLIDIR ve ikinci ayak HENÜZ BOŞ.
        "buyukluk_ayagi": None,
    }
    if n == 0:
        # 🔴 "Ölçüm yok" ile "etki yok" AYNI ŞEY DEĞİLDİR (`03` B2).
        cikti["not"] = ("tüm farklar sıfır — işaret testi TANIMSIZ; "
                        "bu bir 'etki yok' bulgusu değildir")
        return cikti

    cikti["p"] = cift_yonlu_p(pozitif, n)
    ga = medyan_guven_araligi(net, alfa)
    cikti["ga"] = ga
    if ga is not None and tohum_std:
        cikti["ga_std_kati"] = (ga[0] / tohum_std, ga[1] / tohum_std)

    # ------------------------------------------------------------------
    # 🔴 B-125 — ÖLÇÜT YALNIZCA İŞARETE BAKIYORDU, BÜYÜKLÜĞÜ SERBEST
    # BIRAKIYORDU. Denetim iki karşı vaka üretti ve İKİSİ DE GEÇTİ:
    #   16/30 tohumda +2σ  -> p = 0,8555  GEÇTİ  (medyan +2,00 × std)
    #   20/30 tohumda +5σ  -> p = 0,0987  GEÇTİ  (medyan +5,00 × std)
    # Yani tohumların %66,7'sinde aynı yönde ve gürültünün BEŞ KATI olan
    # bir koşu-uzunluğu bağımlılığı "bağımsız" sayılıyordu.
    #
    # 🔒 KARAR (danışmana devredildi, K-088): ölçüt İKİ AYAKLI ilan edilir
    #   ayak 1 — YÖN     : çift yönlü kesin işaret testi, α = 0,05
    #   ayak 2 — BÜYÜKLÜK: |GA uçları| ≤ k × tohumlar arası std
    #
    # 🔴 `k` BUGÜN YAZILAMAZ. `06` Bölüm 7 güç analizini MÜHÜRDE yapıyor;
    # bir sabit ancak ≥30 tohumun GA'sından türetilirse yazılabilir
    # (`03` kural 2). Bugün bir sayı uydurmak, tam olarak bu ölçütün
    # engellemeye çalıştığı şey olurdu.
    #
    # 🔒 Sonucu: `gecti` YALNIZCA AYAK 1'i temsil eder ve alan adı bunu
    # söyler. Koşul 1 bugün HİÇBİR KOL için "sağlandı" sayılamaz —
    # ölçüt EKSİKTİR ve eksikliği raporlanır (B-127 ile birlikte okunur).
    # ------------------------------------------------------------------
    # 🔴 B-158 — eps_rel URETILIYOR. Payda GA'NIN ESTIMANDIDIR
    # (`ga_estimandi`), HAM medyan degil: beraberlik varken HAM medyan
    # TAM SIFIR olabilir ve oran tanimsizlasir. Olculdu: bugunku 18
    # ciftin 2'sinde (DV/S0 ve DV/S2 teslim orani) HAM medyan tam sifir.
    # 🔒 Sifir estimandda oran TANIMSIZDIR ve `None` doner — `03` B2:
    # "`nan` = olcum yok, 'etki yok' DEGIL".
    if ga is not None:
        nokta = ga_estimandi(cikti)
        if nokta:
            cikti["eps_rel"] = 100.0 * ((ga[1] - ga[0]) / 2.0) / abs(nokta)

    cikti["gecti"] = cikti["p"] > alfa          # AYAK 1 (yön) — tek başına
    if ga is not None and tohum_std:
        cikti["buyukluk_ayagi"] = {
            "olculen_ga_std_kati": max(abs(ga[0]), abs(ga[1])) / tohum_std,
            "esik_k": None,                      # 🔒 B4'te güç analizinden
            "yargi": "ESIK YOK — olcut EKSIK (B-125)",
        }
    return cikti


# ==========================================================================
# 🔒 RAPORLAMA SÖZLEŞMESİ — TEK KAYNAK (B-145 · B-146, sekizinci denetim)
# ==========================================================================
# 🔴 NEDEN BU İKİ FONKSİYON VAR.
# B-124 ve B-125'in düzeltmeleri yalnızca `satir()`e yazılmıştı ve
# sekizinci denetim ölçtü: `satir()`in deposunda **SIFIR çağıranı** var
# (AST ile doğrulandı; `tests/test_isaret_testi.py` onu içe bile
# aktarmıyor). `06` §9.1 ve §8.1b'yi FİİLEN basan
# `dogrulama/gecerlilik.py::_yaz_kosul1/_yaz_kosul2` dokunulmamıştı:
#
#     _yaz_kosul1 -> "GECTI"/"GECMEDI", sütun başlığı "yargi"
#                    18 satırın 15'i "GECTI" basıyordu — oysa `06` §9.2(a)
#                    "koşul 1 bugün HİÇBİR KOL için sağlandı sayılamaz" der
#     _yaz_kosul1/2 -> HAM medyanı NET medyanın GA'sının YANINDA basıyordu
#                    18 satırın 7'sinde ayrışıyor, 2'sinde İŞARET TERS
#
# ⚖️ A-25 (sekizinci denetimin ANLAŞILMAYANLAR'ı) *"neden iki ayrı
# biçimlendirici"* diye sordu. Cevap: olmamalı. Kural bir NESNEYE değil
# bir SÖZLEŞMEYE yazılır; iki biçimlendirici de aynı iki fonksiyonu
# çağırır ve üçüncü bir biçimlendirici yazılırsa o da çağırmak zorunda
# kalır. Bu, deponun *"kuralı komşuya uygulamama"* örüntüsüne yapısal
# cevaptır — komşu diye bir şey kalmıyor.

def ayak1_etiketi(s: dict) -> str:
    """`gecti` YALNIZCA AYAK 1'dir (yön) — etiket bunu SÖYLEMEK ZORUNDA.

    🔴 B-125/K3: ölçüt iki ayaklıdır ve ayak 2'nin eşiği `k` BOŞtur
    (`06` §9.2(a); `k` B4'ün güç analizinden gelir). *"GECTI"* yazmak,
    ölçütün tamamının sağlandığını ima eder ve `06`nın kendi cümlesiyle
    çelişir. *"YON-OK"* yalnızca ölçülen şeyi söyler.
    """
    return "YON-OK" if s["gecti"] else "YON-RED"


def ga_estimandi(s: dict) -> float | None:
    """GA'nın estimandı — beraberlik varsa NET medyan (B-124).

    `medyan_guven_araligi` NET farklardan (sıfırlar dışlanmış) kurulur;
    `medyan_fark` ise TÜM farkların medyanıdır. Beraberlik varken ikisi
    ayrışır ve HAM medyan kendi GA'sının **dışında** kalabilir.
    """
    if s.get("berabere") and s.get("medyan_fark_net") is not None:
        return s["medyan_fark_net"]
    return s.get("medyan_fark")


def satir(ad: str, s: dict) -> str:
    """Tek satırlık rapor — p, GA ve dışlanan etki BİRLİKTE yazılır."""
    if s["p"] is None:
        return f"{ad:<34s} TANIMSIZ (tüm farklar sıfır, n_ham={s['n_ham']})"
    ga = s["ga"]
    ga_m = "yok" if ga is None else f"[{ga[0]:+.4f}, {ga[1]:+.4f}]"
    kat = ("" if s["ga_std_kati"] is None
           else f"  = std x [{s['ga_std_kati'][0]:+.2f}, "
                f"{s['ga_std_kati'][1]:+.2f}]")
    # 🔴 B-124: beraberlik varsa GA'nın estimandı `medyan_fark_net`tir;
    # ikisi ayrıştığında İKİSİ DE basılır, yoksa okuyucu GA'yı yanlış
    # medyanla eşleştirir.
    net_not = ""
    if s["berabere"] and s.get("medyan_fark_net") is not None:
        net_not = f" med_net={s['medyan_fark_net']:+.4f}"
    # 🔴 B-125: `gecti` yalnızca AYAK 1'dir; etiket bunu söylemek zorunda.
    # 🔒 B-145: etiket ARTIK TEK KAYNAKTAN — `_yaz_kosul1/2` de aynısını çağırır.
    yon = f"{ayak1_etiketi(s):<7}"
    return (f"{ad:<34s} {s['pozitif']:>3d}/{s['n']:<3d} "
            f"p={s['p']:.4f} {yon} "
            f"ort={s['ortalama_fark']:+.4f} med={s['medyan_fark']:+.4f}"
            f"{net_not} GA={ga_m}{kat}"
            + (f"  (berabere {s['berabere']})" if s["berabere"] else ""))
