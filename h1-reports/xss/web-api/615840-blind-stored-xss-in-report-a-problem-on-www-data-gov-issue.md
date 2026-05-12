# Blind Stored XSS in 'Report a Problem' on data.gov/issue/

## Metadata
- **Source:** HackerOne
- **Report:** 615840 | https://hackerone.com/reports/615840
- **Submitted:** 2019-06-15
- **Reporter:** rioncool22
- **Program:** data.gov
- **Bounty:** unknown
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Blind XSS, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A blind stored XSS vulnerability exists in the 'Report a Problem' form on data.gov/issue/ where user-supplied payloads in the issue title and description fields are not properly sanitized before being stored and displayed in the admin CRM interface. An attacker can inject malicious JavaScript that executes in the admin's browser context when reviewing reports, potentially leading to session hijacking and cookie theft.

## Attack scenario
1. Attacker navigates to https://www.data.gov/issue/ and locates the 'Report a Problem' form
2. Attacker submits an XSS payload (e.g., XSSHunter) in the 'Issue Title' and/or 'Description' fields
3. The payload is stored server-side without proper sanitization or encoding
4. An administrator accesses https://labs.data.gov/crm/admin/report/662445 to review submitted reports
5. The stored XSS payload executes in the admin's browser with their privileges and session cookies
6. Attacker exfiltrates admin session cookies or performs actions on behalf of the administrator

## Root cause
The application fails to implement proper output encoding and input validation when storing and rendering user-submitted form data. The vulnerability likely stems from: (1) lack of HTML entity encoding when displaying report contents in the admin panel, (2) no Content Security Policy (CSP) headers, and (3) insufficient server-side validation of user inputs.

## Attacker mindset
An attacker recognizes that admin panels are high-value targets with elevated privileges. By injecting XSS into user-submitted forms, they exploit the blind XSS principle where the payload doesn't reflect immediately but fires when reviewed by administrators. This provides reliable execution in a privileged context without needing to interact directly with the admin interface.

## Defensive takeaways
- Implement strict input validation on all user-submitted form fields with whitelist-based validation
- Apply proper output encoding (HTML entity encoding, JavaScript escaping, URL encoding) based on context where data is rendered
- Enforce Content-Security-Policy headers to prevent inline script execution and restrict script sources
- Use a templating engine with automatic escaping enabled by default
- Sanitize HTML input using established libraries (e.g., DOMPurify, bleach) if HTML content is required
- Implement security headers (X-XSS-Protection, X-Content-Type-Options, X-Frame-Options)
- Perform regular security testing including automated XSS scanning and manual penetration testing
- Conduct security awareness training for developers on OWASP Top 10 vulnerabilities

## Variant hunting
Search for similar blind XSS vulnerabilities in other user-facing forms that feed into internal admin panels: contact forms, support tickets, feedback forms, help desk systems, and any feature allowing user-generated content displayed to administrators. Test all form fields (including hidden fields) and check if admin interfaces properly escape output. Also investigate whether the CRM system at labs.data.gov has other XSS vectors in report viewing or filtering functionality.

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.002
- T1539

## Notes
This is a blind XSS variant that requires admin interaction to trigger, making it harder to detect during initial reconnaissance but equally dangerous for privilege escalation. The use of XSSHunter suggests automated payload delivery and detection. The distinct URL domains (data.gov vs labs.data.gov) indicate backend infrastructure separation that may have different security postures.

## Full report
<details><summary>Expand</summary>

Step To Produce : 
1. Open :  https://www.data.gov/issue/
2. fill "Issue Title" and "Description" With XSSHunter Payload
3. XSS Fired In  https://labs.data.gov/crm/admin/report/662445

## Impact

Can steal admin cookies

</details>

---
*Analysed by Claude on 2026-05-12*
