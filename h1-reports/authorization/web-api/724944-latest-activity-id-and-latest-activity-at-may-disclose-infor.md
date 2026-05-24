# Information Disclosure of Internal Activity Metadata (latest_activity_id and latest_activity_at) to Unauthorized Report Participants

## Metadata
- **Source:** HackerOne
- **Report:** 724944 | https://hackerone.com/reports/724944
- **Submitted:** 2019-10-29
- **Reporter:** egrep
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** Low
- **Vuln:** Information Disclosure, Insufficient Access Control, Metadata Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
The HackerOne API exposes latest_activity_id and latest_activity_at fields for reports, which reveal the existence and timing of internal team-only comments and group assignments that should not be visible to unauthorized participants. An attacker with report participant access can query these fields via both REST and GraphQL endpoints to infer internal discussion activity without viewing actual content.

## Attack scenario
1. Attacker is added as a report participant by a victim organization
2. Victim organization creates internal team-only comments or performs group assignments on the report
3. Attacker requests the report via REST API (.json endpoint) to obtain the latest_activity_id field
4. Attacker crafts a GraphQL query targeting the Report node to retrieve latest_activity_at timestamp
5. Attacker analyzes the activity timestamps to correlate with known internal events or identify sensitive discussion periods
6. Attacker infers information about internal processes, team coordination, and security assessment activities based on activity patterns

## Root cause
The API authorization layer fails to properly filter sensitive metadata fields based on user permissions. The latest_activity_at and latest_activity_id fields are returned for all queries regardless of whether the authenticated user should have visibility into internal activities. The application provides timestamps for internal-only activities without checking if the querying user has permission to view those specific activities.

## Attacker mindset
A participating researcher or external user seeks to gather intelligence about internal vulnerability assessment processes, team communication patterns, and timing of internal discussions. By observing activity timestamps, they can infer when critical decisions are made, estimate response times, or identify correlations between their submissions and internal team actions, potentially giving them strategic advantage in future submissions.

## Defensive takeaways
- Implement granular authorization checks on all API response fields, filtering metadata fields based on user role and access level
- Audit all timestamp and activity ID fields to ensure they are not exposed in API responses when users lack permission to view the underlying activities
- Consider whether metadata like latest_activity_at should be returned at all for internal-only activities, or return generic/rounded timestamps
- Use consistent authorization logic across REST and GraphQL endpoints to prevent bypassing restrictions through different API interfaces
- Implement field-level security controls that strip sensitive metadata from responses based on user permissions
- Regularly audit GraphQL queries to ensure union types and node queries properly enforce authorization rules

## Variant hunting
Check if other timestamp fields (created_at, updated_at, commented_at) on internal comments are exposed through API queries
Test if activity_count or similar metrics are exposed for internal activities
Investigate whether internal attachment/file metadata timestamps are visible
Check if team-only activity streams or activity logs are queryable through GraphQL
Test if deleted or hidden activities expose timestamps through API responses
Examine if internal custom field updates expose their latest_activity timestamps
Check other resource types (teams, vulnerabilities, comments) for similar metadata leakage

## MITRE ATT&CK
- T1526
- T1592
- T1087

## Notes
This is a relatively minor information disclosure as it does not expose the actual content of internal communications, only that activity occurred and when. However, in the context of security research coordination, even metadata about activity timing can provide valuable intelligence to adversaries. The vulnerability demonstrates the importance of implementing authorization at the field level rather than just the resource level. The researcher demonstrated good methodology by showing exploitation across multiple API endpoints (REST and GraphQL).

## Full report
<details><summary>Expand</summary>

Mini information disclosure related with team's internal comments/assign group activity id and date_time are exposed

Steps:
1) As victim, Create a sandbox team and create report
2) Add attacker as a participant for the report
3) As victim, create some internal comments ( team -only comments )/assign group for the report
4) As attacker , request url "https://hackerone.com/reports/<report-id>.json" ( Eg: ███ ) to view latest_activity_id (█████)
5) As attacker, post below graphql request to view "latest_activity_at" date-time of internal discussion ( ██████ )

Request:

```
POST /graphql? HTTP/1.1
Host: hackerone.com
Connection: close
Content-Length: 123
Accept: */*
X-Auth-Token: ███
Origin: https://hackerone.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36
Sec-Fetch-Mode: cors
Content-Type: application/json
Sec-Fetch-Site: same-origin
Referer: https://hackerone.com/vairaselvamvvs
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: ███

{"query":"query { node(id: \"gid://hackerone/Report/█████\") { ... on Report { _id,latest_activity_at }}}","variables":{}}
```

Response:

```
HTTP/1.1 200 OK
Date: Tue, 29 Oct 2019 17:50:48 GMT
Content-Type: application/json; charset=utf-8
Connection: close
Cache-Control: no-cache, no-store
Content-Disposition: inline; filename="response."
X-Request-Id: eb31d77a-6b54-4bcb-8007-c90f0b19307d
Set-Cookie: ███
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Expect-CT: enforce, max-age=86400
Content-Security-Policy: default-src 'none'; base-uri 'self'; block-all-mixed-content; child-src www.youtube-nocookie.com b5s.hackerone-ext-content.com; connect-src 'self' www.google-analytics.com errors.hackerone.net; font-src 'self'; form-action 'self'; frame-ancestors 'none'; img-src 'self' data: cover-photos.hackerone-user-content.com hackathon-photos.hackerone-user-content.com profile-photos.hackerone-user-content.com hackerone-us-west-2-production-attachments.s3.us-west-2.amazonaws.com; media-src 'self' hackerone-us-west-2-production-attachments.s3.us-west-2.amazonaws.com; script-src 'self' www.google-analytics.com; style-src 'self' 'unsafe-inline'; report-uri https://errors.hackerone.net/api/30/csp-report/?sentry_key=61c1e2f50d21487c97a071737701f598
Referrer-Policy: strict-origin-when-cross-origin
X-Content-Type-Options: nosniff
X-Download-Options: noopen
X-Frame-Options: DENY
X-Permitted-Cross-Domain-Policies: none
X-XSS-Protection: 1; mode=block
CF-Cache-Status: DYNAMIC
Server: cloudflare
CF-RAY: 52d6fe6eed5dd5fc-BOM
Content-Length: 82

{"data":{"node":{"_id":"████████","latest_activity_at":"███████"}}}
```

## Impact

latest_activity_id and latest_activity_at related with team internal discussion exposed

</details>

---
*Analysed by Claude on 2026-05-24*
