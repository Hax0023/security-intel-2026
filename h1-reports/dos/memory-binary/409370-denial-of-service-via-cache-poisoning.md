# Denial of Service via Cache Poisoning with X-Forwarded-Port/Host Headers

## Metadata
- **Source:** HackerOne
- **Report:** 409370 | https://hackerone.com/reports/409370
- **Submitted:** 2018-09-13
- **Reporter:** albinowax
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cache Poisoning, HTTP Header Injection, Denial of Service, Open Redirect
- **CVEs:** None
- **Category:** memory-binary

## Summary
The application caches redirect responses without properly validating the X-Forwarded-Port and X-Forwarded-Host headers, allowing attackers to inject malicious redirect URLs. An attacker can poison the cache with redirects pointing to invalid ports, causing all subsequent users to receive the poisoned cached response and experience denial of service.

## Attack scenario
1. Attacker crafts a request with X-Forwarded-Port: 123 or X-Forwarded-Host: www.hackerone.com:123 header
2. Attacker sends request to a redirect endpoint on www.hackerone.com
3. Server processes the header and generates a redirect response to the invalid port
4. Response is cached by CDN/cache layer without validation
5. Subsequent legitimate users request the same endpoint
6. Users receive cached redirect to invalid port, causing connection failure and DoS

## Root cause
The application trusts X-Forwarded-* headers (proxy headers) without validation and includes them in redirect responses. These headers are then cached by the caching layer, allowing attackers to persistently poison the cache with malicious redirects targeting invalid endpoints.

## Attacker mindset
An attacker recognizes that web applications often blindly trust proxy headers for determining the original request scheme/host, and that caching layers typically cache based on URL without considering header variations. By crafting a request with a valid URL but malicious headers, the attacker can inject poisoned content into the cache that affects all subsequent users.

## Defensive takeaways
- Never blindly trust X-Forwarded-* headers without validating they match expected domains and ports
- Implement strict validation for redirect destinations against a whitelist
- Cache based on normalized headers, excluding user-controlled or proxy-specific headers from cache keys
- Only trust X-Forwarded-* headers from known proxy IPs
- Consider disabling or restricting X-Forwarded-Host header processing
- Implement cache headers with short TTLs or Cache-Control: private for redirects
- Monitor and alert on unusual redirect patterns

## Variant hunting
Test other proxy headers: X-Forwarded-Proto, X-Forwarded-For, X-Original-URL, X-Rewrite-URL
Attempt cache poisoning on other redirect endpoints or dynamic content
Test combinations of headers to bypass validation logic
Check if cache poisoning affects different request methods (GET, POST, HEAD)
Investigate if query parameters affect cache key normalization
Test cache poisoning with path traversal in redirect destinations

## MITRE ATT&CK
- T1190
- T1499

## Notes
This is a classic cache poisoning vulnerability leveraging trusted proxy headers. The attack is particularly effective because it's persistent (affects all users until cache expires) and easy to execute. The research references PortSwigger's cache poisoning methodology, indicating this may be a known attack vector in the wild. The query parameter 'dontpoisoneveryone=1' suggests the researcher exercised responsible disclosure by limiting scope.

## Full report
<details><summary>Expand</summary>

An attacker can persistently block access to any/all redirects on www.hackerone.com by using cache poisoning with the X-Forwarded-Port or X-Forwarded-Host headers to redirect users to an invalid port.

To replicate: 
```curl -H 'X-Forwarded-Port: 123' https://www.hackerone.com/index.php?dontpoisoneveryone=1```
Then try to load https://www.hackerone.com/index.php?dontpoisoneveryone=1 in your browser.

This attack can also be done using the X-Forwarded-Host header:
```curl -H 'X-Forwarded-Host: www.hackerone.com:123' https://www.hackerone.com/index.php?dontpoisoneveryone=1```


For more information on the theory behind this attack, check out https://portswigger.net/blog/practical-web-cache-poisoning

## Impact

An attacker can persistently block access to any/all redirects on www.hackerone.com

</details>

---
*Analysed by Claude on 2026-05-24*
