"""
DESPARETE · komşu yaşam döngüsü — saf, zamanı dışarıdan alan durum makinesi.

Kaynak: `protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/` — `10` (model) ·
`20` §5 (zamanlayıcılar) · `21` §2.1 (sayılar) · `22` §4 (geçişler) · `23` §3
(algoritma). Kararlar: `v2/04` K-150 · K-152 · K-154.

🔒 NEDEN SAF
============
Her geçiş bir ANDA ve bir KANITLA olur; ikisi de dışarıdan verilir. Bu modül
simülatörden hiçbir şey içe aktarmaz, zamanlayıcı KURMAZ — yalnız son
tarihleri tutar ve istenince "şu komşuya şu an uyandır" der. Böylece her
geçiş birim testle, saniyesi saniyesine sınanır (`tests2/test_desparete.py`);
simülatöre bağlama `desparete.py`nin işidir.

🔒 DURUMLAR — `22` §4
=====================
    UNQUALIFIED → ACTIVE → STALE / SUSPECT → EXPIRED

  · İleri yönlü (forwarding-grade) kanıt: `i → j` unicast'inin MAC onayı ya
    da `i`nin başlattığı PROBE'a eşleşen PROBE_REPLY (`23` §3.1). ACTIVE
    kurar ve bütün tazelik sürelerini yeniden başlatır.
  · Pasif duyma ve gelen PROBE kanıt DEĞİLDİR — yalnız aday açar.
  · ACTIVE → STALE: `T_fresh` doldu. ACTIVE → SUSPECT: sert bağ hatası
    (MAC vazgeçti). İkisinde de komşu HEMEN aday olmaktan çıkar.
  · Hata oturumu (en çok iki PROBE) yalnız bir alan o komşuyu doğrulamaya
    İHTİYAÇ duyuyorsa açılır (`23` §3.2: *"if a field needs verification"*) —
    ihtiyacı soran `gerekli_mi` geri çağrısıdır: komşu bir iletilebilir
    alanın ardılıysa evet (`desparete.py`, K-155).
  · ACTIVE sınırını geçen her komşu `degisenleri_al()` ile bildirilir; alanlar
    bunu kendi yeniden hesaplamalarından ÖNCE öğrenir (`22` §3).
  · EXPIRED kayıt tablodan SİLİNİR; eski ölçüm ve ilan canlanmaz. Yeni
    kanıtla yeniden UNQUALIFIED başlar.
  · Doğrulama oturumu (K-158): CAUTION'a giren alanın ACTIVE ardılına en
    çok iki PROBE (`20` §5 `T_probe_start`: *"CAUTION/PROTECT'te ek
    doğrulama ihtiyacı"*). Yanıtsız biterse komşu DÜŞÜRÜLMEZ — `22` §4
    ACTIVE için yanıtsızlığa geçiş tanımlamaz; `T_fresh` karar verir.
    Açık bir oturum varsa yenisi açılmaz.

🔒 ADAYIN HIZ SINIRI — ajan seçimi (K-154)
==========================================
`23` §3.1 adaylığı *"rate-limited bootstrap girdisi"* diye tanımlar ama
sayı vermez. Seçilen: bir komşu için yeni nitelik oturumu, bir öncekinin
başlangıcından en az `T_retention` (5 s) sonra açılabilir. Yeni sabit yok;
duyulup da doğrulanamayan bir komşuya giden PROBE, 5 s'de en çok iki.

🔒 M0.1 YALNIZ ACTIVE KOMŞUDA
=============================
`35` §3.1: uygun sonuç, `i`nin ACTIVE `j`ye yaptığı hedefli unicast
denemesidir. ACTIVE olmayan komşuya giden denemenin sonucu ölçüme GİRMEZ —
nitelik PROBE'unun onayı komşuyu ACTIVE yapar ama kendisi bir örnek değildir.

🔒 ZAMAN PAYI — gerçekleme ayrıntısı, protokol sabiti değil
===========================================================
Uyandırmalar simülatörün küresel zamanında kurulur; protokol düğümün kendi
saatini görür (ofset + sapma, `sim2/cekirdek/saat.py`). 20 ppm σ'lık sapma,
en uzun zamanlayıcıda (≤ 10 s) 5σ'da bile 1 ms'nin altında kalır. Bu yüzden
son tarihi `ZAMAN_PAYI_S` (1 ms) içinde olan olay dolmuş sayılır.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from protokoller.desparete_bicim import (
    J_PROBE_S, N_PROBE, T_FRESH_S, T_IDLE_PROBE_S, T_PROBE_ARA_S,
    T_PROBE_REPLY_S, T_RETENTION_S)
from protokoller.desparete_metrik import BagOlcumu, Olcum

__all__ = ["UNQUALIFIED", "ACTIVE", "STALE", "SUSPECT", "EXPIRED",
           "ZAMAN_PAYI_S", "Komsu", "KomsuTablosu", "ProbeIstegi"]

UNQUALIFIED = "UNQUALIFIED"
ACTIVE = "ACTIVE"
STALE = "STALE"
SUSPECT = "SUSPECT"
EXPIRED = "EXPIRED"

ZAMAN_PAYI_S = 1e-3

_NITELIK, _HATA, _BOSTA, _DOGRULAMA = "nitelik", "hata", "bosta", "dogrulama"
_OLCUM = "olcum"                      # K-163 V7: nitelik sonrası ilk örnek


@dataclass(frozen=True, slots=True)
class ProbeIstegi:
    """"`komsu`ya şu sırayla bir PROBE gönder" — protokol çerçeveyi kurar."""

    komsu: int
    sira: int
    jitter_s: float
    tur: str
    deneme: int = 1                   # oturumun kaçıncı denemesi (K-163 V1)


@dataclass(slots=True)
class _Oturum:
    tur: str
    deneme: int
    sira: int
    yanit_son: float                  # bu denemenin yanıt son tarihi
    sonraki_deneme: float | None = None


@dataclass(slots=True)
class Komsu:
    durum: str
    saklama_son: float
    olcum: BagOlcumu = field(default_factory=BagOlcumu)
    taze_son: float | None = None     # yalnız ACTIVE
    bosta_son: float | None = None    # yalnız ACTIVE
    oturum: _Oturum | None = None
    son_olcum: Olcum | None = None

    def son_tarih(self) -> float | None:
        adaylar = [self.saklama_son, self.taze_son, self.bosta_son]
        if self.oturum is not None:
            adaylar.append(self.oturum.sonraki_deneme
                           if self.oturum.sonraki_deneme is not None
                           else self.oturum.yanit_son)
        adaylar = [t for t in adaylar if t is not None]
        return min(adaylar) if adaylar else None


class KomsuTablosu:
    """Bir düğümün bütün doğrudan komşuları.

    `sira_al` her kontrol mesajının Control Sender Block sırasını verir
    (düğümün TEK sayacı — PROBE'lar da ondan çeker). `gerekli_mi(j)`, bir
    alanın `j`yi doğrulamaya ihtiyacı var mı diye sorar.
    """

    __slots__ = ("_sira_al", "_gerekli_mi", "_bosta", "_bosta_filtre",
                 "_kayit", "_son_nitelik", "_planli", "_degisen", "sayac")

    def __init__(self, sira_al, gerekli_mi=lambda j: False,
                 bosta_sondalama: bool = True, bosta_filtre=None) -> None:
        self._sira_al = sira_al
        self._gerekli_mi = gerekli_mi
        self._bosta = bosta_sondalama       # ablasyon bayrağı (K-159)
        # K-165 V2+: `(j, t) → bool` — boşta PROBE yalnız gerekli komşuya.
        self._bosta_filtre = bosta_filtre
        self._kayit: dict[int, Komsu] = {}
        self._son_nitelik: dict[int, float] = {}
        # j → kurulmuş en erken uyandırmanın anı (tekrarı önlemek için)
        self._planli: dict[int, float] = {}
        # 🔒 ACTIVE'e giren ya da çıkan komşular — alanlar bunu, KENDİ
        # yeniden hesaplamalarından ÖNCE öğrenmeli (`22` §3 adım 3 → 4).
        self._degisen: list[tuple[int, str]] = []
        self.sayac: dict[str, int] = {
            "aday_acilan": 0, "aday_hiz_siniri": 0,
            "probe_nitelik": 0, "probe_hata": 0, "probe_bosta": 0,
            "probe_dogrulama": 0, "dogrulama_acik_oturum": 0,
            "probe_olcum": 0, "bosta_atlandi": 0,
            "gecis_active": 0, "gecis_stale": 0, "gecis_suspect": 0,
            "gecis_expired": 0, "yanit_eslesen": 0, "yanit_eslesmeyen": 0,
            "yanit_fazla": 0, "olcum_sonuc": 0, "olcum_disi_sonuc": 0,
        }

    # ------------------------------------------------------------ okuma
    def durum(self, j: int) -> str:
        k = self._kayit.get(j)
        return EXPIRED if k is None else k.durum

    def aktifler(self) -> tuple[int, ...]:
        return tuple(sorted(j for j, k in self._kayit.items()
                            if k.durum == ACTIVE))

    def kayit(self, j: int) -> Komsu | None:
        return self._kayit.get(j)

    def __len__(self) -> int:
        return len(self._kayit)

    def degisenleri_al(self) -> list[tuple[int, str]]:
        """Son çağrıdan beri ACTIVE sınırını geçen komşular `(j, yeni durum)`."""
        cikti, self._degisen = self._degisen, []
        return cikti

    # --------------------------------------------------------- kanıtlar
    def aday(self, j: int, t: float) -> list[ProbeIstegi]:
        """Doğrudan duyulan komşu (`23` §3.1 `EnsureUnqualifiedPeer`)."""
        if j in self._kayit:
            return []
        son = self._son_nitelik.get(j)
        if son is not None and t - son < T_RETENTION_S - ZAMAN_PAYI_S:
            self.sayac["aday_hiz_siniri"] += 1
            return []
        self._kayit[j] = Komsu(durum=UNQUALIFIED,
                               saklama_son=t + T_RETENTION_S)
        self._son_nitelik[j] = t
        self.sayac["aday_acilan"] += 1
        return [self._oturum_ac(j, _NITELIK, t)]

    def kanit(self, j: int, t: float) -> None:
        """İleri yönlü kanıt (`23` §3.1 `RecordForwardingProof`)."""
        k = self._kayit.get(j)
        if k is None:
            k = self._kayit[j] = Komsu(durum=UNQUALIFIED,
                                       saklama_son=t + T_RETENTION_S)
            self._son_nitelik[j] = t
        if k.durum != ACTIVE:
            self.sayac["gecis_active"] += 1
            self._degisen.append((j, ACTIVE))
        k.durum = ACTIVE
        k.taze_son = t + T_FRESH_S
        k.bosta_son = t + T_IDLE_PROBE_S if self._bosta else None
        k.saklama_son = t + T_RETENTION_S
        k.oturum = None

    def sonuc(self, j: int, t: float, basarili: bool, tekrar: int) -> None:
        """MAC'in unicast sonucu. Önce ölçüm (yalnız ACTIVE), sonra kanıt."""
        k = self._kayit.get(j)
        if k is not None and k.durum == ACTIVE:
            k.olcum.sonuc(t, basarili, tekrar)
            self.sayac["olcum_sonuc"] += 1
        else:
            self.sayac["olcum_disi_sonuc"] += 1
        if basarili:
            self.kanit(j, t)

    def probe_yaniti(self, j: int, sira: int, t: float) -> bool:
        """Eşleşen PROBE_REPLY kanıttır; eşleşmeyen yok sayılır."""
        k = self._kayit.get(j)
        if k is None or k.oturum is None or k.oturum.sira != sira:
            # 🔎 Oturum PROBE'un MAC onayıyla zaten kapanmışsa yanıt FAZLADIR
            # (kanıt önce geldi) — ayrı sayılır, çünkü simülatörde her
            # onaylı PROBE'un yanıtı böyledir (K-155 §4).
            fazla = k is not None and k.oturum is None and k.durum == ACTIVE
            self.sayac["yanit_fazla" if fazla else "yanit_eslesmeyen"] += 1
            return False
        self.sayac["yanit_eslesen"] += 1
        self.kanit(j, t)
        return True

    def bag_hatasi(self, j: int, t: float) -> list[ProbeIstegi]:
        """MAC `j`ye giden bir unicast'ten vazgeçti — sert bağ hatası."""
        k = self._kayit.get(j)
        if k is None or k.durum != ACTIVE:
            return []
        self._gecis(k, SUSPECT, j)
        k.taze_son = k.bosta_son = None
        k.oturum = None
        if self._gerekli_mi(j):
            return [self._oturum_ac(j, _HATA, t)]
        return []

    def dogrula(self, j: int, t: float) -> list[ProbeIstegi]:
        """CAUTION'a giren alanın ardılı için sınırlı doğrulama (K-150 §4)."""
        k = self._kayit.get(j)
        if k is None or k.durum != ACTIVE:
            return []
        if k.oturum is not None:
            self.sayac["dogrulama_acik_oturum"] += 1   # açık oturum doğruluyor
            return []
        return [self._oturum_ac(j, _DOGRULAMA, t)]

    def olcum(self, j: int, t: float) -> list[ProbeIstegi]:
        """K-163 V7: yeni ACTIVE komşuya TEK ölçüm PROBE'u — onayı ACTIVE
        iken geldiği için M0.1'in ilk örneğidir. Örneği olan ya da açık
        oturumu olan komşuya açılmaz."""
        k = self._kayit.get(j)
        if k is None or k.durum != ACTIVE or k.oturum is not None \
                or (k.son_olcum is not None and k.son_olcum.q is not None):
            return []
        return [self._oturum_ac(j, _OLCUM, t)]

    # ------------------------------------------------------ zamanlayıcı
    def zaman(self, j: int, t: float) -> list[ProbeIstegi]:
        """`j`nin dolmuş son tarihlerini işler."""
        if self._planli.get(j, float("inf")) <= t + ZAMAN_PAYI_S:
            del self._planli[j]
        k = self._kayit.get(j)
        if k is None:
            return []
        dolmus = t + ZAMAN_PAYI_S
        istekler: list[ProbeIstegi] = []
        o = k.oturum
        if o is not None:
            if o.sonraki_deneme is not None and o.sonraki_deneme <= dolmus:
                istekler.append(self._tekrar(j, k, t))
            elif o.sonraki_deneme is None and o.yanit_son <= dolmus:
                if o.tur in (_BOSTA, _OLCUM):
                    k.oturum = None           # tek deneme; T_fresh karar verir
                elif o.deneme < N_PROBE:
                    o.sonraki_deneme = o.yanit_son + T_PROBE_ARA_S
                elif o.tur == _DOGRULAMA:
                    k.oturum = None           # ACTIVE düşmez; T_fresh karar verir
                else:
                    return self._bitir(j, k)
        if k.durum == ACTIVE:
            if k.taze_son is not None and k.taze_son <= dolmus:
                self._gecis(k, STALE, j)
                k.taze_son = k.bosta_son = None
                k.oturum = None
                if self._gerekli_mi(j):
                    istekler.append(self._oturum_ac(j, _HATA, t))
            elif (k.bosta_son is not None and k.bosta_son <= dolmus
                  and k.oturum is None):
                k.bosta_son = None            # tek boşta PROBE (`22` §4.2)
                if self._bosta_filtre is None or self._bosta_filtre(j, t):
                    istekler.append(self._oturum_ac(j, _BOSTA, t))
                else:
                    self.sayac["bosta_atlandi"] += 1   # V2+: gerekli değil
        if k.durum != ACTIVE and k.saklama_son <= dolmus:
            return self._bitir(j, k)
        return istekler

    def uyandirmalar(self, t: float) -> list[tuple[int, float]]:
        """Kurulması gereken uyandırmalar: `(j, gecikme_s)`.

        Bir komşu için daha erken bir uyandırma zaten kurulmuşsa yenisi
        kurulmaz; kurulan uyandırma dolunca kalan son tarihler için bir kez
        daha kurulur. Böylece bekleyen uyandırma sayısı komşu başına küçük
        kalır (simülatörün düğüm başına tavanı 256).
        """
        cikti = []
        for j in sorted(self._kayit):
            son = self._kayit[j].son_tarih()
            if son is None:
                continue
            planli = self._planli.get(j)
            if planli is not None and planli <= son + ZAMAN_PAYI_S:
                continue
            self._planli[j] = son
            cikti.append((j, max(son - t, ZAMAN_PAYI_S)))
        return cikti

    def epoch(self, t: float) -> None:
        """`T_metric_epoch`: her kaydın M0.1 ölçümü kapanır (`35` §6)."""
        for k in self._kayit.values():
            k.son_olcum = k.olcum.epoch(t)

    # ------------------------------------------------------------ içsel
    def _gecis(self, k: Komsu, yeni: str, j: int | None = None) -> None:
        eski, k.durum = k.durum, yeni
        self.sayac["gecis_" + yeni.lower()] += 1
        if j is not None and (eski == ACTIVE or yeni == EXPIRED):
            self._degisen.append((j, yeni))

    def _oturum_ac(self, j: int, tur: str, t: float) -> ProbeIstegi:
        k = self._kayit[j]
        if tur == _HATA and k.durum == STALE:
            self._gecis(k, SUSPECT, j)        # `22` §4.2: STALE → SUSPECT
        sira = self._sira_al()
        # İlk deneme `J_PROBE` titreşimiyle kuyruğa girer — `T_probe_start`
        # üst sınırı. Yanıt süresi en geç gönderimden itibaren işler.
        k.oturum = _Oturum(tur=tur, deneme=1, sira=sira,
                           yanit_son=t + J_PROBE_S + T_PROBE_REPLY_S)
        self.sayac["probe_" + tur] += 1
        return ProbeIstegi(j, sira, J_PROBE_S, tur)

    def _tekrar(self, j: int, k: Komsu, t: float) -> ProbeIstegi:
        o = k.oturum
        o.deneme += 1
        o.sira = self._sira_al()
        o.sonraki_deneme = None
        o.yanit_son = t + T_PROBE_REPLY_S
        self.sayac["probe_" + o.tur] += 1
        return ProbeIstegi(j, o.sira, 0.0, o.tur, o.deneme)

    def _bitir(self, j: int, k: Komsu) -> list[ProbeIstegi]:
        self._gecis(k, EXPIRED, j)
        del self._kayit[j]
        return []
