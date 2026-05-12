# Stored XSS in Nextcloud Desktop Client Notifications via Unsanitized Filename

## Metadata
- **Source:** HackerOne
- **Report:** 1668028 | https://hackerone.com/reports/1668028
- **Submitted:** 2022-08-12
- **Reporter:** b911bade858ce8e6a0f50f8
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, HTML Injection
- **CVEs:** CVE-2022-39331
- **Category:** web-api

## Summary
The Nextcloud Desktop Client fails to sanitize file names before rendering them in notification dialogs and UI elements, allowing attackers to inject arbitrary HTML/JavaScript. An attacker with file upload privileges can rename files to contain malicious HTML tags, which will be rendered as markup in the desktop client when sync notifications are displayed.

## Attack scenario
1. Attacker gains access to a Nextcloud Server instance (either as legitimate user or via compromise)
2. Attacker uploads a benign file to the server
3. Attacker renames the file to include HTML/JavaScript payload, e.g., '<img src=x onerror=alert(1)>' or '<h1><b><i><u>payload'
4. Desktop Client user syncs their folder or receives sync notifications
5. Desktop Client renders the malicious filename in notification dialogs without sanitization
6. Injected HTML/JavaScript executes in the context of the Desktop Client application

## Root cause
The Nextcloud Desktop Client application directly renders file names obtained from server responses into UI elements (notifications and dialogs) without proper HTML encoding or escaping. The application treats user-controlled file name data as trusted content.

## Attacker mindset
An attacker with file management capabilities exploits the trust boundary between server and client. By injecting HTML into file names, they can achieve code execution or data theft in the context of the user's desktop client, potentially stealing credentials or local files. This is particularly effective because users expect desktop applications to be safer than web applications.

## Defensive takeaways
- Always sanitize and HTML-encode user-controlled data before rendering in UI, especially file names from untrusted sources
- Use framework-provided escaping functions rather than manual sanitization
- Implement Content Security Policy (CSP) equivalent restrictions in desktop applications
- Validate file names on the server to reject or sanitize dangerous characters/sequences
- Apply principle of least privilege - desktop client should run with minimal permissions
- Test file handling with malicious file names as part of security testing
- Use safe DOM APIs that auto-escape content (e.g., textContent instead of innerHTML)

## Variant hunting
Search for other UI elements displaying file names, folder names, or user-controlled strings without sanitization
Check sync error messages, conflict resolution dialogs, and activity logs for similar issues
Test other string inputs from server (usernames, share names, tags, comments) for XSS
Examine all notification types (sync status, sharing alerts, version updates) for injection points
Review other Nextcloud clients (mobile, web) for similar vulnerabilities
Test with SVG payloads, event handlers in HTML attributes, and JavaScript protocol URLs

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1566 Phishing
- T1204 User Execution

## Notes
This is a stored XSS vulnerability where the payload persists on the server as a file name, affecting all clients that sync with that server. The impact is somewhat limited by the fact that the vulnerability exists in a desktop application rather than a web context, but could still lead to credential theft, local file access, or privilege escalation depending on the desktop client's permissions and sandboxing. The vulnerability demonstrates the importance of treating all external data (including from trusted servers) as untrusted until validated and sanitized.

## Full report
<details><summary>Expand</summary>

## Summary:
The `Nextcloud Desktop Client` application does not properly neutralize the names of files before using them.

## Steps To Reproduce:

### Server Machine
1. Install the `Nextcloud Server` application
2. Log into your account

### Client Machine
3. Install the `Nextcloud Desktop Client` application onto a machine that is running the `Windows 10` operating system
4. Log into your account

### Server Machine
5. Upload any file to your `Nextcloud Server` instance
6. Rename the file that you uploaded to `<h1><b><i><u>MikeIsAStar`

### Client Machine
7. Wait until a notification appears exclaiming that some files could not synchronized
8. Open the main dialog window of the `Nextcloud Desktop Client` application
9. Observe that the name of the file that you uploaded is treated as `HyperText Markup Language`

## Supporting Material/References:
{F1864812}

## Impact

An attacker can inject arbitrary `HyperText Markup Language` into the `Nextcloud Desktop Client` application.

</details>

---
*Analysed by Claude on 2026-05-12*
