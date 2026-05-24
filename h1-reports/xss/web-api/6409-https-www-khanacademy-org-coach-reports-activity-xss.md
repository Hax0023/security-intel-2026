# https://www.khanacademy.org/coach/reports/activity XSS

## Metadata
- **Source:** HackerOne
- **Report:** 6409 | https://hackerone.com/reports/6409
- **Submitted:** 2014-04-08
- **Reporter:** smiegles
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,

I created a class called `"><img src=x onerror=alert(4)>`, I hope that you know how to make a class..
After that, when you go to https://www.khanacademy.org/coach/reports/activity and select a class it might not load directly but when you reloud the page it will (and persistent).

Best regards,

Olivier Beg

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

I created a class called `"><img src=x onerror=alert(4)>`, I hope that you know how to make a class..
After that, when you go to https://www.khanacademy.org/coach/reports/activity and select a class it might not load directly but when you reloud the page it will (and persistent).

Best regards,

Olivier Beg

</details>

---
*Analysed by Claude on 2026-05-24*
