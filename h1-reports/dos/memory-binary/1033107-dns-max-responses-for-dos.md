# DNS Max Responses Denial of Service in Node.js

## Metadata
- **Source:** HackerOne
- **Report:** 1033107 | https://hackerone.com/reports/1033107
- **Submitted:** 2020-11-12
- **Reporter:** zeus1999
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Unbounded Buffer/Memory Allocation
- **CVEs:** CVE-2020-8277
- **Category:** memory-binary

## Summary
Node.js DNS resolution functionality crashes or hangs when processing DNS responses with an excessive number of records (>1300 A records). An attacker controlling a domain with numerous DNS responses can trigger a DoS condition in any Node.js application performing DNS lookups on attacker-controlled domains.

## Attack scenario
1. Attacker registers or compromises a domain (e.g., ticbrasil.com.br) and configures it with 1300+ A record responses
2. Attacker tricks a Node.js application into resolving the attacker's domain via dns.resolve4() or similar DNS functions
3. Node.js DNS resolver receives the oversized response from the authoritative nameserver
4. Node.js fails to handle the large response set, causing memory exhaustion, buffer overflow, or hanging
5. Application becomes unresponsive or crashes, denying service to legitimate users
6. If attacker can influence DNS resolution targets through application logic (e.g., user-supplied hostnames), exploitation is trivial

## Root cause
Node.js DNS resolver lacks proper validation and limits on the number of DNS records it processes from a single response. The underlying C library or Node.js wrapper does not implement safeguards to prevent memory exhaustion when processing abnormally large DNS responses.

## Attacker mindset
Attacker seeks to weaponize public infrastructure (DNS) combined with application logic to achieve remote denial of service without authentication. Targeting widespread Node.js deployments, the attacker leverages inherent trust in DNS protocol to bypass input validation.

## Defensive takeaways
- Implement maximum limits on the number of DNS records accepted per response
- Add timeouts and resource quotas for DNS resolution operations
- Validate DNS response sizes and record counts before processing
- Use private security disclosure processes immediately when security issues are suspected rather than public GitHub issues
- Implement rate limiting on DNS queries to prevent abuse
- Consider sandboxing or isolating DNS resolution operations
- Monitor DNS query patterns for anomalies indicating potential attacks

## Variant hunting
Search for similar unbounded resource handling in: CNAME chaining attacks, TXT record flooding, NS record enumeration DoS, MX record explosion, SRV record proliferation attacks. Check other DNS libraries (c-ares, libuv, getdns) for identical patterns. Examine IPv6 (AAAA) and other record types for same issue.

## MITRE ATT&CK
- T1498.002
- T1190

## Notes
This vulnerability was publicly disclosed on GitHub before proper security disclosure process was followed, creating a zero-day window for attackers. The maintainer (@jasnell) correctly identified the breach of responsible disclosure protocol. Affected versions include v12.18.4 and v14.15.0. The issue demonstrates how seemingly innocuous features (DNS resolution) can become attack vectors when combined with unbounded resource consumption. Practical exploitation requires either social engineering or MITM positioning, but the impact is severe for internet-facing Node.js services.

## Full report
<details><summary>Expand</summary>

See Github (my issue): https://github.com/nodejs/node/issues/36063


When i try to fetch the A Dns records of following domain: ticbrasil.com.br I dont get any response.
I think thats the case because there are over 1300 responses.

Version: v12.18.4, v14.15.0
Platform: 64-bit Windows 10 Pro & Enterprise

What steps will reproduce the bug?
var dns = require('dns'); dns.resolve4('ticbrasil.com.br', function (err, addresses, family) { console.log(err); console.log(addresses); console.log(family); });

How often does it reproduce? Is there a required condition?
It happends everytime

What is the expected behavior?
https://pastebin.com/Tv53Na89

What do you see instead?
Nothing/No output

## Impact

mmomtchev commented 3 hours ago
@mhdawson someone should contact Mitre or whoever you usually contact, this is a confirmed remote security vulnerability. If an attacker can trigger a DNS resolution for an address chosen by him, then it is exploitable for DoS. It is a very high-risk vulnerability. I don't think a remote access is possible, but this should probably be evaluated by an expert.

@jasnell
 
Member
jasnell commented 2 hours ago
We can look into this further but I have to point out: we have a defined process for properly reporting and investigating potential security vulnerabilities. As soon as this issue was suspected as being a security issue, that process should have been followed with investigation and fixes investigated in the private Node.js repo we use for that purpose, otherwise this ends up risking a zero-day for all Node.js users.

</details>

---
*Analysed by Claude on 2026-05-24*
