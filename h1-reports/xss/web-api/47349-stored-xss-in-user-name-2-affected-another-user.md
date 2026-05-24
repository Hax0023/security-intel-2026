# Stored xss in user name (2) affected another user.

## Metadata
- **Source:** HackerOne
- **Report:** 47349 | https://hackerone.com/reports/47349
- **Submitted:** 2015-02-10
- **Reporter:** 4lemon
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Again we have to users:
A - attacker
B - victim

User A (attacker) has name - name<script>alert(1)</script> and add auth to user B (victim).
User B receive a letter and get remider about new request on website. And open it
https://mobilevikings.com/account/requests/
And probably press "Accept" and got xss fired.
x:confirm parameter is the reason of this issue.

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

Again we have to users:
A - attacker
B - victim

User A (attacker) has name - name<script>alert(1)</script> and add auth to user B (victim).
User B receive a letter and get remider about new request on website. And open it
https://mobilevikings.com/account/requests/
And probably press "Accept" and got xss fired.
x:confirm parameter is the reason of this issue.

</details>

---
*Analysed by Claude on 2026-05-24*
