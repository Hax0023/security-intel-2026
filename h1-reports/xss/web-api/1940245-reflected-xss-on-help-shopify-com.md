# Reflected XSS on help.shopify.com via returnTo Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1940245 | https://hackerone.com/reports/1940245
- **Submitted:** 2023-04-09
- **Reporter:** becfe31193676118ae5073d
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the confirm-account-details endpoint on help.shopify.com where the returnTo parameter is not properly sanitized before being used in a redirect action. When a user clicks the 'Continue' button, arbitrary JavaScript can be executed in the context of the user's session, allowing attackers to steal session cookies or credentials. The vulnerability affects multiple language versions of the platform.

## Attack scenario
1. Attacker crafts a malicious URL containing javascript: protocol or external URL in the returnTo parameter
2. Attacker sends the crafted link to a targeted Shopify user via email, chat, or social media
3. Target user clicks the link and is redirected to help.shopify.com/en/support/confirm-account-details
4. If user is not logged in, they authenticate; if logged in, they proceed to the vulnerable page
5. Target user clicks the 'Continue' button, triggering the unsanitized returnTo parameter
6. JavaScript executes with the user's session privileges, allowing cookie theft, credential harvesting, or phishing via open redirect

## Root cause
The returnTo parameter is accepted as user input and directly used in a redirect mechanism without proper validation or sanitization. The application fails to whitelist allowed redirect destinations or encode/escape the parameter value before processing it in the redirect action.

## Attacker mindset
An attacker would recognize that authentication flows commonly use returnTo/redirect parameters and assume minimal validation. They would test common XSS payloads (javascript:, data:, SVG vectors) and open redirect patterns against these parameters to identify unprotected functionality. The multi-language platform exposure increases attack surface and potential victims.

## Defensive takeaways
- Implement strict whitelist validation for redirect parameters—only allow relative URLs or pre-approved domains
- Use URL parsing libraries to validate that redirect targets match expected patterns before processing
- Encode/escape all user-controlled data before inserting into HTML/JavaScript contexts
- Implement Content Security Policy (CSP) headers to restrict script execution and redirect destinations
- Apply the same security validation across all language versions and localized endpoints
- Use framework-provided redirect methods that automatically validate targets rather than manual string concatenation
- Conduct security testing on all authentication/post-auth flows that accept redirect parameters
- Implement server-side validation, not just client-side checks, for all redirect destinations

## Variant hunting
Search for other parameters named returnTo, redirect, next, return_url, goto, or similar across help.shopify.com and related subdomains
Test authentication flows on other Shopify properties (admin, accounts, partners) for similar redirect vulnerabilities
Check if returnTo accepts data: URIs, javascript: protocols, or protocol-relative URLs (//)
Test with encoded payloads (%2f%2f, URL encoding) to bypass basic filters
Examine error pages and form submissions that might accept redirect parameters
Test POST-based redirects or hidden form fields that might process returnTo values
Look for callback, success_url, or error_url parameters in API endpoints

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1539

## Notes
The vulnerability demonstrates a common pattern in authentication workflows where return-to functionality is not properly secured. The dual nature (XSS + Open Redirect) increases severity as attackers have multiple exploitation vectors. The fact that it works across multiple language versions suggests a systemic validation gap in the platform's redirect handling rather than isolated implementation issues.

## Full report
<details><summary>Expand</summary>

## Summary:
Reflected Cross Site Scripting  (XSS) on https://help.shopify.com/en/support/confirm-account-details?returnTo=

## Platform(s) affected:
All platforms in other languages, exp:
* https://help.shopify.com/es/

## Steps To Reproduce:

  1. Open the URL https://help.shopify.com/en/support/confirm-account-details?returnTo=javascript:alert(document.cookie)
  2. Make login
  3. Back again to https://help.shopify.com/en/support/confirm-account-details?returnTo=javascript:alert(document.cookie)
  4. Click on button "Continue"
  5. The JS will execute.

Notes: 
* If the user already logged, just access the url and click on the button that the js will be executed.
* Also possible make a "Open redirect" when the user click on the button.
   EXP:  
https://help.shopify.com/en/support/confirm-account-details?returnTo=https://evil.com

## Supporting Material:

## Impact

The attacker can execute javascript code and redirect targets for others pages.

</details>

---
*Analysed by Claude on 2026-05-12*
