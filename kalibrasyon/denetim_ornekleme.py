"""
ÖRNEKLEME DENETİMİ — "dokuz an mı, bir an mı" sorusunun ÖLÇÜLMÜŞ cevabı.

Üretici:
    PYTHONIOENCODING=utf-8 python kalibrasyon/denetim_ornekleme.py

🔴 NEDEN VAR
============
`karistirici_gucu.py`de ρ, dokuz anda örneklenen karıştırılmış dereceyi TEK
anda örneklenen temiz dereceye bölüyor. 8 Eylül devrinde bu bir ASİMETRİ
şüphesi olarak düşüldü: *"payda sönümleme gürültüsü taşıyor, pay taşımıyor."*

Aynı devirde ikinci bir iddia daha vardı: *"`surekli` zamanla değişmez,
dolayısıyla an sayısı sonucu değiştirmez."* O da ÖLÇÜLMEMİŞTİ.

🔒 Bu betik ikisini de iddia olmaktan çıkarır. Ölçtüğü şey ORTALAMA değil,
**BİREBİR KENAR KÜMESİ**: iki an aynı grafiği veriyorsa kenar kümeleri
aynıdır. Ortalama derece eşit çıkıp kenarların yer değiştirmesi mümkündür
(K-096'daki Jaccard 0,53 tuzağı) — o yüzden derece değil, küme sınanır.

⚠️ SINANAN ŞEY BİR YAPISAL BEKLENTİDİR:
    · statik kolda sönümleme dondurulmuş  (`sonumleme.py`: `_donuk` → k=0, M=1)
    · karıştırıcı gücü YAVAŞ kayıptan geçer (`karistirici.py::_yayilim_kaybi_w`
      yalnız `yavas_kayip_db` çağırır — hızlı sönümleme yok)
    · `Surekli.acik_mi` her t'de True
Üçü birden doğruysa `statik-yok` ve `statik-surekli` grafikleri t ≥ açılma
anı için zamandan BAĞIMSIZDIR. Beklenti bu; ölçüm onu sınar. Beklentiyi
doğrulamak için değil, YANLIŞLAMA ŞANSI VERMEK için koşulur.
"""

from __future__ import annotations

import statistics as ist
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from sim2.yapilandirma.senaryolar import KARISTIRICI_SINIFLARI  # noqa: E402
from kalibrasyon.kahin import KanalGrafigi  # noqa: E402
from kalibrasyon.karistirici_gucu import ORNEK_ANLARI, TOHUMLAR  # noqa: E402

SINIFLAR = tuple(s for s in KARISTIRICI_SINIFLARI if s != "yok")


def _graf(senaryo: str, tohum: int, t_s: float) -> KanalGrafigi:
    kfg = Konfig(kol="rho", senaryo=senaryo, tohum=tohum)
    g = KanalGrafigi(kurulum_yap(kfg))
    g.ozet(t_s)                       # `_tazele` bu an için kurar
    return g


def _kenarlar(g: KanalGrafigi) -> frozenset[tuple[int, int]]:
    return frozenset((i, j) for i, komsu in enumerate(g._komsu)
                     for j in komsu if i < j)


def _ozet_ve_kenar(senaryo: str, tohum: int, t_s: float):
    kfg = Konfig(kol="rho", senaryo=senaryo, tohum=tohum)
    g = KanalGrafigi(kurulum_yap(kfg))
    return g.ozet(t_s), _kenarlar(g)


# ==========================================================================
def a_zaman_degismezligi(senaryolar=("statik-yok", "statik-surekli",
                                     "statik-aldatici")) -> bool:
    """Dokuz anın kenar kümeleri BİREBİR aynı mı — 30 tohum.

    🔒 KAPI (16 Eylül 2026): her senaryoda 30/30 tohum **ve** en küçük
    Jaccard = 1,0000. Aşağıdaki cümle zaten bir ölçüt ilan ediyordu, ama
    verdikt yalnız ekrana basılıyor, süreç her hâlükârda 0 ile çıkıyordu.
    """
    print("=" * 78)
    print("A · ZAMAN DEGISMEZLIGI — dokuz anin KENAR KUMELERI")
    print("=" * 78)
    print(f"  anlar: {ORNEK_ANLARI}")
    print(f"  {'senaryo':>18} {'kenar kumesi 9 anda AYNI':>26} "
          f"{'derece(min..maks)':>22} {'en kucuk Jaccard':>17}")
    hepsi = True
    for sen in senaryolar:
        ayni = 0
        dereceler: list[float] = []
        en_kucuk_j = 1.0
        for tohum in TOHUMLAR:
            kumeler = []
            for t in ORNEK_ANLARI:
                o, k = _ozet_ve_kenar(sen, tohum, t)
                kumeler.append(k)
                dereceler.append(o["derece"])
            ilk = kumeler[0]
            ayni += all(k == ilk for k in kumeler)
            for k in kumeler[1:]:
                birlesim = len(ilk | k)
                if birlesim:
                    en_kucuk_j = min(en_kucuk_j, len(ilk & k) / birlesim)
        gecti = ayni == len(list(TOHUMLAR)) and en_kucuk_j == 1.0
        hepsi &= gecti
        print(f"  {sen:>18} {ayni:>13}/{len(list(TOHUMLAR))} tohum "
              f"{min(dereceler):>10.3f}..{max(dereceler):<10.3f} "
              f"{en_kucuk_j:>17.4f} {'GECTI' if gecti else '🔴 KALDI':>9}")
    print()
    print("  🔒 '30/30 tohum' + 'Jaccard 1,0000' = grafik zamandan BAGIMSIZ.")
    print("     O zaman an sayisi rho'yu DEGISTIREMEZ; iddia olcume dondu.")
    return hepsi


# ==========================================================================
def b_paydanin_duyarliligi() -> None:
    """ρ'nun paydası tek anda mı dokuz anda mı — fark ne? (§3.3)"""
    print()
    print("=" * 78)
    print("B · RHO'NUN PAYDASI — tek an mi, dokuz an mi")
    print("=" * 78)
    temiz_tek: dict[int, float] = {}
    temiz_dokuz: dict[int, float] = {}
    for tohum in TOHUMLAR:
        d = [_ozet_ve_kenar("statik-yok", tohum, t)[0]["derece"]
             for t in ORNEK_ANLARI]
        temiz_tek[tohum] = d[0]
        temiz_dokuz[tohum] = ist.mean(d)
    yayilim = max(abs(temiz_tek[s] - temiz_dokuz[s]) for s in TOHUMLAR)
    print(f"  temiz derece — tek an ortalamasi  : "
          f"{ist.mean(temiz_tek.values()):.6f}")
    print(f"  temiz derece — dokuz an ortalamasi: "
          f"{ist.mean(temiz_dokuz.values()):.6f}")
    print(f"  tohum basina EN BUYUK fark        : {yayilim:.9f}")
    print()
    print(f"  {'sinif':>17} {'rho (payda TEK an)':>20} "
          f"{'rho (payda DOKUZ an)':>22} {'fark':>10}")
    for sinif in SINIFLAR:
        r_tek, r_dokuz = [], []
        for tohum in TOHUMLAR:
            for t in ORNEK_ANLARI:
                o = _ozet_ve_kenar(f"statik-{sinif}", tohum, t)[0]
                r_tek.append(1.0 - o["derece"] / temiz_tek[tohum]
                             if temiz_tek[tohum] else 0.0)
                r_dokuz.append(1.0 - o["derece"] / temiz_dokuz[tohum]
                               if temiz_dokuz[tohum] else 0.0)
        a, b = ist.mean(r_tek), ist.mean(r_dokuz)
        print(f"  {sinif:>17} {a:>20.6f} {b:>22.6f} {abs(a - b):>10.2e}")


# ==========================================================================
def c_aldatici_acik_mi() -> bool:
    """`aldatici` DOKUZ ÖRNEK ANININ HEPSİNDE açık mı? (§3.4)

    🔒 KAPI (16 Eylül 2026): `aldatici` ile `surekli` kenar kümeleri
    270/270'te birebir aynı olmalı. *"Tek fark CSMA görünürlüğü"*
    eşleştirilmiş kontrastı bu eşitliğe dayanıyor (bölüm F onun ARTIĞINI
    ölçer); eşitlik bozulursa kontrast iddiası dayanaksız kalır.
    """
    print()
    print("=" * 78)
    print("C · SINIFLARIN ORNEK ANLARINDAKI DURUMU")
    print("=" * 78)
    print("  🔒 `_acik_orani` SUREKLI bir tarama yapar (150→350 s, 10 ms).")
    print("     Ama rho SADECE dokuz anda okunur. Iki soru AYRIDIR:")
    print("     'sinif ne kadar acik' ile 'orneklendigi anda acik miydi'.\n")
    print(f"  {'sinif':>17} {'ornek anlarinda ACIK':>22} {'desen':>12}")
    for sinif in SINIFLAR:
        kfg = Konfig(kol="rho", senaryo=f"statik-{sinif}", tohum=1000)
        kar = kurulum_yap(kfg).kanal.karistirici
        durum = [bool(kar.acik_mi(t)) for t in ORNEK_ANLARI]
        desen = "".join("1" if d else "0" for d in durum)
        print(f"  {sinif:>17} {sum(durum):>13}/{len(ORNEK_ANLARI)} an "
              f"{desen:>12}")
    print()
    print("  Ayrica: `aldatici` ile `surekli` KENAR KUMELERI birebir ayni mi?")
    ayni = 0
    toplam = 0
    for tohum in TOHUMLAR:
        for t in ORNEK_ANLARI:
            ka = _ozet_ve_kenar("statik-aldatici", tohum, t)[1]
            ks = _ozet_ve_kenar("statik-surekli", tohum, t)[1]
            ayni += (ka == ks)
            toplam += 1
    gecti = ayni == toplam
    print(f"    birebir ayni: {ayni}/{toplam} (tohum x an) "
          f"{'GECTI' if gecti else '🔴 KALDI'}")
    return gecti


# ==========================================================================
def d_temiz_grafik_butunlugu() -> bool:
    """Temiz grafik DOKUZ ANIN HEPSİNDE tek parça mı? (§3.6 sıkılaştırma)

    🔒 KAPI (16 Eylül 2026): 270/270. K-103'ün sert kısıtının ilk dayanağı
    budur ve bölüm G'nin kanıtı buna yaslanır.

    ⚠️ Kapı 30 tohumda okunuyor. C1 (K-125) 120 tohumla kopukluk olasılığını
    %0,8 ölçtü — yani bu kapı bir gün MEŞRU olarak kırmızı yanabilir ve o
    zaman cevap kapıyı gevşetmek değil, çalışma noktasını yeniden
    tartışmaktır.
    """
    print()
    print("=" * 78)
    print("D · TEMIZ GRAFIGIN BUTUNLUGU — dokuz anin hepsinde")
    print("=" * 78)
    kirik = []
    for tohum in TOHUMLAR:
        for t in ORNEK_ANLARI:
            o = _ozet_ve_kenar("statik-yok", tohum, t)[0]
            if o["cok_uyeli_bilesen"] > 1.0 or o["yalniz_dugum"] > 0.0:
                kirik.append((tohum, t, o["cok_uyeli_bilesen"],
                              o["yalniz_dugum"]))
    n = len(list(TOHUMLAR)) * len(ORNEK_ANLARI)
    print(f"  tek parca (cok uyeli bilesen = 1, yalniz dugum = 0): "
          f"{n - len(kirik)}/{n} {'GECTI' if not kirik else '🔴 KALDI'}")
    for k in kirik[:10]:
        print(f"    🔴 tohum {k[0]} t={k[1]:.1f}: bilesen {k[2]} "
              f"yalniz {k[3]}")
    return not kirik


# ==========================================================================
def e_darbe_fazi() -> None:
    """Dokuz an darbe fazını gerçekten düzgün örtüyor mu? (sayı teorisi iddiası)"""
    print()
    print("=" * 78)
    print("E · DARBE FAZININ ORTULMESI")
    print("=" * 78)
    kfg = Konfig(kol="rho", senaryo="statik-surekli_darbeli", tohum=1000)
    periyot = kfg.darbe_periyodu_s
    cevrim = kfg.darbe_gorev_cevrimi
    fazlar = sorted((t % periyot) / periyot for t in ORNEK_ANLARI)
    print(f"  periyot {periyot} s · gorev cevrimi {cevrim}")
    print(f"  dokuz anin NORMALIZE fazi: "
          f"{', '.join(f'{f:.3f}' for f in fazlar)}")
    print(f"  ornek anlarinda ACIK olan: "
          f"{sum(1 for f in fazlar if f < cevrim)}/{len(fazlar)} "
          f"(beklenen ~{cevrim * len(fazlar):.1f})")
    # Düzgünlük: ardışık fazlar arası aralıkların yayılımı.
    araliklar = [fazlar[i + 1] - fazlar[i] for i in range(len(fazlar) - 1)]
    araliklar.append(1.0 - fazlar[-1] + fazlar[0])
    print(f"  faz araliklari min {min(araliklar):.4f} maks "
          f"{max(araliklar):.4f} (duzgun olsa hepsi "
          f"{1.0 / len(fazlar):.4f})")


# ==========================================================================
def f_aldatici_artik_farki() -> None:
    """`aldatici` ↔ `surekli` kontrastı ÇERÇEVE düzeyinde de eşleşiyor mu?

    🔴 A ve C bölümleri kanal grafiğinde BİREBİR eşitlik buldu. Ama o prob
    TRAFİKSİZDİR ve yalnız dokuz ANI örnekler. Aldatıcı zamanın %97,8'inde
    açıktır — kalan %2,2 (DIFS boşlukları) dokuz anın hiçbirine düşmedi.

    ⚠️ Çerçeve düzeyinde durum farklı: `alim_per` çerçeveyi parça parça
    integre eder, yani kapalı geçen her parça aldatıcının hasarını AZALTIR.
    "Eşleştirilmiş kontrast" iddiası (*"tek fark CSMA"*) bu artığın büyüklüğü
    ölçülmeden tam olarak doğru değildir.

    🔒 Ölçüm, PER'i ARA BANTTA (0,02–0,98) olan bağlarda yapılır: doymuş
    bağlarda (PER 0 ya da 1) hiçbir görev çevrimi farkı görünmez, yani orada
    ölçmek farkı yapay olarak sıfır gösterirdi.
    """
    print()
    print("=" * 78)
    print("F · ALDATICI ARTIGI — cerceve duzeyinde eslesme ne kadar tam")
    print("=" * 78)
    from sim2.kanal.cerceve import cerceve_kur
    from sim2.kanal.kanal import Kanal
    from sim2.dunya.geometri import mesafe
    from sim2.dunya.topoloji import topoloji_kur
    from sim2.cekirdek.rng import Akislar

    kan = {}
    for s in ("yok", "surekli", "aldatici"):
        k = Konfig(kol="denetim", senaryo=f"statik-{s}", tohum=1000)
        kan[s] = Kanal(k, topoloji_kur(k, Akislar(1)))
    kfg = kan["yok"].konfig
    cerceve = cerceve_kur(kfg, "veri")
    top = kan["yok"].topoloji
    anlar = [200.0 + 0.00037 * m for m in range(120)]

    def _per(kanal, i, j):
        return ist.mean(kanal.alim_per(i, j, cerceve, bas_s=t) for t in anlar)

    ara, en_buyuk = [], (0.0, None)
    for i in range(kfg.dugum_sayisi):
        for j in range(i + 1, kfg.dugum_sayisi):
            if (mesafe(top.konum(i, 200.0), top.konum(j, 200.0))
                    > kfg.girisim_menzili_m):
                continue
            ps = _per(kan["surekli"], i, j)
            if not 0.02 < ps < 0.98:
                continue
            pa = _per(kan["aldatici"], i, j)
            ara.append(ps - pa)
            if abs(ps - pa) > en_buyuk[0]:
                en_buyuk = (abs(ps - pa), (i, j, ps, pa))
    print(f"  ara bantta (0,02 < PER < 0,98) bag sayisi : {len(ara)}")
    if not ara:
        print("  🔴 ara bantta bag yok — olcum bir sey soylemiyor")
        return
    print(f"  surekli − aldatici PER farki, ortalama    : {ist.mean(ara):+.6f}")
    print(f"  ayni fark, EN BUYUK mutlak deger          : {en_buyuk[0]:.6f}")
    i, j, ps, pa = en_buyuk[1]
    print(f"    (bag {i}-{j}: surekli {ps:.6f} ↔ aldatici {pa:.6f})")
    print()
    print("  🔒 Fark POZITIF bekleniyor: aldatici zamanin %2,2'sinde kapali,")
    print("     yani biraz DAHA AZ hasar verir. Isaret negatifse model yanlis.")
    print("  ⚠️ 'Eslestirilmis kontrast' iddiasi bu artikla birlikte okunur:")
    print("     bag hasari kanal grafiginde BIREBIR ayni, cerceve duzeyinde")
    print("     ise bu kadar sapiyor. Fark saf CSMA degil, CSMA + bu artik.")


# ==========================================================================
def g_darbe_kapali_evre() -> bool:
    """Darbeli karıştırıcının KAPALI evresi gerçekten temiz grafik mi?

    🔴 NEDEN ÖNEMLİ — K-103'ün en zayıf halkası burası.
    Sert kısıtın zaman anlamı şöyle netleştirildi: *"bölünme, en hızlı taban
    çizgisinin rota geçersizleme süresinden (AODV 3 s) uzun sürmeyecek"*.
    Dayanağı iki gözlemdi: (1) temiz grafik 30/30 tohumda tek parça,
    (2) ayrılan tohumun **dört örneğinin dördü de** darbenin AÇIK evresinde.

    ⚠️ (2) bir ÇIKARIMDIR, kanıt değil: dört örnek, bölünmenin açık evreyle
    ÇAKIŞTIĞINI gösterir, kapanınca BİTTİĞİNİ değil. Sınır 1,35 s ancak
    kapalı evrede ağın bütün olduğu KANITLANIRSA geçerlidir.

    🔒 Yapısal iddia şudur: `acik_mi` yanlışken `alinan_guc_w` **sıfır**
    döner, yani kanal karıştırıcısız kanalın ta kendisidir. Doğruysa kapalı
    evre grafiği `statik-yok` ile BİREBİR aynı olmalı — ve `statik-yok`
    270/270 noktada tek parça (bölüm D). O zaman bölünme yapısal olarak
    açık evreyle sınırlıdır ve süresi ≤ açık süre (1,35 s) olur.

    Bu bölüm o iddiayı ölçer: çıkarımı kanıta çevirir ya da çürütür.
    """
    print()
    print("=" * 78)
    print("G · DARBELININ KAPALI EVRESI — cikarimi kanita cevirmek")
    print("=" * 78)
    kfg = Konfig(kol="denetim", senaryo="statik-surekli_darbeli", tohum=1000)
    kar = kurulum_yap(kfg).kanal.karistirici
    periyot = kfg.darbe_periyodu_s
    acik_sure = periyot * kfg.darbe_gorev_cevrimi
    # Kapalı evrenin ortasına düşen dokuz an — açılmadan SONRA.
    kapali = tuple(200.0 + k * periyot + acik_sure + 0.5 * (periyot - acik_sure)
                   for k in range(9))
    print(f"  periyot {periyot} s · acik sure {acik_sure} s")
    print(f"  sinanan KAPALI anlar: "
          f"{', '.join(f'{t:.2f}' for t in kapali)}")
    print(f"  hepsi gercekten kapali mi: "
          f"{all(not kar.acik_mi(t) for t in kapali)}")
    ayni = tek_parca = 0
    toplam = 0
    for tohum in TOHUMLAR:
        temiz_k = _ozet_ve_kenar("statik-yok", tohum, kapali[0])[1]
        for t in kapali:
            o, k = _ozet_ve_kenar("statik-surekli_darbeli", tohum, t)
            ayni += (k == temiz_k)
            tek_parca += (o["cok_uyeli_bilesen"] <= 1.0)
            toplam += 1
    print(f"\n  kapali evre grafigi == temiz grafik : {ayni}/{toplam}")
    print(f"  kapali evrede tek parca             : {tek_parca}/{toplam}")
    if ayni == toplam:
        print("\n  🟢 KANIT TAMAM: kapali evrede ag, karistiricisiz agin")
        print("     BIREBIR aynisi. Bolunme yapisal olarak ACIK evreyle")
        print(f"     sinirli, yani suresi <= {acik_sure} s. AODV'nin 3 s'lik")
        print("     rota gecersizleme suresinin altinda — K-103 ayakta.")
    else:
        print("\n  🔴 IDDIA COKTU: kapali evre temiz grafik DEGIL. K-103'un")
        print("     1,35 s siniri dayanaksiz kalir ve taban gucu yeniden")
        print("     bakilmalidir.")
    return ayni == toplam


if __name__ == "__main__":
    # 🔒 DÖRDÜ KAPI, ÜÇÜ ÖLÇÜM (16 Eylül 2026).
    # Kapı olanlar (a · c · d · g) ilan edilmiş bir ölçüte karşı verdikt
    # üretir ve verdikt artık ÇIKIŞ KODUNA bağlıdır. Ölçüm olanların
    # (b · e · f) bir ölçütü YOKTUR: `b` paydanın duyarlılığını, `e` faz
    # örtmesini, `f` aldatıcı artığını RAPORLAR. Bir ölçümü kapıya çevirmek,
    # sayının kendisini sonradan uydurulmuş bir eşik gibi okumak olurdu.
    BOLUMLER = {"a": a_zaman_degismezligi, "b": b_paydanin_duyarliligi,
                "c": c_aldatici_acik_mi, "d": d_temiz_grafik_butunlugu,
                "e": e_darbe_fazi, "f": f_aldatici_artik_farki,
                "g": g_darbe_kapali_evre}
    _verdiktler = [BOLUMLER[s]()
                   for s in (sys.argv[1:] or ["e", "c", "a", "d", "b", "f", "g"])]
    _kapilar = [v for v in _verdiktler if isinstance(v, bool)]
    print()
    print(f"  🔒 KAPI OZETI: {sum(_kapilar)}/{len(_kapilar)} GECTI")
    if _kapilar and not all(_kapilar):
        raise SystemExit("🔴 KAPI KALDI — yukaridaki kirmizi satir okunmali")
