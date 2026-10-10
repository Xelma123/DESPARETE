"""Kayıp anatomisi — etki alanı (29 Eylül 2026, Faz 5.0).

Anlık bölge sessiz evrede her düğümü "uzak" sayar (karıştırıcı 0 W); etki
alanı, karıştırıcı açık olsaydı alınacak ortalama güçle okunur ve sessiz
evrede de karıştırıcının alanını gösterir. Açık evrede ikisi aynı düğümleri
işaretler (fark yalnız hızlı sönümlemeden).
"""


def _birincil_hucre(monkeypatch):
    monkeypatch.setenv("DESPARETE_DUNYA", "referans_2026")
    from kalibrasyon import dunya_secimi as DS
    from sim2.kanal.yayilim import dbm_to_w
    from sim2.kosum.kurulum import kurulum_yap
    kfg = DS.konfig(kol="anatomi", senaryo="formasyon-surekli", tohum=1003,
                    trafik_deseni="yere_toplama",
                    tehdit_senaryosu="derin_sizma")
    return kfg, kurulum_yap(kfg), dbm_to_w(kfg.ed_esigi_dbm)


def test_ETKI_ALANI_sessiz_evrede_karistiricinin_alanini_gosterir(monkeypatch):
    from kalibrasyon.kayip_anatomisi import _bolge, _etki_alani
    kfg, kur, ed_w = _birincil_hucre(monkeypatch)
    kar = kur.kanal.karistirici
    anlar = [kfg.karistirici_baslangic_s + 0.5 * k for k in range(120)]
    t_acik = next(t for t in anlar if kar.devrede_mi(t))
    t_sessiz = next(t for t in anlar if not kar.devrede_mi(t))
    dugumler = range(kfg.dugum_sayisi)

    assert all(_bolge(kur, n, t_sessiz, ed_w) == "uzak" for n in dugumler)
    sessiz = [_etki_alani(kur, n, t_sessiz, ed_w) for n in dugumler]
    assert any(a != "uzak" for a in sessiz)

    acik = [_etki_alani(kur, n, t_acik, ed_w) for n in dugumler]
    anlik = [_bolge(kur, n, t_acik, ed_w) for n in dugumler]
    assert any(a != "uzak" for a in acik)
    uyusan = sum(a == b for a, b in zip(acik, anlik))
    assert uyusan >= 0.8 * len(acik), (acik, anlik)


def test_ETKI_ALANI_karistiricisiz_kolda_uzak(monkeypatch):
    monkeypatch.setenv("DESPARETE_DUNYA", "referans_2026")
    from kalibrasyon import dunya_secimi as DS
    from kalibrasyon.kayip_anatomisi import _etki_alani
    from sim2.kosum.kurulum import kurulum_yap
    kfg = DS.konfig(kol="anatomi", senaryo="statik-yok", tohum=1003,
                    trafik_deseni="yere_toplama")
    kur = kurulum_yap(kfg)
    assert kur.kanal.karistirici is None
    assert _etki_alani(kur, 1, 100.0, 1.0) == "uzak"


def test_DESPARETE_ONARIM_BOLUMLERI_aclik_adaysiz_ve_sonlari():
    """Faz 5.0 teşhisi: onarıma giriş açlık mı (aynı turdan geçerli ama
    uygulanamaz ilan var) adaysız mı; bölüm aynı turda mı yeni turla mı
    kapandı, ulaşılamaz oldu mu. Saf tablo — simülasyon yok."""
    from types import SimpleNamespace

    from kalibrasyon.kayip_anatomisi import (_desparete_onarim_sar,
                                             _onarim_ozeti)
    from protokoller.desparete_alan import AlanTablosu
    from protokoller.desparete_metrik import SONSUZ

    class Dugum:
        def __init__(self, kimlik, aktif):
            self.kimlik, self.aktif = kimlik, set(aktif)

        def aktif_mi(self, j):
            return j in self.aktif

    kur = SimpleNamespace(olaylar=SimpleNamespace(simdi=0.0))
    bolumler: list = []
    from protokoller.desparete import DESPARETE
    asil = (AlanTablosu._onarima_gir, AlanTablosu._ulasilamaz,
            AlanTablosu.yeniden_hesapla, DESPARETE.sonraki_atlama)
    geri = _desparete_onarim_sar(kur, bolumler)
    try:
        d = Dugum(5, (1, 2, 3))
        t = AlanTablosu(d.aktif_mi, lambda j: 16)
        R, W = 0, 1
        t.ilan_al(1, 9, 1, 1, R, 32, 30, 0.0)            # FD 48, ardıl 1
        t.ilan_al(2, 9, 1, 1, R, 48, 30, 0.1)            # uygulanamaz
        kur.olaylar.simdi = 10.0
        t.ilan_al(1, 9, 1, 2, W, SONSUZ, 0, 0.2)         # açlık bölümü
        kur.olaylar.simdi = 11.0
        t.ilan_al(3, 9, 1, 1, R, 47, 30, 0.3)            # aynı turda kurtuldu
        kur.olaylar.simdi = 20.0
        t.ilan_al(3, 9, 1, 2, W, SONSUZ, 0, 0.4)         # yine açlık (2)
        kur.olaylar.simdi = 23.0
        t.ilan_al(2, 9, 2, 1, R, 64, 30, 0.5)            # yeni tur
        d2 = Dugum(6, (1,))
        t2 = AlanTablosu(d2.aktif_mi, lambda j: 16)
        t2.ilan_al(1, 9, 1, 1, R, 32, 30, 0.0)
        kur.olaylar.simdi = 30.0
        t2.ilan_al(1, 9, 1, 2, W, SONSUZ, 0, 1.0)        # adaysız
        t2.zaman(9, 100.0, 0.0)                          # onarım süresi doldu
    finally:
        geri()
    assert (AlanTablosu._onarima_gir, AlanTablosu._ulasilamaz,
            AlanTablosu.yeniden_hesapla, DESPARETE.sonraki_atlama) == asil,         "sarmalayıcı geri alınmadı"
    assert [(b["dugum"], b["aclik"], b.get("son"), b["ulasilamaz"])
            for b in bolumler] == [(5, True, "ayni_tur", False),
                                   (5, True, "yeni_tur", False),
                                   (6, False, None, True)]
    ozet = _onarim_ozeti(bolumler, 0.0, 50.0, 50.0, lambda t: "acik")
    assert ozet["sayim"] == {"acik|aclik|ayni_tur": 1,
                             "acik|aclik|yeni_tur": 1,
                             "acik|adaysiz|kosu_sonu+U": 1}
    assert ozet["sure"]["acik|kosu_sonu+U"] == [20.0, 20.0, 20.0]


def test_DOGUM_EVRESI_dusen_paket_yollari():
    """Faz 5.0 (10 Ekim): düşen paket, düşüşün yoluna göre bulunur."""
    from types import SimpleNamespace as N

    from kalibrasyon.kayip_anatomisi import _dusen_paket
    P = [object() for _ in range(7)]
    kuyruk = N(f_locals={"self": 0, "paket": P[0], "uretim": True},
               f_back=None)
    assert _dusen_paket("kuyruk_tasmasi", 5, kuyruk, {}, {}) is P[0]
    dus = N(f_locals={"sebep": "x"}, f_back=None)
    for s in ("rota_gecersiz", "hedef_yok", "politika"):
        assert _dusen_paket(s, 5, dus, {5: P[1], 6: P[2]}, {}) is P[1]
    assert _dusen_paket("iletim_basarisiz", 5, dus, {5: P[1]},
                        {5: P[3]}) is P[3]
    tasma = N(f_locals={}, f_back=N(f_locals={"paket": P[4], "eski": P[5]}))
    assert _dusen_paket("tampon_asimi", 5, tasma, {}, {}) is P[5]
    suresi = N(f_locals={}, f_back=N(f_locals={"paket": P[4]}))
    assert _dusen_paket("tampon_asimi", 5, suresi, {}, {}) is P[4]
    olay = N(f_locals={}, f_back=N(f_locals={"paket_kimligi": 7, "p": P[6]}))
    assert _dusen_paket("tampon_asimi", 5, olay, {}, {}) is P[6]
    assert _dusen_paket("ttl", 5, suresi, {}, {}) is P[4]
    assert _dusen_paket("dugum_kaybi", 5, suresi, {5: P[1]}, {5: P[3]}) is None


def test_DOGUM_EVRESI_simulatorun_dusus_yollari_degismedi():
    """`_dusen_paket` simülatörün düşüş yollarındaki yerel adlara dayanır;
    bir ad değişirse bu test kırılır (atıf sessizce yanlış paketi bulmasın).
    Sıra "eski" → "p" → "paket": taşma yolunda `eski` düşer, `paket` değil."""
    from sim2.kosum import gonderim, teslim
    from sim2.kosum.dugum import Dugum

    def yerel(f):
        return set(f.__code__.co_varnames)

    assert {"paket", "eski"} <= yerel(Dugum.beklemeye_al)
    assert "p" not in yerel(Dugum.beklemeye_al)
    assert {"paket_kimligi", "p"} <= yerel(Dugum.tampon_suresi_doldu)
    assert "eski" not in yerel(Dugum.tampon_suresi_doldu)
    assert "paket" in yerel(teslim._yerlestir)
    assert not {"eski", "p"} & yerel(teslim._yerlestir)
    assert "paket" in yerel(Dugum.kuyruga_al)
    # Karar düşüşü: kararın sorulduğu baş paket düşer; iletim başarısızlığı:
    # önce uçuştan indirilir, sonra düşer.
    import inspect
    kaynak = inspect.getsource(gonderim)
    assert "d.sonraki_atlama(d.kuyruk.bak()" in kaynak
    vazgec = inspect.getsource(gonderim.vazgec)
    assert vazgec.index("d.ucustan_indir()") < vazgec.index(
        'd.dus("iletim_basarisiz"')


def test_DOGUM_EVRESI_atif_kalan_ve_celiski():
    """Akıbet doğum evresine yazılır; evre başına oranların toplamı 1;
    aynı paket iki kez ya da teslimden sonra düşerse çelişki."""
    from collections import Counter

    from kalibrasyon.kayip_anatomisi import _dogum_evresi, _evre_orani

    def evre(t):
        return "once" if t < 20 else ("acik" if t < 35 else "sessiz")

    kayit = [
        (1, "rota_gecersiz", 36.0, None, (10, 30.0)),     # açıkta doğdu
        (2, "iletim_basarisiz", 31.0, 7, (11, 30.5)),     # alan alıcıda
        (3, "kuyruk_tasmasi", 15.0, None, (12, 15.0)),    # önce
        (4, "dugum_kaybi", 40.0, None, None),             # atfsız
        (5, "ttl", 5.0, None, (13, 5.0)),                 # pencere dışı
    ]
    dusen, atfsiz, celiski = _dogum_evresi(
        kayit, {20, 21}, 10.0, 50.0, evre, lambda d, t: f"a{d}")
    assert dusen == Counter({"rota_gecersiz|acik|a1": 1,
                             "iletim_basarisiz|acik|a7": 1,
                             "kuyruk_tasmasi|once|a3": 1})
    assert atfsiz == Counter({"dugum_kaybi": 1}) and celiski == 0
    _, _, c = _dogum_evresi(
        kayit + [(6, "ttl", 45.0, None, (10, 30.0)),      # iki kez düştü
                 (7, "ttl", 45.0, None, (20, 30.0))],     # teslim edilmişti
        {20, 21}, 10.0, 50.0, evre, lambda d, t: "x")
    assert c == 2
    dogan = Counter({"acik": 10})
    o = _evre_orani(dogan, Counter({"acik": 6}), dusen, "acik")
    assert o["teslim"] == 0.6 and o["rota_gecersiz"] == 0.1
    assert abs(o["kalan"] - 0.2) < 1e-12
    assert abs(sum(o.values()) - 1.0) < 1e-12
