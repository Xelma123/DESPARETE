# 16 · KAYNAKÇA — rapor için (IEEE biçimi)

> **Güncel:** 10 Ekim 2026. Projede kullanılan bütün kaynakların rapora girecek biçimi. Doğrulama ayrıntısı `v2/02`de (sütundaki kimlik), dosya kopyaları ve SHA-256'lar `protokol_kaynaklari/README.md`de.
> **Kural (`02`):** açılıp okunmamış bir kaynak rapora giremez. Durum sütunu:
> - ✓ açıldı, okundu (tamamı ya da ilgili bölüm);
> - ~ kısmen, ya da iddia kaynağın söylediğinden farklı;
> - ↪ yalnız başka bir kaynak üzerinden biliniyor → raporda ancak "…'de aktarıldığı gibi" diye anılır, ya da önce açılır;
> - uyg. uygulama kaynağı (standardı uygulayan açık kod);
> - ○ henüz açılmadı → rapora girmeden açılmalı.
>
> Yeni bir kaynak `02`ye girdiğinde buraya da eklenir. Numaralar raporda metin içi atıf ([n]) olarak kullanılır; rapor yazılırken sıra, ilk atıf sırasına göre yeniden düzenlenebilir.

## Protokoller ve yönlendirme

| # | künye | `02` | durum |
|---|---|---|---|
| [1] | C. Perkins, E. Belding-Royer, S. Das, "Ad hoc On-Demand Distance Vector (AODV) Routing," IETF RFC 3561, Jul. 2003. | R1 | ✓ |
| [2] | T. Clausen, P. Jacquet (Eds.), "Optimized Link State Routing Protocol (OLSR)," IETF RFC 3626, Oct. 2003. | R2 | ✓ |
| [3] | M. K. Marina, S. R. Das, "On-demand Multipath Distance Vector Routing in Ad Hoc Networks," in *Proc. IEEE ICNP*, 2001, pp. 14–23. | R4 | ✓ |
| [4] | J. Chroboczek, D. Schinazi, "The Babel Routing Protocol," IETF RFC 8966, Jan. 2021. | G3 | ✓ (§1–2) |
| [5] | Vu Khanh Quy, Nguyen Tien Ban, Nguyen Dinh Han, "A High-Performance Routing Protocol for Multimedia Applications in MANETs," *Journal of Communications*, vol. 14, no. 4, Apr. 2019. | D | ✓ |

## Kablosuz fizik ve MAC (802.11b)

| # | künye | `02` | durum |
|---|---|---|---|
| [6] | G. Pei, T. Henderson, "Validation of ns-3 802.11b PHY model," Boeing Research & Technology, May 2009. [Online]. Available: https://www.nsnam.org/~pei/80211b.pdf | G1 | ✓ |
| [7] | J. Boer, "Direct Sequence Spread Spectrum Physical Layer Specification IEEE 802.11," IEEE P802.11-96/49E, Mar. 1996. | G2 | ✓ |
| [8] | IEEE Std 802.11-2020, "Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications," 2020. | G12 · G13 | ↪ [9] ve [10]'un atfıyla (Tablo 16-4, ek C.3); standardın kendisi ücretli, açılmadı |
| [9] | ns-3 Network Simulator, `src/wifi` (wifi-standard-constants.h, wifi-mac.cc, wifi-remote-station-manager.cc, dsss-phy.cc, dsss-error-rate-model.cc, arf-wifi-manager.cc) ve `src/aodv` (aodv-routing-protocol.cc, aodv-rqueue.cc/.h — rota tamponu 64 paket · 30 s), GPL-2.0, erişim 25–28 Eyl. 2026. [Online]. Available: https://gitlab.com/nsnam/ns-3-dev | G12 · G14 | uyg. |
| [10] | Linux kernel, `net/wireless/core.c` (cfg80211), GPL-2.0, erişim 25 Eyl. 2026. [Online]. Available: https://github.com/torvalds/linux | G13 | uyg. |
| [11] | M. B. Pursley, T. C. Royster, "Properties and performance of the IEEE 802.11b complementary-code-key signal sets," *IEEE Trans. Commun.*, vol. 57, no. 2, pp. 440–449, Feb. 2009. | G1 | ↪ [6] |
| [12] | G. Ferrari, G. E. Corazza, "Tight bounds and accurate approximations for DQPSK transmission bit error rate," *Electronics Letters*, vol. 40, no. 20, pp. 1284–1285, Sep. 2004. | G1 | ↪ [6] |
| [13] | G. Judd, P. Steenkiste, "Characterizing 802.11 wireless link behavior," *Wireless Networks*, 2008. | G1 | ↪ [6] (CMU ölçümleri) |
| [14] | G. Bianchi, "Performance analysis of the IEEE 802.11 distributed coordination function," *IEEE J. Sel. Areas Commun.*, 2000. | — | ○ simülatörün MAC doğrulamasında kullanıldı (`07` §10); künye ve sayfa açılıp doğrulanmalı |
| [15] | J. Li, C. Blake, D. S. J. De Couto, H. I. Lee, R. Morris, "Capacity of Ad Hoc Wireless Networks." | A5b | ✓ (§3.2) · yayın yeri (ACM MobiCom 2001) raporda kaynaktan teyit edilecek |
| [39] | A. Kamerman, L. Monteban, "WaveLAN-II: A High-Performance Wireless LAN for the Unlicensed Band," *Bell Labs Technical Journal*, pp. 118–133, Summer 1997. | G14 | ↪ [9] (ns-3 `arf-wifi-manager.h`'nin atfıyla; özgün makale açılmadı) |

## Kanal (İHA)

| # | künye | `02` | durum |
|---|---|---|---|
| [16] | A. A. Khuwaja, Y. Chen, N. Zhao, M.-S. Alouini, P. Dobbins, "A Survey of Channel Modeling for UAV Communications," *IEEE Commun. Surveys Tuts.*, 2018 (arXiv:1801.07359). | G10 | ✓ arXiv sürümü (hava–hava bölümü) · dergi künyesi teyit edilecek |
| [17] | W. Khawaja, I. Guvenc, D. W. Matolak, U.-C. Fiebig, N. Schneckenburger, "A Survey of Air-to-Ground Propagation Channel Modeling for Unmanned Aerial Vehicles," *IEEE Commun. Surveys Tuts.*, 2019 (arXiv:1801.01656). | G11 | ✓ arXiv sürümü (K faktörü bölümü) · dergi künyesi teyit edilecek |
| [18] | A. Al-Hourani, S. Kandeepan, S. Lardner, "Optimal LAP Altitude for Maximum Coverage," *IEEE Wireless Commun. Lett.*, 2014. | G6 | ✓ |
| [19] | N. Goddemeier, K. Daniel, C. Wietfeld, "Role-Based Connectivity Management with Realistic Air-to-Ground Channels for Cooperative UAVs," *IEEE J. Sel. Areas Commun.*, vol. 30, no. 5, pp. 951–963, Jun. 2012. | G8 | ✓ (kanal bölümü) |
| [20] | N. Goddemeier, C. Wietfeld, "Investigation of Air-to-Air Channel Characteristics and a UAV Specific Extension to the Rice Model," in *Proc. IEEE GLOBECOM Workshops (Wi-UAV)*, 2015. | G10 | ↪ [16] (ücretli, açılmadı) |
| [21] | ITU-R Rec. P.1410-2, "Propagation data and prediction methods for the design of terrestrial broadband millimetric radio access systems," 2003. | G6 | ↪ [18] |

## Karıştırma, İHA ve saha

| # | künye | `02` | durum |
|---|---|---|---|
| [22] | H. Pirayesh, H. Zeng, "Jamming Attacks and Anti-Jamming Strategies in Wireless Networks: A Comprehensive Survey," *IEEE Commun. Surveys Tuts.*, 2022 (arXiv:2101.00292). | G5 | ✓ arXiv sürümü (WLAN, tespit bölümleri) · dergi künyesi teyit edilecek |
| [23] | O. Puñal, I. Aktaş, C.-J. Schnelke, G. Abidin, K. Wehrle, J. Gross, (Wi-Fi karıştırma tespiti, makine öğrenmesi). | G5 | ↪ [22]'nin [83]'ü; künye tamamlanmalı |
| [24] | K. Pelechrinis, I. Broustis, S. V. Krishnamurthy, C. Gkantsidis, (karıştırmada hız uyarlaması ve güç kontrolü deneyleri). | G5 | ↪ [22]'nin [79]–[80]'i; künye tamamlanmalı |
| [25] | J. Watling, N. Reynolds, "Meatgrinder: Russian Tactics in the Second Year of Its Invasion of Ukraine," RUSI, May 2023. | A1 | ✓ (s. 4) |
| [26] | V. Andreika, "Lessons from Ukraine," *Military Review*. | A2 | (anlam kayması; `02` A2) |
| [27] | M. Deo, M. Schuß, M. Baddeley, C. A. Boano, "Robust Wi-Fi Mesh Networking with SPIDERMAN," TU Graz. | A6 | ✓ |
| [28] | Y. Kütük, "UAS (Unmanned Aircraft Systems): The Force Multiplier for Law Enforcement Agencies and the Potential Contributor to Stability Policing," NATO SPCoE, 2025 (NATO ATP-3.3.8.1 Ed. B'den aktarır). | G9 | ✓ (§1.4.3) |
| [29] | Mahalakshmi, Ranjitha Kumari, (İHA hız sınıfları), *IJRTE*, vol. 8, no. 5. | A5a | ✓ künye tamamlanmalı |
| [30] | Doodle Labs, "Smart Radio RM-2450 Datasheet," Dec. 2021. | G7 | ✓ |
| [31] | A. Koubâa et al., "Micro Air Vehicle Link (MAVLink) in a Nutshell: A Survey," *IEEE Access*, 2019 (arXiv:1906.10641). | G4 | ✓ arXiv sürümü (ilgili bölümler) · dergi künyesi teyit edilecek |

## Öğrenme tabanlı yönlendirme ve yöntem

| # | künye | `02` | durum |
|---|---|---|---|
| [32] | Hu, Shao, Qian, Du, Li, Lin, Wang, "Meta-Reinforcement Learning in Time-Varying UAV Communications: Adaptive Anti-Jamming Channel Selection." | B5 | ✓ künye (yer, yıl) tamamlanmalı |
| [33] | "Reinforcement Learning-Based Routing Protocols in Flying Ad Hoc Networks: A Survey," *Mathematics*, vol. 10, 3017, 2022. | B6 · B8 | ✓ (B7 ✗ yeniden doğrulanamadı) |
| [34] | J. A. Boyan, M. L. Littman, "Packet Routing in Dynamically Changing Networks: A Reinforcement Learning Approach," 1994. | C4 | ✓ · başlık ve yer kaynaktan teyit edilecek |
| [35] | J. Yoon, M. Liu, B. Noble, "Random Waypoint Considered Harmful," 2003. | C6 | ✓ |
| [36] | D. S. J. De Couto et al., (ETX metriği). | C3 | ○ |
| [37] | B. Liang, Z. J. Haas, (Gauss-Markov mobilite). | C2 | ○ |
| [38] | M. Gudmundson, (gölgeleme korelasyonu), *Electronics Letters*. | C5 | ○ |

**Açık işler (rapor yazımından önce):** ○ işaretlilerin açılması · künyesi eksiklerin (yazar listesi, yer, yıl, sayfa) kaynaktan tamamlanması · ↪ işaretliler için raporda "… aktarıldığı gibi" dili ya da kaynağın kendisine erişim.
