# SSRF in Dundas BI Dashboard Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Server-Side Request Forgery (SSRF), Unvalidated Redirect/Open Redirect, Insufficient Input Validation
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, which allows users to export dashboards as images. The vulnerable 'viewUrl' parameter accepts attacker-controlled values that are processed server-side without proper validation, enabling attackers to manipulate the server into making arbitrary requests to internal or external resources.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI that accepts a 'viewUrl' parameter
2. Attacker crafts a malicious POST request to the export endpoint with a modified 'viewUrl' pointing to an internal resource (e.g., http://localhost:8080/admin or internal IP address)
3. Server processes the request and attempts to fetch the attacker-specified resource server-side without validating the URL
4. Attacker receives response data from internal systems, enabling network reconnaissance and discovery of internal services
5. Attacker uses error messages and response patterns to perform port scanning on internal network infrastructure
6. Attacker leverages SSRF to attack internal HTTP services or perform lateral movement within the network

## Root cause
The application fails to validate and sanitize the 'viewUrl' parameter before using it in server-side requests. The parameter is directly incorporated into HTTP requests without checking for restricted ranges (private IP addresses, localhost) or implementing proper URL schema validation.

## Attacker mindset
An attacker with access to the Dundas BI application can leverage the export feature to perform reconnaissance of the internal network architecture, discover running services on non-standard ports, and potentially launch targeted attacks against internal systems that are not exposed to the internet but are accessible from the application server.

## Defensive takeaways
- Implement strict URL validation to reject requests to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, ::1) and localhost addresses
- Use URL schema whitelisting to allow only necessary protocols (http, https) and reject other schemas (file://, gopher://, etc.)
- Apply network segmentation and firewall rules to restrict outbound connections from application servers to internal resources
- Implement DNS rebinding protections and validate DNS responses before making requests
- Use security headers and Content Security Policy to limit resource fetching capabilities
- Log and monitor all outbound requests from the application for anomalous patterns
- Implement request timeouts and size limits to prevent abuse
- Conduct regular security testing and code reviews focusing on all user input that influences server-side requests

## Variant hunting
['Search for other export/sharing features in web applications that accept URL parameters', 'Audit any features involving external resource fetching (image embedding, file previews, API integrations)', 'Review webhook implementations and notification systems that make server-side requests', 'Test proxy-like features or URL forwarding mechanisms', 'Examine monitoring/health check features that query external systems', 'Analyze file upload features that might process remote URLs', 'Investigate PDF generation features that render content from user-supplied URLs']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1046 - Network Service Discovery
- T1589 - Gather Victim Network Information
- T1040 - Network Sniffing
- T1570 - Lateral Tool Transfer
- T1021 - Remote Services

## Notes
This vulnerability was responsibly disclosed to Dundas BI, who responded positively and released a patched version. The writeup serves as an educational resource on SSRF attack methodology, including the conceptual similarities to Remote File Inclusion (RFI) vulnerabilities. The exploitation relies on understanding error message verbosity and network accessibility from the vulnerable server's perspective. The real-world example demonstrates how SSRF vulnerabilities commonly emerge in legitimate features like export/sharing functionality, requiring security teams to examine all features that process external resources.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
