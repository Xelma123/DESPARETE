"""
İKİ KOLU KARŞILAŞTIRMA — ortak alt küme üzerinden (B-19).

🔴 NEDEN BU DOSYA VAR
=====================
Gecikme yalnızca **teslim edilen** paketlerden ölçülür. Farklı teslim
oranına sahip iki protokolü ham gecikmede karşılaştırmak, kötü protokolü
**iyi gösterir**: zor paketleri hiç teslim etmemiştir, dolayısıyla gecikme
dağılımına hiç girmezler. Bu, `03` B3'ün ⭐ ile işaretlediği
**seçilim yanlılığı (survivorship)** tuzağıdır.

Bağımsız denetim bunu bu araçta ÖLÇTÜ (B-19):

    senaryo   teslim ort.   ort. gecikme
    S0        0,9935        48,63 ms
    S2        0,5029        49,77 ms      ← teslim YARIYA düştü, gecikme +%2

Teslim oranı yarıya inerken gecikmenin yalnızca %2 artması, gecikmenin
zorlaşmadığı anlamına gelmez — **zor paketlerin ölçüme hiç girmediği**
anlamına gelir.

`03` B3'ün çözümü: *"Ortak alt küme üzerinden karşılaştır ve kesişim
oranını raporla."* Bu dosya o karşılaştırmayı yapar.

⚠️ KESİŞİM ORANI HER ZAMAN RAPORLANIR. Ortak alt küme küçüldükçe
karşılaştırma daralır; kesişim yazılmadan verilen bir gecikme farkı,
hangi paketler üzerinde ölçüldüğü bilinmeyen bir sayıdır.
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from statistics import mean


# 🔒 KONTROL PAYININ OKUDUĞU PENCERE — `08` madde 31.
# *"Aile 1'in her karşılaştırması `*_pencere` alanlarını kullanmak
# zorundadır; tüm koşu hâli teşhis içindir."* Ölçüldü: kontrol baytının
# %17,63–22,84'ü ölçüm penceresi DIŞINDA üretiliyor ve çarpıklık KOLA GÖRE
# değişiyor — yani tüm koşu hâliyle yapılan eşleştirilmiş bir kol
# karşılaştırması YANLIDIR.
_PAY_ALANLARI = ("kontrol_bayt_pencere", "veri_bayt_pencere",
                 "kontrol_airtime_s_pencere", "veri_airtime_s_pencere")


def yuzdelik(veri, p: float):
    """En yakın sıra yüzdeliği.

    🔴 GÖVDE DEĞİŞTİRİLEMEZ (Y14). `06` §8.1'in tablosunu üreten tanım
    budur; `int(round(...))` Python'un BANKACI yuvarlamasıdır ve
    `int(x + 0.5)` ile aynı DEĞİLDİR. Başka bir yüzdelik tanımı (doğrusal
    interpolasyon vb.) aynı veriden BAŞKA sayı üretir ve `06`nın dört
    sayısı sessizce bayatlar.

    ⚠️ `dogrulama/gecikme.py` bunu İÇE AKTARIR, kopyalamaz: ikinci bir
    doğru kaynağı B-07'nin tuzağıdır.
    """
    if not veri:
        return None
    s = sorted(veri)
    k = min(len(s) - 1, max(0, int(round(p * (len(s) - 1)))))
    return s[k]


def kontrol_payi_yuzde(sonuc: dict) -> dict | None:
    """Kontrol payı — BAYT ve AIRTIME, ikisi de ölçüm PENCERESİNDEN.

    🔴 İKİ BİRİM DE ZORUNLU (`08` §Ayrıca): ölçüldü — kontrol payı bayt
    cinsinden %2,84, airtime cinsinden %5,12 (**1,80 kat**). Sebep önbelge:
    her çerçeveye sabit 192 µs ekleniyor. **Aynı baytı farklı sayıda
    çerçeveye bölen iki protokol bayt metriğinde EŞİT görünür ve airtime'da
    2 kat farklı olur.** Tek birim raporlamak, K-009'un adalet şartını
    doğrulanamaz yapar.

    🔴 DEJENERE PAYDA TİPLİ REDDEDİLİR (D-11): veri baytı sıfırken oran
    %100 görünür ama bir kontrol payı DEĞİLDİR — bir artefakttır.
    """
    kb, vb = sonuc["kontrol_bayt_pencere"], sonuc["veri_bayt_pencere"]
    ka, va = (sonuc["kontrol_airtime_s_pencere"],
              sonuc["veri_airtime_s_pencere"])
    # 🔴 B-134 (yedinci denetim) — TANIMSIZLIK ARTIK KARŞILAŞTIRMAYI
    # ÖLDÜRMÜYOR, RAPORLANIYOR.
    #
    # Önceki hâli `KarsilastirmaHatasi` fırlatıyordu ve `ortak_alt_kume`
    # bunu dönüş nesnesini kurmadan ÖNCE çağırdığı için TÜM karşılaştırma
    # düşüyordu. Denetim ölçtü: 801 ortak paket üzerinden hesaplanmış,
    # tamamen geçerli bir gecikme farkı (+10,140 ms) GECİKMEYLE HİÇ
    # İLGİSİ OLMAYAN bir payda yüzünden üretilemiyordu.
    #
    # 🔒 KARAR (danışmana devredildi, K-088): `None` döndürülür.
    #   · `06` koşul 3 kontrol payının RAPORLANMASINI istiyor;
    #     *"TANIMSIZ (D-11)"* bir rapordur — hem de sayıdan bilgilendirici.
    #   · `03` B3: *"iki çakışmayan olgu tek metriğe sıkışırsa metriği
    #     İKİYE AYIR."* Gecikme farkı ile kontrol payı iki ayrı olgudur.
    #   · D-11'in asıl derdi *"kendinden emin görünen bir SAYI"*ydı;
    #     `None` + açık etiket o derdi karşılıyor, sayı üretmiyor.
    #
    # ⚠️ Bedeli `08`e madde olarak yazıldı: bir karşılaştırma artık
    # kontrol payı TANIMSIZKEN de üretilebilir ve `ozet()` bunu bağırır.
    if vb == 0 or va == 0:
        return None
    return {"bayt": 100.0 * kb / (kb + vb),
            "airtime": 100.0 * ka / (ka + va)}


def _pay_metni(pay: dict | None) -> str:
    """Kontrol payının rapor metni — TANIMSIZ hâli SESSİZ GEÇMEZ (B-134)."""
    if pay is None:
        return "🔴TANIMSIZ(D-11)"
    return f"%{pay['bayt']:.2f}b/%{pay['airtime']:.2f}a"


class KarsilastirmaHatasi(Exception):
    """İki sonuç karşılaştırılabilir değil."""


@dataclass(frozen=True)
class OrtakAltKume:
    """İki kolun ortak alt kümesi üzerinden karşılaştırma."""

    ortak_paket: int
    birlesim_paket: int
    pencere_paket: int

    ortalama_gecikme_a_s: float | None
    ortalama_gecikme_b_s: float | None

    # Aynı kolun KENDİ teslim ettiklerinden hesaplanan (yanlı) değer
    ham_gecikme_a_s: float | None
    ham_gecikme_b_s: float | None

    teslim_a: int
    teslim_b: int

    # 🔴 B0.3 — ORTAK ALT KÜME ÜZERİNDE YÜZDELİKLER (`06` §8.1 mühürlü).
    # Ortalama tek başına kuyruğu göremez: ölçüldü (30 tohum, eşleştirilmiş,
    # `en_kisa_yol` S0→S2, ortak alt küme) — ortalama +5,40 ms, p95
    # **+28,15 ms**. Kuyruk merkezin ~5 KATI kötüleşiyor.
    yuzdelik_a: dict
    yuzdelik_b: dict

    # 🔴 B0.4 — KONTROL PAYI ZORUNLU (`06` Bölüm 9 koşul 3).
    # *"Kollar arasında gizli asimetri yok"* şartı ölçülmeden hiçbir
    # karşılaştırma geçerli değildir; ölçüldü (30 tohum, DV <-> gözlem,
    # pencere · bayt, n = 58): kollar arası kontrol payı **4,0-38,0 kat**
    # farklılaşabiliyor, ortanca **12,6** (`08` md 25). Fark bir haksızlık
    # değil bir BULGUDUR — ama raporlanmadan karşılaştırma yapılamaz.
    #
    # 🔴 B-169 (2 Eylül 2026): burada **8,3-17,8 kat** yazıyordu. O sayı
    # 3 TOHUMDAN geliyordu ve `08` md 25 onu B0.4'te KENDİSİ geri aldı
    # (`03` kural 2: >=30 tohum). Aynı geri alınan değer `07` §4.3 ve
    # `11`de de duruyordu — B0.4 dört belgeyi güncelledi, üç yeri
    # güncellemedi. Y14: *"bir kod düzeltmesi, ondan önce ölçülmüş HER
    # SAYIYI şüpheli yapar."*
    kontrol_payi_a: dict | None      # 🔴 None = TANIMSIZ (D-11 · B-134)
    kontrol_payi_b: dict | None

    @property
    def kesisim_orani_birlesim(self) -> float:
        """|A∩B| / |A∪B| — iki kolun ne kadarını birlikte ölçebiliyoruz."""
        return self.ortak_paket / self.birlesim_paket if self.birlesim_paket else 0.0

    @property
    def kesisim_orani_pencere(self) -> float:
        """|A∩B| / pencere — üretilen paketlerin ne kadarı ortak."""
        return self.ortak_paket / self.pencere_paket if self.pencere_paket else 0.0

    @property
    def gecikme_farki_s(self) -> float | None:
        """b − a, ORTAK alt küme üzerinden."""
        if self.ortalama_gecikme_a_s is None or self.ortalama_gecikme_b_s is None:
            return None
        return self.ortalama_gecikme_b_s - self.ortalama_gecikme_a_s

    @property
    def p95_farki_s(self) -> float | None:
        """b − a, ORTAK alt küme p95'i üzerinden.

        🔴 Neden ayrı bir özellik: ölçüldü (30 tohum, `en_kisa_yol`,
        S0→S2, eşleştirilmiş) — ortalama farkı **+5,40 ms** (p=0,0003),
        p95 farkı **+28,15 ms** (p=0,0000). Kuyruk merkezin ~5 katı
        kötüleşiyor ve tek başına ortalama bunu göstermiyor.
        """
        if not self.yuzdelik_a or not self.yuzdelik_b:
            return None
        return self.yuzdelik_b["p95"] - self.yuzdelik_a["p95"]

    @property
    def ham_fark_s(self) -> float | None:
        """b − a, HAM (yanlı) değerlerden. Yalnızca yanlılığı göstermek için."""
        if self.ham_gecikme_a_s is None or self.ham_gecikme_b_s is None:
            return None
        return self.ham_gecikme_b_s - self.ham_gecikme_a_s

    def ozet(self) -> str:
        """Rapora giren tek satır — kesişim oranı DAİMA içinde."""
        if self.ortak_paket == 0:
            return (f"ortak alt küme BOŞ (A={self.teslim_a}, B={self.teslim_b}) "
                    f"— gecikme karşılaştırması YAPILAMAZ")
        # 🔒 ÜÇÜ BİRDEN: kesişim oranı · p95 · kontrol payı.
        # Hiçbiri isteğe bağlı değil — üçü de `06`nın geçerlilik
        # koşullarından birini taşıyor (sırasıyla `08` md 16, `06` §8.1
        # mühürlü cümlesi, `06` Bölüm 9 koşul 3).
        return (
            f"ortak {self.ortak_paket} paket "
            f"(kesişim %{100*self.kesisim_orani_birlesim:.1f} birleşim, "
            f"%{100*self.kesisim_orani_pencere:.1f} pencere) · "
            f"gecikme ort A={1000*self.ortalama_gecikme_a_s:.2f} "
            f"B={1000*self.ortalama_gecikme_b_s:.2f} ms · "
            f"p95 A={1000*self.yuzdelik_a['p95']:.2f} "
            f"B={1000*self.yuzdelik_b['p95']:.2f} ms · "
            f"kontrol payı A={_pay_metni(self.kontrol_payi_a)} "
            f"B={_pay_metni(self.kontrol_payi_b)}"
        )


def ortak_alt_kume(sonuc_a: dict, sonuc_b: dict) -> OrtakAltKume:
    """İki koşu sonucunu ORTAK teslim edilen paketler üzerinden karşılaştırır.

    🔴 Y7 — ARAÇ NE KARŞILAŞTIRDIĞINI KENDİSİ DOĞRULAR.
    İki sonucun aynı paket evreninden gelmesi ZORUNLUDUR; gelmiyorsa
    karşılaştırma anlamsızdır ve sessizce yanlış bir sayı üretmek yerine
    `KarsilastirmaHatasi` fırlatılır.

    Paket evreninin protokolden bağımsız olduğu ölçüldü ve teste bağlandı
    (`test_b19_paket_evreni_protokolden_bagimsiz`): trafik akışları
    protokolün çektiği rastgele sayı adedinden etkilenmez.
    """
    for ad, s in (("a", sonuc_a), ("b", sonuc_b)):
        # 🔴 `_PAY_ALANLARI` BU LİSTEDE: `06` Bölüm 9 koşul 3 gereği kontrol
        # payı olmadan karşılaştırma yapılamaz. Taşımayan bir satır sessizce
        # kabul edilip "kontrol payı bilinmeyen" bir gecikme farkı üretemez.
        for alan in ("teslim_kimlikleri", "teslim_gecikmeleri_s",
                     "pencere_kimlik_araligi", "pencerede_uretilen",
                     "pencere_evren_hash", "kurulum_hash",
                     "kaynak_hash", *_PAY_ALANLARI):
            if alan not in s:
                raise KarsilastirmaHatasi(
                    f"sonuc_{ad} bu şemayı taşımıyor: {alan!r} yok. "
                    f"B-19/B-26 öncesi üretilmiş bir satır olabilir — o "
                    f"satırlar ortak alt küme karşılaştırmasını DESTEKLEMEZ."
                )

    # 🔴 B-26 — ASIL KONTROL: PAKET EVRENİ PARMAK İZİ.
    # ---------------------------------------------------------------------
    # ⚠️ ÖNCEKİ KORUMA HİÇBİR ŞEY DOĞRULAMIYORDU. Yalnızca
    # `pencere_kimlik_araligi` ve `pencerede_uretilen`e bakıyordu; ikisi de
    # YALNIZCA `trafik_zamani` akışından belirlenir, dolayısıyla tohum
    # dışında hiçbir konfigürasyon farkı onları değiştiremez.
    #
    # İkinci bağımsız denetim (B-26) bunu kırdı: `dugum_sayisi` 40 → 41
    # yapıldığında iki kolun 3198 paketinin HİÇBİRİ aynı (kaynak, hedef)
    # çiftini taşımıyordu — yani ortak tek bir paket yoktu — ve koruma
    # karşılaştırmayı kabul edip 31,6 ms'lik bir "gecikme farkı" üretti.
    #
    # Daha kötüsü: korumanın tek pozitif testi de TOHUM farkını kullanıyordu,
    # yani koruma **yalnızca yakalayabildiği tek durumla** sınanmıştı.
    #
    # Parmak izi paketin kimliğini tanımlayan her şeyi kapsar
    # (kimlik · doğum anı · kaynak · hedef) ve protokolden bağımsızdır.
    if sonuc_a["pencere_evren_hash"] != sonuc_b["pencere_evren_hash"]:
        raise KarsilastirmaHatasi(
            f"paket EVRENLERİ farklı: {sonuc_a['pencere_evren_hash'][:16]}… vs "
            f"{sonuc_b['pencere_evren_hash'][:16]}… — "
            f"Aynı kimlik iki kolda AYNI paketi göstermiyor; 'ortak alt küme' "
            f"diye bir şey yok. Tohum, trafik ve topoloji konfigürasyonu "
            f"birebir aynı olmalı."
        )

    # 🔴 ÜÇÜNCÜ KONTROL: KOD SÜRÜMÜ (B-46).
    # Konfigürasyon ve paket evreni aynı olsa bile SİMÜLATÖR farklı
    # olabilir. Üçüncü bağımsız denetim bunu ölçtü: birebir aynı konfig
    # ve tohum, tek fark `mac._onay_zaman_asimi`'ndeki geri çekilme —
    # iki parmak izi de AYNI çıktı ve koruma 7,76 ms'lik bir fark
    # üretti. Kod farkı bir TEDAVİ DEĞİLDİR.
    #
    # ⚠️ Bu deponun kendi geçmişi riski gerçek kılıyor: şema bir günde
    # iki kez değişti ve ikinci denetim dört bayat çıktı dosyası buldu.
    if sonuc_a["kaynak_hash"] != sonuc_b["kaynak_hash"]:
        raise KarsilastirmaHatasi(
            f"KOD SÜRÜMLERİ farklı: {sonuc_a['kaynak_hash'][:16]}… vs "
            f"{sonuc_b['kaynak_hash'][:16]}… — konfigürasyon aynı olsa "
            f"bile iki satır FARKLI BİR SİMÜLATÖRDEN geliyor. İki kol "
            f"yalnızca TEDAVİDE ayrılabilir; kod farkı tedavi değildir."
        )

    # 🔴 İKİNCİ KONTROL: KURULUM PARMAK İZİ.
    # Paket evreni aynı kalıp AĞ değişebilir (`iletim_menzili_m` 280→300,
    # `alan_m` 1000→1010): aynı kimlik, aynı doğum, aynı kaynak-hedef — ama
    # farklı topoloji. O iki koşu aynı deneyin iki kolu DEĞİLDİR.
    # Tedavi alanları (kol · senaryo · güç override'ı · ablasyon bayrakları)
    # hariç her şey eşleşmek zorunda.
    if sonuc_a["kurulum_hash"] != sonuc_b["kurulum_hash"]:
        raise KarsilastirmaHatasi(
            f"KURULUMLAR farklı: {sonuc_a['kurulum_hash'][:16]}… vs "
            f"{sonuc_b['kurulum_hash'][:16]}… — paket evreni aynı olsa bile "
            f"ağ/konfigürasyon farklı. İki kol yalnızca TEDAVİDE ayrılabilir "
            f"(kol · senaryo · güç override'ı · ablasyon bayrağı)."
        )

    # Aşağıdakiler artık parmak izinden ÇIKAR; yine de tutulur, çünkü hata
    # mesajını okunur yapar (hangi yönde farklılar).
    if sonuc_a["pencere_kimlik_araligi"] != sonuc_b["pencere_kimlik_araligi"]:
        raise KarsilastirmaHatasi(
            f"paket kimlik aralıkları farklı: "
            f"{sonuc_a['pencere_kimlik_araligi']} vs "
            f"{sonuc_b['pencere_kimlik_araligi']}"
        )
    if sonuc_a["pencerede_uretilen"] != sonuc_b["pencerede_uretilen"]:
        raise KarsilastirmaHatasi("pencerede üretilen paket sayıları farklı")

    # 🔴 DÖRDÜNCÜ EKSEN: SATIRIN KENDİ İÇİ (B-67, K-056).
    # ---------------------------------------------------------------------
    # Üstteki üç kontrol KOLLAR ARASI tutarlılığı denetliyordu; bir satırın
    # KENDİ içindeki yapı hiç denetlenmiyordu. Dördüncü bağımsız denetim
    # dört bozuk satır üretti ve **dördü de kabul edildi**:
    #
    #   gecikme listesi yarıya kırpık -> "gecikme farkı 846,701 ms"
    #   tüm kimlikler aynı            -> ortak=1, fark 551,345 ms
    #   tüm gecikmeler NaN            -> fark = nan, BAYRAK YOK
    #   tüm gecikmeler negatif        -> fark −1 023,977 ms
    #
    # Sebep: `dict(zip(...))` sessizce KIRPAR ve tekrarlı kimliği EZER.
    # NaN maddesi ayrıca `03` B2'nin 🔴 "NaN'ın sessizce zehirlemesi"
    # kuralına dokunuyor: istatistik katmanı yazılmadı ama NaN'ı taşıyan
    # boru zaten çalışıyor.
    #
    # Dördü de bugünkü gerçek çıktıda TUTUYOR — yani kırılabilir.
    for ad, s in (("a", sonuc_a), ("b", sonuc_b)):
        kim = s["teslim_kimlikleri"]
        gec = s["teslim_gecikmeleri_s"]
        if len(kim) != len(gec):
            raise KarsilastirmaHatasi(
                f"sonuc_{ad}: {len(kim)} kimlik ama {len(gec)} gecikme. "
                f"`dict(zip(...))` bunu sessizce KIRPAR ve ortak paket "
                f"sayısını yanlış üretir.")
        if len(set(kim)) != len(kim):
            raise KarsilastirmaHatasi(
                f"sonuc_{ad}: teslim kimlikleri TEKRARLI "
                f"({len(kim)} kayıt, {len(set(kim))} benzersiz). Tekrarlı "
                f"kimlik `dict` içinde EZİLİR.")
        if not all(math.isfinite(x) for x in gec):
            raise KarsilastirmaHatasi(
                f"sonuc_{ad}: gecikmelerde NaN/sonsuz var. `03` B2: "
                f"'NaN sessizce zehirler' — tek bir NaN ortalamayı ve "
                f"düzeltilmiş p'lerin tümünü bozar.")
        if not all(x >= 0.0 for x in gec):
            raise KarsilastirmaHatasi(
                f"sonuc_{ad}: NEGATİF gecikme var (en küçük {min(gec):.6f}). "
                f"Bir paketin teslim anı doğum anından önce olamaz.")

        # ------------------------------------------------------------------
        # 🔴 B-85 (BEŞİNCİ DENETİM) — BEŞİNCİ EKSEN: KARDİNALİTE / KAPSAMA
        #
        # B-67 satır İÇİ yapıyı denetliyordu (uzunluk · tekrar · finite ·
        # negatiflik) ama satırın KENDİ SAYILARIYLA tutarlı olup olmadığını
        # denetlemiyordu. Beşinci denetim beş bozuk satır üretti, BEŞİ DE
        # kabul edildi ve sayı üretti. En keskini:
        #
        #     araç kendi rapor satırında `kesişim %328.5 pencere` bastı
        #
        # Bir kesişim oranı %100'ü AŞAMAZ. `ozet()`, `03` B3'ün *"kesişim
        # oranını raporla"* şartını yerine getiren TEK satırdır ve kendi
        # kendini denetlemiyordu (Y7).
        #
        # 🔒 Üçü de bugünkü GERÇEK çıktıda tutuyor — yani KIRILABİLİR (Y10):
        #     802 ≤ 2 698 · kimlikler [500, 3197) içinde · 802 == len(...)
        # ------------------------------------------------------------------
        uretilen = s.get("pencerede_uretilen")
        if uretilen is not None and len(kim) > uretilen:
            raise KarsilastirmaHatasi(
                f"sonuc_{ad}: {len(kim)} teslim kimliği var ama pencerede "
                f"yalnızca {uretilen} paket ÜRETİLDİ. Teslim, üretilenden "
                f"çok olamaz; kesişim oranı %100'ü aşar ve `ozet()` "
                f"imkânsız bir sayı basar (B-85).")

        aralik = s.get("pencere_kimlik_araligi")
        if aralik and kim:
            alt, ust = aralik[0], aralik[1]
            # ⚠️ ARALIK İKİ UÇTA DA KAPALIDIR: üretici
            # `[pencere[0].kimlik, pencere[-1].kimlik]` yazıyor, yani İLK ve
            # SON paketin kimliği — ikisi de pencerededir. İlk yazımda üst uç
            # DIŞLAYICI sanılmıştı ve `kimlik == ust` olan gerçek bir satır
            # reddedildi (Y5: test kırılınca önce TESTİN VARSAYIMI denetlenir).
            disarida = [k for k in kim if not (alt <= k <= ust)]
            if disarida:
                raise KarsilastirmaHatasi(
                    f"sonuc_{ad}: {len(disarida)} teslim kimliği ölçüm "
                    f"penceresinin ARALIĞI dışında (pencere [{alt}, {ust}], "
                    f"ör. {disarida[:3]}). Hiç üretilmemiş paketlerden "
                    f"gecikme farkı hesaplanır (B-85).")

        p_teslim = s.get("pencerede_teslim")
        if p_teslim is not None and p_teslim != len(kim):
            raise KarsilastirmaHatasi(
                f"sonuc_{ad}: `pencerede_teslim` {p_teslim} diyor ama "
                f"{len(kim)} kimlik var. Satır KENDİ İÇİNDE tutarsız; "
                f"hangisinin doğru olduğu bilinemez (B-85).")

        # 🔴 B-85 · E5 — GECİKME İSTATİSTİKLERİ AYNI LİSTEDEN GELİR.
        # Denetçi E5'i *"şemada üst sınır yok"* diye açık bırakmıştı; üst
        # sınır gerekmiyor: `ortalama_gecikme_s` ve `ortanca_gecikme_s`
        # listenin KENDİSİNDEN türetilir ve onunla tutarlı OLMAK ZORUNDA.
        # ⚖️ Aynı bağ, sonuç şemasının en sinsi mutasyonunu da yakalar:
        # `ortanca_gecikme_s`i ORTALAMAYA çevirmek (C01 — S0'da 22× fark).
        if gec:
            for alan, hesap in (("ortalama_gecikme_s", statistics.fmean),
                                ("ortanca_gecikme_s", statistics.median)):
                yazili = s.get(alan)
                if yazili is None:
                    continue
                gercek = hesap(gec)
                if abs(yazili - gercek) > 1e-9 * max(1.0, abs(gercek)):
                    raise KarsilastirmaHatasi(
                        f"sonuc_{ad}: `{alan}` {yazili:.9f} diyor ama "
                        f"gecikme listesinden {gercek:.9f} çıkıyor. Satır "
                        f"KENDİ İÇİNDE tutarsız — hangi büyüklüğün "
                        f"raporlandığı bilinemez (B-85).")

        oran, uret = s.get("teslim_orani"), s.get("pencerede_uretilen")
        if oran is not None and uret:
            beklenen = len(kim) / uret
            if abs(oran - beklenen) > 1e-9:
                raise KarsilastirmaHatasi(
                    f"sonuc_{ad}: `teslim_orani` {oran:.6f} diyor ama "
                    f"kimlik/üretilen {beklenen:.6f}. Satır KENDİ İÇİNDE "
                    f"tutarsız (B-85).")

    a = dict(zip(sonuc_a["teslim_kimlikleri"], sonuc_a["teslim_gecikmeleri_s"]))
    b = dict(zip(sonuc_b["teslim_kimlikleri"], sonuc_b["teslim_gecikmeleri_s"]))
    ortak = sorted(set(a) & set(b))
    birlesim = set(a) | set(b)

    # 🔴 Kontrol payı BURADA hesaplanır, çağırana bırakılmaz: bırakılsaydı
    # "raporlamayı unutmak" mümkün olurdu ve koşul 3 yine sağlanmazdı.
    # Dejenere payda tipli hatayla reddedilir (D-11).
    pay_a = kontrol_payi_yuzde(sonuc_a)
    pay_b = kontrol_payi_yuzde(sonuc_b)

    y_a = {f"p{int(100*q)}": yuzdelik([a[k] for k in ortak], q)
           for q in (0.50, 0.95, 0.99)} if ortak else {}
    y_b = {f"p{int(100*q)}": yuzdelik([b[k] for k in ortak], q)
           for q in (0.50, 0.95, 0.99)} if ortak else {}

    return OrtakAltKume(
        yuzdelik_a=y_a, yuzdelik_b=y_b,
        kontrol_payi_a=pay_a, kontrol_payi_b=pay_b,
        ortak_paket=len(ortak),
        birlesim_paket=len(birlesim),
        pencere_paket=sonuc_a["pencerede_uretilen"],
        ortalama_gecikme_a_s=mean(a[k] for k in ortak) if ortak else None,
        ortalama_gecikme_b_s=mean(b[k] for k in ortak) if ortak else None,
        ham_gecikme_a_s=mean(a.values()) if a else None,
        ham_gecikme_b_s=mean(b.values()) if b else None,
        teslim_a=len(a),
        teslim_b=len(b),
    )
