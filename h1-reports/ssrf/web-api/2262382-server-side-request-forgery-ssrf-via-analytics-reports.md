# Server Side Request Forgery (SSRF) via Analytics Reports

## Metadata
- **Source:** HackerOne
- **Report:** 2262382 | https://hackerone.com/reports/2262382
- **Submitted:** 2023-11-23
- **Reporter:** hacker1_agent
- **Program:** Unknown (HackerOne Report #2262382)
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Server-Side Request Forgery (SSRF), Information Disclosure, Arbitrary File Read
- **CVEs:** None
- **Category:** web-api

## Summary
An SSRF vulnerability exists in the analytics reports functionality that allows attackers to read arbitrary internal files. The vulnerability enables unauthorized access to sensitive information by exploiting insufficient validation of user-supplied URLs in report generation requests.

## Attack scenario
1. Attacker identifies the analytics reports feature and locates parameters accepting URLs or file paths
2. Attacker crafts a malicious request targeting internal file paths (e.g., file:///etc/passwd or http://localhost:internal-service)
3. The vulnerable application processes the request without proper URL validation or access controls
4. Server executes the SSRF payload and returns the contents of internal files or responses from internal services
5. Attacker exfiltrates sensitive data including configuration files, credentials, or internal service responses
6. With chained vulnerabilities, attacker may pivot to access restricted internal resources or databases

## Root cause
Insufficient validation and sanitization of user-supplied input in analytics report URL/path parameters. The application likely fails to implement proper allowlisting, URL scheme validation, or network-level controls to prevent requests to internal resources.

## Attacker mindset
An attacker seeking to access sensitive internal information without direct system access. They exploit the analytics feature as a proxy to bypass security boundaries and read files or interact with internal services not directly exposed to the internet.

## Defensive takeaways
- Implement strict URL allowlisting for all external URLs used in reports (whitelist known domains)
- Block dangerous URL schemes (file://, gopher://, dict://, etc.) and only permit http/https
- Validate and sanitize all URL/path inputs using robust parsing libraries
- Implement network-level controls: prevent outbound connections to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8)
- Use URL parsing to detect obfuscation techniques (hex encoding, double encoding, IPv4 integer notation)
- Implement request timeouts and size limits to prevent abuse
- Conduct security review of all features accepting URLs or file paths as input
- Use security testing tools to identify SSRF vectors during development

## Variant hunting
Search for other analytics features that accept external URLs or file paths (dashboards, exports, webhooks, integrations)
Test PDF/report generation endpoints with SSRF payloads
Check image processing features for SSRF (avatars, thumbnails, URL-based image insertion)
Review webhook/callback functionality for SSRF vulnerabilities
Test URL shortener or redirect features
Examine API endpoints that fetch remote content (RSS feeds, metadata fetching, proxies)
Test backup/restore functionality accepting URLs
Review third-party API integration features

## MITRE ATT&CK
- T1190
- T1105
- T1552
- T1059
- T1021

## Notes
The writeup is minimal and lacks technical depth (PoC redacted). The vulnerability appears straightforward but the limited details prevent full risk assessment. Standard SSRF mitigation practices should be applied. Follow-up review of analytics report implementation recommended.

## Full report
<details><summary>Expand</summary>

Hello Gents, I would like to report an issue where attackers are able to read internal files via an SSRF vulnerability.


## Proof of concept

+ ███

## Impact

SSRF.

Thanks and have a nice day!

</details>

---
*Analysed by Claude on 2026-05-11*
