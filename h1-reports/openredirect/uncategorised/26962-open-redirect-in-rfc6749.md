# Open Redirect in RFC6749 OAuth Authorization Flow

## Metadata
- **Source:** HackerOne
- **Report:** 26962 | https://hackerone.com/reports/26962
- **Submitted:** 2014-09-04
- **Reporter:** asanso
- **Program:** HackerOne (Generic OAuth Provider Report)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Open Redirect, OAuth Implementation Flaw, Specification Interpretation Issue
- **CVEs:** None
- **Category:** uncategorised

## Summary
OAuth providers strictly implementing RFC6749 are vulnerable to open redirects when authorization requests contain invalid parameters (e.g., wrong scope). The specification allows redirecting users back to the registered redirect_uri even for parameter validation failures, which an attacker can exploit by registering a malicious redirect_uri and crafting requests with invalid parameters to redirect victims to attacker-controlled sites.

## Attack scenario
1. Attacker registers a new OAuth client application with a victim OAuth provider (victim.com)
2. Attacker registers their own domain (attacker.com) as the authorized redirect_uri during client registration
3. Attacker crafts a malicious authorization URL with intentionally invalid parameters (e.g., wrong scope) while keeping client_id and redirect_uri pointing to attacker.com
4. Attacker sends this URL to victim users via phishing, social engineering, or embeds it in a web page
5. When victim clicks the link, the OAuth provider validates parameters, finds the scope invalid, but following RFC6749 redirects the user to attacker.com with error parameters
6. Attacker receives the redirect with error information and can perform credential harvesting, malware distribution, or credential theft

## Root cause
RFC6749 Section 4.1.2.1 specifies that authorization servers must not redirect to invalid redirect URIs for missing/invalid client identifiers, but allows redirection for other parameter failures (invalid scope, etc.). This creates ambiguity where providers redirect users to attacker-registered redirect_uris when non-critical parameters fail validation, enabling open redirect attacks.

## Attacker mindset
An attacker registers a legitimate OAuth application with a malicious redirect_uri, then exploits the specification's parameter validation behavior to create an open redirector. The attacker recognizes that RFC6749 implementations allow redirects for invalid scopes/parameters while blocking redirects only for invalid client IDs or redirect_uris, creating a bypassing opportunity for registered applications.

## Defensive takeaways
- Implement stricter validation: return HTTP 400 errors for all invalid parameters rather than redirecting to redirect_uri on parameter validation failures
- Require explicit user consent on the authorization screen for every authorization request, regardless of parameter validity, before any redirect occurs
- Validate all request parameters before performing any redirect operation
- Consider implementing a confirmation page that shows users the redirect destination before redirecting on errors
- Maintain a whitelist of valid scopes and reject requests with invalid scopes without performing redirects
- Add rate limiting and monitoring on authorization endpoints to detect abuse patterns
- Request specification clarification from IETF OAuth working group and update implementation guidance

## Variant hunting
Test other OAuth parameter validation failures (invalid response_type, invalid state parameter handling)
Check if PKCE parameter validation failures trigger open redirects
Examine custom OAuth parameters and how their validation failures are handled
Test with different registered redirect_uri schemes (javascript:, data:, custom protocols)
Analyze behavior when redirect_uri is partially valid or matches a subdomain pattern
Test interaction between invalid parameters and pre-approved consent flows
Investigate OpenID Connect extensions and their parameter validation redirect behavior

## MITRE ATT&CK
- T1598
- T1598.003
- T1566.002

## Notes
This is a specification interpretation issue actively discussed within the IETF OAuth mailing list. The vulnerability exists at the intersection of compliance with RFC6749 and security best practices. Multiple OAuth providers likely affected. The reporter correctly identifies this as a systematic issue requiring specification updates rather than individual provider fixes. This demonstrates the importance of security review during standards development and the gap between RFC letter and security intent.

## Full report
<details><summary>Expand</summary>

OAuth Providers (servers) that strictly follow rfc6749 are vulnerable to open redirect.
Let me explain, reading [0]

If the request fails due to a missing, invalid, or mismatching
   redirection URI, or if the client identifier is missing or invalid,
   the authorization server SHOULD inform the resource owner of the
   error and MUST NOT automatically redirect the user-agent to the
   invalid redirection URI.

   If the resource owner denies the access request or if the request
   fails for reasons other than a missing or invalid redirection URI,
   the authorization server informs the client by adding the following
   parameters to the query component of the redirection URI using the
   "application/x-www-form-urlencoded" format, per Appendix B:

Now let’s assume this.
I am registering a new client to the victim.com provider. 
I register redirect uri attacker.com.

According to [0] if I pass e.g. the wrong scope I am redirected back to attacker.com.
Namely I prepare a url that is in this form:

http://victim.com/authorize?response_type=code&client_id=bc88FitX1298KPj2WS259BBMa9_KCfL3&scope=WRONG_SCOPE&redirect_uri=http://attacker.com

and this is works as an open redirector.
Of course in the positive case if all the parameters are fine this doesn’t apply since the resource owner MUST approve the app via the consent screen (at least once).

I have notified also this issue to the OAuth mailing list.

See also http://www.ietf.org/mail-archive/web/oauth/current/msg13367.html
and http://www.ietf.org/mail-archive/web/oauth/current/maillist.html.
The consensus seems to be that some of the OAuth family spec should be updated... (currently under discussion)

A solution would be to return error 400 rather than redirect to the redirect URI or always show the consent screen (at least once until the app is accepted by the user) even in case of wrong parameter rather than redirect...

[0] https://tools.ietf.org/html/rfc6749#section-4.1.2.1


</details>

---
*Analysed by Claude on 2026-05-24*
