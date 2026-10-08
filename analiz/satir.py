"""
SONUÇ SATIRLARI — okuma, süzme, eşleştirme ve ham denetimi (`v2/06` §7–§8).

🔒 EŞLEŞTİRME BİR İDDİADIR, DENETLENİR
======================================
Eşleştirilmiş Wilcoxon, iki kolun AYNI tohumda AYNI dünyayı gördüğünü
varsayar (`v2/06` §7: aynı tohum aynı senaryo, kanal hash'ten). Varsayım
satırın kendi kimliğinden sınanır — yoksa yanlış eşlenen iki satır sessizce
teste girer:
  · `arac_hash` bütün satırlarda aynı — aynı simülatör kodu;
  · `kurulum_hash` bütün satırlarda aynı — aynı dünya (tedavi dışı her alan);
  · her tohumda senaryo, tehdit ve desen aynı; `evren_hash` aynı — iki kol
    aynı paket evrenini (kimlik, doğum, kaynak, hedef) taşıyor.
Biri tutmazsa `AnalizHatasi`: karşılaştırma YAPILMAZ.

🔒 GEÇERSİZ SATIR TESTE GİRMEZ ve bu SAYILIR: `korunum.gecerli = False`
olan satır dışlanır, dışlanma sebebiyle döner. Bir kolda dışlanan tohum
eşinden de düşer (eşleştirme bozulmasın) ve rapora yazılır.

🔒 METRİK `None` İSE SESSİZ ATLAMA YOK: `None` "tanımsız" demektir (ör. hiç
paket doğmadı). Ortalamaya da teste de giremez; `AnalizHatasi`.

🔴 HAM DENETİMİ — İKİNCİ GERÇEKLEME (`olcum/metrikler.py` başlığı)
=================================================================
`pdr_pencere`, pencere gecikme yüzdelikleri ve görev teslim oranı satırın
`ham` bölümünden BURADA yeniden üretilir ve satırdaki değerle karşılaştırılır.
Yüzdelik gövdesi `metrikler.yuzdelik` ile aynı tanımdır (doğrusal ara
değerleme) ama bilerek ayrı yazıldı: iki gerçekleme ayrışırsa bu denetim
kırmızı yanar. Simülatör içe aktarılmaz.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable, Sequence

from analiz.istatistik import AnalizHatasi, dogrula

__all__ = ["oku", "alan", "gecerli_suz", "eslestir", "yuzdelik",
           "ham_denetimi"]

_TEDAVI_ESLESEN = ("senaryo", "tehdit_senaryosu", "trafik_deseni")


def oku(yol: str | Path) -> list[dict]:
    satirlar = []
    with open(yol, encoding="utf-8") as dosya:
        for no, metin in enumerate(dosya, start=1):
            metin = metin.strip()
            if not metin:
                continue
            try:
                satirlar.append(json.loads(metin))
            except json.JSONDecodeError as hata:
                raise AnalizHatasi(f"{yol}:{no} bozuk JSON: {hata}") from hata
    return satirlar


def alan(satir: dict, yol: str):
    """Noktalı yol — `metrikler.pdr_pencere`. Yoksa `AnalizHatasi`."""
    deger = satir
    for parca in yol.split("."):
        dogrula(isinstance(deger, dict) and parca in deger,
                f"satırda alan yok: {yol}")
        deger = deger[parca]
    return deger


def gecerli_suz(satirlar: Iterable[dict]) -> tuple[list[dict], list[dict]]:
    """`(geçerli, dışlanan)` — dışlanan her satır `sebep` taşır."""
    gecerli, dislanan = [], []
    for s in satirlar:
        if alan(s, "korunum.gecerli"):
            gecerli.append(s)
        else:
            k = s["korunum"]
            sebep = [ad for ad in ("korunum_tamam", "mutabakat_tamam",
                                   "iletim_sonucu_tamam", "enerji_sure_tamam")
                     if k.get(ad) is False]
            dislanan.append({"tohum": alan(s, "kimlik.tohum"),
                             "protokol": alan(s, "kimlik.protokol"),
                             "sebep": sebep or ["gecerli=False"]})
    return gecerli, dislanan


def _tohum_indeksi(satirlar: Sequence[dict]) -> dict[int, dict]:
    cikti: dict[int, dict] = {}
    for s in satirlar:
        t = alan(s, "kimlik.tohum")
        dogrula(t not in cikti, f"aynı kolda tohum iki kez: {t}")
        cikti[t] = s
    return cikti


def eslestir(a: Sequence[dict], b: Sequence[dict], metrik: str
             ) -> tuple[list[int], list[float], list[float], list[int]]:
    """İki kolun geçerli satırlarını tohumla eşler.

    Döner: `(tohumlar, x, y, eşi_düşen_tohumlar)`. Kimlik denetimi başlıkta."""
    ia, ib = _tohum_indeksi(a), _tohum_indeksi(b)
    ortak = sorted(set(ia) & set(ib))
    dusen = sorted(set(ia) ^ set(ib))
    dogrula(len(ortak) > 0, "iki kolun ortak tohumu yok")
    tum = [ia[t] for t in ortak] + [ib[t] for t in ortak]
    for ozet in ("arac_hash", "kurulum_hash"):
        degerler = {alan(s, f"kimlik.{ozet}") for s in tum}
        dogrula(len(degerler) == 1,
                f"{ozet} satırlar arasında farklı ({len(degerler)} değer) — "
                f"aynı kod/dünya değil, eşleştirme geçersiz")
    x, y = [], []
    for t in ortak:
        sa, sb = ia[t], ib[t]
        for ad in _TEDAVI_ESLESEN:
            dogrula(sa["konfig"].get(ad) == sb["konfig"].get(ad),
                    f"tohum {t}: {ad} kollar arasında farklı")
        dogrula(alan(sa, "kimlik.evren_hash") == alan(sb, "kimlik.evren_hash"),
                f"tohum {t}: paket evreni farklı — eşleştirme geçersiz")
        va, vb = alan(sa, metrik), alan(sb, metrik)
        dogrula(va is not None and vb is not None,
                f"tohum {t}: {metrik} tanımsız (None) — sessiz atlama yok")
        dogrula(math.isfinite(va) and math.isfinite(vb),
                f"tohum {t}: {metrik} sonlu değil")
        x.append(float(va))
        y.append(float(vb))
    return ortak, x, y, dusen


def yuzdelik(ornekler: Sequence[float], p: int) -> float | None:
    """`olcum/metrikler.yuzdelik`in İKİNCİ gerçeklemesi — aynı tanım
    (doğrusal ara değerleme), ayrı gövde. Boşta `None`."""
    if not ornekler:
        return None
    s = sorted(ornekler)
    if len(s) == 1:
        return s[0]
    k = (len(s) - 1) * (p / 100.0)      # ifade sırası metriklerle AYNI
    alt, ust = math.floor(k), math.ceil(k)
    return s[alt] if alt == ust else s[alt] + (k - alt) * (s[ust] - s[alt])


def donem_araliklari(acilma_s: float, bas_s: float, bitis_s: float,
                     acik_s: float, sessiz_s: float, acik: bool = True
                     ) -> tuple[tuple[float, float], ...]:
    """Çizelgenin açık (ya da sessiz) dönemleri, ölçüm penceresine
    kırpılmış — `olcum/evre.py::Evreler.donemler`in İKİNCİ gerçeklemesi
    (ayrı gövde; ham denetimi ikisini karşılaştırır)."""
    periyot = acik_s + sessiz_s
    dogrula(periyot > 0.0, "çizelge periyodu pozitif olmalı")
    cikti: list[tuple[float, float]] = []
    k = 0
    while acilma_s + k * periyot < bitis_s:
        t0 = acilma_s + k * periyot
        a, b = (t0, t0 + acik_s) if acik else (t0 + acik_s, t0 + periyot)
        a, b = max(a, bas_s), min(b, bitis_s)
        if b > a:
            cikti.append((a, b))
        k += 1
    return tuple(cikti)


def donem_pdr(satir: dict, acik: bool = True,
              cizelge: Sequence[float] | None = None) -> float | None:
    """Karıştırıcının açık (ya da sessiz) dönemlerinde DOĞAN paketlerin
    teslim oranı, satırın `ham`ından (K-222, denetim D-01).

    `cizelge` verilmezse satırın kendi çizelgesi (`metrikler.evre_cizelge_s`)
    kullanılır; karıştırıcısız ikiz hücrede aynı çizelge HAYALET olarak
    verilir — aynı zaman dilimleri, karıştırıcı yok. Paydası boşsa `None`."""
    bas, bitis = alan(satir, "kapsam.olcum_penceresi_s")
    if cizelge is None:
        cizelge = satir["metrikler"].get("evre_cizelge_s")
        dogrula(cizelge is not None,
                "satırda çizelge yok — karıştırıcısız kolda `cizelge` ver")
    acilma = alan(satir, "konfig.karistirici_baslangic_s")
    araliklar = donem_araliklari(acilma, bas, bitis, *cizelge, acik=acik)
    ham = satir["ham"]

    def icinde(t: float) -> bool:
        return any(a <= t < b for a, b in araliklar)

    dogan = sum(1 for d in ham["dogum_s"] if icinde(d))
    if not dogan:
        return None
    return sum(1 for d in ham["teslim_dogum_s"] if icinde(d)) / dogan


def ham_denetimi(satir: dict) -> dict[str, tuple]:
    """Satırdaki metrikleri `ham`dan yeniden üretir: `{ad: (satır, ham,
    tutuyor_mu)}`. Karşılaştırma TAM eşitliktir — aynı işlem aynı sırayla."""
    bas, bitis = alan(satir, "kapsam.olcum_penceresi_s")
    ham = satir["ham"]

    def icinde(t: float) -> bool:
        return bas <= t < bitis

    dogan = sum(1 for d in ham["dogum_s"] if icinde(d))
    teslim_idx = [i for i, d in enumerate(ham["teslim_dogum_s"]) if icinde(d)]
    teslim = len(teslim_idx)
    cikti: dict[str, tuple] = {}
    m = satir["metrikler"]
    pdr = teslim / dogan if dogan else None
    cikti["pdr_pencere"] = (m.get("pdr_pencere"), pdr,
                            m.get("pdr_pencere") == pdr)
    gecikme = [ham["teslim_gecikmeleri_s"][i] for i in teslim_idx]
    for p in (50, 95, 99):
        ad = f"gecikme_p{p}_s_pencere"
        h = yuzdelik(gecikme, p)
        cikti[ad] = (m.get(ad), h, m.get(ad) == h)
    # K-222: çizelgeli satırda açık/sessiz PDR'si de ikinci gerçeklemeyle.
    for ad, acik in (("pdr_acik", True), ("pdr_sessiz", False)):
        if m.get(ad) is not None and m.get("evre_cizelge_s") is not None:
            h = donem_pdr(satir, acik=acik)
            cikti[ad] = (m[ad], h, m[ad] == h)
    if "gorev_teslim_orani_pencere" in m:
        plan = (dogan + sum(1 for d in ham.get("olu_hedefe_dogum_s", ())
                            if icinde(d))
                + sum(1 for d in ham.get("uretilmeyen_dogum_s", ())
                      if icinde(d)))
        g = teslim / plan if plan else None
        cikti["gorev_teslim_orani_pencere"] = (
            m["gorev_teslim_orani_pencere"], g,
            m["gorev_teslim_orani_pencere"] == g)
    return cikti
