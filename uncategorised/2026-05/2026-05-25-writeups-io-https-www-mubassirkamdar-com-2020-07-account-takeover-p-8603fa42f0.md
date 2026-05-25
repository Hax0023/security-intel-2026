# Account Takeover via Open Redirect in Password Reset URL Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Private Bug Bounty Program
- **Bounty:** Pending (amount unknown)
- **Severity:** Critical
- **Vuln types:** Open Redirect, Account Takeover, Insufficient URL Validation
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered an account takeover vulnerability in a password reset flow where the resetPasswordUrl parameter accepted arbitrary URLs without proper validation. By supplying a malicious URL, the attacker could receive the password reset token sent to a controlled domain, allowing complete account takeover of any user.

## Attack scenario (step by step)
1. Attacker initiates password reset on target.com using victim's email address
2. Proxy intercepts the request to /identity/v2/auth/password endpoint containing resetPasswordUrl parameter
3. Attacker modifies resetPasswordUrl parameter from http://target.com to http://attacker.com
4. Attacker forwards the tampered request to the server
5. Server generates password reset email with token URL pointing to attacker's domain
6. Attacker receives email with password reset link (http://attacker.com/auth/password/new?token=xyz) and uses token to reset victim's password

## Root cause
The application failed to validate and sanitize the resetPasswordUrl parameter in the password reset endpoint, allowing an attacker to control where password reset tokens are sent. The parameter was processed server-side without checking if the URL belonged to the legitimate application domain.

## Attacker mindset
Methodical reconnaissance and enumeration approach; after failing to find CSRF/IDOR vulnerabilities, attacker focused on less obvious trust boundaries like URL parameters in authenticated endpoints. Demonstrated patience in reviewing all functionality before exploitation attempt.

## Defensive takeaways
- Implement strict allowlist validation for all URL parameters, only permitting whitelisted domains
- Never trust user-supplied URLs in security-critical flows like password reset
- Use hardcoded or environment-configured URLs for sensitive operations instead of parameterized URLs
- Validate that redirect/callback URLs match expected application domains before generating tokens
- Implement rate limiting on password reset endpoints to prevent enumeration
- Log all password reset requests with modified URLs for anomaly detection
- Use relative URLs internally rather than accepting full URLs as parameters

## Variant hunting
['Check password reset functionality in other applications for similar unrestricted URL parameters', 'Search for other endpoints accepting resetUrl, callbackUrl, redirectUrl, returnUrl parameters', 'Test account recovery, email verification, and two-factor setup flows for open redirect variants', 'Examine API endpoints that send sensitive tokens via email for URL parameter manipulation', 'Look for similar patterns in OAuth token callback endpoints', 'Test whether protocol switching (http vs https) or subdomain manipulation bypasses validation']

## MITRE ATT&CK
- T1190
- T1598
- T1589
- T1566

## Notes
Writeup contains informal language and typographical errors typical of raw researcher notes. The vulnerability represents a common security oversight in password reset implementations. The researcher's methodology of starting with subdomain enumeration, then checking common vulnerabilities (CSRF/IDOR) before discovering the open redirect in a less obvious parameter demonstrates a structured reconnaissance approach. The bounty status remaining pending at publication time.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
