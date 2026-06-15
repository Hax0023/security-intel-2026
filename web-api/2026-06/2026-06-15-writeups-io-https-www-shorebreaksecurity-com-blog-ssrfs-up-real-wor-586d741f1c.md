# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Unsafe URL Handling, Insufficient Input Validation
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, allowing attackers to manipulate the 'viewUrl' parameter to force the server to issue arbitrary requests to internal or external resources. The vulnerability exists in the export functionality where user-controlled URL parameters are not properly validated before being used in server-side requests, enabling network reconnaissance and attacks against internal systems.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI that accepts a 'viewUrl' parameter
2. Attacker captures the POST request to the export endpoint and observes the 'viewUrl' parameter contains a relative URI with a shortLink
3. Attacker modifies the 'viewUrl' parameter to point to an internal resource (e.g., 'http://localhost:8080/admin' or '192.168.1.100:22')
4. Server processes the request and makes an outbound connection to the attacker-specified resource on behalf of the application
5. Attacker uses error messages and response codes to identify open ports, services, and internal network topology
6. Attacker escalates by targeting vulnerable internal services accessible only from the compromised server

## Root cause
The application fails to validate and sanitize the 'viewUrl' parameter before using it in server-side HTTP requests. The parameter is treated as trusted user input without implementing allowlist validation, URL scheme restrictions, or checks for private IP addresses and reserved ports. The export feature directly interpolates user-controlled URL values into requests issued by the server.

## Attacker mindset
An attacker exploiting this would approach it methodically: first mapping network topology through port scanning using differential error responses, then pivoting to attack internal services (databases, admin panels, APIs) that are unreachable from the internet but accessible from the compromised application server. The attacker recognizes that the export feature represents a trust boundary violation—the server legitimizes and forwards arbitrary requests.

## Defensive takeaways
- Implement strict allowlist validation for all URL parameters; only permit expected domains/paths
- Enforce URL scheme whitelisting (only http/https if applicable) and reject file://, gopher://, etc.
- Reject requests to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, ::1/128)
- Disable or restrict access to sensitive ports (22, 23, 25, 135-139, 445, 3306, 5432, 6379, 27017, etc.)
- Implement timeout and size limits on server-initiated requests to prevent abuse
- Use URL parsing libraries correctly; avoid string manipulation or regex for URL validation
- Apply principle of least privilege—minimize what the application server can reach network-wise
- Log and monitor outbound requests from the application for anomalies
- Disable unnecessary URL schemes and protocols at the network/firewall level

## Variant hunting
['Search for other export/download features accepting URL parameters (PDF export, image export, report generation)', "Look for API endpoints that accept 'url', 'link', 'resource', 'endpoint', 'target' parameters", 'Identify webhook/callback features that might construct outbound requests', 'Test file upload features with remote URL fetching (e.g., image upload from URL)', 'Examine email notification features that might include links or remote content', 'Review embedded analytics or dashboard features that may accept external data sources', 'Test reverse proxy or forwarding features that might relay requests to user-specified targets', 'Look for import features that fetch configuration/data from external sources']

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1021 Remote Services
- T1046 Network Service Discovery
- T1040 Network Sniffing
- T1557 Adversary-in-the-Middle
- T1557.002 ARP Cache Poisoning

## Notes
This vulnerability was responsibly disclosed to Dundas BI, who patched it promptly. The case study effectively demonstrates how common business features (export/sharing) can become attack vectors when user input isn't validated. The key insight is that 'viewUrl' appeared to be a relative URI, suggesting developers may have assumed it would stay relative, but failed to enforce this assumption. The vulnerability's impact depends on internal network architecture and service accessibility. Error-based SSRF techniques (where timing/error messages reveal information) are particularly valuable for reconnaissance when blind SSRF is encountered.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
