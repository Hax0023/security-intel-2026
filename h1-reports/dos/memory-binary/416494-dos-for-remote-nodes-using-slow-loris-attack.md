# DoS for remote nodes using Slow Loris attack

## Metadata
- **Source:** HackerOne
- **Report:** 416494 | https://hackerone.com/reports/416494
- **Submitted:** 2018-09-30
- **Reporter:** sobhraj_charles
- **Program:** Monero
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Incomplete Resource Cleanup
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Monero daemon is vulnerable to Slow Loris attacks, which can render RPC endpoints unresponsive by exhausting connection resources. An attacker can target multiple remote nodes simultaneously by slowly sending HTTP requests to keep connections alive, preventing legitimate RPC requests from being processed.

## Attack scenario
1. Attacker identifies publicly exposed Monero remote nodes via services like moneroworld.com
2. Attacker initiates Slow Loris attack tool with 1000+ concurrent sockets to target node's RPC endpoint (port 18089)
3. Attacker sends HTTP headers slowly and partial payloads to keep connections alive indefinitely
4. Daemon exhausts available connection pool/file descriptors handling slow connections
5. Legitimate RPC requests timeout or are rejected due to resource exhaustion
6. Node becomes unresponsive to all RPC queries until daemon restart

## Root cause
The daemon does not implement proper connection timeout mechanisms, connection limits, or rate limiting on the HTTP server handling RPC requests. The application holds resources (file descriptors, memory, connection slots) for slow or incomplete HTTP requests without enforcing reasonable completion timeouts.

## Attacker mindset
An attacker seeks to disrupt cryptocurrency infrastructure by targeting publicly accessible remote nodes. By leveraging a well-known attack technique (Slow Loris) with minimal resources, they can achieve widespread impact across multiple nodes in the network, affecting users relying on these services for wallet operations.

## Defensive takeaways
- Implement aggressive HTTP request timeouts (both overall and per-header)
- Enforce strict connection limits per IP/globally on RPC endpoints
- Add rate limiting and request throttling mechanisms
- Use HTTP server hardening techniques: limit header size, enforce maximum request completion time
- Deploy reverse proxy (nginx/HAProxy) with Slow Loris protection before exposing RPC
- Monitor for connection exhaustion and implement alerting
- Restrict RPC endpoint access to trusted networks when possible
- Implement connection pooling with configurable limits

## Variant hunting
Test other cryptocurrency daemons (Bitcoin, Ethereum nodes) for similar Slow Loris vulnerabilities
Check if similar attacks work via WebSocket endpoints if implemented
Investigate partial request attacks with other HTTP methods (PUT, PATCH, DELETE)
Test against gRPC or other protocol endpoints if available
Check if connection limits can be bypassed by rotating source IPs

## MITRE ATT&CK
- T1499.4
- T1201

## Notes
This is a classic application-layer DoS vulnerability. The attack requires no authentication and can be performed from a single machine against multiple targets. The fix requires defensive HTTP server hardening rather than just application-level changes. Monero v0.12.3.0 and earlier confirmed vulnerable; scope of later versions not specified in report.

## Full report
<details><summary>Expand</summary>

**Summary:** 

Using the slow loris attack it's possible to make the the daemon unresponsive to all RPC requests without at least a restart.

**Description:** 

I used this node.js application (https://www.npmjs.com/package/sloww) to perform the attack on one of my remote nodes, but any other implementation of the attack should also work fine.

## Releases Affected:

  * Ubuntu 16.04 x64 - Monero v0.12.3.0 was affected so all releases before should be affected as well.
  
## Steps To Reproduce:

  1. Start the daemon with standard remote node parameters like `./monerod --rpc-bind-ip 0.0.0.0 --confirm-external-bind`
  2. Start the slow loris attack, I tested with 1000 sockets opened and 700 milliseconds as rate at which 
      packets should be sent.
  3. Try sending a normal RPC command like `curl -X POST http://IP:18089/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_block_count"}' -H 'Content-Type: application/json'` there will not be any response from the RPC a few seconds after the attack was started.

## Impact

An attacker could target a large number of remote nodes for example the ones under https://moneroworld.com/, with just a single PC.

</details>

---
*Analysed by Claude on 2026-05-24*
