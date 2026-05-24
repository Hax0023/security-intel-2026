# Open Redirection via OAuth Callback Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 12949 | https://hackerone.com/reports/12949
- **Submitted:** 2014-05-23
- **Reporter:** atom
- **Program:** Urban Dictionary
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Open Redirection, OAuth Misconfiguration, Post-Authentication Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
The OAuth authentication endpoint accepts an attacker-controlled 'origin' parameter that redirects users to arbitrary domains after successful authentication. An attacker can craft a malicious link redirecting authenticated users to a phishing site, potentially capturing authentication tokens or sensitive information during the redirect.

## Attack scenario
1. Attacker crafts malicious URL with origin parameter pointing to attacker-controlled phishing domain
2. Attacker sends link via phishing email/social engineering to Urban Dictionary users
3. Victim clicks link and authenticates with Facebook through legitimate Urban Dictionary OAuth flow
4. Upon successful authentication, victim is redirected to attacker's phishing domain
5. Attacker's site mimics Urban Dictionary or captures auth tokens from referrer headers/browser state
6. Attacker gains access to victim's account or authentication credentials

## Root cause
The application fails to validate or whitelist the 'origin' redirect parameter against a list of trusted domains. The parameter is passed directly to the HTTP redirect without proper sanitization, allowing any URL to be specified.

## Attacker mindset
Attacker recognizes that post-authentication redirects are trusted by users and can be abused for credential theft or token capture. By chaining with OAuth flows, the attacker leverages legitimate authentication to establish trust before redirecting to malicious infrastructure.

## Defensive takeaways
- Implement strict whitelist of allowed redirect URIs for OAuth callbacks
- Validate redirect parameters against hardcoded list of trusted domains only
- Use relative URLs or domain-relative redirects instead of absolute URLs when possible
- Never trust user-supplied redirect parameters; pre-register all valid redirect URIs
- Log and monitor unusual redirect patterns for suspicious activity
- Implement Content-Security-Policy headers to restrict navigation
- Use state parameter validation in OAuth flows to prevent token interception

## Variant hunting
Check other OAuth authentication endpoints (Google, GitHub, Twitter logins) for similar parameter handling
Test URL encoding bypass techniques on the origin parameter (double encoding, case variation)
Search for other redirect parameters: returnUrl, return, redirect_uri, callback, next, url
Test parameter pollution with multiple origin values
Check for open redirects in logout/sign-out endpoints
Test protocol handling: javascript://, data://, //attacker.com

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1187 - Forced Authentication
- T1539 - Steal Web Session Cookie
- T1111 - Multi-Factor Authentication Interception

## Notes
This vulnerability is particularly dangerous in OAuth contexts as users trust the legitimate authentication flow. The attacker doesn't need to intercept HTTPS traffic; they merely need to redirect after auth completes. Modern browsers expose referrer headers during redirects, potentially leaking tokens. The fix is straightforward: implement a strict whitelist rather than blacklist approach for redirect validation.

## Full report
<details><summary>Expand</summary>

Try to connect your facebook using this URL

http://www.urbandictionary.com/auth/facebook?origin=http://google.com

after connecting urbandictionary to FB you will be redirected to google.com

and that is bad because hackers can get the auth token

</details>

---
*Analysed by Claude on 2026-05-24*
