# csrf token did not changed after login/logout many times

## Metadata
- **Source:** HackerOne
- **Report:** 361131 | https://hackerone.com/reports/361131
- **Submitted:** 2018-06-02
- **Reporter:** cryptographer
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
hello team, 
your csrf token did not expired and after login and logout many times , i found that your csrf token is generated same as last one.

## Impact

if an attacker found an xss on your domain and you fixed it but attacker still has csrf token of user, attacker can use it to perform any action.

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

hello team, 
your csrf token did not expired and after login and logout many times , i found that your csrf token is generated same as last one.

## Impact

if an attacker found an xss on your domain and you fixed it but attacker still has csrf token of user, attacker can use it to perform any action.

</details>

---
*Analysed by Claude on 2026-05-24*
