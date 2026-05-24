# Open Redirect in m.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 125000 | https://hackerone.com/reports/125000
- **Submitted:** 2016-03-22
- **Reporter:** bobrov
- **Program:** Uber
- **Bounty:** Not specified in provided content
- **Severity:** medium
- **Vuln:** Open Redirect, URL Validation Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in m.uber.com where improper URL validation allows attackers to redirect users to arbitrary external domains. The vulnerability is triggered by crafting URLs with double slashes and path traversal sequences that bypass validation logic.

## Attack scenario
1. Attacker crafts a malicious URL: https://m.uber.com//youtube.com/%2F../
2. Attacker sends the link via phishing email or social engineering to target users
3. User clicks the link trusting the m.uber.com domain
4. Server processes the request and returns HTTP 303 redirect with Location header pointing to //youtube.com/%2F../
5. Browser follows the redirect to the attacker-controlled domain (youtube.com or attacker's server)
6. Attacker can harvest credentials, perform credential theft, or distribute malware

## Root cause
Insufficient URL validation/canonicalization before generating redirect responses. The application fails to properly parse and validate relative vs absolute URLs, allowing double slashes and path traversal sequences to bypass security checks. The Location header is set to a protocol-relative URL (//youtube.com) which allows open redirects.

## Attacker mindset
An attacker would leverage this vulnerability for phishing campaigns by creating trusted-looking URLs on the legitimate Uber domain to redirect victims to credential harvesting pages or malware distribution sites. The attack is particularly effective because users trust the m.uber.com domain.

## Defensive takeaways
- Implement strict URL validation and canonicalization before any redirect operations
- Maintain a whitelist of allowed redirect destinations
- Use absolute URLs in Location headers and validate the scheme (http/https)
- Reject or normalize URLs with double slashes (//), path traversal sequences (..), and URL-encoded characters in redirect parameters
- Implement Content Security Policy (CSP) headers to restrict redirect capabilities
- Log all redirect operations and monitor for suspicious patterns
- Use framework-provided redirect functions with built-in validation rather than manual header manipulation

## Variant hunting
Test other Uber subdomains (riders.uber.com, partners.uber.com) for similar redirect vulnerabilities
Test alternate path traversal sequences: /../, /.//, %2e%2e/, etc.
Test with different URL schemes: javascript:, data:, etc.
Check for open redirects in other parameters: returnUrl, callback, redirect_uri, return_to
Test with internationalized domain names and Unicode characters in URLs
Probe nested redirect chains and multiple redirects

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link (delivers malicious links)
- T1566.002 - Phishing: Phishing - Spearphishing Link (delivery method)
- T1187 - Forced Authentication (credential harvesting endpoint)

## Notes
This is a classic open redirect vulnerability that commonly affects mobile domains. The double slash normalization bypass (// vs /) and protocol-relative URL handling are common weaknesses. The HTTP 303 redirect response indicates intentional redirect functionality, suggesting the application was designed to support redirects but lacked proper validation. Similar vulnerabilities have been historically common in URL shorteners, OAuth flows, and login redirect mechanisms.

## Full report
<details><summary>Expand</summary>

Reproduction Steps:
`https://m.uber.com//youtube.com/%2F..`

HTTP Response:
```
HTTP/1.1 303 See Other
...
Location: //youtube.com/%2F../
```

</details>

---
*Analysed by Claude on 2026-05-24*
