# Libuv: Improper Domain Lookup that potentially leads to SSRF attacks

## Metadata
- **Source:** HackerOne
- **Report:** 2429894 | https://hackerone.com/reports/2429894
- **Submitted:** 2024-03-21
- **Reporter:** hunt1
- **Program:** Unknown
- **Bounty:** $4,860
- **Severity:** high
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** CVE-2024-24806
- **Category:** web-api

## Summary
I recently encountered a challenge in a CTF competition that led me to discover a vulnerability within Node.js, present in all versions after v10. Upon further investigation and code debugging, it became apparent that the vulnerability originated from its direct dependency, `libuv`.

I submitted a report to the Node.js team via HackerOne, and they subsequently connected me with the libuv team. Thi

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

I recently encountered a challenge in a CTF competition that led me to discover a vulnerability within Node.js, present in all versions after v10. Upon further investigation and code debugging, it became apparent that the vulnerability originated from its direct dependency, `libuv`.

I submitted a report to the Node.js team via HackerOne, and they subsequently connected me with the libuv team. This collaboration resulted in the identification and resolution of the vulnerability, now recorded as CVE-2024-24806.

## Impact

This vulnerability could allow an attacker to craft payloads that results in **SSRF** attacks and **Internal API Access**. Full explanation of vulnerability, PoC and sample scenarios are provided within the original report:
https://github.com/libuv/libuv/security/advisories/GHSA-f74f-cvh7-c6q6

</details>

---
*Analysed by Claude on 2026-05-24*
