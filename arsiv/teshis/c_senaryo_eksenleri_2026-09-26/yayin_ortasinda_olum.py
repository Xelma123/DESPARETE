"""C1 kusurunun yeniden üretimi (ajan, 26 Eylül 2026).

Bir İHA kendi VERİ çerçevesi havadayken ölürse: `dugum_oldur` paketi
`dugum_kaybi` ile uçuştan düşürür ve `_ucustaki`yi temizler. Ama çerçeve
havada kalır; alıcı onu sonunda çözer ve `devret`i ölü göndericiye çağırır.
Uçuşta paket olmadığı için değişmez patlar. İki kip de sınanır:
yayılım gecikmesi kapalı ve açık (A5 — alıcıya varış çerçeve sonundan d/c
sonra).

Ölüm, ilk veri çerçevesinin ortasına zamanlanır (`Dugum.gonderim_ekle`
sarılarak). Kod değiştirilmez.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/c_senaryo_eksenleri_2026-09-26/yayin_ortasinda_olum.py
"""
import inspect
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "tests2"))

from test_kosum import EnYakinKimlik, _defter, _konfig  # noqa: E402
from sim2.kosum import kayip  # noqa: E402
from sim2.kosum.dugum import Dugum  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

IKI_ARGUMAN = len(inspect.signature(Dugum.gonderim_ekle).parameters) == 3


def dene(**ek) -> str:
    kur = kurulum_yap(_konfig("statik-yok", 1000, 3.0, **ek))
    kosu = Kosu(kur, lambda i: EnYakinKimlik())
    asil = Dugum.gonderim_ekle
    kurban: dict = {}

    def izle(self, *args):
        asil(self, *args)
        sure = args[-1]
        t = kosu.olaylar.simdi
        if not kurban and t > 1.0 and self.ucustaki is not None \
                and self.dcf.durum != "bos":
            kurban.update(n=self.kimlik, bas=t, bitis=t + sure)
            kosu.olaylar.ekle(t + sure / 2, kayip.dugum_oldur, kosu,
                              self.kimlik)
    Dugum.gonderim_ekle = izle
    try:
        kosu.kostur()
    except Exception as hata:                     # noqa: BLE001
        return f"ÇÖKTÜ · {type(hata).__name__}: {hata}"
    finally:
        Dugum.gonderim_ekle = asil
    d = kosu.dugumler[kurban["n"]]
    k, _ = _defter(kur, kosu)
    return (f"çökmedi · düğüm {kurban['n']} çerçeve "
            f"[{kurban['bas']:.6f}, {kurban['bitis']:.6f}] s · ölüm "
            f"{d.olum_s:.6f} s · gecerli={k['gecerli']} · dugum_kaybi="
            f"{k['dusen']['dugum_kaybi']}")


if __name__ == "__main__":
    print("gecikme kapalı :", dene())
    print("gecikme açık   :", dene(yayilim_gecikmesi=True))
