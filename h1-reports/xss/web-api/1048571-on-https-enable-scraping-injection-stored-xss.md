# Unauthenticated API Endpoints Enable Data Scraping, Injection, and Stored XSS

## Metadata
- **Source:** HackerOne
- **Report:** 1048571 | https://hackerone.com/reports/1048571
- **Submitted:** 2020-12-02
- **Reporter:** skarsom
- **Program:** HackerOne (Undisclosed Organization)
- **Bounty:** Undisclosed
- **Severity:** Critical
- **Vuln:** Broken Authentication, Broken Authorization, Information Disclosure, SQL Injection, Stored Cross-Site Scripting (XSS), Insecure Direct Object References (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
An open debug API endpoint system lacks authentication and authorization controls, allowing unauthenticated attackers to scrape sensitive student and testing data, inject malicious payloads into the database, and execute stored XSS attacks. The API exposes multiple endpoints that should either be removed or protected with proper access controls, creating multiple attack vectors for data exfiltration and system compromise.

## Attack scenario
1. Attacker discovers the open API endpoints at the debug UI endpoint by analyzing application traffic or common endpoint patterns
2. Attacker uses date-based query parameters to enumerate and extract user IDs and profile information without any authentication
3. Attacker retrieves sensitive student data, language proficiency records, and testing information by iterating through returned user/profile IDs
4. Attacker crafts a malicious request with SQL injection payloads in vulnerable parameters (lngDesc, modDesc, etc.) to manipulate database records or extract additional data
5. Attacker inserts a stored XSS payload within the CData or other profile fields to generate a persistent attack vector accessible to other users
6. Attacker shares the crafted URL containing the stored XSS, which executes arbitrary JavaScript in victims' browsers when they access the affected profile page

## Root cause
Debug or administrative API endpoints were exposed in production without proper authentication, authorization, or input validation controls. The application likely failed to implement access control checks and relied on security-through-obscurity rather than proper API protection mechanisms.

## Attacker mindset
An attacker would recognize this as a goldmine for data exfiltration and privilege escalation. The complete lack of authentication makes exploitation trivial, requiring no special tools or credentials. The combination of data scraping + injection + XSS creates a multi-stage attack capability, allowing the attacker to not only steal data but also modify it and compromise other users.

## Defensive takeaways
- Remove all debug, administrative, and development endpoints from production environments, or implement strict authentication/authorization controls on them
- Implement proper authentication (OAuth 2.0, JWT) and role-based authorization checks on all API endpoints
- Never rely on obscurity as a security control; assume all endpoints will be discovered
- Implement input validation and parameterized queries to prevent SQL injection attacks on all user-controlled inputs
- Apply output encoding and Content Security Policy (CSP) headers to prevent stored XSS attacks
- Conduct regular security audits of all exposed endpoints and their access controls
- Implement request signing or API key validation even for internal-use endpoints to prevent unauthorized access
- Use Web Application Firewalls (WAF) to detect and block suspicious patterns in API requests
- Implement comprehensive logging and monitoring to detect abnormal API access patterns or data extraction attempts

## Variant hunting
Search for other debug endpoints using common patterns (/api/debug, /admin, /internal, /test, /ws) and analyze their access controls
Check for similar unauthenticated endpoints in backup or archive API versions (/v1, /v2, /legacy)
Test for IDOR vulnerabilities on other endpoints by modifying object IDs in requests
Attempt SQL injection in all string parameters across the API endpoints (dbName, OUid, lngDesc, modDesc, etc.)
Test for XXE, LDAP injection, or command injection if endpoints accept structured data or special parameters
Enumerate all available database names and tables through error messages or timing attacks on the dbName parameter
Check for similar debug UIs at common paths: /swagger, /api/docs, /graphql, /.well-known/ endpoints
Analyze JavaScript source maps and comments that might reference additional undocumented endpoints
Test for rate limiting or account lockout mechanisms to identify brute-force opportunities
Investigate whether similar authorization flaws exist in mobile APIs or backend services communicating with this API

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1110 - Brute Force (enumeration of IDs and parameters)
- T1530 - Data from Cloud Storage (data exfiltration)
- T1213 - Data from Information Repositories (scraping stored data)
- T1552 - Unsecured Credentials (unauthenticated access)
- T1598 - Phishing - Spearphishing Link (sharing XSS URL)
- T1189 - Drive-by Compromise (via stored XSS execution)
- T1190 - SQL Injection variant of exploit
- T1136 - Create Account (creating/modifying user records via injection)
- T1040 - Network Sniffing (if API traffic is unencrypted)

## Notes
The report is significantly redacted, masking the specific organization, endpoint names, and exact parameter values. However, the vulnerability pattern is clear: production-exposed debug/admin APIs without authentication controls. The combination of three distinct vulnerability types (IDOR/data scraping, SQL injection, stored XSS) in a single endpoint demonstrates the compounding risk of unauthenticated API exposure. The attacker demonstrates sophistication by chaining multiple endpoints together for progressive data extraction. The mention of 'debug UI' strongly suggests these are development/testing artifacts accidentally deployed to production. This is a common but critical mistake in DevOps practices where debugging interfaces are forgotten during deployment.

## Full report
<details><summary>Expand</summary>

**Summary:**
An open ████████ at the ████████ system enables quick and easy scraping of ███ without authentication nor authorization.

**Description:**
The █████ includes an open set of ██████endpoints at https://██████████. Any individual can execute requests on these endpoints without authorization nor authentication. These include the ability to view ████

Some of these endpoints are legitimately used in the ██████████ of the website, such as the one to ███████.

## Impact
An external, unauthorized, and unauthenticated attacker can scrape data of █████ by date on the ██████.

An external actor may also be able to perform injections against the database service through maliciously crafted attacks.

An external, unauthorized, and unauthenticated attacker can perform a stored XSS attack using on an ████████. 

## Step-by-step Reproduction Instructions

Data Extraction:
███████. Navigate to https://█████████.
████. Navigate to the "██████" ████ (https://████?████████████)
3. Enter the year ███████████████████████████████, the month █████████████, and the day █████████████, then press Invoke.
4. Success (█████████).
5. For further extraction, take one of the user IDs present in the JSON reply and paste it into the ███ ███████ (https://██████████?███████████).
6. For further extraction, take one of the profile IDs present in the JSON reply and paste it into the █████████ ██████ (also set "dbName" to "███") (https://█████████?███████). 

Stored XSS/Information Modification:
███. Navigate to the ███████ █████████ (https://█████████?███).
██████. Parameters: dbName = `██████████`, OUid = `█████████`, lngDesc = `████████`, modDesc = `███████`, wrkPLid = `███████`, clngPLid = `██████`, prfDate = `████████████/█████████/██████████████████████ ███████████████████:█████████████:███████████████████`, timeString = `Tue Dec ████████████ ██████████8:█████9:56 ███████████████████████████`, prfLink = `demofromskarsom`, CData = `<iframe onload="alert(██████)" style="display:none"></iframe>`, sessionID = `██████`
3. Click "Invoke".
4. Navigate to the following page, replacing `(GENSTRING)` with the integer that was returned from invoking the █████ request: `https://█████(GENSTRING)&B=███████&C=████████&D=demofromskarsom&view=true`
5. Success.

## Supporting Material
Navigate to████?A=███9█████98&B=██████&C=██████████&D=dodvdpdemo&view=true to see a stored XSS POC that I uploaded.
#███
#█████████
#████
#███████

## Suggested Mitigation/Remediation Actions
All endpoints unused by the frontend UI (based on a cursory search, this appears to be all but ███Plink) should be removed or guarded by authorization checks.

## Impact

Third-party actors can easily scrape language proficiency, testing, and student information through the ODA's debug UI and endpoints.

Third-party actors may also be able to perform injections against the database service through maliciously crafted strings within the INSERT and UPDATE ███s on the WS endpoints (did not attempt to prevent damage).

Third-party actors can further generate a page with a stored XSS attack within the "██████" of an inserted profile through█████.

</details>

---
*Analysed by Claude on 2026-05-12*
