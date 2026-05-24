# Unauthorized Avatar Upload for Other Users via Insufficient Authorization Check

## Metadata
- **Source:** HackerOne
- **Report:** 501084 | https://hackerone.com/reports/501084
- **Submitted:** 2019-02-25
- **Reporter:** gronke
- **Program:** Rocket.Chat
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Broken Access Control, Insufficient Authorization, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Authenticated users could upload avatar images on behalf of other users by directly specifying a different userId parameter in the ufsImportURL API method. The vulnerable endpoint failed to validate that the authenticated user had authorization to modify the target user's avatar, allowing any authenticated attacker to modify any other user's profile picture.

## Attack scenario
1. Attacker authenticates to the Rocket.Chat API with their own credentials
2. Attacker crafts a ufsImportURL method call specifying a victim's userId in the parameters
3. Attacker provides a URL pointing to an image they control
4. The server processes the request without validating authorization and uploads the image to the victim's avatar store
5. The victim's avatar is replaced with attacker-controlled content on next page load
6. Attacker can use this for account impersonation, phishing, or reputational damage

## Root cause
The ufsImportURL API method in FileUpload.js did not implement authorization checks to verify that the authenticated user was either the target user or an administrator before processing avatar uploads. The userId parameter from the request was used directly without validation against the authenticated user's identity.

## Attacker mindset
An attacker would recognize that API endpoints often lack proper authorization checks, especially when parameters can be user-controlled. They would systematically test whether userId parameters in user-related endpoints could be manipulated to affect other users, discovering that avatar upload functionality had no ownership validation.

## Defensive takeaways
- Always validate that the authenticated user has explicit authorization to perform actions on behalf of other users; never trust userId parameters from requests
- Implement authorization checks at the business logic layer, not just at the endpoint routing level
- For user-specific operations, use the authenticated session's user context rather than accepting userId as a parameter
- Conduct security reviews of all API methods that accept user identifiers as parameters
- Test all endpoints with different user contexts to identify privilege escalation vulnerabilities
- Consider implementing a capability-based access control system where actions are tied to the authenticated principal

## Variant hunting
Check other file upload endpoints (avatars, documents, profiles) for similar userId parameter handling
Search for other methods accepting userId parameters that might lack authorization checks (ufsDeleteFile, ufsImportFile, etc.)
Test room-based operations for similar issues where roomId parameters might be manipulated
Check API methods for accepting user identifiers without validating the requester's relationship to that user
Review all GridFS-backed file operations for authorization gaps
Test bulk operations or administrative functions that might accept user lists for authorization bypasses

## MITRE ATT&CK
- T1190
- T1114
- T1098

## Notes
This vulnerability affects authenticated users only, limiting the attack surface to registered account holders. However, the impact is significant because any authenticated user (including low-privilege accounts) could deface other users' profiles. The fix required implementing proper authorization checks in the FileUpload.js module before processing file uploads. The vulnerability existed in the develop branch at commit 5f0180d and demonstrates the critical importance of authorization validation in multi-tenant applications.

## Full report
<details><summary>Expand</summary>

Unprivileged users were found being able to upload Avatar pictures under the behalf of other users.

Attackers authenticated to the API trigger the `ufsImportURL` method with a different `userId` than their own, so that the other users avatar is changed.

The effect of an exploit depends on the storage backend, but the default one coming with a development release, GridFS, is affected.

## Releases Affected:

  * [develop@5f0180d](https://github.com/RocketChat/Rocket.Chat/commit/5f0180dc1500b4e37b8320b39869babadb5d01cd)

## Steps To Reproduce (from initial installation to vulnerability):

(Add details for how we can reproduce the issue)

  1. Authenticate to the API
  2. Invoke `ufsImportURL` method pointing to other user
  3. Clear browser caches and reload page

## Supporting Material/References:

- see [packages/rocketchat-file-upload/server/lib/FileUpload.js#L210](https://github.com/RocketChat/Rocket.Chat/blob/dc2005b76d8f4e315ebed6e06126102148672e0e/packages/rocketchat-file-upload/server/lib/FileUpload.js#L210)

### Payload
```json
["{\"msg\":\"method\",\"method\":\"ufsImportURL\",\"params\":[\"https://radicallyopensecurity.com/images/ros-logo.gif\",{\"name\": \"ros.jpg\", \"extension\": \"jpg\", \"type\": \"text/plain\", \"userId\": \"<USER_ID>\"},\"Avatars\"],\"id\":\"15\"}"]
```

## Suggested mitigation

  * Properly authenticate Avatar uploads

## Impact

Any authenticated user can upload avatar pictures for any other user.

</details>

---
*Analysed by Claude on 2026-05-24*
