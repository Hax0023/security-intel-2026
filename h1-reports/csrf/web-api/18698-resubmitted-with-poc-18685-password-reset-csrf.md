# Resubmitted with POC #18685 Password reset CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 18698 | https://hackerone.com/reports/18698
- **Submitted:** 2014-07-01
- **Reporter:** shahmeer-amir
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Hey there
I found out that an attacker can use the password reset link to forge requests because there is no CSRF token in that particular request to validate that request. You should always have a CSRF token in the password reset request.


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

Hey there
I found out that an attacker can use the password reset link to forge requests because there is no CSRF token in that particular request to validate that request. You should always have a CSRF token in the password reset request.


</details>

---
*Analysed by Claude on 2026-05-24*
