"""
KAPSAM BEYANI — her sonuç satırı kendi sınırlarını taşır.

Şartname karşılığı: `v2/07-SIMULATOR-TASARIMI.md` §12 *(KAPSAM DIŞI — beyan
edilir, gizlenmez)*.

🔴 NEDEN SATIRIN İÇİNDE, BELGENİN İÇİNDE DEĞİL
==============================================
Kapsam sınırları bugüne kadar yalnız şartnamedeydi. Bir `.jsonl` satırı
aylar sonra açıldığında — ya da `analiz/` katmanı onu okurken — hangi
sınırlarla üretildiği **satırdan okunamıyordu**. Bir sayının yanında kendi
sınırı yoksa, o sayı olduğundan geniş okunur.

🔒 İKİ LİSTE VAR VE FARKLARI ÖNEMLİ
===================================
  · `MODELLENMEYEN`  — aletin YAPISAL sınırları. Elle yazılır, şartname
    §12'nin aynasıdır. Bir gün biri hız uyarlaması eklerse buradan da
    silmek zorundadır; unutulursa satır YANLIŞ beyan eder.
  · `bu_kosumda_kapali()` — KONFİGDEN TÜRER, bayatlayamaz. Sönümlemesi
    kapalı bir koşu bunu kendi satırında söyler; kimsenin hatırlamasına
    gerek yoktur.

⚠️ İkincisi birincisinden daha güvenilirdir ve bu bilinçlidir: elle yazılan
her liste bayatlar. Birincisi de bir gün türetilebilir hâle gelmeli — ama
"hız uyarlaması YOK" gibi bir cümlenin kodda karşılığı bir alan değil, bir
YOKLUKTUR ve yokluk türetilemez.

🔴 A8 (K-181) — YOKLUK ARTIK BİR ANAHTAR. Faz 1 (`v2/15` A2–A5) dört
sınırı anahtarın arkasında modelledi, ama bu liste güncellenmedi: anahtarı
açık koşular da "hız uyarlaması yok" diye YANLIŞ beyan ediyordu (tam olarak
yukarıdaki uyarı). Artık `_ANAHTARLI` o sınırı satırın kendi konfiginden
okur: anahtar açıksa sınır o satırda beyan edilmez.

🔴 BURASI BİR MAZERET LİSTESİ DEĞİL. Her satır, o sınırın sonucu HANGİ YÖNE
çektiğini söyler — çünkü "yayılma kazancı yok" demek yetmez; okuyucunun
bilmesi gereken şey, bunun karıştırıcıyı olduğundan GÜÇLÜ gösterdiğidir.
"""

from __future__ import annotations

from sim2.yapilandirma.senaryolar import bolunme_payi, mobilite_theta

__all__ = ["MODELLENMEYEN", "modellenmeyen", "bu_kosumda_kapali",
           "kapsam_bolumu"]

# ===========================================================================
# YAPISAL SINIRLAR — şartname §12'nin aynası
# ===========================================================================
# Biçim: (ne yok, sonucu HANGİ YÖNE çekiyor)
MODELLENMEYEN: tuple[tuple[str, str], ...] = (
    ("hiz_uyarlamasi",
     "kötü bağda 1 Mb/s'ye düşme yok; gerçek bir savunma eksik — "
     "protokollerin hepsi bu savunmadan YOKSUN, yani kollar arası "
     "karşılaştırma korunur ama mutlak PDR olduğundan DÜŞÜK"),
    ("yayilma_kazanci",
     "11 çipli Barker'ın ~10 dB'i yok → karıştırıcı gerçekte olduğundan "
     "~10 dB DAHA ETKİLİ görünüyor"),
    ("enerji_sezmeli_cca",
     "güçlü gürültü karıştırıcısı ertelemeye yol açmıyor; yalnız aldatıcı "
     "sınıf taşıyıcı dinlemeyi tetikler"),
    ("coklu_kanal",
     "🔒 PROJENİN ÖNCÜLÜ — çözüm yönlendirme katmanında aranıyor, frekans "
     "çevikliğinde değil"),
    ("rts_cts",
     "temel erişim; Bianchi doğrulaması da temel erişim için yapıldı"),
    ("yayilim_gecikmesi",
     "600 m'de 2 µs, slotun onda biri"),
    ("arazi_engel",
     "3B geometri var, engel yok"),
    ("havadan_karistirici",
     "`hava_eslik` ailesi hava platformunu yörüngesiyle taşır ama yayılımı "
     "yer referanslı karıştırıcıyla AYNI modelle hesaplanır; hava–hava "
     "kanalı ayrıca modellenmez"),
    ("hareketli_karistirici",
     "gerçekçi hızlarda koşu içi hareket küçük (derin sızma ~32 m, hava "
     "eşlik ~300–390 m) ve ~2 000 s'lik uzun koşu yok (öğrenci kararı "
     "K-119) — hareketin etkisi olduğundan KÜÇÜK ölçülür"),
    ("patlamali_trafik",
     "CBR; gerçek telemetri patlamalıdır"),
)

# 🔒 A8 (K-181) — anahtarı AÇIK olan sınır o koşuda modellendi.
_ANAHTARLI = {
    "hiz_uyarlamasi": lambda k: k.hiz_uyarlamasi,             # A4 · K-177
    "yayilma_kazanci": lambda k: k.islem_kazanci,             # A2 · K-173
    "enerji_sezmeli_cca": lambda k: k.tasiyici_dinleme == "guc",  # A3 · K-174
    "yayilim_gecikmesi": lambda k: k.yayilim_gecikmesi,       # A5 · K-175
}


def modellenmeyen(konfig) -> dict[str, str]:
    """Bu satırın yapısal sınırları: `MODELLENMEYEN` eksi anahtarı açık
    olanlar. Varsayılan konfigde (`olcek_1_50`) liste tam."""
    return {ad: yon for ad, yon in MODELLENMEYEN
            if not (ad in _ANAHTARLI and _ANAHTARLI[ad](konfig))}


def bu_kosumda_kapali(konfig) -> tuple[str, ...]:
    """🔒 KONFİGDEN TÜRER — bayatlayamaz.

    `MODELLENMEYEN` elle yazılır ve bir gün yanlışlanabilir; burası
    yanlışlanamaz, çünkü satırın kendi konfigürasyonunu okur.
    """
    kapali: list[str] = []
    if not konfig.golgeleme_acik:
        kapali.append("golgeleme")
    if not konfig.sonumleme_acik:
        kapali.append("sonumleme")
    if not konfig.anten_deseni_acik:
        kapali.append("anten_deseni")
    if not konfig.yakalama_etkisi_acik:
        kapali.append("yakalama_etkisi")
    if konfig.karistirici_sinifi == "yok":
        kapali.append("karistirici")
    if not konfig.hareketli:
        kapali.append("mobilite")
    return tuple(kapali)


def kapsam_bolumu(konfig) -> dict[str, object]:
    """Sonuç satırının `kapsam` bölümü."""
    return {
        "modellenmeyen": modellenmeyen(konfig),
        "bu_kosumda_kapali": bu_kosumda_kapali(konfig),
        # 🔴 Karıştırıcının açılma anı BURAYA DA yazılır ve bilerek:
        # evre metriklerinin tamamı ona bağlı, ve bir satır okunurken
        # "hangi ana göre şok" sorusunun cevabı satırın içinde olmalı.
        "karistirici_baslangic_s": konfig.karistirici_baslangic_s,
        # 🔒 A7 (K-178) — satır hangi dünyadan: sayılar dünyalar arasında
        # karşılaştırılamaz (birimler, güç, menzil farklı).
        "dunya": konfig.dunya,
        "olcum_penceresi_s": konfig.olcum_penceresi,
        # 🔒 Y7 — Θ her taban protokol için AYRI (`v2/07` §03.3). Üçüncü
        # sayı, Θ'nın kolu ne kadar TEMSİL ettiğini söyler: hiç kopmayan
        # çift oranı yüksekse Θ yalnız eşiğin kıyısındaki çiftlerden
        # hesaplanmıştır ve aşağı yanlıdır (formasyon kolu, K-122).
        **dict(zip(("theta_olsr", "theta_aodv", "theta_kopmayan_oran"),
                   mobilite_theta(konfig.mobilite_kolu, konfig.dunya))),
        # 🔴 B6 (K-132) — BU TOHUMDA AĞ BÖLÜNMÜŞ MÜYDÜ.
        # Çalışma noktası kopukluk uçurumunun kenarında (K-125) ve ölçüldü:
        # ana deney tohumlarının 15 (kol, tohum) çiftinde ağ ölçüm penceresi
        # içinde bölünüyor. Böyle bir koşuda teslim kaybının bir kısmı
        # YÖNLENDİRMEDEN BAĞIMSIZDIR; satır bunu söylemezse okuyucu onu
        # protokole yazar.
        # 🔒 `None` = ÖLÇÜLMEDİ (kalibrasyon tohumu), `0.0` = ölçüldü ve
        # bölünme yok. Tablo ve sınırları `senaryolar.py`de.
        "bolunme_payi": bolunme_payi(konfig.mobilite_kolu, konfig.tohum,
                                     konfig.dunya),
        "trafik_deseni": konfig.trafik_deseni,
        # 🔒 K-131 — rota bekleme tamponu SİMÜLATÖRÜN sağladığı bir imkândır,
        # protokolün değil: bütün kollarda aynıdır ve iki tavanı da satırda
        # beyan edilir. Beyan edilmeseydi, tamponu dolduran bir protokolün
        # kaybı ile tamponu olmayan bir protokolün kaybı aynı sütunda okunur
        # ve farkın nereden geldiği satırdan görülemezdi.
        "rota_tamponu": {
            "kapasite_paket": konfig.rota_tamponu_kapasitesi,
            "omur_s": konfig.rota_tamponu_omru_s,
            "kaynak": "ns-3 AODV `RequestQueue` varsayılanları (64 paket · "
                      "30 s), köken KAYNAK (K-198); birincil hücrede "
                      "bağlamıyor (K-200)",
        },
        # 🔒 Y5b — karıştırıcı kümesinin biçimi ve ailenin sınırları (K-119).
        "tehdit_senaryosu": konfig.tehdit_senaryosu,
        **({"tehdit_sinirlari": {
            "yerlesim": "eşit aralık ve simetriden türetildi; geçit konumu ve "
                        "trafik deseninden bağımsız",
            "guc": "toplam ORTALAMA yayılan güç tek merkezle eşit; tepe = "
                   "1 / (K × açık oranı); ρ bir sonuç",
            "hizlar": f"kaynaksız varsayım: araç "
                      f"{konfig.tehdit_arac_hiz_kmh:g} km/h · hava "
                      f"{konfig.tehdit_hava_hiz_kmh:g} km/h",
            "uzun_kosu": "yok — hareketin koşu içi etkisi yayın düzeni ve "
                         "hava geçişiyle sınırlı ölçülür",
        }} if konfig.tehdit_senaryosu != "tekli_merkez" else {}),
        # 🔒 Yere toplamanın beş riskinden dördü satırda beyan edilir
        # (`v2/07` §18 Y4, öğrencinin dürüstlük ve gerçekçilik şartı).
        **({"desen_sinirlari": {
            "gecit_yer_bagi": "ideal — uçtan uca teslimi olduğundan İYİ "
                              "gösterir; bütün kollarda ortak, sıralamayı "
                              "değiştirmez",
            "yer_istasyonlu_mimari": "yok — sonuçlar röle İHA geçitli sürü "
                                     "için geçerli; hava–yer kanalı "
                                     "doğrulanmadı",
            "tek_gecit_darbogazi": "kaybın bir kısmı yönlendirmeden bağımsız "
                                   "olabilir; ayrımı `teshis.kayip_yeri`",
            "telemetri_hizi": "kaynaksız; yük ölçütle seçilir (`v2/02` §S4)",
        }} if konfig.yere_toplama else {}),
    }
