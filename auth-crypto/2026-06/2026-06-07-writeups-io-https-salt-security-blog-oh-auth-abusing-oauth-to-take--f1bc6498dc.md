# Oh-Auth — Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak
- **Bounty:** Not specified in provided content
- **Severity:** CRITICAL
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Authentication Bypass, Credential Leakage
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs discovered a critical OAuth implementation vulnerability affecting millions of users across major platforms including Grammarly, Vidio, and Bukalapak. The flaw allows attackers to bypass access token verification and achieve complete account takeover through improper OAuth integration. The vulnerability stems from insecure validation of OAuth authentication flows, enabling credential leakage and unauthorized account access.

## Attack scenario (step by step)
1. Attacker identifies target website using OAuth for social login (e.g., 'Login with Facebook/Gmail')
2. Attacker initiates OAuth flow and intercepts/manipulates the authorization response containing access tokens
3. Attacker crafts malicious requests exploiting improper access token verification in the target application
4. Target application accepts the manipulated token without proper validation or signature verification
5. Attacker gains authentication as legitimate user without possessing actual credentials
6. Attacker gains full account access including sensitive data, financial information, and personal messages

## Root cause
OAuth implementations fail to properly validate access tokens returned from OAuth providers. Developers implement OAuth integration without verifying token signatures, expiration, scope claims, or token binding to the specific user session. The protocol itself is secure, but the integration into existing platforms introduces validation gaps where applications trust tokens without cryptographic verification or additional security checks.

## Attacker mindset
Target high-value platforms using OAuth to maximize credential harvesting and account takeover impact. Exploit the widespread assumption that OAuth handles security automatically, when in reality implementation details matter critically. Focus on authentication flows rather than authorization to achieve maximum privilege escalation with minimal effort.

## Defensive takeaways
- Always cryptographically verify OAuth access token signatures using provider's public keys
- Validate token expiration times and refresh token validity before granting access
- Implement token binding to specific user sessions using state parameters and PKCE
- Verify that token claims (scope, audience, subject) match expected values for the request context
- Use secure token storage and transmission with HTTPS and secure-only cookies
- Implement rate limiting and anomaly detection on authentication endpoints
- Validate redirect URIs against whitelist with exact string matching
- Implement server-side session validation independent of OAuth token validity
- Conduct security code reviews specifically for OAuth implementation logic
- Monitor for token reuse patterns indicating potential compromise

## Variant hunting
Hunt for similar OAuth validation bypasses in: (1) Other social login providers beyond Facebook/Google; (2) Custom OAuth implementations in enterprise applications; (3) Token validation logic in authorization gateways; (4) State parameter handling in multi-step authentication flows; (5) Session fixation vulnerabilities in OAuth to local session binding; (6) Token scope validation mismatches between provider and consumer; (7) Implicit flow implementations lacking state parameters; (8) Applications accepting unsigned or unencrypted JWT tokens

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1598 - Phishing
- T1621 - Multi-Factor Authentication Interception
- T0868 - Brute Force
- T1187 - Forced Authentication

## Notes
This is the third post in a trilogy examining OAuth vulnerabilities; previous posts covered Booking.com and Expo. The researchers estimated impact of 'hundreds of millions of users' across identified vulnerabilities and believe '1000s of websites' remain vulnerable. All identified companies remediated issues quickly, emphasizing that response quality matters in vulnerability disclosure. The fix is described as minimal ('one line of code'), suggesting validation logic was simply missing rather than complex to implement. Research did not exhaustively identify all vulnerable sites to limit potential abuse.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
