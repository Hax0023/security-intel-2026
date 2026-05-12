# Reflected XSS on www.grouplogic.com/files/glidownload/verify.asp

## Metadata
- **Source:** HackerOne
- **Report:** 859395 | https://hackerone.com/reports/859395
- **Submitted:** 2020-04-25
- **Reporter:** ali
- **Program:** Acronis (Group Logic subsidiary)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in the verify.asp endpoint where the 'version' parameter is not properly sanitized or encoded before being reflected in the HTML response. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when visited.

## Attack scenario
1. Attacker crafts malicious URL with XSS payload in the version parameter: http://www.grouplogic.com/files/glidownload/verify.asp?version=AC12'><img src=v onerror=alert(document.domain)>
2. Attacker distributes the crafted URL via phishing email, social engineering, or forum posts targeting Group Logic users
3. Victim clicks the malicious link while authenticated or visiting the site
4. Browser loads verify.asp and reflects the unencoded payload directly into the HTML response
5. The img tag with onerror handler executes JavaScript in the context of www.grouplogic.com
6. Attacker can steal session cookies, perform actions on behalf of the user, or redirect to malicious sites

## Root cause
The verify.asp endpoint accepts user input via the 'version' query parameter and directly reflects it in the HTML response without proper output encoding or input validation. The application fails to HTML-encode special characters that could break out of existing HTML context.

## Attacker mindset
Reconnaissance of third-party/subsidiary domains for quick wins; testing common parameter names (version, id, file, etc.) on legacy ASP applications; leveraging the corporate relationship between Acronis and Group Logic to find less-hardened targets.

## Defensive takeaways
- Implement context-appropriate output encoding for all user-controlled data (HTML encoding for HTML context, JavaScript encoding for JS context)
- Use a security-focused templating engine that auto-escapes by default
- Apply input validation to reject unexpected characters in the version parameter
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Conduct security audits of legacy ASP applications and subsidiary/managed domains
- Use a Web Application Firewall (WAF) with XSS detection rules
- Perform security testing on all first-party and third-party managed domains

## Variant hunting
Test other parameters in verify.asp (file, id, name, path, download, etc.) for similar XSS
Enumerate other endpoints in /files/glidownload/ directory for parameter-based XSS
Check other Acronis-managed domains for similar vulnerable ASP endpoints
Test for stored XSS if user input is persisted in any database or logs
Look for DOM-based XSS variants in client-side JavaScript handling of these parameters
Test filter bypass techniques (case variations, encoding schemes, event handler variations)

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1204.001

## Notes
Legacy ASP applications are common targets for XSS due to older frameworks lacking modern auto-escaping features. The simplicity of the PoC (basic img onerror) suggests minimal or no input filtering was in place. The vulnerability chain includes social engineering (T1566/T1598) to deliver the malicious link, making it a practical attack vector against end users.

## Full report
<details><summary>Expand</summary>

Hello there,
I hope you are well!

As I see, Group Logic is your subsidary and www.grouplogic.com is a managed website by Acronis.
{F803772}

I found a reflected xss on http://www.grouplogic.com/
PoC: http://www.grouplogic.com/files/glidownload/verify.asp?version=AC12%27%3E%3Cimg%20src=v%20onerror=alert(document.domain)%3E

## Impact

Reflected XSS

Best Regards,
@mygf

</details>

---
*Analysed by Claude on 2026-05-12*
