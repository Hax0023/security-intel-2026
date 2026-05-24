# Subdomain Takeover #2 at info.hacker.one via Unbounce Pages Domain Parameter Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 209004 | https://hackerone.com/reports/209004
- **Submitted:** 2017-02-26
- **Reporter:** ak1t4
- **Program:** HackerOne / Unbounce Pages
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Mass Assignment / Parameter Pollution, Insufficient Input Validation, Authorization Bypass, Domain Hijacking
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A researcher discovered a second subdomain takeover vulnerability on info.hacker.one by bypassing the previous fix. The vulnerability exists in Unbounce Pages' page editing endpoint, which allows authenticated users to arbitrarily reassign any domain to their page through mass assignment of the page[domain] parameter. This enables complete control over the subdomain and creation of malicious content impersonating the organization.

## Attack scenario
1. Attacker authenticates to Unbounce Pages application with a legitimate account
2. Attacker creates a new page or edits an existing page and navigates to Edit Notes section
3. Attacker intercepts the PUT request to /[account-id]/pages/[page-id] using a proxy tool like Burp Suite
4. Attacker adds or modifies the page[domain] parameter in the request body to target a branded domain like info.hacker.one
5. Attacker submits the crafted request, causing the application to reassign the domain to their page without authorization checks
6. Attacker can now host arbitrary content on the subdomain, such as phishing pages for credential harvesting or fake login forms

## Root cause
The Unbounce Pages application fails to properly validate and authorize domain assignments in the page update endpoint. The vulnerability stems from: (1) insufficient input validation on the page[domain] parameter allowing any domain to be specified, (2) lack of authorization checks to verify the user owns or has permission to assign the target domain, and (3) mass assignment vulnerability where parameters passed in the request body directly map to domain model attributes without whitelisting.

## Attacker mindset
The attacker demonstrates persistence and technical depth by: analyzing the previous vulnerability fix to identify bypasses, recognizing the mass assignment weakness, using request interception to manipulate parameters, and understanding the business impact of domain takeover for credential harvesting and impersonation attacks. The attacker systematically validates the exploit and provides detailed reproduction steps and video proof of concept.

## Defensive takeaways
- Implement strict whitelist-based parameter filtering; only allow whitelisted parameters in API requests
- Add authorization checks to verify users own or have explicit permission to modify domain assignments before processing requests
- Validate that domain modifications are restricted to domains owned by the authenticated user's account
- Use explicit parameter binding instead of mass assignment; map only intended parameters
- Implement CSRF protection and verify authenticity tokens are properly validated
- Add audit logging for all domain assignment changes to detect suspicious activity
- Validate domain ownership through DNS verification or other mechanisms before allowing domain reassignment
- Apply principle of least privilege to API endpoints; ensure sensitive operations require explicit authorization
- Conduct security testing of previously patched vulnerabilities to identify bypass techniques
- Implement rate limiting on domain modification endpoints to slow down automated attacks

## Variant hunting
Security researchers should investigate: (1) other branded domain management endpoints in Unbounce that may suffer similar mass assignment flaws, (2) whether other page properties (subdomain, path, etc.) are similarly exploitable, (3) if unauthenticated users can trigger domain takeover, (4) whether bulk operations allow mass domain reassignment, (5) if historical domain claim records are properly validated, (6) whether other SaaS platforms using Unbounce as backend have similar issues, (7) if the vulnerability affects API clients differently than web interface, and (8) whether domain validation occurs server-side or relies on client-side checks.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1621 - Multi-Stage Channels
- T1566 - Phishing
- T1598 - Phishing for Information
- T1056 - Input Capture

## Notes
This is a follow-up to CVE/report #202767 showing that the initial fix was incomplete. The researcher effectively bypassed the previous patch by discovering an alternative vulnerable endpoint (page update endpoint vs. domain claim endpoint). The vulnerability has significant real-world impact given HackerOne's reputation and the potential for sophisticated phishing attacks. Unbounce's presence of 'all branded domains under unbounce app are vulnerable' indicates systemic architectural issues rather than isolated bugs. The researcher provided excellent documentation including video proof-of-concept and detailed reproduction steps with actual HTTP requests, demonstrating professional vulnerability research standards.

## Full report
<details><summary>Expand</summary>

**Summary:**

Hi team, looking the fix released from unbounce team at https://hackerone.com/reports/202767 i've been able to bypass it and takeover again the subdomain info.hacker.one with a new __Vulnerable-Endpoint__ at UnbouncePages App

**Actual Dns Entry:**

{F164154}

### Steps To Reproduce & New PoC for HackerOne

1) I have claimed the domain and placed a __new-page__ for PoC validation located under: 
Go to -> http://info.hacker.one/full-takeover/
2) You see the alert box and the subdomain takeover

{F164155}
{F164156}

-

#### [ Unbounce Pages Team Section ]

#### Reproduction Steps PoC at new __Vulnerable-Endpoint__ 

1) Login to account
2) Create a New Page under any domain
3) Go to "Edit Notes"
4) Fill with any input 
5) Intercept Request with burp or another proxy
6) Add this body params:
&page%5Bdescription%5D=test&page%5Bdomain%5D=__anydomain.com__
7) Refresh page - You see the New Claimed Domain at Url Page
{F164159}
{F164161}


[ POST REQUEST ]

POST /2235922/pages/01a8aadb-0198-4fa6-815d-1ae641f0b49e HTTP/1.1
Host: app.unbounce.com
Connection: close
Content-Length: 119
X-NewRelic-ID: XQQAUl9ADAQFV1hW
Origin: https://app.unbounce.com
X-CSRF-Token: 1FSc6oHzQZPfCrlSKHCSXqwyCRn5q7YxTbkva6wQ2oI=
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: */*
X-Requested-With: XMLHttpRequest
Referer: https://app.unbounce.com/2235922/pages/01a8aadb-0198-4fa6-815d-1ae641f0b49e
Accept-Encoding: gzip, deflate, br
Accept-Language: es-ES,es;q=0.8,fi;q=0.6,en;q=0.4
Cookie: ...

utf8=%E2%9C%93&_method=put&authenticity_token=1FSc6oHzQZPfCrlSKHCSXqwyCRn5q7YxTbkva6wQ2oI%3D&page%5Bdescription%5D=test&page%5Bdomain%5D=__anydomain.com__&page%5Bpath%5D=full-takeover


#### Enpoint vulnerable: /[account-id]/pages/[page-id] 
#### param vulnerable: page%5Bdomain%5D=anydomain.com
#### This Request update the page with the New Domain (any domain could be used and creating content into it)
#### All branded domains under unbounce app are vulnerable

I create a new Private Video PoC here for the above explained -> https://youtu.be/cRf3zkdngh0

#### Security Impact at H1:

*An attacker can utilize this domain info.hacker.one for targeting the organization by fake login hackerOne forms, or steal sensitive information of teams (credentials, credit card information, etc) 

#### Security impact at Unbounce Pages:

*An attacker can utilize this bug affecting all branded domains and customers at unbouncepages.com
and use all domains with evil purposes as stealing of sensitive information, credentials, credit card info, etc


Please let me know if more info needed or any help,

Best Regards,
@ak1t4




</details>

---
*Analysed by Claude on 2026-05-24*
