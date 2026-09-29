# -*- coding: utf-8 -*-
"""KONTROL DÜZLEMİ BÜTÇESİ — `08` madde 25'in üretici aracı.

==========================================================================
🔴 NEDEN BU DOSYA VAR (B-80, beşinci bağımsız denetim)

`08` madde 25 bir beyan değil, **bağlayıcı bir kısıttır**:

    "🔒 Aile 1'in ilk karşılaştırmasından önce ya bir tavan konur ya da
     her karşılaştırma kontrol payıyla birlikte raporlanır."

O kısıtın kalibre edileceği sayı 21 Ağustos'ta ölçüldü ve `08`e yazıldı —
**üretici komutuyla birlikte.** Beşinci denetim onu yeniden üretmeye çalıştı
ve **tutmadı**: sayı, B-66'nın *(aynı oturumda yapılan)* maliyet modeli
düzeltmesinden ÖNCEki modelle ölçülmüştü.

⚖️ **Dersin kendisi bir kural oldu (Y14):** bir sayının **üretici satırı
olması, yeniden üretilebildiğini göstermez.** Eksik olan satır değil,
düzeltme sonrası **yeniden koşudur.** Bu dosya o yeniden koşuyu **bir
komuta** indirger:

    python dogrulama/kontrol_payi.py

==========================================================================
⚠️ BU BİR DENEY KOLU DEĞİLDİR; ölçüm aracıdır ve `dogrulama/` altındadır.
Tohumlar **1–3** (ayarlama/kapı kümesi 1–30 içinde). Ana deney tohumları
(2000–2029) burada HİÇBİR AMAÇLA koşulmaz.
==========================================================================
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.config import Konfig                                    # noqa: E402
from dogrulama.olcum import kayit, olc                           # noqa: E402
from dogrulama.aktaricilar import AKTARICILAR                    # noqa: E402
# Pencere okumasi KOPYALANMAZ, ice aktarilir: `sim/karsilastirma.py`
# onu zaten `06` Bolum 9 kosul 3 icin zorunlu kiliyor. Ikinci bir
# formul, B-07'nin "ikinci dogru kaynagi" tuzagidir.
from sim.karsilastirma import (KarsilastirmaHatasi,              # noqa: E402
                               kontrol_payi_yuzde)

SENARYOLAR = ("S0", "S2")
# 3 -> 30 (B0.4). `03` kural 2: "tek/az tohumlu sonuc raporlama;
# >=30 tohum + guven araligi". `08` md 25'in baglayici orani UC
# tohumdan gelmisti ve `06` Bolum 9 kosul 3 ona dayaniyor.
TOHUMLAR = tuple(range(1, 31))


def mesafe_vektoru(kon: Konfig):
    """🔴 KÂHİNSİZ mesafe-vektörü kolu — yalnızca `Gozlem` + `beacon_yuku`.

    Kontrol düzlemi bütçesini ÖLÇMEK için var: her düğüm kendi mesafe
    tablosunu beacon yüküne koyar, yani bilgi **tel üzerinden** taşınır ve
    bedeli `yuk_bayt` ile faturalanır. Topolojiyi konfigürasyondan okumaz.
    """
    d = {"t": {}}

    def ogren(g):
        yeni = {g.dugum: (0, g.dugum)}
        for k in g.komsular:
            yeni.setdefault(k.dugum, (1, k.dugum))
            for ad, v in k.bildirdigi_yuk:
                if not ad.startswith("d"):
                    continue
                try:
                    h = int(ad[1:])
                except ValueError:
                    continue
                if h == g.dugum:
                    continue
                if h not in yeni or v + 1 < yeni[h][0]:
                    yeni[h] = (v + 1, k.dugum)
        d["t"] = yeni
        return yeni

    def sec(g):
        t = ogren(g)
        if g.paket is None or not g.komsular:
            return None
        r = t.get(g.paket.hedef)
        if r is None or r[1] == g.dugum:
            return None
        return r[1] if any(k.dugum == r[1] for k in g.komsular) else None

    sec.beacon_yuku = lambda dug: {
        ("d%d" % h): m for h, (m, _) in (d["t"] or {dug: (0, dug)}).items()
        if m <= 8
    }
    return sec


class DejenereOlcum(ValueError):
    """Kontrol payı bu koşuda TANIMSIZ — bir oran değil, bir artefakt."""


def kontrol_payi(sonuc: dict) -> float:
    """Kontrol baytının toplam bayta oranı, yüzde.

    🔴 D-11 (27 Ağustos 2026) — DEJENERE PAYDA ARTIK REDDEDİLİYOR.

    Ölçüldü: `DV` kolu `S2/seyrek/t11`de **tek bir veri baytı bile
    göndermiyor** —

        kontrol_bayt=533 870   veri_bayt=0   teslim=0/1078

    — ve eski hâl bunu `nan` ya da hata değil, **kendinden emin görünen
    `100.0`** olarak döndürüyordu. Aynı çalışma noktasında gözlem kolu
    %2,647 veriyor; eşleştirilmiş oran **37,8 kat** çıkıyor ve tamamen
    anlamsız. `08` madde 25'in BAĞLAYICI oranı tam olarak bu fonksiyondan
    geçiyor ve Aile 1'in ilk karşılaştırması ona dayanacak.

    `03` B2: *"`nan` = ölçüm yok"*. Burada `nan` bile yoktu. Sessiz bir
    sayı yerine **tipli bir ret** veriliyor — `karsilastirma.py`nin
    `KarsilastirmaHatasi` deseni (B-26) ve `teshis_dogrula`nın *"anında ve
    tipli reddet"* deseni (B-87) ile aynı.

    ⚠️ Sınırı (Y11): yalnızca `veri_bayt == 0` yakalanır. **Çok küçük ama
    sıfır olmayan** bir payda hâlâ gürültülü bir oran üretir ve bu ret
    onu görmez; o eksen `08` madde 25'in çalışma noktası beyanıyla
    yönetilir.
    """
    kb, vb = sonuc["kontrol_bayt"], sonuc["veri_bayt"]
    if vb == 0:
        raise DejenereOlcum(
            f"kontrol payı TANIMSIZ: veri_bayt=0 (kontrol_bayt={kb}). "
            f"Kol bu çalışma noktasında hiç veri göndermemiş; oran %100 "
            f"görünür ama bir kontrol payı DEĞİLDİR (D-11). "
            f"teslim_orani={sonuc.get('teslim_orani')!r}")
    return 100.0 * kb / (kb + vb)


def eslestirilmis_oranlar(
        paylar: dict, senaryolar=None, tohumlar=None
) -> tuple[list[float], list[tuple[str, int]]]:
    """🔴 KARAR ÜRETEN YÜKLEM — ayrı ve test edilebilir (`03` B5).

    Döner: `(oranlar, dejenere_hucreler)`.

    ⚠️ İlk hâli `main()`in içine gömülüydü ve onu koruyan test `ast.unparse`
    metninde *"dejenere"* kelimesini arıyordu. Mutasyon (`dejenere.append`
    → `pass`) o testten **SAĞ ÇIKTI**: değişken adı metinde duruyordu.
    Metin kontrolü davranış kontrolü değildir — deponun kendi dersi
    (B-09 · B-89 · B-111), bu kez benim yazdığım korumada.

    🔴 Dejenere hücre orana GİRMEZ **ve ayrıca sayılır.** Sessizce
    atlanırsa aralık, kaç gözlemden hesaplandığını söylemeden daralır
    (`03` B2: *"üst sınır verirken KAÇ GÖZLEMLE hesaplandığını da yaz"*).
    """
    senaryolar = SENARYOLAR if senaryolar is None else senaryolar
    tohumlar = TOHUMLAR if tohumlar is None else tohumlar
    oranlar: list[float] = []
    dejenere: list[tuple[str, int]] = []
    for sen in senaryolar:
        for t in tohumlar:
            a = paylar[("DV", sen, t)]
            b = paylar[("gurultuden_kacan", sen, t)]
            if a is None or b is None or b == 0:
                dejenere.append((sen, t))
                continue
            oranlar.append(a / b)
    return oranlar, dejenere


def paylari_olc():
    """Uc okuma birden dondurur: TUM KOSU bayt, PENCERE bayt, PENCERE airtime.

    🔴 NEDEN UC OKUMA (B0.4 · F-5)
    ===============================
    Bu fonksiyon `08` madde 25'in baglayici oranini uretiyor ve
    `06` Bolum 9 kosul 3 ona dayaniyor. Ama `kontrol_payi()` TUM KOSU
    baytini okuyor — oysa `08` madde 31 acikca sunu diyor:

        "Aile 1'in her karsilastirmasi `*_pencere` alanlarini kullanmak
         ZORUNDADIR; tum kosu hali teshis icindir."

    Ve ayni madde olcmus: kontrol baytinin %17,63-22,84'u pencere DISINDA
    uretiliyor ve carpiklik KOLA GORE degisiyor. Yani tum kosu haliyle
    kurulan eslestirilmis bir kol orani YANLI olabilir.

    🔴 Hangi okumanin dogru oldugu IDDIA EDILMEZ — ucu de olculur, farki
    yazilir, karar `04`e ureticisiyle gecer.

    ⚠️ AIRTIME ayri bir okumadir, sus payi degil: olculdu — ayni bayti
    farkli sayida cerceveye bolen iki protokol bayt metriginde ESIT
    gorunur ve airtime'da 2 kat farkli olur (`08` §Ayrica).
    """
    tum: dict = {}
    pencere_bayt: dict = {}
    pencere_air: dict = {}
    for ad, fab in (("DV", mesafe_vektoru),
                    ("gurultuden_kacan", AKTARICILAR["gurultuden_kacan"])):
        for sen in SENARYOLAR:
            for t in TOHUMLAR:
                s = olc(Konfig(kol="t", senaryo=sen, trafik="orta",
                               tohum=t), fab, kol=ad)
                anahtar = (ad, sen, t)
                # 🔴 D-11: dejenere hucre bir SAYIYA donusturulmez.
                try:
                    tum[anahtar] = kontrol_payi(s)
                except DejenereOlcum as e:
                    tum[anahtar] = None
                    print("%-18s %s t%d DEJENERE (tum kosu) — %s" % (ad, sen, t, e))
                # 🔴 B-134: TANIMSIZ artik `None` doner, istisna DEGIL.
                pay = kontrol_payi_yuzde(s)
                if pay is None:
                    pencere_bayt[anahtar] = None
                    pencere_air[anahtar] = None
                    print("%-18s %s t%d DEJENERE (pencere) — veri_bayt_pencere=0"
                          % (ad, sen, t))
                else:
                    pencere_bayt[anahtar] = pay["bayt"]
                    pencere_air[anahtar] = pay["airtime"]
                if tum[anahtar] is not None and pencere_bayt[anahtar] is not None:
                    print("%-18s %s t%02d teslim=%.4f  tum=%.2f%%  "
                          "pencere=%.2f%%  airtime=%.2f%%"
                          % (ad, sen, t, s["teslim_orani"], tum[anahtar],
                             pencere_bayt[anahtar], pencere_air[anahtar]))
    return tum, pencere_bayt, pencere_air


def _oran_ozeti(baslik: str, paylar: dict) -> None:
    """Bir okumanin kol araligi + ESLESTIRILMIS orani."""
    dv = [paylar[("DV", s, t)] for s in SENARYOLAR for t in TOHUMLAR]
    gk = [paylar[("gurultuden_kacan", s, t)] for s in SENARYOLAR
          for t in TOHUMLAR]
    dv_g = [x for x in dv if x is not None]
    gk_g = [x for x in gk if x is not None]
    oranlar, dejenere = eslestirilmis_oranlar(paylar)
    print()
    print("--- %s ---" % baslik)
    if not dv_g or not gk_g or not oranlar:
        print("   olculebilir hucre yok")
        return
    print("   DV kolu           : %%%.2f - %%%.2f  (%d hucre)"
          % (min(dv_g), max(dv_g), len(dv_g)))
    print("   gozlem kolu       : %%%.2f - %%%.2f  (%d hucre)"
          % (min(gk_g), max(gk_g), len(gk_g)))
    # 🔴 "ortanca" GERCEK MEDYAN olmali: `sorted[n//2]` cift n'de UST
    # ORTAYI verir ve `statistics.median`dan ayrisir. Ayni veriden iki
    # arac iki "ortanca" bastigi icin fark edildi (12,9 vs 12,6).
    import statistics as _ist
    print("   ESLESTIRILMIS ORAN: %.1f - %.1f kat  (ortanca %.1f, %d hucre)"
          % (min(oranlar), max(oranlar), _ist.median(oranlar), len(oranlar)))
    print("   DEJENERE hucre    : %d  %s"
          % (len(dejenere), dejenere if dejenere else ""))


def main() -> int:
    print("=" * 74)
    print("KONTROL DÜZLEMİ BÜTÇESİ — `08` madde 25 (B-77 · B-80)")
    print("=" * 74)
    print("%d senaryo × %d tohum × 2 kol = %d tam koşu · tahmini ~3 dk"
          % (len(SENARYOLAR), len(TOHUMLAR),
             2 * len(SENARYOLAR) * len(TOHUMLAR)))
    print()
    tum, pencere_bayt, pencere_air = paylari_olc()

    print()
    print("=" * 74)
    print("OZET — `08` madde 25 ve `06` Bolum 9 kosul 3 BU sayilarla yazilir")
    print("=" * 74)
    print("`03` B2: iki kol yalnizca AYNI calisma noktasinda karsilastirilir;")
    print("capraz esleme (bir kolun en kucugu ile digerinin en buyugu)")
    print("ANLAMSIZDIR ve B-80'de bir kez yapilmisti.")
    _oran_ozeti("TUM KOSU · bayt   (eski olcum bunu kullaniyordu)", tum)
    _oran_ozeti("PENCERE  · bayt   (`08` md 31'in sart kostugu okuma)",
                pencere_bayt)
    _oran_ozeti("PENCERE  · airtime (gercek kit kaynak: kanal zamani)",
                pencere_air)
    print()
    print("🔒 Y14: `sim/` ya da `dogrulama/` altında bir maliyet değişikliği")
    print("   olduğunda BU KOMUT YENİDEN KOŞULUR ve `08` güncellenir.")
    return 0


if __name__ == "__main__":
    with kayit("kontrol_payi"):
        raise SystemExit(main())
