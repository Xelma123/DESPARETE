"""4.0 kanıtı: elle `Kurulum` kuran iki araç bugünkü kodla kurulabiliyor mu?

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/faz4_2026-09-26/kirik_araclar.py
"""
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))


def dene(ad, fn):
    try:
        print(f"{ad:<16} KURULDU · {fn()}")
    except Exception as hata:                         # noqa: BLE001
        print(f"{ad:<16} KURULAMADI · {type(hata).__name__}: {hata}")


if __name__ == "__main__":
    from kalibrasyon.iki_cift import kos as iki_cift_kos
    from kalibrasyon.li_replikasyonu import _kos as li_kos
    dene("li_replikasyonu", lambda: li_kos(3, 250.0, 1000, 50.0, bitis_s=1.0))
    dene("iki_cift", lambda: iki_cift_kos(1, 1000, 1000.0, yuk_hz=50.0,
                                          bitis_s=1.0))
