# User Information Disclosure via WebSocket

## Metadata
- **Source:** HackerOne
- **Report:** 168223 | https://hackerone.com/reports/168223
- **Submitted:** 2016-09-14
- **Reporter:** archers123
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Improper Access Control, Sensitive Data Exposure
- **CVEs:** None
- **Category:** web-api

## Summary
User account information including user IDs was being transmitted to clients through WebSocket messages without proper access controls. An attacker monitoring WebSocket traffic could intercept sensitive user data including user IDs and names that should not be exposed to unauthorized parties.

## Attack scenario
1. Attacker establishes a connection to the application and monitors outgoing WebSocket frames
2. Attacker observes WebSocket message containing user profile data in JSON format
3. Message reveals user_id and username in plaintext within the WebSocket payload
4. Attacker correlates intercepted user IDs with other information to identify users
5. Attacker can map user IDs to cart paths and potentially access associated user data
6. Attacker uses discovered user IDs for account enumeration or targeted attacks

## Root cause
The application broadcasts user information through WebSocket messages without implementing proper access controls or data filtering. The API endpoint includes sensitive user identifiers in responses that are sent to all connected clients, violating the principle of least privilege.

## Attacker mindset
An attacker monitoring network traffic or WebSocket frames can passively collect user IDs and account information. This enables user enumeration attacks, account correlation across different sessions, and reconnaissance for targeted attacks against specific users.

## Defensive takeaways
- Implement strict access controls on WebSocket message handlers to ensure users only receive data they are authorized to access
- Filter sensitive fields (user_id, personal identifiers) from WebSocket responses unless explicitly required by the client
- Avoid sending user identifiers in WebSocket messages; use session-based references instead
- Encrypt WebSocket traffic using WSS (WebSocket Secure) to prevent packet sniffing
- Validate that users making requests have proper authorization for the specific resource being accessed
- Audit all WebSocket endpoints for unintended information disclosure
- Implement rate limiting on WebSocket connections to prevent enumeration attacks
- Log and monitor WebSocket data access patterns for suspicious activity

## Variant hunting
Check for user information disclosure in other WebSocket message types (presence, notifications, subscriptions)
Look for other API endpoints that may leak user identifiers in cart/order related paths
Test for user enumeration by monitoring WebSocket responses when accessing different user IDs
Examine real-time collaboration features (shared carts, live updates) for data exposure
Review WebSocket broadcast mechanisms for overly permissive data sharing

## MITRE ATT&CK
- T1592 - Gather Victim Identity Information
- T1590 - Gather Victim Network Information
- T1598 - Phishing for Information

## Notes
This is a classic case of insecure direct object references (IDOR) combined with information disclosure in a real-time communication channel. WebSocket implementations often have weaker security review compared to REST APIs. The severity may be higher if user IDs are used as primary keys for other sensitive operations. Report ID 168223 suggests this was a valid disclosure but bounty amount was not disclosed in the content provided.

## Full report
<details><summary>Expand</summary>

I noticed when monitoring the websocket requests that the account information of user, including user_id is sent to the client. 

__{"t":"d","d":{"r":8,"a":"p","b":{"p":"/carts/3671079_xjdJHqx88J435eDW5zxN/users/-KRbGN8R6uIjy6_OPx_j","d":{"id":25390626,"name":"Username}}}}__

</details>

---
*Analysed by Claude on 2026-05-24*
