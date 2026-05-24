# 1-click DOS in fastify-static via unhandled URL() exception and open redirect

## Metadata
- **Source:** HackerOne
- **Report:** 1361804 | https://hackerone.com/reports/1361804
- **Submitted:** 2021-10-06
- **Reporter:** drstrnegth
- **Program:** fastify-static (Fastify ecosystem)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Open Redirect, Improper Input Validation, Unhandled Exception
- **CVEs:** CVE-2021-22964
- **Category:** memory-binary

## Summary
fastify-static passes user-controlled request URLs directly to NodeJS URL() constructor without try-catch when redirect option is enabled, causing server crashes on malformed URLs. Additionally, the URL API's protocol-relative URL handling enables open redirect vulnerabilities even after adding exception handling.

## Attack scenario
1. Attacker sends HTTP GET request with malicious path like '//^/..' to fastify-static server mounted at root with redirect enabled
2. Request URL is extracted as req.raw.url without validation
3. Malformed URL is passed directly to new URL(req.raw.url) constructor
4. URL constructor throws TypeError for invalid syntax, unhandled exception crashes the process
5. Server becomes unavailable (DOS achieved)
6. Alternatively, attacker uses protocol-relative URL like '//a//youtube.com/%2e%2e%2f%2e%2e' which parses successfully but redirects to external domain due to URL API semantics

## Root cause
Missing input validation and exception handling before passing user-supplied req.raw.url to URL constructor. Additionally, reliance on URL() constructor's behavior with protocol-relative URLs without explicit base URL validation allows open redirect. The specification-compliant behavior of new URL('//foo.com', base) interprets double-slash as protocol-relative, enabling redirect to arbitrary domains.

## Attacker mindset
Simple denial of service exploitation requiring minimal effort - single malformed request crashes service. Open redirect secondary impact for credential theft or malware distribution. Attack surface accessible to unauthenticated remote users.

## Defensive takeaways
- Always wrap URL() constructor calls in try-catch blocks when parsing user input
- Validate and normalize request paths before processing - enforce single leading slash maximum
- Implement whitelist of allowed redirect destinations when implementing redirect functionality
- Explicitly provide base URL parameter to URL constructor to prevent protocol-relative URL interpretation
- Reject paths containing suspicious patterns (../, //, protocol indicators) before URL parsing
- Test redirect functionality with fuzzing inputs containing special characters and double slashes
- Monitor for repeated requests with malformed URLs as potential DOS attack pattern

## Variant hunting
Check for similar URL() usage in other Node.js web frameworks without try-catch
Search for redirect implementations using URLSearchParams or URL API without validation
Examine fastify plugins handling path traversal with insufficient sanitization
Look for other Fastify middleware processing req.raw.url directly to constructors
Audit Node.js applications using URL() for user-supplied protocol-relative URLs
Test express/koa static middleware with same path fuzzing payloads
Identify other redirect implementations vulnerable to protocol-relative URL bypass

## MITRE ATT&CK
- T1499.4
- T1190
- T1598.3
- T1657

## Notes
Reporter demonstrated both DOS impact and open redirect persistence after basic fix attempts. The core issue reveals a gap between specification-compliant URL API behavior and secure defaults - developers must explicitly prevent protocol-relative URL interpretation. The double-slash (//a//domain.com) syntax exploits URL constructor's RFC 3986 compliance where // indicates network-path reference. Fix requires both exception handling AND strict path validation before URL construction.

## Full report
<details><summary>Expand</summary>

## Summary:
When fastify-static is mounted at root and registered the option `{ redirect: true }` (default of redirect option is `false`), the following line directly feed user's input which is `req.raw.url` to URL API without try/catch: https://github.com/fastify/fastify-static/blob/master/index.js#L439. A remote attacker can send a GET request to server with path = `//^/..`, this will cause the URL API to throw error and eventually crash the server.

## Steps To Reproduce:

  1. Download `fastify-dos.zip`
  2. bash run.sh
  3. Open your terminal and run: `curl --path-as-is "http://localhost:3000//^/.."`
 
After that the server will crash and return error `TypeError [ERR_INVALID_URL]: Invalid URL: //^/..`.

## Fix proposal

You can add a try/catch to prevent crash. However, if you only fix by adding try/catch, attacker can still cause open redirect. 

 1. Run the server in my `fastify-dos.zip` again
 2. Use Google Chrome and navigate to `http://localhost:3000//a//youtube.com/%2e%2e%2f%2e%2e` (I tested on Chrome, Firefox, Safari, Opera, Edge, worked on all of them)
 3. You will see that you get redirected to `https://www.youtube.com/..%2F..`

I like the idea of fixing open redirect  by having a base URL = `http://localhost.com/` as second parameter in https://github.com/fastify/fastify-static/blob/master/index.js#L439. However, I looked up on MDN spec about the URL API and I got surprised when I saw the last example at: https://developer.mozilla.org/en-US/docs/Web/API/URL/URL#examples, which is `new URL("//foo.com", "https://example.com")    // => 'https://foo.com' (see relative URLs)`, this is the main reason why the open redirect bug is still persist.

To fix this bug, I think we can check leading slash of `req.raw.url`, and allow at most 1 leading slash `/` before attempt to redirect.

## Impact

- Denial of service
- Open redirect

</details>

---
*Analysed by Claude on 2026-05-24*
