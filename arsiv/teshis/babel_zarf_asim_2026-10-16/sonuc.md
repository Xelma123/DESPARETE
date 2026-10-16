# Babel zarfı aşıyor (eşler arası) — yazılım hatası araması · sonuç

> 17 Ekim 2026 · ölçüt `beklenti.md` (commit `4188039`, koşudan önce) · kopya `1163f81` · koşu 16 Ekim 22:26 – 17 Ekim 01:29, 3 sa 3 dk (beklenti ~3,5–4 sa) · AODV-k döngü iziyle birlikte (8 işçi) · çıktılar `teshis.txt` · `teshis.jsonl` · `zaman.txt` · duman sınaması `duman.txt`

## 1 · Kimlik, sayım ve korunum: kusur izi yok

| hücre | kol | PDR (kayıt) | korunum | kopya | doğan |
|---|---|---|---|---|---|
| görev 1001 | Babel | 0,8935 (0,8935) | geçerli | 0 | 12 799 |
| | ETX kâhini | 0,8403 (0,8403) | geçerli | 0 | 12 799 |
| | en olası teslim | 0,8500 (0,8500) | geçerli | 0 | 12 799 |
| görev 1002 | Babel | 0,8638 (0,8638) | geçerli | 0 | 12 799 |
| | ETX kâhini | 0,8392 (0,8392) | geçerli | 0 | 12 799 |
| | en olası teslim | 0,8632 (0,8632) | geçerli | 0 | 12 799 |
| formasyon 1001 | Babel | 0,9636 (0,9636) | geçerli | 0 | 12 799 |
| | ETX kâhini | 0,9424 (0,9424) | geçerli | 0 | 12 799 |
| | en olası teslim | 0,8891 (0,8891) | geçerli | 0 | 12 799 |

- Ölçüt 1 (kimlik) tuttu. Ölçüt 2'nin üç kusur izinin hiçbiri yok.
- Sızıntı yok: Babel'in içe aktarmaları ve mimari denetimi, beklentideki gibi.

## 2 · Mekanizma (betimleyici)

**M2 · kâhinin fazla düşüşü** (düşen paket, toplamlardan):

| hücre | zarf kâhini | `iletim_basarisiz` kâhin / Babel | kuyruk taşması kâhin / Babel | `hedef_yok` kâhin / Babel |
|---|---|---|---|---|
| görev 1001 | en olası teslim | 1 857 / 1 300 | 63 / 0 | 0 / 63 |
| görev 1002 | en olası teslim | 1 724 / 1 117 | 27 / 0 | 0 / 626 |
| formasyon 1001 | ETX | 737 / 410 | 0 / 0 | 0 / 56 |

- Kâhinin fazla kaybı iletim başarısızlığında toplanıyor (+557 · +607 · +327). En olası teslim kâhininde bir de kuyruk taşması var.
- Babel'in kâhinlerde olmayan kaybı `hedef_yok`, yani rota bulamama.
- Paket düzeyinde, zarf kâhinine göre:

| hücre | yalnız Babel ulaştırdı | yalnız kâhin ulaştırdı |
|---|---|---|
| görev 1001 | 1 705 | 1 148 |
| görev 1002 | 1 087 | 1 079 |
| formasyon 1001 | 686 | 415 |

**M1 · kâhin grafiğinin dilim içi yaşı:** desteklenmedi.

| hücre | zarf kâhininin teslim oranı, dilimin beş evresinde | son − ilk |
|---|---|---|
| görev 1001 | 0,831 · 0,866 · 0,855 · 0,857 · 0,842 | +0,011 |
| görev 1002 | 0,854 · 0,865 · 0,872 · 0,863 · 0,863 | +0,009 |
| formasyon 1001 | 0,950 · 0,946 · 0,932 · 0,937 · 0,946 | −0,004 |

Düşüş hiçbir hücrede R'yi (0,0126) aşmıyor. Kâhin dilim sonunda dilim başından daha kötü değil.

**Öngörü:** M1 tutmadı, M2 tuttu (fazla kayıp `iletim_basarisiz`'da).

**Aday açıklama** (ölçülmedi):
- Kâhinler bağı kanal modelinden (yol kaybı, gölgeleme, sönümleme) değerlendiriyor; trafiğin yarattığı yükü ve çarpışmaları görmüyor. Bütün akışları aynı "en iyi" bağlara yönlendiriyorlar; en olası teslim kâhinindeki kuyruk taşması bunun izi olabilir.
- Babel'in ETX'i Hello kayıplarından ölçülür. Bu kayıplar çarpışmayı da içerdiği için Babel yüklü bağlardan uzaklaşıyor olabilir.
- Eşler arası desen çok akışlı; yere toplamada Babel zarfın içinde kalmıştı.

## 3 · Karar

Beklentinin 4. maddesine göre kusur izi yok. Bu hücrelerde ETX kâhini ve üç kâhinin zarfı üst sınır değil; M2 kâhinin kaybını iletim başarısızlığına bağlıyor.

K-192 (b) zarfı aşan hücreyi kayda almaz; kayıt için kuralın değişmesi gerekir. **Karar yürütücüde**, Babel o karara kadar donmaz.
