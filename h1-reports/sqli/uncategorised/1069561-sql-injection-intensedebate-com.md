# SQL Injection in importStatus.php - acctid Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1069561 | https://hackerone.com/reports/1069561
- **Submitted:** 2021-01-01
- **Reporter:** lu3ky-13
- **Program:** intensedebate.com
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** SQL Injection, Boolean-based Blind SQL Injection, Time-based Blind SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
A critical SQL injection vulnerability exists in the acctid GET parameter of importStatus.php that allows unauthenticated attackers to extract sensitive database information including database names, tables, and potentially user credentials. The vulnerability is exploitable through both boolean-based blind and time-based blind SQL injection techniques using standard tools like sqlmap.

## Attack scenario
1. Attacker identifies the importStatus.php endpoint accessible at https://www.intensedebate.com/js/importStatus.php with an injectable acctid parameter
2. Attacker uses sqlmap to automatically detect and confirm SQL injection vulnerability with boolean-based blind and time-based blind payloads
3. Attacker enumerates available databases (heartbeat, id_comments, information_schema) to understand the target database structure
4. Attacker extracts sensitive data such as user credentials, account information, and comment data from the id_comments database
5. Attacker modifies or deletes records to manipulate application functionality or escalate to OS command execution
6. Attacker gains unauthorized access to user accounts and systems dependent on the compromised database

## Root cause
User-supplied input from the acctid parameter is not properly sanitized or parameterized before being incorporated into SQL queries. The application likely concatenates user input directly into SQL statements without using prepared statements or input validation, allowing attackers to break out of the intended query context and execute arbitrary SQL commands.

## Attacker mindset
An opportunistic attacker with basic security knowledge can quickly weaponize this vulnerability using automated tools like sqlmap. The attacker recognizes that publicly accessible PHP files with numeric parameters are common injection points and systematically probes for SQL injection before attempting data extraction and privilege escalation.

## Defensive takeaways
- Implement parameterized queries (prepared statements) for all database interactions to prevent SQL injection
- Apply input validation and sanitization to the acctid parameter, enforcing expected data types (numeric) and length restrictions
- Use a Web Application Firewall (WAF) to detect and block common SQL injection patterns and payloads
- Enforce principle of least privilege for database user accounts to limit damage from successful SQL injection
- Implement comprehensive logging and monitoring of database queries to detect suspicious activity
- Conduct regular security audits and penetration testing, particularly on publicly accessible endpoints
- Remove or restrict access to sensitive PHP files like importStatus.php that should not be publicly exposed
- Apply security patches promptly and keep all software dependencies updated

## Variant hunting
Search for similar vulnerabilities in other .php files under /js/ directory with numeric parameters (id, acctid, userid, aid, etc.). Test other endpoints that accept account identifiers or numeric IDs. Review other Intense Debate functionality that processes account data, comments, or import operations for similar injection flaws. Check if other legacy endpoints use deprecated query construction methods.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1083 - File and Directory Discovery
- T1087 - Account Discovery
- T1557 - Man-in-the-Middle
- T1078 - Valid Accounts

## Notes
This is a straightforward, high-impact SQL injection vulnerability in a public-facing application. The writeup demonstrates basic reconnaissance using sqlmap but lacks evidence of actual data extraction or impact confirmation. The reporter appears to be a security researcher following responsible disclosure practices. The vulnerability affects a legitimate commenting system (Intense Debate) used across multiple websites, making it a supply chain risk. The presence of multiple injection types (boolean-based and time-based blind) indicates poor input handling throughout the application codebase.

## Full report
<details><summary>Expand</summary>

hello dear support

I have found SQL Injection on intensedebate.com
parameters injectable ?acctid=1
URL:https://www.intensedebate.com/js/importStatus.php?acctid=1

I'm used sqlmap to injection 
command 
sqlmap --url https://www.intensedebate.com/js/importStatus.php?acctid=1 --dbs
{F1140562}

available databases [3]:
[*] heartbeat
[*] id_comments
[*] information_schema

Parameter: acctid (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: acctid=1 AND 1726=1726

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: acctid=1 AND (SELECT 8327 FROM (SELECT(SLEEP(5)))yrDl)

## Impact

An attacker can use SQL injection it to bypass a web application's authentication and authorization mechanisms and retrieve the contents of an entire database. SQLi can also be used to add, modify and delete records in a database, affecting data integrity. Under the right circumstances, SQLi can also be used by an attacker to execute OS commands, which may then be used to escalate an attack even further.

</details>

---
*Analysed by Claude on 2026-05-11*
