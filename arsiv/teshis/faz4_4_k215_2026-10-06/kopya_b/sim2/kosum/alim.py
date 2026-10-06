"""
Alım — çerçevenin bir düğüme ulaşması ve bitmesi. `kosu.py`den taşındı.

🔒 26 Eylül 2026 (`v2/15` B3, K-179): davranış BİREBİR aynı — aynı çağrılar,
aynı sırayla; yalnız `kosu.py`nin 150 kod satırı kapanış ölçütü için ve B3'ün
kanal doluluk muhasebesi bu iki olayın başında çalıştığı için buraya alındı.
"""

from __future__ import annotations

from sim2.kanal.girisim import Iletim
from sim2.kosum import kontrol
from sim2.kosum.gonderim import alim_say
from sim2.kosum.teslim import onay_alindi, veri_alindi

__all__ = ["cerceve_geldi", "cerceve_bitti"]


def cerceve_geldi(kosu, n: int, iletim: Iletim, yuk) -> None:
    d = kosu.dugumler[n]
    if d.olu:
        return                                  # C1: telsiz kapalı
    t = kosu.olaylar.simdi
    d.mesgul_guncelle(t)                    # B3: durum değişmeden ÖNCE
    yeni, ezilen = d.alici.cerceve_geldi(iletim, t)
    alim_say(kosu, yeni)
    alim_say(kosu, ezilen)
    # 🔒 A3 güç kipi (K-174): önbelge kilitlendiyse ya da toplam enerji
    # ED eşiğini aştıysa geri çekilme donar (geometrik kipte `gonder`de).
    if d.guc_kipi and d.kanal_mesgul_mu(t):
        kosu.dondur(d, t)


def cerceve_bitti(kosu, n: int, iletim: Iletim, yuk) -> None:
    d = kosu.dugumler[n]
    if d.olu:
        return                                  # C1: telsiz kapalı
    t = kosu.olaylar.simdi
    d.mesgul_guncelle(t)                    # B3: durum değişmeden ÖNCE
    sonuc = d.alici.cerceve_bitti(iletim, t)
    alim_say(kosu, sonuc)
    if sonuc is not None and sonuc.sebep == "alim_red_per":
        d.phy_hata_say()                    # B3: kilitlendi, gövde çözülemedi
    if sonuc is None or not sonuc.basarili:
        return
    d.alim_kaydet(iletim.cerceve.bayt)
    tip, bilgi = yuk
    # 🔒 `v2/15` B1 — sürücü çerçeveyi raporlar, SONRA üst katman işler.
    kontrol.cerceve_duyuldu(kosu, d, iletim.gonderen, tip, bilgi, sonuc.guc_w)
    if tip == "beacon":
        d.beacon_isle(iletim.gonderen, bilgi, t)
    elif tip == "onay":
        onay_alindi(kosu, n, bilgi)
    elif tip == "veri":
        veri_alindi(kosu, d, iletim.gonderen, bilgi)
    else:
        kontrol.cerceve_alindi(kosu, d, iletim.gonderen, tip, bilgi)
