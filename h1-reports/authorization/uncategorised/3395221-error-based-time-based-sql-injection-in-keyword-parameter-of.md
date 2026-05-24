# Error-Based & Time-Based SQL Injection in 'keyword' Parameter of admin-search.php in Revive Adserver v6.0.0

## Metadata
- **Source:** HackerOne
- **Report:** 3395221 | https://hackerone.com/reports/3395221
- **Submitted:** 2025-10-22
- **Reporter:** kanon4
- **Program:** Revive Adserver v6.0.0
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** SQL Injection, Error-Based SQL Injection, Time-Based Blind SQL Injection, Improper Input Validation, Missing Parameterized Queries
- **CVEs:** CVE-2025-52664
- **Category:** uncategorised

## Summary
A critical SQL Injection vulnerability exists in the admin-search.php file where the 'keyword' GET parameter is passed to multiple database query functions without proper sanitization or parameterization. An authenticated attacker can exploit this vulnerability using both error-based and time-based blind SQL injection techniques to extract sensitive information, modify database contents, or execute arbitrary SQL commands. The vulnerability stems from the use of phpAds_registerGlobalUnslashed() function which registers user input without escaping before it is incorporated into SQL queries.

## Attack scenario
1. Attacker identifies the admin-search.php endpoint and the unprotected 'keyword' parameter by reviewing application source code or through reconnaissance
2. Attacker crafts a malicious SQL payload using EXTRACTVALUE function for error-based injection: keyword=FUZZ') AND EXTRACTVALUE(8429,CONCAT(0x5c,0x716a7a6a71,(SELECT (ELT(8429=8429,1))),0x7178787871))-- Nqvq&compact=t
3. Attacker sends the payload through the keyword parameter to admin-search.php triggering SQL injection in one of the database query functions (getClientByKeyword, getCampaignAndClientByKeyword, etc.)
4. Database error messages leak sensitive information or time-based responses confirm successful injection, allowing attacker to enumerate database structure and contents
5. Attacker uses SQLMap or manual SQL queries to extract database names, table structures, user credentials, and other sensitive data
6. Attacker escalates attack to modify/delete data or potentially execute operating system commands depending on database server configuration and privileges

## Root cause
The application uses phpAds_registerGlobalUnslashed() to register user input variables including the 'keyword' parameter without proper escaping. This unsanitized user-controlled input is then passed directly to multiple database query functions (getClientByKeyword, getCampaignAndClientByKeyword, getBannerByKeyword, getAffiliateByKeyword, getZoneByKeyword) that incorporate it into SQL queries without using parameterized statements or prepared statements. The underlying DAL (Data Access Layer) functions fail to properly sanitize the keyword parameter before SQL query construction.

## Attacker mindset
An authenticated attacker with access to the admin panel would recognize the search functionality as a potential injection point. Upon noticing that user input is directly concatenated into SQL queries without escaping, they would systematically test various SQL injection payloads. The attacker would prioritize database enumeration and credential extraction to further compromise the application and potentially pivot to the underlying server infrastructure.

## Defensive takeaways
- Implement parameterized queries/prepared statements for all database interactions instead of string concatenation
- Use stored procedures with proper parameter binding when possible
- Apply comprehensive input validation with whitelisting approach (validate against known safe patterns) rather than relying on blacklist-based escaping
- Remove or properly secure the phpAds_registerGlobalUnslashed() function - use proper input handling mechanisms
- Implement principle of least privilege for database accounts used by the application
- Use ORM frameworks that enforce parameterized queries by default
- Conduct security code review of all DAL functions to ensure parameterized queries are used
- Implement Web Application Firewall (WAF) rules to detect and block common SQL injection patterns
- Apply output encoding and error suppression to avoid leaking database error details to users
- Perform regular security testing including automated SAST and DAST scanning for SQL injection vulnerabilities
- Implement runtime application self-protection (RASP) to detect SQL injection attempts
- Mandate security training for developers on secure coding practices

## Variant hunting
Hunt for similar patterns across the Revive Adserver codebase: (1) Search for all usages of phpAds_registerGlobalUnslashed() function and audit how those variables are used in database queries; (2) Review all DAL classes (dalClients, dalCampaigns, dalBanners, dalAffiliates, dalZones) for similar keyword parameter handling in other methods beyond the getByKeyword variants; (3) Search for other admin search/filter endpoints that may accept user input parameters without proper parameterization; (4) Audit all database query construction using string concatenation rather than parameterized queries; (5) Check for similar vulnerabilities in other search parameters mentioned in the code (client, campaign, banner, zone, affiliate); (6) Review any custom database abstraction layer for missing parameterization safeguards

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1078
- T1560

## Notes
This vulnerability requires authentication to the admin panel, which limits exposure but still represents critical risk since admin credentials may be compromised. The successful SQLMap confirmation provides strong proof of concept. The vulnerability affects core administrative functionality used for searching clients, campaigns, banners, affiliates, and zones. Video PoC demonstrates practical exploitability. Report references standard SQL injection resources but lacks information about specific bounty amount and vendor response timeline.

## Full report
<details><summary>Expand</summary>

==Cricetinae==

#Summary:

A critical SQL Injection vulnerability has been identified in Revive Adserver's administrative search functionality, specifically in the `admin-search.php` file. The vulnerability exists in the handling of the keyword `GET` parameter, which is passed to multiple database queries without proper sanitization or parameterization.


The vulnerability stems from the use of the phpAds_registerGlobalUnslashed() function to register user input variables, including keyword, without proper escaping:

```php
phpAds_registerGlobalUnslashed('keyword', 'client', 'campaign', 'banner', 'zone', 'affiliate', 'compact');
```

Subsequently, this user-controlled input is passed directly to several database query functions:

```php
$rsClients = $dalClients->getClientByKeyword($keyword, $agencyId);
$rsCampaigns = $dalCampaigns->getCampaignAndClientByKeyword($keyword, $agencyId);
$rsBanners = $dalBanners->getBannerByKeyword($keyword, $agencyId);
$rsAffiliates = $dalAffiliates->getAffiliateByKeyword($keyword, $agencyId);
$rsZones = $dalZones->getZoneByKeyword($keyword, $agencyId);
```

Without examining the implementation of these functions, it's evident they do not properly sanitize the `keyword` parameter before incorporating it into SQL queries, resulting in SQL Injection.

**Technical Analysis**

Testing with SQLMap confirmed two distinct SQL Injection vulnerabilities:

1.Error-based injection using MySQL's EXTRACTVALUE function:

```bash
Payload: keyword=FUZZ') AND EXTRACTVALUE(8429,CONCAT(0x5c,0x716a7a6a71,(SELECT (ELT(8429=8429,1))),0x7178787871))-- Nqvq&compact=t
```

2. Time-based blind injection using MySQL's SLEEP function:

```bash
Payload: keyword=FUZZ') AND (SELECT 3790 FROM (SELECT(SLEEP(5)))yGYJ)-- YFDA&compact=t
```

#Steps To Reproduce:

  1. open `burp suite` And open the built-in browser with it
  1. Go to the following request: `http://localhost/www/admin/admin-search.php?keyword=FUZZ&compact=t`
  1. Capture the request using Burp Suite
  1. Save the request to a text file using `nano testsql.txt`
  1. Run the following command:

```bash
sqlmap -r testsql.txt --dbs
```

  6. ==You will see the database being extracted==

#Supporting Material/References:

**PoC Video**

{F4922045}

https://portswigger.net/web-security/sql-injection
https://owasp.org/www-community/attacks/SQL_Injection
https://www.imperva.com/learn/application-security/sql-injection-sqli/
https://www.cloudflare.com/learning/security/threats/sql-injection/
https://www.acunetix.com/websitesecurity/sql-injection/

## Impact

This vulnerability allows an authenticated attacker to:

- Extract sensitive information from the database
- Modify or delete database contents
- Potentially execute privileged commands on the database server
- Possibly escalate to a more severe attack vector through data exfiltration

The SQLMap test successfully identified the database name and confirmed the ability to execute arbitrary SQL queries through the vulnerable parameter.
Root Cause

The root cause is improper input validation and the absence of prepared statements or parameterized queries. The application directly incorporates user-controlled input into SQL queries without adequate sanitization or escaping mechanisms.

This is a fundamental code flaw in the Revive Adserver source code and not a result of misconfiguration.

</details>

---
*Analysed by Claude on 2026-05-24*
