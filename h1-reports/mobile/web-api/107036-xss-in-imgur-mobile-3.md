# XSS in imgur mobile 3

## Metadata
- **Source:** HackerOne
- **Report:** 107036 | https://hackerone.com/reports/107036
- **Submitted:** 2015-12-27
- **Reporter:** charfee
- **Program:** Imgur
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Input Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in Imgur's mobile platform through improper sanitization of user input in the URL path. An attacker could inject arbitrary JavaScript code via the user parameter that would execute in the victim's browser.

## Attack scenario
1. Attacker crafts a malicious URL containing HTML/JavaScript payload in the user parameter: m.imgur.com/user/"><img src=x onerror=alert(1)>/message
2. Attacker shares the link via email, social media, or forum post to target victims
3. Victim clicks the malicious link while logged into their Imgur account
4. The browser processes the URL and renders the injected img tag with onerror handler
5. JavaScript payload executes in victim's browser with their Imgur session privileges
6. Attacker can steal session cookies, perform actions on behalf of the user, or redirect to phishing page

## Root cause
The application failed to properly URL-decode and HTML-encode user input from the URL path before rendering it in the page. The user parameter value was directly interpolated into HTML without sanitization, allowing quote characters and HTML tags to break out of their intended context.

## Attacker mindset
The researcher systematically tested various parts of the mobile application URL structure, discovering that path parameters were less strictly validated than other input vectors. They recognized that mobile versions often have reduced security controls compared to desktop equivalents.

## Defensive takeaways
- Implement strict output encoding/escaping for all user-controlled data rendered in HTML context
- Apply both URL decoding and HTML entity encoding in the proper sequence
- Use Content Security Policy (CSP) to restrict script execution sources
- Validate and sanitize input at multiple layers (URL parsing, business logic, rendering)
- Apply the same security standards to mobile versions as desktop applications
- Use templating engines that provide auto-escaping by default
- Regularly test path parameters and uncommon input vectors that may be overlooked

## Variant hunting
Similar XSS vulnerabilities likely exist in other URL path parameters on both mobile and desktop versions. Test other user-controlled path segments like /user/{id}/, /gallery/{id}/, and /search/. Check query parameters for similar issues. Investigate other special characters that break HTML context (single quotes, backticks, angle brackets).

## MITRE ATT&CK
- T1190
- T1566

## Notes
This is a relatively simple proof-of-concept demonstrating reflected XSS. The payload uses img onerror handler which is reliable across browsers. The /message path context suggests this may have been discoverable through URL enumeration. This appears to be part of a series of XSS findings in Imgur's mobile platform, indicating systematic security issues during that period.

## Full report
<details><summary>Expand</summary>




Hi
i find other XSS

Poc

http://m.imgur.com/user/%22%3E%3Cimg%20src=x%20onerror=alert(1)%3E/message

thanks ^^ 

</details>

---
*Analysed by Claude on 2026-05-24*
