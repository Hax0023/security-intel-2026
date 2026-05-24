# Stored XSS on Admin Access Page - Email Field

## Metadata
- **Source:** HackerOne
- **Report:** 173501 | https://hackerone.com/reports/173501
- **Submitted:** 2016-10-02
- **Reporter:** pavanw3b
- **Program:** Revive Adserver
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The Email field on the Inventory > Admin Access page fails to sanitize user input, allowing authenticated administrators to inject malicious JavaScript that persists and executes for other administrators viewing the page. This stored XSS vulnerability can be exploited by one admin to compromise other admin accounts through code injection in the email preferences.

## Attack scenario
1. Admin1 logs into Revive Adserver and navigates to Preferences > Change E-mail
2. Admin1 enters a malicious payload in the Email address field: admin1@example.com<script>alert('xss');</script>
3. The application stores the unsanitized email value in the database without validation or encoding
4. Admin2 logs in and navigates to Inventory > Admin Access page
5. The page retrieves and renders Admin1's email from the database without encoding
6. The JavaScript payload executes in Admin2's browser context, allowing session hijacking, credential theft, or further exploitation

## Root cause
The application fails to implement proper output encoding when displaying the email field on the Admin Access page. While the email is stored in the database unsanitized, the critical issue is the lack of HTML entity encoding (e.g., using htmlspecialchars or equivalent) when rendering the value in the admin interface, allowing script tags to execute.

## Attacker mindset
A disgruntled or malicious administrator seeks to compromise other administrators' accounts or the application itself. By injecting a JavaScript payload via the email field, they can execute arbitrary code in victims' browsers when they view the admin access page, potentially escalating privileges, stealing session cookies, or deploying beacons for persistent access.

## Defensive takeaways
- Implement comprehensive output encoding for all user-controlled data before rendering in HTML context (use context-aware encoding: HTML entity encoding, JavaScript encoding, URL encoding as appropriate)
- Apply input validation to email fields to reject non-email characters and payloads (whitelist approach: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$)
- Implement Content Security Policy (CSP) headers to restrict inline script execution and mitigate XSS impact
- Use templating engines with auto-escaping enabled by default
- Conduct security code review of all forms and preference pages handling user input
- Implement automated security testing (SAST/DAST) in CI/CD pipeline to detect XSS vulnerabilities
- Apply principle of least privilege - even admins should have their capabilities restricted where possible
- Add administrative logging and alerts for email changes to detect suspicious modifications

## Variant hunting
Check other preference fields (name, phone, address, company) on the Preferences page for similar XSS vulnerabilities
Test all admin-facing pages that display user or admin data (Admin Access, User Management, Reports) for stored XSS
Examine other email fields throughout the application (contact forms, support pages, advertiser details) for the same sanitization issues
Test for second-order XSS by checking if email data is reflected in exported reports or admin dashboards
Verify if DOM-based XSS exists in JavaScript that processes email field data
Check for CSRF vulnerabilities combined with email change functionality to change admin emails remotely

## MITRE ATT&CK
- T1190
- T1059
- T1566

## Notes
This is a classic stored XSS vulnerability in a legacy admin panel (Revive Adserver v4.0.0). The reporter effectively demonstrated multi-user impact by showing how one admin can compromise another. The vulnerability highlights the importance of defense-in-depth: both input validation AND output encoding are necessary. The use of alert() as proof-of-concept is benign but could easily be replaced with credential harvesting, session stealing, or BeEF integration. This vulnerability likely affects admin privileges, making it critical for system security.

## Full report
<details><summary>Expand</summary>

"Cricetinae" :)

###Short Description

The **Email** field is not sanitized on **Inventory > Admin Access** page resulting in to Stored Cross-Site Scripting vulnerability.

###Vulnerability Details

Cross-Site Scripting issue let's one to run a javascript of choice. It helps most of the client side risks including but not limited to phishing, temporary deface, browser key-logger and others. Exploitation frameworks like BeEF eases the offensive attack.

Stored XSS is more risky than the reflected ones because of the fact that the malicious script is persisted across. It can affect all the time and all the users who has the access to the page.

### Attack Vector
As this is a stored XSS, the attack vector lies in one user phishing other users. If there are multiple administrators, one admin can get a javascript backdoor on another admin's browser.

### Steps to Reproduce
To effectively illustrate one user affect another user, please create 2 admin accounts and follow the below instruction:
* Login as `admin1`. Navigate to **Preferences** *>* **Change E-mail**
* Enter the current password and `admin1@example.com<script>alert('xss');</script>` for *Email address* field. Save and logout
* Login as `admin2`. 
* Navigate to **Inventory** *>* **Admin Access** and notice the alert box.

Attached screenshot for a reference.

### Test Environment Details
Version: Latest as on Oct 2: revive-adserver-4.0.0 downloaded from the official source
Setup type: local
Browser: Firefox 47.0
OS: Mac OS X


Cheers,
Pavan

</details>

---
*Analysed by Claude on 2026-05-24*
