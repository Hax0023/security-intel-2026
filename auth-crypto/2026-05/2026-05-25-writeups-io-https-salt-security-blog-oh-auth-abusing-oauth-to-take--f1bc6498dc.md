# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Grammarly, Vidio, Bukalapak (and potentially thousands of other websites)
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln types:** OAuth Implementation Flaw, Insufficient Token Verification, Account Takeover, Authentication Bypass, Authorization Bypass
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Researchers discovered critical OAuth implementation vulnerabilities affecting millions of users across major platforms including Grammarly, Vidio, and Bukalapak. The vulnerability allows attackers to take over user accounts by exploiting improper OAuth token verification mechanisms. The affected companies have since patched the issues, but similar vulnerabilities are suspected to exist on thousands of other websites.

## Attack scenario (step by step)
1. Attacker identifies a target website using OAuth for social sign-in (e.g., 'Login with Facebook')
2. Attacker initiates OAuth flow with the target website
3. Attacker captures or manipulates the OAuth access token returned during the authentication process
4. Attacker submits the modified/captured token to the target application's token verification endpoint
5. Vulnerable implementation fails to properly validate the token origin, scope, or integrity
6. Attacker gains authenticated access to victim's account without knowing their credentials

## Root cause
Improper implementation of OAuth token verification in web services. The vulnerability stems from inadequate validation of access tokens during the authentication process, allowing tokens to be used in unauthorized contexts or to authenticate as different users than intended.

## Attacker mindset
Opportunistic exploitation of widespread OAuth misconfigurations across popular web platforms. Attackers recognize that OAuth's complexity and ease-of-implementation lead to common mistakes by developers at all expertise levels, creating low-effort, high-impact attack vectors affecting millions of users simultaneously.

## Defensive takeaways
- Implement strict OAuth token verification including origin validation and token binding to user sessions
- Validate token scope and intended audience (aud/client_id) before granting access
- Use state parameter validation to prevent CSRF attacks in OAuth flows
- Implement proper token expiration and refresh token rotation
- Verify token signature and issuer before accepting authentication
- Apply the principle of least privilege to OAuth scopes requested
- Conduct security reviews of OAuth implementations with security experts
- Monitor and log OAuth authentication events for anomaly detection
- Use security headers (SameSite cookies, HSTS) to prevent token theft

## Variant hunting
Search for similar OAuth implementation flaws in: redirect URI validation bypass, PKCE implementation gaps, response_type manipulation, implicit flow vulnerabilities, state parameter mishandling, token endpoint security, cross-site request forgery in OAuth flows, and improper handling of signed JWTs in ID tokens.

## MITRE ATT&CK
- T1190
- T1598
- T1110
- T1556
- T1187
- T1040
- T1539

## Notes
This is part 3 of a trilogy on OAuth vulnerabilities. Previous research covered Booking.com and Expo framework. The research estimated billions of additional Internet users at risk across thousands of potentially vulnerable websites. The fix is described as 'one line of code away,' suggesting simple oversight rather than complex vulnerability. Researchers responsibly disclosed findings and verified patches before public disclosure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
