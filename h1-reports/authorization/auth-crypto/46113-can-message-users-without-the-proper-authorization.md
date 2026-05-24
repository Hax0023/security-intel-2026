# Can message users without the proper authorization

## Metadata
- **Source:** HackerOne
- **Report:** 46113 | https://hackerone.com/reports/46113
- **Submitted:** 2015-02-02
- **Reporter:** jkjkjk
- **Program:** Vimeo
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Authorization Bypass, Missing Access Control, Business Logic Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Vimeo messaging endpoint fails to enforce server-side authorization checks that should restrict private message sending to users who are following the recipient. An attacker can bypass the client-side restriction by sending a direct POST request to the /messages endpoint with any target user ID, allowing them to message arbitrary users without following them.

## Attack scenario
1. Attacker identifies the /messages endpoint structure through normal use or reverse engineering
2. Attacker crafts a POST request with malicious payload including an arbitrary target user ID and message content
3. Attacker submits the request with valid session cookies but bypassing the client-side follow requirement check
4. Server processes the request without validating whether the sender is actually following the recipient
5. Message is delivered to the target user despite not meeting the business logic requirement
6. Attacker can now spam or harass any user on the platform without follower constraints

## Root cause
Missing server-side authorization validation. The application enforces the 'must be following' rule only on the client side (frontend), but the backend /messages endpoint does not verify this business logic constraint before processing message submissions.

## Attacker mindset
Low-skilled attacker with basic HTTP knowledge can exploit this. The vulnerability is trivial to discover and exploit - simply intercept a legitimate message request, modify the user ID parameter, and resend. No sophisticated techniques required.

## Defensive takeaways
- Always enforce authorization rules on the server side; never rely on client-side validation alone
- Validate all business logic constraints at the API endpoint before processing requests
- Implement proper access control checks that verify the relationship between sender and recipient before allowing message transmission
- Audit all user-to-user communication endpoints for similar authorization bypass issues
- Use allowlist validation for user ID parameters rather than accepting arbitrary IDs
- Log suspicious messaging patterns (messages to non-followed users) for detection and analysis

## Variant hunting
Check other communication endpoints: notifications, comments, mentions
Test group messaging or broadcast features for similar bypasses
Verify if other user-relationship-dependent features (like profile viewing restrictions) have similar issues
Test if other actions requiring 'following' status can be bypassed (following, un-following, blocking)
Check for similar authorization bypasses in media sharing or collaboration features

## MITRE ATT&CK
- T1190
- T1566

## Notes
This is a classic example of authorization bypass due to client-side enforcement. The fix is straightforward but highlights a common vulnerability pattern. The POST request structure and parameter names are exposed in the report, making reproduction trivial. This type of vulnerability is particularly dangerous in social platforms as it enables spam, harassment, and phishing campaigns.

## Full report
<details><summary>Expand</summary>

It shouldn't be possible to send messages to users without following users:

> You must be following at least one Vimeo member before you can send a private message. To get started, find a friend, family member, or someone with cool videos and click the "Follow" button on their profile page. 

It's possible to bypass that by just sending a POST request to `/messages`:

```
POST /messages HTTP/1.1
Host: vimeo.com
User-Agent: [CENSORED]
Accept: text/html, application/xml, text/xml, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Requested-With: XMLHttpRequest
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Referer: https://vimeo.com/messages
Content-Length: 141
Cookie: [CENSORED]
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache

name=Jens>&text=blaat&action=send_message&lightbox=true&user=[ANY USER ID HERE]&token=[CENSORED]
```

You can replace the `user` parameter with any random user ID and it will send the message without any issues.

**Fix:**
Add proper server side authorization on the `/messages` endpoint.

</details>

---
*Analysed by Claude on 2026-05-24*
