# SQL Post/Search Injection on bWAPP

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** bWAPP (Buggy Web Application)
- **Bounty:** Not applicable - Educational/Training environment
- **Severity:** High
- **Vuln types:** SQL Injection, CWE-89: Improper Neutralization of Special Elements used in an SQL Command
- **Category:** web-api
- **Writeup:** https://medium.com/@crk2500/sql-post-search-injection-on-bwapp-92996fa3ef67

## Summary
A SQL injection vulnerability exists in the Post/Search functionality of bWAPP where user input from a text box is directly concatenated into SQL queries without proper sanitization. An attacker can inject arbitrary SQL commands through the search field to extract sensitive information such as the underlying operating system and database contents.

## Attack scenario (step by step)
1. Attacker navigates to the SQL Injection (Post/Search) vulnerable page on bWAPP
2. Attacker enters a legitimate movie name in the search text box to understand expected behavior
3. Attacker appends SQL injection payload (e.g., UNION-based or boolean-based injection) to the movie name input
4. The vulnerable application concatenates the unsanitized input directly into the SQL query without parameterization
5. The modified SQL query executes on the backend database, returning unintended results
6. Attacker observes the injected SQL output displayed in the web page, confirming successful exploitation and information disclosure

## Root cause
The application fails to use parameterized queries or prepared statements when handling POST request search parameters. User input from the text box is directly concatenated into SQL query strings without proper escaping or input validation, allowing attackers to break out of the intended query context.

## Attacker mindset
An attacker would first test basic SQL injection payloads in the search field to confirm the vulnerability exists. Upon confirmation, they would escalate to information gathering (system OS, database version) and then attempt to extract sensitive data like user credentials, application secrets, or database contents. The POST-based variant is attractive because it may bypass some WAF rules that focus on URL parameters.

## Defensive takeaways
- Always use parameterized queries/prepared statements with placeholders for all user input in SQL queries
- Implement input validation with whitelisting for search queries (e.g., alphanumeric characters and spaces only)
- Apply principle of least privilege - database accounts should have minimal necessary permissions
- Use Web Application Firewalls (WAF) to detect and block common SQL injection patterns
- Implement proper error handling to avoid exposing database error messages to end users
- Conduct regular security code reviews focusing on database query construction
- Perform dynamic application security testing (DAST) including SQL injection fuzzing

## Variant hunting
Look for similar POST-based injection vulnerabilities in: comment/feedback submission forms, filtering/sorting parameters in tables, file upload metadata fields, user profile update forms, and any backend search functionality. Similar vulnerabilities may exist in GET parameters, HTTP headers, cookies, or other POST fields on the same application.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1005: Data from Local System
- T1007: System Information Discovery
- T1557: Adversary-in-the-Middle

## Notes
This writeup documents exploitation of a deliberately vulnerable training application (bWAPP). The vulnerability is trivial to exploit due to complete lack of input sanitization on the low security setting. Real-world SQL injection exploitation may require more sophisticated techniques such as time-based blind injection, out-of-band data exfiltration, or bypassing WAF rules. The POST variant is less frequently tested than GET-based injection in some security assessments but represents the same underlying flaw.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
