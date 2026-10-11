# JarmRout — gerçekleme tasarımı (kod yazılmadan önce)

> 11 Ekim 2026 · K-229 · K-230 · yürütücünün ilkesi: **makaleye yüzde yüz sadakat**. Kaynak: C. Pu, IEEE Access 6:68472–68486, 2018 (`protokol_kaynaklari/pu_2018_jarmrout_ieee_access.pdf`; Tablo 4 ve Şekil 2 · 4 yayıncı sayfasından okundu).

## 1 · Kaynak sırası

1. **Makale — harfiyen.** Yazan her kural, DSR'den farklı olsa da makaledeki gibi uygulanır.
2. **DSR (RFC 4728) — yalnız makalenin sustuğu yerde.** Makale DSR üzerine kurulu: rota kaydı, ters rotayla RREP, kaynakta tam rota önbelleği, RERR, karşılaştırma tabanı DSR. Her dolgu beyan tablosunda kaynağıyla yazılır.
3. **Bizim seçimimiz — yalnız ikisinin de sustuğu yerde.** Değer gerekçesiyle seçilir, köken defterine SINANMAMIŞ girer, duyarlılığı ölçülür.

**Sadakatin ölçüsü:** makalenin çözümlü örnekleri birim testine dönüşür. Gerçekleme aynı girdilerle makalenin bastığı sayıları birebir üretmek zorundadır:
- Tablo 1: bağ kalitesi
- Tablo 2: trafik yükü (11,6282 · 7,7468 · 8,9054)
- Tablo 3: yollar arası uzaklık, Şekil 1'in koordinatları
- Şekil 3'ün çift önceliği (7,4638 · 6,8831 · 7,7095)

Tablo 1–3 yayıncı sayfasında görüntü; IEEE Xplore 11 Ekim gecesi geçici olarak kapalıydı, yeniden okunacak.

## 2 · Kural tablosu (makale → gerçekleme)

| # | makale | gerçekleme |
|---|---|---|
| J1 | Kaynakta veri var; rota önbellekte yoksa RREQ yayınlanır, varsa önbellekteki rota(lar) kullanılır (Şekil 4) | keşif sürerken paket simülatörün ortak bekleme tamponunda (`beklet`; herkes için 64 paket · 30 s) |
| J2 | RREQ = S_id 4 · D_id 4 · pkt_seq 2 · C_hop 1 · H_route 4n · P_coord 4n · L_qt 4 · T_ld 4 bayt (Şekil 2) | `MesajBicimi` bu genişliklerle; boyut testle bağlı |
| J3 | Ara düğüm, ilk RREQ: pkt_seq ve C_hop'u önbelleğe alır. RREQ'yu gönderenle arasındaki bağ kalitesini (Eş. 5) ve kendi yükünü (Eş. 8) hesaplar; L_qt/T_ld'den büyükse değiştirir. Kimliğini ve konumunu ekler, C_hop'u bir artırıp yeniden yayınlar | aynı |
| J4 | Ara düğüm, yinelenen RREQ: C_hop önbellektekinden büyükse atar; değilse J3'ün işlemiyle yeniden yayınlar (önbellekteki atlama güncellenmez) | aynı, harfiyen (DSR'den farklı: DSR yineleneni atar) |
| J5 | Ara düğüm önbellekten RREP veremez | aynı |
| J6 | Hedef, ilk RREQ: kaydeder. Sonrakiler: kayıtlı yollardan biriyle ortak düğüm (kaynak/hedef hariç) yoksa kaydeder, varsa atar. İlk RREQ'dan sonra `t_wait` bekler | aynı (kayıt varış sırasına göre, açgözlü) |
| J7 | `t_wait` dolunca her yol çifti için P_prio = α(L_qt^p + L_qt^q) + β(T_ld^p + T_ld^q) + γ·e^(−δ(p,q)), α·β·γ = 0,2 · 0,2 · 0,6 (Eş. 13); en küçük P_prio'lu çift seçilir, iki yoldan iki RREP gider | tek yol kayıtlıysa tek RREP (makalenin kısıt tartışması) |
| J8 | Kaynak RREP'lerdeki tam rotaları önbelleğe alır ve **aynı veri paketini iki yoldan gönderir** (§VI.B) | `Karar(rota=X, kopyalar=(Y[0],), kopya_rotalari=(Y,))` — kopya defteri K-231 |
| J9 | Bir düğüm sonraki atlamaya teslimde sürekli başarısız olursa bağı kopmuş sayar ve kaynağa kopan bağla RERR yollar. Kaynak o bağı içeren yolu siler; tek yol kalırsa onu kullanır, ikisi de giderse yeniden keşfeder | "sürekli başarısız" = MAC'in vazgeçmesi (7 deneme; `iletim_basarisiz`); RERR paketin taşıdığı kaynak rotasının tersinden |
| J10 | Bağ kalitesi = komşudan alınan paketlerin RSSI'larının varyansı (Eş. 1–5); küçük = kararlı; L_qt yoldaki en büyük | RSSI `cerceve_duyuldu`dan (gerçek telsizin çerçeve başına RSSI'ı, σ 2 dB, tamsayı dBm) |
| J11 | Trafik yükü: T_busy = NAV'ın alçak geçiren süzgeci (Eş. 6), Q_buf = kuyruk uzunluğunun süzgeci (Eş. 7), TL = Eş. 8 | **beyanlı sapma:** MAC'te RTS/CTS yok, yani NAV yok. NAV'ın ölçtüğü kanalın meşgul payı, CCA meşgul süresiyle (`mesgul_sure_s`, sürücünün "channel busy time"ı) ölçülür |
| J12 | Mekânsal uzaklık 2B konumlarla (Eş. 9–12); konum RREQ'da taşınır | kendi GPS/INS konumu (1,5 m CEP), yatay izdüşüm (makale 2B varsayıyor) |
| J13 | Veri kaynak rotasıyla taşınır (DSR) | **simülatöre kaynak rotası** (§3) |

## 3 · Simülatöre gereken: kaynak rotası

DSR'de rota veri paketinin başlığındadır ve bedeli bayt olarak ödenir (DSR seçenek başlığı 4 B + kaynak rotası seçeneği 4 B + 4 B × ara düğüm; RFC 4728 §6.1 · §6.7). Sadakat için simülatör bunu taşır:
- `Paket.rota` (ara düğümler).
- `PaketGorunumu.rota`: gözlem penceresine bir alan (29 → 30). `05` §7'nin yolu, gerekçesi "paketin başlığında yazan".
- `Karar.rota` · `Karar.kopya_rotalari` (kaynakta).
- Çerçeve boyu paket başına: sabit veri başlığı + adres başına bayt.

Rota taşımayan protokolde boş; regresyon birebir.

Reddedilen seçenek: kaynak rotası yerine RREP'in kurduğu atlama atlama durum. Düğüm-ayrık yollarda iletim aynı olurdu, ama uçuştaki paketin eski rotası, başlık baytı ve RERR'in dönüş yolu makaleden (DSR'den) ayrışırdı.

## 4 · Parametreler

| parametre | durum |
|---|---|
| α · β · γ (Eş. 13) = 0,2 · 0,2 · 0,6 | makale |
| Eş. 6–7'nin süzgeç sabitleri · Eş. 8'in katsayısı ve düzeltme çarpanı | makalede değer yok → Tablo 2'nin örneğinden geriye çözülmeye çalışılır; olmazsa seçim + SINANMAMIŞ |
| RSSI örnek sayısı N_rssi | Tablo 1'in örneği (son dört örnek görünüyor) → doğrulanacak |
| beklenen RSSI (eşitlikte ayırıcı) −55 dBm | makalenin örneği (yalnız eşitlik bozmada) |
| `t_wait` | makalede yok, DSR'de karşılığı yok → seçim + SINANMAMIŞ |
| RREQ yeniden denemesi, titreşim, rota önbelleği ömrü, RREP/RERR biçimi | DSR (RFC 4728 §9: RequestPeriod 500 ms, MaxRequestPeriod 10 s, MaxRequestRexmt 16, BroadcastJitter 10 ms, RouteCacheTimeout 300 s; §6.3 · §6.4) |

## 5 · Makalenin kendi içinde dikkat isteyen yerler (harfiyen uygulanır, beyan edilir)

- Eş. 13'ün mekânsal terimi e^(−δ). δ metre cinsinden yüzlerce/binlerce olunca terim ~0'dır; seçimi bağ kalitesi ve yük belirler, düğüm-ayrıklık zaten zorunlu. Birim, Şekil 1 · 3'ün örnekleriyle (Tablo 3) sınanacak.
- Eş. 8 yük payını kesir (T_busy) ile paket sayısını (Q_buf) toplar. Makalenin örneği de böyle (TL 7,7–11,6).
- Gözlem: RSSI okunduğu için mimari D17, `rssi_olcum_sigma_db`nin DUYARSIZ kaydını yeniden açar. JarmRout'la duyarlılığı ölçülür.
