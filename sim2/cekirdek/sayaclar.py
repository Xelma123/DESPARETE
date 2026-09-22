"""
Sayaç kayıt defteri — TEK KAYNAK.

🔴 NEDEN BU DOSYA VAR
=====================
Eski simülatörde 25 sayaç ifadesi **iki yerde birebir tekrarlanıyordu**: bir
kez anlık görüntü alan fonksiyonda, bir kez sonuç sözlüğünde. Kod bunu
*"ikinci bir doğru kaynağı"* olarak kabul edip bir testle bağlamıştı — yani
borç biliniyordu ama yapısaldı. Ayrıca `*_pencere` ikizlerinin hangi sayaçlar
için üretileceği **elle tutulan ikinci bir listeydi** ve o listeye eklenmeyen
bir sayaç sessizce tüm-koşu değerine düşüyordu.

🔒 BURADA ÇÖZÜM YAPISAL
=======================
Sayaçlar hiçbir sınıfın **niteliği değildir**. Tek bir `Sayaclar` nesnesi
vardır; MAC, kanal, kuyruk, sürücü hepsi onu artırır. Anlık görüntü, pencere
ikizi ve sonuç sözlüğü **hepsi `TANIMLAR`dan türer**. İkinci bir liste yoktur,
dolayısıyla iki listenin ayrışması da mümkün değildir.

⚠️ NEDEN PENCERE İKİZİ ZORUNLU
==============================
Ölçüldü: kontrol baytının **%16,62–23,03'ü** ölçüm penceresi DIŞINDA üretiliyor
ve çarpıklık **kola göre değişiyor** (1,1993–1,2993). Yani tüm koşu hâliyle
yapılan eşleştirilmiş bir kol karşılaştırması **yanlıdır**. Pencere ikizi bir
kolaylık değil, geçerlilik şartıdır.

⚠️ ÜÇ TÜR, ÜÇÜ DE FARKLI TÜRETİLİR
==================================
    sayim    tam sayı, monoton artan   → pencere ikizi = FARK
    birikim  float, monoton artan      → pencere ikizi = FARK
    tepe     maksimum                  → 🔴 FARKLA TÜRETİLEMEZ, ayrı izlenir

🔴 İKİZ PENCEREDE BİTER — 16 Eylül 2026'da düzeltildi (denetim B2)
==================================================================
İkiz `[pencere başı, pencere SONU)` aralığını sayar. Önceden `pencere_bitir`
yalnız bir bayrak indiriyordu ve ikiz koşu SONUNDA `değer − pencere_başı`
olarak türüyordu — yani her ikiz `[pencere başı, KOŞU SONU)` aralığını
sayıyordu, 30 saniyelik boşalma aralığı DÂHİL.

⚠️ Bu bir büyüklük sorunu değil, bir KARŞILAŞTIRMA GEÇERLİLİĞİ sorunuydu ve
ölçüldü (`statik-yok` · `statik-surekli` · `DogrudanKomsu` · tohum 1000):

    boşalmadan gelen pay:  kontrol %7,6–10,7  ·  veri tarafı %0,0
    nrl_bayt_pencere       0,0867 ↔ 0,0788   (+%10,0)
    nrl_cerceve_pencere    3,4688 ↔ 3,2049   (+%8,2)
    nrl_airtime_pencere    0,2212 ↔ 0,2032   (+%8,9)

Payda (veri) boşalmada HİÇ büyümüyor — trafik çizelgesi `olcum_bitis_s`te
biter (`ag/trafik.py`) — ama pay (kontrol) büyümeye devam ediyordu. Ve o
kontrol trafiği PERİYODİKTİR: OLSR'ın HELLO/TC'si boşalmada da akar ve
NRL'sini şişirir, AODV'nin keşif trafiği susar ve şişme sıfıra yakın kalır.
Yani üç manşet metrikten biri iki protokol ailesini SİSTEMATİK OLARAK FARKLI
cezalandırıyordu — tam da H1.1'in mekanizma kontrolünün baktığı yerde.

🔒 Tanım, hiçbir protokol yazılmadan ve hiçbir sonuç görülmeden yazıldı.

🔴 VE BİR TUZAK — `pencere_icinde_olculdu`
==========================================
Koşu BİTTİKTEN sonra yazılan ama ölçüm PENCERESİNDE ölçülmüş sayaçlar var:
`kopma_fiziksel` geometriden, koşu sonunda, `[pencere başı, pencere sonu]`
aralığı için hesaplanır (`kosum/kosu.py`). Naif bir dondurma onu ikizde
**0** yapardı — ölçüldü (`bagimsiz-surekli`, tohum 1000): ham 49, ikiz
49 → **0**, ve `algilama_duyarliligi_pencere` 0,0 yerine `None` dönerdi.
Yani Risk 3'ün NİCEL YARISI sessizce ölürdü.

Onun yolu `pencere_icinde_olculdu`dur: değeri hem ham sayaca hem pencere
anlık görüntüsüne yazar. İkinci bir sayaç listesi DEĞİLDİR — tek bir çağrı
yolu, ve gerekçesi çağrı yerinde.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sim2.cekirdek.degismezler import dogrula

__all__ = [
    "SayacTanimi", "Turev", "TANIMLAR", "Sayaclar",
    "sayac_semasi_hash", "PENCERE_SONEKI", "kume_uyeleri",
]

PENCERE_SONEKI = "_pencere"

Tur = Literal["sayim", "birikim", "tepe"]


@dataclass(frozen=True, slots=True)
class SayacTanimi:
    ad: str
    tur: Tur
    aciklama: str
    # 🔒 Varsayılan AÇIK. Kapatmak İSTEYEREK yapılan bir iştir ve
    # `ikizsiz_gerekce` yazmayı zorunlu kılar (aşağıdaki yükleme denetimi).
    # Böylece "unutmak" mümkün değildir — risk 2'nin yapısal panzehiri.
    pencere_ikizi: bool = True
    ikizsiz_gerekce: str = ""
    # 🔴 Kâhin sayaç: simülatörün her şeyi bilen tarafından yazılır, YALNIZ
    # rapora girer. Protokolün kararına giremez.
    kahin: bool = False
    # 🔒 KAPALI KÜME ÜYELİĞİ. Bazı sayaçlar bir bütünün parçalarıdır ve
    # toplamları denetlenir (ör. alım sonuçları: `Σ sebep = toplam deneme`).
    # Üyelik BURADA tanımlanır; başka bir modülde ikinci bir liste tutmak
    # kusur 6'nın ta kendisi olurdu. Yeni bir sonuç sayacı eklemek onu
    # otomatik olarak kümeye ve toplam denetimine sokar.
    kume: str = ""


@dataclass(frozen=True, slots=True)
class Turev:
    """İki sayacın oranı. Tam koşu VE pencere sürümü otomatik türer.

    🔒 `ek_pay` — paya EKLENEN sayaçlar (22 Eylül 2026, K-151 · Y2). Aynı
    bedelin iki kalemini tek bir sayaçta toplamak için bir artırımı iki yerde
    yazmak gerekirdi (`03` §B5'in hata sınıfı); toplam burada türer. Boş
    demette oran eskisiyle BİREBİR aynıdır ve şema özetine girmez.
    """
    ad: str
    pay: str
    payda: str
    aciklama: str
    olcek: float = 1.0
    ek_pay: tuple[str, ...] = ()


# ===========================================================================
# 🔒 TEK KAYNAK — sayaç eklemek TEK SATIRDIR
# ===========================================================================
TANIMLAR: tuple[SayacTanimi | Turev, ...] = (
    # ---------------------------------------------------------- veri düzlemi
    SayacTanimi("uretilen_paket", "sayim", "ölçüm penceresinde doğan paket"),
    SayacTanimi("teslim_paket", "sayim", "hedefine ulaşan benzersiz paket"),
    SayacTanimi("aktarilan_paket", "sayim", "ara düğümde ileri iletilen"),

    # -------------------------------------------------------------- MAC / PHY
    SayacTanimi("mac_gonderim_istegi", "sayim",
                "MAC'e verilen çerçeve — paket-atlama başına BİR kez, "
                "yeniden denemeler HARİÇ"),
    SayacTanimi("mac_gonderim_basarili", "sayim",
                "gönderenin ONAYLA başarılı saydığı çerçeve — "
                "`mac_basari_orani`nın payı",
                kume="iletim_sonucu"),
    SayacTanimi("mac_deneme", "sayim", "yeniden denemeler dâhil iletim"),
    # 🔒 PSR'NİN PAYI ALICI TARAFINDA — öğrencinin tanımı (K-113, `07` §18 Y1).
    # PSR bağlantı düzeyinde, gönderilen çerçevenin alıcı tarafından CRC
    # denetiminden geçerek alınma oranıdır. Onaya dayalı oran bunu ölçmez:
    # onayı kaybolan bir iletimde veri ALINMIŞTIR ama gönderen başarısız sayar.
    # Tekrarlar DÂHİL, çünkü payda `mac_deneme` de yeniden denemeleri sayıyor.
    SayacTanimi("veri_alim_hedefte", "sayim",
                "adreslenen alıcının gövdesini hatasız çözdüğü veri iletimi — "
                "tekrarlar dâhil; PSR'nin payı"),
    SayacTanimi("mac_vazgecme", "sayim", "yeniden deneme hakkı bitti"),
    # 🔴 "mac_carpisma" KALDIRILDI — 8 Eylül 2026. Adı bir MEKANİZMA iddia
    # ediyordu ("eşzamanlı iletim çakışması") ama kod bir BELİRTİ sayıyordu:
    # onay penceresi her boş geçtiğinde artıyordu — gerçek çarpışmada da,
    # gövde PER'den düştüğünde de, onay çerçevesi kaybolduğunda da.
    # Pratik sonucu: karıştırma altında artışı yanlışlıkla "tıkanıklık" diye
    # okunabiliyordu. Bu tam olarak yaşandı ve ancak yük taramasıyla ayrıldı.
    #
    # 🔒 Yerine İKİ sayaç: ayrım BEDAVA, çünkü `Dugum.devredildi` zaten
    # paketin el değiştirip değiştirmediğini biliyor.
    SayacTanimi("mac_onaysiz_veri", "sayim",
                "onay gelmedi ve veri çerçevesi alıcıya ULAŞMADI — "
                "çarpışma, gövde hatası, alıcı meşgul ya da yarı çift yönlü",
                kume="iletim_sonucu"),
    SayacTanimi("mac_onaysiz_onay", "sayim",
                "onay gelmedi ama veri ULAŞMIŞTI — kaybolan şey ONAYDI. "
                "Gönderen bunu bilemez ve yeniden dener; 802.11'in temel "
                "ikilemi", kume="iletim_sonucu"),

    # 🔴 Alım başarısızlık sebepleri — kapalı küme, toplamı denetlenir
    SayacTanimi("alim_basarili", "sayim", "gövde başarıyla çözüldü",
                kume="alim_sonucu"),
    SayacTanimi("alim_red_yari_cift", "sayim", "alıcı o an gönderiyordu",
                kume="alim_sonucu"),
    SayacTanimi("alim_red_mesgul", "sayim", "alıcı başka çerçeveye kilitliydi",
                kume="alim_sonucu"),
    SayacTanimi("alim_red_onbelge", "sayim", "önbelge kilidi kurulamadı",
                kume="alim_sonucu"),
    SayacTanimi("alim_red_per", "sayim", "kilitlendi ama gövde hatalı",
                kume="alim_sonucu"),
    SayacTanimi("alim_yakalama", "sayim", "güçlü çerçeve zayıfı ezdi (capture)"),

    # ------------------------------------------------------- kontrol düzlemi
    SayacTanimi("kontrol_cerceve", "sayim", "gönderilen kontrol çerçevesi"),
    SayacTanimi("kontrol_bayt", "birikim", "kontrol düzlemi baytı"),
    SayacTanimi("kontrol_airtime_s", "birikim", "kontrol düzlemi kanal zamanı"),
    SayacTanimi("veri_bayt", "birikim",
                "veri düzlemi baytı — protokolün veri BAŞLIĞI HARİÇ (K-151)"),
    SayacTanimi("veri_airtime_s", "birikim",
                "veri düzlemi kanal zamanı — protokol başlığı HARİÇ (K-151)"),
    # 🔒 Y2 · K-151 — protokolün her veri paketine eklediği YÖNLENDİRME
    # başlığı. Fiziksel çerçevenin parçasıdır (süreyi ve hataya açık biti
    # büyütür), ama bedeli veri değil yönlendirme ek yüküdür: `nrl_bayt` ve
    # `nrl_airtime`in payına girer. Başlık taşımayan protokolde 0 kalır.
    SayacTanimi("veri_baslik_bayt", "birikim",
                "veri paketindeki protokol başlığı baytı"),
    SayacTanimi("veri_baslik_airtime_s", "birikim",
                "veri paketindeki protokol başlığının kanal zamanı"),
    # 🔒 Y1 · K-151 — her unicast sonucunun protokole bildirimi.
    SayacTanimi("sonuc_bildirimi", "sayim",
                "protokole bildirilen unicast sonucu (veri ve kontrol)"),
    SayacTanimi("beacon_gonderilen", "sayim", "yayınlanan beacon"),
    SayacTanimi("beacon_alinan", "sayim", "başarıyla alınan beacon"),

    # -------------------------------------------- kontrol defteri (K-112 · Y1)
    # 🔒 `kosum/kontrol_durum.py`deki DÜĞÜM defterinin koşu toplamı. Defterin
    # alan adları buradan türer (`kontrol_` öneki atılır) ve
    # `KontrolDurumu.say` düğüm defteri ile bu sayacı AYNI çağrıda artırır.
    # Kümenin denetimi: koşu sonunda her alanda Σ düğüm defteri = sayaç.
    # Kontrol düzlemi kullanmayan protokolde hepsi sıfır kalır.
    SayacTanimi("kontrol_istenen", "sayim",
                "protokolün istediği kontrol mesajı", kume="kontrol_defteri"),
    SayacTanimi("kontrol_kuyruk_tasmasi", "sayim",
                "kontrol kuyruğu dolu, mesaj atıldı", kume="kontrol_defteri"),
    SayacTanimi("kontrol_yayin_gonderilen", "sayim",
                "havaya çıkıp biten yayın mesajı", kume="kontrol_defteri"),
    SayacTanimi("kontrol_unicast_onaylanan", "sayim",
                "onayı gönderene ulaşan unicast mesaj", kume="kontrol_defteri"),
    SayacTanimi("kontrol_unicast_vazgecilen", "sayim",
                "yeniden deneme hakkı biten unicast mesaj",
                kume="kontrol_defteri"),
    SayacTanimi("kontrol_iletim", "sayim",
                "kontrol mesajı iletimi — yeniden denemeler dâhil",
                kume="kontrol_defteri"),
    SayacTanimi("kontrol_teslim_yayin", "sayim",
                "yayın mesajının alıcı başına teslimi", kume="kontrol_defteri"),
    SayacTanimi("kontrol_teslim_unicast", "sayim",
                "unicast mesajın hedefe teslimi", kume="kontrol_defteri"),
    SayacTanimi("kontrol_tekrar_bastirilan", "sayim",
                "hedefte bastırılan unicast tekrarı", kume="kontrol_defteri"),
    SayacTanimi("kontrol_baskasina_adresli", "sayim",
                "çözülen ama başka düğüme adresli unicast",
                kume="kontrol_defteri"),
    SayacTanimi("kontrol_periyodik_ates", "sayim",
                "periyodik zamanlayıcı ateşi", kume="kontrol_defteri"),
    SayacTanimi("kontrol_dinamik_istenen", "sayim",
                "istenen dinamik uyandırma", kume="kontrol_defteri"),
    SayacTanimi("kontrol_dinamik_ates", "sayim",
                "ateşlenen dinamik uyandırma", kume="kontrol_defteri"),
    # 🔒 Y3 · R3 — MAC bir unicast çerçeveden vazgeçti ve protokole haber
    # verildi. Bildirim SAYILIR: sayılmasaydı, kancanın hiç çağrılmadığı bir
    # koşu ile her seferinde çağrıldığı koşu satırdan ayırt edilemezdi.
    SayacTanimi("kontrol_basarisiz_bildirim", "sayim",
                "protokole bildirilen MAC vazgeçmesi",
                kume="kontrol_defteri"),
    # 🔒 Y3 · R4 — titreşimle geciktirilen kontrol mesajı. İkisi kapalı bir
    # denklem kurar: istenen = ateşlenen + bekleyen (`kontrol_durum.py`).
    SayacTanimi("kontrol_jitter_istenen", "sayim",
                "titreşimle geciktirilen kontrol mesajı",
                kume="kontrol_defteri"),
    SayacTanimi("kontrol_jitter_ates", "sayim",
                "titreşimi dolup kuyruğa giren kontrol mesajı",
                kume="kontrol_defteri"),

    # ------------------------------------------------------------- kuyruk/TTL
    SayacTanimi("kuyruk_tasmasi", "sayim", "kuyruk dolu, paket atıldı"),
    SayacTanimi("ttl_olumu", "sayim", "TTL tükendi"),
    SayacTanimi("hedef_yok", "sayim", "protokol sonraki atlamayı seçemedi"),
    SayacTanimi("en_yuksek_doluluk", "tepe", "kuyruktaki en yüksek paket sayısı"),

    # -------------------------------------- rota bekleme tamponu (K-131 · B1)
    # 🔒 `tampon_giris` SAYILIR ve sebebi `basarisiz_bildirim`inkiyle aynı:
    # sayılmasaydı *"protokol hiç tamponlamadı"* ile *"tamponladı ve hep
    # çözdü"* satırdan AYIRT EDİLEMEZDİ. Tamponsuz bir protokolde üçü de
    # sıfır kalır ve satır birebir aynıdır.
    SayacTanimi("tampon_giris", "sayim",
                "rota bekleme tamponuna giren paket — yeniden girişler dâhil"),
    # 🔴 ADI DÜŞME SEBEBİYLE AYNI DEĞİL ve bu, bir testin konuşmasıyla
    # öğrenildi (16 Eylül 2026). Önce `tampon_asimi` konmuştu — düşme
    # sebebinin adının aynısı — ve `test_IKINCI_bir_sayac_listesi_YOK`
    # kırıldı: `korunum.DUSME_SEBEPLERI` demeti böylece ÜÇ sayaç adı taşır
    # hâle geliyordu ve test bunu *"sayaç adlarının ikinci bir listesi"*
    # sayıyor. Test sezgiseldir (eşiği üç sabit) ve koruduğu asıl değişmez
    # fiilen çiğnenmemişti; yine de ÖLÇÜT SONUÇ GÖRÜLDÜKTEN SONRA
    # GEVŞETİLMEZ (`03` §2 ilke 3) — gevşetilen bir kapı bir daha kapı
    # olmaz. Ad değiştirildi ve zaten var olan geleneğe uyuyor:
    # `ttl` → `ttl_olumu` · `iletim_basarisiz` → `mac_vazgecme`.
    SayacTanimi("tampon_dusen", "sayim",
                "tamponun paket ya da süre tavanı aşıldı, paket düştü — "
                "düşme sebebi `tampon_asimi`"),
    SayacTanimi("en_yuksek_tampon", "tepe",
                "rota bekleme tamponundaki en yüksek paket sayısı"),

    # ------------------------------------------- rota olayları (Δ · COR · kopma)
    SayacTanimi("kopma_fiziksel", "sayim",
                "SINR eşiği altına inen bağ — GEOMETRİDEN bilinir", kahin=True),
    SayacTanimi("kopma_algilanan", "sayim",
                "protokolün kopma BEYAN ettiği olay"),
    SayacTanimi("kopma_rota_gecersiz", "sayim",
                "kopma yüzünden geçersizleşen rota"),
    SayacTanimi("rota_kurtarildi", "sayim", "COR'un PAYI — yeniden kurulan yol"),
    SayacTanimi("rota_etkilendi", "sayim", "COR'un PAYDASI — etkilenen yol"),

    # ------------------------------------------------------------------ ölçüm
    SayacTanimi("islenen_olay", "sayim", "olay kuyruğunda işlenen olay",
                pencere_ikizi=False,
                ikizsiz_gerekce="Bir performans/teşhis sayacıdır, bir ölçüm "
                                "büyüklüğü değil; pencere payı bir sonuca "
                                "girmiyor."),

    # =================================================================== türev
    # 🔴 "pdr" BURADAN KALDIRILDI — 8 Eylül 2026. Sayaç ikizleri FARK alarak
    # türetilir; o yüzden `pdr_pencere` PAYI pencerede TESLİM EDİLENLERİ,
    # PAYDASI pencerede DOĞANLARI sayıyordu — iki ayrı küme.
    #
    # ⚠️ Ölçülen sapma küçüktü (0,0016) ama YÖNÜ tehlikeliydi: gecikmesi
    # uzun bir protokol pencere kenarından daha çok paket kaçırır ve hem
    # gecikmede hem PDR'de cezalandırılır. Eşleştirilmiş bir karşılaştırmada
    # bu doğrudan bir confound'dur.
    #
    # 🔒 PDR artık YALNIZ paket defterinden gelir ve kohort DOĞUMA göredir:
    # pencerede doğan bir paket, ne zaman teslim edilirse edilsin sayılır.
    # Tanım `olcum/metrikler.py`de ve TEKTİR.
    # 🔴 PAYDA `mac_deneme`, `mac_gonderim_istegi` DEĞİL — 5 Eylül 2026'da
    # düzeltildi. İlan edilen tanım şuydu: *"psr = başarıyla alınan veri
    # çerçevesi / GÖNDERİLEN veri çerçevesi (atlama düzeyi, YENİDEN DENEMELER
    # DÂHİL)"*. Sayaç kaydı ise paydayı `mac_gonderim_istegi` yapmıştı ve o
    # sayaç paket-atlama başına BİR kez artıyor — yani yeniden denemeler
    # paydaya girmiyordu. İkisi çelişiyordu ve fark sessiz olurdu: yeniden
    # deneme oranı yükseldikçe PSR olduğundan İYİ görünürdü.
    #
    # 🔴 PAY ALICI TARAFINA TAŞINDI — 11 Eylül 2026 (`v2/07` §18 Y1, K-115).
    # Pay `mac_gonderim_basarili` idi, yani GÖNDERENİN onayla saydığı başarı.
    # Öğrencinin tanımı alıcı tarafıdır (K-113): onayı kaybolan iletimde veri
    # alınmıştır. Onaya dayalı oran silinmedi, adı `mac_basari_orani` oldu;
    # ikisinin farkı onay kaybının kendisidir ve karıştırma altında büyür.
    Turev("psr", "veri_alim_hedefte", "mac_deneme",
          "PSR — alıcının hatasız çözdüğü veri iletimi / deneme, yeniden "
          "denemeler dâhil. PDR ile BİRLİKTE okunur"),
    Turev("mac_basari_orani", "mac_gonderim_basarili", "mac_deneme",
          "onaya dayalı MAC başarı oranı — 11 Eylül 2026'ya kadar `psr` "
          "adını taşıyordu"),
    Turev("nrl_cerceve", "kontrol_cerceve", "teslim_paket",
          "teslim başına kontrol çerçevesi"),
    Turev("nrl_bayt", "kontrol_bayt", "veri_bayt",
          "veri baytı başına yönlendirme ek yükü baytı — kontrol + veri "
          "paketindeki protokol başlığı (K-151)",
          ek_pay=("veri_baslik_bayt",)),
    Turev("nrl_airtime", "kontrol_airtime_s", "veri_airtime_s",
          "veri kanal zamanı başına yönlendirme ek yükü kanal zamanı — "
          "kontrol + veri paketindeki protokol başlığı (K-151)",
          ek_pay=("veri_baslik_airtime_s",)),
    Turev("cor", "rota_kurtarildi", "rota_etkilendi",
          "iletişim kurtarma oranı"),
    Turev("algilama_duyarliligi", "kopma_algilanan", "kopma_fiziksel",
          "🔴 protokol gerçek kopmaların ne kadarını GÖRÜYOR"),
)

_SAYACLAR: tuple[SayacTanimi, ...] = tuple(
    t for t in TANIMLAR if isinstance(t, SayacTanimi))
_TUREVLER: tuple[Turev, ...] = tuple(
    t for t in TANIMLAR if isinstance(t, Turev))
_ADLAR: frozenset[str] = frozenset(t.ad for t in _SAYACLAR)

# Kurulum denetimi — modül yüklenirken bir kez.
dogrula(len(_ADLAR) == len(_SAYACLAR), "sayaç adı tekrarlı")
for _t in _TUREVLER:
    dogrula(_t.pay in _ADLAR, f"türev payı tanımsız sayaç: {_t.pay}")
    dogrula(_t.payda in _ADLAR, f"türev paydası tanımsız sayaç: {_t.payda}")
    for _e in _t.ek_pay:
        dogrula(_e in _ADLAR, f"türev ek payı tanımsız sayaç: {_e}")
dogrula(len({t.ad for t in _TUREVLER}) == len(_TUREVLER), "türev adı tekrarlı")
dogrula(not (_ADLAR & {t.ad for t in _TUREVLER}), "sayaç ve türev adı çakışıyor")
# 🔒 RİSK 2'NİN YAPISAL PANZEHİRİ — yükleme anında, koşuda değil.
# Pencere ikizini kapatmak GEREKÇE yazmayı zorunlu kılar. Varsayılan açık
# olduğu için "unutmak" ikizi silmez; silmek bilinçli bir eylemdir.
for _t in _SAYACLAR:
    dogrula(_t.pencere_ikizi or _t.ikizsiz_gerekce.strip(),
            f"{_t.ad!r}: pencere ikizi kapatılmış ama `ikizsiz_gerekce` boş. "
            f"Ölçüldü — kontrol baytının %16,62–23,03'ü pencere DIŞINDA "
            f"üretiliyor ve çarpıklık kola göre değişiyor; ikizsiz bir sayaç "
            f"eşleştirilmiş karşılaştırmayı YANLI yapar.")
    dogrula(not (_t.pencere_ikizi and _t.ikizsiz_gerekce),
            f"{_t.ad!r}: ikizi var ama `ikizsiz_gerekce` yazılmış — "
            f"gerekçe bayat.")


def kume_uyeleri(kume: str) -> tuple[str, ...]:
    """Bir kapalı kümenin üyeleri — TANIMLAR'dan türetilir.

    🔒 Kusur 6'nın kuralı: sayaç adlarının ikinci bir listesi yoktur. Alım
    sonuçları gibi kapalı kümeler de buradan okunur; `mac/alici.py` kendi
    listesini tutsaydı iki liste ayrışabilirdi.
    """
    dogrula(bool(kume), "küme adı boş olamaz")
    uyeler = tuple(t.ad for t in _SAYACLAR if t.kume == kume)
    dogrula(bool(uyeler), f"boş küme: {kume!r}")
    return uyeler


def sayac_semasi_hash() -> str:
    """`TANIMLAR`ın parmak izi — sonuç satırına yazılır.

    Şema sessizce değişirse iki sonuç satırı **karşılaştırılamaz**; bu özet o
    karşılaştırmayı bir kapıya bağlar.
    """
    import hashlib
    h = hashlib.blake2b(digest_size=8)
    for t in TANIMLAR:
        if isinstance(t, SayacTanimi):
            h.update(f"S|{t.ad}|{t.tur}|{t.pencere_ikizi}|{t.kahin}"
                     f"|{t.kume}".encode())
        else:
            h.update(f"T|{t.ad}|{t.pay}|{t.payda}|{t.olcek}".encode())
            if t.ek_pay:
                h.update(f"|+{'+'.join(t.ek_pay)}".encode())
        h.update(b"\x1f")
    return h.hexdigest()


class Sayaclar:
    """Koşu boyunca tek örnek. Bütün katmanlar bunu artırır."""

    __slots__ = ("_deger", "_pencere_bas", "_pencere_son", "_tepe_pencere",
                 "_pencere_acik")

    def __init__(self) -> None:
        self._deger: dict[str, float] = {t.ad: 0.0 for t in _SAYACLAR}
        self._pencere_bas: dict[str, float] | None = None
        # 🔒 Pencere KAPANDIĞI andaki anlık görüntü. `None` ise pencere henüz
        # kapanmamıştır ve ikiz bugünkü değere göre okunur — koşu bitmeden
        # bir ara rapor alınırsa doğru davranış budur.
        self._pencere_son: dict[str, float] | None = None
        # `tepe` farkla türetilemez — pencere boyunca AYRI izlenir.
        self._tepe_pencere: dict[str, float] = {
            t.ad: 0.0 for t in _SAYACLAR if t.tur == "tepe"}
        self._pencere_acik = False

    # ------------------------------------------------------------- artırma
    def artir(self, ad: str, adet: int = 1) -> None:
        try:
            self._deger[ad] += adet
        except KeyError:
            raise KeyError(f"tanımsız sayaç: {ad!r} — TANIMLAR'a ekle") from None

    def ekle(self, ad: str, deger: float) -> None:
        try:
            self._deger[ad] += deger
        except KeyError:
            raise KeyError(f"tanımsız sayaç: {ad!r} — TANIMLAR'a ekle") from None

    def tepe_guncelle(self, ad: str, deger: float) -> None:
        if ad not in self._tepe_pencere:
            raise KeyError(f"{ad!r} bir 'tepe' sayacı değil")
        if deger > self._deger[ad]:
            self._deger[ad] = deger
        if self._pencere_acik and deger > self._tepe_pencere[ad]:
            self._tepe_pencere[ad] = deger

    def oku(self, ad: str) -> float:
        return self._deger[ad]

    @property
    def pencere_basladi(self) -> bool:
        """Pencere açıldı mı — KAPANMIŞ OLSA BİLE.

        🔒 Yalnız *"ikiz var mı"* sorusunun cevabıdır: pencere hiç açılmadıysa
        ikiz `0` değil `None` olur (`disa_ver`). Bir şeyin ikize GİRİP
        girmediğini soran çağıran `pencere_acik` kullanmalıdır — ikisi 16
        Eylül 2026'dan önce aynı şeydi ve bu, biçim dökümünde sessiz bir
        kaçaktı (aşağıya bak).
        """
        return self._pencere_bas is not None

    @property
    def pencere_acik(self) -> bool:
        """Pencere ŞU AN açık mı — ikize giren şeyin ölçütü.

        🔴 `kosum/kontrol.py` mesaj biçimi dökümünü `pencere_basladi` ile
        çağırıyordu; yani dökümün "pencere" kipi boşalmada da birikiyordu.
        İkizler dondurulup döküm dondurulmasaydı `Σ bicim["pencere"].cerceve`
        ile `kontrol_iletim_pencere` AYRIŞIRDI ve `v2/13` §03.11'in
        *"toplamı `kontrol_iletim` ile denetlenir"* taahhüdü kırılırdı.
        İkisi tek kavrama bağlandı.
        """
        return self._pencere_acik

    # -------------------------------------------------------------- pencere
    def pencere_baslat(self) -> None:
        self._pencere_bas = dict(self._deger)
        self._pencere_son = None
        self._tepe_pencere = {a: 0.0 for a in self._tepe_pencere}
        self._pencere_acik = True

    def pencere_bitir(self) -> None:
        """🔒 SAYAÇLAR BURADA DONAR — ikiz pencerede biter (modül başlığı)."""
        dogrula(self._pencere_bas is not None,
                "pencere_bitir çağrıldı ama pencere hiç açılmamıştı")
        self._pencere_son = dict(self._deger)
        self._pencere_acik = False

    def pencere_icinde_olculdu(self, ad: str, adet: float) -> None:
        """Koşu SONUNDA yazılan ama PENCEREDE ölçülmüş bir büyüklük.

        🔴 Tek çağıranı `kosum/kosu.py::_fiziksel_kopmalari_say`dır ve
        gerekçesi orada yazılı: `kopma_fiziksel` geometriden, koşu bittikten
        sonra, `[pencere başı, pencere sonu]` aralığı için hesaplanır. Sıradan
        `artir` ile yazılsaydı pencere çoktan donmuş olurdu ve ikiz **0**
        çıkardı — ölçüldü, ve `algilama_duyarliligi_pencere` `None`a düşerdi.

        🔒 Ham değere ve pencere anlık görüntüsüne AYNI çağrıda yazar; ikisi
        ayrışamaz. Pencere hiç açılmadıysa yalnız ham değer artar ve ikiz
        `None` kalır — *"ölçüm yok"*.
        """
        self.artir(ad, adet)
        if self._pencere_son is not None:
            self._pencere_son[ad] += adet

    # --------------------------------------------------------------- çıktı
    def disa_ver(self) -> dict[str, float | None]:
        """Ham sayaçlar + **otomatik** pencere ikizleri + türevler.

        🔒 Buradaki hiçbir ad elle yazılmaz; hepsi `TANIMLAR`dan gelir.
        """
        cikti: dict[str, float | None] = {}
        bas = self._pencere_bas
        # 🔒 Pencere KAPANDIYSA oradaki anlık görüntü, kapanmadıysa bugünkü
        # değer. İkiz böylece `[pencere başı, pencere sonu)` aralığını sayar
        # ve boşalma aralığı DIŞARIDA kalır (modül başlığı, B2).
        son = self._pencere_son if self._pencere_son is not None else self._deger

        for t in _SAYACLAR:
            cikti[t.ad] = self._deger[t.ad]
            if not t.pencere_ikizi:
                continue
            ikiz = t.ad + PENCERE_SONEKI
            if bas is None:
                # 🔴 "0" DEĞİL: pencere hiç açılmadıysa ölçüm YOKTUR.
                cikti[ikiz] = None
            elif t.tur == "tepe":
                cikti[ikiz] = self._tepe_pencere[t.ad]
            else:
                cikti[ikiz] = son[t.ad] - bas[t.ad]

        for tv in _TUREVLER:
            cikti[tv.ad] = _oran(_pay(cikti, tv, ""), cikti.get(tv.payda),
                                 tv.olcek)
            cikti[tv.ad + PENCERE_SONEKI] = _oran(
                _pay(cikti, tv, PENCERE_SONEKI),
                cikti.get(tv.payda + PENCERE_SONEKI), tv.olcek)
        return cikti

    def ikizsiz_rapor(self) -> dict[str, tuple[float, str]]:
        """Isınmada artmış, ikizi olmayan sayaçlar — GEREKÇESİYLE.

        🔴 Risk 2 iki katmanda karşılanır:
          1. **Yükleme anında** (yukarıda): ikizi kapatmak gerekçe zorunlu
             kılar → *unutmak* imkânsız.
          2. Burada: ikizsiz bir sayaç ısınmada gerçekten artıyorsa, gerekçesi
             sonuç satırına **yazılır** ve okuyan onu görür.
        """
        bas = self._pencere_bas
        if bas is None:
            return {}
        return {t.ad: (bas[t.ad], t.ikizsiz_gerekce) for t in _SAYACLAR
                if not t.pencere_ikizi and bas[t.ad] > 0.0}


def _pay(cikti: dict, tv: Turev, sonek: str) -> float | None:
    """Türevin payı — `pay` + `ek_pay`. Birinden biri `None`sa `None`."""
    toplam = cikti.get(tv.pay + sonek)
    for e in tv.ek_pay:
        deger = cikti.get(e + sonek)
        if toplam is None or deger is None:
            return None
        toplam += deger
    return toplam


def _oran(pay: float | None, payda: float | None, olcek: float) -> float | None:
    """🔴 Payda sıfırsa `None` — `0.0` DEĞİL.

    *"Ölçüm yok"* ile *"oran sıfır"* aynı şey değildir; `0.0` döndürmek
    ölçülmemiş bir hücreyi ortalamaya sokar.
    """
    if pay is None or payda is None or payda == 0:
        return None
    return olcek * pay / payda
