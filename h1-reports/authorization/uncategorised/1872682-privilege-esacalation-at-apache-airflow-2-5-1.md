# Privilege Escalation via Insecure Log File Permissions in Apache Airflow 2.5.1

## Metadata
- **Source:** HackerOne
- **Report:** 1872682 | https://hackerone.com/reports/1872682
- **Submitted:** 2023-05-08
- **Reporter:** ksw9722
- **Program:** Apache Airflow
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure File Permissions, Privilege Escalation, Symlink Attack, Information Disclosure
- **CVEs:** CVE-2023-25754
- **Category:** uncategorised

## Summary
Apache Airflow 2.5.1 creates log files with world-readable and world-writable permissions (chmod 666), allowing any local Linux user to read sensitive information and perform symlink attacks. An attacker with local access can delete log files and replace them with symlinks to read arbitrary files owned by the airflow process, such as SSH private keys.

## Attack scenario
1. Attacker gains local shell access to the host running Airflow with a non-privileged Linux account
2. Attacker identifies Airflow log file locations and removes a target DAG log file
3. Attacker creates a symbolic link in place of the deleted log pointing to a sensitive file (e.g., SSH private key of the airflow user)
4. Attacker authenticates to the Airflow web UI and navigates to view the DAG logs
5. Airflow reads the symlink and displays the contents of the target file (SSH private key) in the web UI
6. Attacker exfiltrates the SSH private key or other sensitive data, achieving privilege escalation to the airflow account

## Root cause
Airflow creates log files with overly permissive default permissions (666) without proper file permission controls, and fails to validate that log file paths are not symlinks before reading/writing to them. This allows TOCTOU (Time-Of-Check-Time-Of-Use) and symlink attack vulnerabilities.

## Attacker mindset
An attacker with local shell access seeks to escalate privileges by accessing credentials or sensitive data owned by the airflow service account. By exploiting insecure log permissions and symlink handling, they can trick the Airflow process into exposing sensitive files through the web interface without requiring direct access to the airflow account.

## Defensive takeaways
- Set restrictive file permissions on log files (e.g., chmod 600) - readable/writable only by the owning process
- Implement proper file permission validation during log file creation and before reading log contents
- Use secure temporary file creation functions that are resistant to symlink attacks (e.g., O_NOFOLLOW flag)
- Validate that log file paths are not symlinks before serving them via the web UI
- Run Airflow services with minimal required privileges (principle of least privilege)
- Regularly audit file permissions on log directories and files in production environments
- Implement access controls on log access through the web UI to prevent unauthorized reads

## Variant hunting
Check for similar insecure default permissions on other temporary or cache files created by Airflow
Review other Apache projects (Kafka, Spark, etc.) for identical log permission vulnerabilities
Audit symlink handling in other file read operations throughout the Airflow codebase
Investigate if PID files or configuration files have similar permission issues
Search for other instances where user-controlled paths might lead to symlink attacks in log handling

## MITRE ATT&CK
- T1190
- T1548
- T1548.004
- T1552.001
- T1083
- T1566.002

## Notes
CVE-2023-25754 was assigned by Apache Security Team. The vulnerability is a classic symlink attack combined with insecure file permissions. The patch (PR #29506) likely addresses this by implementing secure file creation with restrictive permissions and symlink validation. This is a good example of why temporary files and logs require special attention in security design.

## Full report
<details><summary>Expand</summary>

Hello. I found security issue about airflow's log file. 

Airflow 2.5.1 sets log files to vulnerable privileges.  (chmod 666)

Any Linux user on the host on which the airflow operates can read and tamper with the airflow's logs.

Taking advantage of this, an attacker in local host can retrieve sensitive information from a Linux host that can only access airflow accounts.  ** (This is privilege escaltion from any linux account to airflow's linux account) **
(ex : ssh private key)

** The attack conditions are as follows. **
1. An attacker can log in to a host running airflow with a specific Linux account.
(Or the penetration test was successfully successful.)

2. An attacker can log in to the airflow web server and can read the dag log.

** The attack procedure is as follows.  **

1. After deleting a specific dag log using any account, the attacker regenerates the log file using the ssh private key of the account that runs the airflow as a symbolic link.
{F2171182}

2. The attacker logs in to the airflow webserver and reads the log.
{F2171186}


3. The airflow logs expose SSH PRIVATE KEY.

{F2171190}



## Patch History 
- https://github.com/apache/airflow/pull/29506
- This vulnerability has been allocated CVE-2023-25754 by Apache Security Team.

## Impact

Local linux user can access any file like ssh private key which owned by account which operate airflow.

</details>

---
*Analysed by Claude on 2026-05-24*
