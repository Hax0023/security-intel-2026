# Reflected XSS on $Any$.myshopify.com/admin via return_url Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 422707 | https://hackerone.com/reports/422707
- **Submitted:** 2018-10-11
- **Reporter:** dr_dragon
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper URL Validation, Insufficient Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Shopify admin authentication endpoint via the return_url parameter. An attacker can inject arbitrary JavaScript code that executes in the victim's browser when the malicious link is accessed. The vulnerability allows execution of JavaScript protocol handlers without proper validation or sanitization.

## Attack scenario
1. Attacker crafts a malicious URL with javascript: protocol in the return_url parameter
2. Attacker sends the link to a Shopify store admin via phishing email or social engineering
3. Victim clicks the link and arrives at the /admin/authenticate page with injected payload
4. Victim reloads the page or the page auto-loads the return_url parameter
5. JavaScript payload executes in the victim's browser with admin session privileges
6. Attacker can steal session cookies, perform unauthorized actions, or compromise the store

## Root cause
The return_url parameter is reflected in the page output without proper validation or sanitization. The application fails to validate that the URL uses safe protocols (http/https) and does not escape special characters that could be interpreted as JavaScript protocol handlers.

## Attacker mindset
An attacker would target Shopify store administrators with phishing campaigns containing the malicious return_url link. Once the victim's session is hijacked, the attacker gains full control of the admin panel to modify products, steal customer data, or inject malware.

## Defensive takeaways
- Implement strict whitelist validation for return_url parameters - only allow http and https protocols
- Use URL parsing libraries to validate URLs before reflection or redirection
- Sanitize and encode all user input before outputting to HTML/JavaScript contexts
- Implement Content Security Policy (CSP) headers to restrict script execution
- Use URL canonicalization to prevent protocol confusion attacks
- Implement SameSite cookie attributes to mitigate session hijacking
- Validate that return URLs belong to the same origin or explicitly allowed domains

## Variant hunting
Check other admin endpoints for return_url, redirect, next, callback parameters
Test for data: protocol handlers in URL parameters
Look for similar patterns in checkout, account, and authentication flows
Test for DOM-based XSS through URL parameter reflection in JavaScript
Check if other shops (*.myshopify.com) have similar vulnerable endpoints
Test for stored XSS if return_url values are persisted anywhere
Look for open redirects combined with XSS for more sophisticated attacks

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1059.007

## Notes
This is a classic reflected XSS vulnerability in a critical admin panel. The use of javascript: protocol is a straightforward injection vector. The report lacks specific impact details and bounty amount, suggesting it may have been resolved or triaged at lower severity. The vulnerability affects all Shopify stores using the standard admin authentication flow, making it a high-impact issue if exploitable at scale.

## Full report
<details><summary>Expand</summary>

# Description :
Hi,
I have found a reflected cross site scripting vulnerability in <any>.myshopify.com/admin through return_url parameter .

# Step to reproduce :
1-Go to https://<Any>.myshopify.com/admin/authenticate?return_url=javascript:alert(100)//
2-Click on reload this page
3-Xss alert message

## Impact

Xss attack in <Any>.myshopify.com/admin

</details>

---
*Analysed by Claude on 2026-05-12*
