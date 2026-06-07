# Account Takeover via Password Reset Token Leakage through resetPasswordUrl Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Private Bug Bounty Program
- **Bounty:** Unknown/Pending (researcher awaiting response)
- **Severity:** critical
- **Vuln types:** Open Redirect, Password Reset Token Leakage, Account Takeover, Unvalidated Redirect
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A critical account takeover vulnerability was discovered in a target application's password reset functionality. The resetPasswordUrl parameter accepted attacker-controlled values, allowing an attacker to receive password reset tokens intended for victims by redirecting the reset email to their own domain.

## Attack scenario (step by step)
1. Attacker identifies the password reset endpoint: /identity/v2/auth/password with resetPasswordUrl parameter
2. Attacker crafts a malicious password reset request replacing resetPasswordUrl with attacker-controlled domain (e.g., attacker.com)
3. Attacker forwards the intercepted request or sends it directly to the application
4. Victim receives password reset email with token URL pointing to attacker's domain instead of legitimate site
5. Token is leaked to attacker's server in the URL when victim visits the malicious reset link
6. Attacker uses the captured token to set new password and takeover victim's account

## Root cause
The application failed to validate and whitelist the resetPasswordUrl parameter, allowing arbitrary URL injection. The token was embedded in a user-controlled URL without proper origin validation, resulting in sensitive credential tokens being sent to attacker-controlled servers.

## Attacker mindset
Methodical reconnaissance through subdomain enumeration, functionality mapping, and systematic testing of common vulnerabilities (CSRF, IDOR). When standard attacks failed, the attacker focused on the suspicious-looking resetPasswordUrl parameter and recognized it as an unvalidated redirect vector combined with sensitive data leakage.

## Defensive takeaways
- Implement strict URL whitelist validation for all redirect/callback parameters
- Use relative URLs or URL fragments for password reset tokens instead of embedding tokens in redirect URLs
- Never trust user-supplied parameters for redirect destinations - validate against configuration
- Implement additional security measures like token binding to session/IP or short expiration times
- Sanitize and validate all parameters, especially those controlling URL destinations
- Add rate limiting and anomaly detection on password reset endpoints
- Log all password reset attempts with source information for security monitoring

## Variant hunting
['Search for other URL redirect parameters (returnUrl, redirectTo, callback, continue, target, url, next)', 'Test resetPasswordUrl in different encodings (double URL encoding, Unicode, case variations)', 'Check if parameter validation can be bypassed with protocol handlers (javascript:, data:, file://)', 'Examine account recovery, email verification, and MFA enrollment endpoints for similar issues', 'Test parameter pollution attacks combining resetPasswordUrl with other parameters', 'Check if token appears in HTTP logs, analytics, or referrer headers on attacker-controlled domain']

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1621
- T1078

## Notes
Report date July 2020. Researcher states 'still waiting' for bounty response indicating delayed resolution. The vulnerability is straightforward but high-impact - demonstrates importance of parameter validation in authentication flows. Researcher employed systematic reconnaissance before identifying the vulnerability, suggesting patience and thorough mapping of application functionality increases likelihood of finding impactful bugs.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
