# XSS via password recovering

## Metadata
- **Source:** HackerOne
- **Report:** 131123 | https://hackerone.com/reports/131123
- **Submitted:** 2016-04-15
- **Reporter:** codequick
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
I found that xss can be executed if we provide xss payload as a password in Uber during password recovery.

Steps to follow:

1) Goto https://login.uber.com/forgot-password
2) Enter email and submit
3) Open the recover link you got
4) Enter Set password: <script>alert(document.domain);</script> and submit it
5) Click Show password

 XSS Executed.

Video and screenshot added

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

I found that xss can be executed if we provide xss payload as a password in Uber during password recovery.

Steps to follow:

1) Goto https://login.uber.com/forgot-password
2) Enter email and submit
3) Open the recover link you got
4) Enter Set password: <script>alert(document.domain);</script> and submit it
5) Click Show password

 XSS Executed.

Video and screenshot added

</details>

---
*Analysed by Claude on 2026-05-24*
