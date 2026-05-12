# DOM XSS in Shopify Embedded SDK via setWindowLocation with Cookie Stuffing and Login CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 422043 | https://hackerone.com/reports/422043
- **Submitted:** 2018-10-10
- **Reporter:** filedescriptor
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** DOM-based XSS, Login CSRF, Cookie Stuffing, Open Redirect, PostMessage Origin Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can achieve DOM XSS on any Shopify embedded app by chaining cookie stuffing, login CSRF, and exploitation of the Shopify.API.setWindowLocation handler. The vulnerability allows execution of arbitrary JavaScript in the context of a victim's authenticated embedded app session by manipulating session cookies using path-specific cookie scoping per RFC 6265.

## Attack scenario
1. Attacker discovers Shopify embedded apps accept postMessage events from their own store origin, which validates shopOrigin against logged-in store
2. Attacker identifies Shopify.API.setWindowLocation handler in SDK accepts javascript: pseudo-URLs leading to potential XSS
3. Attacker performs Login CSRF to force victim into attacker's store session
4. Attacker uses JavaScript to stuff session cookies (_secure_admin_session_id and _master_udr) with specific /admin/oauth paths to bypass legitimate cookie precedence (longer paths override shorter paths per RFC 6265)
5. Attacker redirects victim to their store's /admin/oauth/authorize endpoint, triggering OAuth flow with malicious cookies, authenticating victim as attacker
6. Attacker triggers re-authentication via victim's store (using Shopify.com redirect) to re-log victim into embedded app with their own credentials, then injects javascript: payload via postMessage to setWindowLocation handler

## Root cause
Multiple compounded weaknesses: (1) Embedded SDK's setWindowLocation handler does not validate or sanitize navigation targets before assignment to window.location, allowing javascript: protocol execution; (2) postMessage handler only validates origin against logged-in store, not sender legitimacy; (3) Session cookies can be stuffed with path-specific scoping to override legitimate cookies; (4) OAuth flow does not prevent re-authentication under manipulated session state

## Attacker mindset
Attacker methodically identifies security assumptions (embedded app origin validation), finds edge cases (self-XSS), and chains multiple weak links (cookie stuffing via RFC 6265 path precedence, login CSRF, OAuth redirect chains) to achieve exploitation across trust boundaries. Demonstrates deep understanding of cookie mechanics, OAuth flows, and postMessage security model.

## Defensive takeaways
- Validate and sanitize all navigation targets in setWindowLocation; whitelist safe protocols and reject javascript:, data:, vbscript: URIs
- Implement strict Content-Security-Policy headers to prevent inline script execution from postMessage payloads
- Add cryptographic validation tokens to OAuth state parameter and validate CSRF tokens on OAuth authorize endpoints
- Implement SameSite=Strict on sensitive session cookies to prevent CSRF-induced cookie stuffing
- Use origin and sourceOrigin validation for postMessage; avoid wildcard ('*') receivers
- Implement session fixation protections: regenerate session tokens during authentication transitions
- Enforce path restrictions on cookie scoping to prevent subdomain/path exploitation
- Monitor and alert on unusual cookie writes via JavaScript API to detect cookie stuffing attempts

## Variant hunting
Review other Shopify SDK postMessage handlers for navigation/redirect functionality that may not sanitize targets
Audit third-party embedded app SDKs using similar origin-validation patterns for identical setWindowLocation patterns
Test other Shopify endpoints for cookie path traversal via stuffing (_admin_session_id, _master_session_id variants)
Investigate if other OAuth flows (non-Shopify) are vulnerable to cookie stuffing via RFC 6265 path precedence
Search for similar self-XSS patterns that can be escalated via CSRF + cookie manipulation in SaaS platforms with embedded app ecosystems
Test if other Shopify message handlers (setWindowLocation variants) accept javascript: or data: URIs

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1185: Man in the Browser
- T1566: Phishing
- T1539: Steal Web Session Cookie
- T1598: Phishing for Information
- T1656: Impersonation

## Notes
This is a sophisticated, multi-vector attack requiring victim interaction but no user-agent specific exploits. The writeup demonstrates expert-level knowledge of web security standards (RFC 6265 cookie precedence rules). The attacker creatively solves the self-XSS problem by leveraging login CSRF and OAuth flow manipulation. Shopify's embedded app origin validation was actually correctly implemented per design documentation, but the downstream setWindowLocation handler lacked output validation. This exemplifies how security assumptions at one layer can fail when not reinforced in dependent layers.

## Full report
<details><summary>Expand</summary>

Hi Team!

I'm reporting a rather unusual DOMXSS that allows an attacker to perform a XSS attack on any Shopify apps that use the Embedded SDK. To exploit this, several techniques were chained together: Cookie Stuffing -> Login CSRF -> (Not Open) Redirect -> DOMXSS.

#Details
Inspired by #381192, I decided to check all pages to see if there's any broken origin validation. The results were frustrating since they all seemed to be done properly. However I noticed embedded apps did it in a way that it verifies if the coming origin is the logged-in store. Say if I am an admin on foobar.myshopify.com, then an embedded app will check if in-coming messages originate from https://foobar.myshopify.com. I went ahead to look up some [documentations](https://help.shopify.com/en/api/embedded-apps/embedded-app-sdk/initialization), confirming this is by design (`shopOrigin`):

```javascript
ShopifyApp.init({
  shopOrigin: 'https://CURRENT_LOGGED_IN_SHOP.myshopify.com'
[...]
```

Now this is interesting because by design we can execute any JavaScript on our own stores. That means, I can iframe an embedded app on my store, then post any message to it and it will accept it. So I quickly beautify the SDK source code to see if there's any interesting event. Checking common DOMXSS sinks I found that it registers the `Shopify.API.setWindowLocation` event that navigates to a said destination.

https://cdn.shopify.com/s/assets/external/app.js
```javascript
e.setWindowLocation = function(e) {
    return window.location = e
}, e.bindWindowLocation = function() {
    return _Shopify.Messenger.addHandler("Shopify.API.setWindowLocation", function(e) {
        return function(t, n) {
            return e.setWindowLocation(n)
        }
    }(this))
}
```

By navigate to a *javascript:* pseudo URL it can lead to XSS. This can be verified by opening any embedded apps and execute the following code in the DevTools' console
```javascript
$$('iframe')[0].contentWindow.postMessage('{"message":"Shopify.API.setWindowLocation","data":"javascript:alert(document.domain);0[0]"}','*')
```
{F358299}

**However this XSS is almost useless** because the embedded app is authenticated as us, the attacker. When we try to exploit it on a victim it won't work because they are not logged into our store. So you could say this is, a self DOMXSS. Well, almost. 

What if we use Login CSRF to force a victim to be logged into our store? After the victim is logged in to our store, we can then instruct user's browser to log into the embedded app as us by navigating to `/admin/oauth/authorize`. Then the current logged in store will be ours. I came up with an idea to stuff the session cookies using JavaScript.

The session cookies consist of `_secure_admin_session_id` and `_master_udr`. While I could simply write `_secure_admin_session_id` with `docuemnt.cookie` API, I realized a problem with `_master_udr`. Unlike `_secure_admin_session_id`, `_master_udr` is scoped to `.myshopify.com`. If we triy to write our `_master_udr`, then this will happen:

```http
GET https://canvasfoobar.myshopify.com/admin/oauth/authorize?client_id=d25e45407e508f96409c2dd796e9bd95&redirect_uri=https%3A%2F%2Fscript-editor.shopifycloud.com%2Fauth%2Fshopify%2Fcallback&response_type=code&scope=write_scripts%2Cread_products%2Cread_customers&state=a HTTP/1.1
Host: canvasfoobar.myshopify.com
Cookie: _master_udr=LEGIT; _master_udr=EVIL; _secure_admin_session_id=EVIL
```

The legitimate `_master_udr` will override our evil one and the server will refuse to authenticate as us. There is a trick fortunately. 

>“Cookies with longer paths are listed before cookies with shorter paths.” –RFC 6265

By setting a cookie with a very specific (`/admin/oauth` in this case) we can outrun the original one. The code that we will use to force a login will be:

```javascript
document.cookie = '_secure_admin_session_id=EVIL;path=/admin/oauth';
document.cookie = '_master_udr=EVIL;path=/admin/oauth';
```

Another problem is even after all this, the victim will be logged into the embedded app **as us**. That means, all actions only affect our store. 

To solve this we can simply relog in the victim to the embedded app. Since the victim is still logged in their store, we can navigate the victim to https://victim.myshopify.com/admin/oauth/authorize to trigger the auth flow for the embedded app. The drawback is we need to know which store the victim is logged in as. Luckily https://www.shopify.com/path will redirect to the last logged in store of a user, therefore navigating to https://www.shopify.com/admin/oauth/authorize will lead them to https://victim.myshopify.com/admin/oauth/authorize.

Eventually we have our XSS running on the embedded app's domain running with the victim's session.

#Steps to Reproduce

In the PoC, Script Editor will be used as an example.

1. Be logged into your store as an admin and have [Script Editor](https://apps.shopify.com/script-editor) installed
2. Navigate to https://canvasfoobar.myshopify.com/products/canary
3. After the iframe turns grey, click it
4. After a while, a fake modal dialog will show up and a *New Script* will be created

I'm also attaching a video demo.

#Fix

I recommend fixing this issue by validating the URL for `Shopify.API.setWindowLocation`. The other small issues are by design so they are hard to fix.

## Impact

Perform unauthorized actions on a store admin on any embedded apps.

</details>

---
*Analysed by Claude on 2026-05-12*
