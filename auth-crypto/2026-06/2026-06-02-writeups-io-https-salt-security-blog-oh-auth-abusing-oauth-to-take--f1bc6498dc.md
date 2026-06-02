# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** OAuth Implementation Flaw, Account Takeover, Credential Leakage, Access Token Verification Bypass, Authentication Bypass
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs discovered critical OAuth implementation vulnerabilities affecting millions of users across major platforms including Grammarly, Vidio, and Bukalapak. The vulnerabilities allowed attackers to completely take over user accounts through improper access token verification in OAuth implementations. While the protocol itself is secure, poor integration with web services created exploitable security gaps.

## Attack scenario (step by step)
1. Attacker identifies a website using OAuth for social login functionality
2. Attacker analyzes the OAuth token exchange process and discovers improper access token validation
3. Attacker crafts a malicious authentication request or manipulates the token verification mechanism
4. Attacker bypasses access token verification checks due to implementation flaws
5. Attacker gains unauthorized access to victim's account without valid credentials
6. Attacker achieves full account takeover enabling identity theft, financial fraud, and data access

## Root cause
OAuth implementations failed to properly verify access tokens during the authentication flow. Developers, despite OAuth's apparent simplicity, made critical errors in integrating OAuth into existing platforms by not validating tokens according to specification or creating custom verification logic with security gaps.

## Attacker mindset
An attacker targeting OAuth implementations recognizes that while the OAuth protocol is theoretically secure, real-world integrations often contain implementation shortcuts and validation bypasses. By focusing on the integration layer rather than the protocol itself, attackers can exploit millions of accounts across multiple high-value targets simultaneously.

## Defensive takeaways
- Always properly validate OAuth access tokens according to specification before granting access
- Implement strict token verification including signature validation, expiration checks, and audience verification
- Use well-tested OAuth libraries and frameworks rather than custom implementations
- Conduct security code reviews specifically focusing on OAuth integration points
- Implement comprehensive logging and monitoring for OAuth token exchanges
- Apply principle of least privilege when issuing OAuth tokens
- Keep OAuth implementations up-to-date with latest security recommendations
- Test OAuth implementations for common bypass techniques regularly

## Variant hunting
Hunt for similar OAuth implementation flaws in: other platforms using social login, custom OAuth implementations, outdated OAuth libraries, services with multiple identity providers, applications with token delegation features, and APIs that accept external OAuth tokens.

## MITRE ATT&CK
- T1190
- T1528
- T1556
- T1110
- T1199

## Notes
This is the third post in a trilogy on OAuth vulnerabilities; previous posts covered Booking.com and Expo. The research impacted hundreds of millions of users across multiple platforms. All affected companies responded quickly with fixes. The vulnerability requires only a one-line code fix, indicating oversight rather than complex architectural issues. Researchers estimate thousands of other websites remain vulnerable to similar attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
