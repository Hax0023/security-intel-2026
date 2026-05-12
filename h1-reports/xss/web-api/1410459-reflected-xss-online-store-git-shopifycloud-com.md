# Reflected XSS in Shopify GitHub Integration (online-store-git.shopifycloud.com)

## Metadata
- **Source:** HackerOne
- **Report:** 1410459 | https://hackerone.com/reports/1410459
- **Submitted:** 2021-11-25
- **Reporter:** 0xbepresent
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Shopify GitHub integration feature at online-store-git.shopifycloud.com/github/setup endpoint. The 'installation_id' parameter is not properly sanitized or encoded, allowing attackers to inject arbitrary JavaScript that executes in the context of authenticated users. This affects the OAuth/GitHub connection flow for Shopify stores.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'installation_id' parameter with URL-encoded payload (e.g., alert(1337))
2. Attacker sends the crafted link to a Shopify store owner/staff member via phishing email or social engineering
3. Victim clicks the link while authenticated to their Shopify account
4. The victim is redirected to the legitimate-looking GitHub setup page at online-store-git.shopifycloud.com
5. The JavaScript payload executes in the victim's browser with their authentication context
6. Attacker can steal session tokens, credentials, perform account takeover, or redirect to phishing pages

## Root cause
The application fails to properly encode or sanitize user-supplied input from the 'installation_id' query parameter before reflecting it in the HTTP response. The parameter is likely being inserted directly into JavaScript context or HTML without appropriate escaping mechanisms.

## Attacker mindset
An attacker would target this OAuth integration flow because: (1) victims are already in an authenticated state, (2) the official Shopify domain adds credibility, (3) GitHub integration grants sensitive permissions, (4) store owners/staff are high-value targets with access to customer data and business logic.

## Defensive takeaways
- Implement strict input validation and whitelist allowed characters for parameters like 'installation_id'
- Apply context-appropriate output encoding (HTML entity encoding, JavaScript escaping, URL encoding) before reflecting any user input
- Use Content Security Policy (CSP) headers with strict directives to prevent inline script execution
- Sanitize all OAuth/integration flow parameters using libraries like DOMPurify or equivalent
- Implement security headers: X-XSS-Protection, X-Content-Type-Options: nosniff
- Conduct security code review of OAuth callback handlers and integration endpoints
- Perform regular penetration testing on third-party integration flows
- Use templating engines with auto-escaping enabled (not vulnerable by default)

## Variant hunting
Test other OAuth integration endpoints (Google, Facebook, etc.) for similar parameter injection points
Check 'setup_action' parameter for XSS vulnerability (also present in payload)
Fuzz other query parameters in the /github/setup endpoint
Test POST data if available in alternative integration flows
Check for stored XSS if parameters are logged or persisted
Test JavaScript template injection in other Shopify Cloud services
Examine other integration URLs under shopifycloud.com domain
Test for DOM-based XSS in client-side JavaScript handling of these parameters

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1555
- T1187

## Notes
This vulnerability requires user interaction (clicking malicious link) and authentication context, making it suitable for targeted attacks on store owners/staff. The GitHub integration is a critical feature requiring elevated permissions, making this a high-impact vulnerability despite being reflected XSS. The use of URL encoding in the payload suggests some basic WAF/filter evasion awareness by the reporter.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello, I hope you are having a good day!,

There is a feature called "Shopify Github Integration", it helps to associate a GitHub account to a Shopify  store. In the Github connection proccess there is a URL [https://online-store-git.shopifycloud.com](https://online-store-git.shopifycloud.com) which is vulnerable to XXS reflected.

## Shops Used to Test:
- devpresent.myshopify.com

## Relevant Request IDs:
- x-request-id: 1cdb077b2d319acccd1237c1142cf89b

## Steps To Reproduce:
1. Visit the next [URL](https://online-store-git.shopifycloud.com/github/setup?installation_id=20913869%7d%7d%7d%29%3b%7d%3balert%281337%29%3bif%281==2%29%7bk=new%20Promise%28function%28%29%7bif%281==2%29%7bv=%7be:%201&setup_action=install)
```https://online-store-git.shopifycloud.com/github/setup?installation_id=20913869%7d%7d%7d%29%3b%7d%3balert%281337%29%3bif%281==2%29%7bk=new%20Promise%28function%28%29%7bif%281==2%29%7bv=%7be:%201&setup_action=install```
2. Enter an owner or staff credentials.
3. The XSS will fire.

## Supporting Material:
- xss.png
- poc.mp4

## Impact

There are several impacts.

- The attacker could use Javascript in order to do phishing attacks.
- Steal data.
- Reflected JS

May you be well,
-Misa

</details>

---
*Analysed by Claude on 2026-05-12*
