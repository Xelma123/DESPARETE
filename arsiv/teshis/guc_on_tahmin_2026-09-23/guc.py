# §0.4.3'ün yöntemi, normal gürültüyle: n = 40, alpha/m = 0,05/3, B = 2000.
import numpy as np
from scipy.stats import wilcoxon
rng = np.random.default_rng(20260923)
n, B, esik = 40, 2000, 0.05 / 3
sd = 1.0
delta = 2 * sd / np.sqrt(n)
def guc(d):
    ret = 0
    for _ in range(B):
        x = rng.normal(0.0, sd, n) + d
        ret += wilcoxon(x).pvalue < esik
    return ret / B
for kat in (1.0, 1.4, 1.6, 1.7, 1.8):
    print(f"Δ = {kat:.1f}·δ  güç = {guc(kat * delta):.3f}")
