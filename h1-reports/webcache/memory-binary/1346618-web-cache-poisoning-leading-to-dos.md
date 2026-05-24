# Web Cache Poisoning leading to Denial of Service on acquisition-uat.gsa.gov

## Metadata
- **Source:** HackerOne
- **Report:** 1346618 | https://hackerone.com/reports/1346618
- **Submitted:** 2021-09-21
- **Reporter:** letm3through
- **Program:** GSA (General Services Administration)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Web Cache Poisoning, Host Header Injection, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
The acquisition-uat.gsa.gov application is vulnerable to web cache poisoning through manipulation of the Host header. An attacker can poison the cache by sending a request with a malicious Host header, causing the cached response to direct users to an attacker-controlled or non-existent port, resulting in denial of service.

## Attack scenario
1. Attacker identifies that acquisition-uat.gsa.gov caches responses without properly validating the Host header
2. Attacker crafts a request to the application with a modified Host header (e.g., acquisition-uat.gsa.gov:8888) using curl or similar tool
3. The malicious response is cached by the CDN/cache layer, associating the poisoned content with the legitimate URL
4. Subsequent legitimate users visiting the URL receive the poisoned cached response
5. Users' browsers attempt to connect to the non-existent port 8888, generating excessive failed requests
6. Application becomes unavailable or severely degraded due to resource exhaustion from multiple connection attempts

## Root cause
The application does not properly validate or normalize the Host header before caching responses. The caching layer treats requests with different Host headers as separate cache entries without recognizing they are for the same origin, allowing attackers to inject malicious host information into the cache.

## Attacker mindset
The attacker is looking for weaknesses in cache logic and HTTP header handling. They recognize that Host header manipulation combined with caching mechanisms can be weaponized for denial of service attacks with minimal effort. The use of a cache buster parameter shows sophisticated understanding of cache mechanics.

## Defensive takeaways
- Implement strict Host header validation; whitelist only known valid hosts and reject requests with suspicious Host headers
- Configure caching rules to include Host header as part of the cache key, or exclude Host-dependent content from caching
- Implement cache poisoning detection mechanisms that monitor for unusual patterns in cached responses
- Use Content Delivery Networks (CDNs) with built-in protections against Host header attacks
- Implement rate limiting and request throttling to mitigate the impact of poisoned cache entries causing cascading failures
- Regularly audit cache behavior and test for cache poisoning vulnerabilities
- Consider using HTTP/2 or HTTP/3 pseudo-headers (like :authority) which are less susceptible to manipulation

## Variant hunting
Test other URL paths and parameters with malicious Host headers to identify broader cache poisoning scope
Attempt cache poisoning through X-Forwarded-Host and X-Original-Host headers
Test with ports other than 8888 to identify DoS impact patterns
Check if cache poisoning can be combined with stored XSS or other injection attacks
Investigate whether the vulnerability affects other GSA subdomains or related applications
Test cache poisoning with HTTPS and mixed protocol scenarios
Examine if caching rules differ between GET requests and other HTTP methods

## MITRE ATT&CK
- T1190
- T1499
- T1498

## Notes
This is a UAT environment vulnerability, reducing real-world impact but still significant for security posture. The straightforward reproduction steps indicate the vulnerability is easily exploitable. The attacker's use of a cache buster parameter demonstrates understanding of cache mechanics and suggests this may be discovered through methodical security testing rather than accidental exploitation.

## Full report
<details><summary>Expand</summary>

## Summary:
`acquisition-uat.gsa.gov` is vulnerable to web cache poisoning that can lead to Denial of Service (DoS) in the application.

## Steps To Reproduce:
1. Visit https://acquisition-uat.gsa.gov/?letme=4449 to make sure the service is available.
*Note: `letme=4449` is used as cache buster as we do not want to poison the application without parameter.*
2. Poison the link using `curl` command
```
curl https://acquisition-uat.gsa.gov/\?letme\=4447 -H "Host: acquisition-uat.gsa.gov:8888"
```
3. Visit https://acquisition-uat.gsa.gov/?letme=4449 to verify that application is in the state of DoS as it attempts to make plenty of requests to `acquisition-uat.gsa.gov:8888`.

## Impact

The attacker can carry out web cache poisoning to prevent others from accessing the application.

</details>

---
*Analysed by Claude on 2026-05-24*
