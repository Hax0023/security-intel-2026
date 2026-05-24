# Logout CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 223329 | https://hackerone.com/reports/223329
- **Submitted:** 2017-04-24
- **Reporter:** japz
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hi Team,

This is a low risk but want you to know that logout on this domain `demo.weblate.org` did not protect the logout form with csrf token, therefor i can logout any user by sending this url `https://demo.webplate.org/accounts/logout/`.

Logout should have post method with a valid csrf token.

Let me know if you need more info.

Regards
Japz

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

Hi Team,

This is a low risk but want you to know that logout on this domain `demo.weblate.org` did not protect the logout form with csrf token, therefor i can logout any user by sending this url `https://demo.webplate.org/accounts/logout/`.

Logout should have post method with a valid csrf token.

Let me know if you need more info.

Regards
Japz

</details>

---
*Analysed by Claude on 2026-05-24*
