# Account Takeover via Open Redirect in Password Reset Flow

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Private Bug Bounty Program (Unnamed)
- **Bounty:** Pending (awaiting decision)
- **Severity:** critical
- **Vuln types:** Open Redirect, Account Takeover, Password Reset Token Leak, Insufficient URL Validation
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered an account takeover vulnerability in the password reset functionality where the resetPasswordUrl parameter was not properly validated, allowing redirect of password reset tokens to attacker-controlled domains. By modifying the resetPasswordUrl parameter to point to their own domain, the attacker received the password reset token, enabling complete account takeover of any user.

## Attack scenario (step by step)
1. Attacker initiates password reset for target email address at /identity/v2/auth/password?api=key&resetPasswordUrl=http://target.com
2. Attacker intercepts the password reset request using a proxy tool
3. Attacker modifies the resetPasswordUrl parameter from http://target.com to http://attacker.com/
4. Attacker forwards the modified request to the server
5. Server validates the request and sends password reset email with token to victim
6. Password reset link in email redirects to attacker's domain with token in URL (http://attacker.com/auth/password/new?token=xyz), allowing attacker to capture and use the token

## Root cause
The resetPasswordUrl parameter in the password reset endpoint was not properly validated or whitelisted. The application failed to verify that the redirect destination was a legitimate domain before including the password reset token in a URL sent via email to users.

## Attacker mindset
Methodical reconnaissance followed by parameter fuzzing. After initial enumeration (CSRF, IDOR) proved unsuccessful, the attacker focused on suspicious parameters in critical workflows. Recognition that password reset tokens sent via email could be leaked through unvalidated URL parameters led to the discovery.

## Defensive takeaways
- Implement strict whitelist validation for all redirect/URL parameters - reject any domain not explicitly approved
- Never include sensitive tokens in URL parameters that are subject to user-controllable redirect logic
- Use POST-based token delivery or temporary session-based token mechanisms instead of email-based tokens
- Implement additional verification steps in password reset (email confirmation, out-of-band verification)
- Log and alert on suspicious password reset requests from unusual locations
- Use security headers like Content-Security-Policy to restrict redirect destinations
- Conduct security review of all authentication and authorization endpoints

## Variant hunting
['Check other password reset/account recovery endpoints for similar open redirect patterns', 'Test resetPasswordUrl variations: resetUrl, redirectUrl, returnUrl, successUrl, callbackUrl, returnTo', 'Look for similar URL parameters in email verification, email change, and 2FA enrollment flows', 'Test other identity endpoints (/identity/v2/*) for parameter injection vulnerabilities', 'Check if the vulnerability affects password reset emails via SMS or other channels', "Verify if authenticated users can reset other users' passwords via IDOR", 'Test if the resetPasswordUrl parameter can be used for phishing via legitimate domain redirect chains']

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1621

## Notes
The writeup quality is informal with grammatical errors but the technical finding is valid and critical. The researcher's methodology was sound - systematic enumeration of endpoints and features before focusing on parameter analysis. The lack of additional validation controls (Host Header, X-Forwarded-Host) initially made the attack surface harder to exploit but the open redirect in the actual parameter succeeded. The bounty status remains uncertain at time of publication, suggesting the vendor may not have immediately recognized severity. This is a textbook open redirect leading to account takeover - a category of vulnerability that frequently appears in bug bounty programs but often goes unpatched due to underestimation of risk.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
