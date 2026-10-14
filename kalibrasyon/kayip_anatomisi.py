"""
KAYIP ANATOMİSİ — Faz 5.0 (`v2/12`, plan) · K-189 · genişletme K-193.

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/kayip_anatomisi.py \
        --dunya referans_2026 [--kol formasyon] [--aile derin_sizma] \
        [--sinif surekli|yok] \
        [--protokoller aodv,olsrv2,jarmrout,desparete,en_guvenilir_kahin] \
        [--tohumlar 1003,1004,1005] [--kisa] [--isci 8] [--kayit <yol.json>]

    Kol başına konfig farkı (K-198): `aodv@rota_tamponu_kapasitesi=256`,
    birden çoğu `+` ile (`…=256+rota_tamponu_omru_s=60`); sonuç tam etiketle.

🔒 SORU: paket NEREDE ve NEDEN ölüyor? Her düşüş, karıştırıcının o düğüme
ulaşan gücüne göre üç BÖLGEYE ayrılır:

    ed       ≥ ED eşiği (−76 dBm)  — verici kanalı alamaz: KANAL ERİŞİM KİLİDİ
    girisim  ≥ gürültü tabanı       — alıcıda SINR kaybı
    uzak     <  gürültü tabanı       — karıştırıcıdan bağımsız (rota, yük, bağ)

× düşme sebebi (korunum defterinin kapalı kümesi). Kâhin (ETX, aynı kanal)
ile protokol arasındaki PDR farkı KÖRLÜĞÜN BEDELİDİR; DESPARETE'nin Faz 5
hedefleri buradan çıkar.

🔴 K-193 · BÖLGE KİMİN KONUMUNDA OKUNUR: `iletim_basarisiz`i gönderen
düşürür, ama karıştırılan çoğu zaman ALICIDIR (SINR kaybı alıcıda). İlk
sürüm her düşüşü düştüğü düğümde sınıflıyordu; alıcı tarafı karıştırma
"uzak" görünebilirdi. Artık `iletim_basarisiz`in bölgesi DENENEN SONRAKİ
ATLAMANIN konumunda okunur (gönderenin bölgesi ayrıca sayılır); öteki
sebepler (kuyruk taşması = ED kilidinde susan verici, vb.) düştüğü düğümde.

🔒 K-193 · BAĞ KALİTESİ: protokolün her veri kararında seçtiği bağ ve
başarısız olduğu bağ, kâhinin AYNI bağ ölçüsüyle (tek deneme başarısı:
sönümleme ve karıştırıcı dâhil, girişim hariç, ARF tabanında) bantlanır:
`p_atlama = 1 − (1 − p)^(deneme sınırı + 1)` ≥ 0,90 · 0,50–0,90 · < 0,50.
"Protokol kötü bağı SEÇİYOR" (mekanizma) ile "iyi bağda başarısız oluyor"
(girişim, gizli uç, kusur) buradan ayrılır. Statik ve karıştırıcısız kolda
bağ kalitesi sabittir; öteki kollarda karar anının 5 s'lik diliminde okunur.

🔒 K-197 · KARIŞTIRICININ AÇIK / SESSİZ EVRESİ: çizelgeli karıştırıcıda
(`derin_sizma`: 15 s açık · 15 s sessiz) paketler DOĞUM anına, düşüşler
düştüğü ana göre `once` (açılmadan önce) · `acik` · `sessiz` diye ayrılır.
Sessiz evrede PDR'nin temize dönüp dönmediği protokolün çizelgeye zamansal
uyumudur — birincil hücrenin sınadığı şey (K-192 §4).

🔒 29 Eylül · ETKİ ALANI (Faz 5.0; K-200'ün alet sınırı): yukarıdaki bölge
ANLIK güçle okunur — sessiz evrede karıştırıcı 0 W yayar ve her düşüş "uzak"
sayılır; bölge tablosu karıştırıcının etki alanını değil çoğunlukla sessizliği
gösteriyordu. Etki alanı, karıştırıcı o anda AÇIK olsaydı düğümün alacağı
ORTALAMA güçtür — yavaş kayıp (yol kaybı + gölgeleme + yer–hava), açık/sessiz
kapısı ve hızlı sönümleme hariç — ve aynı eşiklerle `ed · girisim · uzak`
diye ayrılır. Karıştırıcının o anki konumu kullanılır (sessizken taşınan
araç). Evre × alan üç tabloda: paketlerin teslimi (paketin GEÇİT DIŞI ucunun
doğumdaki alanı: telemetride kaynak, komutta hedef), veri kararlarının payı
(seçilen sonraki atlamanın alanı) ve düşüşler (bölgeyle aynı düğüm kuralı).
Açık evrede `ed` alanındaki PDR ile sessiz evredeki aynı alanın PDR'si,
karıştırıcının o alandaki etkisini ve protokolün sessizlikte toparlanmasını
birlikte gösterir.

🔒 29 Eylül · DESPARETE ONARIM BÖLÜMLERİ (Faz 5.0): iletilebilir bir alan
ardılını yitirip onarıma girdiği her an bir BÖLÜM açar; alan yeniden
iletilebilir olunca kapanır. Girişte sorulan: protokolün KENDİ açlık
tanımı (`AlanTablosu.aclik_mi`: aynı turdan geçerli, sonlu ilanı olan ACTIVE
bir komşu var ve hiçbiri uygulanabilir değil, P ≥ FD) — "açlık"; değilse
"adaysız". 🔴 DD-11 (K-242): alet önce kendi tanımını kullanıyordu (ardıl
hariç, uygulanabilirliğe bakmadan); ölçümü olmayan uygulanabilir komşuyu
açlık, potansiyeli yükselen ardılı adaysız sayıyordu. Faz 5.0'ın "%64
açlık" payı o tanımla ölçülmüştü. Bölümün sonu: aynı turda kurtuldu · yeni turla (DFSN arttı)
kurtuldu · koşu sonuna kadar kurtulmadı; arada ulaşılamaz olduysa `+U`.
Karıştırıcının evresi bölümün başladığı an. Ayrıca her `rota_gecersiz`
düşüşünde alanın durumu (onarımda: tampon kotası dolu · ulaşılamaz) × evre
sayılır — kaybın bölümün UZUNLUĞUNDAN mı kotadan mı geldiğini ayırır.
Yalnız sayar, davranış aynı.

🔒 10 Ekim · DOĞUM EVRESİ (Faz 5.0): birincil metrik `PDR_açık` (K-222)
paketin DOĞDUĞU evreye göredir; düşüş başka evrede olabilir (onarımda ya da
tamponda bekleyen paket). Her düşüşün paketi bulunur (`_dusen_paket`) ve
pencerede doğan paketin akıbeti doğduğu evreye yazılır: evre evre
`doğan = teslim + Σ düşen + kalan`. Açık − önce farkı (aynı koşu; ikizde
açık ≈ önce, G1ç) karıştırmaya özgü kaybı sebeplere TAM ayırır. Aynı paket
iki kez akıbet bulursa (çelişki) ya da `dugum_kaybi` dışında paketi
bulunamayan düşüş olursa rapor işaretler; açık evre PDR'si satırın
`pdr_acik`ıyla çapraz denetlenir.

🔒 K-193 · TOHUM BAŞINA: sonuçlar tohum başına da basılır; tohumlar tek
çağrıda paralel koşar (eskiden ayrı ayrı koşuluyordu çünkü toplanıyordu).

🔒 SİMÜLATÖR DEĞİŞMEZ: düğümün `_kayip_yeri`, `sonraki_atlama` ve
`ucustan_indir` yöntemleri bu işçi sürecinde SARILIR (davranış aynı; yalnız
kayıt). Kaydedilen düşüş sayısı korunum defterinin toplamına EŞİT olmak
zorundadır; değilse bir yol kancayı atlıyordur ve araç patlar. OLSR'da §13
bildirimi ve §14.3'ün onu geri alışı da sarılarak ölçülür (davranış aynı).

⚠️ Ana deney tohumları (2000–2039) KOŞULMAZ — varsayılan geliştirme
tohumları 1003–1005 (`v2/12` Faz 5).
"""

from __future__ import annotations

import json
import statistics as ist
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from sim2.cekirdek.degismezler import dogrula  # noqa: E402

BOLGELER = ("ed", "girisim", "uzak")
# Bağ kalitesi bantları — kâhinin `ATLAMA_ESIGI`yle (0,90) aynı üst sınır.
BANTLAR = ("iyi", "orta", "kotu")
# Karar bağlarının hareketli/karıştırıcılı kolda örneklendiği dilim (s).
BAG_DILIMI_S = 5.0


def _bolge(kur, dugum: int, t_s: float, ed_w: float) -> str:
    kar = kur.kanal.karistirici
    if kar is None:
        return "uzak"
    p = kar.alinan_guc_w(dugum, kur.topoloji.konum(dugum, t_s), t_s)
    if p >= ed_w:
        return "ed"
    if p >= kur.kanal.yayilim.gurultu_w:
        return "girisim"
    return "uzak"


def _etki_alani(kur, dugum: int, t_s: float, ed_w: float) -> str:
    """Karıştırıcı `t`de AÇIK olsaydı düğümün alacağı ORTALAMA güce göre
    bölge — yavaş kayıp, kapı ve hızlı sönümleme hariç (29 Eylül)."""
    kar = kur.kanal.karistirici
    if kar is None:
        return "uzak"
    konum = kur.topoloji.konum(dugum, t_s)
    p = sum(u.tepe_w / 10.0 ** (u._kayip_db(dugum, konum, t_s) / 10.0)
            for u in getattr(kar, "uyeler", (kar,)))
    if p >= ed_w:
        return "ed"
    if p >= kur.kanal.yayilim.gurultu_w:
        return "girisim"
    return "uzak"


def _bant(p_atlama: float) -> str:
    return "iyi" if p_atlama >= 0.90 else ("orta" if p_atlama >= 0.50
                                          else "kotu")


def _rota_bosalmasi(olsr, gozlem, kayit: dict) -> None:
    """K-193 · OLSR geçide rotasızken (`rota_gecersiz`) düğümün KENDİ
    bilgisinde yol var mı? Düz genişlik-öncelikli arama: ben → simetrik
    komşular · 2-atlama kümesi (simetrik komşunun HELLO'su) · topoloji
    kümesi (TC). RFC §10 topoloji girdisini ancak son atlaması ≥ 2 atlamada
    olan hedefe uygular (h = 2'den başlar); düz arama bu kısıtı tanımaz —
    fark, rotasızlığın RFC'nin kuralından mı bilgi yokluğundan mı geldiğini
    ayırır. Yalnız ölçüm; karar değişmez."""
    simdi = float(gozlem.saat_s)
    hedef = gozlem.paket.hedef
    sym = olsr._simetrik_komsular(simdi)
    kayit["rg_karar"] += 1
    if not sym:
        kayit["rg_sym_yok"] += 1
    if hedef in olsr._bag:
        kayit["rg_hedef_bagda"] += 1
    komsu: dict[int, set[int]] = {olsr.kimlik: set(sym)}
    for (n, z), t in olsr._iki.items():
        if t >= simdi and n in sym and z != olsr.kimlik:
            komsu.setdefault(n, set()).add(z)
    for (d, son), (_s, t) in olsr._topoloji.items():
        if t >= simdi and d != olsr.kimlik:
            komsu.setdefault(son, set()).add(d)
    uzak = {olsr.kimlik: 0}
    sira = [olsr.kimlik]
    while sira:
        u = sira.pop(0)
        for v in komsu.get(u, ()):
            if v not in uzak:
                uzak[v] = uzak[u] + 1
                sira.append(v)
    if hedef in uzak:
        kayit["rg_duz_yol_var"] += 1
        kayit["rg_duz_yol_atlama"].append(uzak[hedef])


def _olsr_s13_sar(kayit: dict):
    """OLSR'ın §13 bildirimini ve §14.3'ün onu geri alışını sayar.

    Döner: geri alma fonksiyonu (asıl yöntemleri geri koyar).
    Ölçülen: §13 anı → aynı bağın `L_LOST_LINK_time`ının süresi dolmadan
    SIFIRLANDIĞI an (kalite eşiği aştı); sıfırlamanın süpürmede mi (yeni
    paket gelmeden) yoksa paket alımında mı olduğu.
    """
    from protokoller import olsr as O
    sinif = O.OLSR
    asil_bas = sinif.iletim_basarisiz
    asil_esik = sinif._histerezis_esik
    asil_ses = sinif._histerezis_sessizlik
    asil_karar = sinif.sonraki_atlama
    durum = {"supurme": False}
    bekleyen: dict[tuple[int, int], float] = {}

    def sonraki_atlama(self, gozlem):
        # K-146 K1 · BAYAT ROTA: seçilen sonraki atlama o anda simetrik mi?
        karar = asil_karar(self, gozlem)
        if gozlem.paket is not None and karar.sonraki is not None:
            kayit["karar"] += 1
            if not self._simetrik_mi(karar.sonraki, float(gozlem.saat_s)):
                kayit["simetriksiz_karar"] += 1
        elif (gozlem.paket is not None
              and any(b.tip == "rota_gecersiz" for b in karar.beyan)):
            _rota_bosalmasi(self, gozlem, kayit)
        return karar

    def iletim_basarisiz(self, gozlem, hedef, tur):
        sonuc = asil_bas(self, gozlem, hedef, tur)
        # K-196: §13 kapalıysa (varsayılan) bildirim yok, sayılmaz
        if getattr(self, "_s13", True) and hedef is not None                 and hedef in self._bag:
            simdi = float(gozlem.saat_s)
            bekleyen[(self.kimlik, hedef)] = simdi
            kayit["s13"] += 1
        return sonuc

    def _histerezis_sessizlik(self, simdi_s):
        durum["supurme"] = True
        try:
            return asil_ses(self, simdi_s)
        finally:
            durum["supurme"] = False

    def _histerezis_esik(self, ni, simdi_s):
        h = self._hist.get(ni)
        once = h is not None and h.kayip_bitis >= simdi_s
        sonuc = asil_esik(self, ni, simdi_s)
        anahtar = (self.kimlik, ni)
        if once and h.kayip_bitis < simdi_s and anahtar in bekleyen:
            gecen = simdi_s - bekleyen.pop(anahtar)
            kayit["geri_alinan"] += 1
            kayit["geri_supurmede" if durum["supurme"]
                  else "geri_pakette"] += 1
            kayit["geri_sure_s"].append(round(gecen, 3))
        return sonuc

    sinif.iletim_basarisiz = iletim_basarisiz
    sinif._histerezis_sessizlik = _histerezis_sessizlik
    sinif._histerezis_esik = _histerezis_esik
    sinif.sonraki_atlama = sonraki_atlama

    def geri():
        sinif.iletim_basarisiz = asil_bas
        sinif._histerezis_sessizlik = asil_ses
        sinif._histerezis_esik = asil_esik
        sinif.sonraki_atlama = asil_karar
    return geri


def _desparete_onarim_sar(kur, bolumler: list, rg: Counter | None = None,
                          evre_adi=None, pencere=(0.0, float("inf"))):
    """DESPARETE alanlarının onarım bölümlerini `bolumler`e, verildiyse
    `rota_gecersiz` düşüşlerini `rg`ye (`evre|alan durumu`) yazar.

    Döner: geri alma fonksiyonu. Zaman simülatörün saatidir (düğüm saati
    ofsetli). Düğüm kimliği tablonun `_aktif_mi` bağlı yönteminden.
    """
    from protokoller.desparete_alan import (FORWARDABLE, REPAIRING,
                                            UNREACHABLE, AlanTablosu)
    from protokoller.desparete_bicim import DURUM_REACHABLE

    asil_gir = AlanTablosu._onarima_gir
    asil_ulas = AlanTablosu._ulasilamaz
    asil_hesap = AlanTablosu.yeniden_hesapla
    acik: dict[tuple[int, int], dict] = {}

    def _dugum(tablo) -> int:
        return tablo._aktif_mi.__self__.kimlik

    def _onarima_gir(self, a, t):
        sonlu = [j for j, i in a.ilanlar.items()
                 if j != a.ardil and self._aktif_mi(j)
                 and i.durum == DURUM_REACHABLE and i.bitis > t
                 and i.dfsn == a.dfsn]
        b = {"dugum": _dugum(self), "hedef": a.hedef,
             "bas": kur.olaylar.simdi, "dfsn": a.dfsn,
             "aclik": self.aclik_mi(a.hedef, t), "sonlu": len(sonlu),
             "ulasilamaz": False}
        acik[(b["dugum"], a.hedef)] = b
        bolumler.append(b)
        return asil_gir(self, a, t)

    def _ulasilamaz(self, a):
        b = acik.get((_dugum(self), a.hedef))
        if b is not None:
            b["ulasilamaz"] = True
        return asil_ulas(self, a)

    def yeniden_hesapla(self, hedef, t):
        a = self.alanlar.get(hedef)
        once = None if a is None else a.durum
        sonuc = asil_hesap(self, hedef, t)
        if (a is not None and once in (REPAIRING, UNREACHABLE)
                and a.durum == FORWARDABLE):
            b = acik.pop((_dugum(self), hedef), None)
            if b is not None:
                b["son"] = "ayni_tur" if a.dfsn == b["dfsn"] else "yeni_tur"
                b["t_son"] = kur.olaylar.simdi
        return sonuc

    from protokoller.desparete import DESPARETE
    asil_karar = DESPARETE.sonraki_atlama

    def sonraki_atlama(self, gozlem):
        karar = asil_karar(self, gozlem)
        p = gozlem.paket
        if (rg is not None and p is not None and karar.sonraki is None
                and pencere[0] <= kur.olaylar.simdi < pencere[1]
                and not karar.beklet
                and any(b.tip == "rota_gecersiz" for b in karar.beyan)):
            rg[f"{evre_adi(kur.olaylar.simdi)}|"
               f"{self.alanlar.durum(p.hedef)}"] += 1
        return karar

    AlanTablosu._onarima_gir = _onarima_gir
    AlanTablosu._ulasilamaz = _ulasilamaz
    AlanTablosu.yeniden_hesapla = yeniden_hesapla
    DESPARETE.sonraki_atlama = sonraki_atlama

    def geri():
        AlanTablosu._onarima_gir = asil_gir
        AlanTablosu._ulasilamaz = asil_ulas
        AlanTablosu.yeniden_hesapla = asil_hesap
        DESPARETE.sonraki_atlama = asil_karar
    return geri


def _onarim_ozeti(bolumler: list, bas: float, bitis: float, kosu_sonu: float,
                  evre_adi) -> dict:
    """Ölçüm penceresinde BAŞLAYAN bölümler: `evre|giriş|son` sayımı ve
    `evre|son` süreleri (p50 · p90 · toplam düğüm-saniye)."""
    sayim: Counter = Counter()
    sure: dict[str, list[float]] = {}
    for b in bolumler:
        if not bas <= b["bas"] < bitis:
            continue
        son = b.get("son", "kosu_sonu") + ("+U" if b["ulasilamaz"] else "")
        e = evre_adi(b["bas"])
        sayim[f"{e}|{'aclik' if b['aclik'] else 'adaysiz'}|{son}"] += 1
        sure.setdefault(f"{e}|{son}", []).append(
            b.get("t_son", kosu_sonu) - b["bas"])
    return {"sayim": dict(sayim),
            "sure": {k: [round(ist.median(v), 2),
                         round(sorted(v)[int(0.9 * (len(v) - 1))], 2),
                         round(sum(v), 1)] for k, v in sure.items()}}


def _olsr_s13():
    """🔒 YALNIZ TEŞHİS KOLU (K-196): §13 AÇIK OLSR — `OLSR-b`, K-147'nin
    istisnası. K-196'dan beri taban OLSR §13'süz; bu kol K-193'ün
    karşılaştırmasını yeniden üretmek içindir."""
    from functools import partial

    from protokoller.olsr import OLSR
    return partial(OLSR, s13=True)


def _olsr_s13siz():
    """🔒 YALNIZ TEŞHİS KOLU (K-146 N1'in tersi): §13 bağ katmanı bildirimi
    KAPALI OLSR — `OLSR-a`nın davranışı. Taban protokol değildir; §13'ün
    referans dünyadaki nedensel payını ölçmek içindir. K-196'dan beri taban
    `olsr` ile AYNI davranış (K-193 komutları yeniden üretilebilsin diye
    duruyor)."""
    from protokoller.olsr import OLSR

    class OLSRS13siz(OLSR):
        def iletim_basarisiz(self, gozlem, hedef, tur):
            return ()
    return OLSRS13siz


def _olsr_2atlama_lsym():
    """🔒 YALNIZ TEŞHİS KOLU (K-193): 2-atlama kümesi (§8.2.1) RFC'nin
    HARFİYEN koşuluyla güncellenir — HELLO'nun göndereniyle bağ demetinin
    `L_SYM_time`ı dolmamışsa. §14.2 histerezisli simetri tanımını yalnız
    komşu durumu, MPR ve rota hesabının ilk adımı için ister ve *"Apart from
    the above, what has been described previously does not interfere"* der.
    K-223'ten (`OLSR-d`) beri taban `olsr` ile AYNI davranış — K-193
    komutları yeniden üretilebilsin diye duruyor."""
    from protokoller.olsr import OLSR

    class OLSR2AtlamaLsym(OLSR):
        def _hello_isle(self, ni, y, gecerlilik, simdi_s):
            self._lsym_kipi = True
            try:
                return super()._hello_isle(ni, y, gecerlilik, simdi_s)
            finally:
                self._lsym_kipi = False

        def _simetrik_mi(self, n, simdi_s):
            if getattr(self, "_lsym_kipi", False):
                b = self._bag.get(n)
                return (b is not None and b.bitis >= simdi_s
                        and b.sym_bitis >= simdi_s)
            return super()._simetrik_mi(n, simdi_s)
    return OLSR2AtlamaLsym


def _is_guvenli(is_) -> dict:
    """`_is`in hatası yalnız o koşuyu düşürür (K-198) — uzun partide tek
    bir işçinin istisnası bütün sonuçları kaybettirmesin."""
    import traceback
    try:
        return _is(is_)
    except Exception as hata:                               # noqa: BLE001
        return {"protokol": is_[0], "tohum": is_[1],
                "hata": f"{type(hata).__name__}: {hata}",
                "iz": traceback.format_exc()[-2000:]}


def _konfig_farklari(metin: str) -> dict:
    """`ad=değer+ad=değer` → Konfig alanları; tip alanın bildiriminden."""
    from sim2.yapilandirma.konfig import Konfig

    alanlar = Konfig.__dataclass_fields__
    cikti: dict = {}
    for parca in filter(None, metin.split("+")):
        ad, _, deger = parca.partition("=")
        dogrula(ad in alanlar, f"bilinmeyen Konfig alanı: {ad!r}")
        tip = str(alanlar[ad].type)
        if tip.startswith("bool"):
            cikti[ad] = deger in ("1", "true", "True", "evet")
        elif tip.startswith("int"):
            cikti[ad] = int(deger)
        elif tip.startswith("float"):
            cikti[ad] = float(deger)
        else:
            cikti[ad] = deger
    return cikti


# DOĞUM EVRESİ (10 Ekim, baştaki açıklama): simülatör düşen paketi
# `_kayip_yeri`ne vermez — davranışa dokunmadan yol yol bulunur.
_KARAR_DUSUSU = ("rota_gecersiz", "hedef_yok", "politika")


def _dusen_paket(sebep: str, dugum: int, cagiran, son_karar: dict,
                 son_ucus: dict):
    """`_kayip_yeri`ni doğuran düşüşün paketi; bulunamazsa `None`.

      kuyruk_tasmasi       `kuyruga_al`ın `paket`i (`cagiran`)
      rota_gecersiz · hedef_yok · politika
                           düğümün son `sonraki_atlama` paketi: gönderim
                           döngüsü kararı baş pakete sorar, onu kuyruktan
                           alıp düşürür (`kosum/gonderim.py`)
      iletim_basarisiz     düğümün son uçuştan indirilen paketi: `vazgec`
                           önce indirir, sonra düşürür
      tampon_asimi         `beklemeye_al`ın `eski`si (taşma) ya da `paket`i
                           (süresi dolmuş) · süre olayında `p`
      ttl                  `_yerlestir`in `paket`i
      dugum_kaybi          bulunmaz (kuyruk boşaltılırken paket bağlanmıyor;
                           birincil hücrede düğüm kaybı yok) → atfsız
    """
    if sebep == "kuyruk_tasmasi":
        return cagiran.f_locals.get("paket")
    if sebep in _KARAR_DUSUSU:
        return son_karar.get(dugum)
    if sebep == "iletim_basarisiz":
        return son_ucus.get(dugum)
    if sebep in ("tampon_asimi", "ttl") and cagiran.f_back is not None:
        yerel = cagiran.f_back.f_locals
        for ad in ("eski", "p", "paket"):
            if ad in yerel:
                return yerel[ad]
    return None


def _dogum_evresi(kayit, teslim_kimlik: set, bas: float, bitis: float,
                  evre_adi, alan) -> tuple[Counter, Counter, int]:
    """Düşüşleri paketin DOĞUM evresine atfeder.

    Dönüş: `sebep|doğum evresi|etki alanı` → adet (yalnız pencerede doğan
    paketler; alan düşüş anında, bölgeyle aynı düğüm kuralıyla) · atfsız
    düşüşler (sebep → adet) · çelişki: aynı eş iki kez düştü ya da (kopyasız
    koşuda) paket hem teslim edildi hem düştü. Çelişki > 0 düşen paketin
    yanlış bulunduğunu gösterir; o koşunun doğum evresi tablosu kullanılamaz.

    🔒 D-23 · K-231 — kopyalı koşuda bir paketin birden çok eşi düşebilir:
    teslim edilmiş paketin düşen eşleri kayıp DEĞİLDİR (atlanır), teslim
    edilmemiş paketin kaybı SON düşen eşine atfedilir. Kopyasız koşuda her
    paketin en çok bir düşüşü vardır; sonuç eskisinin aynısıdır.
    """
    atfsiz: Counter = Counter()
    goruldu: set[tuple[int, int]] = set()
    celiski = 0
    kopyali = any(p is not None and p[1] > 0 for *_, p in kayit)
    son: dict[int, tuple] = {}
    for n, sebep, t, j, p in kayit:
        if p is None:
            atfsiz[sebep] += 1
            continue
        kimlik, kopya, dogum = p
        if (kimlik, kopya) in goruldu:
            celiski += 1
        goruldu.add((kimlik, kopya))
        if kimlik in teslim_kimlik:
            if kopyali:
                continue
            celiski += 1
        onceki = son.get(kimlik)
        if onceki is None or t >= onceki[2]:
            son[kimlik] = (n, sebep, t, j, dogum)
    dusen: Counter = Counter()
    for n, sebep, t, j, dogum in son.values():
        if bas <= dogum < bitis:
            yer = j if sebep == "iletim_basarisiz" and j is not None else n
            dusen[f"{sebep}|{evre_adi(dogum)}|{alan(yer, t)}"] += 1
    return dusen, atfsiz, celiski


def _is(is_) -> dict:
    """Havuz işçisi — bir (protokol, tohum) koşusu ve anatomisi."""
    from kalibrasyon.aodv_uygunluk import _fabrika
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi
    from sim2.kanal.yayilim import dbm_to_w
    from sim2.kosum.dugum import Dugum
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri

    etiket, tohum, kol, aile, kisa, sinif = is_
    # K-198 · kol başına konfig farkı: `aodv@rota_tamponu_kapasitesi=256`
    # (birden çoğu `+` ile). Etiket sonuçta TAM haliyle durur.
    protokol, _, farklar = etiket.partition("@")
    t0 = time.perf_counter()
    pencere = (dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
                    olcum_bitis_s=40.0, kosu_bitis_s=50.0) if kisa else {})
    # `--sinif yok`: karıştırıcısız (U1-B düşük hücrelerinin anatomisi)
    ek = {} if sinif == "yok" else {"tehdit_senaryosu": aile}
    kfg = DS.konfig(kol="anatomi", senaryo=f"{kol}-{sinif}", tohum=tohum,
                    trafik_deseni="yere_toplama", **ek, **pencere,
                    **_konfig_farklari(farklar))
    kur = kurulum_yap(kfg)
    # --- karıştırıcının AÇIK / SESSİZ evresi (`derin_sizma`: 15 s · 15 s) --
    kar = kur.kanal.karistirici
    acilma = kfg.karistirici_baslangic_s
    uyeler = getattr(kar, "uyeler", (kar,)) if kar is not None else ()

    def evre_adi(t_s: float) -> str:
        if kar is None or t_s < acilma:
            return "once"
        return ("acik" if any(u.devrede_mi(t_s) for u in uyeler)
                else "sessiz")

    kayit: list[tuple[int, str, float, int | None,
                      tuple[int, int, float] | None]] = []
    son_hedef: dict[int, int | None] = {}
    kararlar: Counter = Counter()
    donuk = (not kur.topoloji.hareketli) and kur.kanal.karistirici is None
    # Doğum evresi (`_dusen_paket`): düğüm başına son karar ve son uçuş paketi.
    son_karar: dict[int, object] = {}
    son_ucus: dict[int, object] = {}

    asil_yer = Dugum._kayip_yeri
    asil_indir = Dugum.ucustan_indir
    asil_karar = Dugum.sonraki_atlama

    def izle(self, sebep):
        j = son_hedef.get(self.kimlik) if sebep == "iletim_basarisiz" else None
        p = _dusen_paket(sebep, self.kimlik, sys._getframe(1), son_karar,
                         son_ucus)
        kayit.append((self.kimlik, sebep, self.kur.olaylar.simdi, j,
                      None if p is None else (p.kimlik, p.kopya, p.dogum_s)))
        return asil_yer(self, sebep)

    def indir(self):
        son_hedef[self.kimlik] = self._ucus_hedefi
        paket = asil_indir(self)
        son_ucus[self.kimlik] = paket
        return paket

    def karar_izle(self, paket, t_s):
        son_karar[self.kimlik] = paket
        karar = asil_karar(self, paket, t_s)
        if karar.sonraki is not None:
            dilim = 0 if donuk else int(t_s / BAG_DILIMI_S)
            kararlar[(self.kimlik, int(karar.sonraki), dilim,
                      evre_adi(t_s))] += 1
        return karar

    s13 = {"s13": 0, "geri_alinan": 0, "geri_supurmede": 0,
           "geri_pakette": 0, "geri_sure_s": [], "karar": 0,
           "simetriksiz_karar": 0, "rg_karar": 0, "rg_sym_yok": 0,
           "rg_hedef_bagda": 0, "rg_duz_yol_var": 0,
           "rg_duz_yol_atlama": []}
    geri_olsr = (_olsr_s13_sar(s13) if protokol in (
        "olsr", "olsr_s13", "olsr_s13siz", "olsr_2atlama_lsym") else None)
    onarim_bolumleri: list = []
    rg_durum: Counter = Counter()
    geri_desparete = (_desparete_onarim_sar(kur, onarim_bolumleri, rg_durum,
                                            evre_adi, kfg.olcum_penceresi)
                      if protokol == "desparete" else None)
    Dugum._kayip_yeri = izle
    Dugum.ucustan_indir = indir
    Dugum.sonraki_atlama = karar_izle
    try:
        grafik = KanalGrafigi(kur)
        if protokol == "en_guvenilir_kahin":
            fabrika = lambda i: EnGuvenilirKahin(i, grafik)  # noqa: E731
        elif protokol == "olsr_s13":
            fabrika = _olsr_s13()
        elif protokol == "olsr_s13siz":
            fabrika = _olsr_s13siz()
        elif protokol == "olsr_2atlama_lsym":
            fabrika = _olsr_2atlama_lsym()
        else:
            fabrika = _fabrika(protokol, kfg)
        kosu = Kosu(kur, fabrika)
        kosu.kostur()
    finally:
        Dugum._kayip_yeri = asil_yer
        Dugum.ucustan_indir = asil_indir
        Dugum.sonraki_atlama = asil_karar
        if geri_olsr is not None:
            geri_olsr()
        if geri_desparete is not None:
            geri_desparete()
    satir = sonuc_satiri(kur, kosu.dugumler, protokol)
    kr = satir["korunum"]
    dogrula(len(kayit) == kr["dusen_toplam"],
            f"kanca {len(kayit)} düşüş gördü, defter {kr['dusen_toplam']} — "
            f"bir düşüş yolu `_kayip_yeri`ni atlıyor")

    # --- bağ kalitesi: kâhinin aynı ölçüsü (girişim hariç) --------------
    deneme = kfg.yeniden_deneme_siniri + 1
    onbellek: dict[tuple[int, int, int], float] = {}

    def p_tek(i: int, j: int, dilim: int, t_s: float) -> float:
        anahtar = (i, j, dilim)
        p = onbellek.get(anahtar)
        if p is None:
            p = onbellek[anahtar] = grafik._tek_deneme_basarisi(i, j, t_s)
        return p

    def p_atlama(i: int, j: int, dilim: int, t_s: float) -> float:
        return 1.0 - (1.0 - p_tek(i, j, dilim, t_s)) ** deneme

    def mesafe_km(i: int, j: int, t_s: float) -> float:
        return kur.topoloji.mesafe(i, j, t_s) / 1e3

    karar_bant: Counter = Counter()
    # Denetim 2026-10-08 D-02: yayın (HELLO · TC) TEK denemeyle gider; yeniden
    # denemeli bant onu göremez (tek deneme başarısı 0,25 olan bağ "iyi"dir).
    karar_bant_tek: Counter = Counter()
    karar_mesafe: list[tuple[float, int]] = []
    ed_w = dbm_to_w(kfg.ed_esigi_dbm)
    alan_onbellek: dict[tuple[int, int], str] = {}

    def alan(dugum: int, t_s: float) -> str:
        """Etki alanı, 1 s'lik dilimin ortasında (hareket 1 s'de ≤ 33 m)."""
        anahtar = (dugum, int(t_s))
        a = alan_onbellek.get(anahtar)
        if a is None:
            a = alan_onbellek[anahtar] = _etki_alani(
                kur, dugum, int(t_s) + 0.5, ed_w)
        return a

    karar_alan: Counter = Counter()
    for (i, j, dilim, evre), n in kararlar.items():
        t_orta = 0.0 if donuk else (dilim + 0.5) * BAG_DILIMI_S
        karar_bant[_bant(p_atlama(i, j, dilim, t_orta))] += n
        karar_bant_tek[_bant(p_tek(i, j, dilim, t_orta))] += n
        karar_mesafe.append((mesafe_km(i, j, t_orta), n))
        if kar is not None:
            karar_alan[f"{evre}|{alan(j, t_orta)}"] += n

    isinmada: Counter = Counter()          # ölçüm penceresinden ÖNCE düşen
    for _n, sebep, t, _j, _p in kayit:
        if t < kfg.olcum_penceresi[0]:
            isinmada[sebep] += 1
    tablo: Counter = Counter()
    basarisiz_bant: Counter = Counter()
    basarisiz_mesafe: list[float] = []
    basarisiz_bag: Counter = Counter()
    verici_bolge: Counter = Counter()
    evre_alan_dusen: Counter = Counter()
    for n, sebep, t, j, _p in kayit:
        if kar is not None:
            yer = j if sebep == "iletim_basarisiz" and j is not None else n
            evre_alan_dusen[f"{sebep}|{evre_adi(t)}|{alan(yer, t)}"] += 1
        if sebep == "iletim_basarisiz" and j is not None:
            tablo[(sebep, _bolge(kur, j, t, ed_w))] += 1
            verici_bolge[_bolge(kur, n, t, ed_w)] += 1
            dilim = 0 if donuk else int(t / BAG_DILIMI_S)
            basarisiz_bant[_bant(p_atlama(n, j, dilim, t))] += 1
            basarisiz_mesafe.append(mesafe_km(n, j, t))
            basarisiz_bag[(n, j)] += 1
        else:
            tablo[(sebep, _bolge(kur, n, t, ed_w))] += 1

    # Düşüşün yoğunlaştığı düğümler — sebep başına en çok beş (düğüm, adet,
    # geçide mesafe km, t = 0'da).
    dugum_dusen: dict[str, Counter] = {}
    for n, sebep, _t, _j, _p in kayit:
        dugum_dusen.setdefault(sebep, Counter())[n] += 1
    gecit = kfg.gecit
    yogun = {s: [[n, v, round(kur.topoloji.mesafe(n, gecit, 0.0) / 1e3, 1)]
                 for n, v in c.most_common(5)]
             for s, c in dugum_dusen.items()}

    # --- AÇIK / SESSİZ evre: düşüş ve paket (DOĞUM anına göre, `pdr_pencere`
    # gibi) evreye ayrılır — sessiz evrede PDR'nin temize dönüp dönmediği,
    # protokolün çizelgeye zamansal uyumudur (K-192 §4).
    evre_dusen: Counter = Counter()
    for _n, sebep, t, _j, _p in kayit:
        evre_dusen[f"{sebep}|{evre_adi(t)}"] += 1
    bas, bitis = kfg.olcum_penceresi
    evre_dogan: Counter = Counter()
    evre_teslim: Counter = Counter()
    # Paketin GEÇİT DIŞI ucu: telemetride kaynak, komutta hedef; eşler
    # arası desende kaynak.
    uc = {a.kimlik: (a.hedef if a.kaynak == kfg.gecit else a.kaynak)
          for a in kur.trafik.akislar}
    paket_alani: dict[int, str] = {}
    alan_dogan: Counter = Counter()
    alan_teslim: Counter = Counter()
    for k, akis, d in kur.paket_defteri.dogumlar():
        if bas <= d < bitis:
            evre_dogan[evre_adi(d)] += 1
            if kar is not None:
                paket_alani[k] = f"{evre_adi(d)}|{alan(uc[akis], d)}"
                alan_dogan[paket_alani[k]] += 1
    for kd in kur.paket_defteri.kayitlar():
        if bas <= kd.dogum_s < bitis:
            evre_teslim[evre_adi(kd.dogum_s)] += 1
            if kd.kimlik in paket_alani:
                alan_teslim[paket_alani[kd.kimlik]] += 1
    karistirici_evresi = {
        e: {"dogan": evre_dogan[e], "teslim": evre_teslim[e],
            "pdr": (evre_teslim[e] / evre_dogan[e] if evre_dogan[e]
                    else None)}
        for e in ("once", "acik", "sessiz")}
    # Doğum evresi: evre evre `doğan = teslim + Σ düşen + kalan` (kalan:
    # koşu sonunda kuyrukta, tamponda ya da uçuşta).
    dogum_dusen, atfsiz, celiski = _dogum_evresi(
        kayit, {kd.kimlik for kd in kur.paket_defteri.kayitlar()}, bas,
        bitis, evre_adi, alan if kar is not None else (lambda _d, _t: "uzak"))

    teshis: Counter = Counter()
    for dt in satir["teshis"]["dugum"]:
        for k, v in dt.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                teshis[k] += v
            elif k.endswith("_sayac") and isinstance(v, (tuple, list)):
                # DESPARETE: sayaç grupları ad + değer demeti (`teshis`)
                grup = k[:-len("_sayac")]
                for ad, deger in zip(dt.get(f"{grup}_adlari") or (), v):
                    if (isinstance(deger, (int, float))
                            and not isinstance(deger, bool)):
                        teshis[f"{grup}.{ad}"] += deger
    m = satir["metrikler"]
    return {"protokol": etiket, "tohum": tohum, "gecerli": kr["gecerli"],
            "pdr": m["pdr"], "pdr_pencere": m["pdr_pencere"],
            "uretilen": kr["uretilen"], "teslim": kr["teslim"],
            "kuyrukta": kr["kuyrukta"],
            "tablo": {f"{s}|{b}": v for (s, b), v in tablo.items()},
            "isinmada": dict(isinmada),
            "karar_bant": dict(karar_bant),
            "karar_bant_tek": dict(karar_bant_tek),
            "karar_mesafe_km": _yuzdelik(karar_mesafe),
            "basarisiz_bant": dict(basarisiz_bant),
            "basarisiz_mesafe_km": _yuzdelik([(d, 1) for d in
                                              basarisiz_mesafe]),
            "basarisiz_bag_sayisi": len(basarisiz_bag),
            "basarisiz_en_cok_5_bag": [
                [i, j, v] for (i, j), v in basarisiz_bag.most_common(5)],
            "iletim_basarisiz_verici_bolge": dict(verici_bolge),
            "teshis_toplam": dict(teshis),
            "yogun_dugumler": yogun,
            # 🔒 `08` G1'in M4 maddesi GERÇEK protokolle (K-194): açılma anı
            # karıştırıcısız kolda da konfigden gelir; boş kolda tespit
            # gecikmesi SANSÜRLÜ (`None`) olmalı, şok derinliği ~0.
            "evre": {a: m.get(a) for a in (
                "sok_derinligi", "sok_derinligi_se", "toparlanma_suresi_s",
                "tespit_gecikmesi_s", "beyan_etmiyor",
                "evre_metrikleri_yok")},
            "olsr_s13": s13 if geri_olsr is not None else None,
            "karistirici_evresi": karistirici_evresi,
            "evre_dusen": dict(evre_dusen),
            "dogum_evre_dusen": dict(dogum_dusen),
            "dogum_atfsiz": dict(atfsiz),
            "dogum_celiski": celiski,
            "pdr_acik_satir": m.get("pdr_acik"),
            "evre_alan_paket": {a: [alan_dogan[a], alan_teslim[a]]
                                for a in alan_dogan},
            "evre_alan_karar": dict(karar_alan),
            "evre_alan_dusen": dict(evre_alan_dusen),
            "desparete_onarim": (dict(_onarim_ozeti(
                onarim_bolumleri, bas, bitis, kfg.kosu_bitis_s, evre_adi),
                rota_gecersiz_durum=dict(rg_durum))
                if geri_desparete is not None else None),
            "sure_s": round(time.perf_counter() - t0, 1)}


def _yuzdelik(agirlikli: list[tuple[float, int]]) -> dict | None:
    """Ağırlıklı (değer, adet) listesinin p10 · p50 · p90'ı."""
    if not agirlikli:
        return None
    sirali = sorted(agirlikli)
    toplam = sum(n for _, n in sirali)
    cikti, birikim, i = {}, 0, 0
    for ad, oran in (("p10", 0.10), ("p50", 0.50), ("p90", 0.90)):
        while birikim + sirali[i][1] < oran * toplam and i < len(sirali) - 1:
            birikim += sirali[i][1]
            i += 1
        cikti[ad] = round(sirali[i][0], 2)
    return cikti


def _arg(argv: list[str], ad: str, varsayilan: str) -> str:
    if ad in argv:
        i = argv.index(ad)
        deger = argv[i + 1]
        del argv[i:i + 2]
        return deger
    return varsayilan


EVRELER = ("once", "acik", "sessiz")


def _evre_alan_raporu(rs: list[dict], sebepler: list[str]) -> None:
    """Evre × etki alanı — tohumlar toplanmış: paket PDR'si (doğan), veri
    kararlarının alan payı ve düşüşler (üretilene oran)."""
    paket: Counter = Counter()
    karar: Counter = Counter()
    dusen: Counter = Counter()
    for r in rs:
        for a, (dogan, teslim) in r["evre_alan_paket"].items():
            paket[a + "|d"] += dogan
            paket[a + "|t"] += teslim
        karar.update(r["evre_alan_karar"])
        dusen.update(r["evre_alan_dusen"])
    uretilen = sum(r["uretilen"] for r in rs)
    print(f"    evre × etki alanı{'':<3}" + "".join(
        f"{b:>22}" for b in BOLGELER))
    for e in EVRELER:
        hucre = []
        for b in BOLGELER:
            d, t = paket[f"{e}|{b}|d"], paket[f"{e}|{b}|t"]
            hucre.append(f"{t / d:.3f} ({d})" if d else "—")
        print(f"    PDR {e:<16}" + "".join(f"{h:>22}" for h in hucre))
    for e in EVRELER:
        toplam = sum(karar[f"{e}|{b}"] for b in BOLGELER)
        if toplam:
            print(f"    karar payı {e:<9}" + "".join(
                f"{karar[f'{e}|{b}'] / toplam:>22.1%}" for b in BOLGELER))
    print("    düşen/üretilen (ed / girisim / uzak):")
    for s in sebepler:
        parca = [f"{e} " + " / ".join(
                    f"{dusen[f'{s}|{e}|{b}'] / uretilen:.1%}" for b in BOLGELER)
                 for e in EVRELER
                 if any(dusen[f"{s}|{e}|{b}"] for b in BOLGELER)]
        if parca:
            print(f"      {s:<18}" + " · ".join(parca))


def _dogum_sayimi(rs: list[dict]) -> tuple[Counter, Counter, Counter]:
    """Doğum evresine göre sayımlar, tohumlar toplanmış: evre → doğan ·
    evre → teslim · `sebep|evre|alan` → düşen."""
    dogan: Counter = Counter()
    teslim: Counter = Counter()
    dusen: Counter = Counter()
    for r in rs:
        for e in EVRELER:
            dogan[e] += r["karistirici_evresi"][e]["dogan"]
            teslim[e] += r["karistirici_evresi"][e]["teslim"]
        dusen.update(r["dogum_evre_dusen"])
    return dogan, teslim, dusen


def _evre_orani(dogan: Counter, teslim: Counter, dusen: Counter,
                e: str) -> dict[str, float]:
    """Bir evrede doğanların akıbeti, doğana oran: sebep başına düşen ·
    `teslim` (= o evrenin PDR'si) · `kalan` (koşu sonunda yolda)."""
    sebep: Counter = Counter()
    for k, v in dusen.items():
        s, ee, _a = k.split("|")
        if ee == e:
            sebep[s] += v
    o = {s: v / dogan[e] for s, v in sebep.items()}
    o["teslim"] = teslim[e] / dogan[e]
    o["kalan"] = (dogan[e] - teslim[e] - sum(sebep.values())) / dogan[e]
    return o


def _dogum_evre_raporu(rs: list[dict]) -> dict | None:
    """Doğum evresine göre akıbet — tohumlar toplanmış (Faz 5.0). Dönüş:
    açık − önce farkları; toplamları sıfır (Δteslim = −Σ Δsebep − Δkalan),
    yani karıştırmaya özgü kayıp sebeplere TAM ayrılır. Önce ya da açık
    evrede doğan yoksa (kısa pencere) `None`."""
    for r in rs:
        uyari = []
        if r["dogum_celiski"]:
            uyari.append(f"ÇELİŞKİ {r['dogum_celiski']} (düşen paket yanlış "
                         f"bulunuyor — tablo kullanılamaz)")
        if r["dogum_atfsiz"]:
            uyari.append(f"atfsız {r['dogum_atfsiz']}")
        if uyari:
            print(f"    🔴 tohum {r['tohum']} doğum evresi: "
                  + " · ".join(uyari))
    dogan, teslim, dusen = _dogum_sayimi(rs)
    oran = {e: _evre_orani(dogan, teslim, dusen, e)
            for e in EVRELER if dogan[e]}
    sebepler = sorted({k.split("|")[0] for k in dusen})
    print("    doğum evresine göre akıbet (doğana oran, tohumlar toplanmış):")
    print(f"      {'evre':<8}{'doğan':>8}{'teslim':>9}" + "".join(
        f"{s[:16]:>18}" for s in sebepler) + f"{'kalan':>9}")
    for e, o in oran.items():
        print(f"      {e:<8}{dogan[e]:>8}{o['teslim']:>9.3f}" + "".join(
            f"{o.get(s, 0.0):>18.3f}" for s in sebepler)
            + f"{o['kalan']:>9.3f}")
    fark = None
    if "once" in oran and "acik" in oran:
        adlar = set(oran["once"]) | set(oran["acik"])
        fark = {a: oran["acik"].get(a, 0.0) - oran["once"].get(a, 0.0)
                for a in adlar}
        print(f"      {'açık−önce':<16}{fark['teslim']:>+9.3f}" + "".join(
            f"{fark.get(s, 0.0):>+18.3f}" for s in sebepler)
            + f"{fark['kalan']:>+9.3f}")
    for e in ("acik", "once"):
        if not dogan[e]:
            continue
        parca = []
        for s in sebepler:
            v = [dusen.get(f"{s}|{e}|{b}", 0) for b in BOLGELER]
            if sum(v):
                parca.append(f"{s} " + " / ".join(
                    f"{x / dogan[e]:.1%}" for x in v))
        print(f"      {e} evrede doğan, düşen × etki alanı (ed / girisim / "
              f"uzak): " + (" · ".join(parca) or "—"))
    return fark


def _ozel_kayip_tablosu(ozel: dict[str, dict]) -> None:
    """KARIŞTIRMAYA ÖZGÜ KAYIP — doğum evresine göre açık − önce, doğana
    oran; satır toplamı sıfır. DESPARETE varsa öteki kollarla farkı da."""
    adlar = sorted({a for f in ozel.values() for a in f} - {"teslim", "kalan"})
    sutun = ["teslim", *adlar, "kalan"]
    print("\n  KARIŞTIRMAYA ÖZGÜ KAYIP — doğum evresine göre açık − önce "
          "(doğana oran, tohumlar toplanmış; satır toplamı 0)")
    print(f"    {'kol':<28}" + "".join(f"{a[:16]:>18}" for a in sutun))
    for p, f in ozel.items():
        print(f"    {p:<28}" + "".join(f"{f.get(a, 0.0):>+18.3f}"
                                       for a in sutun))
    d = ozel.get("desparete")
    if d is not None:
        for p, f in ozel.items():
            if p == "desparete":
                continue
            print(f"    {'desparete − ' + p:<28}" + "".join(
                f"{d.get(a, 0.0) - f.get(a, 0.0):>+18.3f}" for a in sutun))


def _oranlar(sayac: dict) -> str:
    toplam = sum(sayac.values())
    if not toplam:
        return "—"
    return " · ".join(f"{b} {sayac.get(b, 0) / toplam:.0%}" for b in BANTLAR)


def main() -> int:
    DS.secimi_oku()
    argv = sys.argv[1:]
    kisa = "--kisa" in argv
    if kisa:
        argv.remove("--kisa")
    kol = _arg(argv, "--kol", "formasyon")
    aile = _arg(argv, "--aile", "derin_sizma")
    sinif = _arg(argv, "--sinif", "surekli")
    dogrula(sinif in ("surekli", "yok"), f"sinif surekli|yok: {sinif!r}")
    protokoller = _arg(argv, "--protokoller",
                       "aodv,olsrv2,jarmrout,desparete,en_guvenilir_kahin"
                       ).split(",")
    tohumlar = [int(t) for t in _arg(argv, "--tohumlar",
                                     "1003,1004,1005").split(",")]
    isci = int(_arg(argv, "--isci", "8"))
    kayit_yolu = _arg(argv, "--kayit", "")
    dogrula(not argv, f"tanınmayan argüman: {argv}")
    dogrula(not any(2000 <= t <= 2039 for t in tohumlar),
            "ana deney tohumları (2000–2039) mühürden önce koşulmaz")
    print("=" * 78)
    print(f"KAYIP ANATOMISI — dunya {DS.secili()} · {kol}-{sinif} · aile "
          f"{aile if sinif != 'yok' else '—'} · yere toplama · "
          f"tohum {tohumlar}"
          f"{' · KISA PENCERE' if kisa else ''}")
    print("=" * 78)
    isler = [(p, t, kol, aile, kisa, sinif) for p in protokoller
             for t in tohumlar]
    t0 = time.perf_counter()
    # 🔒 K-198 · UZUN KOŞU GÜVENCESİ: her koşu biter bitmez ara kayda
    # (`<kayit>.jsonl`) yazılır ve bir ilerleme satırı basılır; bir koşunun
    # hatası yalnız onu düşürür. Ara kayıtta olan (etiket, tohum) yeniden
    # koşulmaz — kesintiden sonra aynı komut kaldığı yerden sürer.
    ara = Path(kayit_yolu + "l") if kayit_yolu.endswith(".json") else (
        Path(kayit_yolu + ".jsonl") if kayit_yolu else None)
    sonuc: list[dict] = []
    if ara is not None and ara.exists():
        for satir in ara.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                r = json.loads(satir)
                if "hata" not in r:
                    sonuc.append(r)
        bitti = {(r["protokol"], r["tohum"]) for r in sonuc}
        isler = [i for i in isler if (i[0], i[1]) not in bitti]
        print(f"  ara kayıttan {len(sonuc)} koşu okundu, {len(isler)} koşu "
              f"kaldı ({ara})", flush=True)
    hatalar: list[dict] = []
    if isler:
        with Pool(min(isci, len(isler))) as havuz:
            for n, r in enumerate(havuz.imap_unordered(_is_guvenli, isler,
                                                       chunksize=1), 1):
                if ara is not None:
                    with ara.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                if "hata" in r:
                    hatalar.append(r)
                    print(f"  🔴 {n}/{len(isler)} {r['protokol']} "
                          f"{r['tohum']}: {r['hata']}", flush=True)
                    continue
                sonuc.append(r)
                print(f"  {n:>3}/{len(isler)} {r['protokol']:<42} "
                      f"{r['tohum']} · PDR(pencere) {r['pdr_pencere']:.4f} · "
                      f"{r['sure_s']:.0f} s", flush=True)
    if hatalar:
        print(f"\n  🔴 {len(hatalar)} koşu HATA verdi — özetten çıkarıldı")
    protokoller = [p for p in protokoller
                   if any(r["protokol"] == p for r in sonuc)]
    if kayit_yolu:
        Path(kayit_yolu).write_text(
            json.dumps({"dunya": DS.secili(), "kol": kol, "sinif": sinif,
                        "aile": aile, "kisa": kisa, "sonuc": sonuc},
                       ensure_ascii=False, indent=1), encoding="utf-8")
    sebepler = sorted({k.split("|")[0] for r in sonuc for k in r["tablo"]})
    kahin = {r["tohum"]: r for r in sonuc
             if r["protokol"] == "en_guvenilir_kahin"}
    ozel: dict[str, dict] = {}            # protokol → açık − önce farkları
    for p in protokoller:
        rs = sorted((r for r in sonuc if r["protokol"] == p),
                    key=lambda r: r["tohum"])
        pdr = ist.mean(r["pdr_pencere"] for r in rs)
        uretilen = sum(r["uretilen"] for r in rs)
        print(f"\n  {p:<20} PDR(pencere) ort {pdr:.3f} · üretilen "
              f"{uretilen} · geçerli {all(r['gecerli'] for r in rs)}")
        for r in rs:
            k = kahin.get(r["tohum"])
            oran = (f" · kâhine oran (tüm koşu) {r['pdr'] / k['pdr']:.3f}"
                    if k and p != "en_guvenilir_kahin" and k["pdr"] else "")
            dusen = {s: sum(v for kk, v in r["tablo"].items()
                            if kk.startswith(s + "|")) for s in sebepler}
            ozet = " · ".join(f"{s} {v / r['uretilen']:.1%}"
                              for s, v in sorted(dusen.items(),
                                                 key=lambda x: -x[1]) if v)
            print(f"    tohum {r['tohum']}: PDR {r['pdr']:.4f} (pencere "
                  f"{r['pdr_pencere']:.4f}){oran} · {r['sure_s']:.0f} s")
            print(f"      düşen/üretilen: {ozet or '—'}")
            isn = " · ".join(f"{s} {v}" for s, v in sorted(
                r["isinmada"].items(), key=lambda x: -x[1]))
            print(f"      ısınmada düşen (adet): {isn or '—'}")
            for s in ("rota_gecersiz", "iletim_basarisiz", "ttl"):
                if s in r["yogun_dugumler"]:
                    print(f"      en çok {s} (düğüm, adet, geçide km): "
                          f"{r['yogun_dugumler'][s]}")
            e = r["evre"]
            if e.get("evre_metrikleri_yok"):
                print(f"      evre: TANIMSIZ — {e['evre_metrikleri_yok']}")
            else:
                print(f"      evre: şok derinliği {e['sok_derinligi']} · "
                      f"toparlanma {e['toparlanma_suresi_s']} s · tespit "
                      f"{e['tespit_gecikmesi_s']} s"
                      + (" (boş kolda None olmalı — M4 kapısı)"
                         if sinif == "yok" else "")
                      + (" · BEYAN ETMİYOR" if e["beyan_etmiyor"] else ""))
            ke = r["karistirici_evresi"]
            if sinif != "yok":
                print("      karıştırıcı evresi (doğuma göre PDR · doğan): "
                      + " · ".join(
                          f"{e} {ke[e]['pdr']:.3f} ({ke[e]['dogan']})"
                          if ke[e]["pdr"] is not None else f"{e} —"
                          for e in ("once", "acik", "sessiz")))
                a, b = ke["acik"]["pdr"], r.get("pdr_acik_satir")
                if b is not None:
                    print("      açık PDR, satırın `pdr_acik`ıyla: "
                          + ("birebir" if a is not None and abs(a - b) < 1e-12
                             else f"🔴 UYUŞMUYOR ({a} ↔ {b})"))
                ed = r["evre_dusen"]
                print("      düşen evreye göre (açık/sessiz/önce): " + " · ".join(
                    f"{s} {ed.get(s + '|acik', 0)}/{ed.get(s + '|sessiz', 0)}"
                    f"/{ed.get(s + '|once', 0)}" for s in sebepler
                    if any(ed.get(f"{s}|{e}") for e in
                           ("acik", "sessiz", "once"))))
            print(f"      karar bağı kâhin bandı: {_oranlar(r['karar_bant'])}"
                  f" · mesafe km {r['karar_mesafe_km']}")
            if r.get("karar_bant_tek"):
                print(f"      karar bağı TEK deneme (yayın) bandı: "
                      f"{_oranlar(r['karar_bant_tek'])}")
            print(f"      başarısız bağ bandı:   "
                  f"{_oranlar(r['basarisiz_bant'])} · mesafe km "
                  f"{r['basarisiz_mesafe_km']} · {r['basarisiz_bag_sayisi']}"
                  f" ayrı bağ, en çok {r['basarisiz_en_cok_5_bag']}")
            if r.get("desparete_onarim"):
                o = r["desparete_onarim"]
                print("      onarım bölümleri (evre|giriş|son: adet): " + " · ".join(
                    f"{k} {v}" for k, v in sorted(o["sayim"].items())))
                print("      onarım süresi s (evre|son: p50/p90/toplam): "
                      + " · ".join(f"{k} {v[0]}/{v[1]}/{v[2]}"
                                   for k, v in sorted(o["sure"].items())))
                print("      rota_gecersiz anında alan (evre|durum: adet, "
                      "pencerede): " + " · ".join(
                          f"{k} {v}" for k, v in sorted(
                              o["rota_gecersiz_durum"].items())))
            if r["olsr_s13"] is not None:
                s = r["olsr_s13"]
                sure = s["geri_sure_s"]
                print(f"      OLSR §13: bildirim {s['s13']} · geri alınan "
                      f"{s['geri_alinan']} (süpürmede {s['geri_supurmede']}"
                      f" · pakette {s['geri_pakette']}) · geri alma süresi "
                      f"medyan {ist.median(sure) if sure else '—'} s · "
                      f"simetrik olmayan ardıla karar "
                      f"{s['simetriksiz_karar']}/{s['karar']}")
                if s["rg_karar"]:
                    at = s["rg_duz_yol_atlama"]
                    print(f"      rota boşalması: {s['rg_karar']} karar · "
                          f"simetrik komşu yok {s['rg_sym_yok']} · geçit bağ "
                          f"kümesinde {s['rg_hedef_bagda']} · KENDİ "
                          f"bilgisinde düz yol VAR {s['rg_duz_yol_var']} "
                          f"(atlama medyan "
                          f"{ist.median(at) if at else '—'})")
                t = r["teshis_toplam"]
                print("      OLSR sayaçları (ağ toplamı): " + " · ".join(
                    f"{a} {t.get(a, 0):.0f}" for a in (
                        "komsu_kaybi", "bag_katmani_kopma", "rota_hesap",
                        "hello_uretilen", "tc_uretilen", "tc_iletilen",
                        "tc_simetriksiz", "hist_kayip_psn",
                        "hist_kayip_sessiz", "erken_tc")))
        if sinif != "yok":
            _evre_alan_raporu(rs, sebepler)
            fark = _dogum_evre_raporu(rs)
            if fark is not None:
                ozel[p] = fark
        print(f"    {'sebep':<18}" + "".join(f"{b:>10}" for b in BOLGELER)
              + f"{'toplam':>10}{'üretilene':>11}")
        for s in sebepler:
            satir = [sum(r["tablo"].get(f"{s}|{b}", 0) for r in rs)
                     for b in BOLGELER]
            if sum(satir) == 0:
                continue
            print(f"    {s:<18}" + "".join(f"{v:>10}" for v in satir)
                  + f"{sum(satir):>10}{sum(satir) / uretilen:>10.1%}")
        kuyrukta = sum(r["kuyrukta"] for r in rs)
        print(f"    {'(koşu sonu kuyrukta)':<18}{kuyrukta:>40}"
              f"{kuyrukta / uretilen:>10.1%}")
    if ozel:
        _ozel_kayip_tablosu(ozel)
    print("\n  bolge: ed = karistirici >= ED esigi (kanal erisim kilidi) · "
          "girisim = gurultunun ustu · uzak = karistiricidan bagimsiz")
    print("  etki alani: karistirici o an ACIK olsaydi alinacak ORTALAMA guc "
          "(yavas kayip; kapi ve hizli sonumleme haric), ayni esikler; paket "
          "tablosunda paketin gecit disi ucunda, dogum aninda")
    print("  iletim_basarisiz'in bolgesi ALICIDA (denenen sonraki atlama) "
          "okunur; digerleri dustugu dugumde (K-193)")
    print("  bag bandi: kahinin tek deneme basarisindan p_atlama — iyi >= "
          "0,90 · orta 0,50-0,90 · kotu < 0,50 (girisim haric)")
    print(f"  toplam duvar suresi {time.perf_counter() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
