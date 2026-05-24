# Two-Factor Authentication Bypass via Brute Force on Grab Android App

## Metadata
- **Source:** HackerOne
- **Report:** 202425 | https://hackerone.com/reports/202425
- **Submitted:** 2017-01-31
- **Reporter:** sp1d3rs
- **Program:** Grab
- **Bounty:** Unknown (not specified in report)
- **Severity:** critical
- **Vuln:** Broken Authentication, Insufficient Rate Limiting, Weak Cryptography, Missing Code Expiration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Grab Android app's 2FA verification endpoint lacks rate limiting and code expiration mechanisms, allowing attackers to brute force 4-digit SMS codes (1000-9999 combinations). An attacker with a valid session can systematically enumerate all possible codes to bypass 2FA and achieve account takeover, including changing email and phone numbers.

## Attack scenario
1. Attacker obtains a valid x-mts-ssid session token from a victim's Android app (via network interception or social engineering)
2. Victim initiates profile edit requiring 2FA verification, receiving a 4-digit SMS code
3. Attacker ignores the actual SMS code and uses brute force tool to systematically send all 10,000 possible code combinations (0000-9999) to /api/passenger/v2/profiles/edit endpoint
4. Each incorrect attempt returns HTTP 400 with status code 4000, but no rate limiting prevents continued attempts
5. When correct code is submitted, endpoint returns HTTP 204 No Content, confirming successful authentication bypass
6. Attacker gains full profile control including ability to change email, phone number, and compromise the account

## Root cause
The authentication endpoint enforces neither rate limiting (throttling requests per session/IP) nor code expiration policies. A 4-digit code provides only 10,000 possible combinations, making it trivially vulnerable to brute force attacks. The lack of exponential backoff, account lockout, or temporary credential invalidation allows unlimited verification attempts.

## Attacker mindset
Opportunistic attacker recognizing that ride-sharing platforms contain sensitive personal and payment information. The presence of a weak 4-digit code combined with no defensive mechanisms makes this a low-effort, high-reward target. Attacker automates the exploit via a simple C# brute force tool, focusing on efficiency over stealth.

## Defensive takeaways
- Implement strict rate limiting: max 3-5 attempts per session before temporary lockout (exponential backoff: 5min, 15min, 1hr)
- Enforce code expiration: 2FA codes should expire within 5-10 minutes of generation
- Use stronger OTP mechanisms: 6-8 digit codes or time-based OTP (TOTP) with cryptographic validation
- Implement account lockout: disable profile edits after repeated failed 2FA attempts
- Add server-side request throttling: use sliding windows and IP/session-based rate limiting middleware
- Log and alert: monitor suspicious 2FA verification patterns for security incident response
- Consider CAPTCHA: require CAPTCHA validation after first failed attempt to prevent automated tools
- Use per-request nonces: prevent replay and enforce one-time use of OTP codes

## Variant hunting
Search for similar 2FA bypass vulnerabilities in other Grab endpoints (password reset, email change, payment method modification). Investigate other ride-sharing apps (Uber, Lyft, DiDi) for identical missing rate-limiting patterns on verification endpoints. Test whether other session-dependent operations lack rate limiting. Check if SMS codes are predictable or sequential rather than random.

## MITRE ATT&CK
- T1110 - Brute Force
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1621 - Multi-Factor Authentication Bypass
- T1528 - Steal Application Access Token

## Notes
Report demonstrates clear exploitation with working POC tool. Vulnerability allows complete account takeover on ride-sharing platform with access to payment methods and personal data. Impact amplified by the fact that legitimate 2FA is properly implemented on phone login, suggesting inconsistent security posture across authentication flows. Researcher provided video proof-of-concept demonstrating practical exploitation.

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
