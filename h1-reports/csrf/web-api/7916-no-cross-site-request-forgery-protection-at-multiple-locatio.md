# No Cross-Site Request Forgery protection at multiple locations

## Metadata
- **Source:** HackerOne
- **Report:** 7916 | https://hackerone.com/reports/7916
- **Submitted:** 2014-04-17
- **Reporter:** melvin
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
The Localize application does not provide protection against CSRF attacks at various locations. 
For example, the following actions/pages are vulnerable:

`POST /pages/create_project`
`POST /pages/settings`
`POST /add_phrase/$var/languages/$var`


See https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF) for more information.


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

The Localize application does not provide protection against CSRF attacks at various locations. 
For example, the following actions/pages are vulnerable:

`POST /pages/create_project`
`POST /pages/settings`
`POST /add_phrase/$var/languages/$var`


See https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF) for more information.


</details>

---
*Analysed by Claude on 2026-05-24*
