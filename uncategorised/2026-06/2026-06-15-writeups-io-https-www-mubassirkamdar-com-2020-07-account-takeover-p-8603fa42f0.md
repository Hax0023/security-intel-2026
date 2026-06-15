# Account Takeover via Password Reset URL Manipulation

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Private Bug Bounty Program
- **Bounty:** Pending (awaiting payment)
- **Severity:** Critical
- **Vuln types:** Open Redirect, Account Takeover, Insufficient URL Validation, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered an account takeover vulnerability in the password reset functionality where the resetPasswordUrl parameter could be manipulated to redirect password reset tokens to an attacker-controlled domain. By modifying this parameter, an attacker could intercept password reset tokens and gain unauthorized access to any user account.

## Attack scenario (step by step)
1. Attacker initiates password reset for target user by submitting their email address to the /identity/v2/auth/password endpoint
2. Attacker intercepts the password reset request using a proxy tool
3. Attacker modifies the resetPasswordUrl parameter from the legitimate domain to an attacker-controlled domain (e.g., http://www.attacker.com/)
4. Attacker forwards the modified request to the vulnerable server
5. System generates a password reset token and includes it in the URL sent to the user's email
6. Due to insufficient validation, the token is sent to the attacker's domain instead of the legitimate site, allowing token interception and account takeover

## Root cause
The application failed to properly validate and sanitize the resetPasswordUrl parameter. The parameter accepted arbitrary URLs without verifying they belonged to the same domain, enabling open redirect and token theft. The backend likely used this user-controlled input directly in generating email links without allowlist validation.

## Attacker mindset
Methodical reconnaissance approach: start with subdomain enumeration, test common vulnerabilities (CSRF, IDOR, subdomain takeover), analyze all application functions before focusing on high-risk features like authentication. When initial vectors fail, examine request parameters for URL-based injection points.

## Defensive takeaways
- Never allow user-controlled parameters to define redirect or callback URLs in security-sensitive operations
- Implement strict allowlist validation for URLs in password reset and account recovery flows
- Use relative URLs or URL fragments instead of full URLs when possible in password reset links
- Validate that redirect/callback URLs belong to the same origin/domain as the application
- Avoid parameterizing base URLs; hardcode legitimate domains in backend
- Log and monitor password reset requests for suspicious URL modifications
- Implement rate limiting on password reset endpoints to prevent abuse
- Send reset tokens with short expiration times (5-15 minutes maximum)

## Variant hunting
['Test other authentication endpoints (email verification, 2FA setup, account creation) for similar URL parameter injection', 'Check for Host header injection vulnerabilities in password reset functionality', 'Attempt bypassing URL validation using encoding tricks (double encoding, unicode normalization, path traversal)', 'Test X-Forwarded-Host and X-Original-URL headers to manipulate backend URL generation', 'Look for open redirect vulnerabilities in logout or session termination flows', 'Check if password reset tokens are reusable or can be validated outside intended context', 'Test for account enumeration via password reset timing or email delivery mechanisms']

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1556
- T1187
- T1040

## Notes
The writeup mentions testing host header injection and X-Forwarded-Host headers unsuccessfully before discovering the resetPasswordUrl parameter bypass. This demonstrates that thorough parameter analysis can yield high-impact findings when standard techniques fail. The researcher's systematic approach through enumeration, subdomain analysis, and function mapping preceded the successful exploitation. Status shows bounty still pending at time of publication, which raises questions about acknowledgment and compensation timelines for high-severity findings.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
