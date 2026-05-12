# IDOR Vulnerability Allowing Unauthorized Access to Subreddit Mod Logs via GraphQL

## Metadata
- **Source:** HackerOne
- **Report:** 1658418 | https://hackerone.com/reports/1658418
- **Submitted:** 2022-08-03
- **Reporter:** high_ping_ninja
- **Program:** Reddit
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Missing Authorization Check
- **CVEs:** None
- **Category:** web-api

## Summary
A missing authorization check in Reddit's GraphQL API (gql.reddit.com) allows any authenticated user to access moderation logs from public or restricted subreddits they do not moderate. The vulnerability exists in the operation that retrieves mod logs, as it only validates the subredditName parameter without verifying the requester's moderator status. An attacker can enumerate through pagination to retrieve complete moderation histories of arbitrary subreddits.

## Attack scenario
1. Attacker logs into any Reddit account and obtains an authorization bearer token
2. Attacker crafts a POST request to gql.reddit.com with a GraphQL operation ID and target subredditName parameter
3. Attacker sends request without moderator credentials; the backend fails to validate requester's role in the target subreddit
4. Attacker receives first page of mod logs containing sensitive moderation actions, timestamps, and user information
5. Attacker checks the hasNextPage field in the response and, if true, extracts the endCursor value
6. Attacker iteratively requests subsequent pages by including the after parameter with endCursor values until all mod logs are exfiltrated

## Root cause
The GraphQL endpoint performing mod log retrieval lacks proper authorization middleware or access control checks. The server validates that a subreddit exists and the user is authenticated, but fails to verify that the authenticated user holds a moderator role in the specified subreddit before returning sensitive moderation data.

## Attacker mindset
An attacker seeking competitive intelligence, user harassment data, or to identify moderation patterns and policies. They could target high-profile subreddits to extract information about suspended users, removed content, and internal moderation decisions. The IDOR nature combined with pagination makes bulk harvesting of logs scalable and difficult to detect.

## Defensive takeaways
- Implement explicit authorization checks before returning any resource; verify the requester has the required role (moderator) for the targeted subreddit
- Use attribute-based access control (ABAC) or role-based access control (RBAC) consistently across all endpoints, including GraphQL operations
- Apply the principle of least privilege; sensitive data like mod logs should only be accessible to users with explicit moderator permissions
- Audit all GraphQL resolvers for missing authorization checks, especially those handling sensitive or internal data
- Implement rate limiting on sensitive endpoints to detect and block bulk enumeration attempts
- Log and monitor access to mod logs; alert on access patterns that suggest unauthorized bulk retrieval
- Conduct security review of all operation IDs and GraphQL mutations to ensure access control is consistently applied

## Variant hunting
Search for other endpoints or operations that return moderator-only data without proper authorization: admin action logs, user reports, modqueue items, subreddit settings, ban lists, and appeal requests. Check whether similar IDOR patterns exist in user profile endpoints, private community access, and team/organization resources.

## MITRE ATT&CK
- T1190
- T1526
- T1087

## Notes
The vulnerability is particularly severe because: (1) pagination support allows bulk data exfiltration without per-request detection, (2) the attack requires only basic authentication, not elevated privileges, (3) moderation logs contain sensitive user and moderation metadata, and (4) the GraphQL operation ID structure suggests this may be an internal API exposed unintentionally. The reporter provided a proof-of-concept script, indicating ease of exploitation.

## Full report
<details><summary>Expand</summary>

## Summary:
There's no check if the user is moderator of the particular subreddit or not while trying to access the mod logs via gql.reddit.com by using operation id. You can change the parameter **subredditName** to any target subreddit name which is public or restricted and get access to mod logs of that subreddit.

## Steps To Reproduce:
+  Log into any account as an attacker and get the authorization token
+ Send request given below at gql.reddit.com
```
POST / HTTP/2
Host: gql.reddit.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json
Content-Length: 62
X-Reddit-Compression: 1
Origin: https://www.reddit.com
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
Authorization: Bearer ourtoken
Referer: https://www.reddit.com/
Te: trailers

{"id":"6243efcbc61d","variables":{"subredditName":"any-subreddit"}}
```
The response will look something like below
{F1851522}
+ It only gives one page of logs.Look at the response and see if the value of **hasNextPage** is true or false. If It's false then there are no more logs other than the ones we got
+ If it's true then there are more logs and we can get them by just adding new variable **after** and assigning value of **endCursor**, which we can see in the reponse body of our request {F1851533}
+ Final request body will look something like this
```
{"id":"6243efcbc61d","variables":{"subredditName":"any-subreddit",
"after":"code-from-endCursor"
}}
```
+ After sending the request we'll get second page of logs. If we still get **hasNextPage** as true, Keep doing this untill we see **hasNextPage** set to false in the response. by doing this we can get all the pages of mod logs one by one.

> Use this script to make things easier in confirming this vulnerability (F1851561)
> The output will get stored in mod_log_out.txt in the same directory

  * [attachment / reference]

F1851522
F1851533
F1851561

## Impact

Confidential information getting exposed.

</details>

---
*Analysed by Claude on 2026-05-11*
