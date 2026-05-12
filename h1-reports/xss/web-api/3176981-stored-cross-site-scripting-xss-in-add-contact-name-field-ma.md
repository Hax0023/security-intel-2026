# Stored Cross-Site Scripting (XSS) in MainWP Plugin 'Add Contact' Name Field

## Metadata
- **Source:** HackerOne
- **Report:** 3176981 | https://hackerone.com/reports/3176981
- **Submitted:** 2025-06-04
- **Reporter:** rishail01
- **Program:** MainWP (WordPress Plugin)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored XSS, Improper Input Sanitization, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The MainWP WordPress plugin fails to sanitize user input in the Client Management 'Add Contact' > Contact Name field, allowing attackers to inject malicious JavaScript payloads that persist in the database. When any administrator views the affected client profile, the stored XSS payload executes with full admin privileges, enabling session hijacking and unauthorized actions.

## Attack scenario
1. Attacker identifies the MainWP plugin installation on a target WordPress multisite network
2. Attacker gains access to the client management interface (via compromised low-privilege account, social engineering, or CSRF)
3. Attacker inserts JavaScript payload '</TITLE><SCRIPT>alert("XSS");</SCRIPT>' into the Contact Name field while adding/editing a client
4. Attacker saves the malicious contact, which persists in the database without sanitization
5. Administrator views or edits the infected client profile, triggering automatic execution of the stored XSS payload
6. Attacker's JavaScript executes with admin privileges, enabling cookie theft, admin action impersonation, or malicious plugin installation

## Root cause
The application fails to implement adequate input sanitization (using functions like sanitize_text_field() or wp_kses_post()) and output encoding (htmlspecialchars() or wp_esc_html()) on the Contact Name field before storage and rendering in the DOM.

## Attacker mindset
An attacker with low-to-medium access (subscriber/editor account) exploits the missing validation to plant persistent malicious code targeting high-privilege users. This represents a classic privilege escalation attack where stored XSS in admin-accessible areas leads to full dashboard compromise.

## Defensive takeaways
- Always sanitize user input at the point of entry using appropriate WordPress functions (sanitize_text_field, sanitize_textarea_field) based on expected data type
- Always encode output when rendering stored data to HTML context using wp_esc_html(), wp_esc_attr(), or wp_kses_post()
- Implement Content Security Policy (CSP) headers to mitigate XSS impact by restricting inline script execution
- Use WordPress escaping functions consistently throughout templates and rendering logic
- Conduct security code review of all user-controlled input fields, especially in admin panels
- Implement automated security scanning (SAST) in CI/CD pipeline to detect missing sanitization/escaping
- Apply principle of least privilege: restrict who can add/edit clients to minimize attack surface

## Variant hunting
Search for similar patterns in other MainWP plugin modules that handle user input: Client Notes, Company Name, Address fields, Custom Fields, Contact Email/Phone fields. Check all add/edit forms in the Client Management section and other admin pages that store and display user-controlled data without validation.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1187

## Notes
This is a classic Stored XSS in WordPress plugin admin interface. The vulnerability is particularly dangerous because MainWP manages multiple WordPress sites, making the compromised dashboard a high-value target. The proof-of-concept uses a simple alert() but could easily be replaced with cookie-stealing, admin user creation, or plugin installation payloads. The vulnerability likely affects multiple fields beyond Contact Name and should prompt comprehensive plugin audit.

## Full report
<details><summary>Expand</summary>

While testing the MainWP WordPress plugin (https://github.com/mainwp/mainwp), I discovered a stored XSS vulnerability in the Client Management feature, specifically in the "Add Contact" > Contact Name field.

The issue occurs because the application does not sanitize user input before rendering it back into the DOM. As a result, an attacker can inject malicious JavaScript payloads that are stored in the database and later executed in the browser of any user (typically admin) who views the infected client profile.

I crafted a payload and inserted it into the Contact Name field while editing a client:

`</TITLE><SCRIPT>alert("XSS By Rishail 2025");</SCRIPT>`

After saving the changes, the payload got stored as-is, and the JavaScript executed instantly upon reloading the client’s detail page — proving the XSS vulnerability.

## Impact

This vulnerability allows an attacker to execute arbitrary JavaScript in the browser of any user who views the affected page, leading to full control of the user’s session and actions.

An attacker can exploit this to:

- Steal administrator session cookies.

- Perform unauthorized actions as an admin (e.g., add malicious clients or plugins).

If an attacker stores a malicious script in the Contact Name field, any admin who views or edits that client will unknowingly trigger the payload. This can result in full compromise of the MainWP Dashboard, allowing the attacker to manipulate connected WordPress sites, push fake updates, or leak sensitive client data — causing reputational and operational damage.

</details>

---
*Analysed by Claude on 2026-05-12*
