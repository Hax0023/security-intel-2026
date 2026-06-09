# SQL Post/Search Injection on bWAPP

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** bWAPP (Buggy Web Application)
- **Bounty:** N/A - Educational/CTF environment
- **Severity:** HIGH
- **Vuln types:** SQL Injection, POST-based SQL Injection, Improper Input Validation
- **Category:** web-api
- **Writeup:** https://medium.com/@crk2500/sql-post-search-injection-on-bwapp-92996fa3ef67

## Summary
A SQL injection vulnerability exists in the Post/Search functionality of bWAPP where user-supplied input from form fields is directly concatenated into SQL queries without proper sanitization or parameterized statements. An attacker can inject arbitrary SQL commands through the search textbox to extract sensitive information such as server operating system details.

## Attack scenario (step by step)
1. Attacker navigates to the SQL Injection (Post/Search) vulnerable endpoint on bWAPP
2. Attacker identifies the search textbox accepts user input without apparent validation
3. Attacker crafts a SQL injection payload combining a legitimate movie name with SQL metacharacters and functions
4. Attacker submits the payload via POST request in the form field
5. Application concatenates the unsanitized payload directly into the SQL query
6. Injected SQL executes on the database, returning sensitive information (OS details, database contents, etc.) reflected in the page response

## Root cause
The application fails to use parameterized queries or prepared statements when processing POST-based search input. Instead, it directly concatenates user input into SQL query strings, allowing attackers to break out of the intended query context and execute arbitrary SQL commands.

## Attacker mindset
An attacker would recognize that form-based POST inputs are often overlooked for injection testing compared to URL parameters. They would systematically test SQL metacharacters in the search field to identify improper input handling, then escalate to information disclosure attacks to enumerate database structure and extract sensitive data.

## Defensive takeaways
- Always use parameterized queries/prepared statements with placeholder bindings for all database interactions
- Implement strict input validation using allowlists for expected data types and formats
- Apply principle of least privilege to database accounts used by the application
- Implement Web Application Firewall (WAF) rules to detect and block common SQL injection patterns
- Sanitize and escape all user-supplied data before database operations
- Conduct regular code reviews focusing on database query construction
- Perform automated and manual penetration testing on both GET and POST parameters
- Use ORM frameworks that enforce parameterized query construction

## Variant hunting
['Test POST parameters across all forms for SQL injection (login, registration, search, filters, etc.)', 'Examine multi-parameter POST requests where combinations of fields may bypass validation', 'Check for second-order SQL injection where injected data is stored then queried later', 'Test for time-based blind SQL injection in POST parameters using SLEEP() or WAITFOR delays', 'Investigate whether error-based SQL injection reveals database schema details', 'Verify POST-based injection works across different HTTP methods (PUT, PATCH, DELETE)', 'Test POST injection in API endpoints accepting JSON/XML bodies']

## MITRE ATT&CK
- T1190
- T1110
- T1020
- T1005
- T1040

## Notes
This writeup demonstrates a basic SQL injection exploitation on a deliberately vulnerable training application. bWAPP is designed for educational purposes. The vulnerability is trivially exploitable at 'low' security settings. Real-world applications should never exhibit such flaws. The POST-based variant is functionally equivalent to GET-based SQL injection but highlights the importance of validating all user input vectors, not just URL parameters. The information disclosure of OS details indicates critical server fingerprinting capability, which could be leveraged for further targeted attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
