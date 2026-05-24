# Open Redirect Vulnerability in Acronis Cloud Authorization Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 846389 | https://hackerone.com/reports/846389
- **Submitted:** 2020-04-10
- **Reporter:** angeltsvetkov
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, URL Redirection to Untrusted Site, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the OAuth 2.0 authorization endpoint at mc-beta-cloud.acronis.com where the 'state' parameter is reflected back without proper validation, allowing attackers to redirect users to arbitrary external domains. This enables phishing attacks and credential harvesting by disguising malicious redirects as legitimate Acronis authentication flows.

## Attack scenario
1. Attacker crafts malicious URL with state parameter pointing to attacker-controlled domain (evil.com)
2. Attacker sends link to victim via email, phishing campaign, or social engineering
3. Victim clicks link believing they are authenticating with legitimate Acronis service
4. Authorization endpoint processes request and redirects to malicious domain specified in state parameter
5. Victim lands on attacker's lookalike site which mimics Acronis login page
6. Victim enters credentials on fake site, attacker captures sensitive authentication data

## Root cause
The authorization endpoint fails to validate that the 'state' parameter is a trusted value. Instead of validating the state against a server-side whitelist or cryptographically binding it to the session, the application directly uses the user-supplied value for redirection without sanitization or validation.

## Attacker mindset
An attacker would leverage this for credential theft and account compromise by creating convincing phishing pages that appear to be part of the legitimate authentication flow, exploiting user trust in the Acronis domain to lower security awareness.

## Defensive takeaways
- Implement strict whitelist validation for redirect URIs - use pre-registered callback URLs only
- Never reflect user-supplied parameters directly into redirect locations without validation
- Use cryptographically secure, session-bound state parameters that cannot be manipulated by users
- Implement protocol-level protections: validate that redirect targets use HTTPS and match registered domains
- Add security headers (X-Frame-Options, CSP) to prevent framing attacks on authorization pages
- Log all redirect attempts with mismatched state values for anomaly detection
- Implement rate limiting on authorization endpoint to detect automated phishing attempts

## Variant hunting
Test other OAuth parameters: redirect_uri, client_id for similar validation bypasses
Check if other Acronis domains have similar patterns (cloud.acronis.com, different regional endpoints)
Examine whether state validation is client-side only vs server-side
Test if URL encoding/double-encoding bypasses any validation (e.g., http://evil.com vs %68ttp://evil.com)
Check if relative redirects are possible (e.g., state=//evil.com or state=///evil.com)
Test if JavaScript protocols work (e.g., state=javascript:alert())
Examine other authentication endpoints in the application for similar patterns

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1586.003

## Notes
This is a classic open redirect flaw common in OAuth/OIDC implementations. The 'state' parameter is specifically designed as a CSRF token and should be validated server-side against stored session values, not reflected back directly. The vulnerability is in a beta environment (mc-beta-cloud) which may indicate testing infrastructure had less rigorous security controls than production.

## Full report
<details><summary>Expand</summary>

Open Redirect Vulnerability

Steps To Reproduce:
Type in this URL:

https://mc-beta-cloud.acronis.com/api/2/idp/authorize?client_id=f2e82dbb-78af-4b5b-bc7f-651d4f42a722&redirect_uri=%2Fbc%2Fapi%2Fgateway%2Fcb&response_type=code&scope=offline_access+openid+profile+email&state=http://evil.com&nonce=yhokbempqmmqllfbwpsfzfmf

You got redirect to evil.com

Parameter: state

## Impact

n attacker can use this vulnerability to redirect users to other malicious websites, which can be used for phishing and similar attacks

</details>

---
*Analysed by Claude on 2026-05-24*
