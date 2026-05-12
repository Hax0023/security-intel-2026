# Stored/Reflected XSS in instacart.com/store/partner_recipe via image_url Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 227809 | https://hackerone.com/reports/227809
- **Submitted:** 2017-05-12
- **Reporter:** ak1t4
- **Program:** Instacart
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Improper Input Validation, Unsafe URL Handling
- **CVEs:** None
- **Category:** web-api

## Summary
The /store/partner_recipe endpoint fails to properly validate the image_url parameter, allowing attackers to inject arbitrary JavaScript code via data: URIs with base64-encoded HTML/script payloads. When users interact with the injected link (opening image in new window), the malicious script executes in the context of instacart.com, potentially compromising user sessions and sensitive data.

## Attack scenario
1. Attacker crafts a malicious URL containing base64-encoded JavaScript in the image_url parameter using data: URI scheme
2. Attacker sends the crafted link to victims via social engineering, messaging, or email spoofing
3. Victim clicks the link and visits the vulnerable instacart.com endpoint
4. Victim right-clicks on 'See Image' link or opens image in new window/tab
5. Browser processes the data: URI and executes the embedded JavaScript payload
6. Attacker's script executes with victim's privileges, potentially stealing session cookies, CSRF tokens, or performing unauthorized actions

## Root cause
The application fails to validate, sanitize, or restrict the image_url parameter before rendering it as an href attribute. The endpoint does not implement Content Security Policy (CSP) headers or URL scheme whitelisting to prevent data: URIs. No escaping of special characters or validation against dangerous URI schemes is performed.

## Attacker mindset
An attacker seeks to compromise Instacart users by leveraging the trusted domain to bypass browser same-origin protections. By embedding code in URL parameters, the attacker exploits the application's trust in user-supplied input and can harvest credentials, perform account takeover, or manipulate user orders without detection.

## Defensive takeaways
- Implement strict URL validation: whitelist only safe schemes (http/https) and reject data:, javascript:, vbscript: URIs
- Apply context-aware output encoding: HTML-encode, URL-encode, and JavaScript-encode all user input before rendering in different contexts
- Deploy Content Security Policy (CSP) headers with img-src and script-src directives to restrict resource loading
- Use security-focused templating engines that automatically escape output by default
- Implement a URL sanitization library that removes potentially dangerous URI schemes
- Conduct security code review of all user-facing endpoints accepting URL parameters
- Perform regular XSS testing and maintain an XSS prevention checklist for developers
- Use HTTP-only and Secure flags on cookies to limit session hijacking impact

## Variant hunting
Check other recipe/partner endpoints for similar image_url parameter injection
Test all parameters in partner_recipe endpoint (recipe_url, partner_name, title, description) for XSS
Scan for similar data: URI XSS vulnerabilities in product sharing, saved recipes, or social features
Investigate if SVG/XML-based payloads bypass filters: data:image/svg+xml;base64,...
Test for blind XSS in parameters that may be processed asynchronously or stored
Check for JSONP/callback parameter exploitation on API endpoints
Review all UGC (user-generated content) features for similar encoding bypass techniques

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Gather Victim Identity Information: Spearphishing Link
- T1056.004 - Interaction with User through Web Interface

## Notes
This is a classic reflected XSS vulnerability leveraging data URI encoding to bypass naive input filters. The base64 encoding obfuscates the payload from simple string matching filters. The vulnerability requires user interaction (clicking image link) but still poses significant risk for credential theft and session compromise on a high-traffic e-commerce platform. The report lacks information on whether this is stored or purely reflected XSS, and bounty amount is not disclosed.

## Full report
<details><summary>Expand</summary>

### Summary

Hi team, i found that this endpoint -> https://www.instacart.com/store/partner_recipe? at param ```image_url``` is vulnerable to XSS

#### Reproduction Steps & PoC

1)Go to ```https://www.instacart.com/store/partner_recipe?recipe_url=http://&partner_name=&ingredients[]=apples&ingredients[]=butter&ingredients[]=Splenda+Brown+Sugar+Blend&ingredients[]=cinnamon&ingredients[]=nutmeg&title="Barb%27s+Fried+Apples+-Diabetic-Low+Fat&description=&image_url=data%3atext%2fhtml%3bbase64%2cPHNjcmlwdD5hbGVydCgieHNzIik8L3NjcmlwdD4 ```
2) Right Click on link "See Image" or open image in new window
3) You see the alert popup 

{F183896}
{F183895}

**Vulnerable Enpoint :** ```https://www.instacart.com/store/partner_recipe? ```
**Vulnerable Param:** ``` image_url```
**Vulnerable Payload:** ```data%3atext%2fhtml%3bbase64%2cPHNjcmlwdD5hbGVydCgieHNzIik8L3NjcmlwdD4```

**Tested on Browserss**: Latest **Firefox** & **Chrome**

Let me know if more info needed or anything else,

king regards,
@ak1t4




</details>

---
*Analysed by Claude on 2026-05-12*
