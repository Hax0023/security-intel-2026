# Cache Poisoning Leading to Denial of Service via Host Header Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1198434 | https://hackerone.com/reports/1198434
- **Submitted:** 2021-05-15
- **Reporter:** brumens
- **Program:** Undisclosed (redacted)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cache Poisoning, HTTP Response Splitting, Denial of Service, Host Header Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
A cache poisoning vulnerability was discovered where an attacker can manipulate the Host header with a non-existent port number, causing a 301 redirect that reflects the malicious port. This poisoned response is cached and served to all subsequent users, effectively rendering the domain inaccessible. The vulnerability leverages improper cache key construction that includes the Host header without validation.

## Attack scenario
1. Attacker identifies an endpoint vulnerable to Host header reflection in 301 redirects (e.g., www.example.com/path)
2. Attacker adds a random URL parameter (&CPDoS=1) to ensure the request is cacheable but initially isolated
3. Attacker injects a malicious port number in the Host header (e.g., Host: www.example.com:1234)
4. The server responds with a 301 redirect that reflects the malicious port in the Location header
5. The cache server stores this poisoned response with the malicious port as part of the cache key or response content
6. Subsequent legitimate users requesting the domain receive the poisoned cached response, causing connection failures to the incorrect port

## Root cause
The cache server includes the Host header in the cache key without proper validation and normalization. When a 301 redirect reflects the Host header value back in the response, a malicious port injected into the Host header gets cached. The server likely fails to validate or sanitize the Host header before using it in redirect responses, and the caching layer does not exclude host-variant requests from caching.

## Attacker mindset
An opportunistic attacker discovered this while fuzzing for SSRF vulnerabilities. They recognized the severity upon observing Host header reflection in 301 responses and understood that poisoning the cache with an invalid port would render the service unavailable. A real attacker would remove the random parameter to poison the main path, maximizing impact across all users without limiting it to a specific URL variant.

## Defensive takeaways
- Implement strict Host header validation; reject requests with non-standard ports or malicious values
- Configure cache servers to exclude Host header from cache key generation or use normalized, validated host values only
- Never reflect user-controlled input (especially headers) directly in redirect responses without sanitization
- Use cache key normalization to prevent header-based cache poisoning attacks
- Implement cache poisoning detection by monitoring for unusual port numbers or invalid host values in cached responses
- Apply request normalization before caching to prevent variant attacks
- Consider implementing Cache-Control headers that prevent caching of redirects with user-controlled input
- Use HTTP/2 or HTTP/3 which have improved header handling and validation

## Variant hunting
Test other redirect status codes (302, 307, 308) for similar reflection vulnerabilities
Attempt header injection in other headers (X-Forwarded-For, X-Original-Host, Referer) that might be reflected or cached
Look for cache poisoning via query parameters that affect redirect Location headers
Test whether Path Traversal payloads in Host header get cached and reflected
Investigate if protocol switching (http vs https) in Host header manipulation affects caching
Test CDN-specific headers or cache-control directives that might be bypassable
Attempt to poison cache via X-Forwarded-Host or similar proxy headers if present

## MITRE ATT&CK
- T1190
- T1561
- T1499

## Notes
This report demonstrates responsible disclosure - the researcher used a random parameter to isolate the cache poisoning effect and explicitly warned against full exploitation. The POC video and HTTP request data are referenced but redacted in this writeup. The vulnerability is particularly dangerous because it requires minimal interaction and can affect all users accessing the domain. The attacker mindset section reveals the key insight: removing the random parameter would enable complete domain-wide denial of service. No CVE was assigned at the time of reporting.

## Full report
<details><summary>Expand</summary>

*Hey!
To be clear. This was not an test for Denial of service (DOS). I accidentally come a cross this vulnerability when I was testing for Server side request forgery (SSRF). I have read you policy well and I was not preforming any type of activity that harmed or slowed you system in anyway. You can read why below when I explain the cache poisoning vulnerability that is the core of the impact.*

# Vulnerability Cache Posioning (CPDoS)

**C**ache **P**osioning **D**enial **O**f  **S**ervice (CPDoS) [1] is taking advantage of *301* redirects by storing an false value of either domain, port or header that effect the response in any way. This makes the cache server store the false value and later delivery it to all users that view the domain page.

This vulnerability is in fact an Cache poisoning [2] in the ground which makes it possible to not harm the system in any way when testing. This is because it's possible to add random URL path to the domain that make only that path exploited under *x* time.

An attacker will use intruder to update the cache server every x sec, min or hours to make the domain down. 

# Summary

The vulnerability was discovered when I was testing for SSRF in the host header field.  I notice that it was behaving weard so I added an random parameter in the URL field of the domain that made it redirect with code *301*. This ended up in an reflection of the URL bar in the response.

When the URL of the redirect was reflected I was able to add an random port number and store it into the cache server.

#Proof Of Concept
███

**Supported link**
[1] https://cpdos.org/ - "What is CPDoS?", *Vulnerability explained*
[2]  https://portswigger.net/research/responsible-denial-of-service-with-web-cache-poisoning - "Responsible denial of service with web cache poisoning", *James Kettle*

Best regards,
Alex

## Impact

An attacker is able to Cache posioning the host header. This makes the cache server to store an incorrect port number from the server response and deliver out that incorrect domain and port combined to all users that try access the domain. This make the domain crash and unable to view for users.

**Attackers view**
*For an real attacker to take use of this he/she will disable the random paramter at the url and send it to the home direcly. This will make the domain crash fully*

## System Host(s)
www.███

## Affected Product(s) and Version(s)
/███████

## CVE Numbers


## Steps to Reproduce
**WARNING!** Do not send the request until the step to send the request comes. Otherwise you can by mistage crash the whole domain.

1. Open an browser that is connected to Burp suite
2. Visit: *https://www.███/█████?█████████*
3. Intercept the request with Burp suite and add it to the repeater.
4. **IMPORTEN** Add an random parameter at the end as example: *&CPDoS=1* in the url bar. (*See video POC*).
4. Add an nonexcisting port at the host header domain. Ex: *1234* Your request raw data should look like below:
{F1302641}
5. If an random paramter is added at the end *AND* the port is added to the host header. You can now send the request in Burp suite repeater tab.
The data will look similary to:
```
GET /████████?███████CPDoS=1 HTTP/1.1
Host: www.██████:1234
```
6. You will see an 301 that do redirect and reflect the port you gave inside the request.
7. In the request raw data. Delete the port number inside the host header.
8. Send the request now one more time. You will see the port you added before is still reflecting in the 301 redirect code.
This indicates that it's now cache poisoned and the domain path is down. Image: * FullRequest.png*
████████ <- Might not render...

## Suggested Mitigation/Remediation Actions
Configure the cache server to not store the host header.



</details>

---
*Analysed by Claude on 2026-05-24*
