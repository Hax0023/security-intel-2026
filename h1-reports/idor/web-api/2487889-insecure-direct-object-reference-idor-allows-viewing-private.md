# Insecure Direct Object Reference (IDOR) Allows Viewing Private Report Details via /bugs.json Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 2487889 | https://hackerone.com/reports/2487889
- **Submitted:** 2024-05-02
- **Reporter:** bate5a
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
An unauthenticated or low-privileged attacker can access private bug reports belonging to any organization by sending a POST request to the /bugs.json endpoint with an arbitrary organization_id parameter and a text_query value. The endpoint fails to properly validate authorization, allowing disclosure of sensitive report metadata including titles, URLs, IDs, states, severity ratings, and reporter names.

## Attack scenario
1. Attacker identifies the vulnerable /bugs.json endpoint accepts POST requests with organization_id and text_query parameters
2. Attacker obtains or guesses a target organization_id (e.g., 58579 from program policy page)
3. Attacker crafts a POST request with the target organization_id and a single-digit text_query (e.g., '1')
4. Attacker includes valid session cookies and CSRF tokens in the request
5. The endpoint returns all private reports matching the search criteria without verifying the attacker's authorization to access that organization
6. Attacker exfiltrates sensitive report details including titles, URLs, severity ratings, and reporter information

## Root cause
The /bugs.json endpoint implements insufficient authorization checks. It accepts user-supplied organization_id parameters without verifying that the requesting user has legitimate access to that organization's reports. The endpoint performs text-based search functionality without enforcing organization membership or role-based access control (RBAC).

## Attacker mindset
An attacker seeks to gather intelligence on vulnerability reports submitted to competitor organizations or other targets. By enumerating organization IDs and crafting targeted queries, they can collect information about security issues before patches are released, enabling preparation of exploits or social engineering attacks.

## Defensive takeaways
- Implement strict authorization checks before returning any data - verify the requesting user has explicit access to the queried organization
- Use server-side session context to determine accessible organizations rather than trusting client-supplied organization_id parameters
- Apply principle of least privilege - restrict search functionality to only organizations the user is a member of
- Implement role-based access control (RBAC) with proper enforcement on all API endpoints returning sensitive data
- Add audit logging for all access to report details, particularly by non-program members
- Use opaque identifiers or UUIDs instead of sequential IDs to reduce enumeration attacks
- Implement rate limiting and anomaly detection for bulk queries across organizations

## Variant hunting
Test other endpoints accepting organization_id parameters for similar authorization bypass (e.g., /reports.json, /program_details.json)
Check if text_query parameter allows wildcard or regex patterns to bypass intended search filtering
Attempt to access other resource types (programs, users, comments) through similar endpoints with organization_id manipulation
Test if removing or modifying CSRF token bypasses additional validation layers
Check if changing HTTP method (GET instead of POST) bypasses endpoint-specific security controls
Enumerate organization IDs across a range to discover additional private organizations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Gather Victim Org Information
- T1589 - Gather Victim Identity Information
- T1538 - Cloud Service Discovery

## Notes
The vulnerability requires authentication (session cookie + CSRF token), limiting it to authenticated users or those with session hijacking capability. However, the lack of organization membership verification is the core flaw. The broad exposure of metadata fields (title, severity, reporter name) from private reports represents significant information disclosure that could enable targeting of specific security researchers or organizations.

## Full report
<details><summary>Expand</summary>

### Hi H1 i hope you are Doing Well Today :)



### Explaining

* I Found that any private reports can be accessed by sending a POST request to the `/bugs.json` endpoint. This vulnerable endpoint requires `organization_id`, which takes the organization's ID as a value. It also requires `text_query`, which is used to search for report IDs. within this  org  , Now you can append the example organization ID mentioned on the policy page, `58579`. and For the `text_query`, you can simply append a single digit, such as 1, or any other single number. This will query all reports containing this digit, provided they belong to the specified organization



### Step To Reproduce 

1.Send a POST request to this endpoint. You can change the organization_id to anything, but leave it as it is 

```

POST /bugs.json HTTP/2
Host: hackerone.com
Cookie:  __Host-session=Your-Session-Here
X-Csrf-Token: Your-Csrf-Here
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Te: trailers
Content-Length: 390

text_query=1&organization_id=58579&persist=true&sort_type=pg_search_rank&view=message&substates%5B%5D=new&substates%5B%5D=needs-more-info&substates%5B%5D=triaged&substates%5B%5D=resolved&substates%5B%5D=informative&substates%5B%5D=not-applicable&substates%5B%5D=duplicate&substates%5B%5D=retesting&substates%5B%5D=pending-program-review&substates%5B%5D=spam&duplicates_must_have_no_ref=true

```




### Poc Video

█████████

## Impact

idor lead to view private reports `title`,`url`,`id`,`state`,`substate`,`severity_rating`,`readable_substate`,`created_at`,`submitted_at`,`reporter_name`

</details>

---
*Analysed by Claude on 2026-05-11*
