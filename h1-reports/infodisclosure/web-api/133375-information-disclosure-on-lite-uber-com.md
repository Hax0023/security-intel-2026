# Information Disclosure on lite.uber.com via Stack Trace Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 133375 | https://hackerone.com/reports/133375
- **Submitted:** 2016-04-21
- **Reporter:** kusl
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Stack Trace Exposure, Error-based Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The lite.uber.com authentication endpoint returns detailed stack traces in error responses, exposing sensitive system information including internal file paths, Node.js module names, and application architecture details. An unauthenticated attacker can trigger a 500 error by accessing the login endpoint, receiving a verbose JSON error response containing the complete call stack.

## Attack scenario
1. Attacker sends a GET request to https://lite.uber.com/auth/login without proper session cookies
2. Server encounters a session validation error (missing alipayUser in session)
3. Instead of returning a generic error page, server responds with HTTP 500 and detailed JSON error response
4. Error response includes full stack trace revealing internal paths like /home/udocker/yellow-river/
5. Attacker can map application structure, identify frameworks (Express, Passport), and node_modules versions
6. Information gathered can be used to identify potential vulnerabilities in known versions of dependencies

## Root cause
Error handling middleware configured to return verbose stack traces in production environment; missing or improperly configured global error handler that should sanitize error responses before sending to clients

## Attacker mindset
Reconnaissance-focused attacker mapping application architecture and dependencies to identify known CVEs or misconfigurations in specific library versions

## Defensive takeaways
- Implement global error handling middleware to catch exceptions and return generic error messages to clients
- Never expose stack traces, file paths, or internal architecture details in production error responses
- Configure separate error handling for development vs production environments
- Use environment variables to control error verbosity based on deployment context
- Log detailed errors server-side while returning minimal information to clients
- Implement proper session validation before attempting to access session data
- Regular security testing to identify and eliminate information disclosure vectors

## Variant hunting
Test other endpoints on lite.uber.com for similar stack trace exposure
Attempt to trigger errors on other Uber subdomains (api.uber.com, www.uber.com)
Try various HTTP methods (POST, PUT, DELETE) to see if error handling differs
Send malformed requests to authentication endpoints to trigger different error paths
Test with different Content-Type headers or payloads to trigger validation errors
Check historical patterns: if one endpoint exposes traces, other error handlers may also be misconfigured

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing for Information
- T1592 - Gather Victim Host Information

## Notes
Report demonstrates basic but effective information disclosure via error-based reconnaissance. The stack trace reveals application uses yellow-river (Uber's web framework), Express.js, Passport authentication, and express-session. File path /home/udocker/yellow-river/ suggests containerized deployment. This is a low-effort, high-value reconnaissance vector requiring no authentication or special payloads.

## Full report
<details><summary>Expand</summary>

Hello, according to your [policy] (https://hackerone.com/uber?view_policy=true), you are looking for Local File Disclosure. And lite.uber.com also in scope for your program.

request:
```
GET https://lite.uber.com/auth/login HTTP/1.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Connection: keep-alive
Cache-Control: max-age=0
Content-Length: 0
Host: lite.uber.com
```

answer:
```
HTTP/1.1 500 Internal Server Error
Server: nginx
Date: Thu, 21 Apr 2016 00:04:13 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 14792
Connection: keep-alive
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
ETag: W/"39c8-pwj5OPZu0zqTzGlt6yb/sQ"
Set-Cookie: yellow-river.sid=s%3AYpN9Bih6hDITIudKeIXlF4_PeWUzK6TH.w7fRURCOXvaHVUgiBgP4W3Peewlfw5ua%2F1BsIbg1lCM; Path=/; Expires=Fri, 21 Apr 2017 00:04:13 GMT; HttpOnly
Set-Cookie: yellow-river:sess=MJao-EO0ypYIEB2siVDmpg.YjvcBZ2bV-UhSujiVW6gkv0xkFABxOFBJONOP-jLR4gOR-i70PugOZ4QXKx-Bw87rp3zQ-KlzJbnRwGgsvfLPhcHW5Ie_ebcHHwGbqmRykiMQblEaS8SLU-zKFCuLXrR6VQhgeGFEc0Hq1Ff3DziEg.1461197053672.86400000.Z7p-NsRMyhcNU-OyvtfOEf5Xdaj3bkPktTZ0SSTJ4f4; path=/; expires=Fri, 22 Apr 2016 00:04:14 GMT; httponly
X-Uber-App: yellow-river
Strict-Transport-Security: max-age=0
X-Content-Type-Options: nosniff


{"stack":"Session5xxErrorError: Session error - unable to read alipayUser from session\n    at createError (/home/udocker/yellow-river/node_modules/error/typed.js:31:22)\n    at middleware (token.js:12:19)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/route.js:131:13)\n    at statsdRouteMiddleware (/home/udocker/yellow-river/node_modules/@uber/bedrock/lib/middleware/route-statsd.js:11:5)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/route.js:131:13)\n    at Route.dispatch (/home/udocker/yellow-river/node_modules/express/lib/router/route.js:112:3)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:277:22\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at exportLocalsMiddleware (export-locals.js:16:12)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:312:13)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:280:7\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at SessionStrategy.strategy.pass (/home/udocker/yellow-river/node_modules/passport/lib/middleware/authenticate.js:325:9)\n    at SessionStrategy.authenticate (/home/udocker/yellow-river/node_modules/passport/lib/strategies/session.js:71:10)\n    at attempt (/home/udocker/yellow-river/node_modules/passport/lib/middleware/authenticate.js:348:16)\n    at authenticate (/home/udocker/yellow-river/node_modules/passport/lib/middleware/authenticate.js:349:7)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:312:13)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:280:7\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at initialize (/home/udocker/yellow-river/node_modules/passport/lib/middleware/initialize.js:53:5)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:312:13)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:280:7\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at session (/home/udocker/yellow-river/node_modules/express-session/index.js:397:7)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:312:13)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:280:7\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at setUpRenderHelper (/home/udocker/yellow-river/node_modules/@uber/bedrock/lib/middleware/render.js:68:12)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:312:13)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:280:7\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at /home/udocker/yellow-river/node_modules/express-useragent/index.js:43:9\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:312:13)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:280:7\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at csrf (/home/udocker/yellow-river/node_modules/@uber/bedrock/lib/middleware/csrf.js:17:14)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:312:13)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:280:7\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at resLocals (/home/udocker/yellow-river/node_modules/@uber/bedrock/lib/middleware/locals.js:8:5)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:312:13)\n    at /home/udocker/yellow-river/node_modules/express/lib/router/index.js:280:7\n    at Function.process_params (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:330:12)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/index.js:271:10)\n    at proxyUrlMiddleware (/home/udocker/yellow-river/node_modules/@uber/bedrock/lib/middleware/proxy-url.js:18:5)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at trim_prefix (/home/udocker/yellow-river/node

</details>

---
*Analysed by Claude on 2026-05-24*
