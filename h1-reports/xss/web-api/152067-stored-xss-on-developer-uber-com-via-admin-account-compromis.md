# Stored XSS on developer.uber.com via Unauthorized Admin Account Compromise

## Metadata
- **Source:** HackerOne
- **Report:** 152067 | https://hackerone.com/reports/152067
- **Submitted:** 2016-07-18
- **Reporter:** albinowax
- **Program:** Uber
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Broken Access Control, Privilege Escalation, Stored Cross-Site Scripting (XSS), Insufficient Authorization Checks
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker could add themselves as an administrator to Uber's readme.io project powering developer.uber.com by sending a crafted API request with a non-existent invite ID. Once granted admin privileges, attackers could inject arbitrary JavaScript into documentation pages, leading to stored XSS attacks against all developer.uber.com visitors.

## Attack scenario
1. Attacker creates a normal account on readme.io and verifies their email
2. Attacker identifies Uber's readme.io project ID (578cd33dc27ce20e004e397b) from the public inactive page source
3. Attacker sends POST request to /api/accept-invite/ endpoint with a crafted invite token, using valid session cookies and CSRF token
4. API accepts the invite request despite the invite not existing, granting attacker admin privileges on Uber's project
5. Attacker logs into dash.readme.io and confirms admin access to the Uber project
6. Attacker injects malicious JavaScript into documentation pages to steal developer credentials or perform actions on behalf of users

## Root cause
The readme.io API endpoint /api/accept-invite/ fails to properly validate that the invite ID exists before granting administrator privileges. The authorization check is insufficient, allowing acceptance of non-existent invites. Additionally, the invite mechanism lacks proper validation to ensure only legitimate invitations can be accepted.

## Attacker mindset
An opportunistic attacker discovers that readme.io's access control is weak enough to bypass admin verification through simple API manipulation. They recognize that admin accounts have dangerous capabilities (arbitrary JavaScript injection) and leverage this to compromise a high-value target (Uber's developer documentation) that reaches many developers.

## Defensive takeaways
- Implement strict server-side validation for all invite acceptance requests, verifying the invite exists and belongs to the current user before granting access
- Enforce principle of least privilege - require explicit approval from existing admins before new admins are added to projects
- Add comprehensive audit logging for all administrative role assignments and privilege escalation events
- Implement rate limiting and anomaly detection on admin-related API endpoints
- Restrict admin capabilities to modify documentation, requiring code review or approval workflows for content changes
- Conduct regular security assessments of third-party documentation platforms and their access control models
- Implement Content Security Policy (CSP) headers to limit damage from stored XSS even if injected
- Monitor readme.io admin user lists for unauthorized additions and set up alerts

## Variant hunting
Test other readme.io API endpoints that modify permissions with invalid/non-existent IDs
Check if similar privilege escalation exists in other documentation platforms (GitBook, Confluence, etc.)
Investigate if team member invites have the same vulnerability
Test if expired or revoked invite tokens can still be accepted
Look for authorization bypass on other API operations that should require specific invite IDs
Check if the vulnerability affects other Uber documentation or infrastructure projects on readme.io

## MITRE ATT&CK
- T1190
- T1199
- T1548
- T1136
- T1098
- T1562

## Notes
This is a chained vulnerability combining broken access control with stored XSS. The critical aspect is that an unauthenticated attacker (or any readme.io user) could gain admin access to a high-profile documentation site. The readme.io platform appears to allow admins to inject arbitrary JavaScript, making this a severe supply-chain attack vector. The researcher responsibly removed their admin access after demonstrating the vulnerability.

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
*Analysed by Claude on 2026-05-12*
