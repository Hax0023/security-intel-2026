# DOM Based XSS in mercantile.wordpress.org Apparel Category via subcat Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 230435 | https://hackerone.com/reports/230435
- **Submitted:** 2017-05-21
- **Reporter:** pabster
- **Program:** WordPress.org Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** DOM-based Cross-Site Scripting (XSS), Improper Input Validation, Unsafe DOM Manipulation
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in the apparel product category page where the 'subcat' URL parameter is directly injected into the DOM without proper sanitization or encoding. An attacker can craft a malicious URL containing JavaScript payload that executes in the context of the victim's browser when visited.

## Attack scenario
1. Attacker identifies the vulnerable 'subcat' parameter in the product-category/apparel page URL structure
2. Attacker crafts a malicious URL with JavaScript payload: /?subcat="><img src=x onerror=alert(document.domain)>
3. Attacker distributes the malicious link via phishing email, social media, or other channels to target users
4. Victim clicks the malicious link while authenticated to mercantile.wordpress.org
5. The JavaScript payload executes in the victim's browser context with their session privileges
6. Attacker can steal session cookies, perform actions on behalf of the user, or redirect to credential harvesting pages

## Root cause
The application directly uses the 'subcat' query parameter value in the DOM without proper output encoding or input validation. The parameter is likely reflected in HTML attributes or content without HTML entity encoding, allowing injection of HTML tags and event handlers.

## Attacker mindset
An opportunistic attacker seeking to exploit reflected XSS for account takeover, credential theft, or malware distribution targeting WordPress commerce users. The simplicity of exploitation and public nature of the site makes this attractive for automated scanning.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data reflected in the DOM (use HTML entity encoding for HTML context)
- Apply input validation whitelist to 'subcat' parameter - only allow expected category identifiers or alphanumeric characters
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Utilize templating engines with auto-escaping enabled by default (e.g., Twig, Jinja2)
- Perform security code review of URL parameter handling across all product category pages
- Implement automated scanning (SAST/DAST) in CI/CD pipeline to catch DOM XSS vulnerabilities
- Use Security Development Lifecycle practices with developer training on secure coding

## Variant hunting
Check all other category pages for similar subcat parameter usage (clothing, books, etc.)
Test other URL parameters on product pages (search, filter, sort, pagination) for DOM XSS
Examine other WordPress.org subdomains (wporg.org) for similar parameter injection patterns
Look for stored XSS if subcat values are saved and displayed on other pages
Test for double-encoding or bypass techniques (encoding variations, case manipulation)
Check if the vulnerability exists in related parameters like 'cat', 'product_cat', or 'taxonomy'

## MITRE ATT&CK
- T1190
- T1598.003

## Notes
This is a straightforward reflected DOM XSS with clear PoC. The vulnerability likely affects multiple pages using similar parameter patterns. The WordPress.org property suggests this may impact official WordPress merchandise store, increasing severity due to trust factor and potential user volume. No evidence of patching timeline provided in report excerpt.

## Full report
<details><summary>Expand</summary>

Hello,
There is a DOM XSS in mercantile.wordpress.org in the apparel subcat.
For example: https://mercantile.wordpress.org/product-category/apparel/?subcat=<html payload>

Steps To Reproduce
1. Go to https://mercantile.wordpress.org
2. Click on apparel
3. In the url bar add :  /?subcat="><img src=x onerror=alert(document.domain)>
The domain will pop-up.

Or alternatively just click on the link to: https://mercantile.wordpress.org/product-category/apparel/?subcat=%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E

Hope this helps.
Sincerely,
Pablo

</details>

---
*Analysed by Claude on 2026-05-12*
