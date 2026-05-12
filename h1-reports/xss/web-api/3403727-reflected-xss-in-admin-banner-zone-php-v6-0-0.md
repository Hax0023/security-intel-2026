# Reflected XSS in /admin/banner-zone.php Search Filter

## Metadata
- **Source:** HackerOne
- **Report:** 3403727 | https://hackerone.com/reports/3403727
- **Submitted:** 2025-10-29
- **Reporter:** vidang04
- **Program:** Unknown (HackerOne Report #3403727)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Inadequate Output Encoding
- **CVEs:** CVE-2025-55124
- **Category:** web-api

## Summary
A Reflected XSS vulnerability exists in the banner zone admin interface where user input from the 'Website' search field is reflected without proper HTML encoding. An attacker can craft a malicious URL containing JavaScript payload that executes when an admin visits the link, potentially leading to session hijacking or unauthorized administrative actions.

## Attack scenario
1. Attacker identifies the /admin/banner-zone.php endpoint accepts a 'Website' search parameter
2. Attacker crafts malicious URL with JavaScript payload: /admin/banner-zone.php?search=><script>alert(1)</script>
3. Attacker sends crafted URL to administrator via email or social engineering
4. Administrator clicks the link while logged into the admin panel
5. JavaScript payload executes in administrator's browser context with full session privileges
6. Attacker steals session cookies, performs unauthorized actions, or harvests credentials

## Root cause
User-supplied input from the 'Website' search field in the banner zone functionality is directly reflected into the HTML response without context-aware encoding or sanitization. The application fails to apply proper output encoding (HTML entity encoding) when displaying search parameters back to the user.

## Attacker mindset
An attacker with knowledge of the admin interface structure exploits the common oversight of encoding reflected parameters. By targeting administrators (higher privilege users), the attacker maximizes impact potential. The use of simple payload demonstrates the vulnerability's ease of exploitation, suggesting the attacker is opportunistically reporting or testing.

## Defensive takeaways
- Implement context-aware output encoding for all user-supplied data reflected in HTML responses (use HTML entity encoding, not just text encoding)
- Apply Content Security Policy (CSP) headers to prevent inline script execution
- Use templating engines with auto-escaping enabled by default
- Implement input validation to reject or sanitize suspicious characters in search parameters
- Set HttpOnly and Secure flags on session cookies to prevent JavaScript access
- Conduct security code review focusing on all search/filter functionality across admin interfaces
- Deploy Web Application Firewall (WAF) rules to detect and block common XSS patterns
- Implement comprehensive security testing in CI/CD pipeline for XSS vulnerabilities

## Variant hunting
Search for other admin search/filter fields that may reflect user input without encoding (e.g., /admin/banner.php, /admin/zones.php)
Test various banner-related endpoints for reflected XSS in different parameters
Check if the vulnerability exists in stored banner searches or saved filter functionality (stored XSS variant)
Test other input fields in admin panel that may have similar encoding gaps
Verify if DOM-based XSS exists in client-side search functionality
Check for XSS in export/download features that may preserve unencoded input
Test for bypasses using alternative encoding (Unicode, URL encoding, case variation)

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539
- T1078

## Notes
This vulnerability specifically affects v6.0.0+ of the application. The attack targets administrative interfaces, making it particularly dangerous. The proof-of-concept uses a simple alert() demonstrating clear execution capability. Reported on HackerOne but bounty amount not disclosed in provided content. The vulnerability is straightforward to exploit and verify, likely qualifying for a moderate-to-high severity rating depending on the application's security posture regarding admin session protection.

## Full report
<details><summary>Expand</summary>

##Description:
A Reflected Cross-Site Scripting (Reflected XSS) vulnerability. User-supplied input from the banner search fields ("Website") is reflected into the page without proper context-aware encoding

##Step:
1. When I create Banners, I click it and click 'Linked Zones'. At that, I insert payload '><script>alert()</script> into 'website' field to search

{F4944389}

2. As a result, the alert statement is executed on the browser.

{F4944394}

## Impact

The reflected XSS (demonstrated by "><script>alert(1)</script>) allows execution of attacker-supplied JavaScript in an admin’s browser. This can lead to session theft (if cookies are not HttpOnly), unauthorized admin actions, credential harvesting, and potential full site compromise

</details>

---
*Analysed by Claude on 2026-05-12*
