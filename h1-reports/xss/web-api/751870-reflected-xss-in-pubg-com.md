# Reflected XSS in pubg.com via 'p' Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 751870 | https://hackerone.com/reports/751870
- **Submitted:** 2019-12-05
- **Reporter:** 0xfabiof
- **Program:** PUBG
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
PUBG's main website contains a reflected XSS vulnerability in the 'p' GET parameter that fails to properly sanitize or escape user input. An attacker can inject malicious JavaScript code that executes in the victim's browser when they visit a crafted link. This allows arbitrary JavaScript execution with access to user cookies and session data.

## Attack scenario
1. Attacker identifies the 'p' parameter on pubg.com is vulnerable to XSS injection
2. Attacker crafts a JavaScript payload (e.g., alert(document.cookie)) and encodes it for URL injection
3. Attacker constructs a malicious URL: /?p=iqz78'%3e%3cimg%20src%3da%20onerror%3dalert(document.cookie)%3d1%3echplq
4. Attacker sends the crafted link to a victim via phishing, social engineering, or malicious redirect
5. Victim clicks the link while authenticated to pubg.com
6. JavaScript payload executes in victim's browser context, stealing cookies, session tokens, or performing unauthorized actions

## Root cause
The 'p' GET parameter is reflected in the HTTP response without proper input validation, sanitization, or output encoding. The application fails to escape HTML special characters and does not implement Content Security Policy (CSP) headers to prevent inline script execution.

## Attacker mindset
An attacker seeks to exploit the lack of input validation in a high-traffic gaming website to steal user authentication tokens, perform account takeover, redirect users to malicious sites, or distribute malware to PUBG's user base.

## Defensive takeaways
- Implement strict input validation: reject or sanitize unexpected characters in all GET parameters
- Apply context-appropriate output encoding: HTML-encode all user-controlled data reflected in responses
- Implement Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Use HTTP-only and Secure flags on cookies to prevent JavaScript access
- Deploy a Web Application Firewall (WAF) with XSS detection rules
- Conduct regular security testing including SAST/DAST to identify injection points
- Implement subresource integrity (SRI) and X-XSS-Protection headers as defense-in-depth
- Educate developers on secure coding practices for web applications

## Variant hunting
Test all GET/POST parameters for XSS injection (p, id, page, ref, redirect, etc.)
Check for DOM-based XSS in JavaScript handling of query parameters
Test for stored XSS if the 'p' parameter is cached or stored anywhere
Attempt encoding bypasses: double encoding, UTF-8 encoding, Unicode escapes, HTML entities
Test filter bypass techniques: event handlers (onclick, onload, onmouseover), different tags (svg, iframe, object)
Check for XSS in error messages or 404 pages that reflect the parameter
Identify other endpoints with similar parameter handling vulnerabilities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598.003 - Phishing: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link
- T1204.001 - User Execution: Malicious Link

## Notes
This is a straightforward reflected XSS vulnerability requiring user interaction. The impact is limited to session-based attacks and information disclosure visible to the authenticated user. The PoC uses an img tag with onerror handler to bypass potential script tag filters. Report lacks specific bounty amount and patching timeline information.

## Full report
<details><summary>Expand</summary>

## Summary:

PUBG's main website https://www.pubg.com has an endpoint that is vulnerable to an injection vulnerability - namely a reflected injection of JavaScript, also known as Reflected Cross Site Scripting (XSS). As per OWASP's definition: "Cross-Site Scripting (XSS) attacks are a type of injection, in which malicious scripts are injected into otherwise benign and trusted websites. "
This happens because one of the GET parameters "p" does not properly sanitize/escape user input, allowing an injection to occur.

## Steps To Reproduce:

To reproduce this, an attacker has to:

  * Prepare a Javascript payload that it wants the victim to execute. In this case, for Proof of Concept purposes, our Javascript code will prompt an alert showing the users' cookies.

```javascript
alert(document.cookie);
```

  * Inject this Javascript code properly into the vulnerable parameter, creating thus a crafted future GET request that will inject the payload.

```GETRequest
GET /?p=iqz78'%3e%3cimg%20src%3da%20onerror%3dalert(document.cookie)%3d1%3echplq HTTP/1.1
Host: www.pubg.com
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Referer: https://www.pubg.com/es/feed/
Cookie: _icl_current_language=en; _icl_visitor_lang_js=en-us; wpml_browser_redirect_test=0; __cfduid=de74423d435717d651b1c9e2c63f4acc21575460678
```
Request PoC {F651167}


  * As this injection happens in a GET parameter, the attacker simply needs to send the crafted Link that produces this GET request to the victim and have the victim click it.

Injection Demonstration {F651168}



## Supporting Material/References:

  * Video Demonstration

{F651177}

## Impact

With user interaction, an attacker could execute arbitrary Javascript code in a victim's browser.
This would allow an attacker to unwillingly make a victim:

* Perform any action in the identified endpoint
* View any information that the user is able to view
* Modify any information that the user is able to modify (not sure if applicable in this case)
* Interact with other application users as if it were him - impersonation (not sure if applicable in this case)

</details>

---
*Analysed by Claude on 2026-05-12*
