# 2FA Bypass - Non-Expiring Confirmation Tokens and Reusable CSRF Tokens

## Metadata
- **Source:** HackerOne
- **Report:** 264090 | https://hackerone.com/reports/264090
- **Submitted:** 2017-08-28
- **Reporter:** muskecan
- **Program:** login.gov
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Broken Authentication, Token Expiration Issue, CSRF Token Reuse, Account Lockout Bypass, Insufficient Token Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Confirmation tokens used for account signup/password reset do not expire, allowing attackers to reuse leaked or intercepted tokens to bypass account lockout and reset passwords indefinitely. Additionally, CSRF tokens are not properly invalidated after use, permitting replay attacks to modify account credentials.

## Attack scenario
1. Attacker intercepts or obtains a valid confirmation token from a legitimate signup/password reset email
2. Attacker uses the token in the password reset URL (sign_up/enter_password?confirmation_token=XXXXXX) at any time, even after the account has been locked for 10 minutes
3. Account lockout protection is bypassed and attacker successfully resets the password
4. Alternatively, attacker captures a valid authenticity_token from a legitimate password change request
5. Attacker replays the same authenticity_token in subsequent POST requests to /manage/password with new credentials
6. Password is changed successfully despite token already being used, giving attacker persistent account access

## Root cause
The application fails to implement proper token lifecycle management: confirmation tokens lack expiration timestamps or one-time use validation, and CSRF tokens are not invalidated after first use, creating both authentication and CSRF vulnerabilities

## Attacker mindset
An attacker seeks to gain persistent unauthorized access to user accounts by circumventing security controls designed to prevent brute force and account takeover attacks. Token reuse indicates looking for authentication shortcuts and testing whether rate limiting can be bypassed through alternative mechanisms.

## Defensive takeaways
- Implement strict token expiration times (e.g., 15-30 minutes) for confirmation and password reset tokens
- Enforce one-time use tokens by marking tokens as consumed immediately after validation
- Implement token binding to specific sessions or IP addresses to prevent reuse
- Invalidate all previous confirmation tokens when a new one is issued
- Ensure CSRF tokens are invalidated after first use and regenerated for each request/form
- Store token creation timestamps and validate them server-side on every use
- Log all token usage attempts for security monitoring and incident detection
- Test token expiration and reuse scenarios in security testing
- Implement account lockout mechanisms that cannot be bypassed by alternative authentication methods
- Consider implementing step-up authentication or additional verification for sensitive operations

## Variant hunting
Check if password reset tokens in email flows have similar expiration issues
Test whether other authentication tokens (session tokens, API tokens) are properly invalidated after use
Verify if account recovery/unlock tokens have expiration mechanisms
Examine whether email change confirmation tokens suffer from the same vulnerability
Test if two-factor authentication bypass tokens are properly managed
Check if other CSRF tokens throughout the application are properly invalidated
Investigate whether old authenticity_tokens from cached/archived pages can be reused

## MITRE ATT&CK
- T1110 - Brute Force (Account Lockout Bypass)
- T1556 - Modify Authentication Process
- T1621 - Multi-Factor Authentication Bypass
- T1078 - Valid Accounts (Credential Access)

## Notes
This report demonstrates two distinct but related authentication flaws on a government identity platform (login.gov). The staging environment designation suggests this was caught before production deployment. The finding is particularly critical given login.gov's role as a trusted identity provider for U.S. government services. The reporter provided clear proof-of-concept with actual HTTP requests, making reproduction straightforward.

## Full report
<details><summary>Expand</summary>

Hi there,

Because of the limitation of the site, accounts may be locked down for 10 minutes. I found 2 ways to bypass this lock period.

First one with the confirmation mail that we get when we sign on. 

If we get the token this way below, we can change account password and bypass the lock period at once.

https://idp.staging.login.gov/sign_up/enter_password?confirmation_token=XXXXXX

*XXXXXX= Confirmation token of your account.

Second one is with a POST request below.

POST /manage/password HTTP/1.1
Host: staging.login.gov
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3
Content-Type: application/x-www-form-urlencoded
Content-Length: 219
Referer: https://staging.login.gov/manage/password
Cookie: AWSALB=KkPbvp72NJDrfqzjC97hdllLC4+QMrw8qZXTGzNevDGz3y9nFRrtIyjghxsefOUKkaG2BJX5yhTOY71u+rgMVk5IDaL8G/90affS6zBZBbAOEqqGSp7fYSALOOEL; ahoy_visitor=345467de-0fb9-4154-af8f-329ba5d72408; ahoy_visit=62bcef39-2994-4866-92c8-d21895411c10; ahoy_track=true; _upaya_session=1b94772c05e0dbad70348c3db1f3ccf8; _ga=GA1.2.1438978135.1503936076; _gid=GA1.2.1732157595.1503936076; _ga=GA1.3.1438978135.1503936076; _gid=GA1.3.1732157595.1503936076
Connection: close
Upgrade-Insecure-Requests: 1

utf8=%E2%9C%93&_method=patch&authenticity_token=bGs%2FBZHewYdpRsyPIe108KMc2sR1mK9SL1bbi0X%2F9IYZDJ%2Bh3SpUN79l84qk%2FXZS1%2Fx6Nd9VBVR%2BNCR2a95NZQ%3D%3D&update_user_password_form%5Bpassword%5D=test_?123%2B&commit=Update

If we get an used authenticity_token, we can still change the password and bypass the lock period at once.

King Regards.


</details>

---
*Analysed by Claude on 2026-05-24*
