---
name: iha-mesh-calisma-kurallari
description: Git komutlarını YALNIZ öğrenci çalıştırır (salt-okur olanlar dâhil); Türkçe; 30 dk üstü koşuma izin; kök README GitHub okuru içindir
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5cdbe106-8289-49e7-a318-3bb30615ea86
  modified: 2026-09-27T07:18:22.094Z
---

Öğrencinin koyduğu kurallar (tam listesi `v2/03-YONTEM-KURALLARI.md` §1 ve `DEVIR-PROMPT.md` §4):

- **Git komutlarını yalnız öğrenci çalıştırır** — `status`, `log`, `ls-files` gibi salt-okur olanlar dâhil. 23 Eylül 2026'dan beri depoda git VAR ama bu kural değişmedi. (23 Eylül oturumunda ajan belgeleri okumadan önce `git log` ve `git ls-files` koştu — ihlaldi.)
- Simülatör (`sim2/`) kodunda yapısal değişiklikten önce **yapı anlatılır ve onay alınır**.
- 30 dakikayı aşacak koşumlar için **önce sorulur**; süreler **bant** olarak verilir. Havuz varsayılanı 8 işçi.
- Her Python çağrısında `PYTHONIOENCODING=utf-8` (Türkçe çıktı) ve `PYTHONDONTWRITEBYTECODE=1` (bazı `__pycache__/*.pyc` git'te izleniyor; Python koşmak depoyu değiştirir). 26 Eylül'de bir kez salt-okur `git diff --stat` koşuldu — git'e hiç dokunma.
- **27 Eylül — öğrenci biçim kurallarını gevşetti:** *"o kadar gereksiz ve fazla katı kurallara gerek yok, sonucu etkilemediği sürece… python -c ile çalıştırma gibi konularda daha rahat ol, çok önemli kurallar olmadıkça"*. `python -c` / stdin Python / heredoc gibi sonucu etkilemeyen biçim tercihleri serbest; ihlal diye beyan edilmez. Sıkı kalanlar: git yalnız öğrencide · indirme izinle · silme yok (arşive taşı) · paket kurulmaz · koşu sürerken o koşunun koduna dokunulmaz · beklenti ölçmeden önce · her sayının üreticisi · CRLF korunur.
- Başka bir ajana istem yazarken öğrencinin kurallarını (ör. git) sormadan gevşetme (25 Eylül'de denetim isteminde yapıldı).
- Depoda satır sonları KARIŞIK (bazı dosyalar CRLF, bazıları LF) ve korunmalı: `sed -i` kullanma, Edit aracı korur. Denetim BAYT düzeyinde yapılır (Python `read_bytes`); Git Bash'te `grep -c $'\r$'` LF dosyada da her satırı sayıyor — güvenilmez (23 Eylül'de yanlış alarm verdi).
- Her `sim2/` adımından sonra `kalibrasyon/mimari_denetimi.py` de koşulur (çıkış 0 olsa bile SONUC bölümü okunur): A2–A7'de koşulmadı, 9 bulgu birikti (K-180). Yeni modül sabiti köken defterine, anahtarla modellenen sınır `kapsam`a işlenir.
- **Türkçe konuşulur.** Öğrenciye özetler kısa ve kod referanssız.
- Ölçmeden iddia edilmez; raporlanan her sayı üretici komutunu taşır.
- **Kök `README.md` GitHub okuru içindir** (öğrenci, 23 Eylül 2026): ajan yönergesi içermez, git'in dışladığı dosyalara (`DEVIR*.md`, `arsiv/`, `ciktilar2/`, `v2/arsiv/`) bağlantı vermez. Ajan devri `DEVIR-PROMPT.md` ve `DEVIR.md`dedir; ikisi git dışında, yalnız yereldir.

**Why:** Öğrencinin önceliği dürüstlük ve fikir sahipliği; depo ve commit geçmişi öğrencinindir.

**How to apply:** Git'e dokunma — commit/durum gerekiyorsa komutu öğrenciye ver. README'ye durum eklerken yalnız izlenen dosyalara bağlan. İlgili: [[iha-mesh-projesi-durum]]
