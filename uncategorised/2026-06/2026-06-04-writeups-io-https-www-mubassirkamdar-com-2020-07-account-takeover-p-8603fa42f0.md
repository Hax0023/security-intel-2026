# Account Takeover via Open Redirect in Password Reset Flow

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Private Program (Undisclosed)
- **Bounty:** Pending (researcher awaiting resolution)
- **Severity:** critical
- **Vuln types:** Open Redirect, Account Takeover, Insufficient Input Validation
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A researcher discovered an account takeover vulnerability in a password reset endpoint where the resetPasswordUrl parameter was not properly validated, allowing an attacker to redirect password reset tokens to an arbitrary domain. By modifying the resetPasswordUrl parameter to a malicious domain, the researcher could intercept password reset tokens and gain unauthorized access to any user account.

## Attack scenario (step by step)
1. Attacker initiates password reset for target account via password reset form
2. Attacker intercepts the password reset API request to /identity/v2/auth/password endpoint
3. Attacker modifies resetPasswordUrl parameter from legitimate domain to attacker-controlled domain (e.g., attacker.com)
4. Application constructs password reset email with token embedded in attacker's URL
5. Victim receives reset email with link pointing to attacker's server containing valid reset token
6. Attacker captures token from victim's request to attacker domain and uses it to reset victim's password and takeover account

## Root cause
The application failed to properly validate and sanitize the resetPasswordUrl parameter, allowing arbitrary URL injection. The backend constructed the password reset link by directly incorporating the user-supplied resetPasswordUrl parameter without whitelisting legitimate domains or validating URL schemes. No server-side verification was performed to ensure the token URL matched the intended application domain.

## Attacker mindset
Methodical reconnaissance through subdomain enumeration and functionality mapping, followed by systematic vulnerability testing (CSRF, IDOR, Host Header injection) before discovering the overlooked open redirect in the password reset flow. The attacker recognized that password reset flows are critical paths and attempted common header injection techniques before discovering the direct parameter manipulation vulnerability.

## Defensive takeaways
- Implement strict whitelist validation for any URL parameters - only allow URLs from legitimate, hardcoded application domains
- Never trust user-supplied URL parameters in security-critical flows like password reset
- Use parameterized token generation that doesn't include the reset URL path - construct reset links server-side only
- Validate that password reset tokens are only valid when accessed from the correct application domain
- Implement DNSBL/abuse monitoring on password reset token requests from unexpected origins
- Add logging and alerting for password reset requests with non-standard parameters
- Consider implementing email-based token validation rather than URL-based tokens
- Test all authentication flows (login, password reset, registration) for open redirect vulnerabilities

## Variant hunting
Search for similar open redirect patterns in other password recovery endpoints, account recovery flows, email verification links, two-factor authentication setup URLs, and any endpoint that generates URLs sent via email. Check for variations using URL encoding, protocol-relative URLs (//), data URLs, or JavaScript schemes to bypass basic validation.

## MITRE ATT&CK
- T1190
- T1110
- T1621

## Notes
The vulnerability is particularly severe because it affects the account recovery mechanism, which is typically the last line of defense for account security. The researcher's methodology of comprehensive functionality enumeration followed by targeted testing of critical flows demonstrates effective bug bounty hunting. The lack of server-side validation of the resetPasswordUrl parameter is a common implementation error in password reset functionality. The bounty status remains unclear, suggesting either delayed response or dispute over severity classification.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
