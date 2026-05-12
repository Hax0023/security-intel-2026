# XSS Vulnerability in Shopify Device Manager Admin Panel

## Metadata
- **Source:** HackerOne
- **Report:** 1121900 | https://hackerone.com/reports/1121900
- **Submitted:** 2021-03-10
- **Reporter:** jaka-tingkir
- **Program:** Shopify
- **Bounty:** Unknown (report appears incomplete)
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS
- **CVEs:** None
- **Category:** web-api

## Summary
An XSS vulnerability was discovered in the Shopify Device Manager admin panel at devicemanager.shopifycloud.com/admin where an attacker's XSS Hunter script was executed on the platform. The vulnerability allows arbitrary JavaScript execution, potentially compromising admin session integrity and sensitive data.

## Attack scenario
1. Attacker crafts a malicious payload containing XSS Hunter script or similar XSS payload
2. Attacker injects the payload into a vulnerable input field or parameter in the Device Manager admin panel
3. The payload is stored or reflected without proper sanitization/encoding
4. Admin user accesses the affected page triggering script execution
5. XSS Hunter notification is triggered, confirming code execution
6. Attacker can now steal admin cookies, session tokens, or perform unauthorized actions

## Root cause
Insufficient input validation and output encoding in the Device Manager admin interface. User-supplied input was not properly sanitized before being rendered in the DOM, allowing script injection.

## Attacker mindset
The attacker demonstrated opportunistic vulnerability discovery, likely using automated XSS scanning tools (XSSHunter) to identify unprotected input vectors. The casual tone suggests script-kiddie behavior rather than sophisticated exploitation.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) headers to restrict inline script execution
- Enforce HTML entity encoding and context-aware output encoding for all user inputs
- Use parameterized DOM APIs (textContent, innerText) instead of innerHTML for dynamic content
- Conduct regular security code reviews focusing on input/output handling
- Implement XSS-specific WAF rules on admin panels
- Apply defense-in-depth: validate on client and server, sanitize libraries (DOMPurify)
- Perform penetration testing specifically targeting admin interfaces

## Variant hunting
Search for similar XSS vulnerabilities in other Shopify cloud services (inventory manager, analytics, settings panels). Test all user input fields in Device Manager for stored/reflected XSS. Check for DOM-based XSS in JavaScript handling of URL parameters.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1056 - Interaction with Keystrokes
- T1539 - Steal Web Session Cookie
- T1185 - Traffic Signaling

## Notes
Report is minimal and lacks technical details (specific payload, affected parameter, proof-of-concept). The casual submission format and incomplete information suggest this may be a low-quality or incomplete report. XSSHunter is a legitimate security tool, indicating the researcher was actively scanning for vulnerabilities. Admin panel XSS is critical due to elevated privileges of admin users.

## Full report
<details><summary>Expand</summary>

I don't know where my xsshunter script is, but my script is enabled on your web.
is on your web
1. https://devicemanager.shopifycloud.com/admin

## Impact

xss is triggered

</details>

---
*Analysed by Claude on 2026-05-12*
