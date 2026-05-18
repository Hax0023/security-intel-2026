# RCE in Google Cloud Deployment Manager via Undocumented googleOptions Field

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Google Cloud Platform Vulnerability Reward Program (VRP)
- **Bounty:** $164,674 ($31,337 initial + $133,337 prize)
- **Severity:** Critical
- **Vuln types:** Remote Code Execution, Server-Side Request Forgery (SSRF), Information Disclosure, Improper Access Control
- **Category:** memory-binary
- **Writeup:** https://www.ezequiel.tech/2020/05/rce-in-cloud-dm.html

## Summary
A critical RCE vulnerability was discovered in Google Cloud Deployment Manager through an undocumented googleOptions field in Type Provider creation requests. This allowed attackers to make requests to internal Google APIs and endpoints through the Global Service Load Balancer, potentially leading to RCE on internal systems.

## Attack scenario (step by step)
1. Attacker discovers the undocumented googleOptions field in Deployment Manager Type Provider API
2. Attacker crafts a malicious Type Provider creation request with googleOptions parameter and internal Google API endpoint (e.g., issuetracker.corp.googleapis.com)
3. Deployment Manager processes the async operation and attempts to retrieve descriptor document from attacker-controlled or internal URL
4. Request reaches internal Google infrastructure through Global Service Load Balancer, bypassing external access restrictions
5. Attacker either gains information from error messages revealing internal API responses or successfully issues complex internal API requests
6. Successful requests to internal APIs (App Engine Admin, Issue Tracker) could lead to arbitrary code execution or privilege escalation

## Root cause
Deployment Manager failed to properly validate and restrict the undocumented googleOptions field, allowing it to be used for arbitrary HTTP requests to internal endpoints. The implementation did not enforce proper network segmentation or request validation, permitting access to internal Google services through the Global Service Load Balancer.

## Attacker mindset
Methodical security researcher who persisted through multiple failed approaches (inspecting Python templates, attempting direct internal API access) before discovering the undocumented feature. Focused on API enumeration and gradual feature discovery rather than common vulnerability patterns.

## Defensive takeaways
- Remove or properly restrict undocumented API fields that bypass security controls
- Implement strict URL validation and whitelist for external service endpoints accessed by management APIs
- Enforce network segmentation between user-facing APIs and internal infrastructure
- Validate and sanitize all parameters in async operations before making external requests
- Implement proper access controls for internal endpoints accessed through load balancers
- Audit error messages to avoid leaking sensitive information about internal infrastructure
- Regularly scan for hidden or beta API parameters that may circumvent security controls

## Variant hunting
['Search for other undocumented fields in Google Cloud API methods that accept URLs or endpoints', 'Audit v2beta API versions of other Google Cloud services for similar bypass mechanisms', 'Test other infrastructure-as-code services (Terraform, CloudFormation) for SSRF via descriptor/template URLs', 'Examine other Type Provider-like features in Google Cloud for internal endpoint access', 'Look for similar patterns in custom resource definitions or external service integrations']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1021: Remote Services
- T1057: Process Discovery
- T1552: Unsecured Credentials
- T1526: Cloud Service Discovery
- T1199: Trusted Relationship
- T1021.004: SSH

## Notes
This vulnerability won first place in the 2020 GCP VRP prize. The researcher's persistence through multiple failed attempts demonstrates the value of methodical API exploration. The use of an undocumented field to bypass security controls is a classic pattern worth hunting for in other cloud services. The high bounty reflects the severity and potential impact of RCE on internal Google infrastructure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
