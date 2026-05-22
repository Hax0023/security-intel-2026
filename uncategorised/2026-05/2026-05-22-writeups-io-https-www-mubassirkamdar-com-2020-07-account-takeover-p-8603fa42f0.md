# Account Takeover via Open Redirect in Password Reset Flow

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Private Bug Bounty Program (Undisclosed)
- **Bounty:** Pending (awaiting decision)
- **Severity:** Critical
- **Vuln types:** Open Redirect, Account Takeover, Broken Authentication
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered an account takeover vulnerability by exploiting an open redirect parameter in the password reset functionality. The resetPasswordUrl parameter was not properly validated, allowing an attacker to redirect users to a malicious domain and capture password reset tokens. This enables complete account compromise for any target user.

## Attack scenario (step by step)
1. Attacker identifies the password reset endpoint at /identity/v2/auth/password with the resetPasswordUrl parameter
2. Attacker crafts a malicious reset password link with resetPasswordUrl pointing to attacker-controlled domain
3. Victim receives seemingly legitimate password reset email with link pointing to attacker's server
4. Victim clicks the link and is redirected to attacker's domain where the reset token is exposed in the URL
5. Attacker captures the reset token from the URL and uses it to reset the victim's password
6. Attacker gains complete access to the victim's account with new credentials

## Root cause
Insufficient validation and sanitization of the resetPasswordUrl parameter. The application fails to properly whitelist or validate redirect URLs, allowing arbitrary external domains. The reset token is also exposed in the URL query string making it susceptible to capture via HTTP referrer headers and browser history.

## Attacker mindset
Systematic enumeration approach - thorough reconnaissance of application functionality before attempting exploitation. Attacker tested common vulnerabilities (CSRF, IDOR, host header injection) before finding the actual vulnerability. Recognized suspicious parameter names and tested simple payload manipulation rather than complex exploits.

## Defensive takeaways
- Implement strict URL validation for redirect parameters - maintain a whitelist of allowed domains
- Never include sensitive tokens (reset tokens, session tokens) in URL query parameters; use POST requests with secure cookies instead
- Validate resetPasswordUrl parameter against a strict regex pattern matching only intended domains
- Implement token expiration and single-use enforcement for password reset tokens
- Add additional verification steps before allowing password changes (email confirmation, security questions)
- Log and monitor suspicious password reset attempts and multiple resets for same account
- Use Content Security Policy headers to prevent redirect exploitation
- Implement rate limiting on password reset endpoints

## Variant hunting
Similar open redirect vulnerabilities likely exist in: account recovery flows, email verification links, OAuth callback URLs, account linking endpoints, and any functionality that accepts URL parameters for redirects. Look for parameters named: redirectUrl, returnUrl, callback, next, url, target, destination, forward, goto

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1621

## Notes
The writeup demonstrates practical bug bounty methodology but lacks technical depth. Bounty outcome unknown at publication time. The vulnerability is relatively straightforward but high-impact due to direct account takeover capability. The researcher's enumeration approach (help center, subdomain analysis, function mapping) represents solid reconnaissance practices before vulnerability testing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
