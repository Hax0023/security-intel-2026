# SQL Injection in URL Path Parameters leads to Database Access

## Metadata
- **Source:** HackerOne
- **Report:** 2633959 | https://hackerone.com/reports/2633959
- **Submitted:** 2024-07-31
- **Reporter:** tinopreter
- **Program:** Admyntec (corporate.admyntec.co.za)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** SQL Injection, Improper Input Validation, Path Traversal via SQL
- **CVEs:** None
- **Category:** uncategorised

## Summary
The application accepts ID parameters (userId, customerId, contactPersonId) directly in URL paths and concatenates them into SQL queries without sanitization or parameterized queries. An attacker can inject SQL payloads via single quotes in these parameters to dump the entire backend database containing user registration data including passport numbers, national IDs, and organization information.

## Attack scenario
1. Attacker identifies that the application uses URL path parameters for database lookups (e.g., /customerInsurance/newCustomerStep8/userId/868878/customerId/732562/contactPersonId/0)
2. Attacker tests for SQL injection by appending a single quote to the customerId parameter to trigger a SQL syntax error (732562')
3. Application returns database error or unexpected behavior, confirming SQL injection vulnerability in the parameter
4. Attacker uses SQLmap tool with an asterisk marker on the injection point to automate exploitation and enumerate database structure
5. Attacker successfully extracts the entire backend database including user credentials, passport numbers, national IDs, and organization data
6. Attacker exports sensitive PII data for use in identity theft, fraud, or sale on dark markets

## Root cause
The application concatenates URL path parameters directly into SQL query strings without using parameterized queries or input validation. The developer likely used string concatenation (e.g., 'SELECT * FROM users WHERE customerId = ' + request.param) instead of prepared statements with bound parameters.

## Attacker mindset
An opportunistic attacker scanning for common web vulnerabilities would quickly identify this since SQL injection is straightforward to test. The use of URL path parameters suggests the developer prioritized convenience over security. The presence of the vulnerability across multiple endpoints indicates systemic security negligence rather than isolated oversight, making this a high-confidence target for database exfiltration.

## Defensive takeaways
- Always use parameterized queries or prepared statements for all database interactions - never concatenate user input into SQL strings
- Implement strict input validation and type checking for all URL parameters (e.g., verify customerId is numeric only)
- Use an allowlist approach for parameter formats rather than blacklisting special characters
- Deploy Web Application Firewall (WAF) rules to detect and block common SQL injection patterns
- Implement database access controls with least privilege principles - application database user should have minimal necessary permissions
- Enable SQL error suppression in production to avoid leaking database schema information
- Conduct security code review focusing on all data flow paths from URL parameters to database queries
- Implement comprehensive logging and alerting for SQL injection attempts
- Use ORM frameworks that inherently protect against SQL injection through parameterization

## Variant hunting
Search for similar vulnerabilities in other URL path parameters across the application: userId, organizationId, documentId, insuranceId, etc. Check if POST/GET parameters have the same issue. Look for other endpoints accepting numeric identifiers in paths. Test for time-based blind SQL injection if union-based injection is filtered. Check for NoSQL injection if the backend uses MongoDB/similar. Verify if the vulnerability extends to other operations (update, delete) via different HTTP methods.

## MITRE ATT&CK
- T1190
- T1005
- T1020
- T1583.001

## Notes
The researcher provided clear reproduction steps with actual URLs and tool recommendations (SQLmap). The vulnerability is clearly critical as it affects multiple URL paths throughout the application. The presence of PII data (passport numbers, national IDs) in the database significantly elevates the impact. The researcher's recommendation for WAF is good but insufficient alone - parameterized queries are mandatory. No evidence of responsible disclosure timeline or response from Admyntec provided.

## Full report
<details><summary>Expand</summary>

## Summary:
The application https://corporate.admyntec.co.za/ application has an SQL injection in the URL paths since it takes the ID numbers in there and insert them directly into the backend SQL query without sanitizing them. In the registration, user ID number(Passport or National ID), Organization number are requested, as well as relevant docs. These are all stored in the backend Database.

https://corporate.admyntec.co.za/customerInsurance/newCustomerStep8/userId/868878/customerId/732562'/contactPersonId/0

## Steps To Reproduce:

  1. Using the URL generated when we get displayed the Insurance.   

{F3484515}  

  2. Introduce a single quote next to the customerId number and you realize this breaks the backend query.

```
https://corporate.admyntec.co.za/customerInsurance/newCustomerStep8/userId/868878/customerId/732562'/contactPersonId/0  
```
{F3484523}  
  3. Send this URL to any SQL epxloitation tool like SQLmap, Add an asterisk to the customerId number to tell the tool that's the injection point.  We can dump the database now.

{F3484537}  

##Please Note That This Occurs throughout many URL paths in the application.

#Recommendation
If you are taking parameters and inserting them into the backend SQL query, sanitize them to do away with any special characters attached to them.

Consider putting the application behind a WAF to make a potential SQLi vulnerability exploitation a bit tedious for an attacker.

## Impact

An attacker can exploit this to dump and download the backend database. This will give them access user information.

</details>

---
*Analysed by Claude on 2026-05-24*
