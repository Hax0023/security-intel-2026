# Account Takeover via Open Redirect in Password Reset Flow

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Private Bug Bounty Program (Undisclosed)
- **Bounty:** Unknown - awaiting decision
- **Severity:** critical
- **Vuln types:** Open Redirect, Account Takeover, Insufficient URL Validation
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A critical account takeover vulnerability was discovered in the password reset functionality where an attacker could manipulate the 'resetPasswordUrl' parameter to redirect password reset tokens to an attacker-controlled domain. By intercepting and modifying the password reset request, an attacker could steal password reset tokens and gain unauthorized access to any user account.

## Attack scenario (step by step)
1. Attacker initiates password reset for target user by submitting email address
2. Attacker intercepts the password reset request containing 'resetPasswordUrl=http://target.com' parameter
3. Attacker modifies the resetPasswordUrl parameter to point to attacker's domain: 'resetPasswordUrl=http://attacker.com/'
4. Legitimate password reset email is sent to victim, but token is embedded in link to attacker's domain
5. Attacker receives the password reset token from their server logs when victim clicks the malicious link
6. Attacker uses stolen token to set new password and takeover the victim's account

## Root cause
Insufficient validation and sanitization of the 'resetPasswordUrl' parameter in the password reset endpoint. The application failed to validate that the URL matches the expected domain before embedding it in the password reset email, allowing arbitrary domain injection.

## Attacker mindset
Systematic vulnerability assessment through subdomain enumeration, endpoint discovery via help center documentation, testing common vulnerabilities (CSRF, IDOR), then pivoting to parameter manipulation when initial attacks failed. Demonstrated persistence and logical thinking in identifying and exploiting the weak parameter validation.

## Defensive takeaways
- Implement strict whitelist validation for all URL parameters - only allow URLs matching the application's own domain
- Never trust user-supplied URL parameters in security-sensitive functions like password reset
- Use relative URLs or URL path construction instead of accepting full URLs as parameters
- Implement SSRF (Server-Side Request Forgery) protections on any URL validation logic
- Validate password reset tokens contain user context and verify origin before allowing reuse
- Implement additional verification steps for account recovery (e.g., email confirmation, SMS verification)
- Log and monitor suspicious password reset attempts from multiple IPs or domains

## Variant hunting
['Test other user-supplied URL parameters (redirectUrl, callbackUrl, returnUrl, successUrl) in authentication/authorization flows', 'Check account recovery endpoints for similar open redirect vulnerabilities', 'Test for open redirect in invitation/sharing features that generate external links', 'Look for parameter pollution or encoding bypass techniques (double encoding, Unicode, etc.)', 'Test email verification workflows for similar parameter manipulation', 'Check API endpoints for missing or weak validation on redirect parameters']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1594 - Search Victim-Hosted Content
- T1621 - Multi-Factor Authentication Interception
- T1110 - Brute Force

## Notes
The vulnerability is particularly dangerous because password reset tokens typically have high privileges and short expiration times, making them valuable targets. The writeup lacks some details (program name, final bounty amount, timeline), and the demonstration is more theoretical than a full proof-of-concept. The researcher's methodology of comprehensive enumeration before exploitation is commendable. The original content appears to be a blog post with some formatting issues that made extraction challenging.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
