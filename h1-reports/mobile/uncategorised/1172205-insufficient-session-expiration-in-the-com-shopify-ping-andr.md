# Insufficient Session Expiration in com.shopify.ping Android App - Authentication Token Not Invalidated on Logout

## Metadata
- **Source:** HackerOne
- **Report:** 1172205 | https://hackerone.com/reports/1172205
- **Submitted:** 2021-04-22
- **Reporter:** fr4via
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insufficient Session Expiration, Broken Authentication, Token Management Flaw, Improper Session Invalidation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The com.shopify.ping Android application fails to invalidate authentication tokens when users perform logout actions. Despite sending a logout request, the server rejects it with a 'Missing Logout Token Hint' error, leaving the access token valid for subsequent API calls. This allows attackers who obtain the token to maintain unauthorized access to user accounts.

## Attack scenario
1. Attacker installs com.shopify.ping application and captures network traffic during a legitimate user's logout sequence
2. Attacker observes that the DELETE /api/v1/logout request fails with 'Missing Logout Token Hint' error response
3. Attacker verifies that the Bearer token remains valid by sending a GET request to /oauth/userinfo endpoint
4. Attacker extracts the access token from application storage, network cache, or through other means (device compromise, backup extraction)
5. Attacker uses the valid token to impersonate the user and access protected resources via API calls with the token
6. Attacker maintains persistence and unauthorized access until token naturally expires (if timeout exists) or is manually revoked through other means

## Root cause
The server-side logout endpoint implements incomplete token invalidation logic, rejecting logout requests due to missing 'Logout Token Hint' parameter rather than gracefully handling the revocation. The application appears to send logout request without required parameters, and the backend fails to invalidate the token when logout cannot be properly completed. Additionally, the token lacks proper short expiration times and the application may cache tokens insecurely.

## Attacker mindset
An attacker would recognize that leaked or extracted authentication tokens remain usable after logout, providing persistent unauthorized access. This is particularly valuable if the victim is unaware their session remains active. The attacker could extract tokens from app storage, backups, or network traffic, then use them for account takeover, data exfiltration, or privilege escalation within Shopify accounts.

## Defensive takeaways
- Implement mandatory token invalidation on logout with proper error handling - reject requests if preconditions aren't met rather than silently failing
- Ensure logout endpoint correctly implements OAuth 2.0 token revocation specification (RFC 7009) with all required parameters validated
- Use short-lived access tokens (15-60 minutes) with refresh token rotation to limit window of exposure
- Implement server-side session tracking independent of client-provided tokens to enforce logout
- Clear all cached tokens and sensitive data from application memory and storage upon logout
- Implement token binding to device/application instance to prevent token reuse on different devices
- Add rate limiting and anomaly detection for token reuse after logout events
- Log all token invalidation attempts and failures for security auditing
- Validate Logout Token Hint parameter existence before processing logout to prevent parameter tampering

## Variant hunting
Check other Shopify applications (web, iOS, other Android apps) for identical logout token invalidation flaws
Review similar OAuth 2.0 implementations for missing Logout Token Hint validation across endpoints
Examine token refresh endpoint for similar parameter validation issues
Test other session termination triggers (password change, account deletion, permission revocation) to verify proper token invalidation
Check if /oauth/userinfo or other endpoints can be rate-limited to force token expiration through algorithmic means
Verify if refresh tokens (if used) are also invalidated on logout
Test whether logout succeeds with alternate parameter formats or missing headers

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1550 - Use Alternate Authentication Material
- T1550.001 - Use Alternate Authentication Material: Application Access Token
- T1563 - Steal Web Session Cookie
- T1555 - Credentials from Password Stores
- T1528 - Steal Application Access Token

## Notes
This vulnerability demonstrates a critical gap between client logout action and server-side token revocation. The 'Missing Logout Token Hint' error indicates improper OAuth 2.0 implementation where the server expects additional parameters not being sent by the client. This is a configuration/implementation mismatch that should be immediately fixed. The impact is elevated because Shopify accounts likely contain sensitive business and payment information, making unauthorized access particularly dangerous.

## Full report
<details><summary>Expand</summary>

It was identified that despite a logout action will be taken by the user at the com.shopify.ping application, the authentication token is not invalidated which allows fully recovery of the initially acquired session. More specifically, after the user provides the required credentials, an **access_token** will be fetched from the server at accounts.shopify.com/oauth/token. After establishing a session and by selecting logout from the corresponding control, the application will send the following DELETE request:

```
DELETE /api/v1/logout HTTP/1.1
authorization: Bearer atkn_**********************************
Host: accounts.shopify.com
Connection: close
Cookie: __cfduid=***********; _y=***************; _shopify_y=***************; request_method=POST
User-Agent: okhttp/3.12.12
```

The server will reply as follows:

```
{"error":"Missing Logout Token Hint"}
```
And will cancel the invalidation process, as the token will still be valid on a subsequent request (e.g.):

```
GET /oauth/userinfo HTTP/1.1
Accept-Encoding: gzip, deflate
authorization: Bearer ***************
....
```
REPLY:
```
{"sub":"...","email":".....@gmail.com","email_verified":true,"family_name":"Doe","given_name":"....","locale":"en","name":".... ...","nickname":".....","updated_at":.....,"zoneinfo":"....","tfa_enabled":false}
```

## Impact

An application should always revoke an access token by the time that the end user choses to Log Off from a session. Keeping a token active, while the user is not aware of it imposes a big risk, since by the time that an unauthorised entity fetches it, may recover a fully "functional" session.

</details>

---
*Analysed by Claude on 2026-05-24*
