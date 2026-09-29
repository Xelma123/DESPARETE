# 12 · YOL HARİTASI — durum ve plan

> **Güncel:** 25 Eylül 2026. Süreler ölçüm değil **tahmin**, bant olarak; ölçülmüş sayıların yanında üretici komut. Tamamlanmış işlerin tarihçesi `04`te; önceki tam sürüm `v2/arsiv/12-YOL-HARITASI-2026-09-25.md`. Kodda geçen eski "`12` §5" atıfları (protokolsüz kapanamayan borçlar, DESPARETE'nin parça parça yazımı) bugün §3'te.

---

## 1 · Nerede duruyoruz

**📍 Aşama 3, adım 3.8** — DESPARETE v0.4'ün tam ölçek doğrulaması, sonra resmi U1.

| | |
|---|---|
| aşamalar | 1 (simülasyon) ve 2 (taban protokoller) 🟢 bitti, 22 Eylül · 3 (DESPARETE) 🟡 23 Eylül'den beri |
| taban protokoller | 🟢 `AODV-e` (K-145) · `OLSR-b` (§13 ile, K-147) · `AOMDV-a` (K-149) — U1-U geçti, U1-B'de 2 · 0 · 1 açıklanmış düşük hücre (eşler arası desende). Hüküm: `python -u kalibrasyon/aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/<protokol>_son.json` |
| DESPARETE | 🟢 gerçekleme tamam (3.1–3.7, K-152…K-159) · profil evrimi v0.1 → C (komutlar düşer) → v0.2 yalın → v0.3 → **v0.4 = v0.3 + V8 + V10, varsayılan** (K-160…K-167). v0.4: küçük dünya 300 s'de v0.2'nin teslimi, kontrol yükü v0.2'nin %57'si; **tam ölçekte doğrulanmadı** |
| test takımı | **`820 passed`** — `python -m pytest tests2 -q` (25 Eylül, 751 s) |
| regresyon tabanı | **`k157`**, 45 vaka — `python -u kalibrasyon/regresyon_satirlari.py karsilastir k151 k157` BİREBİR; `k157`'den sonra `sim2/` değişmedi. ⚠️ Matriste gerçek protokol vakası yok |
| mimari denetimi | ihlal 0 · 133 modül · 169 parametre · **SINANMAMIŞ 40** · duyarlılık borcu 9 — `python kalibrasyon/mimari_denetimi.py` |
| çalışma noktası | tek karıştırıcı −15,0 dBm, ρ = 0,258 · 1800 m · N = 40 · yük 40 pkt/s (iki desen eşit) · ana deney tohumlarının 15 (kol, tohum) çiftinde ağ pencerede bölünüyor (`kapsam.bolunme_payi`, K-132) |
| mobilite Θ_OLSR | bağımsız 3,25 · görev 3,99 · formasyon 2,31 (aşağı yanlı) · yüksek çalkantı 1,78 |
| dış çapa · çözünürlük | Li H1 = 0,0871 (tutmadı; mekanizma doğrulandı) · eşleştirilmiş R = 0,0230 (40 tohum) |

## 2 · Aşamalar ve takvim (tahmin)

| aşama | içerik | hedef | durum |
|---|---|---|---|
| 1 · Simülasyon | ölçüm ortamı, doğrulama, kalibrasyon | 26 Eylül | 🟢 16 Eylül |
| 2 · Taban protokoller | AODV · OLSR · AOMDV, U1–U4 | ~15 Ekim | 🟢 22 Eylül |
| 3 · Özgün protokol | DESPARETE gerçekleme ve kabul | Ekim | 🟡 |
| 4 · Pürüz ve veri | mühür · ana deney (40 tohum) · istatistik · keşifsel eksenler | Kasım başı–ortası | ⏳ |
| 5 · Rapor ve sunum | yazım (~5 hafta, kısaltılmaz) · görselleştirme | ~15 Kasım – 19 Aralık | ⏳ |

Bir aşama kayarsa sonrakinin başı kayar; yazım süresi kısaltılmaz. Aşama 1–2'de kazanılan süre Aşama 3'ün ölçümlerine ayrıldı.

## 3 · Açık işler

**Aşama 3 — sıradaki, sırayla**
1. ⏳ **v0.4'ün tam ölçek doğrulaması** — v0.2 ↔ v0.4, N = 40, 120 s, geliştirme tohumları, bağımsız + formasyon + karıştırıcılı birincil hücre; bant 2,5–4 sa (izinle).
2. ⏳ **`kosu_kimligi` düzeltmesi** — kimliğe tedavi alanları ve protokol/profil parmak izi (denetim Y-1; öğrenci onayı 25 Eylül); regresyon ~35 dk (izinle).
3. ⏳ **Resmi U1** (v0.4, yere toplama; 5–7 sa, izinle) ve U3.
4. ⚪ Tasarım paketinin kaynağına düzeltmeler (TV-02 · DFSN_REQUEST boyu · durum makinesindeki eksik satır) — öğrenci.
- Kapsam kararı bekleyen: Güvenlik Profili 1'in bedeli (ayrı kol) · yedekli gönderim.
- **Açık öğrenci kararları:** birincil metrikte komutlar (`06` §9 a) · kâhin kuralı okumasının teyidi (`06` §4.4).

**Aşama 2'den kalan** (ana deneyden önce)
- ⏳ Taban protokollerin yere toplamada sınanması (öğrenci, 25 Eylül).
- ⏳ Adillik ölçümleri: AODV/AOMDV'de RREP-ACK · kara liste yokluğu (karıştırmada SINR asimetrik, denetim O-1) · rota tamponu (64 paket · 30 s; AODV'de doluyor) · yeniden deneme sınırı (4; 802.11 kısa sınırı 7).
- ⚪ M4'ün boş kol kapısı · AOMDV'nin U2/U4 karşılıklarının adıyla eşlenmesi · OLSR §13'ün hareketli kolda mekanizması (hipotez) · AOMDV'nin bayat yedek yolu (S2).

**Aşama 1'den kalan** (Aşama 4'ten önce yeter; C1 düğüm sayısı K-125 · C2 çalışma noktası · C3 yere toplama yükü K-126 · C7 çözünürlük K-128 kapandı)
- C4 formasyonda Θ daha çok tohumla (10–30 dk) · C5 görev yarıçapı büyük örneklemle (1–3 sa; `calisma_noktasi.py --bolum gorev_kolu`) · C6 ısınma × ölçüm penceresi taraması (1–3 sa) · kaynak doğrulamaları: Rician K, 802.11b sabitleri (`02` §S1–S2) · SINANMAMIŞ ve duyarlılık borcu (kaynak, ölçüm ya da eksen ilanı) · B6 iz kanalı (Aşama 5).

**Aşama 4**
- 4.1 Gürültü ölçümü — üç taban × 1100–1119, birincil hücre, tam pencere → δ, güç, tohum sayısı (`06` §0.4).
- 4.2 Ön-kaydın tamamlanması — Aile 1 hipotez ve hücreleri · Aile 3'ün mekanizma kapısı ve ablasyon kolları · AOMDV öngörüsü · çekirdek matris · koşul 1'in k'si · durdurma kuralı (`06` §9).
- 4.3 Borçlar ve doğrulama listesinin tamamı (`DEVIR.md` §2, ~3,5 sa) · `algilama_duyarliligi`nin ikiye bölünmesi.
- 4.4 İstatistik katmanı `analiz/` (Wilcoxon, Holm, GA, NaN kapısı).
- 4.5 🔒 Mühür (öğrenci) · 4.6 Ana deney (2000–2039; parça parça koşulabilir, koşum bütçesi mühürde) · 4.7 Keşifsel eksenler.

**Aşama 5** — rapor (negatif sonuçlar dürüstçe) · görselleştirme (`07` §13) · simülasyon–gerçeklik beyanı (`01`) · fikir sahipliği: karar kaydı ve ablasyonla ölçülmüş katkı · poster, sunum, jüri hazırlığı.

## 4 · Kayma planı — öneri (kapsam kararı öğrencinin)

Takvim sıkışırsa düşme sırası: (1) keşifsel eksenlerin bir kısmı (görev kolu, derinlik, 2 geçit, bazı karıştırıcı senaryoları) · (2) iz kanalının zengin gösterimi · (3) çekirdek hücre sayısı. Çekirdek deney, üç taban protokol ve özgün protokol korunur.
