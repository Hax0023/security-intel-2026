# Blind Stored XSS in Backend Admin Panel with Credential Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 1051369 | https://hackerone.com/reports/1051369
- **Submitted:** 2020-12-05
- **Reporter:** nagli
- **Program:** Undisclosed
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stored Cross-Site Scripting (XSS), Blind XSS, Insufficient Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A blind stored XSS vulnerability was discovered in the backend administration panel that allows attackers to inject malicious JavaScript payloads which are executed when administrators interact with affected functionality. The vulnerability enabled the attacker to extract sensitive information including administrative credentials, session cookies, and private data through an XSSHunter callback.

## Attack scenario
1. Attacker identifies an input field in the application that accepts user-supplied data without proper sanitization
2. Attacker crafts a malicious XSS payload (likely using XSSHunter) and injects it into a vulnerable field accessible to backend administrators
3. The payload is stored in the application database without sanitization or encoding
4. When an administrator accesses the backend functionality containing the stored payload, the JavaScript executes in their browser context
5. The XSSHunter payload collects sensitive information including the admin's IP address, user-agent, session cookies, and database credentials
6. Attacker receives callback notification with extracted data, gaining unauthorized access to administrative accounts and sensitive backend systems

## Root cause
Insufficient input validation and lack of output encoding on backend-facing functionality. The application failed to sanitize user input before storage and did not properly encode data when rendering it in the administrative interface, allowing malicious scripts to execute in administrator browsers.

## Attacker mindset
The attacker demonstrates sophisticated awareness of blind XSS exploitation techniques by utilizing XSSHunter, a specialized tool for detecting and exploiting stored XSS vulnerabilities. They strategically targeted backend administrators rather than regular users, recognizing that admin sessions provide higher-value access to sensitive systems, credentials, and private information.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-controllable input fields, especially those accessible to administrative users
- Apply context-appropriate output encoding (HTML entity encoding, JavaScript escaping, URL encoding) when rendering user-supplied data
- Use a Content Security Policy (CSP) with strict directives to prevent inline script execution and limit script sources
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access and transmission over unencrypted connections
- Never store or log sensitive credentials (database credentials, API keys) in user-accessible contexts or error messages
- Apply defense-in-depth: combine input validation, output encoding, WAF rules, and CSP headers
- Conduct regular security testing including blind XSS payload testing in all application surfaces
- Implement proper access controls and audit logging for administrative functions

## Variant hunting
Look for similar stored XSS vulnerabilities in: form fields saved for later review by admins, comment sections viewable by administrators, file upload metadata, error message displays, logs accessible to admins, notification systems, user profile information displayed in admin dashboards, and any backend functionality that stores and later renders user-supplied content.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1056 - Input Capture
- T1539 - Steal Web Session Cookie
- T1555 - Credentials from Password Stores
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel

## Notes
This report demonstrates critical impact as it successfully extracted administrative credentials and session tokens. The use of XSSHunter indicates a sophisticated attack methodology. The vulnerability's blind nature makes it particularly dangerous as it may persist undetected in production environments. Database credentials exposure elevates this to a system-level compromise risk. The report lacks specific remediation timeline and verification details but the impact claims are substantiated by the callback evidence referenced.

## Full report
<details><summary>Expand</summary>

**Summary:**
I have just gotten an email notification from my XSSHunter payload that my blind stored XSS has been triggered by an administrator on the █████████ site, in the following URL:

```javascript
https://█████/████
```

Admin IP address: 
████████

User-Agent:
█████████

Cookies:
```javascript
██████
```
Injection Image:

███████

DB Creds exposed:

██████████.█████\█████a

## Suggested Mitigation/Remediation Actions

Sanitizing the input on the back-end as well

##Best Regards
nagli

## Impact

Ability to capture administrator action when preforming activities on the back-end.
Extractions of DB credentials.
Access to private information.
Stealing the cookies of the administrator.

</details>

---
*Analysed by Claude on 2026-05-12*
