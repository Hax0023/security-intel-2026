# Lack of CSRF token validation at server side

## Metadata
- **Source:** HackerOne
- **Report:** 163815 | https://hackerone.com/reports/163815
- **Submitted:** 2016-08-27
- **Reporter:** yodha
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Description: Gratipay is not validating csrf token at server side for few requests. So csrf protection is not implemented application wide.

Proof of concept (Video):https://drive.google.com/file/d/0B8z7y7DxxQbwUHY4YTduYzMxbnc/view?usp=sharing

Recommended Fix:
For CSRF Protection:
1. Each critical operation request must be accompanied with a "token"
•Token is:
- Long, Random, not repeated for app

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

Description: Gratipay is not validating csrf token at server side for few requests. So csrf protection is not implemented application wide.

Proof of concept (Video):https://drive.google.com/file/d/0B8z7y7DxxQbwUHY4YTduYzMxbnc/view?usp=sharing

Recommended Fix:
For CSRF Protection:
1. Each critical operation request must be accompanied with a "token"
•Token is:
- Long, Random, not repeated for application lifetime.
- Unique per session or even per operation
- Part of URL in GET
- Hidden Field in POST (forms)
- Attacker cannot know / predict this token and hence cannot create requests to exploit the operation.

</details>

---
*Analysed by Claude on 2026-05-24*
