# Server Header Information Disclosure - PleskLin Detection

## Metadata
- **Source:** HackerOne
- **Report:** 7914 | https://hackerone.com/reports/7914
- **Submitted:** 2014-04-17
- **Reporter:** vhssunny1
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** Low
- **Vuln:** Information Disclosure, Server Misconfiguration, HTTP Header Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
The target server leaks sensitive information through HTTP response headers, specifically the X-Powered-By header revealing the use of PleskLin control panel. This information disclosure allows attackers to identify the hosting platform and target known vulnerabilities associated with Plesk installations.

## Attack scenario
1. Attacker sends HTTP request to target domain
2. Attacker examines HTTP response headers and identifies X-Powered-By: PleskLin
3. Attacker correlates PleskLin version with known CVEs and public exploits
4. Attacker researches Plesk-specific vulnerabilities and misconfigurations
5. Attacker targets known Plesk weaknesses or common default credentials
6. Attacker gains unauthorized access to server control panel or underlying system

## Root cause
Web server (Apache) configured to expose X-Powered-By header containing hosting control panel information. This header was not removed or modified in server configuration files (httpd.conf, .htaccess, or application headers).

## Attacker mindset
Reconnaissance and enumeration phase - gathering intelligence about target infrastructure. Attackers use this banner information to narrow attack surface, identify applicable exploits, and plan targeted attacks against known Plesk vulnerabilities.

## Defensive takeaways
- Remove or obfuscate X-Powered-By and Server headers in Apache configuration
- Use ModSecurity or similar WAF to filter information disclosure headers
- Implement Header hardening: Set X-Powered-By to generic value or omit entirely
- Apply defense-in-depth: Hide technology stack details at all layers
- Regularly audit HTTP response headers for information leakage
- Keep Plesk and all control panel software fully patched and updated
- Restrict access to control panel ports and admin interfaces

## Variant hunting
Search for other control panel headers: X-AspNet-Version, X-Runtime, X-Drupal-Cache
Check for Server header revealing Apache, Nginx, IIS versions
Look for X-Original-URL, X-Rewrite-URL headers in redirects
Scan for Set-Cookie headers revealing session technology
Test for fingerprinting via error pages exposing framework details
Hunt for version information in HTML comments or meta tags

## MITRE ATT&CK
- T1592 - Gather Victim Host Information
- T1590 - Gather Victim Network Information
- T1518 - Software Discovery
- T1010 - Application Window Discovery

## Notes
Low severity information disclosure - requires no authentication to trigger and reveals hosting platform. While not directly exploitable, it significantly aids reconnaissance. Modern security best practice dictates removing all unnecessary server identifying information from HTTP headers to prevent passive reconnaissance and reduce attack surface visibility.

## Full report
<details><summary>Expand</summary>

X-Powered-By:  PleskLin  

HTTP/1.1 200 OK
Date: Thu, 17 Apr 2014 19:52:33 GMT
Server: Apache
Pragma: no-cache
Expires: Mon, 24 Mar 2008 00:00:00 GMT
Cache-Control: no-cache
X-Powered-By: PleskLin
Vary: Accept-Encoding
Keep-Alive: timeout=15, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=utf-8
Content-Length: 127431

</details>

---
*Analysed by Claude on 2026-05-24*
