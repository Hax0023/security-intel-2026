# Information Disclosure via /reports/:id.json Endpoint Exposes Reporter Sensitive Data

## Metadata
- **Source:** HackerOne
- **Report:** 3000510 | https://hackerone.com/reports/3000510
- **Submitted:** 2025-02-19
- **Reporter:** avinash_
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Information Disclosure, Sensitive Data Exposure, Improper Access Control, Data Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
The /reports/:id.json endpoint exposes sensitive reporter account information including email addresses, OTP backup codes, phone numbers, GraphQL secret tokens, and other internal account details through the API response. This vulnerability allows unauthorized access to private data of security researchers who submitted vulnerability reports.

## Attack scenario
1. Attacker identifies a disclosed HackerOne report by its ID number
2. Attacker crafts a GET request to /reports/{id}.json endpoint
3. Server returns JSON response containing full reporter profile details
4. Attacker extracts sensitive data including email, OTP codes, phone number, and API tokens
5. Attacker could use compromised credentials for account takeover or token abuse
6. Attacker could target reporter with phishing or social engineering using disclosed information

## Root cause
The JSON API endpoint lacks proper data filtering/sanitization in its response serialization. The endpoint returns the complete reporter object without excluding sensitive fields that should never be exposed in public API responses. No field-level access control was implemented to differentiate between public-safe and private-sensitive attributes.

## Attacker mindset
An opportunistic attacker could systematically enumerate disclosed reports to harvest researcher credentials, API tokens, and personal contact information for account compromise, identity theft, or social engineering campaigns. The /reports/:id.json endpoint provides a direct, unauthenticated channel to extract this data at scale.

## Defensive takeaways
- Implement explicit allowlist of safe fields for public API serialization rather than default expose-all approach
- Add field-level authorization checks to exclude sensitive attributes (OTP, tokens, phone, email) from unauthenticated responses
- Never serialize authentication tokens, backup codes, or secrets in any public API response
- Use separate response DTOs for public vs authenticated contexts
- Audit all JSON endpoints for similar data leakage patterns across the application
- Implement response filtering middleware that strips sensitive fields based on user context
- Add security headers to prevent cached exposure of sensitive JSON responses

## Variant hunting
Check other report-related endpoints (.xml, .pdf, .csv formats) for similar leakage
Test /reports/:id endpoints with different authentication levels and user roles
Examine user profile JSON endpoints (/users/:id.json) for same serialization issues
Search for other public API endpoints that may expose internal user objects without filtering
Test archived/deleted reports to see if sensitivity data is retained
Check if pagination or bulk report endpoints (/reports.json) have same vulnerability

## MITRE ATT&CK
- T1190
- T1526
- T1592
- T1087
- T1589

## Notes
This is a classic API data exposure vulnerability stemming from improper serialization of domain objects. The vulnerability is particularly severe because it affects security researchers on a bug bounty platform, potentially compromising their primary communication channels and authentication mechanisms. The presence of OTP backup codes and GraphQL tokens suggests direct account takeover is possible.

## Full report
<details><summary>Expand</summary>

Hi

The.json endpoint of any disclosed report is leaking reporter's email, OTP backup codes, reporter's phone number, "graphql_secret_token", tshirt size all the reporter account's internal details etc. 

```
 GET /reports/█████.json HTTP/2
Host: hackerone.com
````

* I was checking Hackerone's disclosed report ██████████ and suddenly during check found .json point is leaking too much data of reporter ```████``` . I immediately reported it to you.

█████



* PoC:- Leakage of data of reporter

█████
█████





## Impact

Reporter H1 account private data disclosed

</details>

---
*Analysed by Claude on 2026-05-11*
