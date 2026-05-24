# Cache Poisoning Leading to Denial of Service (CPDoS) - Bypass of Previous Fix

## Metadata
- **Source:** HackerOne
- **Report:** 1322732 | https://hackerone.com/reports/1322732
- **Submitted:** 2021-08-29
- **Reporter:** brumens
- **Program:** Undisclosed
- **Bounty:** Undisclosed
- **Severity:** High
- **Vuln:** Cache Poisoning, Denial of Service, HTTP Response Splitting, Host Header Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
A cache poisoning vulnerability allows attackers to poison the web cache by injecting malicious port numbers in the Host header, causing 301 redirects to be cached with false values. This bypasses a previous fix (#1198434) by exploiting different paths on the domain, enabling denial of service attacks. An attacker can repeatedly refresh the poisoned cache to keep affected paths unavailable to all users.

## Attack scenario
1. Attacker identifies a target domain path that lacks proper cache poisoning protections
2. Attacker crafts an HTTP request with a random URL parameter (e.g., &CPDoS=1) and injects a non-existent port number in the Host header (e.g., Host: example.com:1234)
3. The vulnerable server processes the request and generates a 301 redirect response containing the injected port number
4. The web cache server stores this poisoned 301 response with the malicious port value
5. Attacker removes the port from Host header and resends the request; the cached poisoned response is served
6. All subsequent users visiting the path receive the poisoned 301 redirect, causing service unavailability and denial of service

## Root cause
Insufficient cache key normalization and Host header validation across all application paths. The remediation for report #1198434 only addressed specific paths, leaving other paths vulnerable to the same cache poisoning technique. The web cache server fails to properly validate and sanitize the Host header before caching 301 redirect responses.

## Attacker mindset
Methodical reconnaissance to find paths not covered by the previous fix; persistence through automated cache refresh attacks to maintain denial of service; understanding of HTTP caching mechanics and redirect behavior to maximize impact across the entire domain.

## Defensive takeaways
- Implement consistent Host header validation and normalization across ALL application paths and endpoints
- Configure cache servers to exclude or properly validate Host header-based variations in cache keys
- Implement rate limiting and request throttling to prevent automated cache poisoning attacks
- Use cache busting headers (Cache-Control, Vary) to limit caching of redirect responses
- Conduct comprehensive security testing on all paths, not just those reported as vulnerable
- Implement monitoring and alerting for unusual redirect patterns or Host header anomalies
- Apply security headers like X-Original-URL validation and strict Host header verification

## Variant hunting
Test alternative HTTP ports in Host header injection on different application paths
Attempt cache poisoning via X-Forwarded-Host and other proxy-related headers
Explore poisoning with different HTTP methods (GET, POST, HEAD) to bypass protections
Test with URL encoding and case variation of parameters to evade detection
Investigate subdomain paths and API endpoints for similar cache poisoning vulnerabilities
Attempt to poison cache with different redirect status codes (302, 303, 307, 308)

## MITRE ATT&CK
- T1190
- T1499
- T1499.004

## Notes
This report demonstrates a critical bypass of a previous security fix, indicating incomplete remediation. The vulnerability relies on improper cache key construction that fails to normalize the Host header. The attacker leverages the predictable behavior of redirect caching to achieve persistent denial of service. The use of random URL parameters helps bypass simple path-based caching strategies. This type of vulnerability is particularly dangerous because it affects all users of the service, not just the attacker.

## Full report
<details><summary>Expand</summary>

#Vulnerability Cache Posioning (CPDoS)
**C**ache **P**osioning **D**enial **O**f **S**ervice (CPDoS) [1] is taking advantage of 301 redirects by storing an false value of either domain, port or header that effect the response in any way. This makes the cache server store the false value and later delivery it to all users that view the domain page.
This vulnerability is in fact an Cache poisoning [2] in the ground which makes it possible to not harm the system in any way when testing. This is because it's possible to add random URL path to the domain that make only that path exploited under x time.
An attacker will use intruder to update the cache server every x sec, min or hours to make the domain down.

#Summary
The vulnerability was discovered when  was retesting the vulnerability and discovered that the domain still was vulnerable for cache poisoning. I did some tests and I was able to re poisoning the domains cache server again in different paths. It looks like the fix from report *#1198434* only fixed one path in the domain but other paths remain vulnerable.

# Proof of concept
*Can be used as step by step if you like*

█████████

Supported link
[1] https://cpdos.org/ - "What is CPDoS?", Vulnerability explained
[2] https://portswigger.net/research/responsible-denial-of-service-with-web-cache-poisoning - "Responsible denial of service with web cache poisoning", James Kettle

Best regards,
Brumens

## Impact

An attacker is able to crash most of the paths related to the domain.

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
**WARNING!** Do not send the request until the step to send the request comes. Otherwise you can by mistage crash the whole domain.
1. Open an browser that is connected to Burp suite
2. Visit: https://██████████/██████████ (*More path are vulnerable but this is an example*)
3. Intercept the request with Burp suite and add it to the repeater.
**IMPORTEN** Add an random parameter at the end as example: &CPDoS=1 in the url bar at *Repeater*. (*See image at step 4.*)
4. Add an nonexcisting port at the host header domain. Ex: 1234 Your request raw data should look like below:
█████ 
If an random paramter is added at the end AND the port is added to the host header. You can now send the request in Burp suite repeater tab. The data will look similary to:

5. You will see an 301 that do redirect and reflect the port you gave inside the request.
In the request raw data. Delete the port number inside the host header.
Send the request now one more time. You will see the port you added before is still reflecting in the 301 redirect code. This indicates that it's now cache poisoned and the domain path is down. Try visit the url and you can see you won't be able to load it.

## Suggested Mitigation/Remediation Actions
Configure the cache server on all paths and locations on the domain.



</details>

---
*Analysed by Claude on 2026-05-24*
