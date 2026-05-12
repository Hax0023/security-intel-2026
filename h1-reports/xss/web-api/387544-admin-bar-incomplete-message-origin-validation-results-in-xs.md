# Admin bar: Incomplete message origin validation results in XSS

## Metadata
- **Source:** HackerOne
- **Report:** 387544 | https://hackerone.com/reports/387544
- **Submitted:** 2018-07-27
- **Reporter:** palant
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Postmessage Origin Validation Bypass, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
Shopify's admin bar JavaScript uses incomplete origin validation when processing postMessage events, allowing attackers to inject malicious origins that pass validation checks. By registering a similar domain (e.g., foo.my instead of foo.myshopify.com), an attacker can send crafted postMessage events with javascript: URLs to achieve XSS execution in the admin's browser session.

## Attack scenario
1. Attacker registers a domain similar to target shop's domain (e.g., foo.my or myshopify.co)
2. Attacker hosts a malicious HTML page on that domain containing postMessage exploit code
3. Attacker lures shop admin to visit malicious page through social engineering
4. Admin bar's message listener receives postMessage with redirect_to_url containing javascript: payload
5. Origin validation passes due to substring matching without slash delimiter (e.g., 'https://foo.my' matches 'https://foo.myshopify.com/admin/bar')
6. JavaScript payload executes in shop context, allowing data theft or admin session compromise

## Root cause
The origin validation logic uses `indexOf()` substring matching without proper delimiter checking. The check `this.iframe.src.indexOf(a) < 0` fails to validate that the origin is a complete domain component, allowing partial domain matches like 'https://foo.my' to pass when the legitimate origin is 'https://foo.myshopify.com'.

## Attacker mindset
An attacker recognizes that postMessage origin validation is a common security implementation point and identifies insufficient string matching as a bypass technique. They understand admin bar is loaded in shop context with potential access to admin sessions, making it a high-value target for privilege escalation attacks.

## Defensive takeaways
- Always validate postMessage origins using exact matching with protocol and domain, not substring matching
- Use URL parsing APIs (URL constructor) rather than string operations for origin validation
- Implement origin validation as `origin === expectedOrigin` rather than indexOf-based checks
- Validate that origin includes proper domain delimiters (/) to prevent partial domain matches
- Apply defense-in-depth by combining origin validation with additional CSRF protections
- Regularly audit postMessage event handlers for similar validation weaknesses
- Use Content Security Policy (CSP) to restrict script execution sources

## Variant hunting
Search for other postMessage event listeners in Shopify assets using indexOf-based origin validation
Check other Shopify injected scripts (checkout, payment flows) for similar validation patterns
Look for other scripts handling redirect_to_url or javascript: protocol handling
Examine third-party embedded scripts on Shopify storefronts for postMessage vulnerabilities
Review similar substring-based validation in other e-commerce platforms and SaaS applications

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1195: Supply Chain Compromise
- T1566: Phishing
- T1598: Phishing for Information
- T1539: Steal Web Session Cookie

## Notes
This vulnerability is noted as similar to a previous finding (report 381192), suggesting recurring validation issues in Shopify's postMessage implementation. The attack requires the admin to visit an attacker-controlled page but succeeds because admins are authenticated to their shop. The use of homograph domains (foo.my vs foo.myshopify.com) is particularly effective for social engineering attacks.

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
*Analysed by Claude on 2026-05-12*
