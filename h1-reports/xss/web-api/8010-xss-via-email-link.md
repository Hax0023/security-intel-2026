# XSS via Email Link

## Metadata
- **Source:** HackerOne
- **Report:** 8010 | https://hackerone.com/reports/8010
- **Submitted:** 2014-04-18
- **Reporter:** prakharprasad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hey,

So, we can send emails to team email address like  - **kfvm@mail.respond.ly** . In the email body if there is a hyperlink pointing to `javascript:alert(0);` or any other `javascript: URI` then open viewing the email in your web application with *original HTML* view and then on clicking it will trigger javascript execution, that is XSS.

Thanks!

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

Hey,

So, we can send emails to team email address like  - **kfvm@mail.respond.ly** . In the email body if there is a hyperlink pointing to `javascript:alert(0);` or any other `javascript: URI` then open viewing the email in your web application with *original HTML* view and then on clicking it will trigger javascript execution, that is XSS.

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
