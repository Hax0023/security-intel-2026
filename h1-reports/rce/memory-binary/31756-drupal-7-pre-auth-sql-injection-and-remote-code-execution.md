# Drupal 7 Pre-Auth SQL Injection Leading to Remote Code Execution (CVE-2014-3704)

## Metadata
- **Source:** HackerOne
- **Report:** 31756 | https://hackerone.com/reports/31756
- **Submitted:** 2014-10-17
- **Reporter:** shorst
- **Program:** Drupal Security
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln:** SQL Injection, Remote Code Execution, Authentication Bypass, Prepared Statement Bypass
- **CVEs:** CVE-2014-3704
- **Category:** memory-binary

## Summary
A critical SQL injection vulnerability in Drupal 7 < 7.32 exists in the expandArguments() function used to handle IN statements in prepared queries. By providing array keys with SQL metacharacters instead of integer indices, attackers can break out of prepared statement placeholders and inject arbitrary SQL. This pre-authentication vulnerability allows unauthenticated attackers to execute arbitrary code by manipulating session data.

## Attack scenario
1. Attacker identifies a Drupal installation vulnerable to CVE-2014-3704 (version < 7.32)
2. Attacker crafts a malicious request with SQL injection payload in array keys (e.g., 'test) -- ' => value)
3. The expandArguments function processes the array and generates invalid placeholder names, breaking prepared statement protection
4. Injected SQL comment characters (--) comment out the rest of the query, allowing arbitrary SQL execution
5. Attacker uses INSERT statement to inject malicious serialized PHP objects into the sessions table with admin privileges (uid=1)
6. When the session is unserialized by Drupal, embedded PHP callbacks are triggered, executing arbitrary code with web server privileges

## Root cause
The expandArguments() function in Drupal's database abstraction layer assumes array keys will be numeric indices only. It concatenates the placeholder name with array keys without sanitization: `$key . '_' . $i`. When non-numeric keys containing SQL metacharacters are provided, the resulting placeholder names contain injection points that break the prepared statement escaping mechanism.

## Attacker mindset
This vulnerability is attractive because it requires zero authentication or prior knowledge of the target system. The attacker recognized that Drupal's 'secure' prepared statements had a logical flaw in array expansion. The multi-query capability in PDO allows chaining multiple statements, enabling both data exfiltration and code execution. The attacker understood Drupal's callback mechanism and session serialization to escalate SQL injection to RCE.

## Defensive takeaways
- Never assume user input structure; validate array key types and reject non-numeric keys in database expansion functions
- Sanitize or validate all components used in SQL query construction, including placeholder name generation
- Use parameterized queries correctly; ensure placeholder names are generated from controlled values only, not user input
- Implement strict input validation for database query parameters before reaching expansion functions
- Disable multi-query execution (set PDO to single-statement mode) unless specifically required
- Apply security patches promptly; this vulnerability was fixed in Drupal 7.32
- Use Web Application Firewalls (WAF) to detect SQL injection patterns in common Drupal parameters
- Monitor database for suspicious session modifications or admin account creation

## Variant hunting
Search for similar issues in other frameworks using prepared statements with array expansion: Laravel's query builder, Symfony Doctrine, CodeIgniter, CakePHP. Look for functions that auto-generate placeholder names from user-controlled array indices. Check for similar issues in PostgreSQL-specific Drupal modules. Investigate whether other callback-based ORM systems can be exploited via session injection.

## MITRE ATT&CK
- T1190
- T1027
- T1056
- T1005
- T1020
- T1078

## Notes
This is one of the most critical Drupal vulnerabilities in history with CVSS 9.8. The vulnerability chain from SQL injection to RCE via session manipulation is particularly sophisticated. The writeup demonstrates strong security research by identifying the logical flaw in 'secure' code. CVE-2014-3704 affected millions of Drupal installations and was actively exploited in the wild immediately after disclosure.

## Full report
<details><summary>Expand</summary>

# Motivation
I found a SQL Injection bug in Drupal < 7.32. Which can lead to a code execution. 

You need not have any user or knowledge of the targeted site.

Since Drupal is used as they state by "millions of websites and applications" I thought about applying for this bug bounty.

# The Bug
Drupal uses Prepared Statements to secure the SQL Querys from Injections. To handle IN statements they created a expandArguments function, which uses the Array keys to create names for the placeholders. 

    foreach ($data as $i => $value) {
          [...]
          $new_keys[$key . '_' . $i] = $value;
    }

The function assumes that it is called with an array which has no keys. Example:

    db_query("SELECT * FROM {users} where name IN (:name)", array(':name'=>array('user1','user2')));

Which results in this SQL Statement

    SELECT * from users where name IN (:name_0, :name_1)

with the parameters name_0 = user1 and name_1 = user2.

The Problem occurs, if the array has keys, which are no integers. Example:

    db_query("SELECT * FROM {users} where name IN (:name)", array(':name'=>array('test) -- ' => 'user1','test' => 'user2')));

this results in an exploitable SQL query:

     SELECT * FROM users WHERE name IN (:name_test) -- , :name_test )

with parameters :name_test = user2.

Since Drupal uses PDO, multi-queries are allowed. So this SQL Injection can be used to insert arbitrary data in the database, dump or modify existing data or drop the whole database.

With the possibility to INSERT arbitrary data into the database an attacker can execute any PHP code through a manipulated Session and Drupal features with callbacks.

# Advisory
https://www.sektioneins.de/advisories/advisory-012014-drupal-pre-auth-sql-injection-vulnerability.html

# CVE Information
The Common Vulnerabilities and Exposures project (cve.mitre.org) has assigned the name CVE-2014-3704 to this vulnerability.

# Poc
I included two PoCs. The first creates one request to create a session which has Admin privileges (UserID 1). The second executes code with only one request and destroys the session afterwards to not create a new Database entry. Some parts of the Second PoC were discovered with help of my coworker Stefan Esser.

</details>

---
*Analysed by Claude on 2026-05-12*
