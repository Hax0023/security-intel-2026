# HTTP Request Smuggling via CL.TE on publishers.basicattentiontoken.org

## Metadata
- **Source:** HackerOne
- **Report:** 866382 | https://hackerone.com/reports/866382
- **Submitted:** 2020-05-05
- **Reporter:** dracomalfoy
- **Program:** Brave/Basic Attention Token
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length/Transfer-Encoding) Desynchronization, HTTP Protocol Confusion
- **CVEs:** None
- **Category:** uncategorised

## Summary
The publishers.basicattentiontoken.org endpoint is vulnerable to HTTP request smuggling attacks due to inconsistent interpretation of Content-Length and Transfer-Encoding headers between frontend and backend servers. An attacker can craft malformed requests to bypass validation, poison caches, and potentially perform session hijacking or privilege escalation.

## Attack scenario
1. Attacker crafts HTTP POST request with both Content-Length and Transfer-Encoding: chunked headers pointing to different message boundaries
2. Frontend proxy/load balancer parses request using Content-Length header, processing only the first 136 bytes as the POST body
3. Backend server parses the same request using Transfer-Encoding header, treating it as chunked and processing additional smuggled GET request
4. Attacker's smuggled GET request for static asset (.woff2) executes on backend without frontend validation awareness
5. Response to smuggled request gets cached or associated with victim session, enabling cache poisoning or session hijacking
6. Attacker repeats process with malicious payloads to escalate privileges or hijack authenticated sessions

## Root cause
Inconsistent HTTP request parsing between frontend and backend servers. Frontend uses Content-Length while backend uses Transfer-Encoding, creating a desynchronization window. The servers do not agree on request boundaries, allowing trailing data to be interpreted as a separate request by the backend only.

## Attacker mindset
Attacker identified infrastructure inconsistency during reconnaissance. They leveraged knowledge of HTTP specification ambiguities and proxy behavior differences to craft a request that bypasses frontend validation while reaching the backend. Used Burp Turbo Intruder to automate and test the attack.

## Defensive takeaways
- Normalize and validate HTTP requests before routing; reject requests with conflicting Content-Length and Transfer-Encoding headers
- Ensure frontend proxy and backend server use consistent request parsing logic (prefer Transfer-Encoding in modern implementations)
- Implement HTTP/2 or HTTP/3 which eliminate ambiguities in message framing
- Configure firewalls to strip or normalize dangerous header combinations
- Add request smuggling detection rules that flag CL.TE and TE.CL patterns
- Test infrastructure with HTTP request smuggling scanner tools (e.g., HTTP Request Smuggler Burp extension)
- Monitor cache for suspicious entries and implement cache key normalization
- Use WAF rules to detect and block request smuggling payloads

## Variant hunting
Search for other endpoints accepting POST requests with JSON payloads on Brave infrastructure. Test form submission endpoints, API gateways, and any publicly exposed registration/authentication flows. Attempt TE.CL variants and HTTP/2 specific smuggling techniques. Look for similar desynchronization on cached assets and API endpoints.

## MITRE ATT&CK
- T1190
- T1021
- T1556
- T1110
- T1557

## Notes
Reporter acknowledged this as first submission and provided clear reproduction steps with Burp intruder. Report lacks specific timeline and exact impact demonstration. No authenticated testing was performed, limiting impact assessment. The vulnerability has medium exploitability as it requires specific infrastructure misconfiguration but high impact due to potential cache poisoning and session hijacking implications. CWE-444 and CAPEC-33 references are accurate.

## Full report
<details><summary>Expand</summary>

When malformed or abnormal HTTP requests are interpreted by one or more entities in the data flow between the user and the web server, such as a proxy or firewall, they can be interpreted inconsistently, allowing the attacker to "smuggle" a request to one device without the other device being aware of it. 

 publishers.basicattentiontoken.org is vulnerable to CL TE ( Front end server uses Content-Length , Back-end Server uses Transfer-encoding ) HTTP request smuggling attack.

## Products affected: 

Brave Website. : publishers.basicattentiontoken.org

## Steps To Reproduce:
1.  Run the burp suite turbo intruder on the following request

```
POST /publishers/registrations.json HTTP/1.1
Host: publishers.basicattentiontoken.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://publishers.basicattentiontoken.org/sign-up
X-Requested-With: XMLHttpRequest
Content-Type: application/json
Origin: https://publishers.basicattentiontoken.org
Content-Length: 136
DNT: 1
Connection: close
Transfer-encoding: chunked

35
{"terms_of_service":true,"email":"dhfs@kdjfksd.dfks"}
00

GET /assets/muli/Muli-Bold-ecdc1a24a0a56f42da0ee128d4c2e35235ef86acfbf98aab933aeb9cc5813bed.woff2 HTTP/1.1
Host: publishers.basicattentiontoken.org
foo: x


```

2. Script for tubro Intruder is attached. Word list can be any list containing any characters.
3. Observe 200 OK response for the /publishers/registrations.json post request which is supposed to give {"message":"Unverified request"}. Please refer the attached screenshot ( Smuggle Request1.png ) whih contain the expected response. 
4. This successfully confirms vulnerability.Please refer attached screenshot ( Final Response.png ). A seprate report is attached as well.


Any suggestions or improvement in reports are welcome as this is my first report.

## Impact

It is possible to smuggle the request and disrupt the user experience. Session Hijacking, Privilege Escalation  and cache poisoning can be the impact of this vulnerability as well.
As unauthenticated testing is performed the exact impact of the vulnerability cannot be predicted.

For more information about the vulnerability please refer :
 https://cwe.mitre.org/data/definitions/444.html ;
  https://capec.mitre.org/data/definitions/33.html

</details>

---
*Analysed by Claude on 2026-05-24*
