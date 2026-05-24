# Broken authentication and invalidated email address leads to account takeover

## Metadata
- **Source:** HackerOne
- **Report:** 22203 | https://hackerone.com/reports/22203
- **Submitted:** 2014-08-03
- **Reporter:** born2hack
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cryptographic Issues - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi, team.
I found a bug in twitter.com
Description and POC:
1) Create a twitter account having email address "abcd@x.com".
2) Now Logout and ask for password reset link. Don't use the password reset link.
3) Login using the same password back and update your email address to "efgh@x.com" and verify the same.
4) Now logout and use the password reset link which was mailed to "abcd@x.com" in st

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

Hi, team.
I found a bug in twitter.com
Description and POC:
1) Create a twitter account having email address "abcd@x.com".
2) Now Logout and ask for password reset link. Don't use the password reset link.
3) Login using the same password back and update your email address to "efgh@x.com" and verify the same.
4) Now logout and use the password reset link which was mailed to "abcd@x.com" in step 2.
5) You can see that it is possible to change the password.
Here  the password reset link of "abcd@x.com" which was old email address associated with twitter can be use to change the password of twitter account having  updated email address "efgh@x.com".

Attack scenario:
If victim's previous "abcd@x.com" account was compromised, he decided to updated his twitter email address to "efgh@x.com" but before updating by mistake he asked for password reset link. As a result his twitter account will be compromised by the attacker.

Fix: As soon as new email address is updated all the previous links should also get expired.

If you want further information please let me know.

Thanks and regards.
Mohd Haji

</details>

---
*Analysed by Claude on 2026-05-24*
