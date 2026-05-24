# Stored xss in user name

## Metadata
- **Source:** HackerOne
- **Report:** 47343 | https://hackerone.com/reports/47343
- **Submitted:** 2015-02-10
- **Reporter:** 4lemon
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
In prev report i showed xss in user name thru cookie, there is another place where this name shows and fired xss.
After send auth request open https://mobilevikings.be/en/account/authorization/overview/ in account who send request and press "Remove authorization" and got another way to fire xss payload.
param x:authorization-to-first-name is properly sanitized but probably when it goes to modal 

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

In prev report i showed xss in user name thru cookie, there is another place where this name shows and fired xss.
After send auth request open https://mobilevikings.be/en/account/authorization/overview/ in account who send request and press "Remove authorization" and got another way to fire xss payload.
param x:authorization-to-first-name is properly sanitized but probably when it goes to modal window it unsanitize.

</details>

---
*Analysed by Claude on 2026-05-24*
