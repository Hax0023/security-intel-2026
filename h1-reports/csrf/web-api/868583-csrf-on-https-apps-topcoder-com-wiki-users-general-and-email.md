# CSRF on https://apps.topcoder.com/wiki/users general and email preferences

## Metadata
- **Source:** HackerOne
- **Report:** 868583 | https://hackerone.com/reports/868583
- **Submitted:** 2020-05-07
- **Reporter:** meryem0x
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi :) There is a CSRF on setting general and email preferences.

## Steps To Reproduce:
There is no CSRF token or anything like that on https://apps.topcoder.com/wiki/users/editmypreferences.action and  https://apps.topcoder.com/wiki/users/editemailpreferences.action . I added the poc html files below. Attacker can change victim's preferences.

Note: This only works to signed-in users.

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

## Summary:
Hi :) There is a CSRF on setting general and email preferences.

## Steps To Reproduce:
There is no CSRF token or anything like that on https://apps.topcoder.com/wiki/users/editmypreferences.action and  https://apps.topcoder.com/wiki/users/editemailpreferences.action . I added the poc html files below. Attacker can change victim's preferences.

Note: This only works to signed-in users. There is a mistake on https://apps.topcoder.com/wiki/login.action now. If you encounter an error, you can login on main site (https://accounts.topcoder.com/member) then try.

## Impact

An attacker can force other users to change their preferences without their knowledge.

</details>

---
*Analysed by Claude on 2026-05-24*
