# HTTP Request Smuggling in pscp.tv and periscope.tv

## Metadata
- **Source:** HackerOne
- **Report:** 713285 | https://hackerone.com/reports/713285
- **Submitted:** 2019-10-13
- **Reporter:** protostar0
- **Program:** Twitter/Periscope (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length.Transfer-Encoding), Cache Poisoning, CSRF Bypass, Account Takeover, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
Multiple subdomains of pscp.tv and periscope.tv were vulnerable to HTTP request smuggling attacks via CL.TE discrepancies between frontend and backend servers. Attackers could exploit this to perform DoS attacks, bypass CSRF protections, inject malicious cookies, and poison victim requests to perform account takeover by linking victims' accounts to attacker-controlled OAuth providers.

## Attack scenario
1. Attacker identifies HTTP request smuggling vulnerability by sending specially crafted POST requests with mismatched Content-Length and Transfer-Encoding headers to detect 504 responses with delays (30-60 seconds)
2. Attacker crafts a POST request with Content-Length header specifying a length larger than actual body content, causing backend to wait for additional data
3. Frontend server processes and forwards the request while backend server buffers waiting for more data, creating a desynchronization window
4. Attacker appends a second request (GET or POST) without proper CRLF termination, causing it to be prepended to the next victim's legitimate request
5. Victim's request becomes poisoned by attacker's injected request, executing within victim's authenticated session context
6. Attacker modifies victim's account settings (e.g., description) or performs OAuth account linking with attacker's Google/Twitter accounts, achieving account takeover

## Root cause
Inconsistent parsing of HTTP headers between frontend and backend servers. Frontend server uses Content-Length while backend uses Transfer-Encoding, or different precedence rules when both headers present. This creates a window where requests can be smuggled into subsequent legitimate user requests.

## Attacker mindset
Reconnaissance-focused attacker who systematically tested multiple subdomains for request smuggling vulnerabilities. Careful exploitation methodology that avoided detection by targeting account metadata changes rather than attempting mass user impacts. Leveraged OAuth linking functionality as a high-impact exploitation vector for account takeover.

## Defensive takeaways
- Enforce consistent HTTP header parsing across all proxy, load balancer, and application server components
- Reject requests with both Content-Length and Transfer-Encoding headers, or enforce strict precedence rules
- Implement request validation to ensure Content-Length matches actual body size; reject mismatches
- Use HTTP/2 exclusively to eliminate ambiguous request boundaries inherent in HTTP/1.1
- Implement request logging and anomaly detection for unexpected 504 responses or delayed processing
- Add rate limiting and request deduplication mechanisms to detect smuggling attempts
- Require re-authentication for sensitive OAuth linking operations regardless of existing session
- Implement CSRF tokens that validate against request headers, not just POST parameters
- Conduct security testing specifically for request smuggling using automated tools against all public endpoints
- Monitor for unusual request patterns that could indicate smuggled requests prepended to legitimate traffic

## Variant hunting
Test TE.CL variants (backend uses Transfer-Encoding, frontend uses Content-Length)
Test TE.TE variants (both use Transfer-Encoding but parse it differently with obfuscation: 'Transfer-Encoding: chunked', 'Transfer-Encoding: x chunked', 'Transfer-Encoding: chunked\r\n Transfer-Encoding: chunked')
Test other subdomains and endpoints on pscp.tv and periscope.tv domains
Test HTTP/2 downstream compatibility with HTTP/1.1 upstreams
Test with different content-types and request methods
Test redirect chains that may involve multiple backend processing
Examine other Periscope/Twitter infrastructure for similar desynchronization patterns

## MITRE ATT&CK
- T1190
- T1598
- T1110
- T1021
- T1550
- T1556

## Notes
Report demonstrates three distinct exploitation variants with increasing impact: DoS detection, basic smuggling, and account takeover via request poisoning. Researcher responsibly noted challenges of testing on high-traffic live sites without impacting genuine users. Related report #704489 showed CSRF bypass and cookie injection impacts. Report references PortSwigger Web Security Academy as authoritative source for HTTP request smuggling fundamentals.

## Full report
<details><summary>Expand</summary>

**Description:** 
the Description of HTTP request smuggling attacks : [here](https://portswigger.net/web-security/request-smuggling)

seems that many subdomains in pscp.tv and periscope.tv vulenrable

##1-Detect HTTP request smuggling attack [504 response with delay (30 s, 60s)] "DoS"

POC & Steps To Reproduce: in this video F606648
Resource: [https://portswigger.net/web-security/request-smuggling/finding] 


##2- [exploit HTTP request smuggling attack ] send two request as one request get two response as one response [low impact]
POC & Steps To Reproduce & impact : in this video F606663
**ps:**
-add the two CRLFs in the end of the second request in GET REQUEST.
-use the valid value of content-length in POST REQUEST.

##3-[exploit HTTP request smuggling attack ]  poison the VICTIM request

POC & Steps To Reproduce & impact : in this video
inject a get request to the victim request F606689 
inject a get request to the victim request F606704 
**ps:**
-don't add the two CRLFs in the end of the second request in GET REQUEST.
-use large value in content-length then the length of request body in POST REQUEST.
Resource:
[exploit] (https://portswigger.net/web-security/request-smuggling/exploiting)

## important:
on a live site with a high volume of traffic like [www.pscp.tv] .it can be hard to prove request smuggling exists without exploiting numerous genuine users in the process.
-in the poc F606704  , i edit the victim request  to my post request `editing the description of my account` and ignore the real victim request. and the description  will change.

## Impact

1-dos
2-bypass csrf token & inject cookie  allow to link attacker account with [google,twitter] victim account
  report : https://hackerone.com/reports/704489
see other impact in 
https://portswigger.net/web-security/request-smuggling/exploiting

</details>

---
*Analysed by Claude on 2026-05-24*
