# Private Grab Messages Accessible and Cached by Search Engines via Auth Token in URL

## Metadata
- **Source:** HackerOne
- **Report:** 221558 | https://hackerone.com/reports/221558
- **Submitted:** 2017-04-17
- **Reporter:** sp1d3rs
- **Program:** Grab
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Information Disclosure, Improper Access Control, Sensitive Data Exposure, Search Engine Indexing of Sensitive Content, Authentication Token Leakage, Insufficient Access Restrictions
- **CVEs:** None
- **Category:** uncategorised

## Summary
Authentication tokens containing sensitive user information (OTP pins, group invites, private messages) are exposed in GET request query parameters to an endpoint that allows search engine indexing. Attackers can discover and access other users' private messages through search engine caches or by directly accessing URLs with leaked tokens.

## Attack scenario
1. Attacker discovers that grab-attention.grabtaxi.com allows search engine crawling via robots.txt or lack of meta tags
2. Attacker performs Google dorking search (e.g., 'passenger site:grab-attention.grabtaxi.com') to discover indexed pages
3. Search engine cache reveals auth_token values in URL parameters from previously accessed private message pages
4. Attacker extracts valid auth_token from cached search results or Google cache
5. Attacker crafts URL with stolen token and accesses victim's private messages, OTP codes, and group invitations
6. Due to long token validity period, attacker maintains access to multiple user accounts and sensitive communications

## Root cause
Multiple security failures combined: (1) Auth tokens passed as GET query parameters instead of secure POST/header transmission, (2) Sensitive endpoint not excluded from search engine indexing, (3) Missing robots.txt or noindex directives, (4) No additional authorization checks beyond token validation, (5) Potentially long token expiration times

## Attacker mindset
An attacker would recognize that search engines are powerful reconnaissance tools for finding exposed credentials and sensitive data. By leveraging public search engine caches, they can discover URLs containing auth tokens without needing to breach the application directly. This is a low-effort, high-impact attack requiring only basic OSINT skills and search engine dorking knowledge.

## Defensive takeaways
- Never transmit authentication credentials in URL query parameters; use POST body, headers (Authorization), or secure cookies with HTTPOnly flag
- Implement robots.txt with Disallow rules and add X-Robots-Tag: noindex headers on all endpoints containing sensitive user data
- Use POST or PUT methods instead of GET for operations accessing private user information
- Implement time-limited, single-use, or short-lived authentication tokens
- Add rate limiting and anomaly detection to identify token abuse patterns
- Enforce additional authorization checks beyond token validation (e.g., user ID matching)
- Regularly audit search engine indices for sensitive content exposure
- Implement Content-Security-Policy and other security headers to prevent token leakage
- Conduct security reviews of all endpoints handling personally identifiable or sensitive information

## Variant hunting
Search for other Grab domains with similar messaging functionality that may have same vulnerability
Test if other user-specific endpoints use query parameter auth tokens (notifications, settings, account info)
Check if auth_token appears in HTTP referrer headers when redirecting from cached pages
Investigate if tokens are cached in browser history, logs, or proxies
Test for token reuse across different endpoints or API versions
Search Google cache for other endpoints from grab-attention.grabtaxi.com containing credentials
Check if similar patterns exist on other Grab services (driver app, payments, support portal)

## MITRE ATT&CK
- T1190
- T1592
- T1526
- T1621
- T1555
- T1087
- T1056
- T1041

## Notes
This report demonstrates a real-world intersection of web security, search engine visibility, and credential management. The vulnerability is particularly severe because: (1) it affects authentication tokens visible in plain text, (2) search engines provide public disclosure without active exploitation, (3) the affected data includes OTP codes and group invitations that could enable account takeover, and (4) multiple users are exposed simultaneously. The reporter provided excellent remediation guidance including both short-term (disable indexing) and long-term (use POST) fixes. This is a textbook example of why sensitive operations must never use GET parameters and why organizations must actively manage what search engines index.

## Full report
<details><summary>Expand</summary>

##Description
Hello. Today i discovered, that Search Engines can access the private users messages (OTP pins, Group invites information etc.)
It happens because the `https://grab-attention.grabtaxi.com` host allows search indexing, and can leak the auth_token to the Search Engines which also can lead to privilege escalation.
When vieving "Notifications" section on the app, i noticed the unsecure GET request to the `https://grab-attention.grabtaxi.com/passenger/passenger.html?auth_token=[my_token]&view=268435456`. I was surprised, when tried to repeat it in the browser - it gave me access to my messages.

##POC
{F176465}
{F176466}

## Steps To Reproduce:
1. Cheking the private messages of other user (me):
https://grab-attention.grabtaxi.com/passenger/passenger.html?auth_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJQQVNTRU5HRVIiLCJleHAiOjQ2NDUyMzk1NDUsImlhdCI6MTQ5MTYzOTU0NSwianRpIjoiZWI0YmFiMjUtYzA2Yi00MGIzLWJiZTctMzZkYzFmMWRkZTMyIiwibG1lIjoiU1lTVEVNIiwibmFtZSI6IiIsInN1YiI6IjM2NWE0NjY0LTY1MGEtNDBjZC05YWU2LTQ4YWQwN2Q2NGY2OSJ9.eTX2dWnooTxm50Dv1VYoIZanOqCe073_AmVk97VE4p7m4e26mcWtnZzQz5IR1EwuWbs52qJLzzAIZ5KcpWoKCvadu6zuRQzy2xRk8BcFDUXGl8w8doPJbuSIHMY0K-x8Q-█████████ZTdgxLI&view=268435456#/
2. Checking that search engines can crawl it:
Use this Google DORK (search text):
`passenger site:grab-attention.grabtaxi.com`
and press Search.
You will see this cached page with auth_token (actually it was cutted due to big query length) - but it is still a huge information disclosure.


## Suggested fix
1. Disable Search indexing on `https://grab-attention.grabtaxi.com`
2. For the better security you can change the request method to the `https://grab-attention.grabtaxi.com/passenger/passenger.html` endpoint from GET to POST (or encrypt it) due to that fact that auth_token are leaked in the query parameters.


</details>

---
*Analysed by Claude on 2026-05-24*
