# Subdomain Takeover via Endpoint/Parameter Bypass at Unbounce Pages

## Metadata
- **Source:** HackerOne
- **Report:** 220002 | https://hackerone.com/reports/220002
- **Submitted:** 2017-04-10
- **Reporter:** ak1t4
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Improper Input Validation, Authorization Bypass, Domain Hijacking
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A researcher discovered a subdomain takeover vulnerability at info.hacker.one by bypassing a previous fix through a new endpoint and parameter combination in the Unbounce Pages application. By modifying the request to POST /[account-id]/pages/[page-id]/url with the injected parameter page%5Burl%5D, an attacker could reassign any branded domain to their controlled content. This vulnerability affected all branded domains under Unbounce and could be exploited for phishing, credential theft, and information stealing.

## Attack scenario
1. Attacker logs into their Unbounce account and creates a new page under any domain
2. Attacker initiates the 'Change URL' function through the normal UI workflow
3. Attacker intercepts the HTTP request using Burp Suite or similar proxy tool
4. Attacker modifies the request endpoint from standard URL to /[account-id]/pages/[page-id]/url and injects page%5Burl%5D=target-domain.com parameter
5. Attacker sends the crafted POST request, which updates the page to point to their target domain
6. Attacker hosts malicious content (fake login forms, phishing pages) on the hijacked subdomain to compromise users

## Root cause
The application failed to properly validate the domain assignment parameter across all endpoint variations. The previous fix (report #217358) only patched the standard endpoint, leaving an alternative endpoint /[account-id]/pages/[page-id]/url vulnerable to the same domain hijacking attack. Input validation and domain ownership verification were insufficient.

## Attacker mindset
The attacker demonstrated sophisticated understanding of web application security by analyzing a previous fix and intentionally searching for bypass techniques. They used request interception to identify alternative endpoints and parameter encodings that circumvented existing controls. This shows methodical vulnerability research and knowledge of common security testing workflows.

## Defensive takeaways
- Implement centralized domain ownership verification that applies to ALL endpoints handling domain assignment, not just primary ones
- Use allowlisting for domain changes rather than blacklisting; verify DNS records and ownership tokens before applying changes
- Implement comprehensive input validation that checks domain format, ownership, and prevents self-referential assignments across all API endpoints
- Apply consistent authorization checks at the application logic level, ensuring users can only modify domains they own
- Audit all endpoint variations that handle sensitive operations like domain management to identify incomplete patches
- Use security headers like CNAME validation to prevent subdomain hijacking at the DNS level
- Implement rate limiting on domain change operations to slow exploitation
- Add logging and alerting for domain reassignment attempts, especially to external domains

## Variant hunting
Hunt for similar bypasses by: (1) identifying all endpoints that handle domain/DNS operations; (2) testing alternative HTTP methods (PUT, PATCH, DELETE) on related endpoints; (3) fuzzing parameter variations using URL encoding, double encoding, and array syntax; (4) checking for alternative parameter names (domain, url, hostname, target, etc.); (5) testing different account ID formats and page ID variations; (6) examining other Unbounce features that interact with DNS/subdomains (email, redirects, CDN settings); (7) analyzing previous vulnerability patches to identify incomplete fixes

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information
- T1110 - Brute Force

## Notes
This is a chained vulnerability exploiting incomplete patching. The researcher responsibly disclosed a previous vulnerability (report #217358) and discovered the incomplete fix. The use of URL-encoded parameter names (page%5Burl%5D = page[url]) suggests Ruby on Rails framework conventions. The vulnerability affected multiple customers and branded domains, indicating widespread impact across the Unbounce platform. The PoC includes proper documentation with video evidence and clear reproduction steps, demonstrating professional vulnerability research practices.

## Full report
<details><summary>Expand</summary>

**Summary:**

Hi team, looking the last fix released from unbounce team at https://hackerone.com/reports/217358 i've been able to bypass it and takeover the subdomain info.hacker.one with a new vulnerable **ENDPOINT + PARAM COMBINATION** at UnbouncePages App

**Actual Dns Entry:**
{F174718}


### Reproduction Steps for HackerOne

1) I have claimed the domain and placed a new-page for PoC validation located under: 
Go to -> http://info.hacker.one/testing-new-takeover-04-10-17/
2) You see the alert box and the New Subdomain Takeover
{F174729}


**[ Unbounce Pages Team Section ]**

### Reproduction Steps PoC at new PARAM-ENPOINT COMBINATION

1) Login to account
2) Create a New Page under any domain or default domain (unbouncepages.com)
3) Go to "Change URL"
4) Fill with any input 
5) Intercept Request with burp or another proxy
6) Change Enpoint to ->  ```/[account-id]/pages/[page-id]/url ```
7) Add this param at the end of body ->  ``` &page%5Burl%5D=info.hacker.one/testing-new-takeover-04-10-17 ```

POST REQUEST

``` 
POST /2235922/pages/4d2a5d74-2119-4c68-8d93-f456566f2fe8/url/   HTTP/1.1
Host: app.unbounce.com
Connection: close
Content-Length: 186
X-NewRelic-ID: XQQAUl9ADAQFV1hW
Origin: https://app.unbounce.com
X-CSRF-Token: 7fHXoRIVY2kDTQxt+k6jjNgJagryJHBfu7MuZLtB7V4=
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept: */*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript
X-Requested-With: XMLHttpRequest
Referer: https://app.unbounce.com/2235922/pages/4d2a5d74-2119-4c68-8d93-f456566f2fe8
Accept-Encoding: gzip, deflate, br
Accept-Language: es-ES,es;q=0.8,fi;q=0.6,en;q=0.4
Cookie: ...

utf8=%E2%9C%93&_method=put&authenticity_token=7fHXoRIVY2kDTQxt%2Bk6jjNgJagryJHBfu7MuZLtB7V4%3D&page%5Bdomain%5D=unbouncepages.com&page%5Bpath%5D=testing-new-takeover-bypass-akita&button=&page%5Burl%5D=info.hacker.one/testing-new-takeover-04-10-17

``` 

**Vulnerable Endpoint: /[account-id]/pages/[page-id]/url**
**Vulnerable Injected PARAM: page%5Burl%5D=anydomain.com**

**This Request update the page with the New Domain (any domain could be used and creating content into it)**

I create a New Private Video PoC here for the above explained -> https://youtu.be/HKYMYkDDYW8

**(All branded domains under unbounce app are vulnerable)**

### Security Impact at H1:

*An attacker can utilize this domain info.hacker.one for targeting the organization by fake login hackerOne forms, or steal sensitive information of teams (credentials, credit card information, etc)

### Security impact at Unbounce Pages:

*An attacker can utilize this bug affecting all branded domains and customers at unbouncepages.com
and use all domains with evil purposes as stealing of sensitive information, credentials, credit card info, etc

Please let me know if more info needed or any help,

Best Regards,
@ak1t4

</details>

---
*Analysed by Claude on 2026-05-24*
