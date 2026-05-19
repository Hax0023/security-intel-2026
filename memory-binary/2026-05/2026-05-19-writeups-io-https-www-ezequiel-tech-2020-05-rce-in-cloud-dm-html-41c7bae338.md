# RCE in Google Cloud Deployment Manager via Undocumented googleOptions Field

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Google Cloud Platform Vulnerability Rewards Program (VRP)
- **Bounty:** $164,674 ($31,337 initial + $133,337 2020 GCP VRP prize)
- **Severity:** Critical
- **Vuln types:** Remote Code Execution, Server-Side Request Forgery (SSRF), Improper Input Validation, Information Disclosure
- **Category:** memory-binary
- **Writeup:** https://www.ezequiel.tech/2020/05/rce-in-cloud-dm.html

## Summary
An attacker could achieve RCE on Google Cloud Deployment Manager by leveraging an undocumented 'googleOptions' field when creating Type Providers, which allowed requests to internal Google endpoints through the Global Service Load Balancer. By crafting requests to internal APIs like App Engine Admin API or Issue Tracker Corp API, an attacker could issue complex internal requests and potentially execute arbitrary code.

## Attack scenario (step by step)
1. Attacker discovers the undocumented 'googleOptions' field in the Type Provider creation API through reverse engineering or documentation analysis
2. Attacker crafts a malicious Type Provider request with googleOptions parameter pointing to an internal Google service endpoint
3. Deployment Manager processes the async operation and attempts to retrieve a descriptor document from the specified internal URL
4. The request traverses Google's Global Service Load Balancer and reaches internal services that are not directly accessible from external networks
5. If the request succeeds, attacker can issue complex internal API calls to privileged services; if it fails, error messages may leak sensitive information about internal infrastructure
6. Attacker leverages the SSRF/RCE capability to compromise internal services or escalate privileges within Google Cloud infrastructure

## Root cause
The Deployment Manager beta API accepted an undocumented 'googleOptions' field in Type Provider creation requests without proper validation or authorization checks. This field bypassed network isolation controls by routing requests through Google's internal load balancer, allowing access to services that should only be reachable from within Google's network. Additionally, the async operation error handling exposed internal server responses containing sensitive information.

## Attacker mindset
Patient, methodical researcher who combined multiple reconnaissance techniques (template injection, exception handling, API enumeration) over an extended period. When direct approaches failed, the attacker persisted by exploring undocumented API features and studying error messages for clues about internal infrastructure. The discovery of 'googleOptions' likely came from API documentation review or fuzzing of Type Provider parameters.

## Defensive takeaways
- Implement strict schema validation for all API inputs; reject unknown/undocumented fields rather than silently processing them
- Apply network segmentation to ensure internal APIs are inaccessible from external-facing services, regardless of request source
- Sanitize error messages to avoid leaking internal infrastructure details, endpoint names, or server responses
- Regularly audit beta/v2beta APIs for security gaps before graduating to general availability
- Implement explicit allowlist controls for Type Provider descriptor URLs to prevent SSRF to internal services
- Add logging and alerting for async operations that attempt to access internal endpoints
- Conduct security reviews of undocumented fields and ensure all API surface is intentionally designed
- Use authentication/authorization checks separate from network controls as defense-in-depth

## Variant hunting
['Search for other undocumented fields in Google Cloud API requests across different services (esp. beta APIs)', 'Test other async operations in Deployment Manager and related services for similar SSRF/RCE patterns', 'Examine error handling in other Google Cloud services for information disclosure via detailed error messages', 'Fuzz Type Provider and Custom Resource creation endpoints with various internal field names (googleOptions variants, internalConfig, etc.)', 'Review other Google services that use internal Deployment Manager instances for similar bypass techniques', 'Test for SSRF via descriptor URL validation bypasses (DNS rebinding, IPv6 syntax, URL encoding tricks)']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1589: Gather Victim Identity Information
- T1590: Gather Victim Network Information
- T1557: Man-in-the-Middle
- T1021: Remote Services
- T1552: Unsecured Credentials
- T1040: Traffic Sniffing

## Notes
This vulnerability demonstrated the risks of beta/undocumented API features reaching production without security hardening. The researcher's patience across multiple failed attempts and eventual success highlights the importance of persistent, methodical security research. The significant bounty ($164,674) reflects the critical nature of achieving RCE on internal Google infrastructure. The vulnerability required understanding of Google Cloud architecture, async operation patterns, and network isolation controls.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
