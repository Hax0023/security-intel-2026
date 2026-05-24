# Unauthorized Access to Administration Pages via HTTP Response Status Code Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1806387 | https://hackerone.com/reports/1806387
- **Submitted:** 2022-12-15
- **Reporter:** qualw1n
- **Program:** U.S. Department of State (speakerkit.state.gov)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper Access Control, Client-Side Security Enforcement, HTTP Response Manipulation, Authentication Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker could bypass authentication and access unauthorized administration pages by manipulating HTTP 302 redirect responses to 200 OK status codes using Burp Suite. This allowed viewing of sensitive admin user information, normal user data, and performing unauthorized administrative operations such as file uploads and category management.

## Attack scenario
1. Attacker logs into https://speakerkit.state.gov/ and is redirected to the login page (spklogin) with a 302 Found response
2. Attacker intercepts traffic in Burp Suite and configures find-and-replace rules to change all 302 responses to 200 OK
3. When accessing admin-protected endpoints, the 302 redirect is converted to 200 OK, allowing the response body from the admin page to be rendered
4. Client-side application accepts the 200 status code and displays admin page content instead of enforcing the redirect
5. Attacker gains access to sensitive admin information including user credentials and account details
6. Attacker performs unauthorized administrative actions such as uploading files, adding categories, and managing user accounts

## Root cause
The application relies solely on HTTP response status codes (302 redirects) for access control enforcement on the client-side, with no server-side validation. When the status code is modified in transit, the security mechanism fails because the server does not validate that the client properly followed the redirect before processing subsequent requests.

## Attacker mindset
Low-skill opportunistic attacker leveraging readily available proxy tools (Burp Suite) to discover and exploit obvious client-side access control weaknesses. The attacker demonstrated methodical testing by comparing authenticated and unauthenticated responses to identify the vulnerability pattern.

## Defensive takeaways
- Implement server-side session validation and access control checks on every request, not relying on client-side redirect compliance
- Use proper authentication tokens/cookies with secure flags and validate them server-side before serving admin content
- Implement role-based access control (RBAC) enforcement at the server layer independent of HTTP status codes
- Never trust client-side response handling; enforce authorization logic on the server for all sensitive operations
- Use authentication frameworks that enforce server-side authorization gates before rendering protected content
- Implement security headers (X-Frame-Options, Content-Security-Policy) to prevent content display manipulation
- Conduct regular security code reviews focusing on authentication and authorization implementation
- Perform penetration testing specifically targeting HTTP response manipulation attacks

## Variant hunting
Test other redirect status codes (301, 303, 307, 308) with similar manipulation techniques
Attempt to modify other response headers that might trigger client-side security decisions
Test POST requests to admin endpoints to see if they can bypass authentication via status code manipulation
Check if other sensitive functionality (payment, data deletion) is similarly protected only client-side
Test for similar patterns in other state.gov subdomains that may share the same framework
Examine if response body content is conditionally included based on status codes rather than authentication state
Test for TOCTOU (Time-of-Check-Time-of-Use) vulnerabilities in the redirect mechanism

## MITRE ATT&CK
- T1190
- T1566
- T1199
- T1550
- T1078

## Notes
The vulnerability demonstrates a critical security anti-pattern where access control is implemented client-side and based solely on HTTP status codes. The fact that authenticated and unauthenticated users receive different response bodies for the same 302 status code indicates server-side content preparation without proper authorization gates. This is a textbook example of broken access control (OWASP A01:2021) affecting a government domain handling potentially sensitive speaker information.

## Full report
<details><summary>Expand</summary>

## Summary:
- I discovered an issue referred to as no-redirect in a subdomain on state.gov.
When you enter the page, it directs you directly to the entrance. When I examined it via burp suite, it gave 302 found, but the homepage data was showing below.
When I tried it as admin, it still gave 302 found, but this time we could see the content of the admin page.
this way i was able to see admin user and normal user's info.
I was also able to perform many transactions.
uploading files, adding categories and many more.

## Steps To Reproduce:
1- Login to https://speakerkit.state.gov/
- and it will throw you to the page named "spklogin". Using the find and replace feature on burpsuite, I told it to change all requests that gave 302 found to 200 Ok, and I easily performed my operations.
You will be able to do it when you watch the video.

## Supporting Material/References:
https://hackerone.com/reports/1026146
https://hackerone.com/reports/95441

  * [attachment / reference]

{F2078131}
{F2078132}
{F2078133}

* [ poc / video]
████████

## Impact

access the admin page. unauthorized.

</details>

---
*Analysed by Claude on 2026-05-24*
