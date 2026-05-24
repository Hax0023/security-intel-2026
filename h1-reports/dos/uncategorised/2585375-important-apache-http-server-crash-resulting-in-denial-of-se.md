# Apache HTTP Server mod_proxy Null Pointer Dereference DoS (CVE-2024-38477)

## Metadata
- **Source:** HackerOne
- **Report:** 2585375 | https://hackerone.com/reports/2585375
- **Submitted:** 2024-07-03
- **Reporter:** orange
- **Program:** Apache HTTP Server
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Null Pointer Dereference, Denial of Service
- **CVEs:** CVE-2024-38477
- **Category:** uncategorised

## Summary
A null pointer dereference vulnerability in mod_proxy of Apache HTTP Server versions 2.4.59 and earlier allows remote attackers to crash the server through a specially crafted malicious request. The vulnerability results in denial of service, making the web server unavailable to legitimate users.

## Attack scenario
1. Attacker crafts a malicious HTTP request targeting the mod_proxy module
2. Request is sent to vulnerable Apache HTTP Server (version 2.4.59 or earlier)
3. mod_proxy processes the request and attempts to dereference a null pointer
4. Null pointer dereference causes the server process to crash
5. Server becomes unavailable, resulting in denial of service
6. Attacker can repeat the request to maintain service disruption

## Root cause
Insufficient null pointer validation in mod_proxy's request handling logic allows processing of malformed requests that trigger dereference of uninitialized or unvalidated pointers

## Attacker mindset
Simple denial of service - attacker seeks to disrupt service availability without requiring authentication or exploitation of complex logic, making this an attractive DoS vector

## Defensive takeaways
- Immediately upgrade Apache HTTP Server to version 2.4.60 or later
- Implement request validation and sanitization in reverse proxy configurations
- Monitor for unusual crash patterns and implement automatic restart mechanisms
- Use web application firewalls (WAF) to filter potentially malicious proxy requests
- Implement proper null pointer checks and defensive programming practices throughout proxy modules
- Consider disabling mod_proxy if not required for operational needs

## Variant hunting
Search for similar null pointer dereference patterns in other Apache modules (mod_rewrite, mod_cache, mod_ssl), proxy implementations in other web servers (nginx, IIS), and request parsing logic that handles edge cases

## MITRE ATT&CK
- T1190
- T1499

## Notes
This vulnerability was responsibly disclosed through official Apache security channels with a 3-month embargo period before public disclosure. The fix was released in Apache HTTP Server 2.4.60. Low complexity exploitation makes this a critical patch priority for organizations running vulnerable versions.

## Full report
<details><summary>Expand</summary>

I reported this vulnerability through the official Apache HTTP Server security email on April 1, 2024, and received a fix along with a CVE number on July 1, 2024. You can check detailed information from there:
> https://httpd.apache.org/security/vulnerabilities_24.html

## Impact

null pointer dereference in mod_proxy in Apache HTTP Server 2.4.59 and earlier allows an attacker to crash the server via a malicious request.

Users are recommended to upgrade to version 2.4.60, which fixes this issue.

</details>

---
*Analysed by Claude on 2026-05-24*
