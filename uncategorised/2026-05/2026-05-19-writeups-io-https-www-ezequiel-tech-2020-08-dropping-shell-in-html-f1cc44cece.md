# Dropping a Shell in Google Cloud SQL: SQL Injection and Parameter Injection Leading to RCE

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Google Cloud SQL
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Command/Parameter Injection, Privilege Escalation, Remote Code Execution
- **Category:** uncategorised
- **Writeup:** https://www.ezequiel.tech/2020/08/dropping-shell-in.html

## Summary
Researchers discovered multiple vulnerabilities in Google Cloud SQL's MySQL implementation (5.6 and 5.7) that allowed unauthenticated attackers to escalate privileges and achieve remote code execution. By exploiting SQL injection in the export feature combined with parameter injection in mysqldump, attackers could execute arbitrary commands with elevated privileges on the managed database service.

## Attack scenario (step by step)
1. Attacker identifies the Cloud SQL web interface export feature accepts custom SQL queries without proper sanitization
2. Attacker crafts malicious SQL query with comment injection (e.g., 'SELECT * FROM database INTO /mysql/tmp/evilfile #') to obtain FILE privileges
3. Attacker intercepts the export API call and modifies the database parameter with mysqldump command-line options (e.g., '--help' or other flags)
4. Attacker discovers mysqldump processes untrusted input, allowing arbitrary option injection and command execution
5. Attacker chains exploits to write malicious files or execute system commands with the privileges of the mysqld process
6. Attacker gains shell access to the Cloud SQL infrastructure and potentially accesses customer data or other instances

## Root cause
Two independent vulnerabilities: (1) Insufficient input validation on custom SQL queries in the export feature allowing SQL injection with FILE privileges, and (2) Unsanitized parameter passing to mysqldump binary enabling command-line option injection that bypasses secure argument handling.

## Attacker mindset
Reconnaissance-focused researcher exploiting managed service limitations by testing error conditions and API parameters. Recognized that combining two separate bugs could escalate from limited FILE write access to full command execution. Tested boundary conditions (typos, comments, parameter manipulation) methodically.

## Defensive takeaways
- Never pass user-supplied input directly to command-line tools; use parameterized/array-based argument passing instead of string concatenation
- Implement strict whitelist validation for SQL query exports; disallow dynamic query construction or use prepared statements
- Sanitize and validate all API parameters before passing to subprocesses; explicitly define allowed characters and options
- Apply principle of least privilege: restrict FILE privileges and secure_file_priv directories; don't grant excessive permissions to service accounts
- Implement query logging and anomaly detection for suspicious patterns (INTO OUTFILE, comment injection attempts)
- Use containerization/isolation to limit blast radius if mysqldump process is compromised
- Add rate limiting and authentication checks on export/import operations
- Regularly audit third-party tool invocations for injection vulnerabilities

## Variant hunting
['Check other Google Cloud managed database services (Cloud Firestore, BigQuery, Spanner) for similar export/import parameter injection', "Test other managed database providers' export features (AWS RDS, Azure Database, Heroku Postgres) for SQL injection in custom query exports", 'Search for mysqldump parameter injection in other contexts where user input influences command-line arguments', 'Investigate if other binary tools (pg_dump, mongodump) are similarly vulnerable to option injection in export workflows', 'Test whether other Cloud SQL features (backups, replication, monitoring) accept unsanitized input', 'Check if comment characters work in other database contexts beyond MySQL']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1059 - Command and Scripting Interpreter
- T1070 - Indicator Removal
- T1083 - File and Directory Discovery
- T1005 - Data from Local System
- T1021 - Remote Service Session Initiation

## Notes
Vulnerabilities were responsibly disclosed and patched by Google. The writeup demonstrates excellent attack methodology by chaining two separate weaknesses (SQL injection + parameter injection) to achieve a critical outcome. The researchers properly identified that secure_file_priv restrictions alone were insufficient when combined with command injection in export utilities. This case highlights the risks of managed services invoking system tools with user-controlled parameters.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
