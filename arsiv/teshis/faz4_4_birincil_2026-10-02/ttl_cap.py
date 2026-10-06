"""`ttl_baslangic` birincil hücrede bağlar mı? — ağın ATLAMA ÇAPI (Faz 4.4, K kalemi).

    PYTHONIOENCODING=utf-8 py -3.11 -u arsiv/teshis/faz4_4_birincil_2026-10-02/ttl_cap.py

Simülasyon koşmaz: birincil hücrenin dünyası kurulur, kâhin grafiği ölçüm
penceresinde her 5 s'de (ve karıştırıcının her açılıp kapanmasında, çünkü
grafik onunla yenilenir) yeniden kurulur. Basılan, geçide giden ve geçitten
çıkan yolların ATLAMA sayısı:
  · eşikli grafikte (en kısa yol kâhini) BFS uzaklığı — döngüsüz en kısa yol,
  · ETX kâhininin seçtiği yolun atlama sayısı (zayıf bağları da kullanır;
    gerçek protokollerin uzun yollarına daha yakın üst kestirim).
TTL ×0,5 = 16 ancak döngüsüz bir yol 16 atlamayı aşarsa bağlar. Ölçüt
(ölçmeden): bütün tohum ve anlarda en uzun yol ≤ 8 ise (16'nın yarısı,
iki kat pay) `ttl_baslangic` döngüsüz yolda bağlamaz; değeri yalnız döngüdeki
paketin ömrünü belirler.
"""
import os
import pathlib
import sys
from collections import deque

KOK = pathlib.Path(os.environ.get("TESHIS_KOK")
                   or pathlib.Path(__file__).resolve().parents[3])
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.kahin import KanalGrafigi  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

TOHUMLAR = (1000, 1001, 1002, 1003, 1004)


def bfs(komsu, kaynak):
    uz = {kaynak: 0}
    q = deque([kaynak])
    while q:
        u = q.popleft()
        for v in komsu[u]:
            if v not in uz:
                uz[v] = uz[u] + 1
                q.append(v)
    return uz


def etx_atlama(g, kaynak, hedef):
    n = 0
    u = kaynak
    while u != hedef:
        v = g.en_guvenilir_sonraki(u, hedef)
        if v is None:
            return None
        u = v
        n += 1
        if n > 64:
            return None
    return n


en_bfs, en_etx = 0, 0
for tohum in TOHUMLAR:
    kfg = DS.konfig(kol="ttl_cap", senaryo="formasyon-surekli", tohum=tohum,
                    trafik_deseni="yere_toplama", tehdit_senaryosu="derin_sizma")
    kur = kurulum_yap(kfg)
    g = KanalGrafigi(kur)
    gecit = kfg.gecit
    bas, bitis = kfg.olcum_penceresi
    t_b, t_e = 0, 0
    t = bas
    while t <= bitis:
        kur.olaylar.simdi = t
        g._tazele(t)
        ileri = bfs(g._komsu, gecit)
        # geçide giden yollar (yönlü grafikte ters yönü de ayrıca bak)
        geri_komsu = [[] for _ in range(kur.dugum_sayisi)]
        for u, ks in enumerate(g._komsu):
            for v in ks:
                geri_komsu[v].append(u)
        geri = bfs(geri_komsu, gecit)
        t_b = max(t_b, max(ileri.values()), max(geri.values()))
        for d in range(kur.dugum_sayisi):
            if d != gecit:
                a = etx_atlama(g, d, gecit)
                if a is not None:
                    t_e = max(t_e, a)
        t += 5.0
    print(f"tohum {tohum}: en uzun BFS {t_b} · en uzun ETX yolu {t_e}  "
          f"(gecit {gecit}, pencere {bas}–{bitis} s)")
    en_bfs, en_etx = max(en_bfs, t_b), max(en_etx, t_e)
print(f"HEPSI: en uzun BFS {en_bfs} · en uzun ETX yolu {en_etx} · TTL 32 / ×0,5 = 16")
print("🟢 TTL dongusuz yolda baglamaz" if max(en_bfs, en_etx) <= 8
      else "🔴 olcut asildi — TTL taranmali")
