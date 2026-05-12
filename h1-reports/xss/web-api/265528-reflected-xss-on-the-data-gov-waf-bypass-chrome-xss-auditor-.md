# Reflected XSS on data.gov with WAF Bypass and Cross-Browser Compatibility

## Metadata
- **Source:** HackerOne
- **Report:** 265528 | https://hackerone.com/reports/265528
- **Submitted:** 2017-09-02
- **Reporter:** sp1d3rs
- **Program:** data.gov
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), WAF Bypass, Chrome XSS Auditor Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered on the data.gov/local/ endpoint within pagination controls that bypasses WAF protections and the Chrome XSS Auditor. The vulnerability is exploitable across all major browsers (Chrome, Firefox, IE) through maliciously crafted URL parameters in the query string.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload embedded in URL parameters with encoding/obfuscation to evade WAF filters
2. Attacker sends the URL to target victim via phishing email, social engineering, or embedded in a website
3. Victim clicks the link and visits the data.gov/local/ endpoint with the crafted payload
4. Victim hovers mouse over pagination element (e.g., 'Page 2' link) triggering the onmouseover event handler
5. JavaScript payload executes in victim's browser context with access to session cookies and sensitive data
6. Attacker steals session tokens, credentials, or performs actions on behalf of the victim within data.gov

## Root cause
Unsanitized user input from URL query parameters is directly reflected into pagination HTML markup without proper encoding or validation. The pagination div includes dynamic URLs constructed from user-controlled parameters without escaping special characters or event handler attributes.

## Attacker mindset
An attacker would recognize that pagination controls often reconstruct URLs dynamically from user input without sanitization. By using obfuscated payloads (HTML entity encoding like %3C for <, %3E for >), they can bypass both WAF rules looking for literal '<script>' patterns and browser XSS auditors that perform pattern matching. The requirement for mouse interaction makes this suitable for social engineering attacks.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data reflected in HTML context (use HTML entity encoding for <, >, &, ", ')
- Use templating engines with auto-escaping enabled to prevent context-specific injection
- Validate and sanitize URL parameters server-side before constructing pagination URLs
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Use allowlist-based validation for query parameters instead of blacklist approaches
- Test WAF rules against encoded payload variants, not just literal patterns
- Implement input validation to reject or normalize unexpected characters in search/filter parameters
- Conduct regular security testing across all browsers and WAF configurations

## Variant hunting
Look for similar pagination implementations across other government/data websites; search for other endpoints using user-controlled parameters in href attributes; test other query parameters (q, filter, sort) for similar reflection issues; check for variations using different encoding schemes (double-encoding, unicode escapes, mixed case HTML tags)

## MITRE ATT&CK
- T1190 (Exploit Public-Facing Application)
- T1598 (Phishing - Link-based)
- T1566 (Phishing)
- T1539 (Steal Web Session Cookie)

## Notes
The vulnerability is particularly severe due to cross-browser compatibility and WAF bypass capability. The obfuscation technique using HTML entities (zzz%27onmou%3Cseover=1) defeats simple pattern matching. The requirement for user interaction (mouse hover) slightly reduces impact but does not eliminate practical exploitability through social engineering. Similar to the earlier report #263226 but with broader browser support.

## Full report
<details><summary>Expand</summary>

##Description
Hello. I discovered Cross-Site scripting issue on the https://www.data.gov/local/ endpoint.
The issue can be site-wide, and exploitable in any place, where pagination exist.

##The Impact and Severity
I assigned the High severity, because unlike the last #263226 report (that XSS was exploitable in the Firefox only), this XSS works in all browsers (Chrome/IE/Firefox).
But, considering that this case requires user interaction (hovering the mouse to the Page 2), the severity can be lowered to the Medium, if you consider so.

##POC (Reflected XSS)
Use this link in the Mozilla Firefox, Chrome or IE
https://www.data.gov/local/?&q&zzz%27onmou%3Cseover=1&ale%3Crt(%27xsp%27%3C)%3C;1;%20//

and hover the mouse to the page 2.
{F217930}

##Suggested fix
Sanitize the URLs in the `<div class="pagination">` block. 


</details>

---
*Analysed by Claude on 2026-05-12*
