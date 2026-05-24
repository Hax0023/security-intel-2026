# CSRF on Periscope Web OAuth authorization endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 215381 | https://hackerone.com/reports/215381
- **Submitted:** 2017-03-22
- **Reporter:** filedescriptor
- **Program:** Twitter/Periscope Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Request Forgery (CSRF), OAuth 2.0 Authorization Code Flow Vulnerability, Missing CSRF Token Validation, Missing Origin/Referer Validation
- **CVEs:** None
- **Category:** web-api

## Summary
Periscope's OAuth authorization endpoint lacks CSRF protection, allowing attackers to trick authenticated users into authorizing malicious third-party applications. An attacker can forge requests to the /oauthAuthorize endpoint without any CSRF token or origin validation, gaining full API access to victim accounts including broadcast creation, publishing, and deletion.

## Attack scenario
1. Attacker identifies a legitimate Periscope developer application or registers their own with a redirect URI under their control
2. Attacker crafts a malicious webpage containing a hidden form that POSTs to https://www.periscope.tv/oauthAuthorize with their client_id and redirect_uri
3. Attacker tricks a logged-in Periscope user into visiting the malicious webpage (via phishing, social engineering, or cross-site attack)
4. The browser automatically includes the user's Periscope session cookie with the POST request, bypassing authentication checks
5. The authorization endpoint processes the request without validating CSRF tokens or origin, authorizing the attacker's application
6. The authorization code is sent to attacker's redirect_uri; attacker exchanges it for an access_token and abuses APIs to create/publish broadcasts or perform other account actions

## Root cause
The OAuth authorization endpoint implementation fails to implement standard CSRF protections: no CSRF token validation in the authorization form, no Origin/Referer header validation, and no state parameter enforcement. The endpoint trusts any POST request from an authenticated session without verifying the request origin.

## Attacker mindset
An attacker would recognize that OAuth endpoints are high-value targets for CSRF attacks since they grant persistent access tokens. By bypassing CSRF protection, they can automate account compromise at scale by injecting malicious iframes/forms into compromised websites or phishing campaigns, gaining the ability to impersonate users and perform actions on their behalf.

## Defensive takeaways
- Always implement CSRF tokens (state parameter) in OAuth 2.0 authorization endpoints and validate them before granting authorization
- Validate Origin and Referer headers on sensitive requests; reject requests from unexpected origins
- Use the OAuth 2.0 state parameter to bind authorization requests to user sessions and prevent cross-site attacks
- Implement SameSite cookie attributes on session cookies to prevent automatic inclusion in cross-site requests
- Require explicit user re-authentication or additional confirmation for sensitive OAuth authorization flows
- Log and monitor authorization requests for anomalies (unusual client_ids, redirect_uris, user agents)
- Provide users with visibility into authorized applications and easy revocation mechanisms

## Variant hunting
Check other OAuth endpoints on periscope.tv for similar CSRF vulnerabilities (token endpoint, revocation endpoint)
Test other Twitter/Periscope products (TweetDeck, Moments) for OAuth CSRF vulnerabilities
Examine whether the vulnerability extends to account linking features in other OAuth integrations
Search for timing-based CSRF protection bypasses (checking if tokens expire or rotate)
Test for POST-based CSRF on other account-sensitive operations (password change, email change, API key generation)
Investigate if the state parameter is properly validated end-to-end in the complete OAuth flow

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1598 - Phishing - Web Phishing
- T1187 - Forced Authentication
- T1550.001 - Use Alternate Authentication Material - Application Access Token

## Notes
This is a classic OAuth CSRF vulnerability that violates RFC 6749 best practices. The reporter demonstrated a working PoC that achieved account takeover by creating and publishing broadcasts. The vulnerability is particularly severe because OAuth grants persistent access tokens, allowing long-term account abuse even if the initial CSRF is detected. The lack of public API documentation made the full impact unclear to the reporter, but the ability to create/publish broadcasts demonstrates substantial unauthorized access. Twitter likely awarded bounty despite non-disclosure of amount. This vulnerability class remains common in OAuth implementations.

## Full report
<details><summary>Expand</summary>

Hi,
I would like to report an issue in the OAuth authorization endpoint on Periscope Web. This allows a malicious 3rd party application to gain full API access to a victim's Periscope account.

#Details
Periscope has developer APIs that allow a 3rd party application to access resources on behalf of a user. The authorizion page is like this https://www.periscope.tv/oauth?client_id=█████████&redirect_uri=https://getmevo.com/oauth/periscope

It was found that the authorize endpoint does not have any protection against CSRF. The request to authorize a 3rd party application to access one's Periscope account is as follows:
```http
POST https://www.periscope.tv/oauthAuthorize HTTP/1.1
Host: www.periscope.tv
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Cookie: sid=[...]

client_id=████&redirect_uri=https%3A%2F%2Fgetmevo.com%2Foauth%2Fperiscope?abc
```
As one can see, there is no CSRF token or Origin validation.

After a 3rd party application gets the *authorization code* from *redirect_uri*, it can then exchange it for an access token.

#Impact
Since the Developer APIs are not public, I have no information what the APIs can perform. Based on the the description on the authorization page however, it looks intimidating that it has **full access** to an account.
{F170579}
At minimum, I found endpoints that allow creating a broadcast (https://public-api.periscope.tv/v1/broadcast/create), tweeting it (https://public-api.periscope.tv/v1/broadcast/publish) and deleting a broadcast (https://public-api.periscope.tv/v1/broadcast/delete).

#PoC
1. Make sure you are logged into Periscope Web (https://periscope.tv)
2. Go to http://innerht.ml/pocs/periscope-oauth-csrf/
3. You will be redirected to something like https://getmevo.com/oauth/periscope?code=abcde&state=, copy the *code* value in the parameter
4. Go to http://innerht.ml/pocs/periscope-oauth-csrf/code.php?code=abcde and replace the above code in the parameter
5. A tweet will be posted in your timeline with a broadcast

The behind the scene is:
1. Exchange *code* for *access_token* (https://public-api.periscope.tv/v1/oauth/token)
2. Create a broadcast (https://public-api.periscope.tv/v1/broadcast/create)
3. Publish it (https://public-api.periscope.tv/v1/broadcast/publish)

Note that a real attack does not require user interaction. In this PoC the manual copying of *code* is because I don't have a 3rd party Periscope application. 

#Fix
Add CSRF protection

</details>

---
*Analysed by Claude on 2026-05-24*
