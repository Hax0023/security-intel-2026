# Chaining Three Bugs to Access All Your ServiceNow Data

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** ServiceNow
- **Bounty:** Not disclosed
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Database Access Control Bypass, ACL Bypass, Privilege Escalation, Arbitrary Data Access
- **Category:** memory-binary
- **Writeup:** https://www.assetnote.io/resources/research/chaining-three-bugs-to-access-all-your-servicenow-data

## Summary
A chain of three vulnerabilities (CVE-2024-4879, CVE-2024-5178, CVE-2024-5217) in ServiceNow allows attackers to bypass authentication and gain full database access plus unauthorized control of MID servers. The attack exploits routing mechanisms, ACL enforcement gaps, and processor security flaws in ServiceNow's architecture.

## Attack scenario (step by step)
1. Attacker identifies ServiceNow instance externally accessible via cloud deployment
2. Exploits first vulnerability (CVE-2024-4879) to bypass initial authentication controls or access restricted endpoints
3. Leverages second vulnerability (CVE-2024-5178) to circumvent ACL system that protects sensitive tables and data
4. Chains third vulnerability (CVE-2024-5217) to gain elevated privileges or access to processor configurations
5. Obtains full database access including sys_users, employee records, and sensitive configuration data
6. Escalates to MID Server compromise through authenticated admin access, enabling remote command execution on internal network infrastructure

## Root cause
ServiceNow's database-driven routing mechanism and JavaScript-based processor system lack sufficient authentication and authorization validation at critical control points. The ACL system has enforcement gaps when handling table access and processor execution. The architecture allows authenticated users to manipulate routing/processor logic to access resources beyond their privilege level.

## Attacker mindset
Opportunistic yet methodical researcher discovering that cloud-hosted business platforms with network integrations (MID servers) represent high-value targets. Focused on understanding application architecture deeply before exploitation, recognizing that chaining multiple small bypasses compounds impact exponentially. Prioritized comprehensive access over single vulnerability exploitation.

## Defensive takeaways
- Implement defense-in-depth authorization checks at every database access point, not just ACL layer
- Validate authentication state and authorization for all processor executions, especially those returning sensitive data
- Restrict or eliminate database-driven routing for security-critical endpoints; use hardcoded mappings instead
- Apply principle of least privilege strictly to JavaScript engine capabilities and available helper classes
- Implement consistent input validation and sanitization in URL routing resolution
- Add comprehensive audit logging for database access, especially to sensitive tables like sys_users and configuration tables
- Segment MID server access with additional authentication layers beyond ServiceNow instance admin credentials
- Conduct security reviews of all custom processors and table access configurations regularly
- Implement rate limiting and anomaly detection for unusual database access patterns

## Variant hunting
['Examine other JavaScript-based processor endpoints for similar authorization bypass patterns', 'Test ACL enforcement across all table types, especially recently added custom tables', 'Probe for additional database-driven routing decision points that may lack validation', 'Review processor helper classes for unintended information disclosure or privilege escalation methods', 'Test for authorization bypass in table creation/modification endpoints (.do handlers)', 'Investigate MID server authentication mechanisms for additional authentication bypass vectors', 'Search for other Rhino JavaScript engine contexts with insufficient sandboxing', 'Examine shared tenancy isolation mechanisms for cross-instance data leakage']

## MITRE ATT&CK
- T1190
- T1199
- T1566
- T1078
- T1087
- T1087.004
- T1526
- T1552
- T1552.007
- T1056
- T1005
- T1021
- T1210

## Notes
This represents a sophisticated supply-chain risk as ServiceNow instances typically contain highly sensitive employee data, HR records, and configuration. The MID server component creates particular danger as it bridges cloud and internal networks. The research demonstrates the importance of understanding architectural decisions (database-driven routing) as they create systemic security implications. Researchers received early access mitigation and noted ServiceNow's responsive security team. The 3-4 week discovery timeline suggests these were subtle vulnerabilities requiring deep architectural understanding rather than obvious flaws.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
