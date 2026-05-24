# No authentication required to add an email address.

## Metadata
- **Source:** HackerOne
- **Report:** 139965 | https://hackerone.com/reports/139965
- **Submitted:** 2016-05-20
- **Reporter:** apok
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi Team,
I hope this mongoose I'm sending will help make phabricator safer.

Description:
==========
The issue in question, is that whenever you add a new email address to your account, no additional authentication is required. Furthermore, when the account has 2FA enabled, it's not necessary to enter high security mode when adding a new email address (But it is necessary to authenticate and login

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
I hope this mongoose I'm sending will help make phabricator safer.

Description:
==========
The issue in question, is that whenever you add a new email address to your account, no additional authentication is required. Furthermore, when the account has 2FA enabled, it's not necessary to enter high security mode when adding a new email address (But it is necessary to authenticate and login).

Of course a malicious individual would have to have access to an open account or hijack the session cookie. But since the session cookies have a long expiration period, it makes this attack more plausible. Specially considering that most people don't logout of their accounts when they are done using them, they just close the tab/browser.

Impact:
=======
A malicious individual with access to an account, can add and validate an email address which can later on be used to get a one time login link and change the user password, thus compromising the account completely.

Recommendation:
===============
Enforce asking the user for the account password prior to adding the new email address. In addition, if 2FA is active on the account, require high security mode to add a new email address.

I'm attaching screenshots of a step by step.
Kind Regards,
Alex.

</details>

---
*Analysed by Claude on 2026-05-24*
