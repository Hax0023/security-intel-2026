# Account Takeover via Password Reset URL Manipulation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Private Bug Bounty Program (Undisclosed)
- **Bounty:** Unknown - Pending
- **Severity:** Critical
- **Vuln types:** Open Redirect, Password Reset Token Exposure, Account Takeover
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A critical account takeover vulnerability was discovered in the password reset functionality where the resetPasswordUrl parameter accepted attacker-controlled values. By modifying this parameter to point to an attacker's domain, password reset tokens were sent to the attacker's server, enabling complete account compromise.

## Attack scenario (step by step)
1. Attacker performs reconnaissance and identifies password reset endpoint at /identity/v2/auth/password with suspicious resetPasswordUrl parameter
2. Attacker initiates password reset for target account and intercepts the request using a proxy tool
3. Attacker modifies resetPasswordUrl parameter from http://target.com to http://attacker.com
4. Attacker forwards the modified request to the application server
5. Application sends password reset email with token pointing to attacker's domain: http://attacker.com/auth/password/new?token=xyzxyzxyzxyz
6. Attacker captures the reset token from their server logs and uses it to reset the victim's password and gain account access

## Root cause
Insufficient validation of the resetPasswordUrl parameter allowing arbitrary URLs to be used in password reset token generation. The application failed to whitelist/validate the domain in the reset URL before generating and sending tokens to that location.

## Attacker mindset
Methodical reconnaissance approach - started with subdomain enumeration, tested common vulnerabilities (CSRF, IDOR, host header injection), then pivoted to analyzing suspicious parameter names in legitimate functionality. Demonstrated persistence in testing variations when initial techniques failed.

## Defensive takeaways
- Implement strict whitelist validation for all URL parameters, especially in security-critical functions like password reset
- Generate password reset tokens server-side and send them only to verified user email addresses
- Never use user-controlled or parameter-based URLs in password reset flows
- Implement URL validation against a strict pattern (e.g., only allow base domain)
- Log all password reset attempts and suspicious parameter modifications
- Consider using out-of-band channels (verified email only) for security tokens instead of URL parameters
- Implement rate limiting on password reset endpoints to slow brute force attacks

## Variant hunting
['Check other API endpoints with URL parameters (resetUrl, returnUrl, redirectUrl, callbackUrl, redirectUri)', 'Test for open redirects in confirmation flows, email verification, and account recovery', 'Examine all endpoints that send tokens via email for similar parameter manipulation', 'Test account recovery flows for the same vulnerability pattern', 'Search for similar vulnerable parameters in mobile API endpoints']

## MITRE ATT&CK
- T1190
- T1621
- T1566
- T1598

## Notes
The vulnerability exploited a common design flaw where password reset URLs are dynamically constructed using user-controllable parameters. The researcher's systematic approach (starting with reconnaissance, testing common vulns, then pivoting to parameter analysis) effectively bypassed initial defensive measures like Host Header validation. No CVE mentioned. The blog post lacks details on disclosure timeline and remediation verification.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
