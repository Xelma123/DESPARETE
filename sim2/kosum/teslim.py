"""
Teslim — paketin EL DEĞİŞTİRMESİ. Korunum defterinin en zor yeri.

🔴 EL DEĞİŞTİRME ONAYA DEĞİL, ALIMA BAĞLI
=========================================
Paket, alıcı çerçeveyi BAŞARIYLA ÇÖZDÜĞÜ anda el değiştirir — onay
geldiğinde değil. Gerçek 802.11'de de öyledir ve *"veri alındı, onay
kayboldu"* durumunun tek doğru modeli budur:

    alıcı çözdü      → paket alıcının kuyruğunda, defterde el değişti
    onay kayboldu    → gönderen bunu BİLMEZ ve yeniden gönderir
    tekrar geldi     → alıcı bastırır, ama YİNE onaylar
    gönderen vazgeçti→ paketi DÜŞÜREMEZ, çünkü kaybolmadı

El değiştirme onaya bağlansaydı, onayı kaybolan her paket defterde
"kaybolmuş" sayılır ve aynı paket alıcının kuyruğunda da durur — korunum
denklemi çift sayardı ve fark, onay kaybı oranıyla birlikte büyürdü.

🔴 TEKRAR BASTIRMA UÇUŞ NUMARASIYLA, PAKET KİMLİĞİYLE DEĞİL
===========================================================
Anahtar `(gönderen, uçuş_no)`. Uçuş numarası gönderende her ATLAMA için
artar, yeniden denemelerde SABİT kalır. Paket kimliğiyle bastırılsaydı, bir
yönlendirme döngüsünde aynı paketin aynı komşuya meşru ikinci ziyareti
sessizce yutulur ve paket defterde asılı kalırdı. Numara komşu başına tek
bir sayı olarak tutulur — kimlik kümesi tutmak koşu boyunca milyonlarca
giriş biriktirirdi.
"""

from __future__ import annotations

from sim2.cekirdek.degismezler import dogrula
from sim2.kanal.girisim import Iletim
from sim2.kosum import kontrol
from sim2.kosum.dugum import Dugum
from sim2.kosum.gonderim import gonder

__all__ = ["veri_alindi", "onay_alindi"]


def veri_alindi(kosu, d: Dugum, gonderen: int, bilgi) -> None:
    """Veri çerçevesi çözüldü. Bize adreslendiyse el değiştirir ve onaylanır."""
    paket, hedef, ucus_no = bilgi
    if hedef != d.kimlik:
        return                          # bize adreslenmemiş; onay da yok
    # 🔒 PSR'nin payı: adreslenen alıcı gövdeyi hatasız çözdü. Tekrar
    # denetiminden ÖNCE — yeniden denemenin başarılı alımı da sayılır.
    kosu.kur.sayaclar.artir("veri_alim_hedefte")
    if not d.tekrar_mi(gonderen, ucus_no):
        d.gorduk(gonderen, ucus_no)
        kosu.dugumler[gonderen].devret(ucus_no)
        _yerlestir(kosu, d, paket)
    _onay_zamanla(kosu, d, gonderen, ucus_no)


def _yerlestir(kosu, d: Dugum, paket) -> None:
    """Paket el değiştirdi: teslim mi, kuyruğa mı, düşer mi.

    🔒 Üç yolun ÜÇÜ DE deftere yazılır. Birini atlamak denklemi ya da
    mutabakatı kırar; ikisi de her koşuda otomatik denetlenir.
    """
    if paket.hedef == d.kimlik:
        kosu.kur.korunum.teslim_et()
        kosu.kur.sayaclar.artir("teslim_paket")
        kosu.kur.paket_defteri.teslim_edildi(paket.kimlik, kosu.olaylar.simdi)
        return
    kosu.kur.korunum.ucustan_kuyruga()
    kosu.kur.sayaclar.artir("aktarilan_paket")
    # TTL AKTARMADA düşer: bu düğüm paketi bir kez daha ilerletecekse önce
    # hakkını harcar. Kalan 1 ise ilerletemez — 0 TTL ile bir paket kuyruğa
    # konsaydı `Paket.ttl_azalt()` değişmezi patlardı.
    if paket.ttl_kalan <= 1:
        d.dus("ttl", nereden="kuyruk")
        return
    if d.kuyruga_al(paket.ttl_azalt(), uretim=False):
        kosu.cekismeye_basla(d)


def _onay_zamanla(kosu, d: Dugum, gonderen: int, ucus_no: int) -> None:
    """SIFS sonra onay. 🔒 TEKRARA DA onay verilir.

    Verilmeseydi, onayı bir kez kaybolan bir paket gönderen vazgeçene kadar
    yeniden denenir ve sonunda `iletim_basarisiz` sayılırdı — oysa alıcı onu
    çoktan almıştı. Ölçülen PSR olduğundan kötü, PDR ile PSR arasındaki
    tutarlılık ise bozuk çıkardı.
    """
    cerceve = kosu.kur.onay_cercevesi
    onay = Iletim(d.kimlik, cerceve,
                  kosu.olaylar.simdi + kosu.kur.zamanlar.sifs_s,
                  kosu.kur.kanal.yayilim.verici_gucu_w)
    s = kosu.kur.sayaclar
    s.artir("kontrol_cerceve")
    s.ekle("kontrol_bayt", cerceve.bayt)
    s.ekle("kontrol_airtime_s", cerceve.sure_s)
    kosu.olaylar.ekle(onay.baslangic_s, gonder, kosu, d.kimlik, onay,
                      ("onay", (gonderen, ucus_no)))


def onay_alindi(kosu, n: int, bilgi) -> None:
    """Onay `n` düğümünde çözüldü — `n` göndericinin kendisiyse gönderen serbest.

    🔴 YALNIZ GÖNDERİCİNİN KENDİSİ — 11 Eylül 2026 (`v2/07` §18 Y2, K-115).
    Eskiden onayı çözen HERHANGİ bir düğüm göndereni serbest bırakıyordu.
    Göndericiye fiziksel olarak alamayacağı bir "başarılı" bilgisi veriliyor ve
    karıştırmanın gönderici tarafındaki etkisi gizleniyordu: karıştırıcı açıkken
    hayalet kredi statik kolda 2,5–3,3 katına çıkıyordu (K-114 §4.2). Kural
    artık kontrol düzleminin onay kuralıyla aynı.

    🔒 Uçuş numarası eşleşmiyorsa bu BAYAT bir onaydır (gönderen çoktan başka
    bir atlamaya geçmiş) ve yok sayılır. Eşleşiyorsa paketin el değiştirmiş
    olması ZORUNLUDUR: onay ancak alıcı çerçeveyi çözdüyse gönderilir.
    """
    hedef, ucus_no = bilgi
    if n != hedef:
        return                          # seyirci çözdü; gönderen bunu bilemez
    d = kosu.dugumler[hedef]
    if not d.onay_bekleniyor or ucus_no != d.ucus_no:
        return
    dogrula(d.devredildi, "onay geldi ama paket el değiştirmemiş — "
                          "alım ile onayın modeli ayrışmış")
    komsu = d.ucus_hedefi             # 🔒 Y1 · K-151 — uçuştan indirmeden
    deneme = d.dcf.deneme             # ve DCF sayacı sıfırlanmadan önce
    d.arf_bildir(komsu, True)         # A4 (K-177)
    d.onay_bekle(False)
    d.ucustan_indir()
    d.dcf.onay_geldi()
    d.iletim_sonucu("onay")
    kosu.kur.sayaclar.artir("mac_gonderim_basarili")
    kontrol.iletim_sonucu(kosu, d, komsu, True, deneme, "veri")
    kosu.cekismeye_basla(d)
