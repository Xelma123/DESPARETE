"""
Sonuç satırı — bir koşunun bıraktığı TEK kayıt, ve onu diske yazan kalem.

🔴 BU DOSYADA TEK BİR SÖZLÜK LİTERALİ YOK
=========================================
Eski simülatörde sonuç sözlüğü **elle yazılmış 25 sayaç ifadesiydi** ve aynı
ifadeler anlık görüntü fonksiyonunda bir kez daha duruyordu. İki liste
sessizce ayrıştı. Buradaki kural yapısaldır: her bölüm kendi kayıt
defterinden TÜRETİLİR — sayaçlar `cekirdek/sayaclar.py`den, konfig
`Konfig.sozluk()`ten, metrikler `olcum/metrikler.py`den. Elle yazılan tek
şey bölüm ADLARIdır ve onlar da tek bir demettedir.

🔴 SATIR BAŞINA `fsync`
=======================
Uzun bir tarama saatler sürer ve ortasında kesilebilir (elektrik, kullanıcı,
işletim sistemi). `fsync` olmadan işletim sisteminin arabelleğindeki son
satırlar YARIM kalır ve `.jsonl` dosyası okunamaz hâle gelir — üstelik hata
dosyanın SONUNDA olduğu için, hatayı görene kadar okunmuş satırlar geçerli
sanılır. Satır başına `fsync` bu maliyeti (koşu başına milisaniyeler) öder.

🔒 GEÇERSİZ SATIR SİLİNMEZ, İŞARETLENİR
=======================================
Korunum ya da mutabakat tutmayan bir koşu dosyaya YAZILIR ve
`gecerli=False` taşır. Yazmamak, bozuk koşuların varlığını gizlemek olurdu;
analiz onları dışlar ama kaç tane olduğunu SAYAR.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

from sim2.cekirdek import kimlik as K
from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import akis_listesi_hash
from sim2.cekirdek.sayaclar import kume_uyeleri, sayac_semasi_hash
from sim2.kosum.kontrol import kontrol_korunumu, kontrol_teshisi
from sim2.kosum.kurulum import Kurulum
from sim2.yapilandirma.kapsam import kapsam_bolumu
from sim2.yapilandirma.kokenler import kova_sayimi
from sim2.olcum.metrikler import metrik_sozlugu

__all__ = ["BOLUMLER", "TEDAVI_ALANLARI", "korunum_bolumu",
           "sonuc_satiri", "SatirYazici"]

# 🔒 Satırın bölümleri. Elle yazılan TEK liste bu; içerikleri türetilir.
BOLUMLER: tuple[str, ...] = (
    "kimlik", "ortam", "konfig", "kapsam", "metrikler", "korunum",
    "ham", "teshis",
)

# 🔴 `kapsam` ve `ham` 8 Eylül 2026'da EKLENDİ — ikisi de bir BOŞLUĞU kapatır.
#
# `kapsam`: kapsam sınırları yalnız şartnamedeydi. Bir `.jsonl` satırı aylar
# sonra açıldığında hangi sınırlarla üretildiği SATIRDAN OKUNAMIYORDU; bir
# sayının yanında kendi sınırı yoksa o sayı olduğundan geniş okunur.
#
# `ham`: `PaketDefteri.ham_sozluk()` VARDI ama hiçbir yerden çağrılmıyordu,
# yani satıra HİÇ yazılmıyordu. `analiz/` katmanı `sim2/`den içe aktarma
# yapamaz, dolayısıyla yüzdelik ve evre metriklerinin ikinci bir gerçeklemesi
# orada olacak — ve iki gerçeklemenin sessizce ayrışmasını engelleyen tek şey
# ham listenin satırda BULUNMASIDIR. `metrikler.py` başlığı bunu bir taahhüt
# olarak yazıyordu; taahhüt bugüne kadar yerine getirilmemişti.
#
# 🔴 BEDELİ ÖLÇÜLDÜ VE BEYAN EDİLİR (8 Eylül 2026, tam uzunluk statik koşu):
#     satır 0,52 MB · bunun 511 KB'ı (%98) `ham`
#     çekirdek deney (360 koşu) ≈ 187 MB · tam matris (2 160) ≈ 1,1 GB
# Üretici: `python kalibrasyon/adim9_kapanis.py 1` → `ciktilar2/*.jsonl`
#
# 🔒 `ham`i KAPATILABİLİR YAPMADIM ve bu bilinçli: kapatılabilir olsaydı iki
# koşum modu doğardı ve birinde metrikler yeniden üretilebilir, diğerinde
# DEĞİL olurdu. Hangi modda koşulduğu bir gün unutulur. Boyut bir sorun
# hâline gelirse çözüm sıkıştırmadır, ATLAMA değil.

# 🔒 İki kolun MEŞRU olarak ayrılabileceği alanlar. `kurulum_hash` bunları
# dışarıda bırakır: başka bir alan farklıysa o ikisi aynı deneyin iki kolu
# değildir ve karşılaştırılamazlar.
TEDAVI_ALANLARI: tuple[str, ...] = ("kol", "senaryo", "tohum", "not_",
                                    "trafik_deseni", "tehdit_senaryosu")


def _kimlik_bolumu(kur: Kurulum, protokol_adi: str) -> dict[str, Any]:
    konfig = kur.konfig
    sozluk = konfig.sozluk()
    arac = K.arac_hash()
    kurulum = K.kurulum_hash(sozluk, TEDAVI_ALANLARI)
    evren = K.evren_hash(_evren(kur))
    sayac_sema = sayac_semasi_hash()
    akis_listesi = akis_listesi_hash()
    return dict(zip(
        ("kosu_kimligi", "calisma_kimligi", "zaman_damgasi_utc", "arac_hash",
         "kurulum_hash", "evren_hash", "sayac_semasi_hash",
         "akis_listesi_hash", "kol", "protokol", "senaryo", "tohum", "not_"),
        (K.kosu_kimligi(arac=arac, kurulum=kurulum, kol=konfig.kol,
                        tohum=konfig.tohum, sayac_semasi=sayac_sema,
                        akis_listesi=akis_listesi),
         K.calisma_kimligi(), K.zaman_damgasi_utc(), arac, kurulum, evren,
         sayac_sema, akis_listesi, konfig.kol, protokol_adi, konfig.senaryo,
         konfig.tohum, konfig.not_)))


def _evren(kur: Kurulum) -> tuple[tuple[int, float, int, int], ...]:
    """Ölçüm penceresindeki paket evreni — `(kimlik, doğum, kaynak, hedef)`.

    🔒 Kaynak/hedef defterden DEĞİL, akış tanımından okunur: defter yalnız
    akış kimliğini tutar ve o kimlik, üretecin akış tablosunda kaynak-hedef
    çiftinin TEK doğru kaynağıdır.
    """
    cikti = []
    for paket, akis_kimligi, dogum_s in kur.paket_defteri.dogumlar(True):
        akis = kur.trafik.akis(akis_kimligi)
        cikti.append((paket, dogum_s, akis.kaynak, akis.hedef))
    return tuple(cikti)


def korunum_bolumu(kur: Kurulum, dugumler: Iterable[Any]) -> dict[str, Any]:
    """🔴 DENKLEM ve MUTABAKAT — iki AYRI kapı, ikisi de yazılır.

    Denklem defterin kendi geçişlerinin tutarlılığını ölçer; mutabakat
    defterin gerçeği doğru modelleyip modellemediğini. Biri tutup öteki
    tutmayabilir ve o durumda satır GEÇERSİZDİR.
    """
    # 🔒 ROTA BEKLEME TAMPONU DA "KUYRUKTA" SAYILIR — K-131 (denetim B1).
    # Tampon defterde ayrı bir havuz DEĞİLDİR: paket arayüz kuyruğu ile
    # tampon arasında yer değiştirir, durum değiştirmez. Buraya eklenmeseydi
    # bekleyen her paket defterde "kuyrukta" görünür ama gerçekte hiçbir
    # kuyrukta olmazdı — ve MUTABAKAT tam olarak bunu yakalamak için var
    # (`cekirdek/korunum.py`: denklem tutar ama defterin modeli ayrışır).
    dugumler = tuple(dugumler)
    kuyrukta = (sum(len(k) for k in kur.kuyruklar)
                + sum(len(d.bekleyenler) for d in dugumler))
    # 🔴 EL DEĞİŞTİRMİŞ PAKET UÇUŞTA SAYILMAZ. `_ucustaki` gönderende, onay
    # gelene ya da zaman aşımına uğrayana kadar durur; ama paket alıcı onu
    # çözdüğü ANDA defterde el değiştirmiştir. Koşu, bu ikisinin arasında
    # biterse gönderende bayat bir `_ucustaki` kalır. Onu "uçuşta" saymak
    # mutabakatı sahte olarak kırardı — 30 tohumluk kapıda 1005'te ölçüldü
    # (`ucus_farki = -1`) ve mutabakatın kendisi bunu YAKALADI.
    ucusta = sum(1 for d in dugumler
                 if d.ucustaki is not None and not d.devredildi)
    rapor = dict(kur.korunum.kontrol())
    rapor.update(kur.korunum.mutabakat(kuyrukta, ucusta))
    # 🔴 ÜÇÜNCÜ KAPI — İLETİM SONUCU KAPALI KÜMESİ (8 Eylül 2026).
    # Her MAC denemesi ya onaylanır ya onaysız kalır; onaysızlık da ya
    # verinin ulaşmamasından ya onayın kaybolmasındandır. Üçünün toplamı
    # deneme sayısına EŞİT olmak zorundadır. Eşit değilse bir deneme
    # hiçbir kovaya girmeden kaybolmuştur — korunum denklemini KIRMADAN.
    # Ölçüldü: kimlik tam tutuyor (fark 0).
    sayac = kur.sayaclar.disa_ver()
    uyeler = kume_uyeleri("iletim_sonucu")
    toplam = sum(float(sayac.get(ad) or 0.0) for ad in uyeler)
    deneme = float(sayac.get("mac_deneme") or 0.0)
    # 🔴 KOŞU SONUNDA SONUCU BEKLEYEN DENEME — 11 Eylül 2026 (K-115).
    # Koşu `kosu_bitis_s`te kesilir ve bitişten sonraya düşen olaylar
    # işlenmez. Son anlarda başlayan bir veri denemesinin onay penceresi
    # bitişi aşarsa deneme SAYILMIŞ ama sonucu YAZILMAMIŞ olur. Onay bekleme
    # bayrağı iletim başında kalkar, kredi ya da zaman aşımında iner; onay
    # beklenirken düğümün sürümü değişmediği için koşu içindeki pencere olayı
    # mutlaka işlenir. Yani bayrağı koşu sonunda kalkık düğüm sayısı TAM
    # OLARAK sonucu yazılmamış deneme sayısıdır ve orta yerde kaybolmuş bir
    # sonucu örtemez. Ölçüldü: Y2'den sonra `d-bagimsiz-surekli-yuklu`
    # vakasında fark 1, bekleyen düğüm 1.
    askida = sum(1 for d in dugumler if d.onay_bekleniyor)
    rapor["iletim_sonucu_toplam"] = toplam
    rapor["iletim_sonucu_askida"] = askida
    rapor["mac_deneme"] = deneme
    rapor["iletim_sonucu_tamam"] = toplam + askida == deneme
    rapor["gecerli"] = bool(rapor["korunum_tamam"]
                            and rapor["mutabakat_tamam"]
                            and rapor["iletim_sonucu_tamam"])
    # 🔒 DÖRDÜNCÜ KAPI — KONTROL DEFTERİ (K-112). Yalnız kontrol düzlemi
    # KULLANILDIYSA satıra girer; kullanmayan protokolde bölüm birebir aynı.
    kk = kontrol_korunumu(dugumler)
    if kk is not None:
        rapor.update(kk)
        rapor["gecerli"] = bool(rapor["gecerli"] and kk["kontrol_mesaj_tamam"]
                                and kk["kontrol_uyandirma_tamam"]
                                and kk["kontrol_jitter_tamam"])
    return rapor


def _teshis_bolumu(kur: Kurulum, dugumler: Iterable[Any]) -> dict[str, Any]:
    """Protokol teşhisleri + ikizsiz sayaç raporu. KARARA GİRMEZ, rapora."""
    rapor: dict[str, Any] = dict()
    rapor["dugum"] = tuple(d.teshis() for d in dugumler)
    rapor["ikizsiz"] = dict(kur.sayaclar.ikizsiz_rapor())
    rapor["bekleyen_olay"] = kur.olaylar.bekleyen_olay_sayisi()
    rapor["cizelgelenen_dogum"] = kur.trafik.toplam_dogum
    rapor["penceredeki_dogum"] = kur.trafik.penceredeki_dogum()
    rapor["pencere_kimlik_araligi"] = kur.paket_defteri.pencere_kimlik_araligi()
    # 🔴 SÖNÜMLEME ÖNBELLEĞİ — tavanın yettiğini HER koşuda göster.
    # Tavan sonucu değiştiremez (saf memo) ama yetmezse bedeli sessiz bir CPU
    # kaybıdır: ıskalama oranı yükselir ve kimse fark etmez. Çalışma noktası
    # değiştiğinde (yol kaybı üsteli, hızlar) sönümleme filtresi uzuyor ve
    # çalışma kümesi büyüyor — o yüzden bu satır rapora giriyor.
    rapor["sonumleme_onbellegi"] = dict(kur.kanal.sonumleme.onbellek_raporu())
    # 🔴 PARAMETRE KÖKEN BORCU — her koşu kendi borcunu BEYAN eder.
    # `SINANMAMIS` sayısı, o koşunun kaç parametresinin gerekçesiz olduğunu
    # söyler. Sıfırlanmadan ön-kayıt mühürlenemez; satıra yazılması, borcun
    # zamanla nasıl eridiğinin (ya da erimediğinin) kaydını tutar.
    rapor["koken_kovalari"] = dict(kova_sayimi())
    kt = kontrol_teshisi(dugumler)
    if kt is not None:
        rapor["kontrol_duzlemi"] = kt
    # Yere toplamada düşüşlerin geçide mesafesi (`v2/07` §18 Y4).
    if kur.kayip_yeri is not None:
        rapor["kayip_yeri"] = kur.kayip_yeri.rapor()
    return rapor


def sonuc_satiri(kur: Kurulum, dugumler: Iterable[Any],
                 protokol_adi: str) -> dict[str, Any]:
    """Bir koşunun sonuç satırı. Bölümler `BOLUMLER`den, içerik defterlerden."""
    dugumler = tuple(dugumler)
    uretici = (
        lambda: _kimlik_bolumu(kur, protokol_adi),
        K.ortam_ozeti,
        kur.konfig.sozluk,
        lambda: kapsam_bolumu(kur.konfig),
        # 🔒 Açılma anı SATIRA konfigden taşınır, `olcum/` onu aramaz:
        # ölçüm defterleri konfigürasyona bağımlı olmamalı.
        lambda: metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                               kur.rota_defteri,
                               acilma_s=kur.konfig.karistirici_baslangic_s),
        lambda: korunum_bolumu(kur, dugumler),
        kur.paket_defteri.ham_sozluk,
        lambda: _teshis_bolumu(kur, dugumler),
    )
    dogrula(len(uretici) == len(BOLUMLER),
            "bölüm adı ile üreticisi ayrışmış — biri eklenmiş, öteki değil")
    return dict(zip(BOLUMLER, (f() for f in uretici)))


class SatirYazici:
    """`.jsonl` yazıcısı — satır başına `flush` + `fsync`.

    🔒 `append` kipi: bir dosyaya iki kez yazmak satırları ÇOĞALTIR ve
    çoğaltılmış satırlar anlamlılığı uydurur (`cekirdek/kimlik.py`deki
    41 katlık ölçüme bak). Kopyayı bulmak analiz katmanının işidir ve
    `kosu_kimligi` bunun için vardır — ama yazıcı kopyayı gizlemez.
    """

    __slots__ = ("yol", "_dosya")

    def __init__(self, yol: str | Path) -> None:
        self.yol = Path(yol)
        self.yol.parent.mkdir(parents=True, exist_ok=True)
        self._dosya = None

    def __enter__(self) -> "SatirYazici":
        self._dosya = open(self.yol, "a", encoding="utf-8", newline="\n")
        return self

    def __exit__(self, *_) -> None:
        if self._dosya is not None:
            self._dosya.close()
            self._dosya = None

    def yaz(self, satir: dict[str, Any]) -> None:
        dogrula(self._dosya is not None,
                "yazıcı açılmadan yazılamaz — `with SatirYazici(...) as y`")
        self._dosya.write(json.dumps(satir, ensure_ascii=False,
                                     default=_donustur) + "\n")
        self._dosya.flush()
        os.fsync(self._dosya.fileno())


def _donustur(nesne: Any) -> Any:
    """JSON'un tanımadığı tipler. 🔴 Sessiz `str()` YOK.

    Bilinmeyen bir tipi metne çevirmek, sonuç satırına ne yazıldığının
    bilinmemesi demektir; şema sessizce kayar. Demet listeye çevrilir
    (JSON'da karşılığı odur), gerisi HATA verir.
    """
    if isinstance(nesne, tuple):
        return list(nesne)
    if isinstance(nesne, (set, frozenset)):
        return sorted(nesne)
    raise TypeError(
        f"sonuç satırına JSON'a çevrilemeyen bir tip girdi: "
        f"{type(nesne).__name__}. Şemaya girecek her değer açıkça "
        f"dönüştürülmelidir.")
