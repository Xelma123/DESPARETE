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
