# Stored XSS on Share-popup of a directory's Gallery-view

## Metadata
- **Source:** HackerOne
- **Report:** 145355 | https://hackerone.com/reports/145355
- **Submitted:** 2016-06-17
- **Reporter:** fransrosen
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding
- **CVEs:** CVE-2016-7419
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Nextcloud Files' Gallery-view share functionality where directory names containing HTML payloads are not properly sanitized before being rendered in the share popup. An attacker can create a directory with a malicious name containing JavaScript code that executes when any user clicks the share icon, potentially affecting administrative users in browsers without CSP support.

## Attack scenario
1. Attacker creates a directory in Nextcloud Files with a malicious name: '<img src=x onerror=alert(1)>'
2. The directory name is stored in the database without sanitization
3. Attacker shares the directory path or invites an admin to access it
4. Admin or victim switches to Gallery-view in the Files application
5. Victim clicks the Share-icon on the malicious directory
6. The unsanitized HTML payload in the directory name executes in the victim's browser context

## Root cause
The directory name is not properly HTML-encoded when displayed in the share popup. The application fails to escape special characters (< > \ " ') before inserting the directory name into the DOM, allowing arbitrary HTML/JavaScript to be injected.

## Attacker mindset
An attacker with file upload/creation privileges exploits the lack of output encoding to persistently inject malicious scripts. The attack is particularly dangerous against administrators and is especially effective in older browsers (like Internet Explorer) that don't enforce Content Security Policy headers.

## Defensive takeaways
- Always HTML-encode user-controlled input before rendering in HTML context (use textContent instead of innerHTML, or proper escaping functions)
- Implement and enforce Content Security Policy (CSP) headers to mitigate XSS even if encoding is missed
- Use templating engines with automatic escaping enabled by default
- Apply input validation for file/directory names to reject or sanitize special characters
- Test security across multiple browsers, including older versions without modern security features
- Implement output encoding consistently across all UI components, especially in modal dialogs and popups

## Variant hunting
Check all other file/directory property displays (rename dialogs, file details, comments, tags)
Test share dialogs for public shares, group shares, and link shares
Check breadcrumb navigation and path displays in Gallery-view
Verify if other views (list view, table view) have similar encoding issues
Test metadata displays (file descriptions, custom properties)
Check if directory names in activity logs or audit trails are encoded

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204.001 - User Execution: Malicious Link
- T1547.011 - Boot or Logon Initialization Scripts: Plist Modification

## Notes
The vulnerability is particularly critical because: (1) any user can create directories, enabling widespread exploitation, (2) administrative users are high-value targets, (3) the attack is persistent/stored, (4) browsers without CSP support are fully vulnerable, and (5) the share functionality is commonly used when collaborating. The reporter appropriately notes CSP as a defense mechanism but correctly identifies it as insufficient against all browsers.

## Full report
<details><summary>Expand</summary>

Hi,
Nice with the program launch! Congrats!

I noticed that there was a Share-icon when toggling to the Gallery-view of a directory under "Nextcloud Files":
{F99938}

If your directory has a malicious name such as a HTML-payload: `<img src=x onerror=alert(1)>`, this HTML will run when clicking on the Share-icon:
{F99937}

I see that you have a proper CSP in place, but remember that Internet Explorer is not there yet:
{F99939}

Also, since any user could create files, a user could potentially execute this for an admin (if that admin is not using a CSP-supported browser that is).

Let me know if you need more information.

Regards,
Frans

</details>

---
*Analysed by Claude on 2026-05-12*
