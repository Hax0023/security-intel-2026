# Reflected XSS in MTN Benin Messages Feature

## Metadata
- **Source:** HackerOne
- **Report:** 1779447 | https://hackerone.com/reports/1779447
- **Submitted:** 2022-11-20
- **Reporter:** vidaamuyarchi
- **Program:** MTN Benin
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Messages feature of mtn.bj where user-supplied input is reflected back without proper sanitization. An attacker can craft a malicious URL containing JavaScript payload that executes in the victim's browser when clicked.

## Attack scenario
1. Attacker identifies the Messages feature on mtn.bj accepts unsanitized user input
2. Attacker crafts a malicious payload using HTML event handlers (e.g., onauxclick) combined with JavaScript functions
3. Attacker sends a phishing link containing the XSS payload to the target user via email, SMS, or social media
4. Victim clicks the link and is redirected to the vulnerable page with the payload in the request
5. Browser executes the injected JavaScript in the context of mtn.bj domain
6. Attacker can steal session cookies, harvest credentials, or perform actions on behalf of the victim

## Root cause
The application fails to properly encode, escape, or validate user input before reflecting it in the HTTP response. Input validation and output encoding mechanisms are either absent or insufficient.

## Attacker mindset
An opportunistic attacker targeting MTN Benin customers would recognize this as a low-complexity way to steal authentication tokens or redirect users to phishing pages. The Messages feature is a high-value target due to user trust and potential for credential harvesting.

## Defensive takeaways
- Implement strict input validation using allowlists for expected data formats
- Apply proper output encoding/escaping based on context (HTML entity encoding, JavaScript escaping, URL encoding)
- Deploy Content Security Policy (CSP) headers to restrict script execution
- Use security frameworks and libraries that provide automatic XSS protection
- Perform server-side validation and sanitization of all user inputs
- Implement HTTPOnly and Secure flags on session cookies to prevent exfiltration
- Conduct regular security testing including automated SAST/DAST scanning
- Apply Web Application Firewall (WAF) rules to detect and block common XSS patterns

## Variant hunting
Hunt for similar reflection points in other features (Notes, Comments, Search functions, User profiles, Contact forms). Check for DOM-based XSS in client-side JavaScript that processes user input. Test event handler attributes (onclick, onmouseover, onauxclick, onload) and JavaScript protocol handlers (javascript:). Look for double-encoded or bypass variations of payloads in other input fields.

## MITRE ATT&CK
- T1190
- T1566
- T1583
- T1598

## Notes
The writeup lacks detail on the exact vulnerable parameter and endpoint. The onauxclick handler suggests right-click context event exploitation. The lack of complexity in the payload (basic confirm() function) indicates minimal WAF/filtering in place. This appears to be a basic reflected XSS with no apparent CSRF token validation or input sanitization. The vulnerability likely affects all users accessing the Messages feature.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi, Team I'm Found Reflected XSS

## Steps To Reproduce:

1.Nave to https://www.mtn.bj/
2.Go to Messages 
3. Enter XSS Payload :

    * <h1 onauxclick=confirm(document.domain)>RIGHT CLICK HERE

4. Reflected the popup

## Impact

Cross site scripting attacks can have devastating consequences. Code injected into a vulnerable application can exfiltrate data or install malware on the user's machine. Attackers can masquerade as authorized users via session cookies, allowing them to perform any action allowed by the user account.

</details>

---
*Analysed by Claude on 2026-05-12*
