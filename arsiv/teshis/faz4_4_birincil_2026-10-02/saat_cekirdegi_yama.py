"""AODV'nin başlangıç durumu yerel saatin SIFIRINA bağlı mı? — yama (K-214 önerisi).

    py -3.11 arsiv/teshis/faz4_4_birincil_2026-10-02/saat_cekirdegi_yama.py <kök>

`_son_yayin_s = -1.0` ve hız sınırı pencereleri `[0.0, 0.0]` yerel saatin
0 anına çapalı. Saat ofseti negatifse (U(−0,5; +0,5) s) düğüm açılışta yerel
0'a kadar HELLO gönderemez ve ilk "saniye" penceresi 1 + |ofset| s sürer.
RFC 3561: §6.9 "son HELLO_INTERVAL içinde başka yayın yapmadıysa" — hiç
yayın yapmamış düğüm için koşul doğrudur; §10 "saniyede en çok". Yama
başlangıcı "hiç olmadı" (−∞) yapar; ilk pencere ilk olayda açılır.
Yalnız verilen kökteki `protokoller/aodv.py`yi değiştirir (önce kopyada sınanır).
"""
import sys
from pathlib import Path

p = Path(sys.argv[1]) / "protokoller" / "aodv.py"
s = p.read_bytes().decode("utf-8")
nl = "\r\n" if "\r\n" in s else "\n"
s = s.replace("\r\n", "\n")
ciftler = [
    ("        self._son_yayin_s = -1.0\n",
     "        self._son_yayin_s = -math.inf\n"),
    ("        self._rreq_pencere: list[float] = [0.0, 0.0]\n"
     "        self._rerr_pencere: list[float] = [0.0, 0.0]\n",
     "        self._rreq_pencere: list[float] = [-math.inf, 0.0]\n"
     "        self._rerr_pencere: list[float] = [-math.inf, 0.0]\n"),
    ("from dataclasses import dataclass, field\n",
     "import math\nfrom dataclasses import dataclass, field\n"),
]
for e, y in ciftler:
    assert s.count(e) == 1, e[:50]
    s = s.replace(e, y)
p.write_bytes(s.replace("\n", nl).encode("utf-8"))
print("yamalandi:", p)
