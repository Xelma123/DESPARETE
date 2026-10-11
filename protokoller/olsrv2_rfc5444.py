"""
RFC 5444 paket/mesaj biçimi — OLSRv2'nin tel kodlayıcısı ve çözücüsü.

Kaynaklar: RFC 5444 §5 (paket · mesaj · adres bloğu · TLV) · RFC 5497 §5
(zaman kodu) · RFC 7181 §6.2 (12 bitlik metrik kodu). Tasarım notu
`arsiv/teshis/olsrv2_2026-10-11/tasarim.md` §5.

🔒 NEDEN BAYT BAYT
==================
Simülatörün biçim sözleşmesi (`MesajBicimi`) boyutu sabit ve tekrarlı
alanlardan hesaplar; protokol toplam bayt yazamaz. RFC 5444'ün TLV'li ve
sıkıştırmalı biçimi sabit bir alan listesine sığmaz. Bu yüzden OLSRv2 paketi
burada RFC 5444'e göre gerçekten kodlanır ve tekrarlı 8 bitlik tek alanla
taşınır: ödenen bayt gerçek tel boyutudur, alıcı aynı baytları çözer. RFC
6130 Ek B'nin iki örnek HELLO'su (45 ve 29 bayt) testle birebir üretilir.

🔒 KODLAYICININ SEÇİMLERİ (RFC 5444 serbest bırakıyor)
=====================================================
  · Adresler çağıranın verdiği sırada; tek adres bloğu. Ortak baş (head)
    yalnız bayt kazandırıyorsa; kuyruk ve önek uzunluğu yok (tam adres).
  · Her TLV kanalı (tür, uzantı ve çağıranın ayırdığı kanal), o TLV'yi
    taşıyan ardışık adres koşularına bölünür. Koşuda değer tekse tek
    değerli, değilse çok değerli TLV. Koşu bütün bloksa indeks yok, tek
    adresse tek indeks, değilse başlangıç–bitiş indeksi.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

__all__ = [
    "Mesaj", "BicimHatasi", "mesaj_kodla", "paket_kodla", "paket_coz",
    "iletim_icin", "zaman_kodla", "zaman_coz", "metrik_kodla", "metrik_coz",
    "C_S",
]

C_S: float = 1.0 / 1024.0          # RFC 5497 §5 · RFC 7181 §5.6.3

# Bayrak bitleri — RFC 5444'te bit 0 en anlamlı bittir.
_P_SIRA, _P_TLV = 0x08, 0x04                          # paket bayrakları
_M_KAYNAK, _M_HLIMIT, _M_HCOUNT, _M_SIRA = 0x80, 0x40, 0x20, 0x10
_A_BAS, _A_TAMKUYRUK, _A_SIFIRKUYRUK = 0x80, 0x40, 0x20
_A_TEKONEK, _A_COKONEK = 0x10, 0x08
_T_UZANTI, _T_TEKINDEKS, _T_COKINDEKS = 0x80, 0x40, 0x20
_T_DEGER, _T_UZUNBOY, _T_COKDEGER = 0x10, 0x08, 0x04


# ======================================================================
# ZAMAN ve METRİK KODLARI
# ======================================================================
def zaman_kodla(t_s: float) -> int:
    """RFC 5497 §5 — `t`den küçük olmayan en küçük gösterilebilir zaman."""
    if not t_s > 0.0:
        raise ValueError("zaman kodu pozitif süre ister")
    x = t_s / C_S
    if x < 1.0:
        raise ValueError(f"{t_s} s gösterilemez (en küçük C)")
    b = math.frexp(x)[1] - 1                    # 2^b <= x < 2^(b+1)
    a = math.ceil(8.0 * (x / (1 << b) - 1.0) - 1e-9)
    if a == 8:
        b, a = b + 1, 0
    if not (0 <= a <= 7 and 0 <= b <= 31):
        raise ValueError(f"{t_s} s gösterilemez")
    return 8 * b + a


def zaman_coz(kod: int) -> float:
    b, a = divmod(int(kod), 8)
    return (1.0 + a / 8.0) * (1 << b) * C_S


def metrik_kodla(v: int) -> int:
    """RFC 7181 §6.2 — `v`den küçük olmayan en küçük gösterilebilir metrik;
    12 bitlik `256·b + a`."""
    v = int(v)
    if not 1 <= v <= 16776960:
        raise ValueError(f"metrik aralık dışında: {v}")
    b = 0
    while v + 256 > (1 << (b + 9)):
        b += 1
    a = -((-(v - 256 * ((1 << b) - 1))) // (1 << b)) - 1
    return 256 * b + a


def metrik_coz(kod: int) -> int:
    b, a = divmod(int(kod) & 0x0FFF, 256)
    return (257 + a) * (1 << b) - 256


# ======================================================================
# KODLAMA
# ======================================================================
@dataclass(frozen=True, slots=True)
class Mesaj:
    """Çözülmüş bir mesaj. `adres_tlv`: adres → [(tür, uzantı, değer)];
    `ham` mesajın tel baytları (iletmede yalnız başlığı değişir)."""
    tur: int
    kaynak: int | None
    hop_limit: int | None
    hop_count: int | None
    sira: int | None
    mesaj_tlv: tuple[tuple[int, int, bytes], ...]
    adresler: tuple[int, ...]
    adres_tlv: dict
    ham: bytes = b""

    def mesaj_tlv_degeri(self, tur: int, uzanti: int = 0) -> list[bytes]:
        return [d for t, u, d in self.mesaj_tlv if t == tur and u == uzanti]

    def adres_degerleri(self, adres: int, tur: int,
                        uzanti: int = 0) -> list[bytes]:
        return [d for t, u, d in self.adres_tlv.get(adres, ())
                if t == tur and u == uzanti]


def _tlv(tur: int, uzanti: int, indeks: tuple | None,
         deger: bytes | None, cok_degerli: bool) -> bytes:
    bayrak = 0
    govde = bytearray()
    if uzanti:
        bayrak |= _T_UZANTI
        govde.append(uzanti)
    if indeks is not None:
        if len(indeks) == 1:
            bayrak |= _T_TEKINDEKS
        else:
            bayrak |= _T_COKINDEKS
        govde.extend(indeks)
    if deger is not None:
        bayrak |= _T_DEGER
        if len(deger) > 255:
            bayrak |= _T_UZUNBOY
            govde.extend(len(deger).to_bytes(2, "big"))
        else:
            govde.append(len(deger))
        if cok_degerli:
            bayrak |= _T_COKDEGER
        govde.extend(deger)
    return bytes((tur, bayrak)) + bytes(govde)


def _tlv_blogu(tlvler: list[bytes]) -> bytes:
    govde = b"".join(tlvler)
    return len(govde).to_bytes(2, "big") + govde


def _adres_blogu(adresler: list[int], boy: int) -> bytes:
    ham = [a.to_bytes(boy, "big") for a in adresler]
    ortak = 0
    while (ortak < boy and all(h[ortak] == ham[0][ortak] for h in ham)):
        ortak += 1
    n = len(ham)
    # Baş yalnız bayt kazandırıyorsa: maliyet(h) = (1 + h) + n·(boy − h).
    bas = min(range(ortak + 1),
              key=lambda h: ((1 + h) if h else 0) + n * (boy - h))
    blok = bytearray((n, _A_BAS if bas else 0))
    if bas:
        blok.append(bas)
        blok.extend(ham[0][:bas])
    for h in ham:
        blok.extend(h[bas:])
    return bytes(blok)


def _adres_tlvleri(adresler: list[int], kanallar) -> list[bytes]:
    """Her kanal (tür, uzantı, {adres: değer}) → ardışık koşulara bölünür."""
    n = len(adresler)
    sira = {a: i for i, a in enumerate(adresler)}
    cikti: list[bytes] = []
    for tur, uzanti, degerler in kanallar:
        indeksler = sorted(sira[a] for a in degerler)
        kosular: list[list[int]] = []
        for i in indeksler:
            if kosular and kosular[-1][-1] == i - 1:
                kosular[-1].append(i)
            else:
                kosular.append([i])
        for kosu in kosular:
            ds = [degerler[adresler[i]] for i in kosu]
            if len(kosu) == n:
                indeks = None
            elif len(kosu) == 1:
                indeks = (kosu[0],)
            else:
                indeks = (kosu[0], kosu[-1])
            if all(d == ds[0] for d in ds):
                cikti.append(_tlv(tur, uzanti, indeks, ds[0], False))
            else:
                if len({len(d) for d in ds}) != 1:
                    raise ValueError("çok değerli TLV'de değer boyu tek olmalı")
                cikti.append(_tlv(tur, uzanti, indeks, b"".join(ds), True))
    return cikti


def mesaj_kodla(tur: int, *, adres_boyu: int = 4, kaynak: int | None = None,
                hop_limit: int | None = None, hop_count: int | None = None,
                sira: int | None = None, mesaj_tlv=(), adresler=(),
                adres_tlv=()) -> bytes:
    """RFC 5444 §5.2. `mesaj_tlv`: [(tür, uzantı, değer)] · `adresler`
    sıralı · `adres_tlv`: [(tür, uzantı, {adres: değer})] kanallar."""
    bayrak = 0
    baslik = bytearray()
    if kaynak is not None:
        bayrak |= _M_KAYNAK
        baslik.extend(int(kaynak).to_bytes(adres_boyu, "big"))
    if hop_limit is not None:
        bayrak |= _M_HLIMIT
        baslik.append(hop_limit)
    if hop_count is not None:
        bayrak |= _M_HCOUNT
        baslik.append(hop_count)
    if sira is not None:
        bayrak |= _M_SIRA
        baslik.extend(int(sira).to_bytes(2, "big"))
    govde = bytearray(_tlv_blogu([_tlv(t, u, None, d, False)
                                  for t, u, d in mesaj_tlv]))
    adresler = list(adresler)
    if adresler:
        govde.extend(_adres_blogu(adresler, adres_boyu))
        govde.extend(_tlv_blogu(_adres_tlvleri(adresler, adres_tlv)))
    boy = 4 + len(baslik) + len(govde)
    return (bytes((tur, bayrak | (adres_boyu - 1)))
            + boy.to_bytes(2, "big") + bytes(baslik) + bytes(govde))


def paket_kodla(mesajlar, sira: int | None = None) -> bytes:
    """RFC 5444 §5.1 — sürüm 0; paket sıra numarası isteğe bağlı."""
    bayrak = _P_SIRA if sira is not None else 0
    bas = bytes((bayrak,))
    if sira is not None:
        bas += int(sira).to_bytes(2, "big")
    return bas + b"".join(mesajlar)


# ======================================================================
# ÇÖZME
# ======================================================================
class BicimHatasi(ValueError):
    """RFC 5444 §5.5 — bozuk öğe."""


class _Okuyucu:
    __slots__ = ("b", "i", "son")

    def __init__(self, b: bytes, i: int = 0, son: int | None = None):
        self.b, self.i = b, i
        self.son = len(b) if son is None else son

    def al(self, n: int) -> bytes:
        if self.i + n > self.son:
            raise BicimHatasi("yetersiz bayt")
        parca = self.b[self.i:self.i + n]
        self.i += n
        return parca

    def bayt(self) -> int:
        return self.al(1)[0]

    def kelime(self) -> int:
        return int.from_bytes(self.al(2), "big")


def _tlvleri_oku(o: _Okuyucu, adres_sayisi: int | None):
    boy = o.kelime()
    son = o.i + boy
    if son > o.son:
        raise BicimHatasi("TLV bloğu taşıyor")
    tlvler = []
    while o.i < son:
        tur, bayrak = o.bayt(), o.bayt()
        uzanti = o.bayt() if bayrak & _T_UZANTI else 0
        if bayrak & _T_TEKINDEKS:
            bas = bit = o.bayt()
        elif bayrak & _T_COKINDEKS:
            bas, bit = o.bayt(), o.bayt()
        else:
            bas, bit = 0, (adres_sayisi - 1 if adres_sayisi else 0)
        deger = b""
        if bayrak & _T_DEGER:
            boy = o.kelime() if bayrak & _T_UZUNBOY else o.bayt()
            deger = o.al(boy)
        tlvler.append((tur, uzanti, bas, bit, deger,
                       bool(bayrak & _T_COKDEGER)))
    if o.i != son:
        raise BicimHatasi("TLV bloğu boyu tutmuyor")
    return tlvler


def _mesaj_oku(o: _Okuyucu) -> Mesaj:
    bas = o.i
    tur = o.bayt()
    bayrak_boy = o.bayt()
    bayrak, adres_boyu = bayrak_boy & 0xF0, (bayrak_boy & 0x0F) + 1
    boy = o.kelime()
    son = bas + boy
    if son > o.son:
        raise BicimHatasi("mesaj paketi taşıyor")
    m = _Okuyucu(o.b, o.i, son)
    kaynak = (int.from_bytes(m.al(adres_boyu), "big")
              if bayrak & _M_KAYNAK else None)
    hop_limit = m.bayt() if bayrak & _M_HLIMIT else None
    hop_count = m.bayt() if bayrak & _M_HCOUNT else None
    sira = m.kelime() if bayrak & _M_SIRA else None
    mesaj_tlv = tuple((t, u, d) for t, u, _b, _s, d, _c
                      in _tlvleri_oku(m, None))
    adresler: list[int] = []
    adres_tlv: dict = {}
    while m.i < son:
        n = m.bayt()
        if n == 0:
            raise BicimHatasi("adres sayısı sıfır")
        ab = m.bayt()
        bas_boy = m.bayt() if ab & _A_BAS else 0
        bas_b = m.al(bas_boy) if bas_boy else b""
        kuyruk_boy, kuyruk_b = 0, b""
        if ab & _A_TAMKUYRUK:
            kuyruk_boy = m.bayt()
            kuyruk_b = m.al(kuyruk_boy) if kuyruk_boy else b""
        elif ab & _A_SIFIRKUYRUK:
            kuyruk_boy = m.bayt()
            kuyruk_b = bytes(kuyruk_boy)
        orta = adres_boyu - bas_boy - kuyruk_boy
        if orta < 0:
            raise BicimHatasi("adres parçaları adres boyunu aşıyor")
        blok = [int.from_bytes(bas_b + (m.al(orta) if orta else b"")
                               + kuyruk_b, "big") for _ in range(n)]
        if ab & _A_TEKONEK:
            m.bayt()
        elif ab & _A_COKONEK:
            m.al(n)
        for uz_t, uz_u, bas_i, bit_i, deger, cok in _tlvleri_oku(m, n):
            if not 0 <= bas_i <= bit_i < n:
                raise BicimHatasi("TLV indeksi blok dışında")
            say = bit_i - bas_i + 1
            if cok:
                if len(deger) % say:
                    raise BicimHatasi("çok değerli TLV boyu bölünmüyor")
                tek = len(deger) // say
                parcalar = [deger[k * tek:(k + 1) * tek] for k in range(say)]
            else:
                parcalar = [deger] * say
            for k in range(say):
                adres_tlv.setdefault(blok[bas_i + k], []).append(
                    (uz_t, uz_u, parcalar[k]))
        adresler.extend(blok)
    o.i = son
    return Mesaj(tur, kaynak, hop_limit, hop_count, sira, mesaj_tlv,
                 tuple(adresler), adres_tlv, bytes(o.b[bas:son]))


def iletim_icin(m: Mesaj) -> bytes:
    """RFC 7181 §14.3 adım 2.3.2 — hop limit −1, varsa hop count +1;
    mesajın geri kalanı DEĞİŞMEZ."""
    if m.hop_limit is None or m.hop_limit < 1:
        raise BicimHatasi("iletilecek mesajda hop limit yok")
    ham = bytearray(m.ham)
    i = 4 + (((ham[1] & 0x0F) + 1) if ham[1] & _M_KAYNAK else 0)
    ham[i] = m.hop_limit - 1
    if m.hop_count is not None:
        ham[i + 1] = min(255, m.hop_count + 1)
    return bytes(ham)


def paket_coz(b: bytes) -> tuple[int | None, list[Mesaj]]:
    """RFC 5444 §5.1 — (paket sıra numarası, mesajlar)."""
    o = _Okuyucu(bytes(b))
    ilk = o.bayt()
    if ilk >> 4 != 0:
        raise BicimHatasi("sürüm 0 değil")
    sira = o.kelime() if ilk & _P_SIRA else None
    if ilk & _P_TLV:
        _tlvleri_oku(o, None)
    mesajlar = []
    while o.i < o.son:
        mesajlar.append(_mesaj_oku(o))
    return sira, mesajlar
