# Information Disclosure at lite.uber.com - Stack Trace Exposure and Internal Resource Exposure

## Metadata
- **Source:** HackerOne
- **Report:** 129712 | https://hackerone.com/reports/129712
- **Submitted:** 2016-04-10
- **Reporter:** kusl
- **Program:** Uber
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Information Disclosure, Stack Trace Exposure, Internal Resource Enumeration, Session Handling Error
- **CVEs:** None
- **Category:** web-api

## Summary
A reoccurrence of issue #128853 where the lite.uber.com OAuth callback endpoint leaks detailed Node.js stack traces containing sensitive internal error information, file paths, and session handling details. Additionally, internal Uber resources like JIRA are accessible and enumerable via API endpoints, exposing internal infrastructure and configuration details.

## Attack scenario
1. Attacker visits the OAuth authorization URL for lite.uber.com with specific scopes (profile, history, places, payment method access)
2. Attacker authenticates with valid credentials through login.uber.com
3. The OAuth callback to lite.uber.com fails during session deserialization when attempting to read alipayUser from session
4. Server returns HTTP 500 error with complete stack trace exposed in JSON response, revealing internal paths like /home/udocker/yellow-river/, module versions, and authentication flow details
5. Attacker uses information from stack trace to understand internal architecture and identify potential weak points in authentication middleware
6. Attacker attempts to enumerate internal Uber resources by accessing jira.uberinternal.com API endpoints and discovering additional internal infrastructure

## Root cause
Improper error handling in the alipay-user-session middleware that fails to gracefully handle session deserialization errors. The Express.js application is configured to expose raw stack traces in production error responses instead of logging them server-side and returning generic error messages to clients. Additionally, internal resources are not properly restricted from external access.

## Attacker mindset
An attacker seeks to understand Uber's internal infrastructure, authentication mechanisms, and platform architecture. By exploiting error pages, they can map internal services, identify third-party integrations (Alipay), discover internal hostnames and file paths, and potentially find authentication bypass opportunities. The discovery of accessible internal JIRA indicates weak access controls on internal tools.

## Defensive takeaways
- Implement proper error handling that logs detailed stack traces server-side only, returning generic error messages (e.g., 'An error occurred') to clients in production
- Use environment-based error response formatting - verbose errors in development, minimal in production
- Implement strict access controls on internal resources with IP whitelisting, VPN requirements, or strong authentication
- Configure web servers and reverse proxies to block access to internal domains from external networks
- Validate and sanitize all error responses before transmission to ensure no sensitive information (file paths, service names, internal IPs) is disclosed
- Implement API rate limiting and authentication for JIRA and other internal tools accessible via REST APIs
- Regular security testing to identify and remove previously patched vulnerabilities that may reappear after deployments
- Use a centralized logging system for error tracking separate from user-facing responses

## Variant hunting
Check other OAuth callback endpoints for similar stack trace exposure vulnerabilities
Scan other lite.uber.com subdomains and endpoints for unhandled error exposures
Test other Uber authentication flows (Google, Apple sign-in) for similar session handling issues
Enumerate other internal Uber subdomains (*.uberinternal.com) for API access
Check for similar information disclosure in staging/testing OAuth endpoints
Search for other middleware layers that deserialize session data without proper error handling
Test Alipay integration endpoints in other Uber products (UberEats, Uber Driver, etc.) for similar vulnerabilities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1592 - Gather Victim Host Information
- T1046 - Network Service Discovery
- T1526 - Enumerate External Targets
- T1087 - Account Discovery
- T1538 - Cloud Service Discovery

## Notes
This is a reoccurrence of previously reported issue #128853, indicating regression in security controls or incomplete remediation. The vulnerability combines stack trace information disclosure with internal resource enumeration. The attacker demonstrates awareness of Uber's internal infrastructure naming conventions (yellow-river being the codename for lite.uber.com backend). The mention of issue #114476 suggests this may be part of a pattern of internal resource exposure. The specific mention that 'You are not responsible for third-party products' suggests Uber may have attempted to dismiss the JIRA exposure as a third-party issue, but this is still an internal Uber resource that should not be externally accessible.

## Full report
<details><summary>Expand</summary>

Issue in #128853  occurs again.
1. go to https://login.uber.com/oauth/v2/authorize?response_type=code&redirect_uri=https%3A%2F%2Flite.uber.com%2Fauth%2Fcallback&scope=profile%20history%20places%20history_lite%20request_receipt%20request%20payment_baidu_wallet&client_id=y-JJyZ_RABnEwbJQq4VdQPORo4EKqv0j
2. Enter your login and password
3. You will redirect to lite.uber.com with trace from nodejs

`{"stack":"Session5xxErrorError: Session error - unable to read alipayUser from session\n    at createError (/home/udocker/yellow-river/node_modules/error/typed.js:31:22)\n    at middleware (alipay-user-session.js:22:17)\n    at Layer.handle [as handle_request] (/home/udocker/yellow-river/node_modules/express/lib/router/layer.js:95:5)\n    at next (/home/udocker/yellow-river/node_modules/express/lib/router/route.js:131:13)\n    at complete (/home/udocker/yellow-river/node_modules/passport/lib/middleware/authenticate.js:250:13)\n    at /home/udocker/yellow-river/node_modules/passport/lib/middleware/authenticate.js:257:15\n    at pass (/home/udocker/yellow-river/node_modules/passport/lib/authenticator.js:421:14)\n    at Authenticator.transformAuthInfo (/home/udocker/yellow-river/node_modules/passport/lib/authenticator.js:443:5)\n    at /home/udocker/yellow-river/node_modules/passport/lib/middleware/authenticate.js:254:22\n    at /home/udocker/yellow-river/node_modules/passport/lib/http/request.js:60:7\n    at pass (/home/udocker/yellow-river/node_modules/passport/lib/authenticator.js:267:43)\n    at serialized (/home/udocker/yellow-river/node_modules/passport/lib/authenticator.js:276:7)\n    at cb (auth.js:16:5)\n    at pass (/home/udocker/yellow-river/node_modules/passport/lib/authenticator.js:284:9)\n    at Authenticator.serializeUser (/home/udocker/yellow-river/node_modules/passport/lib/authenticator.js:289:5)\n    at IncomingMessage.req.login.req.logIn (/home/udocker/yellow-river/node_modules/passport/lib/http/request.js:50:29)\n    at UberOAuth2Strategy.strategy.success (/home/udocker/yellow-river/node_modules/passport/lib/middleware/authenticate.js:235:13)\n    at verified (/home/udocker/yellow-river/node_modules/passport-oauth2/lib/strategy.js:174:20)\n    at UberOAuth2Strategy.cb [as _verify] (auth.js:30:7)\n    at /home/udocker/yellow-river/node_modules/passport-oauth2/lib/strategy.js:190:24\n    at Request._callback (uber-oauth2.js:39:7)\n    at Request.self.callback (/home/udocker/yellow-river/node_modules/request/request.js:199:22)\n    at Request.emit (events.js:98:17)\n    at Request.<anonymous> (/home/udocker/yellow-river/node_modules/request/request.js:1036:10)\n    at Request.emit (events.js:117:20)\n    at IncomingMessage.<anonymous> (/home/udocker/yellow-river/node_modules/request/request.js:963:12)\n    at IncomingMessage.emit (events.js:117:20)\n    at _stream_readable.js:943:16\n    at process._tickDomainCallback (node.js:463:13)","type":"session.5xx.error","status":500,"message":"Session error - unable to read alipayUser from session","name":"Session5xxErrorError","fullType":"session.5xx.error"}` 

Error occurs when user want to connect YellowRiver app to his account with/without Alipay as payment method.

Files attached.

And one more thing:
You have some internal resources, which can be find easy. For example JIRA at 
jira.uber.com (with redirect to jira.uberinternal.com)
And by using API JIRA I can find something like this:
https://jira.uberinternal.com/rest/api/2/dashboard?maxResults=20&startAt=20

I think internal resources must be internal. You are not responsible for third-party products. But sometimes can be this #114476


</details>

---
*Analysed by Claude on 2026-05-24*
