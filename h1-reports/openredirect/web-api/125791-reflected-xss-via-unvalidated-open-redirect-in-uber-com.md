# Reflected XSS via Unvalidated Open Redirect in uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 125791 | https://hackerone.com/reports/125791
- **Submitted:** 2016-03-24
- **Reporter:** mdv
- **Program:** Uber
- **Bounty:** Unknown (not specified in writeup)
- **Severity:** High
- **Vuln:** Open Redirect, Reflected XSS, URL Parameter Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The application contains an open redirect vulnerability in the URL routing mechanism that allows attackers to redirect users to arbitrary domains. This open redirect can be chained with XSS payloads to execute malicious JavaScript in the context of uber.com, potentially compromising user sessions and stealing sensitive data.

## Attack scenario
1. Attacker crafts a malicious URL using the vulnerable redirect pattern: https://www.uber.com/en//[attacker-domain]/
2. Attacker distributes the link via phishing emails or social engineering to target Uber users
3. Victim clicks the link, which initially loads from the trusted uber.com domain
4. The application processes the double-slash path traversal and redirects to the attacker's domain
5. Attacker's domain serves a page that mimics Uber's login or collects credentials
6. Victim enters credentials or sensitive data on the attacker's site, compromising their account

## Root cause
Insufficient input validation and improper URL sanitization in the redirect handler. The application fails to validate that redirect URLs belong to whitelisted domains and does not properly parse or normalize URL paths containing double slashes (//), which can be exploited for path traversal.

## Attacker mindset
Attackers leverage the trust users place in established brands like Uber. By creating a redirect from the legitimate domain, they bypass browser security warnings and increase phishing success rates. The vulnerability requires minimal technical sophistication but yields high success rates in social engineering campaigns.

## Defensive takeaways
- Implement strict whitelist-based validation for all redirect destinations
- Normalize and validate URL paths before processing redirects (handle //, \, encoded variants)
- Use allowlist approach: only permit redirects to known internal URLs or trusted partner domains
- Implement Content Security Policy (CSP) headers to prevent XSS exploitation
- Log all redirect attempts for security monitoring and anomaly detection
- Validate Host header and referer to prevent open redirects via alternative vectors
- Educate users about verifying URLs in the address bar before entering sensitive information
- Implement refresh-based redirects instead of JavaScript redirects where possible

## Variant hunting
Test various path traversal patterns: /en///example.com, /en/./example.com, /en/%2f/example.com
Check other language/locale endpoints: /fr//, /de//, /es// for similar vulnerabilities
Test encoded slashes and double-encoding: %2f%2f, %252f%252f
Look for callback URL parameters in authentication flows
Examine redirect parameters in OAuth/SSO implementations
Check for similar patterns in subdomains: api.uber.com, driver.uber.com
Test with unicode characters and normalization bypasses

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1056

## Notes
This is a classic example of how multiple vulnerabilities (open redirect + path traversal) can be chained to create a high-impact attack. The vulnerability is particularly dangerous because it leverages the trust users have in the uber.com domain. The double-slash technique is a well-known but frequently missed vulnerability pattern in URL parsing.

## Full report
<details><summary>Expand</summary>

Hello,
To reproduce this issue, visit this URL: https://www.uber.com/en//example.com/
This URL will redirect at [example.com](https://example.com/).

</details>

---
*Analysed by Claude on 2026-05-24*
