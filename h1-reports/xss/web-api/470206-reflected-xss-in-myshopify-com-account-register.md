# Reflected XSS in *.myshopify.com/account/register

## Metadata
- **Source:** HackerOne
- **Report:** 470206 | https://hackerone.com/reports/470206
- **Submitted:** 2018-12-20
- **Reporter:** ishahriyar
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Missing Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the customer registration page where user-supplied input (first name and last name) is reflected back in error messages without proper HTML encoding or validation. An attacker can craft a malicious URL containing JavaScript payload and trick customers into clicking it, leading to arbitrary script execution in their browsers.

## Attack scenario
1. Attacker identifies that the registration form accepts first name and last name fields with minimal validation
2. Attacker crafts a malicious URL containing XSS payload in the first/last name parameters (e.g., <script>alert('XSS')</script>)
3. Attacker distributes the malicious link via phishing email, social media, or ads targeting Shopify customers
4. Victim clicks the link and is redirected to *.myshopify.com/account/register with the error message containing the unencoded payload
5. Victim's browser executes the injected JavaScript, allowing the attacker to steal session cookies, capture credentials, or perform actions on behalf of the user
6. Attacker can harvest customer data, perform account takeover, or pivot to further attacks

## Root cause
The application reflects user input (first name and last name) directly into error messages on the registration page without proper HTML encoding, context-aware escaping, or Content Security Policy (CSP) headers. The lack of input validation on client-side and server-side allows special characters and script tags to pass through.

## Attacker mindset
An attacker recognizes that registration pages are high-traffic endpoints visited by many users. By leveraging reflected XSS, they can conduct scalable attacks without needing to store malicious data. The attacker can impersonate legitimate Shopify communications to increase click-through rates and exploit user trust in the Shopify domain.

## Defensive takeaways
- Implement strict input validation on all user-supplied form fields, rejecting or sanitizing HTML/script content
- Apply context-aware output encoding (HTML entity encoding) to all user input reflected in responses
- Deploy a robust Content Security Policy (CSP) header to prevent inline script execution
- Use templating engines that auto-escape output by default
- Implement CSRF tokens on forms to prevent unauthorized submissions
- Apply HTTP-only and Secure flags on sensitive cookies to mitigate session theft
- Conduct regular security testing including XSS scanning on all user input endpoints
- Use a Web Application Firewall (WAF) to detect and block common XSS patterns

## Variant hunting
Check other registration/form pages for similar reflected XSS vulnerabilities
Test contact forms, password reset, and other pages accepting user input
Investigate if stored XSS exists when admin views customer registration data
Test for DOM-based XSS in client-side JavaScript processing of form fields
Check API endpoints for JSON-based XSS reflection
Test other Shopify subdomains and endpoints for similar issues
Verify if custom form fields in checkout pages have the same vulnerability

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing
- T1598: Phishing for Information
- T1539: Steal Web Session Cookie

## Notes
This is a classic reflected XSS vulnerability on a high-value endpoint. The vulnerability is particularly impactful because it targets the registration flow where users may already be in a compromised state. The lack of CSRF protection mentioned in the writeup suggests additional security gaps. The vulnerability likely affects all shops using Shopify's default registration flow.

## Full report
<details><summary>Expand</summary>

Shopify allows shop admin to enable customer registration. When a customer registers with a short password and HTML content as the first name and last name then customer redirects to *.myshopify.com/account/register with error messages and the provided data. As there is no Cross-site Scripting validation and CSRF protection anyone can force the customers to execute  XSS on that page.

{F394911}

## Impact

By exploiting this Vulnerability
An attacker can force the customer to execute XSS and 
1. Steal user's cookie.
2. Launch advanced phishing attacks by rendering arbitrary HTML forms.
3. Force users to download malware/viruses.
4. Execute browser-based attacks etc.

</details>

---
*Analysed by Claude on 2026-05-12*
