# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Unsafe URL Handling, Unvalidated Redirect/Forward
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's export functionality, specifically in the dashboard export-to-image feature. The vulnerable 'viewUrl' parameter allowed attackers to manipulate the server into making arbitrary HTTP requests to internal or external resources on behalf of the application.

## Attack scenario (step by step)
1. Attacker identifies the export feature in Dundas BI that accepts a 'viewUrl' parameter
2. Attacker crafts a malicious POST request with a manipulated 'viewUrl' pointing to an internal resource (e.g., http://localhost:8080/admin or internal IP addresses)
3. The vulnerable application server processes the request and attempts to fetch the attacker-specified URL
4. Attacker observes server responses (connection success/failure, error messages, timing) to map internal network topology
5. Attacker leverages successful SSRF requests to attack internal services (databases, APIs, monitoring tools) hidden from external access
6. Attacker may escalate to information disclosure by reading internal service responses or executing unintended operations

## Root cause
The application failed to validate, sanitize, or restrict the 'viewUrl' parameter before using it in a server-side HTTP request. The parameter was user-controllable but lacked proper allowlist validation or URL scheme restrictions, enabling attackers to specify arbitrary target URLs.

## Attacker mindset
An attacker would first recognize the export feature as a potential attack surface, then systematically test different URL values to confirm SSRF capability. The attacker would use response-time analysis and error message differentiation to enumerate internal resources without direct network access. The goal would be reconnaissance of internal infrastructure followed by targeted attacks against discovered internal services.

## Defensive takeaways
- Implement strict allowlist validation for any user-supplied URL parameters - only permit expected domains/paths
- Use URL parsing libraries to validate scheme (http/https), domain, and port against a whitelist
- Block requests to private/internal IP ranges (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, ::1, fc00::/7)
- Disable or restrict HTTP redirects followed by the server-side HTTP client
- Use a separate, isolated network connection for fetching user-supplied URLs with minimal privileges
- Implement timeout mechanisms and rate limiting on export/fetch operations
- Log and monitor all outbound requests made by server-side functions for anomaly detection
- Return generic error messages that don't leak internal service information (avoid revealing port states, service names)
- Use DNS rebinding prevention techniques and validate resolved IP addresses

## Variant hunting
['Check all features involving external resource fetching: image embedding, PDF generation, QR code generation, email attachments', 'Audit API endpoints that accept URL parameters for webhooks, callbacks, or data import functionality', "Test file upload features that process URLs (e.g., 'import from URL' or 'preview remote content')", 'Examine monitoring/health-check features that verify remote service availability', 'Review authentication/SSO flows that redirect or forward requests to external services', 'Search codebase for HTTP client usage patterns with user-controlled parameters (curl, requests, HttpClient libraries)', 'Test URL shortener or link preview features that fetch remote content', 'Check backup/export/reporting features that might fetch data from user-supplied sources']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1021 - Remote Services
- T1526 - Network Service Scanning
- T1087 - Account Discovery
- T1046 - Network Service Discovery
- T1040 - Network Sniffing

## Notes
This vulnerability demonstrates a common implementation flaw in web applications that generate dynamic content (PDFs, images) from user input. The Dundas BI team responsibly patched the vulnerability after disclosure. SSRF severity is highly context-dependent: impact ranges from low (information disclosure) to critical (RCE via internal service exploitation). Error message verbosity is critical for exploitation - timeouts indicate filtered ports, connection refused indicates open ports. This case highlights the importance of secure defaults in third-party Business Intelligence tools used in enterprise environments.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
