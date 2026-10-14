# Regresyon k236 → k243 · denetimin (14 Ekim) kod düzeltmeleri: kalıcı görüş hattı, AODV'nin yeni sürümü, kapı sertleştirmeleri (K-242) — beklenti (ölçmeden önce)

> 14 Ekim 2026 · tetik: K-242'nin Faz 5 öncesi işleri. Simülatör ve protokol kodu k236'dan beri şu noktalarda değişti:
>
> - **Yer–hava görüş hattı** (`sim2/kanal/yer_hava.py`, denetim DD-01): durum, her (karıştırıcı, düğüm) çifti için her saniye bağımsız çekilmek yerine, ışının tipik bina yüksekliğine indiği yer noktasının bina hücresinden (genişlik √(α/β) km, banliyöde ≈ 11,5 m) çekilir; eşik makalenin P(LoS, θ)'sı. `Konfig.a2g_durum_dilimi_s` kalktı.
> - **AODV** (`protokoller/aodv.py`, `aodv_bicim.py`, DD-04 ve RFC §6.3): yayınlarda U(0, 10 ms) titreşim (RREQ üretimi ve iletimi, HELLO, RERR; ns-3) · §6.2'nin önceki atlama ömrü ve komşuluğu · MY_ROUTE_TIMEOUT 6 → 11,2 s (RFC §10 MUST) · başarısız keşfin tampondaki paketleri düşer (RFC §6.3 SHOULD, ns-3 `DropPacketWithDst`). `AOMDV-f` aynı çekirdeği miras alır.
> - **Kapı sertleştirmeleri** (davranışı değiştirmez): `KontrolIstegi`nin doğrudan kurulumu da değer denetiminden geçer (DD-06); U1-B kayıtlı orana bağlı (DD-07); fark-içinde-fark eşleşme denetimi ve kesirli hesap (DD-08); anatomi aletinin açlık tanımı (DD-11); gecikme tavanlı `PDR_açık` hesabı (DD-03); mimari denetiminde köken eksiği bulgu ve çıkış kodu (DD-19); sızdırmazlık testi izin listesiyle (DD-05).
> - **Köken defteri:** `a2g_durum_dilimi_s` (TÜRETİLMİŞ) silindi; `aodv_uygunluk.py::_JARMROUT_IZ` (ÖLÇÜLMÜŞ), `::KAYITLI_ORAN` (ÖLÇÜLMÜŞ), `::KAYIT_BANDI` (TÜRETİLMİŞ) eklendi.

## Komutlar (dondurulmuş kopyadan, `kosu.sh`)

    py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k243
    py -3.11 -u kalibrasyon/regresyon_satirlari.py karsilastir k236 k243 --izin kimlik.kurulum_hash,konfig.a2g_durum_dilimi_s,teshis.koken_kovalari --degisen <aşağıdaki 18 vaka>
    py -3.11 kalibrasyon/mimari_denetimi.py

Süre ~70 dk (`uret`), karşılaştırma ve mimari denetimi < 1 dk.

## Ölçüt

**Davranışı değişmesi gereken 18 vaka** (`--degisen`; her biri geçerli olmalı: `korunum_tamam` · `mutabakat_tamam`):

- AODV ve AOMDV, 12 vaka: `k-statik-surekli-aodv` · `k-statik-surekli-aomdv` · `r-referans-statik-surekli-aodv` · `t-statik-surekli-aodv-dugum_kaybi` · `u-birincil-aodv` · `u-birincil-aomdv` · `u-gorev-surekli-aomdv-esler_arasi` · `u-statik-aldatici-aodv` · `u-statik-reaktif-aodv` · `u-statik-surekli-aodv-cephe_hatti` · `u-statik-surekli_darbeli-aodv` · `u-statik-taramali-aodv`.
- Referans dünyada yerdeki karıştırıcıyla (derin sızma, cephe hattı), AODV dışı, 6 vaka: `u-birincil-desparete` · `u-birincil-en_guvenilir_kahin` · `u-birincil-evre-en_guvenilir_kahin` · `u-birincil-jarmrout` · `u-birincil-olsr` · `u-birincil-olsrv2`.

**Öteki 67 vaka bulgusuz** (`BIREBIR`). İzinli farklar yalnız:

- kod kimliği (`arac_hash`, `kosu_kimligi`, `protokol_hash`; araç otomatik geçer);
- `kimlik.kurulum_hash`: `Konfig`ten bir alan kalktı, bütün vakalarda değişir;
- `konfig.a2g_durum_dilimi_s`: alan satırdan kalkar;
- `teshis.koken_kovalari`: her satırda yalnız `OLCULMUS` 17 → 19; öteki kovalar aynı (TÜRETİLMİŞ 67'de kalır: bir kayıt silindi, bir kayıt eklendi).

Bu 67 vakadan biri metrikte ya da hamda değişirse, değişiklik ilan edilmemiş bir yola dokunmuştur; sebebi bulunmadan devam edilmez. 18 vakadan biri değişmezse ilan edilen değişiklik o yola ulaşmıyordur; o da incelenir.

**Mimari denetimi:** `Yapisal ihlal YOK`, çıkış kodu 0.

## Öngörüler (ölçüt değil)

- Yerdeki karıştırıcılı birincil hücre vakalarında (kısa pencere) karıştırıcının etkisi zamanda daha kararlı olur: durum artık saniyede bir yeniden çekilmez. PDR'nin yönü önceden bilinmez; ortalama kayıp aynı olasılıktan türer.
- AODV vakalarında titreşim yayın çarpışmalarını azaltır (PDR yukarı), başarısız keşfin paketlerinin düşmesi tampondan geç teslimi keser (PDR aşağı); net yön vakaya bağlıdır.

## Ön koşu (ölçüt değil)

Üç vaka bugünkü çalışma ağacıyla tek başına koşuldu (çökme denetimi; betik oturumun geçici dizininde, `regresyon_satirlari._kos` ile, k236 satırına karşı alan alan):

| vaka | süre | geçerli | k236'ya göre farklı alan | metrik farkı | `pdr_pencere` |
|---|---|---|---|---|---|
| `u-statik-surekli-aodv-cephe_hatti` | 235 s | evet | 197 | 133 | 0,6819 → 0,7610 |
| `u-bagimsiz-surekli-olsrv2-dugum_kaybi` | 15 s | evet | 8 | 0 | 0,0 → 0,0 |
| `u-birincil-evre-en_guvenilir_kahin` | 672 s | evet | 126 | 95 | 0,8137 → 0,8231 |

Değişmemesi gereken OLSRv2 vakasında farklı alanlar yalnız kod kimliği, her koşuda değişenler, `kimlik.kurulum_hash`, `konfig.a2g_durum_dilimi_s` ve köken sayımı — yukarıdaki izin listesiyle aynı.
