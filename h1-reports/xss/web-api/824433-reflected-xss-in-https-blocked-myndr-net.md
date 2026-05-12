# Reflected XSS in https://blocked.myndr.net via trg Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 824433 | https://hackerone.com/reports/824433
- **Submitted:** 2020-03-19
- **Reporter:** thilakesh
- **Program:** Myndr (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the blocked.myndr.net domain via the 'trg' query parameter, allowing attackers to inject arbitrary JavaScript code. The vulnerability occurs because user input is not properly sanitized or encoded before being rendered in the HTML response.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the trg parameter: https://blocked.myndr.net/?trg=><script>alert(document.cookie)</script>
2. Attacker sends the link to victims via phishing email, social media, or other social engineering channels
3. Victim clicks the link while authenticated to the application
4. The injected JavaScript executes in the victim's browser within the context of blocked.myndr.net domain
5. Attacker's script can steal session cookies, tokens, or sensitive data from the page
6. Attacker can redirect victim to malicious site, perform actions on behalf of user, or distribute malware

## Root cause
The application fails to properly validate and encode the 'trg' parameter before outputting it in the HTML response. No Content Security Policy (CSP) or output encoding mechanisms are implemented to prevent script injection.

## Attacker mindset
The attacker exploits trust in the legitimate domain to deliver malicious payloads. By targeting a blocked/filtering domain, the attacker may bypass user security expectations and exploit the false sense of security users have with authenticated sessions.

## Defensive takeaways
- Implement strict input validation for all query parameters using allowlist approach
- Apply proper output encoding (HTML entity encoding) to all user-controlled data before rendering
- Deploy Content Security Policy (CSP) headers to restrict script execution sources
- Use security-focused template engines that auto-escape by default
- Implement HTTP-only and Secure flags on sensitive cookies
- Conduct regular security testing including automated XSS scanning
- Apply principle of least privilege to DOM manipulation
- Use security headers like X-XSS-Protection and X-Content-Type-Options

## Variant hunting
Test other query parameters (id, user, ref, page, search, etc.) for similar XSS
Attempt DOM-based XSS variations using different JavaScript contexts
Test POST parameters with same payloads for reflected XSS in forms
Check subdomains (*.myndr.net) for similar parameter handling issues
Try event handlers: " onload="alert(1)", " onerror="alert(1)
Test URL encoding bypasses and HTML entity variations
Probe for Stored XSS if parameter values are persisted anywhere

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1608.005

## Notes
This is a straightforward reflected XSS with clear reproduction steps. The vulnerability is in a security/blocking domain which increases impact potential. The reporter's impact assessment is accurate but could be enhanced with proof of cookie/token theft. The 'trg' parameter name suggests target redirection functionality, which is a common XSS vector point.

## Full report
<details><summary>Expand</summary>

##Summary:
Reflected XSS in Domain (https://blocked.myndr.net)

## Steps To Reproduce:
1. Go to the https://blocked.myndr.net.
2. Find the endpoint in the domain -https://blocked.myndr.net/?trg=1
3. Add the payload ?trg="><script>alert(1)</script>
4. You can see the pop up in your browser.

## Impact

With the help of XSS, a hacker or attacker can perform social engineering on users by redirecting them from real websites to fake ones. the hacker can steal their cookies and download malware on their system, and there are many more attacking scenarios a skilled attacker can perform with XSS.

</details>

---
*Analysed by Claude on 2026-05-12*
