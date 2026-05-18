# SSRF in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Dundas BI (Business Intelligence Product)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), URL Manipulation, Unvalidated Redirects
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export functionality, which allowed attackers to manipulate the 'viewUrl' parameter to force the server to make arbitrary requests to internal or external resources. The vulnerability existed in the POST request handling for the export-to-image feature, where user-supplied URL values were not properly validated before being fetched by the server.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI that accepts a 'viewUrl' parameter
2. Attacker intercepts the POST export request and observes the viewUrl parameter containing a relative URI path
3. Attacker modifies viewUrl to point to an internal resource (e.g., http://localhost:8080/admin or http://192.168.1.100:22)
4. Server processes the malicious request and attempts to fetch the attacker-specified resource
5. Attacker analyzes error messages and response times to map internal network topology and services
6. Attacker leverages SSRF to port scan internal network, identify vulnerable services, or attack internal applications

## Root cause
Insufficient input validation and URL sanitization in the export functionality. The application failed to validate that the 'viewUrl' parameter pointed only to intended, whitelisted endpoints. The server directly used user-supplied URL values in server-side fetch operations without restricting the request destination to appropriate resources.

## Attacker mindset
Reconnaissance and lateral movement focused. The attacker recognized a feature that inherently makes server-side requests and identified the user-controllable parameter as an attack vector. By manipulating this parameter, they could explore internal infrastructure, perform port scanning, and potentially pivot to attack internal systems that were inaccessible from the internet but reachable from the vulnerable application server.

## Defensive takeaways
- Implement strict URL validation and whitelisting for any feature that makes server-side requests on behalf of user input
- Use URL parsing libraries to validate the protocol, domain, and port against a whitelist of allowed destinations
- Reject or restrict requests to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.1, etc.)
- Implement allowlisting of domains/URLs rather than blocklisting, and maintain strict separation between internal and external resources
- Sanitize and validate all URL parameters before use in HTTP client libraries
- Monitor and log all outbound requests made by the application to detect anomalous behavior
- Use network segmentation to limit what resources the application server can access internally
- Apply principle of least privilege to service account permissions and network access

## Variant hunting
Search for similar export, preview, thumbnail generation, or webhook features in web applications that accept URL parameters. Look for file download utilities, image proxy services, URL shortener implementations, PDF generation features that accept URLs, and any API endpoints that perform HTTP requests to user-supplied URLs. Check for similar patterns in other analytics, BI, or reporting tools.

## MITRE ATT&CK
- T1190
- T1046
- T1040
- T1580
- T1018

## Notes
The writeup is incomplete as provided (appears to cut off mid-sentence), but demonstrates a classic SSRF attack pattern in enterprise software. Dundas BI's rapid patching response and vendor cooperation exemplifies responsible disclosure. The vulnerability highlights how seemingly innocent features (export functionality) can become attack vectors when URL handling is not properly secured. The impact depends heavily on network architecture and what services are accessible from the vulnerable server.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
