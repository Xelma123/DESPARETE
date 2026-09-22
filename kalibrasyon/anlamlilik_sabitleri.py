"""
EVRE METRİKLERİNİN ANLAMLILIK SABİTLERİ — çok pencereli taramada gerçek yanlış alarm ne?

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/anlamlilik_sabitleri.py

Bağlam: `v2/08-EVRE-METRIKLERI.md` §05.3 · K-113 — öğrenci kararı: *"sen
ölçerek en mantıklısını yap."*

🔴 NE ÖLÇÜLÜYOR — simülatörsüz, sentetik boş hipotez
===================================================
M4 (tespit gecikmesi) açılma anından ölçüm penceresinin sonuna kadar 1 s'lik
pencereleri TEK TEK tarar ve eşiği aşan İLK pencereyi alır. Pencere başına α
küçük olsa bile ~170 pencere taranınca "en az bir yanlış tespit" olasılığı
çok büyüyebilir — `08` §05.3 bunu HESAPLA gösterdi, ölçmedi.

Bu betik onu ÖLÇER. Beyanlar sabit hızlı bir Poisson sürecidir ve açılma
anında HİÇBİR değişiklik yoktur; yani bulunan her "tespit" yanlış alarmdır.
Çağrılan fonksiyon gerçek `Evreler.tespit_gecikmesi`dir — ikinci bir
gerçekleme yazılmaz. Eşik kuralı modül sabiti geçici olarak değiştirilerek
oynatılır; `sim2/` dosyalarına dokunulmaz.

Karşılaştırılan iki eşik kuralı:
  · ESKİ (Y10 öncesi) — pencere başına sabit 0,01
  · BUGÜNKÜ (Y10)     — pencere başına `ALFA / taranan pencere` (Bonferroni)

🔒 BU ARTIK BİR KAPIDIR (Y10, `07` §18 Y10): bugünkü kuralın ölçülen aile
düzeyi yanlış alarmı `ALFA`yı aşarsa çıkış kodu 1 olur. Eski kural yalnız
karşılaştırma için koşuyor ve aynı gövdeden geçiyor — ikinci bir eşik
gerçeklemesi yazılmadı: aile düzeyi α `0,01 × taranan pencere` verilerek
pencere başına 0,01'e geri çevriliyor.

⚠️ SINIRLAR — beyan edilir
==========================
  · Süreç HOMOJEN Poisson. Gerçek kopma beyanları kümelenebilir (aşırı
    dağılım); o durumda bugünkü kuralın yanlış alarmı DAHA DA yüksek olur.
    Aşama 2'de gerçek bir protokolle yeniden ölçülür.
  · Yalnız M4 ölçülür. M3'ün (toparlanma süresi) 2·SE bandı da ilk başarılı
    pencereyi aldığı için erken toparlanmaya yanlıdır; onun sentetik sınavı
    paket doğum/teslim süreci ister ve ayrı yapılır.
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

import sim2.olcum.evre as evre  # noqa: E402


class _BosPaketDefteri:
    """`Evreler` kurucusu için boş defter — M4 paket defterini okumaz."""

    def dogumlar(self):
        return ()

    def kayitlar(self):
        return ()


class _SentetikBeyanlar:
    """`RotaDefteri`nin M4'ün okuduğu iki yüzü: beyan anları ve beyan var mı."""

    def __init__(self, anlar: tuple[float, ...]) -> None:
        self._anlar = anlar
        self.beyan_etmiyor = not anlar

    def beyan_anlari(self, tip: str) -> tuple[float, ...]:
        return self._anlar


def _poisson_anlari(r: random.Random, hiz: float, bas_s: float,
                    bitis_s: float) -> tuple[float, ...]:
    """Homojen Poisson süreci — üstel ara süreler."""
    anlar: list[float] = []
    t = bas_s
    while True:
        t += r.expovariate(hiz)
        if t >= bitis_s:
            return tuple(anlar)
        anlar.append(t)


def _yanlis_alarm_orani(hiz: float, deneme: int, aile_alfa: float, tohum: int,
                        bas_s: float, acilma_s: float,
                        bitis_s: float) -> tuple[float, float, int]:
    """(yanlış alarm oranı, 2·SE, taranan pencere sayısı).

    🔒 `aile_alfa` AİLE düzeyindedir; modül onu Bonferroni ile pencere
    başına böler. Eski kuralı yeniden üretmek için
    `aile_alfa = 0,01 × taranan pencere` verilir.
    """
    r = random.Random(tohum)
    eski = evre.ALFA
    evre.ALFA = aile_alfa
    try:
        e = evre.Evreler(_BosPaketDefteri(), bas_s, acilma_s, bitis_s)
        pencere = int(math.floor((bitis_s - acilma_s) / e.izgara_s))
        alarm = 0
        for _ in range(deneme):
            beyan = _SentetikBeyanlar(_poisson_anlari(r, hiz, bas_s, bitis_s))
            if e.tespit_gecikmesi(beyan) is not None:
                alarm += 1
    finally:
        evre.ALFA = eski
    oran = alarm / deneme
    se2 = 2.0 * math.sqrt(max(oran * (1.0 - oran), 1.0 / deneme) / deneme)
    return oran, se2, pencere


def main() -> int:
    # Varsayılan evre kafesi: ölçüm penceresi [50; 320) · açılma 150 s.
    bas_s, acilma_s, bitis_s = 50.0, 150.0, 320.0
    # Ağ genelinde saniye başına kopma beyanı — bilinmediği için geniş bir
    # aralık taranır (TARAMA EKSENİ, bir değer iddiası değil).
    hizlar = (0.1, 0.5, 2.0, 10.0)
    deneme = 4000            # 2·SE ≤ 0,016 — sonuç ölçeğine göre yeterli
    # Y10 ÖNCESİ kuralın pencere başına α'sı; yalnız karşılaştırma için.
    eski_pencere_alfa = 0.01
    print("=" * 88)
    print("M4 · TESPIT GECIKMESI — sentetik bos hipotezde yanlis alarm")
    print(f"  pencere [{bas_s}; {bitis_s}) · acilma {acilma_s} s · "
          f"{deneme} deneme / hucre · ALFA = {evre.ALFA} (aile duzeyi)")
    print("=" * 88)
    print(f"  {'hiz (beyan/s)':>14} {'kural':<12} {'pencere basina a':>17} "
          f"{'taranan':>8} {'yanlis alarm':>13} {'2SE':>7}")
    kapi_kirildi = False
    for i, hiz in enumerate(hizlar):
        _, _, pencere = _yanlis_alarm_orani(hiz, 1, evre.ALFA, 0,
                                            bas_s, acilma_s, bitis_s)
        for kural, aile in (("eski", eski_pencere_alfa * pencere),
                            ("bugunku", evre.ALFA)):
            oran, se2, pencere = _yanlis_alarm_orani(
                hiz, deneme, aile, 1000 + i, bas_s, acilma_s, bitis_s)
            print(f"  {hiz:>14.2f} {kural:<12} {aile / pencere:>17.3g} "
                  f"{pencere:>8} {oran:>13.3f} {se2:>7.3f}")
            if kural == "bugunku" and oran - se2 > evre.ALFA:
                kapi_kirildi = True
    print()
    print(f"  Hesap (bagimsiz pencere varsayimiyla, ust sinir): "
          f"1 - (1 - {eski_pencere_alfa})^170 = "
          f"{1.0 - (1.0 - eski_pencere_alfa) ** 170:.3f}")
    if kapi_kirildi:
        print(f"  🔴 KAPI KIRILDI: bugunku kuralin yanlis alarmi aile "
              f"hedefini (ALFA = {evre.ALFA}) asiyor.")
        return 1
    print(f"  🟢 KAPI GECTI: bugunku kuralin olculen yanlis alarmi aile "
          f"hedefinin (ALFA = {evre.ALFA}) ALTINDA, 2SE marjiyla.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
