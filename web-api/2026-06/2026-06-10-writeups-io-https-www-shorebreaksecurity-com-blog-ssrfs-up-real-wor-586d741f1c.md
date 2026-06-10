# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Server-Side Request Forgery (SSRF), Remote File Inclusion, URL Manipulation
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, allowing attackers to manipulate the 'viewUrl' parameter to force the server to make arbitrary requests to internal or external resources. The vulnerability existed in the export functionality that converts dashboards to different formats, with the server processing user-controlled URL parameters without proper validation.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI and observes POST requests containing a 'viewUrl' parameter
2. Attacker intercepts the export request and modifies the 'viewUrl' parameter from a relative URI to point to an internal resource (e.g., http://localhost:8080/admin or http://192.168.1.1)
3. Attacker submits the modified request, causing the Dundas BI server to issue an HTTP request to the attacker-specified internal resource
4. Attacker analyzes error messages and response codes to perform network reconnaissance (port scanning, service enumeration)
5. Attacker maps internal infrastructure and identifies vulnerable internal services or administrative interfaces
6. Attacker leverages SSRF to attack internal applications, exfiltrate data, or escalate privileges within the organization

## Root cause
Insufficient input validation and lack of URL scheme/destination whitelisting in the export feature. The application accepts user-controlled 'viewUrl' parameters without restricting them to legitimate internal resources or validating the destination against a whitelist of allowed domains/IP addresses.

## Attacker mindset
An attacker exploiting this vulnerability would seek to bypass network segmentation and firewall rules by leveraging the trusted position of the Dundas BI server. They would first perform reconnaissance to map internal infrastructure, then target internal administrative interfaces, APIs, or databases that are only accessible from within the network perimeter.

## Defensive takeaways
- Implement strict URL validation and whitelisting - only allow requests to explicitly permitted domains/IP addresses
- Use a whitelist approach rather than blacklist for SSRF prevention
- Disable or restrict access to internal IP ranges (RFC 1918, 127.0.0.0/8, 169.254.0.0/16, etc.)
- Implement network segmentation to limit what internal resources the application server can access
- Use DNS rebinding protections and validate DNS responses
- Return minimal error messages that don't reveal information about internal network topology
- Implement request timeouts to prevent resource exhaustion
- Log and monitor all outbound requests made by the application
- Apply principle of least privilege - restrict application service account permissions
- Disable unused URL schemes (file://, gopher://, dict://, etc.) if using libraries that support them

## Variant hunting
['Search for other export/sharing features that accept URL parameters in similar BI/analytics applications', 'Examine other Dundas BI features that embed external resources or perform HTTP requests (image embedding, API integrations, webhooks)', 'Test report generation, scheduled report delivery, and data source configuration features for SSRF', 'Look for URL redirect parameters in dashboard sharing, link generation, and authentication callback mechanisms', 'Investigate webhook and notification features that might accept attacker-controlled URLs', 'Check for SSRF in file upload functionality that might fetch remote files', 'Test external data source connections and API integrations in analytics platforms']

## MITRE ATT&CK
- T1190
- T1046
- T1595
- T1040
- T1580

## Notes
This is an informational/educational writeup from Shorebreak Security describing SSRF vulnerability concepts and a real-world example in Dundas BI. The vulnerability was responsibly disclosed and patched by the vendor. The writeup emphasizes that SSRF impact depends heavily on error message verbosity - attackers use differential responses to infer internal network topology and service availability. The attack is particularly dangerous because it bypasses network firewalls by leveraging the trusted position of the vulnerable application server within the internal network.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
