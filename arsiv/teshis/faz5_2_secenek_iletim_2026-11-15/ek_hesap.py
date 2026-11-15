"""Faz 5-2 (b) · ek sayılar — koşudan SONRA yazıldı, karar girdisi değildir.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/ek_hesap.py

Karar kuralının hesabı `sonuc_hesap.py`dedir; burası `sonuc.md` §5'in
("kuraldan sonra görülenler") sayılarını üretir. Simülasyon yok; yalnız
`kayit_taban.json` ve `kayit_secenek.json` okunur.
"""
import math

from sonuc_hesap import AD, D, KOLLAR, T, iletim, oku, pencere, topla

kol, _ = oku([D / "kayit_taban.json", D / "kayit_secenek.json"])
B = "babel"


def kilit(o):
    """Alıcının çerçeveye kilitlendiği pay ve kilitlenince çözme oranı."""
    k = 1.0 - o["alim_red_mesgul"] - o["alim_red_yari_cift"] - o["duyma_disi"]
    return k, o["alim_basarili"] / k


print("== A · alıcıdaki iki aşama (bütün koşu, 4 tohum) ==")
print("  kol     kilitlenme   kilitlenince veri çözüldü   girişimsiz beklenen"
      " g0   gerçek onay kaybı   sayaç 'onay kaybı'")
O_ = {p: iletim(rs) for p, rs in kol.items() if rs}
for p, o in O_.items():
    k, c = kilit(o)
    print(f"  {AD[p]:<6}  {k:.1%}        {c:.1%}                       "
          f"{o['g0']:.3f}                 {o['alim_basarili'] - o['g']:.1%}"
          f"               {o['onay_kaybi']:.1%}")
t, b = O_[T], O_[B]
kt, ct = kilit(t)
kb, cb = kilit(b)
st = t["onbelge+govde"] + (t["alim_basarili"] - t["g"])
sb = b["onbelge+govde"] + (b["alim_basarili"] - b["g"])
et, eb = kt * t["b_d"], kb * b["b_d"]
print(f"  kilitten sonraki başarısızlık (önbelge + gövde + gerçek onay kaybı), "
      f"denemeye oranla: T {st:.1%} · Babel {sb:.1%} · fark {st - sb:+.1%}")
print(f"    bağın kendi kalitesinden beklenen (kilitlenme × b_d): T {et:.1%} · "
      f"Babel {eb:.1%} · fark {et - eb:+.1%}")
print(f"    beklenenin üstü: T {st - et:.1%} · Babel {sb - eb:.1%} · fark "
      f"{(st - et) - (sb - eb):+.1%}")
print(f"    farkın beklenenle açıklanan payı: {(et - eb) / (st - sb):.0%}")

print("\n== B · tohum başına deneme başarısı ve π (T ↔ Babel) ==")
for i, rt in enumerate(kol[T]):
    rb = kol[B][i]
    assert rt["tohum"] == rb["tohum"]
    a, c = iletim([rt]), iletim([rb])
    pi = math.log(a["g0"] / c["g0"]) / math.log(a["g"] / c["g"])
    print(f"  {rt['tohum']}  T g {a['g']:.3f} = {a['g0']:.3f} × "
          f"{a['g'] / a['g0']:.3f} · Babel g {c['g']:.3f} = {c['g0']:.3f} × "
          f"{c['g'] / c['g0']:.3f} · π {pi:.2f} · kilitlenme T "
          f"{kilit(a)[0]:.1%} ↔ Babel {kilit(c)[0]:.1%} · önbelge+gövde T "
          f"{a['onbelge+govde']:.1%} ↔ Babel {c['onbelge+govde']:.1%}")

print("\n== C · en düşük hızdaki denemelerin alıcıdaki sonucu ==")
for p in (T, B, "en_guvenilir_kahin"):
    hz, hh = topla(kol[p], "veri_deneme_hiz"), topla(kol[p], "veri_hedefte_hiz")
    h = min(hz, key=float)
    n = hz[h]
    print(f"  {AD[p]:<6} 1 Mb/s ({n / sum(hz.values()):.1%}): başarılı "
          f"{hh[h + '|alim_basarili'] / n:.1%} · meşgul "
          f"{hh[h + '|alim_red_mesgul'] / n:.1%} · yarı çift "
          f"{hh[h + '|alim_red_yari_cift'] / n:.1%} · önbelge "
          f"{hh[h + '|alim_red_onbelge'] / n:.1%} · gövde "
          f"{hh[h + '|alim_red_per'] / n:.1%}")

print("\n== D · atlama sayısı, kayıp ve kanal yükü (tohum ortalaması) ==")
print("  kol     karar/paket  atlama başarısızlığı  f_a/(1−g)^7  R       İ   "
      "    toplam gönderim  kontrol payı  kilitlenme  k")
for p in KOLLAR:
    rs = kol[p]
    o, w = O_[p], pencere(rs)
    sy, n = topla(rs, "sayaclar"), len(rs)
    gonderim = sum(r["enerji_s"]["enerji_gonderim_s"] for r in rs) / n
    print(f"  {AD[p]:<6}  {o['karar'] / sum(r['uretilen'] for r in rs):.2f}"
          f"         {o['f_a']:.2%}                 "
          f"{o['f_a'] / (1 - o['g']) ** 7:.2f}         {w['R']:.3f}   "
          f"{w['I']:.3f}   {gonderim:6.1f} s         "
          f"{sy['kontrol_airtime_s'] / n / gonderim:.0%}           "
          f"{kilit(o)[0]:.1%}       {o['g'] / o['g0']:.3f}")

print("\n== E · tohum başına: toplam gönderim süresi ↔ kilitlenme ↔ k ==")
for p in KOLLAR:
    print(f"  {AD[p]:<6} " + " · ".join(
        f"{r['tohum']} {r['enerji_s']['enerji_gonderim_s']:.0f} s "
        f"{kilit(iletim([r]))[0]:.1%} {iletim([r])['g'] / iletim([r])['g0']:.3f}"
        for r in kol[p]))

print("\n== F · seçenek kollarında tohum başına ΔR · Δİ (T'ye göre) ==")
for p in KOLLAR[1:4]:
    print(f"  {AD[p]:<3} " + " · ".join(
        f"{r['tohum']} {pencere([r])['R'] - pencere([x])['R']:+.3f} "
        f"{pencere([r])['I'] - pencere([x])['I']:+.3f}"
        for r, x in zip(kol[p], kol[T])))
