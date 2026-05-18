# Dropping a Shell in Google Cloud SQL: SQL Injection and Parameter Injection to RCE

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Google Cloud SQL
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Parameter Injection, Privilege Escalation, Remote Code Execution, Insecure API Design
- **Category:** uncategorised
- **Writeup:** https://www.ezequiel.tech/2020/08/dropping-shell-in.html

## Summary
Two critical vulnerabilities in Google Cloud SQL's MySQL export functionality allowed attackers to escalate privileges and achieve remote code execution. By exploiting SQL injection in custom export queries and parameter injection in the mysqldump API call, an attacker could obtain FILE privileges and execute arbitrary commands on the managed database instance.

## Attack scenario (step by step)
1. Attacker creates a malicious database in Cloud SQL with crafted table names
2. Attacker crafts a SQL injection payload in the custom export query field using INTO OUTFILE and SQL comments to bypass syntax validation
3. Cloud SQL executes the injected query with FILE privileges, writing malicious content to /mysql/tmp directory
4. Attacker intercepts the export API call and modifies the database parameter to inject mysqldump command-line options (e.g., '--print-defaults' or '--secure-file-priv')
5. The injected parameters are passed unsanitized to the mysqldump binary, allowing execution of arbitrary mysqldump options
6. Attacker leverages FILE privileges combined with parameter injection to write web shells or execute system commands, achieving RCE

## Root cause
The vulnerability chain stems from two implementation flaws: (1) The export feature passes user-supplied SQL queries directly to MySQL without properly validating or restricting dangerous SQL commands like INTO OUTFILE, and (2) The API endpoint passes database names and other parameters directly to the mysqldump command without proper escaping or validation, allowing command injection. The design assumption that FILE privileges were restricted proved insufficient when combined with these input validation failures.

## Attacker mindset
An attacker would recognize that managed database services restrict dangerous privileges to prevent direct compromise. However, they would look for indirect paths to privilege escalation through API features meant to help users export data. By chaining a SQL injection vulnerability with parameter injection in the export mechanism, they discovered that the internal service account running these exports had FILE privileges that could be abused. The attacker would methodically test each export feature for injection points and leverage error messages that revealed internal paths and implementation details.

## Defensive takeaways
- Implement strict input validation and parameterized queries for all user-supplied SQL, prohibiting dangerous keywords like INTO OUTFILE, LOAD_FILE, and system-related functions
- Never pass user-controlled data directly to command-line utilities; use APIs or properly escaped/quoted parameters with whitelisting
- Apply principle of least privilege to internal service accounts—export utilities should run with minimal necessary permissions, never FILE privileges
- Sanitize and validate all API parameters before passing to external tools; use allowlists rather than blacklists
- Implement error message filtering to prevent disclosure of internal paths, usernames, and system configuration details
- Add comprehensive logging and monitoring for export operations to detect anomalous SQL patterns and parameter values
- Conduct threat modeling on managed service APIs to identify chaining opportunities across multiple features
- Regularly audit command-line tool invocations and their parameter handling in production systems

## Variant hunting
Similar vulnerabilities likely exist in other export/backup features of Cloud SQL (PostgreSQL, SQL Server), cloud database services (Azure SQL Database, AWS RDS), and other managed services that invoke external tools (pg_dump, mongodump, etc.). Look for: (1) Custom query parameters in backup/export endpoints, (2) API parameters passed unsanitized to system utilities, (3) File operations with elevated privileges in data migration features, (4) Error messages revealing internal paths or privilege levels, (5) Command-line tool invocations in automated backup systems

## MITRE ATT&CK
- T1190
- T1059
- T1548
- T1005
- T1020
- T1082
- T1526

## Notes
This writeup represents sophisticated security research identifying a critical vulnerability chain in a major cloud provider's managed service. The researchers responsibly disclosed to Google, who patched quickly. The vulnerability demonstrates that managed services restricting direct privilege escalation can still be compromised through feature APIs if those APIs lack proper input validation. The error message leaking internal paths proved instrumental in understanding the attack surface. This research highlights the importance of security review for user-facing APIs in managed services, particularly those invoking external tools or executing user-supplied commands/queries. The vulnerability affected MySQL 5.6 and 5.7 on Cloud SQL.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
