"""
Deney kolları — mobilite ekseni × karıştırıcı sınıfı ekseni.

Kol adı `<mobilite>-<sınıf>`; trafik deseni ve tehdit senaryosu ayrı TEDAVİ
eksenleridir, ada girmez. Mobilite bir eksendir, bir ayar değil: kollar
*"mobilite modeli değişince protokol sıralaması değişiyor mu"* sorusunu
bir varsayım olmaktan çıkarıp ölçülen bir sonuca çevirmek için var.

Θ ve bölünme tabloları DÜNYAYA aittir (K-188): referans dünyanın tabloları
`*_REFERANS`; adsızlar eski dünyanındır (regresyonun eski vakaları).
Karıştırıcı gücü referans dünyada öğrenci kararıdır (10 W, K-186,
`kanal/dunya.py`); `KARISTIRICI_GUCU_DBM` eski dünyanın ρ kalibrasyonu.
"""

from __future__ import annotations

from dataclasses import dataclass

from sim2.cekirdek.degismezler import dogrula

__all__ = [
    "MOBILITE_KOLLARI", "MOBILITE_THETA", "TRAFIK_DESENLERI",
    "MOBILITE_BOLUNME", "BOLUNME_OLCULEN_ARALIK", "bolunme_payi",
    "MOBILITE_THETA_REFERANS", "MOBILITE_BOLUNME_REFERANS", "mobilite_theta",
    "TEHDIT_SENARYOLARI", "KARISTIRICI_SINIFLARI",
    "SenaryoTanimi",
    "SENARYOLAR", "UYGULANMAMIS_KARISTIRICI", "KARISTIRICI_GUCU_DBM",
    "senaryo_adi",
]

# --------------------------------------------------------------------- eksen 1
# Dört kol: `statik` (U1'in kontrol kolu) · `bagimsiz` (3B Gauss-Markov,
# FANET literatürünün standardı; tasarım uzayının en yüksek bağıl hızlı
# ucu) · `gorev` (koordineli müfrezeler) · `formasyon` (istasyon tutma, Y6;
# birincil hücrenin kolu). Görev ve formasyon istasyon tutma fiziğini
# paylaşır (`dunya/mobilite.py`).
MOBILITE_KOLLARI: tuple[str, ...] = ("statik", "bagimsiz", "gorev", "formasyon")

# Θ — mobilite kolu başına, iki paydayla (`v2/07` §4): (Θ_OLSR, Θ_AODV,
# hiç kopmayan çift oranı); paydalar OLSR `TOP_HOLD_TIME` 15 s ve AODV
# `ACTIVE_ROUTE_TIMEOUT` 3 s. Statik kolda tanımsız (hiçbir rota
# kopmuyor). Çiftlerin çoğu kopmuyorsa ölçüme yalnız eşiğin kıyısındaki
# çiftler girer → sayı bir alt sınırdır; kopmayan oranı satırda.
# ESKİ DÜNYA — üretici `python -u kalibrasyon/theta_kollari.py`
# (14 Eylül 2026, 6 tohum × 350 s × 40 çift).
MOBILITE_THETA: dict[str, tuple[float | None, float | None, float]] = {
    "statik": (None, None, 1.000),
    "bagimsiz": (3.25, 16.27, 0.404),
    "gorev": (3.99, 19.93, 0.275),
    "formasyon": (2.31, 11.53, 0.921),
}

# ==========================================================================
# AĞ BÖLÜNMESİ — ana deney tohumlarında, kâhin grafiğinde (B6 · K-132)
# ==========================================================================
# Bölünmüş bir tohumda teslim protokolden bağımsız çöker; satır bunu
# söyler (`kapsam.bolunme_payi`), tohum atılmaz (seçilim yanlılığı olurdu).
# Karıştırıcısız (`-yok`) kolda ölçülür: topolojinin bölünmesi, karıştırma
# değil. Dokuz an örneklenir → alt sınır. `None` = ölçülmedi (tohum
# aralık dışında), `0.0` = ölçüldü ve bölünme yok.
BOLUNME_OLCULEN_ARALIK: tuple[int, int] = (2000, 2040)
# ESKİ DÜNYA — üretici `python -u kalibrasyon/dugum_sayisi.py --bolunme`
# (16 Eylül 2026). Yalnız sıfırdan büyük kayıtlar tutulur.
MOBILITE_BOLUNME: dict[str, dict[int, float]] = {
    "statik": {},
    "bagimsiz": {
        2007: 0.1111,
        2011: 0.1111,
        2021: 0.2222,
        2023: 0.1111,
        2028: 0.3333,
        2035: 0.2222,
    },
    "gorev": {
        2001: 0.1111,
        2007: 0.1111,
        2009: 0.3333,
        2019: 0.2222,
        2020: 0.3333,
        2032: 0.2222,
        2034: 0.4444,
    },
    "formasyon": {
        2006: 0.1111,
        2011: 0.7778,
    },
}


# ==========================================================================
# REFERANS DÜNYANIN TABLOLARI — K-188
# ==========================================================================
# Θ — üretici `python -u kalibrasyon/theta_kollari.py --dunya
# referans_2026` (33 km, gölgeleme 2,5 km; 6 tohum). Formasyonda çiftlerin
# %99,6'sı hiç kopmuyor, tek ömür gözlendi → statik kolun kuralıyla tanımsız.
MOBILITE_THETA_REFERANS: dict[str, tuple[float | None, float | None, float]] = {
    "statik": (None, None, 1.000),
    "bagimsiz": (5.15, 25.74, 0.883),
    "gorev": (2.79, 13.94, 0.838),
    "formasyon": (None, None, 0.996),
}
# Bölünme — Üretici: `python -u kalibrasyon/dugum_sayisi.py --dunya
# referans_2026 --bolunme` (33 km; 4 kol × 40 ana deney tohumu × 9 an,
# kâhin grafiği). Bölünmüş (kol, tohum) 8/160; çoğu TEK bir kenar düğümünün
# kopması (39 ulaşılamaz çift). Aynı ölçülen aralık (`BOLUNME_OLCULEN_ARALIK`).
MOBILITE_BOLUNME_REFERANS: dict[str, dict[int, float]] = {
    "statik": {2029: 1.0},
    "bagimsiz": {2007: 0.2222, 2029: 0.3333},
    "gorev": {2002: 0.1111, 2019: 0.1111, 2028: 0.1111},
    "formasyon": {2008: 0.1111, 2029: 0.8889},
}


def mobilite_theta(mobilite_kolu: str, dunya: str = "olcek_1_50"
                   ) -> tuple[float | None, float | None, float]:
    """Kolun `(Θ_OLSR, Θ_AODV, kopmayan oran)`ı — SEÇİLİ DÜNYADAN (K-188)."""
    tablo = (MOBILITE_THETA_REFERANS if dunya == "referans_2026"
             else MOBILITE_THETA)
    return tablo[mobilite_kolu]


def bolunme_payi(mobilite_kolu: str, tohum: int,
                 dunya: str = "olcek_1_50") -> float | None:
    """Bu (kol, tohum) çiftinde ağın bölünmüş olduğu an payı.

    `None` = ÖLÇÜLMEDİ (tohum ana deney kümesinde değil). `0.0` = ölçüldü ve
    bölünme görülmedi. İkisi ayrı şeydir ve karıştırılırsa kalibrasyon
    tohumları sessizce "temiz" diye okunur. Tablo seçili dünyanındır (K-188).
    """
    bas, son = BOLUNME_OLCULEN_ARALIK
    if not bas <= tohum < son:
        return None
    tablo = (MOBILITE_BOLUNME_REFERANS if dunya == "referans_2026"
             else MOBILITE_BOLUNME)
    return tablo.get(mobilite_kolu, {}).get(tohum, 0.0)

# Trafik desenleri (`v2/07` §6) — ayrı bir TEDAVİ ekseni; `esler_arasi`
# varsayılan, `yere_toplama` birincil (ana deney aleti açıkça verir).
TRAFIK_DESENLERI: tuple[str, ...] = ("esler_arasi", "yere_toplama")

# Tehdit senaryoları (`v2/07` §5, K-119) — karıştırıcı KÜMESİNİN biçimi;
# sinyal sınıfı senaryo adından gelir. Ayrı bir TEDAVİ ekseni; ilk değer
# varsayılan. Birincil hücre `derin_sizma` (K-186). Tanımlar `kanal/tehdit.py`.
TEHDIT_SENARYOLARI: tuple[str, ...] = (
    "tekli_merkez", "cephe_hatti", "derin_sizma", "hedef_koruma", "hava_eslik")

# Görev kolunun seçim ölçütü (taramadan önce ilan edildi): müfreze başına en
# az 4 üye (daha küçüğü taktik bir alt birim değildir) ve bu koşulda
# ortalama dereceyi bağımsız kolla eşitleyen (|Δderece| ≤ 0,3) aday. Bağıl
# hız ve rota ömrü sonuçtur, ölçüt değil. Derece eşitlemesi zorunlu: kolları
# karşılaştırılabilir yapan yoğunluğun eşitliğidir.

# --------------------------------------------------------------------- eksen 2
# Onaylı karar 5: beş sınıf + darbeli. `darbeli` ayrı bir eksen DEĞİL, sürekli
# karıştırıcının bir kipidir — ortalama gücü sabit karşılığına eşitlenir ve
# sorulan soru *"aynı ortalama güçte darbeli olmak fark eder mi"*dır.
KARISTIRICI_SINIFLARI: tuple[str, ...] = (
    "yok",             # taban — karıştırma yok
    "surekli",         # sabit güçte kesintisiz gürültü
    "surekli_darbeli", # aynı ORTALAMA güç, darbeli
    "reaktif",         # 🔴 durum tutar: iletim-başladı olayına tepki verir
    "aldatici",        # geçerli görünümlü önbelge — CSMA'ya GÖRÜNÜR
    "taramali",        # konaklar arasında gezinir
)

# Uygulanmamış karıştırıcı sınıfı kalmadı (beşi de `kanal/karistirici.py`);
# ölçülmemiş güçle koşmayı `kanal/karistirici.py` durdurur.
UYGULANMAMIS_KARISTIRICI: frozenset[str] = frozenset()

# ESKİ DÜNYANIN karıştırıcı TABAN gücü — ρ kalibrasyonu (`python
# kalibrasyon/karistirici_gucu.py tarama`, 8 Eylül 2026): referans sınıfta
# (`surekli`) −15 dBm · ρ 0,258, beş sınıfa aynı taban (ayrı güç ρ'yu
# kalibrasyonla eşitlemek, yani aranan farkı silmek olurdu). Darbeli
# sınıfa tepe telafisi eklenir; taramalının ortalaması konak sayısına
# bölünür (beyanlı). Referans dünyada taban `Konfig.karistirici_taban_dbm`.
KARISTIRICI_GUCU_DBM: dict[str, float | None] = {
    "yok": None,             # 🔒 karıştırıcı yok — `None` burada DOĞRU
    "surekli": -15.0,        # referans: ölçüt bu sınıfta koştu
    "surekli_darbeli": -15.0,  # taban; tepe telafisiyle ortalama eşitlenir
    "reaktif": -15.0,
    "aldatici": -15.0,
    "taramali": -15.0,       # ⚠️ tepe eşit, ortalama 1/3 — beyan edilmiş
}


@dataclass(frozen=True, slots=True)
class SenaryoTanimi:
    """Bir kolun TAM tanımı. Kod düzenlemesiyle üretilen kol kaybolmuş deneydir."""
    ad: str
    mobilite_kolu: str
    karistirici_sinifi: str

    @property
    def hareketli(self) -> bool:
        """🔒 Türetilmiş: `statik` dışındaki her kol hareketlidir."""
        return self.mobilite_kolu != "statik"

    @property
    def darbeli(self) -> bool:
        return self.karistirici_sinifi == "surekli_darbeli"

    @property
    def karistirici_var_mi(self) -> bool:
        return self.karistirici_sinifi != "yok"


def senaryo_adi(mobilite_kolu: str, karistirici_sinifi: str) -> str:
    return f"{mobilite_kolu}-{karistirici_sinifi}"


SENARYOLAR: dict[str, SenaryoTanimi] = {
    senaryo_adi(m, j): SenaryoTanimi(senaryo_adi(m, j), m, j)
    for m in MOBILITE_KOLLARI
    for j in KARISTIRICI_SINIFLARI
}

# Kurulum denetimi — modül yüklenirken bir kez.
dogrula(len(SENARYOLAR) == len(MOBILITE_KOLLARI) * len(KARISTIRICI_SINIFLARI),
        "senaryo çapraz çarpımı eksik")
dogrula(set(KARISTIRICI_GUCU_DBM) == set(KARISTIRICI_SINIFLARI),
        "güç tablosu ile sınıf listesi ayrışmış — ikinci bir doğru kaynağı")
dogrula("statik-yok" in SENARYOLAR, "U1 sanity kolu (statik-yok) yok")
dogrula(set(MOBILITE_THETA_REFERANS) == set(MOBILITE_KOLLARI),
        "referans Θ tablosu mobilite kollarıyla ayrışmış")
dogrula(set(MOBILITE_THETA) == set(MOBILITE_KOLLARI),
        "Θ tablosu mobilite kollarıyla ayrışmış — bir kol Θ'sız kalırdı")
