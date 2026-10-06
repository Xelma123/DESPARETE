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
