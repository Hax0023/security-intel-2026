# Chaining Three Bugs to Access All Your ServiceNow Data

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** ServiceNow
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Authorization Bypass, Access Control Bypass, Privilege Escalation, Database Access Control Weakness
- **Category:** memory-binary
- **Writeup:** https://www.assetnote.io/resources/research/chaining-three-bugs-to-access-all-your-servicenow-data

## Summary
Researchers discovered a chain of three vulnerabilities (CVE-2024-4879, CVE-2024-5178, CVE-2024-5217) in ServiceNow that allows unauthenticated attackers to gain full database access and command execution on MID servers. The vulnerabilities exploit ServiceNow's dynamic routing system based on database configuration and access control mechanisms.

## Attack scenario (step by step)
1. Attacker identifies an externally accessible ServiceNow instance through reconnaissance
2. First vulnerability exploited to bypass initial authentication or access controls on the routing system
3. Second vulnerability leveraged to bypass table-level ACLs or processor-level authorization checks
4. Third vulnerability chained to achieve administrative access on the ServiceNow instance
5. With admin access, attacker queries database tables containing sensitive data (HR records, employee information, credentials)
6. Attacker uses admin privileges to execute commands on configured MID servers within the internal network, establishing persistence

## Root cause
ServiceNow's dynamic routing architecture relies on database-stored configuration to determine request handling. The ACL system protecting tables and processors has gaps that can be chained together: the routing mechanism does not properly validate authentication state before consulting database configuration, and the ACL enforcement on tables and processors contains bypass conditions that can be exploited sequentially to escalate privileges from unauthenticated to administrator.

## Attacker mindset
Target cloud SaaS platforms with broad external accessibility and internal network connectivity. Look for custom permission systems layered on dynamic routing. Chain multiple minor bypass conditions to reach admin level, then pivot to internal infrastructure via legitimate admin features like MID servers.

## Defensive takeaways
- Implement authentication gating before any routing decisions are made, regardless of database configuration
- Enforce ACLs at multiple layers (routing, table access, field access) with explicit deny defaults
- Require strong authentication for all processor endpoints, not just table views
- Restrict MID server administrative capabilities and require separate authentication channels
- Implement request signing and validation to prevent tampering with routing parameters
- Regular security audits of dynamic routing systems that depend on database configuration
- Monitor and alert on database modifications to security-relevant tables (ACLs, routing rules)
- Apply principle of least privilege to developer and test instances (don't expose them externally)

## Variant hunting
Search for other applications using dynamic routing based on database configuration (Salesforce, Microsoft Dynamics, Jira, Confluence). Look for ACL bypass chains in systems where multiple authorization layers can be individually bypassed but become exploitable in combination. Examine proxy/agent systems (MID servers, connectors, integrations) that grant elevated privileges to authenticated admins.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1548 - Abuse Elevation Control Mechanism
- T1087 - Account Discovery
- T1010 - Application Window Discovery
- T1565 - Data Manipulation
- T1133 - External Remote Services

## Notes
The vulnerability chain demonstrates the danger of layered custom security controls without unified enforcement. ServiceNow's appeal as a target stems from: (1) external accessibility, (2) sensitive data storage, (3) internal network connectivity via MID servers, and (4) admin access implying RCE. The researchers responsibly disclosed to ServiceNow who responded rapidly. This research highlights the importance of threat modeling privilege escalation chains rather than analyzing vulnerabilities in isolation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
