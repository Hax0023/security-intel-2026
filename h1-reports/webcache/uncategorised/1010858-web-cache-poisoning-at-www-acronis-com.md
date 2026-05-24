# Web Cache Poisoning at www.acronis.com via X-Forwarded Headers

## Metadata
- **Source:** HackerOne
- **Report:** 1010858 | https://hackerone.com/reports/1010858
- **Submitted:** 2020-10-18
- **Reporter:** 9529
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Web Cache Poisoning, Cache Key Injection, HTTP Request Smuggling (related), Potential XSS amplification vector
- **CVEs:** None
- **Category:** uncategorised

## Summary
The attacker discovered that www.acronis.com's caching mechanism is vulnerable to poisoning through the manipulation of X-Forwarded-Port and X-Forwarded-URL headers, which influence cache key generation without proper validation. By injecting malicious headers and URL parameters, an attacker can poison the cache such that subsequent legitimate users receive the compromised response, enabling widespread distribution of XSS payloads or other malicious content.

## Attack scenario
1. Attacker crafts a request to /zh-cn/careers/ with a malicious X-Forwarded-Port header value that causes a cache miss or creates a distinct cache entry
2. Attacker adds URL parameters and reflected content designed to trigger XSS or other vulnerabilities if they exist on the page
3. Attacker repeats requests until the poisoned response is cached by the CDN/caching layer, evidenced by the appearance of the attacker-controlled port in responses
4. Attacker then sends a clean request (without the malicious headers) to the same URL, causing a cache hit with the poisoned content
5. Legitimate users subsequently request the same URL and receive the cached poisoned response containing injected malicious code
6. If the page reflects user input without proper sanitization, the XSS payload executes in victims' browsers without direct attacker-victim interaction

## Root cause
The caching layer includes untrusted/unvalidated request headers (X-Forwarded-Port, X-Forwarded-URL, potentially query parameters) in the cache key generation logic. These headers are commonly used for routing behind proxies/CDNs, but the application fails to normalize or exclude them when determining cache entries. Additionally, the application may reflect these values in responses without sanitization, creating a dual vulnerability.

## Attacker mindset
An attacker seeks to achieve persistent malicious code injection with minimal user interaction. By poisoning shared caches, they can amplify the impact of reflected XSS or other client-side vulnerabilities to reach many users simultaneously without social engineering or phishing. This is attractive because the victims receive the malicious content from a trusted domain (acronis.com), bypassing user skepticism and trust boundaries.

## Defensive takeaways
- Implement strict cache key normalization: exclude or validate X-Forwarded-* headers and ensure they don't influence cache keys unless explicitly required and properly canonicalized
- Use allowlists for headers that influence caching decisions; reject or normalize suspicious header values
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if cache poisoning occurs
- Sanitize and HTML-encode all reflected user input (URL parameters, headers) before rendering in responses
- Configure caching rules to avoid caching responses with user-controlled input variations; cache only stable content
- Monitor cache hit ratios and implement anomaly detection for unusual cache patterns
- Apply defense-in-depth: validate headers at both the caching layer and application layer
- Use Vary header appropriately to ensure semantically different requests do not share cache entries
- Implement cache purging mechanisms and audit logging for cache operations

## Variant hunting
Search for similar cache poisoning vulnerabilities by: (1) Testing other X-Forwarded-* headers (X-Forwarded-Host, X-Forwarded-Proto, X-Forwarded-For) on other endpoints and subdomains; (2) Checking if other reflected headers (User-Agent, Accept-Language, custom headers) influence cache keys; (3) Testing parameter pollution and multi-value headers to bypass cache normalization; (4) Examining static asset caching (CSS, JS) for poisoning via Referer or Origin headers; (5) Testing subdomain takeover combined with cache poisoning for enhanced impact; (6) Investigating if cache poisoning can be combined with open redirect vulnerabilities already present on the site

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information (distributing XSS via cache)
- T1566 - Phishing (cache-poisoned pages delivered to victims)
- T1203 - Exploitation for Client Execution (XSS via cached poisoned content)

## Notes
The researcher provided excellent references to PortSwigger's cache poisoning research. The vulnerability is particularly dangerous because it operates at the infrastructure layer (caching), making it difficult for end users to detect. The attack succeeds even if there is no stored XSS on the backend—it only requires reflected parameters or headers to be rendered in responses. The researcher's methodology of using distinct markers (yig1bt7ai4) to track cache hits is sound. This vulnerability class has been under-reported historically but is gaining recognition as critical. Organizations using CDNs/reverse proxies must ensure proper cache key design and header normalization.

## Full report
<details><summary>Expand</summary>

## Summary
I found the problem of cache poisoning in www.acronis.com. A poisoned web cache can potentially be a devastating means of distributing numerous different attacks, exploiting vulnerabilities such as XSS, JavaScript injection, open redirection, and so on.

## Steps To Reproduce

1. Use x-forwarded-port to destroy the cache, repeat the request until www.acronis.com:0 appears in the response  
```
GET /zh-cn/careers/?yig1bt7ai4=1 HTTP/1.1
Host: www.acronis.com
Connection: close
sec-ch-ua: "Chromium";v="86", "\"Not\\A;Brand";v="99", "Google Chrome";v="86"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 yig1bt7ai4
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9, text/yig1bt7ai4
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://www.acronis.com/zh-cn/cloud/cyber-protect/
Accept-Encoding: gzip, deflate, yig1bt7ai4
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
x-forwarded-port: zwrtxqvas9lm4kzkia
Origin: https://yig1bt7ai4.com
```

2. Remove the parameters, x-forwarded-port, and origin in the request header. Then send the request, the cache has been polluted (due to the cache hit, it may take several more requests).  
```
GET /zh-cn/careers/ HTTP/1.1
Host: www.acronis.com
Connection: close
sec-ch-ua: "Chromium";v="86", "\"Not\\A;Brand";v="99", "Google Chrome";v="86"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 yig1bt7ai4
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9, text/yig1bt7ai4
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://www.acronis.com/zh-cn/cloud/cyber-protect/
Accept-Encoding: gzip, deflate, yig1bt7ai4
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
```

3.Other users visit the /zh-cn/careers/ page, and the result has been poisoned.
4.The currently discovered causes of cache poisoning:
  - url params (if there is reflected XSS on the server side, it will be very dangerous)
  - x-forwarded-port header
  - x-forwarded-url header

## Recommendations
Cache poisoning is caused by different requests hitting the same cache. Remove these influencing factors, or only cache requests with unchanged results.

## Impact

1. Launch a denial of service attack
2. If a page contains url parameters or request header reflection XSS, cache poisoning can easily spread the page containing malicious code to other people without the need to communicate with the victim

More ways to exploit:
https://portswigger.net/research/practical-web-cache-poisoning
https://portswigger.net/research/web-cache-entanglement

</details>

---
*Analysed by Claude on 2026-05-24*
