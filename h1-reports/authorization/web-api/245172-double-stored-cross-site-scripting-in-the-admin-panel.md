# Double Stored Cross-Site Scripting in Admin Panel Custom Domain Fields

## Metadata
- **Source:** HackerOne
- **Report:** 245172 | https://hackerone.com/reports/245172
- **Submitted:** 2017-07-01
- **Reporter:** sp1d3rs
- **Program:** Federalist
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Stored XSS, Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
Two stored XSS vulnerabilities were discovered in the Custom Domain and Demo Domain fields of the Federalist admin panel settings page. Attackers with admin access could inject malicious JavaScript payloads (e.g., javascript:alert()) that execute when other admins interact with the 'View Website' button or visit the published sites page.

## Attack scenario
1. Attacker with admin credentials logs into Federalist and navigates to a site's settings page (/sites/<siteid>/settings)
2. Attacker enters a JavaScript payload like 'javascript:alert(document.domain)' in the Custom Domain field and a variation like 'javascript:alert(document.domain);' in the Demo Domain field to bypass equality checks
3. Attacker saves the settings; the malicious payloads are stored in the database without sanitization
4. Another admin views the same site settings or clicks the 'View Website' button, triggering the stored XSS payload
5. The JavaScript executes in the admin's browser with their privileges, potentially allowing session hijacking, credential theft, or further admin panel compromise
6. Attacker can also trigger the XSS by having admins visit the published sites page (/sites/<siteid>/published)

## Root cause
Input validation and output encoding were insufficiently implemented. The Custom Domain and Demo Domain fields accepted and stored JavaScript protocol handlers without sanitization. The fields should restrict input to alphanumeric characters and dots only, and output should be properly encoded when rendered in HTML contexts.

## Attacker mindset
An insider or compromised admin account holder seeks to escalate impact by compromising other administrators through persistent XSS attacks. The attacker exploits the trust relationship between admins and bypasses simplistic duplicate-value checks by adding minor variations (semicolons) to payloads.

## Defensive takeaways
- Implement strict whitelist-based input validation: only allow alphanumeric characters, hyphens, and dots for domain fields
- Apply output encoding/escaping appropriate to the context (HTML entity encoding when rendering in HTML)
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Reject or sanitize any input containing protocol handlers (javascript:, data:, etc.)
- Implement server-side validation, not just client-side checks
- Consider using templating engines with auto-escaping enabled
- Apply the principle of least privilege; restrict who can modify domain settings
- Conduct security code review of all user input handling in admin panels

## Variant hunting
Check other domain/URL input fields in the application for similar validation bypass
Test other admin panel fields for stored XSS (site name, descriptions, metadata fields)
Attempt similar payload variations with data: URIs, vbscript:, or event handlers
Check if the vulnerability exists in user-facing inputs that admins control (page templates, content fields)
Test for mutation-based XSS bypass techniques
Investigate whether the semicolon bypass works in other equality checks throughout the application

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The vulnerability requires admin-level access to exploit, limiting the attack surface but still critical for insider threats or account compromise scenarios. The two-field bypass (using semicolon differentiation) demonstrates weak validation logic that checks for duplicate values rather than validating format. This is a classic case of security through obscurity rather than proper input validation.

## Full report
<details><summary>Expand</summary>

##Description
Hello. I discovered a Stored XSS attack vector in the `Custom Domain` field

##POC & Reproduction steps
1. Login to the federalist and go to the some instance `http://localhost:1337/sites/<siteid>/settings`
2. Fill the `Custom Domain` field by the
```
javascript:alert(document.domain)
```
and `Demo domain`
```
javascript:alert(document.domain);
```
(it cannot be the same so we bypass the check by adding `;`)

3. Save and press `View Website` button. You will be XSSed.
{F199337}
{F199336}
4) Go to the `http://localhost:1337/sites/<siteid>/published` - and press view on the demo site to test second Stored XSS
{F199338}

##The impact
The XSS requires user interaction (e.g. clicking the button). But still, it is a bad thing. Anyone who gain access here, can conduct stored XSS attack against other admins.

##The root cause & suggested fix
The input fields not sanitized properly - it should allow only alphanumeric characters, and dots.


</details>

---
*Analysed by Claude on 2026-05-24*
