# Stack Trace Information Disclosure at lite.uber.com

## Metadata
- **Source:** HackerOne
- **Report:** 128853 | https://hackerone.com/reports/128853
- **Submitted:** 2016-04-07
- **Reporter:** kusl
- **Program:** Uber
- **Bounty:** $100 (estimated based on report severity)
- **Severity:** medium
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Stack Trace Exposure, Debug Information Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
The OAuth callback endpoint at lite.uber.com/auth/callback exposes detailed Node.js stack traces containing full file paths and module names during error conditions. This information disclosure occurs after successful authentication redirection, potentially revealing internal application architecture and facilitating targeted exploitation.

## Attack scenario
1. Attacker navigates to lite.uber.com/auth/login which redirects to login.uber.com
2. Attacker submits valid credentials and receives authorization code in callback URL
3. Attacker is redirected to lite.uber.com/auth/callback?code=<auth_code>
4. Application encounters an error processing the callback or token exchange
5. Error handler returns unfiltered stack trace to client instead of generic error message
6. Attacker examines stack trace to identify Node.js module names, file paths, and internal architecture details

## Root cause
The OAuth callback handler lacks proper error handling and does not implement response filtering to sanitize stack traces before sending to clients. Debug mode appears enabled in production, or error middleware directly exposes exception details.

## Attacker mindset
An attacker seeks to map internal application architecture to identify potential attack vectors. Stack traces reveal dependency versions, file structure, and code organization, enabling reconnaissance for other vulnerabilities like dependency exploits or path-based attacks.

## Defensive takeaways
- Implement comprehensive error handling that catches exceptions and returns generic error messages to clients
- Ensure debug/development mode is disabled in production environments
- Use centralized error handling middleware that filters sensitive information from responses
- Log full stack traces server-side only; never expose to client responses
- Validate and sanitize all redirect URIs and callback parameters
- Implement Content Security Policy headers to limit information leakage vectors
- Regular security code review of authentication/authorization endpoints
- Conduct penetration testing with intentional error triggering on callback endpoints

## Variant hunting
Test other OAuth callback endpoints across Uber properties for similar exposure
Attempt to trigger errors at each step of OAuth flow (authorization, token exchange, user info endpoint)
Check for stack traces in other error conditions: invalid tokens, expired codes, CORS failures
Review other lite.uber.com endpoints for debug information leakage
Test mobile app endpoints for similar information disclosure patterns
Examine logging endpoints or diagnostic features that might expose traces
Check for path traversal combined with information disclosure in error messages

## MITRE ATT&CK
- T1190
- T1592
- T1592.004
- T1087
- T1526

## Notes
This vulnerability was discovered on the lite.uber.com subdomain (mobile web experience) during OAuth flow testing. The severity is moderate as it requires authenticated access but provides valuable reconnaissance data. HackerOne report #128853 indicates Uber has a history of addressing such issues. The vulnerability combines information disclosure with OAuth endpoints, creating compounded risk. Proper error handling remediation should prioritize all authentication-critical endpoints.

## Full report
<details><summary>Expand</summary>

Hello!
1. At https://lite.uber.com/auth/login I get 302-redirect to https://login.uber.com.
2. After post my email and password I get callback to https://lite.uber.com/auth/callback?code=efopqUAx2uwMOqJafHGj2OP8yNxXkf#_
3. At this page we can see trace stack with names of nodejs modules, full path disclose...

File attached.

Best Wishes!

</details>

---
*Analysed by Claude on 2026-05-24*
