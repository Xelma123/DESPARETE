"""
AOMDV mesaj biçimleri ve sabitleri — makale + RFC 3561, TEK KAYNAK.

🔒 KAYNAK HİYERARŞİSİ (öğrenci, 22 Eylül 2026 — `v2/02` §R4.1 seçenek a)
=======================================================================
1. **Makale** — M. K. Marina, S. R. Das, *"On-demand Multipath Distance
   Vector Routing in Ad Hoc Networks"*, IEEE ICNP 2001
   (`protokol_kaynaklari/marina_das_2001_aomdv_icnp.pdf`; Şekil 3'ün ve k'nin
   dökümü aynı klasörün README'sinde).
2. Makalenin değiştirmediği her şey **RFC 3561** — makalenin kendi ilkesi:
   *"the use of routing information already available in the underlying AODV
   protocol as much as possible"*. Bu yüzden RFC sabitleri burada YENİDEN
   YAZILMAZ; `aodv_bicim.py`den gelir.
3. İkisinde de olmayan her şey `aomdv.py`nin başlığında **beyanlı seçim**.
   ns-2.35'in (Caleffi 2008) seçimleri İTHAL EDİLMEDİ.

🔴 RREQ'E BİR ALAN EKLENİR — `ilk_atlama`
==========================================
Makale §3.2: *"Each RREQ now carries an additional field called firsthop to
indicate the first hop (neighbor of the source) taken by it."* Genişliği
makalede yok; alan bir DÜĞÜM ADRESİ taşıdığı için RFC 3561'in adres
alanlarıyla aynı genişlikte (32 bit) seçildi.

    ölçülen bedel : RREQ 25 → 29 bayt (AODV'nin beyanlı TTL baytı dâhil)
    yönü          : AOMDV'yi AODV'den 4 bayt PAHALI gösterir — makalenin
                    tanımladığı gerçek bir bedel, kaçak değil

RREP ve RERR AODV'ninkiyle AYNIDIR — makale ikisine alan eklemiyor. RREP'in
`atlama` alanı AOMDV'de *"ilan edilen atlama sayısı"*nı taşır (§3.1); biçim
değişmez, anlam değişir.
"""

from __future__ import annotations

from sim2.gozlem.kontrol import MesajBicimi
from protokoller.aodv_bicim import RREQ as _AODV_RREQ

__all__ = ["RREQ", "K_CEVAP"]

# 🔒 AODV'nin RREQ alanları + `ilk_atlama`. Ad "RREQ" kalır: kontrol düzlemi
# biçimleri adıyla sayar ve AOMDV'nin RREQ'i yine bir RREQ'tir.
RREQ = MesajBicimi("RREQ", _AODV_RREQ.alanlar + (("ilk_atlama", 32),))

# Makale §3.2: *"the destination node adopts a 'looser' reply policy. It
# replies up to k copies of RREQ (arriving via unique neighbors) ... We have
# used k = 3 in our experiments."* 🔒 Değer makaledeki deneylerinki; `k`
# metinde Type 3 bit eşlem yazı tipinde ve ÖĞRENCİNİN EKRAN GÖRÜNTÜSÜNDEN
# okundu (`protokol_kaynaklari/README.md`).
K_CEVAP: int = 3
