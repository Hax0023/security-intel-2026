# Information Disclosure in API Endpoint /users

## Metadata
- **Source:** HackerOne
- **Report:** 3027405 | https://hackerone.com/reports/3027405
- **Submitted:** 2025-03-09
- **Reporter:** moha1sd
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
An endpoint (/user) is exposing sensitive user information, including id, first name, last name, email, role, and auth_data, to unauthenticated users. This allows anyone to retrieve private user details without authentication, leading to a severe security risk.

## Impact

1- Critical exposure of Personally Identifiable Information (PII), violating data protection policies.

2- Unauthorized access

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

An endpoint (/user) is exposing sensitive user information, including id, first name, last name, email, role, and auth_data, to unauthenticated users. This allows anyone to retrieve private user details without authentication, leading to a severe security risk.

## Impact

1- Critical exposure of Personally Identifiable Information (PII), violating data protection policies.

2- Unauthorized access to user details, allowing attackers to collect user data.

3- Potential for phishing and social engineering attacks by exploiting leaked emails and user roles.

4- Exposure of authentication-related data (auth_data), which could aid in further attacks or unauthorized access.

## System Host(s)
█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Visit the vulnerable website ████████ as an unauthenticated user

Navigate to the /user endpoint.

Observe the response containing exposed user data.


You can also use the below request:

GET /users HTTP/2
Host: ██████████
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

And observe the response

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
