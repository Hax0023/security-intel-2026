# Digging for SSRF in Next.js Apps

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Unknown
- **Bounty:** Unknown
- **Severity:** unknown
- **Vuln types:** Server-Side Request Forgery (SSRF)
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
Research article investigating Server-Side Request Forgery (SSRF) vulnerabilities in Next.js applications. The article examines attack vectors and exploitation techniques specific to Next.js framework implementations.

## Attack scenario (step by step)
1. Attacker identifies a Next.js application endpoint that accepts user-controlled input
2. Attacker crafts a malicious request containing a URL parameter pointing to internal services
3. The vulnerable Next.js application processes the request without proper validation of the destination
4. The application makes a server-side request to the attacker-controlled URL or internal resource
5. Attacker exfiltrates sensitive data from internal services, metadata endpoints, or local resources
6. Attacker pivots to internal network reconnaissance or accesses protected resources

## Root cause
Insufficient input validation and URL filtering in Next.js API routes or server-side functions that perform HTTP requests without proper sanitization of user-supplied URLs

## Attacker mindset
An attacker seeks to bypass network boundaries and access internal resources by leveraging the server's ability to make outbound requests, focusing on Next.js-specific patterns that may lack robust SSRF protections

## Defensive takeaways
- Implement strict URL validation and allowlisting for any server-side HTTP requests in Next.js applications
- Restrict outbound connections from application servers to internal IP ranges and private network addresses
- Use URL parsing libraries to validate URLs and prevent bypasses using URL encoding or alternative formats
- Apply network segmentation to limit the impact of SSRF by isolating sensitive internal services
- Monitor and log all outbound requests made by the application for anomaly detection
- Disable or restrict access to cloud metadata endpoints (AWS IMDSv1, GCP metadata API) from application code

## Variant hunting
['Test all API routes and server-side functions accepting URL parameters or file paths', 'Check for SSRF in Next.js Image Optimization feature which handles external image URLs', 'Examine getServerSideProps and getStaticProps functions for unsafe external requests', 'Investigate middleware and API route handlers that proxy requests', 'Test for SSRF in webhook handlers, notification systems, and PDF/screenshot generation features', 'Look for bypasses using alternative URL schemes (file://, gopher://, dict://) in Next.js contexts']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1018 - Remote System Discovery
- T1580 - Cloud Infrastructure Discovery
- T1040 - Traffic Sniffing

## Notes
The provided content appears to be a page header/footer rather than the full research article. The actual detailed technical content of the SSRF research article was not accessible in the provided snippet. This analysis is based on the title and inferred content about SSRF in Next.js applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
