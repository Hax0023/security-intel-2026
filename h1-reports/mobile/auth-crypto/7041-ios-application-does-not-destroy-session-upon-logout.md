# iOS Application Does Not Destroy Session Upon Logout

## Metadata
- **Source:** HackerOne
- **Report:** 7041 | https://hackerone.com/reports/7041
- **Submitted:** 2014-04-11
- **Reporter:** uname
- **Program:** IRCCloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Improper Session Management, Insufficient Session Invalidation, Authentication Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The iOS application fails to invalidate user sessions on the server side when users log out, allowing attackers to reuse captured session cookies for persistent unauthorized access. Although the logout request is processed successfully, the server does not invalidate the session token, leaving it valid for future API calls.

## Attack scenario
1. Attacker monitors network traffic or obtains a valid session cookie from a user's device (e.g., via packet sniffing, malware, or device compromise)
2. User logs out of the iOS application, which sends an apn-unregister request with the session identifier
3. Server responds with success but fails to invalidate the session token on the backend
4. Attacker uses the captured session cookie in subsequent HTTP requests to the API
5. Server accepts the request because the session token was never invalidated and remains valid in the session store
6. Attacker gains full account access, including ability to read messages, change settings, and perform actions as the legitimate user

## Root cause
The server's logout/apn-unregister endpoint does not implement proper session termination logic. While it processes the unregister request successfully, it fails to mark the session as invalid or remove it from the active sessions store, allowing the token to be reused indefinitely.

## Attacker mindset
An attacker would focus on session fixation and replay attacks. After obtaining a valid session cookie through network interception, device access, or application-level vulnerabilities, they recognize that the logout mechanism is ineffective and can maintain persistent access without needing to re-authenticate or perform additional attacks.

## Defensive takeaways
- Implement server-side session invalidation on logout that removes or marks the session as expired in the session store
- Use short-lived session tokens with refresh token rotation patterns
- Implement session binding to device identifiers or IP addresses to prevent token reuse across different contexts
- Clear all sensitive data associated with a session when invalidation occurs
- Implement server-side session timeout mechanisms independent of client-side logout
- Log all session termination events for audit and anomaly detection
- Use secure, HttpOnly, and SameSite flags on session cookies to prevent client-side access
- Implement server-side checks to verify session validity on every authenticated request
- Monitor for reuse of invalidated sessions and alert on suspicious patterns

## Variant hunting
Look for similar issues in: (1) Web applications with incomplete logout implementations where sessions aren't removed from backend stores; (2) APIs that accept session tokens without validating their status; (3) Mobile applications where client-side logout doesn't communicate session termination to server; (4) Applications using token-based auth (JWT) without blacklist/revocation mechanisms; (5) Systems where session IDs persist across authentication state changes

## MITRE ATT&CK
- T1190
- T1556
- T1111
- T1021

## Notes
This vulnerability is particularly dangerous in mobile applications where devices may be lost, stolen, or accessed by others. The persistent nature of the session token means a single compromise grants indefinite access. The request/response logs show the session ID is transmitted in both the Cookie header and request body, increasing exposure surface. The application appears to be IRCCloud (real-time communication platform), making unauthorized access especially sensitive due to access to private messages and conversations.

## Full report
<details><summary>Expand</summary>

After a user logs out of the iOS application, the server should be destroying the user's session. However, this is not occurring in the iOS application.

When the log out request is made, the following request and response is sent and received from the server:

REQUEST:

POST /apn-unregister HTTP/1.1
Host: www.irccloud.com
Proxy-Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate
Cookie: session=1.eaf395c450d6ad52023804d9846b7376
Accept-Language: en-us
Accept: */*
Content-Length: 117
Connection: keep-alive
User-Agent: IRCCloud/1.8 (iPhone; en; iPhone OS 6.1.6)

device_id=438a32983a261b01464b8c6cebf3630e8d0f5ca5cd004d973ebb40461ab890c9&session=1.eaf395c450d6ad52023804d9846b7376

device_id=438a32983a261b01464b8c6cebf3630e8d0f5ca5cd004d973ebb40461ab890c9&session=2.0b73bfd76e44eae93257c5c33d7c232c

RESPONSE:

HTTP/1.1 200 OK
X-Frame-Options: SAMEORIGIN
X-UA-Compatible: chrome=1
Strict-Transport-Security: max-age=31536000
server: Cowboy
date: Fri, 11 Apr 2014 05:29:54 GMT
content-length: 28
content-type: application/javascript

{"_reqid":0,"success":true}

The session identifer "1.eaf395c450d6ad52023804d9846b7376"  is not destroyed and can be re-used over an over again. If this cookie is captured or leaked, an attacker would have persistent access to a victim's account.




</details>

---
*Analysed by Claude on 2026-05-24*
