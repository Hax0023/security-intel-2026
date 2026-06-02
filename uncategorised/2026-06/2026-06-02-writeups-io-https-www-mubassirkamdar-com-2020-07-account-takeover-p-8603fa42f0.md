# Account Takeover via Password Reset URL Manipulation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Private Bug Bounty Program
- **Bounty:** Pending (amount unknown)
- **Severity:** Critical
- **Vuln types:** URL Redirection, Open Redirect, Account Takeover, Password Reset Token Interception
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered a critical account takeover vulnerability by manipulating the resetPasswordUrl parameter in a password reset endpoint. By redirecting the reset token to an attacker-controlled domain, the attacker could intercept the password reset token and take over any user account.

## Attack scenario (step by step)
1. Researcher initiates password reset on target.com and intercepts the request containing the resetPasswordUrl parameter
2. Original request contains resetPasswordUrl=http://target.com which generates a legitimate password reset link
3. Researcher modifies the parameter to resetPasswordUrl=http://www.attacker.com/
4. The application constructs the password reset link but changes the domain back to target.com in the email body, however the token is sent to the attacker's domain
5. Password reset email is sent containing the token pointing to attacker's server
6. Attacker captures the password reset token and uses it to reset the victim's password, gaining account access

## Root cause
The application fails to properly validate and sanitize the resetPasswordUrl parameter, allowing an attacker to control where the password reset token is sent. The parameter is processed server-side without sufficient validation, trusting user-supplied input for constructing the password reset URL.

## Attacker mindset
Methodical reconnaissance-based approach: started with subdomain enumeration, checked for common vulnerabilities (CSRF, IDOR, subdomain takeover), reviewed all application functionality through help center, then systematically tested parameters. Demonstrated patience and persistence after initial failures, leading to discovery of an overlooked open redirect vulnerability in a critical function.

## Defensive takeaways
- Never trust user-supplied URL parameters, especially in password reset flows; implement strict whitelist validation
- Use parameterized token generation without allowing dynamic URL construction from user input
- Implement URL validation to ensure password reset links only redirect to authorized domains
- Conduct security testing on all sensitive flows including account recovery and password reset
- Implement logging and monitoring for password reset requests to detect suspicious activity
- Use server-side redirect validation rather than relying on client-side or email-based validation
- Apply defense-in-depth: validate tokens, implement rate limiting, and correlate IP addresses

## Variant hunting
['Check other user account recovery functions (security questions, 2FA recovery codes, account unlock) for similar parameter manipulation', 'Test email change functionality for similar resetEmailUrl or verificationUrl parameters', 'Examine API endpoints for other redirects or URL parameters in authentication flows', 'Look for similar patterns in password change, email verification, and account confirmation flows', "Test other applications' password reset mechanisms for the same vulnerability class"]

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1199

## Notes
The researcher demonstrated good reconnaissance and enumeration methodology but the actual vulnerability was relatively straightforward parameter manipulation. The writeup lacks technical depth regarding token generation and expiration, and doesn't discuss whether the token had any additional validation beyond URL origin. The bounty status remains unresolved at time of publication. This type of vulnerability is common in legacy applications and those developed without security-first principles.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
