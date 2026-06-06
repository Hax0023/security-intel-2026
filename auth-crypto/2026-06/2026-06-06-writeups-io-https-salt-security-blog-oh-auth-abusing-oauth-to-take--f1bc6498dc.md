# Oh-Auth — Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak (and potentially thousands of other websites)
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Credential Leakage, Authentication Bypass
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs discovered a critical OAuth implementation vulnerability affecting millions of users across multiple major web services including Grammarly, Vidio, and Bukalapak. The vulnerability allows attackers to bypass access token verification mechanisms and take over user accounts through improper OAuth integration. The flaw stems from inadequate validation of OAuth tokens during the authentication flow, enabling complete account takeover attacks.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth for social login (e.g., 'Login with Facebook')
2. Attacker intercepts or crafts a malicious OAuth authorization response with an invalid or forged access token
3. Attacker exploits insufficient server-side token validation that fails to properly verify the token authenticity
4. The vulnerable OAuth implementation accepts the invalid token and grants authentication to the attacker's account
5. Attacker gains unauthorized access to victim's account without possessing valid credentials
6. Attacker can perform account takeover, access sensitive data, modify account settings, or commit fraud

## Root cause
The root cause is improper implementation of OAuth token verification on the service provider side. Developers failed to implement strict validation of access tokens returned from OAuth providers, trusting tokens without verifying their authenticity, expiration, or proper signature validation. This represents a critical gap between the secure OAuth protocol design and its flawed integration into existing web service platforms.

## Attacker mindset
An attacker would exploit this vulnerability through reconnaissance to identify websites using vulnerable OAuth implementations, then craft malicious OAuth flows to bypass authentication checks. The attacker mindset focuses on finding the path of least resistance in token validation—exploiting the assumption that tokens received from the OAuth flow are inherently trustworthy without proper cryptographic verification.

## Defensive takeaways
- Always validate OAuth access tokens on the server side with cryptographic verification (signature validation, not just presence checks)
- Implement proper token expiration checks and refresh token handling
- Verify token issuer and audience claims match expected values
- Use secure token storage mechanisms and avoid trusting tokens at face value
- Implement state parameter validation to prevent CSRF attacks during OAuth flow
- Conduct security code reviews specifically focused on OAuth integration points
- Use well-tested OAuth libraries rather than custom implementations
- Implement comprehensive logging and monitoring of authentication failures
- Follow OAuth 2.0 Security Best Current Practices (BCP) and OWASP guidelines
- Regular penetration testing of OAuth implementations across all integrated services

## Variant hunting
Security researchers should hunt for similar vulnerabilities by: (1) identifying websites using OAuth social login functionality, (2) intercepting OAuth token exchange to observe how tokens are validated server-side, (3) testing with expired, invalid, or forged tokens to see if they're accepted, (4) examining token payload validation logic, (5) checking for proper signature verification on JWT tokens, (6) testing cross-origin OAuth flows for validation gaps, (7) analyzing error handling that might leak validation logic information.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1056
- T1539
- T1110
- T1187
- T1528

## Notes
This is the third in a trilogy of OAuth implementation vulnerability posts by Salt Labs, with previous research on Booking.com and Expo. The vulnerability affects hundreds of millions of users across multiple platforms. All identified companies responded quickly with mitigations. The research suggests thousands of additional websites may be vulnerable to similar attacks, potentially putting billions of users at risk. The fix is reportedly simple (one line of code), highlighting the gap between protocol security and implementation security.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
