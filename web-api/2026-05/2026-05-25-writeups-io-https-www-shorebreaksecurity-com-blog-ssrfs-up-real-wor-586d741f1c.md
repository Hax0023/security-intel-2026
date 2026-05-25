# SSRF Vulnerability in Dundas BI Dashboard Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), URL Manipulation, Unvalidated Redirect/Forward
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, which allows attackers to manipulate the 'viewUrl' parameter to force the server to issue requests to unintended internal or external resources. The vulnerability exists in the image export functionality where user-supplied URLs are processed by the server without proper validation. This enables attackers to perform network reconnaissance, attack internal services, or access resources hidden from direct internet access.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI and intercepts the POST request containing the 'viewUrl' parameter
2. Attacker modifies the 'viewUrl' parameter from a legitimate relative path to an internal IP address (e.g., http://192.168.1.1:8080)
3. Server processes the malicious request and attempts to fetch the resource, revealing whether internal services are accessible via error messages and response times
4. Attacker analyzes response patterns to map internal network topology, identifying open ports and running services
5. Attacker crafts targeted SSRF requests to exploit internal HTTP services, query metadata services (e.g., AWS EC2 metadata), or access admin panels
6. Attacker exfiltrates sensitive data or gains unauthorized access to internal systems accessible only from the vulnerable server

## Root cause
The application fails to validate and sanitize the 'viewUrl' parameter before using it in server-side HTTP requests. The parameter is accepted as user-controlled input without restrictions on protocol, hostname, or IP address ranges, allowing attackers to redirect requests to arbitrary destinations.

## Attacker mindset
An attacker would recognize that export/rendering features commonly perform server-side requests to fetch resources. By analyzing request parameters (viewUrl, imageUrl, etc.), they identify injection points where URLs can be modified. The attacker leverages this to explore internal networks and services that aren't exposed to the internet, treating the vulnerable server as a proxy to bypass network segmentation and access controls.

## Defensive takeaways
- Implement strict URL validation using allowlists for permitted domains, protocols, and IP ranges; reject localhost, private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16), and link-local addresses by default
- Use URL parsing libraries to prevent bypasses via encoding tricks, alternative IP notations, or redirect chains
- Enforce network-level controls: restrict outbound connections from application servers to only necessary external services
- Disable HTTP redirects or strictly validate redirect targets to prevent chaining attacks
- Implement comprehensive logging and monitoring of all server-initiated requests with alerts for suspicious patterns (internal IPs, port scanning attempts)
- Apply principle of least privilege: run application processes with minimal network access required
- Use timeout mechanisms to prevent resource exhaustion from slow SSRF attacks
- Regularly audit and penetration test features that involve URL handling, file inclusion, or external resource fetching

## Variant hunting
['Search for other export/rendering features (PDF export, report generation, screenshot capture, email delivery) that may accept URL parameters', 'Examine API endpoints that accept URL parameters: webhooks, callbacks, notification URLs, API proxies, or forwarding mechanisms', 'Test embedded resource features: image embedding, logo upload with URL specification, style sheet inclusion, iframe/object embedding', 'Investigate monitoring and health-check features that accept URLs for endpoint validation', 'Review file upload features with URL specification (fetch from URL instead of upload) or preview functionality', 'Test OAuth/authentication flows with callback or redirect URL parameters for SSRF chains', 'Check template rendering engines that process URLs, particularly in automation/scheduling features', 'Examine integration points with external services (Slack, Teams, email) that may accept URL parameters for content fetching']

## MITRE ATT&CK
- T1190
- T1498
- T1526
- T1557
- T1570

## Notes
The vulnerability was responsibly disclosed to Dundas BI, who released a patched version promptly. The writeup effectively explains both the conceptual nature of SSRF and practical exploitation methodology. The real-world example demonstrates how seemingly innocent features (dashboard export) can become critical security issues. The analysis highlights the importance of error message verbosity in SSRF exploitation—detailed error responses enable attackers to infer internal network topology. The article's comparison to Remote File Inclusion (RFI) is valuable for understanding conceptual overlap between related vulnerabilities. This is a classic example of input validation failure in a feature handling user-influenced URL construction.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
