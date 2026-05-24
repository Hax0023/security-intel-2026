# Sign-up Form CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 7865 | https://hackerone.com/reports/7865
- **Submitted:** 2014-04-17
- **Reporter:** robin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Cross-site request forgery, also known as a one-click attack or session riding and abbreviated as CSRF or XSRF, is a type of malicious exploit of a website whereby unauthorized commands are transmitted from a user that the website trusts.


Form action: http://www.localize.io/pages/sign_up
Form method: POST

Form inputs:

sign_up[type] [Radio]
sign_up[username] [Text]
sign_up[password1] 

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

Cross-site request forgery, also known as a one-click attack or session riding and abbreviated as CSRF or XSRF, is a type of malicious exploit of a website whereby unauthorized commands are transmitted from a user that the website trusts.


Form action: http://www.localize.io/pages/sign_up
Form method: POST

Form inputs:

sign_up[type] [Radio]
sign_up[username] [Text]
sign_up[password1] [Password]
sign_up[password2] [Password]


The impact of this vulnerability:-

An attacker may force the users of a web application to execute actions of the attacker's choosing. A successful CSRF exploit can compromise end user data and operation in case of normal user. If the targeted end user is the administrator account, this can compromise the entire web application.

How to fix this vulnerability:-

Check if this form requires CSRF protection and implement CSRF countermeasures if necessary.


</details>

---
*Analysed by Claude on 2026-05-24*
