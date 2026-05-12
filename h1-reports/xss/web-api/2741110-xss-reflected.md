# Reflected Cross-Site Scripting (XSS) via Query Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 2741110 | https://hackerone.com/reports/2741110
- **Submitted:** 2024-09-25
- **Reporter:** k0x
- **Program:** Undisclosed
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected XSS, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the tags/image endpoint where user-supplied query parameters (view, sort) are reflected back in the HTTP response without proper sanitization or encoding. An attacker can craft a malicious URL with encoded JavaScript payloads that execute in the victim's browser when the link is visited, potentially leading to session hijacking or credential theft.

## Attack scenario
1. Attacker crafts a malicious URL containing encoded XSS payload in the 'view' parameter with event handlers like OnFocus
2. Attacker distributes the URL via email, social media, or embeds it on a compromised website
3. Victim clicks the malicious link while authenticated to the target application
4. Server reflects the unsanitized query parameter back in the HTML response
5. Victim's browser interprets the reflected payload as legitimate code and executes the JavaScript
6. Attacker's script executes in the context of the victim's session, enabling cookie theft, credential harvesting, or malicious actions on behalf of the victim

## Root cause
The application fails to properly validate and encode user-supplied input from query parameters (specifically 'view' and 'sort') before including them in the HTTP response. The server reflects the raw or inadequately encoded input directly into HTML attributes or content without context-aware output encoding.

## Attacker mindset
An opportunistic attacker leverages the ease of crafting and distributing a malicious link to compromise unsuspecting authenticated users. The use of URL encoding obfuscation suggests an attempt to bypass simple input validation filters. The focus on event handlers (OnFocus) indicates targeting interactive elements to trigger automatic payload execution.

## Defensive takeaways
- Implement context-aware output encoding for all user-supplied data reflected in responses (HTML entity encoding, JavaScript encoding, URL encoding as appropriate)
- Apply strict input validation using allowlists for expected parameter values and formats
- Use Content Security Policy (CSP) headers to restrict script execution and prevent inline script injection
- Employ templating engines with auto-escaping enabled to prevent accidental XSS
- Validate and sanitize all query parameters on the server-side before processing
- Implement security headers such as X-XSS-Protection and X-Content-Type-Options
- Conduct regular security testing including automated XSS scanning and manual penetration testing
- Train developers on secure coding practices and the OWASP Top 10

## Variant hunting
Test other query parameters (sort, filter, page, id, search) for similar reflection issues
Attempt double-encoding bypasses (e.g., %252526 as second-level encoding)
Test for DOM-based XSS in client-side JavaScript handling of URL parameters
Check for XSS in different endpoints with similar parameter structures
Test various event handlers beyond OnFocus (onClick, onLoad, onError, onMouseOver)
Attempt polyglot payloads that work across multiple contexts
Test for mutation-based XSS with browser-specific quirks

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1657

## Notes
The report is heavily redacted with censored domain and product information, limiting detailed analysis. The payload uses multiple encoding layers (%26, %23, %60) suggesting an attempt to evade basic input filters. The specific use of 'AutoFocus' and 'OnFocus' attributes indicates targeting form elements or interactive DOM nodes. The lack of remediation details in the report suggests this may be a template or incomplete submission. Real-world reflected XSS often succeeds due to developers underestimating the importance of output encoding versus input validation alone.

## Full report
<details><summary>Expand</summary>

### **Description**

Reflected Cross-Site Scripting (XSS) occurs when a web application accepts untrusted data in an HTTP request and includes that data in its immediate response without proper sanitization or validation. This vulnerability allows an attacker to inject malicious scripts into web pages viewed by other users. When victims click on a specially crafted link containing the attacker's payload, the server reflects the input back to the user's browser, executing the malicious script within the context of the victim’s session. This can lead to various attacks, such as cookie theft, session hijacking, or phishing.

### **References**

- [OWASP XSS (Cross Site Scripting)](https://owasp.org/www-community/attacks/xss/)
- [MDN Web Docs on XSS](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting)
- [CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html)

## Impact

If an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user. Amongst other things, the attacker can:

- Perform any action within the application that the user can perform.
- View any information that the user is able to view.
- Modify any information that the user is able to modify.
- Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user.

There are various means by which an attacker might induce a victim user to make a request that they control, to deliver a reflected XSS attack. These include placing links on a website controlled by the attacker, or on another website that allows content to be generated, or by sending a link in an email, tweet or other message. The attack could be targeted directly against a known user, or could be an indiscriminate attack against any users of the application.

## System Host(s)
www.████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
This URL demonstrates a potential XSS (Cross-Site Scripting) attack by injecting hidden JavaScript code. Here’s how it works:

1. **Open the URL:** When the user navigates to the URL, the server processes the request with the embedded parameters.

```url
https://www.██████/tags/image/sizzle-reel?&view=K0X%22%20AutoFocus%20%2526%252362%20OnFocus%0c%3dprompt%601%60%20kaos%3d%22uwps2&sort=date
```

2. **Hidden code execution:** The URL contains special characters and encoded payloads (`%22`, `%2526`, `%252362`, `%60`, etc.) that are interpreted in different ways by the browser or the application.

███████

3. **XSS attack:** Specifically, the injected code (`AutoFocus`, `OnFocus`, `kaos="uwps2"`) attempts to execute when a particular event occurs. In this case, it could be something like a focus event (`OnFocus`). When a user interacts with an element on the page (for example, clicks a link or inputs data), the hidden code executes, potentially triggering the XSS payload.

████████

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
