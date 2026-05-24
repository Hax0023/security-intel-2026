# Broken Authentication – Session Token bug

## Metadata
- **Source:** HackerOne
- **Report:** 400826 | https://hackerone.com/reports/400826
- **Submitted:** 2018-08-27
- **Reporter:** code_monkey
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** auth
- **CVEs:** None
- **Category:** auth-crypto

## Summary
I found a broken authentitication vuln

POC:

1- Create a https://demo.weblate.org/accounts/profile/ account
2- Confirm your email
3- Now request a password reset for your account.
4- Don’t use the password reset link that was sent to your email.
5- Login to your account, remember don’t use first the reset password link you requested in 3 step
6- Change your password in the Account Settings( url: 

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

I found a broken authentitication vuln

POC:

1- Create a https://demo.weblate.org/accounts/profile/ account
2- Confirm your email
3- Now request a password reset for your account.
4- Don’t use the password reset link that was sent to your email.
5- Login to your account, remember don’t use first the reset password link you requested in 3 step
6- Change your password in the Account Settings( url: https://demo.weblate.org/accounts/profile/
Step 5. After you changed your password inside your account, Check now the reset password link you requested in Step 3 in your email.
Step 6. Change your password using the reset password link you requested.


See this link: https://www.owasp.org/index.php/Broken_Authentication_and_Session_Management

## Impact

tokken should expire 


If the site has a token issue, The result is the reset password token in the Step 3 is still usable and did not expire yet. Not invalidating the session token for the reset password is not a good practice for a company.

</details>

---
*Analysed by Claude on 2026-05-24*
