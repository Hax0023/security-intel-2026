# Open Redirect in Shopify Theme Preview via domain_name Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 101962 | https://hackerone.com/reports/101962
- **Submitted:** 2015-11-25
- **Reporter:** blinkms
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Open Redirect, CWE-601
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in Shopify's theme preview endpoint that accepts an unvalidated domain_name parameter and redirects users to attacker-controlled domains. An attacker can craft malicious URLs to redirect legitimate users to phishing sites, leveraging the trusted Shopify domain to bypass user skepticism.

## Attack scenario
1. Attacker identifies the vulnerable endpoint at /services/google/themes/preview/ accepting domain_name parameter
2. Attacker crafts a malicious URL: https://app.shopify.com/services/google/themes/preview/supply--blue?domain_name=attacker.com
3. Attacker embeds the URL in phishing emails or social media posts, appearing to come from legitimate Shopify domain
4. Victim clicks the link, seeing the trusted Shopify URL in browser address bar
5. Application redirects victim to attacker.com/admin without validation
6. Victim lands on attacker's fake admin page and submits credentials or other sensitive information

## Root cause
The application uses user-supplied domain_name parameter directly in redirect logic without validation against a whitelist of allowed domains, sanitization, or verification that the target is a legitimate internal endpoint.

## Attacker mindset
Leverage trust in established brands like Shopify to increase phishing success rates. The legitimate Shopify domain in the initial click makes attacks more convincing, bypassing basic URL inspection by security-conscious users.

## Defensive takeaways
- Implement whitelist-based validation for all redirect parameters - only allow redirects to known, trusted domains or relative paths
- Use relative URLs (e.g., /path/to/page) instead of absolute URLs when possible
- Encode and validate all user-supplied redirect destinations against a strict allowlist pattern
- Implement Content Security Policy (CSP) headers to restrict redirect destinations
- Add user confirmation dialogs for cross-domain redirects
- Log and monitor suspicious redirect patterns for security analytics
- Implement SSRF-like controls to prevent redirects to internal/private IP ranges

## Variant hunting
Check other theme preview endpoints and parameter names (redirect, return_url, callback, url, goto, target)
Test other Shopify services endpoints (/services/*, /admin/*, /apps/*) for similar redirect parameters
Look for unvalidated parameters in OAuth callback handlers and post-login redirects
Examine API endpoints that may accept URL parameters for theme customization or preview features
Test for chained redirects to bypass validation (parameter containing another redirect URL)

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Link
- T1021.005 - Remote Service Session Hijacking (credential theft via phishing)

## Notes
The CVSS score of 6.5 (Medium) is appropriate as this requires user interaction and relies on social engineering. The vulnerability is particularly dangerous in enterprise contexts where Shopify merchant credentials provide access to payment processing and customer data. The proof of concept demonstrates hosting a fake /admin page, which aligns with common phishing tactics.

## Full report
<details><summary>Expand</summary>

An open redirect is an application that takes a parameter and redirects a user to the parameter value without any validation. This vulnerability is used in phishing attacks to get users to visit malicious sites without realizing it. 

Vulnerable Endpoint - https://app.shopify.com/services/google/themes/preview/supply--blue?domain_name=example.com
Impact - Medium
CVSS - 6.5 

Proof of concept :- 

[1] Go to https://app.shopify.com/services/google/themes/preview/supply--blue?domain_name=example.com
[2] You will be redirected to http://example.com/admin
[3] I can host a site where /admin is not 404 {not valid page } , This can lead and increase risk of phisiing attacks & so on .




</details>

---
*Analysed by Claude on 2026-05-24*
