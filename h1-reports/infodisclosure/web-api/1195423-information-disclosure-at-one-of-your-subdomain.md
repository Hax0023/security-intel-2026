# Information Disclosure of Internal IPs and Ports via RPC Endpoints

## Metadata
- **Source:** HackerOne
- **Report:** 1195423 | https://hackerone.com/reports/1195423
- **Submitted:** 2021-05-13
- **Reporter:** omemishra
- **Program:** Sifchain
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Network Topology Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
RPC endpoints at rpc.sifchain.finance and rpc-testnet.sifchain.finance expose sensitive network information including internal IP addresses and port numbers through the /net_info endpoint. This information disclosure allows attackers to map the network topology and conduct targeted attacks against internal services.

## Attack scenario
1. Attacker discovers RPC endpoints by enumerating subdomains or public documentation
2. Attacker accesses /net_info endpoint which returns network peer information including internal IPs
3. Attacker extracts internal IP addresses, ports, and node identifiers from the response
4. Attacker uses this topology information to map internal network architecture and identify target services
5. Attacker conducts reconnaissance or direct attacks against discovered internal services
6. Attacker exploits knowledge of origin IPs to perform targeted DDoS or exploitation campaigns

## Root cause
RPC endpoint exposed sensitive debugging/administrative endpoints (/net_info) publicly without authentication or access restrictions. The endpoint returns detailed peer network information meant for internal monitoring rather than public exposure.

## Attacker mindset
Reconnaissance-focused attacker seeking to map target infrastructure and identify attack surface before launching exploitation. Intelligence gathering for network topology enables more precise and effective attacks against critical services.

## Defensive takeaways
- Restrict access to debugging endpoints like /net_info to internal networks or authenticated users only
- Implement authentication and authorization checks on all RPC endpoints
- Filter sensitive network information from API responses exposed to untrusted clients
- Use separate internal and external RPC endpoints with different security postures
- Monitor and alert on access to sensitive endpoints from external sources
- Implement rate limiting and request filtering on RPC endpoints
- Review all exposed endpoints for information disclosure vulnerabilities
- Document which endpoints should never be publicly accessible

## Variant hunting
Search for other exposed RPC endpoints or similar blockchain infrastructure with /net_info access
Test other debugging endpoints like /debug, /health, /peers, /status for information disclosure
Check staging/testnet environments for overly permissive configurations that may exist in production
Enumerate other Sifchain subdomains for similar exposure patterns
Test WebSocket RPC endpoints for same information disclosure issues
Review other blockchain projects' RPC implementations for similar misconfigurations

## MITRE ATT&CK
- T1592 - Gather Victim Network Information
- T1526 - Exposure of Infrastructure
- T1589 - Gather Victim Identity Information
- T1590 - Gather Victim Network Information

## Notes
The report lacks technical depth and specific response examples, but correctly identifies a real security issue. RPC endpoints commonly expose network debugging information that should be restricted. The vulnerability severity depends on how much sensitive information is actually disclosed and whether it directly enables exploitation of other systems. This is a common misconfiguration in blockchain infrastructure.

## Full report
<details><summary>Expand</summary>

Dear Team,

Hope you are doing very well and safe.
I was looking into your application and i find some bugs on your application which is disclosing internal port and also the ips.

That can leads an attacker to do lots of serious attacks.

Please verify:-
https://rpc.sifchain.finance/
https://rpc-testnet.sifchain.finance/
https://rpc.sifchain.finance/net_info?
https://rpc-testnet.sifchain.finance/net_info?

## Impact

1. Critical information disclosure leads an attacker to do direct attack on your services and origin ip.

Thanks & Regards
Ome

</details>

---
*Analysed by Claude on 2026-05-24*
