"""
Kontrol düzlemi DAVRANIŞI — niyetlerin uygulanması. K-112.

Sözleşme: `v2/13-KONTROL-DUZLEMI.md`. Durum: `kosum/kontrol_durum.py`.

🔒 AYNI KANAL, AYNI MAC, AYNI KAYIP (sözleşme kararı 3)
=======================================================
Kontrol çerçevesi ayrı bir yoldan havaya ÇIKMAZ. Veri çerçevesiyle aynı DCF
geri çekilmesine girer (aynı düğüm alt akışı), aynı `gonderim.gonder` ile
havaya verilir, aynı alıcı zincirinden (önbelge · gövde PER · yakalama ·
yarım çift) geçer. UNICAST kontrol onaylanır ve `yeniden_deneme_siniri`ne
kadar yeniden denenir; YAYIN onaylanmaz — 802.11'in kuralı.

🔒 TESLİM YALNIZ BAŞARIDA (sözleşme kararı 4)
=============================================
`kontrol_alindi` alıcı zinciri `alim_basarili` dediğinde ve çerçeve o
düğüme ait olduğunda çağrılır. Yayında her başarılı alıcı AYRI bir teslim
üretir. Başkasına adresli unicast çerçeve fiziksel olarak çözülse de
teslim EDİLMEZ (`baskasina_adresli`); unicast tekrarı onaylanır ama ikinci
kez teslim edilmez (`tekrar_bastirilan`).

🔴 ONAY, YALNIZ GÖNDERENİN KENDİSİ ÇÖZDÜĞÜNDE SAYILIR
====================================================
Kontrol onayı `n == gönderen` şartıyla işlenir. Veri yolunun onayı
(`teslim.onay_alindi`) K-112'de bu şartı aramıyordu. Etkisi K-114 §4.2'de
ölçüldü ve öğrenci kararıyla 11 Eylül 2026'da aynı kurala getirildi (Y2).

🔒 BELİRLENİMCİLİK
==================
Periyodik zamanlayıcı fazı düğüm başına `beacon_faz` ALT AKIŞINDAN çekilir
(`akislar.dugum`): kurulumdaki beacon fazları o akışın ANA dizisinden
çekildiği için hiçbiri kaymaz. Kontrol düzlemi kullanmayan protokolde bu
alt akış hiç yaratılmaz, hiçbir olay eklenmez — sonuç birebir aynı kalır.
"""

from __future__ import annotations

import math

from sim2.gozlem.kontrol import (KontrolIstegi, Uyandirma,  # noqa: F401
                                 niyetleri_dogrula)
from sim2.cekirdek.rng import normal_cekimi
from sim2.kanal.cerceve import cerceve_kur
from sim2.kanal.girisim import Iletim
from sim2.kosum.gonderim import gonder
from sim2.kosum.kontrol_durum import DEFTER_ALANLARI, KontrolDuzlemiHatasi

__all__ = ["BEKLEYEN_UYANDIRMA_TAVANI", "sirada_mi", "zamanlayicilari_kur",
           "gelenleri_uygula", "iletime_basla", "iletim_bitti",
           "onay_zaman_asimi", "cerceve_alindi", "iletim_basarisiz",
           "iletim_sonucu", "cerceve_duyuldu", "kontrol_teshisi",
           "kontrol_korunumu"]

# 🔒 Düğüm başına bekleyen DİNAMİK uyandırma tavanı — köken defterinde.
# Aşılırsa koşu durur; tamamlanan hiçbir koşunun sonucunu değiştiremez.
BEKLEYEN_UYANDIRMA_TAVANI: int = 256


def _gozlem(kosu, d):
    """Kanca için gözlem — 16 Eylül 2026, K-131 (denetim B4).

    🔒 Eskiden kancalara `(dugum, …, saat_s)` geçiliyordu; `Gozlem` ikisini de
    taşıdığı için HİÇBİR BİLGİ EKSİLMEDİ, donanım ölçümleri eklendi. Yüzey
    büyümedi (`05` §5) — değişen tek şey, pencerenin artık tek bir yerde
    değil her kancada sunulması.

    ⚠️ `paket=None`: bu anlarda elde taşınan bir paket yoktur ve `Gozlem`
    onu zaten isteğe bağlı tutuyor.
    """
    return d.gozlem(kosu.olaylar.simdi, None)


def _uygula(kosu, d, niyetler) -> None:
    """Bir kancanın döndürdüğü niyetleri SIRAYLA uygular.

    🔒 KANCALAR BEYAN DA DÖNDÜREBİLİR — 16 Eylül 2026 (`04` K-134).
    `beyan_izinli=True`: protokol kopmayı ÖĞRENDİĞİ anda söyleyebilsin diye.
    Öncesinde beyanın tek kanalı veri gönderme kararıydı ve kuyruğu boş bir
    düğüm hiçbir şey bildiremezdi — ölçülen sonucu, `algilama_duyarliligi`nin
    proaktif aileyi sistematik olarak düşük göstermesiydi.
    """
    niyetleri_dogrula(niyetler, beyan_izinli=True)
    k, t = d.kontrol, kosu.olaylar.simdi
    kuyruga_girdi = False
    for niyet in niyetler:
        if isinstance(niyet, KontrolIstegi):
            h = niyet.hedef
            if h is not None and not (0 <= h < kosu.kur.dugum_sayisi
                                      and h != d.kimlik):
                raise KontrolDuzlemiHatasi(
                    f"düğüm {d.kimlik}: geçersiz unicast hedefi {h}")
            # 🔒 Y3 · R4 — titreşim kuyruğa GİRMEYİ geciktirir. Mesaj o ana
            # kadar deftere `istenen` yazılmaz; `jitter_istenen`de bekler ve
            # kapalı denklem onu görünür tutar.
            if niyet.jitter_s > 0.0:
                k.jitter_istendi()
                kosu.olaylar.ekle(
                    t + _titresim(kosu, d.kimlik, niyet.jitter_s),
                    _jitter_doldu, kosu, d.kimlik, niyet)
                continue
            kuyruga_girdi |= k.kuyruga_al(niyet)
            continue
        if not isinstance(niyet, Uyandirma):
            # 🔒 Geriye yalnız `Beyan` kalır ve bu GÜVENCEDİR, tahmin değil:
            # `niyetleri_dogrula` kapalı bir küme uygular. Tip burada İÇE
            # AKTARILMIYOR — `kosum/` onu görmesi gereken katman değil.
            d.beyan_isle(niyet, t)
            continue
        # 🔒 Alt sınır bir MAC slotu: daha kısa bir zamanlayıcı MAC'in
        # çözemeyeceği bir şey ister ve aynı anda sonsuz döngüye kapı açar.
        # Titreşim bu sınırın ÜSTÜNE eklenir, altını oymaz.
        if niyet.gecikme_s < kosu.kur.zamanlar.slot_s:
            raise KontrolDuzlemiHatasi(
                f"düğüm {d.kimlik}: uyandırma gecikmesi {niyet.gecikme_s!r} "
                f"< bir slot ({kosu.kur.zamanlar.slot_s!r})")
        gecikme = niyet.gecikme_s
        if niyet.jitter_s > 0.0:
            gecikme += _titresim(kosu, d.kimlik, niyet.jitter_s)
        k.uyandirma_istendi(BEKLEYEN_UYANDIRMA_TAVANI, d.kimlik, t)
        kosu.olaylar.ekle(t + gecikme, _uyandir, kosu, d.kimlik,
                          niyet.etiket)
    if kuyruga_girdi:
        kosu.cekismeye_basla(d)


def _tamponu_yeniden_sor(kosu, d) -> None:
    """Rota bekleyen paketleri yeniden sorulmak üzere kuyruğa döker (K-131).

    🔒 YALNIZ `uyandi`DAN SONRA — ve bu bir ÖLÇÜMLE daraltıldı (16 Eylül
    2026, `04` K-135).
    ======================================================================
    İlk kural *"`kontrol_alindi` · `uyandi` · `iletim_basarisiz` sonrası"*
    idi: üçü de dışarıdan bir olay taşıyor, yani rota bilgisi değişmiş
    olabilir. Gerekçe makuldü ve YANLIŞTI — ilk gerçek AODV koşumunda
    ölçüldü:

        1 598 paket  →  **146 678 tampon girişi**

    Sebep: AODV her RREQ selini duyar. Her alınan kontrol mesajı tamponun
    tamamını kuyruğa döküyor, her paket yeniden soruluyor, rota hâlâ yok ve
    hepsi tampona geri giriyordu. Yani kural, tamponu **kontrol trafiği
    hızında dönen bir yoklama döngüsüne** çevirmişti. Bedeli yalnız sayaç
    değildi: her tur DCF'yi yeniden çekişmeye sokup vazgeçiriyordu.

    🔒 Yeni kural tektir ve protokole aittir: **yeniden sorulmak isteyen
    protokol bir `Uyandirma` döndürür.** Sözleşmenin zaten istediği disiplin
    budur (`13` §03.5) ve simülatör "rota bulundu mu" diye TAHMİN ETMEZ —
    bilen taraf protokoldür.

    🔴 `Beyan("rota_kuruldu")`ya BAĞLANMADI, oysa anlamı tam oydu: `Beyan`
    *"YALNIZ ÖLÇÜME GİDER, simülatörün davranışını değiştirmez"* diye
    sözleşmelidir (`gozlem/karar.py`). Ölçüm kanalını bir eyleme bağlamak o
    sözleşmeyi kırardı ve beyan etmeyen bir protokol sessizce farklı
    davranırdı.

    ⚠️ Kontrol kancası taşımayan protokolde bu fonksiyon hiç çağrılmaz; onu
    yalnız süre tavanı kurtarır ve bu, `Karar.beklet`in belgesinde yazılıdır.
    """
    if d.bekleyenler and d.tamponu_kuyruga_dok():
        kosu.cekismeye_basla(d)


def _titresim(kosu, n: int, jitter_s: float) -> float:
    """🔒 `U(0, jitter_s)` — `protokol_kesif`in DÜĞÜM ALT AKIŞINDAN (R4).

    Alt akış ZORUNLU: tek akışta çok mesaj gönderen düğüm ötekilerin
    dizisini kaydırır ve düğümler arası sessiz bir kuplaj doğar
    (`cekirdek/rng.py`). Titreşim kullanılmayan koşuda bu akıştan HİÇ çekim
    yapılmaz; bugünkü satırlar birebir aynı kalır.
    """
    return kosu.kur.akislar.dugum("protokol_kesif", n).uniform(0.0, jitter_s)


def _jitter_doldu(kosu, n: int, istek) -> None:
    """Titreşim doldu: mesaj ŞİMDİ kuyruğa girer ve deftere yazılır."""
    d = kosu.dugumler[n]
    d.kontrol.jitter_atesledi()
    if d.kontrol.kuyruga_al(istek):
        kosu.cekismeye_basla(d)


def iletim_basarisiz(kosu, d, hedef: int | None, tur: str) -> None:
    """MAC bir unicast çerçeveden VAZGEÇTİ — protokole haber ver (R3).

    🔒 Kontrol düzlemi taşımayan protokolde hiçbir şey yapmaz; o protokolün
    satırları birebir aynı kalır. Çağrı SAYILIR: `basarisiz_bildirim`.
    """
    if not d.kontrol.etkin:
        return
    d.kontrol.say("basarisiz_bildirim")
    # 🔒 Yeniden sorma YOK (K-135): bağ kopması bir rota KAZANDIRMAZ,
    # kaybettirir. Buradan sorulsaydı paketler boşuna tura girerdi.
    _uygula(kosu, d, d.protokol.iletim_basarisiz(
        _gozlem(kosu, d), hedef, tur))


def iletim_sonucu(kosu, d, hedef: int | None, basarili: bool, deneme: int,
                  tur: str) -> None:
    """Y1 · K-151 — bir unicast çerçevenin sonucunu isteyen protokole bildirir.

    🔒 `deneme` DCF'nin bu çerçeve için yaptığı iletim sayısıdır ve DCF
    sayacı SIFIRLANMADAN önce okunmuş olmalıdır; protokole ilk denemeden
    sonraki yeniden iletim sayısı gider (`deneme - 1`).
    🔒 Kontrol düzleminden BAĞIMSIZDIR: kontrol kancası taşımayan protokol de
    bu bildirimi isteyebilir. Taşımayanda hiçbir şey yapılmaz.
    """
    if not d.sonuc_kancasi or hedef is None:
        return
    kosu.kur.sayaclar.artir("sonuc_bildirimi")
    donen = d.protokol.iletim_sonucu(_gozlem(kosu, d), hedef, basarili,
                                     max(0, deneme - 1), tur)
    if donen:
        raise KontrolDuzlemiHatasi(
            "`iletim_sonucu` niyet döndüremez — yalnız protokolün kendi "
            f"geçmişine girer; dönen: {donen!r}")


def cerceve_duyuldu(kosu, d, gonderen: int, tip: str, bilgi,
                    guc_w: float) -> None:
    """`v2/15` B1 · B2 — çözülen çerçeveyi isteyen protokole bildirir.

    🔒 RSSI = alıcının kilitlendiği güç + N(0, σ²), tamsayı dBm. Hata
    DURUMSUZ hash çekimidir (`kanal_karar` alanı, `rssi` anahtarı — yeni
    alan açılmaz, eski çekimler kaymaz): aynı tohumda aynı çerçevenin
    RSSI'ı protokolden bağımsız aynıdır. Alım kararına GİRMEZ.
    🔒 Taşımayan protokolde hiçbir şey yapılmaz.
    """
    if not d.duyma_kancasi:
        return
    if tip == "veri":
        paket, hedef, _ = bilgi
        gorunum = d.paket_gorunumu(paket)
    else:
        gorunum = None
        if tip in ("onay", "konay"):
            hedef = bilgi[0]
        elif tip == "kontrol":
            istek = bilgi[0]
            hedef = None if istek.yayin_mi else istek.hedef
        else:                                   # beacon
            hedef = None
    t = kosu.olaylar.simdi
    konfig = kosu.kur.konfig
    hata_db = konfig.rssi_olcum_sigma_db * normal_cekimi(
        "kanal_karar", konfig.tohum, gonderen, d.kimlik,
        int(t / konfig.kanal_dilimi_s), "rssi")
    rssi = round(10.0 * math.log10(guc_w * 1e3) + hata_db)
    kosu.kur.sayaclar.artir("duyma_bildirimi")
    donen = d.protokol.cerceve_duyuldu(d.gozlem(t, None), gonderen, tip,
                                       hedef, rssi, gorunum)
    if donen:
        raise KontrolDuzlemiHatasi(
            "`cerceve_duyuldu` niyet döndüremez — yalnız protokolün kendi "
            f"geçmişine girer; dönen: {donen!r}")


def sirada_mi(d) -> bool:
    return d.kontrol.sirada_mi(d.ucustaki is not None)


def gelenleri_uygula(kosu, d) -> None:
    """`Karar.niyetler` — kararın ardından, veri çerçevesi havaya çıktıktan sonra."""
    if not d.kontrol.gelen:
        return
    niyetler = tuple(d.kontrol.gelen)
    d.kontrol.gelen.clear()
    _uygula(kosu, d, niyetler)


# ======================================================================
# ZAMANLAYICILAR — iki AYRI mekanizma (sözleşme kararı 5)
# ======================================================================
def zamanlayicilari_kur(kosu) -> None:
    """PERİYODİK ilan — kurulumda BİR KEZ, etiket sırasıyla."""
    slot, bitis = kosu.kur.zamanlar.slot_s, kosu.kur.konfig.kosu_bitis_s
    for d in kosu.dugumler:
        if not d.kontrol.etkin:
            continue
        ilan = d.protokol.zamanlayicilar()
        if not isinstance(ilan, dict):
            raise KontrolDuzlemiHatasi("`zamanlayicilar()` bir sözlük döndürmeli")
        rng = kosu.kur.akislar.dugum("beacon_faz", d.kimlik)
        for etiket in sorted(ilan):
            periyot = ilan[etiket]
            if not (isinstance(etiket, str) and etiket
                    and isinstance(periyot, (int, float))
                    and not isinstance(periyot, bool)
                    and math.isfinite(periyot) and periyot >= slot):
                raise KontrolDuzlemiHatasi(
                    f"düğüm {d.kimlik}: geçersiz periyodik ilan "
                    f"{etiket!r}={periyot!r} (etiket boş olamaz, periyot ≥ "
                    f"bir slot ve sonlu)")
            faz = rng.uniform(0.0, float(periyot))
            if faz <= bitis:
                kosu.olaylar.ekle(faz, _zamanlayici_ates, kosu, d.kimlik, etiket,
                                  float(periyot))


def _zamanlayici_ates(kosu, n: int, etiket: str, periyot: float) -> None:
    d = kosu.dugumler[n]
    d.kontrol.say("periyodik_ates")
    _uygula(kosu, d, d.protokol.zamanlayici_doldu(_gozlem(kosu, d), etiket))
    sonraki = kosu.olaylar.simdi + periyot
    if sonraki <= kosu.kur.konfig.kosu_bitis_s:
        kosu.olaylar.ekle(sonraki, _zamanlayici_ates, kosu, n, etiket, periyot)


def _uyandir(kosu, n: int, etiket: str) -> None:
    d = kosu.dugumler[n]
    d.kontrol.uyandirma_ateslendi()
    _uygula(kosu, d, d.protokol.uyandi(_gozlem(kosu, d), etiket))
    _tamponu_yeniden_sor(kosu, d)


# ======================================================================
# GÖNDERİM — veri yoluyla AYNI DCF ve AYNI `gonder`
# ======================================================================
def iletime_basla(kosu, d) -> None:
    """Geri çekilme bitti ve sıra kontrolde. Uçuştaki varsa YENİDEN DENEME."""
    k = d.kontrol
    istek = k.ucustaki if k.ucustaki is not None else k.ucusa_al()
    # A4 (K-177): yayın temel hızda, unicast ARF hızıyla; kapalıyken hız yok.
    hiz = None
    if d.hiz_denetcisi is not None:
        hiz = (kosu.kur.konfig.temel_bit_hizi_bps if istek.yayin_mi
               else d.hiz_denetcisi.hiz(istek.hedef))
    cerceve = cerceve_kur(kosu.kur.konfig, "kontrol",
                          mesaj_bayt=istek.mesaj_bayt, hiz_bps=hiz)
    iletim = Iletim(d.kimlik, cerceve, kosu.olaylar.simdi,
                    kosu.kur.kanal.yayilim.verici_gucu_w)
    s = kosu.kur.sayaclar
    s.artir("kontrol_cerceve")
    s.ekle("kontrol_bayt", cerceve.bayt)
    s.ekle("kontrol_airtime_s", cerceve.sure_s)
    k.say("iletim")
    # 🔒 `pencere_acik`, `pencere_basladi` DEGIL — 16 Eylul 2026 (B2).
    # Ikincisi pencere kapandiktan sonra da True doner; bu cagri onunla
    # yapildigi surece bicim dokumunun "pencere" kipi bosalmada da birikirdi
    # ve toplami `kontrol_iletim_pencere` ile AYRISIRDI.
    k.bicim_say(istek.bicim.ad, cerceve.bayt, cerceve.sure_s,
                s.pencere_acik)
    d.dcf.gonderime_basladi()
    if not istek.yayin_mi:
        d.dcf.onay_bekle()
        k.onay_bekleniyor = True
    gonder(kosu, d.kimlik, iletim, ("kontrol", (istek, k.ucus_no)))


def iletim_bitti(kosu, d, yuk) -> None:
    """Kontrol çerçevesi havadan indi: yayın biter, unicast onay bekler."""
    istek, _no = yuk[1]
    if istek.yayin_mi:
        d.kontrol.ucustan_indir("yayin_gonderilen")
        d.dcf.onay_geldi()
        kosu.cekismeye_basla(d)
        return
    z = kosu.kur.zamanlar
    kosu.olaylar.ekle(kosu.olaylar.simdi + z.sifs_s + z.onay_s + z.slot_s
                      + 2.0 * kosu.kur.maks_gecikme_s,     # A5 (K-175)
                      kosu._onay_penceresi, d.kimlik, d.surum)


def onay_zaman_asimi(kosu, d) -> None:
    d.kontrol.onay_bekleniyor = False
    if d.kontrol.ucustaki is not None:                     # A4 (K-177)
        d.arf_bildir(d.kontrol.ucustaki.hedef, False)
    deneme = d.dcf.deneme               # 🔒 Y1 — sayaç sıfırlanmadan önce
    if d.dcf.onay_gelmedi():
        # 🔒 Y3 · R3 — hedef, uçuştan İNDİRİLMEDEN önce okunur.
        hedef = d.kontrol.ucustaki.hedef if d.kontrol.ucustaki else None
        d.kontrol.ucustan_indir("unicast_vazgecilen")
        iletim_sonucu(kosu, d, hedef, False, deneme, "kontrol")
        iletim_basarisiz(kosu, d, hedef, "kontrol")
        kosu.cekismeye_basla(d)
    else:
        kosu.geri_cekilmeyi_zamanla(d)


# ======================================================================
# ALIM — yalnız alıcı zinciri başarı dediğinde buraya gelinir
# ======================================================================
def cerceve_alindi(kosu, d, gonderen: int, tip: str, bilgi) -> None:
    if tip == "konay":
        _onay_alindi(kosu, d, bilgi)
        return
    if tip != "kontrol":
        raise KontrolDuzlemiHatasi(f"bilinmeyen çerçeve yükü: {tip!r}")
    istek, no = bilgi
    k = d.kontrol
    if not istek.yayin_mi and istek.hedef != d.kimlik:
        k.say("baskasina_adresli")
        return
    if istek.yayin_mi:
        k.say("teslim_yayin")
    else:
        _onay_zamanla(kosu, d, gonderen, no)          # tekrara da onay
        if no <= k.son_gorulen.get(gonderen, -1):
            k.say("tekrar_bastirilan")
            return
        k.son_gorulen[gonderen] = no
        k.say("teslim_unicast")
    # 🔒 Yeniden sorma YOK (K-135): her kontrol mesajında sormak tamponu
    # kontrol trafiği hızında bir yoklama döngüsüne çeviriyordu — ölçüldü,
    # 1 598 pakete karşı 146 678 tampon girişi. Rota kurulduğunu BİLEN taraf
    # protokoldür ve bir `Uyandirma` döndürerek söyler.
    _uygula(kosu, d, d.protokol.kontrol_alindi(
        _gozlem(kosu, d), gonderen, istek.bicim.ad, istek.yuk,
        istek.yayin_mi))


def _onay_zamanla(kosu, d, gonderen: int, no: int) -> None:
    """SIFS sonra onay — veri yolunun `teslim._onay_zamanla`sıyla aynı fizik."""
    cerceve = kosu.kur.onay_cercevesi
    onay = Iletim(d.kimlik, cerceve,
                  kosu.olaylar.simdi + kosu.kur.zamanlar.sifs_s,
                  kosu.kur.kanal.yayilim.verici_gucu_w)
    s = kosu.kur.sayaclar
    s.artir("kontrol_cerceve")
    s.ekle("kontrol_bayt", cerceve.bayt)
    s.ekle("kontrol_airtime_s", cerceve.sure_s)
    kosu.olaylar.ekle(onay.baslangic_s, gonder, kosu, d.kimlik, onay,
                      ("konay", (gonderen, no)))


def _onay_alindi(kosu, d, bilgi) -> None:
    hedef, no = bilgi
    if d.kimlik != hedef:                 # 🔒 yalnız gönderenin kendisi
        return
    k = d.kontrol
    if not k.onay_bekleniyor or no != k.ucus_no:
        return                            # bayat onay
    komsu = k.ucustaki.hedef if k.ucustaki else None   # 🔒 Y1 — indirmeden
    deneme = d.dcf.deneme                              # önce okunur
    d.arf_bildir(komsu, True)                          # A4 (K-177)
    k.ucustan_indir("unicast_onaylanan")
    d.dcf.onay_geldi()
    iletim_sonucu(kosu, d, komsu, True, deneme, "kontrol")
    kosu.cekismeye_basla(d)


# ======================================================================
# RAPOR — yalnız kontrol düzlemi KULLANILDIYSA satıra girer
# ======================================================================
def kontrol_teshisi(dugumler) -> dict | None:
    if not any(d.kontrol.etkin for d in dugumler):
        return None
    # Mesaj biçimi dökümü (`v2/07` §18 Y1) — düğümlerin toplamı, ada göre sıralı.
    bicim: dict = {}
    for kip in ("tum", "pencere"):
        toplam: dict[str, list] = {}
        for d in dugumler:
            for ad, (cerceve, bayt, airtime) in d.kontrol.bicim[kip].items():
                t = toplam.setdefault(ad, [0, 0, 0.0])
                t[0] += cerceve
                t[1] += bayt
                t[2] += airtime
        bicim[kip] = {ad: {"cerceve": c, "bayt": b, "airtime_s": a}
                      for ad, (c, b, a) in sorted(toplam.items())}
    return {
        "defter": {a: sum(d.kontrol.defter[a] for d in dugumler)
                   for a in DEFTER_ALANLARI},
        "bicim": bicim,
        "tepe_bekleyen_uyandirma": max(d.kontrol.tepe_bekleyen
                                       for d in dugumler),
        "bekleyen_uyandirma_tavani": BEKLEYEN_UYANDIRMA_TAVANI,
        # 🔒 Y3 · R2 — beacon kapalı düğüm sayısı SATIRDA beyan edilir;
        # kapalıysa gözlemdeki komşu listesi boş kalır ve bu bir kapsamdır.
        "kosum_beaconi_kapali_dugum": sum(
            1 for d in dugumler if not d.kontrol.kosum_beaconi),
    }


def kontrol_korunumu(dugumler) -> dict | None:
    if not any(d.kontrol.etkin for d in dugumler):
        return None
    r = [d.kontrol.korunum() for d in dugumler]
    return {
        "kontrol_mesaj_tamam": all(x["mesaj_tamam"] for x in r),
        "kontrol_uyandirma_tamam": all(x["uyandirma_tamam"] for x in r),
        "kontrol_jitter_tamam": all(x["jitter_tamam"] for x in r),
        "kontrol_bekleyen_jitter": sum(x["bekleyen_jitter"] for x in r),
        "kontrol_kuyrukta": sum(x["kuyrukta"] for x in r),
        "kontrol_ucusta": sum(x["ucusta"] for x in r),
        "kontrol_bekleyen_uyandirma": sum(x["bekleyen_uyandirma"] for x in r),
    }
