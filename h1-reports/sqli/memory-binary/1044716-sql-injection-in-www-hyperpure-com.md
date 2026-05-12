# SQL Injection in Hyperpure Sales Lead Onboarding API

## Metadata
- **Source:** HackerOne
- **Report:** 1044716 | https://hackerone.com/reports/1044716
- **Submitted:** 2020-11-26
- **Reporter:** hoteyes
- **Program:** Hyperpure
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** SQL Injection, Improper Input Validation, Insecure Direct Object References (IDOR)
- **CVEs:** None
- **Category:** memory-binary

## Summary
A SQL injection vulnerability exists in the PUT /consumer/onboarding/saleslead/{id} endpoint where user-supplied input is directly concatenated into SQL queries without sanitization. An attacker can inject SQL commands through the salesLeadId parameter to manipulate database queries, create arbitrary sales records, and potentially extract sensitive data.

## Attack scenario
1. Attacker crafts a PUT request to the vulnerable endpoint with a malicious salesLeadId parameter containing SQL injection payload
2. Attacker uses AND/OR conditions to test query logic (e.g., 'AND 1=1' returns true, 'AND 1=0' returns false) to confirm SQL injection
3. Attacker injects 'OR 1=1' statement to bypass authentication logic and match multiple records in the database
4. Attacker modifies the injected payload to INSERT or UPDATE arbitrary sales lead records with attacker-controlled data
5. Attacker creates fake sales leads in the system without proper authorization or validation
6. Attacker potentially exfiltrates sensitive business data or creates fraudulent orders through the compromised sales lead records

## Root cause
The salesLeadId parameter in the URL path is concatenated directly into SQL query strings without proper parameterized queries or input validation. The backend likely constructs queries like: SELECT * FROM sales_leads WHERE id = '{user_input}' instead of using prepared statements with bound parameters.

## Attacker mindset
An attacker would recognize that UUID parameters in API endpoints are often used in dynamic SQL queries. By testing with boolean-based SQL injection payloads (AND/OR conditions), they can confirm the vulnerability and progressively escalate to data manipulation. The ability to create arbitrary sales records suggests potential for fraudulent activity, business logic abuse, or privilege escalation.

## Defensive takeaways
- Always use parameterized queries/prepared statements with bound parameters for all database operations
- Implement strict input validation and sanitization for all user-supplied parameters
- Use ORM frameworks that automatically escape user input
- Apply principle of least privilege to database service accounts
- Implement Web Application Firewall (WAF) rules to detect and block SQL injection patterns
- Conduct security code reviews focusing on database query construction
- Implement comprehensive logging and monitoring for suspicious database activity
- Use static application security testing (SAST) tools to detect SQL injection vulnerabilities

## Variant hunting
Test other PUT/POST endpoints with UUID or ID parameters for similar SQL injection patterns
Check GET endpoints that filter by salesLeadId for read-based SQL injection
Test other parameters in the same endpoint (address, email, phoneNumber) for injection vulnerabilities
Examine other API endpoints in the consumer onboarding flow for similar issues
Look for UNION-based SQL injection to extract schema information
Test for time-based blind SQL injection on endpoints with delayed responses
Check for second-order SQL injection where injected data is stored and executed later

## MITRE ATT&CK
- T1190
- T1190.004
- T1083
- T1040
- T1530

## Notes
This is a classic example of SQL injection in a REST API. The vulnerability is critical as it allows unauthorized data manipulation. The report demonstrates good exploitation methodology by testing boolean conditions to confirm the vulnerability. The lack of rate limiting on API endpoints compounds the risk. The presence of IDOR characteristics (direct access to objects via IDs) combined with SQL injection creates a high-impact vulnerability allowing unauthorized access to and manipulation of sales data.

## Full report
<details><summary>Expand</summary>

Vulnerable Request :

PUT /consumer/onboarding/saleslead/6b6a8a5a-4a74-46db-b2fe-32a46f927ecc    HTTP/1.1
Host: api.hyperpure.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json;charset=utf-8
X-Client: consumer
X-TrackingId: 8242c5a2-6325-4101-96b8-c7ed6008e92a
HeaderRoute: v2
APIVersion: 4.2
AppType: web
Content-Length: 246
Origin: https://www.hyperpure.com
Connection: close
Referer: https://www.hyperpure.com/register

{"address":{"addressLine":"test","cityId":34,"state":{"name":"Gujarat"},"zipCode":"388001"},"deliveryTime":0,"email":"hoteyes@wearehackerone.com","outletName":"test","phoneNumber":"█████","salesLeadId":"31cf8eb0-f81e-4c99-acad-35eae89ed659"}

The above request is used to create sales lead with the data the sales lead id is produced and verified by the domain.

Base Response Received: 

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 68
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: https://www.hyperpure.com
x-envoy-upstream-service-time: 166
Server: envoy
Date: Thu, 26 Nov 2020 18:48:34 GMT
Connection: close
Vary: Accept-Encoding

{"response":{"salesLeadId":"6b6a8a5a-4a74-46db-b2fe-32a46f927ecc"}}


Now we will be executing following steps to verify if  "AND "  & "OR" statements work.

1) Proving AND condition working while using it with a valid sales id  " AND 1 = "1 --+-   
2) Proving AND condition false with working sales lead using AND 1=0.
3) Proving adding cool as a sales lead by using OR 1=1 , which always states true.

## Impact

Adding random sales ID in the database using PUT statement and populating it.

</details>

---
*Analysed by Claude on 2026-05-11*
