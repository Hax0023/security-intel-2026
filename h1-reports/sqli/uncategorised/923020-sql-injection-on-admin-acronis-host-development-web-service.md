# SQL Injection in Admin API Search Parameter (admin.acronis.host)

## Metadata
- **Source:** HackerOne
- **Report:** 923020 | https://hackerone.com/reports/923020
- **Submitted:** 2020-07-14
- **Reporter:** stealthy
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** SQL Injection, Authentication Bypass (separate report), Improper Input Validation, Inadequate API Security
- **CVEs:** None
- **Category:** uncategorised

## Summary
A SQL injection vulnerability was discovered in the search parameter of the admin API endpoint (/api/admin/pages) on the development admin panel for Acronis. The vulnerability allows authenticated attackers with admin panel access to query the backend database directly, potentially exposing sensitive user data including credentials and password reset tokens. The attacker demonstrated successful enumeration of three databases and 24 tables including users, password_resets, and other sensitive information.

## Attack scenario
1. Attacker gains unauthorized access to the admin panel at https://admin.acronis.host (via separate vulnerability)
2. Attacker navigates to the Pages section and attempts to search for content, intercepting the HTTP request
3. Attacker identifies that the 'search' parameter in the GET request to /api/admin/pages is unsanitized and vulnerable to SQL injection
4. Attacker crafts malicious SQL payloads in the search parameter and uses SQLMap to automate exploitation with flags like --dbs and --tables
5. Attacker successfully enumerates three accessible databases and 24 tables containing sensitive data (users, password_resets, etc.)
6. Attacker could escalate by dumping user credentials, password reset tokens, or executing stacked queries for remote code execution

## Root cause
The search parameter in the /api/admin/pages API endpoint fails to implement proper input validation or parameterized queries. User-supplied search input is directly concatenated into SQL queries without sanitization or prepared statement usage, allowing attackers to inject arbitrary SQL syntax.

## Attacker mindset
The attacker demonstrated responsible disclosure practices by: (1) testing a non-sensitive quote character first to confirm vulnerability, (2) only exploring non-sensitive data in the databases, (3) ceasing exploitation immediately after confirming the vulnerability, and (4) reporting directly to the vendor. This indicates a security researcher mindset focused on impact assessment rather than malicious data exfiltration.

## Defensive takeaways
- Implement parameterized queries (prepared statements) for all database interactions to prevent SQL injection
- Apply strict input validation and whitelisting on all search/filter parameters - only allow expected characters and patterns
- Use ORM frameworks that automatically escape queries rather than raw SQL strings
- Implement API rate limiting and query complexity limits to restrict automated exploitation tools like SQLMap
- Enforce principle of least privilege - database service account should have minimal necessary permissions (e.g., SELECT-only for search operations)
- Add Web Application Firewall (WAF) rules to detect and block common SQL injection patterns
- Implement comprehensive logging and alerting for unusual database query patterns or multiple failed authentication attempts
- Conduct regular security audits and penetration testing on development/staging admin panels before production deployment
- Isolate development infrastructure (admin.acronis.host vs prod) with separate credentials and strict access controls

## Variant hunting
Test other API parameters (filter, sort, limit, page) for similar SQL injection vulnerabilities
Check other admin API endpoints (/api/admin/*) for injection flaws in search/filtering functionality
Investigate if the same vulnerability exists in the main Acronis website API endpoints
Test for time-based or boolean-based blind SQL injection if union-based injection is patched
Check if database error messages reveal schema information for more targeted exploitation
Attempt to exploit SQL injection to write files to the filesystem or execute OS commands (xp_cmdshell, INTO OUTFILE, etc.)
Review password_resets table structure to determine if tokens can be enumerated and used for unauthorized account access
Test if stacked queries are allowed (;DROP TABLE, CREATE USER, etc.) for more severe database manipulation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (SQL injection in web API)
- T1110 - Brute Force (potential escalation after credential theft)
- T1078 - Valid Accounts (leveraged initial admin panel access)
- T1005 - Data from Local System (database enumeration)
- T1213 - Data from Information Repositories (sensitive user/password data in database)

## Notes
This report demonstrates the compound risk of multiple vulnerabilities: the initial unauthorized admin panel access (separate report) combined with SQL injection creates critical impact. The development environment designation is important - this suggests the vulnerability may also exist in production if code is deployed without remediation. The researcher's restraint in only exploring non-sensitive data and immediate disclosure is commendable but does not reduce the severity of the underlying vulnerability. The presence of password_resets and users tables indicates potential for privilege escalation or account takeover if fully exploited. The JWT token visible in the request shows the authorization mechanism in use - if the admin panel compromise was through weak credentials or session handling, the security posture is significantly degraded.

## Full report
<details><summary>Expand</summary>

**Summary:**
I found an Acronis domain and started hunting on it. During my hunting, I found an admin panel and was able to access this panel (separate report inbound). It was easy to gain access to this panel, and I was not sure if it was for testing purposes or a genuine admin panel. I played around with minor settings to see if I could change some content on the main page and ensure that this was a real admin panel. I put a quote in the search bar for indexing dashboard pages and intercepted the request. Then I realized all requests are through the administrator API, which I now have access to and an authorization bearer token. Admin API access, combined with the entire site index in the panel (including all content for all pages), confirmed that I am in a real live admin panel.

Next, I noticed the quote returned a server error in the API. I  tested an SQL injection (along with one other critical bug) and confirmed its presence. I can view three databases, and I dumped the table names for one of the databases to see what type of information it contained. In the database, there are tables named `users`, `password_resets`, and more. Furthermore, the login redirected to the main Acronis website, so I knew this data is quite sensitive. I only explored nonsensitive data. The extent of what I did with the SQL injection is diclosed in this report below.

I understand this domain is not rated critical, but I set it because of the severity of the bug.

**Steps to Reproduce:**
Visit the admin panel for Acronis hosting.

    https://admin.acronis.host/

Login with the given credentials and visit the pages section.

    https://admin.acronis.host/#/pages

Here input any data and intercept the request. Below is a copy of the raw request.

```text
GET /api/admin/pages?page=1&limit=100&sort=%2Btype&filter=%7B%7D&search=* HTTP/1.1
Host: dev.acronis.host
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9kZXYuYWNyb25pcy5ob3N0XC9hcGlcL2F1dGhcL2xvZ2luIiwiaWF0IjoxNTk0Njk1MzgzLCJleHAiOjE1OTQ3MzEzODMsIm5iZiI6MTU5NDY5NTM4MywianRpIjoiSnBkczlKY0x6VHF5QXphOCIsInN1YiI6MSwicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9._K-nn1elXhqx1RNszBeZFwX1dbyCVtv63m_-DGp7UmE
Origin: https://admin.acronis.host
Connection: close
Referer: https://admin.acronis.host/dev.acronis.host/en-US/products/4372

```

The `search` parameter is vulnerable. Save the request I provided as a text file on your desktop and run the following command with SQLMap.
```
sudo python sqlmap.py -r {PATH TO FILE} --level 5 --risk 3 --random-agent --dbs
```

This will drop the following three databases.

{F906431}

Next, I used the following flags in SQLMap `-D acronis_site --tables`. The `-D` tells SQLMap which database and `--tables` tells SQLMap to drop table names. I only explored nonsensitive information.
```text
Database: acronis_site
[24 tables]
+----------------------+
| awards               |
| failed_jobs          |
| files                |
| history_pages        |
| locales              |
| migrations           |
| page_products        |
| page_translations    |
| pages                |
| pages_1              |
| pages_2              |
| pages_3              |
| password_resets      |
| product_prices       |
| product_translations |
| products             |
| products_1           |
| related_products     |
| related_tags         |
| resources            |
| tags                 |
| users                |
| variables            |
| webinars             |
+----------------------+
```

After seeing this, I ceased testing this SQL injection and reported the vulnerability directly to your team.

## Impact

Server-side SQL injection leading to database access and exposure of sensitive information. Reading this information likely allows an attacker to execute remote code by stealing admin password resets and user information.

</details>

---
*Analysed by Claude on 2026-05-11*
