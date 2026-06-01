# SSRF in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Unvalidated URL Handling, Internal Resource Access
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, which allowed attackers to manipulate the 'viewUrl' parameter to force the server to issue arbitrary HTTP requests to internal or external resources. The vulnerability existed in the export functionality that converts dashboards to different formats, potentially enabling network reconnaissance and attacks against internal systems.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI that generates shareable links
2. Attacker discovers the POST request containing the 'viewUrl' parameter with a relative URI path
3. Attacker modifies the 'viewUrl' parameter to point to internal resources (e.g., http://localhost:8080/admin, 192.168.1.x/api endpoints)
4. Server processes the malicious request and attempts to fetch the attacker-specified resource on behalf of the vulnerable application
5. Attacker analyzes server responses (connection timeouts, error messages, response content) to map internal network topology
6. Attacker leverages gathered intelligence to launch targeted attacks against discovered internal services or perform data exfiltration

## Root cause
Insufficient input validation and lack of URL scheme/destination filtering on the 'viewUrl' parameter. The application failed to implement allowlisting of permitted domains, restrict to external URLs only, or validate that user-controlled input could not be manipulated to target internal resources.

## Attacker mindset
An attacker would recognize that dashboard export functionality commonly requires fetching remote resources, making it a natural attack vector. By observing the 'viewUrl' parameter structure, they would attempt parameter manipulation to discover if the server blindly follows user-supplied URLs. The goal would be reconnaissance of internal infrastructure and subsequent targeted exploitation of internal services.

## Defensive takeaways
- Implement strict URL validation: use allowlists of permitted domains/IPs rather than blocklists
- Disable access to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, ::1) in any server-side request functionality
- Enforce HTTPS for external requests and validate SSL/TLS certificates
- Use separate network interfaces or sandboxed environments for handling user-controlled URL requests
- Implement rate limiting and logging for all server-initiated requests
- Apply principle of least privilege: limit network access from application servers to only required external services
- Regularly test SSRF attack vectors during security assessments, particularly in features involving exports, embeds, webhooks, or API integrations
- Use security headers and firewall rules to restrict outbound connections from application servers

## Variant hunting
['Search for other export/download features that accept URL parameters (PDF generation, image export, report generation)', 'Identify webhook or callback functionality that accepts user-supplied URLs', 'Look for API integrations, external authentication handlers (OAuth redirects), or proxy-like functionality', 'Test file upload features that process remote resources or URL schemes in metadata', 'Examine import/migration features that fetch data from user-specified URLs', 'Review dashboard sharing, embedding, or preview features that construct URLs from user input', 'Test email generation features that might fetch resources for inclusion in messages', 'Check for reverse proxy or request forwarding functionality with inadequate validation']

## MITRE ATT&CK
- T1190
- T1570
- T1040
- T1046
- T1018

## Notes
This vulnerability exemplifies a common pattern in web applications where legitimate features (dashboard export, sharing) create SSRF opportunities. The use of relative URIs in the initial parameter was a strong indicator of potential abuse. The vendor (Dundas BI) responded responsibly by patching the vulnerability, demonstrating the importance of coordinated disclosure. The impact depends heavily on: (1) verbosity of error messages returned to attackers, (2) internal network topology and service availability, (3) firewall rules restricting outbound connections, (4) authentication requirements of internal services. This is a classic example of trusting user input in a server-side operation without proper validation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
