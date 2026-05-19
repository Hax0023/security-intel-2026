# Server-Side Request Forgery (SSRF) in Dundas BI Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Dundas BI (Business Intelligence)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Server-Side Request Forgery (SSRF), URL Manipulation, Unvalidated Redirect
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, where the 'viewUrl' parameter could be manipulated to force the server to make arbitrary requests to internal or external resources. The vulnerability existed in the export functionality that allowed users to share dashboards as images, enabling attackers to perform internal network reconnaissance, port scanning, and attacks against backend systems.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI that accepts a 'viewUrl' parameter
2. Attacker crafts a malicious POST request to the export endpoint with a modified 'viewUrl' pointing to an internal IP address (e.g., 192.168.1.1)
3. Server processes the request and attempts to fetch the resource from the attacker-specified internal IP address
4. Attacker analyzes server responses (timeout, refused, success) to map internal network topology and identify open ports
5. Attacker performs targeted attacks against discovered internal services (databases, admin panels, metadata services)
6. Attacker escalates access by exploiting internal systems not exposed to the internet but accessible from the vulnerable server

## Root cause
The application failed to validate and sanitize the 'viewUrl' parameter before using it in server-side HTTP requests. No URL whitelist/blacklist was implemented to restrict requests to legitimate external resources, allowing arbitrary URL schemes and internal IP addresses to be specified.

## Attacker mindset
An attacker would recognize that user-supplied URL parameters in export/sharing features are common SSRF vectors. They would systematically test different URL formats (internal IPs, localhost, different ports/protocols) and leverage verbose error messages to map internal infrastructure. The goal would be reconnaissance and lateral movement to attack backend systems not directly exposed to the internet.

## Defensive takeaways
- Implement strict URL validation: maintain whitelist of allowed domains/protocols, reject internal IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, ::1)
- Use URL parsing libraries to validate scheme, host, and port before making requests
- Implement network-level controls: use egress firewalls to restrict server outbound connections
- Avoid exposing detailed error messages that reveal connection status; use generic error responses
- Require user authentication and authorization checks before processing resource requests
- Consider disallowing certain protocols (file://, gopher://, dict://) and restricting to HTTPS only
- Implement request rate limiting and monitoring for unusual access patterns
- Use allowlists for external resources rather than blacklists

## Variant hunting
Search for other export/sharing features accepting URL parameters (PDF export, email sharing, webhook configuration). Look for API endpoints accepting 'url', 'callback', 'redirect', 'endpoint', 'proxy', 'target' parameters. Test image embedding features, document preview functionality, external API integrations, and webhook/notification systems. Check for URL schemes like file://, gopher://, dict://, ldap://, and jar:// in addition to HTTP/HTTPS.

## MITRE ATT&CK
- T1190
- T1498
- T1046
- T1087
- T1589

## Notes
This vulnerability was responsibly disclosed to Dundas BI, which released a patched version promptly. The writeup effectively explains SSRF conceptually and demonstrates a real-world exploitation scenario. The vulnerability's impact depends on internal network topology and the services accessible from the vulnerable server. Error message verbosity is critical for successful exploitation—overly detailed responses enable attackers to distinguish between open ports, closed ports, and filtered connections.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
