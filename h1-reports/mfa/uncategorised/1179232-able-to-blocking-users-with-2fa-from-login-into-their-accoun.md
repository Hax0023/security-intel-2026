# Account Lockout DoS via 2FA Bypass - SteamID Cookie Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1179232 | https://hackerone.com/reports/1179232
- **Submitted:** 2021-04-29
- **Reporter:** benjamin-mauss
- **Program:** cs.money
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Authentication, Insufficient Rate Limiting, Cookie-based Authentication Bypass, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can block any user account with 2FA enabled from logging in for 5 minutes by manipulating the steamid cookie during 2FA code confirmation. By submitting 4 incorrect 2FA codes with a victim's SteamID, the attacker triggers an account lockout mechanism without needing the victim's credentials or valid authentication.

## Attack scenario
1. Attacker identifies target user's SteamID (often publicly available)
2. Attacker initiates login flow for any account and reaches 2FA confirmation page
3. Attacker intercepts the POST request to /login/confirm endpoint
4. Attacker modifies steamid cookie from their own ID to victim's SteamID
5. Attacker submits 4 requests with incorrect 2FA codes while maintaining victim's SteamID
6. Victim's account triggers lockout mechanism for 300 seconds, preventing legitimate login

## Root cause
The application validates the 2FA code against a user ID derived from the steamid cookie without verifying that the cookie belongs to the authenticated session initiator. Rate limiting and brute-force protection mechanisms are tied to the cookie value rather than the authenticated session, allowing cross-user exploitation.

## Attacker mindset
Griefing/Harassment - Target specific users or competitors to disrupt their platform access. Mass disruption potential if automated against multiple accounts. Low-effort attack with high impact on user experience.

## Defensive takeaways
- Implement server-side session management instead of relying on client-controllable cookies for authentication state
- Bind 2FA code verification requests to the authenticated session that initiated the login process
- Apply rate limiting per session/IP + per user account to prevent cross-user brute forcing
- Implement CSRF tokens or signed requests for sensitive operations like 2FA confirmation
- Monitor for multiple failed 2FA attempts from different sources targeting the same account
- Add progressive backoff delays: exponential increase in lockout duration or response delays per failure
- Log and alert on suspicious patterns: multiple failed 2FA from different IPs or regions in short timeframe

## Variant hunting
Check other authentication endpoints that use similar cookie-based user identification
Test if other sensitive operations (password reset, email confirmation) suffer from same cookie manipulation
Verify if rate limiting works per-IP vs per-account for password reset flows
Test cross-user operations in payment/transaction endpoints using same technique
Check if user enumeration is possible via 2FA response timing differences
Investigate if steamid cookie is validated server-side or if other user identifiers have same weakness

## MITRE ATT&CK
- T1110.004
- T1190
- T1056.004
- T1021.006
- T1499.004

## Notes
SteamID is typically not a secret - it's often public on Steam profiles, making this a severe account-based DoS vector. The 5-minute lockout duration is significant for time-sensitive transactions. The attack requires no special privileges, making it critical for any platform using SteamID authentication. The researcher demonstrated excellent methodology by showing exact HTTP request reproduction steps.

## Full report
<details><summary>Expand</summary>

Hi, team!

## Summary:
By changing the steamID cookie on confirm 2fa code request, I am able to block the login of an account with 2fa for 5 minutes (300 seconds).
So I am able to block users with 2fa from login into their accounts by just knowing the SteamID.

## Steps To Reproduce:

  1. Login into your account with 2fa. 
1. Get the request to confirm the 2fa code.

{F1282394}


```http
POST /login/confirm HTTP/1.1
Host: cs.money
Content-Length: 28
Connection: close
Cookie: steamid=<victim_steam_id>;

{"token":"foo","code":"foo"}
```

2. Change the cookie steamid to the victim one.
3. Repeat the request 4 times (4 wrong codes).

-------

█████

## Impact

I hacker could block everyone with 2fa from login into cs.money.

</details>

---
*Analysed by Claude on 2026-05-24*
