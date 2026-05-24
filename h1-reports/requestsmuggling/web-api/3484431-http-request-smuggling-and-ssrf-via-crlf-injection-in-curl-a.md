# HTTP Request Smuggling and SSRF via CRLF Injection in Curl_add_custom_headers

## Metadata
- **Source:** HackerOne
- **Report:** 3484431 | https://hackerone.com/reports/3484431
- **Submitted:** 2026-01-02
- **Reporter:** n12d11n
- **Program:** curl/libcurl
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, CRLF Injection, Server-Side Request Forgery (SSRF), Header Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A missing CRLF validation in libcurl's Curl_add_custom_headers function (lib/http.c:1761) allows attackers to inject arbitrary HTTP headers through carriage return and line feed characters. This violation of RFC 7230 §3.2.4 enables HTTP Request Smuggling attacks and potential SSRF bypass, with injected headers persisting across redirects.

## Attack scenario
1. Attacker crafts a malicious application or controls an API endpoint that uses libcurl to make requests
2. Attacker injects CRLF characters (\r\n or 0d 0a in hex) within custom header values passed to curl_easy_setopt()
3. libcurl transmits the unsanitized header bytes directly in the HTTP request without validation
4. Intermediate proxies, load balancers, or destination servers interpret the injected CRLF as a header terminator, treating subsequent data as new headers
5. Attacker leverages header injection to perform request smuggling, accessing unauthorized endpoints or bypassing SSRF filters
6. If redirects are enabled (-L flag), injected headers persist across multiple requests, amplifying the attack surface to internal services

## Root cause
The Curl_add_custom_headers function in lib/http.c:1761 lacks validation to reject carriage return (\r, 0x0d) and line feed (\n, 0x0a) characters in user-supplied header values. RFC 7230 Section 3.2.4 mandates that header field values must not contain bare CR or LF characters. The absence of a strchr-based validation check or sanitization allows these characters to pass through unmodified into the HTTP request stream.

## Attacker mindset
An attacker recognizes libcurl as a foundational library used across countless applications and servers. By injecting CRLF characters into custom headers, they can achieve request smuggling—a technique that exploits inconsistencies in how HTTP parsers handle ambiguous requests. This allows bypass of security controls, SSRF restrictions, and cache poisoning. The persistence of injected headers across redirects multiplies the attack surface, making it possible to target isolated internal services without direct network access.

## Defensive takeaways
- Validate all user-supplied HTTP header values to reject CR (0x0d) and LF (0x0a) characters before transmission
- Implement strict RFC 7230 compliance checks in HTTP header handling code
- Sanitize or reject custom headers containing control characters; consider using a whitelist of allowed characters
- Apply the same validation logic to all redirect chains to prevent header injection persistence
- Conduct security audits of HTTP library implementations, especially foundational libraries like libcurl used across multiple products
- Update libcurl to a patched version that implements CRLF validation in header functions
- Monitor and log suspicious header patterns (e.g., hex sequences 0d 0a within header values) in HTTP proxies and servers
- Consider disabling custom header functionality if not required, or implement application-level whitelist validation

## Variant hunting
Check for similar CRLF injection points in other HTTP header handling functions (e.g., User-Agent, Referer, Authorization)
Examine curl's handling of cookies and Set-Cookie headers for CRLF injection vectors
Investigate whether other HTTP libraries (wget, httplib, requests) have similar validation gaps
Look for CRLF injection in proxy headers, custom User-Agent strings, or other request metadata fields
Test whether injected headers bypass other security mechanisms (authentication headers, X-Forwarded-For, X-Real-IP)
Explore CRLF injection in the URL itself or in HTTP method specifications
Analyze if header injection can be used to craft cache-poisoning attacks on CDNs or proxies

## MITRE ATT&CK
- T1190
- T1557
- T1598
- T1584
- T1589

## Notes
The researcher explicitly disclosed use of AI assistance for initial code analysis but manually verified all findings via hex dumps and proxy simulations, demonstrating responsible disclosure practices. The vulnerability affects development versions (8.18.0-DEV) and stable releases (8.15.0), indicating broad exposure. The persistence of injected headers across redirects significantly increases practical exploitability. A suggested patch using strchr() to validate header content appears straightforward, but comprehensive testing across different HTTP servers and proxies is needed to confirm the fix prevents all request smuggling variants.

## Full report
<details><summary>Expand</summary>

## Summary:

A lack of CRLF validation in `Curl_add_custom_headers` at `lib/http.c:1761` allows users to inject arbitrary HTTP headers. This violation of RFC 7230 §3.2.4 leads to HTTP Request Smuggling and potential SSRF bypass. **AI Disclosure:** I utilized an AI assistant to aid in the initial code analysis and patch generation, but I have manually verified all claims using hex dumps and proxy simulations to ensure technical accuracy.

## Affected version

* **curl/libcurl version:** 8.18.0-DEV and 8.15.0
* **Platform:** Linux (Kali Linux)
* **curl -V output:** `curl 8.18.0-DEV (x86_64-pc-linux-gnu) libcurl/8.18.0-DEV OpenSSL/3.5.4`

## Steps To Reproduce:

1. Start a listener to capture raw traffic: `nc -l -p 8080 > raw_http.txt`.
2. Execute a `libcurl` application (or curl CLI) that appends a custom header containing CRLF: `curl -H "X-Injected: Value\r\nInjected-Header: Malicious" http://localhost:8080`.
3. Inspect the captured output: `hexdump -C raw_http.txt`.
4. Observe that the CRLF bytes (`0d 0a`) are transmitted unsanitized, causing the receiver to interpret the injected string as a separate, valid HTTP header.

## Supporting Material/References:

* **Hexdump Proof:** The hex dump shows `0d 0a` at offset `0x49`, confirming request splitting at the protocol level.
* **Suggested Patch:** A verification patch using `strchr` to reject `\r` and `\n` in `lib/http.c` successfully mitigates the issue.

---

## Impact

> The lack of CRLF validation in `libcurl`'s header handling allows for **HTTP Request Smuggling**, enabling an attacker to bypass security boundaries and perform **Server-Side Request Forgery (SSRF)**. As `libcurl` is a foundational library used by countless applications and backends, this vulnerability poses a systemic risk. Specifically, injected headers persist across redirects (`-L`), which significantly increases the attack surface and allows for the potential exposure of isolated internal services or cache poisoning.

---

</details>

---
*Analysed by Claude on 2026-05-24*
