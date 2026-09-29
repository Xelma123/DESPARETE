---
name: olcum-ve-baglam-ekonomisi
description: "Öğrenci bağlam (context) yükünden ve uzun/gereksiz test-ölçümlerden şikâyetçi — belgeler öz, koşular en kısa gerekli olan"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5cdbe106-8289-49e7-a318-3bb30615ea86
  modified: 2026-09-26T00:07:52.617Z
---

Belgeler öz ve kayıpsız tutulur (tam metin arşive, etkin belgede öz); testler ve ölçümler yalnız bir soruyu cevaplamak için gereken en kısa hâliyle koşulur.

**Why:** 25 Eylül 2026, öğrenci: *"context yani bağlam sorunu çok fazla dosyamız olduğu için olur olmaz gereksiz şeyleri de barındırıyoruz ayrıca yapılan testler ve ölçümler hem çok uzun hem de çoğu zaman gereksiz oluyor"*. Karar kaydı 590 KB'a, belgeler ~1 MB'a ulaşmıştı; oturumlarda doğrulama amaçlı yeniden koşular, tam takım tekrarları ve çok kollu taramalar birikmişti.

**How to apply:** Yeni kayıt kısa yazılır (karar · gerekçe · kim · sayı + üretici komut; tablolar yalnız karar için şartsa). Aynı bilgiyi birden çok belgeye kopyalama — tek yerde yaz, öbürlerinden atıf ver. Ölçüm: önce "bu koşu hangi kararı değiştirir?" diye sor; cevap yoksa koşma. En az tohum/süre/kol ile başla, gerekirse büyüt. Tam test takımını yalnız bir iş bitince bir kez koş (ara adımda ilgili dosya). Doğrulama için "yeniden koşup birebir mi" kontrolünü yalnız şüphe varsa yap. Belge öz hâle getirilirken **koddaki `NN` §x.y atıflarının gösterdiği bölüm numaraları korunur** (önce kodda atıfları tara); 25 Eylül'de 05/07/08/09/13 bu yüzden eski numaralarla yeniden düzenlendi. Git Bash `sed -i` CRLF dosyada CR'ları siler — depo dosyasında `sed -i` HİÇ kullanma (26 Eylül'de bir kez daha oldu); Edit aracını ya da satır sonunu koruyan bir yama betiği kullan, kazara olursa `crlf.py` ile geri çevir. Satır sonunu `grep -c $'\r$'` ya da `cat -A` ile ÖLÇME — Git Bash'te yanlış sonuç veriyor (25 Eylül sınandı: CRLF dosyada 0); dosya baytlarını sayan bir betik kullan (`b.count(b"\r\n")`). Edit/Write CRLF'yi de LF'yi de koruyor; KARIŞIK dosyayı baskın biçime çeviriyor. İlgili: [[sorunu-coz-raporlayip-birakma]] [[iha-mesh-calisma-kurallari]]
