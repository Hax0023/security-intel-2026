# Stored XSS via HTML Comment Bypass in Store Settings

## Metadata
- **Source:** HackerOne
- **Report:** 415484 | https://hackerone.com/reports/415484
- **Submitted:** 2018-09-27
- **Reporter:** dr_dragon
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, WAF Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Shopify's admin settings where HTML comment sequences (<!-->) can bypass WAF protections designed to strip HTML tags. An attacker can inject malicious SVG payloads with event handlers in the street address field that execute when the dashboard is accessed.

## Attack scenario
1. Attacker creates or gains access to a Shopify store account
2. Attacker navigates to the store settings general configuration page
3. Attacker inputs a crafted XSS payload with HTML comments in the street address field: xss"><!--><svg/onload=alert(document.domain)>
4. The WAF filters the closing tag but the HTML comment (<!-->) allows the SVG tag to bypass filtering
5. Attacker or victim visits the admin dashboard live view at /admin/dashboards/live
6. The malicious SVG payload executes in the victim's browser context, demonstrating XSS via alert dialog

## Root cause
The WAF implementation only strips obvious HTML tags but fails to handle HTML comment sequences that can obscure or separate tag syntax. The input validation does not properly sanitize or escape user-supplied data before rendering in the admin dashboard, allowing encoded payloads to execute.

## Attacker mindset
Researcher discovered that WAF rules have predictable filtering patterns and can be circumvented using HTML comments as separators. By testing variations of comment syntax, they found that <!--> allows malicious tags to persist and execute when rendered.

## Defensive takeaways
- Implement proper output encoding/escaping based on context (HTML, JavaScript, CSS, URL) rather than relying solely on input filtering
- Use a robust sanitization library that understands HTML semantics and handles edge cases like comments, CDATA, and conditional statements
- Apply Content Security Policy (CSP) headers to prevent inline script execution
- Implement server-side input validation that rejects suspicious patterns, not just strips known tags
- Test WAF rules against common bypass techniques including HTML comments, character encoding, and mixed case variations
- Use allowlist-based validation for address fields rather than blocklist-based filtering
- Validate that sanitization removes all executable contexts, not just specific tag names

## Variant hunting
Look for similar bypasses in other fields accepting user input (product descriptions, customer notes, shipping addresses). Test other HTML/XML constructs: <!--[if IE]>, <![CDATA[, nested comments <!--<!-->, encoded entities, case variations, and polyglot payloads. Check if the vulnerability exists in other Shopify admin pages or themes that display user-supplied data.

## MITRE ATT&CK
- T1190
- T1598
- T1598.004

## Notes
The writeup lacks specific bounty amount and disclosure timeline. The vulnerability demonstrates a classic WAF bypass technique using comments. The presence of this in admin settings is particularly critical as it affects store administrators. The '/admin/dashboards/live' endpoint appears to render unsanitized user data from settings.

## Full report
<details><summary>Expand</summary>

# Description :
WAF cut html tages but when put <!--> before tages we can bypass it :) .

#Step to reproduce :
1-Open your store account
2-Navigate to https://xxx.myshopify.com/admin/settings/general
3-Put your street address xss payload (xss"><!--><svg/onload=alert(document.domain)>)
4-Go to https://xxx.myshopify.com/admin/dashboards/live
5-XSS alert message

## Impact

XSS attack

</details>

---
*Analysed by Claude on 2026-05-12*
