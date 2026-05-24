# Authorization Bypass via Exposed Admin JavaScript Leading to IDOR and PII Leakage of Military Personnel

## Metadata
- **Source:** HackerOne
- **Report:** 1489470 | https://hackerone.com/reports/1489470
- **Submitted:** 2022-02-23
- **Reporter:** lubak
- **Program:** Redacted (Military/Government Related)
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Access Control, Insecure Direct Object Reference (IDOR), Missing Authentication, Sensitive Data Exposure, Improper Authorization
- **CVEs:** None
- **Category:** web-api

## Summary
An administrative JavaScript file was publicly accessible without authentication, exposing an API endpoint that returns sensitive PII data including names, phone numbers, and emails of military personnel and family members. The endpoint suffered from IDOR vulnerability, allowing enumeration of approximately 50,000 user application records through parameter manipulation.

## Attack scenario
1. Attacker discovers publicly accessible admin.js file via directory enumeration or source code analysis
2. Attacker analyzes JavaScript to identify administrative API endpoints and their parameters
3. Attacker crafts POST request to the application data endpoint without authentication credentials
4. Attacker modifies the ID/URL parameter to retrieve different user application records
5. Attacker systematically enumerates IDs (0-60000) to extract all accessible PII records
6. Attacker obtains complete dataset of military personnel and family member information including names, phone numbers, and emails

## Root cause
The administrative interface was deployed with default public accessibility without proper authentication and authorization checks. The application failed to: (1) implement authentication gates before serving admin.js, (2) validate user authorization on API endpoints, (3) implement IDOR protections through proper access control checks per request

## Attacker mindset
An attacker identified and exploited the combination of missing authentication, exposed admin functionality, and IDOR vulnerabilities to conduct large-scale data harvesting. The systematic enumeration approach (testing sequential IDs up to 60000) demonstrates methodical reconnaissance and exploitation targeting sensitive military data.

## Defensive takeaways
- Implement mandatory authentication before serving any administrative JavaScript or functionality
- Add per-request authorization checks on all API endpoints verifying user role and resource ownership
- Remove or properly secure admin.js files from public-facing directories; use build-time bundling and authentication gating
- Implement IDOR protections: use unpredictable identifiers, verify user owns the resource, implement rate limiting on enumeration attempts
- Conduct security code review focusing on access control in JavaScript files and API endpoints
- Implement logging and anomaly detection for bulk data access patterns
- Apply principle of least privilege: admin endpoints should require explicit admin authentication tokens
- Use Web Application Firewall (WAF) rules to detect and block sequential ID enumeration patterns

## Variant hunting
Search for other exposed .js files in /admin, /management, /dashboard directories without authentication
Test other POST endpoints in admin.js for IDOR vulnerabilities with sequential parameter values
Check if GET requests also bypass authentication on the same endpoint
Attempt to enumerate other resource types (users, settings, configurations) through similar IDOR patterns
Test if authorization bypass works for DELETE/PUT operations on sensitive data
Search for similar endpoints in JavaScript files that may accept different parameter names or formats
Check if authentication can be bypassed through HTTP header manipulation or token tampering

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Acquire Infrastructure: Discover Infrastructure
- T1556 - Modify Authentication Process: Disable or Modify MFA
- T1110 - Brute Force
- T1078 - Valid Accounts
- T1530 - Data from Cloud Storage: Exfiltration

## Notes
This report demonstrates a critical infrastructure vulnerability in military/government systems with extremely high impact due to PII exposure of military personnel. The combination of three vulnerabilities (missing authentication, IDOR, and unauthenticated endpoint exposure) created a severe data leakage vector affecting approximately 50,000 records. The redacted nature of the report suggests sensitivity around the affected organization and data types involved.

## Full report
<details><summary>Expand</summary>

Hi team!
During testing ████ I found  javascript file containing administrative panel functionality.
It is accessible at: 
https://████/█████████
In this file I found an end point responsible for returning data about applications of the website users to the website administrators.
The returned data contains PII data (Full name, phone and email) of military personnel, and or their family members.


## References
Steps to reproduce:

Run following curl command to retrieve data:
curl https://███/███ -X POST -data="url=%2F████████" -k

Modifying ██████████ parameter result in different Application being returned.
I have tested retrieving following ids: █████.

Trying to retrieve record 60000 returns no information, so maybe ~50000 applications are accessible.

## Impact

PII leak of military personnel and family members

## System Host(s)
█████████

## Affected Product(s) and Version(s)
/█████████

## CVE Numbers


## Steps to Reproduce
Run following command to retrieve data:
curl https://███████/███ -X POST -data="url=%2F████████" -k

Modifying ██████ parameter result in different Application being returned.
I have tested retrieving following ids: ███.
Trying to retrieve record 60000 returns no information, so maybe ~50000 applications are accessible.

## Suggested Mitigation/Remediation Actions
1. admin.js should be available only after Administrator successfully logs in
2. all administrative end points must check if authorized administrator is requesting them



</details>

---
*Analysed by Claude on 2026-05-24*
