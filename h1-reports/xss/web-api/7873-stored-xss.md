# Stored XSS

## Metadata
- **Source:** HackerOne
- **Report:** 7873 | https://hackerone.com/reports/7873
- **Submitted:** 2014-04-17
- **Reporter:** mickyd
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hey!!

Steps to reproduce :

1) while making account add xss payload in username like : "><img src=a onerror=prompt(1);>
2) login using this .
3) Go to settings tab (http://www.localize.io/pages/settings)
4) XSS ll get executed .

Attached PoC .

Daksh

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

Hey!!

Steps to reproduce :

1) while making account add xss payload in username like : "><img src=a onerror=prompt(1);>
2) login using this .
3) Go to settings tab (http://www.localize.io/pages/settings)
4) XSS ll get executed .

Attached PoC .

Daksh

</details>

---
*Analysed by Claude on 2026-05-24*
