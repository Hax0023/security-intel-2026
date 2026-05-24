# IDOR leads to PII Leak

## Metadata
- **Source:** HackerOne
- **Report:** 2586584 | https://hackerone.com/reports/2586584
- **Submitted:** 2024-07-04
- **Reporter:** prakhar0x01
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
Hii Triager,

Through research, I discovered a vulnerability in DoD, that **exposes other users' email addresses through IDOR.**

Vulnerable domain: `www.███████`

## Step To Reproduce

1 - Naviagate to https://www.█████████/ , Create an account.
2 - Go to `Update Profile` Section i..e -> *`https://www.█████/JOINOnline/UpdateProfile/<user-id>`*
3 - Change the *Numeric* `user-id` to any other, and 

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

Hii Triager,

Through research, I discovered a vulnerability in DoD, that **exposes other users' email addresses through IDOR.**

Vulnerable domain: `www.███████`

## Step To Reproduce

1 - Naviagate to https://www.█████████/ , Create an account.
2 - Go to `Update Profile` Section i..e -> *`https://www.█████/JOINOnline/UpdateProfile/<user-id>`*
3 - Change the *Numeric* `user-id` to any other, and you'll see other user's email-addresses.

## Impact

1 - Leaks Users Email (PII) and Name
2 - IDOR

## System Host(s)
www.███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
## Step To Reproduce

1 - Naviagate to https://www.████████/ , Create an account.
2 - Go to `Update Profile` Section i..e -> *`https://www.███████/JOINOnline/UpdateProfile/<user-id>`*
3 - Change the *Numeric* `user-id` to any other, and you'll see other user's email-addresses.

## Suggested Mitigation/Remediation Actions
1 - Chain the User session with user-id in the backend



</details>

---
*Analysed by Claude on 2026-05-24*
