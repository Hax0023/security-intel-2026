# Stored XSS on developer.uber.com via Unauthorized Admin Account Compromise on readme.io

## Metadata
- **Source:** HackerOne
- **Report:** 152067 | https://hackerone.com/reports/152067
- **Submitted:** 2016-07-18
- **Reporter:** albinowax
- **Program:** Uber
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Broken Access Control, Privilege Escalation, Stored Cross-Site Scripting (XSS), Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker could add themselves as an administrator to Uber's readme.io documentation project (developer.uber.com) by exploiting an IDOR vulnerability in the invite acceptance endpoint, bypassing authorization checks. Once elevated to admin, the attacker could inject arbitrary JavaScript into documentation pages, resulting in stored XSS affecting all developers viewing the documentation.

## Attack scenario
1. Attacker identifies Uber's readme.io project ID (578cd33dc27ce20e004e397b) from the public inactive page source
2. Attacker creates a legitimate readme.io account and verifies email address
3. Attacker obtains an invite token/ID through reconnaissance or enumeration (e.g., 5617f98f7f74330d00dfd86d)
4. Attacker sends a POST request to accept-invite endpoint with the target invite ID and their XSRF token
5. Server fails to validate authorization and grants admin privileges despite invite not existing for the user
6. Attacker logs into dash.readme.io and injects malicious JavaScript into documentation pages viewed by developers

## Root cause
The readme.io accept-invite API endpoint (POST /api/accept-invite/{invite_id}) performs insufficient authorization validation. The server does not verify that the invite belongs to the authenticated user before granting admin privileges, allowing any authenticated user to accept arbitrary invites. Additionally, the endpoint returns a misleading 'Invite doesn't exist' message while silently granting access.

## Attacker mindset
An attacker recognizes that documentation platforms often lack proper access controls on invitation mechanisms. By chaining an IDOR vulnerability with admin privileges, they can compromise a high-visibility property (developer documentation) to conduct supply-chain attacks against Uber's developer ecosystem. The attacker demonstrates restraint by removing their access after proof-of-concept, indicating responsible disclosure mindset.

## Defensive takeaways
- Implement strict authorization checks on all invitation acceptance endpoints, verifying that the invite is bound to the authenticated user before granting access
- Use cryptographically secure, single-use invite tokens that cannot be enumerated or guessed
- Validate invite ownership and expiration status before processing acceptance
- Implement rate limiting and monitoring on privilege escalation endpoints
- Audit all admin capability changes and log who modified project memberships
- Apply principle of least privilege: third-party documentation platforms should have restricted capabilities
- Implement Content Security Policy (CSP) headers to mitigate stored XSS impact even if injection occurs
- Regular access control testing and IDOR vulnerability scanning on authentication-related endpoints

## Variant hunting
Test other readme.io endpoints for similar IDOR patterns in project management APIs
Check if other invite-related endpoints (cancel-invite, resend-invite) have similar validation gaps
Enumerate other Uber projects on readme.io that may have the same vulnerability
Test whether organization-level admin invites are subject to the same flaw
Check if the vulnerability applies to other documentation platforms Uber uses
Investigate if user enumeration is possible on readme.io through failed invite attempts
Test CSRF protection: does the vulnerability work without valid XSRF tokens

## MITRE ATT&CK
- T1190
- T1548
- T1078
- T1199
- T1566
- T1185

## Notes
This is a critical privilege escalation chain combining IDOR with broken access control. The writeup demonstrates good researcher ethics by removing admin access after proof-of-concept. The impact is amplified by the fact that admin users can inject arbitrary JavaScript by design, creating a stored XSS vulnerability affecting all downstream users. The vulnerability exploits the trust relationship between Uber and readme.io, making it a supply-chain risk vector.

## Full report
<details><summary>Expand</summary>

Hi,

Anyone can add themselves as an administrator on the readme.io uber project that powers developer.uber.com/documentation

To replicate this, first fetch https://uber.readme.io/inactiveand and grab Uber's project ID from the source: 578cd33dc27ce20e004e397b

Then, using this ID, create a normal account on readme.io, verify the email address, log in, and send the following HTTP request:

POST /api/accept-invite/5617f98f7f74330d00dfd86d HTTP/1.1
Host: dash.readme.io
Connection: close
Content-Length: 2
Accept: application/json, text/plain, */*
X-NewRelic-ID: XQEHWF5UGwYHXVlSDgY=
Origin: https://dash.readme.io
X-XSRF-TOKEN:<your token here>
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36
DNT: 1
Referer: https://dash.readme.io/
Accept-Encoding: gzip, deflate, br
Accept-Language: en-GB,en-US;q=0.8,en;q=0.6
Cookie: <your cookies here>


The server will respond with "Invite doesn't exist". However, if you go to dash.readme.io you will find that you can now access uber as an administrator. After logging in, I went straight to the users page, took a screenshot as evidence (attached) and removed myself as an administrator. 

Administrators are able to inject arbitrary JavaScript into documentation pages by design, so this could be used for a stored XSS attack on developer.uber.com to hijack developer accounts.


</details>

---
*Analysed by Claude on 2026-05-24*
