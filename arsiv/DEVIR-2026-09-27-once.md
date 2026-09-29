# DEVİR — kısa devir notu

> **Güncel: 25 Eylül 2026.** Yalnız ajandan ajana devir içindir; güncel bilgi `v2/` belgelerinde, çelişirse onlar geçerli. Devralana verilecek mesaj: `DEVIR-PROMPT.md`. Önceki uzun sürüm (tarihçe, eski taban zinciri, AODV kod hâli tabloları): `arsiv/DEVIR-2026-09-25.md`.

---

## 1 · Durum

- **Aşama 1–2 bitti (22 Eylül), Aşama 3 sürüyor. 25 Eylül akşamı yön değişti (K-168):** önce gerçekçilik (1:1 kaynaklı taktik sürü, işlem kazancı, ED-CCA, gerçek telsiz gözlemleri), sonra DESPARETE'nin karıştırmayı çözmesi. Onaylı plan Faz 0–7 → `v2/12` (tek kaynak): §1 durum · §3 fazlar · §4 öğrenci kararları. 25 Eylül'e kadarki bütün ölçümler **eski dünyanın** (1:50).
- **Kod hâlleri:** `AODV-e` (K-145) · `OLSR-b` (§13 ile, K-147) · `AOMDV-a` (K-149) · **DESPARETE v0.4.1** (varsayılan `PROFIL_V02` + `SECENEK_V041` = v0.4 + V11 komut geri izi, K-172) · v0.4 (`SECENEK_V04`, K-167; v0.3 = `SECENEK_V03`, v0.2 = `SECENEK_YOK`, v0.1 = `PROFIL_V01` + `SECENEK_YOK`). Bir tablo hangi kod hâline ait olduğu yazılmadan başka bir tabloyla karşılaştırılmaz.
- **Faz 0 bitti** (referans dünya `v2/14` K-169 · yapı paketi `v2/15` K-170, ikisi onaylı; kaynakça `v2/16`). **Faz 1 sürüyor, `v2/15` §E sırasıyla:** A1 ✅ (K-171) · B1+B2 ✅ öne alındı (K-172) · A2 ✅ (K-173) · A3 ✅ (K-174) · A5 ✅ (K-175) · A6 ✅ (K-176) · A4 ✅ (K-177) · A7 ✅ (K-178; referans dünya `sim2/kanal/dunya.py::referans_2026`) · B3 ✅ (K-179) · C ✅ + B4 ✅ (K-180) · A8 ✅ (K-181) → **Faz 1–3 KAPANDI.** **Faz 4 sürüyor** (öğrenci onayı 4.1–4.3; plan `arsiv/teshis/faz4_2026-09-26/plan.md`): KR-E ✅ (K-182) · 4.0 kâhin/araçlar/iki kırık araç ✅ (K-183) · `analiz/` ✅ (K-184) · karıştırıcı rejimi: hava karıştırıcısı sürüyü böler, öğrenci birincil hücreyi `derin_sizma` 10 W seçti (K-186) · Li referansta sabit hızda TUTTU, ARF bulgusu, araçların dünya tuzağı kapandı (K-187) · gölgeleme birim hatası düzeldi, alan **33 km**, görev 16 km, Θ/bölünme tabloları dünyaya ait (K-188) · 4.3 U1 referansta KOŞUYOR (K-189; `h_u1_kos.sh`, `kopya_43`) · SINANMAMIŞ 44 · `analiz/hucre.py` · `kalibrasyon/kayip_anatomisi.py` (Faz 5.0) → sıradaki: U1 yere toplama sonuçları (AODV ✓ 5,6 sa; OLSR, AOMDV koşuyor) · yavaş kayıp önbelleği (K-190, %41) · AODV düşük hücrelerinin açıklaması · birincil hücrede kayıp anatomisi · **EN SON U1 eşler arası** (öğrenci onayı 27 Eylül: "önerdiğin gibi yapalım da kalan işler bittikten sonra"). Taban `k185`. Uzun koşular dondurulmuş kopyadan (`dondur.py`). Her adımdan sonra tam takım + regresyon (izin K-170), beklenen fark önceden yazılır.
- **Açık öğrenci kararları:** `v2/12` §4 (KR-1 kâhin · KR-2 komutlar — alanlar artık satırda, K-171 · KR-D tasarım paketi). KR-E kapandı (K-182).
- ⚠️ Ana deney aleti deseni (`trafik_deseni`) ve profili her satırda açıkça vermeli; `Konfig` varsayılanı eşler arası ve `kosu_kimligi` bugün tedaviyi ayırmıyor (denetim Y-1).

## 2 · Doğrulama listesi

Depo kökünden, `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1` önekiyle. Kırmızı yanarsa önce kapının kendisini oku. Liste her **aşama geçişinde** bir kez bütün koşulur (koşulmayan kapı kapı değildir — K-129).

| # | komut | beklenen | son koşum | bant |
|---|---|---|---|---|
| 1 | `python -m pytest tests2 -q` | **`921 passed`** | 27 Eylül (1720 s, U1 ile paylaşımlı) | 15–30 dk |
| 2 | `python kalibrasyon/mimari_denetimi.py` | `Yapisal ihlal YOK` · 206 parametre: TÜRETİLMİŞ 59 · ÖLÇÜLMÜŞ 18 · KAYNAK 24 · DUYARSIZ 16 · TEDAVİ 30 · KOL TANIMI 11 · **SINANMAMIŞ 48** · borç 9 · 138 modül · D16 0 · ölü kayıt 0 · DUYARSIZ \|Δ\| 13/13. 🔴 Her `sim2/` adımından sonra koşulur — A2–A7'de koşulmadı, 9 bulgu birikti (K-180) | 26 Eylül | 1–5 dk |
| 3 | `python -u kalibrasyon/uretici_duman.py` (önce `--kapi`) | 14/14 `GECTI` · dört dal `OK` | 16 Eylül | 30–45 dk |
| 4 | `python -u kalibrasyon/bag_kumesi.py a` | `G-a` · `G-b GECTI` | 15 Eylül | 1–3 dk |
| 5 | `python kalibrasyon/karistirici_gucu.py tarama` | `SECILEN: -15.0 dBm · rho = 0.258` | 16 Eylül | 10–25 dk |
| 5b | `… karistirici_gucu.py aile` | beş aile `GECER`; ρ 0,258 · 0,142 · 0,170 · 0,240 · 0,260; çıkış 0 | 16 Eylül | 8–12 dk |
| 5c | `… karistirici_gucu.py acik_evre` | `hedef_koruma` 0,240 · `derin_sizma` 0,382 `GECER`; çıkış 0 | 16 Eylül | 3–5 dk |
| 6 | `python kalibrasyon/denetim_ornekleme.py` | 30/30 · Jaccard 1,0000 · ρ farkı 0 · 270/270 · `KAPI OZETI: 4/4 GECTI` | 16 Eylül | 10–20 dk |
| 7 | `python kalibrasyon/adim9_kapanis.py` | bölüm 1 ve 3 `HEPSI TAMAM` | 16 Eylül | 60–90 dk |
| 8 | `python -u kalibrasyon/pdr_tavani.py 1` | statik 1,000 · 0,999 · 0,996 · bağımsız 0,915 · 0,844 | 16 Eylül | 15–25 dk |
| 9 | `python -u kalibrasyon/evre_metrikleri_kapilari.py` | dört kapı `GECTI`, çıkış 0 | 16 Eylül | 50–70 dk |
| 10 | `python -u kalibrasyon/kontrol_duzlemi_kapilari.py` | `KAPI OZETI: 21/21 GECTI` · P6 yüzeyi **17/6/6** bekleniyor (B3, K-179; 16 Eylül koşumu 12/6/5 — o günden beri koşulmadı) | 16 Eylül | 16–20 dk |
| 11 | `python -u kalibrasyon/li_replikasyonu.py` (eski dünya) · `… --dunya referans_2026` + `arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py` | eski: H1 `0.0871` TUTMADI · referans A8: `0.0426` TUTMADI (ARF) · **referans sabit hız: `0.1270` TUTTU** (K-187) | 27 Eylül | 5–10 dk |
| 12 | `python -u kalibrasyon/cozunurluk.py --tohum 40` | `pdr_etx 0.0244` · `pdr_atlama 0.0316` · `KULLANILACAK ESIK R = 0.0230` · `saklanan sabit TAZE` | 16 Eylül | 10–20 dk |
| 13 | `python -u kalibrasyon/anlamlilik_sabitleri.py` | `KAPI GECTI` · eski kural 0,374–0,696 · bugünkü 0,022–0,034 | 15 Eylül | < 5 dk |
| 14 | `python -u kalibrasyon/onay_semantigi.py --kapi` · `… y2kapi kisa_2026-09-11` | dört kapı `OK` · 16/16 `BIREBIR`, `Y2 KAPISI GECTI` | 16 Eylül | 3–10 dk |
| 15 | `python -u kalibrasyon/ust_referans.py --kapi` · `… teshis` | üç kapı `OK` · `bagimsiz-surekli` 1000 PDR 0.9048 · 0.8623 · 0.9658 | 16 Eylül | 5–8 dk |
| 16 | `python -u kalibrasyon/regresyon_satirlari.py karsilastir <önce> <sonra> [--izin …] [--yeni …]` | `BIREBIR` ve çıkış 0; her `sim2/` değişikliğinden sonra, önce `uret <etiket>`; beklenen fark karşılaştırmadan ÖNCE yazılır. Geçerli taban **`k185`** (67 vaka: `k-` gerçek protokoller, DESPARETE v0.4.1; `l-` işlem kazancı; `n-` güç kipi; `o-` yayılım gecikmesi; `p-` karıştırıcı gerçekçiliği; `q-` hız uyarlaması; `r-` referans dünya, A8'den beri bütün anahtarlar açık; `s-` gözlem v2; `t-` düğüm kaybı; referans alanı 33 km, karıştırıcı 10 W, K-186/188) | 27 Eylül (`k184 ↔ k185`, 42,6 dk) | üretim 20–40 dk · karşılaştırma < 1 dk |
| 17 | `python -u kalibrasyon/onay_semantigi.py analiz kisa_2026-09-11` | PDR: çözünürlük üstünde 0 · altında 5 · karar yok 3 | 15 Eylül | < 1 dk |
| 19 | `python -u kalibrasyon/aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/<aodv\|olsr\|aomdv>_son.json` | AODV-e: U1-U 🟢 · U1-B 🟢 · 2 açıklanmış düşük hücre · OLSR-b: 0 · AOMDV-a: 1; çıkış 0. Tam koşum `… --protokol <p>` (8 işçi 2,5–4,5 sa); DESPARETE `--protokol desparete` (5–7 sa) | 25 Eylül (hüküm) | hüküm saniyeler |
| 20 | `python arsiv/dogrulama/kayit_indeksi.py --kontrol` | `indeks güncel` | 25 Eylül | < 1 s |

## 3 · Devralırken bilinmesi gerekenler

- Aşama numaralaması tek: `v2/01` §5 (eski "Faz N" o günün numarası).
- Çalışma anlaşmaları `v2/03` §1 · öğrenci kararlarının tek listesi `v2/07` §15 · karar kaydı `v2/04` (öz; tam metin `v2/arsiv/04-NEDEN-BOYLE-K090-K167.md`).
- Belgeler öz tutulur: aynı bilgi tek yerde, ötekiler atıf verir; ölçümler en kısa gerekli olanla (25 Eylül, öğrenci).
