# Faz 4.5 doğrulama listesi — son kodla (7 deneme, `OLSR-d`) yeniden (ölçmeden önce)

> 10 Ekim 2026 · ajan · tetik: K-219'un listesi 8 denemeyle koşulmuştu; deneme sayısını okuyan aletler (Li zinciri, bağ kümesi, üst referans, kâhin) ve unicast kontrol düzlemi K-223'ten etkilenir. Faz geçiş kuralı (öğrenci, 29 Eylül): geride doğrulanmamış iddia kalmasın. Kopya `kopya_d` (commit'le birebir doğrulanır), `kuyruk_d.sh`, sırayla, ~2 sa.

Ölçütler K-219'unkiyle aynı (`arsiv/teshis/faz4_5_2026-10-08/beklenti.md`):

| # | komut (`DESPARETE_DUNYA=referans_2026`, aksi yazılmadıkça) | ölçüt |
|---|---|---|
| D1 | `bag_kumesi.py a` | G-a · G-b `GECTI`, çıkış 0 |
| D2 | `li_replikasyonu.py --dunya referans_2026` | aracın kendi H1'i (A8, ARF) ≈ 0,04 TUTMADI (K-187 · K-219); sayı oynayabilir, sebebi yazılır |
| D3 | `b_li_ayristirma.py <kopya>` | **A8-arf (sabit hız) H1 bantta (0,1–0,2) TUTAR**; A8 TUTMAZ. Bant dışına düşerse dış çapa iddiası (`v2/07` · `v2/09` · `v2/14`) düşer → öğrenciye |
| D4 | `kontrol_duzlemi_kapilari.py` | `KAPI OZETI` hepsi GECTI (21/21) |
| D5 | `denetim_ornekleme.py` · `denetim_ornekleme.py c` | 4/4; C referans biçiminde (ED dışarıda) 270/270 birebir |
| D6 | `ust_referans.py --kapi` | üç kapı `OK`, çıkış 0 |
| D7 | `evre_metrikleri_kapilari.py` (varsayılan; G3 referansta anlamsız, yerine B3'ün G3ç'si) | G1 · G1-P · G2 · G4 `GECTI` |
| D8 | `uretici_duman.py` (dünya ortamı yok; kesitler kendi dünyalarında) | bütün kesitler çıkış 0, kapsam kapısı temiz |

Dışarıda: `anlamlilik_sabitleri.py` (sentetik, dünyadan ve MAC'ten bağımsız) · G3ç (B3'te 7 denemeyle geçti). Kalan bir kapı Faz 5'ten önce teşhis edilir.
