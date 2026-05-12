# Stored XSS in WordPress.com Custom Style Section

## Metadata
- **Source:** HackerOne
- **Report:** 1054526 | https://hackerone.com/reports/1054526
- **Submitted:** 2020-12-09
- **Reporter:** ucuping
- **Program:** WordPress.com
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in the Custom Style section of WordPress.com's Polling feature where user-supplied style names are not properly sanitized or encoded before being stored and displayed. An attacker can inject malicious JavaScript payloads that execute in the context of any user who interacts with the compromised style, enabling session hijacking, unauthorized actions, and phishing attacks.

## Attack scenario
1. Attacker creates or edits a post in the Polling section and accesses the Custom Style feature
2. Attacker creates a new style with an innocuous name, then modifies the style name to inject a malicious payload: <noscript><p title="</noscript><img src=x onerror=alert(document.cookie)>
3. Attacker saves the style with the payload, which is stored in the database without proper sanitization
4. Attacker invites a victim to join the WordPress.com site/project with appropriate permissions (Manager or Administrator)
5. Victim accepts the invitation and navigates to the Polling section to create or edit a post
6. Victim clicks on Custom Styles or interacts with the stored malicious style, triggering the XSS payload execution and allowing the attacker to steal cookies or perform unauthorized actions

## Root cause
The Custom Style feature fails to properly sanitize user input when storing style names and does not apply adequate output encoding when rendering stored style data. The application accepts and stores HTML/JavaScript payloads without validation, and renders them without proper escaping, allowing arbitrary script execution.

## Attacker mindset
An attacker with basic understanding of XSS can exploit this to compromise other users on a shared WordPress.com instance. By leveraging the invitation system, the attacker ensures victims have necessary permissions to access the vulnerable feature. The stored nature of the XSS makes it persistent and affecting multiple users over time, increasing the attack surface and potential impact.

## Defensive takeaways
- Implement strict input validation for all user-supplied data, particularly style names and CSS-related fields
- Apply proper output encoding/escaping based on context (HTML entity encoding for HTML context) when rendering stored data
- Use a Content Security Policy (CSP) to restrict script execution and mitigate XSS impact
- Sanitize user input using well-tested libraries designed for HTML sanitization
- Implement a Web Application Firewall (WAF) to detect and block common XSS payloads
- Perform security code review of all features handling user-generated content, especially styling and metadata fields
- Use templating engines with auto-escaping enabled by default
- Conduct regular penetration testing focusing on stored XSS vulnerabilities across all user input features

## Variant hunting
Check other style-related features (custom fonts, custom colors, custom CSS) for similar XSS vulnerabilities
Test all user input fields in the Polling feature for stored XSS (titles, descriptions, options)
Examine other WordPress.com site customization areas (themes, widgets, custom blocks) for payload injection points
Test metadata fields and administrative labels for stored XSS
Investigate whether similar flaws exist in post metadata, custom fields, or plugin settings
Review all features allowing user-generated content that gets displayed to multiple users

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539

## Notes
The vulnerability report demonstrates a multi-step attack requiring social engineering (inviting victims), suggesting the attacker needs some level of access to the platform. However, the persistent nature of the XSS makes it suitable for targeting specific users or groups. The use of the <noscript> tag as a wrapper suggests an attempt to bypass basic XSS filters that might block img onerror payloads directly.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello Team,
I found the Stored XSS vulnerability in the Custom Style section, this vulnerability can result in an attacker to execute arbitrary JavaScript in the context of the attacked website and the attacked user. This can be abused to steal session cookies, performing requests in the name of the victim or for phishing attacks, by inviting the victim to become part of the manager or administrator.

## Platform(s) Affected:
wordpress.com

## Steps To Reproduce:
1. As an attacker, go to the feedback section, then go to the Polling section.
2. Add a new post or edit an existing post.
3. Scroll down, click All Styles.
4. Add a new Style.
5. Named the temporary style, click Save Style.
6. Change the Style Name with <noscript><p title= "</noscript><img src=x onerror=alert(document.cookie)>">, check the checkbox next to Save Style, click Save Style.
7. Script will be run.
8. Invite the victim in a way, go to manage then users.
9. Click invite, enter username or email, and send.
10. As a Victim, accept the attacker's invitation.
11. Go to the Feedback section.
12. Then go to the Polling section.
13. Add a new post or edit an existing post.
14. Scroll down, click All Styles.
15. Enter the Style that has been created by the previous Attacker.
16. Script will be run.

## Supporting Material/References:
F1109567
F1109568
F1109569

## Impact

this vulnerability can result in an attacker to execute arbitrary JavaScript in the context of the attacked website and the attacked user. This can be abused to steal session cookies, performing requests in the name of the victim or for phishing attacks, by inviting the victim to become part of the manager or administrator.

</details>

---
*Analysed by Claude on 2026-05-12*
