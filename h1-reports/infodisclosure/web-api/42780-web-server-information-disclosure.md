# Web Server Information Disclosure via HTTP Headers and Methods

## Metadata
- **Source:** HackerOne
- **Report:** 42780 | https://hackerone.com/reports/42780
- **Submitted:** 2015-01-07
- **Reporter:** xavinux
- **Program:** wnmlive.com
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Server Fingerprinting, Unnecessary HTTP Methods Enabled
- **CVEs:** None
- **Category:** web-api

## Summary
The web server exposes sensitive information through HTTP response headers (Server, X-Powered-By) and allows potentially dangerous HTTP methods (OPTIONS, TRACE). An attacker can easily identify the server software (Microsoft-IIS/8.0 with ASP.NET) and gain insights into enabled HTTP methods to facilitate further attacks.

## Attack scenario
1. Attacker sends an OPTIONS HTTP request to the target domain www.wnmlive.com
2. Server responds with Allow header listing all supported HTTP methods including TRACE
3. Response headers reveal Server: Microsoft-IIS/8.0 and X-Powered-By: ASP.NET
4. Attacker uses this information to research known vulnerabilities specific to IIS 8.0 and ASP.NET versions
5. Attacker leverages enabled TRACE method to perform HTTP TRACE attacks or XST (Cross-Site Tracing) attacks
6. Attacker gains knowledge of attack surface and can tailor exploits to the specific technology stack

## Root cause
Server misconfiguration failing to suppress verbose HTTP headers and not disabling unnecessary HTTP methods. The Allow header explicitly lists all supported methods, and the server responds to OPTIONS requests with detailed capability information. Default IIS configuration exposes Server and X-Powered-By headers without modification.

## Attacker mindset
Reconnaissance-focused. An attacker seeks to gather intelligence about the target infrastructure with minimal interaction. By fingerprinting the server software, version, and enabled methods, they can efficiently identify applicable exploits and craft targeted attacks. This information reduces attack surface analysis time and increases exploit success probability.

## Defensive takeaways
- Remove or obfuscate Server and X-Powered-By HTTP response headers
- Disable unnecessary HTTP methods (especially TRACE and OPTIONS) unless explicitly required
- Configure web servers to suppress detailed capability advertisements in responses
- Implement HTTP response header filtering to prevent information leakage
- Use Web Application Firewalls (WAF) to strip revealing headers
- Regularly audit HTTP responses for information disclosure vulnerabilities
- Apply vendor hardening guidelines for IIS and ASP.NET deployments
- Monitor and control CORS headers (Access-Control-* headers should be restrictive)

## Variant hunting
Search for similar information disclosure issues: HTTP HEAD requests revealing server details, error pages exposing framework versions, XML/JSON API responses containing software versions, git/svn repository exposure, source map files with path information, deprecated HTTP methods enabled (CONNECT, DELETE, PUT), Upgrade header information disclosure, WWW-Authenticate header leakage, Server banner grabbing via FTP/SMTP/SSH ports

## MITRE ATT&CK
- T1590.002 - Gather Victim Infrastructure Information: Software
- T1592.004 - Gather Victim Host Information: Software
- T1046 - Network Service Discovery

## Notes
This is a classic low-severity information disclosure vulnerability. While not directly exploitable, it significantly reduces the reconnaissance effort for attackers by providing immediate technology stack identification. The severity is appropriately rated as Low since information disclosure alone doesn't compromise confidentiality, integrity, or availability without chaining to other vulnerabilities. The TRACE method is particularly concerning as it can be leveraged in XST attacks. Modern security guidance recommends treating server fingerprinting prevention as a best practice defense-in-depth measure. AWS EC2 metadata exposure (DNS mismatch: ec2-54-67-11-12.us-west-1.compute.amazonaws.com) is also notable as it reveals infrastructure provider.

## Full report
<details><summary>Expand</summary>

Dear sirs.

Seems to have a vulnerability that exposed Web System information through the HTTP Headers Methods.

As a PoC run:

# nc -vv www.wnmlive.com 80
DNS fwd/rev mismatch: www.wnmlive.com != ec2-54-67-11-12.us-west-1.compute.amazonaws.com
www.wnmlive.com [54.67.11.12] 80 (http) open
OPTIONS / HTTP/1.1
Host: www.wnmlive.com

HTTP/1.1 200 OK
Cache-Control: no-transform
Allow: OPTIONS, TRACE, GET, HEAD, POST
Server: Microsoft-IIS/8.0
Public: OPTIONS, TRACE, GET, HEAD, POST
X-Powered-By: ASP.NET
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Request-Method: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Accept, origin, referring-domain, X-UNIT-MEASUREMENT, X-AUTH-TOKEN, X-DEVICE-TYPE, X-SOFTWARE-VERSION
Date: Wed, 07 Jan 2015 17:00:11 GMT
Content-Length: 0
^C sent 42, rcvd 518

Expose information which let anyone know that Microsoft-IIS/8.0 with ASP.NET is running.

Also the Methods Allow: OPTIONS, TRACE, GET, HEAD, POST

Thank you for your attention.

Best Regards,

Javier Romero

</details>

---
*Analysed by Claude on 2026-05-24*
