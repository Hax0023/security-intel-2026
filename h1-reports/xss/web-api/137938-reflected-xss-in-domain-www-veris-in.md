# Reflected XSS in domain www.veris.in

## Metadata
- **Source:** HackerOne
- **Report:** 137938 | https://hackerone.com/reports/137938
- **Submitted:** 2016-05-11
- **Reporter:** aziose
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi tream,

veris.in is vulnerable  reflected XSS that stems from an insecure URL sanitization process performed in the file flashmediaelement.swf

PoC:
===
https://www.veris.in/wp-includes/js/mediaelement/flashmediaelement.swf?jsinitfunctio%gn=alert`1`

Fix:
===
Update to WordPress 4.5.2

regards,
aziose




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

Hi tream,

veris.in is vulnerable  reflected XSS that stems from an insecure URL sanitization process performed in the file flashmediaelement.swf

PoC:
===
https://www.veris.in/wp-includes/js/mediaelement/flashmediaelement.swf?jsinitfunctio%gn=alert`1`

Fix:
===
Update to WordPress 4.5.2

regards,
aziose




</details>

---
*Analysed by Claude on 2026-05-24*
