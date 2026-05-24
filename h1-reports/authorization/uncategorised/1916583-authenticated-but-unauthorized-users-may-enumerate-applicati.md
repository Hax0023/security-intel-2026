# Authenticated but unauthorized users may enumerate Application names via the API

## Metadata
- **Source:** HackerOne
- **Report:** 1916583 | https://hackerone.com/reports/1916583
- **Submitted:** 2023-03-24
- **Reporter:** bean-zhang
- **Program:** Argo CD
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Enumeration, Improper Access Control
- **CVEs:** CVE-2022-41354
- **Category:** uncategorised

## Summary
Argo CD versions 0.5.0 and later are vulnerable to information disclosure through API error messages that reveal application names to authenticated users without appropriate authorization. Unauthorized users can enumerate valid application names by inspecting error responses from the `/api/v1/application/**/logs` endpoint, which disclose whether applications exist via messages like 'error getting application by name: [name] not found'.

## Attack scenario
1. Attacker creates or obtains a low-privileged Argo CD user account with no application module privileges
2. Attacker systematically requests the `/api/v1/application/**/logs` endpoint with various application name guesses or common naming patterns
3. API responds with differentiated error messages: some indicating 'not found' (non-existent apps) vs authorization errors (existing apps without access)
4. Attacker analyzes error response patterns to identify which application names actually exist in the system
5. Attacker compiles list of discovered application names for use in social engineering or follow-up privilege escalation attacks
6. Attacker uses application knowledge to target administrators or exploit subsequent vulnerabilities with informed targeting

## Root cause
Insufficient error message sanitization and information leakage in API responses. The system fails to distinguish between 'resource not found' and 'unauthorized access' errors at the API layer, allowing attackers to infer resource existence through error message analysis.

## Attacker mindset
Information gathering and reconnaissance attacker seeking to build situational awareness about target infrastructure. The enumeration serves as a precursor to social engineering or privilege escalation attacks rather than direct exploitation.

## Defensive takeaways
- Implement consistent error responses that do not leak resource existence information to unauthorized users
- Return generic 'Unauthorized' or 'Forbidden' status codes for all access denied scenarios regardless of whether the resource exists
- Sanitize all API error messages to prevent information disclosure about valid resource names or identifiers
- Apply consistent authorization checks before any resource operation including logging endpoints
- Implement rate limiting on API endpoints to prevent systematic enumeration attempts
- Log and alert on suspicious enumeration patterns (multiple 404s or authorization failures from same user/IP)
- Review all API endpoints for similar information leakage vulnerabilities through error messages
- Use structured logging that separates security-relevant details from user-facing error responses

## Variant hunting
Check other API endpoints for similar error message information leakage (projects, repositories, clusters)
Audit webhook and notification endpoints for enumeration vectors
Examine configuration export/import endpoints for resource name leakage
Test status endpoints that might reveal application state information
Investigate metrics or audit log endpoints for enumeration possibilities
Check sync and deployment endpoints for similar authorization bypass patterns

## MITRE ATT&CK
- T1590
- T1526
- T1087
- T1028

## Notes
This is a classic case of information disclosure through error message analysis. The vulnerability requires authentication but allows unauthorized enumeration, making it useful for reconnaissance in targeted attacks. The fix likely involved returning uniform error responses regardless of authorization vs existence status. The impact is heightened in multi-tenant or organizational deployments where application names might be sensitive.

## Full report
<details><summary>Expand</summary>

All versions of Argo CD starting with v0.5.0 are vulnerable to an information disclosure bug allowing unauthorized users to enumerate application names by inspecting API error messages. 

STEPS:
1. Login argocd with a user who has not application module's priviledge.
2. The user request 'api/v1/application/**/logs' restful api to download a log file.
3. The log file's content lead a information disclosure bug, which allowing unauthorized users to enumerate application names by inspecting API error messages. The error messages like 'error gettingg applicaiton by name: ** not found'.

## Impact

An attacker could use the discovered application names as the starting point of another attack. For example, the attacker might use their knowledge of an application name to convince an administrator to grant higher privileges (social engineering).

</details>

---
*Analysed by Claude on 2026-05-24*
