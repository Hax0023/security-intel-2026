# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak (and thousands of other websites)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Authentication Bypass, Credential Leakage
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs discovered critical OAuth implementation vulnerabilities affecting millions of accounts across major platforms including Grammarly, Vidio, and Bukalapak. The vulnerability allows attackers to bypass OAuth access token verification mechanisms to achieve complete account takeover without valid credentials. The flaw stems from improper implementation of OAuth token validation rather than issues with the OAuth protocol itself.

## Attack scenario (step by step)
1. Attacker identifies a web service using OAuth for social login authentication
2. Attacker crafts a malicious OAuth authorization request with modified parameters
3. Attacker manipulates the access token verification process during the OAuth callback
4. Attacker bypasses server-side token validation checks through implementation flaws
5. Attacker gains authentication without possessing valid OAuth credentials
6. Attacker successfully takes over victim's account on the target service

## Root cause
Improper implementation of OAuth access token verification on the service provider side. The vulnerability exists not in the OAuth protocol specification but in how web services integrate and validate OAuth tokens. Specifically, services fail to properly validate access tokens returned from OAuth providers, allowing attackers to forge or manipulate token verification.

## Attacker mindset
An attacker recognizes that while OAuth is cryptographically sound, its implementation complexity creates gaps when developers integrate it into existing platforms. By reverse-engineering the OAuth flow and testing various token manipulation techniques, an attacker can identify services that skip critical validation steps, enabling mass account compromise with minimal effort.

## Defensive takeaways
- Always validate OAuth access tokens server-side against the authorization provider
- Never trust token parameters without cryptographic verification
- Implement strict CSRF protection for OAuth callback handlers
- Validate state parameters and redirect URIs according to OAuth 2.0 specification
- Use token introspection endpoints to verify token validity with the OAuth provider
- Log and monitor unusual OAuth authentication patterns
- Conduct security reviews of OAuth implementation alongside protocol compliance checks
- Implement rate limiting on OAuth callback endpoints
- Use modern OAuth libraries that handle validation correctly rather than custom implementations

## Variant hunting
Search for other web services implementing OAuth social login without proper token validation. Test for: (1) acceptance of modified access tokens, (2) lack of token signature verification, (3) missing state parameter validation, (4) insufficient redirect URI validation, (5) improper handling of token expiration checks, (6) absence of PKCE implementation in OAuth flows.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1110 - Brute Force
- T1535 - Unsecured Credentials
- T1098 - Account Manipulation

## Notes
This is the third in a trilogy of blog posts by Salt Labs on OAuth vulnerabilities. Previous posts covered similar issues on Booking.com and Expo. The vulnerability affects billions of users globally across thousands of websites. The fix is reportedly 'one line of code away' according to the researchers, indicating a simple but critical implementation oversight. All mentioned companies (Grammarly, Vidio, Bukalapak) remediated the issues quickly upon notification.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
