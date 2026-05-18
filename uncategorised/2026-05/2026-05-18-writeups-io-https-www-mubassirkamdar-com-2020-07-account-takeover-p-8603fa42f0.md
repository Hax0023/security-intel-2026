# Account Takeover via Unsafe Password Reset URL Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Private Bug Bounty Program (Undisclosed)
- **Bounty:** Pending/Unknown
- **Severity:** Critical
- **Vuln types:** Open Redirect, Account Takeover, Unsafe URL Parameter Handling
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered an account takeover vulnerability in a password reset endpoint where the resetPasswordUrl parameter was not properly validated, allowing an attacker to redirect password reset tokens to an attacker-controlled domain. By modifying the resetPasswordUrl parameter from the legitimate domain to an attacker's domain, the reset token was sent to the attacker's server, enabling full account takeover.

## Attack scenario (step by step)
1. Attacker initiates password reset on target.com by providing their email address
2. Attacker intercepts the password reset API request using a proxy tool
3. Attacker modifies the resetPasswordUrl parameter from http://target.com to http://attacker.com
4. Attacker forwards the modified request to the server
5. Server sends password reset email with token redirecting to attacker's domain instead of legitimate domain
6. Attacker captures the password reset token from their server logs and uses it to reset the victim's password, gaining account access

## Root cause
The resetPasswordUrl parameter in the password reset endpoint accepted user-supplied input without proper validation or allowlist verification, allowing arbitrary URL injection. The application failed to validate that the redirect domain matched the legitimate application domain before sending sensitive reset tokens.

## Attacker mindset
Systematic reconnaissance and methodical vulnerability hunting. The attacker first attempted common vulnerabilities (subdomain takeover, CSRF, IDOR) before discovering the less obvious parameter manipulation weakness. Demonstrated persistence in analyzing API endpoints and request parameters for hidden vulnerabilities.

## Defensive takeaways
- Never accept user-supplied URLs in password reset or sensitive functionality endpoints
- Implement strict allowlist validation for any redirect or URL parameters - only permit known safe domains
- Use relative URLs or hardcoded domain references for password reset token generation instead of user-supplied parameters
- Validate the Host header and request origin to prevent URL parameter injection attacks
- Implement server-side token storage with session binding rather than relying on URL parameters for sensitive operations
- Apply rate limiting and monitoring on password reset endpoints to detect abuse patterns
- Test all parameters in authentication and account recovery flows with malicious input

## Variant hunting
['Check for similar resetUrl, callbackUrl, redirectUrl, or returnUrl parameters in other endpoints', 'Test for open redirect in email verification, 2FA, and account recovery flows', 'Attempt parameter pollution combining legitimate and malicious URLs', 'Test alternate parameter names and encodings (URL encoding, double encoding, case variations)', 'Check for Host Header Injection vulnerabilities in token generation logic', 'Test if tokens generated for one URL can be used with another domain', 'Look for similar patterns in API endpoints across different subdomains']

## MITRE ATT&CK
- T1190
- T1598
- T1110
- T1556

## Notes
The writeup lacks specific timestamps, bounty amount, and final resolution. The vulnerability represents a critical authentication bypass enabling complete account takeover of any user. The researcher's methodology showed good OSINT and enumeration practices before discovering this parameter manipulation vulnerability. The response timeframe from the vendor is unclear from the post.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
