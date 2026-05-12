# SQL Injection on docs.atavist.com reader_api/stories.php

## Metadata
- **Source:** HackerOne
- **Report:** 1039315 | https://hackerone.com/reports/1039315
- **Submitted:** 2020-11-20
- **Reporter:** lu3ky-13
- **Program:** Atavist (HackerOne)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** SQL Injection, Time-based Blind SQL Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
A time-based blind SQL injection vulnerability was discovered in the search parameter of the stories.php API endpoint on docs.atavist.com. The vulnerable parameter fails to properly sanitize user input before executing SQL queries against the MySQL database, allowing unauthenticated attackers to extract sensitive data.

## Attack scenario
1. Attacker identifies the /reader_api/stories.php endpoint accepts a search parameter
2. Attacker crafts a payload using time-based blind SQL injection: search=0' AND SLEEP(5) AND 'wRIg' LIKE 'wRIg
3. Application concatenates unsanitized user input directly into SQL query without parameterization
4. Database executes malicious SQL with SLEEP(5) command, causing observable time delay in response
5. Attacker uses response timing differences to infer database structure and extract data (e.g., user credentials, organization data)
6. Attacker automates exploitation to systematically dump sensitive information from the database

## Root cause
The application constructs SQL queries by directly concatenating user-supplied input from the search parameter without using prepared statements or parameterized queries. The backend fails to validate, escape, or sanitize the search input before passing it to the MySQL database engine.

## Attacker mindset
An attacker would recognize that API endpoints accepting search/filter parameters are common SQL injection targets. By testing with time-based payloads (SLEEP), they can confirm the vulnerability even without visible error messages. The blind SQL injection approach allows data exfiltration without needing to see query results directly.

## Defensive takeaways
- Always use parameterized queries (prepared statements) for all database operations involving user input
- Implement input validation and whitelisting for query parameters (limit acceptable values, characters, lengths)
- Apply principle of least privilege to database user accounts running application queries
- Use Web Application Firewall (WAF) rules to detect and block SQL injection patterns
- Implement rate limiting on API endpoints to slow down blind SQL injection exploitation
- Enable database query logging and alerting for suspicious queries containing SLEEP, BENCHMARK, or timing functions
- Conduct regular security testing including SAST/DAST to identify SQL injection flaws
- Update Apache and other server software to latest versions (reporter noted Apache 2.2.34, which is outdated)

## Variant hunting
Search for similar vulnerabilities in other API endpoints on docs.atavist.com and atavist.com accepting filter/search parameters (sort, limit, offset, organization_id). Test other user-controllable parameters in GET/POST requests. Look for similar patterns in other PHP applications using direct string concatenation in SQL queries.

## MITRE ATT&CK
- T1190
- T1565
- T1526

## Notes
The reporter referenced a related vulnerability report (1039315), suggesting multiple security issues in the same application. The endpoint is unauthenticated and publicly accessible. Time-based blind SQL injection is slower but reliable when error-based injection isn't possible. The vulnerability affects the API layer, not just the web UI, expanding attack surface.

## Full report
<details><summary>Expand</summary>

hello dear team 

I have found SQL injection on docs.atavist.com
url:http://docs.atavist.com/reader_api/stories.php?limit=10&offset=20&organization_id=88822&search=0&sort=

parameters: injectable search=0

```
Parameter: search (GET)
    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind
    Payload: limit=10&offset=20&organization_id=88822&search=0' AND SLEEP(5) AND 'wRIg' LIKE 'wRIg&sort=
```
```
[20:54:30] [INFO] the back-end DBMS is MySQL
web application technology: Apache 2.2.34
back-end DBMS: MySQL >= 5.0.12
```


Request
-----------

```
GET /reader_api/stories.php?limit=10&offset=20&organization_id=88822&search=0&sort= HTTP/1.1
Host: docs.atavist.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: _fbp=fb.1.1605829485735.1219501220; __stripe_mid=f950034a-6de5-408c-b227-5ef48058f129d296dd; rgisanonymous=true; rguserid=5625868d-bfff-49dc-90ac-0269e5138dc8; rguuid=true
Upgrade-Insecure-Requests: 1


```

F1087069: 43.PNG

the website in scope other report
https://hackerone.com/reports/950881

## Impact

Use parameterized queries when dealing with SQL queries that contains user input. Parameterized queries allows the database to understand which parts of the SQL query should be considered as user input, therefore solving SQL injection.

</details>

---
*Analysed by Claude on 2026-05-11*
