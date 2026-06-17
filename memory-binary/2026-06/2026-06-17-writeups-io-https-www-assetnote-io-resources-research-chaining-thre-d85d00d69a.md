# Chaining Three Bugs to Access All ServiceNow Data

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** ServiceNow
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Authorization Bypass, Access Control Bypass, Privilege Escalation
- **Category:** memory-binary
- **Writeup:** https://www.assetnote.io/resources/research/chaining-three-bugs-to-access-all-your-servicenow-data

## Summary
A chain of three vulnerabilities (CVE-2024-4879, CVE-2024-5178, CVE-2024-5217) allows unauthenticated attackers to gain full database access and command execution on MID servers in ServiceNow instances. The attack exploits routing mechanisms, ACL bypasses, and processor vulnerabilities to escalate from anonymous access to administrative control.

## Attack scenario (step by step)
1. Attacker discovers ServiceNow instance is externally accessible via cloud hosting
2. Attacker exploits first vulnerability (CVE-2024-4879) to bypass authentication/routing controls
3. Attacker leverages second vulnerability (CVE-2024-5178) to bypass ACL restrictions on sensitive tables
4. Attacker chains third vulnerability (CVE-2024-5217) to gain admin-level access to database records
5. Attacker obtains database credentials and accesses all sensitive data (HR records, employee data)
6. Attacker leverages admin access to execute commands on internal MID servers within corporate network

## Root cause
ServiceNow's database-driven routing architecture combined with insufficient validation of database access requests. The platform consults database tables for routing decisions rather than hardcoded endpoints, creating multiple bypass opportunities. ACL system implementation has gaps when routing through processors, and authentication checks are not consistently enforced across all code paths.

## Attacker mindset
Reconnaissance-focused researcher identifying that ServiceNow is widely deployed in cloud with sensitive data and internal network access. Systematically analyzed the architecture, specifically the routing mechanism and request handling flow. Chained multiple moderate vulnerabilities into a critical impact scenario, understanding that administrative access translates to command execution on privileged MID servers.

## Defensive takeaways
- Implement whitelist-based routing instead of database-driven dynamic routing for security-critical paths
- Enforce authentication and authorization checks at every request entry point before routing decisions
- Apply principle of least privilege strictly - avoid admin-level database modification endpoints for normal users
- Add integrity checks and signature verification for processor code and table access rules
- Implement consistent ACL enforcement across all code paths (tables, processors, APIs)
- Require multi-factor authentication for administrative actions, especially those affecting MID servers
- Audit and restrict MID server connectivity capabilities based on principle of least privilege
- Implement request validation at routing layer to prevent path traversal and parameter manipulation

## Variant hunting
['Look for similar database-driven routing in other enterprise platforms (Salesforce, Oracle NetSuite, Workday)', 'Test for ACL bypass in other processor types or custom code execution endpoints', 'Investigate authentication decorators and their consistent application across all request handlers', 'Search for parameter pollution techniques in routing parameters that could bypass authentication', 'Test for privilege escalation through role assignment in database tables', 'Examine MID server communication protocols for authentication weaknesses', 'Look for default credentials or shared secrets in processor code or configuration tables']

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1078
- T1134
- T1087
- T1021
- T1570

## Notes
The writeup emphasizes ServiceNow's unique architecture where most routing and configuration is database-driven rather than hardcoded. This design choice, while providing flexibility, creates security challenges when ACL implementation is inconsistent. The research demonstrates the importance of architectural security reviews in configurable platforms. ServiceNow's rapid response and communication was noted positively. The shared tenancy free developer instances made testing feasible. The attack chain highlights how moderate vulnerabilities compound into critical impact when chained - each individual bug may have been caught by surface-level security review, but the combination requires deeper architectural understanding.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
