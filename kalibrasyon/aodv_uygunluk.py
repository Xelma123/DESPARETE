"""
U1 — AODV'nin teslim oranı kâhin referansına YAKIN mı? (`v2/06` §4.3)

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py --protokol olsrv2
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py --protokol desparete
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 \
        --desen yere_toplama --protokol aodv,olsrv2,babel,desparete
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py duman
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py hukum [kayit]
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py u3

🔒 BÜTÜN TABAN PROTOKOLLERİN U1 KAPISI — adı TARİHSELDİR (19 Eylül 2026)
Eşikler üç taban protokolü birden bağlar (K-136); dolayısıyla hüküm kodu TEK
kalmalı — her protokol için ayrı bir alet yazmak, iki hükmün bir gün ayrışması
demek olurdu. Protokol bir argümandır; açıklanmış düşük hücre listesi
protokol başınadır. Dosya adı AODV ilk protokol olduğu için böyle kaldı:
adı değiştirmek köken defterindeki ve belgelerdeki atıfları kırardı.
🔒 DESPARETE de AYNI hüküm koduyla ve aynı eşiklerle sınanır — tek fark
deseni: yere toplama, kâhin de o desende (K-150 §4 · K-160).

🔴 BU DOSYA NEDEN VAR — BİR KAPI YANLIŞ YERDE KURULMUŞTU
========================================================
U1'in ilk hâli `tests2/test_aodv.py` içinde MUTLAK bir eşikti: `PDR ≥ 0,95`.
Eşik gevşek ya da sıkı olduğu için değil, **yanlış dünyada** durduğu için
yanlıştı. `06` §4.3'ün ölçütü *"teslim oranı KÂHİN REFERANSINA yakın"*dır ve
o referans konfigürasyona bağlıdır; tam ölçekte ölçülmüş bir referans
(0,996–1,000) 14 düğümlük test dünyasına taşınmıştı. Aynı dünyada ölçünce:

    kâhin 0,9687  ·  AODV 0,8512  ·  oran 0,879

Yani test kırmızıydı ama gösterdiği şey protokolün kusuru değil, kapının
kendi kusuruydu. Bir kapı neyi ölçtüğünü bilmiyorsa, kırmızı yanması bir
teşhis değildir.

🔒 ÖLÇÜT ORANDIR, MUTLAK DEĞER DEĞİL
====================================
Kapı AODV'yi **aynı konfigürasyonda** koşan ETX kâhinine oranlar:

    oran = PDR(AODV) / PDR(EnGuvenilirKahin)

Oranın üç kazancı var:
  1. *"Yakın"* sözcüğü ölçülebilir hâle gelir — neye yakın olduğu yazılıdır.
  2. §4.3'ün *"bağlı ağ"* ön koşulu **kendini nötrler**: kâhinin geçemediği
     bir bölünme paydayı da düşürür, dolayısıyla topolojinin kusuru
     protokolün hanesine yazılmaz. Ayrı bir bağlantılılık taraması gerekmez.
  3. Kâhin MAC'i, kanalı, kuyruğu ve TTL'i değiştirmez (`pdr_tavani.py`);
     yani payda *"yönlendirme hiç hata yapmasaydı"* demektir ve oran tam
     olarak **yönlendirmenin payını** ölçer.

🔒 EŞİKLER — ÖĞRENCİ KARARI, 17 Eylül 2026 (`04` K-136)
=======================================================
    statik kol     oran ≥ 0,90
    hareketli kol  oran ≥ 0,60

Hareketli kolun eşiği neden bu kadar düşük: kâhin her an en güvenilir yolu
BİLİR; gerçek bir protokol o yolu HELLO gecikmesi kadar sonra öğrenir ve
hareket, bağları kâhinin hiç ödemediği bir hızda kırar. `06` §4.3 bunu zaten
söylüyordu — *"«≈ 1» yalnız statik kolda anlamlıdır"*.

🔴 EŞİK, SAYILAR GÖRÜLDÜKTEN SONRA SEÇİLDİ — VE BU BİR ZAYIFLIKTIR
==================================================================
Ön-kayıt disiplini ölçütün ölçümden ÖNCE yazılmasını ister (`03` §2). Burada
öyle olmadı: öğrenciye dört ölçülmüş oran gösterildi ve eşiği onların üstünde
seçti. Bu gizlenmiyor; üç hafifletici sebeple birlikte yazılıyor:

  1. U1 bir **kabul kapısıdır**, bir hipotez testi değil. `06` §4.4 onu
     *"geçilmeden protokol kabul edilmez"* diye tanımlar; hiçbir sonuç
     iddiası bu eşiğe dayanmıyor ve dayanmayacak.
  2. Eşik **üç taban protokolü de** bağlayacak. AODV'ye göre ayarlanmış
     olması öteki taban protokollere bir avantaj sağlamaz — tersine, AODV'nin
     bugünkü değerine yakın bir eşik onlar için DAHA sıkıdır.
  3. Seçenekler, hangisinin bugün geçtiği açıkça yazılarak sunuldu.

⚠️ AÇIK BORÇ: eşiğin seçildiği dört sayı KISA PENCEREDE ölçülmüştü
(`ısınma 10 · ölçüm 40 · koşu 50 s`); bu alet GERÇEK pencerede koşar
(`50 · 320 · 350`). Aynı koşu tam pencerede 0,9875 değil **0,9777** verdi —
yön aşağı. Eşik buna rağmen DEĞİŞTİRİLMEDİ: sonuç görüldükten sonra bir
ölçütü gevşetmek de sıkmak da aynı hatadır (`03` §2.1). Tam pencerede ölçülen
değerler aşağıda basılıyor. Eşik sonradan her taban protokolün karşısında
sınandı ve değiştirilmedi (Faz 4: K-224 · Faz 4b: K-238, K-239).

🔴 KAPI İKİ PARÇADIR (17 Eylül 2026, K-137 · öğrenci kararı "A")
================================================================
İlk hâlinde U1 iki ayrı soruyu tek kapıya bağlıyordu — *"gerçekleme RFC'ye
sadık mı"* ve *"protokol iyi teslim ediyor mu"*. İkincisi bir kabul ölçütü
DEĞİL, deneyin kendi sonucudur: AODV'nin zayıf bağlı bir topolojide kötü
teslim vermesi, gerçeklemenin bozuk olduğunu göstermez — RFC 3561 atlama
sayısıyla yönlendirir ve **bağ kalitesi eşiği yoktur**.

    U1-U · UYGUNLUK   defter kapanıyor · teslim var · kâhin AŞILMIYOR
                      → kalırsa protokol KABUL EDİLMEZ
    U1-B · BAŞARIM    oran eşikleri
                      → kalırsa protokol reddedilmez, ama hücre
                        AÇIKLANMADAN geçemez

🔒 "AÇIKLANMADAN GEÇEMEZ" KAPININ DİŞİDİR — ve üç yönlü denetlenir:
  1. Eşiğin altındaki hücre `ACIKLANMIS_DUSUK`ta yoksa kapı KIRMIZI yanar.
  2. Listedeki bir hücre ARTIK düşük değilse o bir **ölü kayıttır** ve kapı
     yine KIRMIZI yanar — bir muafiyet listesi kendi bayatlığını gizleyemez
     (köken defterinin D12 taramasıyla aynı disiplin).
  3. Uygunluk parçası her hâlükârda bağlayıcıdır ve gevşetilemez.

🔒 KAPI ÇIKIŞ KODUNA BAĞLIDIR — geçti 0, kaldı 1.
"""

from __future__ import annotations

import json
import os
import statistics as ist
import sys
import time
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
for _yol in (KOK, KOK / "tests2"):
    if str(_yol) not in sys.path:
        sys.path.insert(0, str(_yol))

from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi  # noqa: E402
from protokoller.aodv import AODV  # noqa: E402
from protokoller.olsr import OLSR  # noqa: E402
from protokoller.aomdv import AOMDV  # noqa: E402
from protokoller.desparete import DESPARETE  # noqa: E402
from protokoller.jarmrout import JarmRout  # noqa: E402
from protokoller.olsrv2 import OLSRv2  # noqa: E402
from protokoller.babel import Babel  # noqa: E402
from protokoller.desparete_bayrak import PROFIL_V02, SECENEK_V041  # noqa: E402
from protokoller.desparete5 import Desparete5  # noqa: E402
from protokoller.desparete5_bicim import (  # noqa: E402
    CEKIRDEK, CEKIRDEK_19K, DEGERLER_ESKI, ESKI_CEKIRDEK, TAM)
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)

__all__ = ["U1_ESIK_STATIK", "U1_ESIK_HAREKETLI", "KOLLAR", "TOHUMLAR", "u1",
           "hukum", "PROTOKOLLER"]

# Kapının sınadığı protokoller — ad → sınıf.
PROTOKOLLER = {"aodv": AODV, "olsr": OLSR, "aomdv": AOMDV,
               "desparete": DESPARETE,
               # Faz 4b'nin rakipleri (K-229 · K-235 · K-236).
               "jarmrout": JarmRout, "olsrv2": OLSRv2,
               # Üçüncü rakip (K-242 · K-244).
               "babel": Babel,
               # Faz 5-3 · DESPARETE'nin yeni sürümü (`v2/17`, `v2/kural/`):
               # bütün bayraklar açık · karıştırmaya karşı mekanizmalar kapalı
               # (mekanizma kapısının "hepsi kapalı" kolu, KK-00).
               "desparete5": Desparete5, "desparete5_cekirdek": Desparete5,
               # 18 Kasım'ın çekirdeği (FD ve tur, eski veri tetiği; 19 Kasım):
               # ilk ölçümü ve açlık teşhisinin `cekirdek` kolunu birebir
               # üretmeli (`v2/kural/KK-00` genel kural 5).
               "desparete5_eski_cekirdek": Desparete5,
               # 19 Kasım'ın çekirdeği (KK-04 kural 13–14 öncesi; 20 Kasım):
               # yeni çekirdeğin ölçümündeki `cekirdek` kolunu birebir
               # üretmeli.
               "desparete5_cekirdek_19k": Desparete5}
# DESPARETE 5'in bayrak profilleri (`protokoller/desparete5_bicim.py`).
DESPARETE5_PROFILLERI = {"desparete5": TAM, "desparete5_cekirdek": CEKIRDEK,
                         "desparete5_eski_cekirdek": ESKI_CEKIRDEK,
                         "desparete5_cekirdek_19k": CEKIRDEK_19K}
# Varsayılandan ayrılan değerler (yoksa `Degerler()`).
DESPARETE5_DEGERLERI = {"desparete5_eski_cekirdek": DEGERLER_ESKI}
# 🔒 DESPARETE v0.1 tek-sink işletme profilidir: U1'i YERE TOPLAMADA koşulur
# (`04` K-150 §4 · K-160); kâhin AYNI desende koşar, oran aynı dünyanın
# oranıdır. Taban protokollerin U1'i eşler arası desende geçerli kalır.
TRAFIK_DESENI: dict[str, str] = {"desparete": "yere_toplama",
                                 "desparete5": "yere_toplama",
                                 "desparete5_cekirdek": "yere_toplama",
                                 "desparete5_eski_cekirdek": "yere_toplama",
                                 "desparete5_cekirdek_19k": "yere_toplama"}


# 🔒 Faz 4.3 (K-189) — `--desen esler_arasi|yere_toplama`: planın "U1 hem
# eşler arası hem yere toplama desenlerinde" maddesi. Ortam değişkeniyle
# taşınır ki havuz işçileri (Windows `spawn`) de görsün; kayıt dosyası
# desenin adını taşır, desenler birbirini ezmez.
DESEN_ORTAM = "DESPARETE_U1_DESEN"
DESENLER = ("esler_arasi", "yere_toplama")


def _desen_adi(protokol: str) -> str | None:
    """Protokolün U1 deseni — `--desen` verildiyse o, yoksa taban
    protokollerde `None` (`Konfig` varsayılanı; DESPARETE'de yere toplama)."""
    return os.environ.get(DESEN_ORTAM) or TRAFIK_DESENI.get(protokol)


def _desen(protokol: str) -> dict[str, str]:
    """`_desen_adi`nın `Konfig` argümanı hâli."""
    desen = _desen_adi(protokol)
    return {"trafik_deseni": desen} if desen else {}


def _kayit_adi(protokol: str) -> str:
    """Kayıt dosyasının adı — dünya soneki (K-183) ve verildiyse desen."""
    desen = os.environ.get(DESEN_ORTAM)
    ad = DS.etiket(protokol)
    return f"{ad}_{desen}" if desen else ad


def _fabrika(protokol: str, kfg: Konfig):
    """DESPARETE geçidi (SinkID) kurucudan alır — yapılandırma (`36` §2).
    Profil AÇIKÇA verilir: v0.4.1 (K-172; v0.4 K-167, v0.3 K-164). ⚠️
    `ciktilar2/aodv_uygunluk/desparete_*` v0.4 ve öncesiyle üretildi."""
    if protokol == "desparete":
        return lambda i: DESPARETE(i, kfg.gecit, bayraklar=PROFIL_V02,
                                   secenekler=SECENEK_V041)
    if protokol in DESPARETE5_PROFILLERI:
        bayraklar = DESPARETE5_PROFILLERI[protokol]
        degerler = DESPARETE5_DEGERLERI.get(protokol)
        return lambda i: Desparete5(i, kfg.gecit, bayraklar=bayraklar,
                                    degerler=degerler)
    return PROTOKOLLER[protokol]

# 🔒 Tam koşumun ölçtüğü hücreler buraya yazılır (`regresyon_satirlari.py`
# ile aynı gelenek). Sebebi ölçüldü, 19 Eylül 2026: açıklanmış hücre listesi
# değiştiğinde verdikti yeniden üretmek için 4 SAATLİK koşumu tekrarlamak
# gerekiyordu — oysa simülasyon deterministik ve ölçülen sayılar değişmez.
# `hukum` kipi aynı DEĞERLENDİRME KODUNU kayıtlı sayılara uygular; ikinci
# bir hüküm gerçeklemesi yazılmaz.
DIZIN = KOK / "ciktilar2" / "aodv_uygunluk"

# 🔒 ÖLÇÜTÜN KENDİSİ — öğrenci kararı (K-136). Tek kaynak burasıdır; başka
# hiçbir dosya bu iki sayıyı yeniden yazmaz.
U1_ESIK_STATIK: float = 0.90
U1_ESIK_HAREKETLI: float = 0.60

# 🔒 U1 KARIŞTIRICISIZDIR (`06` §4.3) — dört hareketlilik kolunun `-yok`
# senaryosu. Karıştırma altındaki davranış U1'in işi değil; onu H1 ailesi
# ölçer ve orada kâhin de bozulur.
KOLLAR: tuple[str, ...] = ("statik-yok", "bagimsiz-yok",
                           "gorev-yok", "formasyon-yok")
# 🔒 GELİŞTİRME TOHUMLARI. Ana deney tohumları (2000–2039) burada KOŞULMAZ —
# `06` §0.2: *"hiçbir kolda koşulmaz"*, mühür bozulmaz.
TOHUMLAR: tuple[int, ...] = (1000, 1001, 1002)
# 🔒 AÇIKLANMIŞ DÜŞÜK HÜCRELER (`06` §4.4 madde 3 · `04` K-137 §4).
# Bir hücrenin buraya girmesinin ŞARTI, kaybın bir yazılım kusurundan DEĞİL
# protokolün kendi mekanizmasından geldiğinin ÖLÇÜLMÜŞ olmasıdır. Üretici:
# yapısal ölçüm simülasyon koşmaz, doğrudan kanal grafiğinden okur.
# 🔴 Ayıran değişken TEK: eşiksiz en kısa yolun uçtan uca teslimi. AODV'nin
# bağ kalitesi kabul eşiği yoktur; hedef ilk ulaşan RREQ kopyasının ters
# yoluna cevap verir ve o kopya genelde en az atlamalı, yani en uzun bağlı
# olandır. Dört kolun DÖRDÜNDE de en düşük eşiksiz atlama yoluna sahip hücre,
# en düşük U1 oranına sahip.
# 🔒 PROTOKOL BAŞINA: bir protokolün açıklaması öbürünü aklamaz — her
# protokolün düşük hücresi KENDİ ölçümüyle açıklanır.
# 🔴 İKİ KAYIT ÖLÜ KAYIT TARAMASIYLA SİLİNDİ (19 Eylül 2026, `04` K-145).
# RFC §6.11 öncül kuralı düzelince (K-143, AODV-e) iki hücre eşiği geçti ve
# kapı onları kendiliğinden yakaladı — tasarlandığı gibi:
#     statik-yok/1002     0,897 → 0,932   (eşik 0,90)
#     formasyon-yok/1002  0,572 → 0,646   (eşik 0,60)
# ⚠️ statik-yok/1002'nin açıklaması (eşiksiz en kısa yol kolun en düşüğü)
# YANLIŞ DEĞİLDİ — hücre hâlâ statik kolun en düşüğü. Ama eşiğin altında
# kalmasının sebebi o yapıyla §6.11 kusurunun BİRLEŞİMİYDİ; kusur gidince
# hücre geçti. Açıklamanın TEK BAŞINA yeterli sayılması bir hataydı.
ACIKLANMIS_DUSUK: dict[str, dict[tuple[str, int], str]] = {"aodv": {
    ("bagimsiz-yok", 1002):
        "esiksiz en kisa yol 0,2386 (kolun en dusugu; 1000'de 0,4589). "
        "Ag hicbir anda bolunmuyor. K-137 §4",
    ("gorev-yok", 1001):
        "esiksiz en kisa yol 0,2502 (kolun en dusugu; 1000'de 0,5519). "
        "Ag hicbir anda bolunmuyor. K-137 §4",
}, "olsr": {}, "desparete": {}, "jarmrout": {}, "olsrv2": {}, "babel": {},
    "desparete5": {}, "desparete5_cekirdek": {},
    "desparete5_eski_cekirdek": {}, "desparete5_cekirdek_19k": {},
    "aomdv": {
    # 🔒 AOMDV, AODV'nin atlama sayısıyla yönlendirmesini miras alır; bağ
    # kalitesi kabul eşiği YOKTUR. Ölçüm tam pencerede, bu hücrede yapıldı
    # (22 Eylül 2026; `arsiv/teshis/aomdv_gorev1001_2026-09-22/`, ön-kayıtlı
    # dört hipotez).
    ("gorev-yok", 1001):
        "esiksiz en kisa yol 0,2502 (kolun en dusugu; 1000'de 0,5519; "
        "K-137 §4). Tam pencerede OLCULDU: veri basarisizliklarinin %70'i, "
        "atlama teslim olasiligi 0,90'in ALTINDAKI baglarda — o baglar "
        "kullanimin yalniz %23'u. Rota boslugu yok (hedef_yok 0), tampon "
        "tavani baglamiyor (dusen 0), kayip birkac akista yogun (10 akisin "
        "3'u neredeyse hic teslim etmiyor, 2'si tam). AODV ayni hucrede ayni "
        "desen (%72 / %25) ve daha dusuk. K-149",
}}

# 🔒 REFERANS DÜNYANIN AÇIKLANMIŞ HÜCRELERİ — eski dünyanınkiler burada
# geçmez (K-188). Anahtar (desen, kol, tohum): aynı hücre iki desende başka
# ağdır. Girme şartı aynı: ölçülmüş mekanizma, dışlanmış kusur izleri
# (K-192 c). OLSR K-196'ya atıfla girer ("açıklanmış, sıralamasız";
# mekanizma yere toplamada ölçüldü, K-193). Eşler arası keşifseldir: oradaki
# düşük hücre açıklanmamış BULGU kalır, donmayı durdurmaz.
# K-224 (9–10 Ekim 2026): `OLSR-d` ve en çok 7 iletim denemesiyle yeniden;
# anatomi her düşük hücrede ölçüldü (`arsiv/teshis/denetim_duzeltme_2026-10-09/
# A3_anatomi_statik.txt`, `B2_anatomi_*.txt`; PDR'ler U1 kaydıyla birebir).
# Statik kolda düşüş `rota_gecersiz` ile iyi bağdaki iletim başarısızlığı
# (girişim) arasında bölünüyor; hareketli kollarda en büyük düşüş
# `rota_gecersiz`. Karar bağları her hücrede yeniden denemeli bantta iyi; tek
# deneme bandında (HELLO · TC'nin gördüğü) statikte %94–95, hareketlide
# %75–84 iyi — RFC'nin yayınları onaysızdır, kusur değil.
_OLSR_K224_STATIK = ("OLSR-d · K-196 atfi (aciklanmis, siralamasiz); anatomi "
                     "K-224: rota_gecersiz %6-17 + iyi bagda iletim_basarisiz "
                     "%10-14 (basarisiz baglarin %85-92'si iyi), karar "
                     "baglari yeniden denemeli %99-100 · tek deneme %94-95 "
                     "iyi. U1 9 Ekim 2026, 7 deneme")
_OLSR_K224_HAREKETLI = ("OLSR-d · K-196 atfi (aciklanmis, siralamasiz); "
                        "anatomi K-224: en buyuk dusus rota_gecersiz %28-50 "
                        "(iletim_basarisiz %12-16), karar baglari yeniden "
                        "denemeli %100 · tek deneme %75-84 iyi. U1 9 Ekim "
                        "2026, 7 deneme")
# `AODV-j` ve `AOMDV-f`ninkiler K-207'ye atıfla: kaynağına kural kural sadık
# (K-208, K-210, K-215) ve yine eşik altındaysa protokolün KENDİ sınırıdır —
# bulgu, kusur değil. K-224'te 7 denemeyle yeniden koşuldu; kodları K-218'den
# beri aynı.
# K-244 kuyruğu (16 Ekim 2026): `AODV-k` yere toplamada AODV-j'nin yerine.
# Düşüşü ns-3'ün iki varsayılanından (karşılıksız RREP, yayın titreşimi),
# gerçekleme ikisine sadık (A/B, `arsiv/teshis/aodv_k_ab_2026-10-15/`). Yedi
# düşük hücrenin anatomisi `arsiv/teshis/aodv_k_anatomi_2026-10-16/` (PDR'ler
# U1 kaydıyla birebir). AODV-j'nin üç hücrelik kaydı (statik 1000 · 1002 ·
# bağımsız 1000, K-224) git geçmişinde.
_AODV_K207 = ("AODV-k · sadakat denetiminden gecti (RFC 3561 + ns-3, 42 "
              "kural, K-244); esik alti protokolun kendi siniri (ogrenci, "
              "K-207). AODV-j'den dususu ns-3'un iki varsayilani (karsiliksiz "
              "RREP, yayin titresimi; arsiv/teshis/aodv_k_ab_2026-10-15/). "
              "Anatomi (arsiv/teshis/aodv_k_anatomi_2026-10-16/): korunum "
              "gecerli, karar baglari yeniden denemeli bantta %98-99 iyi. "
              "U1 15 Ekim 2026, 7 deneme")
# Bağımsız 1000 · görev 1000 · görev 1001'de birer TTL düşüşü var; kuyruğun
# ön-kaydı "döngü/TTL düşüşü 0" ister. K-207 madde 2'ye göre döngü izi
# alındı (`arsiv/teshis/aodv_k_dongu_2026-10-16/`, zincir sürekliliği 0
# boşluk): üç döngü de RFC'nin kurallarından, ns-3'le aynı.
_DONGU_IZI = ("TTL dususu 1, dongu izi RFC kuralindan (K-207 madde 2; "
              "arsiv/teshis/aodv_k_dongu_2026-10-16/): ")
_AODV_K_IZ: dict[tuple[str, str, int], tuple[str, str, str]] = {
    # (desen, kol, tohum): (U1 orani, dusen/uretilen en buyuk iki sebep,
    # TTL dususu)
    ("yere_toplama", "statik-yok", 1000): (
        "0,852", "iletim_basarisiz %8,6 · rota_gecersiz %6,9",
        "TTL dususu 0"),
    ("yere_toplama", "statik-yok", 1001): (
        "0,856", "iletim_basarisiz %9,4 · rota_gecersiz %6,2",
        "TTL dususu 0"),
    ("yere_toplama", "statik-yok", 1002): (
        "0,812", "iletim_basarisiz %9,9 · rota_gecersiz %9,4",
        "TTL dususu 0"),
    ("yere_toplama", "bagimsiz-yok", 1000): (
        "0,475", "rota_gecersiz %39,3 · iletim_basarisiz %21,2",
        _DONGU_IZI + "ayni kaynagin eszamanli iki RREQ'i iki dugumun ters "
        "rotasini birbirine cevirdi (§6.5; ns-3 RecvRequest)"),
    ("yere_toplama", "bagimsiz-yok", 1002): (
        "0,576", "rota_gecersiz %30,0 · iletim_basarisiz %21,9",
        "TTL dususu 0"),
    ("yere_toplama", "gorev-yok", 1000): (
        "0,490", "rota_gecersiz %31,4 · iletim_basarisiz %23,9",
        _DONGU_IZI + "sirasiz komsu rotasi RREP'le degisti (§6.2 + §6.7 i) "
        "ve ters rota (§6.5)"),
    ("yere_toplama", "gorev-yok", 1001): (
        "0,596", "rota_gecersiz %25,9 · iletim_basarisiz %22,3",
        _DONGU_IZI + "RERR'de sira kopyalama (§6.11 iii) + esit sirada "
        "etkin olmayan rotanin guncellenmesi (§6.7 iii; K-205)"),
}
_AOMDV_K207 = ("AOMDV-f · Marina-Das + RFC 3561 tabani (K-210, K-215); esik "
               "alti protokolun kendi siniri (K-207 kurali, K-215 on-kaydi). "
               "U1 9 Ekim 2026, 7 deneme (K-224): bagimsiz 1000 0,588 · "
               "statik 1000 0,899 · statik 1002 0,891")
# `JarmRout-b` (K-234) K-207'ye atıfla ve ölçülmüş mekanizmayla (K-238):
# makalenin yinelenen RREQ kuralı (Şekil 4, harfiyen) toplu akışta kendini
# besleyen tıkanıklık çöküşü üretir (`arsiv/teshis/jarmrout_sel_2026-10-12/`).
# Temsilci anatomiler yere toplamada, her kolun en düşük hücresinde
# (`arsiv/teshis/faz4b_kapanis2_2026-10-12/anatomi_*`; PDR'ler U1 kaydıyla
# birebir). Her hücrenin çöküş izi U1 kaydından: rota tamponu girişi ve tepe
# doluluğu (geçen hücrelerde giriş 41–3 674, tepe 2–26). Eşler arası
# keşifseldir (K-218); oradaki anatomi yere toplamanınkine dayanır.
_JARMROUT_K238 = ("JarmRout-b · Pu 2018 Sekil 4 harfiyen (K-234); esik alti "
                  "protokolun kendi siniri (K-207): yinelenen RREQ kurali "
                  "toplu akista tikaniklik cokusu uretir (K-238). Temsilci "
                  "anatomiler (yere toplama): korunum gecerli, dongu/TTL 0, "
                  "rotasiz_paket 0, RREQ basina yeniden yayin 54-75, RERR "
                  "5850-7697, en buyuk dusus iletim_basarisiz. U1 11-12 Ekim "
                  "2026, 7 deneme")
_JARMROUT_IZ: dict[tuple[str, str, int], tuple[str, int, int]] = {
    # (desen, kol, tohum): (U1 orani, rota tamponu girisi, tepe doluluk)
    ("yere_toplama", "statik-yok", 1000): ("0,547", 30511, 42),
    ("yere_toplama", "statik-yok", 1002): ("0,517", 31150, 32),
    ("yere_toplama", "bagimsiz-yok", 1000): ("0,304", 113139, 50),
    ("yere_toplama", "bagimsiz-yok", 1001): ("0,408", 86701, 43),
    ("yere_toplama", "bagimsiz-yok", 1002): ("0,386", 85408, 40),
    ("yere_toplama", "gorev-yok", 1000): ("0,303", 133001, 49),
    ("yere_toplama", "gorev-yok", 1001): ("0,417", 53870, 33),
    ("yere_toplama", "gorev-yok", 1002): ("0,496", 64626, 33),
    ("yere_toplama", "formasyon-yok", 1000): ("0,373", 116442, 50),
    ("yere_toplama", "formasyon-yok", 1001): ("0,426", 44296, 33),
    ("yere_toplama", "formasyon-yok", 1002): ("0,385", 80333, 32),
    ("esler_arasi", "bagimsiz-yok", 1001): ("0,478", 119295, 64),
    ("esler_arasi", "bagimsiz-yok", 1002): ("0,452", 59393, 64),
    ("esler_arasi", "gorev-yok", 1001): ("0,433", 55135, 64),
    ("esler_arasi", "gorev-yok", 1002): ("0,464", 47144, 64),
    ("esler_arasi", "formasyon-yok", 1001): ("0,545", 40813, 64),
}
ACIKLANMIS_DUSUK_REFERANS: dict[str, dict[tuple[str, str, int], str]] = {
    "aodv": {h: f"{_AODV_K207} · bu hucre: oran {o}, dusen/uretilen {s}, "
                f"{ttl}"
             for h, (o, s, ttl) in _AODV_K_IZ.items()},
    "aomdv": {("yere_toplama", kol, t): _AOMDV_K207 for kol, t in (
        ("statik-yok", 1000), ("statik-yok", 1002), ("bagimsiz-yok", 1000))},
    "desparete": {}, "olsrv2": {}, "babel": {},
    "desparete5": {}, "desparete5_cekirdek": {},
    "desparete5_eski_cekirdek": {}, "desparete5_cekirdek_19k": {},
    "jarmrout": {h: (f"{_JARMROUT_K238} · bu hucre: oran {o}, rota tamponu "
                     f"girisi {g}, tepe {t}/64"
                     + (" · esler arasi kesifsel (K-218)"
                        if h[0] == "esler_arasi" else ""))
                 for h, (o, g, t) in _JARMROUT_IZ.items()},
    "olsr": {**{("yere_toplama", "statik-yok", t): _OLSR_K224_STATIK
                for t in (1000, 1001, 1002)},
             **{("yere_toplama", kol, t): _OLSR_K224_HAREKETLI for kol, t in (
        ("bagimsiz-yok", 1000), ("gorev-yok", 1000), ("gorev-yok", 1001),
        ("gorev-yok", 1002), ("formasyon-yok", 1000),
        ("formasyon-yok", 1002))}},
}

# 🔒 K-192 (b) · KÂHİN AŞIMI OTOMATİK RET DEĞİL, PROSEDÜR: aşım çözünürlükten
# büyükse (ya da R geçerli ölçülemiyorsa) aynı hücrede üç kâhinin zarfına
# bakılır; protokol zarfın İÇİNDEYSE "ETX kâhini bu hücrede üst sınır değil"
# beyan edilir ve kayıt buraya girer. Zarfı da aşan hücrede yazılım hatası
# aranır. Anahtar (desen, kol, tohum); ölü kayıt taraması aynı.
# K-248 (17 Ekim 2026, yürütücü; sonuçtan sonra): zarfı da aşan hücre, ön-
# kayıtlı hata araması (sızıntı · sayım · korunum · kimlik) temiz çıkar ve
# kâhinin fazla kaybı ölçülürse "kâhin bu hücrede üst sınır değil" beyanıyla
# kayda girer. Kâhinler bağ bilgisinin referansıdır, tavan değil: kanal
# modelinden yönlendirir, trafiğin yükünü ve çarpışmaları görmez (K-110).
# Kapı her aşımı (oran > 1) kayıt ister; R'den küçük aşım zarf adımı istemez,
# kaydı ölçümü yazar. K-224: AOMDV'nin eşler arası kaydı ÖLDÜ (0,9814 <
# 0,9827); AODV'nin aşımı 0,0002 < R — çözünürlük içinde. Arşiv K-206 ·
# K-211 · K-218.
# K-238 · KOPYA KURALI: kopya gönderen bir protokolde aşım, mimari denetimi
# kâhin sızıntısı bulmuyorsa ve yalnız kopyayla teslim edilen paketler
# (aslı hedefe hiç varmamış) çıkarılınca oran ≤ 1 + R ise açıklanmıştır.
# K-244 kuyruğu (15 Ekim 2026): `Babel-a` yere toplamada altı hareketli
# hücrede ETX kâhinini aşıyor. Dördü R'den büyük ve üç kâhinin zarfının
# içinde (zarfı her hücrede en olası teslim kâhini veriyor;
# `arsiv/teshis/babel_zarf_2026-10-15/`). Formasyonun ikisi R içinde.
# Eşler arası (16–17 Ekim): sekiz aşım; beşi R'den büyük. İkisi zarfın içinde
# (`arsiv/teshis/babel_zarf_esler_2026-10-16/`); üçü zarfı da aşıyor, hata
# araması temiz, kâhinin fazla kaybı `iletim_basarisiz`'da
# (`arsiv/teshis/babel_zarf_asim_2026-10-16/`; K-248). Üçü R içinde.
_BABEL_ZARF = ("ETX kahini bu hucrede ust sinir degil (K-192 b): zarf "
               "arsiv/teshis/babel_zarf_2026-10-15/ (16 Ekim 2026). U1 15 "
               "Ekim 2026, K-244 kuyrugu")
_BABEL_ZARF_ES = ("ETX kahini bu hucrede ust sinir degil (K-192 b): zarf "
                  "arsiv/teshis/babel_zarf_esler_2026-10-16/ (16 Ekim 2026). "
                  "U1 16 Ekim 2026, K-244 kuyrugu")
_BABEL_ZARF_ASIM = ("zarf da asiliyor; hata aramasi temiz (sizinti, sayim, "
                    "korunum, kimlik), kahin bu hucrede ust sinir degil "
                    "(K-248; arsiv/teshis/babel_zarf_asim_2026-10-16/). U1 16 "
                    "Ekim 2026, K-244 kuyrugu")
KAHIN_ASIMI_ACIKLANMIS: dict[str, dict[tuple[str, str, int], str]] = {
    "olsr": {}, "desparete": {}, "aomdv": {}, "olsrv2": {},
    "babel": {
        ("yere_toplama", "bagimsiz-yok", 1001):
            "Babel-a 0,9095 · ETX kahini 0,8882 (oran 1,0240) · en olasi "
            "teslim 0,9663 · en kisa yol 0,6762 → zarf 0,9663. " + _BABEL_ZARF,
        ("yere_toplama", "bagimsiz-yok", 1002):
            "Babel-a 0,8548 · ETX kahini 0,8334 (oran 1,0257) · en olasi "
            "teslim 0,8803 · en kisa yol 0,6311 → zarf 0,8803. " + _BABEL_ZARF,
        ("yere_toplama", "gorev-yok", 1001):
            "Babel-a 0,8957 · ETX kahini 0,8679 (oran 1,0320) · en olasi "
            "teslim 0,9261 · en kisa yol 0,5826 → zarf 0,9261. " + _BABEL_ZARF,
        ("yere_toplama", "gorev-yok", 1002):
            "Babel-a 0,9198 · ETX kahini 0,8998 (oran 1,0222) · en olasi "
            "teslim 0,9626 · en kisa yol 0,6739 → zarf 0,9626. " + _BABEL_ZARF,
        ("yere_toplama", "formasyon-yok", 1001):
            "Babel-a 0,9517 · ETX kahini 0,9467 (15 Ekim, K-244 kuyrugu): "
            "asim 0,0053 < R 0,0126 — cozunurluk icinde, zarf adimi "
            "gerekmez (K-192 b)",
        ("yere_toplama", "formasyon-yok", 1002):
            "Babel-a 0,9549 · ETX kahini 0,9495 (15 Ekim, K-244 kuyrugu): "
            "asim 0,0057 < R 0,0126 — cozunurluk icinde, zarf adimi "
            "gerekmez (K-192 b)",
        ("esler_arasi", "bagimsiz-yok", 1002):
            "Babel-a 0,8963 · ETX kahini 0,8787 (oran 1,0200) · en olasi "
            "teslim 0,9068 · en kisa yol 0,6504 → zarf 0,9068. "
            + _BABEL_ZARF_ES,
        ("esler_arasi", "gorev-yok", 1000):
            "Babel-a 0,9755 · ETX kahini 0,9612 (oran 1,0148) · en olasi "
            "teslim 0,9929 · en kisa yol 0,9145 → zarf 0,9929. "
            + _BABEL_ZARF_ES,
        ("esler_arasi", "gorev-yok", 1001):
            "Babel-a 0,8935 · ETX kahini 0,8403 (oran 1,0633) · en olasi "
            "teslim 0,8500 · en kisa yol 0,5661 → zarf 0,8500; kahinin "
            "fazla kaybi iletim_basarisiz +557, kuyruk tasmasi +63. "
            + _BABEL_ZARF_ASIM,
        ("esler_arasi", "gorev-yok", 1002):
            "Babel-a 0,8638 · ETX kahini 0,8392 (oran 1,0293) · en olasi "
            "teslim 0,8632 · en kisa yol 0,6768 → zarf 0,8632 (+0,0006); "
            "kahinin fazla kaybi iletim_basarisiz +607, kuyruk tasmasi "
            "+27. " + _BABEL_ZARF_ASIM,
        ("esler_arasi", "formasyon-yok", 1001):
            "Babel-a 0,9636 · ETX kahini 0,9424 (oran 1,0225) · en olasi "
            "teslim 0,8891 · en kisa yol 0,7968 → zarf 0,9424; kahinin "
            "fazla kaybi iletim_basarisiz +327. " + _BABEL_ZARF_ASIM,
        ("esler_arasi", "statik-yok", 1001):
            "Babel-a 0,9864 · ETX kahini 0,9827 (16 Ekim, K-244 kuyrugu): "
            "asim 0,0037 < R 0,0126 — cozunurluk icinde, zarf adimi "
            "gerekmez (K-192 b)",
        ("esler_arasi", "formasyon-yok", 1000):
            "Babel-a 0,9895 · ETX kahini 0,9855 (16 Ekim, K-244 kuyrugu): "
            "asim 0,0040 < R 0,0126 — cozunurluk icinde, zarf adimi "
            "gerekmez (K-192 b)",
        ("esler_arasi", "formasyon-yok", 1002):
            "Babel-a 0,9647 · ETX kahini 0,9563 (16 Ekim, K-244 kuyrugu): "
            "asim 0,0087 < R 0,0126 — cozunurluk icinde, zarf adimi "
            "gerekmez (K-192 b)"},
    "jarmrout": {
        ("esler_arasi", "statik-yok", 1001):
            "JarmRout-b 0,9954 · ETX kahini 0,9827 (oran 1,0129 > 1 + R): "
            "kopya kurali (K-238) — 12 799 paketin 12'si yalniz kopyayla "
            "teslim; cikarilinca 0,9945, oran 1,0120 <= 1,0126. Mimari "
            "denetimi kahin sizintisi bulmuyor. arsiv/teshis/"
            "faz4b_kapanis2_2026-10-12/kopya_payi.txt",
        ("esler_arasi", "formasyon-yok", 1000):
            "JarmRout-b 0,9937 · ETX kahini 0,9855 (12 Ekim, 7 deneme, "
            "K-238): asim 0,0083 < R 0,0126 — cozunurluk icinde, zarf adimi "
            "gerekmez (K-192 b)"},
    "aodv": {("esler_arasi", "statik-yok", 1001):
             "AODV-k 0,9877 · ETX kahini 0,9827 (16 Ekim, 7 deneme, K-244 "
             "kuyrugu): asim 0,0051 < R 0,0126 — cozunurluk icinde, zarf "
             "adimi gerekmez (K-192 b). AODV-j 0,9829 (K-224); 7 Ekim'in "
             "zarfi 0,9998 (8 deneme, K-218)"},
}

# 🔒 DD-07 (K-242) · KAYDIN ORANI: muafiyet listesi yalnız hücrenin listede
# olup olmadığına bakıyordu; AODV-j'nin kayıtlı 0,886'lık hücresi 0,45'e
# düşse de kapı "TEMİZ" diyordu. Her kayıt (açıklanmış düşük hücre ve kâhin
# aşımı) ölçüldüğü oranı taşır; bugünkü oran ondan `KAYIT_BANDI`ndan fazla
# saparsa "KAYIT SAPTI" kapıyı kırmızı yakar ve açıklama yeniden ölçülür.
# Oranlar `ciktilar2/aodv_uygunluk/<protokol>_referans_2026_<desen>_son.json`
# kayıtlarından (K-224 · K-238 · Babel: K-244 kuyruğu, 15 Ekim 2026).
KAYITLI_ORAN: dict[str, dict[tuple[str, str, int], float]] = {
    "aodv": {("yere_toplama", "statik-yok", 1000): 0.8522,
             ("yere_toplama", "statik-yok", 1001): 0.8558,
             ("yere_toplama", "statik-yok", 1002): 0.8123,
             ("yere_toplama", "bagimsiz-yok", 1000): 0.4753,
             ("yere_toplama", "bagimsiz-yok", 1002): 0.5762,
             ("yere_toplama", "gorev-yok", 1000): 0.4903,
             ("yere_toplama", "gorev-yok", 1001): 0.5960,
             ("esler_arasi", "statik-yok", 1001): 1.0051},
    "aomdv": {("yere_toplama", "statik-yok", 1000): 0.8989,
              ("yere_toplama", "statik-yok", 1002): 0.8912,
              ("yere_toplama", "bagimsiz-yok", 1000): 0.5885},
    "olsr": {("yere_toplama", "statik-yok", 1000): 0.6573,
             ("yere_toplama", "statik-yok", 1001): 0.8144,
             ("yere_toplama", "statik-yok", 1002): 0.7452,
             ("yere_toplama", "bagimsiz-yok", 1000): 0.3878,
             ("yere_toplama", "gorev-yok", 1000): 0.4446,
             ("yere_toplama", "gorev-yok", 1001): 0.5665,
             ("yere_toplama", "gorev-yok", 1002): 0.5803,
             ("yere_toplama", "formasyon-yok", 1000): 0.4211,
             ("yere_toplama", "formasyon-yok", 1002): 0.5926},
    "jarmrout": {**{h: float(o.replace(",", "."))
                    for h, (o, _g, _t) in _JARMROUT_IZ.items()},
                 ("esler_arasi", "statik-yok", 1001): 1.0129,
                 ("esler_arasi", "formasyon-yok", 1000): 1.0083},
    "babel": {("yere_toplama", "bagimsiz-yok", 1001): 1.0240,
              ("yere_toplama", "bagimsiz-yok", 1002): 1.0257,
              ("yere_toplama", "gorev-yok", 1001): 1.0320,
              ("yere_toplama", "gorev-yok", 1002): 1.0222,
              ("yere_toplama", "formasyon-yok", 1001): 1.0053,
              ("yere_toplama", "formasyon-yok", 1002): 1.0057,
              ("esler_arasi", "bagimsiz-yok", 1002): 1.0200,
              ("esler_arasi", "gorev-yok", 1000): 1.0148,
              ("esler_arasi", "gorev-yok", 1001): 1.0633,
              ("esler_arasi", "gorev-yok", 1002): 1.0293,
              ("esler_arasi", "formasyon-yok", 1001): 1.0225,
              ("esler_arasi", "statik-yok", 1001): 1.0037,
              ("esler_arasi", "formasyon-yok", 1000): 1.0040,
              ("esler_arasi", "formasyon-yok", 1002): 1.0087},
    "desparete": {}, "olsrv2": {},
}
# Bant = çözünürlük R (K-224): kod değişmeden yeniden koşulan hücre birebir
# aynı oranı verir; R'den büyük sapma açıklamanın yeniden ölçülmesini ister.
KAYIT_BANDI = 0.0126


def _kayit_sapti_mi(protokol: str, desen: str | None, kol: str, t: int,
                    oran: float) -> str | None:
    """Kayıtlı oranla bugünkü oranın farkı bandı aşıyorsa açıklaması."""
    kayitli = KAYITLI_ORAN.get(protokol, {}).get((desen, kol, t))
    if kayitli is None:
        return "kayitta oran yok"
    if abs(oran - kayitli) > KAYIT_BANDI:
        return f"kayitli oran {kayitli:.4f}, fark {oran - kayitli:+.4f}"
    return None


DUMAN_KOLLARI: tuple[str, ...] = ("statik-yok",)
DUMAN_TOHUMLARI: tuple[int, ...] = (1000,)
# 🔴 DUMAN KESİTİ SAYIYI ÜRETMEZ — ve bunun sebebi ölçüldü: tam pencerede
# TEK bir (AODV, kâhin) çifti 505 s sürüyor, yani `uretici_duman.py`nin
# *"ucuz kesit"* sözleşmesi tam pencereyle tutturulamaz. Kesit bu yüzden
# KISA pencere koşar ve bastığı oran KAPININ ORANI DEĞİLDİR.
# 🔒 Kısa pencere `yere_toplama_yuku.py::YAN_GOZLEM_PENCERESI` ile aynı
# idiomdur ve orada da aynı beyanla duruyor.
DUMAN_PENCERESI: dict[str, float] = {
    "isinma_s": 10.0, "olcum_bitis_s": 40.0, "kosu_bitis_s": 50.0}


def _pdr(kfg: Konfig, kahin: bool, protokol: str = "aodv") -> tuple:
    """Bir koşu — (PDR, korunum geçerli mi, tampon teşhisi).

    🔒 TAMPON TEŞHİSİ AYNI KOŞUMDAN OKUNUYOR ve sebebi bir çalışma kuralı
    (`03` §1, 17 Eylül 2026): *bir iş bitirilir, sonra ölçülür* — aynı
    dört saatlik koşumu iki ayrı soru için iki kez koşmak yerine, kapanış
    koşumu iki soruyu birden cevaplar.

    İkinci soru: `rota_tamponu_kapasitesi` (64) ve `rota_tamponu_omru_s`
    (30 s) — ns-3 AODV'nin değerleri, köken KAYNAK (K-198); birincil hücrede
    bağlamadıkları ölçüldü (K-200). Tablo tamponun bu koşumda da dolup
    dolmadığını gösterir.
    """
    kur = kurulum_yap(kfg)
    if kahin:
        grafik = KanalGrafigi(kur)
        kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
    else:
        kosu = Kosu(kur, _fabrika(protokol, kfg))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m = satir["metrikler"]
    tampon = {ad: m.get(ad) for ad in
              ("tampon_giris", "tampon_dusen", "en_yuksek_tampon")}
    return m["pdr"], satir["korunum"]["gecerli"], tampon


def _is(gorev):
    """Havuz işçisi: (kol, tohum, kâhin mi, pencere, protokol, desen) →
    ölçüm. Kâhin görevinde protokol `None`dır: kâhin koşusu protokolden
    bağımsızdır, yalnız desene bağlıdır."""
    kol, tohum, kahin, pencere, protokol, desen = gorev
    try:
        t0 = time.perf_counter()
        pdr, gecerli, tampon = _pdr(
            DS.konfig(kol="u1", senaryo=kol, tohum=tohum,
                      **({"trafik_deseni": desen} if desen else {}),
                      **dict(pencere)), kahin, protokol)
        return {"pdr": pdr, "gecerli": gecerli, "tampon": tampon,
                "sure": time.perf_counter() - t0}, None
    except Exception as e:                       # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def _is_etiketli(gorev):
    """`imap_unordered` için: sonucu görevle birlikte döndürür."""
    return gorev, _is(gorev)


def _kod_imzasi() -> str:
    """Ara kaydın bağlı olduğu kod hâli: simülatör · protokoller · aletler.
    Kod değişince ara kayıttaki ölçüm başka bir kodundur, sürdürülemez."""
    from sim2.cekirdek.kimlik import arac_hash
    return "/".join(arac_hash(KOK / p)
                    for p in ("sim2", "protokoller", "kalibrasyon"))


def _ara_kayit_yolu() -> Path:
    """Tam koşumun ara kaydı — dünya ve desen başına bir dosya."""
    desen = os.environ.get(DESEN_ORTAM)
    ad = DS.etiket("u1_ara")
    return DIZIN / (f"{ad}_{desen}.jsonl" if desen else f"{ad}.jsonl")


def _ara_kayit_oku(yol: Path, imza: str) -> dict:
    """Ara kayıttaki hatasız ölçümler — görev anahtarıyla. Başka bir kod
    hâlinin satırı varsa durur: iki kod hâlinin sayısı tek kayda karışmaz."""
    bitti: dict = {}
    if not yol.exists():
        return bitti
    for satir in yol.read_text(encoding="utf-8").splitlines():
        if not satir.strip():
            continue
        r = json.loads(satir)
        if r["kod"] != imza:
            raise SystemExit(
                f"ara kayıt başka bir kod hâlinin ({r['kod']} ≠ {imza}): "
                f"{yol} — arsiv/'e taşı ya da aynı kodla sür")
        if r["hata"] is None:
            bitti[(r["kol"], r["tohum"], r["kahin"], (), r["protokol"],
                   r["desen"])] = (r["olcum"], None)
    return bitti


def u1(kollar=KOLLAR, tohumlar=TOHUMLAR, isci: int = 8,
       pencere: dict[str, float] | None = None,
       protokol: str | tuple[str, ...] = "aodv") -> int:
    """U1 kapısı — bir ya da birkaç protokol. Çıkış kodu: 0 hepsi geçti,
    1 en az biri kaldı.

    🔒 KÂHİN DESEN BAŞINA BİR KEZ KOŞULUR (29 Eylül 2026). Kâhin koşusu
    protokolden bağımsızdır (aynı konfig, aynı dünya); aynı desendeki
    protokoller aynı kâhin ölçümünü paylaşır. Kanıt: 27 Eylül'ün referans
    dünya kayıtlarında (AODV · OLSR · AOMDV, ayrı ayrı koşulmuş) kâhinin
    PDR'si 12 hücrenin hepsinde üç protokolde birebir aynı. Kayıt biçimi ve
    hüküm protokol başına değişmedi: her protokolün kaydı kâhin hücrelerini
    kendisi taşır.

    🔒 ARA KAYIT (tam koşumda): her koşu biter bitmez `_ara_kayit_yolu()`na
    yazılır; kesintiden sonra aynı komut, aynı kod hâlindeyse, bitmiş
    koşuları yeniden koşmaz (`kayip_anatomisi.py` ile aynı gelenek, K-198).

    ⚠️ `pencere` YALNIZ duman kesiti içindir ve verildiğinde bastığı oran
    kapının oranı DEĞİLDİR; başlıkta bir uyarı satırı basılır.
    """
    protokoller = (protokol,) if isinstance(protokol, str) else tuple(protokol)
    desenler = {p: _desen_adi(p) for p in protokoller}
    print("=" * 78)
    print(f"U1 — {', '.join(p.upper() for p in protokoller)} / ETX KAHINI "
          f"ORANI  (`06` §4.3 · tam olcek)")
    print("=" * 78)
    if pencere:
        print("  ⚠️ DUMAN KESITI — KISA PENCERE. Bastigi oran KAPININ")
        print("     orani DEGILDIR; yalniz aletin kostugunu gosterir.")
    for desen in dict.fromkeys(desenler.values()):
        ornek = DS.konfig(kol="u1", senaryo=kollar[0], tohum=tohumlar[0],
                          **({"trafik_deseni": desen} if desen else {}),
                          **dict(pencere or {}))
        print(f"  N = {ornek.dugum_sayisi} · pencere "
              f"({ornek.isinma_s:.0f}; {ornek.olcum_bitis_s:.0f}) s · "
              f"kosu {ornek.kosu_bitis_s:.0f} s · desen {ornek.trafik_deseni}")
    print(f"  kollar: {list(kollar)}")
    print(f"  tohumlar: {list(tohumlar)}  (GELISTIRME — ana deney tohumu YOK)")
    print(f"  🔒 OLCUT: statik oran >= {U1_ESIK_STATIK:.2f} · "
          f"hareketli oran >= {U1_ESIK_HAREKETLI:.2f}")
    print()

    sabit = tuple(sorted((pencere or {}).items()))
    gorevler = [(kol, t, False, sabit, p, desenler[p])
                for p in protokoller for kol in kollar for t in tohumlar]
    gorevler += [(kol, t, True, sabit, None, d)
                 for d in dict.fromkeys(desenler.values())
                 for kol in kollar for t in tohumlar]
    ham: dict = {}
    ara = None if pencere else _ara_kayit_yolu()
    imza = _kod_imzasi() if ara else ""
    if ara is not None:
        istenen = set(gorevler)
        ham = {g: v for g, v in _ara_kayit_oku(ara, imza).items()
               if g in istenen}
        if ham:
            print(f"  ara kayittan {len(ham)} kosu okundu ({ara})")
    # 🔒 Havuza UZUN işler ÖNCE verilir: hareketli kollar, protokol kâhinden
    # önce. Yalnız süreyi etkiler, sonucu değil — kayıt ve hüküm aşağıda
    # yine kanonik sırayla kurulur. Ölçülmüş gerekçe (`AODV-e` kaydının iş
    # süreleri, K-145): kanonik sırada statik işler başta biter ve sonda
    # uzun hareketli işler tek başına kalır; 8 işçide çekişmesiz tahmin
    # 2,58 → 2,14 sa (alt sınır 1,91).
    sira = sorted((g for g in gorevler if g not in ham),
                  key=lambda g: (g[0].startswith("statik"), g[2]))
    print(f"  {len(gorevler)} kosu ({len(sira)} kaldi) · {isci} isci")
    t0 = time.perf_counter()
    if sira:
        with Pool(min(isci, len(sira))) as havuz:
            for n, (g, (olcum, hata)) in enumerate(havuz.imap_unordered(
                    _is_etiketli, sira, chunksize=1), 1):
                ham[g] = (olcum, hata)
                if ara is not None:
                    ara.parent.mkdir(parents=True, exist_ok=True)
                    with ara.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(
                            {"kol": g[0], "tohum": g[1], "kahin": g[2],
                             "protokol": g[4], "desen": g[5], "olcum": olcum,
                             "hata": hata, "kod": imza},
                            ensure_ascii=False) + "\n")
                ne = "kahin" if g[2] else g[4]
                durum = (f"🔴 {hata}" if hata is not None else
                         f"PDR {olcum['pdr'] or 0:.4f} · "
                         f"{olcum['sure'] / 60:.0f} dk")
                print(f"  {n:>3}/{len(sira)} {ne:<10}{g[0]:<15}{g[1]:>5}  "
                      f"{durum}", flush=True)
    sure_s = time.perf_counter() - t0
    print()
    cikis = 0
    for p in protokoller:
        sonuc = {(kol, t, kahin, sabit):
                 ham[(kol, t, kahin, sabit, None if kahin else p, desenler[p])]
                 for kol in kollar for t in tohumlar for kahin in (False, True)}
        if not pencere:
            _kaydet(sonuc, p)
        cikis |= _degerlendir(sonuc, kollar, tohumlar, sabit, sure_s,
                              len(sonuc), p, desenler[p])
        print()
    return cikis


# ==========================================================================
# U3 · YÜK PROFİLİ — ölçüm, KAPI DEĞİL (`06` §4.3 · K-142 · K-143 · K-144)
# ==========================================================================
# 🔒 Aynı küçük dünyada 60 s ve 120 s koşulur; kontrol çerçevesi oranı
# yükün süreyle nasıl büyüdüğünü söyler: ~2 sabit hız (periyodik yük),
# belirgin biçimde 2'nin altı başta yığılan yük (keşif susar).
# ⚠️ Küçük test dünyası `tests2/test_kosum.py::_konfig` — ikinci bir tanım
# yazılmaz; `kontrol_duzlemi_kapilari.py` ile aynı gelenek.
U3_SURELERI_S: tuple[float, ...] = (60.0, 120.0)


def _u3_is(gorev):
    protokol, bitis = gorev
    from test_kosum import _konfig
    kfg = _konfig("statik-yok", 1000, bitis, **_desen(protokol))
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, _fabrika(protokol, kfg))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u3")
    bicim = satir["teshis"]["kontrol_duzlemi"]["bicim"]["tum"]
    teshis: dict[str, float] = {}
    for d in satir["teshis"]["dugum"]:
        for k, v in d.items():
            if isinstance(v, (int, float)):
                teshis[k] = teshis.get(k, 0) + v
    return (protokol, bitis, {n: v["cerceve"] for n, v in bicim.items()},
            satir["metrikler"]["pdr"], teshis)


def u3() -> int:
    """Taban protokollerin yük profilini yan yana basar. Çıkış 0 — bir ÖLÇÜMDÜR."""
    print("=" * 78)
    print("U3 — KONTROL YUKU SUREYLE NASIL BUYUYOR  (kucuk dunya, statik-yok)")
    print("=" * 78)
    gorevler = [(p, b) for p in PROTOKOLLER for b in U3_SURELERI_S]
    with Pool(len(gorevler)) as havuz:
        sonuc = havuz.map(_u3_is, gorevler, chunksize=1)
    tablo = {(p, b): (c, pdr, t) for p, b, c, pdr, t in sonuc}
    kisa, uzun = U3_SURELERI_S
    for p in PROTOKOLLER:
        for b in U3_SURELERI_S:
            c, pdr, t = tablo[(p, b)]
            ek = (f"  kesif {t.get('kesif_basarili', 0):.0f} · "
                  f"rerr_onculsuz {t.get('rerr_onculsuz', 0):.0f}"
                  if p in ("aodv", "aomdv") else "")
            print(f"  {p:<5}{b:>6.0f} s  pdr {pdr:.4f}  {c}{ek}")
        oran = (sum(tablo[(p, uzun)][0].values())
                / sum(tablo[(p, kisa)][0].values()))
        print(f"  → {p} oran ({uzun:.0f}/{kisa:.0f} s): {oran:.3f}")
        print()
    return 0


def _kaydet(sonuc: dict, protokol: str) -> None:
    """Ölçülen hücreleri diske yazar — `<protokol>_son.json` ve damgalı kopya."""
    DIZIN.mkdir(parents=True, exist_ok=True)
    satirlar = [{"kol": kol, "tohum": t, "kahin": kahin,
                 "olcum": olcum, "hata": hata}
                for (kol, t, kahin, _s), (olcum, hata) in sonuc.items()]
    metin = json.dumps({"kaynak": "tam kosum", "protokol": protokol,
                        "desen": _desen_adi(protokol),
                        "kahin": "desen basina ortak kosu",
                        "hucreler": satirlar}, ensure_ascii=False, indent=1)
    damga = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    # K-183: referans dünyanın kaydı eskisini EZMEZ (`_referans_2026` soneki)
    ad = _kayit_adi(protokol)
    (DIZIN / f"{ad}_{damga}.json").write_text(metin, encoding="utf-8")
    (DIZIN / f"{ad}_son.json").write_text(metin, encoding="utf-8")


def hukum(yol: Path | None = None, protokol: str = "aodv") -> int:
    """Kayıtlı bir ölçüme BUGÜNKÜ hüküm kodunu uygular. Çıkış kodu = verdikt.

    🔒 Ölçmez, yalnız değerlendirir. Açıklanmış hücre listesi ya da eşikler
    değiştiğinde verdikti yeniden üretmenin yolu budur. Kaydın KAYNAĞI
    başlıkta basılır: tam koşumun kendi kaydı mı, yoksa yazdırılmış bir
    tablodan mı kuruldu.
    """
    yol = yol or DIZIN / f"{_kayit_adi(protokol)}_son.json"
    # 🔒 K-191: kayıt dünyasını SÖYLEMEZ, adı söyler (`_kayit_adi`). Referans
    # kaydı `--dunya` verilmeden okunursa eski dünyanın açıklanmış hücreleri
    # uygulanır ve "ölü açıklama" yanlış alarmı çıkar — dünya uyuşmalı.
    kayit_referans = "_referans_2026" in Path(yol).name
    if kayit_referans != DS.referans_mi():
        raise SystemExit(
            f"kayıt {'referans' if kayit_referans else 'eski'} dünyanın, "
            f"seçili dünya {DS.secili()} — `--dunya` ile aynı dünyayı ver")
    veri = json.loads(Path(yol).read_text(encoding="utf-8"))
    # Kayıt kendi protokolünü söyler; eski kayıtlar (alan yok) AODV'dir.
    protokol = veri.get("protokol", "aodv")
    # Desen: kayıt söylüyorsa o; 30 Eylül öncesi kayıtlar adından.
    desen = veri.get("desen") or next(
        (d for d in DESENLER if f"_{d}_" in Path(yol).name), None)
    print("=" * 78)
    print("U1 — HUKUM KIPI  (olcmez, kayitli olcume bugunku kodu uygular)")
    print("=" * 78)
    print(f"  kayit  : {yol}")
    print(f"  protokol: {protokol}")
    print(f"  desen  : {desen}")
    print(f"  kaynak : {veri.get('kaynak')}")
    sonuc = {}
    kollar: list[str] = []
    tohumlar: list[int] = []
    for h in veri["hucreler"]:
        sonuc[(h["kol"], h["tohum"], h["kahin"], ())] = (h["olcum"], h["hata"])
        if h["kol"] not in kollar:
            kollar.append(h["kol"])
        if h["tohum"] not in tohumlar:
            tohumlar.append(h["tohum"])
    print(f"  🔒 OLCUT: statik oran >= {U1_ESIK_STATIK:.2f} · "
          f"hareketli oran >= {U1_ESIK_HAREKETLI:.2f}")
    print()
    return _degerlendir(sonuc, tuple(kollar), tuple(tohumlar), (),
                        0.0, len(sonuc), protokol, desen)


def _degerlendir(sonuc: dict, kollar, tohumlar, sabit, sure_s: float,
                 n_gorev: int, protokol: str = "aodv",
                 desen: str | None = None) -> int:
    """🔒 Hükmün TEK gerçeklemesi — tam koşum da `hukum` kipi de buradan geçer."""
    # 🔴 K-188: `ACIKLANMIS_DUSUK` ESKİ DÜNYANIN hücreleridir (K-137, K-149);
    # referans dünyada yalnız kendi listesi, o desenin hücreleri geçerlidir.
    aciklanmis = ({(k, t): g for (d, k, t), g
                   in ACIKLANMIS_DUSUK_REFERANS[protokol].items()
                   if d == desen}
                  if DS.referans_mi() else ACIKLANMIS_DUSUK[protokol])
    print(f"  {'kol':<16}{'tohum':>6}{protokol.upper():>9}{'ETX kahin':>11}"
          f"{'oran':>8}{'esik':>7}{'karar':>18}")
    uygunluk = True            # U1-U — kalirsa protokol KABUL EDILMEZ
    basarim_temiz = True       # U1-B — aciklanmamis dusuk ya da olu kayit
    olculen_dusuk: set = set()
    kol_oranlari: dict[str, list[float]] = {}
    hucre_oranlari: dict[tuple[str, int], float] = {}
    for kol in kollar:
        esik = (U1_ESIK_STATIK if kol.startswith("statik-")
                else U1_ESIK_HAREKETLI)
        for t in tohumlar:
            a, a_hata = sonuc[(kol, t, False, sabit)]
            k, k_hata = sonuc[(kol, t, True, sabit)]
            if a_hata is not None or k_hata is not None:
                print(f"  {kol:<16}{t:>6}  🔴 HATA: {a_hata or k_hata}")
                uygunluk = False
                continue
            # 🔒 BOS GECMEYE KAPALI: korunum defteri kapanmadiysa satirin
            # PDR'si bir sayi degil, bir artiktir.
            if not (a["gecerli"] and k["gecerli"]):
                print(f"  {kol:<16}{t:>6}  🔴 KORUNUM KAPANMADI  [U1-U]")
                uygunluk = False
                continue
            if not a["pdr"] or not k["pdr"]:
                print(f"  {kol:<16}{t:>6}  🔴 PDR YOK  [U1-U] "
                      f"({protokol.upper()}={a['pdr']} kahin={k['pdr']})")
                uygunluk = False
                continue
            oran = a["pdr"] / k["pdr"]
            kol_oranlari.setdefault(kol, []).append(oran)
            hucre_oranlari[(kol, t)] = oran
            sapma = (_kayit_sapti_mi(protokol, desen, kol, t, oran)
                     if DS.referans_mi() and (kol, t) in aciklanmis else None)
            if oran >= esik:
                karar = "GECTI"
            elif (kol, t) in aciklanmis and sapma is not None:
                # 🔴 DD-07: açıklama BAŞKA bir oran için yazılmıştı.
                karar = "🔴 KAYIT SAPTI"
                olculen_dusuk.add((kol, t))
                basarim_temiz = False
                print(f"  🔴 [U1-B] {kol}/{t}: {sapma}")
            elif (kol, t) in aciklanmis:
                # 🟡 U1-B · dusuk AMA aciklamasi OLCULMUS ve kayitli.
                karar = "DUSUK (aciklanmis)"
                olculen_dusuk.add((kol, t))
            else:
                # 🔴 Yeni bir dusuk hucre SESSIZCE gecemez.
                karar = "🔴 ACIKLANMAMIS"
                basarim_temiz = False
            print(f"  {kol:<16}{t:>6}{a['pdr']:>9.4f}{k['pdr']:>11.4f}"
                  f"{oran:>8.3f}{esik:>7.2f}{karar:>18}")
    print()
    print(f"  {'kol':<16}{'oran ort':>10}{'en dusuk':>10}")
    for kol, oranlar in kol_oranlari.items():
        print(f"  {kol:<16}{ist.mean(oranlar):>10.3f}{min(oranlar):>10.3f}")
    print()
    # 🔒 TAMPON — bağlıyor mu (yukarıdaki beyan; köken KAYNAK, K-198).
    print("  ROTA TAMPONU  (kapasite 64 · omur 30 s — ns-3, K-198)")
    print(f"  {'kol':<16}{'tohum':>6}{'giris':>9}{'dusen':>8}{'tepe':>7}")
    tepe_en = 0.0
    dusen_top = 0.0
    for kol in kollar:
        for t in tohumlar:
            a, a_hata = sonuc[(kol, t, False, sabit)]
            if a_hata is not None or a is None:
                continue
            tm = a.get("tampon") or {}
            g, d, tp = (tm.get("tampon_giris"), tm.get("tampon_dusen"),
                        tm.get("en_yuksek_tampon"))
            tepe_en = max(tepe_en, tp or 0.0)
            dusen_top += (d or 0.0)
            print(f"  {kol:<16}{t:>6}{(g or 0):>9.0f}{(d or 0):>8.0f}"
                  f"{(tp or 0):>7.0f}")
    print(f"  → en yuksek doluluk {tepe_en:.0f}/64 · "
          f"toplam sure tavanindan dusen {dusen_top:.0f}")
    print()
    print(f"  toplam {n_gorev} kosum · {sure_s:.0f} s")
    print()
    # ⚠️ KAHINI GECMEK DE BIR HATADIR: kahin her seyi bilir. Asiliyorsa
    # kahin bilgisi protokole sizmis demektir ve bu bir KAZANC degil, bir
    # kacaktir. Kapinin ikinci yarisi budur.
    asan_tum = [(kol, t, o) for (kol, t), o in hucre_oranlari.items()
                if o > 1.0]
    zarfli = {(k, t) for (d, k, t) in (
        KAHIN_ASIMI_ACIKLANMIS.get(protokol, {}) if DS.referans_mi() else {})
        if d == desen}
    for kol, t, o in asan_tum:
        if (kol, t) in zarfli:
            sapma = _kayit_sapti_mi(protokol, desen, kol, t, o)
            if sapma is not None:
                # 🔴 DD-07: kayıt başka bir aşım için yazılmıştı.
                print(f"  🔴 [U1-U] kahin asimi KAYIT SAPTI: {kol}/{t} "
                      f"oran = {o:.4f} — {sapma}")
                uygunluk = False
                continue
            # Kayıt üç yoldan biriyle girer: zarf (K-192 b), aşım < R ya da
            # kopya kuralı (K-238); gerekçe kaydın kendisinde.
            print(f"  🟡 [U1-U] kahin asimi ACIKLANMIS (K-192 b · K-238): "
                  f"{kol}/{t} oran = {o:.3f} — gerekce "
                  f"KAHIN_ASIMI_ACIKLANMIS'ta")
    asan = [(kol, o) for kol, t, o in asan_tum if (kol, t) not in zarfli]
    # Ölü kayıt: bu koşumda ölçülen ama artık aşmayan hücre (D12 emsali).
    olu_zarf = sorted((zarfli & set(hucre_oranlari))
                      - {(k, t) for k, t, _ in asan_tum})
    if olu_zarf:
        print("  🔴 [U1-U] OLU ZARF KAYDI — artik asim yok, kayit silinmeli: "
              f"{olu_zarf}")
        uygunluk = False
    if asan:
        print(f"  🔴 [U1-U] {protokol.upper()} KAHINI GECTI — kahin bilgisi "
              f"sizmis olabilir:")
        for kol, o in asan:
            print(f"     {kol}  oran = {o:.3f}")
        uygunluk = False

    # 🔴 OLU ACIKLAMA TARAMASI — bu kosumda OLCULEN ama artik dusuk OLMAYAN
    # bir kayit. Muafiyet listesi kendi bayatligini gizleyemez (D12 emsali).
    # ⚠️ Bu kosumda hic olculmemis hucre (duman kesiti) olu SAYILMAZ.
    olculen = {(kol, t) for kol in kollar for t in tohumlar}
    olu = sorted((olculen & set(aciklanmis)) - olculen_dusuk)
    if olu:
        print("  🔴 [U1-B] OLU ACIKLAMA — artik dusuk degil, kayit silinmeli:")
        for kol, t in olu:
            print(f"     {kol} / {t}")
        basarim_temiz = False

    print("=" * 78)
    print(f"  U1-U uygunluk : {'GECTI 🟢' if uygunluk else 'KALDI 🔴'}"
          f"   (kalirsa protokol KABUL EDILMEZ)")
    print(f"  U1-B basarim  : {'TEMIZ 🟢' if basarim_temiz else 'KALDI 🔴'}"
          f"   (aciklanmamis dusuk / olu aciklama yok mu)")
    if olculen_dusuk:
        print(f"  🟡 aciklanmis dusuk hucre: {len(olculen_dusuk)} — "
              f"BULGU olarak raporlanir, kusur DEGIL")
    print("=" * 78)
    return 0 if (uygunluk and basarim_temiz) else 1


if __name__ == "__main__":
    DS.secimi_oku()                         # Faz 4 (K-183): --dunya
    print(f"  DUNYA: {DS.secili()}")
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    arg = sys.argv[1:]
    protokoller = ("aodv",)
    if "--protokol" in arg:
        i = arg.index("--protokol")
        protokoller = tuple(arg[i + 1].split(","))
        del arg[i:i + 2]
    for protokol in protokoller:
        if protokol not in PROTOKOLLER:
            raise SystemExit(f"bilinmeyen protokol: {protokol} — "
                             f"{sorted(PROTOKOLLER)}")
    if len(set(protokoller)) != len(protokoller):
        raise SystemExit(f"tekrarlanan protokol: {protokoller}")
    protokol = protokoller[0]
    if len(protokoller) > 1 and arg and arg[0] in ("u3", "hukum"):
        raise SystemExit(f"{arg[0]} tek protokolle çalışır")
    if "--desen" in arg:
        i = arg.index("--desen")
        if arg[i + 1] not in DESENLER:
            raise SystemExit(f"bilinmeyen desen: {arg[i + 1]} — {DESENLER}")
        os.environ[DESEN_ORTAM] = arg[i + 1]
        del arg[i:i + 2]
        print(f"  DESEN: {os.environ[DESEN_ORTAM]}")
    if arg and arg[0] == "u3":
        raise SystemExit(u3())
    if arg and arg[0] == "hukum":
        raise SystemExit(hukum(Path(arg[1]) if len(arg) > 1 else None,
                               protokol))
    if "duman" in arg:
        # ⚠️ UCUZ KESIT — SAYIYI URETMEZ, yalniz aletin kostugunu gosterir.
        raise SystemExit(u1(DUMAN_KOLLARI, DUMAN_TOHUMLARI, isci=4,
                            pencere=DUMAN_PENCERESI, protokol=protokoller))
    raise SystemExit(u1(protokol=protokoller))
