# Web Cache Poisoning leading to Denial of Service on acquisition-uat.gsa.gov

## Metadata
- **Source:** HackerOne
- **Report:** 1346618 | https://hackerone.com/reports/1346618
- **Submitted:** 2021-09-21
- **Reporter:** letm3through
- **Program:** GSA (General Services Administration) - Acquisition Portal
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Web Cache Poisoning, HTTP Host Header Injection, Denial of Service
- **CVEs:** None
- **Category:** memory-binary

## Summary
The acquisition-uat.gsa.gov application fails to properly validate the Host header, allowing an attacker to poison the web cache by injecting a malicious host header (acquisition-uat.gsa.gov:8888). When cached responses are served to legitimate users, the application attempts to make requests to the injected host, causing resource exhaustion and denial of service.

## Attack scenario
1. Attacker crafts a malicious HTTP request to acquisition-uat.gsa.gov with an injected Host header pointing to a non-existent or attacker-controlled port (8888)
2. The vulnerable application caches this response without properly validating the Host header
3. Subsequent legitimate user requests are served the poisoned cached content containing the malicious host reference
4. Application attempts to make backend requests to the injected host (acquisition-uat.gsa.gov:8888) which either times out or consumes excessive resources
5. Resource exhaustion occurs as many users receive poisoned cache entries triggering repeated connection attempts
6. Legitimate users experience denial of service as the application becomes unresponsive

## Root cause
The application does not properly validate or normalize the Host header before caching responses. The caching mechanism treats requests with different Host headers as distinct cache entries, but the backend processing uses the injected host header for subsequent requests without validation, leading to resource exhaustion.

## Attacker mindset
An attacker would recognize that web caches often use request headers (including Host) as cache key components. By injecting an invalid Host header, they can poison cache entries that will be served to all subsequent users, causing widespread disruption without needing to target individual users directly. This provides a high-impact attack surface with minimal effort.

## Defensive takeaways
- Implement strict Host header validation - maintain a whitelist of allowed hosts and reject requests with invalid Host headers
- Normalize Host headers before using them in cache keys to prevent cache poisoning via header variations
- Do not include untrusted headers (like Host) in cache keys without careful consideration
- Implement cache key specification standards (RFC 7234) and ensure consistent cache behavior
- Add rate limiting and circuit breakers for backend connection attempts to mitigate DoS impact
- Monitor for suspicious Host header variations in access logs
- Use Security header validation at the WAF/reverse proxy level before requests reach the origin server
- Implement connection timeouts and resource limits for backend requests

## Variant hunting
Test other headers commonly used in cache keys (X-Forwarded-Host, Referer, X-Original-URL) for similar poisoning
Attempt cache poisoning with different port numbers to identify resource exhaustion patterns
Test if other URL parameters can be chained with Host header injection for amplified impact
Check if the vulnerability affects different application endpoints or only specific paths
Investigate if query string parameters interact with Host header validation logic
Test for cache poisoning on related subdomains (*.gsa.gov) that may share cache infrastructure

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1561 - Disk Wipe
- T1499 - Endpoint Denial of Service
- T1499.004 - Application Exhaustion Flood
- T1657 - Financial Theft

## Notes
This vulnerability demonstrates the critical importance of proper HTTP header validation in cached content. The use of a cache buster parameter (letme=4449) during testing shows good security research practice. The UAT environment designation suggests this should have been caught before production deployment. Web cache poisoning is particularly dangerous because it affects all users indiscriminately and can be difficult to detect without proper logging. The attacker requires no authentication and can conduct the attack with simple curl commands, indicating low exploitation barriers.

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
