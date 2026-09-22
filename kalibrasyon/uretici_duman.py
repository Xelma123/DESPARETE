"""ÜRETİCİ DUMAN KOŞUCUSU — defterin andığı komutlar hâlâ koşuyor mu?

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/uretici_duman.py
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/uretici_duman.py --liste

🔴 NEDEN BU ALET VAR — dört örnek, hepsi 9 Eylül 2026'da bulundu
================================================================
Köken defteri her `OLCULMUS` sayının yanına *"bunu şu komut üretti"* yazar.
Hiçbir kapı o komutun **hâlâ koştuğunu** sormuyordu. Sonuç:

  1. `calisma_noktasi.py` — çalışma noktasının (**1800 m**) üreticisi.
     5 Eylül'de müfreze yarıçapı 250 → 650 m olunca taramanın ilk ızgara
     noktası (1000 m) bir `Konfig` değişmezini çiğnedi ve betik **dört
     gündür** kendi bölüm 2'sinin ilk çağrısında patlıyordu.
  2. `calisma_noktasi.py` (aynı dosya, ikinci kusur) — ölçütü *"30 tohum"*
     diyordu, varsayılanı **6**'ydı. Belgelenen komut, belgelenen sayıyı
     üretmiyordu: 6 tohumla 2000 m, 30 tohumla **1800 m**.
  3. `adim4_sonumleme.py` — `sonumleme_parca_suresi_s` üreticisi. K-102
     Doppler'i tam ölçek hızına bağlamıştı; betik güncellenmedi ve koddaki
     değerin **51 katını** basıyor, farkı hiç açıklamıyordu. Ayrıca sonda
     `KeyError` ile çöküyordu.
  4. `sonumleme_onbellegi.py` — önbellek sınırının zararsızlığını sınayan
     kapı. K-106 sonuç satırına önbelleğin KENDİ durumunu ekleyince
     karşılaştırma **her satırda** `🔴 HAYIR` demeye başladı. Yani doğru
     çalışan bir mekanizmayı kırmızıya boyayan bir yanlış alarm.

🔒 MEVCUT KAPILAR BU SINIFI YAPISAL OLARAK GÖREMİYOR
====================================================
    D11  betiğin **içe aktarılabildiğini** sınar — dördü de içe aktarılabiliyordu
    D15  **terk edilmiş** üretici arar — dördü de terk edilmiş değil, KIRIK
K-110 bu boşluğu bir kez fark edip tek bir betiği (`adim3_kapanis.py`)
onarmıştı; boşluğun kendisi açık kalmıştı. Bu alet onu kapatır.

🔴 BU ALETİN İDDİA ETMEDİĞİ ŞEY — ve bu sınır bağlayıcıdır
==========================================================
Duman koşusu **"betik koşuyor"** der; **"sayıyı yeniden üretti"** DEMEZ.
Bazı üreticiler saatler sürdüğü için burada UCUZ bir kesitle koşarlar ve o
kesit çoğu zaman kaydın sayısını vermez *(örnek: `calisma_noktasi.py` 6
tohumla 2000 m der, kayıttaki 1800 m ise 30 tohumun sonucudur)*.

    duman GEÇTİ  →  komut çalışıyor, çıkış kodu 0
    duman KALDI  →  kayıt bir HAYALETİ gösteriyor, sayı yeniden üretilemez

🔒 Bu yüzden her satır kendi kesitini ve **tam koşumun bandını** yazar.
Mühürden önce tam koşumlar ayrıca yapılır; duman onların yerine geçmez.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.yapilandirma.kokenler import KOKENLER, MODUL_KOKENLERI  # noqa: E402

__all__ = ["DUMAN_KESITI", "anilan_ureticiler", "kos"]

# 🔒 HER ÜRETİCİ İÇİN UCUZ KESİT — ve tam koşumun bandı.
# Bir betik buraya yazılmadan duman koşusuna giremez: "varsayılan olarak
# tamamını koştur" demek, saatler süren betikleri her denetimde koşturmak
# olurdu ve alet kullanılmaz hâle gelirdi (kimsenin koşmadığı bir kapı,
# kapı değildir — bu dosyanın 4 numaralı bulgusu tam olarak budur).
DUMAN_KESITI: dict[str, tuple[list[str], str, str]] = {
    #  betik                    argüman            kesit           tam koşum
    "adim4_kapanis.py":       ([],                "tamamı",       "BANT 2–6 dk"),
    "adim4_sonumleme.py":     ([],                "tamamı",       "BANT 2–6 dk"),
    "bag_kumesi.py":          (["a"],             "yalnız kapılar (a)",
                                                                  "BANT saatler"),
    # 🔴 15 Eylul 2026: kesit DARALTILDI. Onceki hali dort bolumu de
    # kosturuyordu ve "ucuz kesit" sozlesmesini ciginiyordu — olculdu:
    # `zaman_ve_kol` 2 tohumla bile 7 dk+, `gorev_kolu` C5'in saatler
    # suren olcumu. Duman kapisinin isi "hala kosuyor mu", "olcumu
    # yeniden yap" degil.
    # ⚠️ BEYAN: `zaman_ve_kol` ve `gorev_kolu` duman kapsaminda DEGIL;
    # onlarin kapisi kendi kosumlaridir (`12` §3 C5).
    "calisma_noktasi.py":     (["--bolum", "yaricaplar,alan_taramasi",
                                "--tohum", "6"],
                                                  "iki ucuz bölüm — SAYIYI ÜRETMEZ",
                                                                  "BANT 25–35 dk"),
    "calkanti.py":            ([],                "tamamı",       "BANT 3–10 dk"),
    "cozunurluk.py":          ([],                "tamamı",       "BANT 5–20 dk"),
    "duyarlilik.py":          (["statik", "cw_min"],
                                                  "tek parametre — TARAMA DEĞİL",
                                                                  "BANT saatler"),
    "karistirici_gucu.py":    (["tarama"],        "tamamı",       "BANT 10–25 dk"),
    # 🔴 15 Eylul 2026'da EKLENDI — bu dordu defterde ANILIYOR ama kesitleri
    # tanimli degildi ve kapsam kapisi SESSIZ kaliyordu. Uc tanesi 14 Eylul'un
    # yapi adimlarindan, biri 15 Eylul'un kalibrasyonundan geldi.
    "anlamlilik_sabitleri.py": ([],               "tamamı — zaten bir kapı",
                                                                  "BANT < 5 dk"),
    # 🔴 17 Eylul 2026'da EKLENDI (K-136). Kesit KISA PENCERE kosar ve
    # SAYIYI URETMEZ: tam pencerede tek bir (AODV, kahin) cifti 505 s
    # suruyor, yani tam kosum bu defterde yeri olmayacak kadar pahali.
    "aodv_uygunluk.py":       (["duman"],         "tek kol × tek tohum × KISA PENCERE — SAYIYI ÜRETMEZ",
                                                                  "BANT 3,5–4,5 saat"),
    "dugum_sayisi.py":        ([],                "tamamı",       "BANT 5–15 dk"),
    "theta_kollari.py":       ([],                "tamamı",       "BANT 2–5 dk"),
    "yere_toplama_yuku.py":   (["duman"],         "tek hız × tek tohum — SAYIYI ÜRETMEZ",
                                                                  "BANT 25–35 dk"),
    "sonumleme_onbellegi.py": (["2"],             "yalnız bölüm 2",
                                                                  "BANT 30–40 dk"),
}

_KAL = re.compile(r"kalibrasyon/([a-z0-9_]+\.py)")


def anilan_ureticiler() -> dict[str, set[str]]:
    """Defterin andığı her betik → onu anan kovaların kümesi."""
    bulunan: dict[str, set[str]] = {}
    for defter in (KOKENLER, MODUL_KOKENLERI):
        for ad, (kova, gerekce) in defter.items():
            for m in _KAL.finditer(gerekce):
                bulunan.setdefault(m.group(1), set()).add(kova)
    return bulunan


def kos(betik: str, argv: list[str], zaman_asimi_s: float
        ) -> tuple[int | None, float, str]:
    """Betiği koştur; (çıkış kodu, süre, son satır) döndür."""
    t0 = time.perf_counter()
    try:
        p = subprocess.run(
            [sys.executable, "-u", str(KOK / "kalibrasyon" / betik), *argv],
            cwd=str(KOK), capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=zaman_asimi_s,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    except subprocess.TimeoutExpired:
        return None, time.perf_counter() - t0, "ZAMAN ASIMI"
    sure = time.perf_counter() - t0
    if p.returncode == 0:
        return 0, sure, ""
    # Çıkış kodu 0 değilse SEBEBİ taşı — "kaldı" tek başına teşhis değildir.
    satirlar = [s for s in (p.stderr or p.stdout).strip().splitlines() if s]
    return p.returncode, sure, (satirlar[-1] if satirlar else "(çıktı yok)")


def kendi_kapisi() -> bool:
    """🔒 ALETİN KENDİ KAPISI — `bag_kumesi.py a` ile aynı idiom.

    K-103'ün dersi: *"kapı eklendiğinde sorulacak soru 'ne kırıldı' değil,
    'ne hâlâ geçiyor ama artık hiçbir şey doğrulamıyor'dur."* Ateş etmeyen
    bir kapı, kapı değildir. Dört dalın dördü de burada sınanır.
    """
    print("=" * 78)
    print("K - KAPININ KENDI SINAVI  (ates ediyor mu)")
    print("=" * 78)
    tamam = True

    kod, sure, son = kos("bag_kumesi.py", ["zzz"], 120.0)
    ok = kod not in (0, None)
    tamam &= ok
    print(f"  1) kirik kosum yakalaniyor mu  : cikis {kod} "
          f"({sure:.1f} s)  {'OK' if ok else '🔴 GECIRDI'}")
    if son:
        print(f"     sebep tasiniyor mu          : {son[:60]!r}")

    kod2, sure2, _ = kos("uretici_duman.py", ["--liste"], 120.0)
    ok2 = kod2 == 0
    tamam &= ok2
    print(f"  2) saglam betik geciyor mu     : cikis {kod2} "
          f"({sure2:.1f} s)  {'OK' if ok2 else '🔴 YANLIS ALARM'}")

    anilan = anilan_ureticiler()
    bir = next(iter(sorted(anilan)))
    sahte = {k: v for k, v in DUMAN_KESITI.items() if k != bir}
    eksik = sorted(set(anilan) - set(sahte))
    ok3 = eksik == [bir]
    tamam &= ok3
    print(f"  3) kapsam kapisi konusuyor mu  : {eksik}  "
          f"{'OK' if ok3 else '🔴 SESSIZ'}")

    ok4 = not (KOK / "kalibrasyon" / "olmayan_betik.py").exists()
    tamam &= ok4
    print(f"  4) olmayan dosya goruluyor mu  : {'OK' if ok4 else '🔴'}")

    print()
    print("  🟢 KAPI ATES EDIYOR." if tamam
          else "  🔴 KAPI BOS GECIYOR — duman kosusu KOSULMAZ.")
    return bool(tamam)


def main() -> None:
    zaman_asimi_s = 1800.0
    anilan = anilan_ureticiler()
    yalniz_liste = "--liste" in sys.argv
    if "--kapi" in sys.argv:
        raise SystemExit(0 if kendi_kapisi() else 1)

    print("=" * 78)
    print("URETICI DUMAN KOSUCUSU — defterin andigi komutlar kosuyor mu?")
    print("=" * 78)
    print(f"  defterin andigi betik : {len(anilan)}")
    print(f"  duman kesiti tanimli  : {len(DUMAN_KESITI)}")

    # 🔴 KAPSAM KAPISI — defterin andigi ama kesiti tanimlanmamis bir betik
    # sessizce atlanamaz. K-109'un dersi: bir denetimin kapsami, denetledigi
    # defterin kapsamindan DAR olamaz.
    eksik = sorted(set(anilan) - set(DUMAN_KESITI))
    fazla = sorted(set(DUMAN_KESITI) - set(anilan))
    yok = sorted(b for b in DUMAN_KESITI
                 if not (KOK / "kalibrasyon" / b).exists())
    if eksik:
        print(f"  🔴 KESITI TANIMLANMAMIS   : {eksik}")
    if fazla:
        print(f"  ⚠️ defterde ANILMAYAN     : {fazla} (kesit tanimli ama "
              f"hicbir kayit gostermiyor)")
    if yok:
        print(f"  🔴 DOSYASI YOK            : {yok}")
    print()

    if yalniz_liste:
        print(f"  {'betik':<26} {'kesit':<32} {'tam kosum':<14} kovalar")
        for b in sorted(DUMAN_KESITI):
            _, kesit, bant = DUMAN_KESITI[b]
            print(f"  {b:<26} {kesit:<32} {bant:<14} "
                  f"{','.join(sorted(anilan.get(b, {'-'})))}")
        return

    # 🔒 Olculdu (10 Eylul 2026, tam kosum): 45,6 dk. Betik basina:
    # calisma_noktasi 1008 s · cozunurluk 539 · sonumleme_onbellegi 479 ·
    # karistirici_gucu 341 · duyarlilik 264 · adim4_kapanis 24 · gerisi <10.
    print(f"  ⚠️ zaman asimi: {zaman_asimi_s/60:.0f} dk/betik. "
          f"Tamami BANT 40–60 dk (olculdu: 45,6 dk).")
    print()
    print(f"  {'betik':<26} {'kesit':<32} {'sure_s':>8} {'sonuc':>10}")
    kalan = []
    for betik in sorted(DUMAN_KESITI):
        argv, kesit, _bant = DUMAN_KESITI[betik]
        kod, sure, son = kos(betik, argv, zaman_asimi_s)
        sonuc = "GECTI" if kod == 0 else "🔴 KALDI"
        print(f"  {betik:<26} {kesit:<32} {sure:>8.1f} {sonuc:>10}")
        if kod != 0:
            kalan.append((betik, kod, son))

    print()
    print("=" * 78)
    if kalan:
        print(f"🔴 {len(kalan)} URETICI KOSMUYOR — kayitlari bir HAYALETI "
              f"gosteriyor:")
        for betik, kod, son in kalan:
            print(f"   · {betik}  (cikis {kod})")
            print(f"       {son[:110]}")
        raise SystemExit(1)
    print("🟢 Defterin andigi her uretici kosuyor (ucuz kesitleriyle).")
    print("⚠️ Bu 'sayilar yeniden uretildi' DEMEK DEGILDIR — ustteki")
    print("   basligin 'IDDIA ETMEDIGI SEY' bolumune bak.")


if __name__ == "__main__":
    main()
