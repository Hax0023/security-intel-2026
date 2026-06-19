# SSRF in Dundas BI Dashboard Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Dundas BI (Commercial Business Intelligence Product)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Improper Input Validation, URL Manipulation
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, which allows attackers to manipulate the 'viewUrl' parameter to force the server to make arbitrary HTTP requests to internal or external resources. The vulnerability exists in the export-to-image functionality where user-controlled URL parameters are not properly validated before being used by the server to fetch resources. This enables attackers to scan internal networks, access restricted services, or attack backend systems.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export feature in Dundas BI web interface
2. Attacker intercepts the POST request to the export endpoint and observes the 'viewUrl' parameter containing a relative URI
3. Attacker modifies 'viewUrl' to point to an internal IP address and port (e.g., http://192.168.1.1:8080)
4. Server processes the malicious request and attempts to fetch the resource, allowing port scanning of internal networks
5. Attacker analyzes error messages and response times to map internal infrastructure and identify running services
6. Attacker crafts targeted SSRF requests to exploit internal services (databases, admin panels, metadata endpoints) to escalate privileges or extract sensitive data

## Root cause
The application fails to properly validate and sanitize the 'viewUrl' parameter before using it in server-side HTTP requests. The vulnerable code does not implement allowlist validation, URL scheme restrictions, or private IP range blocking, allowing arbitrary URLs to be processed.

## Attacker mindset
An attacker would recognize that export/rendering features often involve server-side resource fetching and proactively test such features with non-standard URLs. They would leverage error message verbosity to distinguish between open/closed ports and gradually map the internal network topology. The goal would be to identify and attack internal services that are not directly accessible from the internet but accessible from the vulnerable server.

## Defensive takeaways
- Implement strict URL validation with allowlist/whitelist of permitted domains and protocols
- Reject requests to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16)
- Use URL parsing libraries to validate scheme, host, and port before making requests
- Implement network segmentation to limit server's ability to access internal resources
- Disable HTTP redirects or strictly control redirect destinations
- Implement request timeouts and rate limiting on export features
- Log and monitor all outbound requests made by the application
- Use separate credentials and service accounts with minimal necessary permissions for internal requests
- Conduct security testing of all features that fetch external resources or process user-supplied URLs

## Variant hunting
Search for other export/rendering features in web applications (PDF export, image conversion, document generation, report scheduling). Test any parameters containing URLs or file paths. Look for analytics, BI, reporting, or integration platforms that process external data. Examine webhook implementations, URL preview/metadata features, link checkers, and screenshot tools. Test API endpoints accepting URL parameters and proxy/forwarding features.

## MITRE ATT&CK
- T1190
- T1552
- T1526
- T1046

## Notes
This was a real-world vulnerability in commercial software following responsible disclosure. The vendor (Dundas BI) was responsive to the report and released patches promptly. The vulnerability demonstrates how seemingly benign features (dashboard export) can introduce significant security risks. Error message analysis and response differentiation are critical components of SSRF exploitation for network reconnaissance. The writeup effectively illustrates the progression from vulnerability discovery to exploitation to internal network mapping.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
