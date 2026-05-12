# Reflected XSS in Shopify Collections Vendor Search via Query Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 324136 | https://hackerone.com/reports/324136
- **Submitted:** 2018-03-10
- **Reporter:** gromoza
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, WAF Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Shopify collections vendor search endpoint (*.myshopify.com/collections/vendors?q=) where user input is insufficiently sanitized. Although the WAF blocks angle brackets, double and single quotes are permitted, allowing attackers to inject event handlers and execute arbitrary JavaScript.

## Attack scenario
1. Attacker crafts malicious URL with XSS payload in the 'q' query parameter
2. Payload uses double quotes to break out of existing HTML attributes while bypassing '<' and '>' character filters
3. Attacker injects event handler attribute (e.g., onmouseover) with JavaScript code
4. Victim visits the crafted link or is redirected to it via phishing
5. Payload renders in victim's browser without sanitization
6. JavaScript executes in victim's session context, enabling session hijacking, credential theft, or malware distribution

## Root cause
The application implements incomplete input validation by blacklisting only '<' and '>' characters while allowing quote characters. This permits HTML attribute injection attacks even without angle brackets. The output is not properly HTML-escaped before rendering in the response.

## Attacker mindset
Reconnaissance to identify blacklist-based protections, testing quote characters to bypass WAF, leveraging event handlers as alternative XSS vectors, crafting user-friendly PoC with visual feedback (alert box) to demonstrate impact.

## Defensive takeaways
- Implement whitelist-based input validation rather than blacklist approaches
- Use context-aware output encoding (HTML entity encoding for HTML context)
- Apply Content Security Policy (CSP) headers to restrict inline script execution
- Sanitize all user inputs regardless of character restrictions
- Test WAF rules comprehensively for bypass techniques using quotes, encoding, and alternative payload vectors
- Implement proper parameterized template rendering to prevent injection
- Regular security testing including fuzzing quote combinations and event handler attributes

## Variant hunting
Search for other query parameters accepting user input on *.myshopify.com domains
Test other Shopify endpoints with search/filter functionality for similar quote injection
Attempt single quote variants: q=X' onmouseover='alert(1)' style='
Test backtick injection for template literal escaping
Check for similar incomplete WAF rules in other parameters (product, collection, customer search)
Investigate if the vendor endpoint has authenticated vs unauthenticated variations with different protections

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a classic WAF bypass demonstrating the danger of blacklist-only filtering. The large font-size styling (1001pt) was likely used to make the invisible character 'X' visually obvious for PoC. The vulnerability affects all Shopify merchant stores using this collections feature, making it a high-impact, widely exploitable issue. The simplicity of the payload suggests the WAF configuration was not thoroughly tested against quote-based injection vectors.

## Full report
<details><summary>Expand</summary>

WAF cut "<",">, but " and ' still in.
1. 
[PoC example link](https://lostvalues.myshopify.com/collections/vendors?q=X" onmouseover="alert('XSS')" style="font-size: 1001pt;") 
2.mouse on X
3. ..
4.XSS alert message

## Impact

XSS atack

</details>

---
*Analysed by Claude on 2026-05-12*
