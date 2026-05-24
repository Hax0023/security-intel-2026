# Unsafe CORS Sharing of Admin Users via WordPress REST API

## Metadata
- **Source:** HackerOne
- **Report:** 772744 | https://hackerone.com/reports/772744
- **Submitted:** 2020-01-12
- **Reporter:** pwrspl0it
- **Program:** Lone Star Cell (HackerOne #772744)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Cross-Origin Resource Sharing (CORS) Misconfiguration, Sensitive Information Disclosure, Broken Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
The WordPress REST API endpoint /wp-json/wp/v2/users/ exposes a list of admin usernames due to overly permissive CORS headers that allow cross-origin requests to retrieve sensitive user information. An attacker can craft a malicious webpage that, when visited by a logged-in user, exfiltrates admin usernames via CORS-enabled requests without proper authentication enforcement.

## Attack scenario
1. Attacker identifies that the target site has CORS misconfiguration allowing requests from any origin
2. Attacker creates a malicious webpage containing JavaScript that makes XHR requests to the WordPress REST API /wp-json/wp/v2/users/ endpoint
3. Victim (authenticated admin user) visits the attacker's malicious webpage
4. The JavaScript sends a GET request with credentials (xhr.withCredentials = true) to the vulnerable endpoint
5. Due to CORS misconfiguration and lack of authentication checks on the endpoint, the API returns the full list of admin usernames
6. Attacker successfully exfiltrates sensitive admin user information for potential targeted attacks (password spraying, phishing, account takeover)

## Root cause
The WordPress REST API endpoint /wp-json/wp/v2/users/ lacks proper authentication and authorization checks, returning user data to any origin with CORS headers permitting cross-origin access. The endpoint should either: (1) require authentication, (2) implement strict CORS policies, or (3) restrict sensitive user data from unauthenticated requests.

## Attacker mindset
An attacker recognizes that admin usernames are valuable reconnaissance information for subsequent attacks. By exploiting CORS misconfiguration, they can passively harvest admin identities without direct interaction with the target, enabling targeted phishing, brute force, or social engineering campaigns. The attack requires minimal technical skill and can be weaponized at scale.

## Defensive takeaways
- Implement strict authentication/authorization on all REST API endpoints that expose sensitive data
- Review and restrict CORS policies to specific trusted origins; avoid wildcard (*) configurations for sensitive endpoints
- Disable the REST API for unauthenticated users or limit exposed endpoints using WordPress plugins/filters
- Exclude sensitive user information (usernames, email addresses, user IDs) from public API responses
- Implement rate limiting and IP-based access controls on admin-related endpoints
- Regular security audits of API configurations, especially inherited WordPress default settings
- Apply principle of least privilege: only expose necessary data to necessary consumers

## Variant hunting
Search for other WordPress REST API endpoints returning sensitive data without authentication (e.g., /wp-json/wp/v2/posts/, /wp-json/wp/v2/comments/). Test CORS headers on all API endpoints. Check custom plugins/themes for similar API implementations. Identify other CMS platforms (Drupal, Joomla) with default REST APIs having CORS misconfiguration. Test for username enumeration via registration endpoints and password reset functionality.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information
- T1566 - Phishing
- T1110 - Brute Force

## Notes
The vulnerability is particularly concerning because WordPress by default exposes /wp-json/wp/v2/users/ to unauthenticated requests. The PoC uses xhr.withCredentials = true, which would only send cookies if the endpoint returns appropriate CORS headers. This is a common misconfiguration in WordPress installations where administrators fail to restrict REST API access. The bounty amount is not disclosed in the writeup, suggesting this may have been a low-priority or duplicate report.

## Full report
<details><summary>Expand</summary>

hello,


the following endpoint https://lonestarcell.com/wp-json/wp/v2/users/ has an unsafe sharing of sensitive information of admin usernames

check poc script below :

```html
<html>
     <body>
         <h2>CORS PoC</h2>
         <div id="demo">
             <button type="button" onclick="cors()">Exploit</button>
         </div>
         <script>
             function cors() {
             var xhr = new XMLHttpRequest();
             xhr.onreadystatechange = function() {
                 if (this.readyState == 4 && this.status == 200) {
                 document.getElementById("demo").innerHTML = alert(this.responseText);
                 }
             };
              xhr.open("GET",
                       "https://lonestarcell.com/wp-json/wp/v2/users/", true);
             xhr.withCredentials = true;
             xhr.send();
             }
         </script>
     </body>
 </html>
```
If another domain is allowed by the policy, then that domain can potentially attack users of the application. If a user is logged in to the application, and visits a domain allowed by the policy, then any malicious content running on that domain can potentially retrieve content from the application, and sometimes carry out actions within the security context of the logged in user.
Even if an allowed domain is not overtly malicious in itself, security vulnerabilities within that domain could potentially be leveraged by an attacker to exploit the trust relationship and attack the application that allows access. CORS policies on pages containing sensitive information should be reviewed to determine whether it is appropriate for the application to trust both the intentions and security posture of any domains granted access.
Remediation
=====================
###Rest API should be visible just for logged admins .


best regards,

## Impact

References
=====================

###https://portswigger.net/research/exploiting-cors-misconfigurations-for-bitcoins-and-bounties

</details>

---
*Analysed by Claude on 2026-05-24*
