# Open Redirect via Follow Parameter Leaking Authenticity Token to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 49759 | https://hackerone.com/reports/49759
- **Submitted:** 2015-03-02
- **Reporter:** seifelsallamy
- **Program:** Twitter
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Open Redirect, Cross-Site Request Forgery (CSRF), Credential/Token Leakage, Post-Redirect-Get (PRG) Token Exposure
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability in Twitter's mobile follow endpoint allowed attackers to redirect users to arbitrary domains while submitting a POST request containing their authenticity_token. The leaked CSRF token could be captured and used to perform account takeover via unauthorized actions like tweeting, account modifications, or mobile number changes enabling account recovery attacks.

## Attack scenario
1. Attacker crafts malicious URL: https://mobile.twitter.com/messages/follow?recipient=/attacker.com
2. Attacker sends link to target Twitter user via social engineering
3. User clicks link and arrives at Twitter's follow endpoint with attacker-controlled redirect parameter
4. User clicks 'Follow' button, triggering POST request submission
5. Browser follows redirect to attacker.com while transmitting POST data containing authenticity_token
6. Attacker captures the leaked authenticity_token and uses it to perform CSRF attacks against victim's account

## Root cause
Insufficient validation of the 'recipient' parameter allowing open redirects, combined with POST request parameters (authenticity_token) being transmitted across domain boundaries during redirect operations. The application failed to implement proper redirect validation and token handling in cross-domain scenarios.

## Attacker mindset
Exploit trust in legitimate domains by chaining common web vulnerabilities. Recognizing that CSRF tokens leaking to attacker-controlled domains enables full account compromise. Identifying that mobile endpoints may have less security hardening than desktop versions.

## Defensive takeaways
- Implement strict whitelist validation for all redirect parameters (deny-by-default approach)
- Never transmit sensitive tokens (CSRF tokens, session identifiers) in POST data across domain boundaries
- Use secure token binding or SameSite cookie attributes to prevent CSRF token exfiltration
- Implement POST-Redirect-GET (PRG) pattern safely: POST to same origin, then redirect without sensitive data
- Apply same security controls to mobile endpoints as desktop versions
- Use relative redirects or validate against explicit allowlist of internal URLs only
- Monitor for redirect parameter patterns and block common bypass techniques
- Implement Content Security Policy (CSP) to limit where form submissions can be sent

## Variant hunting
Search for other endpoints accepting user-controlled redirect parameters (follow, login callbacks, logout, share endpoints)
Test redirect parameters on both mobile and desktop versions
Look for parameters like 'redirect', 'redirect_uri', 'return_to', 'next', 'url', 'recipient', 'callback'
Check for POST endpoints that perform redirects with user input
Test for open redirects on account-sensitive operations (settings, security, payment)
Examine token leakage in referrer headers during redirects
Test double-encoding and protocol bypass techniques (javascript:, data:, //)

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1187
- T1555.003
- T1556

## Notes
This vulnerability represents a critical account takeover vector by chaining open redirect with CSRF token leakage. The attacker demonstrated sophisticated understanding that leaked authenticity_tokens enable not just direct CSRF attacks but also account recovery attacks via mobile number modification. The mobile endpoint targeting suggests attackers actively search for less-secured alternative interfaces. The writeup is concise but effectively communicates the security impact.

## Full report
<details><summary>Expand</summary>

Hey guys
URL: https://mobile.twitter.com/messages/follow?recipient=/example.com
when I click 'Follow'
I will send my POST request to https://example.com
witch contains my authenticity_token
that can be used for anything like tweeting, following, sending messages, changing username.,.,.etc
it can be used too to Add a mobile number, and then steal the account by recovering it by the mobile number.
Thank You.

</details>

---
*Analysed by Claude on 2026-05-24*
