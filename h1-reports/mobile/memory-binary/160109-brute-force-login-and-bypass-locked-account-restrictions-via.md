# Brute Force Login and Account Lockout Bypass via iOS App OAuth Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 160109 | https://hackerone.com/reports/160109
- **Submitted:** 2016-08-17
- **Reporter:** cablej
- **Program:** Instacart
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Brute Force Attack, Insufficient Rate Limiting, Authentication Bypass, Broken Account Lockout Mechanism
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Instacart iOS mobile app's OAuth token endpoint (`/oauth/token`) lacks rate limiting and account lockout restrictions present on the web login interface, allowing attackers to brute force user credentials. Even accounts already locked on the web platform can be accessed via the mobile endpoint, completely bypassing the intended security controls.

## Attack scenario
1. Attacker identifies that Instacart implements account lockout after ~15 failed login attempts on the web interface
2. Attacker discovers the mobile app uses a separate OAuth endpoint (`POST /oauth/token`) without equivalent protections
3. Attacker configures a proxy (BurpSuite) to intercept and replay mobile login requests
4. Attacker performs repeated login attempts against target user account via the mobile endpoint without triggering lockout
5. Attacker observes differential response codes (401 for invalid, 200 for valid credentials) to identify correct password
6. Attacker successfully gains unauthorized access to target account despite web-side lockout protections

## Root cause
Security controls were implemented only on the web login handler without corresponding protections on the mobile OAuth endpoint. The mobile and web authentication systems operate independently without shared state validation for failed attempts or account lockout status.

## Attacker mindset
Reconnaissance revealed disparate authentication mechanisms with different security postures. Rather than attacking the well-protected web interface, the attacker pivoted to the weaker mobile endpoint, then identified password enumeration was feasible through response code differentiation. This demonstrates intelligent security boundary testing.

## Defensive takeaways
- Implement rate limiting and account lockout mechanisms at the authentication service layer, not just at individual endpoint handlers
- Share account lockout state across all authentication endpoints (web, mobile, API) with centralized enforcement
- Use consistent HTTP response codes across all authentication pathways to prevent information leakage (avoid 401 vs 200 differentiation)
- Implement exponential backoff on failed attempts across all endpoints for a given username/IP combination
- Add CAPTCHA challenges after threshold of failed attempts, even on mobile endpoints
- Monitor for brute force patterns across disparate authentication endpoints using shared credential databases
- Conduct security testing across all authentication pathways simultaneously rather than in isolation

## Variant hunting
Test alternative API endpoints (OAuth endpoints besides `/token`)
Check if password reset flows on mobile also lack rate limiting
Verify if 2FA bypass exists when account is locked on web but accessible via mobile
Test if account enumeration is possible via timing differences in mobile endpoint responses
Investigate if other mobile apps (Android, third-party clients) use different unprotected endpoints
Check if API token endpoints for integrations lack equivalent protections
Test if username enumeration is possible through differential response handling

## MITRE ATT&CK
- T1110.001 - Brute Force: Password Guessing
- T1110.004 - Brute Force: Credential Stuffing
- T1556 - Modify Authentication Process
- T1021.005 - Remote Services: Cloud APIs

## Notes
This report demonstrates a critical class of vulnerability where authentication security controls are compartmentalized rather than unified. The use of response code differentiation (401 vs 200) made password enumeration straightforward. The reporter's POC was methodical and clear, successfully demonstrating the vulnerability with concrete examples. The fix suggested was appropriate and implementable.

## Full report
<details><summary>Expand</summary>

When logging in to an account on the website, a user's account gets locked out after ~15 tries to prevent an attacker from brute forcing access to the account.

These same restrictions do not apply to the mobile sign-in endpoint (a POST request to `https://www.instacart.com/oauth/token`), which allows an attacker to brute force login of any user's account (I have attempted logging into my account ~50 times, with no restrictions).

In addition, if an account has already been locked from too many sign-ins on the website, an attacker can still log in using the app's endpoint.

POC:

1. Configure a mobile proxy, such as BurpSuite.
2. Make a login request in the Instacart app.
3. Repeat this request to brute force any account's password.

As an example, I found a list of the most common 100 passwords and added my own password somewhere in the list. All invalid passwords returned a 401 error, while the correct password returned a 200 error.

Suggested fix:

Apply the same rate limiting and locking-out to mobile login as web login.

</details>

---
*Analysed by Claude on 2026-05-24*
