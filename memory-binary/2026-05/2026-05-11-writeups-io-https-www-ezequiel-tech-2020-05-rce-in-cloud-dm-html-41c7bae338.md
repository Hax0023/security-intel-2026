# RCE in Google Cloud Deployment Manager via Undocumented googleOptions Field

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Google Cloud Platform Vulnerability Reward Program (VRP)
- **Bounty:** $164,674 ($31,337 initial + $133,337 VRP prize)
- **Severity:** critical
- **Vuln types:** Remote Code Execution, Server-Side Request Forgery (SSRF), Privilege Escalation, Information Disclosure
- **Category:** memory-binary
- **Writeup:** https://www.ezequiel.tech/2020/05/rce-in-cloud-dm.html

## Summary
A critical RCE vulnerability in Google Cloud Deployment Manager was discovered through an undocumented 'googleOptions' field in Type Provider creation requests. This allowed attackers to issue requests to internal Google endpoints through the Global Service Load Balancer, potentially leading to remote code execution and access to sensitive internal APIs. The vulnerability was chained with SSRF capabilities to target internal Google services that would normally be inaccessible from external sources.

## Attack scenario (step by step)
1. Attacker creates a Type Provider in Deployment Manager v2beta API using an undocumented 'googleOptions' parameter
2. Attacker specifies a descriptorUrl pointing to an internal Google endpoint (e.g., internal App Engine Admin API, Issue Tracker API, or GAIA backend)
3. Deployment Manager attempts to fetch the descriptor document from the specified URL through Google's internal network (bypassing external restrictions)
4. If the request fails, error messages may leak sensitive information about internal server responses; if successful, attacker can issue complex requests to internal services
5. Attacker leverages the successful internal request capability to interact with privileged APIs and potentially execute code through chained exploits
6. Attacker exfiltrates data or gains unauthorized access to internal Google infrastructure

## Root cause
Deployment Manager exposed an undocumented 'googleOptions' field in the Type Provider API that allowed callers to specify arbitrary descriptor URLs. The service failed to properly validate and restrict which endpoints could be accessed, and made requests from a privileged internal context that had access to Google's internal networks and services. The async operation handling also leaked error information that could reveal internal infrastructure details.

## Attacker mindset
Methodical researcher who systematically explored Deployment Manager's attack surface through multiple approaches: examining internal Types, exploiting template interpretation, testing API access patterns, and eventually discovering an undocumented parameter that bypassed security controls. The attacker demonstrated patience and pivoted strategies when initial approaches failed, ultimately finding a high-impact vulnerability through careful API exploration.

## Defensive takeaways
- Validate and whitelist all URL destinations in service-to-service communication, especially those involving infrastructure management tools
- Never expose undocumented or internal API parameters, even if not officially supported
- Implement strict network segmentation to prevent infrastructure services from accessing internal-only endpoints
- Sanitize and limit error messages returned in async operations to prevent information disclosure about internal infrastructure
- Conduct regular security audits of beta/internal API versions, which may lack the same security controls as GA versions
- Restrict which internal services can be accessed from user-controlled configuration parameters
- Implement request signing and validation for internal API calls to ensure they originate from authorized services

## Variant hunting
['Check for similar undocumented parameters in other Google Cloud services that accept external URLs or endpoints', 'Search for SSRF vectors in other infrastructure management services (Terraform Provider APIs, Cloud Composer, etc.)', 'Test for information disclosure in error messages across Google Cloud async operations', 'Examine other v2beta APIs for undocumented fields that may have been left unprotected', 'Look for similar descriptor/endpoint configuration patterns in other Google services', 'Check custom resource providers and plugin systems for improper URL validation']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1021 - Remote Service Session Hijacking
- T1098 - Valid Accounts
- T1552 - Unsecured Credentials
- T1526 - Exposure of Sensitive Data
- T1105 - Ingress Tool Transfer
- T1548 - Abuse of Elevation Control Mechanism

## Notes
This vulnerability demonstrates the dangers of exposing infrastructure management APIs with inadequate input validation. The use of an undocumented parameter suggests the field may have been added for internal testing/dogfooding without proper security review before being exposed. The 2020 VRP prize of $133,337 was exceptionally high, indicating Google's assessment of the severity and impact. The vulnerability required no authentication bypass and could be exploited by any user with Deployment Manager API access in their project. The write-up was chosen as first place for 2020 GCP VRP, and LiveOverflow created an educational video explaining the discovery methodology.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
