# Oh-Auth — Abusing OAuth to take over millions of accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Bug Bounty Research (Salt Labs)
- **Bounty:** Not specified in content
- **Severity:** critical
- **Vuln types:** OAuth Implementation Flaw, Insufficient Token Validation, Account Takeover, Authentication Bypass, Credential Leakage
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs identified a critical OAuth implementation vulnerability affecting millions of users across Grammarly, Vidio, and Bukalapak. The flaw allows attackers to bypass OAuth token validation and take over user accounts through improper access token verification. While the affected companies patched the issues, thousands of other websites remain vulnerable to the same attack vector.

## Attack scenario (step by step)
1. Attacker initiates OAuth login flow on vulnerable website (e.g., Grammarly)
2. Attacker intercepts or manipulates the OAuth callback containing access tokens
3. Vulnerable service fails to properly validate the access token against OAuth provider
4. Attacker crafts malicious token or exploits insufficient validation checks
5. Attacker gains unauthorized access to victim's account without valid credentials
6. Full account takeover achieved, enabling identity theft, financial fraud, or data access

## Root cause
Improper implementation of OAuth access token verification in the service's integration layer. The OAuth protocol itself is secure, but developers failed to adequately validate tokens during the authentication callback phase, likely trusting unvalidated token claims or skipping server-side verification against the OAuth provider.

## Attacker mindset
Opportunistic and systematic - identifying that OAuth implementation flaws are common across many websites due to developer knowledge gaps. The attacker recognizes that while OAuth appears simple to implement, the nuances of token validation are frequently overlooked, creating a scalable attack vector affecting millions of users across multiple platforms.

## Defensive takeaways
- Always validate OAuth access tokens server-side against the OAuth provider, never trust client-provided tokens
- Implement strict token validation including signature verification, expiration checks, and scope validation
- Use standardized OAuth libraries rather than custom implementations to reduce implementation gaps
- Validate token binding to specific users and sessions to prevent token reuse attacks
- Implement comprehensive logging and monitoring of OAuth authentication flows
- Conduct security code reviews specifically focused on OAuth integration points
- Test OAuth implementations against known attack vectors and OWASP guidelines
- Maintain updated dependencies for OAuth libraries to receive security patches

## Variant hunting
Hunt for similar OAuth validation bypasses by examining: (1) other services using social login features, (2) token validation logic in authentication callbacks, (3) insufficient scope validation, (4) missing signature verification on JWT tokens, (5) improper user identity binding during token exchange, (6) state parameter validation gaps

## MITRE ATT&CK
- T1190
- T1528
- T1110
- T1078
- T1556
- T1539

## Notes
This is the third post in Salt Labs' OAuth vulnerability trilogy, following similar critical issues in Booking.com and Expo. The research demonstrates that OAuth vulnerabilities are systematic across the industry, with potentially thousands of websites affected. The fix is reportedly 'one line of code away,' suggesting simple validation checks were omitted. The vulnerability impacts hundreds of millions of users globally and represents a fundamental implementation gap rather than a protocol flaw.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
