"""
ÜÇ ÜRETİCİ ARACIN ÇAPA TESTİ — B-130 *(yedinci bağımsız denetim)*.

🔴 NEDEN BU DOSYA VAR
=====================
`gecerlilik.py` · `pencere_kapsami.py` · `li_calisma_noktasi.py` —
**`06`nın üç geçerlilik koşulunu ve `08`in iki maddesini üreten araçlar** —
hiçbir test modülü tarafından **içe aktarılmıyordu**. Denetim ölçtü:

    üç araca 10 hedefli mutasyon  ->  0 yakalandı
    %95 GA [%0,0 · %27,8]         ->  "gerçek kapsam en fazla %25,9"

Ve mutasyonların ne yaptığı önemliydi. Örneğin **V3**:
`ortak_p95.append(o.p95_farki_s)` → `o.gecikme_farki_s`. Bu **tek satır**,
`06` §8.1b'nin *"kuyruk merkezden ~5 kat fazla kötüleşiyor
(+28,15 ↔ +5,40 ms)"* cümlesini **+5,40 ↔ +5,40** yapar — reçetenin **en
güçlü gerekçesini** sessizce siler ve 462 testin hiçbiri kırılmaz.

🔒 ÇÖZÜM — KOŞU GEREKTİRMEYEN ÇAPA
==================================
Bu araçların karar yüklemleri **saf fonksiyonlardır** ve depodaki
`ciktilar/sonuclar/*.jsonl` satırlarıyla beslenebilir. Bu dosya onları
**sentetik ve gerçek** girdilerle sabitler; tam koşu açmaz.

⚠️ **KAPSAMI (Y11 — koruma kendi sınırıyla yazılır):**
| vaka | yakalanır mı |
|---|---|
| karar yükleminin **hesabı** bozulursa | ✅ |
| okuma **etiketi** yanlış büyüklüğe bağlanırsa *(V3 · B-121 sınıfı)* | ✅ |
| 🆕 **`sim/` değişmişken** yukarıdaki iki vaka | ✅ **B-143'ten sonra** |
| `main()` içindeki akış bozulursa *(V4 · P3 sınıfı)* | ❌ **HAYIR** — `main()` çağrılmıyor |
| tam koşunun **fiziği** bozulursa | ❌ o `sim/`in mutasyon paketinin işi |
| 🔴 çapa verisinin **GÜNCEL** olup olmadığı | ❌ bu dosyanın işi değil — **kapı Ç1.5** ve `06`/`13`/README'deki bayatlık beyanı (B-129) |

🔴 **B-143 ÖNCESİ ÖLÇÜLEN — ve düzeltmeden sonra yeniden ölçülen:**

| | `sim/` temiz | `sim/` değişmiş |
|---|---|---|
| **önce** *(8. denetim)* | `9 passed` · 8 mutasyonun **7'si** | 🔴 `4 passed, 5 skipped` · **6'sı** |
| 🟢 **sonra** *(B0.9)* | `11 passed` · **8/8** | 🟢 `11 passed` · **8/8** |

Eşleştirilmiş fark **0** *(önce 1, McNemar yönü tek taraflıydı)*. Üretici:
`scratchpad/olcum/m_b143_etki.py` — iç içe, aynı mutasyon kümesi, iki durum.
"""

from __future__ import annotations

import ast
import json
import pathlib

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
SONUC = KOK / "ciktilar" / "sonuclar"


# ==========================================================================
# gecerlilik.py — `06` §9.1 (koşul 1) · §8.1b (koşul 2) · koşul 3
# ==========================================================================

def _satirlar(dosya: str) -> list[dict]:
    yol = SONUC / dosya
    if not yol.exists():
        pytest.skip(f"{dosya} yok — üretici henüz koşmamış")
    return [json.loads(s) for s in yol.open(encoding="utf-8") if s.strip()]


# ==========================================================================
# 🔴 B-143 (SEKİZİNCİ DENETİM) — ÇAPA `sim/` DEĞİŞİNCE SUSUYORDU
# ==========================================================================
# Önceki hâl satırları **bugünkü `kaynak_hash`e** göre süzüyor ve eşleşme
# yoksa `pytest.skip` çağırıyordu. Ölçüldü (kopyada, `sim/packet.py`ye tek
# zararsız yorum):
#
#     A · sim/ TEMİZ    ->  9 passed in 3.31s
#     B · sim/ DEĞİŞMİŞ ->  4 passed, 5 skipped in 1.94s
#
# Yani üç üreticinin TEK koruması, korumaya en çok ihtiyaç duyulan anda
# susuyordu — ve **B1'in ilk işi `sim/`e Kat 4 eklemektir.**
#
# 🔒 ÇÖZÜM VE NEDEN "fail" DEĞİL:
# `skip`i `fail`e çevirmek yanlış olurdu. Ç1.3'ün 41 mutasyonunun 41'i de
# `sim/` altındadır (ölçüldü); her mutantta `kaynak_hash` değişir, yani bu
# beş test **41 mutantın 41'inde de** kırılır ve kapı onları "EVRENSEL
# KIRICI" diye işaretler — mutasyon ölçümü bozulur.
#
# Doğru ayrım: çapanın sorusu *"bu yüklemler hâlâ doğru hesaplıyor mu"*dur;
# bu soru BUGÜNKÜ `sim/`den üretilmiş satır gerektirmez, **kendi içinde
# tutarlı** bir satır kümesi gerektirir. Bu yüzden çapa artık dosyadaki
# **EN SON YAZILAN hash grubunu** kullanır: grup tek bir kod sürümünden
# gelir (`ortak_alt_kume`nin kendi `kaynak_hash` kontrolü bunu zorlar) ve
# **asla boş olmaz**.
#
# ⚠️ Verinin GÜNCEL olup olmadığı ayrı bir sorudur ve ayrı yerde zorlanır:
#   · `test_b143_capa_verisi_TEK_kod_surumunden`  — grup karışık değil
#   · `test_b143_capa_dosyasi_KAPI_KRITERINDE`    — dosya kapıda (Y12)
#   · kapı kriteri **Ç1.5** — bir test atlanırsa `!!SEÇİM` ile DÜŞER
#   · `06`/`13`/README — kapının bayatlığı zaten sekiz belgede yazılı (B-129)
# ==========================================================================

def _en_son_hash_grubu(satirlar: list[dict]) -> tuple[str, list[dict]]:
    """Dosyadaki **en son yazılan** `kaynak_hash` grubunu döndürür.

    🔴 Neden "en son yazılan" ve "en çok satırlı" DEĞİL: `.jsonl` `append`
    modunda büyür (`08` md 36), yani dosya sırası zaman sırasıdır. Eski bir
    grup daha kalabalık olabilir — ölçüldü: `gecerlilik.jsonl`de
    `0a1a94e5…` altında **480 satır (240 anahtar 2×)**, güncel `fc73905b…`
    altında **360**. En kalabalığı seçen bir kural, aynı anahtarı iki kez
    okur ve `n` iki katına çıkar (B-164'ün yanlış okuma vakası).
    """
    if not satirlar:
        pytest.skip("dosya boş — üretici henüz koşmamış")
    h = satirlar[-1]["kaynak_hash"]
    return h, [d for d in satirlar if d["kaynak_hash"] == h]


@pytest.fixture(scope="module")
def gecerlilik_veri():
    """Dosyadaki EN SON koşu grubu — `veri` sözlüğü biçiminde.

    🔴 B-143: `sim/` değişse bile **atlanmaz**; bkz. yukarıdaki blok.
    """
    _, grup = _en_son_hash_grubu(_satirlar("gecerlilik.jsonl"))
    veri = {}
    for d in grup:
        veri[(d["kol_adi"], d["senaryo_etiket"], d["uzunluk"],
              d["konfig"]["tohum"])] = d["metrikler"]
    assert veri, (
        "🔴 çapa verisi BOŞ — `gecerlilik.jsonl` satır taşıyor ama hiçbiri "
        "okunamadı. Çapa sessizce boşalmış demektir (Y7: boş küme de "
        "0 kırık verir).")
    return veri


def test_b143_capa_verisi_TEK_kod_surumunden():
    """🔴 B-143 — çapa iki farklı kod sürümünün satırını KARIŞTIRMAMALI.

    `.jsonl` `append` modunda büyüyor (`08` md 36) ve bugün üç ayrı
    `kaynak_hash` taşıyor. Karışık bir grup okunursa `ortak_alt_kume`nin
    kod sürümü kontrolü tetiklenir ve koşul 2 **sessizce boşalır**.
    """
    for dosya in ("gecerlilik.jsonl", "pencere_kapsami.jsonl"):
        h, grup = _en_son_hash_grubu(_satirlar(dosya))
        assert grup, f"{dosya}: en son hash grubu boş"
        assert {d["kaynak_hash"] for d in grup} == {h}, (
            f"🔴 {dosya}: çapa grubu KARIŞIK kod sürümü taşıyor")


def test_b143_capa_dosyasi_KAPI_KRITERINDE():
    """🔴 B-144 (Y12) — bu dosya bir kapı kriterinde OLMAK ZORUNDA.

    Ölçüldü (sekizinci denetim): dosya hiçbir kriterde yoktu ve
    `_pytest()` yalnızca `passed`/`failed` ayrıştırdığı için bir `skip`
    kapıyı **düşürmüyordu** — `"468 passed, 5 skipped"` satırından
    `gecen=468, kirilan=0` çıkar ve ölçüt geçer.

    🔒 Kriterin `adet`i verildiği için artık bir test atlanırsa
    `gecen + kirilan != adet` olur ve kapı `!!SEÇİM` ile DÜŞER.
    """
    from dogrulama.aile0_kapi_raporu import KAPI_SECIMLERI

    bu = "tests/test_gecerlilik_araclari.py"
    tasiyan = [k for k, v in KAPI_SECIMLERI.items() if bu in v.yollar]
    assert tasiyan, (
        f"🔴 {bu} hiçbir kapı kriterinde YOK. Üç üreticinin tek koruması "
        f"kapı tarafından hiç koşulmuyor demektir (B-144).")
    for k in tasiyan:
        assert KAPI_SECIMLERI[k].adet is not None, (
            f"🔴 {k} kriterinin `adet`i yok — bir test sessizce atlanırsa "
            f"kapı bunu göremez (B-144).")


def test_b130_kosul2_DORT_okumayi_da_uretiyor(gecerlilik_veri):
    """🔴 B-121 + V3 — dört okuma, ve her biri KENDİ büyüklüğünden.

    V3 mutasyonu *(ORTAK p95 aslında ORTAK ortalamayı basıyor)* buradan
    yakalanır: iki okumanın medyanı **aynı çıkamaz**, çünkü p95 farkı
    ortalama farkından ölçülebilir biçimde büyüktür.
    """
    from dogrulama.gecerlilik import kosul2

    sonuc = kosul2(gecerlilik_veri)
    okumalar = {(r["kol"], r["metrik"]): r for r in sonuc}
    kollar = {k for k, _ in okumalar}
    assert kollar, "hiç kol ölçülmemiş"

    for kol in kollar:
        adlar = {m for k, m in okumalar if k == kol}
        assert adlar == {"HAM ortalama", "HAM p95",
                         "ORTAK ortalama", "ORTAK p95"}, (
            f"{kol}: dört okuma bekleniyordu, {sorted(adlar)} var")

        # 🔴 V3 — ORTAK çift. Ve 🔴 B-143/X6 — HAM çift de aynı yükleme
        # bağlanır: sekizinci denetim ölçtü, `("HAM p95", ham_p95)` yerine
        # `ham_ort` yazan bir mutasyon `sim/` temizken bile SAĞ KALIYORDU.
        # B-121 tam olarak bu satırı eklemişti (`06` §8.1b'nin TAŞIYICI
        # satırı) ve hiçbir test onu koruyordu.
        for etiket, a_ad, b_ad in (
                ("ORTAK", "ORTAK ortalama", "ORTAK p95"),
                ("HAM", "HAM ortalama", "HAM p95")):
            ort = okumalar[(kol, a_ad)]["medyan_fark"]
            p95 = okumalar[(kol, b_ad)]["medyan_fark"]
            assert ort != p95, (
                f"🔴 {kol}: {etiket} p95 ile {etiket} ortalama AYNI sayı "
                f"({ort}) — p95 yanlış büyüklükten okunuyor olabilir "
                f"(V3 · B-121)")
            assert abs(p95) > abs(ort), (
                f"🔴 {kol}: |{etiket} p95 farkı| ({p95}) |{etiket} ortalama "
                f"farkı|ndan ({ort}) büyük değil — kuyruk merkezden fazla "
                f"kötüleşmeli")


def test_b130_kosul1_KISA_ile_TAM_i_karsilastiriyor(gecerlilik_veri):
    """🔴 V2 — `UZUNLUKLAR["kisa"]` `tam` ile aynı yapılırsa test BOŞALIR.

    Boş bir test *"tüm farklar sıfır → TANIMSIZ"* verir ve hiçbir şey
    ölçmez (Y7'nin *"boş küme de 0 kırık verir"* tuzağı).
    """
    from dogrulama.gecerlilik import UZUNLUKLAR, kosul1

    assert UZUNLUKLAR["kisa"] != UZUNLUKLAR["tam"], (
        "kısa ve tam koşu aynı — koşul 1 kendi kendisiyle karşılaştırılıyor")

    sonuc = kosul1(gecerlilik_veri)
    assert sonuc, "koşul 1 hiç satır üretmedi"
    tanimli = [r for r in sonuc if r["p"] is not None]
    assert len(tanimli) == len(sonuc), (
        f"🔴 {len(sonuc) - len(tanimli)} satır TANIMSIZ — tüm farklar sıfır "
        f"çıkıyorsa kısa/tam ayrımı kaybolmuş olabilir (V2)")


def test_b130_kosul1_farkin_ISARETI_kisa_eksi_tam(gecerlilik_veri):
    """🔴 V1 — farkın işareti ters çevrilirse hangi kolun düştüğü değişir.

    Yükleme bağımsız bir yeniden hesapla bağlanır: bilinen bir kol/metrik
    çifti için fark, satırlardan elle hesaplanan `kısa − tam` ile aynı
    işareti taşımalı.
    """
    import statistics as ist

    from dogrulama.gecerlilik import kosul1

    sonuc = {(r["kol"], r["senaryo"], r["metrik"]): r for r in kosul1(gecerlilik_veri)}
    hedef = ("en_kisa_yol", "S0", "teslim_orani")
    if hedef not in sonuc:
        pytest.skip("beklenen kol/senaryo bu koşuda yok")

    elle = []
    for t in range(1, 31):
        a = gecerlilik_veri.get(("en_kisa_yol", "S0", "kisa", t))
        b = gecerlilik_veri.get(("en_kisa_yol", "S0", "tam", t))
        if a and b:
            elle.append(a["teslim_orani"] - b["teslim_orani"])
    assert elle, "elle hesap için satır yok"
    assert sonuc[hedef]["medyan_fark"] == pytest.approx(ist.median(elle)), (
        "🔴 koşul 1'in farkı `kısa − tam` değil — işaret ters olabilir (V1)")


def test_b130_kosul3_BAGLAYICI_cifti_okuyor():
    """🔴 B-135 — koşul 3'ün bağlayıcı çifti ilan edilmiş olmalı."""
    from dogrulama.gecerlilik import BAGLAYICI_CIFT, KOLLAR

    assert BAGLAYICI_CIFT == ("DV", "gurultuden_kacan")
    for k in BAGLAYICI_CIFT:
        assert k in KOLLAR, (
            f"🔴 bağlayıcı çiftin kolu `{k}` ölçülebilir kollarda YOK — "
            f"koşul 3'ü ölçen araç bağlayıcı oranı üretemez (B-135)")


def test_b130_kosul3_tohum_std_HESAPLANIYOR(gecerlilik_veri):
    """🔴 V5 — tohum std'si hesaplanmazsa GA/std sütunu daima boş kalır."""
    from dogrulama.gecerlilik import kosul1

    sonuc = kosul1(gecerlilik_veri)
    dolu = [r for r in sonuc if r.get("ga_std_kati") is not None]
    assert dolu, (
        "🔴 hiçbir satırda GA/std yok — `tohum_std` hesaplanmıyor olabilir "
        "(V5). Dışlanan etki büyüklüğü `03` B2 gereği zorunludur")


# ==========================================================================
# pencere_kapsami.py — `08` madde 31
# ==========================================================================

def test_b130_pencere_dis_pay_ve_carpiklik_TERS_DEGIL():
    """🔴 P1 · P2 — pay yanlış paydadan, çarpıklık ters çevrilirse.

    İkisi de bağımsız bir yeniden hesapla bağlanır; sentetik girdi
    kullanılıyor, koşu açılmıyor.
    """
    from dogrulama.pencere_kapsami import carpiklik, dis_pay

    s = {"kontrol_bayt": 1000.0, "kontrol_bayt_pencere": 800.0}
    assert dis_pay(s, "kontrol_bayt") == pytest.approx(20.0), (
        "pencere dışı pay (tüm − pencere)/tüm olmalı")
    assert carpiklik(s, "kontrol_bayt") == pytest.approx(1.25), (
        "çarpıklık tüm/pencere olmalı — ters çevrilmiş olabilir (P2)")

    # 🔴 Y8 — yüklem sağlam girdide de bir şey üretiyor mu (boş küme tuzağı)
    assert dis_pay({"kontrol_bayt": 0, "kontrol_bayt_pencere": 0},
                   "kontrol_bayt") is None


def test_b130_olu_kolunun_ANALITIK_capasi_hala_gecerli():
    """🔒 B-120 — kalan TEK analitik çapa: `olu` yalnız beacon üretir.

    Bu, bandın kendisi ampirik olsa da **analitik olan** tek ilişkidir ve
    `pencere_kapsami.py` onu `assert` ile zorluyor. Burada aynı ilişki
    depodaki gerçek satırlardan doğrulanır.
    """
    from dogrulama.pencere_kapsami import carpiklik

    # 🔴 B-143 — `kaynak_hash()` süzgeci KALDIRILDI: `sim/` değişince bu
    # analitik çapa da susuyordu ve B-120'nin bıraktığı TEK analitik
    # ilişkiydi. Artık dosyanın en son koşu grubundan okunur.
    _, grup = _en_son_hash_grubu(_satirlar("pencere_kapsami.jsonl"))
    olcum = [d for d in grup if d.get("kol_adi") == "olu"]
    assert olcum, (
        "🔴 en son koşu grubunda `olu` kolu YOK — B-120'nin kalan tek "
        "analitik çapası ölçülemiyor (Y7: boş küme de 0 kırık verir)")

    m0 = olcum[0]["metrikler"]
    bas, bit = m0["olcum_penceresi_s"]
    beklenen = olcum[0]["konfig"]["kosu_bitis_s"] / (bit - bas)
    for d in olcum:
        c = carpiklik(d["metrikler"], "kontrol_bayt")
        assert c == pytest.approx(beklenen, abs=1e-3), (
            f"🔴 `olu` kolunun çarpıklığı {c} — düzgün beacon beklentisi "
            f"{beklenen}. Ölçülen şey çarpıklık DEĞİL (Y7)")


# ==========================================================================
# li_calisma_noktasi.py — `08` Ç4
# ==========================================================================

def test_b130_li_hedefleri_OLCUME_uydurulmamis():
    """🔴 L2 — literatürün hedefi ölçüme uydurulursa fark sıfırlanır.

    Li vd.'nin sayıları **kaynaktan** gelir ve bizim ölçümümüz değildir;
    bir gün ölçüme yaklaştırılırlarsa replikasyon iddiası boşalır.
    """
    from dogrulama.li_calisma_noktasi import (LI_PLATO_TERS,
                                              LI_TEK_ATLAMA_MBPS,
                                              LI_UZUN_ZINCIR_MBPS)

    assert LI_TEK_ATLAMA_MBPS == 1.7
    assert LI_UZUN_ZINCIR_MBPS == 0.25
    assert LI_PLATO_TERS == 7.0


def test_b130_li_fark_yuzdesi_DOGRU_paydadan():
    """🔴 L1 — fark yüzdesi `(ölçülen − li) / li` olmalı, tersi değil."""
    from dogrulama.li_calisma_noktasi import _satir

    s = _satir("deneme", 1.1, 1.0)          # ölçülen 1,1 · hedef 1,0
    assert "+10.0 %" in s, (
        f"fark yüzdesi yanlış paydadan hesaplanıyor olabilir (L1): {s!r}")

# ==========================================================================
# 🔴 B-145 · B-146 · B-166 · B-148 — CANLI URETICININ SOZLESMESI
# ==========================================================================
# Sekizinci denetim olctu: B-124 ve B-125'in duzeltmeleri
# `isaret_testi.satir()`e yazilmisti ve o fonksiyonun deposunda SIFIR
# cagirani vardi. `06` 9.1 ve 8.1b'yi FIILEN basan `_yaz_kosul1/2`
# dokunulmamisti.
#
# 🔒 Asagidaki dort test URETICININ CIKTISINI denetler, kodunu degil —
# `03` B5: "bildirim != kullanim". Girdi SENTETIKtir, yani depo verisine
# ve `sim/`e hic bagli degil: bu testler B1 boyunca da konusur.
# ==========================================================================

def _sonuc(**k):
    """`isaret_testi`nin dondurdugu sozlugun asgari hali."""
    d = {"n_ham": 30, "n": 30, "berabere": 0, "pozitif": 20,
         "ortalama_fark": 1.0, "medyan_fark": 1.0, "medyan_fark_net": 1.0,
         "std_fark": 1.0, "p": 0.5, "ga": (0.5, 1.5), "ga_std_kati": None,
         "gecti": True, "buyukluk_ayagi": None, "eps_rel": 50.0,
         "pay_tanimsiz": 0,
         "kol": "K", "senaryo": "S0", "metrik": "m", "tohum_std": 1.0,
         "reddedilen": 0, "kesisim_ort": 0.5, "kesisim_min": 0.4,
         "kesisim_max": 0.6}
    d.update(k)
    return d


def test_b145_kosul1_ETIKETI_GECTI_DEMIYOR(capsys):
    """🔴 B-145 — `gecti` yalnizca AYAK 1'dir; etiket bunu SOYLEMEK ZORUNDA.

    Olculdu (sekizinci denetim): `_yaz_kosul1` 18 satirin 15'ine `GECTI`
    basiyordu ve sutun basligi `yargi` idi — `06` 9.2(a)'nin
    *"kosul 1 bugun HICBIR KOL icin saglandi sayilamaz"* cumlesinin tam
    tersi. `k` (ayak 2 esigi) B4'e kadar BOS oldugu icin hicbir satir
    *"gecti"* diye okunamaz.
    """
    from dogrulama.gecerlilik import _yaz_kosul1

    _yaz_kosul1([_sonuc(gecti=True), _sonuc(gecti=False, metrik="m2")])
    cikti = capsys.readouterr().out

    assert "GECTI" not in cikti, (
        "🔴 uretici hala `GECTI` basiyor — olcut EKSIKken 'gecti' demek "
        "`06` 9.2(a) ile celisir (B-145)")
    assert "GECMEDI" not in cikti
    assert "YON-OK" in cikti and "YON-RED" in cikti, (
        "🔴 etiket ayak 1'i (yon) adlandirmiyor (B-145)")
    assert "yargi" not in cikti, (
        "🔴 sutun basligi hala `yargi` — olcutun tamamini ima ediyor")


def test_b146_AYRISAN_estimand_IKISI_DE_basiliyor(capsys):
    """🔴 B-146 — HAM medyan, NET medyanin GA'sinin yaninda basilamaz.

    Kirici vaka (B-124'un kendi ornegi): 20 tohum berabere, 10 tohum +4/+5
    -> HAM medyan 0,00 · GA [+4,00 · +5,00]. Medyan KENDI GA'SININ DISINDA.
    Olculdu: kosul 1'in 18 satirinin 7'si ayrisiyor, 2'sinde ISARET TERS.
    """
    from dogrulama.gecerlilik import _yaz_kosul1, _yaz_kosul2

    ayrisan = _sonuc(berabere=20, n=10, pozitif=10, medyan_fark=0.0,
                     medyan_fark_net=4.5, ga=(4.0, 5.0))
    _yaz_kosul1([ayrisan])
    c1 = capsys.readouterr().out
    assert "+4.50000" in c1, (
        "🔴 GA'nin estimandi (NET medyan) BASILMIYOR — okuyucu GA'yi "
        "yanlis medyanla eslestirir (B-146)")
    assert "0.00000" in c1, "HAM medyan da basilmali (ikisi birden)"

    _yaz_kosul2([ayrisan])
    c2 = capsys.readouterr().out
    assert "+4.50" in c2, (
        "🔴 kosul 2 ayni sozlesmeye bagli DEGIL — kural bir nesneye "
        "uygulanip komsusuna uygulanmamis (B-146)")


def test_b166_kosul2_REDDEDILEN_sayisini_basiyor(capsys):
    """🔴 B-166 — `03` B2: "kac gozlemle hesaplandigini da yaz".

    `kosul2` `reddedilen`i HESAPLIYORDU ama `_yaz_kosul2` onu basmiyordu;
    komsusu `_yaz_kosul3` `dejenere` sutununu basiyor. Sonucu: `06` 8.1b
    DV icin `14/26` yaziyor ve 26'nin neden 30 olmadigi hicbir yerde yok.
    """
    from dogrulama.gecerlilik import _yaz_kosul2

    _yaz_kosul2([_sonuc(reddedilen=7, n=21)])
    cikti = capsys.readouterr().out
    assert "n_red" in cikti, "🔴 `reddedilen` sutunu YOK (B-166)"
    assert "7" in cikti, "🔴 reddedilen sayisi basilmiyor (B-166)"


def test_b148_kosul2_AYAK2_yoklugunu_YAZIYOR(capsys):
    """🔴 B-148 — kosul 2'de ayak 2 YAPISAL OLARAK BOS ve bu yazilmali.

    `kosul1` `isaret_testi(..., tohum_std=std)` cagiriyor (18/18 dolu),
    `kosul2` `isaret_testi([...])` cagiriyor (0/12). K3'un ayak 2'si
    kosul 2'ye UYGULANAMIYOR; `03` B5'in "bildirim != kullanim" tuzagi.
    """
    from dogrulama.gecerlilik import _yaz_kosul2

    _yaz_kosul2([_sonuc(ga_std_kati=None)])
    assert "AYAK 2 YOK" in capsys.readouterr().out, (
        "🔴 kosul 2 ayak 2'nin bos oldugunu YAZMIYOR (B-148)")

    # Y11 — koruma kendi siniriyla: dolu oldugunda uyari BASILMAMALI
    _yaz_kosul2([_sonuc(ga_std_kati=(0.1, 0.2))])
    assert "AYAK 2 YOK" not in capsys.readouterr().out, (
        "uyari kosulsuz basiliyor — bir sey olcmuyor (Y7)")


def test_b145_OZET_ayak2_uyarisini_KOSULSUZ_yaziyor(capsys):
    """🔴 B-145 — ozet, DUSEN CIFT OLMASA DA ayak 2'nin bos oldugunu yazar.

    Onceki hali hicbir cift dusmediginde *"hepsi gecti"* basiyordu; bu,
    `06` 9.2(a)'nin (*"kosul 1 bugun HICBIR KOL icin saglandi
    sayilamaz"*) tam tersidir. Bugunku veride 18 satirin 15'i ayak 1'i
    geciyor, yani bu satir en cok goze carpan yerde yanlisti.

    ⚠️ Bu yuklem `_yaz_kosul1_ozeti`yi AYRI cagirir; ilk yazimda
    `_yaz_kosul1`in ciktisina bakiyordu ve BASLIK da ayni kelimeyi
    tasidigi icin ozet silinse bile geciyordu (Y7: bos kume de 0 kirik
    verir — kendi korumamda).
    """
    from dogrulama.gecerlilik import _yaz_kosul1_ozeti

    # (a) hicbir cift dusmemisken bile uyari basilmali
    _yaz_kosul1_ozeti(set())
    bos = capsys.readouterr().out
    assert "SAGLANDI" in bos.upper() and "sayilamaz" in bos, (
        "🔴 dusen cift yokken ozet ayak 2 uyarisini YAZMIYOR — okuyucu "
        "'hepsi gecti' anlar (B-145)")
    assert "hepsi gecti" not in bos.lower()

    # (b) dusen cift varken de hem cift hem uyari basilmali (Y11 — sinir)
    _yaz_kosul1_ozeti({("DV", "gecikme ort")})
    dolu = capsys.readouterr().out
    assert "DV" in dolu and "gecikme ort" in dolu
    assert "sayilamaz" in dolu, "uyari yalnizca bos kumede basiliyor"


def test_b158_eps_rel_URETILIYOR_ve_dogru_paydadan():
    """🔴 B-158 — `06` Bolum 7'nin durdurma kuralinin URETICISI.

    Sekizinci denetim olctu: `06` 9.2(b) bir eps_rel BANDI yaziyordu
    (%77,9 - %4 397) ama deponun hicbir yerinde onu ureten kod yoktu
    (AST/grep: sifir) — sayi ELLE hesaplanmisti, `03` kural 1'in ihlali
    ve muhre giden bir sayfada.

    🔒 Payda GA'NIN ESTIMANDIDIR, HAM medyan degil (B-146 ile ayni
    sozlesme): beraberlik varken HAM medyan TAM SIFIR olabilir ve oran
    tanimsizlasir. Bugunku veride 18 ciftin 2'sinde HAM medyan tam sifir.
    """
    from dogrulama.isaret_testi import ga_estimandi, isaret_testi

    # (a) berabersiz vaka — payda HAM = NET
    r = isaret_testi([1.0] * 12 + [-1.0] * 3)
    assert r["eps_rel"] is not None
    yari = (r["ga"][1] - r["ga"][0]) / 2.0
    assert r["eps_rel"] == pytest.approx(
        100.0 * yari / abs(ga_estimandi(r)))

    # (b) 🔴 KIRICI VAKA — HAM medyan TAM SIFIR, NET degil.
    # HAM ile bolunse ZeroDivisionError ya da sonsuz cikardi.
    r0 = isaret_testi([0.0] * 20 + [4.0] * 5 + [5.0] * 5)
    assert r0["medyan_fark"] == 0.0, "kurici vaka kurulamadi (Y8)"
    assert r0["medyan_fark_net"] == 4.5
    assert r0["eps_rel"] is not None, (
        "🔴 HAM medyan sifirken eps_rel uretilemiyor — payda yanlis "
        "estimanddan aliniyor (B-158 · B-146)")
    yari0 = (r0["ga"][1] - r0["ga"][0]) / 2.0
    assert r0["eps_rel"] == pytest.approx(100.0 * yari0 / 4.5)

    # (c) Y11 — korumanin SINIRI: estimand da sifirsa oran TANIMSIZ
    rt = isaret_testi([0.0] * 5 + [1.0, -1.0])
    if rt["ga"] is not None and not rt["medyan_fark_net"]:
        assert rt["eps_rel"] is None, (
            "estimand sifirken eps_rel bir SAYI uretmemeli — "
            "`03` B2: 'nan = olcum yok'")


def test_b158_kosul1_tablosu_eps_rel_BASIYOR(capsys):
    """🔴 B-158 — durdurma kurali kosul 1'e HIC UYGULANMAMISTI."""
    from dogrulama.gecerlilik import _yaz_kosul1

    _yaz_kosul1([_sonuc(eps_rel=123.4)])
    c = capsys.readouterr().out
    assert "eps_rel" in c, "🔴 eps_rel sutunu YOK (B-158)"
    assert "%123" in c, "🔴 eps_rel degeri basilmiyor"

    _yaz_kosul1([_sonuc(eps_rel=None)])
    assert "TANIMSIZ" in capsys.readouterr().out, (
        "🔴 uretilemeyen eps_rel sessizce bos basiliyor — "
        "'olcum yok' ile 'etki yok' karisir (`03` B2)")


# ==========================================================================
# 🔴 B-152 · B-153 · B-154 · B-155 · B-165 (SEKİZİNCİ DENETİM)
# ==========================================================================

def _pay(kb, vb, ka=None, va=None):
    """Kontrol payı alanlarını taşıyan asgari sonuç sözlüğü."""
    return {"kontrol_bayt_pencere": kb, "veri_bayt_pencere": vb,
            "kontrol_airtime_s_pencere": kb / 1000 if ka is None else ka,
            "veri_airtime_s_pencere": vb / 1000 if va is None else va}


def test_b155_eslesmis_oran_SIFIR_paydayi_TIPLI_reddediyor():
    """🔴 B-155 — `bayt == 0` ZeroDivisionError fırlatıyordu.

    `kontrol_payi_yuzde` `vb == 0`ı `None`a çeviriyor, ama **`kb == 0`**
    *(kol pencerede hiç kontrol baytı üretmemiş)* geçerli bir dönüş olan
    `bayt = 0.0` veriyor ve `max/min` bölmesi patlıyordu — ölçüldü ve
    tetiklendi. Komşusu `kontrol_payi.eslestirilmis_oranlar` aynı vakayı
    `b == 0` ile **açıkça** eliyor: D-11'in dersi iki araçtan birine
    uygulanmış, komşusuna uygulanmamıştı.

    🔴 Y8 — bozulan yolun sağlam koşuda ÇALIŞTIĞI önce gösterilir.
    """
    from sim.karsilastirma import kontrol_payi_yuzde

    import dogrulama.gecerlilik as G

    # (a) Y8: kb = 0 GEÇERLİ bir dönüş üretiyor — yani yol tetikleniyor
    assert kontrol_payi_yuzde(_pay(0, 1000)) == {"bayt": 0.0, "airtime": 0.0}

    eski_s, eski_t = G.SENARYOLAR, G.TOHUMLAR
    G.SENARYOLAR, G.TOHUMLAR = ("S0",), range(1, 2)
    try:
        saglam = {("DV", "S0", "tam", 1): _pay(500, 1000),
                  ("gurultuden_kacan", "S0", "tam", 1): _pay(100, 1000)}
        r = G.eslesmis_kol_orani(saglam)
        assert r and r["n"] == 1, "sağlam kurulumda oran üretilmiyor (Y7)"

        bozuk = dict(saglam)
        bozuk[("gurultuden_kacan", "S0", "tam", 1)] = _pay(0, 1000)
        r2 = G.eslesmis_kol_orani(bozuk)          # 🔴 önce ZeroDivisionError
        assert r2 == {}, (
            "🔴 dejenere payda bir SAYI üretti — D-11: 'sessiz bir sayı "
            "yerine tipli bir ret' (B-155)")
    finally:
        G.SENARYOLAR, G.TOHUMLAR = eski_s, eski_t


def test_b153_eslesmis_oran_IKI_YUKLEMI_de_basiyor(capsys):
    """🔴 B-153 — `08` md 25'in oranı İKİ FARKLI yüklemle hesaplanıyordu.

        `kontrol_payi.eslestirilmis_oranlar` -> a / b    (YÖNLÜ, <1 olabilir)
        `gecerlilik.eslesmis_kol_orani`      -> max/min  (YÖNSÜZ, ≥1)

    Bugün 58/58 hücrede aynı çıkıyorlar **çünkü DV her hücrede gözlemden
    büyük** — tesadüfen. Mutasyonum `X9` ikisini ayrıştırdı ve 473 testin
    hiçbiri kırılmadı. Faz 1'de sessiz senaryodaki reaktif AODV gözlem
    kolundan **az** kontrol baytı üretebilir; o an iki okuma ayrışır.
    """
    import dogrulama.gecerlilik as G

    eski_s, eski_t = G.SENARYOLAR, G.TOHUMLAR
    G.SENARYOLAR, G.TOHUMLAR = ("S0",), range(1, 3)
    try:
        # 🔴 KIRICI VAKA: bir hücrede DV KÜÇÜK (yön ters)
        veri = {("DV", "S0", "tam", 1): _pay(500, 1000),
                ("gurultuden_kacan", "S0", "tam", 1): _pay(100, 1000),
                ("DV", "S0", "tam", 2): _pay(50, 1000),
                ("gurultuden_kacan", "S0", "tam", 2): _pay(400, 1000)}
        r = G.eslesmis_kol_orani(veri)
        assert r["n"] == 2
        assert r["ters_yon"] == 1, (
            "🔴 yön değişimi SAYILMIYOR — iki yüklem ayrıştığında hiçbir "
            "şey konuşmaz (B-153)")
        assert min(r["yonlu_min"], r["yonlu_max"]) < 1.0 <= r["min"], (
            "🔴 YÖNLÜ ve YÖNSÜZ okuma aynı sayıyı veriyor — yüklemlerden "
            "biri kaybolmuş olabilir (B-153)")

        G._yaz_kosul3([], r)
        cikti = capsys.readouterr().out
        assert "YONLU" in cikti and "YONSUZ" in cikti, (
            "🔴 iki yüklem YAN YANA basılmıyor (B-153)")
        assert "YON DEGISTI" in cikti, (
            "🔴 yön değiştiğinde okuyucu uyarılmıyor (B-153)")
    finally:
        G.SENARYOLAR, G.TOHUMLAR = eski_s, eski_t


def test_b154_kalibrasyon_UC_EKSENI_de_ornekliyor():
    """🔴 B-154 — F-11'in kalibrasyonu kendi maliyet eksenini kaçırıyordu.

    Ölçüldü: üç örneğin **3'ü de S0**, **2'si kısa** → ortalama
    `kosu_bitis_s` **250 s**, iş listesinde **275 s** *(−%9,1)*. Tahmin
    sistematik olarak **iyimser**di ve `03` kural 7'nin *"30 dk'yı aşarsa
    SOR"* kapısı tam olarak bu tahmine bağlı — F-9'un teşhisinin birebir
    aynısı, F-11'in düzeltmesinin **içinde**.
    """
    import statistics as ist

    from dogrulama.gecerlilik import (KOLLAR, SENARYOLAR, UZUNLUKLAR,
                                      _isler, _kalibrasyon_ornekleri)

    isler = _isler()
    ornekler = _kalibrasyon_ornekleri(isler)
    assert len(ornekler) == len(KOLLAR) * len(SENARYOLAR) * len(UZUNLUKLAR), (
        "🔴 kalibrasyon üç ekseni birden örneklemiyor (B-154)")
    for eksen in ("senaryo_etiket", "uzunluk"):
        i_kume = {x[0][eksen] for x in isler}
        o_kume = {x[0][eksen] for x in ornekler}
        assert o_kume == i_kume, (
            f"🔴 `{eksen}` ekseni kalibrasyonda eksik: {sorted(o_kume)} "
            f"↔ iş listesi {sorted(i_kume)} (B-154)")
    i_ort = ist.mean(x[1]["kosu_bitis_s"] for x in isler)
    o_ort = ist.mean(x[1]["kosu_bitis_s"] for x in ornekler)
    assert o_ort == pytest.approx(i_ort), (
        f"🔴 kalibrasyonun ortalama koşu uzunluğu {o_ort:.1f} s, iş "
        f"listesininki {i_ort:.1f} s — tahmin sistematik olarak "
        f"{'iyimser' if o_ort < i_ort else 'kötümser'} (B-154)")


def test_b165_dogrulama_araclari_MUTLAK_yol_kullaniyor():
    """🔴 B-165 — iki araç `sys.path.insert(0, ".")` kullanıyordu.

    `03` B5: *"Göreli sonuç yolu — yolları **depo köküne** mutlakla."*
    Ve `gecerlilik.py` artık o ikisinden birini **içe aktarıyor**, yani
    bir üretim aracı içe aktarıldığı her yerde `sys.path`e `"."`
    enjekte ediyordu.

    🔒 AST ile denetlenir — dizgi araması `KOSUCU_BETIGI` gibi bir
    **metin sabitinin içindeki** satırı da bulur ve yanlış alarm verir
    *(bu denetimde bir kez oldu)*.
    """
    goreli = []
    for yol in sorted((KOK / "dogrulama").glob("*.py")):
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if (isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute)
                    and n.func.attr == "insert"
                    and isinstance(n.func.value, ast.Attribute)
                    and n.func.value.attr == "path"
                    and len(n.args) > 1
                    and isinstance(n.args[1], ast.Constant)
                    and n.args[1].value == "."):
                goreli.append(f"{yol.name}:{n.lineno}")
    assert not goreli, (
        f"🔴 göreli `sys.path.insert(0, '.')`: {goreli}. Çağıranın "
        f"çalışma dizinine bağlı — `03` B5 (B-165).")


def test_b152_kosul2_kontrol_payi_TANIMSIZLIGINI_sayiyor(capsys):
    """🔴 B-152 — `08` md 35'in güvencesi ÜRETİM YOLUNDA yoktu.

    Madde *"okuyan, `ozet()`in TANIMSIZ etiketini görmek **zorundadır**"*
    diyor. Ama `ortak_alt_kume`ın tek üretim çağıranı `kosul2`dir ve o
    `kontrol_payi_a/b`yi hiç okumuyor, `ozet()`i hiç çağırmıyordu —
    `ozet()`i zorlayan tek şey bir **testti**. *"Zorunda"* bir dilekti,
    mekanizma değil.
    """
    from dogrulama.gecerlilik import _yaz_kosul2

    _yaz_kosul2([_sonuc(pay_tanimsiz=8, metrik="HAM ortalama"),
                 _sonuc(pay_tanimsiz=8, metrik="HAM p95"),
                 _sonuc(pay_tanimsiz=8, metrik="ORTAK ortalama"),
                 _sonuc(pay_tanimsiz=8, metrik="ORTAK p95")])
    c = capsys.readouterr().out
    assert "TANIMSIZ" in c, (
        "🔴 kontrol payı bilinmeyen hücreler SESSİZCE geçiyor (B-152)")
    # 4 satırın 4'ü de aynı kolun `pay_tanimsiz`ını taşır (kosul2 kol
    # başına 4 okuma basar), o yüzden üretici 4'e böler: 32 // 4 = 8.
    assert "8 hucre" in c, f"🔴 sayı yanlış ölçekleniyor: {c[-300:]}"

    # Y11 — sınır: hiç tanımsız yokken de OKUYANA söylenir
    _yaz_kosul2([_sonuc(pay_tanimsiz=0)])
    assert "TANIMSIZ hucre: 0" in capsys.readouterr().out, (
        "sıfır durumu yazılmıyor — okuyucu ölçüldüğünü bilemez (Y7)")
