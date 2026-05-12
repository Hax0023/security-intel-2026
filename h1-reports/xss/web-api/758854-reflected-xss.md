# Reflected XSS in Embedded Auth Redirect Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 758854 | https://hackerone.com/reports/758854
- **Submitted:** 2019-12-15
- **Reporter:** 0xelkomy
- **Program:** Unknown (Redacted HackerOne Report #758854)
- **Bounty:** Undisclosed
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Unsafe URL Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the embeddedAuthRedirect.html endpoint where the 'auth' parameter is not properly sanitized, allowing attackers to inject arbitrary JavaScript code. An attacker can craft malicious URLs to execute code in a victim's browser context, potentially stealing session tokens, credentials, or performing actions on behalf of the user.

## Attack scenario
1. Attacker identifies that the 'auth' parameter in embeddedAuthRedirect.html accepts JavaScript protocol handlers without validation
2. Attacker crafts a malicious URL with payload: https://target.com/en/embeddedAuthRedirect.html?auth=javascript:alert('xss') or more dangerous payloads like fetch() to exfiltrate cookies
3. Attacker sends the URL to victims via phishing email, chat, or social media, disguising it as a legitimate redirect link
4. Victim clicks the link while authenticated to the target application
5. JavaScript payload executes in victim's browser with their authentication context and privileges
6. Attacker can steal session cookies, perform unauthorized actions, or redirect to phishing page

## Root cause
The application fails to validate, sanitize, or encode the 'auth' parameter before processing it as a redirect target. The code likely uses unsafe methods like direct window.location assignment or unvalidated eval-like operations without checking for javascript: protocol or other dangerous schemes.

## Attacker mindset
Low-skill attacker demonstrates basic XSS exploitation with an alert() proof-of-concept. However, this same vulnerability could be leveraged by sophisticated attackers for session hijacking, credential harvesting, malware distribution, or account takeover through stored interactions.

## Defensive takeaways
- Implement strict input validation: whitelist allowed URLs and reject javascript:, data:, and vbscript: protocols
- Use URL parsing libraries to validate redirect targets belong to trusted domains only
- Encode all user-controlled output based on context (HTML, JavaScript, URL encoding)
- Implement Content Security Policy (CSP) headers with script-src 'self' to mitigate XSS impact
- Never pass user input directly to window.location or eval-like functions
- Use security headers like X-Content-Type-Options: nosniff, X-Frame-Options: DENY
- Implement output encoding libraries (OWASP ESAPI) instead of manual sanitization
- Add security testing to CI/CD pipeline for reflected XSS detection

## Variant hunting
Search for similar vulnerable patterns: other endpoints with redirect/auth parameters, embedded iframes with untrusted src attributes, dynamically constructed script tags, event handler attributes (onclick, onerror) accepting user input, data binding in template engines without sanitization, old legacy pages still using document.write() with user input

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1598 Phishing
- T1566 Phishing
- T1539 Steal Web Session Cookie
- T1187 Forced Authentication

## Notes
The writeup demonstrates basic exploitation skills but lacks sophistication. The actual impact could be severe depending on application context (financial institution, SaaS platform, etc.). The 'embeddedAuthRedirect' endpoint name suggests this is part of authentication/SSO flow, making it particularly dangerous. Lack of HTTPS enforcement details and security header information in the report suggests broader security posture issues.

## Full report
<details><summary>Expand</summary>

>>hello security team i found reflected XSS in this subdomain https://███

POC:-
1-go in subdomain
2-go here 
https://███████/en/embeddedAuthRedirect.html?auth=javascript:alert("xElkomy")
3-Done

Image:-
███████
#xElkomy

## Impact

reflected cross-site scripting (XSS) operation with JavaScript, which runs in the client context. i can put malicious code in URL

</details>

---
*Analysed by Claude on 2026-05-12*
