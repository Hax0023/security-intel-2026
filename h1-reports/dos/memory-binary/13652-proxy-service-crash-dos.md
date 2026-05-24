# Proxy Service Crash via Malformed URL Schemes

## Metadata
- **Source:** HackerOne
- **Report:** 13652 | https://hackerone.com/reports/13652
- **Submitted:** 2014-05-27
- **Reporter:** bitquark
- **Program:** FCT (Fct.li)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service (DoS), Improper Input Validation, Unhandled Exception, Protocol Handler Vulnerability
- **CVEs:** None
- **Category:** memory-binary

## Summary
The proxy service crashes (resulting in 502 Bad Gateway) when processing certain malformed or non-standard URL schemes, particularly data: and javascript: URLs. An attacker can trigger repeated service restarts by sending a sequence of crafted URLs to the vulnerable endpoint, causing denial of service.

## Attack scenario
1. Attacker identifies that the proxy accepts a 'url' parameter for URL processing
2. Attacker crafts URLs using non-standard schemes (data://, javascript:) that the proxy may not properly validate
3. Attacker sends the malformed URLs in rapid succession to staging.fct.li/?url=[payload]
4. The proxy service attempts to process these URLs and crashes due to unhandled exceptions
5. Nginx returns 502 Bad Gateway error, indicating backend service failure
6. Service remains unavailable until manually restarted, disrupting legitimate users

## Root cause
The proxy service lacks proper input validation and exception handling for non-HTTP URL schemes. When the proxy attempts to process data: or javascript: URLs (likely attempting to fetch or validate them as remote resources), it encounters an unhandled error condition that crashes the entire service rather than gracefully rejecting the input.

## Attacker mindset
An attacker would recognize that the proxy service has inadequate input sanitization for the URL parameter and exploits this to achieve persistent denial of service without requiring authentication or complex payloads. The simplicity of the attack (just sending URLs) makes it low-effort and reproducible.

## Defensive takeaways
- Implement strict URL scheme validation - only allow http:// and https:// schemes, explicitly reject data:, javascript:, file:, and other non-standard schemes
- Add comprehensive exception handling around URL parsing and processing to prevent unhandled crashes
- Implement input validation before passing user-supplied URLs to any processing function
- Use a whitelist approach for allowed URL schemes rather than blacklist
- Add rate limiting to prevent rapid sequential requests that could trigger crashes
- Implement service health checks and auto-restart mechanisms to improve resilience
- Log and monitor all malformed URL attempts for security analysis

## Variant hunting
Test other URL schemes: file://, ftp://, gopher://, telnet://, etc.
Try embedded null bytes in URLs: data:text/html%00,test
Test extremely long URLs or URLs with excessive nesting
Combine multiple scheme types: javascript:http://example.com
Test URLs with special characters not properly encoded
Attempt URLs with circular references or recursive data: URIs

## MITRE ATT&CK
- T1499.4
- T1190

## Notes
The reporter noted uncertainty about whether all five requests were necessary or if javascript:confirm() alone triggered the crash, indicating the exact reproduction steps may need refinement. The staging environment discovery suggests reconnaissance was performed. This is a classic input validation vulnerability leading to DoS - while not directly exploitable for data theft, it demonstrates lack of defensive programming practices.

## Full report
<details><summary>Expand</summary>

Sending certain URLs to the proxy appears to crash the service, leading to a _502 Bad Gateway_ from nginx, presumably until the service is restarted. The following sequence sent in a short period appears to cause the crash (it could just be the _javascript:confirm()_ request, as the last request receives the 502, but I can't re-test to be sure):

http://staging.fct.li/?url=data:text/html,Hello
http://staging.fct.li/?url=data://text/html,Hello
http://staging.fct.li/?url=data://staging.fct.li/
http://staging.fct.li/?url=javascript:confirm()
http://staging.fct.li/?url=javascript:confirm("staging.fct.li")

</details>

---
*Analysed by Claude on 2026-05-24*
