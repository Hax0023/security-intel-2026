# Oh-Auth — Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Authentication Bypass, Credential Leakage
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs discovered critical OAuth implementation flaws in multiple major platforms (Grammarly, Vidio, Bukalapak) that allowed attackers to take over millions of user accounts through improper access token verification. The vulnerability exploited the gap between OAuth protocol design and its insecure integration into existing platforms, enabling complete account takeover without user credentials. All affected companies remediated the issues upon disclosure.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth for social login authentication
2. Attacker initiates OAuth authentication flow with a social provider (Facebook, Google, etc.)
3. Attacker intercepts or manipulates the OAuth flow to obtain an access token intended for one user
4. Attacker crafts a request to the target website with a modified or misused access token
5. Target website fails to properly verify the access token validity/ownership, granting access to arbitrary account
6. Attacker gains complete account takeover with ability to modify credentials, access personal data, and perform fraudulent actions

## Root cause
The OAuth protocol itself is secure, but implementation flaws occur during integration with existing platforms. Specifically, developers failed to properly verify that access tokens returned from OAuth providers actually belong to the requesting user, creating a disconnect between token validation and account binding.

## Attacker mindset
Attackers recognize that while OAuth is standardized, implementations vary widely and developers often take shortcuts. By finding the weakest link in the OAuth chain (token verification), attackers can gain access to hundreds of millions of accounts across multiple platforms without brute force or credential theft.

## Defensive takeaways
- Always verify that OAuth access tokens belong to the authenticated user before granting account access
- Implement strict token validation on the server-side, not just client-side
- Validate token ownership by comparing token claims with expected user identity
- Use OAuth state parameters correctly to prevent token mixing attacks
- Implement additional verification steps such as matching user IDs from token with authenticated session
- Regularly audit OAuth implementation against OAuth 2.0 Security Best Current Practice guidelines
- Conduct security code reviews specifically focused on OAuth integration points
- Test OAuth flows with tokens from different users to catch verification bypasses

## Variant hunting
Search for similar OAuth implementation flaws in websites using social login. Test if access tokens from different user accounts can be swapped or reused. Look for improper token scope validation. Check if redirect URI validation is properly enforced. Examine if PKCE (Proof Key for Code Exchange) is properly implemented in OAuth authorization code flow.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1110 - Brute Force (credential-based account access)
- T1098 - Account Manipulation
- T1185 - Traffic Signaling
- T1187 - Forced Authentication

## Notes
This is part three of a trilogy on OAuth vulnerabilities. The research impacted hundreds of millions of users across the disclosed vulnerabilities. The authors estimate thousands of additional websites may be vulnerable. The fix for this class of vulnerability is reportedly 'one line of code away,' suggesting simple but critical oversights in token validation logic. All three affected companies responded quickly to remediation, demonstrating that responsible disclosure processes worked effectively.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
