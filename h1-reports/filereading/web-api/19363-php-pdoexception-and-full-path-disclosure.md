# PHP PDOException and Full Path Disclosure via Type Confusion in phraseChange Action

## Metadata
- **Source:** HackerOne
- **Report:** 19363 | https://hackerone.com/reports/19363
- **Submitted:** 2014-07-07
- **Reporter:** supernatural
- **Program:** Localize.im
- **Bounty:** Unknown
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Type Confusion, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
The phraseChange/phraseDelete actions in index.php fail to properly validate input types before passing parameters to PDO::quote(), causing type confusion when arrays are submitted instead of strings. This triggers unhandled PDOExceptions that expose full server file paths and database structure in error messages.

## Attack scenario
1. Attacker identifies the phraseChange or phraseDelete action endpoint
2. Attacker crafts a malicious request with array parameters instead of expected string values
3. Application passes the array to PDO::quote() at Database.php line 30 without type checking
4. PDO::quote() throws a warning due to type mismatch (expects string, received array)
5. Application constructs invalid SQL query and passes to PDO::exec() at line 57
6. Unhandled PDOException is thrown, exposing full file paths and database error details in stack trace

## Root cause
Insufficient input validation and type checking before passing user-supplied parameters to PDO methods. The application does not validate that expected string parameters are actually strings before calling PDO::quote(). Additionally, uncaught exceptions are exposed to users instead of being logged privately.

## Attacker mindset
Reconnaissance-focused attacker seeking to gather sensitive information about application structure, file paths, and database schema through error messages. Information disclosure enables targeted attacks on other vulnerabilities.

## Defensive takeaways
- Implement strict input validation and type checking for all user-supplied parameters before database operations
- Use parameterized queries/prepared statements instead of manual quote() calls to prevent type-related injection issues
- Implement global exception handling to catch PDOExceptions and log them securely without exposing paths to users
- Configure PHP error reporting to never display detailed errors in production (display_errors = Off)
- Sanitize all error messages shown to users; return generic messages while logging detailed errors server-side
- Use allowlisting for acceptable input types and reject unexpected array parameters early
- Implement Web Application Firewall rules to detect and block requests with suspicious parameter types

## Variant hunting
Search for similar patterns where: (1) user input is passed directly to PDO methods without type validation, (2) unhandled database exceptions propagate to user output, (3) other actions in index.php accept flexible parameter types that could cause type confusion, (4) other PDO method calls (prepare, exec, query) receive unvalidated input, (5) custom wrapper methods in Database class lack input validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Gather Victim Identity Information - Information Disclosure
- T1592 - Gather Victim Host Information - via error messages

## Notes
This is a classic information disclosure vulnerability that exposes server architecture details useful for reconnaissance. The actual impact is moderate as it doesn't directly lead to code execution or data theft, but it significantly aids attackers in understanding the target system. The vulnerability demonstrates the importance of fail-secure error handling. The report format suggests early security research documentation style.

## Full report
<details><summary>Expand</summary>

hi
phrasekey , agian!

in phraseChange action if set to array pdo quote show error!
line 755 index.php

Warning: PDO::quote() expects parameter 1 to be string, array given in /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php on line 30

Fatal error: Uncaught exception 'PDOException' with message 'SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1' in /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php:57 Stack trace: #0 /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php(57): PDO->exec('DELETE FROM phr...') #1 /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php(325): Database::delete('DELETE FROM phr...') #2 /srv/data/web/vhosts/www.localize.im/htdocs/index.php(768): Database::phraseDelete(340, Array) #3 {main} thrown in /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php on line 57

</details>

---
*Analysed by Claude on 2026-05-24*
