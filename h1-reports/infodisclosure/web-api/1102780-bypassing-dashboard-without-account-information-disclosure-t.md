# Authentication Bypass via CRLF Injection and Information Disclosure through Exposed WebSocket

## Metadata
- **Source:** HackerOne
- **Report:** 1102780 | https://hackerone.com/reports/1102780
- **Submitted:** 2021-02-13
- **Reporter:** deb0con
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Authentication Bypass, CRLF Injection, Information Disclosure, Improper Access Control, Exposed WebSocket
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can bypass authentication on the Nextcloud support dashboard by injecting CRLF characters in the password reset URL parameter, allowing unauthenticated access to the dashboard panel. Additionally, exposed WebSocket endpoints leak sensitive information through the API without proper authorization checks.

## Attack scenario
1. Attacker navigates to the password reset functionality at https://support.nextcloud.com/#password_reset
2. Attacker crafts a malicious URL containing CRLF injection payload: //%0d%0aSet-Cookie:%20crlf-injection=mickeybrew//
3. The injected CRLF characters manipulate the HTTP response to inject a Set-Cookie header, bypassing authentication mechanisms
4. Attacker gains unauthenticated access to the dashboard panel without providing valid credentials
5. Attacker inspects network traffic and discovers the WebSocket endpoint at https://support.nextcloud.com/api/v1/signshow
6. Attacker connects to the unprotected WebSocket endpoint and retrieves sensitive information through information disclosure

## Root cause
The application fails to properly validate and sanitize URL parameters in the password reset functionality, allowing CRLF injection to manipulate HTTP headers. Additionally, WebSocket endpoints lack proper authentication and authorization validation, exposing sensitive data to unauthenticated clients.

## Attacker mindset
An attacker seeks to gain unauthorized administrative access to support infrastructure and exfiltrate sensitive information. The discovery of CRLF injection as an authentication bypass combined with exposed WebSocket APIs suggests reconnaissance to identify multiple attack vectors for maximum impact.

## Defensive takeaways
- Implement strict input validation and sanitization for all URL parameters, rejecting or encoding CRLF characters (%0d%0a)
- Apply proper authentication and authorization checks to all WebSocket connections before allowing data transmission
- Implement rate limiting and anomaly detection on authentication endpoints to detect bypass attempts
- Use security headers like X-Frame-Options, CSP, and X-Content-Type-Options to prevent header injection attacks
- Regularly audit API endpoints and WebSocket connections for exposed sensitive data
- Implement comprehensive logging and monitoring of authentication bypass attempts and unusual WebSocket connections

## Variant hunting
Search for similar CRLF injection points in other URL parameters (login, registration, profile). Investigate other WebSocket endpoints for missing authentication checks. Test for HTTP response splitting via various parameters that get reflected in headers.

## MITRE ATT&CK
- T1190
- T1566
- T1078
- T1040
- T1041

## Notes
The writeup lacks detailed proof-of-concept screenshots and specific vulnerable code. The WebSocket endpoint name 'signshow' suggests real-time signaling functionality. The vulnerability appears to affect a support domain rather than the main Nextcloud service, though the impact could still be significant depending on data stored in the support dashboard.

## Full report
<details><summary>Expand</summary>

**Sumarry :** 
I found a information disclosure for bypassing parameter url attacker can redirect to dashboard without login user/pass page
and websocket can be exposed in response/dashboard.

**URL Effected**
https://support.nextcloud.com/#password_reset

### Steps To Reproduce:
  * Opened directory at https://support.nextcloud.com/#password_reset
  * Forget-password  and repeat url to burp-suite
  * In directory added a parameter bypass is ``//%0d%0aSet-Cookie:%20crlf-injection=mickeybrew//``
  * and look a responsive , you can be redirect to dashboard panel without user/pass
  * Show the ``network-browser`` and you can found api directory and websocket
  * Directory websocket is https://support.nextcloud.com/api/v1/signshow
  * Opened it and **Boom** You can see Information disclosure through websocket

**Request**
```
GET #password_reset/%0d%0aSet-Cookie:%20crlf-injection=mickey HTTP/1.1
Host: support.nextcloud.com
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Length: 91
```
 ### Screenshots POC
█████
██████
███████
███

## Impact

It may cause the attacker to log into the dashboard page without logging in via user/pass, and the attacker finds sensitive files on open fires.

</details>

---
*Analysed by Claude on 2026-05-24*
