# SQL Injection on https://soa-accp.glbx.tva.gov/ via /api/ path

## Metadata
- **Source:** HackerOne
- **Report:** 1125752 | https://hackerone.com/reports/1125752
- **Submitted:** 2021-03-15
- **Reporter:** yassinek3ch
- **Program:** U.S. Tennessee Valley Authority (TVA)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** SQL Injection, Union-Based SQL Injection, Time-Based Blind SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
A critical SQL injection vulnerability exists in the /api/river/observed-data/ endpoint on soa-accp.glbx.tva.gov that allows unauthenticated attackers to execute arbitrary SQL queries. The vulnerability is exploitable via both union-based and time-based blind techniques, allowing complete database compromise including extraction of sensitive system information.

## Attack scenario
1. Attacker discovers the vulnerable endpoint at /api/river/observed-data/ accepts unsanitized user input
2. Attacker crafts a union-based SQL injection payload using MySQL-specific comment syntax (/*! */) to bypass potential filters
3. Attacker executes HOST_NAME() function to enumerate database server hostname and confirm exploitation
4. Attacker extracts database version information (SQL Server 2017) revealing system architecture and patch level
5. Attacker alternates to time-based blind SQL injection using WAITFOR DELAY to exfiltrate data when direct output is unavailable
6. Attacker gains ability to read/write sensitive data, escalate privileges, or pivot to underlying infrastructure

## Root cause
User-supplied input from the 'observed-data' parameter is concatenated directly into SQL queries without proper parameterization, input validation, or prepared statements. The application fails to sanitize special characters and SQL keywords, allowing attackers to break out of intended query context.

## Attacker mindset
The attacker methodically tested multiple SQL injection techniques (union-based, time-based) to identify which worked, demonstrating knowledge of SQL syntax variations and database-specific functions. The choice to extract HOST_NAME() and @@version suggests reconnaissance-oriented behavior to gather system intelligence before deeper exploitation.

## Defensive takeaways
- Implement parameterized queries/prepared statements for all database interactions to separate SQL logic from user data
- Apply input validation with strict whitelisting of allowed characters and reject unexpected inputs
- Disable database user permissions to only necessary stored procedures; prevent direct table access
- Implement Web Application Firewall (WAF) rules to detect and block SQL injection patterns
- Conduct security code review of all /api/ endpoints, particularly data retrieval functions
- Enable SQL Server query logging and monitoring to detect suspicious query patterns
- Establish rate limiting on API endpoints to slow brute-force data exfiltration attempts
- Perform regular penetration testing on government-facing applications with focus on API security

## Variant hunting
Search for similar /api/*/observed-data patterns across TVA subdomains; test other API parameters for injection (filters, search fields, identifiers); check for blind SQL injection variants using benchmark() or sleep() functions; look for second-order SQL injection in stored data; enumerate other endpoints accepting user-controlled IDs or parameters

## MITRE ATT&CK
- T1190
- T1005
- T1557

## Notes
This is a critical vulnerability on a U.S. government infrastructure organization (TVA). The MSSQL Server 2017 version identified is several years old with known CVEs. The affected system appears to be an ACCP (Advanced Control Center Platform or similar) for river observation data, suggesting potential impact on critical water management systems. The use of URL encoding (%2f = /, %20 = space) and MySQL-specific comment syntax indicates the attacker was testing bypass techniques. No indication of authentication requirements on the /api/ endpoint suggests unauthenticated remote code execution risk.

## Full report
<details><summary>Expand</summary>

## Summary:
 
i've found this subdomain ```soa-accp.glbx.tva.gov``` also is vulnerable to SQLI through /api/ path

## Steps To Reproduce:

```https://soa-accp.glbx.tva.gov/api/river/observed-data/GVDA1'+%2f*!50000union*%2f+SELECT+HOST_NAME()--+-``` hostname dumped

```https://soa-accp.glbx.tva.gov/api/river/observed-data/GVDA1'+%2f*!50000union*%2f+SELECT+@@version--+-``` 

Microsoft SQL Server 2017 (RTM-CU22-GDR) (KB4583457) - 14.0.3370.1 (X64) \n\tNov  6 2020 18:19:52 \n\tCopyright (C) 2017 Microsoft Corporation\n\tEnterprise Edition (64-bit) on Windows Server 2012 R2 Standard 6.3 <X64> (Build 9600: ) (Hypervisor)\n

also you can retest it through time bassed trick

```time curl -k "https://soa-accp.glbx.tva.gov/api/river/observed-data/-GVDA1'+WAITFOR+DELAY+'0:0:10'--+-"```

{F1230364}

## Impact

An attacker can manipulate the SQL statements that are sent to the MySQL database and inject malicious SQL statements. The attacker is able to change the logic of SQL statements executed against the database.

</details>

---
*Analysed by Claude on 2026-05-24*
