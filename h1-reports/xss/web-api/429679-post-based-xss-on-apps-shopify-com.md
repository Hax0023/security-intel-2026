# POST-based XSS on apps.shopify.com via App Name Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 429679 | https://hackerone.com/reports/429679
- **Submitted:** 2018-10-27
- **Reporter:** chaosbolt
- **Program:** Shopify
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Stored/Reflected XSS, DOM-based XSS, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A POST-based XSS vulnerability exists in the Shopify app store listing creation feature where unsanitized user input (App name) is inserted directly into a script tag. The vulnerability allows attackers to inject malicious HTML/JavaScript that executes in the context of apps.shopify.com, potentially affecting multiple users across Firefox, IE, and Edge browsers.

## Attack scenario
1. Attacker navigates to partners.shopify.com and selects an app to create a store listing
2. Attacker captures the redirect URL containing the signature parameter by copying the full URL
3. Attacker injects malicious payload '</script><svg onload=alert()>' into the App name field
4. Attacker opens the captured URL in an incognito/private browsing window
5. Attacker clicks 'Preview changes' button to trigger the XSS payload
6. Malicious JavaScript executes in the victim's browser, potentially stealing session tokens, credentials, or performing actions on behalf of the user

## Root cause
The App name parameter is directly inserted into a JavaScript context (within a <script> tag) without proper HTML entity encoding or sanitization, allowing script tag closure and injection of arbitrary HTML/JavaScript payloads.

## Attacker mindset
An attacker with app developer access could craft malicious URLs to distribute to other developers or users, causing XSS execution in their browsers. The signature parameter may protect against CSRF but doesn't prevent injection attacks.

## Defensive takeaways
- Implement strict output encoding for all user-supplied data before inserting into HTML/JavaScript contexts
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Never directly interpolate user input into script tags; use data attributes or JSON serialization instead
- Perform input validation and sanitization on all user-supplied parameters
- Use a templating engine with automatic escaping enabled
- Implement context-aware encoding based on where data appears (HTML, JavaScript, URL, CSS)
- Test for XSS vulnerabilities across multiple browsers and rendering engines

## Variant hunting
Test other input fields in app creation forms for similar vulnerabilities (description, category, pricing details)
Check if other Shopify partner tools have similar script tag injection points
Investigate whether the signature parameter can be bypassed or reused across different app contexts
Test for stored XSS by checking if app name persists and executes for other users viewing the listing
Look for similar patterns in preview/staging functionality across Shopify admin interfaces
Test with alternative payload variations (e.g., different event handlers, data URLs, base64 encoding)

## MITRE ATT&CK
- T1190
- T1566
- T1566.002

## Notes
The vulnerability demonstrates a common pattern where developers incorrectly assume data within script tags needs no encoding. The POST-based nature and preview functionality suggest this is likely a Stored or Reflected XSS. The mention of browser-specific behavior (Firefox, IE, Edge vs Safari) indicates potential differences in HTML parsing across engines. The signature parameter suggests CSRF protection but doesn't address injection attacks.

## Full report
<details><summary>Expand</summary>

Hello Shopify team! I found a post-based XSS which may be shared to other users and occurs in firefox, IE, Edge.

How to reproduce:
1. at partners.shopify.com go to apps -> choose one -> more actions -> create shopify app store listing
2. you will get redirected to url with ?signature parameter. Full copy whole URL.
3. as App name specify </script><svg onload=alert()>
4. in incognito tab open URL copied in step 2
5. click Preview changes

How to fix: 

Sanitize parameters which are getting inserted in <script> tag.

## Impact

POST-based XSS in firefox/ie/edge. probably safari too

</details>

---
*Analysed by Claude on 2026-05-12*
