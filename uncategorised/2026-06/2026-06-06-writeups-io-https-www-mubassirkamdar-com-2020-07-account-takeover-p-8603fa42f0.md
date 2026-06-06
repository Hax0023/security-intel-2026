# Account Takeover via Open Redirect in Password Reset Flow

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Private Bug Bounty Program (Undisclosed)
- **Bounty:** Pending (amount unknown)
- **Severity:** Critical
- **Vuln types:** Open Redirect, Account Takeover, Password Reset Token Leakage
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered an account takeover vulnerability in a private program's password reset endpoint. The resetPasswordUrl parameter accepted arbitrary domains without validation, allowing an attacker to redirect password reset tokens to attacker-controlled servers. This enabled complete account compromise as reset tokens were sent directly to the malicious URL.

## Attack scenario (step by step)
1. Attacker initiates password reset for target account via legitimate password reset form
2. Attacker intercepts the password reset request to /identity/v2/auth/password endpoint
3. Attacker modifies resetPasswordUrl parameter from target.com to attacker-controlled domain (attacker.com)
4. Attacker forwards modified request, causing server to generate reset token and send it to attacker's server
5. Password reset email is sent with link pointing to attacker.com containing valid reset token
6. Attacker uses leaked token to set new password and gain full account access

## Root cause
The resetPasswordUrl parameter in the password reset endpoint was not properly validated. The application accepted arbitrary domain values without whitelisting or validation, trusting user-supplied input to construct the password reset link sent to users.

## Attacker mindset
Methodical reconnaissance through subdomain enumeration and functionality mapping, followed by systematic vulnerability testing (CSRF, IDOR), then creative parameter manipulation when initial approaches failed. The attacker recognized that user-controllable URL construction in security-critical functions represents a significant risk.

## Defensive takeaways
- Never allow user-supplied domains in password reset URLs; generate tokens server-side and use hardcoded safe domains only
- Implement strict whitelist validation for any URL-based parameters, especially in authentication flows
- Validate and sanitize the resetPasswordUrl parameter against a whitelist of allowed domains
- Use relative URLs instead of absolute URLs in password reset emails
- Implement rate limiting on password reset endpoints to detect abuse
- Log all password reset requests including source and destination URLs
- Consider using short-lived tokens with additional validation tied to user session/IP

## Variant hunting
['Check other authentication endpoints for similar URL parameter injection (registration, email verification, 2FA setup)', 'Test if resetPasswordUrl supports javascript: or data: schemes for XSS payloads', 'Verify if the token can be replayed across different users or sessions', 'Test if manipulating other parameters like api key or redirect endpoints yields additional bypass techniques', 'Check mobile app implementations for similar open redirect in deep linking', 'Investigate if other subdomains have similar vulnerable endpoints']

## MITRE ATT&CK
- T1190
- T1556
- T1110
- T1078

## Notes
This is a straightforward but critical vulnerability resulting from insufficient input validation in a security-sensitive function. The researcher's methodology was sound—systematic enumeration followed by testing common vulnerability classes before discovering the less obvious open redirect. The post indicates the bounty was still pending at time of writing, suggesting either slow review process or initial rejection requiring additional documentation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
