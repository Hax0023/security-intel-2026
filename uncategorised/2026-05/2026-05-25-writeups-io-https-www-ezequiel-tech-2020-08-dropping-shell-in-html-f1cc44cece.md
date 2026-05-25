# Dropping a Shell in Google Cloud SQL: Multi-stage Privilege Escalation via SQL Injection and Parameter Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Google Cloud SQL
- **Bounty:** Not explicitly stated in writeup
- **Severity:** Critical
- **Vuln types:** SQL Injection, Parameter Injection, Command Injection, Privilege Escalation, Unsafe API Parameter Handling
- **Category:** uncategorised
- **Writeup:** https://www.ezequiel.tech/2020/08/dropping-shell-in.html

## Summary
Researchers discovered a chained vulnerability in Google Cloud SQL's export functionality that allowed unauthenticated database users to escalate privileges and achieve remote code execution. By combining SQL injection through the CSV export feature with parameter injection in the mysqldump export function, attackers could write arbitrary files and eventually execute shell commands with database service privileges.

## Attack scenario (step by step)
1. Attacker gains access to a Cloud SQL MySQL instance with root@'%' credentials (publicly available in some misconfigured environments)
2. Attacker discovers the CSV export feature accepts custom SQL queries and tests for injection by submitting malformed SQL
3. Error message reveals the underlying query structure and confirms FILE privileges are available through the export mechanism
4. Attacker intercepts the database export API call and identifies the database name parameter is passed unsanitized to mysqldump
5. Attacker modifies the database parameter to inject mysqldump command-line options (e.g., '--skip-comments', '--execute') to modify dump behavior
6. Attacker chains multiple injections to write a malicious .sql file to a known path, then uses subsequent export operations to execute arbitrary commands

## Root cause
Two distinct design flaws: (1) The CSV export feature executed user-supplied SQL queries with FILE privileges without proper parameterization, allowing direct file write access; (2) The mysqldump wrapper in the API accepted user-controlled database names without proper escaping or validation, passing them directly as command-line arguments, enabling parameter injection attacks.

## Attacker mindset
A sophisticated attacker would recognize that managed database services often restrict privileges (SUPER, FILE) through policy, but may implement features that circumvent these restrictions internally. By examining error messages, intercepting API calls, and understanding how tools like mysqldump parse arguments, the attacker could chain seemingly limited vulnerabilities into a full system compromise. The attacker would exploit the service's own tooling against it.

## Defensive takeaways
- Never expose internal query structure in error messages; sanitize and generalize error responses
- Implement parameterized/prepared statements for all user input, including database names and export parameters
- Escape and validate all user-supplied parameters before passing to external tools or system commands
- Use allowlists for database operations rather than blacklists; only permit specific, safe parameter values
- Run export/import operations with minimal required privileges; avoid using FILE-privileged accounts for user-initiated exports
- Implement strict argument parsing for tool wrappers; use '--' to terminate option parsing or use direct API calls instead of shell invocation
- Log and audit all database export/import operations with parameter inspection
- Sandbox export processes to limit file system access to specific directories
- Implement rate limiting and anomaly detection on database operations

## Variant hunting
Search for similar patterns in: (1) Other managed database services (AWS RDS, Azure Database) - check export/import features for injection points; (2) MySQL-based tools that accept user parameters (phpMyAdmin, Adminer, database management GUIs); (3) Other Google Cloud services that wrap command-line tools (Cloud Dataflow, Dataproc); (4) Any service that generates SQL errors with query structure information; (5) APIs that pass user input to system commands without sanitization

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force
- T1548 - Abuse Elevation Control Mechanism
- T1070 - Indicator Removal
- T1565 - Data Manipulation
- T1020 - Automated Exfiltration
- T1059 - Command and Scripting Interpreter

## Notes
This writeup demonstrates excellent responsible disclosure practices. The researchers properly identified a vulnerability chain that could be weaponized by attackers with database credentials. The vulnerability is particularly severe because: (1) Cloud SQL instances are sometimes exposed to the internet; (2) Default credentials or leaked credentials could provide initial access; (3) The vulnerability chain is reliable and reproducible; (4) It provides full RCE equivalent through the database service account. The research was conducted by Ezequiel Peña and Wouter ter Maat and patched by Google before publication.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
