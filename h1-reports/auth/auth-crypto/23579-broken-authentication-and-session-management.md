# Broken Authentication and Session Management

## Metadata
- **Source:** HackerOne
- **Report:** 23579 | https://hackerone.com/reports/23579
- **Submitted:** 2014-08-11
- **Reporter:** vinothkumar
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi,

Hope you are good!

Steps to Reproduce:
1) Create a Secret account having email address "a@email.com".
2) Now Logout and ask for password reset link. Don't use the password reset link.
3) Login using the same password back and update your email address to "b@email.com" and verify the same.
4) Now logout and use the password reset link which was mailed to "a@email.com" in step 2.
5) P

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

Hi,

Hope you are good!

Steps to Reproduce:
1) Create a Secret account having email address "a@email.com".
2) Now Logout and ask for password reset link. Don't use the password reset link.
3) Login using the same password back and update your email address to "b@email.com" and verify the same.
4) Now logout and use the password reset link which was mailed to "a@email.com" in step 2.
5) Password will be changed.

All previous password reset links should automatically expire once a user changes his email address.
Please let me know if this can be fixed.

Best Regards,
Vinoth Kumar J

</details>

---
*Analysed by Claude on 2026-05-24*
