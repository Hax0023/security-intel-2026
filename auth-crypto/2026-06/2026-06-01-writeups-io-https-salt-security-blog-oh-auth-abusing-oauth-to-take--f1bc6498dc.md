# Oh-Auth: Abusing OAuth to Take Over Millions of Accounts

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Salt Labs Security Research (Grammarly, Vidio, Bukalapak)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** OAuth Implementation Flaw, Access Token Verification Bypass, Account Takeover, Authentication Bypass, Credential Leakage
- **Category:** auth-crypto
- **Writeup:** https://salt.security/blog/oh-auth-abusing-oauth-to-take-over-millions-of-accounts

## Summary
Researchers discovered critical OAuth implementation vulnerabilities in major web services (Grammarly, Vidio, Bukalapak) that allowed attackers to take over millions of accounts without authentication. The vulnerability stemmed from improper access token verification in OAuth implementations, enabling complete account takeover with potential for identity theft, financial fraud, and unauthorized access to sensitive data.

## Attack scenario (step by step)
1. Attacker identifies OAuth implementation flaw in target website's social login mechanism
2. Attacker crafts malicious OAuth request exploiting improper access token verification
3. Attacker bypasses token validation checks through implementation gaps
4. Attacker gains unauthorized access to user accounts without credentials
5. Attacker can escalate privileges and access sensitive user data (PII, payment info)
6. Mass account takeover becomes possible across hundreds of millions of users

## Root cause
OAuth protocol itself is secure, but improper server-side implementation of access token verification during the OAuth flow allows attackers to bypass authentication. The vulnerability exists in how web services integrate OAuth into their existing platform architecture without proper validation of returned tokens and user identity binding.

## Attacker mindset
Target widely-adopted OAuth implementations where developers may cut corners or misunderstand security requirements. Focus on popular services with millions of users to maximize impact. Exploit the assumption that OAuth handles all security automatically, when implementation details matter critically.

## Defensive takeaways
- Implement strict server-side access token verification - validate token signature, expiration, and issuer
- Bind access tokens to specific user identities and validate this binding on every request
- Do not rely solely on OAuth protocol security; thoroughly validate all responses from OAuth providers
- Implement proper state parameter validation to prevent CSRF attacks
- Use token introspection endpoints to verify token validity before granting access
- Implement rate limiting and anomaly detection on authentication endpoints
- Conduct security code review of OAuth integration implementations
- Test OAuth flows for edge cases and implementation gaps
- Keep OAuth libraries and dependencies up to date

## Variant hunting
Search for similar OAuth implementation flaws in other major platforms implementing social login. Focus on: improper PKCE implementation, state parameter handling, redirect URI validation bypasses, token scope enforcement issues, and cross-origin request validation in OAuth callbacks. Examine how different frameworks (Node.js, Python, PHP) implement OAuth to find common patterns of vulnerability.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1078 - Valid Accounts
- T1110 - Brute Force
- T1621 - Multi-Factor Authentication Bypass

## Notes
This is part of a three-part research series by Salt Labs on OAuth vulnerabilities. Previous posts covered vulnerabilities in Booking.com and Expo. The researchers responsibly disclosed all findings and companies patched quickly. The fix is described as 'one line of code away' suggesting simple validation checks were missing. Research estimated impact on hundreds of millions of users across three sites alone, with potential for thousands of additional vulnerable websites.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
