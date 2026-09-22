# DESPARETE — Çekirdek Algoritmalar ve Pseudocode

**Sürüm:** 0.1 (onaylı ilk-sürüm algoritmaları, Security Profile 1 ve M0.1 eki)  
**Durum:** Onaylı state modeli, timer profili, wire format, güvenlik kapıları ve M0.1 tamsayı metriği için deterministik event-handler sözleşmesi.  
**Tarih:** 2026-09-20

## 1. Uygulama kapsamı ve notasyon

İlk operasyon profili tek-sink'tir. Her node, yapılandırılmış `SinkID`yi bilir; gelen DATA'nın `Application-Destination-ID` değeri bu kimlikle eşleşmelidir. Wire format, `K=(Destination-ID,OIID)` anahtarı ve tüm tablolarda çok-hedefe genellenebilir kalır, fakat v0.1 algoritmaları birden çok hedefin ortak kaynak bütçesini yönetmez.

| Sembol | Anlam |
|---|---|
| `Valid(p)` | Paket biçimi, sürüm, reserved alan, Hop Limit, Security Profile 1 AUTH biçimi, roster/Key-ID, gerekli Hop/Origin/Source imzaları ve R1 control anti-replay kontrollerinin geçmesi. |
| `Active(j)` | `N_i[j].state = ACTIVE` ve forwarding-grade kanıtın güncel olması. |
| `Fresh(a)` | `A_j[K]` finite/REACHABLE, ADS açısından güncel ve `advertisement_expiry > now` olması. |
| `C(i,j)` | Doygunluklu, sonlu yönlü link maliyeti; `C_hop + C_quality(Q) + C_risk(R)`. M0.1'de `35`in tamsayı tablolarıyla hesaplanır. |
| `Cost(a,j)` | `sat_add(a.AdvertisedPotential, C(i,j))`; overflow `∞`dir. |
| `FD_i[K]` | `(S_FD,M_FD)` feasibility distance; aynı DFSN'de yükselmez veya sıfırlanmaz. |
| `SerialCmp(x,y)` | RFC 1982'e göre `OLDER`, `EQUAL`, `NEWER` veya `AMBIGUOUS`. AMBIGUOUS fail-closed'dur. |
| `⊥` | Tanımsız successor veya mevcut olmayan state. |

`sat_add` yalnız `0…0xFFFFFFFE` sonlu potential aralığında çalışır; sonuç sınırı aşarsa `∞` üretir. `∞` successor kurulumu için kullanılamaz.

## 2. Ortak paket kabul kapısı

Her paket handler'ı aşağıdaki yordamı çağırır. Handler, `DROP` sonucunda field, neighbor, FD, policy veya buffer state'ini iyimser biçimde değiştirmez.

```text
function AcceptPacket(packet, incomingNeighbor):
    if packet.Version != 1 or packet.Type is reserved: return DROP
    if packet.HeaderLength is malformed or reserved bits are nonzero: return DROP
    if packet.HopLimit == 0: return DROP
    if packet.Type is one-hop and packet.HopLimit != 1: return DROP
    if packet contains unknown critical TLV: return DROP
    if packet contains malformed TLV/padding: return DROP
    if packet has not exactly one final Profile-1 AUTHENTICATION TLV: return DROP
    if Hop-Key-ID has no unique roster owner or HopSignature is invalid: return DROP
    if packet.Type == control and ControlSenderID != RosterOwner(Hop-Key-ID): return DROP
    if packet.Type == DATA and incomingNeighbor is known and
       incomingNeighbor != RosterOwner(Hop-Key-ID): return DROP
    if packet.Type == FIELD_UPDATE and OriginSignature is absent/invalid: return DROP
    if packet.Type == DATA and SourceSignature is absent/invalid: return DROP
    if packet.Type == DATA and packet.RB > packet.SourceRB: return DROP
    if packet.Type == PROBE and packet.TargetNeighbourID != i.NodeID: return DROP
    if packet.Type == control:
        if AR_i[(Sender-ID, Sender-Instance-ID)] is undefined:
            initialR1Allowed := Active(incomingNeighbor)
                or (packet.Type == PROBE
                    and IsRosterAuthorizedDirectPeer(incomingNeighbor)
                    and packet.TargetNeighbourID == i.NodeID)
                or (packet.Type == PROBE_REPLY
                    and packet exactly matches a locally pending PROBE)
            if not initialR1Allowed: return DROP
            AR_i[(Sender-ID, Sender-Instance-ID)] := packet.MessageSequence
        else if SerialCmp(packet.MessageSequence,
                          AR_i[(Sender-ID, Sender-Instance-ID)]) != NEWER:
            return DUPLICATE
        else:
            AR_i[(Sender-ID, Sender-Instance-ID)] := packet.MessageSequence
    if packet is a duplicate control Message-ID: return DUPLICATE
    return ACCEPT
```

R1 control high-water yalnız authenticated sender/instance için tutulur. State tanımsızsa ilk değer yalnız active-peer bağlamında, bu node'a hedefli authenticated PROBE'da veya taze eşleşen kendi pending qualification/failure PROBE'una ait PROBE_REPLY'de atomik olarak kurulur. Bu ilk kabul, peer'i ACTIVE yapmaz; gelen PROBE yalnız reply ve outbound qualification sürecini açar. `DFSN_REQUEST` için Request-ID duplicate kontrolü, Control Message-ID/R1 kontrolünden **ayrı** yapılır. İlk görülen Request-ID `T_req_duplicate=4 s` boyunca en fazla bir kez işlenir/iletilebilir. Aynı Request-ID'nin başka forwarder üzerinden gelmesi yeni istek değildir. Güvenlik reddi state değiştirmez ve ACTIVE komşuyu tek başına düşürmez.

### 2.1 Korumalı paket gönderim sözleşmesi

Her `send`, `broadcast`, `forward-control` veya `transmit` işlemi aşağıdaki yordamı çağırır. Bu yordam kriptoyu state transition yerine koymaz; yalnız seçilmiş state sonucunun gerçek on-air byte dizisine bağlanmasını sağlar.

```text
function ProtectForTransmit(packet, nextHop):
    if packet.Type is control:
        packet.ControlSenderBlock := (i.NodeID, i.InstanceID, NextMessageSequence())
    if packet.Type == FIELD_UPDATE:
        require packet carries valid target OriginSignature for (DestinationID,OIID,DFSN)
    if packet.Type == DATA:
        require packet carries valid SourceSignature and packet.RB <= packet.SourceRB

    set packet.AUTH.HopKeyID to i's active roster Key-ID
    serialize final header fields, including decremented HopLimit/current RB and HeaderLength
    packet.AUTH.HopSignature := Ed25519.Sign(i.privateKey, HOP_INPUT(packet))
    transmit packet to nextHop
```

Forwarder, immutable OriginSignature veya SourceSignature'ı değiştiremez. FIELD_UPDATE üreten relay, target proof'u taşır fakat kendi Control Sender Block'u, ADS/Potential/Lifetime'ı ve HopSignature'ı iletir. DATA için `incomingNeighbor`, AUTH Hop-Key-ID'nin roster sahibidir; Data Source-ID yalnız source proof kimliğidir.

## 3. Komşu kanıtı algoritması

### 3.1 Forwarding-grade kanıt güncellemesi

```text
function RecordForwardingProof(j, proof):
    require j is a roster-authorized direct peer bound to this local link
    if N_i[j] does not exist or N_i[j].state == EXPIRED:
        N_i[j] := UNQUALIFIED record without resurrecting old advertisements
        start T_retention = 5.0 s

    if proof is matching reply to a locally-originated PROBE
       or proof is confirmed local unicast/ACK to j:
        N_i[j].state := ACTIVE
        reset T_fresh = 3.0 s
        reset T_retention = 5.0 s
        reset T_idle_probe = 2.0 s
        cancel pending qualification or failure-bound probe session for j
        RecomputeFieldsUsing(j)
```

Pasif duyma ve yalnız incoming PROBE, `RecordForwardingProof` çağrısı değildir. Node, incoming PROBE'a PROBE_REPLY gönderir; fakat kendi `i → j` yönünü kanıtlanmış saymaz.

```text
function StartQualificationProbe(j):
    require N_i[j].state == UNQUALIFIED
    if no pending qualification session exists:
        schedule PROBE(j) within T_probe_start = 0.1 s
        start T_probe_session = 1.3 s with at most N_probe = 2 sends

function EnsureUnqualifiedPeer(j):
    if N_i[j] does not exist or N_i[j].state == EXPIRED:
        N_i[j] := UNQUALIFIED record without resurrecting old advertisements
        start T_retention = 5.0 s
    if N_i[j].state == UNQUALIFIED:
        StartQualificationProbe(j)
```

Yerel link katmanı rosterla eşleşen doğrudan bir peer adayı bildirdiğinde `EnsureUnqualifiedPeer(j)` çağrılır. Bu aday, forwarding kanıtı değildir; yalnız node'un imzalı ilk PROBE'u gönderebileceği, rate-limited bootstrap girdisidir.

### 3.2 Negatif kanıt ve komşu timerları

```text
on LinkFailure(j) or T_fresh(j) expiry:
    if N_i[j].state == ACTIVE:
        N_i[j].state := SUSPECT for hard failure, otherwise STALE
        InvalidateCandidatesFrom(j)
        RecomputeFieldsUsing(j)
        if a field needs verification: StartFailureProbe(j)

function StartFailureProbe(j):
    if no matching probe session exists:
        schedule PROBE(j) within T_probe_start = 0.1 s
        start T_probe_session = 1.3 s with at most N_probe = 2 sends

on T_idle_probe(j) expiry while state == ACTIVE:
    send one normal PROBE(j)
    # This does not consume N_probe and does not itself change neighbor state.

on qualification or failure-bound probe timeout:
    if attempts remain: wait at least 0.2 s, then send another PROBE(j)
    else: N_i[j].state := EXPIRED; RemoveR1State(j); InvalidateCandidatesFrom(j); RecomputeFieldsUsing(j)

on T_retention(j) expiry while state != ACTIVE:
    N_i[j].state := EXPIRED
    RemoveR1State(j)
    InvalidateCandidatesFrom(j)
    RecomputeFieldsUsing(j)
```

`InvalidateCandidatesFrom(j)` hiçbir field'in DFSN veya FD'sini değiştirmez; yalnız `j`den gelen ilanların forwarding adaylığını kaldırır. Böylece komşu kaybı, ara node'a yeni DFSN üretme yetkisi vermez.

## 4. FIELD_UPDATE kabulü ve safe-successor seçimi

### 4.1 FIELD_UPDATE handler'ı

```text
on ReceiveFieldUpdate(update, j):
    result := AcceptPacket(update, j)
    if result != ACCEPT: return
    if update.sender != j or update.K is malformed: return
    if update.Lifetime/State/Potential combination is illegal: return

    if OIID(update.K) is retired: return
    if not VerifyTargetOriginProof(update.DestinationID, update.OIID, update.DFSN): return
    if not Active(j):
        record only non-forwarding diagnostic evidence; return

    if update carries new accepted OIID for Destination-ID:
        RetireAllFieldsForDestination(Destination-ID)

    old := N_i[j].Advertisement[update.K, update.DFSN]
    if old exists and SerialCmp(update.ADS, old.ADS) != NEWER:
        return  # EQUAL, OLDER and AMBIGUOUS cannot refresh lifetime or state

    if update.State == WITHDRAWAL:
        store withdrawal ordering record until now + T_withdraw_cache
        remove j's finite candidate for update.K/update.DFSN
    else:
        advertisement_expiry := now + min(update.Lifetime × 100 ms, L_adv_max)
        store update as j's current finite advertisement with advertisement_expiry

    RecomputeField(update.K, FIELD_UPDATE)
```

Bir OIID/DFSN bağlamı, target roster key'i ile doğrulanan OriginSignature olmadan kabul edilmez. Target proof'u geçse bile ACTIVE olmayan peer'dan gelen update yalnız tanısal kayda girer; yeni OIID ile mevcut field'leri emekliye ayıramaz, candidate/FD/successor state'ini değiştiremez. Relay'in HopSignature'ı, yalnız bu hopta kendi potential/ADS/Lifetime ilanının bütünlüğünü bağlar; relay target yetkisi kazanmaz.

### 4.2 Candidate ve tie-break

```text
function IsCandidate(K, S, j):
    a := N_i[j].Advertisement[K,S]
    return Active(j)
       and Fresh(a)
       and a.State == REACHABLE
       and a.Potential is finite
       and C(i,j) is finite

function IsFeasible(K, S, j):
    a := N_i[j].Advertisement[K,S]
    if FD_i[K] is UNINITIALIZED: return true
    if SerialCmp(S, FD_i[K].seq) == NEWER: return true
    if SerialCmp(S, FD_i[K].seq) == EQUAL and a.Potential < FD_i[K].metric: return true
    return false

function CandidateOrder(K, j):
    return (Cost(A_j[K],j), j.NodeID, j.InstanceID)
```

Önerilen tie-break, en düşük sonlu toplam maliyet; eşitlikte küçük 64-bit `NodeID`, sonra küçük `InstanceID` sırasıdır. Kimlikler wire'da opaque kalır; burada yalnız deterministik unsigned karşılaştırma için kullanılır. Tie-break feasibility koşulunun yerine geçmez.

### 4.3 Field yeniden hesaplama

```text
function RecomputeField(K, trigger):
    S_new := newest defined DFSN among ACTIVE, valid advertisements for K
    if S_new is undefined and CurrentDFSN_i[K] is UNDEFINED:
        return  # e.g., only a withdrawal cache exists; no field context is invented
    if S_new is defined and CurrentDFSN_i[K] is defined and
       comparison of S_new with CurrentDFSN_i[K] is AMBIGUOUS:
        FailClosedFreshness(K); return

    if S_new is defined and (CurrentDFSN_i[K] is UNDEFINED or
                             S_new is NEWER than CurrentDFSN_i[K]):
        Succ_i[K] := ⊥
        P_i[K] := ∞
        CurrentDFSN_i[K] := S_new
        FD_i[K] := UNINITIALIZED
        cancel stale repair/request state from older DFSN

    candidates := { j | IsCandidate(K, CurrentDFSN_i[K], j) and
                         IsFeasible(K, CurrentDFSN_i[K], j) }

    if candidates is nonempty:
        j* := min candidates by CandidateOrder(K,j)
        oldSuccessor := Succ_i[K]
        Succ_i[K] := j*
        P_i[K] := Cost(A_j*[K], j*)
        if FD_i[K] is UNINITIALIZED or P_i[K] < FD_i[K].metric:
            FD_i[K] := (CurrentDFSN_i[K], P_i[K])
        F_i[K] := FORWARDABLE
        CancelAcquisitionOrRepair(K)
        ResetEffectivePolicyToSteadyIfRecovering(K)
        if oldSuccessor != j* or local advertised potential changed:
            ScheduleFieldUpdate(K, REACHABLE)
        return

    if F_i[K] == FORWARDABLE:
        Succ_i[K] := ⊥
        P_i[K] := ∞
        ScheduleFieldUpdate(K, WITHDRAWAL)
        StartRepair(K, trigger)
    else if F_i[K] == REPAIRING:
        continue current bounded repair only
    else if F_i[K] == UNREACHABLE:
        do not restart control solely because a DATA packet arrived
```

`S_new` yalnız aynı `K` içindeki target-produced DFSN'dir. Daha eski DFSN'li ilanlar cache/diagnostic için kalabilir fakat CurrentDFSN'i geriye çekemez. CurrentDFSN için relevant active ilanların kendi aralarındaki serial kıyası ambiguous ise node field'i fail-closed tutar.

### 4.4 Fail-closed freshness ve repair başlatma

```text
function FailClosedFreshness(K):
    Succ_i[K] := ⊥
    P_i[K] := ∞
    F_i[K] := REPAIRING
    # Same-DFSN FD is preserved; it is never raised/reset here.
    ScheduleFieldUpdate(K, WITHDRAWAL)
    StartAcquisition(K, reason = FRESHNESS_AMBIGUITY)

function StartRepair(K, reason):
    F_i[K] := REPAIRING
    Succ_i[K] := ⊥
    P_i[K] := ∞
    DisableEffectivePolicyActions(K)
    start T_repair_max = 6.0 s if no repair episode exists
    StartAcquisition(K, reason)
```

Withdrawal, yalnız previously finite local state için bir kez planlanır; ADS bu son state'i sıralar. `StartRepair` aynı failure episode'unda FD'yi, DFSN'yi veya request budget'ını sıfırlamaz.

## 5. FIELD_SOLICIT ve DFSN_REQUEST algoritmaları

### 5.1 Yerel acquisition controller

```text
function StartAcquisition(context, reason):
    if A_i[context] == REQUESTING or SOLICITING: return  # coalesce
    A_i[context] := SOLICITING
    send FIELD_SOLICIT within local rate budget
    await valid FIELD_UPDATE for T_solicit_reply = 0.4 s
    repeat at most N_solicit = 2, separated by at least T_solicit_backoff = 0.2 s

on solicit attempts exhausted:
    if a new field is still required:
        A_i[context] := REQUESTING
        start T_req_session = 4.0 s
        SendNewDFSNRequest(context, reason)

function SendNewDFSNRequest(context, reason):
    if request-wave count == N_req = 2: return
    RequestID := (i.NodeID, i.InstanceID, NextRequestSequence())
    mark RequestID for T_req_duplicate = 4.0 s
    broadcast/forward-control to ACTIVE neighbors with HopLimit = H_req = 16
    increment request-wave count
```

OIID bilinmeyen ilk acquisition, `A_i[SinkID]` ile yürür ve FIELD_SOLICIT'ta `HAS_CONTEXT=0` kullanır. İlk DATA paketi field bulunmadığında acquisition başlatabilir; önceki FORWARDABLE field'den REPAIRING'e geçmediği için bu paket repair buffer'a alınmaz. Yerel delivery-failure üretilir. Sonraki veriler, valid field oluşana kadar yeni kontrol dalgası başlatmaz.

```text
on T_req_retry expiry while A_i[context] == REQUESTING:
    if no valid safe field and request-wave count < N_req:
        SendNewDFSNRequest(context, same reason)  # produces a new Request-ID

on T_req_session or T_repair_max expiry:
    A_i[context] := QUIESCENT
    if corresponding field has no safe successor:
        F_i[K] := UNREACHABLE
```

`UNREACHABLE` field yalnız yeni valid OIID/DFSN üzerinden safe candidate, ilk acquisition veya explicit local `Acquire(SinkID)` ile yeni bounded acquisition başlatabilir. Yeni DATA tek başına bu çağrı değildir.

### 5.2 FIELD_SOLICIT alma

```text
on ReceiveFieldSolicit(solicit, j):
    if AcceptPacket(solicit,j) != ACCEPT: return
    if not Active(j): return
    K := current local field for solicit.Destination-ID
    if K exists and F_i[K] == FORWARDABLE and solicit context is compatible:
        send current FIELD_UPDATE(K) once to j
```

Yanıt, alıcının kendi current local ilanıdır; gelen solicit stateless biçimde forward edilmez. Field yoksa negatif yanıt zorunlu değildir.

### 5.3 DFSN_REQUEST alma ve forwarding

```text
on ReceiveDFSNRequest(req, previousHop):
    if AcceptPacket(req, previousHop) != ACCEPT: return
    if RequestID(req) already seen: return
    mark RequestID seen for T_req_duplicate

    if i.NodeID == req.DestinationID:
        HandleAtTarget(req)
        return

    if i has a current FORWARDABLE field that satisfies req context/minimum:
        send current FIELD_UPDATE to previousHop

    if req.HopLimit > 1:
        forward one copy of req to each ACTIVE neighbor except previousHop,
        decrementing HopLimit exactly once
```

Bu forwarding data-plane successor seçimi değildir. Yalnız ACTIVE komşulara, Request-ID duplicate cache'i ve `H_req=16` ile sınırlı control yayılımıdır.

### 5.4 Hedefte DFSN_REQUEST işleme — önerilen dar yetki

```text
function HandleAtTarget(req):
    K := target's current (i.NodeID, OIID)
    if req.HAS_CONTEXT == 0:
        SendOriginFieldUpdate(K)             # target signs/carries current OriginSignature; no DFSN increment
        return
    if req.KnownOIID != OIID(K):
        SendOriginFieldUpdate(K)             # target signs/carries current OriginSignature
        return
    if SerialCmp(CurrentDFSN(K), req.KnownDFSN) == NEWER:
        SendOriginFieldUpdate(K)             # target signs/carries current OriginSignature
        return
    if SerialCmp(CurrentDFSN(K), req.KnownDFSN) in {OLDER, AMBIGUOUS}:
        return                               # malformed/stale or unsafe request context
    if req.Reason != FEASIBLE_STARVATION:
        SendOriginFieldUpdate(K)             # target signs/carries current OriginSignature
        return
    if req.RequestedMinimumDFSN != SerialSuccessor(CurrentDFSN(K)):
        return                               # request cannot force an arbitrary jump

    CurrentDFSN(K) := SerialSuccessor(CurrentDFSN(K))
    P_i[K] := 0
    FD_i[K] := (CurrentDFSN(K), 0)
    SendOriginFieldUpdate(K)                 # signs new (DestinationID,OIID,DFSN) OriginSignature
```

Bu dar yetki, target'ın yalnız kendi güncel OIID'si ve mevcut DFSN bağlamını teyit eden feasible-starvation isteği üzerine **bir** tur artırmasını önerir. Acquisition ve freshness-ambiguity isteği yeni turn üretmez; hedef yalnız mevcut origin update'ini yollar. Hedef, birden çok eşdeğer valid isteği tek incrementte coalesce edebilir.

## 6. PROBE, PROBE_REPLY ve FAILURE_REPORT

```text
on ReceiveProbe(probe, j):
    if AcceptPacket(probe,j) != ACCEPT: return
    if probe.TargetNeighbourID != i.NodeID: return
    EnsureUnqualifiedPeer(j)
    send PROBE_REPLY matching probe's requester identity and MessageSequence to j

on ReceiveProbeReply(reply, j):
    if AcceptPacket(reply,j) != ACCEPT: return
    if reply exactly matches locally pending PROBE to j:
        RecordForwardingProof(j, matching PROBE_REPLY)

on ReceiveFailureReport(report, j):
    if AcceptPacket(report,j) != ACCEPT: return
    if i.NodeID == report.ReportDestinationID: deliver report to local management endpoint
    else if report.ReportDestinationID != SinkID: drop report locally
    else:
        K_report := current FORWARDABLE field for SinkID
        if K_report exists: forward report using its selected safe successor
        else: drop report locally  # no reverse-path inference and no new repair for the failed data field
```

## 7. DATA alma, buffering ve redundancy

```text
on ReceiveData(data, ingress):
    if not Valid(data): return
    if i.NodeID == data.ApplicationDestinationID:
        if ReserveDataIDIfNew(data.DataID): deliver once to application
        return
    if data.ApplicationDestinationID != SinkID: return local policy failure
    if data.HopLimit <= 1: return local policy failure
    if not ReserveDataIDIfNew(data.DataID): return  # duplicate

    K := current valid field for SinkID
    if K exists and F_i[K] == FORWARDABLE:
        ForwardData(data, K)
    else if K exists and F_i[K] == REPAIRING and BufferQuotaAllows(data):
        hold data until min(T_buffer[class], quota/event expiry)
    else:
        emit LocalDeliveryFailure(data, FIELD_UNREACHABLE or NO_FIELD)
        mark Data-ID DROPPED until T_data_duplicate
```

```text
function ForwardData(data, K):
    primary := Succ_i[K]
    nextHops := [primary]
    if EffectivePolicy(K) == PROTECT
       and data.ProtectionEligible
       and data.ReplicationBudget > 0
       and an alternate safe successor exists
       and local resource budget allows:
        append exactly one deterministic alternate successor
        outgoingRB := data.ReplicationBudget - 1
    else:
        outgoingRB := data.ReplicationBudget

    for each nextHop in nextHops:
        copy := data with immutable Data-ID, RB = outgoingRB,
                HopLimit = data.HopLimit - 1
        ProtectForTransmit(copy, nextHop)  # preserves SourceSignature; renews HopSignature
    mark Data-ID FORWARDED until T_data_duplicate = 10.0 s
```

`nextHops` en çok iki eleman içerir: primary + bir alternate. Bu, `MaxReplicaFanout=2` toplam sınırını uygular. Primary tek başına iletiliyorsa RB azaltılmaz. Ek kopya yaratılmışsa her iki çıkış kopyasında RB bir azaltılır. Daha aşağıda yeniden çoğaltma, yalnız selected Replication-Budget profili izin veriyorsa mümkündür; ilk-sürüm için §10'daki `RB ∈ {0,1}` önerisi kabul edilirse hiçbir downstream kopya tekrar çoğaltamaz.

```text
on field becomes FORWARDABLE(K):
    for each HELD data bound to K whose buffer lifetime has not expired:
        ForwardData(data, K)

on data buffer quota/lifetime expiry:
    drop HELD data
    emit LocalDeliveryFailure(data, BUFFER_QUOTA or BUFFER_LIFETIME)
```

## 8. Timer dispatch özeti

| Timer | Handler |
|---|---|
| `T_idle_probe`, `T_fresh`, `T_probe_start`, `T_probe_session`, `T_retention` | §3 komşu algoritması |
| `T_adv_refresh`, `T_coalesce`, `T_urgent` | Güncel local finite/withdrawal state için ADS artışlı FIELD_UPDATE planla |
| Advertisement guard/expiry | SOLICITING başlat veya candidate'i çıkarıp `RecomputeField` çağır |
| `T_solicit_reply`, `T_solicit_backoff`, `T_req_retry`, `T_req_session`, `T_repair_max` | §5 acquisition/repair algoritması |
| `T_buffer[class]`, duplicate cache, withdrawal cache, retired OIID | İlgili kaydı sonlandır; forwarding state'i iyimser biçimde yenileme |
| `T_metric_epoch=0.5 s` | ACTIVE peer için `35` M0.1 Q/H/U/R/C güncellemesini yürüt; ilgili cached candidate alanlarında normal `RecomputeField` ve policy evidence değerlendirmesini çağır |
| Policy evidence/dwell | §22 policy geçişini uygula; safety result'i asla geçersiz kılma |

## 9. Uygulama değişmezleri

Bir implementasyon, event-handler sınırlarında en az aşağıdakileri assert edebilmelidir:

1. `F_i[K]=FORWARDABLE` ise `Succ_i[K]` ACTIVE ve safe'tir; değilse packet forward edilmez.
2. Aynı DFSN'de `FD_i[K]` artmaz veya resetlenmez.
3. Ara node hiçbir handler'da OIID/DFSN üretmez veya artırmaz.
4. Withdrawal finite candidate değildir; eski ADS/DFSN lifetime uzatmaz.
5. Her DFSN_REQUEST Request-ID'si bir node'da en fazla bir kez forward edilir.
6. Data duplicate cache, enqueue/forward/replicate öncesi rezerve edilir.
7. Policy, STALE/SUSPECT komşuyu veya unsafe candidate'i geçerli yapamaz.
8. Accepted FIELD_UPDATE target OriginSignature, DATA SourceSignature ve current HopSignature olmadan state/forwarding etkisi üretmez; forward edilmiş mutable alan değişikliği yeni HopSignature gerektirir.

## 10. Onaylanmış algoritma kararları

İlk sürüm için aşağıdaki dört normatif ayrıntı proje sahibi tarafından onaylanmıştır:

1. **Tie-break:** Eşit toplam maliyette küçük `(NodeID, InstanceID)` seçilir.
2. **Hedefin DFSN yetkisi:** Target, yalnız current OIID/current DFSN ile tam eşleşen `FEASIBLE_STARVATION` isteğinde ve `RequestedMinimumDFSN = current + 1` ise DFSN'yi bir artırır; diğer geçerli isteklerde current origin update'i yollar.
3. **İlk acquisition paketi:** Önceki FORWARDABLE field yoksa ilk DATA, acquisition başlatabilir fakat repair buffer'a alınmaz; local delivery-failure üretir.
4. **İlk-sürüm RB profili:** Protection-eligible DATA girişinde `Replication-Budget` yalnız `0` veya `1` olabilir. `RB=1`, tek bir node'un primary + bir secondary oluşturmasına izin verir; iki çıkışta `RB=0` kalır ve downstream yeniden çoğaltma olmaz.

**Kazanç:** Deterministik successor seçimi, request kaynaklı DFSN sıçramasını önleme, buffer kapsamının açık kalması ve ilk sürümde paket-başına iki çıkıştan büyük replication ağacının önlenmesi sağlanır. Algoritmalar, onaylı state/timer/wire sözleşmesini doğrudan uygular.

**Bedel:** İlk data paketi field edinimini beklemez; target, bazı freshness ambiguity isteklerinde yeni DFSN üretmek yerine mevcut update'i tekrarlar. `RB>1` ile çok-atlama redundancy, daha gelişmiş trafik sınıfı veya çok-hedef profili ek state/bütçe algoritması gerektirir.

Bu ayrıntılar forwarding, recovery ve initial delivery davranışını etkileyen; proje sahibi tarafından onaylanmış MAJOR kararlardır.
