"""
Topoloji — düğüm konumları ve geometrik komşuluk.

🔴 BU MODÜL SENARYO KURULUMUDUR, PROTOKOL BİLGİSİ DEĞİLDİR.
--------------------------------------------------------------
Buradaki komşuluk tablosu ve bağlantılı bileşen hesabı, deneyi KURMAK için
kullanılır: kaynak–hedef çiftleri seçilirken. Hiçbir protokol bu modüle
erişemez.

Bir protokol komşularını yalnızca ALDIĞI BEACON'lardan bilir ve karıştırma
altında beacon da kaybolur — komşu görünmez olur. Menzil tablosunu protokole
vermek, karıştırmanın en temel etkisini iptal ederdi.
(05-GOZLEM-PENCERESI.md, §A4)

BASİTLEŞTİRME — rapora girer
-----------------------------
Düğümler kare bir alana düzgün rastgele yerleştirilir. Gerçek bir İHA sürüsü
formasyon tutar; düzgün dağılım bir basitleştirmedir. Sabit topoloji kararının
gerekçesi 04-NEDEN-BOYLE.md K-008'de.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .config import Konfig
from .rng import Akislar


@dataclass(frozen=True)
class Topoloji:
    konumlar: tuple[tuple[float, float], ...]
    iletim_menzili_m: float
    girisim_menzili_m: float

    # ------------------------------------------------------------------ kur
    @staticmethod
    def uret(kon: Konfig, akislar: Akislar) -> "Topoloji":
        """Konumları `yerlesim` akışından çeker.

        Akış ayrı olduğu için, bir protokolün kaç rastgele sayı çektiği
        topolojiyi ETKİLEMEZ. Aynı tohum → aynı topoloji, hangi kol
        koşarsa koşsun.

        BAĞLANTI KOŞULLAMASI (K-017)
        -----------------------------
        `baglanti_kosullamasi=True` iken, bağlı bir yerleşim çıkana kadar
        yeniden çekilir. Bu bir ÖNYARGIDIR ve büyüklüğü ölçülmüştür.

        🔴 SAYILAR 19 AĞUSTOS 2026'DA DÜZELTİLDİ (B-08, K-039).
        Üretici: `python dogrulama/kurulum_kalibrasyonu.py --a`

            doğal bağlantı oranı    %82,93   (200 000 bağımsız çekim)
            ortalama deneme         1,2058   (gerçek akışta en kötü 4)
            ortalama derece kayması −%0,364 ± 0,026

        ⚠️ Önceki hâli "%0,9" yazıyordu ve İŞARETİ TERSTİ. Koşullama
        dereceyi düşürüyor, yükseltmiyor. Nitel sonuç değişmiyor:
        |kayma| < %1, yani gürültü mertebesinde. Referans olarak koşulsuz
        ortalama derecenin analitik kapalı formu kullanıldı (7,44258;
        ölçülen 7,44242 — beşinci haneye kadar uyuşuyor).

        Neden kabul edilebilir: incelenen evren "bağlı 40 düğümlük rastgele
        yerleşimler"dir ve bu açıkça yazılır. Kopuk bir ağda yönlendirme
        sorusu zaten anlamsızdır — ilginç soru, BAĞLI bir ağa karıştırıcı
        girdiğinde ne olduğudur.

        Neden koşullamadan yapılamaz: ölçüldü — 30 düğüm/250 m'de en büyük
        bileşen tohumlar arasında 10 ile 30 arasında geziniyordu. Tohum
        varyansı protokol farkını gömerdi.
        """
        r = akislar["yerlesim"]
        for deneme in range(1, kon.topoloji_max_deneme + 1):
            konumlar = tuple(
                (r.uniform(0.0, kon.alan_m), r.uniform(0.0, kon.alan_m))
                for _ in range(kon.dugum_sayisi)
            )
            topo = Topoloji(
                konumlar=konumlar,
                iletim_menzili_m=kon.iletim_menzili_m,
                girisim_menzili_m=kon.girisim_menzili_m,
            )
            if not kon.baglanti_kosullamasi:
                return topo
            if len(topo.bagli_bilesenler()) == 1:
                return topo
        raise RuntimeError(
            f"{kon.topoloji_max_deneme} denemede bağlı topoloji üretilemedi "
            f"(n={kon.dugum_sayisi}, menzil={kon.iletim_menzili_m} m, "
            f"alan={kon.alan_m} m). Yoğunluk çok düşük — parametreler "
            f"yeniden ölçülmeli, sessizce kopuk ağla devam edilmemeli."
        )

    # --------------------------------------------------------------- geometri
    @property
    def dugum_sayisi(self) -> int:
        return len(self.konumlar)

    def mesafe(self, i: int, j: int) -> float:
        (x1, y1), (x2, y2) = self.konumlar[i], self.konumlar[j]
        return math.hypot(x1 - x2, y1 - y2)

    def iletim_menzilinde_mi(self, i: int, j: int) -> bool:
        return i != j and self.mesafe(i, j) <= self.iletim_menzili_m

    def girisim_menzilinde_mi(self, i: int, j: int) -> bool:
        """Girişim menzili iletim menzilinden GENİŞTİR.

        Bu fark gizli terminal etkisinin kaynağıdır ve Li replikasyonundaki
        1/7 sayısı bu olmadan çıkmaz. (06-ON-KAYIT.md, K4)
        """
        return i != j and self.mesafe(i, j) <= self.girisim_menzili_m

    def geometrik_komsular(self, i: int) -> tuple[int, ...]:
        """⚠️ YALNIZCA KURULUM İÇİN. Protokol bunu göremez."""
        return tuple(j for j in range(self.dugum_sayisi)
                     if self.iletim_menzilinde_mi(i, j))

    # ------------------------------------------------------- bağlı bileşenler
    def bagli_bilesenler(self) -> list[list[int]]:
        """İletim menziline göre bağlı bileşenler, büyükten küçüğe."""
        gorulen = [False] * self.dugum_sayisi
        bilesenler: list[list[int]] = []
        for basla in range(self.dugum_sayisi):
            if gorulen[basla]:
                continue
            yigin, bilesen = [basla], []
            gorulen[basla] = True
            while yigin:
                d = yigin.pop()
                bilesen.append(d)
                for k in self.geometrik_komsular(d):
                    if not gorulen[k]:
                        gorulen[k] = True
                        yigin.append(k)
            bilesenler.append(sorted(bilesen))
        bilesenler.sort(key=len, reverse=True)
        return bilesenler

    def en_buyuk_bilesen(self) -> list[int]:
        return self.bagli_bilesenler()[0]

    def ulasilabilir_ciftler(self, dugumler: list[int] | None = None
                             ) -> list[tuple[int, int]]:
        """Aynı bileşende olan (kaynak, hedef) çiftleri.

        NEDEN ÖNEMLİ — Ulaşılamayan bir hedefe giden paketin kaybı,
        protokolün değil TOPOLOJİNİN suçudur. Bu çiftler dışlanmazsa
        karıştırıcısız kontrol kolunda bile teslim oranı %100'ün altında
        kalır ve "etkinin sıfır olması gereken kol" anlamını yitirir.
        (06-ON-KAYIT.md, SENARYOLAR)
        """
        havuz = set(dugumler) if dugumler is not None else None
        ciftler: list[tuple[int, int]] = []
        for bilesen in self.bagli_bilesenler():
            if len(bilesen) < 2:
                continue
            uyeler = [d for d in bilesen if havuz is None or d in havuz]
            for a in uyeler:
                for b in uyeler:
                    if a != b:
                        ciftler.append((a, b))
        return ciftler

    # --------------------------------------------------------------- teşhis
    def ozet(self) -> dict[str, float | int]:
        """Sonuç satırına yazılır: hangi topolojide ölçtüğümüzün kaydı."""
        bilesenler = self.bagli_bilesenler()
        dereceler = [len(self.geometrik_komsular(i))
                     for i in range(self.dugum_sayisi)]
        return {
            "dugum_sayisi": self.dugum_sayisi,
            "bilesen_sayisi": len(bilesenler),
            "en_buyuk_bilesen": len(bilesenler[0]),
            "yalniz_dugum": sum(1 for b in bilesenler if len(b) == 1),
            "ortalama_derece": sum(dereceler) / len(dereceler),
            "en_kucuk_derece": min(dereceler),
            "en_buyuk_derece": max(dereceler),
        }
