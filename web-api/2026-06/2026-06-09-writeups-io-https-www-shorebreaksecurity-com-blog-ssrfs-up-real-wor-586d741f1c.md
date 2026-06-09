# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Unvalidated URL Redirect, Insufficient Input Validation
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, where the 'viewUrl' parameter could be manipulated to force the server to issue requests to arbitrary resources. An attacker could exploit this to perform network reconnaissance, port scanning, or targeted attacks against internal systems accessible from the vulnerable server.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export functionality in Dundas BI that accepts a 'viewUrl' parameter
2. Attacker crafts a malicious POST request to the export endpoint with a modified 'viewUrl' pointing to an internal resource (e.g., http://192.168.1.1:8080/admin)
3. Attacker analyzes the server's response or error messages to determine if the resource is accessible
4. Attacker iteratively probes internal network ranges and ports to map network topology and identify running services
5. Attacker leverages knowledge of internal services to launch targeted attacks (e.g., accessing metadata services, internal APIs, or authentication systems)
6. Attacker extracts sensitive information or gains unauthorized access to internal systems

## Root cause
Insufficient validation and sanitization of the 'viewUrl' parameter allowed user-controlled input to be passed directly to server-side request functions without proper restrictions on target URLs. The application failed to implement allowlisting or URL validation to prevent requests to internal IP ranges and sensitive endpoints.

## Attacker mindset
An attacker would recognize that user-controllable URL parameters in server-side operations are a common SSRF vector. The attacker would test parameter manipulation, analyze error responses for information leakage, and systematically probe internal networks to map infrastructure before launching targeted attacks on identified services.

## Defensive takeaways
- Implement strict URL validation and sanitization - use allowlists for permitted domains/IPs rather than blocklists
- Disable requests to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, metadata services)
- Use defensive coding practices: avoid passing user input directly to HTTP client libraries
- Implement proper error handling to avoid information disclosure through detailed error messages
- Consider using a reverse proxy or network segmentation to limit what services the application server can reach
- Apply principle of least privilege - only allow the application to access required external resources
- Use DNS rebinding protections and TOCTOU (Time-of-Check-Time-of-Use) mitigations
- Monitor and log outbound connections from the application server

## Variant hunting
Search for similar patterns in export/sharing features, webhook implementations, image/PDF generation services, API integrations that accept URL parameters, proxy/forwarding functionality, file download features, and any server-side HTTP request operations. Look for parameters named 'url', 'viewUrl', 'imageUrl', 'embedUrl', 'webhookUrl', 'callbackUrl', or similar patterns across the application.

## MITRE ATT&CK
- T1190
- T1498
- T1570
- T1046
- T1040

## Notes
The vulnerability was responsibly disclosed and patched by Dundas BI. This represents a real-world example of SSRF in a commercial product, demonstrating that the vulnerability is prevalent even in mature enterprise software. The export feature is a common SSRF vector as it inherently requires server-side resource fetching. The vulnerability's impact depends on network architecture and what internal services are accessible from the application server.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
