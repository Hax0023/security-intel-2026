# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Bug Bounty Research (Grammarly, Vidio, Bukalapak)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Authentication Bypass, Credential Leakage
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs discovered critical OAuth implementation vulnerabilities across multiple major platforms (Grammarly, Vidio, Bukalapak) that allowed attackers to take over user accounts by bypassing access token verification mechanisms. The vulnerability stems from improper implementation of OAuth authentication flows, enabling account takeover affecting hundreds of millions of users. All affected companies patched the issues, but researchers estimate thousands of other websites remain vulnerable.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth for social login (e.g., Facebook/Gmail authentication)
2. Attacker captures or intercepts the OAuth authorization flow and access token exchange
3. Attacker exploits the improper access token verification by submitting malformed or unverified tokens
4. The vulnerable OAuth implementation accepts the invalid token without proper validation
5. Attacker gains authenticated session access to victim's account on the target service
6. Attacker can now access sensitive user data, modify account settings, or perform unauthorized actions

## Root cause
OAuth implementations failed to properly verify access tokens during the authentication flow. Developers did not implement sufficient validation mechanisms to confirm token legitimacy, expiration, and scope, allowing attackers to bypass authentication by submitting invalid or crafted tokens that the service incorrectly accepted.

## Attacker mindset
Attackers recognize that OAuth's complexity and ease of implementation create security blindspots. They target the integration layer between OAuth providers and service implementations, exploiting the assumption that if a token exists, it must be valid. The widespread adoption of OAuth makes this a high-impact, scalable attack targeting millions of users across multiple platforms.

## Defensive takeaways
- Always validate access tokens server-side before granting authentication - never trust token presence alone
- Implement token signature verification using cryptographic methods to ensure token integrity
- Verify token expiration time and revocation status on every authentication request
- Validate token scope matches the requested permissions and operations
- Use state parameters and CSRF tokens to prevent authorization code interception attacks
- Implement proper logging and monitoring of OAuth authentication failures
- Conduct security code reviews specifically focused on OAuth integration points
- Follow OAuth 2.0 Security Best Current Practice guidelines (RFC 8252, 8628)
- Test OAuth flows with intentionally malformed and expired tokens during QA
- Regularly audit OAuth implementations for drift from security standards

## Variant hunting
Researchers should search for similar token validation bypasses in: custom OAuth implementations, third-party authentication libraries with poor update practices, mobile app OAuth flows, API gateway authentication layers, single sign-on (SSO) providers, and legacy OAuth 1.0 implementations. Focus on applications where token validation happens client-side or where token presence is assumed to equal validity.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1078 - Valid Accounts
- T1110 - Brute Force
- T1621 - Multi-Stage Channels
- T1199 - Trusted Relationship

## Notes
This research is part of a trilogy by Salt Labs examining OAuth vulnerabilities. Previous posts covered Booking.com and Expo framework. The fix required only one line of code, indicating the criticality of proper token validation. Researchers estimate thousands of websites remain vulnerable with billions of users at risk. The third-party nature of OAuth means vulnerabilities can cascade across platforms - a flaw in one implementation potentially affects all services using that provider's tokens.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
