# Port of Antwerp-Bruges Asset Enumeration and Scope Change Tracking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Port of Antwerp-Bruges via Intigriti
- **Bounty:** Not specified in writeup
- **Severity:** MEDIUM
- **Vuln types:** Asset Discovery, Scope Enumeration, Infrastructure Exposure, Test Environment Exposure
- **Category:** uncategorised
- **Writeup:** https://huntdash.xyz/

## Summary
A bug bounty dashboard (HuntDash) exposed comprehensive enumeration of Port of Antwerp-Bruges' active bug bounty scope, revealing 51+ targets across production, acceptance, and test environments. The exposure included newly added login pages in test environments and IP ranges, enabling attackers to conduct systematic reconnaissance of the organization's entire attack surface.

## Attack scenario (step by step)
1. Attacker discovers HuntDash.xyz and accesses the publicly visible Port of Antwerp-Bruges scope dashboard
2. Attacker reviews 51+ updated targets including production URLs (api.portofantwerp.com, webapps.portofantwerp.com) and test environments (login-test.portofantwerpbruges.com)
3. Attacker identifies newly added assets (NEW login page annotation) indicating recent infrastructure additions with potentially incomplete security hardening
4. Attacker notes IP ranges (94.107.237.192/26, 188.118.8.0/25) and performs network reconnaissance and service enumeration
5. Attacker prioritizes test/acceptance environment targets (marked as -accpt, -test, webapps-test) for vulnerability research, knowing these have relaxed security controls
6. Attacker maps application stack (Maximo, ServiceDesk, AS2, Unit4 ERP) and targets known vulnerabilities in identified technologies

## Root cause
The HuntDash dashboard provided public visibility into a private bug bounty program's complete scope and target list, including newly deployed assets and multiple environment tiers. This appears to be a public-facing tracking system that inadvertently exposed competitive intelligence and comprehensive attack surface mapping.

## Attacker mindset
An attacker would view this as a treasure map for reconnaissance. The enumeration of 51+ targets with severity ratings, environment classifications (prod/accpt/test), and recently added assets enables systematic targeting. Test environments are particularly valuable as they often have debugging enabled, default credentials, or incomplete security configurations. The asset list reveals the full technology stack and dependency landscape.

## Defensive takeaways
- Restrict access to bug bounty scope dashboards - require authentication and implement IP whitelisting
- Segregate public and private scope information; avoid exposing internal tracking systems to unauthenticated users
- Do not publicly announce new assets or infrastructure additions - wait for security hardening completion
- Implement stricter access controls on test/acceptance environments that are exposed to public bug bounty programs
- Monitor for unauthorized access to scope enumeration tools and implement audit logging
- Use scope change notifications sparingly; batch updates rather than real-time exposure of new targets
- Implement rate limiting and anomaly detection on asset discovery/enumeration endpoints

## Variant hunting
['Search for other public bug bounty tracking dashboards or scope exposure mechanisms across popular platforms', 'Check for exposed Git repositories containing .env files with scope information', 'Look for publicly cached versions of scope pages in archive.org or similar services', 'Search for automated tools that scrape bug bounty platform scope information', 'Investigate API endpoints that may expose scope data (e.g., /api/scopes, /api/targets)', 'Check for misconfigured S3 buckets or cloud storage containing scope documentation', 'Search for leaked emails or Slack messages that contain target lists']

## MITRE ATT&CK
- T1592
- T1589
- T1590
- T1598
- T1591
- T1046
- T1087

## Notes
This writeup lacks technical vulnerability details and instead documents a reconnaissance/information disclosure scenario. The real impact is enabling comprehensive asset enumeration of a critical infrastructure organization (Port of Antwerp). The presence of test environment URLs (webapps-test.portofantwerpbruges.com/xui) suggests XUI framework usage, which may have known CVEs. The note about 'NEW login page' in test environment indicates recent deployments likely undergoing security assessment. This would have been reported to Intigriti for scope remediation rather than a traditional vulnerability bounty.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
