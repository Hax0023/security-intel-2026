# 2-factor authentication can be disabled when logged in without confirming account password

## Metadata
- **Source:** HackerOne
- **Report:** 783258 | https://hackerone.com/reports/783258
- **Submitted:** 2020-01-25
- **Reporter:** zerboa
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Business Logic Errors
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Description
===
When users wants to Disable his/her TwoFactor Authentication, they have to know their account password. But using this vulnerability They don't need password to disable it. this will allow hacker who get someone cookie to disabling twofactor auth and also Fullytakeover the account.

How To Reproduce
===
1. Open Your BurpSuite and Turn on the intercept
2. Go To 2Factor Authenticatio

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

Description
===
When users wants to Disable his/her TwoFactor Authentication, they have to know their account password. But using this vulnerability They don't need password to disable it. this will allow hacker who get someone cookie to disabling twofactor auth and also Fullytakeover the account.

How To Reproduce
===
1. Open Your BurpSuite and Turn on the intercept
2. Go To 2Factor Authentication page click the red buttons "Disable two factor ...."
3. Put any wrong password and copy all the header
4. Go to repeater and make a POST request to `https://localizestaging.com/api/user/two-factor/set` also Paste the header here.
5. add a body request like this `method=sms&phone=%2B62-hacker-phone-number` then click GO
6. Bypassed !

## Impact

disable twofactor authentication without needing to know the password

</details>

---
*Analysed by Claude on 2026-05-24*
