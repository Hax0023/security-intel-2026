# Reflected XSS in Akamai ARL master-config Interface

## Metadata
- **Source:** HackerOne
- **Report:** 1315907 | https://hackerone.com/reports/1315907
- **Submitted:** 2021-08-22
- **Reporter:** renzi
- **Program:** Akamai
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Akamai ARL (Application Request Loader) master-config endpoint where user-supplied URL parameters are not properly sanitized or encoded before being reflected in HTTP responses. An attacker can craft a malicious URL containing JavaScript payloads that execute in the victim's browser with the context of the vulnerable domain.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the 'where' parameter with SVG/onload event handler
2. Attacker sends phishing email or embeds link on trusted site directing victim to malicious URL
3. Victim clicks link while authenticated to Akamai master-config interface
4. Browser sends request to vulnerable endpoint with XSS payload in query parameter
5. Server reflects unsanitized payload in HTTP response without encoding special characters
6. Victim's browser executes JavaScript payload, potentially stealing session tokens, credentials, or performing unauthorized actions

## Root cause
The application fails to implement proper output encoding/escaping when reflecting user-supplied query parameters from the URL into the HTML response. The endpoint accepts user input in the 'where' parameter and renders it without HTML entity encoding, allowing HTML/JavaScript injection.

## Attacker mindset
An attacker would recognize that URL construction patterns and query parameters are often reflected in responses. By testing common XSS payloads with event handlers (onload, onerror) embedded in SVG or IMG tags, they identified that the application does not sanitize these inputs, allowing arbitrary JavaScript execution in the context of an internal/sensitive domain.

## Defensive takeaways
- Implement consistent output encoding: HTML-encode all user-supplied data before reflecting in HTML context using context-appropriate encoding (HTML entity encoding for HTML context)
- Apply input validation: Whitelist expected parameter formats and reject inputs containing HTML/JavaScript syntax
- Use Content Security Policy (CSP) headers to restrict script execution and mitigate XSS impact
- Implement httpOnly and Secure flags on session cookies to prevent token theft via XSS
- Conduct regular security code reviews focusing on all data reflection points
- Perform automated security testing (SAST/DAST) as part of CI/CD pipeline
- Use templating engines with auto-escaping enabled (e.g., Jinja2, Thymeleaf)
- Apply defense-in-depth: WAF rules, input validation, and output encoding

## Variant hunting
Test other URL parameters in the endpoint for reflection (what, where, place, etc.)
Attempt stored XSS by testing if parameters are logged or stored anywhere
Test different payload encodings (URL encoding, double encoding, Unicode escapes)
Check other Akamai ARL endpoints and configurations for similar patterns
Test DOM-based XSS by examining JavaScript handling of URL parameters
Attempt breaking out of different HTML contexts (attributes, JavaScript blocks)
Test with different SVG event handlers and HTML5 event attributes
Investigate if this affects other master-config or config-related URLs

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Link
- T1566: Phishing
- T1059: Command and Scripting Interpreter

## Notes
This is a straightforward reflected XSS vulnerability on an internal/administrative Akamai interface. The writeup lacks detail on impact and mitigation steps. The URL pattern suggests this is part of Akamai's URL rewriting/configuration system. The vulnerability is easily exploitable and could lead to account compromise if the interface handles sensitive credentials or configurations. The reporter's mitigation section is empty, suggesting limited security guidance provided.

## Full report
<details><summary>Expand</summary>

**Description:**

Hello,
I found a Reflected Cross site Scripting (XSS) Open Akamai ARL on  http://master-config-██████████, With this security flaw is possible executing JS codes...

## References
https://owasp.org/www-community/attacks/xss/
https://community.akamai.com/customers/s/article/WebPerformanceV1V2ARLChangeStartingFebruary282021?language=en_US

## Impact

The attacker can execute JS code.

## System Host(s)
master-config-█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Go to http://master-config-████████/7/0/33/1d/www.citysearch.com/search?what=x&where=place%22%3E%3Csvg+onload=confirm(document.domain)%3E

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
