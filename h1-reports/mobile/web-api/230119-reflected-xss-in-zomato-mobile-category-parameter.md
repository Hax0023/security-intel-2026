# Reflected XSS in Zomato Mobile - category parameter

## Metadata
- **Source:** HackerOne
- **Report:** 230119 | https://hackerone.com/reports/230119
- **Submitted:** 2017-05-20
- **Reporter:** harrymg
- **Program:** Zomato
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Zomato's mobile photo gallery feature where the 'category' URL parameter is not properly sanitized or encoded before being reflected in the HTML response. An attacker can inject malicious JavaScript code that executes in the victim's browser when visiting a crafted URL, potentially leading to session hijacking, credential theft, or malware distribution.

## Attack scenario
1. Attacker crafts a malicious URL with XSS payload in the category parameter (e.g., photos?category=...svg/onload payload...)
2. Attacker shares the crafted URL via social engineering, phishing emails, or malicious websites to target Zomato mobile users
3. Victim clicks the link while using Zomato's mobile site (or Zomato mobile app's web view)
4. The category parameter value is reflected unsanitized into the HTML/JavaScript context of the restaurant photos page
5. Victim's browser executes the injected JavaScript payload, allowing the attacker to steal session cookies, capture keystrokes, or perform actions on behalf of the user
6. Attacker gains unauthorized access to victim's Zomato account, personal information, or payment details

## Root cause
The application fails to properly encode user-supplied input (category parameter) before reflecting it back in the HTML response. The parameter value is directly inserted into the page without HTML entity encoding or JavaScript escaping, allowing script tags and event handlers to be interpreted as code rather than data.

## Attacker mindset
Low-skill attackers can easily exploit this via simple URL manipulation. The mobile-specific nature and photo gallery context make it a plausible vector for spear-phishing campaigns targeting food delivery users who may be less security-aware.

## Defensive takeaways
- Implement input validation: whitelist allowed category values (ambience, food, exterior, interior, etc.) and reject anything else
- Apply context-aware output encoding: HTML-encode all user input reflected in HTML context, JavaScript-encode if in script context
- Use Content Security Policy (CSP) headers to restrict inline script execution and limit script sources
- Employ a Web Application Firewall (WAF) to detect and block common XSS patterns in URL parameters
- Implement HTTP-only and Secure flags on session cookies to mitigate session hijacking impact
- Conduct regular security testing (SAST/DAST) of all user input handling, especially in mobile implementations
- Use security libraries/frameworks that automatically encode output based on context

## Variant hunting
Test other category-like parameters in photo galleries (cuisine, diet, location, filter, sort, view, etc.)
Check restaurant listing pages, user review sections, and search results for similar parameter injection
Test mobile vs desktop implementations separately - mobile code paths often receive less scrutiny
Look for XSS in other restaurant metadata parameters (name, description, address in URL)
Test both URL-encoded and double-encoded payloads to bypass naive filters
Check if the vulnerability exists in other Zomato features using category/filter parameters
Test for stored XSS if category values are saved in user preferences or shared wishlists

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Gather Victim Information: Spearphishing Link
- T1539 - Steal Web Session Cookie
- T1185 - Man in the Browser

## Notes
The use of URL encoding and SVG/onload event handler bypass technique shows moderate sophistication. Mobile applications and webviews are common targets for XSS as they receive less security attention than desktop sites. The restaurant/photos context is particularly suitable for phishing as users trust restaurant links. The vulnerability is straightforward to patch through output encoding but may indicate similar issues elsewhere in the Zomato codebase, especially in mobile-specific code paths.

## Full report
<details><summary>Expand</summary>

Hi there. I have found a reflected XSS in Zomato.com mobile. This XSS affects mobile users of Zomato. Steps to reproduce:

1. Go to Zomato.com and change your user agent to mobile *(iPhone/Android user agent)*
2. Go to a certain restaurant/place and their photos *(e.g. site: https://www.zomato.com/manila/artsy-cafe-diliman-quezon-city/photos?category=ambience)*
3. Change the value in the ```category``` parameter to an XSS payload: ```
"--><%2Fscript><svg%2Fonload%3D'%3Balert(document.domain)%3B'>```
4. Final URL will look like this: https://www.zomato.com/manila/artsy-cafe-diliman-quezon-city/photos?category=%22--%3E%3C%2Fscript%3E%3Csvg%2Fonload%3D%27%3Balert%28document.domain%29%3B%27%3E

XSS will execute. POC attached.

Thanks and I hope you consider and fix this

</details>

---
*Analysed by Claude on 2026-05-24*
