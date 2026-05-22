# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Bug Bounty Research (Grammarly, Vidio, Bukalapak)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Credential Leakage, Authentication Bypass
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Researchers discovered a critical OAuth implementation vulnerability affecting millions of users across major platforms including Grammarly, Vidio, and Bukalapak. The vulnerability allows attackers to bypass access token verification mechanisms and achieve complete account takeover through improper OAuth integration. The flaw stems from inadequate validation of OAuth tokens during the authentication flow, enabling unauthorized access to user accounts.

## Attack scenario (step by step)
1. Attacker initiates OAuth login flow on vulnerable website (e.g., Grammarly)
2. During callback from OAuth provider, attacker intercepts or manipulates the access token or authorization code
3. Vulnerable application fails to properly verify the token's validity, issuer, or audience
4. Attacker obtains valid session/authentication for victim's account without possessing credentials
5. Attacker gains full account access including personal data, settings, and sensitive information
6. Compromise could lead to identity theft, financial fraud, or access to linked accounts and services

## Root cause
Improper implementation of OAuth token verification in web services. The applications fail to adequately validate access tokens returned from OAuth providers, specifically not verifying token authenticity, expiration, intended audience, or issuer. This represents a one-line code fix according to researchers, suggesting validation logic was either omitted or incorrectly implemented.

## Attacker mindset
An attacker recognizes that while OAuth protocol itself is secure, real-world implementations often have gaps. By targeting the integration layer between OAuth providers and relying services, the attacker exploits common developer mistakes in token validation. The attacker understands that social login mechanisms are ubiquitous, making this attack broadly applicable across thousands of websites for maximum impact.

## Defensive takeaways
- Always validate OAuth access tokens thoroughly: verify signature, expiration time, issuer, and intended audience (aud claim)
- Implement proper token verification libraries and frameworks rather than custom implementations
- Use state parameters and PKCE extensions to prevent authorization code interception attacks
- Validate token claims match expected values for your application
- Implement token revocation and refresh token rotation mechanisms
- Conduct security audits specifically focused on OAuth integration points
- Monitor token validation failures and suspicious authentication patterns
- Keep OAuth libraries and dependencies updated to latest secure versions
- Test OAuth flows with invalid, expired, and malformed tokens during development
- Implement proper logging and alerting for authentication anomalies

## Variant hunting
Search for similar OAuth implementation flaws in: 1) Other e-learning platforms with social login (Coursera, Udemy, edX), 2) Financial services using OAuth (PayPal, Stripe, Square), 3) Healthcare platforms with federated identity, 4) SaaS applications with OAuth integration, 5) E-commerce platforms (Amazon, eBay), 6) Communication platforms, 7) Any service accepting third-party OAuth tokens without proper validation

## MITRE ATT&CK
- T1190
- T1111
- T1556
- T1110
- T1078

## Notes
This is the third in a series of OAuth vulnerability research by Salt Labs, following Booking.com and Expo exploits. The vulnerability affects hundreds of millions of users across multiple platforms. All identified companies remediated issues quickly. Researchers estimate thousands of additional vulnerable websites exist globally. The fix requires only minimal code changes, making non-compliance a significant oversight. OAuth's popularity and ease of implementation paradoxically increase risk due to developer misunderstanding of security requirements.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
