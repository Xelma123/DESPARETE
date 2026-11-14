"""Faz 5-2 · anatomi kayıtlarından ek sayılar (simülasyon yok).

Koşudan SONRA yazıldı: karar kuralının girdisi değildir, `sonuc.md` §5'in
("kuraldan sonra görülenler") sayılarını üretir. Kuralın hesabı `sonuc_hesap.py`.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_2_anatomi_2026-11-14/ek_hesap.py
"""
import json
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
KOLLAR = ("desparete", "babel", "en_guvenilir_kahin")
EVRELER = ("once", "acik", "sessiz")
ALANLAR = ("uzak", "girisim", "ed")
SAYAC = {
    "desparete": (
        "protokol.veri_iletilen", "protokol.veri_bekletilen",
        "protokol.tampon_kota_disi", "alan.ardil_degisti",
        "alan.onarima_girdi", "alan.ulasilamaz", "alan.tur_artirildi",
        "komsu.aday_acilan", "komsu.gecis_active", "komsu.gecis_suspect",
        "komsu.gecis_stale", "komsu.gecis_expired",
        "komsu.probe_nitelik", "komsu.probe_olcum", "komsu.probe_hata",
        "komsu.probe_dogrulama", "protokol.probe_alinan",
        "protokol.probe_yaniti_gonderilen",
        "protokol.ilan_gonderilen", "alan.tetik_ilan", "alan.withdrawal",
        "protokol.ilan_alinan", "alan.ilan_kabul", "alan.ilan_aktif_disi",
        "protokol.solicit_gonderilen", "protokol.solicit_yanitlanan",
        "protokol.istek_gonderilen", "politika.caution_girdi"),
    "babel": (
        "hello_gonderilen", "ihu_gonderilen", "dokum_gonderilen",
        "tetik_acil", "tetik_normal", "guncelleme_alinan",
        "uygulanamaz_alinan", "uygulanamaz_yoksayilan", "secim_degisti",
        "sira_istegi_uretilen", "sira_istegi_iletilen", "sira_artirildi",
        "rota_suresi_doldu", "komsu_silindi", "geri_cekme"),
}


def oku(ad):
    sonuc = json.loads((D / f"kayit_{ad}.json").read_text(
        encoding="utf-8"))["sonuc"]
    return {p: sorted((r for r in sonuc if r["protokol"] == p),
                      key=lambda r: r["tohum"]) for p in KOLLAR}


def topla(rs, anahtar):
    c = Counter()
    for r in rs:
        c.update(r.get(anahtar) or {})
    return c


def atlama(ad, kol):
    """Bütün koşu (0–350 s): karar = sonraki atlaması olan veri kararı."""
    print(f"\n== Atlama başına başarısızlık — {ad} (bütün koşu) ==")
    for p, rs in kol.items():
        karar, bas = topla(rs, "karar_bant"), topla(rs, "basarisiz_bant")
        nk, nb = sum(karar.values()), sum(bas.values())
        uretilen = sum(r["uretilen"] for r in rs)
        print(f"  {p:<20} karar/paket {nk / uretilen:.2f} · başarısız/karar "
              f"{nb / nk:.2%} · 'iyi' bağda {bas['iyi'] / karar['iyi']:.2%} · "
              f"orta+kötü bağda "
              f"{(bas['orta'] + bas['kotu']) / max(karar['orta'] + karar['kotu'], 1):.1%}"
              f" (karar {karar['orta'] + karar['kotu']})")
        print("      tohum başına başarısız/karar: " + " · ".join(
            f"{r['tohum']} "
            f"{sum(r['basarisiz_bant'].values()) / sum(r['karar_bant'].values()):.2%}"
            for r in rs))


def evre_olay(kol):
    """Birincil: olayın ANINA göre evre (paketin doğumuna göre değil)."""
    print("\n== Birincil · olay anına göre evre: karar ve düşüş ==")
    for p, rs in kol.items():
        karar, dusen = topla(rs, "evre_alan_karar"), topla(rs, "evre_alan_dusen")
        for e in EVRELER:
            nk = sum(v for k, v in karar.items() if k.startswith(e + "|"))
            s = Counter()
            for k, v in dusen.items():
                sebep, ev, _a = k.split("|")
                if ev == e:
                    s[sebep] += v
            print(f"  {p:<20} {e:<7} karar {nk:>6} · iletim_basarisiz/karar "
                  f"{s['iletim_basarisiz'] / nk:.2%} · düşüş: " + " · ".join(
                      f"{a} {v}" for a, v in s.most_common()))


def alan_pdr(kol):
    """Birincil: paketin geçit dışı ucunun doğum anındaki etki alanına göre."""
    print("\n== Birincil · doğum evresi × paket ucunun alanı: PDR (doğan) ==")
    for p, rs in kol.items():
        c = Counter()
        for r in rs:
            for k, (dogan, teslim) in (r.get("evre_alan_paket") or {}).items():
                c[k, "d"] += dogan
                c[k, "t"] += teslim
        for e in EVRELER:
            print(f"  {p:<20} {e:<7} " + " · ".join(
                f"{a} {c[f'{e}|{a}', 't'] / c[f'{e}|{a}', 'd']:.3f} "
                f"({c[f'{e}|{a}', 'd']})" for a in ALANLAR
                if c[f"{e}|{a}", "d"]))
    # Buradaki alan paketin ucunun değil DÜŞÜŞÜN olduğu yerin alanıdır
    # (iletim_basarisiz'de alıcı, ötekilerde düşüren düğüm); payda o evrede
    # doğan bütün paketlerdir, satırın toplamı sebebin evredeki oranını verir.
    print("\n== Birincil · doğum evresi × düşüşün olduğu alan: evrede doğana "
          "oran ==")
    for p, rs in kol.items():
        dusen = topla(rs, "dogum_evre_dusen")
        for e in ("once", "acik"):
            dogan = sum(r["karistirici_evresi"][e]["dogan"] for r in rs)
            for sebep in ("rota_gecersiz", "iletim_basarisiz"):
                if not any(k.startswith(f"{sebep}|{e}|") for k in dusen):
                    continue
                print(f"  {p:<20} {e:<5} {sebep:<17} " + " · ".join(
                    f"{a} {dusen[f'{sebep}|{e}|{a}'] / dogan:.3f}"
                    for a in ALANLAR))


def sayaclar(ad, kol):
    print(f"\n== Sayaçlar, tohum ortalaması (ağ toplamı, 350 s) — {ad} ==")
    for p, adlar in SAYAC.items():
        rs = kol[p]
        t = Counter()
        for r in rs:
            for a, v in (r.get("teshis_toplam") or {}).items():
                if isinstance(v, (int, float)):
                    t[a] += v
        print(f"  {p}: " + " · ".join(
            f"{a} {t[a] / len(rs):.0f}" for a in adlar))


def main():
    ikiz, birincil = oku("ikiz"), oku("birincil")
    atlama("ikiz", ikiz)
    sayaclar("ikiz", ikiz)
    atlama("birincil", birincil)
    evre_olay(birincil)
    alan_pdr(birincil)
    sayaclar("birincil", birincil)


if __name__ == "__main__":
    main()
