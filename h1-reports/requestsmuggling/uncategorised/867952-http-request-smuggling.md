# HTTP Request Smuggling (CL.TE) on console.helium.com

## Metadata
- **Source:** HackerOne
- **Report:** 867952 | https://hackerone.com/reports/867952
- **Submitted:** 2020-05-07
- **Reporter:** dracomalfoy
- **Program:** Helium
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length/Transfer-Encoding) Desynchronization, Protocol Confusion
- **CVEs:** None
- **Category:** uncategorised

## Summary
console.helium.com is vulnerable to HTTP request smuggling due to inconsistent parsing of Content-Length and Transfer-Encoding headers between frontend and backend servers. An attacker can craft malformed requests to smuggle arbitrary requests, bypassing authentication checks and potentially enabling session hijacking, cache poisoning, or privilege escalation attacks.

## Attack scenario
1. Attacker crafts an HTTP POST request to /api/sessions with both Content-Length and Transfer-Encoding headers
2. Frontend server interprets the request using Content-Length header, consuming only 109 bytes of the request body
3. Backend server interprets the same request using Transfer-Encoding: chunked, processing additional payload as part of the same request
4. The smuggled portion (GET / HTTP/1.1) is interpreted as a separate request by the backend
5. Attacker receives a 200 OK response instead of the expected 401 Unauthorized, confirming request smuggling
6. Attacker can leverage this to bypass authentication, poison caches, escalate privileges, or hijack sessions

## Root cause
Inconsistent HTTP request parsing between frontend and backend servers when both Content-Length and Transfer-Encoding headers are present. The frontend prioritizes Content-Length while the backend prioritizes Transfer-Encoding (chunked), causing request boundary desynchronization.

## Attacker mindset
An attacker recognizes that multi-layer architectures (proxy/firewall/backend) may parse HTTP specifications differently. By deliberately crafting ambiguous requests with conflicting length indicators, they can cause the frontend and backend to disagree on where one request ends and another begins, allowing injection of unintended requests that bypass security controls.

## Defensive takeaways
- Implement strict HTTP request validation: reject requests containing both Content-Length and Transfer-Encoding headers
- Ensure frontend and backend servers use identical HTTP parsing logic and request boundary detection
- Configure web servers to prioritize consistent header interpretation (e.g., disable Transfer-Encoding if Content-Length is present, or vice versa)
- Implement request smuggling detection and prevention at proxy/WAF level
- Use HTTP/2 or HTTP/3 which have stricter parsing requirements and prevent ambiguity
- Normalize requests at network boundary to strip conflicting headers
- Conduct regular security audits of the request handling pipeline across all tiers

## Variant hunting
Test TE.CL variants (backend uses Content-Length, frontend uses Transfer-Encoding)
Test TE.TE variants (both use Transfer-Encoding but parse it differently)
Test with obscured Transfer-Encoding headers (spaces, tabs, case variations)
Test with multiple Content-Length headers with conflicting values
Test with multiple Transfer-Encoding headers
Test against other endpoints (auth bypass, admin panels, sensitive APIs)
Test cache poisoning scenarios by smuggling requests that populate cache with malicious content
Test against different HTTP methods (PUT, PATCH, DELETE) for request smuggling

## MITRE ATT&CK
- T1190
- T1021
- T1548
- T1550
- T1021.001

## Notes
The report demonstrates practical exploitation using Burp Suite's Turbo Intruder tool with clear reproduction steps. The vulnerability is confirmed by the unexpected 200 OK response instead of 401 Unauthorized. While the exact impact on unauthenticated testing is noted as unpredictable, the potential for session hijacking, privilege escalation, and cache poisoning is significant. This is a classic HTTP request smuggling vulnerability requiring coordination between frontend and backend teams to remediate. The vulnerability likely affects users of the Helium console authentication mechanism.

## Full report
<details><summary>Expand</summary>

When malformed or abnormal HTTP requests are interpreted by one or more entities in the data flow between the user and the web server, such as a proxy or firewall, they can be interpreted inconsistently, allowing the attacker to "smuggle" a request to one device without the other device being aware of it. 

console.helium.com s vulnerable to CL TE ( Front end server uses Content-Length , Back-end Server uses Transfer-encoding ) HTTP request smuggling attack.

##Products affected:

Helium console Website. :  console.helium.com

##Steps To Reproduce:

1. Run the burp suite turbo intruder on the following request

```

POST /api/sessions HTTP/1.1
Host: console.helium.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://console.helium.com/login
Content-Type: application/json
Content-Length: 109
DNT: 1
Connection: close
Cookie: __cfduid=dc0212a0b1dcc0fe5853ef4e6b6d669ff1588840067; amplitude_id_2b23c37c10c54590bf3f2ba705df0be6helium.com=eyJkZXZpY2VJZCI6ImJmZDVjNzFmLWVhMWUtNDlmZi1hZGYyLTNlYWY3OTBjNmU3YlIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTU4ODg0MDA3NzA2MiwibGFzdEV2ZW50VGltZSI6MTU4ODg0MTg5MDk3NiwiZXZlbnRJZCI6NywiaWRlbnRpZnlJZCI6Miwic2VxdWVuY2VOdW1iZXIiOjl9
Transfer-Encoding: chunked

39
{"session":{"email":"fdsfsd@fgd.jk","password":"sdfsdf"}}
00

GET / HTTP/1.1
Host: www.helium.com
foo: x


```

2. Script for tubro Intruder is attached. Word list can be any list containing any characters.

3. Observe 200 Ok response for the /api/sessions post request which is supposed to give  401 Unauthorized   {"errors":{"error":["The email address or password you entered is not valid"]}} Please refer the attached screenshot ( Smuggle Request1.png ) which contain the expected response. 

4. This successfully confirms vulnerability.Please refer attached screenshot ( Final Response.png ). A recoding is attached as well.

Any suggestions or improvement in reports are welcome

## Impact

It is possible to smuggle the request and disrupt the user experience. Session Hijacking, Privilege Escalation and cache poisoning can be the impact of this vulnerability as well. Self-Xss can be escalated to XSS. It can be chained with other vulnerabilities to raise their severity.
As unauthenticated testing is performed the exact impact of the vulnerability cannot be predicted.

For more information about the vulnerability please refer :
https://cwe.mitre.org/data/definitions/444.html ;
https://capec.mitre.org/data/definitions/33.html

</details>

---
*Analysed by Claude on 2026-05-24*
