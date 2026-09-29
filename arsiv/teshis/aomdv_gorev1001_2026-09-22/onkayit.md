# AOMDV · `gorev-yok/1001` — teşhis ön-kaydı (22 Eylül 2026, ÖLÇÜMDEN ÖNCE)

Gözlenen (AOMDV kapanış ölçümü, `aomdv_son.json`): oran **0,512** (eşik 0,60).
Aynı hücre: AODV 0,462 (açıklanmış düşük) · OLSR 0,628 (geçiyor) ·
ETX kâhini PDR 0,7394.

Daha önce ölçülmüş yapısal sayı (K-137 §4, kanal grafiğinden, simülasyonsuz):
bu hücre görev kolunun **en zayıf eşiksiz en kısa yoluna** sahip (0,2502;
1000'de 0,5519). ⚠️ K-145'in dersi: sıralamayı açıklamak, KUSUR OLMADIĞINI
kanıtlamaz. Bu yüzden ölçülüyor.

## Hipotezler ve ayırıcı ölçü

| # | hipotez | tür | öngörü |
|---|---|---|---|
| M1 | atlama sayısıyla yönlendirme zayıf bağları seçiyor: AODV ailesinin bağ kalitesi kabul eşiği yok, hedef İLK ULAŞAN RREQ kopyasına cevap veriyor | mekanizma | kaybın çoğu `iletim_basarisiz`; başarısızlıkların **> %60'ı** atlama teslim olasılığı 0,90'ın ALTINDAKİ bağlarda |
| M2 | rota boşluğu (tablo kurulamıyor) | kusur adayı | pencere içinde `hedef_yok` + `rota_gecersiz` baskın |
| M3 | döngü | kusur adayı | `ttl` düşmesi belirgin |
| M4 | tampon tavanı | mekanizma | 🔴 ZATEN ÇÜRÜDÜ: kapanış ölçümünde bu hücrede tampon girişi 14 234, düşen **0** |

Ek ölçüm (yorum ölçümden sonra): akış başına teslim · AOMDV'nin yedek yola
geçiş sayısı · AOMDV ile AODV'nin aynı bağları kaç kez kullandığı.

🔒 Bağ kalitesi HAREKETLİ kolda zamanla değişir: kullanım ve başarısızlık
50 s'lik altı kovaya ayrılır ve her kovanın ORTA ANINDA kanal grafiğinden
okunur (K-137'nin "altı an" emsali). Eşik 0,90 U1'in statik eşiğidir ve
ölçümden önce yazılmıştır; sonuç ne olursa olsun değiştirilmeyecek.
