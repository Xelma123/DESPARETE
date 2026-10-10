"""
KARAR KAYDI INDEKSI — `04`un basindaki indeks tablosunu URETIR.

🔴 NEDEN BU DOSYA VAR
=====================
`04-NEDEN-BOYLE.md` **81 kayit / 7 500+ satir**. Indeks olmadan bir ajan
hangi kaydin hala gecerli oldugunu bilemez ve **eski bir karari bugunku
karar sanar** — ogrencinin *"bu dosyalar halisunasyona sebep oluyor"*
dedigi sey tam olarak budur.

🔴 VE INDEKS ELLE TUTULMAZ. Elle tutulan bir indeks bayatlar; bu depoda
ayni sinif hata **dort kez** yasandi *(Ç5'in beklenen test sayisi iki kez,
`08`in madde sayaci, kor tarama havuzu)*. Bu yuzden indeks **uretilir**.

🔒 REVIZE EDILEN KAYIT SILINMEZ
================================
Deponun kulturu: *"curutulen bir iddia revizyonla duzeltilir, silinmez."*
Bir kararin sonradan degistigini gostermek, hic verilmemis gibi
gorunmesinden **guclüdur** — ve TUBITAK'in en cok agirlik verdigi
*fikir sahipligi* kriteri tam olarak bunu odullendirir.

Indeks bunun yerine **durumu** yazar: gecerli mi, revize mi, nereye bakilmali.

KULLANIM
--------
    PYTHONIOENCODING=utf-8 python arsiv/dogrulama/kayit_indeksi.py
    PYTHONIOENCODING=utf-8 python arsiv/dogrulama/kayit_indeksi.py --kontrol

`--kontrol` dosyayi DEGISTIRMEZ; indeks bayatsa `1` doner. CI/ongorusu
icin: indeks ile gercek kayit listesi ayrisirsa hata verir.

🔴 KAPSAMI (Y11 — koruma kendi siniriyla yazilir)

    | ne yakalanir                                   | evet/hayir |
    | yeni kayit eklenmis, indekse girmemis          | evet       |
    | kayit basligi degismis, indeks eski            | evet       |
    | 🔴 REVIZE HARITASI bayatlamis                  | HAYIR      |
    |    (SUPERSEDE elle tutulur — asagiya bak)      |            |

⚠️ `SUPERSEDE` **elle tutulur** ve bu bilincli: bir kaydin hangi kayitla
revize edildigi **anlamsal** bir iliskidir, metinden cikarilamaz. Ama
listedeki her kimlik **var olmak zorundadir** — bayat bir kimlik hata verir.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# 🔴 17 Eylul 2026'da ONARILDI. Kok SABIT bir ust dizin sayisiyla
# turetiliyordu (`parent.parent`) ve betik `arsiv/`e tasininca kok `arsiv/`
# oldu: `arsiv/v2/04-NEDEN-BOYLE.md` diye var olmayan bir dosya araniyordu.
# Yani `04`un indeksi DORT GUNDUR uretilemiyordu ve indeks K-088'de donmustu.
# 🔒 Kok artik KONUMDAN degil ARANAN DOSYADAN turer; betik bir daha
# tasinirsa kirilmaz. Ayni hatanin sinifi `uretici_duman.py`nin 1 numarali
# bulgusudur: belgelenen komut, belgelenen sayiyi uretmiyordu.
def _kok() -> Path:
    for aday in [Path(__file__).resolve(), *Path(__file__).resolve().parents]:
        if (aday / "v2" / "kayit" / "KARAR-GUNLUGU.md").is_file():
            return aday
    raise SystemExit("🔴 `v2/kayit/KARAR-GUNLUGU.md` bulunamadi — "
                     "betik depo agacinin disinda kosuyor")


KOK = _kok()
# 28 Eylül 2026 (belge temizliği): tam günlük `v2/kayit/`e taşındı;
# `v2/04-KARARLAR.md` yalnız bugün geçerli kararları tutar.
KAYIT_DOSYASI = KOK / "v2" / "kayit" / "KARAR-GUNLUGU.md"

BAS = "# 📇 KAYIT İNDEKSİ"
SON = "<!-- INDEKS SONU -->"

# --------------------------------------------------------------------------
# 🔴 REVİZE HARİTASI — elle tutulur, her biri gerekçesiyle.
# Bir kayıt burada YOKSA "geçerli" sayılır. Buraya eklemek, o kararın
# ARTIK BAĞLAYICI OLMADIĞINI ilan etmektir; kayıt yine de silinmez.
# --------------------------------------------------------------------------
# 📦 23 Eylül 2026: K-001…K-089 `v2/arsiv/04-NEDEN-BOYLE-K001-K089.md`ye
# ayrıldı. Onların revize eşlemeleri AŞAĞIDA, tarihsel kayıt olarak durur ve
# etkin dizine GİRMEZ — etkin dosyada olmayan bir kimlik "hayalet" sayılırdı.
ARSIV_SUPERSEDE: dict[str, tuple[str, str]] = {
    "K-009": ("kural 4 revizyonu + `07` §4.3",
              "*Eşit kontrol düzlemi bütçesi* şartı **kalktı**: AODV/OLSR HELLO "
              "aralıkları eşitlenmez, kontrol yükü **raporlanır**"),
    "K-026": ("K-035",
              "Karıştırıcı hızı 20,944 → **15,0**'e geri alındı; gerekçe ölçümle çürütüldü"),
    "K-077": ("K-081",
              "*Boşluk A yetiyor* okuması **daraltıldı**: A-dar yetiyordu, **A-tam seçildi**"),
    "K-079": ("K-081",
              "*A-dar* kararı **tersine döndü**; kapsam maddesi 32 → **33**"),
    "K-086": ("K-087",
              "Yedinci bağımsız denetim **dört iddiayı çürüttü**: *çarpıklık "
              "1,004–1,079 olamaz* **yanlış** (band analitik değil) · *`yuzdelik` "
              "tek gövde* **yanlış** (üç gövde) · *iki bağımsız ölçüm hattı* "
              "**tautoloji** (aynı deterministik koşular) · md 31'in bandı "
              "**tek tohumluk**. Ölçümleri ayakta, gerekçeleri değil"),
}

SUPERSEDE: dict[str, tuple[str, str]] = {
    "K-140": ("K-143 · K-145",
              "AODV kapanışının U1 tablosu `AODV-c` hâline aitti; RFC §6.11 öncül "
              "kuralı davranışı değiştirdi (K-143) ve kapanış `AODV-e` ile yeniden "
              "koşuldu (K-145). Açıklanmış düşük hücre 4 → **2**"),
    "K-191": ("K-196",
              "OLSR'ın U1 sayıları (0,642…) §13 açık `OLSR-b` hâline aitti; K-196 "
              "§13'ü kapattı (`OLSR-c`) ve düşük hücreleri \"açıklanmış, "
              "sıralamasız\" okudu"),
    "K-205": ("K-208",
              "`AODV-g` için \"RFC'ye sadık\" iddiası **fazlaydı**: kural kural "
              "denetimde 11 sapma daha çıktı (`AODV-h`)"),
    "K-211": ("K-218",
              "Donan hâller `AODV-i` · `AOMDV-e` ve U1 hükmü 6 örnekli "
              "(yakınsamamış) kâhine aitti; **`AODV-j` · `OLSR-c` · `AOMDV-f`** "
              "yakınsamış kâhinle yeniden dondu"),
    "K-212": ("K-217",
              "G2ç'nin kalışı \"formasyonun zaman kayması\" diye teşhis edilmişti — "
              "**yanlış**: sebep 6 örnekli kâhinin yakınsamamasıydı (K-214); 48 "
              "örnekte G1ç · G2ç · G4ç **GEÇTİ**"),
    "K-218": ("K-224",
              "Donan `OLSR-c` ve 8 iletim denemesiydi; OLSR'ın §8.2.1 düzeltmesi "
              "(`OLSR-d`, K-223) ve standarttaki 7 denemeyle U1 yeniden — "
              "**`AODV-j` · `OLSR-d` · `AOMDV-f`** dondu"),
    "K-213": ("K-216",
              "R = 0,0188 6 örnekli kâhinle ölçülmüştü; yakınsamış kâhinle "
              "**0,0142** (kısa pencere kesiti — denetim D-03)"),
    "K-229": ("K-230",
              "Verici 27 dBm maddesi **geri alındı** (ağ 1–2 atlamaya iniyordu; "
              "güç yalnız mesafeyi ölçekler); rakip değişikliği (AODV · OLSRv2 · "
              "JarmRout) **geçerli**, K-230'da yeniden yazıldı"),
}


def kayitlari_oku() -> list[tuple[str, str]]:
    t = KAYIT_DOSYASI.read_text(encoding="utf-8")
    p = re.split(r"(?m)^# (K-\d\d\d)", t)
    return [(p[i], p[i + 1]) for i in range(1, len(p), 2)]


def baslik(govde: str) -> str:
    """Kaydın ilk anlamlı satırından kısa bir konu çıkarır."""
    for satir in govde.splitlines():
        s = satir.strip()
        if not s or s.startswith(">"):
            continue
        s = re.sub(r"^[·\s]*", "", s).replace("*", "").replace("`", "")
        return s[:88]
    return "(başlıksız)"


def indeks_uret(kayitlar: list[tuple[str, str]]) -> str:
    revize = sum(1 for k, _ in kayitlar if k in SUPERSEDE)
    satirlar = [
        BAS + " — *(üretildi)*",
        "",
        "> 🔴 **BU İNDEKS ELLE TUTULMAZ, ÜRETİLİR.** Bayatlarsa yeniden koşulur:",
        "> ```bash",
        "> PYTHONIOENCODING=utf-8 python arsiv/dogrulama/kayit_indeksi.py",
        "> ```",
        "> Değiştirmeden kontrol: `--kontrol` *(bayatsa 1 döner)*",
        "",
        "🔴 **REVİZE EDİLMİŞ kayıtlar SİLİNMEDİ** — bir kararın sonradan",
        "değiştiğini göstermek, hiç verilmemiş gibi görünmesinden **güçlüdür**.",
        "Hangisinin geçerli olduğu **burada** yazılı.",
        "",
        "| kayıt | konu | durum |",
        "|---|---|---|",
    ]
    for k, g in kayitlar:
        if k in SUPERSEDE:
            yer, neden = SUPERSEDE[k]
            satirlar.append("| **%s** | %s | 🔄 **REVİZE → %s**<br>%s |"
                            % (k, baslik(g), yer, neden))
        else:
            satirlar.append("| %s | %s | 🟢 geçerli |" % (k, baslik(g)))
    satirlar += [
        "",
        "**%d kayıt · %d revize · %d geçerli**" % (len(kayitlar), revize, len(kayitlar) - revize),
        "",
        SON,
    ]
    return "\n".join(satirlar)


def main(argv: list[str]) -> int:
    kayitlar = kayitlari_oku()

    # 🔴 Y7 — tarama gerçekten bir şey buluyor mu (boş küme tuzağı)
    if len(kayitlar) < 10:
        print("🔴 yalnızca %d kayıt bulundu — ayrıştırma bozuk olabilir"
              % len(kayitlar))
        return 2

    # 🔴 SUPERSEDE'deki her kimlik VAR OLMALI — bayat harita sessizce yanlışlar
    mevcut = {k for k, _ in kayitlar}
    hayalet = sorted(set(SUPERSEDE) - mevcut)
    if hayalet:
        print("🔴 REVİZE HARİTASINDA OLMAYAN KAYIT: %s" % hayalet)
        return 2

    t = KAYIT_DOSYASI.read_text(encoding="utf-8")
    yeni_indeks = indeks_uret(kayitlar)

    if BAS in t and SON in t:
        i, j = t.index(BAS), t.index(SON) + len(SON)
        eski = t[i:j]
        güncel = t[:i] + yeni_indeks + t[j:]
    else:
        eski = ""
        # İlk kaydın önüne yerleştir
        m = re.search(r"(?m)^# K-\d\d\d", t)
        if m is None:
            print("🔴 hiç kayıt başlığı yok")
            return 2
        güncel = t[:m.start()] + yeni_indeks + "\n\n---\n\n" + t[m.start():]

    if "--kontrol" in argv:
        if eski.strip() == yeni_indeks.strip():
            print("✅ indeks güncel — %d kayıt" % len(kayitlar))
            return 0
        print("🔴 İNDEKS BAYAT — `python arsiv/dogrulama/kayit_indeksi.py` koştur")
        return 1

    KAYIT_DOSYASI.write_text(güncel, encoding="utf-8")
    revize = sum(1 for k, _ in kayitlar if k in SUPERSEDE)
    print("✅ indeks üretildi — %d kayıt · %d revize · %d geçerli"
          % (len(kayitlar), revize, len(kayitlar) - revize))
    return 0


if __name__ == "__main__":        # 🔴 Windows `spawn`
    sys.exit(main(sys.argv[1:]))
