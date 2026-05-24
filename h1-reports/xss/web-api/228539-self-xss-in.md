# self xss in

## Metadata
- **Source:** HackerOne
- **Report:** 228539 | https://hackerone.com/reports/228539
- **Submitted:** 2017-05-15
- **Reporter:** panther
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Quora security team,

there is self XSS vulnerability in https://www.quora.com/profile/Username/

Steps:

copy and paste the link in chrome browser (copy entire link within double quotes
**"javascript:alert(document.domain)//https://www.quora.com/profile/Username/"**

then XSS payload will trigger

please let me know if you need more information.

best

Panther

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

Hi Quora security team,

there is self XSS vulnerability in https://www.quora.com/profile/Username/

Steps:

copy and paste the link in chrome browser (copy entire link within double quotes
**"javascript:alert(document.domain)//https://www.quora.com/profile/Username/"**

then XSS payload will trigger

please let me know if you need more information.

best

Panther

</details>

---
*Analysed by Claude on 2026-05-24*
