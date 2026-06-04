# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Server-Side Request Forgery (SSRF), Unsafe URL Handling, Insufficient Input Validation
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, which allows users to export dashboards to various formats including images. The vulnerability exists in the 'viewUrl' parameter of the export functionality, which accepts user-controlled input that the server uses to fetch resources, allowing attackers to force the application to issue arbitrary requests to internal or external resources.

## Attack scenario (step by step)
1. Attacker identifies the export feature in Dundas BI that accepts a 'viewUrl' parameter containing a URI
2. Attacker manipulates the 'viewUrl' parameter to point to an internal resource (e.g., http://localhost:8080/admin or internal IP addresses)
3. Attacker submits the malicious export request, causing the server to fetch the attacker-specified resource
4. Server processes the request and returns responses/error messages that reveal information about internal infrastructure (port scanning, service discovery)
5. Attacker maps internal network topology and identifies accessible services by analyzing error messages and response variations
6. Attacker leverages discovered internal services to perform further attacks (accessing metadata services, internal APIs, local databases)

## Root cause
The application fails to properly validate and restrict the 'viewUrl' parameter in the export functionality. The parameter accepts user-supplied URLs without implementing whitelist validation, URL scheme restrictions, or preventing access to internal/private IP address ranges (127.0.0.1, 10.x.x.x, 172.16.x.x, 192.168.x.x). The server then automatically fetches resources from these attacker-controlled URLs without proper security controls.

## Attacker mindset
An attacker would recognize that export/sharing features commonly interact with external resources and likely implement URL handling logic. By analyzing the 'viewUrl' parameter, the attacker would test whether the application validates destination URLs, leading to discovery that arbitrary URLs can be supplied. The attacker would then systematically probe internal network ranges and ports to map infrastructure, seeking high-value targets like cloud metadata services, internal admin panels, or database management interfaces.

## Defensive takeaways
- Implement strict URL validation with whitelisting of allowed domains/protocols before server-side requests
- Block requests to private IP ranges (127.0.0.1/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16) and local services
- Use URL parsing libraries to prevent bypasses via encoding, IPv6, or DNS rebinding techniques
- Restrict allowed URL schemes to only necessary protocols (https preferred over http)
- Implement timeout controls and rate limiting on server-side requests
- Log and monitor all server-initiated external requests for anomalies
- Avoid exposing detailed error messages that reveal service availability or type to users
- Use a dedicated proxy/gateway for outbound requests with additional validation
- Disable unnecessary URL/URI handling features if not required for core functionality
- Regularly conduct security testing focusing on request-forwarding features

## Variant hunting
Look for similar SSRF vulnerabilities in other areas: (1) Image rendering/processing features that accept image URLs, (2) PDF generation utilities with 'sourceUrl' or similar parameters, (3) Web scraping/monitoring features, (4) Report scheduling with URL parameters, (5) Webhook or callback URL configurations, (6) File upload features accepting remote URLs, (7) API integrations with user-supplied endpoints, (8) QR code generation with data sources, (9) Document conversion services, (10) Analytics data source connectors accepting URLs

## MITRE ATT&CK
- T1190
- T1570
- T1046
- T1526
- T1040

## Notes
This vulnerability was responsibly disclosed to Dundas BI, who released a patch. The writeup effectively demonstrates the SSRF attack methodology and emphasizes the importance of proper URL validation in export/sharing features. The vulnerability is particularly concerning in enterprise Business Intelligence tools due to their typical network positioning and access to sensitive data sources. Similar vulnerabilities should be expected in other BI and analytics platforms with export/sharing capabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
