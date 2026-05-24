# Authorization Bypass via OTP Brute Force - Lack of Rate Limiting on SMS Resend Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 205000 | https://hackerone.com/reports/205000
- **Submitted:** 2017-02-09
- **Reporter:** sp1d3rs
- **Program:** Grab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Authentication, Insufficient Rate Limiting, Horizontal Privilege Escalation, Account Takeover, Weak Cryptography
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Grab Android app's phone login flow contains a critical vulnerability allowing account takeover of any user. The SMS resend endpoint lacks rate limiting (only 30-second cooldown), while the OTP verification endpoint has just 3 attempts before expiration. An attacker can continuously reset the OTP code and brute-force 4-digit codes at ~6 attempts per minute, compromising any account with only knowledge of the phone number.

## Attack scenario
1. Attacker identifies target victim's phone number registered with Grab
2. Attacker initiates login flow using 'Login with mobile number' option via Android app
3. Attacker repeatedly calls activationsms endpoint every 30 seconds to refresh OTP without rate limiting
4. For each fresh code, attacker attempts 3 predetermined OTP values (e.g., 1056, 1057, 1058)
5. After 3 failed attempts, code expires; attacker immediately requests new code and repeats cycle
6. Within 24-72 hours, brute-forcing 8,640+ combinations against 9,999 possible 4-digit codes yields valid OTP
7. Attacker gains authentication token and full account access including payment methods and ride history

## Root cause
Insufficient rate limiting on SMS resend endpoint combined with weak OTP validation logic. The activationsms endpoint allows unlimited code regeneration with only a 30-second delay, while activate endpoint's 3-attempt limit resets on each new code. No exponential backoff or account lockout mechanism implemented.

## Attacker mindset
Opportunistic threat actor seeking account takeover capability against any Grab user. Attacker recognizes the mathematical weakness: 9,999 possible codes versus unlimited code regeneration cycles. Automated tooling (C# POC provided) enables scalable attacks against multiple targets simultaneously. 24-72 hour attack window is acceptable for high-value accounts with saved payment methods.

## Defensive takeaways
- Implement strict rate limiting on OTP resend endpoints (e.g., max 3 resends per hour per phone number)
- Implement progressive backoff delays: increase wait time after each resend (30s, 60s, 300s, etc.)
- Add account lockout after 10+ failed OTP attempts across all codes
- Implement per-IP rate limiting on activation attempts
- Use stronger OTP codes (6-8 digits minimum, preferably 6 digits = 1M combinations)
- Implement CAPTCHA challenges after repeated failed attempts
- Add velocity checks: flag/block rapid code resend requests from same IP
- Require user confirmation email/app notification before OTP becomes valid
- Log and monitor unusual OTP request patterns for fraud detection
- Implement device fingerprinting to detect automated attacks

## Variant hunting
Check if password reset flow has similar rate limiting bypass via resend endpoints
Test email-based 2FA for identical resend endpoint weaknesses
Audit all account recovery flows for OTP brute-force vulnerabilities
Examine web version of Grab for parallel authentication bypasses
Review iOS app implementation for equivalent vulnerabilities
Check if other Grab services (GrabFood, GrabExpress) share vulnerable code
Test if account enumeration possible via differential SMS sending responses
Verify if rate limiting bypassed through HTTP headers (X-Forwarded-For, etc.)

## MITRE ATT&CK
- T1110.001 - Brute Force: Password/OTP Guessing
- T1621 - Multi-Factor Authentication Bypass
- T1078.001 - Valid Accounts: Default Accounts
- T1199 - Trusted Relationship
- T1040 - Traffic Signaling
- T1598 - Phishing

## Notes
Report demonstrates sophisticated understanding of attack surface. Attacker provides working POC tool and mathematical proof (6 attempts/min × 1,440 min/day = 8,640 daily attempts). Similar vulnerability pattern documented in referenced HackerOne report #149598. The 30-second resend window is security-theater only; true vulnerability is unlimited resend capability combined with 4-digit OTP entropy. Critical severity justified by account takeover with only phone number required. No authentication, social engineering, or user interaction needed.

## Full report
<details><summary>Expand</summary>

**Description:**
After my previous report about 2FA bypass on the Profile Edit endpoint i was interested to find enpoint, which will allow me horizontal privileges escalation.
So, I found the endpoint using android app `https://p.grabtaxi.com/api/passenger/v2/profiles/activationsms` which allow me to bypass OTP code due to lack of rate limiting.
The root cause of the problem it that facts: resend code endpoint do not have rate limiting (it has only 30 seconds timing for resending possibility). But code activation on the `https://p.grabtaxi.com/api/passenger/v2/profiles/activate` has 3 attempts limit, then it will be expired.
Combined this two facts, i found that it is possible to succeed in the account takeover of any user using only phone number.
Method: we have only 3 code attempts, and we can reset the code every 30 seconds without rate limiting.
**This gave us 6 attempts in the minute, 360 attempts in the hour, and 8640 attempts in 24 hour**. Since codes range has only 9999 values (it is 4-digit), we will likely succeed with the correct code in the 24-72 hours.
Attacker just need to choose some 3 custom OTP codes, for example, 1056, 1057, 1058, and start trying to send them every 30 seconds. If all 3 codes will fail - reset it and try again in next 30 seconds. Sooner or later, Grab Server will throw some of this codes, and this code will be accepted, and we will have access to the victim's account. How it looks in the Web Debugger - you can see on the screenshot attached (`test.png`).
Example report, where used similar method: https://hackerone.com/reports/149598

##Impact

The attacker can bypass OTP verification on Grab android app on any mobile number using "Login with mobile number" option. Attacker can succeed in the account takeover of any user without any privileges, using only phone number and country code.

##Steps To Reproduce:

1. Use my POC tool, attached to the report (written on C#, requires .NET 4.0). Sources included.
2. Enter your test phone number  to the field (it must starts with country code without `+` and be the connected to the Grab account on Android app) - or you can use my test number `███` and press Start.
3. Tool will start sending 3 code attempts `1056, 1057, 1058` and refreshing the code in case of failing every 30 seconds. The process may take many hours, but sooner or later you will receive message with success response and session header. 


##Mitigation/Remediation Steps:
I suggest you implement a rate-limiting on this endpoint `https://p.grabtaxi.com/api/passenger/v2/profiles/activationsms`, for example, blocking code resending for some time after 5 or more resends.





</details>

---
*Analysed by Claude on 2026-05-24*
