# CSRF with logout action

## Metadata
- **Source:** HackerOne
- **Report:** 1971589 | https://hackerone.com/reports/1971589
- **Submitted:** 2023-05-03
- **Reporter:** mbi3s
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi, I wanted let you know and saw that previously similar issue was fixed.
Repro steps: Go to https://weblate.org/pl/ and click top right icon for logging in (user-tab user-anonymous, https://weblate.org/saml2/login/?next=/pl/).
Log in using username and password (https://hosted.weblate.org/accounts/login/?next=/idp/login/process/). 
Logged in on site https://weblate.org/pl/ use link: https://webl

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

Hi, I wanted let you know and saw that previously similar issue was fixed.
Repro steps: Go to https://weblate.org/pl/ and click top right icon for logging in (user-tab user-anonymous, https://weblate.org/saml2/login/?next=/pl/).
Log in using username and password (https://hosted.weblate.org/accounts/login/?next=/idp/login/process/). 
Logged in on site https://weblate.org/pl/ use link: https://weblate.org/logout/
See logged out.

The similar result with using external page with prepared CSRF payload like:
`<a href="https://weblate.org/logout/"> Click me to see bonus pack`
Here as logged in user use this link from external page, next go to tab where logged in and refresh the page - see logged out there too.

Best regards,

## Impact

Bad actor can affect the user's login status - logged out.

</details>

---
*Analysed by Claude on 2026-05-24*
