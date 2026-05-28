# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln types:** Server-Side Request Forgery (SSRF), Insufficient Input Validation, Unvalidated Redirects
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, where the 'viewUrl' parameter could be manipulated to force the server to make arbitrary requests to internal or external resources. The vulnerability existed in the export functionality that allows users to share dashboards in various formats, with user-controlled URL parameters not being properly validated.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI web application
2. Attacker intercepts the POST request containing the 'viewUrl' parameter
3. Attacker modifies 'viewUrl' from a relative URI to an arbitrary internal IP address (e.g., 'http://192.168.1.1:8080')
4. Server processes the request and attempts to fetch the attacker-specified resource, bypassing firewall restrictions
5. Attacker analyzes response codes and error messages to map internal network topology and services
6. Attacker leverages discovered internal services for further attacks (port scanning, accessing internal APIs, credential harvesting)

## Root cause
The 'viewUrl' parameter in the dashboard export endpoint accepted user-supplied input without proper validation or sanitization. The application failed to implement URL scheme validation, prevent access to private/reserved IP ranges (RFC 1918, 127.0.0.0/8, 169.254.0.0/16), or restrict the target of server-initiated requests to whitelisted domains.

## Attacker mindset
An attacker would recognize the export feature as a trusted internal operation and exploit it to bypass network segmentation. The attacker would methodically use error messages and response times to enumerate the internal network architecture, then pivot to attacking internal services (databases, admin panels, APIs) that are invisible from the internet but accessible from the vulnerable application server.

## Defensive takeaways
- Implement strict URL validation: reject non-HTTP(S) schemes and private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16, 0.0.0.0/8)
- Use URL parsing libraries to normalize and validate URLs before server-side requests
- Maintain a whitelist of allowed domains/IPs for external requests rather than blacklisting
- Disable access to cloud metadata services (169.254.169.254) and internal DNS resolution where possible
- Implement network-level controls: restrict outbound connections from application servers to necessary services only
- Use DNS rebinding protections and implement TOCTOU checks
- Log and monitor all server-initiated outbound requests for anomalies
- Apply principle of least privilege: run application with minimal network access required
- Conduct security testing specifically for SSRF vectors during code review and penetration testing

## Variant hunting
['Search for other export/reporting features that accept URL parameters (PDF export, email delivery, scheduled reports)', 'Look for webhook functionality, callback URLs, or redirect parameters', 'Test image/media embedding features, favicon fetchers, and link preview generators', 'Examine authentication integrations that perform external API calls or LDAP/SAML lookups', 'Check for XML external entity (XXE) injection vulnerabilities which share similar exploitation patterns', 'Review any proxy or forwarding functionality in the application', 'Test GraphQL implementations for aliases to internal services', 'Examine webhook destinations, notification URLs, and subscription callbacks']

## MITRE ATT&CK
- T1190
- T1570
- T1559
- T1021
- T1046

## Notes
This writeup serves as an educational case study on SSRF vulnerabilities in commercial enterprise software. The vendor (Dundas Data Visualization, Inc.) responded responsibly to disclosure and released patches. The vulnerability demonstrates how trusted internal operations (export features) can become attack vectors when user input flows into critical security-sensitive operations (server-initiated requests). The conceptual similarity to RFI vulnerabilities and the effectiveness against network reconnaissance makes SSRF a critical vulnerability class to test during security assessments of web applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
