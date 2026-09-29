# OLSR teşhisi — 2. tur beklentisi (ölçmeden ÖNCE)

> 28 Eylül 2026 · ajan · 1. tur `sonuc_1.md` · duman (kısa pencere, 1000; ölçüm değil): `rota_gecersiz` kararlarının 343/615'inde (%56) düğümün KENDİ bilgisinde geçide düz yol var (medyan 2 atlama); düşüşler geçide 7,8–11,5 km'deki düğümlerde yoğun.
> Komut: `python -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol statik --protokoller olsr,olsr_2atlama_lsym --tohumlar 1000,1001,1002 --isci 6 --kayit <bu klasör>/tam_2.json` (dondurulmuş kopya)

## Aday sapma (koddan, RFC ham metniyle)

RFC 3626 §8.2.1 2-atlama kümesini, HELLO'nun göndereniyle bağ demetinin `L_SYM_time`ı dolmamışsa günceller. §14.2 histerezisli simetri tanımını (LOST_LINK dolmuş · bekleyen değil · L_SYM dolmamış) yalnız komşu durumu (§8.1), MPR hesabı ve rota hesabının ilk adımları için ister ve *"Apart from the above, what has been described previously does not interfere with the advanced link sensing fields"* der. Bugünkü OLSR 2-atlama güncellemesini histerezisli tanıma bağlıyor: histerezisle "bekleyen"e düşen komşu geri gelince 2-atlama kayıtları o komşunun BİR SONRAKİ HELLO'suna kadar boş kalır → geçit 2 atlamadaysa rota yok → `rota_gecersiz` (OLSR tamponlamaz). RFC §10 topoloji girdisini 2. atlamaya uygulamadığı için TC bilgisi bu boşluğu dolduramaz.

Teşhis kolu `olsr_2atlama_lsym`: yalnız bu koşul RFC'nin harfiyen hâline çevrilir (başka hiçbir şey değişmez).

## Öngörü

1. OLSR (değişmemiş) kimliği yine birebir: 0,5912 · 0,7953 · 0,5186.
2. OLSR'da `rota_gecersiz` kararlarının ≥ %40'ında düz yol var (dumanda %56); düşüşler geçide 7–12 km'deki düğümlerde yoğun.
3. `olsr_2atlama_lsym`: üç tohumda da PDR OLSR'dan yüksek; `rota_gecersiz` göreli en az %30 azalır; düz yol oranı düşer.
4. Kalırsa (fark ≤ 0,02): aday sapma açıklama değildir; rota boşalması başka yoldan (topoloji kümesi, MPR/TC çalkantısı) aranır.

## Karar kuralı

3 tutarsa bu bir GERÇEKLEME SAPMASIdır (RFC'nin harfiyen koşulu uygulanmamış) → OLSR düzeltilir (`OLSR-c`), testle bağlanır, U1 yeniden koşulması gereken işler listesine girer. Tutmazsa OLSR değişmez.

Süre bandı: 6 iş, statik → 15–25 dk.
