# Account Takeover via Password Reset URL Parameter Manipulation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Private bug bounty program (undisclosed)
- **Bounty:** Pending (status unknown at time of writeup)
- **Severity:** critical
- **Vuln types:** Open Redirect, Account Takeover, Unvalidated Redirect, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
The researcher discovered a critical account takeover vulnerability in the password reset functionality where the resetPasswordUrl parameter was not properly validated, allowing manipulation to redirect password reset tokens to attacker-controlled domains. By intercepting the password reset request and modifying the resetPasswordUrl parameter from the legitimate target.com to a malicious domain, the attacker could receive the password reset token and gain unauthorized access to any user account.

## Attack scenario (step by step)
1. Attacker initiates password reset on target.com and intercepts the request using a proxy tool
2. Attacker identifies the suspicious resetPasswordUrl parameter in the request: resetPasswordUrl=http://target.com
3. Attacker modifies the parameter to point to attacker-controlled domain: resetPasswordUrl=http://www.mubassirkamdar.com/
4. Attacker forwards the modified request to the vulnerable endpoint
5. Target application sends password reset email with token redirecting to attacker's domain instead of legitimate domain
6. Attacker receives the password reset token and uses it to reset the victim's password and gain account access

## Root cause
Insufficient input validation and lack of whitelist/allowlist enforcement on the resetPasswordUrl parameter. The application failed to properly validate that redirect URLs only point to legitimate application domains, enabling an open redirect vulnerability in the critical password reset functionality.

## Attacker mindset
Systematic enumeration and documentation of all application functions to understand attack surface, followed by methodical testing of common vulnerability patterns (CSRF, IDOR, Host Header Injection) until finding the exploitable parameter. The attacker recognized the suspicious parameter name and tested direct parameter manipulation, demonstrating understandi of how password reset tokens are typically handled.

## Defensive takeaways
- Never allow user-controlled redirect parameters in sensitive functions like password reset
- Implement strict whitelist/allowlist validation for any redirect URLs - only allow known, legitimate internal URLs
- Use relative URLs instead of absolute URLs in password reset links when possible
- Validate the origin and destination of all redirect parameters server-side
- Implement token binding and expiration to limit the window of exploitation
- Use security headers like X-Frame-Options and Content-Security-Policy to prevent further abuse
- Log and monitor password reset requests for suspicious patterns or redirects
- Apply same security controls to all endpoints involving sensitive operations, not just authentication

## Variant hunting
['Test similar parameters on other sensitive endpoints (email verification, account recovery, two-factor authentication setup)', 'Check for alternative parameter names that might control redirects (callback, return_url, redirect_uri, next, continue)', 'Test URL encoding, double encoding, and other bypass techniques on the resetPasswordUrl parameter', 'Check for protocol variations (javascript:, data:, etc.) that might bypass basic URL validation', 'Test on subdomains and alternate domains to see if validation is domain-specific', 'Look for race conditions between token generation and validation', 'Test if tokens are reusable or single-use, and their expiration windows', 'Check password reset flows for other users (horizontal privilege escalation)']

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1021
- T1078

## Notes
The writeup demonstrates a classic open redirect leading to account takeover vulnerability. The researcher's methodical approach to enumeration and testing is noteworthy, though the initial hypothesis testing (CSRF, IDOR, Host Header Injection) was not fruitful before discovering the direct parameter manipulation vulnerability. The fact that the bounty status was pending at writeup time and the program remains private suggests either disclosure restrictions or possible delayed resolution. This vulnerability type remains common in password reset implementations where parameters controlling redirect behavior are not properly validated.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
