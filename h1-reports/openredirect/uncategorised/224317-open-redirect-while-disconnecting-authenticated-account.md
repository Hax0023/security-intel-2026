# Open Redirect on Account Disconnection Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 224317 | https://hackerone.com/reports/224317
- **Submitted:** 2017-04-27
- **Reporter:** gsecure
- **Program:** Weblate
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Open Redirect, Unvalidated Redirect
- **CVEs:** None
- **Category:** uncategorised

## Summary
An open redirect vulnerability exists in the account disconnection endpoint that allows attackers to redirect authenticated users to arbitrary external domains via the 'next' parameter. An attacker can craft a malicious URL and trick users into disconnecting their OAuth2 accounts while being redirected to a phishing or malicious site.

## Attack scenario
1. Attacker crafts a malicious URL containing the vulnerable disconnect endpoint with a 'next' parameter pointing to attacker-controlled domain
2. Attacker sends the URL to target user via phishing email, social engineering, or embedded link
3. Authenticated user clicks the link while logged into Weblate
4. User's browser navigates to the account disconnection endpoint
5. After successful disconnection, user is redirected to the attacker's domain (evil.com)
6. Attacker can then perform credential harvesting, malware distribution, or further social engineering on the victim

## Root cause
The 'next' parameter in the disconnect endpoint is not validated or sanitized before being used in a redirect. The application trusts user-supplied input without checking if the redirect destination is within the allowed domain whitelist.

## Attacker mindset
An attacker exploits the trust users place in legitimate Weblate URLs to redirect them to malicious sites during an account management action, increasing click-through rates and bypassing user suspicion since the initial domain is legitimate.

## Defensive takeaways
- Implement strict URL validation for all redirect parameters using whitelist-based approach
- Only allow redirects to relative URLs or explicitly whitelisted domains
- Use URLValidator with allowed_schemes and restrict to HTTPS only
- Validate that redirect URLs match the current domain or are in a pre-approved list
- Implement redirect parameter naming conventions (e.g., 'next_url') with dedicated validation functions
- Log all redirect attempts for security monitoring and audit trails
- Apply consistent redirect validation across all endpoints that use 'next' parameters

## Variant hunting
Check all endpoints with 'next', 'redirect', 'return_to', 'goto', 'url' parameters
Test other OAuth2 disconnect flows (Google, GitHub, Facebook, etc.)
Check login/logout endpoints for similar redirect vulnerabilities
Test parameter pollution: next=X&next=evil.com or double encoding
Verify if relative redirects with //evil.com bypass validation
Test if JavaScript protocol (javascript:) is accepted in redirect
Check post-authentication flows and invitation links for open redirects

## MITRE ATT&CK
- T1190
- T1598
- T1598.003

## Notes
This is a classic open redirect vulnerability commonly found in web applications. While lower severity than XSS or CSRF, it is frequently chained with phishing campaigns. The vulnerability is straightforward to exploit and impacts user trust. The demo.weblate.org endpoint suggests this was a public demonstration instance, making the vulnerability easily discoverable.

## Full report
<details><summary>Expand</summary>

Hi team, 
there is a open redirect end point when any account owner disconnect authenticated accounts say
google. He is redirected to some other domain.

Vulnerable URL
---
[demo.weblate.org/accounts/disconnect/google-oauth2/2335/?next=](demo.weblate.org/accounts/disconnect/google-oauth2/2335/?next=)

POC 
1. Go to authentication tab.
2. Disconnect Google account and capture the request.
3. Now, after next= write https://evil.com.
4. You are redirected to evil.com

video POC is attached.

Best Regards
Gurwinder

</details>

---
*Analysed by Claude on 2026-05-24*
