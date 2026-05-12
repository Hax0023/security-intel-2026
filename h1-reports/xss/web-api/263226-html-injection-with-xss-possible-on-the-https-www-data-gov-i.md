# HTML Injection and Reflected XSS via media_url Parameter on data.gov/issue/

## Metadata
- **Source:** HackerOne
- **Report:** 263226 | https://hackerone.com/reports/263226
- **Submitted:** 2017-08-25
- **Reporter:** sp1d3rs
- **Program:** data.gov
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** HTML Injection, Reflected Cross-Site Scripting (XSS), WAF Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An HTML injection vulnerability exists in the media_url parameter of the data.gov/issue/ endpoint, allowing attackers to inject arbitrary HTML and execute JavaScript code. The vulnerability bypasses Akamai WAF filters through crafted payloads, enabling reflected XSS attacks that can steal session tokens or perform actions on behalf of users.

## Attack scenario
1. Attacker identifies the media_url parameter in data.gov/issue/ endpoint is not properly sanitized
2. Attacker crafts a malicious URL with HTML/SVG injection payload in the media_url parameter
3. Attacker bypasses Akamai WAF filters by encoding or obfuscating the payload (e.g., using special characters, event handlers like onbeforescriptexecute)
4. Attacker distributes the crafted URL via phishing email, social media, or other channels targeting data.gov users
5. Victim clicks the malicious link while authenticated to data.gov
6. Injected JavaScript executes in victim's browser with their privileges, exfiltrating cookies, CSRF tokens, or performing unauthorized actions

## Root cause
Insufficient input validation and output encoding on the media_url parameter. The application fails to sanitize user-supplied input before reflecting it in the HTML response, and relies solely on WAF protection which can be bypassed.

## Attacker mindset
Opportunistic vulnerability researcher discovering low-hanging fruit through parameter fuzzing. Demonstrates persistent testing against WAF filters to identify bypass techniques, showing methodical approach to security research.

## Defensive takeaways
- Implement server-side input validation for all parameters, rejecting or sanitizing URL-like inputs
- Apply proper HTML entity encoding/escaping to all user-controlled data reflected in responses
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Do not rely solely on WAF for XSS protection; implement defense-in-depth with application-level controls
- Use security-focused templating engines that auto-escape output by default
- Implement allowlist validation for media_url parameter (whitelist expected domains/patterns)
- Regular security testing including XSS payload testing against WAF filters

## Variant hunting
Test other parameters accepting URLs (image_url, thumbnail_url, etc.). Attempt WAF bypass variations: encoding (double URL, Unicode), case manipulation, null bytes, alternative event handlers (onerror, onload, onmouseover). Test on different endpoints accepting media resources. Check for stored XSS if media_url values are saved and displayed elsewhere.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
Reporter demonstrated two variants: SVG-based HTML injection and event handler-based XSS. Firefox-specific rendering noted with onbeforescriptexecute event. The WAF bypass demonstrates that endpoint protection alone is insufficient without application-hardening. No monetary bounty amount disclosed in report.

## Full report
<details><summary>Expand</summary>

##Description
Hello. I discovered Cross-Site scripting issue on the https://www.data.gov/issue/ endpoint.

##Akamai WAF and bypass
At the srart i was not able to do the XSS due to Akamai Waf XSS filters, but later, i was able to bypass it.

##POC (HTML injection)
https://www.data.gov/issue/?media_url=catalog.data.gov/dataset/consumer-complaint-database%22%3E%3Csvg%20height=%22100%22%20width=%22100%22%3E%20%3Ccircle%20cx=%2250%22%20cy=%2250%22%20r=%2240%22%20stroke=%22black%22%20stroke-width=%223%22%20fill=%22red%22%20/%3E%20%3C/svg%3E
{F215755}

##POC (Reflected XSS)
Use this link in the Mozilla Firefox
https://www.data.gov/issue/?media_url=catalog.data.gov/dataset/consumer-complaint-database%22%3E%3C/div%3E%3C/div%3E%3Cbrute%20onbeforescriptexecute=%27confirm(document.domain)%27%3E
{F215768}

##Suggested fix
Sanitize all input fields on this page. 

</details>

---
*Analysed by Claude on 2026-05-12*
