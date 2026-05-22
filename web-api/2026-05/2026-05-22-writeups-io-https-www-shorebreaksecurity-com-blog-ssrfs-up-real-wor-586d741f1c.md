# SSRF in Dundas BI Dashboard Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), URL Manipulation, Internal Resource Access
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, where the 'viewUrl' parameter could be manipulated to force the server to make arbitrary requests to internal or external resources. The vulnerability allowed attackers to access unintended resources by encapsulating malicious requests within legitimate export functionality.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI that generates shareable links
2. Attacker intercepts the POST request containing the 'viewUrl' parameter with a relative URI
3. Attacker modifies the 'viewUrl' parameter to point to an internal resource (e.g., http://localhost:8080/admin or internal IP addresses)
4. Server processes the export request and makes a server-side request to the attacker-controlled URL
5. Attacker observes server responses to determine which internal services are accessible and their characteristics
6. Attacker leverages SSRF to port scan internal network, access internal APIs, or attack internal services

## Root cause
Insufficient input validation and lack of URL allowlisting in the dashboard export feature. The 'viewUrl' parameter accepted user-controlled input without properly validating or restricting the destination URLs, allowing manipulation to point to arbitrary internal or external resources.

## Attacker mindset
Reconnaissance and lateral movement focused. An attacker would systematically probe internal network resources, map infrastructure, identify open ports and services, and potentially launch targeted attacks against discovered internal applications, all while hiding behind legitimate application functionality.

## Defensive takeaways
- Implement strict URL validation and allowlisting for any user-controlled URL parameters
- Use a whitelist of permitted domains/IPs rather than blacklist approaches
- Disable access to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, etc.)
- Implement network-level controls to restrict outbound connections from application servers
- Monitor and log all outbound requests made by the application
- Use URL parsing libraries carefully and avoid string manipulation for URL validation
- Implement request timeouts to prevent hanging connections
- Return generic error messages that don't leak information about internal network topology

## Variant hunting
['Search for other parameters accepting URLs or resource identifiers (imageUrl, reportUrl, dataSource, apiEndpoint, webhookUrl)', 'Test other export formats (PDF, Excel, CSV) for similar SSRF vectors', 'Examine embedding/linking features for external resources', 'Review API endpoints that accept URL parameters for reports or data fetching', 'Test authentication/SSO redirect parameters that may construct URLs', 'Check for SSRF via URL redirects or meta-refresh functionality', 'Look for features that check resource status or health monitoring']

## MITRE ATT&CK
- T1190
- T1040
- T1046
- T1083
- T1570
- T1557

## Notes
This writeup serves primarily as educational content on SSRF vulnerabilities rather than a detailed exploit case study. The Dundas BI vendor was properly notified via responsible disclosure and released patches promptly, demonstrating good security practices. The vulnerability exemplifies how common features like export/sharing functionality can become attack vectors when URL handling is not properly secured. The blog emphasizes the importance of error message verbosity in SSRF exploitation - different error responses ('Connection refused' vs 'Connection timed out' vs 'Request failed') provide attackers with information to fingerprint services and determine accessibility of internal resources.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
