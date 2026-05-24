# Brute Force Password on 2FA Disable Endpoint Leads to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 1465277 | https://hackerone.com/reports/1465277
- **Submitted:** 2022-01-31
- **Reporter:** sachinrajput
- **Program:** Omise
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Brute Force Attack, Insufficient Rate Limiting, Inadequate Password Verification, Information Disclosure (Response Length), Account Takeover
- **CVEs:** None
- **Category:** memory-binary

## Summary
The 2FA disable endpoint at https://dashboard.omise.co/signin lacks proper brute force protection, allowing attackers to enumerate valid passwords through response length analysis. An attacker with access to an authenticated session can disable 2FA and gain full account control by systematically guessing the user's password.

## Attack scenario
1. Attacker gains access to a victim's authenticated session (e.g., shared device, session hijacking, or public computer where user forgot to logout)
2. Attacker navigates to Two-Factor Authentication settings and selects 'Disable 2FA'
3. Attacker captures the password confirmation request in an HTTP interception proxy
4. Attacker sends multiple password guesses to the endpoint, observing response content length variations
5. Attacker identifies correct password when response length changes compared to incorrect attempts
6. Attacker successfully disables 2FA and gains full account control without authentication alerts

## Root cause
The 2FA disable endpoint implements password verification without adequate protections: (1) No rate limiting on password attempts, (2) Responses leak information via content-length differences between correct and incorrect passwords, (3) No account lockout after failed attempts, (4) No secondary confirmation or CAPTCHA after multiple failures

## Attacker mindset
An opportunistic attacker exploiting unattended sessions in shared environments (cyber cafes, offices, libraries). The attacker seeks to gain persistent account access by circumventing the strongest security control (2FA). The discovery of response length variance suggests reconnaissance and testing of the endpoint's behavior.

## Defensive takeaways
- Implement exponential backoff and rate limiting (e.g., 3-5 attempts per 15 minutes) on password verification endpoints
- Enforce account lockout after consecutive failed password attempts (e.g., 5 failures = 24-hour lockout)
- Add constant-time comparison functions to prevent timing/length-based side-channel attacks
- Require consistent response sizes regardless of password correctness
- Implement CAPTCHA after 2-3 failed password attempts on sensitive operations
- Send security alerts to registered email/phone when 2FA disable is attempted
- Require multi-factor verification for sensitive operations (e.g., email confirmation + password)
- Implement session timeout for inactivity and require re-authentication for sensitive settings changes
- Add logging and monitoring for multiple failed password attempts on critical endpoints

## Variant hunting
Check password reset endpoints for similar brute force vulnerabilities
Test account recovery flows for inadequate rate limiting
Examine email change, phone change, and API key endpoints for password verification brute force
Look for response length/timing differences on other authenticated password confirmation endpoints
Test if error messages differ between 'user not found' and 'wrong password' states
Verify if legitimate failed attempts trigger notifications to the account owner
Check if session hijacking during sensitive operations is logged and alerted

## MITRE ATT&CK
- T1110 - Brute Force (Password Guessing)
- T1110.001 - Brute Force: Password Guessing
- T1040 - Network Sniffing (capturing requests)
- T1098 - Account Manipulation
- T1556 - Modify Authentication Process (disabling 2FA)
- T1021 - Remote Services (session exploitation)

## Notes
This vulnerability is particularly dangerous because it targets the 2FA disable mechanism itself, undermining the security control rather than bypassing authentication. The response length information disclosure is a critical indicator of the vulnerability's exploitability. The report demonstrates a common real-world scenario: users forgetting to logout on shared devices. Organizations should prioritize fixing this by implementing rate limiting and constant-time responses on all password verification endpoints, especially those controlling critical security features.

## Full report
<details><summary>Expand</summary>

Summary:
This Attack happen when victim login in other device and forget to logout ,Then attacker can enable 2-factor authentication by brute fore the password of victim endpoints.

## Steps To Reproduce:
(1)Login in https://dashboard.omise.co/signin
(2) Click on your username
(3)Navigate to Two-factor authentication --> Disable 2FA
(4)add random password in Please confirm your identity to register a new Two-Factor Authenticator
(5)Capture the request and send it for fuzz


POC
In screenshot you can see change in length of content when request encounter right password.

## Impact

Attacker can disable 2fa and brute force currrent password.

</details>

---
*Analysed by Claude on 2026-05-24*
