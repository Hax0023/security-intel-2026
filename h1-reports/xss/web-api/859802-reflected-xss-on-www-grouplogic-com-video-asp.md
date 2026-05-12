# Reflected XSS on www.grouplogic.com/video.asp

## Metadata
- **Source:** HackerOne
- **Report:** 859802 | https://hackerone.com/reports/859802
- **Submitted:** 2020-04-26
- **Reporter:** ali
- **Program:** GroupLogic
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS)
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the video.asp parameter 'v' where user input is not properly sanitized before being reflected in the response. An attacker can inject arbitrary JavaScript code through the 'v' parameter to execute malicious scripts in a victim's browser and steal sensitive data like cookies.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'v' parameter: video.asp?v=Acroxx1%22%3C/script%3E%3Cscript%3Ealert(document.cookie)%3C/script%3Es_aE
2. Attacker distributes the URL via phishing email, social engineering, or malicious website to target users
3. Victim clicks the link while authenticated to www.grouplogic.com
4. The malicious URL is processed by the server and reflected in the HTML response without sanitization
5. Victim's browser parses and executes the injected JavaScript code
6. Attacker's script accesses and exfiltrates the victim's session cookies or other sensitive data

## Root cause
The video.asp endpoint fails to properly validate, encode, or sanitize the 'v' parameter before reflecting it in the HTTP response. The application trusts user-supplied input and includes it directly in the HTML output without context-aware encoding.

## Attacker mindset
An opportunistic attacker recognizing low-hanging fruit in poorly secured legacy applications. The simplicity of the PoC suggests this was discovered through basic parameter fuzzing or automated scanning. The attacker likely seeks to steal session credentials or perform account takeover attacks.

## Defensive takeaways
- Implement input validation: whitelist allowed characters and reject unexpected input patterns
- Apply context-aware output encoding: HTML-encode all user-controlled data before reflection in HTML context
- Use a Web Application Firewall (WAF) to detect and block common XSS patterns
- Implement Content Security Policy (CSP) headers to restrict script execution
- Use security frameworks/libraries that provide automatic XSS protection
- Conduct security code reviews focusing on parameter handling and data flow
- Regular penetration testing and vulnerability scanning of web applications
- Mark cookies with HttpOnly and Secure flags to limit JavaScript access

## Variant hunting
Test other parameters on video.asp (e, width, height) for similar XSS vulnerabilities
Search for other .asp endpoints with similar parameter reflection patterns
Attempt DOM-based XSS vectors through JavaScript event handlers (onload, onerror)
Test for stored XSS if video data is saved and displayed to other users
Enumerate other legacy pages on grouplogic.com domain for similar weaknesses
Test for filter bypass techniques: double encoding, case variation, alternative tags
Check if CORS misconfiguration allows cross-origin script execution

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539

## Notes
This is a straightforward reflected XSS in a legacy ASP application. The PoC demonstrates successful script injection via query parameter manipulation. The vulnerability appears in an old technology stack (ASP, not ASP.NET), suggesting potentially outdated security practices. No patching timeline or resolution status provided in the report excerpt.

## Full report
<details><summary>Expand</summary>

Hello there,
I hope you are well!

PoC:
http://www.grouplogic.com/video.asp?v=Acroxx1%22%3C/script%3E%3Cscript%3Ealert(document.cookie)%3C/script%3Es_aE&e=mp4&width=560&height=315

## Impact

Stealing cookies

Best Regards,
@mygf

</details>

---
*Analysed by Claude on 2026-05-12*
