# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Bug Bounty Research (Grammarly, Vidio, Bukalapak)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** OAuth Implementation Flaw, Insufficient Token Verification, Authentication Bypass, Account Takeover, Credential Leakage
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Researchers identified a critical OAuth implementation vulnerability affecting millions of users across multiple major platforms including Grammarly, Vidio, and Bukalapak. The flaw allows attackers to bypass OAuth access token verification mechanisms, enabling complete account takeover without requiring legitimate user credentials. The vulnerability stems from improper validation of OAuth tokens during the authentication flow, allowing attackers to inject or manipulate tokens.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth social login (e.g., 'Login with Facebook')
2. Attacker initiates OAuth flow and intercepts the authorization code or access token exchange
3. Attacker crafts a malicious request with a forged or manipulated OAuth token
4. Target website fails to properly verify the token's validity, issuer, or cryptographic signature
5. Server accepts the malicious token and establishes an authenticated session for the victim's account
6. Attacker gains complete account access including personal data, credentials, and sensitive information

## Root cause
Inadequate OAuth token validation during implementation. Developers failed to properly verify access token signatures, expiration times, intended audience (aud claim), or token issuer before accepting authentication. The vulnerability exists at the intersection of OAuth protocol design (which is secure) and flawed integration into web services.

## Attacker mindset
Target widely-used platforms with OAuth implementations to maximize impact. Exploit common developer mistakes in token validation rather than attacking the OAuth protocol itself. Chain the vulnerability with social engineering or credential stuffing for mass account compromise across multiple services.

## Defensive takeaways
- Always validate OAuth access token signatures cryptographically using the issuer's public keys
- Verify token expiration timestamps and reject expired tokens immediately
- Validate the 'aud' (audience) claim matches your application's identifier
- Confirm the 'iss' (issuer) claim matches the expected OAuth provider
- Never trust tokens without full cryptographic validation
- Implement token revocation and maintain issuer key rotation mechanisms
- Use well-tested OAuth libraries rather than custom implementations
- Conduct security code reviews specifically for OAuth integration points
- Test OAuth flows with malformed, expired, and forged tokens

## Variant hunting
Hunt for similar OAuth validation bypass vulnerabilities in other platforms using social login. Search for applications that accept OAuth tokens without validating signatures or expiration. Examine token handling in mobile applications and API integrations. Look for improper state parameter validation, missing PKCE implementation in native apps, and insecure token storage mechanisms.

## MITRE ATT&CK
- T1190
- T1598
- T1111
- T1556
- T1621
- T1187

## Notes
Part of a trilogy of OAuth research by Salt Labs. Previous research detailed vulnerabilities in Booking.com and Expo. The fix is described as requiring minimal code changes (one line), suggesting simple validation logic was missing. All affected companies responded quickly with patches. Researchers estimate thousands of additional vulnerable websites exist, potentially affecting billions of users. This represents a systemic implementation issue across the industry rather than a protocol-level flaw.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
