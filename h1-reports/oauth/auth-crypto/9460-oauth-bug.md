# OAuth Bug

## Metadata
- **Source:** HackerOne
- **Report:** 9460 | https://hackerone.com/reports/9460
- **Submitted:** 2014-04-24
- **Reporter:** atom
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
I read the bug of @melvin and I also try to bypass this
https://app.respond.ly/_oauth/twitter/?requestTokenAndRedirect=https://hackerone.com

so I made a bypassing tehcnique but didnt work 
https://app.respond.ly/_oauth/twitter/?requestTokenAndRedirect=//hackerone.com

But I think I found a bug 
This is the Screen shot: http://prntscr.com/3cu58e

When a user authorizes their twitter to co

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

I read the bug of @melvin and I also try to bypass this
https://app.respond.ly/_oauth/twitter/?requestTokenAndRedirect=https://hackerone.com

so I made a bypassing tehcnique but didnt work 
https://app.respond.ly/_oauth/twitter/?requestTokenAndRedirect=//hackerone.com

But I think I found a bug 
This is the Screen shot: http://prntscr.com/3cu58e

When a user authorizes their twitter to connect with the URL above they will encounter that error.

</details>

---
*Analysed by Claude on 2026-05-24*
