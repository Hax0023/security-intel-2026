# PHP PDOException and Full Path Disclosure via Parameter Type Confusion

## Metadata
- **Source:** HackerOne
- **Report:** 15899 | https://hackerone.com/reports/15899
- **Submitted:** 2014-06-10
- **Reporter:** supernatural
- **Program:** Localize.im
- **Bounty:** Unknown
- **Severity:** Medium
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Type Confusion, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A type confusion vulnerability exists in the phrase management functionality where array parameters are passed to PDO::quote() which expects strings, causing unhandled PDOException errors. The error messages expose the full file system path and internal code structure, allowing attackers to enumerate the application architecture and gain sensitive information about the backend implementation.

## Attack scenario
1. Attacker identifies the phraseChange or phraseMove endpoints that accept phraseKey parameter
2. Attacker crafts a request with phraseKey set to an array instead of string (e.g., phraseChange[phraseKey][11]=test)
3. The application passes the array directly to PDO::quote() without type validation or casting
4. PDO::quote() throws a warning due to type mismatch, followed by a malformed SQL syntax error
5. Unhandled PDOException is thrown with full stack trace and file paths exposed in error output
6. Attacker gains information about file structure, class names, and method flow for further exploitation

## Root cause
Insufficient input validation and type checking before passing user-controlled parameters to database query functions. The application fails to validate that phraseKey is a scalar value before passing it to PDO::quote(), and lacks proper exception handling to prevent stack trace disclosure.

## Attacker mindset
Information gathering and reconnaissance phase - using type confusion to trigger verbose error messages that reveal application internals, file paths, and code structure useful for planning further attacks such as SQL injection or authentication bypass.

## Defensive takeaways
- Implement strict input validation and type checking (whitelist approach) for all parameters before database operations
- Cast or validate scalar inputs explicitly before passing to PDO::quote() or prepared statements
- Implement comprehensive exception handling to catch PDOException and prevent stack trace leakage in error messages
- Configure error reporting to never display detailed errors to end users; log internally only
- Use prepared statements with parameterized queries instead of manual quote() escaping where possible
- Sanitize error messages to remove sensitive information like file paths before returning to client
- Implement input filtering at the framework/controller level to catch type anomalies early

## Variant hunting
Look for similar patterns where user input arrays/objects are passed to functions expecting scalars: PDO methods, string functions (strlen, substr, etc.), or filter functions that don't perform type coercion. Check for other endpoints accepting parameters named with array syntax like param[key][index].

## MITRE ATT&CK
- T1190
- T1592
- T1592.004

## Notes
This is a low-hanging fruit vulnerability combining type confusion with information disclosure. The attacker requires no authentication and can trigger errors with minimal effort. While not directly exploitable for SQL injection due to the type mismatch failing before query execution, the exposed path information significantly aids attackers in planning subsequent attacks. The vulnerability demonstrates inadequate input sanitization at the application controller/action level.

## Full report
<details><summary>Expand</summary>

hi

in phrases on phrasemove or phraseChange action

- parameter phrasekey set to array  like phraseChange[phraseKey][11]:test
pdo quote show error :

Warning: PDO::quote() expects parameter 1 to be string, array given in /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php on line 30

Fatal error: Uncaught exception 'PDOException' with message 'SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1' in /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php:53 Stack trace: #0 /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php(53): PDO->exec('UPDATE phrases ...') #1 /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php(351): Database::update('UPDATE phrases ...') #2 /srv/data/web/vhosts/www.localize.im/htdocs/index.php(789): Database::setPhraseGroup(339, Array, '326') #3 {main} thrown in /srv/data/web/vhosts/www.localize.im/htdocs/classes/Database.php on line 53




</details>

---
*Analysed by Claude on 2026-05-24*
