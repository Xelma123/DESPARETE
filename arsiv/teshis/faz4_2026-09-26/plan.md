# Faz 4 · Referans dünyada yeniden kalibrasyon ve doğrulama — çalışma planı

> 26 Eylül 2026 · ajan · öğrenci onayı: 4.1 ve 4.2 koşumları (2,5–5 sa); 4.3'ün uzun taban protokol koşuları da onaylı. 4.3 sürerken ajan koşunun kullanmadığı işlerle devam eder (öğrenci: "boş durma").

## İlkeler

- **Ölçütler değişmez; yalnız dünya değişir.** Her araç eski dünyada ilan ettiği ölçütü korur (`calisma_noktasi` · `karistirici_gucu` · `yere_toplama_yuku` başlıkları). Değişen yalnız birimler ve tarama aralıklarıdır.
- **Beklenti her ölçümden önce yazılır:** `arsiv/teshis/faz4_…/<adim>_beklenti.md`.
- **Uzun koşular dondurulmuş bir kod kopyasından** koşulur. Ana depoda iş sürerken koşunun kimlik özetleri karışmaz.

## 4.0 · Hazırlık — kod, uzun koşu yok

1. **Kâhin grafiği referans dünyayı görmeli** (`kalibrasyon/kahin.py`). İki eksik var; ikisi de anahtara bağlı, eski dünya birebir kalır.
   - **ED susturması.** Güç kipinde, karıştırıcıdan aldığı enerji ED eşiğini aşan verici kanalı alamaz; bağı i→j kullanılamaz. Onay kanal dinlemeden SIFS sonra gider, bu yüzden yalnız verici tarafı kilitlenir.
   - **Hız uyarlaması.** Bağ kalitesi ARF'nin tabanında, yani 1 Mb/s'de ölçülür. Zayıf bağ gerçekte oraya iner (K-181 ayrıştırması: MAC vazgeçmesi 135 → 0).
2. **Dünya seçimi.** `kalibrasyon/dunya_secimi.py` ve her araçta `--dunya referans_2026`. Havuz işçileri seçimi ortam değişkeninden devralır.

## 4.1 · Çalışma noktası (onaylı, 1,5–3 sa)

| adım | araç | ölçüt (değişmez) | referansta değişen |
|---|---|---|---|
| a | `calisma_noktasi` | sert kısıt: statik kolda 30 tohumda kopukluk %0 · amaç: atlama derinliği en büyük | alan taraması km ölçeğinde (4–12 km); bağ ARF tabanında |
| b | `karistirici_gucu` | sert kısıt: 30 tohumda birden fazla çok üyeli bileşen yok · amaç: ρ en büyük | güç EIRP olarak (10–40 dBm); ρ kâhin grafiğinde ED susturması dâhil; gerekirse konum/mesafe |
| c | `yere_toplama_yuku` | karıştırıcısız kâhin PDR ≥ 0,95 tutan en büyük telemetri hızı (eksen dengesi korunur) | — |
| d | `theta_kollari` · bölünme tablosu | mevcut tanımlar | referans hız ve alan |

## 4.2 · Doğrulama (onaylı, 1–2 sa)

- **Bianchi:** yuva düzeneği referansın zamanlamalarıyla (±%15).
- **Li:** zincir referans menziliyle. Öngörü önceden yazılır: işlem kazancıyla girişim/iletim oranı düşer, H1 banda yaklaşır.
- **PER eğrileri:** 1/2/5,5/11 Mb/s, G1'in (Pei & Henderson) kapalı formlarıyla bağımsız karşılaştırma; ölçümden sapma beyanı (1 Mb/s ~2 dB).
- **ED-CCA sınavı:** sürekli karıştırıcı yanında vericinin ertelemesi, analitik susturma payıyla (`ed_payi.py`).
- **Kâhin tavanı:** `pdr_tavani` referansta.

## 4.3 · Taban protokoller (onaylı, 12–27 sa)

- AODV/OLSR/AOMDV uygunluğu (`aodv_uygunluk`) referans dünyada, iki desende.
- Sonra **taban protokoller donar.**
- Koşu sürerken ajan şunlarla ilerler (hiçbiri koşunun kodunu değiştirmez):
  - `analiz/` katmanı (Faz 6);
  - Faz 5.0 kayıp anatomisi aracı;
  - ön-kayıt taslakları;
  - kaynakça açıkları.

## 4.4 · Kapanış

- Yeni regresyon tabanı.
- Doğrulama listesinin tamamı bir kez (4–6 sa, ayrıca sorulur).
- SINANMAMIŞ borcunun kaynağa bağlanabilen kısmı kapatılır.

## İlerleme (26 Eylül akşamı)

- 4.0 ✅ K-183 (kâhin · araçlar · iki kırık araç · Bianchi referansta ±%0,6) · `analiz/` ✅ K-184
- 4.1a ✅ alan 35 km (K-185, öğrenci: gerçekçilik önce)
- 4.1b ✅ K-186:
  - hava karıştırıcısı (1–5 W) sürüyü her geometride böler;
  - yer/araç karıştırıcısı 10 W'ta kısmi kalır;
  - öğrenci birincil hücreyi `derin_sizma` 10 W seçti;
  - ölçü kusuru düzeltildi: yönlü grafikte güçlü bileşenler.
- 4.1c ⏳ yük (`d_yuk_beklenti.md`) · 4.1d ⏳ Θ kolları, bölünme tablosu, görev yarıçapı (35 km'de)
- 4.2 ⏳ Li (araç onarıldı) · PER · ED-CCA · kâhin tavanı
- 4.3 ⏳ taban protokoller (uzun; dondurulmuş kopyadan)

## Öğrenci kararı (27 Eylül, öğlen)

> "önerdiğin gibi yapalım da kalan işler bittikten sonra"

- U1 **eşler arası** deseni önbellekli kodla (K-190) koşulur; tahmini 10–17 sa, bandı aşar ama onaylandı.
- Sıra: yere toplama (OLSR, AOMDV) → kalan işler (K-190 kaydı, AODV düşük hücrelerinin açıklaması, birincil hücrede kayıp anatomisi) → **en son** eşler arası U1.
