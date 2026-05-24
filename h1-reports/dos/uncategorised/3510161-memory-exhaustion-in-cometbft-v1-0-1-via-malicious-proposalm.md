# Memory Exhaustion in CometBFT v1.0.1 via Malicious ProposalMessage Leading to Network-Wide DoS

## Metadata
- **Source:** HackerOne
- **Report:** 3510161 | https://hackerone.com/reports/3510161
- **Submitted:** 2026-01-14
- **Reporter:** 0xjam
- **Program:** CometBFT
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln:** Denial of Service (Memory Exhaustion), Unvalidated Input Processing, Unbounded Memory Allocation, P2P Protocol Vulnerability
- **CVEs:** None
- **Category:** uncategorised

## Summary
CometBFT v1.0.1 fails to validate the PartSetHeader.Total field before memory allocation in ProposalMessage processing, allowing attackers to trigger immediate 512MB allocations via a ~50-byte P2P message. A single attacker can halt consensus on networks like Berachain (69 validators) by crashing just 23 validators with minimal bandwidth (~1.15 KB total).

## Attack scenario
1. Attacker establishes P2P connection to target CometBFT v1.0.1 node on port 26656
2. Attacker crafts malicious ProposalMessage with PartSetHeader.Total set to 2^32-1 (4,294,967,295)
3. Malicious message is routed to consensus reactor (reactor.go:334-336) without input validation
4. Node attempts to allocate memory via bit_array.go:31 based on unvalidated Total field, requesting 512MB
5. Operating system OOM killer terminates the node within ~10ms of message receipt
6. Attacker repeats process against 23+ validators in 69-validator network to achieve consensus failure

## Root cause
Input validation for PartSetHeader.Total is performed too late in the execution flow (consensus/state.go:2075-2077) after memory allocation has already occurred in bit_array.go:31. The ProposalMessage handler lacks pre-allocation bounds checking, allowing attackers to control allocation size directly via an untrusted P2P message field.

## Attacker mindset
An attacker with P2P network access seeks to economically disrupt blockchain consensus. The vulnerability is attractive because: (1) minimal bandwidth required (~50 bytes), (2) deterministic crash with no mitigation, (3) low barrier to entry (any P2P peer), (4) affects all validators equally, and (5) complete network halt achievable with <34% validator targeting. Motivation could be economic (shorting token), political (network disruption), or competitive (chain sabotage).

## Defensive takeaways
- Validate all untrusted input at entry points before any resource allocation occurs
- Implement bounds checking on message fields that control memory allocation (establish maximum reasonable values)
- Add pre-flight sanity checks for PartSetHeader.Total against block size limits (typically 100MB max, Total should be <100 for 1MB parts)
- Apply rate limiting and peer reputation scoring to P2P message handlers to slow down DoS attacks
- Implement resource quotas and circuit breakers to prevent single messages from allocating excessive memory
- Add monitoring/alerting for memory allocation spikes correlated with specific message types
- Require explicit field validation before passing to downstream processing functions
- Consider staged allocation with early validation gates rather than eager allocation

## Variant hunting
Secondary vulnerability exists in InitProposalBlockParts() (reactor.go:1184) exploitable via NewValidBlockMessage, suggesting systematic validation gaps in message handlers. Hunt for other message types with untrusted numeric fields controlling allocation: BlockPartMessage, VoteMessage, ProposalPOLMessage. Check for similar patterns in other P2P consensus layers (Tendermint, other BFT implementations). Examine all NewBitArray() calls for upstream validation. Test maximum field values in all structs passed through MsgTypeXXX handlers.

## MITRE ATT&CK
- T1190
- T1561
- T1499
- T1499.4

## Notes
Proof of concept is trivially reproducible. Upstream v0.38.20 contains working mitigation. Impact is network-wide rather than isolated; a single attacker can halt any CometBFT v1.0.1 network. No effective workaround exists without code patch. Attack is indistinguishable from legitimate traffic to naive monitoring. This vulnerability highlights the critical importance of validating P2P message fields before resource-intensive operations in consensus-critical software.

## Full report
<details><summary>Expand</summary>

### Summary of Impact
CometBFT v1.0.1 contains a critical memory exhaustion vulnerability that allows any peer to crash nodes with a single ~50-byte P2P message. An attacker can send a malicious `ProposalMessage` with `PartSetHeader.Total` set to `2^32-1`, causing the receiving node to immediately allocate 512 MB of memory without prior validation, resulting in an OOM kill.

The impact is complete network denial of service. For a 69-validator network (like Berachain mainnet), an attacker can halt consensus by crashing just 23 validators (34%) with only 1.15 KB of bandwidth.

Severity: HIGH/CRITICAL (depends on chain, if being validator is permissionless etc)

### Steps to Reproduce

1. Create a malicious `ProposalMessage` with `PartSetHeader.Total` set to `2^32-1` (4,294,967,295)
2. Connect to a target node running CometBFT v1.0.1 via P2P protocol
3. Send the malicious message to the target node
4. The node will immediately allocate 512 MB of memory and be terminated by the OOM killer

Vulnerable code path:
- Entry point: `internal/consensus/reactor.go:334-336` - No validation before processing
- Unvalidated allocation: `internal/consensus/reactor.go:1169` - Attacker controls Total value
- Unsafe allocation: `internal/bits/bit_array.go:31` - Unbounded memory allocation
- Validation that never executes: `internal/consensus/state.go:2075-2077` - Too late in execution flow

A second vulnerability vector exists in `InitProposalBlockParts()` at `reactor.go:1184` which may be exploitable via `NewValidBlockMessage` or other message types.

### Workarounds
No effective mitigation exists without a code patch. Operators must manually restart nodes after they crash.

### Supporting Material/References

* Proof of Concept:
```go
package main

import (
    "math"
    "github.com/cometbft/cometbft/types"
    cmtcons "github.com/cometbft/cometbft/api/cometbft/consensus/v1"
)

func main() {
    // Create malicious proposal
    proposal := types.NewProposal(1, 0, -1, types.BlockID{
        Hash: make([]byte, 32),
        PartSetHeader: types.PartSetHeader{
            Total: math.MaxUint32,  // 2^32-1 = 4,294,967,295
            Hash:  make([]byte, 32),
        },
    }, nil)
    proposal.Signature = []byte{0x01}
    
    // Send to target node on port 26656
    // (P2P connection and handshake code omitted for brevity)
    
    // Result: Target node crashes within 10ms
}
```

* Affected networks include Berachain mainnet (69 validators) and potentially all blockchain networks using CometBFT v1.0.1
* Upstream v0.38.20 version correctly mitigates the issue

</details>

---
*Analysed by Claude on 2026-05-24*
