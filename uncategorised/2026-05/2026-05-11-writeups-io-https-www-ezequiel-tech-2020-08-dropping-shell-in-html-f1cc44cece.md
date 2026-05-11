# Dropping a Shell in Google Cloud SQL - Parameter Injection and FILE Privilege Escalation

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Google Cloud SQL
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** SQL Injection, Parameter Injection, Command Injection, Privilege Escalation, Arbitrary File Write
- **Category:** uncategorised
- **Writeup:** https://www.ezequiel.tech/2020/08/dropping-shell-in.html

## Summary
Researchers discovered critical vulnerabilities in Google Cloud SQL's MySQL 5.6/5.7 implementations allowing attackers to escalate privileges and execute arbitrary commands. By combining SQL injection in custom export queries with parameter injection in mysqldump invocation, attackers could write arbitrary files and ultimately achieve remote code execution on the managed database instance.

## Attack scenario (step by step)
1. Attacker obtains access to Cloud SQL instance with root@% account (legitimate user or via compromised credentials)
2. Attacker crafts malicious SQL query in the CSV export feature, exploiting FILE privilege available to the export process via SQL injection
3. Attacker intercepts the export API call and modifies the database parameter from legitimate database name to malicious mysqldump options (e.g., '--help')
4. Attacker leverages parameter injection to execute arbitrary mysqldump options and write output to writable directories like /mysql/tmp
5. Attacker chains the FILE write capability with mysqldump options to write shell scripts or executable files to predictable locations
6. Attacker achieves remote code execution and system compromise by executing written files or leveraging MySQL's ability to write to startup directories

## Root cause
Two separate vulnerabilities working in tandem: (1) The Cloud SQL export feature passes user-supplied SQL queries directly to mysqldump without sanitization, and the underlying MySQL user executing queries retains FILE privileges despite managed service restrictions; (2) The database name parameter in the export API call is passed unsanitized to the mysqldump command line, allowing option injection that bypasses intended parameter boundaries

## Attacker mindset
An insider or compromised legitimate user recognizing that managed database services often have unintended capability combinations. The attacker systematically probed the export functionality, intentionally triggered errors to reveal backend command construction, and methodically escalated from information disclosure (help output) to arbitrary file write capabilities by chaining two separate injection vulnerabilities.

## Defensive takeaways
- Implement strict privilege separation: Remove FILE and SUPER privileges from user-accessible accounts, even in managed services where they should theoretically be restricted
- Use prepared statements and parameterized queries for all user input, particularly in administrative operations like exports
- Apply strict shell argument validation and use argument vectors instead of command string concatenation when invoking external tools
- Implement allowlists for database names and custom query patterns in export functionality
- Apply principle of least privilege: create dedicated, unprivileged database users for backend administrative operations rather than using root accounts
- Monitor and audit all export/import operations, particularly those with custom queries
- Run mysqldump and other administrative tools with minimally privileged service accounts
- Implement input validation at API boundaries before passing parameters to system commands

## Variant hunting
['Test other Cloud SQL import/export features for similar parameter injection vulnerabilities', 'Investigate whether backup/snapshot operations have similar mysqldump parameter injection opportunities', 'Check if other Cloud databases (Cloud Spanner, Firestore) have comparable managed service escape vectors', 'Review whether SELECT INTO OUTFILE can be chained with other MySQL features for amplified impact', 'Test if other command-line tools invoked by Cloud SQL APIs accept parameter injection (e.g., pg_dump for PostgreSQL)', 'Examine whether the secure_file_priv restrictions can be bypassed through symlinks or race conditions', 'Check for similar patterns in other Google Cloud managed services that invoke external tools']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548.004 - Privilege Escalation: Abuse Elevation Control Mechanism
- T1070.004 - Indicator Removal: File Deletion
- T1059.002 - Command and Scripting Interpreter: AppleScript
- T1083 - File and Directory Discovery
- T1105 - Ingress Tool Transfer
- T1578.001 - Modify Cloud Compute Infrastructure: Create Cloud Instance
- T1091 - Replication Through Removable Media

## Notes
This is a well-executed chained vulnerability attack demonstrating excellent security research methodology. The researchers properly disclosed the vulnerabilities and Google patched them quickly. The attack required legitimate Cloud SQL access, making it a post-authentication escalation vector. The combination of two seemingly minor issues (FILE privilege exposure + parameter injection) created a critical RCE path, illustrating the importance of defense-in-depth and the danger of privilege creep in managed services. The writeup was authored by Ezequiel and Wouter ter Maat and demonstrates responsible disclosure practices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
