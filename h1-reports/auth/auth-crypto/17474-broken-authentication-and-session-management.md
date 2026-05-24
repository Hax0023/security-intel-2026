# Broken Authentication and Session Management

## Metadata
- **Source:** HackerOne
- **Report:** 17474 | https://hackerone.com/reports/17474
- **Submitted:** 2014-06-24
- **Reporter:** anandpingsafe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi,

Hope you are good!

Steps to repro:
1) Create a Phabricator account having email address "a@x.com".
2) Now Logout and ask for password reset link. Don't use the password reset link sent to your mail address.
3) Login using the same password back and update your email address to "b@x.com" and verify the same. Remove "a@x.com".
4) Now logout and use the password reset link which was mai

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

Steps to repro:
1) Create a Phabricator account having email address "a@x.com".
2) Now Logout and ask for password reset link. Don't use the password reset link sent to your mail address.
3) Login using the same password back and update your email address to "b@x.com" and verify the same. Remove "a@x.com".
4) Now logout and use the password reset link which was mailed to "a@x.com" in step 2.
5) Password will be changed.

All previous password reset links should automatically expire once a user changes his email address.
Please fix this.

Best Regards
Anand Prakash

</details>

---
*Analysed by Claude on 2026-05-24*
