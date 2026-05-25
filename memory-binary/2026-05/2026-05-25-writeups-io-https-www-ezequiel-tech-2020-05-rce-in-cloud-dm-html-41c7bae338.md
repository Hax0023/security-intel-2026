# RCE in Google Cloud Deployment Manager via Undocumented googleOptions Field

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Google Cloud Platform Vulnerability Reward Program (VRP)
- **Bounty:** $164,674 total ($31,337 initial + $133,337 2020 GCP VRP prize)
- **Severity:** Critical
- **Vuln types:** Remote Code Execution, Server-Side Request Forgery (SSRF), Information Disclosure, Insufficient Access Controls
- **Category:** memory-binary
- **Writeup:** https://www.ezequiel.tech/2020/05/rce-in-cloud-dm.html

## Summary
A critical vulnerability in Google Cloud Deployment Manager allowed attackers to issue requests to internal Google APIs by creating Type Providers with an undocumented 'googleOptions' field. By manipulating descriptor URLs and leveraging Google's internal load balancer, attackers could potentially achieve RCE through internal endpoints like App Engine Admin API and Issue Tracker APIs.

## Attack scenario (step by step)
1. Attacker identifies the undocumented 'googleOptions' field in the Type Provider creation API
2. Attacker crafts a malicious Type Provider request targeting an internal Google API endpoint (e.g., issuetracker.corp.googleapis.com or App Engine Admin API test version)
3. Deployment Manager's async operation attempts to retrieve a descriptor document from the attacker-specified URL through Google's internal load balancer
4. If the request reaches the internal endpoint, Deployment Manager may successfully communicate with the internal service, bypassing external access restrictions
5. Error messages in failed operations leak sensitive information about internal server responses and configurations
6. Attacker uses successful communication to issue complex internal requests or chain with other vulnerabilities for RCE

## Root cause
Deployment Manager exposed an undocumented 'googleOptions' field that was not properly validated or restricted. The service failed to adequately control which URLs Type Providers could communicate with, allowing requests to internal Google services through the internal load balancer. The lack of input validation on the descriptor URL combined with insufficient access controls on internal endpoints enabled SSRF to internal systems.

## Attacker mindset
Determined researcher who methodically explored Deployment Manager's attack surface through multiple vectors (hidden types, template injection, private IP exploration). Persistence was key—after initial failures attempting direct internal API access, the attacker pivoted to discovering undocumented API fields that became the breakthrough. The researcher understood that Google services often use infrastructure they expose publicly, creating potential internal access paths.

## Defensive takeaways
- Implement strict allowlist validation for all URL/endpoint parameters, especially those that trigger outbound requests
- Enforce consistent access controls—internal-only services must be blocked from external API requests regardless of network origin
- Audit and document ALL API fields, removing or properly controlling undocumented parameters that may bypass security controls
- Implement rate limiting and monitoring on requests attempting to access internal endpoints through service proxies
- Separate internal and external load balancers/routing logic to prevent internal service exposure through external APIs
- Add explicit validation rejecting requests to internal domains and private IP ranges at the API handler level
- Implement comprehensive logging of descriptor URL resolution attempts and error messages to detect reconnaissance activity
- Restrict async operations from making requests to unauthenticated or insufficiently authenticated internal services

## Variant hunting
['Search other Google Cloud services for undocumented fields that trigger outbound requests (Cloud Functions, Cloud Run, App Engine, Cloud Composer)', "Test similar 'options' or 'config' fields in other GCP services that handle external URLs or webhooks", 'Enumerate other internal Google API endpoints beyond those mentioned, testing descriptor resolution against each', 'Investigate whether similar Type Provider vulnerabilities exist in other infrastructure-as-code services (Terraform providers, CloudFormation, etc.)', 'Test whether the googleOptions field exists in v2 (GA) version of Deployment Manager API, not just v2beta', 'Probe for similar SSRF vectors in service mesh configurations, API gateways, and webhook handlers across GCP', 'Check if other Type Providers or resource types accept undocumented fields that could bypass validation']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1557 - Adversary-in-the-Middle
- T1021 - Remote Services
- T1105 - Ingress Tool Transfer
- T1059 - Command and Scripting Interpreter

## Notes
This vulnerability was a first-place winner of the 2020 GCP VRP prize. The researcher demonstrated exceptional persistence, pivoting from multiple failed approaches to eventually discover the undocumented field. The vulnerability highlights the risks of internal dogfood systems being reachable through production APIs and the importance of explicit field documentation and validation. LiveOverflow created an educational video explaining the discovery methodology.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
