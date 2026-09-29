"""
AİLE 0 ÇIKIŞ RAPORU — tek tablo.

Her çıkış kriteri: ölçülen değer · eşik · geçti/geçmedi.

🔴 AİLE 0, BU TABLODA TEK BİR "GEÇMEDİ" KALMADIĞINDA KAPANIR.

Kullanım:
    python dogrulama/aile0_kapi_raporu.py            # mutasyon paketi dahil
    python dogrulama/aile0_kapi_raporu.py --hizli    # mutasyon paketi hariç
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

# 🔴 ALT SÜREÇ ÇIKTISI UTF-8 OLARAK ÇÖZÜLÜR (20 Ağu 2026).
# `subprocess.run(..., text=True)` kodlama verilmezse çıktıyı YEREL KOD
# SAYFASIYLA çözer. Bu makinede o cp1254 ve çocuk süreç UTF-8 basıyor
# (PYTHONIOENCODING ayarlı). Türkçe "Ş" (U+015E → C5 9E) gibi karakterler
# cp1254'te TANIMSIZ olduğu için ebeveyn `UnicodeDecodeError` fırlatır ve
# araç, işini bitirmişken çöker. Ölçüldü: bir doğrulama koşusu tam olarak
# böyle düştü. `errors="replace"` ile ayrıştırma asla çökmez.

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))


# ==========================================================================
# 🔴 B-111 (ALTINCI DENETİM) — Ç6.1 VE Ç6.3 İKİ YÖNDE DE KANDIRILABİLİYORDU
#
# Eski hâlleri TÜM DOSYA ÜZERİNDE DİZGİ ARAMASIYDI — yorum ve docstring
# dâhil. Denetçi dört denemeyi de ölçtü (her biri geçici bir kopyada):
#
#   (a1) onay YÖNÜ ters çevrildi + aynı dizgi YORUMA kondu -> Ç6.1 GEÇTİ 🔴
#   (a2) kimlik -> DEĞER karşılaştırması + dizgi YORUMDA   -> Ç6.3 GEÇTİ 🔴
#   (b1) `if x is il` -> `if il is x` (davranış BİREBİR aynı) -> Ç6.3 DÜŞTÜ 🔴
#   (b2) yorumda `.remove(il)` geçiyor (kod değişmedi)        -> Ç6.3 DÜŞTÜ 🔴
#
# Yani hem YANLIŞ POZİTİF hem YANLIŞ NEGATİF ölçüldü.
#
# ⚖️ Bu, B-09'un Ç6.2'de kapattığı hata sınıfının BİREBİR AYNISIDIR ve
# Ç6.1/Ç6.3'te açık bırakılmıştı. Çözüm de aynı oturumda yazılmıştı —
# B-89'un PROZA/kod ayırt etme deseni (`ast`) — ama yalnızca gözlem
# işaretleyicisine uygulanmış, kapıya uygulanmamıştı.
#
# 🔴 YÜKLEMLER KAYNAK METNİ ALIR, DOSYA OKUMAZ. Sebebi Y11: kapsam dışı bir
# vaka ancak SENTETİK bir kaynakla üretilebilir ve 150 dakikalık kapıyı
# koşturmadan sınanabilir. Zorlayan test:
#     tests/test_kapi_secimleri.py::test_b111_*
# ==========================================================================

def _fonksiyon(agac: "ast.Module", ad: str):
    for d in ast.walk(agac):
        if isinstance(d, ast.FunctionDef) and d.name == ad:
            return d
    return None


def _konumsal_parametreler(fn) -> list[str]:
    """`self` hariç konumsal parametre adları — SIRAYLA."""
    return [a.arg for a in fn.args.args if a.arg != "self"]


def c61_onay_yonu_dogru(kaynak_mac: str) -> bool:
    """Ç6.1 — onay GERÇEK bir iletimdir ve YÖNÜ doğrudur.

    Değişmez: `_onay_ilet(alici, veri_gonderen)` içinde kurulan `Iletim`in
    **gönderen**i fonksiyonun BİRİNCİ parametresi, **alan**ı İKİNCİsidir.
    Onayı veri alıcısı gönderir; ters çevrilirse onay yanlış düğümden çıkar.

    🔴 Parametre ADINA değil, SIRASINA bağlıdır: ikisi birden yeniden
    adlandırılırsa davranış aynıdır ve ölçüt de aynı kalır (yanlış negatif
    yok). Argümanlar takas edilirse ölçüt DÜŞER (yanlış pozitif yok).
    """
    fn = _fonksiyon(ast.parse(kaynak_mac), "_onay_ilet")
    if fn is None:
        return False
    p = _konumsal_parametreler(fn)
    if len(p) < 2:
        return False
    for d in ast.walk(fn):
        if (isinstance(d, ast.Call) and isinstance(d.func, ast.Name)
                and d.func.id == "Iletim" and len(d.args) >= 2):
            return (isinstance(d.args[0], ast.Name) and d.args[0].id == p[0]
                    and isinstance(d.args[1], ast.Name)
                    and d.args[1].id == p[1])
    return False


def c63_iletim_kimlikle_karsilastiriliyor(kaynak_mac: str) -> bool:
    """Ç6.3 — aktif iletim listesinden çıkarma KİMLİKLE yapılır.

    `Iletim` bir `dataclass`tır: `__eq__` DEĞER karşılaştırır ve aynı alanlara
    sahip iki çerçeve birbiriyle karıştırılabilir. `_iletim_bitir` içinde:

      · `is` / `is not` ile bir karşılaştırma OLMALI *(operand sırası serbest)*
      · `==` / `!=` ile ÇIPLAK bir karşılaştırma OLMAMALI
        *(`il.gonderen == dugum` gibi ÖZNİTELİK karşılaştırmaları meşrudur)*
      · `.remove(il)` çağrısı OLMAMALI — `list.remove` `==` kullanır
    """
    fn = _fonksiyon(ast.parse(kaynak_mac), "_iletim_bitir")
    if fn is None:
        return False
    p = _konumsal_parametreler(fn)
    if not p:
        return False
    il = p[0]

    def ciplak(x) -> bool:
        return isinstance(x, ast.Name) and x.id == il

    kimlik = False
    for d in ast.walk(fn):
        if isinstance(d, ast.Compare):
            operandlar = [d.left, *d.comparators]
            if any(ciplak(x) for x in operandlar):
                for op in d.ops:
                    if isinstance(op, (ast.Is, ast.IsNot)):
                        kimlik = True
                    if isinstance(op, (ast.Eq, ast.NotEq)):
                        return False           # DEĞER karşılaştırması
        if (isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute)
                and d.func.attr == "remove"
                and any(ciplak(a) for a in d.args)):
            return False                       # list.remove `==` kullanır
    return kimlik


@dataclass
class Kriter:
    kod: str
    ad: str
    olculen: str
    esik: str
    gecti: bool


# ==========================================================================
# 🔴 KAPI SEÇİMLERİ — BEKLENEN TEST SAYILARININ TEK KAYNAĞI
# ==========================================================================
# kod -> (ad, dosya yolları, `-k` seçimi, BEKLENEN TEST SAYISI)
#
# K-033'ün kuralı: her kapı için beklenen test sayısı YAZILI olur. Yoksa bir
# seçim sessizce daralır ve kapı yine "0 kırık" der (Y7).
#
# 🔴 AMA BU SAYILAR ELLE TUTULUYOR VE İKİ KEZ SESSİZCE BAYATLADI:
#   · Ç5: 11 -> 14 — K-036'da B-01/B-02 regresyonları eklendi
#   · Ç5: 14 -> 18 — 20 Ağu 2026, B-27b'nin dört `test_b27b_*` içerik testi
# İkisinde de kapının KENDİ mekanizması sürüklenmeyi yakaladı; yakalayamadığı
# şey ZAMANDI. Kapı ~71 dk sürüyor, bu yüzden günlerce koşulmadı ve iki
# bağımsız denetim boyunca sayı bayat kaldı. İkincisini kapı 20 Ağustos 2026
# koşusunda `!!SEÇİM 18≠14` ile düşürdü.
#
# 🔴 ÇÖZÜM: `tests/test_kapi_secimleri.py` aynı kontrolü SANİYELER içinde
# yapar. Pahalı kapı, ucuz bir testle korunuyor — Y3 ("kapı çıktısı bir
# TEST'tir") ve K-042'nin dersi ("pahalı koşudan önce ucuz ön kontrol").
#
# Üretici komut (her satır için):
#   python -m pytest <yollar> [-k <seçim>] --collect-only -q
# 🔴 B-41 (K-047) — Ç1.3'ÜN EŞİĞİ ARTIK VERİDEN TÜREMİYOR.
# K-044 bu sabiti ekledi**ğini yazdı**; sabit koda hiç girmedi ve eşik iki
# oturum boyunca `{toplam}/{toplam}` kaldı. Üçüncü bağımsız denetim ölçtü:
# mutasyon listesi 35 -> 5'e düşmüş gibi davrandığında kapı "Ç1.3 · 5/5 · OK"
# ve "13/13" yazıyordu — Ç1.1'de düzeltilen tuzağın birebir ikizi.
#
# Üretici: python -c "from dogrulama.mutasyon_paketi import MUTASYONLAR; print(len(MUTASYONLAR))"
# 35 -> 41: B-131 (yedinci denetim) — `sim/karsilastirma.py`nin
# KANITLANMIS alti boslugu pakete girdi. Modul 1 -> 7 mutasyon.
BEKLENEN_MUTASYON = 41


class KapiSecimi(NamedTuple):
    """Bir kapı kriterinin NE ÖLÇTÜĞÜ — tek kaynak.

    🔴 `zorunlu` NEDEN VAR (B-42, K-047):
    Önceki sürüm yalnızca `adet` taşıyordu ve koruma *"yazılı sayı = bugün
    toplanan sayı"* diyordu. Üçüncü denetim bunu kırdı: Ç5'in seçimini
    `-k "not test_b27b"` yapıp adedi 18 -> 14 indirince **üç katman da
    sustu** — 284/284 test geçti, ucuz koruma geçti, kapının Ç5 kriteri
    GEÇTİ dedi; B-27b'nin dört içerik testi kapsamdan tamamen çıkmışken.

    Sayı ve kapsam **iki ayrı eksendir**; biri diğerini korumaz:
      · `adet`    -> testler sessizce EKLENDİ/KAYBOLDU mu
      · `zorunlu` -> seçim sessizce DARALDI mı
    """
    ad: str
    yollar: list[str]
    secim: str | None
    adet: int
    zorunlu: frozenset[str]


KAPI_SECIMLERI: dict[str, KapiSecimi] = {
    "Ç2": KapiSecimi(
        "belirlenimcilik (tam koşu · hashseed · iki kol)",
        ["tests/test_kapi_aile0.py"], "c2_", 6,
        # Üç belirlenimcilik ekseninin üçü de kapsamda OLMAK ZORUNDA.
        frozenset({"test_c2_1_", "test_c2_2_", "test_c2_3_"})),
    # 🔴 B-15: `adet=None` idi — K-033'ün KENDİ kuralı Ç3'te uygulanmamıştı.
    # 39 -> 44: Ç3.3 dört görev çevriminde parametrize edildi (+3, B-07) ve
    # iki B-14 regresyonu eklendi (+2).
    "Ç3": KapiSecimi(
        "analitik kontroller (kapı + radyo)",
        ["tests/test_kapi_aile0.py", "tests/test_radio.py"],
        # 44 -> 46: B-117/M07'nin PARÇALAMA testleri (2), K-074. Ölçüldü:
        # parçalama yok sayılınca 65 sayısal alanın 43-51'i kayıyor ve
        # `test_c3_2`/`test_c3_2b`nin İKİSİ DE susuyor (ikisi de TEK YÖNLÜ).
        "c3_ or test_radio or test_b117_m07_", 46,
        # Dört analitik kontrol + B-22/B-35'in kırılabilirlik regresyonu +
        # B-14'ün varsayılan-yok regresyonu.
        frozenset({"test_c3_1_", "test_c3_2_", "test_c3_3_", "test_c3_4_",
                   "test_ber_kapali_form", "test_b14_",
                   # 🔴 B-117/M07: kısmi çakışma VE darbe eksenleri.
                   # Kapsam dışına alınırsa `alim_per` parça sınırlarını
                   # yeniden yok sayabilir ve hiçbir test konuşmaz.
                   "test_b117_m07_"})),
    # 🔴 Ç5 TAM DOSYA kriteridir: `secim` None OLMAK ZORUNDA (aşağıdaki
    # TAM_DOSYA_KRITERLERI). U10 tam olarak burayı hedefledi.
    "Ç5": KapiSecimi(
        "gözlem sözleşmesi",
        # 18 -> 23: B-43'un isaretleyici korumasi (2) + listede olup testi
        # olmayan uc alanin gercek icerik testleri (3), K-048.
        # 23 -> 24: A-4'un dugum basina protokol izolasyonu testi, K-049.
        # 29 -> 39: B-66'nin BOYUT ekseni testleri (8 parametrik + 2), K-056.
        # 43 -> 47: B-82/B-83'un Y7 CANLILIK testleri (4), K-062. Y12'nin
        # ucuz korumasi bu bayatlamayi 15,7 sn'de yakaladi -- kapi 150 dk
        # kosmadan once. Kural tam olarak bunun icin yazilmisti (K-060).
        # 47 -> 48: B-86'nin DORT KANAL taramasi (1), K-065.
        # 48 -> 50: B-87'nin `teshis` sozlesmesi (2: sozlesme + entegrasyon),
        # K-065. Ikiye bolundu cunku tek testin 12 tam kosusu pakete 3 dk,
        # mutasyon kapisina ~105 dk ekliyordu (Y12).
        # 50 -> 51: B-99'un `KomsuKaydi` icerik testi (1), K-067.
        # 51 -> 52: B-89'un PROZA/kod ayirt etme testi (1), K-068.
        # 52 -> 55: B-101'in derinlik taramasi testleri (3), K-073.
        # Elle secilmis `_TARAMA_DERINLIGI = 3` kaldirildi; kapsam
        # disina alinirsa tarama yeniden derinlik >=4'te KOR kalir.
        ["tests/test_gozlem.py"], None, 55,
        frozenset({"test_c5_", "test_b01_", "test_b02_", "test_b27b_",
                   "test_saf_gozlem", "test_a4_", "test_b44_",
                   "test_b47_", "test_b66_", "test_b69_",
                   # 🔴 B-82/B-83: Y7 oz-denetiminin CANLI oldugunu gosteren
                   # testler. Kapsam disina alinirsa koruma yeniden `x >= x`e
                   # doner ve hicbir davranis testi bunu gormez.
                   "test_b82_", "test_b83_",
                   # 🔴 B-86: `08`in DORT kanalini goren tarama.
                   # Kapsam disina alinirsa tarama yeniden tek
                   # kanala doner ve beyan kagitta kalir.
                   "test_b86_",
                   # 🔴 B-87: `teshis` sozlesmesi. Kapsam disina
                   # alinirsa kanca yeniden denetimsiz kalir ve
                   # ihlal koşu BITTIKTEN SONRA patlar.
                   "test_b87_",
                   # 🔴 B-99: B-27b kurali UC kumeye birden.
                   # Kapsam disina alinirsa `KomsuKaydi` ve
                   # `PaketGorunumu` yeniden kural disi kalir.
                   "test_b99_",
                   # 🔴 B-89: isaretleyici PROZAYI koddan ayirt
                   # ediyor. Kapsam disina alinirsa alan adi
                   # yalnizca docstringde gecen bir test
                   # "isaretlenmis" sayilir.
                   "test_b89_",
                   # 🔴 B-101: paylasim taramasinin DERINLIK sinirini
                   # kaldiran testler. Kapsam disina alinirsa
                   # derinlik >=4'teki kahin kanali yine gorunmez.
                   "test_b101_"})),
    # 🔴 Ç1.5 — B-144 (SEKİZİNCİ DENETİM). ÜÇ ÜRETİCİNİN ÇAPASI
    # KAPININ HİÇBİR KRİTERİNDE YOKTU.
    # `tests/test_gecerlilik_araclari.py` — `06`nın üç geçerlilik koşulunu
    # ve `08`in iki maddesini üreten üç aracın TEK korumasıydı ve kapı onu
    # hiç koşmuyordu. Ölçüldü: `dogrulama/` altında dosyaya sıfır gönderme;
    # kriterlerin dokunduğu beş dosyanın hiçbiri bu değil.
    #
    # 🔴 VE BİR `skip` KAPIYI DÜŞÜRMÜYORDU: `_pytest()` yalnızca `passed` ve
    # `failed` ayrıştırıyor; `"468 passed, 5 skipped"` satırından
    # `gecen=468, kirilan=0` çıkar ve ölçüt (`k == 0 and g > 0`) GEÇER.
    # `adet` verildiği için artık `gecen + kirilan != adet` olur ve kapı
    # `!!SEÇİM` ile düşer — çapa susarsa kapı da susmaz.
    #
    # Üretici: python -m pytest tests/test_gecerlilik_araclari.py --collect-only -q
    # 9 -> 11: B-143'ün iki koruması (grup tekliği + kapı üyeliği).
    # 11 -> 18: B-145 · B-146 · B-166 · B-148'in üretici-çıktısı testleri
    # (4) + `_yaz_kosul1_ozeti`nin koşulsuz uyarısı (1) + B-158'in
    # `eps_rel` üreteci ve tablo satırı (2).
    # 18 -> 23: B-152 · B-153 · B-154 · B-155 · B-165 (5).
    "Ç1.5": KapiSecimi(
        "üç üreticinin çapa testi (gecerlilik · pencere_kapsami · li)",
        ["tests/test_gecerlilik_araclari.py"], None, 23,
        frozenset({"test_b130_kosul1_", "test_b130_kosul2_",
                   "test_b130_kosul3_", "test_b130_olu_",
                   "test_b130_pencere_", "test_b130_li_",
                   # 🔴 B-143: çapanın KENDİ korumaları. Kapsam dışına
                   # alınırsa çapa yeniden sessizce boşalabilir.
                   "test_b143_",
                   # 🔴 B-145/B-146/B-166/B-148: canlı üreticinin çıktı
                   # sözleşmesi. Kapsam dışına alınırsa `_yaz_kosul1/2`
                   # yeniden `GECTI` ve HAM medyan basabilir ve hiçbir
                   # test konuşmaz — sekizinci denetimin ölçtüğü hâl.
                   "test_b145_", "test_b146_", "test_b166_",
                   "test_b148_",
                   # 🔴 B-158: `06` Bölüm 7'nin durdurma kuralının ÜRETECİ.
                   # Kapsam dışına alınırsa `eps_rel` yeniden elle
                   # hesaplanan bir sayı olur (`03` kural 1).
                   "test_b158_",
                   # 🔴 B-152 · B-153 · B-154 · B-155 · B-165: üreticinin
                   # dejenere/asimetri/kalibrasyon sözleşmeleri. Kapsam
                   # dışına alınırsa `eslesmis_kol_orani` yeniden
                   # ZeroDivisionError fırlatır, kalibrasyon yeniden tek
                   # eksene döner ve hiçbir test konuşmaz.
                   "test_b152_", "test_b153_", "test_b154_",
                   "test_b155_", "test_b165_"})),
    "Ç4.1": KapiSecimi(
        "Li regresyon testi",
        ["tests/test_li_regresyon.py"], None, 6,
        frozenset({"test_tek_atlama_verimi_analitige_esit",
                   "test_ideal_zincir_bolgesi_dorde_yakin",
                   "test_uzun_zincir_platosu"})),
    # 🔴 B-09: Ç6.2 artık dizgi eşleşmesi değil, gerçek değişmez testi.
    "Ç6.2": KapiSecimi(
        "kanal dilimi marj DEĞİŞMEZİ (gerçek hesap)",
        # 2 -> 4: B-117/M25'in DİLİM DEĞERİ testleri (2), K-074.
        # Ç6.2'nin marj değişmezi `Konfig.kanal_dilimi_s`ten ANALİTİK hesap
        # yapıyor ve `kanal_cekimi`in İÇİNDEKİ bölene bakmıyordu; bölen
        # 10 kat kabalaşınca 44-48 alan kayıyor ve değişmez SUSUYORDU.
        ["tests/test_rng.py"], "test_dilim_ or test_b117_m25_", 4,
        frozenset({"test_dilim_en_kucuk_cerceveyle_bile_guvenli",
                   "test_dilim_hala_protokol_zaman_farkini_yutuyor",
                   # 🔴 B-117/M25: kabalaşma VE incelme, iki yön ayrı.
                   "test_b117_m25_"})),
}

# 🔴 Bu kriterler kendi dosyalarının TAMAMINI ölçer; `-k` ile daraltılamaz.
# Dosyayı paylaşmayan bir kriterde `-k`, kapsamı sessizce daraltmanın en
# ucuz yoludur (B-42/U10).
# 🔴 Ç1.5 de TAM DOSYA kriteridir (B-144): `-k` ile daraltmak, çapayı
# yeniden sessizleştirmenin en ucuz yolu olurdu.
TAM_DOSYA_KRITERLERI = frozenset({"Ç5", "Ç4.1", "Ç1.5"})


class ToplamaHatasi(RuntimeError):
    """`--collect-only` sayılamadı — bu, 0 ile KARIŞTIRILMAMALIDIR."""


def toplanan_test_sayisi(yollar, secim=None) -> int:
    """Bir kapı seçiminin BUGÜN kaç test topladığı — kapıyı koşmadan.

    🔴 Y7 — ARAÇ NE SAYDIĞINI KENDİSİ DOĞRULAR.
    `--collect-only` en az üç ayrı sebeple "0" gibi görünebilir:
      · seçim gerçekten boş                (pytest çıkış kodu 5)
      · dosya yolu yanlış / toplama hatası (çıkış kodu 2 ya da 4)
      · çıktı biçimi beklenenden farklı
    Üçü de sessizce 0 dönseydi, bunu kullanan kontrol `0 == 0` ile GEÇERDİ —
    bu depoda yedi kez yapılan hata. Bu yüzden **yalnızca** pytest'in açıkça
    "hiç test yok" demesi 0 döndürür; ayrıştırılamayan her durum
    `ToplamaHatasi` fırlatır.
    """
    komut = [sys.executable, "-m", "pytest", *yollar, "--collect-only", "-q",
             "-p", "no:cacheprovider"]
    if secim:
        komut += ["-k", secim]
    p = subprocess.run(komut, cwd=KOK, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    # pytest çıkış kodları: 0 = test toplandı · 5 = hiç test toplanmadı
    if p.returncode == 5:
        return 0
    if p.returncode != 0:
        raise ToplamaHatasi(
            f"pytest toplama hatası (rc={p.returncode}) · {yollar} -k {secim!r}\n"
            f"{p.stdout[-1500:]}\n{p.stderr[-1500:]}")
    eslesme = re.search(r"(\d+)(?:/\d+)? tests? collected", p.stdout)
    if not eslesme:
        raise ToplamaHatasi(
            f"'N tests collected' satiri bulunamadi · {yollar} -k {secim!r}\n"
            f"{p.stdout[-1500:]}")
    return int(eslesme.group(1))


def toplanan_test_kimlikleri(yollar, secim=None) -> list[str]:
    """Bir kapı seçiminin BUGÜN topladığı test KİMLİKLERİ — kapıyı koşmadan.

    🔴 Y7 — `toplanan_test_sayisi`in ikizi, aynı gerekçeyle: ayrıştırılamayan
    her durum `ToplamaHatasi` fırlatır, sessizce boş liste dönmez. Boş liste
    **yalnızca** pytest açıkça "hiç test yok" dediğinde (rc=5) dönebilir.

    B-42 için var: sayı doğru kalırken KAPSAM daralabilir.
    """
    komut = [sys.executable, "-m", "pytest", *yollar, "--collect-only", "-q",
             "-p", "no:cacheprovider"]
    if secim:
        komut += ["-k", secim]
    p = subprocess.run(komut, cwd=KOK, capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    if p.returncode == 5:
        return []
    if p.returncode != 0:
        raise ToplamaHatasi(
            f"pytest toplama hatası (rc={p.returncode}) · {yollar} -k {secim!r}\n"
            f"{p.stdout[-1500:]}\n{p.stderr[-1500:]}")
    kimlikler = [x.strip() for x in p.stdout.splitlines() if "::" in x]
    if not kimlikler:
        raise ToplamaHatasi(
            f"rc=0 ama hiçbir '::' satırı yok · {yollar} -k {secim!r}\n"
            f"{p.stdout[-1500:]}")
    return kimlikler


def eksik_zorunlu(sec: "KapiSecimi") -> set[str]:
    """Kriterin kapsamından DÜŞMÜŞ zorunlu desenler.

    🔴 B-42 — SAYI DEĞİL, KAPSAM. `adet` kontrolü seçimle birlikte
    değiştirilirse susar; bu kontrol susmaz, çünkü ölçtüğü şey
    *"şu testler hâlâ bu kriterin içinde mi"*.
    """
    kimlikler = toplanan_test_kimlikleri(sec.yollar, sec.secim)
    metin = "\n".join(kimlikler)
    return {d for d in sec.zorunlu if d not in metin}


def kapsam_notu(sec: "KapiSecimi") -> str:
    """Kapı tablosuna giren not — kapsam daraldıysa kriter DÜŞER."""
    eksik = eksik_zorunlu(sec)
    return f" !!KAPSAM eksik={sorted(eksik)}" if eksik else ""


def _pytest(yollar: list[str], secim: str | None = None,
            beklenen_sayi: int | None = None) -> tuple[int, int, str]:
    """Belirtilen DOSYALARDA pytest koşar; (geçen, kırılan, not) döndürür.

    🔴 DOSYA YOLU ZORUNLU, `-k` isteğe bağlı.

    İlk yazımı yalnızca `-k` kullanıyordu ve BULANIKTI: `-k "li_"` seçimi
    10 dosyadan 60 test topluyordu, çünkü Türkçe test adlarındaki
    "bağlı_", "menzilli_" gibi parçalar eşleşiyor. Kapı "0 kırık" diyordu
    ama HANGİ KÜMEDE 0 kırık olduğu belirsizdi.

    `beklenen_sayi` verilirse, toplanan test sayısı doğrulanır. Bir seçim
    sessizce 0 test toplarsa kapı yanlışlıkla GEÇER — bu kontrol onu önler.
    """
    komut = [sys.executable, "-m", "pytest", *yollar, "-q", "--tb=no",
             "-p", "no:cacheprovider"]
    if secim:
        komut += ["-k", secim]
    p = subprocess.run(komut, cwd=KOK, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    son = [x for x in p.stdout.splitlines() if " passed" in x or " failed" in x]
    metin = son[-1] if son else ""
    gecen = int(metin.split(" passed")[0].split()[-1]) if "passed" in metin else 0
    kirilan = int(metin.split(" failed")[0].split()[-1]) if "failed" in metin else 0
    notu = ""
    if beklenen_sayi is not None and gecen + kirilan != beklenen_sayi:
        notu = f" !!SEÇİM {gecen+kirilan}≠{beklenen_sayi}"
    return gecen, kirilan, notu


def main() -> None:
    hizli = "--hizli" in sys.argv
    t0 = time.perf_counter()
    print("=" * 80)
    print("AİLE 0 ÇIKIŞ RAPORU")
    print("=" * 80)
    # ⚠️ SÜRE ÖLÇÜLDÜ, TAHMİN EDİLMEDİ (19 Ağustos 2026):
    #   Ç1 korunum matrisi (540 koşu)      ~ 6 dk
    #   Ç1.3 taban kontrolü + 22 mutasyon  ~18 dk   <- B-21 ile eklendi
    #   Ç2/Ç3/Ç5/Ç4 + kod denetimi         ~ 5 dk
    # 🔴 BEŞ TAM KOŞU ÖLÇÜLDÜ: **71,0** · **73,9** *(20 Ağu)* ·
    # **98,2** *(21 Ağu)* · **127,8** *(25 Ağu, DÜŞTÜ)* · **150,2 dk**
    # *(25 Ağu, 13/13). Artışların sebebi
    # ölçüldü değil tahmin edildi diye YAZILMAZ — bilinen ek yükler:
    # B-45'in seçim avantajı sayacı (karar başına ~6,4 ek PER hesabı, tek
    # koşuda %7,4), B-42'nin kapsam kontrolü (5 ek `--collect-only`), ve
    # test paketinin büyümesi (240 → 367).
    # Tahmin, ÖLÇÜLEN EN BÜYÜĞÜNÜ verir.
    #
    # ⚠️ TAHMİN BEŞ KEZ TUTMADI: "~98" → 127,8 dk (%30) · "~130" → 150,2 dk
    # (%15,5). Tahmin, ÖLÇÜLEN EN BÜYÜĞÜNÜN üstüne yazılır — ortalamasına
    # değil, ve asla "bu sefer daha hızlı olur" varsayımıyla değil.
    #
    # 🔴 25 Ağu'daki DÜŞEN koşu: mutant başına `timeout` 1200 sn'de kalmıştı
    # ve 35 mutantın 31'i zaman aşımına uğradı (K-058). Zaman aşımı 3600
    # sn'ye çıkarıldı ve AYNI GÜN kapı 13/13 geçti — Ç1.3: 4/35 → **35/35**.
    # Süre 127,8 → 150,2 dk çıktı: mutantlar artık 20 dk'da KESİLMİYOR,
    # bitiyor. Yani düzeltmenin bedeli ~22 dk ve BEKLENEN bir bedeldir.
    #
    # `--hizli` Ç1.3'ü atlar ama o zaman kapı GEÇMEZ — atlanan kriter
    # başarısız sayılır.
    print(f"Tahmini süre: ~{'25' if hizli else '150'} dk")
    print()

    K: list[Kriter] = []

    # ---------------------------------------------------------------- Ç1
    print("Ç1 — korunum matrisi koşuluyor (540 koşu)...")
    from dogrulama.kapi_korunum import ana_matris, uc_durum_matrisi
    ana = ana_matris()
    # 🔴 BEKLENEN KOŞU SAYISI SABİT YAZILIR — K-033'ün kuralı, Ç1.1'e de.
    # Önceki hâlinde eşik VERİDEN türetiliyordu (`len(ana)/len(ana)`) ve
    # ölçüt `tutan == len(ana)` idi: matris BOŞ dönseydi `0 == 0` olur ve
    # Ç1.1 "0/0" ile GEÇERDİ. "0 kırık" ile "0 koşu" ayırt edilemiyordu —
    # kapı raporunun kendi kurucu dersi (Y7), Ç1.1'de uygulanmamıştı.
    BEKLENEN_KOSU = 6 * 3 * 30            # senaryo × trafik × ayarlama tohumu
    tutan = sum(1 for r in ana if r["korunum_tamam"])
    sayi_notu = "" if len(ana) == BEKLENEN_KOSU else f" !!KOŞU {len(ana)}≠{BEKLENEN_KOSU}"
    K.append(Kriter("Ç1.1", "korunum, gerçek MAC yolundan",
                    f"{tutan}/{len(ana)}{sayi_notu}",
                    f"{BEKLENEN_KOSU}/{BEKLENEN_KOSU}",
                    tutan == len(ana) == BEKLENEN_KOSU))

    uc = uc_durum_matrisi()
    toplam: dict[str, int] = {}
    for r in ana:
        for s, v in r["dusen"].items():
            toplam[s] = toplam.get(s, 0) + v
    tetiklenen = {s for s, v in toplam.items() if v}
    for _ad, beklenen, sonuclar in uc:
        if sum(r["dusen"][beklenen] for r in sonuclar):
            tetiklenen.add(beklenen)
    K.append(Kriter("Ç1.2", "dört düşme sebebi de tetikleniyor",
                    f"{len(tetiklenen)}/4", "4/4", len(tetiklenen) == 4))

    oranlar = [r["boruda_kalan"] / r["uretilen"] for r in ana if r["uretilen"]]
    # Boş küme `max()` ile ValueError fırlatırdı — kapı çökerdi, geçmezdi;
    # yine de sessiz olmayan bir başarısızlık açıkça yazılır.
    K.append(Kriter("Ç1.4", "boşaltma: boruda kalan",
                    f"%{max(oranlar)*100:.3f}" if oranlar else "!!VERİ YOK",
                    "< %1", bool(oranlar) and max(oranlar) < 0.01))

    # ---------------------------------------------------------------- Ç1.3
    if hizli:
        K.append(Kriter("Ç1.3", "mutasyon paketi", "ATLANDI (--hizli)",
                        "7/7", False))
    else:
        # 🔴 B-21: kapı, mutasyon paketinin TEK giriş noktasını çağırır.
        # Önceki hâlde `_kosu`yu doğrudan çağırıp kendi ölçütünü uyguluyordu:
        # taban kontrolü ATLANIYORDU ve "en az bir test kırıldı" yetiyordu.
        # İki ayrı uygulama = kapının kendi aracını denetlememesi (K-033).
        from dogrulama.mutasyon_paketi import paketi_kostur
        print("Ç1.3 — taban kontrolü + mutasyon paketi koşuluyor...")
        mp = paketi_kostur()
        if not mp["taban_tamam"]:
            K.append(Kriter("Ç1.3", "mutasyon paketi (TABAN KIRIK)",
                            "!!TABAN", "taban temiz", False))
        else:
            notu = ""
            if mp["beklenen_kirilmadi"]:
                notu = f" !!YANLIŞ TEST x{len(mp['beklenen_kirilmadi'])}"
                # 🔴 HANGİSİ olduğunu YAZ. İlk sürüm yalnızca sayıyı
                # basıyordu ve teşhis için ayrı bir betik yazmak gerekti —
                # bir kapı, neyin düştüğünü söylemeden düşmemeli (Y7).
                print("  🔴 beklenen testi kırılmayan mutasyonlar:")
                for _ad, _bek in mp["beklenen_kirilmadi"]:
                    print(f"       {_ad}  ->  {_bek}")
            if mp.get("gecersiz"):
                print("  🔴 geçersiz mutasyon:")
                for _ad, _sebep in mp["gecersiz"]:
                    print(f"       {_ad}  ({_sebep})")
            # 🔴 B-41: EŞİK SABİTTEN GELİR, veriden değil. Liste kazayla
            # küçülürse (bir düzenleme, bir `replace` kayması) kapı artık
            # "N/N · OK" diyemez.
            if mp["toplam"] != BEKLENEN_MUTASYON:
                notu += f" !!LİSTE {mp['toplam']}≠{BEKLENEN_MUTASYON}"
            K.append(Kriter(
                "Ç1.3", "mutasyon paketi (her mutasyon KENDİ testiyle)",
                f"{mp['yakalanan']}/{mp['toplam']}{notu}",
                f"{BEKLENEN_MUTASYON}/{BEKLENEN_MUTASYON}",
                mp["gecti"] and mp["toplam"] == BEKLENEN_MUTASYON))
            if mp["evrensel_kiricilar"]:
                print(f"  ⚠️ evrensel kırıcı: {mp['evrensel_kiricilar']}")

    # ---------------------------------------------------------------- Ç2, Ç3, Ç5
    print("Ç1.5/Ç2/Ç3/Ç5 — kapı testleri koşuluyor (dosya bazlı kesin seçim)...")
    # 🔴 Beklenen sayılar `KAPI_SECIMLERI`den gelir — tek kaynak; ve
    # `tests/test_kapi_secimleri.py` onları saniyeler içinde denetler.
    for kod in ("Ç1.5", "Ç2", "Ç3", "Ç5"):
        sec = KAPI_SECIMLERI[kod]
        ad = sec.ad
        g, k, notu = _pytest(sec.yollar, sec.secim, sec.adet)
        notu += kapsam_notu(sec)
        K.append(Kriter(kod, ad, f"{g} geçti, {k} kırıldı{notu}", "0 kırık",
                        k == 0 and g > 0 and not notu))

    # ---------------------------------------------------------------- Ç4
    print("Ç4 — Li platosu ölçülüyor (30 tohum)...")
    from dogrulama.li_duyarlilik import TOHUM_TAM, plato_olc
    li = plato_olc(TOHUM_TAM)
    K.append(Kriter("Ç4.2", "Li platosu, %95 GA genişliği",
                    f"1/{li['ters']:.2f}, GA %{li['ga_genislik_yuzde']:.2f}",
                    "GA < %5", li["ga_genislik_yuzde"] < 5))
    s41 = KAPI_SECIMLERI["Ç4.1"]
    g, k, notu = _pytest(s41.yollar, s41.secim, s41.adet)
    notu += kapsam_notu(s41)
    K.append(Kriter("Ç4.1", s41.ad,
                    f"{g} geçti, {k} kırıldı{notu}", "0 kırık",
                    k == 0 and g > 0 and not notu))

    # ---------------------------------------------------------------- Ç6
    print("Ç6 — kaynak denetimi + marj değişmezi...")

    # 🔴 B-09: Ç6.2 ARTIK DİZGİ EŞLEŞMESİ DEĞİL.
    # Önceki hâli `"kanal_dilimi_s: float = 1e-4" in config.py` idi ve
    # ölçtüğünü iddia ettiği şeyle TERS korelasyonluydu:
    #   · `0.0001` yazılsaydı (davranış birebir aynı) → Ç6.2 GEÇMEZDİ
    #   · `slot_s`/`sifs_s`/`onay_bayt` değişip marj bozulsaydı, dizgi
    #     durduğu için Ç6.2 GEÇERDİ
    # Gerçek değişmez testi zaten vardı (`test_rng.py`) ama HİÇBİR KAPIYA
    # DAHİL DEĞİLDİ. Artık Ç6.2 doğrudan ona bağlı.
    s62 = KAPI_SECIMLERI["Ç6.2"]
    g62, k62, n62 = _pytest(s62.yollar, s62.secim, s62.adet)
    n62 += kapsam_notu(s62)
    K.append(Kriter("Ç6.2", s62.ad,
                    f"{g62} geçti, {k62} kırıldı{n62}", "0 kırık",
                    k62 == 0 and g62 > 0 and not n62))

    # 🔴 B-111 (26 Ağu → altıncı denetim): Ç6.1 ve Ç6.3 ARTIK DİZGİ ARAMASI
    # DEĞİL. Eski hâlleri yorumdaki bir dizgiyle KANDIRILABİLİYOR, davranışı
    # birebir aynı bir yeniden yazımla da YANLIŞLIKLA DÜŞÜYORDU (dördü de
    # ölçüldü). Yüklemler yukarıda, AST üzerinde; sentetik kaynaklarla ucuz
    # sınanabiliyorlar (`test_b111_*`).
    #
    # ⚠️ Bunlar hâlâ KOD DENETİMİDİR, davranış testi değildir — etiket bunu
    # söylemek zorunda (B-09'un asıl dersi).
    kaynak_mac = (KOK / "sim" / "mac.py").read_text(encoding="utf-8")
    denetim = [
        ("Ç6.1", "kaynak denetimi (AST): onay gerçek iletim, yönü doğru",
         c61_onay_yonu_dogru(kaynak_mac)),
        ("Ç6.3", "kaynak denetimi (AST): Iletim KİMLİKLE karşılaştırılıyor",
         c63_iletim_kimlikle_karsilastiriliyor(kaynak_mac)),
        ("Ç6.4", "kaynak denetimi: skeleton.py silindi",
         not (KOK / "sim" / "skeleton.py").exists()),
    ]
    for kod, ad, ok in denetim:
        K.append(Kriter(kod, ad, "evet" if ok else "HAYIR", "evet", ok))

    # ---------------------------------------------------------------- tablo
    print("\n" + "=" * 80)
    print(f"{'kriter':>6}  {'ne':<44} {'ölçülen':>18} {'eşik':>10}  ")
    print("-" * 80)
    for k in K:
        isaret = "OK " if k.gecti else "!! "
        print(f"{isaret}{k.kod:>4}  {k.ad:<44} {k.olculen:>18} {k.esik:>10}")

    kalan = [k.kod for k in K if not k.gecti]
    print("=" * 80)
    print(f"Süre: {(time.perf_counter()-t0)/60:.1f} dk")
    if kalan:
        print(f"!! AİLE 0 KAPANMADI — geçmeyen: {', '.join(kalan)}")
        sys.exit(1)
    print(f"OK AİLE 0 KAPANMAYA HAZIR — {len(K)}/{len(K)} kriter geçti.")


if __name__ == "__main__":
    # 🔴 B-106 — kapı Ç1'in 540 koşusunu KENDİ içinden çağırıyor
    # (`ana_matris` / `uc_durum_matrisi`), `kapi_korunum.main()`ten
    # değil. Üretim yolu budur; sonuç satırları buradan yazılır.
    from dogrulama.olcum import kayit
    with kayit("aile0_kapi_raporu"):
        main()
