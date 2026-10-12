# Faz 4b kapanış ölçümleri, ikinci kuyruk — JarmRout'un U1 açıklaması, kopya kuralı ve çizelgeli evre kapıları — beklenti (ölçmeden önce)

> 12 Ekim 2026 · K-238 · ilk kuyruk `arsiv/teshis/faz4b_kapanis_2026-10-11/` (U1 iki desende tamam; G1ç ve G2ç yürütücünün kararıyla durduruldu) · JarmRout'un incelemesi `arsiv/teshis/jarmrout_sel_2026-10-12/inceleme.md` · kod `JarmRout-b` · `OLSRv2-b` (değişmedi).

## Önceden bilinen (ölçüt değil)

- **OLSRv2 U1:** iki desende temiz geçti (yere toplama oranları 0,76–0,96; eşler arası 0,79–0,97). U1-U ✅ · U1-B ✅.
- **JarmRout U1:**
  - U1-U eşler arası desende kâhin aşımı yüzünden kaldı: statik-yok 1001 oranı 1,013 (> 1 + R), formasyon-yok 1000 oranı 1,008 (< 1 + R).
  - U1-B iki desende kaldı: yere toplamada 11 hücre, eşler arasında 5 hücre eşik altında.
  - İnceleme sebebi ölçtü: makalenin yinelenen RREQ kuralının seli, toplu akışta tıkanıklık çöküşü üretiyor.

## Kuyruk (`kuyruk.sh`, dondurulmuş kopyadan)

1. **Paralel** (~11 sa; JarmRout koşularıyla sınırlı):
   - (a) kopya payı: `kopya_payi.py statik-yok 1001 esler_arasi 0.9827` (~15 dk);
   - (b) temsilci anatomiler, yere toplama, her kolda oranı en düşük hücre: `kayip_anatomisi.py --dunya referans_2026 --sinif yok --protokoller jarmrout --isci 1` ile statik 1002 · bağımsız 1000 · görev 1000 · formasyon 1000;
   - (c) G1ç: `DESPARETE_DUNYA=referans_2026 evre_metrikleri_kapilari.py 1c`.

   Adım ~12 süreçle başlar ve bir saat sonra 6'ya iner. Sonuçlar deterministiktir; eşzamanlılık yalnız süreyi etkiler.
2. **G2ç + G4ç:** `… evre_metrikleri_kapilari.py 2c` (~5 sa).

## Ölçütler

### A · Kopya kuralı (K-238)
Kopya gönderen bir protokolde kâhin aşımı iki şartla açıklanmış sayılır:
- mimari denetimi kâhin sızıntısı bulmuyor (bugün ihlal yok);
- yalnız kopyayla teslim edilen paketler (aslı hedefe hiç varmamış) çıkarılınca oran ≤ 1 + R (R = 0,0126).

Uygulama:
- **statik-yok 1001:** ölçülür. Sağlanırsa `KAHIN_ASIMI_ACIKLANMIS`a kayıt girer; sağlanmazsa yazılım hatası aranır ve JarmRout donmaz.
- **formasyon-yok 1000:** aşım R'den küçük; K-224'ün kuralıyla zarf adımı gerekmez, kayıt ölçümü yazar.
- **Önkoşul:** betiğin bastığı PDR, U1 kaydıyla (0,9954) birebir olmalı. Değilse ölçüm geçersiz.

### B · JarmRout'un düşük hücreleri (K-238'in açıklama kuralı)
Her temsilci anatomi şu dördünü sağlamalı:
1. korunum ve mutabakat tamam; çelişki ve atfsız düşüş yok;
2. döngü/TTL düşüşü 0;
3. `rotasiz_paket` 0;
4. sel izi:
   - RREQ yeniden yayınının üretilen RREQ'ya oranı 39'dan büyük (40 düğümde DSR'nin üst sınırı);
   - RERR > 0;
   - en büyük düşüş sebebi tıkanıklık mekanizmasıyla uyumlu (iletim başarısızlığı · kuyruk taşması · rota yok ya da tampon).

Dördü de sağlanırsa:
- yere toplamanın 11 ve eşler arasının 5 düşük hücresi `ACIKLANMIS_DUSUK_REFERANS`a girer;
- her hücrenin metni U1 kaydındaki çöküş izini yazar (rota tamponu girişi ve tepe doluluğu);
- kayıtlar `hukum` ile yeniden değerlendirilir.

Biri tutmazsa kusur aranır, JarmRout donmaz. Eşler arası keşifsel (K-218); düşük hücreleri bulgu kalır.

### C · Çizelgeli evre kapıları (değişmez, `v2/08` §08)
- **G1ç:** M4 yanlış tespit ≤ 1/8 koşu; M1 2 SE dışında ≤ 1/4 protokol; D'si iki tohumda dışarıda protokol yok.
- **G2ç + G4ç:** kâhinin M1'i etkili ve D'si boş kolunkine göre 2 SE içinde; her protokolde p99 < açık süre.
- Kalan kapı Faz 5'ten önce teşhis edilir. JarmRout yüzünden kalırsa sebep ölçülür ve yürütücüye bildirilir.

## Donma (yeni K)

Şu dört şart tutarsa `JarmRout-b` ve `OLSRv2-b` donar ve `tests2/test_donma.py`ye bağlanır; ardından tam takım ve mimari denetimi:
- A sağlandı;
- B'nin dört anatomisi geçti;
- iki protokolde U1-U ✅ (kopya kuralıyla);
- G1ç ile G2ç + G4ç geçti.

## Öngörüler (ölçüt değil)

- Kopya payı: statik-yok 1001'de aşım 0,013; yalnız kopyayla teslimin binde 13'ten fazla olması beklenir.
- Anatomilerde en büyük düşüş iletim başarısızlığı ya da tampon. RREQ başına yeniden yayın 60–80 (incelemenin hücresinde 70–78).
- G4ç: JarmRout'un p99'u keşif bekleyişleri yüzünden yüksek olabilir.
