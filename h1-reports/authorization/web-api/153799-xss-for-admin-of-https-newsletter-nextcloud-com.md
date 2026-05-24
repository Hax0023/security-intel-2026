# Stored XSS in Nextcloud Newsletter Admin Panel (phplist 3.2.5)

## Metadata
- **Source:** HackerOne
- **Report:** 153799 | https://hackerone.com/reports/153799
- **Submitted:** 2016-07-25
- **Reporter:** sergeym
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected/stored XSS vulnerability exists in the phplist 3.2.5 instance running on newsletter.nextcloud.com in the template viewing functionality. An attacker can inject malicious JavaScript through the 'id' parameter that executes in the admin's browser context, potentially compromising administrative sessions and account takeover.

## Attack scenario
1. Attacker crafts a malicious URL with JavaScript payload in the 'id' parameter: https://newsletter.nextcloud.com/admin/?page=viewtemplate&id=123"><script>alert(document.domain)</script>
2. Attacker tricks admin user into clicking the malicious link (via phishing, social engineering)
3. Admin clicks link while authenticated to newsletter.nextcloud.com
4. Payload executes in admin's browser with full session privileges
5. Attacker can steal session cookies, CSRF tokens, or perform actions as the admin
6. Attacker gains control of newsletter administration and mailing lists

## Root cause
The 'id' parameter in the viewtemplate page is not properly sanitized or HTML-encoded before being reflected in the response. The application fails to validate numeric input and escape HTML special characters, allowing arbitrary JavaScript injection.

## Attacker mindset
An external attacker discovered a common parameter injection point (id parameter) and tested basic HTML/JavaScript escape sequences to bypass filtering. The simplicity of the payload suggests reconnaissance of phplist version combined with public vulnerability knowledge.

## Defensive takeaways
- Implement strict input validation: whitelist allowed characters for 'id' parameter (numeric only if expected)
- Apply context-appropriate output encoding: use HTML entity encoding for all user-controlled data rendered in HTML context
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Keep phplist and all dependencies updated; version 3.2.5 is outdated
- Implement HTTPOnly and Secure flags on session cookies to prevent XSS-based theft
- Use templating engines with auto-escaping enabled
- Conduct security code review of template rendering logic
- Implement Web Application Firewall (WAF) rules to detect XSS patterns in parameters

## Variant hunting
Test other numeric ID parameters across admin interface for similar XSS (e.g., campaign ID, list ID, subscriber ID)
Check GET/POST parameters for insufficient encoding in template system and message rendering
Investigate stored XSS vectors by injecting payload into template names or content that persists
Test attribute-based XSS: id=123 onload=alert(1) to bypass angle bracket filters
Attempt DOM-based XSS in client-side template processing if JavaScript-heavy admin interface exists
Test different phplist versions (3.2.x series) for similar parameter injection points
Check newsletter preview functionality for XSS in template variables and merge fields

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1566 - Phishing
- T1539 - Steal Web Session Cookie
- T1561 - Disk Wipe

## Notes
This is a classic reflected XSS in a legacy phplist deployment. The vulnerability affects administrative users specifically, making it high impact despite requiring user interaction. The PoC video provides strong evidence of exploitation. Nextcloud should have immediately patched or removed the vulnerable phplist version from newsletter.nextcloud.com.

## Full report
<details><summary>Expand</summary>

a site https://newsletter.nextcloud.com to have phplist 3.2.5

steps to reproduce:

1. to use firefox browser, latest version
2. go to  https://newsletter.nextcloud.com/admin/?page=viewtemplate&id=123%22%3E%3Cscript%3Ealert(document.domain)%3C/script%3E

3. log in as admin
4. alert box with name of domain

please, look at my poc video in attachment (has been installed phplist 3.2.5 on the localhost)



</details>

---
*Analysed by Claude on 2026-05-24*
