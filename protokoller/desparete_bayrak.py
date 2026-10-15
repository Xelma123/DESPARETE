"""
DESPARETE · ablasyon bayrakları — her mekanizma ayrı bir yapılandırma bayrağı.

Kaynak: `v2/06` §5.3 · §6 (*"her mekanizma ayrı bir konfigürasyon
bayrağı"*) · `v2/03` §B1 (*"ablasyon kolu bir konfigürasyon bayrağıdır;
kod düzenlemesiyle üretilen kol kaynağından ayırt edilemez"* · *"mekanizma
sınırlarından bölünür"*). Kararlar: `v2/04` K-159.

🔒 HEPSİ AÇIK = v0.1 · VARSAYILAN BAYRAK PROFİLİ = v0.2 (K-161)
===============================================================
Bütün bayraklar açıkken davranış bayraksız gerçeklemeyle BİREBİRDİR (K-159
§3'ün ölçümü) — `PROFIL_V01`. Öğrencinin v0.2 kararı (yalın profil) üç
mekanizmayı kapatır — `PROFIL_V02`; `DESPARETE`'nin kurucusu onu varsayar.
Bugünkü DESPARETE v0.4.1 = `PROFIL_V02` + `SECENEK_V041` (K-172).
Hangi bayrağın bir ablasyon KOLU olacağı mühürde seçilir (`06` §6); v0.2'de
kapalı bir mekanizmayı AÇMAK da bir koldur.

🔒 BAYRAKLAR — mekanizma sınırı ve "kapalı"nın anlamı
=====================================================
  risk_maliyeti    `35` §4 `C_risk(R)` → 0. Postür H/U'yu yine görür (ayrı
                   mekanizma).
  kalite_maliyeti  `35` §4 `C_quality(Q)` → 0. İkisi kapalı: atlama sayısı.
  postur           `22` §7 değerlendirmesi hiç yapılmaz; doğrulama yok.
  bosta_sondalama  `20` §5 `T_idle_probe` PROBE'u yok; ACTIVE komşu yalnız
                   trafiğin kanıtıyla tazelenir.
  onarim_tamponu   `22` §8.1 — REPAIRING alana giden paket tutulmaz, düşer.
  onarim_edinimi   `23` §4.4 `StartRepair` → `StartAcquisition` yok: onarım
                   yalnız olağan ilanları bekler (en çok `T_repair_max`).
  ilan_korumasi    `20` §6.2 — seçili ilan bitmeden önceki FIELD_SOLICIT yok.
  yeniden_edinim   K-152 §2 — ULAŞILAMAZ alan kendi paketiyle yeniden
                   edinilmez. Hiç bilinmeyen hedefin İLK edinimi sürer
                   (`22` §11 madde 4: *"ilk acquisition"*).

🔒 BAYRAKLA KAPANMAYANLAR — güvenlik değişmezleri
=================================================
Uygulanabilirlik koşulu (FD) · DFSN/OIID tazeliği ve fail-closed · ACTIVE
kapısı · Hop Limit. Bunları kapatmak bir mekanizmayı ayırmaz, öteki bütün
mekanizmaların dayandığı döngüsüzlük garantisini bozar; `15` §1 politikanın
bile onları atlayamayacağını söyler.

🔒 KOL KİMLİĞİ
==============
Koşu kimliği protokolün parametrelerini İÇERİR (K-171:
`DESPARETE.kimlik_parametreleri` → `protokol_hash`). Her ablasyon kolu yine
kendi `kol` etiketini taşır; satır, düğümlerin GERÇEKTEN kullandığı
bayrakları teşhiste taşır ve analiz ikisinin uyuştuğunu denetler.
"""

from __future__ import annotations

from dataclasses import dataclass, fields

__all__ = ["Bayraklar", "TUMU_ACIK", "TUMU_KAPALI", "PROFIL_V01",
           "PROFIL_V02", "Secenekler", "SECENEK_YOK", "SECENEK_V03",
           "SECENEK_V03_EDINIM", "SECENEK_V04", "SECENEK_V041"]


@dataclass(frozen=True, slots=True)
class Bayraklar:
    risk_maliyeti: bool = True
    kalite_maliyeti: bool = True
    postur: bool = True
    bosta_sondalama: bool = True
    onarim_tamponu: bool = True
    onarim_edinimi: bool = True
    ilan_korumasi: bool = True
    yeniden_edinim: bool = True

    @classmethod
    def adlar(cls) -> tuple[str, ...]:
        return tuple(f.name for f in fields(cls))

    def degerler(self) -> tuple[bool, ...]:
        return tuple(getattr(self, ad) for ad in self.adlar())

    def kapali(self) -> tuple[str, ...]:
        return tuple(ad for ad in self.adlar() if not getattr(self, ad))


TUMU_ACIK = Bayraklar()
TUMU_KAPALI = Bayraklar(**{ad: False for ad in Bayraklar.adlar()})

# 🔒 PROFİLLER — K-161. v0.1 tasarım paketinin kendisidir (hepsi açık).
# v0.2 "yalın profil" öğrenci kararıdır (24 Eylül 2026): tam ölçekte kontrol
# yükünün doğrusal olmayan çöküşü ölçüldü; üç mekanizma BİRLİKTE kapalıyken
# hareketli kollar kâhine oranda eşiğin üstüne çıktı (K-161 §2).
PROFIL_V01 = TUMU_ACIK
PROFIL_V02 = Bayraklar(bosta_sondalama=False, onarim_edinimi=False,
                       ilan_korumasi=False)


@dataclass(frozen=True, slots=True)
class Secenekler:
    """v0.2 ÜSTÜ İYİLEŞTİRMELER (K-162 §5 · K-163 · K-164).

    Ablasyon bayraklarından AYRI: bayrakların "hepsi açık = v0.1"
    sözleşmesi bozulmasın. Hepsi kapalıyken davranış v0.2 ile BİREBİR
    (K-163'ün ölçümü). Benimsenen seçenek bir profile girer: v0.3 = V1 + V5
    + V7 (`SECENEK_V03`, öğrenci, K-164) · v0.4 = v0.3 + V8 + V10
    (`SECENEK_V04`; ajan, öğrencinin devriyle, K-167) · **v0.4.1 = v0.4 +
    V11** (`SECENEK_V041`, DESPARETE'nin varsayılanı; K-172).

      yanit_yalniz_onaysiz  V1 — PROBE_REPLY yalnız sondalayan isterse:
                            oturumun 2. ve sonraki denemelerinde (ilki
                            MAC onayıyla kanıtlanmadı demektir) PROBE
                            bayraklarının 0. biti; alıcı yalnız o bitle
                            yanıtlar. 🔴 Tel biçimi: ayrılmış bit kullanılır.
      ihtiyac_nitelik       V5 — duyulan komşu yalnız bizim için
                            UYGULANABİLİR bir FIELD_UPDATE'i varsa
                            nitelendirilir (alan/FD yok · daha yeni tur ·
                            aynı turda potansiyel < FD). Başka çerçeve
                            nitelik açmaz.
      nitelik_olcumu        V7 — yeni ACTIVE olan, henüz örneği olmayan
                            komşuya TEK ölçüm PROBE'u: onayı M0.1'in ilk
                            örneğidir (K-163 §2: v0.2'de ilk örneği karşı
                            yönün PROBE yanıtı sağlıyordu; V1/V5 onu
                            kaldırınca maliyet hiç doğmuyor, ağ kilitleniyor).
      ilan_sakla            V5a — ACTIVE OLMAYAN komşunun uygulanabilir
                            ilanı reddedilmek yerine SAKLANIR; komşu ACTIVE
                            olunca kalan ömrüyle, OLAĞAN kabul yolundan
                            (`ilan_al`: sıra · tur · uygulanabilirlik
                            denetimleri o anda) uygulanır. 🔴 `23` §4.1
                            değişikliği: güvenlik kapısı değişmez, yalnız
                            ilan bir sonraki periyodik ilanı beklemez.
                            K-164: kararlı durumda zararlı — benimsenmedi.
      hedefli_canlilik      V2+ — boşta sondalama (v0.2'de kapalı) YALNIZ
                            gerekli komşu için: bir iletilebilir alanın
                            ardılı ya da en iyi `K_YEDEK_CANLI` uygulanabilir
                            yedeği (K-165). Öteki komşu sondalanmaz, T_fresh
                            dolunca STALE olur.
      istek_tanidik         V8 — DFSN_REQUEST'i gönderen ACTIVE DEĞİLSE de
                            bana hedefli bir PROBE göndermişse ("tanıdık")
                            kabul edilir: `23` §2 AcceptPacket'in ilk kabul
                            kuralı (ACTIVE ya da bu düğüme hedefli PROBE).
                            K-150'nin tek yayını kapıyı ALICIYA koymuştu
                            ("gönderen benim için ACTIVE mi") — tasarımda
                            gönderen isteği KENDİ ACTIVE komşularına yollar;
                            ACTIVE simetrikken ikisi aynıydı, V5 simetriyi
                            bozunca istek yolu kapandı (K-166, denetim K-1).
      soru_nitelik          V9 — V5 açıkken, iletilebilir bir alanımız varsa
                            ACTIVE olmayan komşunun FIELD_SOLICIT'i nitelik
                            açar (V5'in "ihtiyaç"ı: komşu bir alan istiyor).
                            Yanıt yine yalnız ACTIVE'e (`23` §5.2) — soranın
                            tekrarında (`N_solicit = 2`). K-167: V8'in üstüne
                            6/6 koşuda zararlı — benimsenmedi.
      aclik_nitelik         V10 — V5 açıkken, alanım iletilebilir DEĞİLSE
                            (onarımda ya da ulaşılamaz) aynı turdan sonlu
                            ilan yapan komşu da nitelendirilir: yeni turdan
                            sonra ardıl adayıdır. Açlığın tanımı (`23` §5.4
                            FEASIBLE_STARVATION: ACTIVE, sonlu, aynı turda ama
                            uygulanabilir olmayan ilan) ACTIVE komşu ister;
                            V5 o komşuları hiç nitelendirmediği için açlık
                            GÖRÜNMEZ oluyor, istek "edinim" gidiyor ve hedef
                            tur artırmıyordu (K-167 §5).
      komut_ters_yol        V11 — geçitten çıkan komut, telemetrinin
                            bıraktığı GERİ İZLE taşınır (K-172). Her düğüm
                            kendisine adreslenen, geçide giden DATA'dan
                            "kaynak S'nin paketi bana j'den geldi" öğrenir
                            (`cerceve_duyuldu`, `v2/15` B1); iz yalnız DAHA
                            YENİ `kaynak_sira` ile güncellenir ve
                            `T_GERI_IZ_S` sonra bayatlar. Komut, hedefin
                            izini izler; iz yoksa düşer (`hedef_yok`). Ek
                            kontrol mesajı YOK — K-160'ta komut alanları
                            (A) kontrol yükünden çökmüştü. Kapalıyken v0.1
                            C kararı: komut `politika` ile düşer.
    """

    yanit_yalniz_onaysiz: bool = False
    ihtiyac_nitelik: bool = False
    nitelik_olcumu: bool = False
    ilan_sakla: bool = False
    hedefli_canlilik: bool = False
    istek_tanidik: bool = False
    soru_nitelik: bool = False
    aclik_nitelik: bool = False
    komut_ters_yol: bool = False

    @classmethod
    def adlar(cls) -> tuple[str, ...]:
        return tuple(f.name for f in fields(cls))

    def degerler(self) -> tuple[bool, ...]:
        return tuple(getattr(self, ad) for ad in self.adlar())


SECENEK_YOK = Secenekler()
# 🔒 v0.3 (K-164, öğrenci: "üçlüyü benimse"): v0.2 bayrakları + V1 · V5 · V7.
SECENEK_V03 = Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                         nitelik_olcumu=True)
# K-167'nin İLK adayı: v0.3 + V8 · V9 — V9 zararlı çıktı (K-167 §5).
SECENEK_V03_EDINIM = Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                                nitelik_olcumu=True, istek_tanidik=True,
                                soru_nitelik=True)
# 🔒 v0.4 (K-167 §7, ajan — öğrencinin devriyle): v0.3 + V8 · V10 — K-1'in
# düzeltmesi. DESPARETE'nin VARSAYILANI.
SECENEK_V04 = Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                         nitelik_olcumu=True, istek_tanidik=True,
                         aclik_nitelik=True)
# 🔒 v0.4.1 (K-172, ajan — öğrencinin "bulguyu düzelteceksin" talebiyle):
# v0.4 + V11 komut geri izi. DESPARETE'nin VARSAYILANI. Yukarı yön (alan,
# ardıl, postür) v0.4 ile aynı; eklenen tek şey geçitten çıkan komutun
# taşınması. Eski v0.4 = `SECENEK_V04` (komut `politika` ile düşer).
SECENEK_V041 = Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                          nitelik_olcumu=True, istek_tanidik=True,
                          aclik_nitelik=True, komut_ters_yol=True)
