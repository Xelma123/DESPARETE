

# K-183 · 🟢 FAZ 4.0 — kâhin referans dünyayı görür · araçlar referans dünyada · iki kırık araç onarıldı · Bianchi referansta
> 26 Eylül · Faz 4 (öğrenci onayı: 4.1–4.3) · gerçekleme ve ölçüm ajan · beklenti ölçmeden önce `arsiv/teshis/faz4_2026-09-26/0_hazirlik_beklenti.md`

**1 · Kâhin grafiği** (`kalibrasyon/kahin.py`) — referans dünyanın üç gerçeğini görmüyordu; üçü de anahtara bağlı, eski dünya birebir:
- **ED susturması (güç kipi):**
  - Karıştırıcı enerjisi ED eşiğini aşan verici kanalı alamaz; i→j bağı yoktur.
  - Onay kanal dinlemeden gider, bu yüzden yalnız verici kilitlenir ve grafik yönlü olur.
  - Susturma kuralı `Dugum._guc_mesgul_mu`nun karıştırıcı dalının aynısı. Aldatıcı için "gürültünün üstünde" yaklaşımı kullanılır (beyan).
- **Hız uyarlaması:** bağ ARF tabanında (1 Mb/s) ölçülür. K-181 ayrıştırması gösterdi ki zayıf bağ oraya iner ve ayakta kalır.
- **Kesme mesafesi:** simülatörün duyma kümesiyle aynıdır (`duyanlar_menzili_m`). Girişim menzilinde (5,97 km) kesseydi kâhin 1 Mb/s'in uzak bağlarını atardı.
- ⚠️ **Beyan:** eski dünyada da kâhin aldatıcının CSMA susturmasını görmüyordu. O dünya deneyde kullanılmayacağı için değiştirilmedi.

**2 · Dünya seçimi** (`kalibrasyon/dunya_secimi.py`, yeni):
- Araçlar `--dunya referans_2026` alır; havuz işçileri seçimi ortamdan devralır.
- Çıktılar `_referans_2026` sonekiyle yazılır; eski kayıtlar ezilmez.
- Uyarlanan araçlar: `calisma_noktasi`, `karistirici_gucu` (tohumlar havuzda; `mesafe` bölümü), `li_replikasyonu`, `yere_toplama_yuku`, `theta_kollari`, `pdr_tavani`, `aodv_uygunluk`.
- **Ölçütlerin hiçbiri değişmedi**; değişen dünya ve tarama aralıklarıdır.

**3 · 🔴 İki kırık araç** (ajan kusuru, Faz 4.0'da bulundu):
- `li_replikasyonu` ve `iki_cift`, `Kurulum`u elle kuruyordu ve A5/C1'in alanlarını almamıştı; iki çift ayrıca yere toplamanın alanını da almamıştı.
- İkisi de `TypeError` ile **kurulamıyordu** (`kirik_araclar_once.txt`). Son koşumları eskiydi, kimse fark etmedi. Sınıf aynı: "üretici var, koşmuyor".
- Düzeltme: duyma/gecikme türetimi `kurulum.py::duyma_turetimi`de tek yerde. Araçlar formülü kopyalamaz, onu çağırır.
- İki araç her takımda kurulur ve kısa koşar (duman testi).

**4 · `analiz/`** (Faz 6'nın katmanı, erken): K-184.

**Ölçüm:**
- **Bianchi referans dünyada** (`b_bianchi.py`): n = 5/10/20/40'ta ölçülen ile analitik arasındaki bağıl fark %−0,6 · −0,5 · −0,0 · +0,3 (eşik ±%15). Eski dünyayla aynı kalite.
- Tam takım: (doldurulacak) · regresyon `k182 ↔ k183`: (doldurulacak)
