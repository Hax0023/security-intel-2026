# Blind SSRF to Internal Services in Matrix preview_link API

## Metadata
- **Source:** HackerOne
- **Report:** 1960765 | https://hackerone.com/reports/1960765
- **Submitted:** 2023-04-24
- **Reporter:** la_revoltage
- **Program:** Reddit
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Information Disclosure, Internal Service Enumeration, Port Scanning
- **CVEs:** None
- **Category:** web-api

## Summary
Reddit's Matrix-based chat implementation contains an SSRF vulnerability in the preview_link API endpoint that fails to validate or filter URLs before making requests. Attackers can enumerate internal services, perform port scanning, and potentially escalate to RCE by extracting metadata from responses.

## Attack scenario
1. Attacker identifies the preview_link API endpoint at https://matrix.redditspace.com/_matrix/media/r0/preview_url/
2. Attacker crafts requests with internal service URLs (localhost, private IP ranges) as the url parameter
3. API processes request without validation and fetches the URL, returning response metadata including og:title tags
4. Attacker enumerates services by analyzing response titles and latency patterns to identify accessible internal services
5. Attacker performs port scanning by testing various ports on internal hosts and observing response differences
6. Attacker attempts RCE exploitation against identified vulnerable internal services through SSRF proxy

## Root cause
The preview_link API endpoint accepts user-supplied URLs and makes backend requests to fetch preview metadata without implementing URL validation, allowlist filtering, or network segmentation controls. The application fails to restrict requests to external URLs only, allowing access to internal service addresses.

## Attacker mindset
An attacker recognizes that preview/metadata extraction functionality commonly requires backend HTTP requests and immediately targets it for SSRF. The attacker systematically enumerates internal services through response analysis, demonstrating reconnaissance discipline by requesting escalation permission before attempting RCE rather than blindly exploiting.

## Defensive takeaways
- Implement strict URL validation: reject private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16), localhost, and link-local addresses
- Use URL allowlist approach: only permit requests to known external domains or enforce explicit domain validation
- Implement network segmentation: restrict outbound connections from preview services to external URLs only via firewall rules
- Add request timeouts: implement aggressive timeouts (< 5 seconds) to reduce attacker's ability to infer service presence through response timing
- Sanitize response data: extract only necessary metadata and avoid exposing full HTML responses containing service banners or error messages
- Monitor SSRF patterns: detect and alert on requests to private IP ranges or internal service ports
- Use dedicated proxy/gateway: funnel all external requests through a separate service with strict controls rather than direct backend requests

## Variant hunting
Check other preview/metadata endpoints (image preview, link preview, thumbnail generation) for similar SSRF patterns
Test alternative protocol schemes: gopher://, file://, dict://, ldap://, to bypass URL validation
Attempt URL encoding/obfuscation bypasses: double encoding, case variations, mixed case IP addresses
Test redirect-based SSRF: craft external URLs that redirect to internal services
Examine error messages and response timing for information leakage about internal service availability
Check if API accepts data URLs or base64-encoded payloads that could bypass validation
Test similar APIs in other Reddit services (video preview, media processing) for equivalent SSRF vulnerabilities

## MITRE ATT&CK
- T1190
- T1526
- T1570
- T1046
- T1592

## Notes
The reporter demonstrated exceptional security research discipline by: (1) thoroughly testing the vulnerability, (2) identifying escalation potential to RCE, and (3) explicitly requesting permission before attempting critical-level exploitation. The redacted content suggests internal service IPs, ports, and specific RCE vectors were discovered but responsibly withheld. The 2-second timeout behavior suggests possible service timeouts or network detection mechanisms. This vulnerability likely affects other Matrix instances beyond Reddit's deployment.

## Full report
<details><summary>Expand</summary>

## Summary:
Reddit' new chat is based on Matrix software which has preview_link functionality which doesn't filter the URL before sending the request

## Impact:
Attacker can enumerate services by grabbing og:title and port scanning, also possible RCE escalation (Asking for permission on this one)

## Steps To Reproduce:


  1. Visit the https://matrix.redditspace.com/_matrix/media/r0/preview_url/?url=*
  2. Replace * with http://██████ to get og:title ███████
  3. Replace * with http://█████████ to get og:title ███████
 4. Replace * with http://██████████to get og:title ██████
 5. Replace * with ████████ to get og:title █████████

Note: If the request is stuck and not responding in 2 seconds reload the page until it does

## Permit for escalation attempt? 
Since the ███ URL is accessible it may be possible to run ███:
GET █████████

There are also possibilities to test ██████, but I thought that it would be incorrect to do such activity without permission and as such report vulnerability in this state. I also therefore request a permission to try to escalate this to Critical

## Impact

Attacker can enumerate services and launch attacks against them

</details>

---
*Analysed by Claude on 2026-05-11*
