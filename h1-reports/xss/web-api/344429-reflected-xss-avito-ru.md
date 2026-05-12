# Reflected XSS in Avito.ru Login Redirect

## Metadata
- **Source:** HackerOne
- **Report:** 344429 | https://hackerone.com/reports/344429
- **Submitted:** 2018-04-29
- **Reporter:** circuit
- **Program:** Avito
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Open Redirect, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the login redirect mechanism on avito.ru where the 'next' parameter in the URL fragment is not properly sanitized. An attacker can craft a malicious link containing JavaScript code that executes after user authentication through OAuth providers (OK.ru, VK.com).

## Attack scenario
1. Attacker crafts a malicious URL: https://www.avito.ru/sankt-peterburg?verifyUserLocation=1#login?next=javascript:alert();// containing JavaScript payload
2. Attacker sends the link to a victim via phishing email, social media, or chat
3. Victim clicks the link and is redirected to the login page
4. Victim authenticates using OAuth provider (Odnoklassniki, VKontakte, etc.)
5. After successful authentication, the JavaScript payload in the 'next' parameter is executed in the victim's browser context
6. Attacker can steal session cookies, perform actions on behalf of the user, or redirect to phishing page

## Root cause
The application fails to validate and sanitize the 'next' parameter used for post-login redirects. The parameter accepts javascript: protocol URIs without proper encoding or validation, allowing arbitrary JavaScript execution after OAuth callback.

## Attacker mindset
Looking for post-authentication XSS vectors by testing OAuth redirect chains. Leveraging URL fragment handling and weak parameter validation in redirect logic to bypass initial XSS filters that may only check the main URL path.

## Defensive takeaways
- Implement strict whitelist validation for redirect URLs - only allow same-origin redirects or explicitly whitelisted domains
- Encode all user-controlled parameters before use in URL contexts
- Use URL parsing libraries to properly validate protocol (reject javascript:, data:, vbscript:)
- Validate redirect parameters on both client and server side
- Implement Content Security Policy (CSP) headers to restrict script execution
- Test OAuth callback handling and post-login redirects as part of security testing
- Sanitize and validate URL fragments in addition to query parameters

## Variant hunting
Test other OAuth providers for similar redirect parameter handling
Look for 'returnUrl', 'callback', 'redirect', 'redirect_uri' parameters in login flows
Test data: and vbscript: protocol handlers in redirect parameters
Check if other Avito subdomain/regions have similar vulnerability
Test XSS in other post-authentication redirect scenarios
Verify if stored XSS is possible through user profile fields used in redirects

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
Writeup is in Russian. The vulnerability leverages URL fragment handling (#) combined with improper redirect parameter validation. The use of OAuth providers increases impact as users trust the authentication flow. Simple but critical flaw in post-auth security logic.

## Full report
<details><summary>Expand</summary>

Привет, авито) 

Я нашел у вас хсс.

1. Переходим по этой ссылке https://www.avito.ru/sankt-peterburg?verifyUserLocation=1#login?next=javascript:alert();//
2. Логинимся через ОК, ВК и т.д.
3. XSS выполнена.

## Impact

XSS

</details>

---
*Analysed by Claude on 2026-05-12*
