# Stored XSS on new Calling plugin (spreed)

## Metadata
- **Source:** HackerOne
- **Report:** 190870 | https://hackerone.com/reports/190870
- **Submitted:** 2016-12-13
- **Reporter:** coolboss
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
There's a stored xss vulnerability ....

Proof Of Concept :
===============
1. Set `name` as an xss payload like `"x><img src=a onerror=alert(1)>`.
{F143238}
2. Invite people to single call room.
3. Xss will execute in IE. (It doesn't support CSP)
{F143237}

Impact :
========
Admin user can be xssed via this method if admin uses browsers like IE.

Let me know if you need help in reproducing

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

There's a stored xss vulnerability ....

Proof Of Concept :
===============
1. Set `name` as an xss payload like `"x><img src=a onerror=alert(1)>`.
{F143238}
2. Invite people to single call room.
3. Xss will execute in IE. (It doesn't support CSP)
{F143237}

Impact :
========
Admin user can be xssed via this method if admin uses browsers like IE.

Let me know if you need help in reproducing

</details>

---
*Analysed by Claude on 2026-05-24*
