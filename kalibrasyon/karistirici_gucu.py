"""
KARIŞTIRICI ŞİDDETİ — dBm ile değil, ρ (ENGELLENEN BAĞ ORANI) ile.

Üretici:
    PYTHONIOENCODING=utf-8 python kalibrasyon/karistirici_gucu.py

🔴 NEDEN GÜÇLE DEĞİL
====================
`senaryolar.KARISTIRICI_GUCU_DBM` sözlüğündeki beş değerin beşi de `None`
ve bu **bilinçli**: sessiz bir varsayılan, çalışma noktasını ölçmeden
seçmek olurdu.

Ama dBm'in kendisi de yanlış birimdir — ÇALIŞMA NOKTASI SEÇERKEN. Bir gücün
ne kadar ağ yok ettiği alan, yoğunluk ve yayılım üstelinin hepsine bağlıdır;
−15 dBm tek başına hiçbir şey ifade etmez. Bu yüzden nokta ρ ile seçilir.

🔴 AMA SINIFLARI ρ İLE EŞİTLEMEK DÖNGÜSELDİR — ilk beyanım yanlıştı
====================================================================
Bu başlıkta önce *"sınıflar aynı ETKİDE eşitlenmelidir"* yazıyordu. Yanlış:
ρ bir ETKİDİR, yani bağımlı değişken — deneyin ölçmek istediği şeyin ta
kendisi. Her sınıfa aynı ρ'yu verdirmek, aramaya çıktığımız mekanizma
farkını kalibrasyonla SİLMEK olurdu.

🔒 DOĞRU İLKE: eşitleme, karıştırıcının HARCADIĞI şey üzerinden yapılır
(yayılan **ortalama güç** — bir verici özelliği, bir girdi), BAŞARDIĞI şey
üzerinden değil. `karistirici.py` bunu zaten böyle yapıyor:
`surekli_darbeli` görev çevrimini `tepe_telafisi_db` ile telafi eder.

⚠️ BEYAN EDİLMİŞ TEK ASİMETRİ: `taramali` TEPE gücü eşit tutar, ortalaması
konak sayısına bölünür (≈ −4,8 dB). Bu bilinçli ve `karistirici.py`de
gerekçeli — ama bir ŞİDDET farkıdır ve *"taramalı daha zayıf çıktı"*
bulgusu mekanizmaya tek başına yazılamaz. Ön-kayıtta böyle geçer.

🔒 ρ — ENGELLENEN BAĞ ORANI
===========================
    ρ = 1 − (karıştırıcı açıkken kullanılabilir bağ sayısı)
            ────────────────────────────────────────────
            (karıştırıcı yokken kullanılabilir bağ sayısı)

Yani *"ağın kaçta kaçı yok edildi"*. Yönlendirmenin karşılaştığı şey budur;
dBm bir çıktıdır, girdi değil.

⚠️ Ölçüm KÂHİN GRAFİĞİNDE yapılır (`kalibrasyon/kahin.py`): gölgeleme,
sönümleme ve karıştırıcı dâhil, yeniden denemelerle atlama başarısı
`ATLAMA_ESIGI`ni geçen bağlar. Kâhinin karıştırıcıyı görmesi 8 Eylül
2026'da eklendi — öncesinde karıştırılan bölgenin etrafından dolaşmıyordu.

🔴 İLK İLAN EDİLEN ÖLÇÜT YANLIŞ TANIMLIYDI — ve nedeni öğreticidir
==================================================================
İlk hâli şuydu: *"statik kolda 30 tohumun hiçbirinde ulaşılamaz çift yok."*
Tarama onu −24 dBm'e, yani **ρ = 0,058**'e götürdü — bağların %6'sı. O
karıştırıcı hiçbir şey yapmıyor ve deney yine *"fark yok"* derdi.

Sorun eşikte değil, TANIMDA: *"ulaşılamaz çift"* iki farklı olguyu tek
kovaya koyuyordu.

  1. Karıştırıcının dibinde kalıp **boğulan bir düğüm** — bu, incelediğimiz
     olgunun ta kendisi. Gerçek bir İHA da karıştırıcının yanında bağlantısını
     kaybeder ve yönlendirme onu kurtaramaz.
  2. Ağın **iki büyük parçaya ayrılması** — asıl confound. O zaman bütün
     protokoller eşit çöker ve ölçülen şey yönlendirme değil bölünme olur.

Ölçüt ikisini de yasaklıyordu; oysa yalnız (2) confound. Yani ölçüt,
İNCELEDİĞİMİZ OLGUYU yasaklıyordu — bu bir şartname hatasıdır, hoşa gitmeyen
bir sonucu gevşetmek değil. Testi sonuçtan bağımsızdır ve taramaya bakmadan
da sorulabilirdi.

🔒 ÖLÇÜLDÜ (bileşen yapısı, açılmadan sonra):

    güç    ulaşılabilirlik  en büyük bileşen  ÇOK ÜYELİ bileşen  yalnız düğüm
    −15         1,000            1,000                1              0,0
    −12         0,942            0,970                1              1,2   ← boğulma
     −9         0,876            0,935                1              2,6   ← boğulma
     −6         0,647            0,760              **2**            3,2   ← AYRILMA

Ayrılma ancak −6 dBm'de başlıyor; öncesinde ağ bölünmüyor, yalnız birkaç
düğüm boğuluyor.

🔒 YENİDEN FORMÜLASYON — SIFIR SERBEST PARAMETRE
================================================
    Sert kısıt : 30 tohumun hiçbirinde BİRDEN FAZLA ÇOK ÜYELİ bileşen yok
                 (tek tek boğulmuş düğümler SERBEST — olgunun kendisi)
    Amaç       : bu kısıt altında ρ'yu EN BÜYÜK yapmak

Eşik gevşetilmedi: yanlış tanımlanmış bir kısıt DOĞRU TANIMLANDI. Yeni
ölçütün de sıfır serbest parametresi var — "birden fazla çok üyeli bileşen"
bir sayı değil, bir yapı sorusudur.

**Neden ρ amaç:** yönlendirmenin zorlanması gerekir. ρ küçükse karıştırıcı
etkisiz kalır ve yine ölçülecek bir şey olmaz.

🔒 Bu ölçüt, alan büyüklüğü seçiminde kullanılanın AYNISIDIR
(`calisma_noktasi.py`) ve aynı sebeple: sert kısıt bağlantılılık, amaç
zorluk. Aynı mantığı iki yerde farklı uygulamak, ikisinin ayrışması demek
olurdu.

⚠️ ÇAPRAZ KONTROL YAPILDI — ve iki şeyi karıştırdığımı gösterdi
===============================================================
Beklenti şuydu: *"harp altında ilk şokta %50'nin altına düşer, mesh tepki
verince %70–80'e çıkabilmeli."*

⚠️ ÖLÇÜM 3 TOHUMLUK — GEÇİCİ, SONUÇ SATIRI DEĞİL (8 Eylül 2026 denetimi):
    kâhin PDR: temiz 0,998  →  karıştırılmış **0,959**
    tohumlar arası yayılım: 0,989 · 0,994 · **0,894** — büyük.

🔴 Kural 8 sonuç için ≥30 tohum istiyor; bu sayı bir ÇAPRAZ KONTROLDÜR ve
sonuç satırına giremez. Yayılım ortalamanın kendisiyle kıyaslanabilir
mertebede olduğu için "%95,9" tek başına okunmamalıdır.

🔴 VE 8 EYLÜL'E KADAR ÜRETİCİSİ YOKTU — kural 7 çiğnenmişti. `pdr_tavani.py`
üç bölümünde de yalnız `-yok` kolunu koşuyordu; bu sayıyı üreten hiçbir
betik depoda yoktu. Artık var:
    Üretici: `python kalibrasyon/pdr_tavani.py 4`      (3 tohum, geçici)
    Sonuç için: `python kalibrasyon/pdr_tavani.py 4x30`

🔒 YENİ ÜRETİCİ ESKİ SAYIYI DOĞRULUYOR (tohum 1000): temiz 1,000 →
karıştırılmış **0,988**; eski kayıttaki ilk tohum 0,989 idi. Yani kurulum
eşleşiyor ve 0,959'luk ORTALAMA tek bir aykırı tohumun (0,894) eseri.
Bu, "3 tohum yetmez" uyarısını güçlendiriyor — sayı değil, YAYILIM sorun.

🔴 Yani bağların **dörtte birini** yok etmek, mükemmel yönlendirmeyle
yalnız **4 puana** mal oluyor. Ağın yedekliliği yetiyor: kâhin deliğin
etrafından dolaşıyor. *Bağ yok etmek ≠ teslim kaybı.*

🔒 Bu bir çelişki DEĞİL — karşılaştırılan şeyler yanlıştı. Beklenen %70–80
bir PROTOKOLÜN performansını tarif ediyor, ulaşılabilir tavanı değil. Tavan
0,96 iken bir protokol 0,75'e ulaşıyorsa aradaki 21 puan **protokolün
körlüğüdür** — ve ölçmek istediğimiz şey tam olarak odur.

⭐ Ayırt etme için geniş manevra alanı var: farklı güçlerde kâhin tavanı
0,44 ile 0,96 arasında geziyor, protokoller o aralıkta ayrışacak.

🔴 AMA ÖLÇÜLMÜŞ BİR GERGİNLİK VAR ve kayda geçer:
Tavanı %70–80'e indirmek karıştırıcıyı ~−9 dBm'e çıkarmayı gerektirir; orada
30 tohumun **9'unda ağ AYRILIYOR**. Yani *"tavan %70–80 olsun"* ile *"ağ
bölünmesin"* **aynı anda sağlanamaz**. Bu bir tercih değil, bu ağın
yedekliliğinin ölçülmüş bir sonucudur. Sert kısıt bağlantılılık olduğu için
tavan yüksek kalır ve fark protokollerden gelir.

🔴 ρ HER SINIFTA OKUNAMAZ — kodu okuyarak doğrulandı, varsayılmadı
==================================================================
ρ, TRAFİKSİZ bir kanal grafiği probunda ölçülür. Beş sınıfın dördünün zaman
yapısı var ve prob onları eşit görmüyor:

| sınıf | `acik_mi` neye bakar | probda ρ |
|---|---|---|
| `surekli` | hep açık | ✔ temiz — çalışma noktası BUNUNLA seçildi |
| `surekli_darbeli` | 2,7 s periyot · %50 | ⚠️ sabit anlar periyotla ÖRTÜŞÜR |
| `reaktif` | `ortam.aktif(t)` | 🔴 **yapısal olarak 0** — probda iletim yok |
| `aldatici` | çerçeve+DIFS ≈ %98 | ⚠️ yanlış şeyi ölçer (zararı CSMA'da) |
| `taramali` | hash'li konak · 1/3 | ✔ istatistiksel |

🔒 ÖLÇÜLDÜ — beş sınıf, hepsi −15,0 dBm TABAN gücünde, 30 tohum × 9 an:

    sınıf              açık   ort_dBm     ρ    boğulan  AYRILAN
    surekli           1,000     −15,0  0,258     0,13     0/30
    surekli_darbeli   0,499     −15,0  0,169     0,21     1/30  🔴
    reaktif           0,000        −∞  0,000     0,00     0/30
    aldatici          0,978     −15,1  0,258     0,13     0/30
    taramali          0,325     −19,9  0,081     0,04     0/30

⭐ `aldatici` ile `surekli` KANAL GRAFİĞİNDE TIPATIP AYNI. Bu bir kusur
değil, EŞLEŞTİRİLMİŞ KARŞITLIK: bağ hasarı sabit tutulmuş, tek fark CSMA
görünürlüğü. İkisinin farkı saf kanal-erişim etkisidir ve bu, tehdit
modelindeki en temiz kontrastır.

🔴 DARBELİ KOL SERT KISITI 1/30 TOHUMDA ÇİĞNEDİ — ve nedeni fiziktir
====================================================================
Eşit ORTALAMA güç, eşit TEPE güç demek değildir: darbeli %50 görev
çevriminde tepesini +3,01 dB yükseltir. Açıkken yok ettiği bağ oranı
0,169 × 9/4 = **0,380** (sürekli 0,258). Yani eşit ortalama güçle eşitlemek,
sert kısıtın her sınıfta sağlanacağını GARANTİ ETMİYOR.

⚠️ ÖLÇÜT SONUCA GÖRE EĞİLMEDİ — ZAMAN ANLAMI NETLEŞTİRİLDİ, ve iki ölçüm
bunu iddia değil OLGU yaptı:

  1. Temiz grafik **30 tohumun 30'unda tek parça**. Karıştırıcı kapanınca
     ağın bütünleşmesi garanti, şans değil.
  2. Ayrılan tek tohum 1028 ve dört örneğinin dördü de darbe fazı < 1,35 —
     yani HEPSİ AÇIK EVREDE. Kapalı evrede hiç ayrılma yok.

Dolayısıyla ayrılmanın süresi yapısal olarak **en çok 1,35 s**dir. AODV'nin
`ACTIVE_ROUTE_TIMEOUT`u 3 s (RFC 3561) — en hızlı taban çizgisinin rota
geçersizleme zamanı. Ayrılma o zamandan kısa olduğu için hiçbir protokol
KARARLI bir bölünmüş topoloji göremez; gördüğü şey bir bağ arızası salvosudur.

🔒 KISITIN NETLEŞMİŞ HÂLİ (sıfır serbest parametre, dış çıpası RFC 3561):
    Hiçbir kolda, bölünmüş topoloji EN HIZLI TABAN ÇİZGİSİNİN ROTA
    GEÇERSİZLEME SÜRESİNDEN uzun sürmeyecek.

Sürekli karıştırıcı için bu, eski hâliyle AYNI şeydir (orada bir ayrılma
sonsuza kadar sürer). Fark yalnız zamanla değişen sınıflarda ortaya çıkar —
eski hâli onlar için hiç tanımlanmamıştı, tıpkı "ulaşılamaz çift"in boğulma
ile bölünmeyi ayırmaması gibi.

⚠️ NE ZAMAN YAZILDIĞI: bu netleştirme 1/30 sonucu GÖRÜLDÜKTEN SONRA yazıldı
ve bu kayda geçer. Yapıdan önce de sorulabilirdi — dört sınıfın zaman yapısı
olduğunu kod okumasıyla ZATEN saptamıştım, *"karıştırıcı kapanıyorsa
'ayrılma yok' ne demek"* sorusunu o an sormayı atladım.

🔴 YANLIŞLAMA KOŞULU: darbe süresi AODV'nin 3 s'sini aşarsa bu gerekçe
ÇÖKER ve taban gücü düşürülmek zorundadır. `darbe_periyodu_s` ya da
`darbe_gorev_cevrimi` duyarlılık denetiminde oynatılırken bu SINANIR.

🔴 REAKTİF'İN ρ'SI SIFIR ÇIKARSA BU BİR KUSUR DEĞİL, TANIMDIR: reaktif
karıştırıcı yalnız birileri iletirken vardır. Zararı ancak protokol koşarken
görülür — bu yüzden onun şiddeti Faz 2'de trafikli ölçümle raporlanır.

⚠️ ÖRTÜŞME (aliasing) DÜZELTİLDİ: örnek anları 15,6 s aralıklı seçildi.
15,6 mod 2,7 = 2,1 = 7×0,3 ve gcd(7, 9) = 1 olduğundan dokuz an, darbe
fazını [0; 2,7) aralığına DÜZGÜN dağıtır — şansa değil sayı teorisine
dayanır. Eski üç sabit an darbeliyi %50 yerine %67 açık yakalıyordu.
Ölçütü değil, ÖLÇÜM ARACINI düzeltiyor.
"""

from __future__ import annotations

import statistics as ist
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import dogrula  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from sim2.yapilandirma.senaryolar import (  # noqa: E402
    KARISTIRICI_GUCU_DBM, KARISTIRICI_SINIFLARI, TEHDIT_SENARYOLARI)
from sim2.kanal.tehdit import tehdit_tanimlari  # noqa: E402
from kalibrasyon.kahin import KanalGrafigi  # noqa: E402

TOHUMLAR = range(1000, 1030)          # 30 tohum — ölçütün gerektirdiği

# 🔒 ÖRTÜŞMEYİ KIRAN ANLAR — adım 15,6 s. 15,6 mod 2,7 = 2,1 = 7×0,3 ve
# gcd(7, 9) = 1 olduğu için dokuz an, darbe fazını 0,3'ün dokuz katına —
# yani [0; 2,7) aralığına DÜZGÜN — oturtur. Şansa değil, sayı teorisine
# dayanır. Sabit aralıklı üç an (200/260/310) darbeliyi %50 yerine %67
# açık yakalıyordu; 15,7'lik ilk denemem ise %33'e düşürüyordu.
ORNEK_ANLARI = tuple(200.0 + k * 15.6 for k in range(9))   # 200,0 … 324,8 s

# 🔒 Sınıf listesi KAYNAĞINDAN türetilir, elle yazılmaz. Elle yazılmıştı ve
# ayrışmıştı: burada `darbeli`, tabloda `surekli_darbeli`. Yalnız `surekli`
# koştuğum için hiç ateşlenmedi — sıra o sınıfa gelseydi KeyError verirdi.
SINIFLAR = tuple(s for s in KARISTIRICI_SINIFLARI if s != "yok")


def _graf_ozeti(senaryo: str, tohum: int, guc_dbm: float | None,
                t_s: float, aile: str | None = None) -> dict[str, float]:
    ek: dict[str, object] = {}
    if guc_dbm is not None:
        ek["karistirici_guc_override_dbm"] = guc_dbm
    if aile is not None:
        ek["tehdit_senaryosu"] = aile
    kfg = Konfig(kol="rho", senaryo=senaryo, tohum=tohum, **ek)
    kur = kurulum_yap(kfg)
    g = KanalGrafigi(kur)
    return g.ozet(t_s)


def olc(sinif: str, guc_dbm: float | None) -> dict[str, float]:
    """Bir sınıf ve güçte ρ, bağlantılılık ve BİLEŞEN YAPISI."""
    rho, ulas, yalniz = [], [], []
    ayrilan_tohum = 0
    for tohum in TOHUMLAR:
        temiz = _graf_ozeti("statik-yok", tohum, None, ORNEK_ANLARI[0])
        ayrildi = False
        for t in ORNEK_ANLARI:
            o = _graf_ozeti(f"statik-{sinif}", tohum, guc_dbm, t)
            rho.append(1.0 - o["derece"] / temiz["derece"]
                       if temiz["derece"] else 0.0)
            ulas.append(o["ulasilabilirlik"])
            yalniz.append(o["yalniz_dugum"])
            # 🔴 SERT KISIT: birden fazla ÇOK ÜYELİ bileşen = AYRILMA.
            # Tek tek boğulmuş düğümler ayrılma DEĞİLDİR.
            if o["cok_uyeli_bilesen"] > 1.0:
                ayrildi = True
        ayrilan_tohum += ayrildi
    return {"rho": ist.mean(rho), "ulasilabilirlik": ist.mean(ulas),
            "yalniz_dugum": ist.mean(yalniz),
            "ayrilan_tohum": float(ayrilan_tohum)}


def tarama(sinif: str = "surekli",
           gucler=(-30.0, -24.0, -18.0, -15.0, -12.0, -9.0, -6.0)) -> None:
    print("=" * 78)
    print(f"RHO TARAMASI — sinif '{sinif}'")
    print("=" * 78)
    print(f"  OLCUT: {len(list(TOHUMLAR))} tohumun hicbirinde BIRDEN FAZLA "
          f"COK UYELI bilesen YOK")
    print("         (tek tek bogulmus dugumler SERBEST — olgunun kendisi)")
    print("         bu kisit altinda rho EN BUYUK")
    print(f"  ornek anlari (acilmadan SONRA): {ORNEK_ANLARI}\n")
    print(f"  {'guc_dBm':>9} {'rho':>7} {'ulas':>7} {'bogulan':>8} "
          f"{'AYRILAN tohum':>15} {'olcut':>8}")
    secilen = None
    for guc in gucler:
        s = olc(sinif, guc)
        gecti = s["ayrilan_tohum"] == 0.0
        if gecti:
            secilen = (guc, s["rho"])
        print(f"  {guc:>9.1f} {s['rho']:>7.3f} {s['ulasilabilirlik']:>7.3f} "
              f"{s['yalniz_dugum']:>8.2f} "
              f"{int(s['ayrilan_tohum']):>10}/{len(list(TOHUMLAR))} "
              f"{'GECER' if gecti else 'kalir':>8}")
    print()
    if secilen is None:
        print("  🔴 HICBIR GUC OLCUTU SAGLAMADI — tarama araligi zayif")
        print("     guclere dogru genisletilmeli.")
    else:
        guc, rho = secilen
        print(f"  🟢 SECILEN: {guc:.1f} dBm  ·  rho = {rho:.3f}")
        print("     Agin AYRILMADIGI EN GUCLU karistirici.")
        print("     ⚠️ Sayi ELLE KONMADI: sert kisit ile amacin kesistigi nokta.")


def _acik_orani(sinif: str) -> tuple[float, float]:
    """Sınıfın örnek anlarında AÇIK kalma oranı ve yayılan ortalama güç.

    🔒 ρ'nun okunabilir olup olmadığını söyleyen tanıdır. Açık oranı ~0 ise
    ölçülen ρ o sınıfın şiddetini DEĞİL, yalnız prob koşullarını yansıtır.
    """
    # 🔒 OVERRIDE YOK — güç `senaryolar.KARISTIRICI_GUCU_DBM`den okunur.
    # Zorunlu: override darbeli sınıfta tepe telafisini atlar ve "aynı
    # ortalama güç" eşitlemesini kırar; `Konfig` bunu zaten yasaklıyor.
    kfg = Konfig(kol="rho", senaryo=f"statik-{sinif}", tohum=1000)
    kar = kurulum_yap(kfg).kanal.karistirici
    dogrula(kar is not None, f"'{sinif}' icin karistirici kurulmadi")
    # İnce ızgara — açık oranı, örnek anlarından değil sürekli taramadan.
    izgara = [150.0 + k * 0.01 for k in range(20_000)]      # 150 → 350 s
    acik = sum(kar.acik_mi(t) for t in izgara) / len(izgara)
    import math
    ort_dbm = (kfg.karistirici_guc_dbm + 10.0 * math.log10(acik)
               if acik > 0.0 else float("-inf"))
    return acik, ort_dbm


def sinif_raporu() -> None:
    """🔒 ρ'yu SONUÇ olarak raporlar — hedef olarak DEĞİL.

    Güç beş sınıfta da aynıdır (`senaryolar.KARISTIRICI_GUCU_DBM`); burada
    okunanlar o tek gücün sınıf mekanizmasına göre ne yaptığıdır.
    """
    print("=" * 78)
    taban = KARISTIRICI_GUCU_DBM["surekli"]
    print(f"SINIF RAPORU — hepsi {taban:.1f} dBm TABAN gucunde "
          f"(senaryolar.KARISTIRICI_GUCU_DBM)")
    print("=" * 78)
    print("  🔒 rho bir SONUCTUR, hedef degil. Siniflar YAYILAN ORTALAMA")
    print("     GUC uzerinden esitlenir; etkiyi esitlemek dongusel olurdu.")
    print(f"  {len(list(TOHUMLAR))} tohum x {len(ORNEK_ANLARI)} an "
          f"(darbe fazi duzgun ortulu)\n")
    print(f"  {'sinif':>17} {'acik':>7} {'ort_dBm':>9} {'rho':>7} "
          f"{'ulas':>7} {'bogulan':>8} {'AYRILAN':>9} {'rho okunur mu':>15}")
    for sinif in SINIFLAR:
        acik, ort = _acik_orani(sinif)
        s = olc(sinif, None)
        if acik < 0.01:
            yorum = "🔴 HAYIR"
        elif sinif == "aldatici":
            yorum = "⚠️ eksik"
        else:
            yorum = "evet"
        ort_yazi = "—∞" if ort == float("-inf") else f"{ort:>9.1f}"
        print(f"  {sinif:>17} {acik:>7.3f} {ort_yazi:>9} {s['rho']:>7.3f} "
              f"{s['ulasilabilirlik']:>7.3f} {s['yalniz_dugum']:>8.2f} "
              f"{int(s['ayrilan_tohum']):>6}/{len(list(TOHUMLAR))} "
              f"{yorum:>15}")
    print()
    print("  🔴 'reaktif' icin acik orani 0 BEKLENIR: trafiksiz probda")
    print("     patlayacagi bir iletim yoktur. Kusur degil, TANIM.")
    print("  ⚠️ 'aldatici' icin rho eksiktir: zarari CSMA'yi mesgul etmek,")
    print("     ve o kanal grafiginde gorunmez.")



def _aile_gucu(aile: str) -> tuple[int, float]:
    """Ailenin üye sayısı ve TOPLAM ORTALAMA güç payı.

    🔒 Eşitleme burada DOĞRULANIR, varsayılmaz: `tehdit.py::_guc_payi`
    1/(K × açık oranı) verdiği için toplam ortalama payın her ailede 1,0
    çıkması gerekir. Çıkmazsa aileler farklı ŞİDDETTE demektir ve
    "aile X daha kötü" bulgusu mekanizmaya yazılamaz.
    """
    kfg = Konfig(kol="rho", senaryo="statik-surekli", tohum=1000,
                 tehdit_senaryosu=aile)
    tanimlar = tehdit_tanimlari(kfg)
    if tanimlar is None:
        return 1, 1.0
    toplam = 0.0
    for t in tanimlar:
        y = t.yayin
        oran = (1.0 if y.duzen == "surekli"
                else y.acik_s / (y.acik_s + y.sessiz_s))
        toplam += t.guc_payi * oran
    return len(tanimlar), toplam


def olc_aile(aile: str, sinif: str = "surekli") -> dict[str, float]:
    """Bir ailede ρ, bağlantılılık ve BİLEŞEN YAPISI.

    `olc` ile aynı gövde; tek fark karıştırıcı kümesinin biçimi. Temiz
    referans grafiği aileden BAĞIMSIZDIR (karıştırıcı yok), bu yüzden
    aileler arası ρ karşılaştırması aynı paydayı kullanır.
    """
    rho, ulas, yalniz = [], [], []
    ayrilan_tohum = 0
    for tohum in TOHUMLAR:
        temiz = _graf_ozeti("statik-yok", tohum, None, ORNEK_ANLARI[0])
        ayrildi = False
        for t in ORNEK_ANLARI:
            o = _graf_ozeti(f"statik-{sinif}", tohum, None, t, aile)
            rho.append(1.0 - o["derece"] / temiz["derece"]
                       if temiz["derece"] else 0.0)
            ulas.append(o["ulasilabilirlik"])
            yalniz.append(o["yalniz_dugum"])
            if o["cok_uyeli_bilesen"] > 1.0:
                ayrildi = True
        ayrilan_tohum += ayrildi
    return {"rho": ist.mean(rho), "ulasilabilirlik": ist.mean(ulas),
            "yalniz_dugum": ist.mean(yalniz),
            "ayrilan_tohum": float(ayrilan_tohum)}


def aile_raporu(sinif: str = "surekli") -> bool:
    """🔒 C2'nin YENİ parçası — tehdit AİLELERİ sert kısıtta sınanır.

    Ölçüt DEĞİŞMEDİ (`karistirici_gucu.py` yeniden formülasyonu):
        Sert kısıt : 30 tohumun hiçbirinde BİRDEN FAZLA ÇOK ÜYELİ bileşen yok
        Amaç       : bu kısıt altında ρ en büyük

    ⚠️ Ailelerde kısıt DAHA SERTTİR ve sebebi zaman yapısıdır: keskinleşmiş
    hâl *"bölünme en hızlı tabanın rota geçersizleme süresinden (3 s, RFC
    3561) uzun sürmesin"* diyor. `cephe_hatti` sürekli yayar — orada bir
    bölünme KALICIDIR. Çevrimli ailelerde açık evre 15 s, yine 3 s'in çok
    üstünde. Yani bu ailelerde tek bir örnek anında görülen bölünme bile
    kısıtı çiğner.

    🔒 `surekli` sınıfı seçilir: ρ yalnız onda temiz okunur (sınıf raporu).

    🔒 VERDİKT DÖNER — 16 Eylül 2026. Bu bölüm bir KAPIDIR (doğrulama listesi
    #5b) ama verdikti yalnız ekrana basıyordu ve süreç her hâlükârda 0 ile
    çıkıyordu. Kırmızı yanan bir kapı "geçti" gibi okunuyordu; 8–12 dakikalık
    bir çıktının içindeki tek satırlık `KALIR` eninde sonunda kaçırılır.
    Projenin kendi dersinin ikizi: *okunmayan kapı da kapı değildir.*
    """
    print("=" * 78)
    taban = KARISTIRICI_GUCU_DBM[sinif]
    print(f"AILE RAPORU — bes tehdit ailesi, hepsi {taban:.1f} dBm TABAN "
          f"toplam gucunde")
    print("=" * 78)
    print("  🔒 SERT KISIT: 30 tohumun hicbirinde BIRDEN FAZLA COK UYELI")
    print("     bilesen YOK. Ailelerde bolunme 3 s'den (RFC 3561) uzun")
    print("     surer, cunku acik evre 15 s ya da sureklidir.")
    print("  🔒 rho bir SONUCTUR, hedef degil: aileler YAYILAN ORTALAMA GUC")
    print("     uzerinden esitlenir. Asagidaki 'pay' sutunu bunu DOGRULAR.")
    print(f"  {len(list(TOHUMLAR))} tohum x {len(ORNEK_ANLARI)} an")
    print()
    print(f"  {'aile':>14} {'K':>3} {'toplam pay':>11} {'rho':>7} "
          f"{'ulas':>7} {'bogulan':>8} {'AYRILAN':>9} {'olcut':>8}")
    bozan = []
    for aile in TEHDIT_SENARYOLARI:
        k, pay = _aile_gucu(aile)
        s = olc_aile(aile, sinif)
        gecti = s["ayrilan_tohum"] == 0.0
        if not gecti:
            bozan.append(aile)
        print(f"  {aile:>14} {k:>3} {pay:>11.3f} {s['rho']:>7.3f} "
              f"{s['ulasilabilirlik']:>7.3f} {s['yalniz_dugum']:>8.2f} "
              f"{int(s['ayrilan_tohum']):>6}/{len(list(TOHUMLAR))} "
              f"{'GECER' if gecti else '🔴 KALIR':>8}")
    print()
    print("  'toplam pay' her ailede 1,000 olmali — esitleme dogrulamasi.")
    if bozan:
        print(f"  🔴 SERT KISITI CIGNEYEN AILE(LER): {', '.join(bozan)}")
        print("     Bu bir BULGUDUR: o ailede ag boluniyor ve olculen sey")
        print("     yonlendirme degil bolunme olur. Karar ogrenciye gider.")
    else:
        print("  🟢 BES AILE DE SERT KISITI GECIYOR — calisma noktasi,")
        print("     tehdit kumesi eklendikten SONRA da gecerli.")
    return not bozan



# 🔒 AÇIK EVREYE KİLİTLENMİŞ ANLAR — `ORNEK_ANLARI` darbeli SINIFIN 2,7 s
# periyoduyla örtüşmeyi kırmak için seçilmişti; çevrimli AİLELERİN periyodu
# 30 s ve o ızgarada 9 anın yalnız 4'ü açık evreye düşüyor. Bölünme yalnız
# açık evrede olabilir (kapalıyken karıştırıcı hiç yok), dolayısıyla karma
# ızgarada okunan "ayrılan tohum" bir ALT SINIRDIR. Burada dokuzu da açık:
# üç AYRI çevrim × evre başı/ortası/sonu.
ACIK_EVRE_ANLARI = tuple(150.0 + 30.0 * m + u
                         for m in (2, 3, 4) for u in (1.0, 7.0, 13.0))
# Teşhis varyantının batıya kaydırılmış x'i — 0,75 yerine.
TESHIS_X = 0.60
CEVRIMLI_AILELER = ("hedef_koruma", "derin_sizma")


def acik_evre_raporu() -> bool:
    """🔒 Çevrimli aileler, örneklem AÇIK EVREYE kilitlenmiş hâliyle.

    Ölçüt DEĞİŞMEZ (birden fazla çok üyeli bileşen yok); değişen tek şey
    ölçümün ONU GÖREBİLECEĞİ yerde yapılmasıdır. ⚠️ Buradaki ρ AÇIK EVRE
    ρ'sudur ve karma ızgaradaki değerle doğrudan kıyaslanamaz — o, sessiz
    anları da ortalıyordu (karma × 9/4 ≈ açık evre).

    🔒 VERDİKT DÖNER (16 Eylül 2026) — `aile_raporu` ile aynı gerekçe.
    """
    global ORNEK_ANLARI
    print("=" * 78)
    print("CEVRIMLI AILELER — dokuz anin dokuzu da ACIK EVREDE")
    print("=" * 78)
    print(f"  anlar: {ACIK_EVRE_ANLARI}")
    print(f"  {'aile':>14} {'acik evre rho':>14} {'ulas':>7} {'bogulan':>8} "
          f"{'AYRILAN':>9} {'olcut':>8}")
    onceki = ORNEK_ANLARI
    ORNEK_ANLARI = ACIK_EVRE_ANLARI
    hepsi = True
    try:
        for aile in CEVRIMLI_AILELER:
            s = olc_aile(aile)
            gecti = s["ayrilan_tohum"] == 0.0
            hepsi &= gecti
            print(f"  {aile:>14} {s['rho']:>14.3f} {s['ulasilabilirlik']:>7.3f} "
                  f"{s['yalniz_dugum']:>8.2f} "
                  f"{int(s['ayrilan_tohum']):>6}/{len(list(TOHUMLAR))} "
                  f"{'GECER' if gecti else '🔴 KALIR':>8}")
    finally:
        ORNEK_ANLARI = onceki
    return hepsi


def hedef_teshisi() -> None:
    """🔴 `hedef_koruma` sert kısıtı NEDEN çiğniyordu — TEŞHİS, seçim değil.

    Aile iki şeyde birden `tekli_merkez`den ayrılıyordu ve hangisinin
    bölünmeyi ürettiği ölçülmeden bilinemezdi:
      (a) ÇEVRİM — %50 görev çevrimi, pay 1/(2×0,5) = 1,0, açıkken toplam
          TEPE güç tabanın iki katı
      (b) KONUM  — iki üye x = 0,75'te, doğu çeyreğini kesecek yerde

    Ölçüldü (30 tohum): V1 sürekli yayında 0/30 · V2 çevrim kalırken x =
    0,60'ta yine 2/30. Yani konumu kaydırmak kurtarmıyor, tepe gücünü
    tabana indirmek kurtarıyor (K-127).

    ⚠️ BU BÖLÜM `sim2.kanal.kanal.tehdit_tanimlari`yı GEÇİCİ olarak
    değiştirir. Bir ölçüm aletinde bu ancak teşhis için kabul edilebilir:
    ölçülen şey depodaki tanım değil, ONUN İKİ VARYANTIDIR. `finally` ile
    geri alınır ve başka hiçbir bölüm bu yoldan geçmez.
    """
    import sim2.kanal.kanal as kanal_mod
    from sim2.kanal.karistirici import KaristiriciTanimi, Yayin, Yorunge

    def uretici(surekli: bool, x: float, ozgun):
        def yenisi(konfig):
            if konfig.tehdit_senaryosu != "hedef_koruma":
                return ozgun(konfig)
            if surekli:
                yayin, pay = Yayin(), 0.5
            else:
                yarim = 15.0
                yayin = Yayin(duzen="gorev_cevrimli", acik_s=yarim,
                              sessiz_s=yarim)
                pay = 1.0
            return tuple(KaristiriciTanimi(
                platform="sabit_yer",
                yorunge=Yorunge(baslangic=(x, (2 * i + 1) / 4)),
                yayin=yayin, guc_payi=pay) for i in range(2))
        return yenisi

    global ORNEK_ANLARI
    print("=" * 78)
    print("hedef_koruma TESHISI — sert kisiti ne cigniyordu?")
    print("=" * 78)
    print("  🔒 V0 KALDIRILAN TASARIMDIR (cevrim, x=0,75) ve burada YASIYOR:")
    print("     depodan silinen bir sayinin ureticisi de silinmis olurdu.")
    print("  Iki izgara: 'karma' = ORNEK_ANLARI (9 anin 4'u acik evrede),")
    print("              'acik'  = ACIK_EVRE_ANLARI (dokuzu da acik evrede).")
    print()
    print(f"  {'varyant':>34} {'izgara':>7} {'rho':>7} {'ulas':>7} "
          f"{'bogulan':>8} {'AYRILAN':>9}")
    ozgun = kanal_mod.tehdit_tanimlari
    onceki = ORNEK_ANLARI
    try:
        for etiket, surekli, x in (
                ("V0 KALDIRILAN (cevrim, x=0,75)", False, 0.75),
                ("V1 surekli yayin (tepe = taban)", True, 0.75),
                (f"V2 cevrim kalir, x={TESHIS_X:.2f}", False, TESHIS_X)):
            kanal_mod.tehdit_tanimlari = uretici(surekli, x, ozgun)
            for izgara, anlar in (("karma", onceki),
                                  ("acik", ACIK_EVRE_ANLARI)):
                ORNEK_ANLARI = anlar
                s = olc_aile("hedef_koruma")
                print(f"  {etiket:>34} {izgara:>7} {s['rho']:>7.3f} "
                      f"{s['ulasilabilirlik']:>7.3f} {s['yalniz_dugum']:>8.2f} "
                      f"{int(s['ayrilan_tohum']):>6}/{len(list(TOHUMLAR))}")
            print()
    finally:
        kanal_mod.tehdit_tanimlari = ozgun
        ORNEK_ANLARI = onceki
    print("  🔒 Surekli varyantta iki izgara AYNI sayiyi vermeli: hep acik")
    print("     olan bir karistiricida 'acik evre' diye ayri bir evre yoktur.")


if __name__ == "__main__":
    # 🔒 KAPI OLAN BÖLÜM VERDİKT DÖNER, ÖLÇÜM OLAN BÖLÜM `None` (16 Eylül 2026).
    # `tarama`, `sinif` ve `hedef_teshis` birer ÖLÇÜMDÜR: bir ölçütü yoktur,
    # dolayısıyla "kalabilecekleri" bir kapı da yoktur. `aile` ve `acik_evre`
    # sert kısıtı sınar ve verdikti artık ÇIKIŞ KODUNA bağlıdır.
    BOLUMLER = {"tarama": lambda: tarama("surekli"),
                "sinif": sinif_raporu, "aile": aile_raporu,
                "acik_evre": acik_evre_raporu,
                "hedef_teshis": hedef_teshisi}
    _verdiktler = [BOLUMLER[s]() for s in (sys.argv[1:] or ["sinif"])]
    _kapilar = [v for v in _verdiktler if isinstance(v, bool)]
    if _kapilar and not all(_kapilar):
        raise SystemExit("🔴 KAPI KALDI — yukarıdaki sert kısıt ihlali okunmalı")
