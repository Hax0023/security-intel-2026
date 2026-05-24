# No Rate-Limit in Two-Factor Authentication Leads to Bypass via Brute Force

## Metadata
- **Source:** HackerOne
- **Report:** 128777 | https://hackerone.com/reports/128777
- **Submitted:** 2016-04-06
- **Reporter:** bugs3ra
- **Program:** Algolia
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Authentication, Insufficient Rate Limiting, Brute Force Attack, Missing Controls
- **CVEs:** None
- **Category:** memory-binary

## Summary
The 2FA verification endpoint at /users/testqr lacks rate limiting, allowing attackers to brute force the 6-digit TOTP/SMS code sent to the user's mobile device. With no throttling mechanism, an attacker can attempt all 1,000,000 possible combinations within a reasonable timeframe to bypass two-factor authentication.

## Attack scenario
1. Attacker obtains or guesses a user's primary credentials (username/password)
2. User has 2FA enabled; system prompts for TOTP/SMS code verification
3. Instead of waiting for legitimate code entry, attacker sends rapid POST requests to /users/testqr with sequential gauth_token values (0000-9999 or 000000-999999)
4. No rate limiting or account lockout occurs; server processes each request
5. Attacker statistically finds correct code within minutes (average 500k attempts)
6. Authentication bypass achieved; attacker gains account access despite 2FA being enabled

## Root cause
The 2FA verification endpoint lacks implemented rate limiting controls (e.g., throttling per IP/session, exponential backoff, account lockout after N failed attempts, CAPTCHA challenges). No protective mechanisms exist to slow or block rapid-fire verification attempts.

## Attacker mindset
An attacker who has compromised first-factor credentials sees 2FA as a speed bump rather than a barrier. Recognizing the endpoint has no rate limiting, they view brute forcing the 4-6 digit code as a trivial computational problem solvable in seconds to minutes, making 2FA ineffective.

## Defensive takeaways
- Implement strict rate limiting on 2FA verification endpoints (e.g., 5 failed attempts per minute, per IP/session, with exponential backoff)
- Enforce account lockout or temporary suspension after N consecutive failed 2FA attempts
- Add CAPTCHA or additional friction after 2-3 failed verification attempts
- Log and alert on multiple failed 2FA attempts from the same session/IP
- Use time-window validation: invalidate codes after 30-60 seconds and require user re-request
- Implement progressive delays: first failure 1s, second 2s, third 5s, etc.
- Consider hardware-based or app-based TOTP over SMS; SMS codes are time-sensitive but brute-forceable without rate limits

## Variant hunting
Check password reset endpoints for similar missing rate limits (e.g., /users/reset_password accepting arbitrary reset codes)
Review OTP/SMS code endpoints across all authentication flows (signup, login, email verification)
Test account recovery, email verification, and account unlock endpoints for brute force vulnerabilities
Examine backup code verification endpoints (if 2FA supports backup codes)
Test API endpoints that accept authentication codes (not just web forms)
Check if rate limiting is implemented inconsistently (web UI vs API vs mobile endpoints)
Look for similar patterns in session validation, CSRF token handling, or state verification

## MITRE ATT&CK
- T1110.001 - Brute Force: Password Guessing (credential stuffing + brute force codes)
- T1528 - Steal Application Access Token (bypass 2FA to access account)
- T1621 - Multi-Factor Authentication Interception (defeating 2FA implementation)

## Notes
This is a classic authentication bypass; 2FA is rendered useless without rate limiting on code verification. The vulnerability is trivial to exploit and high-impact. The HTTP request shows a POST to /users/testqr with gauth_token parameter—likely a TOTP code. No evidence of rate-limit headers (X-RateLimit-*) in response. Severity warrants immediate remediation. Algolia's response/bounty status not documented in excerpt provided.

## Full report
<details><summary>Expand</summary>

Hi,

There is no rate limit set for Two factor authentication, which demand for code sent to mobile. This code can be bruteforced easily to bypass this.

```
POST /users/testqr HTTP/1.1
Host: www.algolia.com
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://www.algolia.com/users/displayqr
Cookie: __cfduid=dbe6010b3183f275b85d61f6dbce0417a1459962341; _ga=GA1.2.1293083525.1459962367; PRUM_EPISODES=s=1459971091672&r=https%3A//www.algolia.com/users/displayqr; _session_id=c8f877144126b9e3142d158ce5fbadfb; kvcd=1459971056919; km_ai=20868; km_uq=; km_lv=x; visitor_id139121=7630498; __cid=2af41b1f-9f59-4c7e-a3ef-e0c43327b92f; km_ni=20868; _hjIncludedInSample=1; _gat=1; _dc_gtm_UA-32446386-9=1; km_vs=1; km_identity=f7975d47418f3d188a1ed45468bc2c7e; _gat_UA-32446386-9=1; km_aliased=true
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 168

utf8=%E2%9C%93&authenticity_token=twHnV25SUnlKr2rqoBCjEcZ5M749eY1aLiX8gL9f7NiR4PJreIlBlBtn3X6F6qi7Z1JBQOKNgFxFVKapX4lCdg%3D%3D&users%5Bgauth_token%5D=6700&commit=Verify
```
F83580


</details>

---
*Analysed by Claude on 2026-05-24*
