# Reflected XSS on delivery.glovoapp.com /referrals/ endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1264805 | https://hackerone.com/reports/1264805
- **Submitted:** 2021-07-15
- **Reporter:** celesian
- **Program:** Glovo
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on the /referrals/ endpoint where the 'email' parameter is not properly sanitized or encoded before being reflected in the HTTP response. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when visited, allowing arbitrary script execution in the context of the vulnerable domain.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the email parameter: https://delivery.glovoapp.com/referrals/?email=%22%3E%3CsCriPt%3Eprompt(1)%3C%2Fscript%3E
2. Attacker distributes the URL via email, social media, or other social engineering channels to Glovo users
3. Victim clicks the malicious link while authenticated to their Glovo account
4. The JavaScript payload executes in the victim's browser with their session privileges
5. Attacker can steal session cookies, perform actions on behalf of the user, redirect to phishing sites, or harvest credentials
6. Attacker's script can access sensitive data, modify referral information, or facilitate account takeover

## Root cause
The 'email' query parameter is reflected directly into the page HTML without proper sanitization or output encoding. The application fails to implement context-aware output encoding (HTML entity encoding) or input validation, allowing angle brackets and script tags to pass through unfiltered.

## Attacker mindset
An attacker identifies that user-controlled input (email parameter) is echoed back in responses without validation. They recognize the referrals endpoint as a high-value target due to its customer-facing nature and potential for mass distribution. By using mixed-case script tags (sCriPt), they attempt to bypass basic case-sensitive filters.

## Defensive takeaways
- Implement strict input validation on all query parameters with whitelist-based approach for email format
- Apply proper output encoding using context-aware encoding functions (HTML entity encoding for HTML context)
- Use a templating engine with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to restrict script execution
- Apply HTTPOnly and Secure flags on session cookies to prevent XSS-based theft
- Conduct security code review focusing on user input handling across all endpoints
- Implement Web Application Firewall (WAF) rules to detect and block XSS patterns
- Use automated security testing (SAST/DAST) in CI/CD pipeline

## Variant hunting
Test other endpoints with similar parameter patterns (referral, email, contact, invite, share parameters)
Attempt DOM-based XSS variants using JavaScript event handlers (onerror=, onload=)
Test other query parameters on /referrals/ (lang parameter shown in PoC should also be tested)
Look for stored XSS if user data is persisted (referral links stored in database)
Test SVG-based XSS payloads: <svg onload=prompt(1)>
Test data exfiltration scenarios targeting referral tokens or user identifiers
Check for second-order XSS where parameters are stored and reflected later
Test for bypassable filters using Unicode encoding, HTML entities in payload

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1566.002 - Phishing: Spearphishing Link
- T1598 - Phishing for Information
- T1020 - Automated Exfiltration

## Notes
The PoC uses intentional case variation in script tag (sCriPt) suggesting awareness of potential case-sensitive filter mechanisms. The vulnerability affects delivery.glovo.com subdomain which appears to be customer-facing, making it high-risk for credential theft or mass exploitation. The lang=rs parameter should also be tested for similar vulnerabilities. No patching information was provided in the writeup.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi, there's a reflected XSS vulnerability present on the https://delivery.glovoapp.com/referrals/ endpoint.

## Steps To Reproduce:
Opening the following URL should trigger the prompt() window specified in the request parameters, indicating that arbitrary javascript can be injected into the page.
- https://delivery.glovoapp.com/referrals/?email=%22%3E%3CsCriPt%20class%3Ddalfox%3Eprompt%281%29%3C%2Fscript%3E&lang=rs

## Impact

An attacker can do several client-side attacks on Glovo customers.

</details>

---
*Analysed by Claude on 2026-05-12*
