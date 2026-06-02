# RCE in Google Cloud Deployment Manager via Undocumented googleOptions Field

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Google Cloud Platform Vulnerability Rewards Program (VRP)
- **Bounty:** $164,674 (initial $31,337 + additional $133,337 VRP prize)
- **Severity:** Critical
- **Vuln types:** Remote Code Execution, Server-Side Request Forgery (SSRF), Information Disclosure, Unsafe Deserialization
- **Category:** memory-binary
- **Writeup:** https://www.ezequiel.tech/2020/05/rce-in-cloud-dm.html

## Summary
By leveraging an undocumented `googleOptions` field in Google Cloud Deployment Manager's Type Provider creation, an attacker could trigger requests to internal Google endpoints through the Global Service Load Balancer. This vulnerability allowed arbitrary requests to internal APIs such as App Engine Admin API and Issue Tracker Corp API, potentially leading to RCE and unauthorized access to internal systems.

## Attack scenario (step by step)
1. Attacker discovers the undocumented `googleOptions` field in Deployment Manager Type Provider API
2. Attacker crafts a malicious request to create a Type Provider with a controlled descriptorUrl and googleOptions parameter
3. Deployment Manager initiates an async operation and attempts to fetch the descriptor document from the specified URL
4. Request traverses through Google's Global Service Load Balancer, reaching internal endpoints inaccessible from external networks
5. Attacker either exploits the internal API endpoint directly or extracts sensitive information from error responses containing internal server data
6. Successful exploitation could allow RCE on internal systems, data exfiltration, or lateral movement within Google's infrastructure

## Root cause
Google Cloud Deployment Manager exposed an undocumented API field (`googleOptions`) that allowed users to specify internal Google endpoints in Type Provider requests. The service failed to properly validate and restrict descriptor URLs to external endpoints only, and the Global Service Load Balancer treated requests from the Deployment Manager service as trusted internal traffic, bypassing network segmentation controls.

## Attacker mindset
A methodical security researcher examining API differences between documented (v2) and beta (v2beta) versions, exploring template injection vectors, then systematically probing internal endpoint access. When external attempts failed, persistence led to discovery of the undocumented field that bypassed restrictions by leveraging the service's trusted network position.

## Defensive takeaways
- Audit all API versions (beta, alpha, dogfood) for undocumented fields that may bypass security controls
- Implement strict URL validation and whitelisting for external-facing services that fetch remote resources; prevent internal IP ranges and internal domain resolution
- Apply consistent authentication and authorization checks regardless of request origin; service-to-service calls should not bypass endpoint restrictions
- Segment internal and external service networks; use network policies to prevent compromised services from accessing sensitive internal endpoints
- Perform threat modeling on async operations that fetch remote resources; validate all untrusted input before passing to external systems
- Implement comprehensive logging and anomaly detection for unusual internal endpoint access patterns
- Regularly scan documentation against actual API implementations to identify undocumented, exposed parameters

## Variant hunting
['Search for other Google Cloud services that support Type Providers or similar plugin/descriptor mechanisms for similar undocumented fields', 'Examine Cloud Functions and Cloud Run deployment mechanisms for similar descriptor URL injection vectors', 'Probe other Google APIs (Kubernetes Engine, Dataflow, etc.) that use async operations with resource fetching for undocumented override fields', 'Test Cloud Build custom builders and integration configurations for similar SSRF vulnerabilities', 'Investigate if googleOptions or similar internal override fields exist in other Cloud Platform services (Firestore, BigQuery, etc.)', 'Check for similar bypass mechanisms in related Google services accessible through service accounts with broad permissions']

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1498 Network Denial of Service
- T1552 Unsecured Credentials
- T1563 Modify Cloud Compute Infrastructure
- T1578 Modify Cloud Compute Infrastructure
- T1591 Gather Victim Org Information
- T1046 Network Service Discovery
- T1021 Remote Services
- T1105 Ingress Tool Transfer

## Notes
This vulnerability was highly impactful due to its position in a foundational Cloud service used for infrastructure management. The undocumented field suggests inadequate API design review processes and insufficient separation between internal and external API surfaces. The researcher's persistence through multiple failed approaches demonstrates the value of comprehensive API enumeration. March 2021 update notes indicate this finding was selected as the top VRP submission for 2020, with LiveOverflow producing educational video content explaining the discovery methodology.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
