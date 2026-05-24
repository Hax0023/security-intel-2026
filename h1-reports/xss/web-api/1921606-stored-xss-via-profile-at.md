# Stored XSS via ' profile ' at ███

## Metadata
- **Source:** HackerOne
- **Report:** 1921606 | https://hackerone.com/reports/1921606
- **Submitted:** 2023-03-28
- **Reporter:** 0xs4m
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
hi team 
i found stored xss on profile 

1. Go to registration page  (██████)
2. Verified your account.
3. Go to login page and login your account.

For the fastly test, use this credentials to login (my test account)

█████████ For Attacker 

email: █████████
pass: Password
████ For Victime

email: █████████
pass: password

After login i change animal name to payload xss .. i open victime account

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

hi team 
i found stored xss on profile 

1. Go to registration page  (██████)
2. Verified your account.
3. Go to login page and login your account.

For the fastly test, use this credentials to login (my test account)

█████████ For Attacker 

email: █████████
pass: Password
████ For Victime

email: █████████
pass: password

After login i change animal name to payload xss .. i open victime account and i put attacker profile url so i succeeded.

██████████

## Impact

Stored Cross Site Scripting which attacker can execute malicious javascript payload.

</details>

---
*Analysed by Claude on 2026-05-24*
