# SQL Injection in agent-manager API endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 962889 | https://hackerone.com/reports/962889
- **Submitted:** 2020-08-20
- **Reporter:** bourbon
- **Program:** Acronis
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln:** SQL Injection, Improper Input Validation, Inadequate Parameterization
- **CVEs:** None
- **Category:** uncategorised

## Summary
A SQL injection vulnerability was discovered in the agent-manager API v2 endpoint at /api/agent_manager/v2/unit_configurations. The 'unit' parameter accepts unsanitized user input that is concatenated directly into SQL queries, allowing attackers to execute arbitrary SQL commands. This enables attackers to extract sensitive information such as database names, user credentials, and other confidential data from the backend database.

## Attack scenario
1. Attacker identifies the vulnerable endpoint /api/agent_manager/v2/unit_configurations which accepts the 'unit' parameter
2. Attacker crafts a malicious SQL payload using extractvalue() function with UNION-based or error-based injection techniques
3. Attacker injects SQL metacharacters (single quotes, comments) into the 'unit' parameter to break out of the intended SQL query
4. Attacker appends SQL commands to extract sensitive data like database(), user(), or table contents using SELECT statements
5. Database executes the modified SQL query and returns results through error messages or response data
6. Attacker retrieves sensitive information including database credentials, schema information, and confidential data

## Root cause
The application fails to properly sanitize or parameterize the 'unit' query parameter before incorporating it into SQL queries. User-supplied input is concatenated directly into the query string without using prepared statements or parameterized queries, allowing SQL syntax to be injected.

## Attacker mindset
An attacker would recognize this as a straightforward SQL injection opportunity in an API endpoint. They would systematically test parameters for SQL injection, identify that the 'unit' parameter is vulnerable, and escalate from basic injection (AND 1=1) to data extraction using built-in SQL functions. The public nature of the endpoint makes this easily discoverable and exploitable.

## Defensive takeaways
- Always use parameterized queries or prepared statements for all database interactions
- Implement strict input validation and whitelisting for all user-supplied parameters
- Apply principle of least privilege to database accounts used by the application
- Use Web Application Firewalls (WAF) to detect and block common SQL injection patterns
- Conduct regular security code reviews focused on database query construction
- Implement comprehensive logging and monitoring of database queries for anomalous activity
- Perform penetration testing on all API endpoints, especially those accepting dynamic query parameters
- Use ORM frameworks that enforce parameterization by default

## Variant hunting
Look for similar SQL injection patterns in other agent-manager API endpoints, particularly those accepting 'name', 'tenant_id', or other parameters. Search for similar vulnerable endpoints in other Acronis services that construct dynamic SQL queries. Test other query parameters in the unit_configurations endpoint and related endpoints like unit_profiles, agent_configs, and similar management APIs.

## MITRE ATT&CK
- T1190
- T1190-SQL Injection
- T1583.003-Acquire Infrastructure: Virtual Private Server
- T1566.002-Phishing: Spearphishing Link

## Notes
The vulnerability uses error-based SQL injection via extractvalue() function to retrieve database metadata. The payload structure char(126) (tilde character) is used as a separator to make extracted data visible in error messages. This is a high-confidence critical vulnerability affecting a cloud-based management service with access to potentially sensitive tenant data.

## Full report
<details><summary>Expand</summary>

1.https://mc-beta-cloud.acronis.com/api/agent_manager/v2/unit_configurations?name=update-schedule&no_data=false&tenant_id=1590228&unit=atp-agent%27and%2F%2A%2A%2Fextractvalue%281%2Cconcat%28char%28126%29%2C%28select+database%28%29%29%29%29and%27
2.https://mc-beta-cloud.acronis.com/api/agent_manager/v2/unit_configurations?name=update-schedule&no_data=false&tenant_id=1590228&unit=atp-agent%27and%2F%2A%2A%2Fextractvalue%281%2Cconcat%28char%28126%29%2C%28select+user%28%29%29%29%29and%27

## Impact

sql injection

</details>

---
*Analysed by Claude on 2026-05-11*
