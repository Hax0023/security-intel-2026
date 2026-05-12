# Stored Cross-Site Scripting (XSS) in Oberlo Account Profile Settings

## Metadata
- **Source:** HackerOne
- **Report:** 542258 | https://hackerone.com/reports/542258
- **Submitted:** 2019-04-18
- **Reporter:** masterhackor
- **Program:** Oberlo
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the account profile settings page where user-supplied JavaScript code injected into the Name field is stored and executed in the browser of any user viewing that profile. An attacker can inject malicious payloads like ><img src=x onerror=alert(document.domain)> to achieve arbitrary code execution.

## Attack scenario
1. Attacker creates an account on Oberlo and navigates to /settings/account/profile
2. Attacker injects XSS payload ><img src=x onerror=alert(document.domain)> into the Name form field
3. Payload is accepted and stored in the backend database without proper sanitization
4. When any user (including victims) views the attacker's profile or the profile data is rendered, the JavaScript payload executes in their browser
5. Attacker can escalate to session hijacking, credential theft, or malware distribution using more sophisticated payloads
6. Impact is persistent across all users and page reloads until the malicious content is removed

## Root cause
The application fails to properly validate and encode user input in the Name field before storage and rendering. Input validation is absent or insufficient, and output encoding is not applied when displaying the stored profile name.

## Attacker mindset
An attacker would recognize that profile fields are typically displayed across the application and to other users, making them high-value injection points. The attacker would test common XSS payloads to identify input that bypasses filters, then weaponize the vulnerability for persistent attacks affecting multiple users.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields with whitelisting of allowed characters
- Apply context-appropriate output encoding (HTML entity encoding) when rendering user data in HTML context
- Use templating engines that provide automatic escaping by default
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Perform security code review focusing on all data flows from user input to output
- Add automated security testing (SAST/DAST) to catch XSS vulnerabilities in CI/CD pipeline
- Sanitize user input server-side using established libraries (e.g., DOMPurify for client-side, OWASP ESAPI)

## Variant hunting
Test other profile fields (bio, description, company name, website URL) for stored XSS
Check if profile data is reflected in emails, exports, or API responses without encoding
Verify if admin/support panel displays user profiles with the same vulnerability
Test SVG/XML injection vectors in profile fields
Check for DOM-based XSS when profile data is manipulated via JavaScript
Test Unicode/UTF-8 bypasses for XSS filters on the Name field

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a classic stored XSS vulnerability in a user profile field. The attack surface is wide as profile information is typically displayed to other users and across multiple pages. The vulnerability severity is elevated because it affects all users who view the compromised profile. No complexity is required to exploit - basic XSS knowledge and account creation are sufficient. The report lacks specific remediation timeline but demonstrates a serious risk to Oberlo users.

## Full report
<details><summary>Expand</summary>

1- create an account from **https://app.oberlo.com/**

2- path to https://app.oberlo.com/settings/account/profile

3- inject javascript code or xss payload at **Name** form

4- it will be printed at page and executed

payload that i used it **"><img src=x onerror=alert(document.domain)>**

## Impact

This vulnerability can be used by attacker to serve malicious JavaScript against any user.

</details>

---
*Analysed by Claude on 2026-05-12*
