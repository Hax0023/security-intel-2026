# SSRF in Dundas BI Dashboard Export Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Dundas BI (Business Intelligence)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Server-Side Request Forgery (SSRF), URL Manipulation, Unvalidated Redirect
- **Category:** web-api
- **Writeup:** https://www.shorebreaksecurity.com/blog/ssrfs-up-real-world-server-side-request-forgery-ssrf/

## Summary
A Server-Side Request Forgery vulnerability was discovered in Dundas BI's dashboard export feature, which allows attackers to manipulate the 'viewUrl' parameter to force the server to make arbitrary requests. The vulnerability enables internal network scanning, port enumeration, and attacks against internal services not exposed to the internet. The vendor was responsibly notified and released a patched version.

## Attack scenario (step by step)
1. Attacker identifies the dashboard export functionality that accepts a 'viewUrl' parameter in POST requests
2. Attacker manipulates the 'viewUrl' parameter to point to internal network resources (e.g., http://192.168.1.1:8080)
3. Server processes the request and attempts to fetch the resource, revealing information through error messages or response timing
4. Attacker uses differential response analysis to determine open ports and services on internal networks
5. Attacker targets specific internal HTTP services (databases, APIs, admin panels) discovered through reconnaissance
6. Attacker leverages SSRF to interact with internal systems, potentially escalating to data exfiltration or unauthorized access

## Root cause
Insufficient input validation and lack of URL scheme/destination restrictions on the 'viewUrl' parameter. The application did not implement a whitelist of allowed domains or prevent requests to private IP ranges (RFC1918), allowing arbitrary server-side requests.

## Attacker mindset
Reconnaissance-focused adversary seeking to map internal network topology and identify attack surface. The attacker recognizes that export features commonly perform server-side operations and deliberately tests parameters controlling resource fetching. They iterate on payloads based on error message responses to enumerate services.

## Defensive takeaways
- Implement strict URL validation: whitelist allowed domains/protocols and reject private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16)
- Use URL parsing libraries to prevent bypass techniques (e.g., DNS rebinding, IPv6 addresses, octal notation)
- Disable unnecessary URL schemes (file://, gopher://, etc.) and restrict to https/http only
- Implement network segmentation to limit impact if SSRF is exploited
- Use DNS allowlisting and avoid public DNS resolvers that could be exploited for DNS rebinding
- Log and monitor all outbound requests from the application server
- Implement timeout and size limits on responses to prevent amplification attacks
- Apply principle of least privilege to application service accounts and network firewall rules

## Variant hunting
['Test all file upload/export features for SSRF via parameters controlling resource URLs', 'Search for other parameters accepting URLs: imageUrl, redirectUrl, callbackUrl, webhookUrl, proxyUrl', 'Test link preview/thumbnail generation features commonly found in social platforms and communication tools', 'Examine metadata extraction features (PDF, image EXIF data parsing) that may fetch remote resources', 'Look for webhook implementations that construct requests to user-controlled URLs', 'Test mail server features (sending test emails) that may construct SMTP requests', 'Review external API integrations that proxy user-supplied endpoints', 'Check for SSRF in file format conversion services that may fetch source documents']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1200 - Hardware Additions
- T1046 - Network Service Discovery
- T1592 - Gather Victim Network Information
- T1040 - Network Sniffing
- T1021 - Remote Services
- T1078 - Valid Accounts

## Notes
This writeup serves as an educational resource on SSRF exploitation methodology rather than a specific bounty disclosure. The Dundas BI vendor responsibly patched the vulnerability. The article emphasizes the importance of error message analysis and differential response timing in SSRF exploitation. The conceptual overlap between SSRF and RFI is noted, with key distinction that SSRF typically doesn't enable code execution but facilitates network reconnaissance and internal service attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
