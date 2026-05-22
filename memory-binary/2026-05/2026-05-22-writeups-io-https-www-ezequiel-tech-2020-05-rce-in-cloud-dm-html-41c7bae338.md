# RCE in Google Cloud Deployment Manager via Undocumented googleOptions Field

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Google Cloud Platform VRP (Vulnerability Rewards Program)
- **Bounty:** $164,674 (initial $31,337 + additional $133,337 prize)
- **Severity:** Critical
- **Vuln types:** Remote Code Execution, Server-Side Request Forgery (SSRF), Information Disclosure, API Abuse
- **Category:** memory-binary
- **Writeup:** https://www.ezequiel.tech/2020/05/rce-in-cloud-dm.html

## Summary
A critical RCE vulnerability existed in Google Cloud Deployment Manager that allowed attackers to issue arbitrary requests to internal Google endpoints by creating a Type Provider with an undocumented googleOptions field. This enabled attackers to interact with internal Google APIs and potentially achieve remote code execution through the Global Service Load Balancer.

## Attack scenario (step by step)
1. Attacker discovers the undocumented googleOptions field in Deployment Manager's Type Provider creation API
2. Attacker crafts a malicious Type Provider creation request including the googleOptions parameter pointing to an internal Google endpoint
3. Deployment Manager initiates an async operation to retrieve a descriptor document from the attacker-controlled URL
4. The internal request is routed through Google's Global Service Load Balancer to internal services (App Engine Admin API, Issue Tracker Corp API, etc.)
5. Upon failure, the error response leaks sensitive information from internal endpoints; upon success, attacker can issue complex authenticated requests
6. Attacker leverages internal API access to escalate privileges, access sensitive data, or achieve RCE

## Root cause
An undocumented field (googleOptions) in the Type Provider API allowed bypassing external-only restrictions and routing requests through Google's internal load balancer. The async descriptor document retrieval mechanism did not properly validate or restrict the target endpoints, and error messages leaked information from internal services.

## Attacker mindset
The attacker demonstrated patience and methodical research, starting with surface-level reconnaissance (hidden types, template injection) before pivoting to API structure analysis. The discovery involved understanding Google's internal architecture, service boundaries, and load balancer routing logic—classic insider knowledge exploitation or sophisticated external research.

## Defensive takeaways
- Implement strict allowlisting for all outbound network requests from cloud services; reject internal/private IPs and internal domain patterns
- Remove or redact sensitive information from error messages returned to users; never expose internal service responses
- Audit all API parameters for undocumented fields; disable or properly validate any legacy/internal parameters accessible to users
- Implement network-level segmentation preventing customer-controlled services from accessing internal service mesh or load balancers
- Use separate authentication/authorization contexts for internal vs. external operations; require additional verification for internal endpoint access
- Conduct regular security audits of beta/internal API versions before GA release to identify undocumented attack surfaces
- Implement request validation and sanitization at load balancer level to prevent SSRF attacks targeting internal services

## Variant hunting
['Search for other undocumented fields in beta/v2beta API endpoints across GCP services', 'Test other GCP services using Infrastructure-as-Code (IaC) patterns for similar SSRF/internal endpoint access vulnerabilities', 'Examine async operation handlers across GCP for information disclosure in error messages', 'Investigate whether googleOptions field exists in other Google Cloud APIs beyond Deployment Manager', 'Test Type Provider creation with variations of internal Google domain names and IP addresses to find bypass techniques', 'Analyze other service load balancer routing mechanisms for similar SSRF vulnerabilities', 'Look for similar undocumented parameters in API schemas and API discovery documents']

## MITRE ATT&CK
- T1190
- T1021
- T1552.007
- T1526
- T1091
- T1105

## Notes
This vulnerability was selected as first place winner of the 2020 GCP VRP prize and received significant media attention (LiveOverflow video explanation). The bug demonstrates the danger of undocumented API parameters and the importance of treating beta/internal API versions as security-critical. The researcher's methodical approach—starting with obvious vectors and gradually pivoting based on failed assumptions—is exemplary bug bounty methodology. The vulnerability chain leveraged legitimate async operations + SSRF + information disclosure to achieve RCE potential.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
