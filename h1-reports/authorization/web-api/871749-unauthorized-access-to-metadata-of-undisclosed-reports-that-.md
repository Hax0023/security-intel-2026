# Unauthorized access to metadata of undisclosed reports via report_retests GraphQL query

## Metadata
- **Source:** HackerOne
- **Report:** 871749 | https://hackerone.com/reports/871749
- **Submitted:** 2020-05-12
- **Reporter:** msdian7
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Information Disclosure, Insufficient Access Control, GraphQL Authorization Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
An unauthenticated attacker can query the GraphQL endpoint to retrieve sensitive metadata about undisclosed reports by accessing the report_retests object in the User node. The vulnerability allows disclosure of asset names, asset types, severity ratings, and weakness names from reports that should remain confidential. This enables reconnaissance of vulnerability information across HackerOne programs without proper authorization.

## Attack scenario
1. Attacker identifies a target username of a HackerOne researcher or user known to participate in retest activities
2. Attacker constructs a GraphQL query requesting the report_retests fragment from the User node, including sensitive fields like asset_name, severity_rating, weakness_name, and asset_type
3. Attacker sends the POST request to /graphql endpoint and receives response containing retest metadata for both disclosed and undisclosed reports
4. Attacker filters results by identifying entries where report field is null, which indicates undisclosed reports
5. Attacker extracts sensitive metadata (asset names, vulnerability types, severity) from the null-report objects
6. Attacker correlates this information across multiple users to build a comprehensive profile of unreleased vulnerabilities in target programs

## Root cause
The GraphQL schema exposes sensitive fields from report_retests without proper authorization checks to verify that the requesting user has permission to view report metadata. The API returns report metadata even when the report reference itself is null (undisclosed), failing to implement consistent field-level access control across related objects.

## Attacker mindset
An attacker seeks to gather intelligence about unreported vulnerabilities affecting specific targets before public disclosure, potentially to identify zero-days, prioritize targets for exploitation, or gain competitive advantage in bug bounty hunting.

## Defensive takeaways
- Implement field-level authorization checks in GraphQL resolvers to verify user permissions before returning sensitive data
- Apply consistent access control across related objects - if a report is undisclosed, all metadata derived from that report should also be inaccessible
- Audit all GraphQL queries that return report data to ensure access checks are enforced at query depth, not just root level
- Consider filtering report_retests to exclude undisclosed reports entirely from public user profiles
- Implement rate limiting and monitoring on GraphQL endpoints to detect reconnaissance patterns
- Regularly review GraphQL schema to identify information leakage through sibling/related objects

## Variant hunting
Check other user-related GraphQL queries (activity feeds, submission history, reputation breakdowns) for similar metadata leakage
Examine nested objects in organization and program endpoints for report metadata exposure
Test permission boundaries when accessing deleted, private, or unverified reports through various entry points
Query relationships between users and reports to identify other paths to undisclosed report metadata
Check if other retest-related queries (report_retest_invitations, report_retest_state_changes) expose similar information

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (GraphQL API exploitation)
- T1526 - Enumerate External Network Infrastructure (reconnaissance of target programs)
- T1589 - Gather Victim Identity Information (enumerate users and their activities)
- T1598 - Phishing for Information (could be combined with social engineering using gathered intel)

## Notes
The vulnerability is particularly severe because it enables systematic reconnaissance of vulnerability reports across all HackerOne programs. An attacker can profile multiple researchers to aggregate information about unreleased vulnerabilities. The fact that metadata is returned even when report=null demonstrates a logic error in authorization checks. The disclosure includes redacted usernames and IDs suggesting HackerOne's initial response included fixing access controls. This type of vulnerability is common in GraphQL implementations where developers fail to implement field-level authorization consistent with root-level checks.

## Full report
<details><summary>Expand</summary>

**Summary:**
`report_retests` object in `User` node discloses some information about undisclosed report

**Description:**
An attacker can get some infomation such as "asset_name" , "asset_type" , "severity_rating" , "weakness_name" of undisclosed report

### Steps To Reproduce

1. Invoke the below graphql call 

POST /graphql HTTP/1.1
Host: hackerone.com

```
{"operationName":"UserMiniProfile","variables":{"username":"msdian7"},"query":"query UserMiniProfile($username: String!) {\n  user(username: $username) {\n    id\n    ...UserMiniProfileLayout\n    __typename\n  }\n}\n\nfragment UserMiniProfileLayout on User {\n  id\n  large_profile_picture: profile_picture(size: large)\n  name\n  username\n  bio\n  reputation\n  signal\n  report_retests{total_count,approved_count,nodes{report{_id},created_at,asset_name,asset_type,award_amount,claimed_at,report_state,weakness_name,severity_rating,report_substate,report_retest_users{total_count,nodes{_id,user{username},state,invitation{id}}}}}\n  cleared\n  __typename\n}\n"}
```

2.  You will get below response 

```
████
```
3.  From that above response search for "report":null  , all that "report":null json objects are , undisclosed report , i take the last json object for my POC 

{"report":null,"created_at":"2020-05-11T19:21:25.507Z","asset_name":"https://www.hackerone.com","asset_type":"URL","award_amount":"50.00","claimed_at":null,"report_state":"closed","weakness_name":null,"severity_rating":"low","report_substate":"resolved","report_retest_users":{"total_count":1,"nodes":[{"_id":"███","user":{"username":"██████████"},"state":"approved","invitation":null}

from this json, we  can see user █████ retested one undisclosed report . 
 and the informations about that undisclosed report are ,
a. That report filed to "https://www.hackerone.com"
b. severity of that report is "low"


We can see some other  undisclosed reports too .

the another example is ,

{"report":null,"created_at":"2020-03-17T22:20:07.215Z","asset_name":"https://hackerone.com","asset_type":"URL","award_amount":"0.00","claimed_at":null,"report_state":"closed","weakness_name":"Information Disclosure","severity_rating":"medium","report_substate":"resolved","report_retest_users":{"total_count":1,"nodes":[{"_id":"███████","user":{"username":"████"},"state":"unassigned","invitation":null}]}

This is another undisclosed report, filed to "https://hackerone.com" asset with the "Information Disclosure" weakness and severity of report is "medium"

@security program, has more undisclosed report, so we cant detect exact undisclosed report, Consider if a new program start to use hackerone.com and uses retest feature , we can get that program's  asset_name , asset_type, weakness_name and severity_rating without disclosure of that report

## Impact

an attacker can get Information of undisclosed report

</details>

---
*Analysed by Claude on 2026-05-24*
