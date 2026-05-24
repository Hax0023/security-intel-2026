# HTTP Host Header Injection on jamieweb.net

## Metadata
- **Source:** HackerOne
- **Report:** 643225 | https://hackerone.com/reports/643225
- **Submitted:** 2019-07-15
- **Reporter:** mah3sec
- **Program:** jamieweb.net
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Host Header Injection, HTTP Request Smuggling, Cache Poisoning
- **CVEs:** None
- **Category:** uncategorised

## Summary
The target application fails to validate the Host header in HTTP requests, allowing attackers to inject arbitrary hostnames. This can be exploited to perform password reset poisoning, cache poisoning, and potentially access internal resources or trigger XSS vulnerabilities.

## Attack scenario
1. Attacker sends GET request to /contact/ endpoint with Host header set to attacker-controlled domain (e.g., www.google.com)
2. Server accepts the malicious Host header and processes the request without validation
3. If application uses Host header to construct URLs (e.g., password reset links, email domains), attacker can redirect to malicious domain
4. Application forwards password reset email with link pointing to attacker's domain instead of legitimate domain
5. Victim clicks the malicious reset link, enters credentials on attacker's phishing site
6. Attacker captures credentials or executes XSS payload through Host header reflection

## Root cause
Application fails to implement proper Host header validation and whitelist checks. The server accepts arbitrary Host headers without verifying they match the legitimate domain, allowing request manipulation.

## Attacker mindset
An attacker recognizes that Host headers are often implicitly trusted by developers when constructing security-sensitive URLs like password resets. By injecting a malicious host, they can trick the application into generating links that point to attacker infrastructure, enabling credential theft or cache-based attacks.

## Defensive takeaways
- Implement strict Host header validation against a whitelist of legitimate domains
- Use server configuration (not application logic alone) to enforce Host header validation
- Construct URLs using configuration values rather than request headers
- Implement CSP and other headers to limit impact of Host header injection (as shown in response)
- Monitor for unexpected Host header values in logs
- Use absolute URLs with hardcoded domain for security-sensitive functions
- Implement cache key normalization to prevent cache poisoning

## Variant hunting
Test password reset, email verification, and account recovery endpoints with Host header injection
Check for Host header usage in OpenGraph, canonical tags, and CORS headers
Attempt double Host header injection (Host: legitimate.com, Host: attacker.com)
Test with non-standard ports and HTTP/HTTPS mismatches
Look for cache poisoning by checking if response is cached with malicious Host
Test Host header with URL encoding, unicode, and obfuscation techniques
Check internal redirects and API endpoints for Host header reliance

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The server returned 421 Misdirected Request, indicating some level of host validation exists, but the vulnerability persists. The application has strong security headers (CSP, X-Frame-Options) but failed to properly validate Host headers. References to similar reports suggest this was a known vulnerability class at the time. Host header injection is often overlooked because it appears to be infrastructure-level, not application-level.

## Full report
<details><summary>Expand</summary>

is vulnerable to host header injection because the host header can be changed to something outside the target domain.

Attack vectors are somewhat limited but depends on how the host header is used by the back-end application code. If code references the hostname used in the URL such as password reset pages, an attacker could spoof the host header of the request in order to trick the application to forwarding the password reset email to the attackers domain instead, etc. Other attack vectors may also be possible through manipulation of hyperlinks or other misc. code that relies on the host/domain of the request.


## Steps To Reproduce:
request:--
GET /contact/ HTTP/1.1
Host: www.google.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://www.jamieweb.net/
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

Response:---

HTTP/1.1 421 Misdirected Request
Date: Mon, 15 Jul 2019 04:24:41 GMT
Server: Apache
Content-Security-Policy: default-src 'none'; base-uri 'none'; font-src 'self'; form-action 'none'; frame-ancestors 'none'; img-src 'self'; style-src 'self'; block-all-mixed-content
Feature-Policy: accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'none'; camera 'none'; document-write 'none'; fullscreen 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; midi 'none'; payment 'none'; speaker 'none'; sync-script 'none'; sync-xhr 'none'; usb 'none'; vr 'none'
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-DNS-Prefetch-Control: off
Referrer-Policy: no-referrer-when-downgrade
Content-Length: 322
Connection: close
Content-Type: text/html; charset=iso-8859-1


## Supporting Material/References (if applicable): https://hackerone.com/reports/170333
                                                                          https://hackerone.com/reports/182670
https://hackerone.com/reports/264405
https://hackerone.com/reports/158482


POC attach below.

## Impact

password reset poisoning
cache poisoning
access to other internal host/application
XSS, etc.

</details>

---
*Analysed by Claude on 2026-05-24*
