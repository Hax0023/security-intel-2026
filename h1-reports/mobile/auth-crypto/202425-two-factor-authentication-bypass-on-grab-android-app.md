# Two-factor authentication bypass on Grab Android App via brute force attack

## Metadata
- **Source:** HackerOne
- **Report:** 202425 | https://hackerone.com/reports/202425
- **Submitted:** 2017-01-31
- **Reporter:** sp1d3rs
- **Program:** Grab
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Brute Force Attack, Missing Rate Limiting, Missing Code Expiration, Insufficient Input Validation, Authentication Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Grab Android app's profile edit endpoint lacks rate limiting and code expiration mechanisms on the 2FA SMS verification code, allowing attackers to brute force the 4-digit code (1000-9999 combinations) without restrictions. An attacker with a valid session can systematically attempt all possible codes to bypass 2FA and gain unauthorized account access.

## Attack scenario
1. Attacker obtains a valid x-mts-ssid session token from a target user's Grab Android app (via MITM, phishing, or compromised device)
2. Attacker triggers a profile edit action that sends a 4-digit SMS code to the victim's phone
3. Attacker develops or uses a brute force tool to send sequential PUT requests to /api/passenger/v2/profiles/edit with profileActivationCode values from 0000-9999
4. System returns 400 Bad Request for incorrect codes and 204 No Content for the correct code, allowing easy identification
5. Attacker identifies the correct code within minutes (worst case: 10,000 attempts)
6. Attacker successfully bypasses 2FA and gains full account access to modify email, phone number, and other sensitive profile data

## Root cause
The authentication endpoint implements no rate limiting, no attempt throttling, no code expiration after failed attempts, and no account lockout mechanisms. The 4-digit code space (10,000 possibilities) combined with fast API response times makes brute force feasible. Distinguishable HTTP responses (400 vs 204) enable reliable code validation.

## Attacker mindset
An attacker with moderate technical skills can exploit this vulnerability by: (1) obtaining or intercepting a valid session token, (2) automating brute force requests using basic tooling, (3) exploiting the small 4-digit keyspace and lack of defensive controls to achieve account takeover in minutes without triggering alerts.

## Defensive takeaways
- Implement strict rate limiting on 2FA verification endpoints (e.g., max 3-5 attempts per minute per session/IP)
- Enforce code expiration after a fixed time window (5-10 minutes) regardless of attempts
- Lock the account or require re-sending code after N consecutive failed attempts (e.g., 5 attempts)
- Use identical response codes and timing for both correct and incorrect codes to prevent information leakage
- Implement server-side session binding to prevent code reuse across sessions
- Add CAPTCHA or other bot detection after initial failed attempts
- Log and monitor unusual 2FA verification patterns for fraud detection
- Use longer code lengths or alphanumeric codes instead of 4-digit codes

## Variant hunting
Check other endpoints accepting session-based OTP/codes for identical brute force vulnerabilities
Review password reset flows for similar missing rate limiting and code expiration
Audit all SMS/email verification endpoints across Grab's web and mobile APIs
Test profile update endpoints in other Grab services (driver app, business accounts)
Examine payment confirmation or sensitive action verification flows
Check if code length varies across different authentication scenarios (some may have shorter codes)
Verify if the vulnerability extends to password reset or email verification flows

## MITRE ATT&CK
- T1110.001
- T1110.004
- T1621
- T1078.001
- T1190

## Notes
This vulnerability exemplifies poor implementation of 2FA on the backend despite correct implementation on SMS-based phone login flows. The attacker's PoC tool demonstrates the feasibility with readily available C# code. The use of a 4-digit PIN is weak compared to 6-digit standards; combined with the complete absence of rate limiting, this creates a critical account takeover risk. The report includes video proof of concept and suggests practical mitigations. Session token requirement limits immediate exploitability but doesn't eliminate the risk given common session hijacking vectors.

## Full report
<details><summary>Expand</summary>

## Description
I found the endpoint using android app `https://p.grabtaxi.com/api/passenger/v2/profiles/edit` which allow me to bypass 2FA (sms code) due to lack of rate limiting\code expiration after unsuccessful attempts.
The root cause of the problem it that facts: no rate limiting+ no code expiration. Since code has 4 digits, attacker just need to count all possible combinations from 1000 to 9999.
What happens if we do the wrong request to `https://p.grabtaxi.com/api/passenger/v2/profiles/edit` endpoint? Let's take a look:

```
PUT /api/passenger/v2/profiles/edit HTTP/1.1
Content-Type: application/x-www-form-urlencoded
x-mts-ssid: [current session id, its too long so i removed it for report space economy]
x-request-id: 3b609418-0e40-4f86-8ff6-4f23dfac420f
Host: p.grabtaxi.com
Content-Length: 26
Accept-Encoding: gzip
Connection: Keep-Alive

profileActivationCode=3122
```

Response (bad request):

```
HTTP/1.1 400 Bad Request
Content-Encoding: gzip
Content-Type: application/json; charset=utf-8
Date: Tue, 31 Jan 2017 17:45:43 GMT
X-Api-Source: grabapi
X-Request-Id: 01800ddb-fb58-4b53-aecc-97473225f732
Content-Length: 47
Connection: keep-alive

{"status":400,"code":4000}
```
And what when code will be correct?
Response (correct request):

```
HTTP/1.1 204 No Content
Content-Type: application/json; charset=utf-8
Date: Tue, 31 Jan 2017 17:45:43 GMT
X-Api-Source: grabapi
X-Request-Id: 9d0eae1a-9c16-4aa5-8b40-01105a7cb994
Connection: keep-alive
```
I looked to it, and wrote a simple C# tool which sends all possible codes combinations, until it finds a correct code. Source code and POC tool included to the report (it requires at least Windows 7 and NET 4.0 to run).

## Impact
The attacker can bypass 2FA authentication on Grab android app. Attacker can succeed in the account takeover, changing email, phone number of the victim who use Google Auth on the app etc.

## Steps To Reproduce:
1. Login to your Grab Android app using Google with valid phone number (2FA on the phone login option is correctly implemented, and not vulnerable).
2. Edit your profile name and press Save.
3. The 4-digit sms code will be send to your phone. Dont look to it now:)
4.  Use my POC tool (written on C#, requires .NET 4.0). You need a one header from the any app web request (`x-mts-ssid`) for proper testing. You can extract it from the any request from Android app, using some Web Proxy.
If you have troubles with extracting x-mts-ssid session header from the web request - let me know. It can be tricky thing (i used android emulator, connected to Charles Web Proxy, for request monitoring).
Open the program, paste the x-mts-ssid in the text field and press "Start". Wait till process will ends (correct code will be found).
5. Compare code from the tool, and code that you received on the phone earlier - they must be equal. Also i wrote a POC video (https://drive.google.com/file/d/0B8dmpoHKDZsZSFI5WXY2RzRYT00/view?usp=sharing).

## Mitigation/Remediation Steps:
I suggest you implement a rate-limiting on this endpoint, or force 2FA code expiring after, for example, 5 wrong attempts (or both of this for better security).




</details>

---
*Analysed by Claude on 2026-05-24*
