# Oh-Auth — Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak
- **Bounty:** Unknown
- **Severity:** critical
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification, Account Takeover, Credential Leakage, Social Sign-in Abuse
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs researchers discovered critical OAuth implementation vulnerabilities affecting millions of users across Grammarly, Vidio, and Bukalapak that could enable complete account takeover through social sign-in mechanisms. The vulnerabilities stemmed from improper access token verification and validation during OAuth integration, allowing attackers to hijack user sessions and steal credentials. While the affected companies patched the issues, the researchers estimate thousands of other websites remain vulnerable to similar attacks.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth for social login (Facebook, Google, etc.)
2. Attacker analyzes the OAuth implementation to find access token verification weaknesses
3. Attacker intercepts or manipulates the OAuth callback process and access token validation
4. Attacker crafts malicious requests to bypass token verification mechanisms
5. Attacker successfully authenticates as legitimate user without knowing their credentials
6. Attacker gains full account access including sensitive data, payment methods, and personal information

## Root cause
Improper implementation of OAuth access token verification during the OAuth integration process. Developers failed to properly validate access tokens returned from OAuth providers, allowing attackers to bypass authentication checks with malformed or invalid tokens.

## Attacker mindset
OAuth is widely implemented but rarely implemented correctly. By targeting the integration layer rather than OAuth itself, attackers can exploit the gap between protocol specification and real-world implementation. Account takeover via social sign-in is high-impact because it affects millions of users across multiple platforms simultaneously.

## Defensive takeaways
- Always validate access tokens cryptographically and verify they were issued by the legitimate OAuth provider
- Implement server-side token verification rather than relying on client-side validation
- Verify token expiration, scope, and audience claims match expected values
- Use PKCE (Proof Key for Code Exchange) for additional authorization code protection
- Implement strict state parameter validation to prevent CSRF attacks
- Never trust token format or content; always verify signature and origin
- Maintain updated OAuth library dependencies and monitor security advisories
- Conduct security audits specifically focused on OAuth implementation details

## Variant hunting
['Check other websites using OAuth with similar implementation patterns (Slack, Discord, Stripe, GitHub)', 'Look for insufficient token audience validation allowing cross-site token reuse', 'Identify services not validating token expiration properly', 'Search for implementations missing PKCE protection on mobile redirects', 'Test for state parameter bypass or missing CSRF token validation', 'Examine services trusting client-submitted token data without server verification']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1621 - Multi-Factor Authentication Interception
- T1556 - Modify Authentication Process
- T1078 - Valid Accounts
- T1550 - Use Alternate Authentication Material
- T1598 - Phishing for Information

## Notes
This is part three of a trilogy by Salt Labs on OAuth vulnerabilities. Previous posts covered Booking.com and Expo. The researchers estimate the impact affects hundreds of millions of users globally, with thousands of additional vulnerable websites likely exploitable through similar techniques. All three affected companies responded swiftly to patches, demonstrating the importance of coordinated vulnerability disclosure. The fix is reportedly minimal (one line of code), indicating implementation oversight rather than fundamental protocol issues.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
