# DOM-based Reflected XSS in rockstargames.com/newswire/tags via Cross-Domain AJAX with JSONP Callback Injection

## Metadata
- **Source:** HackerOne
- **Report:** 172843 | https://hackerone.com/reports/172843
- **Submitted:** 2016-09-29
- **Reporter:** zombiehelp54
- **Program:** Rockstar Games
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS) - DOM-based Reflected, Path Traversal, JSONP Callback Injection, Unsafe Dynamic Script Execution
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the /newswire/tags endpoint where user-supplied tags parameter values are passed to an AJAX request that fetches content from /newswire/tagContent/[tags_param]/1. When the response has application/javascript content-type, it is executed as JavaScript. An attacker can leverage path traversal encoding to redirect requests to JSONP endpoints with callback parameter injection to execute arbitrary JavaScript.

## Attack scenario
1. Attacker crafts a malicious URL with path traversal sequences encoded as %2e%2e to escape the /newswire/tagContent/ directory
2. Traversal payload reaches the /comments_dal/users/getGlobalLoginSettings.json JSONP endpoint
3. Attacker injects callback parameter (e.g., ?callback=alert(/xss/);//) into the traversed request
4. Server returns JSONP response wrapping user-controlled callback function with sensitive data
5. Response content-type is application/javascript, triggering automatic script execution in the browser
6. Attacker's JavaScript (alert(/xss/)) executes in victim's session context with access to session cookies and sensitive data

## Root cause
Multiple security flaws combine: (1) Insufficient input validation on tags parameter allowing path traversal via encoded dots (%2e%2e), (2) Unsafe concatenation of user input into request path without canonicalization, (3) Automatic execution of responses with application/javascript content-type, (4) Unprotected JSONP endpoint accepting arbitrary callback parameters without sanitization, (5) Missing same-origin policy enforcement for dynamic script loading from user-controlled paths

## Attacker mindset
Reconnaissance-focused attacker identifying that tags parameter flows into XHR requests and discovering the application respects JavaScript content-type. Through methodical endpoint enumeration, attacker finds an exploitable JSONP endpoint and realizes path traversal can redirect requests across the application. By chaining these weaknesses (traversal + JSONP callback injection), attacker achieves code execution while bypassing apparent restrictions on the tags endpoint.

## Defensive takeaways
- Implement strict input validation and whitelist allowed tag values; reject any input containing path traversal sequences or special characters
- Use path canonicalization to resolve and validate the final request path before execution
- Never automatically execute responses with application/javascript content-type based on user-controlled routing
- Disable or properly secure JSONP endpoints by validating callback parameter against strict whitelist of allowed function names
- Implement Content Security Policy (CSP) headers to restrict script sources and prevent inline script execution
- Use URL encoding/decoding consistently and validate at multiple layers; be aware attackers may double-encode or use alternative encodings
- Employ same-origin policy enforcement and CORS headers to restrict cross-domain requests
- Implement request signing or tokens for sensitive endpoints like user settings retrieval
- Log and monitor unusual path traversal attempts and JSONP callback injection patterns

## Variant hunting
Search for: (1) Other JSONP endpoints accepting unsanitized callback parameters across Rockstar Games domains, (2) Additional path traversal vulnerable endpoints that pass user input into dynamic request construction, (3) Other locations where application/javascript responses are automatically executed without origin validation, (4) Encoded traversal sequences (%2e, %252e, etc.) in parameters flowing to backend requests, (5) Callback parameter patterns in legacy APIs that may be similarly exploitable, (6) User input reflected in XHR requests to sensitive endpoints (settings, profile, authentication)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (initial vulnerability exploitation)
- T1012 - Query Registry/Reconnaissance (endpoint discovery and parameter mapping)
- T1601 - Modify System Image (potential data exfiltration via XSS)
- T1113 - Screen Capture (session hijacking via XSS context)

## Notes
This vulnerability demonstrates the danger of chaining multiple seemingly minor weaknesses: path traversal alone might be restricted, JSONP callback injection alone might be benign, but together they achieve RCE equivalent in browser context. The use of %2e%2e encoding suggests the application may have basic traversal filters checking for literal '..' but not encoded variants. The JSONP callback injection is a classic vulnerability pattern from earlier web frameworks before same-origin policy enforcement became standard. This attack would likely grant access to authentication tokens and session data.

## Full report
<details><summary>Expand</summary>

Hi,
I have found a reflected XSS issue in `http://www.rockstargames.com/newswire/tags` which is , IMO , somekinda tricky. 

#PoC:
- **URL:** `http://www.rockstargames.com/newswire/tags#/?tags=\%2e%2e\%2e%2e\%2e%2e\comments_dal\users\getGlobalLoginSettings%2ejson?callback=alert(%2fxss%2f);%2f%2f` 
- **Vulnerable Parameter:** `#/?tags=` 
- **Payload:** `\%2e%2e\%2e%2e\%2e%2e\comments_dal\users\getGlobalLoginSettings%2ejson?callback=alert(%2fxss%2f);%2f%2f`  

{F123778}

The value of the `tags` parameter is sent as an XHR request to `/newswire/tagContent/[tags_param]/1` and the response gets printed in the page , also I have found that if the `content-type` of the response is `application/javascript` , it gets executed as javascript. 
After digging for a while I found this endpoint `www.rockstargames.com/comments_dal/users/getGlobalLoginSettings.json` which returns a callback function in the response if the request is XHR. so I used the callback function to execute javascript through `?callback=alert(/xss/);//` 

Thanks!

</details>

---
*Analysed by Claude on 2026-05-12*
