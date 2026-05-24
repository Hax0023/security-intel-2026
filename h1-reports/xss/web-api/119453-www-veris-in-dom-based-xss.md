# www.veris.in DOM based XSS

## Metadata
- **Source:** HackerOne
- **Report:** 119453 | https://hackerone.com/reports/119453
- **Submitted:** 2016-02-29
- **Reporter:** reactors08
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,
An attacked can execute arbitrary js at your main page 
https://www.veris.in/?#<img src=x onerror=alert(1)>

vulnerable js source:
https://www.veris.in/wp-content/plugins/Ultimate_VC_Addons/assets/min-js/ultimate.min.js?ver=7e111f63322706ef9e00ec1e58f2edf4

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

Hi,
An attacked can execute arbitrary js at your main page 
https://www.veris.in/?#<img src=x onerror=alert(1)>

vulnerable js source:
https://www.veris.in/wp-content/plugins/Ultimate_VC_Addons/assets/min-js/ultimate.min.js?ver=7e111f63322706ef9e00ec1e58f2edf4

</details>

---
*Analysed by Claude on 2026-05-24*
