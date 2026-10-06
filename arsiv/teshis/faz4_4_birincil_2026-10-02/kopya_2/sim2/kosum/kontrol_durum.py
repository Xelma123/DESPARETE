"""
Kontrol düzlemi DURUMU — düğüm başına, davranışsız. K-112.

🔒 NEDEN AYRI DOSYA
===================
Davranış `kosum/kontrol.py`dedir ve `gonderim.gonder`i kullanır; `gonderim`
ise `dugum`u içe aktarır. Durum burada durmasaydı `dugum → kontrol →
gonderim → dugum` döngüsü doğardı. Bu dosya hiçbir `kosum/` modülünü içe
aktarmaz.

🔒 KONTROL DEFTERİ — korunum defterinin kontrol karşılığı
=========================================================
Kontrol çerçeveleri VERİ korunum defterine girmez (sözleşme K5): o defter
yalnız paketleri sayar ve mutabakatı kuyruklardaki paketlerle yapar. Ama
sessiz kayıp kontrol düzleminde de en zor bulunan hata sınıfıdır. Bu yüzden
ayrı ve kapalı bir defter tutulur:

    istenen = kuyruk_tasmasi + yayin_gonderilen + unicast_onaylanan
              + unicast_vazgecilen + kuyrukta + ucusta
    dinamik_istenen = dinamik_ates + bekleyen_uyandirma
    jitter_istenen  = jitter_ates + bekleyen_jitter

Tutmayan satır `gecerli=False` olur (`kosum/sonuc.py`).

🔒 ÖNCELİK — kontrol çerçevesi VERİDEN ÖNCE, ama uçuştaki MSDU'yu kesmez
=========================================================================
NS-2'nin MANET arayüz kuyruğu (`PriQueue`) yönlendirme paketlerine öncelik
verir ve bu, taban çizgisi karşılaştırmalarının fiilî geleneğidir. Ama
802.11 yeniden denemesi AYNI MSDU'dur: uçuştaki bir veri paketinin yeniden
denemeleri arasına kontrol çerçevesi giremez. Kural tek satır:
`sirada_mi`.
"""

from __future__ import annotations

from collections import deque

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.sayaclar import kume_uyeleri
from sim2.gozlem.kontrol import KONTROL_KANCALARI, KontrolIstegi

__all__ = ["KontrolDuzlemiHatasi", "UyandirmaTavaniAsildi", "DEFTER_ALANLARI",
           "KontrolDurumu"]


class KontrolDuzlemiHatasi(RuntimeError):
    """Kontrol düzlemi sözleşmesi koşu sırasında çiğnendi — koşu DURUR."""


class UyandirmaTavaniAsildi(KontrolDuzlemiHatasi):
    """Sözleşme kararı 2: bekleyen dinamik uyandırma tavanı aşıldı.

    🔒 Zamanlayıcı sessizce düşürülmez. Düşürülseydi protokol bir
    zaman aşımını hiç görmez ve ölçülen şey onun davranışı değil,
    simülatörün kestiği bir davranış olurdu.
    """


# 🔒 DEFTERİN ALANLARI SAYAÇ KÜTÜĞÜNDEN TÜRER (`v2/07` §18 Y1).
# Her alan kütükte `kontrol_<alan>` adıyla, `kume="kontrol_defteri"` olarak
# durur ve `KontrolDurumu.say` ikisini AYNI çağrıda artırır. İkinci bir ad
# listesi yok — alıcı zincirinin `ALIM_SONUCLARI` deseni. Böylece kontrol
# istatistikleri pencere ikizleriyle birlikte satırın `metrikler` bölümüne
# girer ve düğüm defteri ile sayaç ayrışamaz.
_SAYAC_ONEKI = "kontrol_"
dogrula(all(ad.startswith(_SAYAC_ONEKI)
            for ad in kume_uyeleri("kontrol_defteri")),
        "kontrol defteri sayacının adı `kontrol_` ile başlamalı")
DEFTER_ALANLARI: tuple[str, ...] = tuple(
    ad.removeprefix(_SAYAC_ONEKI) for ad in kume_uyeleri("kontrol_defteri"))


class KontrolDurumu:
    """Bir düğümün kontrol kuyruğu, uçuş durumu, uyandırmaları ve defteri."""

    __slots__ = ("etkin", "kosum_beaconi", "kuyruk", "kapasite", "ucustaki",
                 "ucus_no", "onay_bekleniyor", "gelen", "bekleyen_uyandirma",
                 "tepe_bekleyen", "bekleyen_jitter", "son_gorulen",
                 "defter", "bicim", "_sayaclar")

    def __init__(self, protokol, kapasite: int, sayaclar) -> None:
        var = tuple(hasattr(protokol, h) for h in KONTROL_KANCALARI)
        if any(var) and not all(var):
            eksik = [h for h, v in zip(KONTROL_KANCALARI, var) if not v]
            raise KontrolDuzlemiHatasi(
                f"kontrol kancaları HEPSİ-YA-HİÇ: eksik {eksik}. Kısmi bir "
                f"protokol gönderdiği mesajın cevabını sessizce yutardı.")
        dogrula(kapasite > 0, "kontrol kuyruğu kapasitesi pozitif olmalı")
        self.etkin = all(var)
        # 🔒 Y3 · R2 — koşum düzeyindeki beacon protokol başına kapatılabilir.
        # Yalnız kontrol düzlemini KULLANAN protokol kapatabilir: kancasız ve
        # beacon'sız bir protokolün komşu tablosu kalıcı olarak boş kalırdı ve
        # ölçülen şey protokolün kararı değil, körlüğü olurdu.
        self.kosum_beaconi = bool(getattr(protokol, "kosum_beaconi", True))
        if not self.kosum_beaconi and not self.etkin:
            raise KontrolDuzlemiHatasi(
                "kontrol düzlemi taşımayan protokol koşum beaconunu "
                "kapatamaz: komşu tablosu kalıcı olarak boş kalırdı")
        self.bekleyen_jitter = 0
        self.kuyruk: deque[KontrolIstegi] = deque()
        self.kapasite = kapasite
        self.ucustaki: KontrolIstegi | None = None
        self.ucus_no = 0
        self.onay_bekleniyor = False
        self.gelen: list = []
        self.bekleyen_uyandirma = 0
        self.tepe_bekleyen = 0
        # Unicast tekrar bastırma: komşu başına EN SON teslim edilen numara —
        # veri yolunun `Dugum._son_ucus` kuralının aynısı.
        self.son_gorulen: dict[int, int] = {}
        self.defter: dict[str, int] = {a: 0 for a in DEFTER_ALANLARI}
        # Mesaj biçimi dökümü (`v2/07` §18 Y1): kip → biçim adı → [çerçeve,
        # bayt, airtime_s]. HELLO ↔ TC ↔ RREQ yükünü ayırmak içindir; toplamı
        # `kontrol_iletim` ile denetlenir. `pencere` kipi sayaç ikizleriyle
        # AYNI tanımı kullanır: pencere başladıktan sonraki artış.
        self.bicim: dict[str, dict[str, list]] = {"tum": {}, "pencere": {}}
        self._sayaclar = sayaclar

    @property
    def bos_mu(self) -> bool:
        return not self.kuyruk

    def niyet_al(self, niyetler: tuple) -> None:
        """`Karar.niyetler` — yalnız kontrol kancalarını taşıyan protokolden."""
        if niyetler and not self.etkin:
            raise KontrolDuzlemiHatasi(
                "kontrol kancaları olmayan protokol `Karar.niyetler` "
                "dolduramaz — cevabı alacak kanca yok")
        self.gelen.extend(niyetler)

    def sirada_mi(self, veri_ucusta: bool) -> bool:
        """DCF sırası kontrolde mi? Uçuştaki kontrol her zaman; kuyruktaki
        kontrol, uçuşta VERİ yoksa."""
        return self.ucustaki is not None or (not veri_ucusta
                                             and bool(self.kuyruk))

    def say(self, alan: str) -> None:
        """Düğüm defteri ve sayaç kütüğü — AYNI çağrıda (`v2/07` §18 Y1)."""
        self.defter[alan] += 1
        self._sayaclar.artir(_SAYAC_ONEKI + alan)

    def bicim_say(self, ad: str, bayt: int, airtime_s: float,
                  pencerede: bool) -> None:
        """Bir kontrol iletimini mesaj biçimi dökümüne yazar."""
        for kip in (("tum", "pencere") if pencerede else ("tum",)):
            t = self.bicim[kip].setdefault(ad, [0, 0, 0.0])
            t[0] += 1
            t[1] += bayt
            t[2] += airtime_s

    def kuyruga_al(self, istek: KontrolIstegi) -> bool:
        self.say("istenen")
        if len(self.kuyruk) >= self.kapasite:
            self.say("kuyruk_tasmasi")
            return False
        self.kuyruk.append(istek)
        return True

    def ucusa_al(self) -> KontrolIstegi:
        dogrula(self.ucustaki is None and bool(self.kuyruk),
                "uçuşta kontrol varken ya da kuyruk boşken uçuşa alınamaz")
        self.ucustaki = self.kuyruk.popleft()
        self.ucus_no += 1
        return self.ucustaki

    def ucustan_indir(self, sonuc: str) -> None:
        dogrula(self.ucustaki is not None, "uçuşta kontrol çerçevesi yok")
        dogrula(sonuc in ("yayin_gonderilen", "unicast_onaylanan",
                          "unicast_vazgecilen"), f"bilinmeyen sonuç {sonuc}")
        self.say(sonuc)
        self.ucustaki = None
        self.onay_bekleniyor = False

    def uyandirma_istendi(self, tavan: int, kimlik: int, t_s: float) -> None:
        self.say("dinamik_istenen")
        self.bekleyen_uyandirma += 1
        self.tepe_bekleyen = max(self.tepe_bekleyen, self.bekleyen_uyandirma)
        if self.bekleyen_uyandirma > tavan:
            raise UyandirmaTavaniAsildi(
                f"düğüm {kimlik}: t={t_s!r} anında bekleyen dinamik uyandırma "
                f"{self.bekleyen_uyandirma} > tavan {tavan}. Koşu durduruldu "
                f"(sözleşme kararı 2 — sessiz düşürme yok).")

    def uyandirma_ateslendi(self) -> None:
        dogrula(self.bekleyen_uyandirma > 0, "bekleyen uyandırma yokken ateş")
        self.bekleyen_uyandirma -= 1
        self.say("dinamik_ates")

    def jitter_istendi(self) -> None:
        """Titreşimli mesaj beklemeye alındı (Y3 · R4) — henüz KUYRUKTA DEĞİL."""
        self.say("jitter_istenen")
        self.bekleyen_jitter += 1

    def jitter_atesledi(self) -> None:
        dogrula(self.bekleyen_jitter > 0, "bekleyen titreşim yokken ateş")
        self.bekleyen_jitter -= 1
        self.say("jitter_ates")

    def korunum(self) -> dict[str, object]:
        d = self.defter
        sag = (d["kuyruk_tasmasi"] + d["yayin_gonderilen"]
               + d["unicast_onaylanan"] + d["unicast_vazgecilen"]
               + len(self.kuyruk) + (1 if self.ucustaki is not None else 0))
        return {
            "mesaj_tamam": d["istenen"] == sag,
            "uyandirma_tamam": (d["dinamik_istenen"]
                                == d["dinamik_ates"] + self.bekleyen_uyandirma),
            "jitter_tamam": (d["jitter_istenen"]
                             == d["jitter_ates"] + self.bekleyen_jitter),
            "bekleyen_jitter": self.bekleyen_jitter,
            "kuyrukta": len(self.kuyruk),
            "ucusta": 1 if self.ucustaki is not None else 0,
            "bekleyen_uyandirma": self.bekleyen_uyandirma,
            "tepe_bekleyen": self.tepe_bekleyen,
        }
