# Reflected XSS on Invalid Path Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 1057419 | https://hackerone.com/reports/1057419
- **Submitted:** 2020-12-12
- **Reporter:** 0x0d0
- **Program:** Department of Defense (DoD) Program
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on the target domain where invalid URL paths are reflected without sanitization in the 404 error response. An attacker can craft a malicious URL containing JavaScript payloads that execute in the victim's browser when they visit the crafted link.

## Attack scenario
1. Attacker identifies that non-existent paths are reflected in 404 error messages without encoding
2. Attacker crafts a malicious URL containing SVG with onload event handler (e.g., http://target/<svg onload=alert('xss')>)
3. Attacker sends the crafted URL to a victim via email, social media, or malicious advertisement
4. Victim clicks the link or is redirected to the malicious URL
5. The browser renders the 404 page with the unencoded payload, executing the JavaScript
6. Attacker's script can steal session cookies, credentials, perform phishing, or conduct further attacks

## Root cause
The application reflects the requested path parameter directly into the HTTP response without proper HTML encoding or sanitization. The 404 error message handler concatenates user-controlled input (the invalid path) into the response body without applying output encoding functions.

## Attacker mindset
An attacker would view this as a simple but effective vector for social engineering attacks. By crafting a deceptive short URL or embedding the payload in a trusted-looking link, they can trick users into executing arbitrary JavaScript. The DoD scope indicates this could be leveraged for credential harvesting, data exfiltration, or lateral movement in a government/military context.

## Defensive takeaways
- Always HTML-encode or escape user-controlled input before reflecting it in responses
- Implement a strict Content Security Policy (CSP) to prevent inline script execution
- Use generic error messages that do not reflect user input (e.g., 'The requested page was not found')
- Apply input validation to reject or sanitize paths containing HTML/JavaScript characters
- Implement output encoding libraries/frameworks that automatically escape dangerous characters
- Conduct regular security testing including manual code review and automated scanning for XSS vulnerabilities
- Use templating engines that auto-escape by default

## Variant hunting
Check other error pages (403, 500, 502, etc.) for similar reflection vulnerabilities
Test redirect parameters (?redirect=, ?return=, ?next=) for reflected XSS
Examine search functionality for reflected XSS in 'no results' messages
Test API endpoints that return error messages with user-supplied data
Check for DOM-based XSS in client-side error handling code
Test different payload types (script tags, img onerror, iframe, etc.) on the same parameter

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link (delivery mechanism)
- T1566 - Phishing (delivery mechanism)
- T1059 - Command and Scripting Interpreter

## Notes
The reporter appropriately flagged the DoD scope concern and requested self-closure if out of scope, demonstrating responsible disclosure. The vulnerability is trivially exploitable and requires no authentication. The SVG onload vector bypasses some naive XSS filters that only block <script> tags. This is a classic reflected XSS with straightforward exploitation and high impact potential in a government context.

## Full report
<details><summary>Expand</summary>

## Summary 
Reflected XSS on `█████████` for invalid paths.

## Description
Requesting a non-existent path on `█████`, such as `https://██████████/chron0x` the site responds with `No jsonpage404 is /chron0x versus /chron0x./chron0x does not exist`. As it can be seen, the path is reflected. This can be exploited with an XSS. 

Note: I am reporting this here, since the foorter of `███` states `Official ███ Website. The ████████ is an Equal Opportunity Employer.`, and the █████ underlies the DoD. If this should not belong to the DoD scope I would kindly ask to self close this issue.

## Step-by-step Reproduction Instructions

1. Visit `http://█████████/<svg onload=alert("chron0x")>`


## Mitigation/Remediation Actions
Sanitize the path input or switch to a generic error message.

## Impact

Javascript can be executed to steal data, etc.

</details>

---
*Analysed by Claude on 2026-05-12*
