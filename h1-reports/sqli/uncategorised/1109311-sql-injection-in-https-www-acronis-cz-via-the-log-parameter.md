# SQL Injection in POST 'log' Parameter on Acronis.cz

## Metadata
- **Source:** HackerOne
- **Report:** 1109311 | https://hackerone.com/reports/1109311
- **Submitted:** 2021-02-23
- **Reporter:** mmg
- **Program:** Acronis (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** SQL Injection, CWE-89
- **CVEs:** None
- **Category:** uncategorised

## Summary
A SQL injection vulnerability was discovered in the POST parameter 'log' on https://www.acronis.cz/, allowing an attacker to execute arbitrary SQL queries. The vulnerability was confirmed using sqlmap, which successfully retrieved the database user 'u_acronis@localhost'. This could enable complete database compromise, authentication bypass, and potential OS command execution.

## Attack scenario
1. Attacker identifies the POST parameter 'log' on the Acronis.cz website
2. Attacker crafts a malicious SQL payload designed to break out of the intended query context
3. Attacker uses sqlmap or manual payloads to confirm SQL injection with level=2 and risk=2 settings
4. Attacker queries database metadata to identify current user and database structure
5. Attacker escalates privilege to extract sensitive data or execute OS commands via database functions
6. Attacker gains unauthorized access to customer data or system control depending on database permissions

## Root cause
The application fails to properly sanitize or parameterize the 'log' POST parameter before incorporating it into SQL queries, allowing attacker-controlled input to be interpreted as SQL code rather than data.

## Attacker mindset
An opportunistic reconnaissance-focused attacker who identified a common web application parameter name ('log') and tested it for injection flaws. The use of automated tools (sqlmap) suggests efficiency over sophisticated exploitation, indicating the vulnerability may be easily discoverable by other attackers.

## Defensive takeaways
- Implement parameterized queries/prepared statements for all database interactions
- Apply input validation and whitelisting for the 'log' parameter
- Use ORM frameworks that enforce parameterized queries by default
- Apply principle of least privilege to database user accounts (u_acronis account should have minimal permissions)
- Implement Web Application Firewall (WAF) rules to detect and block SQL injection patterns
- Conduct security code review focusing on all user-supplied input handling
- Implement comprehensive logging and monitoring to detect SQL injection attempts
- Perform regular penetration testing and vulnerability scanning with tools like sqlmap

## Variant hunting
Search for other parameter names commonly associated with logging functionality (request_log, log_id, logs, logging, trace, debug) that may share the same vulnerable code patterns. Test other POST/GET parameters for similar injection flaws, particularly those processing user input without sanitization.

## MITRE ATT&CK
- T1190
- T1059
- T1078
- T1530

## Notes
The researcher demonstrated responsible disclosure by limiting testing to user enumeration and not performing destructive actions. The vulnerability appears relatively straightforward to exploit given the successful use of standard sqlmap parameters. The presence of a 'log' parameter suggests this may be a legitimate logging/debugging feature improperly exposed or inadequately secured in production.

## Full report
<details><summary>Expand</summary>

I have discovered a SQL injection in https://www.acronis.cz/ using the POST request via the log parameter.
Using sqlmap, I have retrieved the current user: 'u_acronis@localhost''

The command used:
sqlmap  -p log -r request-cz.txt --current-user  --level=2 --risk=2

I did not perform any other actions.

## Impact

An attacker can use SQL injection it to bypass a web application's authentication and authorization mechanisms and retrieve the contents of an entire database.
This can also be used by an attacker to execute OS commands, which may then be used to escalate an attack even further.

</details>

---
*Analysed by Claude on 2026-05-11*
