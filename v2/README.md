# v2 — PROJE BELGELERİ

> Her bilgi tek yerde. Durum yalnız `12`de, geçerli kararlar yalnız `04`te; DESPARETE'nin güncel tasarımı `18`de ve `bilesen/`de (24 Kasım'dan beri yeniden tasarım, K-253); `17` ve `kural/` önceki tasarımdır, bugünkü kodun belgesi olarak kalır (`04` §6). Güncel: 26 Kasım 2026. Önceki hâller `arsiv/`de (git'te izlenir).
>
> Belgeler bilgi kaydıdır, doğruluğun kanıtı değildir: bir iddia kodla, ölçümle ya da birincil kaynakla sınanır. Belge ile kod çelişirse hangisinin yanlış olduğu ölçülerek bulunur (`03` §1).

| # | belge | ne anlatır |
|---|---|---|
| 01 | `01-PROBLEM-VE-AMAC.md` | problem · kapsam · özgünlük · başarı ölçütü · simülasyon–gerçeklik beyanı |
| 02 | `02-DOGRULANMIS-KAYNAKLAR.md` | açılıp okunmuş kaynaklar · literatür taramasından alınanlar (§L) · açık kaynak soruları |
| 03 | `03-YONTEM-KURALLARI.md` | bilimsel ilkeler · bu projede görülen hata sınıfları · doğrulama seviyeleri |
| 04 | `04-KARARLAR.md` | **bugün geçerli bütün kararlar**, konu konu; açık kararlar §10 |
| 05 | `05-GOZLEM-PENCERESI.md` | protokolün görebildiği her şey — sözleşme |
| 06 | `06-ON-KAYIT.md` | ön-kayıt taslağı: aileler · tohumlar · metrikler · uygunluk · eşik · istatistik |
| 07 | `07-SIMULATOR-TASARIMI.md` | simülatörün katmanları ve bugünkü modeli |
| 08 | `08-EVRE-METRIKLERI.md` | şok · toparlanma · tespit gecikmesi metrikleri ve kapıları |
| 09 | `09-LI-REPLIKASYONU.md` | aletin dış çapası: ön-kayıt ve sonuç |
| 12 | `12-YOL-HARITASI.md` | **durum ve plan** (Faz 0–7), hesap bütçesi |
| 13 | `13-KONTROL-DUZLEMI.md` | protokolün yapabildikleri — sözleşme |
| 14 | `14-REFERANS-DUNYA.md` | referans dünyanın sayıları ve kaynakları |
| 16 | `16-KAYNAKCA.md` | rapor için kaynakça (IEEE biçimi) |
| 17 | `17-TASARIM-KARARLARI.md` | **önceki tasarım:** 5-2'nin ve 5-3'ün ilk tasarımının ilkeleri ve kararları (T-1…T-20); bugünkü kodun (`desparete5*`) belgesi, `18` donunca arşive |
| 18 | `18-YENI-TASARIM.md` | **güncel tasarım:** DESPARETE'nin baştan, bileşen bileşen tasarımı (24 Kasım'dan): hedef, kısıtlar, kanıt envanteri, mimari iskelet, yöntem, eksiksizlik listesi; bileşen bileşen sorun, kanıt, seçenekler ve kararlarım |
| — | `kural/KK-*.md` | **önceki tasarımın** kural kâğıtları: `17`nin kararlarından kurallar, formüller, başlangıç değerleri ve ablasyon bayrakları (`KK-00` dizin); bugünkü kodun belgesi |
| — | `bilesen/*.md` | **güncel tasarımın** (`18`) bileşen kâğıtları (B1–B4 onaylı); değerler, bayraklar ve gözlemin kullanımı tek yerde, `bilesen/00-DIZIN.md` |
| — | `kayit/KARAR-GUNLUGU.md` | kronolojik karar günlüğü K-090…; koddaki `K-xxx` atıflarının adresi; tarihsel kayıttır, yeniden yazılmaz |

**Koddaki eski atıflar** (belgeler 28 Eylül ve 13 Ekim'de sadeleştirildi; koddaki bölüm numaraları eski sürümlerindir):
- `` `04` K-xxx `` → `kayit/KARAR-GUNLUGU.md`.
- `` `07` ``nin iki haneli bölümleri (§03.3 · §05.3.1 · §06.2 · §07.2 · §09.4 · §11.3) ve §15, §18 Yn (Y0–Y10) → `arsiv/07-SIMULATOR-TASARIMI-2026-09-25.md` (tam sürüm; `…-2026-09-28-temizlik.md` özeti).
- `` `08` §05.3 `` → `arsiv/08-EVRE-METRIKLERI-2026-09-25.md`.
- `` `12` §3 C1–C3 `` → `arsiv/12-YOL-HARITASI-2026-09-25.md`.
- `` `03` §B5 `` ve `` `03` §2.1 `` → `arsiv/03-YONTEM-KURALLARI-*.md`.
- `` `15` `` ve `` `v2/15` `` (yapı paketi, tamamlandı) → `arsiv/15-GERCEKCILIK-YAPI-PAKETI-2026-09-28-tamamlandi.md`.
- `` `10` `` → `02` §L.
- DESPARETE dosyalarındaki `protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/` yolları → `../arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/` (v0.1 taslağı, bayat; bağlayıcı olan kod).

Numara boşlukları (00, 10, 11, 15) emekli belgelerden.

**Diğer:** `../protokol_kaynaklari/` — RFC'ler, makaleler, uygulama kaynakları (künye ve SHA-256 `README.md`de) · literatür taraması (ikinci el; `02` §L).
