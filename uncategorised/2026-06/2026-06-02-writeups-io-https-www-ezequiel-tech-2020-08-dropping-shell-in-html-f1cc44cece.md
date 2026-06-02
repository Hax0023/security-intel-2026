# Dropping a Shell in Google Cloud SQL: Privilege Escalation and RCE

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Google Cloud SQL
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** SQL Injection, Parameter Injection, Privilege Escalation, Command Injection, Arbitrary File Write
- **Category:** uncategorised
- **Writeup:** https://www.ezequiel.tech/2020/08/dropping-shell-in.html

## Summary
Two critical vulnerabilities were discovered in Google Cloud SQL's MySQL export functionality that allowed attackers to escalate privileges and achieve remote code execution. Bug 1 involved SQL injection to abuse FILE privileges in custom export queries, while Bug 2 exploited parameter injection in mysqldump to execute arbitrary commands with elevated privileges.

## Attack scenario (step by step)
1. Attacker gains access to a Cloud SQL instance with root@% credentials
2. Attacker identifies the export feature accepts custom SQL queries that internally use mysqldump
3. Attacker performs SQL injection by inserting comment characters to execute SELECT INTO OUTFILE with FILE privileges
4. Attacker writes malicious files to /mysql/tmp (secure_file_priv directory) with SQL injection
5. Attacker modifies API export parameters to inject mysqldump flags like --help or other command-line options
6. Attacker chains parameter injection with file write to execute arbitrary commands, achieving RCE

## Root cause
Google Cloud SQL's export API failed to properly sanitize user inputs when constructing mysqldump commands and allowed custom SQL queries without validating dangerous file operations. The backend service directly passed user-controlled database names and query parameters to system commands without proper escaping or validation.

## Attacker mindset
An attacker with legitimate database access would recognize the export feature as a potential vector, test error messages to understand backend behavior, and systematically escalate from SQL injection to parameter injection. The attacker would recognize that FILE privileges combined with command-line tool parameter injection could enable full system compromise.

## Defensive takeaways
- Implement strict input validation and parameterized commands for all user-supplied inputs passed to system utilities
- Never construct command-line arguments by string concatenation; use safe APIs with argument arrays
- Sanitize and whitelist database names and parameters before passing to mysqldump
- Restrict or disable FILE privilege even for administrative accounts in managed database services
- Implement rate limiting and logging for export/import operations to detect abuse
- Use principle of least privilege: invoke mysqldump with minimal necessary permissions, not as root
- Employ command sandboxing or containerization to limit blast radius of parameter injection attacks
- Regular security audits of API endpoints that invoke external tools

## Variant hunting
['Test other database management APIs (import, backup, restore) for similar parameter injection', 'Check if other Cloud SQL database engines (PostgreSQL) have analogous vulnerabilities in pg_dump', 'Investigate whether user-defined functions or stored procedures can bypass secure_file_priv restrictions', 'Test for SQL injection in other custom query fields (monitoring, data validation, migration tools)', 'Examine if other GCP managed services invoking system tools have similar parameter injection issues', 'Check if symbolic links in /mysql/tmp can bypass file write restrictions', 'Test race conditions between file creation and storage bucket export for privilege escalation']

## MITRE ATT&CK
- T1190
- T1548
- T1059
- T1083
- T1021
- T1040

## Notes
Researchers responsibly disclosed to Google who patched quickly. This represents a severe failure in secure API design where a managed service provider exposed dangerous OS command injection through insufficiently validated user inputs. The chaining of SQL injection + parameter injection demonstrates why defense-in-depth is critical for database services.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
