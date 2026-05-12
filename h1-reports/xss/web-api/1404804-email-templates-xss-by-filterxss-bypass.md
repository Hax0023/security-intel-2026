# Email Templates XSS via js-xss Filter Bypass Leading to Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 1404804 | https://hackerone.com/reports/1404804
- **Submitted:** 2021-11-19
- **Reporter:** caue
- **Program:** Judge.me
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Cross-Site Scripting (XSS), Filter/WAF Bypass, Clickjacking, CSP Bypass, Authentication Bypass (HMAC), Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A Self-XSS vulnerability in email template previews exploits improper parsing differences between the js-xss library and browsers to bypass sanitization filters. The attacker chains this with HMAC-based authentication and CSP bypass to achieve single-click account takeover and leak sensitive authentication tokens.

## Attack scenario
1. Attacker crafts malicious email template using HTML payload `<![endif]-- onerror=... onload=...>` that exploits js-xss parser differences
2. Attacker tricks victim into clicking HMAC-authenticated link that auto-logs victim into attacker's account and previews the malicious template
3. XSS payload executes in victim's browser context with victim's authentication cookies intact
4. Attacker uses XSS to dynamically load iframes on subdomain (www.judge.me) bypassing CSP frame-ancestors restrictions
5. Attacker loads victim's protected pages as iframes and exfiltrates HTML content via same-origin access to parent.frames[0]
6. Attacker performs clickjacking on settings page button to trick victim into revealing private API token for account complete takeover

## Root cause
The js-xss library's `onIgnoreTag` custom handler has inconsistent tag parsing logic compared to browser HTML parsers. Specifically, malformed CDATA-like syntax `<![endif]--` is parsed differently, allowing attribute injection. Additionally, HMAC authentication tokens lack proper validation scope, and CSP policy allows same-domain subdomains enabling frame escape attacks.

## Attacker mindset
Sophisticated attacker combining multiple vulnerability classes (XSS + auth bypass + CSP bypass + clickjacking) into a single account takeover chain. Demonstrates deep knowledge of HTML parsing quirks, authentication mechanisms, and browser security models. Uses legitimate features (HMAC auth, email templates) as attack vectors.

## Defensive takeaways
- Never rely solely on library security assumptions; test sanitizers against actual browser parsing behavior
- Implement strict Content-Security-Policy with frame-ancestors that excludes all subdomains, use frame-src as secondary control
- Validate HMAC/authentication tokens with multiple factors: origin, referer, user-agent, timestamp; avoid single-factor token validation
- Treat Self-XSS as critical if it can be cross-domain escalated or combined with social engineering
- Require explicit user consent (not clickjacking-vulnerable buttons) for sensitive token generation
- Use SameSite=Strict cookies and additional origin validation on cross-subdomain requests
- Implement frame-busting and X-Frame-Options as defense-in-depth against clickjacking

## Variant hunting
Search for other uses of js-xss with custom `onIgnoreTag` handlers with permissive rules
Test for HMAC/token authentication that validates insufficient parameters (missing referer, user-agent, timestamp)
Hunt for CSP policies allowing *.domain.com that can be bypassed via subdomain XSS
Look for sensitive endpoints protected by single Referer header validation instead of origin/host
Search for clickjacking-vulnerable buttons on administrative/settings pages that generate tokens

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing: Spearphishing Link
- T1566 - Phishing: Email
- T1200 - Traffic Signaling
- T1539 - Steal Web Session Cookie
- T1113 - Screen Capture
- T1056 - Input Capture

## Notes
This is a chain of 5+ distinct vulnerabilities combined into single attack: XSS filter bypass + HMAC auth token replay + CSP misconfiguration + same-origin policy exploitation + clickjacking. The critical insight is that Self-XSS becomes account takeover when combined with authentication bypass (HMAC) and the attacker can force victim context. The HMAC authentication feature is the single biggest weakness - it should require additional validation beyond just query parameters.

## Full report
<details><summary>Expand</summary>

## Summary:
`js-xss` is used to prevent XSS on email templates previews but the custom `onIgnoreTag` function can be used to bypass this filter. This leads to a Self-XSS scenario that can be used to achieve Account Takeover in 1-click.

```js
onIgnoreTag: function (e, t) {
   return "!--[if" === e || "![endif]--" === e || "<!-->" === t ? t : void 0; 
},
```

## XSS

The way how `js-xss` parse tags starting with `<![` differ from how browser parse it, so it's possible to abuse this in this way:
```html
<![endif]-- onerror="<![endif]-->" onload="<img src=1 onerror='alert(1)' />">
```
Sending this as the HTML email template will trigger an XSS when the email is previewed. Since email templates are private and only the owner of the template can preview it, this can be considered a Self-XSS. But there is a way to do another user preview it, leading to an account takeover in 1-click.
We can use HMAC authentication feature to force another user login in our account and preview the malicious email:
```
https://www.judge.me/shop/emails/2243518/edit?no_iframe=1&shop_domain=wordpress.caueo.me&platform=woocommerce&hmac=████
```
This URL authenticates as admin on `wordpress.caueo.me` domain, where the malicious email will be. The HMAC hash is created on this way (taken from wordpress plugin):
```php
$hmac       = hash_hmac( 'sha256', "no_iframe=1&platform=woocommerce&shop_domain={$domain}", $token, false );
```

Having this XSS with the victim logged in my account is possible to leak HTML content of a page that was loaded with victim's account cookie:

1. Load an iframe with the victim's page (HTML content to leak) - Authenticated as victim
2. Load another iframe with the XSS (Use HMAC authentication) - Authenticated as me
3. We can use the XSS to read `parent.frames[0]` HTML content since it is same-origin

## CSP bypass
At a first sight we can't load an iframe to victim's page, since it has a CSP that whitelists iframe origins:
```
frame-ancestors https://wordpress.caueo.me http://wordpress.caueo.me wordpress.caueo.me https://woocommerce-adapter.judge.me/ *.judge.me
```
To bypass it we can use the XSS to load the iframes, but we need to do it on another subdomain, because to trigger this XSS is needed to login in my account and then it would not be possible to load the victim's page authenticated as victim's account later. So we trigger the XSS on `www.judge.me` subdomain.

## Limitation to 0-click account takeover
At this point it is already **possible to read HTML content of almost any page authenticated as victim**. To achieve account takeover we only need to get the private API token from victim because it is used as the key of HMAC authentication.
The problem is that the endpoint that retrieves the API private token checks if the `Referer` header starts with `https://judge.me/settings`, so is not possible to load this endpoint in an iframe.

## Clickjacking
We can load an iframe to `https://judge.me/settings` where has a button that retrieves the API token from the endpoint successfully. So it is possible to perform a clickjacking to that button, and if the victim clicks on it, we can get the API private token. 

## PoC
I made a PoC on how is possible to perform this account takeover with user interaction and leak some stuffs without user interaction.
[PoC](https://www.judge.me/shop/emails/2243518/edit?no_iframe=1&shop_domain=wordpress.caueo.me&platform=woocommerce&hmac=█████████)

In this PoC I leaked FreshChat token without clickjacking, so we can impersonate another user in support chat without needing a user click.

## Impact

Shop account takeover (user interaction)
Impersonation on support chat
Private content leak

</details>

---
*Analysed by Claude on 2026-05-12*
