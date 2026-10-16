# Babel'in kâhin aşımı, eşler arası — K-192 (b) zarf prosedürü · sonuç

> 16 Ekim 2026 · ölçüt `beklenti.md` (commit `e0ab0b1`, koşudan önce) · kopya `1163f81` · koşu 17:48–20:39, 2 sa 50 dk (beklenti ~2–2,5 sa; en olası teslim kâhini 90–125 dk sürdü) · AODV-k'nin döngü iziyle aynı anda, toplam 8 işçi · çıktılar `zarf.txt` · `zarf.jsonl` · `zaman.txt`

## 1 · Zarf (eşler arası, referans dünya)

| kol | tohum | ETX kâhini | en kısa yol | en olası teslim | zarf | Babel | Babel − zarf |
|---|---|---|---|---|---|---|---|
| bağımsız | 1002 | 0,8787 | 0,6504 | 0,9068 | 0,9068 | 0,8963 | −0,011 |
| görev | 1000 | 0,9612 | 0,9145 | 0,9929 | 0,9929 | 0,9755 | −0,017 |
| görev | 1001 | 0,8403 | 0,5661 | 0,8500 | 0,8500 | 0,8935 | **+0,044** |
| görev | 1002 | 0,8392 | 0,6768 | 0,8632 | 0,8632 | 0,8638 | **+0,0006** |
| formasyon | 1001 | 0,9424 | 0,7968 | 0,8891 | 0,9424 | 0,9636 | **+0,021** |

**Üç hücrede Babel zarfı da aşıyor.** Ölçüte göre: *"yazılım hatası aranır (kâhin sızıntısı, sayım, korunum); Babel donmaz."*

- Görev 1002'nin aşımı 0,0006; R'nin (0,0126) çok altında. Ölçüt R'den söz etmediği için harfiyen uygulanır ve hücre aşanlar arasında sayılır.
- Formasyon 1001'de zarfı ETX kâhini veriyor; en olası teslim kâhini ondan düşük kalıyor (0,8891). Yere toplamada her hücrede tersiydi.
- Öngörü görev 1001 için yön vermemişti; hücre zarfın dışına çıktı. Formasyon 1001'in aşımı öngörülmemişti.

## 2 · Kayıt

Hiçbir eşler arası hücre kayda girmedi. Bağımsız 1002 ve görev 1000 zarfın içinde, ama Babel'in eşler arası kaydı hata araması bitince birlikte yazılır.

## 3 · Hata araması

`arsiv/teshis/babel_zarf_asim_2026-10-16/` (ayrı beklentiyle):

- **Kâhin sızıntısı:** `protokoller/babel.py` yalnız gözlem arayüzlerini (`sim2.gozlem.*`) ve kendi biçim dosyasını içe aktarıyor; kanal, konum, kurulum ya da kâhin erişimi yok. Mimari denetimi ihlalsiz (16 Ekim).
- **Sayım:** paket defteri bir paketin iki kez ya da doğmadan teslimini yapısal olarak reddediyor (`sim2/olcum/paket_defteri.py`, `teslim_edildi`). U1'de korunum geçerli. Kopya ve yeniden koşuda kimlik teşhisle denetlenir.
- **Mekanizma:** Babel'in ulaştırıp zarf kâhininin ulaştıramadığı paketlere ve kâhin grafiğinin dilim içi yaşına teşhis bakar.
