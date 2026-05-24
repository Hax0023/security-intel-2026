# Failure to strip Proxy-Authorization header on change in origin

## Metadata
- **Source:** HackerOne
- **Report:** 3180396 | https://hackerone.com/reports/3180396
- **Submitted:** 2025-06-06
- **Reporter:** grahamcampbell
- **Program:** PHP Guzzle HTTP package
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Information Disclosure, Header Leakage, Improper Credential Handling
- **CVEs:** None
- **Category:** web-api

## Summary
The Guzzle HTTP client (via curl) fails to strip the Proxy-Authorization header when following redirects to different origins, exposing proxy credentials to untrusted hosts. This mirrors a similar vulnerability recently patched in Go (CVE-2025-4673) and represents a critical oversight in credential sanitization during cross-origin redirects.

## Attack scenario
1. Attacker controls or monitors a secondary server on a different domain
2. Attacker tricks a user/application into making an HTTP request to their primary server using Guzzle with proxy authentication enabled
3. Primary server responds with HTTP 301/302 redirect pointing to the attacker's secondary server on different origin
4. Guzzle follows the redirect and sends the follow-up request to the attacker's secondary server
5. Proxy-Authorization header is retained in the redirect request (unlike Authorization and Cookie headers)
6. Attacker captures the Proxy-Authorization header and gains proxy credentials to impersonate the victim

## Root cause
The Guzzle HTTP library inherits curl's header-stripping logic during redirects, which properly removes Authorization and Cookie headers on origin change but fails to remove Proxy-Authorization header. This creates an asymmetric security posture where sensitive proxy credentials are leaked while other credentials are protected.

## Attacker mindset
An attacker would exploit this by setting up a malicious redirect endpoint or intercepting legitimate redirects to capture proxy credentials. This is especially valuable in corporate environments where proxy authentication provides access to internal resources or egress filtering bypass.

## Defensive takeaways
- Implement strict header stripping policies that treat Proxy-Authorization with same priority as Authorization and Cookie headers during cross-origin redirects
- Audit all HTTP client libraries for inconsistent credential handling across different header types
- Monitor upstream library vulnerabilities (curl, underlying HTTP implementations) and promptly apply similar fixes
- Consider disallowing automatic redirect following when proxy authentication is active, requiring explicit user approval
- Implement header filtering at application level as defense-in-depth measure independent of library behavior
- Add security tests specifically validating credential stripping behavior during cross-origin redirects

## Variant hunting
Search for similar header-stripping inconsistencies in: (1) Other HTTP client libraries (urllib3, requests, httpx, node-fetch); (2) Different header types that may carry sensitive data (Authorization, X-API-Key, X-Auth-Token, X-Access-Token); (3) Other redirect scenarios beyond origin change (scheme change, port change, HTTPS->HTTP downgrades); (4) Proxy header variants (Proxy-Authorization vs Proxy-Connection vs Proxy-Authenticate)

## MITRE ATT&CK
- T1190
- T1598
- T1040
- T1557

## Notes
This vulnerability follows CVE-2025-4673 in Go, indicating this is a systemic issue across multiple HTTP implementations. The fact that curl already has this issue and Guzzle inherits it highlights the importance of independent security reviews rather than assuming upstream libraries have solved all security problems. The selective stripping of Authorization/Cookie but not Proxy-Authorization suggests this was an oversight rather than intentional design. Cross-origin redirect handling is a critical security boundary that deserves comprehensive testing.

## Full report
<details><summary>Expand</summary>

## Summary:

Failure to strip Proxy-Authorization header on change in origin.

AI was not used. I maintain the PHP Guzzle HTTP package which uses curl, and noticed we have the same issue as curl in this regard. I was made aware of this issue when golang patched something similar a few hours ago: CVE-2025–4673.

## Affected version

8.14.1

## Steps To Reproduce:

cURL appears to strip authorization and cookie, but not proxy-authorization. Send a request to a server that responds with a redirect to another host with all three headers set, and notice only the first two get stripped off the follow-up request.

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

## Impact

## Summary:

Information from the proxy authorization header exposed to bad actor.

</details>

---
*Analysed by Claude on 2026-05-24*
