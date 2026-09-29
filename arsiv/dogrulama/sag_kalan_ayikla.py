"""
SAĞ KALAN MUTANT AYIKLAYICI — "eşdeğer mi, gerçek boşluk mu?"

🔴 SORDUĞU SORU: `kor_mutasyon.py`den sağ çıkan bir mutant, davranışı
GERÇEKTEN değiştiriyor mu?

NEDEN BU ARAÇ VAR
=================
Kör tarama sağ kalanları listeler ve *"elle ayıklanacak"* der. Elle ayıklamak
demek, koda bakıp *"bu herhalde eşdeğerdir"* demek demektir — yani
`03` B5'in ⭐ **"yargıyı elle yazmak"** tuzağı. Yargı veriden çıkmalı.

NASIL ÇALIŞIR
=============
Her sağ kalan için:
  1. Depo geçici bir dizine kopyalanır, mutasyon uygulanır
  2. SABİT bir koşu matrisi koşulur (aşağıda, açıkça yazılı)
  3. Her koşunun TAM sonuç sözlüğü tabanla karşılaştırılır
  4. Fark varsa → 🔴 DAVRANIŞ DEĞİŞTİ (gerçek boşluk, test yazılmalı)
     Fark yoksa → ⚪ bu matriste EŞDEĞER

🔴 "EŞDEĞER" DEĞİL, "BU MATRİSTE EŞDEĞER"
==========================================
Bu araç eşdeğerliği KANITLAYAMAZ — eşdeğerlik genel olarak karar
verilemezdir. Söyleyebileceği tek şey: *"aşağıdaki matriste hiçbir metrik
değişmedi."* Matris çıktının başına basılır ki iddia ölçeğiyle birlikte
okunsun (`03` B3: çalışma noktasını yazmayan bulgu sessizce yanlış olur).

⚠️ Mutasyonlar geçici kopyada uygulanır; asıl depo hiç değişmez.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

# 🔴 B-100 — kopyalama kuralı TEK KAYNAKTAN (`dogrulama/kopya.py`).
from dogrulama.kopya import depoyu_kopyala                       # noqa: E402

# --------------------------------------------------------------------------
# KOŞU MATRİSİ — açıkça yazılı, çıktının başına basılır
#
# 6 senaryo × 2 trafik × 3 tohum = 36 ana koşu + 4 UÇ DURUM × 2 tohum.
# Tohumlar AYARLAMA kümesinden (1–30); ana deney tohumları (2000–2029)
# hiçbir amaçla koşulmaz (K-025).
#
# 🔴 UÇ DURUMLAR NEDEN ZORUNLU — Y8
# ----------------------------------
# İlk sürüm yalnızca ana matrisi koşuyordu ve dokuz mutantı "eşdeğer" ilan
# etti. Sonra ölçtüm: o matriste `ttl_olumu`, `kuyruk_tasmasi` ve
# `hedef_yok` **sıfır** (denetim raporu da bunu söylüyordu). Yani TTL
# sınırını değiştiren bir mutasyonun "eşdeğer" çıkması, mutasyonun zararsız
# olduğunu DEĞİL, o yolun hiç koşulmadığını gösteriyordu.
#
# Y8: bir mutasyon testi, bozduğu yolun sağlam koşuda TETİKLENDİĞİNİ önce
# göstermek zorundadır. Uç durumlar `kapi_korunum.UC_DURUMLAR`dan alındı ki
# dört düşme sebebi de fiilen tetiklensin.
# --------------------------------------------------------------------------
SENARYOLAR = ("S0", "S1", "S2", "S3", "S4", "S5")
TRAFIKLER = ("yogun", "seyrek")
TOHUMLAR = (1, 7, 23)

# (ad, aktarıcı, ek konfig) — tetiklediği düşme sebebi yorumda
UC_DURUMLAR = (
    ("dar_kuyruk", "en_kisa_yol",
     dict(kuyruk_kapasitesi=1, trafik="yogun", cbr_araligi_s=0.05)),  # kuyruk_tasmasi
    ("kisa_ttl", "dongu_yapan", dict(ttl_baslangic=2)),               # ttl
    ("rota_yok", "olu", dict()),                                      # hedef_yok
    ("denemesiz", "en_kisa_yol", dict(yeniden_deneme_siniri=0)),      # iletim_basarisiz
)
UC_TOHUMLAR = (1, 7)


@dataclass(frozen=True)
class SagKalan:
    """Kör taramadan sağ çıkmış bir mutant.

    🔴 `satir` ARTIK BİLGİ AMAÇLI DEĞİL — 0 bırakılır ve rapor anında
    ÜRETİMDEN okunur (`_satir_no`). Elle yazılmış satır numarası kodun her
    düzenlemesinde bayatlar: ikinci bağımsız denetim 12 girdinin **10'unun**
    satır numarasının yanlış olduğunu ölçtü — ve o numaralar çıktının içinde
    delil olarak basılıyordu (B-24).
    """

    ad: str
    dosya: str
    satir: int          # ⚠️ ölü alan; `_satir_no()` kullanılır
    eski: str
    yeni: str
    kural: str
    # 🔴 B-36 — MUTASYONUN BAĞLI OLDUĞU YOL.
    # Araç tetiklenme sayaçlarını basıyor ve "sıfır olan bir yol için
    # 'eşdeğer' kararı GEÇERSİZDİR" diye uyarıyordu — ama hangi mutasyonun
    # hangi yola dokunduğu HİÇBİR YERDE yazılı değildi, dolayısıyla uyarı
    # hiçbir kararı geçersizleştiremiyordu. K-038 uyarıyı hiç anmamıştı.
    # 🔴 B-52 (K-053) — `yol` ZORUNLU, varsayılanı YOK.
    # B-36'nın düzeltmesi 7 girdinin yalnızca 2'sini kapsıyordu: kalan 5'i
    # `yol=None` ile `_tetiklendi()` kontrolünü **tamamen atlıyordu** ve yine
    # "eşdeğer" damgası alıyordu. `03` B5'in *"etiketi elle taşımak"* tuzağı,
    # B-36'nın düzeltmesinin İÇİNDE.
    #
    # Artık her girdi ya bir sayaç adı taşır ya `YOLSUZ` beyanı yapar —
    # ikisi de AÇIK bir karardır ve unutma ile karışmaz.
    yol: str


def _satir_no(m: "SagKalan") -> "int | str":
    """Mutasyon deseninin ŞU ANKİ satır numarası — üretimden okunur."""
    try:
        metin = (KOK / m.dosya).read_text(encoding="utf-8")
    except OSError:
        return "?"
    ilk_satir = m.eski.splitlines()[0]
    yer = metin.find(ilk_satir)
    return metin[:yer].count("\n") + 1 if yer >= 0 else "BULUNAMADI"


# --------------------------------------------------------------------------
# 🔴 20 AĞUSTOS 2026 · `python dogrulama/kor_mutasyon.py 24`
# Havuz 203 · taban temiz (271 passed) · skor %55,6 (10/18) · 8 sağ kalan.
#
# ⚠️ ÖNCEKİ LİSTE (19 Ağustos, havuz 185, 12 sağ kalan) DEĞİŞTİRİLDİ, birine
# eklenmedi. Sebep B-24: o listenin bir girdisi kod değişince bayatladı ve
# araç bunu "korumasız kod yolu" diye raporladı. Bir tarama listesi, ait
# olduğu KOD DURUMUNA aittir; iki taramanın listesi toplanamaz.
# Önceki 12'nin ayıklaması K-038'de; davranışı değiştiren 4'ü mutasyon
# paketine D16–D19 olarak girdi ve orada korunuyor.
#
# 🔴 Sekizincisi (`_kurulum_bitti = True → False`) bu listede YOK: taramadan
# sonra teste bağlandı (KM6) — Ç6'nın iddia ettiği ama hiç sınamadığı
# yazım hatası koruması. Artık yakalanıyor, yani sağ kalan değil.
# --------------------------------------------------------------------------
# 🔴 B-52: "bu mutasyonun tetiklenebilir bir yolu yok" AÇIK beyanı.
# `None` ile farkı: `None` bir unutma da olabilirdi; bu bir karardır.
YOLSUZ = "__YOLSUZ__"

# ⚠️ KOD DURUMU — 20 Ağustos 2026, havuz **203**, taban **271 test**.
# ---------------------------------------------------------------------------
# 🔴 BU LİSTE BAYAT SAYILIR (B-75, K-056). Girdiler 203'lük havuzdan çekilmiş
# 24'lük bir örneklemin ürünüdür; havuz bugün **215** ve aynı tohumla çekilen
# 24'ün içinde bu 7'den **yalnızca 1'i** var (`T06_ilet_jetonu_isareti`).
# Yedisi de bugünkü HAVUZDA var — ama ÖRNEKLEMDE yok.
#
# Yani bu araç bugün koşulduğunda "7/7 eşdeğer" der ve bu **doğrudur**;
# doğru olmayan, o cümleyi *"bugünkü taramanın sonucu"* diye okumaktır.
# B-24'ün ("araç doğru, girdisi bayat") deseni, üçüncü kez.
#
# Üzerindeki testler (`test_b52_*`) YAPISALDIR: her girdinin `yol` taşıdığına
# bakar, girdilerin bugünkü taramaya ait olup olmadığına BAKMAZ.
#
# 🔒 Tazelemek için: `python dogrulama/kor_mutasyon.py 24` (~18 dk), sonra
# çıkan sağ kalanlarla bu liste yeniden türetilir ve bu başlık güncellenir.
SAG_KALANLAR = [
    # Parça sınırı — İKİ ayrı yerde aynı desen. Bağlamla ayrıştırılır.
    SagKalan("T01_parca_siniri_carpisma_kapali", "sim/mac.py", 0,
             "            for t in (baska.baslangic_s, baska.bitis_s):\n"
             "                if il.baslangic_s < t < il.bitis_s:",
             "            for t in (baska.baslangic_s, baska.bitis_s):\n"
             "                if il.baslangic_s <= t < il.bitis_s:", "lt_le",
             # B-52: parça sınırı yolu alım değerlendirmesinden geçer
             yol="mac_basarisiz_alim"),
    SagKalan("T02_parca_siniri_darbe_kapali", "sim/mac.py", 0,
             "                    t = (k + kesir - kj.faz_kesri) * p\n"
             "                    if il.baslangic_s < t < il.bitis_s:",
             "                    t = (k + kesir - kj.faz_kesri) * p\n"
             "                    if il.baslangic_s <= t < il.bitis_s:", "lt_le",
             # B-52: darbe dalı S4'te 8 293 kez çalışıyor
             yol="mac_basarisiz_alim"),
    # Hata mesajı METNİ — beklenen sonuç: eşdeğer (metin, davranış değil)
    SagKalan("T03_assert_mesaji_metni", "sim/kosucu.py", 0,
             'f"koşu bitiminden sonra beacon: {self.olaylar.simdi} > "',
             'f"koşu bitiminden sonra beacon: {self.olaylar.simdi} >= "',
             "metin",
             # B-52: yalnızca bir hata METNİ — tetiklenecek yol yok
             yol=YOLSUZ),
    SagKalan("T04_sira_sayaci_isareti", "sim/mac.py", 0,
             "        self._sira_sayaci[dugum] += 1",
             "        self._sira_sayaci[dugum] -= 1", "arti_eksi",
             "mac_kopya_alim"),
    SagKalan("T05_sonuc_dizini_olusturma", "sim/results.py", 0,
             "        self.dosya.parent.mkdir(parents=True, exist_ok=True)",
             "        self.dosya.parent.mkdir(parents=False, exist_ok=True)",
             "true_false",
             # 🔴 B-52: `SonucYazici` bu matriste HİÇ kurulmuyor; karar
             # "eşdeğer" DEĞİL, "bu matriste hiç koşmadı"
             yol=YOLSUZ),
    # ⚠️ `m.durum = "gonderiyor"` iki yerde geçiyor (yayın ve veri).
    # `_ilet` olanı jeton artırımıyla birlikte; bağlam ondan alındı.
    SagKalan("T06_ilet_jetonu_isareti", "sim/mac.py", 0,
             "    def _ilet(self, dugum: int) -> None:\n"
             "        m = self.mac[dugum]\n"
             '        m.durum = "gonderiyor"\n'
             "        m.jeton += 1",
             "    def _ilet(self, dugum: int) -> None:\n"
             "        m = self.mac[dugum]\n"
             '        m.durum = "gonderiyor"\n'
             "        m.jeton -= 1", "arti_eksi",
             # B-52: jeton tekilliği — sayaçla ölçülebilir bir yolu yok
             yol=YOLSUZ),
    # ⚠️ Bu desen `alim_per` ve `_alim_basarili_mi`de İKİ kez geçiyor.
    # Kör tarayıcı ikincisini (satır 614) vurmuştu; bağlam ondan.
    SagKalan("T07_yari_cift_yonlu_siniri", "sim/mac.py", 0,
             "        # Dogrusu: alici, bu cercevenin SURESI BOYUNCA herhangi bir an\n"
             "        # gonderiyorduysa duyamaz.\n"
             "        g_bas, g_bit = self.gonderim_araligi[alici]\n"
             "        if g_bas < il.bitis_s and il.baslangic_s < g_bit:",
             "        # Dogrusu: alici, bu cercevenin SURESI BOYUNCA herhangi bir an\n"
             "        # gonderiyorduysa duyamaz.\n"
             "        g_bas, g_bit = self.gonderim_araligi[alici]\n"
             "        if g_bas <= il.bitis_s and il.baslangic_s < g_bit:",
             "lt_le", "mac_basarisiz_alim"),
]


# Mutant kopyanın İÇİNDE koşacak betik. Sonuç sözlüğünü JSON olarak basar.
# `topoloji`/`trafik` alt sözlükleri de dahil — kurulum değişikliği de görünsün.
KOSUCU_BETIGI = '''
import json, sys
sys.path.insert(0, ".")
from sim.config import Konfig
from dogrulama.olcum import olc
from dogrulama.aktaricilar import AKTARICILAR

# 🔴 ALT SÜREÇ ÇIKTISI UTF-8 OLARAK ÇÖZÜLÜR (20 Ağu 2026).
# `subprocess.run(..., text=True)` kodlama verilmezse çıktıyı YEREL KOD
# SAYFASIYLA çözer. Bu makinede o cp1254 ve çocuk süreç UTF-8 basıyor
# (PYTHONIOENCODING ayarlı). Türkçe "Ş" (U+015E → C5 9E) gibi karakterler
# cp1254'te TANIMSIZ olduğu için ebeveyn `UnicodeDecodeError` fırlatır ve
# araç, işini bitirmişken çöker. Ölçüldü: bir doğrulama koşusu tam olarak
# böyle düştü. `errors="replace"` ile ayrıştırma asla çökmez.

SENARYOLAR = %r
TRAFIKLER = %r
TOHUMLAR = %r
UC_DURUMLAR = %r
UC_TOHUMLAR = %r

cikti = {}
for s in SENARYOLAR:
    for t in TRAFIKLER:
        for tohum in TOHUMLAR:
            cikti["ana/%%s/%%s/%%d" %% (s, t, tohum)] = olc(
                Konfig(kol="ayikla", senaryo=s, trafik=t, tohum=tohum),
                AKTARICILAR["en_kisa_yol"])

# UC DURUMLAR — dort dusme sebebini fiilen tetikler (Y8)
for ad, aktarici, ek in UC_DURUMLAR:
    for tohum in UC_TOHUMLAR:
        kw = dict(ek)
        trafik = kw.pop("trafik", "orta")
        cikti["uc/%%s/%%d" %% (ad, tohum)] = olc(
            Konfig(kol="ayikla_uc", senaryo="S2", trafik=trafik,
                   tohum=tohum, **kw), AKTARICILAR[aktarici])

print("---JSON---")
print(json.dumps(cikti, sort_keys=True, default=str))
''' % (SENARYOLAR, TRAFIKLER, TOHUMLAR, UC_DURUMLAR, UC_TOHUMLAR)


def _imza(hedef: Path) -> dict:
    """Verilen depo kopyasında matrisi koşar, sonuç sözlüklerini döndürür."""
    betik = hedef / "_ayikla_kosucu.py"
    betik.write_text(KOSUCU_BETIGI, encoding="utf-8")
    p = subprocess.run(
        [sys.executable, str(betik)], cwd=hedef, capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=3600,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    if "---JSON---" not in p.stdout:
        return {"__hata__": (p.stderr or p.stdout)[-400:]}
    return json.loads(p.stdout.split("---JSON---", 1)[1])


def _kopya(mutasyon: SagKalan | None) -> Path:
    gecici = Path(tempfile.mkdtemp(prefix="ayikla_"))
    hedef = depoyu_kopyala(gecici / "depo")
    if mutasyon is not None:
        yol = hedef / mutasyon.dosya
        metin = yol.read_text(encoding="utf-8")
        if mutasyon.eski not in metin:
            raise RuntimeError(f"mutasyon uygulanamadı: {mutasyon.ad}")
        yol.write_text(metin.replace(mutasyon.eski, mutasyon.yeni, 1),
                       encoding="utf-8")
    return hedef


def _tetiklendi(taban: dict, yol: str) -> bool:
    """Bu yol taban matrisinde fiilen tetiklendi mi? (Y8)"""
    return sum(abs(r.get(yol) or 0) for r in taban.values()) > 0


# 🔴 B-113 (ALTINCI DENETİM) — KARAR KANALI SATÜREYDİ
#
# B-46/K-051 (21 Ağustos) `sonuc()`e `kaynak_hash` ekledi ve o hash
# **`sim/` altındaki tüm `.py` dosyalarının içeriğini** kapsıyor. Bu araç
# ise her koşunun TAM sonuç sözlüğünü tabanla karşılaştırıyor.
#
#   ⇒ `sim/` altındaki HER mutasyon `kaynak_hash`i değiştirir
#   ⇒ her matris hücresi farklı çıkar
#   ⇒ `durum = "degisti"` — HER ZAMAN
#
# Yani `"esdeger"`, `"karar_yok"` ve `"yolsuz"` dalları `sim/` mutasyonları
# için **ULAŞILAMAZDI**. Altıncı denetim aracın KENDİ `_kosu`/`_imza`sıyla
# ölçtü: üç mutantın üçünde de tek fark `['kaynak_hash']`.
#
# 🔴 Yayımlanan çıktı (`ciktilar/ayikla_cikti.txt`, 20 Ağu, "7/7 eşdeğer")
# B-46'dan **bir gün önceye** ait ve araç o günden beri hiç koşulmadı.
#
# 🔴 VE ONU KORUYAN TEST BİR GREP'Tİ: `test_b52_*` dalın VAR OLDUĞUNU
# doğruluyordu, ULAŞILABİLİR olduğunu değil — `03`ün *"tetiklenemeyen
# kontrol"* kuralı, korumanın kendisinde.
#
# ⚠️ `konfig` de karşılaştırma dışı DEĞİLDİR ve olmamalı: mutasyon
# konfigürasyonu değiştirmiyorsa aynı kalır, değiştiriyorsa bu GERÇEK bir
# farktır ve görülmelidir.
KARSILASTIRMA_DISI = ("kaynak_hash",)


def imza_karsilastir(taban: dict, imza: dict) -> list:
    """İki matrisin farklı hücreleri — `kaynak_hash` HARİÇ.

    🔴 Ayrı ve test edilebilir bir yüklem (`03` B5): dalların
    ULAŞILABİLİRLİĞİ ancak böyle sınanabilir. Gömülü hâli yalnızca
    grep'lenebiliyordu (B-113'ün asıl dersi).
    """
    farklar = []
    for anahtar in sorted(taban):
        a = {k: v for k, v in taban[anahtar].items()
             if k not in KARSILASTIRMA_DISI}
        ham_b = imza.get(anahtar) or {}
        b = {k: v for k, v in ham_b.items() if k not in KARSILASTIRMA_DISI}
        if a == b:
            continue
        farklar.append((anahtar, sorted(k for k in a if a.get(k) != b.get(k))))
    return farklar


def karar_ver(farklar: list, yol: str, taban: dict) -> str:
    """Dört kovadan biri — ayrı ve test edilebilir (`03` B5)."""
    if farklar:
        return "degisti"
    if yol is YOLSUZ:
        # 🔴 B-52 — YOLSUZ beyanı: tetiklenebilir bir sayaç yolu YOK.
        # "Eşdeğer" demek burada meşru DEĞİL; ölçüm bir şey söyleyemiyor.
        return "yolsuz"
    if not _tetiklendi(taban, yol):
        # 🔴 B-36 — "eşdeğer" DEĞİL, "yol tetiklenmedi". Mutasyonun bağlı
        # olduğu sayaç bu matriste hiç artmadıysa, "fark yok" ile "o kod hiç
        # koşulmadı" aynı çıktıyı verir ve karar VERİLEMEZ (Y8).
        return "karar_yok"
    return "esdeger"


def _kosu(arg) -> dict:
    m, taban = arg
    hedef = None
    try:
        hedef = _kopya(m)
        imza = _imza(hedef)
        if "__hata__" in imza:
            return {"ad": m.ad, "durum": "cokme", "detay": imza["__hata__"]}

        farklar = imza_karsilastir(taban, imza)
        durum = karar_ver(farklar, m.yol, taban)
        return {"ad": m.ad, "durum": durum, "yol": m.yol,
                "farkli_kosu": len(farklar), "toplam_kosu": len(taban),
                "ornek": farklar[:3]}
    except RuntimeError as e:
        # 🔴 B-24 — ARAÇ HATASI, BULGU DEĞİL.
        # Mutasyon deseni dosyada bulunamadı: GİRDİ LİSTESİ BAYATLAMIŞ.
        # Önceki sürüm bunu `degisen` listesine koyup altına "hiçbir testin
        # görmediği bir davranış değişikliğidir — yani korumasız bir kod
        # yolu" basıyordu. Yani araç, KENDİ GİRDİSİNİN bayatlığını
        # korumasız kod yolu diye raporluyordu (Y7, yedinci kez).
        #
        # Bu fiilen yaşandı: S02'nin hedef aldığı satır B-13 kapanışında
        # `assert`e çevrildi ve araç "5 korumasız yol" dedi — doğrusu 4'tü.
        return {"ad": m.ad, "durum": "arac_hatasi", "yol": m.yol,
                "detay": str(e)[:300]}
    except Exception as e:                        # noqa: BLE001
        return {"ad": m.ad, "durum": "hata", "detay": repr(e)[:300]}
    finally:
        if hedef is not None:
            shutil.rmtree(hedef.parent, ignore_errors=True)


def main() -> None:
    n_ana = len(SENARYOLAR) * len(TRAFIKLER) * len(TOHUMLAR)
    n = n_ana + len(UC_DURUMLAR) * len(UC_TOHUMLAR)
    print("=" * 78)
    print("SAĞ KALAN MUTANT AYIKLAYICI — eşdeğer mi, gerçek boşluk mu?")
    print("=" * 78)
    print(f"Sağ kalan sayısı : {len(SAG_KALANLAR)}")
    print(f"Koşu matrisi     : {len(SENARYOLAR)} senaryo × "
          f"{len(TRAFIKLER)} trafik × {len(TOHUMLAR)} tohum = {n_ana} ana koşu")
    print(f"                 + {len(UC_DURUMLAR)} uç durum × "
          f"{len(UC_TOHUMLAR)} tohum = {n - n_ana} koşu  →  TOPLAM {n}")
    print(f"   senaryolar    : {', '.join(SENARYOLAR)}")
    print(f"   trafik        : {', '.join(TRAFIKLER)}")
    print(f"   tohumlar      : {TOHUMLAR}  (ayarlama kümesi; 2000–2029 KOŞULMAZ)")
    print(f"   uç durumlar   : {', '.join(a for a, _, _ in UC_DURUMLAR)}")
    print("Karşılaştırılan  : her koşunun TAM sonuç sözlüğü")
    print()
    print("⚠️ Bu araç eşdeğerliği KANITLAYAMAZ. 'Eşdeğer' = 'bu matriste hiçbir")
    print("   metrik değişmedi'. Daha geniş bir matris farklı sonuç verebilir.")
    print()

    t0 = time.perf_counter()
    print("TABAN — mutasyonsuz kopyada matris koşuluyor...")
    hedef = _kopya(None)
    try:
        taban = _imza(hedef)
    finally:
        shutil.rmtree(hedef.parent, ignore_errors=True)
    if "__hata__" in taban:
        print(f"🔴 TABAN KOŞULAMADI: {taban['__hata__']}")
        sys.exit(1)
    # 🔴 Y7 — araç ne koşturduğunu kendisi doğrular.
    if len(taban) != n:
        print(f"🔴 TABAN EKSİK: {len(taban)} koşu, beklenen {n}. Durduruldu.")
        sys.exit(1)
    print(f"  OK taban hazır — {len(taban)} koşu, "
          f"{(time.perf_counter()-t0)/60:.1f} dk")

    # 🔴 Y8 — "eşdeğer" kararının geçerli olması için ilgili yolun TETİKLENMİŞ
    # olması gerekir. Tetiklenmemiş bir yolda hiçbir mutasyon fark yaratmaz ve
    # "eşdeğer" damgası YANILTICI olur. Sayaçlar burada basılır ki okuyucu
    # kararı tetiklenmeyle birlikte görsün.
    tetik = {}
    for alan in ("ttl_olumu", "kuyruk_tasmasi", "hedef_yok", "mac_dusurmesi",
                 "mac_kopya_alim", "donguyle_olen", "mac_deneme"):
        tetik[alan] = sum(r.get(alan) or 0 for r in taban.values())
    print("  TETİKLENME (Y8) — bu matriste kaç kez gerçekleşti:")
    for alan, v in tetik.items():
        isaret = "OK " if v else "!! "
        print(f"    {isaret}{alan:18s} {v}")
    if not all(tetik.values()):
        print("    ⚠️ Sıfır olan bir yol için 'eşdeğer' kararı GEÇERSİZDİR.")
    print()

    with Pool(min(len(SAG_KALANLAR), 6)) as havuz:
        sonuclar = havuz.map(_kosu, [(m, taban) for m in SAG_KALANLAR])

    isaret = {"degisti": "🔴 DEĞİŞTİ ", "esdeger": "⚪ eşdeğer ",
              "cokme": "⚠️ ÇÖKME  ", "hata": "⚠️ HATA    "}
    degisen: list[str] = []
    # 🔴 B-24 — ARAÇ HATASI AYRI KOVADA.
    # Mutasyon deseni dosyada bulunamazsa bu bir BULGU değil, girdi
    # bayatlığıdır; `degisen`e girerse araç kendi bakım eksikliğini
    # "korumasız kod yolu" diye raporlar (Y7, yedinci kez).
    arac_hatasi: list[str] = []
    for r in sonuclar:
        m = next(x for x in SAG_KALANLAR if x.ad == r["ad"])
        print("-" * 78)
        print(f"{isaret[r['durum']]} {r['ad']}")
        print(f"    {m.dosya}:{_satir_no(m)}  [{m.kural}]")
        print(f"    -  {m.eski.strip().splitlines()[-1][:70]}")
        print(f"    +  {m.yeni.strip().splitlines()[-1][:70]}")
        if r["durum"] == "degisti":
            degisen.append(r["ad"])
            print(f"    farklı koşu : {r['farkli_kosu']}/{r['toplam_kosu']}")
            for anahtar, alanlar in r["ornek"]:
                print(f"       {anahtar}: {', '.join(alanlar[:6])}")
        elif r["durum"] in ("cokme", "hata"):
            degisen.append(r["ad"])
            print(f"    detay : {r.get('detay', '')[:200]}")

    print()
    print("=" * 78)
    print(f"Süre: {(time.perf_counter()-t0)/60:.1f} dk")
    print(f"🔴 DAVRANIŞI DEĞİŞTİREN : {len(degisen)}")
    yolsuzlar = [r["ad"] for r in sonuclar if r.get("durum") == "yolsuz"]
    print(f"⚪ bu matriste eşdeğer  : "
          f"{len(sonuclar) - len(degisen) - len(arac_hatasi) - len(yolsuzlar)}")
    print(f"🔧 ARAÇ HATASI (girdi bayat) : {len(arac_hatasi)}")
    # 🔴 B-52: YOLSUZ girdiler "eşdeğer" sayılmaz — ölçüm onlar
    # hakkında bir şey SÖYLEYEMEZ ve bu açıkça yazılır.
    print(f"⛔ YOLSUZ (ölçülemez)   : {len(yolsuzlar)}")
    if yolsuzlar:
        for _ad in yolsuzlar:
            print(f"     {_ad}")
    kararsiz = [r["ad"] for r in sonuclar if r.get("durum") == "karar_yok"]
    if kararsiz:
        print()
        print("!" * 78)
        print("❓ KARAR VERİLEMEDİ — bağlı olduğu yol bu matriste TETİKLENMEDİ:")
        for _ad in kararsiz:
            _y = next(m.yol for m in SAG_KALANLAR if m.ad == _ad)
            print(f"     {_ad}  (yol: {_y})")
        print("   'Fark yok' ile 'o kod hiç koşulmadı' aynı çıktıyı verir (Y8).")
        print("   Matrise o yolu tetikleyen bir uç durum eklenmeden okunamaz.")
        print("!" * 78)

    if arac_hatasi:
        print()
        print("!" * 78)
        print("🔧 GİRDİ LİSTESİ BAYAT — bu bir BULGU DEĞİL, bakım işidir:")
        for _ad in arac_hatasi:
            print(f"     {_ad}")
        print("   Mutasyon deseni artık dosyada yok (kod değişmiş olmalı).")
        print("   Desen güncellenmeden bu aracın çıktısı okunamaz.")
        print("!" * 78)
    if degisen:
        print()
        print("Bunların her biri, hiçbir testin görmediği bir davranış")
        print("değişikliğidir — yani korumasız bir kod yolu:")
        for ad in degisen:
            print(f"     {ad}")
        print("Kural 10: 'düşük öncelik' deyip bırakılamaz.")


if __name__ == "__main__":
    main()
