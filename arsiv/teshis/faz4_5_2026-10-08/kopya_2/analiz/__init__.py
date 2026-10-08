"""
ANALİZ KATMANI — ön-kaydın analiz planı (`v2/06` §0.4, §7) · K-184.

`istatistik` : Wilcoxon (NaN tuzağı kapalı) · Holm · δ · GA · hüküm · güç
`satir`      : JSONL okuma · geçerlilik süzgeci · eşleştirme kimlik denetimi ·
               ham ikinci gerçekleme

🔒 Simülatörden HİÇBİR ŞEY içe aktarılmaz (`tests2/test_analiz.py` tarar):
analiz sonuç satırları üzerinde çalışır ve `arac_hash` onu kapsamaz.
"""
