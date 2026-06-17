# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak (and potentially thousands of other websites)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Credential Leakage, Improper State Parameter Validation, CSRF in OAuth Flow
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Salt Labs discovered critical OAuth implementation vulnerabilities affecting millions of users across major platforms including Grammarly, Vidio, and Bukalapak that could enable complete account takeover. The vulnerabilities stem from improper access token verification and state parameter validation in OAuth implementations. The research demonstrates that while OAuth protocol itself is secure, poor integration into existing platforms creates exploitable gaps requiring minimal code changes to fix.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth for social login (e.g., Grammarly with Facebook login)
2. Attacker initiates OAuth flow and captures the authorization code returned by the OAuth provider
3. Attacker modifies the access token or bypasses token verification by exploiting implementation gaps
4. Attacker manipulates state parameters or exploits CSRF protections in the OAuth redirect flow
5. Attacker redirects victim to the target website with crafted OAuth parameters or reuses leaked credentials
6. Victim's account is taken over as the attacker's identity is now authenticated on the target service

## Root cause
OAuth implementations fail to properly verify access tokens and validate state parameters during the redirect phase. Developers integrate OAuth into existing platforms without adequately implementing verification mechanisms, allowing attackers to bypass token validation or exploit state parameter handling. The fix typically requires a single line of code addition for proper token verification.

## Attacker mindset
An attacker recognizes that OAuth's complexity and widespread adoption creates implementation gaps. By focusing on how services integrate OAuth rather than the protocol itself, attackers can find simple yet critical vulnerabilities affecting millions of users. The attacker targets high-value platforms knowing that account takeover enables identity theft, financial fraud, and access to sensitive personal data.

## Defensive takeaways
- Always verify access tokens server-side before granting authentication, never rely solely on client-side validation
- Implement proper state parameter validation to prevent CSRF attacks in OAuth flows
- Validate that tokens match the request context and user identity before session creation
- Conduct security reviews of OAuth integration code with the same rigor as core authentication logic
- Implement token expiration and refresh token rotation mechanisms
- Log and monitor OAuth authentication failures for anomalous patterns
- Use OAuth provider's token introspection endpoints to validate tokens server-side
- Apply principle of least privilege to OAuth scopes requested
- Educate developers on common OAuth implementation pitfalls through secure coding guidelines

## Variant hunting
Search for OAuth implementations across platforms using similar social login patterns. Examine redirect handling, token validation logic, and state parameter processing. Look for sites that accept OAuth tokens without server-side verification, or that fail to bind tokens to specific users or sessions. Check for improper error handling in OAuth flows that leaks token information. Audit sites using custom OAuth implementations rather than established SDKs.

## MITRE ATT&CK
- T1190
- T1598
- T1606
- T1110
- T1040
- T1539
- T1528

## Notes
This is the third in a series of OAuth vulnerability disclosures by Salt Labs, following similar findings on Booking.com and Expo. The research impacts hundreds of millions of users globally. All affected companies responded quickly to remediation. The authors estimate thousands of additional vulnerable websites exist, putting billions of users at risk. The simplicity of the fix (one line of code) contrasts sharply with the critical severity, highlighting the gap between protocol security and implementation reality.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
