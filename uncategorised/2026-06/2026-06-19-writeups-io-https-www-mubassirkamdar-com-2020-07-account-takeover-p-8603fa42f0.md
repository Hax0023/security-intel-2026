# Account Takeover via Open Redirect in Password Reset Flow

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Private Bug Bounty Program (Undisclosed)
- **Bounty:** Pending (status unknown at time of publication)
- **Severity:** Critical
- **Vuln types:** Open Redirect, Account Takeover, Password Reset Token Leakage
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered a critical account takeover vulnerability in a password reset endpoint that accepted user-controlled resetPasswordUrl parameter without proper validation. By modifying the resetPasswordUrl parameter to attacker-controlled domain, password reset tokens were leaked to the attacker's server, enabling account takeover of any user account.

## Attack scenario (step by step)
1. Attacker initiates password reset on target.com using victim's email address
2. Attacker intercepts the password reset request at /identity/v2/auth/password endpoint
3. Attacker modifies resetPasswordUrl parameter from http://target.com to attacker-controlled domain (e.g., http://attacker.com)
4. Target application validates and sends password reset email with token embedded in URL pointing to attacker's domain
5. Victim receives email with legitimate-looking reset link but pointing to attacker's server
6. Attacker captures the reset token when victim clicks the malicious link, then uses it to reset victim's password and takeover account

## Root cause
Insufficient validation of the resetPasswordUrl parameter in the password reset endpoint. The application failed to implement whitelist validation or URL scheme/domain verification, allowing arbitrary redirect URLs to be embedded in password reset tokens sent via email.

## Attacker mindset
Systematic vulnerability enumeration starting with reconnaissance (subdomain enumeration), then methodically testing known vulnerability classes (CSRF, IDOR, Host Header Injection) before discovering the overlooked open redirect parameter in the password reset flow. The attacker recognized that user-supplied URL parameters in security-critical functions require strict validation.

## Defensive takeaways
- Never trust user-supplied URL parameters in security functions like password reset without strict validation
- Implement whitelist validation for redirect URLs - only allow redirects to known, trusted domains
- Use relative URLs or URL path validation instead of accepting arbitrary absolute URLs
- Generate short-lived, single-use password reset tokens independent of redirect URLs
- Include domain/origin validation checks before embedding URLs in emails
- Implement rate limiting and monitoring on password reset endpoints for abuse patterns
- Security test all authentication flows (login, logout, password reset, account recovery) with particular focus on URL parameters

## Variant hunting
['Check other authentication endpoints for similar resetUrl/redirectUrl/callbackUrl parameters', 'Test other recovery/notification flows (email verification, two-factor setup) for open redirects', 'Look for similar patterns in password reset flows across different API versions', 'Check if tokens are reusable or if multiple reset attempts can be chained', 'Test if resetPasswordUrl validation can be bypassed with URL encoding, double encoding, or protocol confusion', 'Examine if subdomain-based whitelisting can be bypassed (e.g., attacker.target.com)']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1550

## Notes
This is a classic open redirect vulnerability in a high-impact context. The researcher's methodology was sound - systematic enumeration led to discovery after testing common vulnerability classes first. The vulnerability is particularly dangerous because password reset tokens are high-value secrets. At time of writeup, bounty status was unknown ('still waiting for it'). The writeup demonstrates importance of testing all user-supplied parameters in security-critical functions, not just obvious injection points.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
