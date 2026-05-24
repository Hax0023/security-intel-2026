# Member Users Can Integrate Email and Connect Calendar via Improper Access Control on Calendar Auth Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1486310 | https://hackerone.com/reports/1486310
- **Submitted:** 2022-02-20
- **Reporter:** emperor
- **Program:** 8x8 Inc (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Broken Access Control, Improper Authorization, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Member users without permission to access the admin rooms section can bypass access controls by directly calling the calendar authentication endpoint GET /meet-external/spot-roomkeeper/v1/calendar/auth/init. By crafting a request with their JWT token and specifying a redirect URL pointing to the admin rooms area, unprivileged users can complete OAuth integration and add their email to calendar synchronization features reserved for administrators.

## Attack scenario
1. Attacker with member-level user account identifies that the admin section has a rooms management area inaccessible to their role
2. Attacker discovers the unauthenticated calendar auth initialization endpoint /meet-external/spot-roomkeeper/v1/calendar/auth/init accepts GET requests with redirect URL parameters
3. Attacker crafts a request to the endpoint using their member JWT token with successRedirectUrl parameter pointing to admin.8x8.vc/#/rooms/add
4. Endpoint returns an OAuth authorization URL (Cronofy) without validating whether the requesting user has permission to integrate calendars
5. Attacker completes the OAuth flow by authenticating with their email provider, establishing calendar integration
6. Member user gains unauthorized access to calendar integration functionality intended only for administrators

## Root cause
The calendar authentication initialization endpoint performs authentication (verifies JWT) but lacks authorization checks to validate whether the requesting user has the required role/permission to integrate calendars. The endpoint accepts arbitrary redirect URLs without validating them against user permissions, allowing privileged admin-only features to be accessed by lower-privilege users.

## Attacker mindset
An attacker with member-level access notices clear permission boundaries in the UI (rooms area restricted to admins) and systematically searches for API endpoints that might bypass these controls. By directly calling backend APIs with their valid JWT token, they attempt to access restricted functionality. The use of redirect URL manipulation suggests the attacker understands OAuth flows and leverages them to complete the privilege escalation.

## Defensive takeaways
- Implement role-based access control (RBAC) checks on ALL endpoints, not just UI-exposed ones; verify user permissions before processing calendar integration requests
- Validate redirect URLs against a whitelist and ensure they only redirect to pages the user has permission to access
- Use consistent authorization decorators/middleware across all endpoints to prevent developers from accidentally omitting permission checks
- Implement proper separation of concerns between authentication (who are you) and authorization (what can you do)
- Audit all OAuth/third-party integration endpoints for missing authorization checks
- Log and alert on OAuth integration attempts by users without appropriate permissions
- Require explicit admin approval for calendar integrations rather than allowing direct OAuth completion

## Variant hunting
Check other /meet-external/* endpoints for similar missing authorization checks
Search for other admin-only features (rooms, policies, settings) with backend API endpoints that might be directly callable
Test redirect URL validation on other OAuth endpoints to see if arbitrary redirect URLs are accepted
Examine whether other sensitive operations (data export, configuration changes) lack authorization checks
Check if authorization bypass is possible on related endpoints like calendar/auth/callback or calendar/sync endpoints
Test if higher-privilege operations can be performed by chaining multiple under-protected endpoints

## MITRE ATT&CK
- T1078.001
- T1548
- T1199
- T1550.001

## Notes
The vulnerability is straightforward broken access control where authorization validation is missing on a critical operation. The use of JWT tokens suggests the backend can identify the user but fails to check their permissions. The OAuth integration mechanism makes this particularly dangerous as it establishes persistent calendar access without proper privilege validation. The attack requires only HTTP-level modifications (changing the JWT token) and doesn't require exploiting complex technical flaws, making it easily reproducible.

## Full report
<details><summary>Expand</summary>

Dear Team,

Greetings!!!

I have observed an Improper access control Issue. Member users do not have permission to rooms area of the admin section. But member users can exploit this via GET /meet-external/spot-roomkeeper/v1/calendar/auth/init?successRedirectUrl=https%3A%2F%2Fadmin.8x8.vc%2F%23%2Frooms%2Fadd HTTP/2

Steps to reproduce
**Step1**: Member users do not have access to the room's area.
Use {F1625870}

**Step2**: Admin users can add their email to sync calendars from this area.
Use {F1625869}

**Step3**: From member user's JWT send a request to below endpoint
Use ██████

```
GET /meet-external/spot-roomkeeper/v1/calendar/auth/init?successRedirectUrl=https%3A%2F%2Fadmin.8x8.vc%2F%23%2Frooms%2Fadd HTTP/2
Host: admin.8x8.vc
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://admin.8x8.vc/
Content-Type: application/json
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers
Connection: close
Authorization: <Member user's JWT>
```

**Step4**: You will receive the Link as below from the above endpoint: 
```
{"url":"https://app.cronofy.com/oauth/authorize?response_type=code&client_id=M0wBDPDXk6EQLaGCqp-pTN_VGt7_AtM9&redirect_uri=https://api-vo.jitsi.net/rosy/sso/cronofy/callback&scope=read_only&delegated_scope=read_only&state=███████&avoid_linking=true"}
```

**Step5**: Now use this link and complete the OAuth sign up. (There is no validation and the application will allow you to add your email)
Use {F1625872}

**Step6**: Member user successfully added his/her email into admin's room area
Use ███

Best regards,
Emperor

## Impact

- Member users with no permission can integrate email to connect calendar

</details>

---
*Analysed by Claude on 2026-05-24*
