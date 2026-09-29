# OLSR statik düşük hücreler — teşhis ön-kaydı (22 Eylül 2026, ölçümden ÖNCE)

Gözlenen (U1 kapanışı, `olsr_son.json`): statik-yok 1000 0,926 · 1001 **0,859** · 1002 **0,866**.
AODV-e aynı hücrelerde 0,995 · 0,999 · 0,932. Kâhin 1,000 · 1,000 · 0,996.

⚠️ AODV'nin yapısal açıklaması (eşiksiz en kısa yol, 1002 en zayıf) OLSR'ın
sıralamasını AÇIKLAMIYOR: OLSR'da en düşük hücre 1001, ve AODV 1001'de 0,999.
Yani AODV'nin açıklaması OLSR'a taşınamaz.

## Hipotezler ve ayırıcı ölçü — aşama 1 (düşme sebepleri + akış başına teslim)

| # | hipotez | tür | öngörü |
|---|---|---|---|
| H1 | gri bölge: OLSR bağı HELLO'yla (kısa yayın) kabul ediyor, veri (uzun unicast) o bağda başarısız; §13 (bağ katmanı bildirimi, MAY, beyanlı) uygulanmadığı için OLSR başarısızlığa tepki vermiyor, histerezis HELLO'ya baktığı için bağı düşürmüyor | mekanizma + beyanlı sapma | kayıpların çoğu `iletim_basarisiz`; kayıp BİRKAÇ akışta yoğun (kalıcı kötü rota); AODV aynı hücrede başarısızlıktan sonra rota değiştirebildiği için iyi |
| H2 | rota tablosu boşluğu (TC kaybı / topoloji kusuru) | kusur adayı | kayıpların çoğu `hedef_yok` |
| H3 | döngü (tutarsız tablolar) | kusur adayı | `ttl` düşmesi belirgin |
| H4 | kuyruk taşması (periyodik kontrol yükü) | mekanizma | `kuyruk_tasmasi` belirgin |

Aşama 1'in sonucu hangi hipotezin sürdüğünü söyler; ikinci aşama o hipotezi
sınar (H1 için: kayıp akışların rotasındaki bağların veri teslim olasılığı).
Hiçbir eşik ve hiçbir açıklama bu ölçüme göre DEĞİŞTİRİLMEZ; bir açıklama
ancak ölçülmüş mekanizmayla yazılır, kusur çıkarsa düzeltilir.

---

## SONUÇ — ölçümden SONRA yazıldı (22 Eylül 2026)

Üreticiler bu klasörde: `python olsr_teshis.py` · `python olsr_teshis2.py` ·
`python gri_bolge.py` (sonuncusu ilkinin JSON'unu okur, simülasyon koşmaz).
Sarmalayıcı davranışı değiştirmedi: beş koşunun PDR'si U1 kaydıyla birebir.

- H2 · H3 · H4 düştü: kaybın ~%80'i `iletim_basarisiz`; `hedef_yok`un TAMAMI
  ısınmada (K2); `ttl` 3–12; kuyruk taşması 0.
- K1 · bayat rota ihlali **0** (üç tohum) — kusur adayı düştü.
- 🔴 H1'in GÜÇLÜ biçimi ÇÜRÜDÜ: önceden konan tanımla (kontrol ≥ 0,80 ve
  atlama < 0,90) gri bölge payı **%0**. Başarısız bağlarda kontrol çerçevesinin
  tek seferde geçme olasılığı 0,57–0,76 — yüksek değil. Tanım sonradan
  değiştirilmedi.
- Görülen mekanizma: RFC histerezisi (0,5 · 0,8 · 0,3) son birkaç pakete
  bakar; kontrol başarısı 0,57–0,76 olan bir bağ zamanın %53–86'sında açık
  sayılır, atlama sayısıyla yönlendirme onu tercih eder, verinin 5 denemeyle
  teslimi 0,38–0,73.
- N1 · §13 harfiyen: PDR 0,9257 → 0,9434 · 0,8589 → 0,9263 · 0,8630 → 0,9048
  (kâhine oran 0,943 · 0,926 · 0,908 — üçü de ≥ 0,90); veri başarısızlığı
  %38–58 azaldı; kontrol çerçevesi +%3–4; `ttl` 10 → 47 · 3 → 8 · 12 → 32.
