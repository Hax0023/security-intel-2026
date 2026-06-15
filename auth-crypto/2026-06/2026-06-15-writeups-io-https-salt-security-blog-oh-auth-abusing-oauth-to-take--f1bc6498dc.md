# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak (and potentially thousands of other websites)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Credential Leakage, Authentication Bypass
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs discovered a critical OAuth implementation vulnerability affecting millions of users across major platforms including Grammarly, Vidio, and Bukalapak. The flaw allows attackers to completely take over user accounts by exploiting improper access token verification in OAuth implementations. The vulnerability affects a wide range of websites using OAuth for social sign-in authentication.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth for social login (e.g., Grammarly)
2. Attacker analyzes the OAuth implementation and discovers improper access token verification
3. Attacker initiates OAuth flow or intercepts/manipulates the authentication process
4. Attacker bypasses token validation checks due to implementation flaw
5. Attacker obtains or forges valid session credentials without proper authentication
6. Attacker gains complete account access to victim's account on target platform

## Root cause
Improper implementation of OAuth access token verification in the integration layer. While OAuth protocol itself is secure, developers failed to correctly validate and verify access tokens during the authentication flow, allowing tokens to be bypassed, forged, or improperly validated. The fix requires only one line of code, suggesting a missing or incorrect validation check.

## Attacker mindset
Opportunistic and systematic - recognizing that OAuth's popularity and ease of implementation paradoxically creates widespread vulnerabilities. The attacker focuses on the implementation layer rather than the protocol itself, understanding that developers often overlook critical verification steps in token validation. This represents scalable mass account takeover capability across multiple platforms.

## Defensive takeaways
- Always validate and verify OAuth access tokens on the server-side before granting authentication
- Implement explicit token signature verification and expiration checks
- Never trust token claims without proper cryptographic validation
- Conduct thorough security reviews of OAuth integration code, not just protocol compliance
- Implement proper error handling that doesn't leak information about token validity
- Test OAuth flows with modified/invalid tokens to ensure rejection
- Use established OAuth libraries rather than custom implementations
- Validate token audience (aud), issuer (iss), and other critical claims
- Implement token scope verification to ensure tokens only access intended resources
- Regular security audits of authentication and authorization mechanisms

## Variant hunting
Search for similar OAuth token validation bypasses in other platforms using social login, particularly those with custom OAuth implementations. Focus on: 1) Token verification logic that may be missing or incomplete, 2) Improper state parameter validation, 3) Redirect URI validation bypasses, 4) Token audience/issuer mismatches, 5) Missing signature verification on JWTs, 6) Improper scope validation. Test across e-commerce platforms, SaaS applications, and social networks that implement OAuth authentication.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1111 - Multi-Factor Authentication Interception
- T1557 - Adversary-in-the-Middle
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process
- T1621 - Multi-Factor Authentication Bypass
- T1040 - Network Sniffing

## Notes
This is part three of Salt Labs' OAuth vulnerability research trilogy. Previous posts detailed similar issues in Booking.com and Expo. The vulnerability potentially affects billions of internet users globally. All identified companies patched the issues responsibly. The research demonstrates that OAuth protocol security does not guarantee secure implementation, and developers must carefully validate every step of the authentication flow. The 'one-line fix' suggests a missing validation statement, likely a token signature or expiration check.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
