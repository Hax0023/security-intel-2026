# Oh-Auth — Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Bug Bounty (Grammarly, Vidio, Bukalapak)
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln types:** OAuth Implementation Flaw, Insufficient Token Validation, Account Takeover, Authentication Bypass, Credential Leakage
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Researchers discovered a critical OAuth implementation vulnerability affecting millions of users across multiple major platforms including Grammarly, Vidio, and Bukalapak. The flaw allows attackers to bypass OAuth access token verification mechanisms, enabling complete account takeover without valid credentials. The vulnerability stems from improper implementation of OAuth standards rather than protocol design flaws.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth social login (Facebook, Google, etc.)
2. Attacker intercepts or crafts an OAuth flow request with a malicious or forged access token
3. Target application fails to properly validate the access token against the OAuth provider
4. Application accepts the invalid token and creates authenticated session for attacker
5. Attacker gains full account access without possessing victim's credentials
6. Attacker can perform identity theft, financial fraud, or access sensitive personal data

## Root cause
OAuth implementations fail to properly verify access tokens returned from OAuth providers. Applications do not adequately validate token authenticity, expiration, scope, or signature before establishing user sessions. The integration of OAuth into existing application logic introduced security gaps where developers bypassed critical validation steps.

## Attacker mindset
An attacker recognizes that OAuth's complexity and widespread adoption creates implementation blindspots. Rather than attacking the OAuth protocol itself, they target the weakest link—the integration layer where developers make assumptions about token validity. This approach scales across thousands of websites since many developers copy-paste implementations without understanding the security requirements.

## Defensive takeaways
- Always validate OAuth access tokens server-side against the OAuth provider's token introspection endpoint
- Verify token signature using provider's public keys for token verification
- Check token expiration, issued-at time, and scopes before accepting authentication
- Implement state parameter validation in OAuth callback to prevent CSRF attacks
- Use PKCE (Proof Key for Code Exchange) for all OAuth flows, especially mobile and SPA applications
- Never trust client-side token validation; perform all security-critical checks server-side
- Log and monitor OAuth authentication failures for anomalous patterns
- Regularly audit OAuth implementations against OWASP OAuth 2.0 Security Best Practices
- Test OAuth implementations with invalid, expired, and forged tokens

## Variant hunting
Search for other applications using OAuth social login features, particularly those with custom implementations. Test with modified access tokens, expired tokens, tokens from different users, and tokens with altered claims. Check for applications that trust client-side token validation or skip server-side verification steps. Review GitHub for common OAuth implementation patterns and identify repositories with potential gaps.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1110
- T1556
- T1199

## Notes
This is the third in a trilogy of OAuth vulnerability research papers by Salt Labs, following similar findings in Booking.com and Expo. The researchers estimate thousands of websites remain vulnerable to this attack vector, potentially affecting billions of users. All identified companies responded quickly with fixes. The vulnerability highlights the gap between protocol design security and real-world implementation complexity.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
