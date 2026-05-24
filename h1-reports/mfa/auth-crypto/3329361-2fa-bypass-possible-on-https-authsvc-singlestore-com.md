# 2FA Bypass via Brute Force on SingleStore Authentication Service

## Metadata
- **Source:** HackerOne
- **Report:** 3329361 | https://hackerone.com/reports/3329361
- **Submitted:** 2025-09-06
- **Reporter:** axolot23
- **Program:** SingleStore
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Authentication Bypass, Broken Authentication, Insufficient Rate Limiting, Improper Input Validation, Insecure Direct Object References
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The 2FA authentication mechanism on authsvc.singlestore.com can be completely bypassed through brute force attack on the MFA token parameter. After three failed attempts, the server returns a 302 redirect but fails to invalidate the session, allowing attackers to continue attempting MFA codes and gain unauthorized account access with only email and password.

## Attack scenario
1. Attacker obtains victim's email and password through phishing, credential stuffing, or data breach
2. Attacker logs into https://portal.singlestore.com with victim's credentials
3. Attacker intercepts the 2FA code submission request using Burp Suite
4. Attacker sends request to Intruder and configures brute force attack on mfaToken parameter with numeric payload range
5. After third failed attempt, server returns 302 redirect but session remains valid in Burp
6. Attacker continues sending requests with different MFA codes until correct code is found, gaining full account access

## Root cause
The authentication server incorrectly implements 2FA validation by: (1) failing to enforce rate limiting on MFA attempts, (2) not invalidating session after threshold of failed attempts, (3) allowing continued brute force attempts despite returning 302 redirect status, (4) not implementing exponential backoff or account lockout mechanisms

## Attacker mindset
Attacker recognizes that 2FA protection can be circumvented through automated brute force when rate limiting is absent. The HTTP status code change (200→302) is misinterpreted by the application as a termination signal, but the underlying session remains valid. Attacker exploits this logic flaw by continuing requests outside normal browser flow using proxy tools.

## Defensive takeaways
- Implement strict rate limiting (max 3-5 attempts per MFA session with exponential backoff)
- Invalidate MFA session and require re-authentication after threshold of failed attempts
- Enforce server-side session termination - do not rely on HTTP status codes to signal authentication failure to the client
- Add CAPTCHA challenges after first failed MFA attempt
- Log and alert on multiple failed MFA attempts for anomaly detection
- Implement account lockout mechanism (temporary or requiring verification)
- Use time-sensitive OTP tokens with short validity windows (30-60 seconds)
- Enforce HTTPS and prevent request manipulation via proxy interception by using pinned certificates or additional validation tokens
- Implement server-side request signing/HMAC validation to prevent tampering

## Variant hunting
Search for similar authentication bypass patterns: (1) Check other login endpoints for improper session handling after failed authentication, (2) Test if other token-based mechanisms (password reset, email verification) have similar brute force vulnerabilities, (3) Examine if API endpoints have different rate limiting than web portal, (4) Test for timing-based attacks on MFA validation logic

## MITRE ATT&CK
- T1110.001
- T1110.003
- T1190
- T1078.001
- T1556

## Notes
CVSS score 8.6 (Critical) indicates high severity - full account takeover requiring only credential knowledge. The vulnerability is straightforward to exploit and requires no special privileges or user interaction. The researcher's detailed PoC demonstrates trivial exploitation complexity. SingleStore should prioritize immediate patching. This represents a complete failure of 2FA as a security control.

## Full report
<details><summary>Expand</summary>

## Summary:
To exploit this vulnerability and break into the victim's account, the attacker only needs to know the email address and password of the victim's account. The 2FA authentication mechanism can be bypassed completely.

## Steps To Reproduce:
 * Firstly, enter the victim's account e-mail address and password at `https://portal.singlestore.com/` and click login.
 * Then make a fake 2FA code attempt, intercept the request in Burp and do not send the request in Burp, leave Intercept on.
 * Then, send the request you caught to the intruder, tick the code next to the mfaToken parameter. Then, mark the Payload type as Number. For example, if the 2FA code sent to your e-mail address is 156289, enter a value between 155900 and 1556300 so that the brute force does not take too long. Then press the start attack button.
 * Observe the transition from status code 303 to 302 at the end of the attack. Since the 2FA mechanism was developed incorrectly, as a result of the 3rd incorrect attempt, it switches from an HTTP status code of 200 to a status code of 302 and returns you to the beginning of the login process, but you can still try the request via Burp, and when you make a correct 2FA attempt, including subsequent attempts, it switches to a status code of 302 and you are logged into the account in the browser.

CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N/CR:H/IR:H/AR:H

## Impact

This vulnerability makes it possible to completely bypass the 2FA mechanism developed to protect victims from malicious attacks when logging into their account

</details>

---
*Analysed by Claude on 2026-05-24*
