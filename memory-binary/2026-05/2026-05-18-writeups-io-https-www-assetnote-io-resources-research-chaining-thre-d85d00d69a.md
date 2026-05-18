# Chaining Three Bugs to Access All Your ServiceNow Data

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** ServiceNow
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Authentication Bypass, Authorization Bypass, Access Control Vulnerability, Privilege Escalation
- **Category:** memory-binary
- **Writeup:** https://www.assetnote.io/resources/research/chaining-three-bugs-to-access-all-your-servicenow-data

## Summary
A chain of three vulnerabilities (CVE-2024-4879, CVE-2024-5178, CVE-2024-5217) in ServiceNow allows attackers to achieve full database access and compromise all configured MID servers. The vulnerabilities exploit ServiceNow's database-driven routing architecture and ACL system to bypass authentication and gain unauthorized access to sensitive data including HR records and internal systems.

## Attack scenario (step by step)
1. Attacker identifies a publicly accessible ServiceNow instance through external reconnaissance
2. Attacker exploits CVE-2024-4879 to bypass initial authentication mechanisms or access protected endpoints
3. Attacker leverages CVE-2024-5178 to escalate privileges or bypass access control lists (ACLs) on sensitive tables
4. Attacker chains CVE-2024-5217 to gain administrator-level access on the ServiceNow instance
5. With administrator access, attacker executes commands on connected MID servers within the internal network
6. Attacker achieves full database compromise and lateral movement into the victim's internal infrastructure

## Root cause
ServiceNow's architecture relies on database-driven request routing and a sophisticated but bypassable ACL system. The vulnerabilities stem from improper validation of permissions when accessing database tables through URL-based table access (e.g., /sys_users_list.do) and insufficient security checks in custom processors. The combination of these three bugs creates a complete authentication and authorization bypass chain.

## Attacker mindset
A sophisticated attacker recognizes that cloud-hosted ServiceNow instances are externally accessible and often contain highly sensitive data (HR records, employee information). Understanding that administrator access leads to MID server compromise, the attacker methodically chains multiple vulnerabilities to escalate from unauthenticated access to full administrative control, maximizing impact by gaining access to both the SaaS platform and internal network resources.

## Defensive takeaways
- Implement robust input validation and permission verification for all database table access endpoints, not relying solely on URL patterns
- Apply principle of least privilege strictly - administrator roles should not automatically grant command execution capabilities on connected infrastructure
- Validate and enforce ACLs at multiple layers (routing, processor execution, database query) rather than a single point
- Implement rate limiting and anomaly detection on authentication attempts and privilege escalation indicators
- Regularly audit custom processors for security flaws, especially those handling authentication or sensitive parameters
- Segment MID servers with network-level controls; don't allow ServiceNow instance compromise to automatically grant internal access
- Maintain strict access controls on shared tenancy cloud instances through tenant isolation verification
- Monitor and log all administrative actions and unusual access patterns to sensitive tables

## Variant hunting
Hunt for similar ACL bypass vulnerabilities in other database-driven routing systems; examine other processor types beyond the sample shown; investigate whether other ServiceNow modules (HR, IT Service Management) have similar table access vulnerabilities; look for race conditions in ACL enforcement; test for parameter pollution in table access endpoints; examine authentication mechanisms in other cloud-hosted ServiceNow instances; investigate whether MID server communication channels have similar bypass opportunities.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1134 - Access Token Manipulation
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts
- T1110 - Brute Force
- T1199 - Trusted Relationship
- T1570 - Lateral Tool Transfer
- T1021 - Remote Services

## Notes
The researchers emphasized ServiceNow's rapid response and excellent cooperation during the disclosure process. The vulnerability affects shared tenancy cloud instances, making it particularly dangerous as developer instances are publicly available. The three CVEs work in concert to create a complete attack chain; individual patches may not be sufficient. The architecture decision to use database-driven routing instead of hardcoded endpoints creates a larger attack surface. MID server integration represents a critical escalation path from SaaS compromise to internal network access.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
