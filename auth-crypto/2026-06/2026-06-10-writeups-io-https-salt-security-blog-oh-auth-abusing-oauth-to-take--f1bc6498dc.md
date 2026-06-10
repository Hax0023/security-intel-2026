# Oh-Auth — Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Bug Bounty - Multiple Programs (Grammarly, Vidio, Bukalapak)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** OAuth Implementation Flaw, Account Takeover, Authentication Bypass, Credential Leakage, Improper Token Verification
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Researchers discovered critical OAuth implementation vulnerabilities affecting millions of users across Grammarly, Vidio, and Bukalapak that could enable complete account takeover through improper access token verification. The vulnerability stemmed from a single-line-of-code OAuth implementation error that allowed attackers to bypass authentication mechanisms. All affected companies patched the issues, but thousands of other websites likely remain vulnerable to the same attack vector.

## Attack scenario (step by step)
1. Attacker identifies a web service using OAuth social login (e.g., 'Login with Facebook')
2. Attacker initiates OAuth flow and obtains an authorization code from the OAuth provider
3. Attacker crafts a malicious request exploiting improper token verification logic in the target application
4. Target application fails to properly validate the access token or mishandles token verification
5. Attacker bypasses authentication and gains access to victim's account without valid credentials
6. Attacker can now perform account takeover, access personal data, financial information, or impersonate the user

## Root cause
OAuth implementations at affected services failed to properly verify access tokens during the authentication flow. The vulnerability was attributed to a single-line-of-code implementation error in token verification logic, suggesting developers either skipped validation steps or implemented incomplete validation checks.

## Attacker mindset
Opportunistic attacker targeting widespread OAuth implementation patterns to achieve mass account compromise. Focus on finding common implementation mistakes across multiple high-value targets serving millions of users. Goal is rapid exploitation of a systematic flaw rather than targeted attacks.

## Defensive takeaways
- Always implement strict access token validation in OAuth flows - verify token signature, expiration, scope, and intended audience
- Conduct security code reviews specifically for OAuth integration logic before deployment
- Use well-tested OAuth libraries and frameworks rather than custom implementations
- Implement proper state parameter validation to prevent cross-site request forgery attacks
- Validate redirect URIs against strict whitelists
- Use PKCE (Proof Key for Code Exchange) for OAuth flows
- Implement comprehensive logging and monitoring of authentication events
- Regularly audit OAuth implementations for common vulnerabilities
- Test OAuth flows with invalid, expired, and mismatched tokens
- Educate developers on OAuth security best practices and common pitfalls

## Variant hunting
Search for similar token verification bypass patterns in other OAuth implementations. Look for applications that skip validation of token claims, don't verify token audience matching, fail to check token expiration, or implement custom token parsing logic. Test applications using OAuth with manipulated tokens, cross-service tokens, and expired tokens. Examine source code for missing validation steps in OAuth callback handlers.

## MITRE ATT&CK
- T1190
- T1110
- T1078
- T1528
- T1556

## Notes
This is part three of a trilogy of OAuth vulnerability research. Previous posts covered Booking.com and Expo vulnerabilities. The research demonstrates that the OAuth protocol itself is secure, but implementation details in web services create exploitable gaps. Researchers estimated the vulnerabilities affected hundreds of millions of users across just three target sites, with thousands of additional websites likely vulnerable. The fix required only one line of code, highlighting how subtle implementation errors can have catastrophic security impact.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
