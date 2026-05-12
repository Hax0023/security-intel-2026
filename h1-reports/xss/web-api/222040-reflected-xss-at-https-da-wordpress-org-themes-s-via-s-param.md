# Reflected XSS at da.wordpress.org/themes via 's=' parameter

## Metadata
- **Source:** HackerOne
- **Report:** 222040 | https://hackerone.com/reports/222040
- **Submitted:** 2017-04-18
- **Reporter:** jon_bottarini
- **Program:** WordPress.org
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the WordPress theme search functionality at da.wordpress.org/themes where the 's=' parameter is not properly sanitized or encoded. An attacker can inject arbitrary JavaScript that executes in the victim's browser by crafting a malicious URL with XSS payloads, bypassing HTML/script filters through encoding and tag manipulation.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the 's=' parameter using various encoding techniques (URL encoding, backticks, HTML comments)
2. Attacker distributes URL via phishing email, social media, or posts it on forums targeting WordPress administrators/users
3. Victim clicks the link while logged into WordPress.org or another WordPress-related service
4. Browser renders the page and reflects the unencoded user input directly into the HTML/JavaScript context
5. Payload bypasses weak filters using polyglot techniques (combining image tags, onerror handlers, and comment syntax)
6. Attacker's JavaScript executes with victim's privileges, potentially stealing session cookies, performing actions on behalf of user, or redirecting to malicious site

## Root cause
The search parameter 's=' is reflected in the HTML response without proper HTML entity encoding or Content Security Policy protection. The application likely implements naive or bypassable input filtering that doesn't account for polyglot XSS techniques combining multiple HTML/XML contexts (script tags, image tags with srcset, event handlers, comment syntax).

## Attacker mindset
An attacker would recognize that search parameters are commonly vulnerable to XSS due to being reflected directly in results pages. They would craft polyglot payloads specifically designed to break out of existing filter contexts by mixing HTML tags, event handlers, and comment syntax. The use of backticks and image srcset indicates understanding of modern HTML parsing and event handler execution contexts.

## Defensive takeaways
- Implement strict output encoding based on context (HTML entity encoding, JavaScript encoding, URL encoding, CSS encoding)
- Apply Content Security Policy (CSP) with strict script-src directives to prevent inline script execution
- Use templating engines with automatic escaping by default rather than manual encoding
- Implement input validation whitelist for search parameters (alphanumeric, common search terms only)
- Apply defense-in-depth: never rely solely on input filtering; focus on output encoding
- Conduct security testing with polyglot XSS payloads, not just basic '<script>' tags
- Use HTTPOnly and Secure flags on sensitive cookies to limit XSS impact
- Implement sub-resource integrity and frame-ancestors CSP directives

## Variant hunting
Test other search/query parameters on WordPress properties (wp-admin, wordpress.com, developer.wordpress.org). Look for similar reflection patterns in filter parameters, sort parameters, pagination parameters, and any user-controlled input reflected in search results or error pages. Test with variants: template literal injection, SVG event handlers, data URI schemes, nested tag contexts.

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002

## Notes
The payload demonstrates sophisticated XSS bypass techniques: URL encoding to evade initial pattern matching, use of backticks for template literal context, image srcset attribute for breaking out of standard tag contexts, onerror handler for execution, and HTML comment syntax to consume trailing characters. This suggests the application had basic XSS protections (likely regex-based) that were successfully bypassed. The report lacks reproduction confirmation but includes sufficient technical detail for verification.

## Full report
<details><summary>Expand</summary>

Hello - 

You have a reflected XSS vulnerability located at this domain:

https://da.wordpress.org/themes/?s=

This was tested on the latest version of Chrome (Version 57.0.2987.133 (64-bit)

By entering this payload in the URL, you are able to execute a script to fire:

`1%3C!%27/*%22/*\%27/*\%22/*--%3E%3C/Script%3E%3CImage%20Srcset=K%20*/;%20Onerror=confirm`1`%20//%3E#`

Note that the "1" in the confirm is enclosed in backticks, the HackerOne editor just makes it difficult to show. I have attached a screenshot to show the full URL, as well as included it below: 

https://da.wordpress.org/themes/?s=1%3C!%27/*%22/*\%27/*\%22/*--%3E%3C/Script%3E%3CImage%20Srcset=K%20*/;%20Onerror=confirm`1`%20//%3E#

Please let me know if you have any other questions, thanks!



</details>

---
*Analysed by Claude on 2026-05-12*
