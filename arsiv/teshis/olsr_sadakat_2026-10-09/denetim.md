# OLSR — RFC 3626'ya kural kural sadakat denetimi (denetim D-02, K-223)

> 9 Ekim 2026 · ajan · K-208'in kalıbıyla (AODV). Kaynak: `protokol_kaynaklari/rfc3626_olsr.txt` (ham metin). Kod: `protokoller/olsr.py` · `olsr_bicim.py` (denetim `OLSR-c` üzerinde; sonuç `OLSR-d`). ns-3'ün OLSR kaynağı depoda yok; RFC'nin sustuğu ya da çeliştiği bir yer çıkmadığı için hakeme gerek olmadı. Karar kuralı (öğrenci, K-207): SHOULD uygulanır, MAY beyan edilir, gerekçesiz sapma düzeltilir.

| § | kural (RFC) | sözü | kod | hüküm |
|---|---|---|---|---|
| 3.3 · 6.1 · 9.1 | paket 4 B + mesaj başlığı 12 B; HELLO 4 + Σ(4 + 4n), TC 4 + 4n | MUST | `olsr_bicim.py` biçimleri; boyut testle bağlı | ✅ |
| 3.4 adım 2 | TTL ≤ 0 ya da kaynak kendimizse at | MUST | `kontrol_alindi` | ✅ |
| 3.4 adım 3–4 | tekrar kümesindeyse yeniden işleme yok, (tek arayüzde) iletme yok | MUST / SHOULD NOT | `_tc_isle` taze kayıtta döner | ✅ |
| 3.4.1 adım 1 | gönderen simetrik 1-atlama komşuluğunda değilse iletme yok | MUST | `_simetrik_mi` (N_status, §14.2'li tanım) | ✅ |
| 3.4.1 adım 4–8 | MPR seçicisinden ve TTL > 1 ise ilet; TTL −1, atlama +1, başlığın gerisi aynı; tekrar kaydı D_retransmitted ile | MUST / SHOULD | `_tc_isle` | ✅ |
| 3.5 | üretim aralığı = ARALIK − U(0, MAXJITTER); iletmede U(0, MAXJITTER) bekleme | SHOULD | `Uyandirma(ARALIK − MAXJITTER, jitter=MAXJITTER)` · iletme `jitter_s` | ✅ |
| 6.2 | bağ tipi L_SYM/L_ASYM'den; komşu tipi MPR · SYM · NOT; ilan edilmemiş komşular UNSPEC_LINK | MUST | `_hello_kur` | ✅ |
| 7.1.1 | bağ girdisi oluşturma/güncelleme (L_SYM_time, L_ASYM_time, L_time = max) | SHOULD | `_hello_isle` | ✅ birebir |
| 8.1 · 8.1.1 | N_status bağlardan; N_willingness HELLO'dan | MUST · SHOULD | `_simetrik_mi` · `_hello_isle` (`_istek` sözlüğü) | ✅ |
| **8.2.1** | **2-atlama kümesi, kaynağın L_SYM_time'ı dolmamış bir bağı varsa güncellenir** | SHOULD | `_simetrik_mi` (histerezisli) kullanıyordu | 🔴 **sapma → düzeltildi** (`OLSR-d`): §14.2 histerezisli tanımı yalnız N_status, MPR ve rota tablosunun ilk adımları için ister ve *"does not modify the function of any other fields"*. K-193 farkı ölçmüş (+0,009 · −0,021 · +0,046), beyan edilmemişti. Test `test_K223_IKI_ATLAMA_…` |
| 8.3.1 | MPR buluşsalı adım 1–4 (WILL_ALWAYS · tek erişen · istek → erişim → D(y)) | MUST (per arayüz) | `_mpr_hesapla`; eşitlikte küçük kimlik | ✅ · adım 5 MAY, beyanlı |
| 8.4.1 | MPR_NEIGH ilanında seçici girdisi, MS_time | SHOULD | `_hello_isle` | ✅ |
| 8.5 | komşu kaybında 2-atlama ve seçici girdileri silinir; MPR yeniden | MUST | `_guncelle` | ✅ · ek HELLO MAY, beyanlı |
| 9.2 | ANSN kaldırmada MUST, eklemede SHOULD artar | MUST · SHOULD | `_tc_kur` | ✅ |
| 9.3 | MPR seçilen TC üretir; boş küme TOP_HOLD_TIME boyunca sürer; bağ kaybına bağlı seçici değişiminde erken TC | SHOULD | `_tc_kur` · `_guncelle` | ✅ |
| 9.5 | adım 1 simetrik olmayandan at · 2 sıra dışı · 3 eski ANSN'leri sil · 4 girdileri tazele | MUST | `_tc_isle` · `_topoloji_guncelle` (4.1'de T_seq'in ANSN'e yazılması adım 2–3'ten sonra eşdeğer) | ✅ |
| 10 | rota: h = 1 simetrik komşular · h = 2 2-atlama (WILL_NEVER hariç) · h ≥ 2 topoloji | MUST | `_rota_hesapla` | ✅ |
| 10 adım 3.2 | eşitlikte istek ve MPR seçicisi tercih | küçük harf "should" | uygulanmıyor, küçük kimlik | ⚪ beyan (normatif değil; bütün düğümler WILL_DEFAULT) |
| 13 | bağ katmanı bildirimi | MAY | kapalı (K-196) | ✅ beyanlı |
| 14.1–14.3 | histerezis: ilk duyuluş · kararlılık/kararsızlık · eşikler · uzun sessizlik | SHOULD | `_histerezis_*` | ✅ · PSN boşluğunun `MAXJITTER` beklemesi ve ilk paketin yalnız kurulum olması gerçekleme ayrıntısı, beyanlı |
| 18 | sabitler (HELLO 2 s · TC 5 s · NEIGHB_HOLD 6 s · TOP_HOLD 15 s · DUP_HOLD 30 s · MAXJITTER 0,5 s · HYST 0,8/0,3/0,5 · WILL_DEFAULT 3 · TC TTL 255) | — | `olsr_bicim.py` | ✅ |

**Sonuç:** bir gerekçesiz sapma (§8.2.1) düzeltildi; üç gerçekleme ayrıntısı ve bir normatif olmayan "should" beyan tablosuna girdi (`olsr_bicim.py`). Kod hâli **`OLSR-d`**.

**Kalan soru — K-193'ün "kötü bağ seçimi değil" hükmü:** kayıp anatomisinin bağ bandı yeniden denemeli başarıyla okunuyordu (o gün 8 deneme, K-223'ten sonra 7); OLSR'ın yayınları (HELLO · TC) tek denemeyle gider. Alet artık karar bağlarını TEK DENEME bandıyla da basıyor (`karar_bant_tek`); hüküm yeniden okunur (ölçüt `arsiv/teshis/faz4_4_k223_2026-10-09/beklenti.md`).
