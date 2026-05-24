# xss on reset password page

## Metadata
- **Source:** HackerOne
- **Report:** 1763404 | https://hackerone.com/reports/1763404
- **Submitted:** 2022-11-06
- **Reporter:** 0x53_0x52_0x59
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
target:https://█████/Default.aspx?TabId=81&ctl=SendPassword&returnurl=%252fUOTSHelpDesk

When a user goes on the forget password page and enters a username it is reflected onto the page. An attacker could simply enter a username like <script>alert(1)</script> and it would execute an alert not to mention there is no csrf protection allowing a attacker to possibly chain csrf with this and cause alot

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

target:https://█████/Default.aspx?TabId=81&ctl=SendPassword&returnurl=%252fUOTSHelpDesk

When a user goes on the forget password page and enters a username it is reflected onto the page. An attacker could simply enter a username like <script>alert(1)</script> and it would execute an alert not to mention there is no csrf protection allowing a attacker to possibly chain csrf with this and cause alot of harm.


references:
https://owncloud.com/security-advisories/reflected-xss-in-login-page-forgot-password-functionallity/
https://hackerone.com/reports/125059

## Impact

an attacker could steal cookies from a user social engineer them or redirect them

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
go to https://████/Default.aspx?TabId=81&ctl=SendPassword&returnurl=%252fUOTSHelpDesk
enter a payload in username field

## Suggested Mitigation/Remediation Actions
put a character limit and sanitize user input



</details>

---
*Analysed by Claude on 2026-05-24*
