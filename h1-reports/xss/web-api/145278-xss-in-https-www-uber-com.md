# Reflected XSS in Uber.com via kxsrc Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 145278 | https://hackerone.com/reports/145278
- **Submitted:** 2016-06-17
- **Reporter:** netfuzzer
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Unsafe Parameter Handling, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Uber.com through the kxsrc query parameter, which is passed to third-party tracking code (Krxd/Krux beacon) without proper sanitization. An attacker can craft a malicious URL containing JavaScript payload in the callback parameter that executes in the victim's browser when the page loads.

## Attack scenario
1. Attacker identifies that the kxsrc parameter controls the Krux tracking beacon URL and callback function
2. Attacker crafts a malicious URL with JavaScript payload in the callback parameter: ?kxsrc=https://beacon.krxd.net/optout_check?callback=alert(/XSSED/.source)
3. Attacker sends the malicious URL to victim via phishing email, social engineering, or malicious advertisement
4. Victim visits the crafted URL on Uber.com
5. Browser loads the page and the kxsrc parameter value is processed without sanitization
6. JavaScript payload executes in victim's browser with full access to Uber.com cookies, session tokens, and sensitive data

## Root cause
The application fails to sanitize or validate the kxsrc query parameter before passing it to third-party tracking code. The parameter value is reflected in the DOM and processed as a URL without encoding special characters or validating callback function names. Third-party integrations (Krux beacon) are not properly isolated or sandboxed.

## Attacker mindset
Opportunistic researcher discovering parameter pollution and third-party integration weaknesses. The duplicate reporting suggests awareness of similar vulnerabilities and systematic testing of query parameters. The casual tone and mention of bounty eligibility indicates beginner-to-intermediate skill level.

## Defensive takeaways
- Implement strict input validation and whitelisting for all query parameters, especially those used in third-party integrations
- Encode all user-controlled data before reflecting it in HTML, JavaScript, or URL contexts using context-appropriate encoding
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Sandbox third-party tracking code in iframes with restricted permissions (allow-scripts only)
- Implement URL validation to ensure parameters reference expected domains only
- Apply X-XSS-Protection and X-Content-Type-Options security headers
- Conduct security code review specifically targeting third-party integrations and external parameter handling
- Use automated scanning and SAST tools to detect reflected XSS patterns during development

## Variant hunting
Test other tracking/analytics parameters (utm_*, ga_*, fbclid, etc.) for similar XSS vulnerabilities
Try alternative encoding schemes (hex, unicode, HTML entities) in callback parameter
Test for stored XSS if kxsrc parameter values are saved in user preferences or profiles
Check for Server-Side Template Injection if callback processing occurs server-side
Investigate other third-party integration parameters across Uber subdomains and properties
Test DOM-based XSS by checking if kxsrc is processed by client-side JavaScript frameworks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598 - Phishing for Information
- T1539 - Steal Web Session Cookie
- T1056.004 - Interaction Data Capture

## Notes
Report appears to be a duplicate of #145276, reducing its value. The vulnerability leverages third-party Krux (Krxd) beacon integration, a common tracking service. The proof-of-concept uses alert() to demonstrate code execution. Reporter's uncertainty about bounty eligibility and casual approach suggests possible first-time reporter. The vulnerability represents a common pattern of unsafe parameter passing to third-party code without proper isolation or validation.

## Full report
<details><summary>Expand</summary>

Hey,

this vulnerability is essentially the same as bug 145276, i'm reporting it again just in case.

there's a cross site scripting vulnerability in https://www.uber.com/.

steps to reproduce:

1.visit https://www.uber.com/?kxsrc=https%3A//beacon.krxd.net/optout_check%3Fcallback%3Dalert%28/XSSED/.source%29
2. wait until the page finishes loading
3.see the xss alert.

wonder it would be eligible for a bounty?

Cheers,
Mario

</details>

---
*Analysed by Claude on 2026-05-12*
