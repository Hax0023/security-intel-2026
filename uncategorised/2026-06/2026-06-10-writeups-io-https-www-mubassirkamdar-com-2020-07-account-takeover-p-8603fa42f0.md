# Account Takeover via Unvalidated resetPasswordUrl Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Private Bug Bounty Program (Undisclosed)
- **Bounty:** Pending - awaiting payment confirmation
- **Severity:** critical
- **Vuln types:** Open Redirect, Account Takeover, Insufficient URL Validation
- **Category:** uncategorised
- **Writeup:** https://www.mubassirkamdar.com/2020/07/account-takeover-poc.html

## Summary
A critical account takeover vulnerability was discovered in the password reset functionality where the resetPasswordUrl parameter was not properly validated. An attacker could redirect password reset tokens to an attacker-controlled domain, capturing the reset token and gaining full account access to any user account.

## Attack scenario (step by step)
1. Attacker initiates a password reset request for any target user account on target.com
2. The password reset API endpoint includes a resetPasswordUrl parameter that specifies where the reset link should be sent
3. Attacker modifies the resetPasswordUrl parameter from http://target.com to http://attacker.com in the intercepted request
4. The server generates a password reset token and constructs the reset link using the attacker-supplied resetPasswordUrl parameter
5. Password reset email is sent to the victim containing a link pointing to attacker.com with the valid reset token
6. Attacker captures the reset token from their server logs when the victim clicks the link, then uses it to reset the account password and take over the account

## Root cause
The application failed to validate and restrict the resetPasswordUrl parameter to only trusted domains. The parameter was treated as user-controllable input without proper whitelisting or validation, allowing arbitrary URLs to be injected into the password reset flow.

## Attacker mindset
Systematic reconnaissance approach: subdomain enumeration → functionality mapping → common vuln testing (CSRF, IDOR) → parameter analysis → creative payload manipulation. The attacker maintained persistence despite initial failed attempts and examined suspicious parameters for exploitation opportunities.

## Defensive takeaways
- Implement strict whitelist validation for any URL parameters - only permit known trusted domains
- Never allow user-controlled input to modify authentication token delivery mechanisms
- Use relative URLs or server-side URL construction instead of accepting full URLs as parameters
- Implement additional protections on password reset tokens: short expiration times, single-use enforcement, rate limiting
- Apply secure coding reviews specifically targeting authentication and authorization flows
- Test password reset functionality with fuzzing and URL injection payloads during security testing
- Log and monitor suspicious password reset attempts or token generation from unusual sources

## Variant hunting
['Check for similar resetURL, redirectURL, callback, successURL parameters in other endpoints', 'Test other authentication flows (email verification, account recovery, two-factor setup) for similar parameter injection', 'Look for open redirects in confirmation links, notification URLs, and callback handlers', 'Investigate if the vulnerability exists across multiple subdomains or API versions', 'Test with protocol handlers (javascript:, data:, file:) and bypass techniques', 'Check if other user identifiers can be used in the API to trigger password resets for arbitrary accounts']

## MITRE ATT&CK
- T1190
- T1056
- T1111
- T1598
- T1621

## Notes
The writeup demonstrates a practical account takeover that bypassed initial mitigations (Host Header injection and X-Forwarded-Host were attempted but failed). The vulnerability was straightforward once the suspicious parameter was identified. The researcher's persistence through initial failed attempts on common vulnerabilities (CSRF, IDOR) shows importance of parameter-level analysis. Payment status remains unclear as of writeup publication.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
