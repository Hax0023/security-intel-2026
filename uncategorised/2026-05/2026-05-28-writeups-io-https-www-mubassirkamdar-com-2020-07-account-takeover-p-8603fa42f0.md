# Account Takeover via Password Reset URL Parameter Manipulation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Private Bug Bounty Program
- **Bounty:** Pending (awaiting resolution)
- **Severity:** Critical
- **Vuln types:** Open Redirect, Account Takeover, Password Reset Token Exposure, URL Parameter Manipulation
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered a critical account takeover vulnerability in a target application's password reset functionality. By manipulating the 'resetPasswordUrl' parameter in the password reset request, an attacker could redirect password reset tokens to an attacker-controlled domain, enabling unauthorized account access.

## Attack scenario (step by step)
1. Attacker identifies the password reset endpoint: /identity/v2/auth/password?api=somesortofkey&resetPasswordUrl=http://target.com
2. Attacker modifies the resetPasswordUrl parameter from http://target.com to http://attacker.com
3. Attacker intercepts the password reset request using a proxy tool and forwards the modified request
4. Victim requests password reset using their email address
5. Password reset token is sent to the attacker's controlled domain instead of the legitimate target.com
6. Attacker accesses the reset link with the token and gains complete account access to the victim's account

## Root cause
The application failed to properly validate and sanitize the 'resetPasswordUrl' parameter, allowing arbitrary domain substitution in password reset emails. The parameter was not restricted to whitelisted domains, enabling open redirect and token theft.

## Attacker mindset
Systematic reconnaissance approach: subdomain enumeration, function mapping, vulnerability pattern testing (CSRF, IDOR), then parameter manipulation. Demonstrates patience and methodical testing when initial attack vectors fail.

## Defensive takeaways
- Implement strict whitelist validation for URL parameters used in security-sensitive operations
- Never trust user-supplied URLs in password reset flows; generate and serve reset links server-side only
- Sanitize and validate all parameters, especially those affecting redirect/email destinations
- Use allowlists for permitted redirect domains rather than blocklists
- Implement security headers like X-Frame-Options and Content-Security-Policy
- Conduct code review specifically for authentication and account recovery flows
- Add logging and monitoring for abnormal password reset patterns
- Use opaque, single-use tokens with short expiration times for password resets

## Variant hunting
['Test all URL parameters in password reset/account recovery endpoints for open redirect behavior', 'Search for similar parameters (resetUrl, redirectUrl, returnUrl, callback) across applications', 'Test Host header injection in password reset email generation', 'Check if tokens can be reused or have excessive expiration times', 'Investigate if password reset tokens are logged or exposed in response headers', "Test for email parameter manipulation to reset other users' passwords", 'Look for similar patterns in 2FA reset, session recovery, and email verification flows']

## MITRE ATT&CK
- T1190
- T1598
- T1187
- T1566

## Notes
The writeup indicates the researcher attempted Host Header injection and X-Forwarded-Host header manipulation before discovering the simple parameter substitution vector. The application's response indicating the URL was 'replaced' suggests server-side validation existed but was bypassable. The 'still waiting' bounty status suggests potential disclosure timeline issues or ongoing remediation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
