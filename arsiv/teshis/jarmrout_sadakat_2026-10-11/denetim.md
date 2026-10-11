# JarmRout — Pu 2018'e kural kural sadakat denetimi (K-234)

> 11 Ekim 2026 · K-208'in kalıbıyla (AODV) · kaynak `protokol_kaynaklari/pu_2018_jarmrout_ieee_access.pdf` (§III.A–E, Şekil 2–4, Tablo 1–3); makalenin sustuğu yerde RFC 4728 (`protokol_kaynaklari/rfc4728_dsr.txt`) · kod `protokoller/jarmrout.py` · `jarmrout_bicim.py` (denetim K-233'ün hâli üzerinde). Kaynak sırası tasarım notunda (`arsiv/teshis/jarmrout_2026-10-11/tasarim.md` §1): makale harfiyen → DSR → gerekçeli seçim.

## 1 · Makalenin kuralları

| yer | kural (makale) | kod | hüküm |
|---|---|---|---|
| §III.A | konum 2B (sabit irtifa); düğüm konumunu GPS/IMU'dan bilir | `kendi_konum`un yatay bileşeni, 16 bit metre | ✓ |
| §III.B Eş. 5 · Tablo 1 | bağ kalitesi = komşudan en son alınan N_rssi paketin RSSI varyansı; küçük = kararlı | `cerceve_duyuldu` çözülen her çerçeveyi (veri, kontrol, onay) işlemeden önce raporlar; son 4 örnek; `bag_kalitesi` | ✓ Tablo 1 birebir |
| §III.B | eşit LQ'da son paketi beklenen RSSI'a (−55 dBm) yakın olan komşu | — | ○ uygulanmaz: JarmRout komşu sıralamaz; yolu hedef Eş. 13'le seçer, L_qt yolun en büyük LQ'su |
| §III.C Eş. 6 | T_busy = NAV'ın alçak geçiren süzgeci; ölçüm "son ortama erişimden" | ölçüm: önceki erişimden bu yana CCA'nın meşgul süresi, ms (beyanlı sapma: RTS/CTS yok). **Örnekleme:** her `sonraki_atlama` ve her `kontrol_alindi`da güncelleniyordu | ✗ **sapma → düzeltildi.** Alım ortama erişim değildir. RREQ selinde birkaç ms arayla gelen kopyalar ölçümü sıfıra çekiyor, taşınan T_ld'yi alımların sıklığına bağlıyordu. Süzgeç artık yalnız düğümün kendi erişimlerinde güncellenir: veri iletim kararı (kuyruk başında) ve ürettiği ya da ilettiği her kontrol çerçevesi |
| §III.C Eş. 7 | Q_buf = kuyruktaki paket sayısının süzgeci | `kuyruk_uzunlugu`, Eş. 6 ile aynı anlarda | ✓ (düzeltmeyle) |
| §III.C Eş. 8 · Tablo 2 | TL = γ·T_busy + (1−γ)·Q_buf + (T_busy + Q_buf)·ε | `trafik_yuku`; γ 0,5 · ε 0,02 Tablo 2'den | ✓ Tablo 2 birebir |
| §III.D Eş. 9–12 · Tablo 3 | yollar arası uzaklık; size(p) kaynak ve hedef hariç | `yol_uzakligi`; konumlar RREQ'nun P_coord'u | ✓ Tablo 3 birebir |
| §III.E ¶1 | kaynak rota tablosunda rota yoksa RREQ yayınlar | `sonraki_atlama` → bekletme + `_kesif_baslat` | ✓ |
| Şekil 2 | RREQ: S_id · D_id · pkt_seq · C_hop · H_route · P_coord · L_qt · T_ld | `RREQ` (19 + 8n bayt) | ✓ boyut testli |
| §III.E ¶1 | ara düğüm, ilk RREQ: pkt_seq ve C_hop önbelleğe; gönderenle LQ ve kendi TL'si; büyükse L_qt/T_ld değişir; kimliği ve konumu eklenir; C_hop +1; yeniden yayın | `_rreq_isle` | ✓ |
| §III.E ¶1 | yinelenen RREQ: taşınan C_hop önbellektekinden büyükse at; değilse aynı işlem ve yeniden yayın | `_rreq_isle`; önbellek ilk alıştaki değerde kalır (makale yalnız ilk alışta önbelleğe alır) | ✓ |
| §III.E ¶1 | ara düğüm önbellekten RREP veremez | ara düğümde rota önbelleği ve önbellekten RREP yolu yok | ✓ |
| §III.E ¶2 | hedef ilk RREQ'yu kaydeder, `t_wait` bekler; yinelenen RREQ kayıtlı her yolla ortak ara düğümü yoksa kaydedilir, varsa atılır; ilk varan yol önceliklidir | `_hedefte_kaydet` (varış sırasıyla) | ✓ |
| §III.E ¶2 Eş. 13 · Şekil 3 | `t_wait` dolunca her çift için P_prio; en küçük çift; iki RREP ters rotayla | `_yol_sec`; eşitlikte ilk bulunan çift | ✓ Şekil 3 birebir |
| §VI.A | tek yol bulunursa tek yol | tek RREP | ✓ |
| §III.E ¶2 · §VI.B | kaynak RREP'lerdeki tam rotaları önbelleğe alır, aynı veri paketini iki yoldan gönderir | `_rrep_isle` (en çok iki rota) · `Karar(rota, kopyalar, kopya_rotalari)` (K-231 · K-232) | ✓ |
| §III.E ¶3 | sonraki atlamaya sürekli teslim edemeyen düğüm bağı kopmuş sayar, kaynağa kopan bağla RERR | `iletim_basarisiz` (MAC'in 7 denemeden vazgeçmesi); RERR paketin rotasının tersinden | ✓ |
| §III.E ¶3 | kaynak kopan bağı içeren bütün yolu siler; biri kalırsa onu kullanır; ikisi de giderse yeniden keşif | `_bagi_sil` · `_gecerli_rotalar` · sıradaki pakette keşif | ✓ |
| §III.E | α · β · γ = 0,2 · 0,2 · 0,6 | `jarmrout_bicim.py` | ✓ |

## 2 · Makalenin sustuğu yerde DSR (RFC 4728)

| RFC | kural | sözü | kod | hüküm |
|---|---|---|---|---|
| §8.2.2 | rota kaydında (başlatıcı dâhil) kendi adresi varsa RREQ atılır | MUST | `_rreq_isle`nin ilk denetimi | ✓ |
| §8.2.2 · §4.3 | Route Request Table: (başlatıcı, kimlik) önbelleği, RequestTableIds 16 | MUST | `_istek` (başlatıcı başına son 16) | ✓ yineleneni atma kuralının yerini makalenin C_hop kuralı alır |
| §8.2.2 | yeniden yayın 0–BroadcastJitter (10 ms) titreşimle | SHOULD | `jitter_s=BROADCAST_JITTER_S` | ✓ |
| §8.2 · §4.3 · §9 | RREQ yeniden denemesi: RequestPeriod 0,5 s, iki katına, en çok 10 s, en çok 16 kez | SHOULD | `uyandi` | ✓ · ilk istekte yayılmayan RREQ (hop limit 0) MAY, kullanılmadı |
| §6.1 · §6.3 · §6.4 · §6.7 | DSR seçenek başlığı · Route Reply · Route Error · Source Route | MUST | `RREP` · `RERR` · `VERI_BASLIK_BAYT` + `ROTA_ADRES_BAYT` | ✓ boyut testli |
| §9 | RouteCacheTimeout 300 s | — | `_rrep_isle` | ✓ |
| §9 | DiscoveryHopLimit 255 | — | C_hop 255'te RREQ atılır (alan da 8 bit, Şekil 2) | ✓ |
| §9 | SendBufferTimeout 30 s | — | simülatörün ortak bekleme tamponu (64 paket · 30 s) | ✓ |
| §8.3.4 | en çok deneme sayısından sonra bağ doğrulanamazsa RERR paketin IP kaynağına | SHOULD | veri paketinde `iletim_basarisiz` → RERR kaynağa ✓. RREP'in iletimi başarısız olursa RERR RREP'in başlatıcısına (hedef) giderdi; hedef JarmRout'ta rota tutmaz, etkisi olmaz | ✓ veri · ○ kontrol çerçevesinin başarısızlığı yok sayılır, kaynak RREQ'yu yeniden dener |
| §8.3.6 | ara düğüm önbelleğinde başka rota varsa paketi kurtarır (salvage) | SHOULD | yok | ○ makale kopmadaki işlemi kendisi tanımlar (RERR → kaynak, kaynak yolu siler, kalan yolu kullanır); kurtarma eklenmez. Ara düğümde rota önbelleği yok (rota yalnız RREP'lerden, yalnız kaynakta) |

## 3 · Sonuç

Bir gerekçesiz sapma (Eş. 6 · 7'nin örnekleme anı) düzeltildi; davranış `tests2/test_jarmrout.py::test_YUK_SUZGECI_yalniz_kendi_erisiminde` ile bağlı (eski kod aynı girdilerle T_ld 1,04 · 3,25 · 4,225, yeni kod 0 · 1,04 · 3,12 taşır). Makalenin dört çözümlü örneği birebir. Beyan tablosunda eşitlik bozan RSSI'ın kullanılmadığı yazıldı, kullanılmayan sabit kaldırıldı; RFC 4728 bölüm atıfları düzeltildi (Route Request Table §4.3 · §8.2.2, yeniden deneme §8.2, bağ onayı ve RERR §8.3.1 · §8.3.4; eski metin §3.3'ü gösteriyordu). Kod hâli **`JarmRout-b`**.
