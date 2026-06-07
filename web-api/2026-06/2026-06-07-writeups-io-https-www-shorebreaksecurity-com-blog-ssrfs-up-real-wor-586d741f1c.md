# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Server-Side Request Forgery (SSRF), Unsafe URL/Parameter Handling, Request Manipulation
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, allowing attackers to manipulate the 'viewUrl' parameter to force the application to issue requests to unintended resources. By controlling this parameter, attackers could perform network reconnaissance, port scanning, and targeted attacks against internal systems accessible from the vulnerable server.

## Attack scenario (step by step)
1. Attacker discovers that Dundas BI's export-to-image feature accepts a 'viewUrl' parameter in POST requests
2. Attacker modifies the 'viewUrl' parameter from a relative URI (e.g., '/Link/?shortLink=...') to an internal IP address or hostname (e.g., 'http://192.168.1.1:8080/admin')
3. The vulnerable server processes the request and attempts to fetch the resource specified in the manipulated 'viewUrl' parameter
4. Attacker analyzes server responses (error messages, timeouts, connection refused) to infer information about internal network topology, open ports, and running services
5. Attacker uses response variations to conduct blind port scanning of internal networks
6. Attacker leverages SSRF to attack internal applications or services (e.g., internal APIs, administrative panels) that are protected from external access

## Root cause
The application fails to validate and restrict the 'viewUrl' parameter to only expected/safe values before using it in server-side requests. The parameter is directly incorporated into the server's request logic without proper allowlisting or URL validation, allowing manipulation to arbitrary internal/external resources.

## Attacker mindset
An attacker would identify the export feature as an entry point for request manipulation, recognize that user-controlled parameters are passed to server-side request functions, and exploit the lack of input validation to probe internal infrastructure and attack hidden services that are isolated from external networks.

## Defensive takeaways
- Implement strict allowlisting of URLs/domains that the application is permitted to request; reject all others
- Validate and sanitize all user-controlled parameters used in server-side requests
- Restrict requests to appropriate protocols (HTTP/HTTPS) and block access to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, localhost)
- Use DNS rebinding protection and implement network segmentation to limit server access to internal resources
- Minimize error message verbosity to prevent attackers from inferring network topology through response analysis
- Implement request timeout limits and rate limiting on resource-fetching features
- Maintain updated software patches and monitor vendor security advisories

## Variant hunting
['Search for other parameters that accept URLs or file paths (imageUrl, templateUrl, sourceUrl, dataUrl, webhookUrl, callbackUrl)', 'Test other export/sharing/publishing features that may perform server-side requests', 'Examine API endpoints that accept external resource references or perform proxy-like functionality', 'Review authentication and forwarding mechanisms that may delegate requests to external services', 'Test image embedding, document generation, and report scheduling features for similar vulnerabilities', 'Analyze third-party integrations or plugins that handle external resource fetching']

## MITRE ATT&CK
- T1190
- T1526
- T1046
- T1040

## Notes
This is an educational example demonstrating real-world SSRF exploitation. The vendor (Dundas Data Visualization, Inc.) was notified through responsible disclosure and released a patch. SSRF differs from RFI in that it typically doesn't lead to code execution but is powerful for network reconnaissance and internal service exploitation. The vulnerability's impact depends on error message verbosity and internal network accessibility from the affected server.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
