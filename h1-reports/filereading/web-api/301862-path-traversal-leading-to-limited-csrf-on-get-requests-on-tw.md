# Path Traversal Leading to Limited CSRF on GET Requests via Confirmation and Password Reset Endpoints

## Metadata
- **Source:** HackerOne
- **Report:** 301862 | https://hackerone.com/reports/301862
- **Submitted:** 2018-01-02
- **Reporter:** kapytein
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Path Traversal, Cross-Site Request Forgery (CSRF), Server-Side Request Forgery (SSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
Two endpoints (/users/confirmation and /users/password/new) are vulnerable to path traversal through the confirmation_token and invitation_token parameters, allowing attackers to trigger arbitrary GET requests to internal resources. While CSRF protection via state parameters mitigates some attacks, the ability to make unauthorized requests to arbitrary paths could lead to information disclosure or unintended state changes.

## Attack scenario
1. Attacker crafts a malicious URL containing path traversal sequences in the invitation_token parameter (e.g., /../../test)
2. Attacker tricks victim into visiting the malicious URL or embeds it in a webpage
3. The victim's browser automatically sends the request with their authenticated session cookies
4. The vulnerable endpoint processes the path traversal payload and makes a request to the attacker-controlled path (e.g., /test.json)
5. Sensitive information or unintended actions may be exposed or triggered
6. If state parameter can be obtained, Slack authorization could be triggered leading to report leakage

## Root cause
Insufficient input validation and sanitization on the confirmation_token and invitation_token parameters. The application fails to strip or validate path traversal sequences (../) before using these parameters in redirect or request construction logic, allowing directory traversal attacks.

## Attacker mindset
An attacker would look for parameter manipulation opportunities in authentication flows, focusing on token parameters that might be used in URL construction. They would recognize that path traversal in GET parameters can bypass typical CSRF protections and potentially chain this with session hijacking or state parameter theft to escalate impact.

## Defensive takeaways
- Implement strict input validation on all token parameters - use whitelisting instead of blacklisting for allowed characters
- Canonicalize and validate all paths before use to prevent traversal sequences
- Apply CSRF tokens to all state-changing operations including GET requests that trigger side effects
- Use allowlists for redirect destinations and avoid accepting user-controlled redirect targets
- Implement proper URL encoding and parameter validation in redirect/request logic
- Regularly audit authentication and authorization endpoints as they are high-value targets
- Use security headers like X-Frame-Options and Content-Security-Policy to limit request exploitation

## Variant hunting
Check other endpoints accepting tokens or codes for similar path traversal issues
Look for similar patterns in password reset, email verification, and invitation flows across the platform
Test all parameters that might be used in redirect construction (redirect_uri, return_url, next, etc.)
Examine any endpoint that constructs URLs from user input for traversal vulnerabilities
Review API endpoints that might accept path parameters for traversal opportunities

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539

## Notes
This is a follow-up to report #99708 which identified similar CSRF issues. The path traversal aspect makes this particularly interesting as it combines two vulnerability classes. The practical impact is limited by state parameter requirements but demonstrates a chain that could have severe consequences if the state parameter is compromised. The ability to make GET requests to arbitrary paths (.json files) suggests potential information disclosure vectors.

## Full report
<details><summary>Expand</summary>

Hi team!

I've found more endpoints which are vulnerable to the limited CSRF stated in report https://hackerone.com/reports/99708. The endpoints cause a CSRF over GET requests, however, I've been unable to exploit it.

The following endpoints are vulnerable to this:

**Proof of Concept**

1. Visit https://hackerone.com/users/confirmation?confirmation_token=z2-aaa&invitation_token=/../../test or https://hackerone.com/users/password/new?invitation_token=/../../test (the two endpoints which are still vulnerable)
1. Inspect the network traffic via developer tools or an intercepting proxy, and notice a request being made to https://hackerone.com/test.json.

We can get HackerOne to authorize Slack within a team (as attempted to do so in report 99708), however due to the state parameter it will be hard to exploit that one unless an attacker is able to get the state parameter from the victim.

## Impact

As mentioned above, it will have a big impact on HackerOne if an attacker is able to get the state parameter of the victim to, as it would lead to reports being leaked.

</details>

---
*Analysed by Claude on 2026-05-24*
