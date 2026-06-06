# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), URL Manipulation, Unvalidated Redirect
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export functionality, allowing attackers to manipulate the 'viewUrl' parameter to force the server to make requests to arbitrary internal or external resources. The vulnerability enabled network reconnaissance, internal service enumeration, and potential attacks against internal infrastructure not directly accessible from the internet.

## Attack scenario (step by step)
1. Attacker discovers the dashboard export feature in Dundas BI that accepts a 'viewUrl' parameter
2. Attacker modifies the 'viewUrl' parameter from a relative path to an internal network address (e.g., http://192.168.1.1:8080)
3. Server processes the malicious request and attempts to fetch the resource from the internal network address
4. Attacker analyzes error messages and response times to determine open ports and running services on internal infrastructure
5. Attacker leverages discovered internal services to perform targeted attacks or extract sensitive information
6. Attacker optionally develops automated scanning scripts to comprehensively map the internal network topology

## Root cause
Insufficient input validation and lack of URL scheme/destination restrictions on the 'viewUrl' parameter. The application failed to validate that the URL parameter only references intended resources, allowing arbitrary URL injection for the server-side request mechanism.

## Attacker mindset
An attacker would recognize the export feature as a vector for making server-initiated requests and test parameter manipulation to redirect these requests. The goal would be reconnaissance of internal infrastructure, identification of running services, and potential pivoting to attack internal systems from a trusted network position.

## Defensive takeaways
- Implement strict URL validation: whitelist allowed domains/protocols and reject any URLs pointing to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16)
- Use allowlists rather than blocklists for acceptable URL destinations and schemes
- Disable or restrict HTTP redirects that could be leveraged to bypass URL restrictions
- Implement network-level controls: restrict outbound connections from application servers to only necessary external services
- Log and monitor all outbound requests initiated by the application with full URL details for detection of SSRF attempts
- Use DNS rebinding protection and implement timeouts on server-initiated requests
- Apply principle of least privilege to application server network access permissions
- Conduct security testing specifically targeting URL manipulation in all features that accept user-controlled URLs

## Variant hunting
Search for similar export/sharing features in other Dundas BI modules, other BI tools (Tableau, Power BI, QlikView), and general web applications with URL parameters in POST requests. Look for parameters named: url, link, viewUrl, redirectUrl, imageUrl, sourceUrl, targetUrl, destination, or similar. Test features involving: report generation, PDF/image export, email delivery, preview functionality, and API endpoints accepting URL parameters.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1021 - Remote Services (internal lateral movement potential)
- T1046 - Network Service Discovery (port scanning via SSRF)
- T1040 - Network Sniffing (information gathering)
- T1105 - Ingress Tool Transfer (potential payload delivery)

## Notes
The vulnerability was responsibly disclosed to Dundas BI, which released a patch promptly. This is a textbook SSRF case highlighting the importance of URL parameter validation in features involving server-initiated requests. The impact varies based on internal network topology and verbosity of error messages returned to attackers. Similar vulnerabilities are common in analytics, reporting, and integration platforms that frequently require URL handling.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
