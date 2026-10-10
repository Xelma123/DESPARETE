"""
Gönderim — bir çerçevenin havaya çıkışı ve akıbeti.

🔒 NEDEN AYRI DOSYA
===================
`kosu.py` olay döngüsüdür: olayı alır, durumu ilerletir. Bir çerçevenin
havaya çıkması ise ayrı bir sorumluluk — kimler duyar, kimin geri çekilmesi
donar, hangi sayaçlar artar. İkisi tek dosyada olduğunda dosya 214 koda
satırına çıkmıştı ve olay döngüsü, kendi doğurduğu ayrıntının içinde
kayboluyordu.

🔒 SERBEST FONKSİYON, METOT DEĞİL
=================================
Buradaki fonksiyonlar `Kosu`yu ilk argüman olarak alır. Bir karışım sınıfı
(mixin) da işi görürdü ama yapıyı GİZLERDİ: `Kosu`nun yüzeyine bakan biri,
metotların nereden geldiğini göremezdi. Açık bir argüman bunu görünür yapar.
"""

from __future__ import annotations

from sim2.cekirdek.degismezler import dogrula
from sim2.kanal.cerceve import cerceve_kur
from sim2.kanal.girisim import Iletim
from sim2.kosum.dugum import Dugum
from sim2.yapilandirma.konfig import HIZLAR_BPS

__all__ = ["alim_say", "beacon_cercevesi", "beacon_gonder", "gonder",
           "veri_gonder", "veri_cercevesi_kur", "iletime_basla", "vazgec"]


def veri_cercevesi_kur(kur, dugumler) -> tuple:
    """Y2 · K-151 — koşunun veri çerçevesi: `(çerçeve, başlık baytı, süresi)`.

    🔒 Protokol sınıfı isteğe bağlı `veri_baslik_bayt` ile her veri paketine
    eklediği yönlendirme başlığını bildirir (yoksa 0). Kurulum protokolden
    BAĞIMSIZ kalır (`kurulum_hash` değişmez); başlıklı çerçeve koşuda türer.
    Başlığın süresi iki çerçevenin FARKIDIR — bit hızı aritmetiği yalnız
    `kanal/cerceve.py`de yapılır. Başlıksız protokolde kurulumun çerçeve
    NESNESİ döner: sonuç birebir aynıdır.
    """
    basliklar = {int(getattr(d.protokol, "veri_baslik_bayt", 0))
                 for d in dugumler}
    dogrula(len(basliklar) == 1, "düğümlerin veri başlığı farklı")
    baslik = basliklar.pop()
    dogrula(baslik >= 0, "veri başlığı negatif olamaz")
    k = kur.konfig
    if k.hiz_uyarlamasi:
        # A4 (K-177): koşunun EN UZUN veri çerçevesi (en düşük hız) — iletim
        # defterinin budaması bunu kapsamalı; asıl çerçeve gönderimde seçilir.
        yuk = cerceve_kur(k, "veri", hiz_bps=HIZLAR_BPS[0])
        cerceve = (cerceve_kur(k, "veri", bayt=k.paket_bayt + baslik,
                               hiz_bps=HIZLAR_BPS[0]) if baslik else yuk)
        return cerceve, baslik, cerceve.sure_s - yuk.sure_s
    if not baslik:
        return kur.veri_cercevesi, 0, 0.0
    cerceve = cerceve_kur(k, "veri", bayt=k.paket_bayt + baslik)
    return cerceve, baslik, cerceve.sure_s - kur.veri_cercevesi.sure_s


def _hizda_veri_cerceveleri(kosu, hiz: float) -> tuple:
    """A4 (K-177): verilen hızda `(başlıklı çerçeve, yük çerçevesi)` —
    önbellekli (saf memo)."""
    anahtar = ("veri", hiz)
    c = kosu._cerceve_onbellegi.get(anahtar)
    if c is None:
        k = kosu.kur.konfig
        yuk = cerceve_kur(k, "veri", hiz_bps=hiz)
        baslikli = (cerceve_kur(k, "veri", bayt=k.paket_bayt
                                + kosu.veri_baslik_bayt, hiz_bps=hiz)
                    if kosu.veri_baslik_bayt else yuk)
        c = kosu._cerceve_onbellegi[anahtar] = (baslikli, yuk)
    return c


def alim_say(kosu, sonuc) -> None:
    """Bir alım denemesinin sonucunu sayar.

    🔒 `Σ sebep = toplam deneme` kapanış ölçütünün geçtiği TEK yer burasıdır;
    her sonuç üreticisi (önbelge, gövde, yarım çift) buraya iner.
    """
    if sonuc is None:
        return
    kosu.kur.sayaclar.artir(sonuc.sebep)
    if sonuc.yakalama:
        kosu.kur.sayaclar.artir("alim_yakalama")


def beacon_cercevesi(kosu, ek_bayt: int):
    """Beacon çerçevesi — protokolün taşıdığı yük KADAR uzar.

    🔒 `kosu.py`den buraya TAŞINDI (K-112): davranış birebir aynı,
    yalnız `kosu.py`nin 150 kod satırı kapanış ölçütü için.

    🔴 ESKİDEN UZAMIYORDU ve bu bir bedel kaçağıydı (K-111 EK-2).
    Ölçüldü: 250 baytlık bir yükte çerçeve 320 µs yerine **1 320 µs**
    sürmeliydi (4,12 kat). Yük yalnız sayaçta ödeniyor, kanalda
    ödenmiyordu.

    🔒 `ek_bayt == 0` yolu kurulumdaki çerçeveyi AYNEN döndürür: bugünkü
    üç protokol gerçeklemesinin üçü de boş yük taşıdığı için düzeltme
    ölçülmüş hiçbir sayıyı değiştirmez — parmak izi birebir aynı kalır.
    Düzeltmenin bugün yapılmasının sebebi de budur: bir protokol yük
    taşımaya başladıktan sonra yapılsaydı o güne kadarki her sayı
    bayatlardı.

    ⚠️ Boyuta göre önbelleklenir: beacon koşu başına ~14 000 kez
    gönderiliyor ve her seferinde `Cerceve` kurmak ölçüme değil hıza
    mal olurdu. Önbellek SAF bir memo'dur — sonucu değiştiremez.
    """
    if ek_bayt == 0:
        return kosu.kur.beacon_cercevesi
    cerceve = kosu._cerceve_onbellegi.get(ek_bayt)
    if cerceve is None:
        cerceve = cerceve_kur(kosu.kur.konfig, "beacon",
                              bayt=kosu.kur.konfig.beacon_bayt + ek_bayt)
        kosu._cerceve_onbellegi[ek_bayt] = cerceve
    return cerceve


def beacon_gonder(kosu, d: Dugum, t: float) -> None:
    """Beacon'ı havaya verir — çekişme kararı `kosu._beacon`da verilmiştir.

    🔒 `kosu.py`den buraya TAŞINDI (23 Eylül 2026, K-151 kapanışı): davranış
    BİREBİR aynı — aynı çağrılar, aynı sırayla; yalnız `kosu.py`nin 150 kod
    satırı kapanış ölçütü için. Çerçeveyi havaya vermek bu dosyanın işidir.
    🔒 TEK KAYNAK: bedel çerçevenin boyutundan okunur. `Dugum` ayrıca
    saymaz — yoksa yük çift faturalanırdı.
    """
    yuk, ek_bayt = d.beacon_yuku(t)
    cerceve = beacon_cercevesi(kosu, ek_bayt)
    s = kosu.kur.sayaclar
    s.artir("beacon_gonderilen")
    s.artir("kontrol_cerceve")
    s.ekle("kontrol_bayt", cerceve.bayt)
    s.ekle("kontrol_airtime_s", cerceve.sure_s)
    gonder(kosu, d.kimlik, Iletim(d.kimlik, cerceve, t,
                                  kosu.kur.kanal.yayilim.verici_gucu_w),
           ("beacon", yuk))


def gonder(kosu, n: int, iletim: Iletim, yuk) -> None:
    """Çerçeveyi havaya verir: duyanlara olay, gönderene bitiş.

    🔴 Duyma kümesi GEOMETRİKTİR (girişim menzili) — gerekçesi `kurulum.py`de.
    Aynı küme hem alım denemesini hem geri çekilme donmasını belirler; ikisi
    ayrı kümeler olsaydı bir düğüm duymadığı bir çerçeve yüzünden donabilir
    ya da duyduğu bir çerçeveye rağmen sayaç işletebilirdi.
    """
    t = kosu.olaylar.simdi
    if kosu.dugumler[n].olu:
        return                  # C1: ölümden önce zamanlanmış onay vb. — susar
    kosu.dugumler[n].mesgul_guncelle(t)          # B3: durum değişmeden önce
    kosu.dugumler[n].gonderim_ekle(t, iletim.cerceve.sure_s)    # C3
    kosu.kur.kanal.ortam.ekle(iletim)
    alim_say(kosu, kosu.dugumler[n].alici.gonderime_basla(t))
    bitis = t + iletim.cerceve.sure_s
    for m in range(kosu.kur.dugum_sayisi):
        d = kosu.dugumler[m]
        if m == n or d.olu or not d.duyar_mi(n, t):      # C1: ölü duymaz
            continue
        # 🔒 A5 (K-175): varış d/c sonra; anahtar kapalıyken gecikme 0,0.
        g = d.gecikme_s(n, t)
        kosu.olaylar.ekle(t + g, kosu._cerceve_geldi, m, iletim, yuk)
        kosu.olaylar.ekle(bitis + g, kosu._cerceve_bitti, m, iletim, yuk)
        # 🔒 A3 güç kipi (K-174): donma alım kararından SONRA, `_cerceve_geldi`de
        # — önbelge kilitlendiyse ya da enerji ED eşiğini aştıysa.
        if not d.guc_kipi:
            if g > 0.0:                 # A5: donma VARIŞ anında
                kosu.olaylar.ekle(t + g, kosu.dondur, d, t + g)
            else:
                kosu.dondur(d, t)
    kosu.olaylar.ekle(bitis, kosu._iletim_bitti, n, iletim, yuk)


def veri_gonder(kosu, d: Dugum, paket, hedef: int) -> None:
    """Uçuştaki paketi bir kez gönderir — ilk deneme ya da yeniden deneme.

    🔒 Yük, paketin YANINDA uçuş numarasını taşır: alıcı tekrarları bununla
    bastırır ve gönderen onayı bununla eşler. Paket kimliğiyle eşlenseydi bir
    döngüde aynı paketin meşru ikinci ziyareti tekrar sanılırdı.
    """
    cerceve, yuk = kosu.veri_cercevesi, kosu.kur.veri_cercevesi
    baslik_s = kosu.veri_baslik_sure_s
    if d.hiz_denetcisi is not None:                      # A4 (K-177)
        cerceve, yuk = _hizda_veri_cerceveleri(kosu,
                                               d.hiz_denetcisi.hiz(hedef))
        baslik_s = cerceve.sure_s - yuk.sure_s
    iletim = Iletim(d.kimlik, cerceve, kosu.olaylar.simdi,
                    kosu.kur.kanal.yayilim.verici_gucu_w)
    s = kosu.kur.sayaclar
    s.artir("mac_deneme")
    # 🔒 Y2 · K-151 — veri düzlemi yalnız YÜKÜ sayar; protokolün başlığı
    # yönlendirme ek yüküdür ve ayrı sayılır. Başlıksız protokolde çerçeve
    # ve sayılan değerler eskisiyle BİREBİR aynıdır.
    s.ekle("veri_bayt", yuk.bayt)
    s.ekle("veri_airtime_s", yuk.sure_s)
    if kosu.veri_baslik_bayt:
        s.ekle("veri_baslik_bayt", kosu.veri_baslik_bayt)
        s.ekle("veri_baslik_airtime_s", baslik_s)
    d.dcf.gonderime_basladi()
    d.dcf.onay_bekle()
    d.onay_bekle(True)
    d.iletim_kaydet(iletim, hedef, None)
    gonder(kosu, d.kimlik, iletim, ("veri", (paket, hedef, d.ucus_no)))


def iletime_basla(kosu, d: Dugum) -> None:
    """Geri çekilme bitti — sıradaki çerçeve havaya çıkıyor.

    🔒 PROTOKOLE ATLAMA BAŞINA BİR KEZ SORULUR. Uçuşta bir paket varsa bu bir
    YENİDEN DENEMEDİR ve aynı komşuya gider; her denemede yeniden sorulsaydı
    MAC katmanı sessizce bir yönlendirme kararı verir ve ölçülen şey
    protokolün kararı olmaktan çıkardı.

    🔒 "BEKLET" KUYRUĞU TIKAMAZ — K-131 (denetim B1).
    Protokol kuyruk başındaki paket için *"beklet"* derse o paket tampona
    geçer ve **sıradaki paket sorulur**; döngü ilerletilebilir bir paket
    bulana ya da kuyruk boşalana kadar sürer. Paket kuyruk başında
    bekletilseydi tek bir rotasız paket düğümün BÜTÜN kuyruğunu tıkardı
    (baş-hat tıkanması) — gerçek AODV'de olmayan ve yalnız reaktif aileyi
    vuran bir ceza.

    ⚠️ `hedef_yok` dalı döngüye GİRMEZ ve bu bilinçli: bugünkü davranış
    (düşür · DCF'den vazgeç · çekişmeye yeniden başla) korunuyor. Değişseydi
    `beklet` döndürmeyen bugünkü dört protokolün satırları oynardı.
    """
    if d.ucustaki is not None:
        veri_gonder(kosu, d, d.ucustaki, d.ucus_hedefi)
        return
    while not d.kuyruk.bos_mu:
        # 🔒 D-23 · K-231 — eşin sonraki atlaması kopya anında verildi; eş
        # protokole yeniden SORULMAZ.
        zorunlu = d.kopya_sonraki_al(d.kuyruk.bak())
        if zorunlu is not None:
            kosu.kur.korunum.kuyruktan_al()
            kosu.kur.sayaclar.artir("mac_gonderim_istegi")
            d.ucusa_al(d.kuyruk.al(), zorunlu)
            veri_gonder(kosu, d, d.ucustaki, zorunlu)
            return
        karar = d.sonraki_atlama(d.kuyruk.bak(), kosu.olaylar.simdi)
        if karar.beklet:
            d.beklemeye_al(d.kuyruk.al(), kosu.olaylar.simdi, kosu.olaylar)
            continue
        if karar.sonraki is None:
            d.kuyruk.al()
            # 🔒 DÜŞME SEBEBİ BEYANA BAKAR — 16 Eylül 2026 (`04` K-134).
            # `gozlem/karar.py` bunu baştan söylüyordu (*"protokol rotayı
            # geçersiz ilan ederse paket düşer ve deftere `rota_gecersiz`
            # sebebiyle geçer"*) ama DAL KODDA YOKTU. Ölçüldü: 320 beyan,
            # o sebeple **0** düşüş; hepsi `hedef_yok` yazıyordu.
            # 🔒 AODV'de ayrım gerçektir: rota HİÇ bulunamadı (keşif
            # başarısız) ile rota VARDI ve koptu (RFC 3561 §6.11 — ara düğüm
            # RERR gönderir ve paketi DÜŞÜRÜR) ayrı şeylerdir.
            # 🔒 `politika` — protokol paketi BİLEREK taşımıyor (K-171);
            # `Karar` ikisinin birlikte verilmesine izin vermez.
            sebep = ("politika" if karar.beyanlar("politika")
                     else "rota_gecersiz" if karar.beyanlar("rota_gecersiz")
                     else "hedef_yok")
            d.dus(sebep, nereden="kuyruk")
            d.dcf.vazgec()
            kosu.cekismeye_basla(d)
            return
        kosu.kur.korunum.kuyruktan_al()
        kosu.kur.sayaclar.artir("mac_gonderim_istegi")
        d.ucusa_al(d.kuyruk.al(), karar.sonraki)
        for komsu in karar.kopyalar:                     # D-23 · K-231
            no = kosu.kopya_no.get(d.ucustaki.kimlik, 0) + 1
            kosu.kopya_no[d.ucustaki.kimlik] = no
            d.kopya_kuyruga_al(d.ucustaki, komsu, no)
        veri_gonder(kosu, d, d.ucustaki, karar.sonraki)
        return
    # 🔒 Kuyruğun tamamı tampona geçti: gönderilecek veri YOK. DCF'den
    # vazgeçilir; paketleri tekrar çekişmeye sokacak olan şey tamponun
    # yeniden sorulmasıdır (`kosum/kontrol.py`) ya da süre tavanıdır.
    d.dcf.vazgec()
    kosu.cekismeye_basla(d)


def vazgec(kosu, d: Dugum) -> None:
    """Yeniden deneme hakkı bitti.

    🔴 Paket EL DEĞİŞTİRDİYSE düşürülmez: kaybolmadı, alıcıya geçti ve
    defterde artık uçuşta değil. Düşürülseydi defter çift sayardı — üretilen
    bir paket hem "düşen"e hem alıcının "kuyrukta"sına yazılırdı.
    """
    devredildi = d.devredildi
    d.ucustan_indir()
    if not devredildi:
        d.dus("iletim_basarisiz", nereden="ucus")
    kosu.cekismeye_basla(d)
