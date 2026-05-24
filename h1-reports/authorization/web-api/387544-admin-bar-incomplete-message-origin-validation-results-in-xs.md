# Admin bar: Incomplete message origin validation results in XSS

## Metadata
- **Source:** HackerOne
- **Report:** 387544 | https://hackerone.com/reports/387544
- **Submitted:** 2018-07-27
- **Reporter:** palant
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Insufficient Origin Validation, PostMessage API Misuse
- **CVEs:** None
- **Category:** web-api

## Summary
The Shopify admin bar injector script performs incomplete origin validation on postMessage events, allowing attackers to bypass origin checks via substring matching. An attacker can craft a malicious domain (e.g., `foo.my` instead of `foo.myshopify.com`) that passes the indexOf validation and inject arbitrary JavaScript code into shop admin sessions.

## Attack scenario
1. Attacker registers a domain like `foo.myshopify.co` or `foo.my` that matches the beginning of legitimate shop domains through substring matching
2. Attacker hosts a malicious HTML page on their domain containing an exploit that sends postMessage events to the admin bar iframe
3. Attacker lures a shop admin to visit the malicious page via social engineering (e.g., fake support ticket)
4. The admin bar's incomplete origin validation (using indexOf instead of exact match) accepts the attacker's origin as valid
5. Attacker sends a `redirect_to_url` postMessage with a `javascript:` payload, injecting arbitrary code into the shop context
6. Injected JavaScript executes in the admin's browser context, enabling theft of CSRF tokens, shop data, or account takeover

## Root cause
The origin validation logic uses `this.iframe.src.indexOf(a) < 0` which performs substring matching without enforcing strict boundaries. Since `e.origin` lacks a trailing slash and `indexOf` doesn't guarantee positional matching, origins like `https://foo.my` pass validation against `https://foo.myshopify.com/admin/bar`. The correct approach requires checking that the origin matches a proper path prefix (e.g., `this.iframe.src.indexOf(a + "/") == 0`).

## Attacker mindset
An attacker recognizes that postMessage origin validation is a common source of vulnerabilities and tests for substring matching bypasses. They understand that domain registration is accessible (registering `.co` TLDs or similar-looking domains) and that social engineering can reliably deliver shop admins to malicious sites. The attacker recognizes that JavaScript injection in an admin context provides high-value access to shop data and account credentials.

## Defensive takeaways
- Always use exact origin matching when validating postMessage events, never rely on substring matching with indexOf
- Validate origins using explicit string equality or proper URL parsing libraries that respect protocol and domain boundaries
- Implement strict postMessage policies: whitelist expected origins entirely rather than blacklisting or partial matching
- Consider using the `targetOrigin` parameter in postMessage to restrict message delivery to specific origins
- Audit all postMessage implementations for similar substring matching vulnerabilities, especially in security-critical contexts
- Implement Content Security Policy (CSP) to restrict JavaScript execution and mitigate XSS impact
- Use iframe sandboxing attributes to limit capabilities of injected content
- Educate admins about phishing risks and provide indicators when admin bar is active for domain verification

## Variant hunting
Search for other postMessage listeners using indexOf-based validation in Shopify CDN assets
Test other Shopify embedded tools and admin features that use cross-origin messaging
Look for similar origin validation patterns in other e-commerce platforms (WooCommerce, BigCommerce, etc.)
Check for postMessage implementations in third-party Shopify apps that may have similar flaws
Test variations of domain bypasses: `https://foo.my`, `https://foo.myshopify.c`, `https://malicious.foo.myshopify.com` (subdomain injection)
Examine historical patches for related postMessage vulnerabilities (referenced report 381192) to identify patterns

## MITRE ATT&CK
- T1190
- T1559.001
- T1598.003
- T1566.002

## Notes
This vulnerability chains social engineering (phishing) with insufficient input validation to achieve RCE-equivalent compromise in admin context. The vulnerability explicitly references a similar prior issue (report 381192), suggesting pattern recurrence across codebases. The attack demonstrates how cloud-hosted admin panels remain attractive targets due to session continuity and high-privilege operations. The reliance on popup blockers as a secondary defense is insufficient security practice.

## Full report
<details><summary>Expand</summary>

This issue is very similar to https://hackerone.com/reports/381192, identical logic in a different script. The JavaScript code at https://cdn.shopify.com/s/assets/storefront/bars/admin_bar_injector-7461c2cab955bf9ef3df40acd10741df8c4e27c86d9dc323f65a4e786a1786f2.js (loaded by the shop front when the admin bar is active) installs a `message` event listener. The following check is used to reject invalid origins:

    var t=e.data,i=t.action,r=t.height,n=t.url,s=t.isCollapsed,a=e.origin;
    !i||
    o.returnObjectValues(this.POST_MESSAGE_ACTIONS).indexOf(i)<0||
    this.iframe.src.indexOf(a)<0||
    this.postMessageHandler(i,r,n,s)

With `this.iframe.src` being something like `https://foo.myshopify.com/admin/bar`, this *mostly* does the job correctly. However, `e.origin` doesn't end with a slash, meaning that for example `https://foo.my` is a possible origin and would be accepted here. Sending an `redirect_to_url` message allows the attacker to specify a URL to redirect to, supplying a `javascript:` URLs here will result in script injection, only to be prevented by the pop-up blocked - if active.

*Recommendation*: Changing the check into `this.iframe.src.indexOf(a + "/") != 0` should reliably reject all invalid origins.

This attack works against shop admins who have the admin bar enabled. If admin bar doesn't show up at the bottom of your shop, clear cookies and make sure you are logged into the admin interface. I assume here that your shop is located under `foo.myshopify.com` - change the host name appropriately.

1. Download the attached `ssl_server.py` script and `exploit_admin_bar.html` page to the same directory on your computer.
2. Edit `/etc/hosts` file (that's `%Windir%\Sysnative\drivers\etc\hosts` on Windows) and add the following entry: `127.0.0.1 foo.myshopify.co` (note that it has to end with `.co` instead of `.com`). The real attackers would register `myshopify.co` or `foo.my` instead to attack your shop.
3. Start `ssl_server.py` script (requires Python 3) to run a local SSL-protected web server. On Linux and macOS this script needs to be run with administrator privileges.
4. Open https://foo.myshopify.co/exploit_admin_bar.html in your browser and accept the invalid certificate (real attacker would actually own `foo.myshopify.co`, so they would be able to get a valid certificate for it).
5. Click the link on the page.

Your shop will open in a new tab. Note a message from the pop-up blocker (if enabled) saying that a pop-up was blocked. If you are careless enough to allow that pop-up (it comes from your own shop) or disable pop-up blocker, you will see the message "Hi, script running on foo.myshopify.com here!" - JavaScript code has been successfully injected into your shop front and can make its way to the admin interface from there.

## Impact

Shop admins can be easily lured to a malicious website, e.g. by reporting a supposed issue via support channels. Once a shop admin opens that website, it gets a chance to run JavaScript code in their shop. This JavaScript code can then open https://foo.myshopify.com/admin/ in a small pop-up window and abuse the active admin session to extract data from it (CSRF tokens, shop configuration) or maybe even change admin password to take over the account.

</details>

---
*Analysed by Claude on 2026-05-24*
