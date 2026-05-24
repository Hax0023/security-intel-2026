# Known DoS Condition (Null Pointer Dereference) in Nginx 1.10.0 - help.nextcloud.com

## Metadata
- **Source:** HackerOne
- **Report:** 145409 | https://hackerone.com/reports/145409
- **Submitted:** 2016-06-17
- **Reporter:** shoveller
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Denial of Service (DoS), Null Pointer Dereference, Unpatched Software Vulnerability
- **CVEs:** CVE-2016-4450
- **Category:** memory-binary

## Summary
The help.nextcloud.com subdomain runs vulnerable Nginx 1.10.0 affected by CVE-2016-4450, which allows remote attackers to crash the Nginx process via a malformed HTTP request. The vulnerability results in a null pointer dereference that terminates the web server, causing service unavailability.

## Attack scenario
1. Attacker identifies help.nextcloud.com is running Nginx 1.10.0 by examining HTTP response headers or requesting the server IP directly
2. Attacker crafts a specially malformed HTTP request that triggers the null pointer dereference vulnerability in Nginx's request handling logic
3. Attacker sends the malicious request to the vulnerable Nginx instance on help.nextcloud.com
4. The Nginx process encounters the null pointer dereference and crashes unexpectedly
5. The web server becomes unavailable, preventing legitimate users from accessing help documentation
6. Attacker can repeat the attack to maintain continuous denial of service

## Root cause
Nginx 1.10.0 contains a null pointer dereference bug in HTTP request processing that was not addressed until a later patch version. The vulnerability allows malformed HTTP requests to trigger an unsafe code path that dereferences a null pointer without proper validation.

## Attacker mindset
An attacker would recognize this as a low-effort, high-impact opportunity to disrupt service availability. The vulnerability is trivial to exploit once the version is identified, requiring only a crafted HTTP request. This appeals to script-kiddies and state-level actors alike seeking quick wins or service disruption.

## Defensive takeaways
- Maintain an inventory of all software versions running in production, including reverse proxies and web servers
- Implement automated patching workflows to promptly apply security updates, especially for high-severity DoS vulnerabilities
- Monitor software version information leakage in HTTP headers; consider suppressing or obfuscating server version strings
- Deploy rate limiting and request validation at the load balancer level to detect and block malformed requests
- Use process monitoring and auto-restart mechanisms (e.g., systemd, supervisord) to minimize downtime from process crashes
- Perform regular security audits of all public-facing infrastructure to identify outdated or unpatched components
- Establish a vulnerability management program with defined SLAs for patching critical services

## Variant hunting
Search for other Nextcloud subdomains or services running Nginx versions 1.10.x without patches. Check for similar null pointer dereference vulnerabilities in other versions of Nginx or competing web servers (Apache, IIS). Test for other CVEs affecting Nginx 1.10.0 that may have been bundled in the same maintenance release cycle.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1499: Endpoint Denial of Service

## Notes
This report demonstrates responsible disclosure by identifying a known CVE affecting production infrastructure. The researcher respected the stated policy against DoS testing but provided sufficient information for Nextcloud to patch. CVE-2016-4450 specifically involves null pointer dereference in Nginx's handling of certain HTTP request types. The vulnerability is publicly documented and easily exploitable, making rapid patching critical.

## Full report
<details><summary>Expand</summary>

The https://help.nextcloud.com sub-site is running Nginx/1.10.0 which is vuln to a known issue (CVE-2016-4450) which allows a remote malformed HTTP request to cause the Nginx process to crash.

DoS testing is mentioned as not requested, but if you know of an issue give it a go .. 

You can determine the version running by requesting the IP of the site and getting the HTTP 301, eg: https://88.198.160.135

https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2016-4450

</details>

---
*Analysed by Claude on 2026-05-24*
