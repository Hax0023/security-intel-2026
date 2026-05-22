# Google Cloud SQL Shell Injection via SQL Injection and Parameter Injection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Google Cloud SQL
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** SQL Injection, Command Injection, Parameter Injection, Privilege Escalation, Insecure API Design
- **Category:** uncategorised
- **Writeup:** https://www.ezequiel.tech/2020/08/dropping-shell-in.html

## Summary
Two chained vulnerabilities in Google Cloud SQL's export functionality allowed attackers to escalate from regular database user to shell code execution. By exploiting SQL injection in custom export queries to gain FILE privileges, combined with parameter injection in the mysqldump invocation, attackers could write malicious files and achieve remote code execution on the managed database instance.

## Attack scenario (step by step)
1. Attacker gains access to Cloud SQL instance as regular 'root'@'%' user via legitimate credentials or application compromise
2. Attacker crafts malicious SQL query in the web console export feature, injecting INTO OUTFILE directive to bypass FILE privilege restrictions using SQL comment characters
3. Attacker intercepts the export API call via Burp Suite and modifies the database parameter from legitimate database name to '--help' or other mysqldump command options
4. Cloud SQL backend executes mysqldump with attacker-controlled parameters, allowing arbitrary command-line flags to be injected
5. Attacker chains these vulnerabilities to write executable files to writable directories or trigger further RCE through mysqldump's advanced options
6. Attacker achieves shell access on the Cloud SQL instance, breaking out of the managed service restrictions

## Root cause
Two independent design flaws: (1) Cloud SQL's export feature constructs SQL queries by concatenating user input without proper parameterization, and (2) the mysqldump invocation passes unsanitized database name parameters directly to the command line without escaping or validation, allowing attackers to inject arbitrary command-line flags.

## Attacker mindset
Methodical reconnaissance of managed service restrictions, identifying that FILE and SUPER privileges were blocked by design. Probed the export functionality to understand how it works, discovered the temporary CSV export mechanism revealed FILE privilege usage, then systematically tested injection points in both SQL and API parameter layers. Focused on chaining multiple weak controls to bypass security boundaries.

## Defensive takeaways
- Always use parameterized queries and prepared statements in database operations, never concatenate user input into SQL
- Sanitize and validate all command-line arguments passed to external tools; use allowlists for database names and parameters
- Implement strict input validation at API boundaries; database names should match a whitelist pattern like ^[a-zA-Z0-9_-]+$
- Apply principle of least privilege: export operations should use a restricted user account without FILE privileges when possible
- Use subprocess execution APIs that prevent shell expansion (e.g., execve with argument arrays vs. shell=True)
- Implement defense-in-depth: even if one injection point exists, secondary controls should catch malicious payloads
- For managed services, restrict what administrative operations are exposed through user-facing APIs
- Monitor and audit export/import operations for suspicious database names or query patterns

## Variant hunting
Hunt for similar patterns in other Cloud database services (Cloud Datastore, Firestore, BigQuery exports). Check for other mysqldump invocations in Cloud SQL for backup operations. Test other export formats (JSON, SQL, Parquet) for similar parameter injection. Examine import functionality for reverse injection attacks. Investigate restore operations and snapshot management for similar command injection vectors. Check for other gcloud CLI integrations that might invoke external tools with unsanitized parameters.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force (potentially, for initial access)
- T1190 - Exploitation of Remote Services
- T1598 - Phishing (for credential harvesting to gain initial database access)
- T1021 - Remote Services (SQL)
- T1059 - Command and Scripting Interpreter
- T1548 - Abuse Elevation Control Mechanism (privilege escalation through SQL)
- T1136 - Create Account (creating backdoor database accounts)
- T1005 - Data from Local System (exfiltrating database contents)

## Notes
This vulnerability demonstrates the danger of managed service abstractions - Google restricted SUPER and FILE privileges by design, but failed to secure the API layer that invokes tools on behalf of users. The researchers demonstrated excellent methodology: reconnaissance of service limitations, systematic probing of user-facing features, traffic interception for API analysis, and chaining of multiple weak controls. The vulnerability was responsibly disclosed and patched quickly by Google. This is a canonical example of how security boundaries can be bypassed through seemingly innocuous features. The writeup is incomplete (appears truncated) but the core vulnerability chain is clearly established.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
