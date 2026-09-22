# PROJE HARİTASI

**TÜBİTAK 2204-A · Yazılım / Bilgisayar Bilimleri**
Karıştırma (jamming) altındaki taktik İHA mesh ağlarında yönlendirme

| | |
|---|---|
| **Ürün** | Öğrencinin kendi tasarladığı yönlendirme protokolü **DESPARETE**. AODV · OLSR · AOMDV kıyas tabanıdır |
| **Teslim** | 19 Aralık 2026 |
| **Durum (23 Eylül 2026)** | **Aşama 1 (simülasyon) ve Aşama 2 (taban protokoller) bitti** — AODV, OLSR ve AOMDV yazıldı ve U1 kapısından geçti. **Aşama 3 başladı:** DESPARETE v0.1'in gerçeklenmesi. Ayrıntı: [`v2/12-YOL-HARITASI.md`](v2/12-YOL-HARITASI.md) §1 · devir: [`DEVIR-PROMPT.md`](DEVIR-PROMPT.md) |

> **Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.**

---

## Nereden başlanır

| kim | ne okur |
|---|---|
| projeyi anlamak isteyen | [`v2/README.md`](v2/README.md) → `v2/01` (problem, iş akışı) → `v2/12` (durum, plan) → `v2/07` (simülatör) |
| devralan ajan | [`DEVIR-PROMPT.md`](DEVIR-PROMPT.md) ve [`DEVIR.md`](DEVIR.md) — ikisi yalnız devir anı içindir |

---

## Dizinler

| dizin | ne |
|---|---|
| `sim2/` | kesikli-olay simülatörü |
| `kalibrasyon/` | ölçüm ve kapı betikleri — kayıtlı sayıların üreticileri |
| `tests2/` | testler |
| `protokoller/` | taban protokoller (AODV · OLSR · AOMDV — kapalı) ve koşum aletleri; DESPARETE Aşama 3'te buraya yazılır |
| `protokol_kaynaklari/` | birincil kaynaklar (RFC 3561 · RFC 3626 · AOMDV makalesi), DESPARETE tasarım paketi, literatür taraması |
| `ciktilar2/` | sonuç satırları (`.jsonl`) |
| `v2/` | proje belgeleri |
| `arsiv/` · `v2/arsiv/` | emekli simülatör, eski belgeler ve belgelerin önceki sürümleri — oradaki sayılar bayat olabilir |
| `arsiv/SIMULATOR-TEKNIK-REFERANS-2026-09-10.md` | ARŞİV — koddan çıkarılmış geçici döküm (10 Eylül 2026); bayat, güncel bilgi için kod başlıkları ve `v2/` |

---

## Sık kullanılan komutlar

Depo kökünden. Süreler bant olarak verilmiştir.

```bash
PYTHONIOENCODING=utf-8 python -m pytest tests2 -q
```
Test takımı — BANT 8–25 dk.

```bash
PYTHONIOENCODING=utf-8 python kalibrasyon/mimari_denetimi.py
```
Yapısal denetim ve köken defteri sayımı.

```bash
PYTHONIOENCODING=utf-8 python -u kalibrasyon/uretici_duman.py
```
Kayıtlı üretici komutların hâlâ koştuğunu sınar — BANT 40–60 dk.

Tam doğrulama listesi: [`DEVIR.md`](DEVIR.md) §2.

---

## Ortam notları

- Windows · PowerShell · Python 3.11
- Her Python çağrısında `PYTHONIOENCODING=utf-8` — konsol Türkçe karakterde çöküyor
- `Pool` kullanan betiklerde `if __name__ == "__main__":` gerekir; `python -` ile stdin'den çalıştırılmaz
- Bu projede `git` komutu çalıştırılmaz — `status` dâhil
- Çalışma anlaşmalarının tamamı: `v2/03-YONTEM-KURALLARI.md` §1
