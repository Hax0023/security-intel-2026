# No Rate Limiting on Email 2FA Code - Brute Force Attack

## Metadata
- **Source:** HackerOne
- **Report:** 979820 | https://hackerone.com/reports/979820
- **Submitted:** 2020-09-11
- **Reporter:** akashhamal0x01
- **Program:** Bitwarden
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insufficient Rate Limiting, Weak Authentication, Brute Force Vulnerability, 2FA Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Bitwarden's email-based 2FA implementation lacks rate limiting on verification attempts, allowing attackers to brute force the 6-digit code within minutes. An attacker with valid credentials can systematically test all possible codes (0-999999) and gain unauthorized account access.

## Attack scenario
1. Attacker obtains user credentials through credential stuffing, phishing, or data breach
2. Attacker initiates login to vault.bitwarden.com with stolen credentials
3. System prompts for 2FA code sent to victim's email address
4. Attacker intercepts the 2FA verification request using Burp Suite
5. Attacker sends the request to intruder and iterates through numeric codes (0-999999)
6. System returns HTTP 200 on valid code match, granting full account access to attacker

## Root cause
Backend 2FA verification endpoint lacks rate limiting mechanisms, allowing unlimited verification attempts without delays, exponential backoff, account lockout, or CAPTCHA challenges.

## Attacker mindset
Low-effort account takeover post-credential compromise. 2FA is perceived as a false security control. Attacker recognizes that rate limiting is often overlooked and exploits it for quick account access without triggering security alerts.

## Defensive takeaways
- Implement strict rate limiting on 2FA verification endpoints (e.g., 5 attempts per 15 minutes per account)
- Add exponential backoff delays between failed attempts
- Lock accounts after N failed 2FA attempts and require email verification to unlock
- Log and alert on multiple failed 2FA attempts as potential compromise indicator
- Use time-based one-time passwords (TOTP) or WebAuthn as stronger 2FA alternatives to email codes
- Implement CAPTCHA after 2-3 failed attempts
- Set code expiration to 5-10 minutes maximum
- Add IP-based and device-based rate limiting in addition to account-based limits

## Variant hunting
Test 2FA endpoints for any HTTP method bypass (GET, HEAD, OPTIONS, TRACE)
Check if rate limits differ between valid vs invalid user accounts
Investigate whether rate limits reset on password reset or account recovery flows
Test concurrent request handling for parallel brute force attempts
Examine if SMS, TOTP, or push notification 2FA have similar rate limiting issues
Check backup code validation for brute force vulnerabilities
Test account enumeration via 2FA endpoint responses
Analyze timing side-channel attacks on code validation

## MITRE ATT&CK
- T1110.001
- T1621
- T1078.001
- T1589.001
- T1555.003

## Notes
This is a critical infrastructure security issue. Email-based 2FA with 6-digit codes provides only ~1 million possible combinations. Without rate limiting, brute force success is guaranteed within hours or minutes depending on request speed. Bitwarden's vault contains highly sensitive data (passwords, payment methods), making this vulnerability particularly severe. The attack requires valid credentials but defeats the purpose of 2FA entirely.

## Full report
<details><summary>Expand</summary>

NO RATE LIMIT ON 2FA CAN LEAD TO ACCOUNT COMPROMISE!

1. Create account on vault.bitwarden.com  if you don't have.
2.Setup 2FA via email 
3.Logout and log in again. This time along with password you have to fill the 2fa code which is sent to the email.
4.Type Any Random number, intercept request with burp  then send to intruder, mark the code position and start bruteforcing

Results:

>>Invalid Code Response = 400 
>>Valid Code Response = 200

## Impact

2FA acts as extra security. Even if the attacker has user credentials 2FA always protects them from accessing the user data and compromise their whole account.
If the 2FA can be bruteforced it can lead to account compromise assuming that attacker already knows email and password!

</details>

---
*Analysed by Claude on 2026-05-24*
