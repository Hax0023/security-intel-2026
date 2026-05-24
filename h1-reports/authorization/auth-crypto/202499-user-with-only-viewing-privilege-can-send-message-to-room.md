# User with Only Viewing Privilege Can Send Messages to Chat Room via Direct POST Request

## Metadata
- **Source:** HackerOne
- **Report:** 202499 | https://hackerone.com/reports/202499
- **Submitted:** 2017-02-01
- **Reporter:** lucasveigaf
- **Program:** Phabricator
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Authorization Bypass, Access Control Weakness, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A user granted only viewing privilege on a chat room can send messages by directly crafting POST requests to the update endpoint, bypassing the UI-level authorization checks. The backend fails to validate that the user has message-sending permissions before processing the request.

## Attack scenario
1. Attacker creates or identifies a chat room and obtains viewing-only access through legitimate means
2. Attacker examines the legitimate POST request structure used by users with full privileges by analyzing network traffic or documentation
3. Attacker crafts a POST request to /conpherence/update/ endpoint with message content and required CSRF tokens
4. Attacker sends the malicious POST request with their viewing-only account credentials
5. Backend processes the request without validating the user's actual privilege level for the message action
6. Message appears in the chat room, effectively granting message-sending capability despite authorization restrictions

## Root cause
The backend authorization logic fails to enforce privilege checks at the API/endpoint level. The application relies on UI-level restrictions (hiding the message form) rather than implementing server-side permission validation. The /conpherence/update endpoint accepts message actions without verifying that the authenticated user has the required privilege level for that specific action.

## Attacker mindset
An attacker would recognize that UI-level protections are easily bypassed through direct HTTP requests. They would test whether the backend properly validates permissions and exploit this gap to exceed their assigned role. Motivation could range from disrupting communication to impersonating legitimate room members.

## Defensive takeaways
- Implement comprehensive server-side authorization checks for all API endpoints, not just UI elements
- Enforce permission validation at the action level before processing any state-changing operations
- Use a role-based access control (RBAC) matrix to explicitly define which actions are permitted for each privilege level
- Never trust client-side restrictions; validate all user actions against backend permission policies
- Add audit logging for privilege-based access attempts to detect unauthorized action patterns
- Implement consistent authorization middleware/interceptors across all endpoints to prevent inconsistent enforcement

## Variant hunting
Test other endpoints in the /conpherence/ path for similar authorization bypasses (edit, delete, modify room settings)
Attempt to perform privilege-escalation actions in other modules (tasks, documents, etc.) with minimal permissions
Check if users with no privilege at all can also send messages via the same POST endpoint
Test whether users can send messages to rooms they don't have any explicit privilege for
Examine if other state-changing actions (marking as read, editing metadata) are similarly vulnerable
Test with different CSRF token/session combinations to understand token validation scope

## MITRE ATT&CK
- T1190
- T1548
- T1550

## Notes
The reporter correctly notes this is more serious than 'low' severity in certain scenarios (e.g., confidential room disclosures, harassment vectors). The vulnerability is particularly dangerous because it's silent—no UI warning appears to indicate unauthorized message sending. Phabricator is an open-source collaboration platform used in security-sensitive environments, making this authorization bypass especially concerning.

## Full report
<details><summary>Expand</summary>

Hey, mongoose

When the owner of a chat room gives any user Viewing Privilege, that user can then send messages to the room. As expected, there's no form to send messages when the user access the room since in theory it shouldn't be possible. However, messages via POST requests can still be sent and processed.

The Severity of this issue is marked as low, but it still can be a serious problem depending on the scenario.

Steps to reproduce
====================

1. Create a new room
2. Give **only** Viewing Privilege to a user or all users
3. Send the following POST as the user with Viewing Privilege only
4. Refresh browser and see the message sent

```
POST /conpherence/update/1/ HTTP/1.1
Host: 192.168.25.10
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-Phabricator-Csrf: B@6uaixbh422c60ea95853fee4
X-Phabricator-Via: /
Content-Type: application/x-www-form-urlencoded
Content-Length: 110
Cookie: phsid=35yvcfc22xj27th6hwawazghx5cnritidfccxdhh; phusr=lucasveiga
Connection: close

__form__=1&action=message&text=TESTTEXT&latest_transaction_id=10&__wflow__=true&__ajax__=true&__metablock__=6
```

This isn't session related since logging in and out doesn't affect anything. Just replace "X-Phabricator-Csrf" and "phsid" with the new ones and the message still will be sent.

Let me know if you need further information. 

</details>

---
*Analysed by Claude on 2026-05-24*
