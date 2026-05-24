# Admin Password Disclosure via Publicly Accessible Log File

## Metadata
- **Source:** HackerOne
- **Report:** 1121972 | https://hackerone.com/reports/1121972
- **Submitted:** 2021-03-10
- **Reporter:** darkdream
- **Program:** DeviceLock
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Inadequate Logging Controls, Authentication Credential Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
A publicly accessible log file at /log.txt exposed admin credentials in the form of MD5 password hashes along with usernames and authentication attempts. An unauthenticated attacker could access this file and potentially crack the MD5 hash to gain administrative access to the application.

## Attack scenario
1. Attacker discovers /log.txt is publicly accessible without authentication
2. Attacker retrieves log file contents and identifies admin credentials
3. Attacker extracts MD5 hash '2bca2f877b7a727861b59f4a4039d2e9' and username 'admin'
4. Attacker uses online MD5 reverse lookup or rainbow tables to crack the hash
5. Attacker obtains plaintext password and authenticates as admin user
6. Attacker achieves full administrative control over DeviceLock application

## Root cause
Sensitive log files containing authentication credentials were placed in a publicly accessible web directory without access controls. The application logged password hashes in plaintext format alongside usernames, and failed to restrict directory listing or file access via HTTP.

## Attacker mindset
Opportunistic reconnaissance - scanning common paths like /log.txt, /logs/, /debug/ for exposed sensitive information. Attackers often target administrative functions as they provide maximum impact.

## Defensive takeaways
- Never log authentication credentials, password hashes, or sensitive tokens in any log file
- Store logs outside the web root directory
- Implement access controls and authentication for all log files
- Disable directory listing on web servers
- Use security headers to prevent information disclosure
- Implement log rotation and secure retention policies
- Audit application logging to identify sensitive data exposure
- Use hash-only authentication mechanisms without storing plaintext hashes in logs

## Variant hunting
Check for other common log paths: /logs.txt, /debug.log, /error.log, /app.log, /audit.log
Search for backup files: log.txt.bak, .log.swp, log.txt~
Look for compressed logs: /log.tar.gz, /logs.zip
Check /admin/, /api/, /config/ directories for exposed files
Test for information disclosure via error pages and stack traces
Scan for exposed .env files, config files with secrets
Check git repositories exposed via .git directory

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Reconnaissance
- T1087 - Account Discovery
- T1589 - Gather Victim Identity Information
- T1040 - Network Sniffing
- T1110 - Brute Force

## Notes
MD5 is cryptographically broken for password hashing. The hash '2bca2f877b7a727861b59f4a4039d2e9' likely cracks quickly using publicly available tools. This is a simple but critical misconfiguration combining multiple vulnerabilities: exposed files, improper access controls, and sensitive data logging. The severity is amplified due to admin account compromise potential.

## Full report
<details><summary>Expand</summary>

Hi
I have log file disclose admin password  on https://www.devicelock.com/log.txt
u can see md5 password in log file ,
```
2020-03-20 08:12:15 - main - <br>Module: change password (4.1.2)<br>change_password=yes;/forum/forum_auth.php;login=admin;md5=2bca2f877b7a727861b59f4a4039d2e9
```

## Impact

this information (admin password) can lead to admin account takeover

</details>

---
*Analysed by Claude on 2026-05-24*
