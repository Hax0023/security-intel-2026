# Authorization Bypass via OTP Rate Limiting and Horizontal Privilege Escalation in Grab Android App

## Metadata
- **Source:** HackerOne
- **Report:** 205000 | https://hackerone.com/reports/205000
- **Submitted:** 2017-02-09
- **Reporter:** sp1d3rs
- **Program:** Grab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Insufficient Rate Limiting, Weak OTP Implementation, Authorization Bypass, Account Takeover, Brute Force Vulnerability
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Grab Android app's phone login feature lacks proper rate limiting on the OTP resend endpoint (/profiles/activationsms), allowing an attacker to request unlimited code resets every 30 seconds. Combined with only 3 failed attempts per OTP code and a limited 4-digit code space (0000-9999), an attacker can achieve account takeover of any user within 24-72 hours by systematically testing OTP combinations.

## Attack scenario
1. Attacker identifies target user's phone number and initiates phone-based login on Grab Android app
2. Attacker sends initial OTP request, receiving a 4-digit code with 3 verification attempts before expiration
3. Attacker attempts 3 pre-selected codes (e.g., 1056, 1057, 1058) against the activation endpoint
4. Upon failure, attacker exploits lack of rate limiting to immediately resend a new OTP code without waiting
5. Attacker repeats process every 30 seconds, achieving ~6 attempts per minute or 8640 attempts in 24 hours
6. Due to limited OTP space (9999 possibilities), attacker statistically gains valid code within 24-72 hours and completes account takeover

## Root cause
The application implements inconsistent security controls: the OTP activation endpoint enforces a 3-attempt limit with expiration, while the OTP resend endpoint lacks rate limiting, allowing unlimited requests every 30 seconds. The 4-digit OTP space (10,000 total combinations) combined with high request velocity makes brute force mathematically feasible within reasonable timeframes.

## Attacker mindset
An attacker seeking account takeover without credentials would recognize that phone-based authentication is a common recovery mechanism. By analyzing the app's behavior, the attacker identifies the asymmetry between resend rate limiting (absent) and verification attempt limits (present), enabling a time-based brute force attack. The attacker understands probability and timing constraints to optimize exploitation window.

## Defensive takeaways
- Implement consistent rate limiting across all OTP-related endpoints (request, resend, verify) with decreasing wait times or exponential backoff
- Increase OTP code length from 4 to 6-8 digits to expand keyspace beyond 10,000 combinations
- Implement account-level lockout after multiple failed verification attempts across resend cycles (e.g., lock after 10 total attempts in 1 hour)
- Add CAPTCHA or other anti-automation challenges to the resend endpoint
- Implement IP-based rate limiting and device fingerprinting to detect systematic OTP testing
- Use time-based OTP (TOTP) or cryptographic challenges instead of simple numeric codes
- Log and alert on unusual OTP resend patterns indicating brute force attempts
- Implement progressive delays between OTP resets (30s becomes 60s, then 120s after repeated resets)

## Variant hunting
Check for similar rate limiting gaps on password reset SMS endpoints
Audit two-factor authentication flows for inconsistent rate limiting between request and verification steps
Review other authentication mechanisms (email-based OTP, app-based verification) for equivalent vulnerabilities
Examine account recovery features for similar OTP weaknesses with numeric-only codes
Test second factor enrollment endpoints for comparable rate limiting bypasses
Investigate if other Grab services (web, driver app) have similar phone-based login vulnerabilities

## MITRE ATT&CK
- T1110.004 - Brute Force: Credential Stuffing
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1621 - Multi-Factor Authentication Interception
- T1078.001 - Valid Accounts: Default Accounts

## Notes
This report demonstrates a sophisticated understanding of security controls layering. The vulnerability is particularly dangerous because it requires only a phone number (often public information) for complete account takeover. The researcher provided working proof-of-concept code, demonstrating practical exploitability. The reference to similar vulnerability (report #149598) suggests this is a known attack pattern that should be detected during security reviews. The fix is straightforward (implement proper rate limiting) but the impact is critical (complete account compromise).

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
