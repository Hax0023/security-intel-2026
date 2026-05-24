# Stealing SSO Login Tokens via CSRF, XSS, and Token Reuse in snappublisher.snapchat.com

## Metadata
- **Source:** HackerOne
- **Report:** 265943 | https://hackerone.com/reports/265943
- **Submitted:** 2017-09-05
- **Reporter:** coolboss
- **Program:** Snapchat Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Cross-Site Request Forgery (CSRF), Cross-Site Scripting (XSS), Insecure Redirect/Open Redirect, Broken Authentication, Insecure Token Management, Insufficient Input Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can steal SSO login tokens for snappublisher.snapchat.com by chaining multiple vulnerabilities: CSRF to log victims into attacker-controlled accounts, XSS via SVG upload, open redirect via unvalidated referrer parameter, and token reuse. This allows complete account takeover with persistent token access.

## Attack scenario
1. Victim is logged into accounts.snapchat.com and visits attacker-controlled website containing CSRF payload
2. CSRF attack logs victim into attacker's snappublisher.snapchat.com account
3. Attacker crafts malicious SSO URL with SVG file URL containing XSS payload as referrer parameter with hash fragment
4. Victim unknowingly triggers SSO token fetch via phishing/CSRF which redirects to attacker's SVG file with token in URL hash
5. SVG file executes JavaScript code that exfiltrates the SSO login token from hash fragment to attacker
6. Attacker reuses stolen token multiple times via sso_continue endpoint to hijack victim's snappublisher account and access APIs

## Root cause
Multiple chained security flaws: (1) Lack of CSRF protection on SSO endpoints via missing state parameter; (2) Overly permissive referrer parameter validation allowing any snappublisher.snapchat.com URL with hash fragments; (3) SVG file upload functionality permitting XSS execution; (4) URL hash fragments passed through 307 redirects to third-party storage; (5) SSO tokens lacking expiration and one-time-use enforcement; (6) Insufficient validation of redirect targets in OAuth/SSO flow.

## Attacker mindset
Attacker systematically identified and chained multiple security boundaries: authentication mechanism (SSO), file upload capability (SVG XSS), parameter validation (referrer), and token management (reuse). Demonstrates sophisticated understanding of OAuth/SSO flows, browser behavior with URL fragments across redirects, CSRF mechanics, and XSS via SVG files. Attack is highly reproducible and affects all logged-in users.

## Defensive takeaways
- Implement CSRF protection via state parameter on all SSO endpoints, especially token issuance and consumption flows
- Strictly validate and whitelist redirect/referrer URIs; explicitly reject URLs containing hash fragments or query parameters that could be exploited
- Enforce one-time-use tokens with immediate expiration after consumption; implement token binding to prevent reuse
- Disable inline script execution in SVG files or serve user-uploaded media with Content-Security-Policy headers preventing script execution
- Use POST requests for sensitive operations instead of GET to prevent URL fragment leakage in referrer headers
- Implement SameSite cookie attributes and ensure session tokens are httpOnly to prevent XSS exfiltration
- Add rate limiting and suspicious activity detection on SSO token endpoints
- Implement security headers (CSP, X-Frame-Options, X-Content-Type-Options) on media serving endpoints

## Variant hunting
Test other OAuth/SSO client_ids for similar referrer validation bypasses and hash fragment handling
Check if other Snapchat products (Ads Manager, Business Manager) share the same SSO infrastructure and vulnerabilities
Investigate file upload mechanisms in other Snapchat services for XSS via SVG, XML, or other formats
Search for token reuse vulnerabilities in other authentication tokens (API keys, refresh tokens, session tokens)
Test for CSRF protection gaps in other account-level operations beyond SSO login
Analyze redirect chain behavior across different HTTP status codes (301, 302, 307, 308) with hash fragments
Review Google Cloud Storage integration for bucket policy misconfigurations allowing attacker control
Examine whether tickets/tokens appear in browser logs, server logs, or analytics that could leak tokens

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (SVG XSS, SSO redirect)
- T1566 - Phishing (CSRF payload delivery)
- T1187 - Forced Authentication (CSRF login attack)
- T1056 - Input Capture (Token exfiltration via XSS)
- T1539 - Steal Web Session Cookie (SSO token hijacking)
- T1550 - Use Alternate Authentication Material (Stolen SSO token reuse)
- T1199 - Trusted Relationship (Exploiting SSO trust boundary)
- T1021 - Remote Services (Using stolen token for unauthorized API access)

## Notes
This is a sophisticated multi-stage attack demonstrating the danger of chained vulnerabilities in authentication systems. The reporter clearly understood OAuth/SSO attack vectors and browser security boundaries. The lack of token expiration is particularly severe as it enables persistent account compromise. Snapchat's recommendations align with OAuth 2.0 security best practices. The report demonstrates why file upload functionality near authentication boundaries requires extreme scrutiny. Video PoC provided but redacted in this analysis.

## Full report
<details><summary>Expand</summary>

# Description
Attacker can steal SSO login tokens for snappublisher.snapchat.com by chaining different flaws in SSO and Snapchat’s Snappublisher tool. Detailed attack flow is as follows.

# Attack Flow
1.. Snapchat fetches a `SSO LOGIN TOKEN` from `accounts.snapchat.com` to login into different products of Snapchat i.e. SnapPublisher, Ads Manager, Business Manager, etc. provided that user is logged into `accounts.snapchat.com`.
eg. To login into SnapPublisher following requests are made …
1] https://accounts.snapchat.com/accounts/login?client_id=creativesuite-prod&referrer=https://snappublisher.snapchat.com/sso_continue
2] 302 redirect to
https://accounts.snapchat.com/accounts/sso?client_id=creativesuite-prod&referrer=https%3A%2F%2Fsnappublisher.snapchat.com%2Fsso_continue
3] again 302 redirect to 
https://snappublisher.snapchat.com/sso_continue?ticket=redacted

So, a SSO login token `ticket` is sent from `accounts.snapchat.com` to `snappublisher.snapchat.com` which is used to login the user. And is also used in `Authorization header` when making requests to API.

Now, we are going to steal this SSO login token `ticket` which will allow us to login and control victim’s account.

2.. On `snappublisher.snapchat.com`, I was able to upload a `svg` image to google cloud storage, using which I run my javascript code.
Note: Use `import from site` functionality via `https://snappublisher.snapchat.com/snaps/create/new` and import my `xss-svg` image from here (███████/tokenstealer.svg). This alerts and logs `#hashfragment` in the console. 
I have already did this in my POC so this is just for understanding purpose. My image URL is `https://snappublisher.snapchat.com/api/v1/media/████████/file/somthine.svg?%23pranav`

3.. Now, other flaws in SSO …
1] In this URL 
`https://accounts.snapchat.com/accounts/sso?client_id=creativesuite-prod&referrer=https://snappublisher.snapchat.com/api/v1/media/████████/file/somthine.svg?%23pranav`

`referrer` parameter can be controlled and any `snappublisher.snapchat.com` URL is allowed.
Also, `%23pranav`, this `#hashfragment` is allowed in `referrer ` parameter. 

I take advantage of both these flaws to flow the `SSO login token` to my website or land to a page which I control.
Note: `#hashfragment` is send further by browser for `302` / `307` redirects.


4.. CSRF Login flaw
SSO functionality is vulnerable to CSRF attack so I can login other people into my account. I use this functionality to login user into my account.

5.. Token doesn’t expire flaw 
Once the SSO login token is used, it doesn’t expire and can be reused multiple times.

So, simple attack flow is as follows :
1. User is logged into `accounts.snapchat.com`.
2. Attacker logs user into his/her `snappublisher.snapchat.com` account via CSRF login flaw.
3. Now, attacker makes a request to fetch SSO login token `https://accounts.snapchat.com/accounts/sso?client_id=creativesuite-prod&referrer=https://snappublisher.snapchat.com/api/v1/media/█████████/file/somthine.svg?%23pranav` and redirects the token in `#hashfragment` to `https://snappublisher.snapchat.com/api/v1/media/█████/file/somthine.svg?%23pranav`
4. `https://snappublisher.snapchat.com/api/v1/media/████/file/somthine.svg?%23pranav` this redirects with `307` status code to `storage.googleapis.com/creativesuite-prod-media/*` with `SSO login token ticket` in  `#hashfragment` carried forward by browser.
5. Svg image executes my js code and alerts and logs the `SSO login token ticket` in the console.
6. I can use the `ticket` to login into victim’s account. Via `https://snappublisher.snapchat.com/sso_continue?ticket=<stolen token>`

# Proof Of Concept

Video POC : █████████(Unlisted video on youtube)

1. Login into your account on `accounts.snapchat.com`.
2. Login into your SnapPublisher account `snappublisher.snapchat.com`.
3. Visit (█████) which fetches `user’s SSO login token` which can be used to login. (This alerts and logs the `token` in console.)
4. Use the token via `https://snappublisher.snapchat.com/sso_continue?ticket=<stolen token>`


# Impact 
1. Gain unauthorized access to Snappublisher account.
2. Can use the SSO login token to make API requests.

# Recommendations

1. For SSO functionality …
1] Add `state` param to prevent `CSRF login` on `https://snappublisher.snapchat.com/sso_continue?ticket=<token>` 
2] In `referrer` param of the following URL 
`https://accounts.snapchat.com/accounts/sso?client_id=creativesuite-prod&referrer=https://snappublisher.snapchat.com/api/v1/media/██████████/file/somthine.svg?%23pranav` disallow `#hashfragments` to be included.
3] Make the `referrer` param of the following URL 
`https://accounts.snapchat.com/accounts/sso?client_id=creativesuite-prod&referrer=https://snappublisher.snapchat.com/api/v1/media/███████/file/somthine.svg?%23pranav` more specific and restricted similar to your OAuth2 adsapi.
4] SSO login token should be one time use and should not be able to use it again and again.

2. For SnapPublisher
1] I observed you are using Google Cloud Storage, so blocking `svg` images or disallowing any uploads of `svg-xss` images will further enhance security. Otherwise, one can easily get `xss` on `storage.google`


Let me know if you need any help. :-)

Regards,
Pranav Hivarekar


</details>

---
*Analysed by Claude on 2026-05-24*
