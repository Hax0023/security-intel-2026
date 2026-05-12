# Reflected XSS in Shopify Theme Preview via theme_handle Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 226428 | https://hackerone.com/reports/226428
- **Submitted:** 2017-05-05
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Inadequate Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Shopify's theme preview functionality through the theme_handle parameter on <account>.myshopify.com domains. The parameter lacks proper quote escaping and output encoding, allowing attackers to inject arbitrary JavaScript that executes in the victim's browser. The injected payload persists across shop pages until the theme preview is cancelled.

## Attack scenario
1. Attacker identifies that the theme_handle parameter is vulnerable to XSS injection
2. Attacker crafts a malicious URL containing JavaScript payload in theme_handle parameter (e.g., xx'-alert(document.cookie)-')
3. Attacker tricks a shop owner/user into clicking the crafted link (via phishing, social engineering, or malicious referral)
4. When the victim navigates to the URL, the JavaScript payload executes in their authenticated browser session
5. Attacker can steal session cookies, perform actions as the victim, or redirect to phishing pages
6. The XSS remains active across all shop pages until the victim clicks 'Cancel theme preview'

## Root cause
The theme_handle parameter value is interpolated into a JavaScript context (Shopify.theme object) without proper quote escaping or output encoding. Single quotes are not escaped, allowing an attacker to break out of the string context and inject arbitrary JavaScript code.

## Attacker mindset
An attacker would seek to compromise shop administrators or users to steal authentication tokens, exfiltrate sensitive business data, modify storefront content, or redirect customers to phishing sites. The persistent nature across pages makes this particularly valuable for maintaining access.

## Defensive takeaways
- Implement strict input validation on all URL parameters, especially those used in JavaScript contexts
- Apply context-aware output encoding: use JavaScript string escaping (not just HTML escaping) for values inserted into JavaScript code
- Escape or sanitize all special characters in strings interpolated into JavaScript, particularly quotes and backslashes
- Use Content Security Policy (CSP) headers to restrict inline script execution and reduce XSS impact
- Employ templating engines with automatic escaping enabled by default
- Validate theme_handle against a whitelist of known valid theme identifiers
- Implement security headers like X-XSS-Protection and X-Content-Type-Options
- Conduct regular security testing and code reviews focusing on user input handling in JavaScript contexts

## Variant hunting
Test style_id and style_handle parameters for similar XSS vulnerabilities
Check preview_theme_id parameter for injection points
Look for other Shopify endpoints that use theme preview functionality with similar parameter handling
Test encoded variations (double encoding, unicode encoding) to bypass filters
Investigate if other myshopify.com subdomains have similar issues
Check if the vulnerability exists in other parameter combinations or request methods (POST vs GET)
Test for stored XSS if theme preview settings are saved

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1563

## Notes
Report demonstrates good vulnerability disclosure with clear reproduction steps and PoC. The vulnerability affects shop owners/administrators during theme preview, making it a high-impact finding. The persistent nature across pages until explicitly cancelled increases the severity. The reporter properly obfuscated the actual shop name in examples while providing clear technical details for remediation.

## Full report
<details><summary>Expand</summary>

Hi,
I have found a reflected cross site scripting vulnerability in `<any>.myshopify.com` through `theme_hanlde` parameter due to not single quotes.

#Steps to reproduce: 
1. Navigate to `<account>.myshopify.com` 
2. view the source of the page and copy the value of `Shopify.theme` Id.
3. Navigate to `https://echo.myshopify.com/?theme_handle=xx%27-alert(document.cookie)-%27&style_id=1&style_handle=1&preview_theme_id=<theme_ID>` 
> *replace `<theme_ID>` with the ID you just copied*.
4. XSS will trigger in all of the online shop pages unless you click `Cancel theme preview` .

**PoC:** 
`https://test.myshopify.com/?theme_handle=xx%27-alert(document.cookie)-%27&style_id=1&style_handle=1&preview_theme_id=3572` 

{F182252}
Thanks!

</details>

---
*Analysed by Claude on 2026-05-12*
