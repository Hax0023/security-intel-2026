# CSRF to make any user accept the invitation to the team

## Metadata
- **Source:** HackerOne
- **Report:** 360834 | https://hackerone.com/reports/360834
- **Submitted:** 2018-06-01
- **Reporter:** albatraoz
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
#Description:
The victim can be tricked into accepting the invite as a normal GET request is sent while accepting the request.

#Steps to reproduce
Make an html page using the following code:
```
<a href="https://liberapay.com/test/membership/accept">click here</a>
```
Change" test" with your team mate.

## Impact

The impact is low but still it can make a user to accept the request even if he wan

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

#Description:
The victim can be tricked into accepting the invite as a normal GET request is sent while accepting the request.

#Steps to reproduce
Make an html page using the following code:
```
<a href="https://liberapay.com/test/membership/accept">click here</a>
```
Change" test" with your team mate.

## Impact

The impact is low but still it can make a user to accept the request even if he wanted not to.

</details>

---
*Analysed by Claude on 2026-05-24*
